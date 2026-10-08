"""Physics-based property models for BCC refractory alloys: density and solid-solution yield strength.

Density (ideal mixing of atomic volumes):
    rho = sum c_i M_i / (N_A sum c_i V_i)

Yield strength: Maresca & Curtin edge-dislocation model for BCC high-entropy alloys,
F. Maresca and W. A. Curtin, Acta Materialia 182 (2020) 235-249 (arXiv:1901.02100). Reduced form:
    misfit  = sum c_n dV_n^2 / b^6,  dV_n = V_n - V_bar,  V_bar = sum c_n V_n
    a = (2 V_bar)^(1/3), b = (sqrt(3)/2) a
    P = (1 + nu) / (1 - nu)
    tau_y0 = A_tau * alpha^(-1/3) * mu * P^(4/3) * misfit^(2/3)
    dE_b   = A_E   * alpha^( 1/3) * mu * b^3 * P^(2/3) * misfit^(1/3)
    x = k T / dE_b * ln(rate0 / rate)
    tau_y = tau_y0 (1 - x^(2/3))       if that ratio >= 0.5   (low temperature / high stress)
          = tau_y0 exp(-x / 0.55)       otherwise              (high temperature / low stress)
    sigma_y = M tau_y
Alloy mu and nu are composition averages of the elemental isotropic values (data/elements.yaml).

ALL MODEL CONSTANTS BELOW ARE UNVERIFIED (written from memory; the paper could not be retrieved from this
environment). TODO: verify from source: A_tau, A_E, alpha, M, rate0, the 0.5 switch and 0.55 factor, and how
the original work averages elastic constants and chooses volumes for non-BCC elements. Until then, compare
this model with experiments as a calibration check only, not as a validated benchmark.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import numpy as np
import yaml

HERE = Path(__file__).parent
K_B = 1.380649e-23
N_A = 6.02214076e23

MC_PARAMS = {  # TODO: verify from source (Maresca & Curtin 2020)
    "A_tau": 0.040, "A_E": 2.00, "alpha": 0.123, "taylor_M": 3.06, "rate0": 1.0e4,
    "switch_ratio": 0.5, "high_T_factor": 0.55,
}
STRENGTH_ELEMENTS = ["Al", "Cr", "Hf", "Mo", "Nb", "Ta", "Ti", "V", "W", "Zr"]  # Si excluded


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


def strength(comp: dict[str, float], T_K: float, strain_rate: float = 1e-3, params: dict | None = None) -> dict:
    """Maresca-Curtin edge model. Returns sigma_y (MPa) and intermediate quantities."""
    p = {**MC_PARAMS, **(params or {})}
    if any(k not in STRENGTH_ELEMENTS for k, v in comp.items() if v > 0):
        raise ValueError(f"strength model covers {STRENGTH_ELEMENTS} only")
    keys, c, V = _arr(comp, "atomic_volume_A3")
    _, _, mu_i = _arr(comp, "shear_modulus_GPa_used")
    _, _, nu_i = _arr(comp, "poissons_ratio")
    V = V * 1e-30  # m^3
    Vbar = c @ V
    misfit_V2 = c @ (V - Vbar) ** 2
    a = (2 * Vbar) ** (1 / 3)
    b = np.sqrt(3) / 2 * a
    mu, nu = (c @ mu_i) * 1e9, c @ nu_i
    P = (1 + nu) / (1 - nu)
    m = misfit_V2 / b**6
    tau0 = p["A_tau"] * p["alpha"] ** (-1 / 3) * mu * P ** (4 / 3) * m ** (2 / 3)
    dEb = p["A_E"] * p["alpha"] ** (1 / 3) * mu * b**3 * P ** (2 / 3) * m ** (1 / 3)
    x = K_B * T_K / dEb * np.log(p["rate0"] / strain_rate) if dEb > 0 else np.inf
    low = 1 - x ** (2 / 3) if np.isfinite(x) else -np.inf
    ratio = low if low >= p["switch_ratio"] else np.exp(-x / p["high_T_factor"])
    return {"sigma_y_MPa": float(p["taylor_M"] * tau0 * ratio / 1e6), "tau_y0_MPa": float(tau0 / 1e6),
            "dEb_eV": float(dEb / 1.602176634e-19), "delta_V_rms_A3": float(np.sqrt(misfit_V2) * 1e30),
            "mu_GPa": float(mu / 1e9), "nu": float(nu), "b_A": float(b * 1e10), "regime": "low_T" if low >= p["switch_ratio"] else "high_T"}
