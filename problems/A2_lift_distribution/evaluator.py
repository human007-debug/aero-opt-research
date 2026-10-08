"""A2 evaluator: lifting-line theory with a Fourier circulation distribution.

With y = -(b/2) cos(theta) and Gamma(theta) = 2 b V sum_n A_n sin(n theta) (odd n), and q = rho V^2:

    L      = (pi/2) q b^2 A1
    D_i    = (pi/2) q b^2 sum_n n A_n^2
    M_root = (q b^3 / 2) sum_n A_n I_n,   I_n = int_0^{pi/2} sin(n phi) sin(phi) cos(phi) dphi
    W      = (q b^4 / 8) sum_n A_n J_n,   J_n = int_0^{pi/2} sin(n phi) sin(phi) cos^2(phi) dphi

where W = int_0^{b/2} M(y) dy = (1/2) int_0^{b/2} l(y) y^2 dy is the span-integrated bending moment.
Closed forms (odd n): I_n = -sin(n pi/2) / (n^2 - 4);  J_1 = J_3 = pi/16, J_n = 0 otherwise.
"""
from __future__ import annotations

from typing import Any, Sequence

import numpy as np

from core.problem import EvalResult

Q = 1.0   # rho V^2
B0 = 1.0  # reference span
LIFT = 1.0


def odd_orders(n_harmonics: int) -> np.ndarray:
    return 2 * np.arange(n_harmonics + 1) + 1  # 1, 3, 5, ...


def root_moment_integrals(n: np.ndarray) -> np.ndarray:
    return -np.sin(n * np.pi / 2) / (n.astype(float) ** 2 - 4)


def integrated_moment_integrals(n: np.ndarray) -> np.ndarray:
    return np.where((n == 1) | (n == 3), np.pi / 16, 0.0)


def coefficients(design: Sequence[float]) -> tuple[float, np.ndarray]:
    """design -> (span b, Fourier coefficients A_n for n = 1, 3, 5, ...)."""
    b = float(design[0]) * B0
    A1 = 2 * LIFT / (np.pi * Q * b**2)
    return b, A1 * np.concatenate([[1.0], np.asarray(design[1:], dtype=float)])


def aero(b: float, A: np.ndarray) -> dict[str, float]:
    n = odd_orders(len(A) - 1)
    return {
        "lift": np.pi / 2 * Q * b**2 * A[0],
        "drag": np.pi / 2 * Q * b**2 * float(np.sum(n * A**2)),
        "root_moment": Q * b**3 / 2 * float(np.sum(A * root_moment_integrals(n))),
        "integrated_moment": Q * b**4 / 8 * float(np.sum(A * integrated_moment_integrals(n))),
    }


def circulation(b: float, A: np.ndarray, y: np.ndarray, V: float = 1.0) -> np.ndarray:
    theta = np.arccos(np.clip(-2 * np.asarray(y) / b, -1, 1))
    n = odd_orders(len(A) - 1)
    return 2 * b * V * np.sin(np.outer(theta, n)) @ A


def reference(n_harmonics: int) -> dict[str, float]:
    return aero(*coefficients([1.0] + [0.0] * n_harmonics))


def evaluate(design: Sequence[float], config: dict[str, Any]) -> EvalResult:
    K = config["design"]["n_harmonics"]
    if len(design) != K + 1:
        raise ValueError(f"expected {K + 1} variables, got {len(design)}")
    b, A = coefficients(design)
    res, ref = aero(b, A), reference(K)

    key = {"integrated": "integrated_moment", "root": "root_moment"}[config["constraints"]["bending_moment"]]
    constraints = {"bending_moment": res[key] / ref[key] - 1.0}
    if config["constraints"].get("nonnegative_lift"):
        theta = np.linspace(0, np.pi / 2, 401)[1:]  # cosine spacing clusters stations at the tip
        g = circulation(b, A, -(b / 2) * np.cos(theta))
        constraints["nonnegative_lift"] = float(-g.min() / g.max())

    drag_ratio = res["drag"] / ref["drag"]
    return EvalResult(
        objective=drag_ratio,
        constraints=constraints,
        feasible=all(v <= 1e-9 for v in constraints.values()),
        metadata={
            **res,
            "span_ratio": b / B0,
            "span_efficiency": A[0] ** 2 / float(np.sum(odd_orders(K) * A**2)),
            "root_moment_ratio": res["root_moment"] / ref["root_moment"],
            "integrated_moment_ratio": res["integrated_moment"] / ref["integrated_moment"],
        },
    )
