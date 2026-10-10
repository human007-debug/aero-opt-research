"""M3X: refractory alloy composition for high-temperature specific strength and oxidation resistance.

design      at. fractions of ELEMENTS (normalised inside; values below `min_fraction` are set to zero)
objective   minimise -[ sigma_y(T) / rho ]  (specific yield strength, MPa cm^3 / g)
constraints oxidation:   log10 mass gain (mg/cm^2) at (T_ox, t_ox) - limit <= 0
            phase:       0.5 - P(single-phase BCC) <= 0
            trust_strength:  calibrated strength sd - max_sd_log_strength <= 0
            trust_oxidation: distance (at.% moved) to the nearest oxidation-tested alloy - max <= 0.
                         Oxidation surrogate: GP (best and best-calibrated on the external RefOxDB test).
                         Both limits = 75th percentile of the same quantity for held-out known alloys.
metadata    predictions, their sd, density, physics-model strength (for reference)

All three surrogates are data-driven and validated on held-out alloys (see data/*_validation.md).
Results are predictions for candidate alloys, not measured properties.
"""
from __future__ import annotations

from functools import lru_cache
from typing import Any, Sequence

import numpy as np

from . import oxidation_model as ox
from . import phase_model as ph
from . import properties as pr
from . import strength_model as st

ELEMENTS = pr.STRENGTH_ELEMENTS  # Al Cr Hf Mo Nb Ta Ti V W Zr


@lru_cache(maxsize=1)
def oxidation_alloys() -> np.ndarray:
    """Distinct oxidation-tested compositions (fractions, ox.ELEMENTS order)."""
    df = ox.load()
    return np.unique(np.round(df[ox.ELEMENTS].to_numpy() / 100, 4), axis=0)


def distance_to_oxidation_data(C_ox: np.ndarray) -> np.ndarray:
    U = oxidation_alloys()
    return np.abs(C_ox[:, None, :] - U[None, :, :]).sum(-1).min(1) * 100 / 2


@lru_cache(maxsize=4)
def models(oxidation_model: str = "gp"):
    s_model = st.fit("ml")
    o_model, o_kind = ox.fit(oxidation_model, "base")
    p_model = ph.fit("logistic")
    return s_model, (o_model, o_kind), p_model


def ox_model_has_std(m) -> bool:
    est = m.steps[-1][1] if hasattr(m, "steps") else m
    return type(est).__name__ in ("GaussianProcessRegressor", "BayesianRidge")


def normalise(design: Sequence[float], min_fraction: float) -> np.ndarray:
    x = np.clip(np.asarray(design, float), 0, None)
    if x.sum() <= 0:
        return np.full(len(x), 1 / len(x))
    x = x / x.sum()
    x[x < min_fraction] = 0.0
    return x / x.sum()


def predict(C: np.ndarray, config: dict[str, Any]) -> dict[str, np.ndarray]:
    """Batch predictions for compositions C (n, len(ELEMENTS)) at the configured conditions."""
    s_model, (o_model, o_kind), p_model = models(config.get("surrogates", {}).get("oxidation", "gp"))
    cond = config["conditions"]
    n = len(C)
    comps = [dict(zip(ELEMENTS, c)) for c in C]
    Xs = st.features(comps, np.full(n, cond["T_strength_C"] + 273.15), kind="ml")
    ls, ls_sd = s_model.predict(Xs, return_std=True)
    C_ox = np.zeros((n, len(ox.ELEMENTS)))
    for j, e in enumerate(ELEMENTS):
        C_ox[:, ox.ELEMENTS.index(e)] = C[:, j]
    Xo = ox.features(C_ox, np.full(n, cond["T_ox_C"]), np.full(n, cond["t_ox_h"]), o_kind)
    if hasattr(o_model, "predict") and ox_model_has_std(o_model):
        lo, lo_sd = o_model.predict(Xo, return_std=True)
    else:
        lo, lo_sd = o_model.predict(Xo), np.full(n, np.nan)
    p_bcc = p_model.predict_proba(ph.descriptors(C))[:, 1]
    d_ox = distance_to_oxidation_data(C_ox)
    rho = np.array([pr.density(c) for c in comps])
    cal = config["uncertainty_calibration"]
    return {"log_sigma": ls, "log_sigma_sd": ls_sd * cal["strength"], "sigma_MPa": 10**ls,
            "log_mass_gain": lo, "log_mass_gain_sd": lo_sd * cal["oxidation"], "ox_distance_at_pct": d_ox,
            "p_bcc": p_bcc, "density": rho,
            "specific_strength": 10**ls / rho}


def evaluate(design: Sequence[float], config: dict[str, Any]):
    from core.problem import EvalResult
    C = normalise(design, config["design"]["min_fraction"])[None, :]
    p = {k: float(v[0]) for k, v in predict(C, config).items()}
    lim = config["constraints"]
    constraints = {
        "oxidation": p["log_mass_gain"] - lim["log10_mass_gain_max"],
        "phase": lim["p_bcc_min"] - p["p_bcc"],
        "trust_strength": p["log_sigma_sd"] - lim["max_sd_log_strength"],
        "trust_oxidation": p["ox_distance_at_pct"] - lim["max_ox_distance_at_pct"],
    }
    return EvalResult(objective=-p["specific_strength"], constraints=constraints,
                      feasible=all(v <= 0 for v in constraints.values()),
                      metadata={**p, "composition": {e: round(float(c), 4) for e, c in zip(ELEMENTS, C[0]) if c > 0}})


def search_space(config: dict[str, Any]) -> dict[str, Any]:
    n = len(ELEMENTS)
    return {"type": "continuous", "lower": [0.0] * n, "upper": [1.0] * n, "x0": [1.0 / n] * n,
            "names": ELEMENTS}
