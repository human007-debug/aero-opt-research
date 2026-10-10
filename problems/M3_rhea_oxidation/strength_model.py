"""Yield-strength surrogate for single-phase BCC refractory alloys: physics, data-driven and hybrid.

    python -m problems.M3_rhea_oxidation.strength_model     # validation study -> data/strength_validation.{json,md}

Data: single-phase BCC compression tests from the MPEA dataset (Borg et al. 2020), restricted to the
elements covered by the physics model (properties.STRENGTH_ELEMENTS), duplicates of (formula, T, YS)
removed (compilation papers repeat earlier measurements).

Models (target log10 sigma_y):
  physics      reduced Maresca-Curtin edge model (properties.strength), no fitting. Evaluated only on the
               Mo-Nb-Ta-V-W alloys, the family for which the paper provides validated inputs.
  ml           GP on composition and T, all alloys
Validation: random rows vs whole alloys held out (as for oxidation), repeated with random group folds.
A hybrid (physics prediction as a GP feature) is not possible across the design space, because the physics
model has no validated inputs for Al, Cr, Hf, Ti, Zr.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel, WhiteKernel
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from . import properties as pr
from .oxidation_model import group_folds

HERE = Path(__file__).parent
RAW = HERE / "data" / "raw" / "MPEA_dataset.csv"
EL = pr.STRENGTH_ELEMENTS
FLOOR_MPA = 10.0


def parse_formula(f: str) -> dict[str, float]:
    return {m[0]: float(m[1]) for m in re.findall(r"([A-Z][a-z]?)([\d.]+)", f)}


def load() -> pd.DataFrame:
    df = pd.read_csv(RAW)
    df.columns = [c.split(": ")[1] if ": " in c else c for c in df.columns]
    df = df.rename(columns={"Test temperature ($^\\circ$C)": "T_C", "YS (MPa)": "YS"})
    df["comp"] = df["FORMULA"].map(parse_formula)
    keep = (df["comp"].map(lambda c: set(c) <= set(EL)) & (df["Microstructure"] == "BCC")
            & (df["Type of test"] == "C") & df["YS"].notna() & df["T_C"].notna())
    d = df[keep].drop_duplicates(["FORMULA", "T_C", "YS"]).reset_index(drop=True)
    d["T_K"] = d["T_C"] + 273.15
    in_mc = d["comp"].map(lambda c: set(c) <= set(pr.MC_ELEMENTS))
    d["sigma_mc"] = [pr.strength(c, T)["sigma_y_MPa"] if ok else np.nan
                     for c, T, ok in zip(d["comp"], d["T_K"], in_mc)]
    return d


def comp_matrix(comps) -> np.ndarray:
    M = np.array([[c.get(e, 0.0) for e in EL] for c in comps], float)
    return M / M.sum(1, keepdims=True)


def features(comps, T_K, kind="ml") -> np.ndarray:
    return np.column_stack([comp_matrix(comps), np.asarray(T_K, float) / 1000])


def gp(n):
    return make_pipeline(StandardScaler(), GaussianProcessRegressor(
        ConstantKernel(1.0) * RBF(np.ones(n), length_scale_bounds=(1e-2, 1e5)) + WhiteKernel(0.02),
        normalize_y=True, random_state=0))


def cross_validate(d: pd.DataFrame, model: str, split: str, repeats: int = 3, k: int = 5,
                   score_rows: np.ndarray | None = None) -> dict:
    """score_rows: optional boolean mask; train on all of d but score only these rows."""
    y = np.log10(d["YS"].to_numpy())
    groups = np.arange(len(d)) if split == "rows" else pd.factorize(d["FORMULA"])[0]
    k = min(k, int(groups.max()) + 1)  # leave-one-group-out when there are few groups
    rmse, r2, cov, rz = [], [], [], []
    for rep in range(repeats):
        pred, sd = np.empty_like(y), np.full_like(y, np.nan)
        if model == "physics":
            pred = np.log10(np.maximum(d["sigma_mc"].to_numpy(), FLOOR_MPA))
        else:
            X = features(d["comp"], d["T_K"])
            for tr, te in group_folds(groups, k, np.random.default_rng(rep)):
                m = gp(X.shape[1]).fit(X[tr], y[tr])
                pred[te], sd[te] = m.predict(X[te], return_std=True)
        sel = np.ones(len(y), bool) if score_rows is None else np.asarray(score_rows)
        e = (pred - y)[sel]
        rmse.append(float(np.sqrt(np.mean(e**2))))
        r2.append(float(1 - np.mean(e**2) / np.var(y[sel])))
        if not np.isnan(sd).all():
            z = np.abs(e) / sd[sel]
            cov.append(float(np.mean(z <= 1.645)))
            rz.append(float(np.sqrt(np.mean(z**2))))
    out = {"model": model, "split": split, "n": int(len(d) if score_rows is None else np.sum(score_rows)), "rmse_mean": float(np.mean(rmse)),
           "rmse_sd": float(np.std(rmse)), "r2_mean": float(np.mean(r2))}
    if cov:
        out.update(coverage90_mean=float(np.mean(cov)), rms_z_mean=float(np.mean(rz)))
    return out


def validation_study() -> dict:
    d = load()
    res = {"n_rows": len(d), "n_alloys": int(d["FORMULA"].nunique()),
           "target_std_log10": float(np.log10(d["YS"]).std()), "results": []}
    mc = d[d["sigma_mc"].notna()].reset_index(drop=True)
    res["mc_family"] = {"n_rows": int(len(mc)), "n_alloys": int(mc["FORMULA"].nunique())}
    in_mc = d["sigma_mc"].notna().to_numpy()
    for split, data, model, rows in (("rows", d, "ml", None), ("alloy", d, "ml", None), ("none (no fitting)", mc, "physics", None),
                                     ("alloy", d, "ml", in_mc)):
        if True:
            r = cross_validate(data, model, split, score_rows=rows)
            r["subset"] = "Mo-Nb-Ta-V-W" if (data is mc or rows is not None) else "all"
            res["results"].append(r)
            print(f"{split:6s} {r['subset']:12s} {model:8s} RMSE {r['rmse_mean']:.3f}±{r['rmse_sd']:.3f} R2 {r['r2_mean']:.3f}"
                  + (f" cover90 {r['coverage90_mean']:.2f} rms_z {r['rms_z_mean']:.2f}" if "coverage90_mean" in r else ""),
                  flush=True)
    return res


def write_report(res: dict, path: Path):
    lines = ["# Strength surrogate validation", "",
             f"Data: {res['n_rows']} single-phase BCC compression records, {res['n_alloys']} alloys (MPEA dataset). "
             f"Target log10 sigma_y, std {res['target_std_log10']:.3f}.", "",
             "Physics model: reduced Maresca-Curtin (2020) edge model with the paper's own inputs, applicable to "
             f"Mo-Nb-Ta-V-W only ({res['mc_family']['n_rows']} records, {res['mc_family']['n_alloys']} alloys in the data). "
             "The Mo-Nb-Ta-V-W ml row is the all-alloy grouped CV scored on those records only (GP trained on all other alloys).", "",
             "| Subset | Split | Model | RMSE (log10) | R² | 90% coverage | RMS z |", "|---|---|---|---|---|---|---|"]
    for r in res["results"]:
        lines.append(f"| {r['subset']} | {r['split']} | {r['model']} | {r['rmse_mean']:.3f} ± {r['rmse_sd']:.3f} | {r['r2_mean']:.3f} | "
                     f"{r.get('coverage90_mean', float('nan')):.2f} | {r.get('rms_z_mean', float('nan')):.2f} |")
    path.write_text("\n".join(lines).replace("| nan |", "|  |") + "\n")


def fit(kind: str = "ml", d: pd.DataFrame | None = None):
    d = load() if d is None else d
    X = features(d["comp"], d["T_K"])
    return gp(X.shape[1]).fit(X, np.log10(d["YS"].to_numpy()))


if __name__ == "__main__":
    res = validation_study()
    (HERE / "data" / "strength_validation.json").write_text(json.dumps(res, indent=2))
    write_report(res, HERE / "data" / "strength_validation.md")
