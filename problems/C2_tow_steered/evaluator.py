"""C2 evaluator: buckling of a variable-angle-tow plate by a two-step Rayleigh-Ritz method.

Plate x in [-a/2, a/2], y in [-b/2, b/2]; xi = 2x/a, eta = 2y/b. Symmetric, balanced layup, so B = 0.

Step 1, prebuckling (in-plane). Balanced +-theta pairs make A16 = A26 = 0 at every point, and the
angle field is even in x and y, so the in-plane problem is solved on the quarter plate
X = 2x/a, Y = 2y/b in [0, 1] (where A is smooth; the |r| kink sits on the symmetry line).
Unit end-shortening Delta = 1:
    u = -(Delta/2) X + X (1 - X) sum c_ij P_i(2X-1) P_j(2Y-1)     (u odd in x, prescribed at X = 1)
    v =                Y         sum d_ij P_i(2X-1) P_j(2Y-1)     (v odd in y)
P are Legendre polynomials. Remaining edge conditions are natural (traction-free transverse edges,
shear-free loaded edges). The Ritz coefficients minimise U = 1/2 int eps^T A eps dA; N = A eps is
mirrored to the full plate (Nx, Ny even-even; Nxy odd-odd).

Quadrature is composite Gauss-Legendre on each half of [-1, 1], so the kink lies on a cell boundary.

Step 2, buckling. Simply supported w = sum W_mn sin(m pi (xi+1)/2) sin(n pi (eta+1)/2), and
    (K_b + lambda K_g[N]) W = 0,
    K_b = int kappa^T D(x, y) kappa dA,   K_g = int grad(w)^T [[Nx, Nxy], [Nxy, Ny]] grad(w) dA.
The buckling load is P_cr = lambda * (compressive force carried by the plate at unit Delta).
"""
from __future__ import annotations

from functools import lru_cache
from typing import Any, Sequence

import numpy as np
from numpy.polynomial import legendre as L
from scipy.linalg import eigh

from core.laminate import abd_matrices, reduced_stiffness
from core.problem import EvalResult


# ---------------------------------------------------------------- angle field

def angle_field(T0: float, T1: float, x: np.ndarray, y: np.ndarray, plate: dict, layup: dict) -> np.ndarray:
    """Linear variation theta = phi + T0 + (T1 - T0) |r| / d, in degrees."""
    if layup["variation_axis"] == "x":
        r, d = x, plate["a"] / 2
    else:
        r, d = y, plate["b"] / 2
    return layup["phi"] + T0 + (T1 - T0) * np.abs(r) / d


def steering_curvature(T0: float, T1: float, x: np.ndarray, y: np.ndarray, plate: dict, layup: dict) -> np.ndarray:
    """Fibre path curvature kappa = grad(theta) . (cos theta, sin theta), in 1/m."""
    th = np.radians(angle_field(T0, T1, x, y, plate, layup))
    if layup["variation_axis"] == "x":
        dth = np.radians(T1 - T0) / (plate["a"] / 2) * np.sign(x)
        return np.abs(dth * np.cos(th))
    dth = np.radians(T1 - T0) / (plate["b"] / 2) * np.sign(y)
    return np.abs(dth * np.sin(th))


def layer_angles(theta: np.ndarray, n_pairs_half: int) -> list[np.ndarray]:
    """[+theta, -theta] * n_pairs_half, mirrored about the mid-plane."""
    half = [s * theta for _ in range(n_pairs_half) for s in (1.0, -1.0)]
    return half + half[::-1]


# ---------------------------------------------------------------- bases at quadrature points

