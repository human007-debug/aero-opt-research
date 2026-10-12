"""Confidence intervals for the headline numbers of the methods paper (papers/rhea_ml_validation).

    python -m problems.M3_rhea_oxidation.paper_stats [--refit]

Intervals are 95% percentile intervals from a clustered bootstrap (B = 2000): whole clusters are resampled,
because rows of one alloy (different T, t) or one curve are correlated. Cluster units:
  internal CV, rows/alloy splits -> alloy;  internal CV, source split -> source paper
  external RefOxDB test          -> composition
  digitisation agreement         -> RefOxDB curve
  Pareto-front cross-scoring     -> optimiser seed (10 independent runs; reported as mean and range)
Out-of-fold predictions (3 repeats x 5 folds, as in oxidation_model.py) are cached in
data/paper_oof.npz so the bootstrap and figures can be rerun without refitting.
Writes data/paper_stats.json.
"""
from __future__ import annotations

import argparse
import copy
import glob
import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

from . import oxidation_model as ox
from . import refoxdb as rx

HERE = Path(__file__).parent
OOF = HERE / "data" / "paper_oof.npz"
OUT = HERE / "data" / "paper_stats.json"
MODELS = ("bayes_ridge", "gbdt", "gp")
SPLITS = ("rows", "alloy", "source")
B = 2000
LN10 = np.log(10)


# ---------------------------------------------------------------- out-of-fold predictions
def _oof(model: str, split: str, repeats: int = 3, k: int = 5):
    df = ox.load()
    X, y = ox.xy(df, "base")
    groups = {"rows": np.arange(len(y)), "alloy": ox.alloy_groups(df), "source": ox.source_groups(df)}[split]
    P, S = np.empty((repeats, len(y))), np.full((repeats, len(y)), np.nan)
    D = np.empty((repeats, len(y)))
    C = df[ox.ELEMENTS].to_numpy() / 100
    for rep in range(repeats):
        for tr, te in ox.group_folds(groups, k, np.random.default_rng(rep)):
            m = ox.make_model(model, X.shape[1]).fit(X[tr], y[tr])
            if model in ox.PROBABILISTIC:
                P[rep, te], S[rep, te] = m.predict(X[te], return_std=True)
            else:
                P[rep, te] = m.predict(X[te])
            U = np.unique(C[tr], axis=0)
            D[rep, te] = np.abs(C[te][:, None, :] - U[None]).sum(-1).min(1) * 50
    return model, split, P, S, D


def compute_oof(workers: int = 4):
    out = {}
    with ProcessPoolExecutor(workers) as pool:
        for model, split, P, S, D in pool.map(_oof, *zip(*[(m, s) for m in MODELS for s in SPLITS])):
            out[f"{model}|{split}|pred"], out[f"{model}|{split}|sd"], out[f"{model}|{split}|dist"] = P, S, D
            print("oof done", model, split, flush=True)
    np.savez_compressed(OOF, **out)


# ---------------------------------------------------------------- bootstrap helpers
def cluster_index(clusters: np.ndarray):
    uniq, inv = np.unique(clusters, return_inverse=True)
    members = [np.flatnonzero(inv == i) for i in range(len(uniq))]
    return members


def boot(stat, members, rng, n_boot=B):
    """Percentile CI of stat(idx) over cluster resamples; stat receives row indices."""
    vals = []
    for _ in range(n_boot):
        pick = rng.integers(0, len(members), len(members))
        vals.append(stat(np.concatenate([members[i] for i in pick])))
    vals = np.array(vals)
    return vals


def ci(vals):
    return [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]


def r2(y, p):
    return 1 - np.mean((p - y) ** 2) / np.var(y)


