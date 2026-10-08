"""Prandtl bell-shaped optimum under the span-integrated bending-moment constraint.

Closed-form derivation used as the benchmark (lifting-line theory, fixed lift):
  With A1 = 2/(pi b^2) and a = A3/A1, the integrated-moment terms J_n vanish for n >= 5,
  so higher harmonics only add drag and are zero at the optimum. Then
      D / D_ell(b0) = (b0/b)^2 (1 + 3 a^2),   W / W_ell(b0) = (b/b0)^2 (1 + a).
  Holding W fixed gives D ~ (1 + 3a^2)(1 + a), with d/da = (3a + 1)^2 >= 0. D therefore decreases
  monotonically as a decreases. a = -1/3 is a stationary inflection, not an unconstrained minimum.
  Near the tip Gamma ~ (1 + 3a) theta, so Gamma >= 0 requires a >= -1/3. With that constraint the
  optimum is at the boundary:
      a = -1/3,  b/b0 = sqrt(3/2) ~ 1.2247,  D/D_ell = 8/9 ~ 0.8889.
  These match the commonly cited figures (~22% more span, ~11% less induced drag).
  TODO: verify from source that Prandtl (1933) reports these values (benchmark.cited_values_verified).
"""
import copy

import numpy as np
import pytest
from scipy.optimize import minimize

from core.problem import load_config
from problems.A2_lift_distribution import evaluator as ev

PID = "A2_lift_distribution"
CFG = load_config(PID)
TOL = CFG["benchmark"]["tolerance_rel"]
K = CFG["design"]["n_harmonics"]
BELL = [np.sqrt(1.5), -1 / 3] + [0.0] * (K - 1)


def _solve(cfg, x0=None):
    """Small deterministic SLSQP solve. Used only to check that the closed form is the optimum."""
    bounds = [tuple(cfg["design"]["bounds"]["span_ratio"])] + [tuple(cfg["design"]["bounds"]["harmonic_ratio"])] * K
    x0 = [1.0] + [0.0] * K if x0 is None else x0
    f = lambda x: ev.evaluate(x, cfg).objective
    cons = [{"type": "ineq", "fun": (lambda x, k=k: -ev.evaluate(x, cfg).constraints[k])}
            for k in ev.evaluate(x0, cfg).constraints]
    return minimize(f, x0, method="SLSQP", bounds=bounds, constraints=cons,
                    options={"ftol": 1e-14, "maxiter": 1000})


def test_bell_distribution_values():
    r = ev.evaluate(BELL, CFG)
    assert r.feasible
    assert r.objective == pytest.approx(8 / 9, rel=TOL)
    assert r.metadata["span_ratio"] == pytest.approx(np.sqrt(1.5), rel=TOL)
    assert r.constraints["bending_moment"] == pytest.approx(0.0, abs=1e-12)


def test_bell_shape_is_one_minus_eta_squared_to_three_halves():
    b, A = ev.coefficients(BELL)
    eta = np.linspace(-0.99, 0.99, 41)
    g = ev.circulation(b, A, eta * b / 2)
    np.testing.assert_allclose(g / g[20], (1 - eta**2) ** 1.5, rtol=1e-12)


@pytest.mark.parametrize("seed", range(5))
def test_numerical_optimum_equals_closed_form(seed):
    rng = np.random.default_rng(seed)
    x0 = [1.0] + [0.0] * K if seed == 0 else [rng.uniform(1.0, 1.4), rng.uniform(-0.3, 0.1)] + list(rng.normal(0, 0.02, K - 1))
    res = _solve(CFG, x0)
    assert res.success, res.message
    assert ev.evaluate(res.x, CFG).feasible
    # Near the optimum D - 8/9 ~ (a + 1/3)^3, so the design is only resolvable to ~ftol^(1/3).
    np.testing.assert_allclose(res.x[:2], BELL[:2], rtol=1e-3)
    np.testing.assert_allclose(res.x[2:], 0.0, atol=1e-3)
    assert res.fun == pytest.approx(8 / 9, rel=1e-8)


def test_without_nonnegative_lift_the_bell_is_beaten():
    cfg = copy.deepcopy(CFG)
    cfg["constraints"]["nonnegative_lift"] = False
    r = ev.evaluate([np.sqrt(2.0), -0.5] + [0.0] * (K - 1), cfg)
    assert r.feasible and r.objective == pytest.approx(0.875) and r.objective < 8 / 9


def test_root_moment_variant_is_a_different_problem():
    # Root bending moment couples to every odd harmonic (I_n != 0), so the optimum is not the bell.
    cfg = copy.deepcopy(CFG)
    cfg["constraints"]["bending_moment"] = "root"
    res = _solve(cfg)
    assert res.success, res.message
    assert np.max(np.abs(res.x[2:])) > 1e-3
    assert res.fun < 1.0
