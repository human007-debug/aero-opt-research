"""Two-objective composition search: specific strength (max) vs oxidation mass gain (min).

    python -m problems.M3_rhea_oxidation.search [--budget N] [--seeds S] [--out DIR]

Optimizers with equal evaluation budgets: NSGA-II (pymoo) and random search. Every evaluated
composition is logged. Hypervolume (in the normalised objective space below) is reported against the
number of evaluations, and the final fronts are compared with the known alloys of both datasets,
scored by the same surrogates.

Constraints: P(single-phase BCC) >= p_bcc_min, and both predictive sds within the trust limits
(problem.yaml). Mass gain is not constrained here; it is the second objective.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from . import evaluator as ev
from . import oxidation_model as ox
from . import strength_model as st

HERE = Path(__file__).parent
REF_POINT = np.array([0.0, 2.5])  # (-specific strength, log10 mass gain): worse than any useful alloy


def config() -> dict:
    return yaml.safe_load((HERE / "problem.yaml").read_text())


def batch(X: np.ndarray, cfg: dict) -> tuple[np.ndarray, np.ndarray, dict]:
    C = np.array([ev.normalise(x, cfg["design"]["min_fraction"]) for x in X])
    p = ev.predict(C, cfg)
    lim = cfg["constraints"]
    F = np.column_stack([-p["specific_strength"], p["log_mass_gain"]])
    G = np.column_stack([lim["p_bcc_min"] - p["p_bcc"], p["log_sigma_sd"] - lim["max_sd_log_strength"],
                         p["ox_distance_at_pct"] - lim["max_ox_distance_at_pct"]])
    return F, G, {**p, "C": C}


def hypervolume(F: np.ndarray) -> float:
    from pymoo.indicators.hv import HV
    F = F[np.all(F < REF_POINT, 1)]
    return float(HV(ref_point=REF_POINT)(F)) if len(F) else 0.0


def nondominated(F: np.ndarray) -> np.ndarray:
    from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting
    return NonDominatedSorting().do(F, only_non_dominated_front=True) if len(F) else np.array([], int)


class Log:
    def __init__(self, path: Path):
        self.f = open(path, "w")
        self.n = 0
        self.F, self.ok = [], []

    def add(self, F, G, p, source):
        for i in range(len(F)):
            self.n += 1
            feas = bool(np.all(G[i] <= 0))
            self.F.append(F[i]); self.ok.append(feas)
            self.f.write(json.dumps({"eval_id": self.n, "source": source, "feasible": feas,
                                     "composition": {e: round(float(c), 4) for e, c in zip(ev.ELEMENTS, p["C"][i]) if c > 0},
                                     "specific_strength": float(-F[i, 0]), "log10_mass_gain": float(F[i, 1]),
                                     "constraints": G[i].tolist(), "sigma_MPa": float(p["sigma_MPa"][i]),
                                     "density": float(p["density"][i]), "p_bcc": float(p["p_bcc"][i]),
                                     "log_sigma_sd": float(p["log_sigma_sd"][i]),
                                     "log_mass_gain_sd": float(p["log_mass_gain_sd"][i]),
                                     "ox_distance_at_pct": float(p["ox_distance_at_pct"][i])}) + "\n")

    def hv_curve(self, every: int = 50):
        F, ok = np.array(self.F), np.array(self.ok)
        return [(n, hypervolume(F[:n][ok[:n]])) for n in range(every, len(F) + 1, every)]


def run_random(cfg, budget, seed, log: Log, batch_size=100):
    rng = np.random.default_rng(seed)
    while log.n < budget:
        k = min(batch_size, budget - log.n)
        X = rng.dirichlet(np.ones(len(ev.ELEMENTS)) * 0.5, size=k)
        F, G, p = batch(X, cfg)
        log.add(F, G, p, "random")


def run_nsga2(cfg, budget, seed, log: Log, pop_size=100):
    from pymoo.algorithms.moo.nsga2 import NSGA2
    from pymoo.core.problem import Problem
    from pymoo.optimize import minimize

    class P(Problem):
        def __init__(self):
            super().__init__(n_var=len(ev.ELEMENTS), n_obj=2, n_ieq_constr=3, xl=0.0, xu=1.0)

        def _evaluate(self, X, out, *a, **k):
            F, G, p = batch(X, cfg)
            log.add(F, G, p, "nsga2")
            out["F"], out["G"] = F, G

    minimize(P(), NSGA2(pop_size=pop_size), termination=("n_eval", budget), seed=seed, verbose=False)


def known_alloys(cfg) -> pd.DataFrame:
    """Compositions present in either dataset (restricted to the design elements), scored by the surrogates."""
    comps = []
    for c in st.load()["comp"]:
        comps.append(c)
    o = pd.read_csv(ox.CLEAN)
    for _, r in o.iterrows():
        c = {e: r[e] for e in ox.ELEMENTS if r[e] > 0}
        if set(c) <= set(ev.ELEMENTS):
            comps.append(c)
    C = np.array([[c.get(e, 0.0) for e in ev.ELEMENTS] for c in comps], float)
    C = np.unique(np.round(C / C.sum(1, keepdims=True), 4), axis=0)
    F, G, p = batch(C, {**cfg, "design": {**cfg["design"], "min_fraction": 0.0}})
    return pd.DataFrame({"composition": [" ".join(f"{e}{c*100:.0f}" for e, c in zip(ev.ELEMENTS, row) if c > 0) for row in C],
                         "specific_strength": -F[:, 0], "log10_mass_gain": F[:, 1], "p_bcc": p["p_bcc"],
                         "log_sigma_sd": p["log_sigma_sd"], "log_mass_gain_sd": p["log_mass_gain_sd"],
                         "ox_distance_at_pct": p["ox_distance_at_pct"],
                         "density": p["density"], "sigma_MPa": p["sigma_MPa"], "feasible": np.all(G <= 0, 1)})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", type=int, default=5000)
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--out", type=Path, default=HERE / "runs" / "m3x_pareto")
    args = ap.parse_args()
    cfg = config()
    args.out.mkdir(parents=True, exist_ok=True)
    from core.repro import environment_info, seed_everything
    summary = {"budget": args.budget, "seeds": args.seeds, "conditions": cfg["conditions"],
               "constraints": cfg["constraints"], "environment": environment_info(), "runs": {}}
    fronts = {}
    for opt in ("random", "nsga2"):
        hvs, allF = [], []
        for s in range(args.seeds):
            seed_everything(s)
            d = args.out / opt / f"seed_{s:03d}"
            d.mkdir(parents=True, exist_ok=True)
            log = Log(d / "evaluations.jsonl")
            t0 = time.perf_counter()
            (run_random if opt == "random" else run_nsga2)(cfg, args.budget, s, log)
            curve = log.hv_curve()
            hvs.append(curve)
            F, ok = np.array(log.F), np.array(log.ok)
            allF.append(F[ok])
            print(f"{opt} seed {s}: {log.n} evals, feasible {ok.mean():.2f}, HV {curve[-1][1]:.3f}, "
                  f"{time.perf_counter() - t0:.0f} s", flush=True)
        summary["runs"][opt] = {"final_hv": [h[-1][1] for h in hvs], "hv_curves": hvs}
        fronts[opt] = np.vstack(allF)
    known = known_alloys(cfg)
    known.to_csv(args.out / "known_alloys_scored.csv", index=False)
    kf = known[known.feasible]
    summary["known_alloys"] = {"n": int(len(known)), "n_feasible": int(len(kf)),
                               "hv": hypervolume(kf[["specific_strength", "log10_mass_gain"]].to_numpy() * [-1, 1])}
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2))
    plot(args.out, fronts, known, summary)
    print(json.dumps({k: v for k, v in summary.items() if k != "environment"}, indent=1)[:2000])


def plot(out: Path, fronts: dict, known: pd.DataFrame, summary: dict):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.6))
    ax = axs[0]
    k = known[known.feasible]
    ax.scatter(known.specific_strength, known.log10_mass_gain, s=10, c="0.75", label="known alloys (outside constraints)")
    ax.scatter(k.specific_strength, k.log10_mass_gain, s=16, c="0.3", label="known alloys (feasible)")
    for name, F in fronts.items():
        idx = nondominated(F)
        P = F[idx][np.argsort(F[idx][:, 0])]
        ax.plot(-P[:, 0], P[:, 1], "o-", ms=3, label=f"{name} front (all seeds)")
    ax.set_xlabel("predicted specific yield strength at 1000 C (MPa cm³/g)")
    ax.set_ylabel("predicted log10 mass gain, 1000 C / 20 h (mg/cm²)")
    ax.legend(fontsize=8)
    ax.set_title("Surrogate-predicted trade-off (predictions, not measurements)")
    ax = axs[1]
    for name, r in summary["runs"].items():
        curves = np.array([[h for _, h in c] for c in r["hv_curves"]])
        n = [n for n, _ in r["hv_curves"][0]]
        ax.plot(n, np.median(curves, 0), label=f"{name} (median of {len(curves)})")
        ax.fill_between(n, curves.min(0), curves.max(0), alpha=0.2)
    ax.axhline(summary["known_alloys"]["hv"], color="k", ls="--", lw=1, label="known feasible alloys")
    ax.set_xlabel("evaluations")
    ax.set_ylabel("hypervolume")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "pareto.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
