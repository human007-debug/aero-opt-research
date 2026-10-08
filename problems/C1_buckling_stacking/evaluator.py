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

from core.laminate import abd_matrices, reduced_stiffness, transformed_stiffness  # noqa: F401
from core.problem import EvalResult


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

def load_sets(config: dict[str, Any]) -> list[tuple[float, float]]:
    """(Nx, Ny) pairs of the selected load case. Compression positive."""
    sets = config["load_cases"][config["loads"]["case"]]
    return [(float(nx), float(ny)) for nx, ny in sets]


def evaluate(design: Sequence[int], config: dict[str, Any]) -> EvalResult:
    """lambda_cr = min over the case's load sets of min(lambda_buckling, lambda_strength)."""
    d = config["design"]
    mat, plate = config["material"], config["plate"]
    cons, buck = config["constraints"], config["buckling"]

    n_genes = d["n_plies_total"] // 4
    if len(design) != n_genes:
        raise ValueError(f"expected {n_genes} stack genes, got {len(design)}")

    angles = decode(design, d["stack_alphabet"])
    Q = reduced_stiffness(mat["E1"], mat["E2"], mat["G12"], mat["nu12"])
    A, B, D = abd_matrices(angles, Q, mat["ply_thickness"])

    lam_b, lam_s, mode = np.inf, np.inf, None
    for Nx, Ny in load_sets(config):
        lb, m = buckling_load_factor(D, plate["a"], plate["b"], Nx, Ny, buck["max_half_waves"])
        if lb < lam_b:
            lam_b, mode = lb, m
        if cons["strength"]["enabled"]:
            lam_s = min(lam_s, strength_load_factor(A, angles, Nx, Ny, cons["strength"]))
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
            "lambda_strength": None if lam_s == np.inf else lam_s,
            "failure_mode": "buckling" if lam_b <= lam_s else "strain",
            "buckling_mode_mn": mode,
            "max_contiguous_run": run,
            "D16_over_D11": float(D[0, 2] / D[0, 0]),
            "D26_over_D22": float(D[1, 2] / D[1, 1]),
        },
    )


def search_space(config: dict[str, Any]) -> dict[str, Any]:
    n = config["design"]["n_plies_total"] // 4
    return {"type": "categorical", "n_vars": n, "n_values": len(config["design"]["stack_alphabet"])}


# ---------------------------------------------------------------- batch (exhaustive enumeration)

def batch_evaluate(genes: np.ndarray, config: dict[str, Any], chunk: int = 20000) -> dict[str, np.ndarray]:
    """Vectorised evaluate() for many designs at once; genes has shape (n_designs, n_genes).

    Uses the same physics as evaluate(). Used to enumerate small design spaces exhaustively.
    """
    genes = np.asarray(genes, dtype=int)
    n, K = genes.shape
    mat, plate, cons = config["material"], config["plate"], config["constraints"]
    alpha = config["design"]["stack_alphabet"]
    Q = reduced_stiffness(mat["E1"], mat["E2"], mat["G12"], mat["nu12"])
    t = mat["ply_thickness"]
    h = 4 * K * t

    # Per-position, per-stack-type contributions (both halves of the symmetric laminate).
    codes = sorted(alpha)
    Dc = np.zeros((K, len(codes), 3, 3))
    Ac = np.zeros((len(codes), 3, 3))
    for c_i, c in enumerate(codes):
        for p_i, ang in enumerate(alpha[c]):
            Qb = transformed_stiffness(Q, ang)
            Ac[c_i] += 2 * Qb * t
            for k in range(K):
                z0 = -h / 2 + (2 * k + p_i) * t
                Dc[k, c_i] += 2 * Qb * ((z0 + t) ** 3 - z0**3) / 3

    M = config["buckling"]["max_half_waves"]
    mm = (np.arange(1, M + 1)[:, None] / plate["a"]) ** 2
    nn = (np.arange(1, M + 1)[None, :] / plate["b"]) ** 2
    angles_by_code = {ci: alpha[c] for ci, c in enumerate(codes)}

    lam_b = np.full(n, np.inf)
    lam_s = np.full(n, np.inf)
    for s0 in range(0, n, chunk):
        g = genes[s0:s0 + chunk]
        idx = np.searchsorted(codes, g)
        D = Dc[np.arange(K)[None, :], idx].sum(1)  # (c, 3, 3)
        counts = np.stack([(idx == ci).sum(1) for ci in range(len(codes))], 1)
        A = np.einsum("nc,cij->nij", counts, Ac)
        for Nx, Ny in load_sets(config):
            num = np.pi**2 * (D[:, 0, 0, None, None] * mm**2 + 2 * (D[:, 0, 1] + 2 * D[:, 2, 2])[:, None, None] * mm * nn
                              + D[:, 1, 1, None, None] * nn**2)
            den = mm * Nx + nn * Ny
            lb = np.where(den > 0, num / np.where(den > 0, den, 1.0), np.inf).reshape(len(g), -1).min(1)
            lam_b[s0:s0 + chunk] = np.minimum(lam_b[s0:s0 + chunk], lb)
            if cons["strength"]["enabled"]:
                al = cons["strength"]
                eps = np.linalg.solve(A, np.broadcast_to(np.array([-Nx, -Ny, 0.0]), (len(g), 3))[..., None])[..., 0]
                ls = np.full(len(g), np.inf)
                for ci in range(len(codes)):
                    present = counts[:, ci] > 0
                    for th in set(angles_by_code[ci]):
                        r = np.radians(th); c, s = np.cos(r), np.sin(r)
                        e1 = c * c * eps[:, 0] + s * s * eps[:, 1] + s * c * eps[:, 2]
                        e2 = s * s * eps[:, 0] + c * c * eps[:, 1] - s * c * eps[:, 2]
                        g12 = -2 * s * c * eps[:, 0] + 2 * s * c * eps[:, 1] + (c * c - s * s) * eps[:, 2]
                        for val, lim in ((e1, al["eps1_allow"]), (e2, al["eps2_allow"]), (g12, al["gamma12_allow"])):
                            with np.errstate(divide="ignore"):
                                f = np.where(np.abs(val) > 0, lim / (al["safety_factor"] * np.abs(val)), np.inf)
                            ls = np.where(present, np.minimum(ls, f), ls)
                lam_s[s0:s0 + chunk] = np.minimum(lam_s[s0:s0 + chunk], ls)

    # Contiguity on the full symmetric ply sequence.
    half = np.concatenate([np.array([alpha[c] for c in codes])[np.searchsorted(codes, genes)][:, k] for k in range(K)], 1)
    full = np.concatenate([half, half[:, ::-1]], 1)
    key = np.abs(full) if cons["contiguity_mode"] == "abs" else full
    run = np.ones(n, dtype=int); best = np.ones(n, dtype=int)
    for j in range(1, full.shape[1]):
        run = np.where(key[:, j] == key[:, j - 1], run + 1, 1)
        best = np.maximum(best, run)

    return {"lambda_cr": np.minimum(lam_b, lam_s), "lambda_buckling": lam_b, "lambda_strength": lam_s,
            "max_contiguous_run": best, "contiguity_ok": best <= cons["max_contiguous"]}


def enumerate_designs(n_genes: int, n_codes: int = 3) -> np.ndarray:
    """All n_codes ** n_genes stack sequences, shape (n_codes ** n_genes, n_genes)."""
    return np.array(np.unravel_index(np.arange(n_codes**n_genes), (n_codes,) * n_genes)).T
