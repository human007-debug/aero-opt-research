"""C1 evaluator: classical laminate theory + closed-form orthotropic plate buckling.

Simply supported rectangular plate a x b under in-plane loads Nx, Ny (compression
positive). With D16 = D26 = 0 the buckling load factor for mode (m, n) is

    lambda_b(m, n) = pi^2 [D11 (m/a)^4 + 2 (D12 + 2 D66) (m/a)^2 (n/b)^2 + D22 (n/b)^4]
                     / [(m/a)^2 Nx + (n/b)^2 Ny]

and lambda_cr = min over (m, n) with a positive denominator.
"""
from __future__ import annotations

from typing import Any, Sequence

import numpy as np

from core.problem import EvalResult


# ---------------------------------------------------------------- laminate theory

def reduced_stiffness(E1: float, E2: float, G12: float, nu12: float) -> np.ndarray:
    nu21 = nu12 * E2 / E1
    d = 1.0 - nu12 * nu21
    return np.array([
        [E1 / d, nu12 * E2 / d, 0.0],
        [nu12 * E2 / d, E2 / d, 0.0],
        [0.0, 0.0, G12],
    ])


def transformed_stiffness(Q: np.ndarray, theta_deg: float) -> np.ndarray:
    t = np.radians(theta_deg)
    c, s = np.cos(t), np.sin(t)
    Q11, Q12, Q22, Q66 = Q[0, 0], Q[0, 1], Q[1, 1], Q[2, 2]
    c2, s2, c4, s4 = c * c, s * s, c**4, s**4
    Qb11 = Q11 * c4 + 2 * (Q12 + 2 * Q66) * s2 * c2 + Q22 * s4
    Qb22 = Q11 * s4 + 2 * (Q12 + 2 * Q66) * s2 * c2 + Q22 * c4
    Qb12 = (Q11 + Q22 - 4 * Q66) * s2 * c2 + Q12 * (s4 + c4)
    Qb66 = (Q11 + Q22 - 2 * Q12 - 2 * Q66) * s2 * c2 + Q66 * (s4 + c4)
    Qb16 = (Q11 - Q12 - 2 * Q66) * s * c**3 + (Q12 - Q22 + 2 * Q66) * s**3 * c
    Qb26 = (Q11 - Q12 - 2 * Q66) * s**3 * c + (Q12 - Q22 + 2 * Q66) * s * c**3
    return np.array([
        [Qb11, Qb12, Qb16],
        [Qb12, Qb22, Qb26],
        [Qb16, Qb26, Qb66],
    ])


def abd_matrices(angles: Sequence[float], Q: np.ndarray, t_ply: float):
    """A, B, D for a laminate listed from the top surface (z = -h/2) downward."""
    n = len(angles)
    z = np.linspace(-n * t_ply / 2, n * t_ply / 2, n + 1)
    A = np.zeros((3, 3)); B = np.zeros((3, 3)); D = np.zeros((3, 3))
    for k, th in enumerate(angles):
        Qb = transformed_stiffness(Q, th)
        A += Qb * (z[k + 1] - z[k])
        B += Qb * (z[k + 1] ** 2 - z[k] ** 2) / 2
        D += Qb * (z[k + 1] ** 3 - z[k] ** 3) / 3
    return A, B, D


# ---------------------------------------------------------------- design encoding

def decode(genes: Sequence[int], alphabet: dict) -> list[float]:
    """Stack genes (outer -> mid-plane) to the full symmetric ply-angle list."""
    half = [ang for g in genes for ang in alphabet[int(g)]]
    return half + half[::-1]


def max_contiguous(angles: Sequence[float], mode: str = "ply") -> int:
    """Longest run of identical orientation. mode='ply' compares signed angles;
    mode='abs' treats +theta and -theta as the same orientation."""
    key = (lambda a: abs(a)) if mode == "abs" else (lambda a: a)
    best = run = 1
    for prev, cur in zip(angles, angles[1:]):
        run = run + 1 if key(cur) == key(prev) else 1
        best = max(best, run)
    return best


# ---------------------------------------------------------------- buckling

