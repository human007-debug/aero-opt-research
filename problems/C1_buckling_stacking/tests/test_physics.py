"""Physics checks against textbook closed forms (independent of the benchmark)."""
import copy

import numpy as np
import pytest

from core.problem import load_config
from problems.C1_buckling_stacking import evaluator as ev

PID = "C1_buckling_stacking"
evaluate = ev.evaluate


@pytest.fixture
def cfg():
    c = copy.deepcopy(load_config(PID))
    c["load_cases"]["uniaxial"] = [[1.0e4, 0.0]]
    c["loads"]["case"] = "uniaxial"
    c["constraints"]["strength"]["enabled"] = False
    return c


def test_isotropic_plate_matches_kirchhoff_D():
    E, nu, t = 70e9, 0.3, 1e-3
    Q = ev.reduced_stiffness(E, E, E / (2 * (1 + nu)), nu)
    _, _, D = ev.abd_matrices([0, 45, 90, 90, 45, 0], Q, t / 6)
    Dk = E * t**3 / (12 * (1 - nu**2))
    np.testing.assert_allclose(D[0, 0], Dk, rtol=1e-12)
    np.testing.assert_allclose(D[1, 1], Dk, rtol=1e-12)
    np.testing.assert_allclose(D[0, 1], nu * Dk, rtol=1e-12)
    np.testing.assert_allclose(D[2, 2], (1 - nu) / 2 * Dk, rtol=1e-12)


def test_isotropic_square_plate_uniaxial_k_equals_4():
    # Classical result: N_cr = 4 pi^2 D / b^2 for a square SS plate in uniaxial compression.
    E, nu, t, b = 70e9, 0.3, 1e-3, 0.5
    Q = ev.reduced_stiffness(E, E, E / (2 * (1 + nu)), nu)
    _, _, D = ev.abd_matrices([0, 0], Q, t / 2)
    lam, mode = ev.buckling_load_factor(D, b, b, Nx=1.0, Ny=0.0)
    Dk = E * t**3 / (12 * (1 - nu**2))
    np.testing.assert_allclose(lam, 4 * np.pi**2 * Dk / b**2, rtol=1e-12)
    assert mode == (1, 1)


def test_isotropic_long_plate_mode_count():
    # For a/b = 3 the uniaxial minimum is at m = 3 half-waves, k = 4.
    E, nu, t, b = 70e9, 0.3, 1e-3, 0.2
    Q = ev.reduced_stiffness(E, E, E / (2 * (1 + nu)), nu)
    _, _, D = ev.abd_matrices([0], Q, t)
    lam, mode = ev.buckling_load_factor(D, 3 * b, b, Nx=1.0, Ny=0.0)
    np.testing.assert_allclose(lam, 4 * np.pi**2 * D[0, 0] / b**2, rtol=1e-12)
    assert mode == (3, 1)


def test_load_factor_scales_inversely_with_load(cfg):
    design = [1, 0, 2] * 4
    r1 = evaluate(design, cfg)
    cfg["load_cases"]["uniaxial"] = [[2.0e4, 0.0]]
    r2 = evaluate(design, cfg)
    np.testing.assert_allclose(r1.metadata["lambda_cr"], 2 * r2.metadata["lambda_cr"], rtol=1e-12)


def test_symmetric_balanced_by_construction(cfg):
    rng = np.random.default_rng(0)
    alpha = cfg["design"]["stack_alphabet"]
    Q = ev.reduced_stiffness(*(cfg["material"][k] for k in ("E1", "E2", "G12", "nu12")))
    for _ in range(50):
        genes = rng.integers(0, 3, 12)
        A, B, _ = ev.abd_matrices(ev.decode(genes, alpha), Q, cfg["material"]["ply_thickness"])
        assert np.abs(B).max() < 1e-9 * A[0, 0] * cfg["material"]["ply_thickness"]
        assert abs(A[0, 2]) < 1e-9 * A[0, 0] and abs(A[1, 2]) < 1e-9 * A[0, 0]


