"""Classical laminate theory shared across composite problems."""
from __future__ import annotations

import numpy as np


def reduced_stiffness(E1: float, E2: float, G12: float, nu12: float) -> np.ndarray:
    nu21 = nu12 * E2 / E1
    d = 1.0 - nu12 * nu21
    return np.array([
        [E1 / d, nu12 * E2 / d, 0.0],
        [nu12 * E2 / d, E2 / d, 0.0],
        [0.0, 0.0, G12],
    ])


def transformed_stiffness(Q: np.ndarray, theta_deg) -> np.ndarray:
    """Q-bar for a ply at angle theta (degrees). theta may be an array; result has shape (*theta.shape, 3, 3)."""
    t = np.radians(np.asarray(theta_deg, dtype=float))
    c, s = np.cos(t), np.sin(t)
    Q11, Q12, Q22, Q66 = Q[0, 0], Q[0, 1], Q[1, 1], Q[2, 2]
    c2, s2, c4, s4 = c * c, s * s, c**4, s**4
    Qb11 = Q11 * c4 + 2 * (Q12 + 2 * Q66) * s2 * c2 + Q22 * s4
    Qb22 = Q11 * s4 + 2 * (Q12 + 2 * Q66) * s2 * c2 + Q22 * c4
    Qb12 = (Q11 + Q22 - 4 * Q66) * s2 * c2 + Q12 * (s4 + c4)
    Qb66 = (Q11 + Q22 - 2 * Q12 - 2 * Q66) * s2 * c2 + Q66 * (s4 + c4)
    Qb16 = (Q11 - Q12 - 2 * Q66) * s * c**3 + (Q12 - Q22 + 2 * Q66) * s**3 * c
    Qb26 = (Q11 - Q12 - 2 * Q66) * s**3 * c + (Q12 - Q22 + 2 * Q66) * s * c**3
    return np.stack([
        np.stack([Qb11, Qb12, Qb16], -1),
        np.stack([Qb12, Qb22, Qb26], -1),
        np.stack([Qb16, Qb26, Qb66], -1),
    ], -2)


def abd_matrices(angles, Q: np.ndarray, t_ply: float):
    """A, B, D for plies listed from the top surface (z = -h/2) downward.

    Each entry of ``angles`` may be a scalar or an array of the same shape (point-wise
    angles for variable-stiffness laminates); A, B, D then have shape (*shape, 3, 3).
    """
    n = len(angles)
    z = np.linspace(-n * t_ply / 2, n * t_ply / 2, n + 1)
    A = B = D = 0.0
    for k, th in enumerate(angles):
        Qb = transformed_stiffness(Q, th)
        A = A + Qb * (z[k + 1] - z[k])
        B = B + Qb * (z[k + 1] ** 2 - z[k] ** 2) / 2
        D = D + Qb * (z[k + 1] ** 3 - z[k] ** 3) / 3
    return A, B, D