def buckling_load_factor(D: np.ndarray, a: float, b: float, Nx: float, Ny: float,
                         max_half_waves: int = 20) -> tuple[float, tuple[int, int]]:
    m = np.arange(1, max_half_waves + 1)[:, None]
    n = np.arange(1, max_half_waves + 1)[None, :]
    alpha, beta = (m / a) ** 2, (n / b) ** 2
    num = np.pi**2 * (D[0, 0] * alpha**2 + 2 * (D[0, 1] + 2 * D[2, 2]) * alpha * beta
                      + D[1, 1] * beta**2)
    den = alpha * Nx + beta * Ny
    lam = np.where(den > 0, num / np.where(den > 0, den, 1.0), np.inf)
    i, j = np.unravel_index(np.argmin(lam), lam.shape)
    return float(lam[i, j]), (int(i + 1), int(j + 1))


def strength_load_factor(A: np.ndarray, angles: Sequence[float], Nx: float, Ny: float,
                         allow: dict) -> float:
    """First-ply failure load factor from maximum-strain criterion (compression positive
    loads are applied as negative in-plane resultants)."""
    eps = np.linalg.solve(A, np.array([-Nx, -Ny, 0.0]))  # midplane strains, B = 0
    sf = allow["safety_factor"]
    lam = np.inf
    for th in set(angles):
        t = np.radians(th)
        c, s = np.cos(t), np.sin(t)
        e1 = c * c * eps[0] + s * s * eps[1] + s * c * eps[2]
        e2 = s * s * eps[0] + c * c * eps[1] - s * c * eps[2]
        g12 = -2 * s * c * eps[0] + 2 * s * c * eps[1] + (c * c - s * s) * eps[2]
        for val, lim in ((e1, allow["eps1_allow"]), (e2, allow["eps2_allow"]),
                         (g12, allow["gamma12_allow"])):
            if abs(val) > 0:
                lam = min(lam, lim / (sf * abs(val)))
    return float(lam)


# ---------------------------------------------------------------- evaluate

def evaluate(design: Sequence[int], config: dict[str, Any]) -> EvalResult:
    d = config["design"]
    mat, plate, loads = config["material"], config["plate"], config["loads"]
    cons, buck = config["constraints"], config["buckling"]
    if loads["Nx"] is None or loads["Ny"] is None:
        raise ValueError("loads.Nx / loads.Ny are unset in problem.yaml (benchmark load case not verified)")

    n_genes = d["n_plies_total"] // 4
    if len(design) != n_genes:
        raise ValueError(f"expected {n_genes} stack genes, got {len(design)}")

    angles = decode(design, d["stack_alphabet"])
    Q = reduced_stiffness(mat["E1"], mat["E2"], mat["G12"], mat["nu12"])
    A, B, D = abd_matrices(angles, Q, mat["ply_thickness"])

    lam_b, mode = buckling_load_factor(D, plate["a"], plate["b"], loads["Nx"], loads["Ny"],
                                       buck["max_half_waves"])
    lam_cr = lam_b
    lam_s = None
    if cons["strength"]["enabled"]:
        lam_s = strength_load_factor(A, angles, loads["Nx"], loads["Ny"], cons["strength"])
        lam_cr = min(lam_b, lam_s)

    run = max_contiguous(angles, cons["contiguity_mode"])
    constraints = {
        "contiguity": float(run - cons["max_contiguous"]),
        # Satisfied by construction for the stacks encoding; reported for completeness.
        "balance": float(abs(A[0, 2]) + abs(A[1, 2]) > 1e-9 * abs(A[0, 0])),
        "symmetry": float(np.abs(B).max() > 1e-9 * abs(A[0, 0]) * mat["ply_thickness"]),
    }
    feasible = all(v <= 0 for v in constraints.values())
    return EvalResult(
        objective=-lam_cr,
        constraints=constraints,
        feasible=feasible,
        metadata={
            "lambda_cr": lam_cr,
            "lambda_buckling": lam_b,
            "lambda_strength": lam_s,
            "buckling_mode_mn": mode,
            "max_contiguous_run": run,
            "angles": angles,
            "D16_over_D11": float(D[0, 2] / D[0, 0]),
            "D26_over_D22": float(D[1, 2] / D[1, 1]),
        },
    )
