"""Benchmark: Gurdal, Tatting & Wu (2008), Composites Part A 39, 911-922 (square panels, 12 layers)."""
import copy

import numpy as np
import pytest

from core.laminate import reduced_stiffness, transformed_stiffness
from core.problem import load_config
from problems.C2_tow_steered import evaluator as ev

CFG = load_config("C2_tow_steered")
BENCH = CFG["benchmark"]
TOL = BENCH["tolerance_rel"]


def _cfg(case):
    c = copy.deepcopy(CFG)
    c["layup"].update(variation_axis=case["variation_axis"], phi=case["phi"])
    c["boundary_conditions"]["transverse_edges"] = case["transverse_edges"]
    return c


@pytest.mark.parametrize("case", BENCH["cases"], ids=lambda c: c["name"])
def test_quoted_values(case):
    r = ev.analyse(case["T0"], case["T1"], _cfg(case))
    assert r["normalised_load"] == pytest.approx(case["normalised_load"], rel=TOL)
    if "normalised_stiffness" in case:  # quoted to 2 decimals
        assert r["normalised_stiffness"] == pytest.approx(case["normalised_stiffness"], abs=5e-3)


def test_case_Ib_straight_fibre_optimum():
    s = BENCH["straight_case_Ib"]
    c = _cfg(s)
    res = [(ev.analyse(t, t, c), t) for t in np.arange(20.0, 41.0, 1.0)]
    best, angle = max(res, key=lambda rt: rt[0]["normalised_load"])
    assert best["normalised_load"] == pytest.approx(s["max_normalised_load"], rel=TOL)
    assert best["normalised_stiffness"] == pytest.approx(s["stiffness_at_max"], abs=0.01)
    assert angle != s["quoted_angle"]  # see problem.yaml: the quoted +-32 is inconsistent with 0.65


def test_straight_restrained_stiffness_is_qbar11():
    # Exact for straight fibres with v = 0 on the transverse edges: E_x^eq = A11 / h.
    m = CFG["material"]
    Q = reduced_stiffness(m["E1"], m["E2"], m["G12"], m["nu12"])
    c = _cfg(BENCH["straight_case_Ib"])
    for t in (28.0, 32.0, 45.0):
        r = ev.analyse(t, t, c)
        assert r["normalised_stiffness"] == pytest.approx(transformed_stiffness(Q, t)[0, 0] / m["E1"], rel=1e-8)


@pytest.mark.parametrize("key,case", [("Ib", BENCH["cases"][0]), ("IIa", BENCH["cases"][2])])
def test_optimum_location_on_5_degree_grid(key, case):
    c = _cfg(case)
    grid = np.arange(0.0, 91.0, 5.0)
    loads = [ev.analyse(0.0, t, c)["normalised_load"] for t in grid]
    assert grid[int(np.argmax(loads))] == BENCH["argmax_T1_at_T0_0"][key]


def test_case_II_straight_optimum_is_45():
    c = _cfg(BENCH["cases"][1])
    grid = np.arange(0.0, 91.0, 5.0)
    loads = [ev.analyse(t, t, c)["normalised_load"] for t in grid]
    assert grid[int(np.argmax(loads))] == 45.0