# ---------------------------------------------------------------- internal CV
def internal(rng):
    df = ox.load()
    _, y = ox.xy(df, "base")
    z = np.load(OOF)
    res = {}
    for split in SPLITS:
        clusters = ox.source_groups(df) if split == "source" else ox.alloy_groups(df)
        members = cluster_index(clusters)
        idx_all = np.arange(len(y))
        res[split] = {}
        draws = {}
        for m in MODELS:
            P, S = z[f"{m}|{split}|pred"], z[f"{m}|{split}|sd"]
            r2_fn = lambda idx, P=P: np.mean([r2(y[idx], P[k, idx]) for k in range(len(P))])
            mae_fn = lambda idx, P=P: np.mean(np.abs(P[:, idx] - y[idx])) * LN10
            v_r2, v_mae = boot(r2_fn, members, rng), boot(mae_fn, members, rng)
            draws[m] = v_mae
            e = {"r2": float(r2_fn(idx_all)), "r2_ci": ci(v_r2), "mae_ln": float(mae_fn(idx_all)), "mae_ln_ci": ci(v_mae)}
            if not np.isnan(S).all():
                cov_fn = lambda idx, P=P, S=S: np.mean(np.abs(P[:, idx] - y[idx]) <= 1.645 * S[:, idx])
                e.update(coverage90=float(cov_fn(idx_all)), coverage90_ci=ci(boot(cov_fn, members, rng)))
            res[split][m] = e
        res[split]["ranking"] = pairwise(draws, members, rng, y, z, split)
    # error vs distance, alloy split
    members = cluster_index(ox.alloy_groups(df))
    bins = (0, 5, 10, 15, 20, 30, 100)
    res["by_distance"] = {}
    for m in MODELS:
        P, D = z[f"{m}|alloy|pred"], z[f"{m}|alloy|dist"]
        AE = np.abs(P - y) * LN10
        rows = []
        for lo, hi in zip(bins[:-1], bins[1:]):
            sel = (D >= lo) & (D < hi)
            f = lambda idx, sel=sel: AE[:, idx][sel[:, idx]].mean() if sel[:, idx].any() else np.nan
            v = boot(f, members, rng)
            rows.append({"lo": lo, "hi": hi, "n": int(sel.sum() / len(P)), "mae_ln": float(f(np.arange(len(y)))),
                         "ci": ci(v[~np.isnan(v)])})
        res["by_distance"][m] = rows
    return res


def pairwise(draws, members, rng, y, z, split):
    """P(model A has lower MAE than B) from paired bootstrap (same cluster draws for all models)."""
    out = {}
    names = list(draws)
    # recompute with shared draws so the comparison is paired
    P = {m: z[f"{m}|{split}|pred"] for m in names}
    wins = {f"{a}<{b}": 0 for a in names for b in names if a < b}
    for _ in range(B):
        pick = rng.integers(0, len(members), len(members))
        idx = np.concatenate([members[i] for i in pick])
        mae = {m: np.mean(np.abs(P[m][:, idx] - y[idx])) for m in names}
        for key in wins:
            a, b = key.split("<")
            wins[key] += mae[a] < mae[b]
    for key, w in wins.items():
        out[f"P({key.replace('<', ' beats ')})"] = w / B
    return out


# ---------------------------------------------------------------- external test
def external(rng):
    g = ox.load()
    r = pd.read_csv(rx.OUT)
    new = r[~r["in_gorsse"]].reset_index(drop=True)
    Xg, yg = ox.xy(g, "base")
    Xn, yn = ox.xy(new, "base")
    U = np.unique(g[ox.ELEMENTS].to_numpy() / 100, axis=0)
    dist = np.abs(new[ox.ELEMENTS].to_numpy(float)[:, None, :] / 100 - U[None]).sum(-1).min(1) * 50
    members = cluster_index(new[ox.ELEMENTS].round(1).astype(str).agg("|".join, axis=1).to_numpy())
    preds, sds = {}, {}
    for m in MODELS:
        model = ox.make_model(m, Xg.shape[1]).fit(Xg, yg)
        if m in ox.PROBABILISTIC:
            preds[m], sds[m] = model.predict(Xn, return_std=True)
        else:
            preds[m], sds[m] = model.predict(Xn), None
    res = {"n_points": int(len(new)), "n_compositions": len(members), "models": {}, "ranking": {}}
    allidx = np.arange(len(yn))
    bins = (0, 5, 10, 20, 100)
    for m in MODELS:
        p = preds[m]
        e = {"r2": float(r2(yn, p)), "r2_ci": ci(boot(lambda i: r2(yn[i], p[i]), members, rng)),
             "mae_ln": float(np.mean(np.abs(p - yn)) * LN10),
             "mae_ln_ci": ci(boot(lambda i: np.mean(np.abs(p[i] - yn[i])) * LN10, members, rng))}
        if sds[m] is not None:
            s = sds[m]
            e.update(coverage90=float(np.mean(np.abs(p - yn) <= 1.645 * s)),
                     coverage90_ci=ci(boot(lambda i: np.mean(np.abs(p[i] - yn[i]) <= 1.645 * s[i]), members, rng)))
        rows = []
        for lo, hi in zip(bins[:-1], bins[1:]):
            sel = (dist >= lo) & (dist < hi)
            if not sel.any():
                continue
            f = lambda i, sel=sel: np.mean(np.abs(p[i] - yn[i])[sel[i]]) * LN10 if sel[i].any() else np.nan
            v = boot(f, members, rng)
            rows.append({"lo": lo, "hi": hi, "n": int(sel.sum()), "n_compositions": int(len({tuple(new.loc[j, ox.ELEMENTS].round(1)) for j in np.flatnonzero(sel)})),
                         "mae_ln": float(f(allidx)), "ci": ci(v[~np.isnan(v)])})
        e["by_distance"] = rows
        res["models"][m] = e
    wins = {"gp<bayes_ridge": 0, "gbdt<bayes_ridge": 0, "gp<gbdt": 0}
    for _ in range(B):
        pick = rng.integers(0, len(members), len(members))
        i = np.concatenate([members[j] for j in pick])
        mae = {m: np.mean(np.abs(preds[m][i] - yn[i])) for m in MODELS}
        for key in wins:
            a, b = key.split("<")
            wins[key] += mae[a] < mae[b]
    res["ranking"] = {f"P({k.replace('<', ' beats ')})": v / B for k, v in wins.items()}
    res["_predictions"] = {"y": yn.tolist(), "dist": dist.tolist(), **{m: preds[m].tolist() for m in MODELS}}
    return res


