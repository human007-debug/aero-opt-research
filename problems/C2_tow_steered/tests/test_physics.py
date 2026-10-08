"""C2 checks that need no benchmark data: closed forms, equilibrium, symmetry, convergence."""
import copy

import numpy as np
import pytest

from core.problem import load_config
from problems.C1_buckling_stacking.evaluator import buckling_load_factor
from problems.C2_tow_steered import evaluator as ev

PID = "C2_tow_steered"
VAT = [(60.0, 30.0), (0.0, 45.0), (45.0, 0.0)]


@pytest.fixture
def cfg():
    return copy.deepcopy(load_config(PID))


@pytest.mark.parametrize("theta", [0.0, 90.0])
def test_straight_fibres_match_closed_form(cfg, theta):
    # D16 = D26 = 0 for 0 and 90 degree plies, so the closed form is exact.
    r = ev.analyse(theta, theta, cfg)
    A, D = r["A"][0, 0], r["D"][0, 0]
    a, b = cfg["plate"]["a"], cfg["plate"]["b"]
    Nx = (A[0, 0] - A[0, 1] ** 2 / A[1, 1]) / a  # free transverse edges, unit end-shortening
    lam, _ = buckling_load_factor(D, a, b, Nx, 0.0)
    assert r["lambda"] == pytest.approx(lam, rel=1e-10)


def test_isotropic_square_plate_k_equals_4(cfg):
    E, nu = 70e9, 0.3
    cfg["material"].update(E1=E, E2=E, G12=E / (2 * (1 + nu)), nu12=nu)
    r = ev.analyse(20.0, 70.0, cfg)  # angles are irrelevant for an isotropic material
    t = 4 * cfg["layup"]["n_layer_pairs_half"] * cfg["material"]["ply_thickness"]
    Dk = E * t**3 / (12 * (1 - nu**2))
    b = cfg["plate"]["b"]
    assert r["buckling_load"] == pytest.approx(4 * np.pi**2 * Dk / b**2 * b, rel=1e-10)


def test_straight_fibre_prebuckling_is_uniform(cfg):
    r = ev.analyse(30.0, 30.0, cfg)
    A, a = r["A"][0, 0], cfg["plate"]["a"]
    Nx = -(A[0, 0] - A[0, 1] ** 2 / A[1, 1]) / a
    np.testing.assert_allclose(r["N"][..., 0], Nx, rtol=1e-10)
    np.testing.assert_allclose(r["N"][..., 1:], 0.0, atol=1e-10 * abs(Nx))


@pytest.mark.parametrize("axis", ["x", "y"])
@pytest.mark.parametrize("T", VAT)
def test_section_force_equilibrium(cfg, axis, T):
    # Ritz satisfies equilibrium weakly; with the quarter-plate basis the error falls spectrally.
    cfg["layup"]["variation_axis"] = axis
    cfg["discretisation"]["prebuckling_legendre_degree"] = 18
    assert ev.analyse(*T, cfg)["section_force_spread"] < 1e-10


@pytest.mark.parametrize("axis", ["x", "y"])
def test_traction_free_transverse_edges(cfg, axis):
    # Weak (Ritz) boundary condition: Ny at the outermost Gauss row is small relative to Nx.
    cfg["layup"]["variation_axis"] = axis
    N = ev.analyse(60.0, 30.0, cfg)["N"]
    assert np.abs(N[:, -1, 1]).max() < 0.02 * np.abs(N[..., 0]).max()


@pytest.mark.parametrize("T", VAT)
def test_mirror_symmetry_of_angles(cfg, T):
    p1 = ev.analyse(*T, cfg)["buckling_load"]
    p2 = ev.analyse(-T[0], -T[1], cfg)["buckling_load"]
    assert p1 == pytest.approx(p2, rel=1e-10)


def test_curved_fibres_change_load_distribution(cfg):
    # y-variation, stiffer (near-0 deg) edges: the edges carry more axial load than the centre.
    cfg["layup"].update(variation_axis="y", phi=0.0)
    N = ev.analyse(60.0, 0.0, cfg)["N"][..., 0]
    nq = N.shape[1]
    assert abs(N[nq // 2, -1]) > 2 * abs(N[nq // 2, nq // 2])


def test_ritz_buckling_is_upper_bound_in_M(cfg):
    loads = []
    for M in (4, 6, 8, 10, 12):
        cfg["discretisation"]["buckling_sine_terms"] = M
        loads.append(ev.analyse(60.0, 30.0, cfg)["buckling_load"])
    assert all(l2 <= l1 * (1 + 1e-9) for l1, l2 in zip(loads, loads[1:]))


def test_default_discretisation_converged(cfg):
    base = ev.analyse(60.0, 30.0, cfg)["buckling_load"]
    cfg["discretisation"].update(prebuckling_legendre_degree=14, buckling_sine_terms=16, quadrature_points=80)
    assert base == pytest.approx(ev.analyse(60.0, 30.0, cfg)["buckling_load"], rel=1e-3)


@pytest.mark.parametrize("axis", ["x", "y"])
def test_steering_curvature_matches_finite_difference(cfg, axis):
    cfg["layup"]["variation_axis"] = axis
    plate, layup = cfg["plate"], cfg["layup"]
    x, y, h = np.array([0.07]), np.array([0.11]), 1e-6
    th = lambda x, y: np.radians(ev.angle_field(10.0, 70.0, x, y, plate, layup))
    t = th(x, y)
    grad = np.array([(th(x + h, y) - th(x - h, y)) / (2 * h), (th(x, y + h) - th(x, y - h)) / (2 * h)])
    kappa_fd = np.abs(grad[0] * np.cos(t) + grad[1] * np.sin(t))
    np.testing.assert_allclose(ev.steering_curvature(10.0, 70.0, x, y, plate, layup), kappa_fd, rtol=1e-6)


def test_straight_fibres_have_no_curvature_and_are_feasible(cfg):
    r = ev.evaluate([45.0, 45.0], cfg)
    assert r.metadata["max_steering_curvature"] == 0.0 and r.feasible