@lru_cache(maxsize=8)
def _gauss(nq: int):
    """Composite Gauss-Legendre on [-1, 0] and [0, 1], nq // 2 points each (nq must be even)."""
    if nq % 2:
        raise ValueError("quadrature_points must be even")
    t, w = L.leggauss(nq // 2)
    half = (t + 1) / 2
    return np.concatenate([-half[::-1], half]), np.concatenate([w[::-1], w]) / 2


def _legendre(p: int, s: np.ndarray):
    """Values and first derivatives of P_0..P_p at s; shape (len(s), p+1)."""
    val = L.legvander(s, p)
    der = np.stack([L.legval(s, L.legder(np.eye(p + 1)[i])) for i in range(p + 1)], -1)
    return val, der


def _sines(M: int, s: np.ndarray):
    """sin(m pi (s+1)/2) and its first two derivatives w.r.t. s, m = 1..M; shape (len(s), M)."""
    k = np.arange(1, M + 1) * np.pi / 2
    arg = np.outer(s + 1, k)
    return np.sin(arg), k * np.cos(arg), -(k**2) * np.sin(arg)


# ---------------------------------------------------------------- step 1: prebuckling

def prebuckling(A: np.ndarray, a: float, b: float, p: int, nq: int):
    """In-plane stress resultants N = (Nx, Ny, Nxy) on the full quadrature grid, unit end-shortening.

    A has shape (nq, nq, 3, 3), indexed [xi, eta], and must satisfy A16 = A26 = 0.
    """
    if np.abs(A[..., [0, 1], [2, 2]]).max() > 1e-9 * np.abs(A[..., 0, 0]).max():
        raise ValueError("quarter-plate prebuckling needs A16 = A26 = 0 (balanced +-theta pairs)")
    s, w = _gauss(nq)
    h = nq // 2
    S, W = s[h:], w[h:]  # positive half: X in (0, 1)
    P, dP = _legendre(p, 2 * S - 1)
    dP = 2 * dP  # d/dX
    gu, dgu = (S * (1 - S))[:, None] * P, (1 - 2 * S)[:, None] * P + (S * (1 - S))[:, None] * dP
    gv, dgv = S[:, None] * P, P + S[:, None] * dP

    def outer(fx, fy):  # (h, h, (p+1)^2)
        return np.einsum("xi,yj->xyij", fx, fy).reshape(h, h, -1)

    zero = np.zeros((h, h, (p + 1) ** 2))
    Bu = np.stack([(2 / a) * outer(dgu, P), zero, (2 / b) * outer(gu, dP)], 2)
    Bv = np.stack([zero, (2 / b) * outer(P, dgv), (2 / a) * outer(dP, gv)], 2)
    B = np.concatenate([Bu, Bv], -1)  # (h, h, 3, ndof)

    Aq = A[h:, h:]
    wt = np.outer(W, W)
    eps0 = np.array([-1.0 / a, 0.0, 0.0])
    K = np.einsum("xy,xykn,xykl,xylm->nm", wt, B, Aq, B, optimize=True)
    f = -np.einsum("xy,xykn,xykl,l->n", wt, B, Aq, eps0, optimize=True)
    q = np.linalg.solve(K, f)
    Nq = np.einsum("xykl,xyl->xyk", Aq, eps0 + np.einsum("xykn,n->xyk", B, q))

    N = np.empty((nq, nq, 3))
    for sx, ix in ((1, slice(h, None)), (-1, slice(h - 1, None, -1))):
        for sy, iy in ((1, slice(h, None)), (-1, slice(h - 1, None, -1))):
            N[ix, iy] = Nq * np.array([1.0, 1.0, sx * sy])
    return N


# ---------------------------------------------------------------- step 2: buckling

def buckling(D: np.ndarray, N: np.ndarray, a: float, b: float, M: int, nq: int):
    """Smallest positive load factor lambda and its mode coefficients W (M x M)."""
    s, w = _gauss(nq)
    S, dS, d2S = _sines(M, s)

    def outer(fx, fy):
        return np.einsum("xm,yn->xymn", fx, fy).reshape(nq, nq, -1)

    wx, wy = (2 / a) * outer(dS, S), (2 / b) * outer(S, dS)
    kappa = np.stack([(2 / a) ** 2 * outer(d2S, S), (2 / b) ** 2 * outer(S, d2S),
                      2 * (2 / a) * (2 / b) * outer(dS, dS)], 2)
    wt = np.outer(w, w) * (a / 2) * (b / 2)

    Kb = np.einsum("xy,xykn,xykl,xylm->nm", wt, kappa, D, kappa, optimize=True)
    Nx, Ny, Nxy = (wt * N[..., i] for i in range(3))
    Kg = (np.einsum("xy,xyn,xym->nm", Nx, wx, wx) + np.einsum("xy,xyn,xym->nm", Ny, wy, wy)
          + np.einsum("xy,xyn,xym->nm", Nxy, wx, wy) + np.einsum("xy,xyn,xym->nm", Nxy, wy, wx))
    mu, vec = eigh(Kg, Kb)  # Kg W = mu Kb W  ->  lambda = -1/mu
    i = int(np.argmin(mu))
    if mu[i] >= 0:
        return np.inf, None
    return float(-1.0 / mu[i]), vec[:, i].reshape(M, M)


# ---------------------------------------------------------------- evaluate

def analyse(T0: float, T1: float, config: dict[str, Any]) -> dict[str, Any]:
    mat, plate, layup, disc = config["material"], config["plate"], config["layup"], config["discretisation"]
    a, b, nq = plate["a"], plate["b"], disc["quadrature_points"]
    s, w = _gauss(nq)
    X, Y = np.meshgrid(s * a / 2, s * b / 2, indexing="ij")

    theta = angle_field(T0, T1, X, Y, plate, layup)
    Q = reduced_stiffness(mat["E1"], mat["E2"], mat["G12"], mat["nu12"])
    A, _, D = abd_matrices(layer_angles(theta, layup["n_layer_pairs_half"]), Q, mat["ply_thickness"])

    N = prebuckling(A, a, b, disc["prebuckling_legendre_degree"], nq)
    force = -(N[..., 0] @ w) * (b / 2)  # compressive force through each x-section, unit Delta
    lam, mode = buckling(D, N, a, b, disc["buckling_sine_terms"], nq)
    return {
        "lambda": lam,  # critical end-shortening (m)
        "buckling_load": lam * float(force.mean()),
        "axial_stiffness": float(force.mean()),  # N per m of end-shortening
        "section_force_spread": float(np.ptp(force) / abs(force.mean())),
        "N": N, "A": A, "D": D, "mode": mode, "X": X, "Y": Y,
        "max_steering_curvature": float(steering_curvature(T0, T1, X, Y, plate, layup).max()),
    }


def evaluate(design: Sequence[float], config: dict[str, Any]) -> EvalResult:
    T0, T1 = (float(v) for v in design)
    r = analyse(T0, T1, config)
    R = config["constraints"]["min_steering_radius"]
    constraints = {"steering_radius": r["max_steering_curvature"] * R - 1.0}
    return EvalResult(
        objective=-r["buckling_load"],
        constraints=constraints,
        feasible=all(v <= 0 for v in constraints.values()),
        metadata={k: r[k] for k in ("buckling_load", "lambda", "axial_stiffness",
                                    "section_force_spread", "max_steering_curvature")},
    )
