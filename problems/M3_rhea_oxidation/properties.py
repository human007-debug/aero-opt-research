"""Physics-based property models for BCC refractory alloys: density and solid-solution yield strength.

Density (ideal mixing of atomic volumes):
    rho = sum c_i M_i / (N_A sum c_i V_i)

Yield strength: reduced (elasticity-based) edge-dislocation model of
F. Maresca and W. A. Curtin, Acta Materialia 182 (2020) 235-249; arXiv:1901.02100v3 (verified against v3):
    misfit  = sum c_n dV_n^2 / b^6,  dV_n = V_n - V_bar,  V_bar = sum c_n V_n  (Vegard)        p.19
    a = (2 V_bar)^(1/3), b = (sqrt(3)/2) a
    C_ij alloy = sum c_n C_ij^n (rule of mixtures);  mu = sqrt(C44 (C11 - C12) / 2),
    B = (C11 + 2 C12) / 3,  nu = (3B - 2 mu) / (2 (3B + mu))                                    p.12, p.19
    tau_y0 = 0.040 alpha^(-1/3) mu P^(4/3) misfit^(2/3),  P = (1 + nu)/(1 - nu)                p.19
    dE_b   = 2.00  alpha^( 1/3) mu b^3 P^(2/3) misfit^(1/3)                                   p.19
    tau_y = tau_y0 [1 - (kT/dE_b ln(rate0/rate))^(2/3)]   if tau_y/tau_y0 >= 0.5               Eq. 11
          = tau_y0 exp(-(1/0.55) kT/dE_b ln(rate0/rate))   otherwise                           Eq. 12
    rate0 = 1e4 /s (p.10), alpha = 1/12 (p.12), sigma_y = M tau_y with M = 3.067 (p.17).
Elemental C_ij and BCC volumes for Mo, Nb, Ta, V, W are recovered from the paper's Table 2
(data/elements.yaml, block maresca_curtin_2020). The paper validates the model only for this family, so
strength() refuses other elements.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import numpy as np
import yaml

HERE = Path(__file__).parent
K_B = 1.380649e-23
N_A = 6.02214076e23

MC_PARAMS = {  # verified: Maresca & Curtin (2020), arXiv:1901.02100v3, pp.10, 12, 17, 19
    "A_tau": 0.040, "A_E": 2.00, "alpha": 1 / 12, "taylor_M": 3.067, "rate0": 1.0e4,
    "switch_ratio": 0.5, "high_T_factor": 0.55,
}
STRENGTH_ELEMENTS = ["Al", "Cr", "Hf", "Mo", "Nb", "Ta", "Ti", "V", "W", "Zr"]  # design space of M3X (Si excluded)
MC_ELEMENTS = ["Mo", "Nb", "Ta", "V", "W"]  # validated family of the physics strength model


@lru_cache(maxsize=1)
def elements() -> dict:
    return yaml.safe_load((HERE / "data" / "elements.yaml").read_text())


def _arr(comp: dict[str, float], key: str):
    el = elements()
    keys = [k for k, v in comp.items() if v > 0]
    c = np.array([comp[k] for k in keys], float)
    c = c / c.sum()
    return keys, c, np.array([el[k][key] for k in keys], float)


def density(comp: dict[str, float]) -> float:
    """g/cm^3 from at. fractions (any normalisation)."""
    keys, c, M = _arr(comp, "atomic_mass")
    _, _, V = _arr(comp, "atomic_volume_A3")
    return float((c @ M) / N_A / ((c @ V) * 1e-24))


def mc_inputs(comp: dict[str, float]):
    mc = elements()["maresca_curtin_2020"]
    keys = [k for k, v in comp.items() if v > 0]
    c = np.array([comp[k] for k in keys], float)
    c = c / c.sum()
    get = lambda q: np.array([mc[k][q] for k in keys], float)
    return c, get("V_bcc"), get("C11"), get("C12"), get("C44")


def strength(comp: dict[str, float], T_K: float, strain_rate: float = 1e-3, params: dict | None = None) -> dict:
    """Reduced Maresca-Curtin edge model. Returns sigma_y (MPa) and intermediate quantities."""
    p = {**MC_PARAMS, **(params or {})}
    if any(k not in MC_ELEMENTS for k, v in comp.items() if v > 0):
        raise ValueError(f"Maresca-Curtin inputs available for {MC_ELEMENTS} only")
    c, V, C11, C12, C44 = mc_inputs(comp)
    V = V * 1e-30  # m^3
    Vbar = c @ V
    misfit_V2 = c @ (V - Vbar) ** 2
    a = (2 * Vbar) ** (1 / 3)
    b = np.sqrt(3) / 2 * a
    c11, c12, c44 = (c @ C11) * 1e9, (c @ C12) * 1e9, (c @ C44) * 1e9
    mu = np.sqrt(0.5 * c44 * (c11 - c12))
    B = (c11 + 2 * c12) / 3
    nu = (3 * B - 2 * mu) / (2 * (3 * B + mu))
    P = (1 + nu) / (1 - nu)
    m = misfit_V2 / b**6
    tau0 = p["A_tau"] * p["alpha"] ** (-1 / 3) * mu * P ** (4 / 3) * m ** (2 / 3)
    dEb = p["A_E"] * p["alpha"] ** (1 / 3) * mu * b**3 * P ** (2 / 3) * m ** (1 / 3)
    x = K_B * T_K / dEb * np.log(p["rate0"] / strain_rate) if dEb > 0 else np.inf
    low = 1 - x ** (2 / 3) if np.isfinite(x) else -np.inf
    ratio = low if low >= p["switch_ratio"] else np.exp(-x / p["high_T_factor"])
    return {"sigma_y_MPa": float(p["taylor_M"] * tau0 * ratio / 1e6), "tau_y0_MPa": float(tau0 / 1e6),
            "dEb_eV": float(dEb / 1.602176634e-19), "delta_V_rms_A3": float(np.sqrt(misfit_V2) * 1e30),
            "mu_GPa": float(mu / 1e9), "nu": float(nu), "b_A": float(b * 1e10), "a_A": float(a * 1e10),
            "regime": "low_T" if low >= p["switch_ratio"] else "high_T"}
