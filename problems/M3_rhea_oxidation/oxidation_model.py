"""Oxidation surrogate: log10 specific mass gain from composition, temperature and time.

    python -m problems.M3_rhea_oxidation.oxidation_model      # validation study -> data/oxidation_validation.{json,md}

Trained on the audited dataset (data/oxidation_clean.csv, see data_audit.py).

Validation is the point of this module. Rows of the dataset are time and temperature points of the
same alloy, so a random row split puts every alloy in both training and test sets. For alloy design
the relevant question is accuracy on compositions that were never tested, so models are compared
under three splits, each repeated with different random group assignments:
  rows    random rows                      (interpolation within known alloys)
  alloy   all rows of an alloy held out    (new composition)
  source  all rows of a publication held out (new composition and new laboratory)
The noise floor is the pooled scatter of repeated (composition, T, t) measurements.

Feature sets
  base     11 at. fractions, 1000/T (K), log10 t (h)
  physics  base + group sums of scale-forming (Al, Cr, Si), volatile / low-melting-oxide forming
           (Mo, W, V) and non-protective-oxide forming (Nb, Ta, Ti, Zr, Hf) elements, the Cr x Ta
           product (CrTaO4 scale), and the interactions of those sums with 1000/T and log10 t.
           The element groupings are qualitative literature knowledge, not fitted numbers.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel, WhiteKernel
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).parent
CLEAN = HERE / "data" / "oxidation_clean.csv"
ELEMENTS = ["Al", "Cr", "Hf", "Mo", "Nb", "Si", "Ta", "Ti", "V", "W", "Zr"]
T_COL, t_COL, Y_COL = "Temperature (C)", "time (h)", "specific mass gain (mg/cm2)"
SCALE_FORMERS = ["Al", "Cr", "Si"]
VOLATILE = ["Mo", "W", "V"]
NONPROTECTIVE = ["Nb", "Ta", "Ti", "Zr", "Hf"]


def load(path: Path = CLEAN) -> pd.DataFrame:
    return pd.read_csv(path)


def features(comp: np.ndarray, T_C: np.ndarray, t_h: np.ndarray, kind: str = "physics") -> np.ndarray:
    """comp: (n, 11) at. fractions in ELEMENTS order (sum 1)."""
    comp = np.asarray(comp, float)
    invT = 1000.0 / (np.asarray(T_C, float) + 273.15)
    lt = np.log10(np.asarray(t_h, float))
    base = np.column_stack([comp, invT, lt])
    if kind == "base":
        return base
    idx = {e: i for i, e in enumerate(ELEMENTS)}
    s = lambda els: comp[:, [idx[e] for e in els]].sum(1)
    sf, vo, npo = s(SCALE_FORMERS), s(VOLATILE), s(NONPROTECTIVE)
    crta = comp[:, idx["Cr"]] * comp[:, idx["Ta"]]
    extra = [sf, vo, npo, crta, sf * invT, vo * invT, npo * invT, sf * lt, vo * lt, npo * lt]
    return np.column_stack([base] + extra)


def xy(df: pd.DataFrame, kind: str = "physics"):
    X = features(df[ELEMENTS].to_numpy() / 100, df[T_COL].to_numpy(), df[t_COL].to_numpy(), kind)
    return X, np.log10(df[Y_COL].to_numpy())


def alloy_groups(df: pd.DataFrame) -> np.ndarray:
    return pd.factorize(df[ELEMENTS].round(2).astype(str).agg("|".join, axis=1))[0]


def source_groups(df: pd.DataFrame) -> np.ndarray:
    return pd.factorize(df["source"])[0]


MODELS = {
    "ridge": lambda: make_pipeline(StandardScaler(), Ridge(alpha=1.0)),
    "gbdt": lambda: HistGradientBoostingRegressor(max_iter=400, learning_rate=0.05, random_state=0),
    "gp": lambda: make_pipeline(StandardScaler(), GaussianProcessRegressor(
        ConstantKernel(1.0) * RBF(1.0) + WhiteKernel(0.05), normalize_y=True, random_state=0)),
    "gp_ard": lambda n: make_pipeline(StandardScaler(), GaussianProcessRegressor(
        ConstantKernel(1.0) * RBF(np.ones(n), length_scale_bounds=(1e-2, 1e6)) + WhiteKernel(0.05),
        normalize_y=True, random_state=0)),
}


def make_model(name: str, n_features: int):
    return MODELS[name](n_features) if name == "gp_ard" else MODELS[name]()


def group_folds(groups: np.ndarray, k: int, rng: np.random.Generator):
    """Random assignment of whole groups to k folds (unlike GroupKFold, varies with the seed)."""
    ug = np.unique(groups)
    fold_of = dict(zip(ug, rng.permutation(len(ug)) % k))
    f = np.array([fold_of[g] for g in groups])
    return [(np.flatnonzero(f != i), np.flatnonzero(f == i)) for i in range(k)]


def noise_floor(df: pd.DataFrame) -> dict:
    y = np.log10(df[Y_COL])
    g = y.groupby([df[e] for e in ELEMENTS] + [df[T_COL], df[t_COL]])
    n = g.transform("size")
    resid = (y - g.transform("mean"))[n > 1]
    dof = (n[n > 1] - 1) / n[n > 1]
    return {"groups": int((g.size() > 1).sum()), "rows": int((n > 1).sum()),
            "pooled_std_log10": float(np.sqrt(np.sum(resid**2) / np.sum(dof)))}


def cross_validate(df: pd.DataFrame, model: str, kind: str, split: str, repeats: int = 5, k: int = 5) -> dict:
    X, y = xy(df, kind)
    groups = {"rows": np.arange(len(y)), "alloy": alloy_groups(df), "source": source_groups(df)}[split]
    rmse, r2, cover90, z = [], [], [], []
    for rep in range(repeats):
        rng = np.random.default_rng(rep)
        pred, sd = np.empty_like(y), np.full_like(y, np.nan)
        for tr, te in group_folds(groups, k, rng):
            m = make_model(model, X.shape[1]).fit(X[tr], y[tr])
            if model.startswith("gp"):
                pred[te], sd[te] = m.predict(X[te], return_std=True)
            else:
                pred[te] = m.predict(X[te])
        e = pred - y
        rmse.append(float(np.sqrt(np.mean(e**2))))
        r2.append(float(1 - np.mean(e**2) / np.var(y)))
        if model.startswith("gp"):
            zz = np.abs(e) / sd
            cover90.append(float(np.mean(zz <= 1.645)))
            z.append(float(np.sqrt(np.mean(zz**2))))
    out = {"model": model, "features": kind, "split": split, "repeats": repeats, "folds": k,
           "rmse_mean": float(np.mean(rmse)), "rmse_sd": float(np.std(rmse)),
           "r2_mean": float(np.mean(r2)), "r2_sd": float(np.std(r2))}
    if cover90:
        out.update(coverage90_mean=float(np.mean(cover90)), rms_z_mean=float(np.mean(z)))
    return out


def validation_study(repeats: int = 3, workers: int = 4) -> dict:
    from concurrent.futures import ProcessPoolExecutor
    df = load()
    res = {"n_rows": len(df), "n_alloys": int(alloy_groups(df).max() + 1),
           "n_sources": int(source_groups(df).max() + 1),
           "target_std_log10": float(np.log10(df[Y_COL]).std()), "noise_floor": noise_floor(df), "results": []}
    configs = [(m, k, s) for s in ("rows", "alloy", "source") for k in ("base", "physics")
               for m in ("ridge", "gbdt", "gp", "gp_ard")]
    with ProcessPoolExecutor(workers) as pool:
        futs = [pool.submit(cross_validate, df, m, k, s, repeats) for m, k, s in configs]
        for f in futs:
            r = f.result()
            res["results"].append(r)
            print(f"{r['split']:6s} {r['features']:7s} {r['model']:6s} RMSE {r['rmse_mean']:.3f}±{r['rmse_sd']:.3f} "
                  f"R2 {r['r2_mean']:.3f}" + (f" cover90 {r['coverage90_mean']:.2f} rms_z {r['rms_z_mean']:.2f}"
                                              if "coverage90_mean" in r else ""), flush=True)
    return res


def write_report(res: dict, path_md: Path):
    nf = res["noise_floor"]
    lines = ["# Oxidation surrogate validation", "",
             f"Data: {res['n_rows']} rows, {res['n_alloys']} alloys, {res['n_sources']} sources "
             "(audited Gorsse et al. 2025 dataset). Target: log10 specific mass gain (mg/cm²), "
             f"std {res['target_std_log10']:.3f}.",
             f"Noise floor (pooled scatter of {nf['groups']} repeated composition/T/t groups): "
             f"{nf['pooled_std_log10']:.3f} log10.", "",
             "5-fold cross-validation, groups randomly assigned to folds, mean ± sd over repeats.", "",
             "| Split | Features | Model | RMSE (log10) | R² | 90% interval coverage | RMS z |", "|---|---|---|---|---|---|---|"]
    for r in res["results"]:
        cov = f"{r['coverage90_mean']:.2f}" if "coverage90_mean" in r else ""
        rz = f"{r['rms_z_mean']:.2f}" if "rms_z_mean" in r else ""
        lines.append(f"| {r['split']} | {r['features']} | {r['model']} | {r['rmse_mean']:.3f} ± {r['rmse_sd']:.3f} | "
                     f"{r['r2_mean']:.3f} | {cov} | {rz} |")
    path_md.write_text("\n".join(lines) + "\n")


def fit(model: str = "gp", kind: str = "physics", df: pd.DataFrame | None = None):
    """Fit on the full cleaned dataset; returns (model, kind)."""
    df = load() if df is None else df
    X, y = xy(df, kind)
    return make_model(model, X.shape[1]).fit(X, y), kind


if __name__ == "__main__":
    res = validation_study()
    (HERE / "data" / "oxidation_validation.json").write_text(json.dumps(res, indent=2))
    write_report(res, HERE / "data" / "oxidation_validation.md")