# ---------------------------------------------------------------- digitisation agreement
def agreement(rng):
    g = ox.load()
    r = pd.read_csv(rx.OUT)
    gk = g.assign(k=g["source"].map(rx.doi_key))
    d, cur = [], []
    for _, row in r[r["in_gorsse"]].iterrows():
        c = gk[(gk["k"] == rx.doi_key(row["source"])) & (abs(gk[ox.T_COL] - row[ox.T_COL]) < 5) & (gk[ox.t_COL] == row[ox.t_COL])]
        c = c[np.abs(c[ox.ELEMENTS].to_numpy() - row[ox.ELEMENTS].to_numpy(float)).max(1) <= 2.0]
        if len(c):
            d.append(np.log10(row[ox.Y_COL]) - np.log10(c[ox.Y_COL].to_numpy()).mean())
            cur.append(row["curve"])
    d, cur = np.array(d), np.array(cur)
    members = cluster_index(cur)
    mad = lambda i: np.median(np.abs(d[i]))
    x2 = lambda i: np.mean(np.abs(d[i]) > np.log10(2))
    return {"pairs": int(len(d)), "curves": len(members), "median_abs_log10": float(mad(np.arange(len(d)))),
            "median_abs_log10_ci": ci(boot(mad, members, rng)), "frac_over_x2": float(x2(np.arange(len(d)))),
            "frac_over_x2_ci": ci(boot(x2, members, rng)), "_diffs": d.tolist()}


# ---------------------------------------------------------------- optimiser's curse, per seed
def curse_per_seed():
    from . import evaluator as ev
    from .search import config, nondominated
    runs = {"gp": "m3x_pareto", "gbdt": "m3x_pareto_gbdt", "bayes_ridge": "m3x_pareto_bayes_ridge"}
    cfg0 = config()
    out = {}
    for own, run in runs.items():
        fr = {b: [] for b in runs if b != own}
        for f in sorted(glob.glob(str(HERE / "runs" / run / "nsga2" / "seed_*" / "evaluations.jsonl"))):
            df = pd.DataFrame([json.loads(l) for l in open(f)])
            df = df[df.feasible]
            F = np.column_stack([-df.specific_strength, df.log10_mass_gain])
            front = df.iloc[nondominated(F)]
            C = np.array([[c.get(e, 0.0) for e in ev.ELEMENTS] for c in front.composition])
            for b in fr:
                cfg = copy.deepcopy(cfg0)
                cfg["surrogates"]["oxidation"] = b
                other = ev.predict(C, cfg)["log_mass_gain"]
                fr[b].append(float(np.mean(other - front.log10_mass_gain.to_numpy() > np.log10(3))))
        out[own] = {b: {"mean": float(np.mean(v)), "min": float(np.min(v)), "max": float(np.max(v)), "seeds": len(v)}
                    for b, v in fr.items()}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refit", action="store_true")
    args = ap.parse_args()
    if args.refit or not OOF.exists():
        compute_oof()
    rng = np.random.default_rng(20261012)
    from core.repro import environment_info
    res = {"seed": 20261012, "environment": environment_info(), "bootstrap_draws": B, "internal": internal(rng), "external": external(rng), "agreement": agreement(rng),
           "curse_frac_other_3x_worse": curse_per_seed()}
    OUT.write_text(json.dumps(res, indent=1))
    print("written", OUT)


if __name__ == "__main__":
    main()