def test_A_matrix_independent_of_stacking_order(cfg):
    alpha = cfg["design"]["stack_alphabet"]
    Q = ev.reduced_stiffness(*(cfg["material"][k] for k in ("E1", "E2", "G12", "nu12")))
    t = cfg["material"]["ply_thickness"]
    A1, _, D1 = ev.abd_matrices(ev.decode([0, 1, 2, 1], alpha), Q, t)
    A2, _, D2 = ev.abd_matrices(ev.decode([2, 1, 1, 0], alpha), Q, t)
    np.testing.assert_allclose(A1, A2, rtol=1e-12, atol=1e-12 * A1[0, 0])
    assert not np.allclose(D1, D2)


def test_outer_zero_plies_maximise_D11(cfg):
    alpha = cfg["design"]["stack_alphabet"]
    Q = ev.reduced_stiffness(*(cfg["material"][k] for k in ("E1", "E2", "G12", "nu12")))
    t = cfg["material"]["ply_thickness"]
    _, _, Dout = ev.abd_matrices(ev.decode([0, 2, 2, 2], alpha), Q, t)
    _, _, Din = ev.abd_matrices(ev.decode([2, 2, 2, 0], alpha), Q, t)
    assert Dout[0, 0] > Din[0, 0]


@pytest.mark.parametrize("angles,mode,expected", [
    ([0, 0, 45, -45, 90, 90], "ply", 2),
    ([0, 0, 0, 0, 0, 90], "ply", 5),
    ([45, -45, 45, -45], "ply", 1),
    ([45, -45, 45, -45], "abs", 4),
])
def test_max_contiguous(angles, mode, expected):
    assert ev.max_contiguous(angles, mode) == expected


def test_contiguity_counts_across_midplane(cfg):
    # Two 90_2 stacks at the mid-plane become 8 contiguous 90 plies in the full laminate.
    r = evaluate([1] * 10 + [2, 2], cfg)
    assert r.metadata["max_contiguous_run"] == 8
    assert not r.feasible


def test_deterministic(cfg):
    design = [1, 0, 1, 2, 1, 0, 1, 2, 1, 0, 1, 2]
    assert evaluate(design, cfg).to_dict() == evaluate(design, cfg).to_dict()


def test_multiple_load_sets_take_the_minimum(cfg):
    design = [1, 0, 1, 2, 1, 0, 1, 2, 1, 0, 1, 2]
    cfg["load_cases"]["a"], cfg["load_cases"]["b"] = [[1.0e4, 0.0]], [[0.0, 1.0e4]]
    cfg["load_cases"]["ab"] = [[1.0e4, 0.0], [0.0, 1.0e4]]
    lam = {}
    for k in ("a", "b", "ab"):
        cfg["loads"]["case"] = k
        lam[k] = evaluate(design, cfg).metadata["lambda_cr"]
    assert lam["ab"] == pytest.approx(min(lam["a"], lam["b"]))


def test_strain_load_factor_scales_with_thickness():
    # Max-strain lambda is linear in laminate thickness for the same proportions (1995 paper, p.153).
    c = copy.deepcopy(load_config(PID))
    r1 = evaluate([1, 0, 2] * 4, c)
    c["design"]["n_plies_total"] = 96
    r2 = evaluate([1, 0, 2] * 8, c)
    assert r2.metadata["lambda_strength"] == pytest.approx(2 * r1.metadata["lambda_strength"], rel=1e-10)


def test_yaml_numeric_fields_parse_as_numbers():
    # PyYAML (YAML 1.1) reads `1.0e9` without an exponent sign as a string.
    c = load_config(PID)
    for k in ("E1", "E2", "G12", "nu12", "ply_thickness"):
        assert isinstance(c["material"][k], float), k
    for k in ("a", "b"):
        assert isinstance(c["plate"][k], float), k
