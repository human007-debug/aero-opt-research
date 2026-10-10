"""C6: how much does the predicted Pareto front depend on the oxidation surrogate?

    python -m problems.M3_rhea_oxidation.surrogate_dependence

Uses the NSGA-II runs made with each oxidation surrogate (runs/m3x_pareto{,_gbdt,_bayes_ridge}). For each
front: (i) cross-score its compositions with the other surrogates; (ii) distance of each front point to the
nearest front point of the other surrogates' fronts; (iii) expected error of each point from its distance
to the oxidation data, using the external (RefOxDB) error-vs-distance curve of the GP.
Writes data/surrogate_dependence.json and runs/surrogate_dependence.png.
"""
from __future__ import annotations

import copy
import glob
import json
from pathlib import Path

import numpy as np
import pandas as pd

from . import evaluator as ev
from .search import config, nondominated

HERE = Path(__file__).parent
RUNS = {"gp": "m3x_pareto", "gbdt": "m3x_pareto_gbdt", "bayes_ridge": "m3x_pareto_bayes_ridge"}


def front(run: str) -> pd.DataFrame:
    recs = [json.loads(l) for f in sorted(glob.glob(str(HERE / "runs" / run / "nsga2" / "seed_*" / "evaluations.jsonl")))
            for l in open(f)]
    df = pd.DataFrame([r for r in recs if r["feasible"]])
    F = np.column_stack([-df.specific_strength, df.log10_mass_gain])
    f = df.iloc[nondominated(F)].sort_values("specific_strength").reset_index(drop=True)
    f["C"] = [np.array([r.get(e, 0.0) for e in ev.ELEMENTS]) for r in f.composition]
    return f


def score(C: np.ndarray, model: str) -> np.ndarray:
    cfg = copy.deepcopy(config())
    cfg["surrogates"]["oxidation"] = model
    return ev.predict(C, cfg)["log_mass_gain"]


def expected_error_log10(dist: np.ndarray) -> np.ndarray:
    ext = json.loads((HERE / "data" / "refoxdb_external_test.json").read_text())["external"]["models"]["gp"]["by_distance"]
    out = np.empty_like(dist)
    for i, d in enumerate(dist):
        b = next((b for b in ext if b["lo"] <= d < b["hi"]), ext[-1])
        out[i] = b["mae_ln"] / np.log(10)
    return out


def main():
    fronts = {m: front(r) for m, r in RUNS.items()}
    res = {"fronts": {}}
    for a, fa in fronts.items():
        C = np.vstack(fa.C)
        own = fa.log10_mass_gain.to_numpy()
        entry = {"n_points": int(len(fa)), "specific_strength_range": [float(fa.specific_strength.min()), float(fa.specific_strength.max())],
                 "own_log10_mass_gain_range": [float(own.min()), float(own.max())],
                 "distance_to_ox_data_median": float(np.median(fa.ox_distance_at_pct)),
                 "expected_abs_error_log10_median": float(np.median(expected_error_log10(fa.ox_distance_at_pct.to_numpy()))),
                 "cross_scored": {}, "nearest_point_in_other_front_at_pct": {}}
        for b, fb in fronts.items():
            if b == a:
                continue
            other = score(C, b)
            entry["cross_scored"][b] = {"median_abs_diff_log10": float(np.median(np.abs(other - own))),
                                        "frac_other_predicts_3x_worse": float(np.mean(other - own > np.log10(3))),
                                        "spearman_rank_along_front": float(pd.Series(own).corr(pd.Series(other), method="spearman"))}
            Cb = np.vstack(fb.C)
            entry["nearest_point_in_other_front_at_pct"][b] = float(np.median(np.abs(C[:, None, :] - Cb[None]).sum(-1).min(1) * 50))
        res["fronts"][a] = entry
    (HERE / "data" / "surrogate_dependence.json").write_text(json.dumps(res, indent=2))
    plot(fronts)
    print(json.dumps(res, indent=1))


def plot(fronts):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7, 4.6))
    for name, f in fronts.items():
        err = expected_error_log10(f.ox_distance_at_pct.to_numpy())
        ax.plot(f.specific_strength, f.log10_mass_gain, "-", lw=1.5, label=f"front with {name} oxidation model")
        ax.fill_between(f.specific_strength, f.log10_mass_gain - err, f.log10_mass_gain + err, alpha=0.12)
    ax.set_xlabel("predicted specific yield strength at 1000 C (MPa cm³/g)")
    ax.set_ylabel("predicted log10 mass gain, 1000 C / 20 h")
    ax.set_title("Pareto fronts by oxidation surrogate; bands = expected external error")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(HERE / "runs" / "surrogate_dependence.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
