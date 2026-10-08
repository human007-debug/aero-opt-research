"""Check the Fourier closed forms against direct numerical integration of Gamma(y)."""
import copy

import numpy as np
import pytest
from scipy.integrate import quad

from core.problem import load_config
from problems.A2_lift_distribution import evaluator as ev

PID = "A2_lift_distribution"
RHO, V = 1.0, 1.0  # q = rho V^2 = 1
DESIGNS = [
    [1.0] + [0.0] * 10,
    [1.3, -0.25, 0.05] + [0.0] * 8,
    [0.8, 0.1, -0.03, 0.02, 0.01] + [0.0] * 6,
]


@pytest.fixture
def cfg():
    return copy.deepcopy(load_config(PID))


@pytest.mark.parametrize("n", [1, 3, 5, 7, 9, 21])
def test_moment_integral_closed_forms(n):
    I = quad(lambda p: np.sin(n * p) * np.sin(p) * np.cos(p), 0, np.pi / 2)[0]
    J = quad(lambda p: np.sin(n * p) * np.sin(p) * np.cos(p) ** 2, 0, np.pi / 2)[0]
    np.testing.assert_allclose(ev.root_moment_integrals(np.array([n]))[0], I, atol=1e-13)
    np.testing.assert_allclose(ev.integrated_moment_integrals(np.array([n]))[0], J, atol=1e-13)


@pytest.mark.parametrize("design", DESIGNS)
def test_loads_match_direct_quadrature(design):
    b, A = ev.coefficients(design)
    gam = lambda y: ev.circulation(b, A, np.array([y]))[0]
    res = ev.aero(b, A)
    lift = RHO * V * quad(gam, -b / 2, b / 2, limit=200)[0]
    m_root = RHO * V * quad(lambda y: gam(y) * y, 0, b / 2, limit=200)[0]
    w_int = 0.5 * RHO * V * quad(lambda y: gam(y) * y**2, 0, b / 2, limit=200)[0]
    np.testing.assert_allclose(res["lift"], lift, rtol=1e-9)
    np.testing.assert_allclose(res["root_moment"], m_root, rtol=1e-9)
    np.testing.assert_allclose(res["integrated_moment"], w_int, rtol=1e-9)


@pytest.mark.parametrize("design", DESIGNS)
def test_drag_matches_trefftz_plane_integral(design):
    # D_i = rho int Gamma(y) w(y) dy with downwash w = V sum n A_n sin(n theta) / sin(theta).
    b, A = ev.coefficients(design)
    n = ev.odd_orders(len(A) - 1)

    def integrand(t):  # dy = (b/2) sin(theta) dtheta, so the sin(theta) cancels
        g = 2 * b * V * np.sum(A * np.sin(n * t))
        return RHO * g * V * np.sum(n * A * np.sin(n * t)) * b / 2

    np.testing.assert_allclose(ev.aero(b, A)["drag"], quad(integrand, 0, np.pi, limit=200)[0], rtol=1e-9)


def test_lift_held_fixed_for_any_design():
    for d in DESIGNS:
        np.testing.assert_allclose(ev.aero(*ev.coefficients(d))["lift"], ev.LIFT, rtol=1e-12)


def test_elliptic_reference(cfg):
    r = ev.evaluate([1.0] + [0.0] * 10, cfg)
    assert r.objective == pytest.approx(1.0)
    assert r.metadata["span_efficiency"] == pytest.approx(1.0)
    assert r.constraints["bending_moment"] == pytest.approx(0.0, abs=1e-12)
    assert r.feasible


def test_elliptic_drag_scales_inverse_square_of_span(cfg):
    cfg["constraints"]["nonnegative_lift"] = False
    r = ev.evaluate([1.5] + [0.0] * 10, cfg)
    assert r.objective == pytest.approx(1 / 1.5**2)
    assert not r.feasible  # longer elliptic wing carries more bending moment


def test_nonnegative_lift_constraint(cfg):
    cfg["constraints"]["nonnegative_lift"] = True
    assert ev.evaluate([1.0] + [0.0] * 10, cfg).constraints["nonnegative_lift"] <= 0
    # A3/A1 = -1/3 gives sin^3: zero only at the tips. A3/A1 = -0.6 produces negative tip loading.
    assert ev.evaluate([1.0, -0.6] + [0.0] * 9, cfg).constraints["nonnegative_lift"] > 0


def test_wrong_length_rejected(cfg):
    with pytest.raises(ValueError):
        ev.evaluate([1.0, 0.0], cfg)
