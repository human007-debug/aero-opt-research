"""Run an experiment file: every optimizer x every seed with an equal evaluation budget.

    python -m core.run experiments/<name>.yaml [--report-only]

Runs are written to problems/<id>/runs/<experiment>/<optimizer>/seed_<n>/ and a summary
(summary.json, convergence.png, reliability.png) to problems/<id>/runs/<experiment>/.
Existing seed directories are skipped, so an interrupted experiment can be resumed.
"""
from __future__ import annotations

import argparse
import importlib
import json
import time
from pathlib import Path

import numpy as np
import yaml

from . import metrics, plots
from .problem import PROBLEMS_DIR
from .search import Problem, run


def load_experiment(path: Path) -> dict:
    with open(path) as f:
        exp = yaml.safe_load(f)
    exp["seeds"] = list(range(*exp["seeds"])) if isinstance(exp["seeds"], list) and len(exp["seeds"]) == 2 \
        and exp.get("seed_range", True) else exp["seeds"]
    return exp


def experiment_dir(exp: dict) -> Path:
    return PROBLEMS_DIR / exp["problem"] / "runs" / exp["name"]


def run_all(exp: dict, verbose: bool = True) -> None:
    problem = Problem(exp["problem"], exp.get("overrides"))
    for opt_name, spec in exp["optimizers"].items():
        optimize = importlib.import_module(spec["module"]).optimize
        for seed in exp["seeds"]:
            d = experiment_dir(exp) / opt_name / f"seed_{seed:03d}"
            if (d / "evaluations.jsonl").exists():
                continue
            t0 = time.perf_counter()
            f = run(problem, optimize, exp["budget"], seed, d, opt_name, spec.get("params"), exp.get("overrides"))
            if verbose:
                best = f.best[1].objective if f.best else float("inf")
                print(f"{opt_name:>10s} seed {seed:3d}: {f.n_evals} evals, best {best:.6g}, "
                      f"{time.perf_counter() - t0:.1f} s", flush=True)


def report(exp: dict) -> dict:
    out_dir = experiment_dir(exp)
    curves = {}
    for opt_name in exp["optimizers"]:
        dirs = sorted((out_dir / opt_name).glob("seed_*"))
        curves[opt_name] = np.array([metrics.best_so_far(d, exp["budget"]) for d in dirs])

    summary = {"experiment": exp["name"], "problem": exp["problem"], "budget": exp["budget"], "optimizers": {}}
    tgt = None
    if "optimum" in exp:
        tgt = metrics.target_from_optimum(exp["optimum"]["objective"], exp["optimum"]["rel_tol"])
        summary["target_objective"] = tgt
    for name, c in curves.items():
        final = c[:, -1]
        s = {"runs": int(c.shape[0]), "final_best_median": float(np.median(final)),
             "final_best_min": float(np.min(final)), "final_best_max": float(np.max(final))}
        if tgt is not None:
            s["price_80"] = metrics.price(c, tgt)
            s["reliability_at_budget"] = float(metrics.reliability(c, tgt)[-1])
        summary["optimizers"][name] = s
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))

    sign = exp.get("plot_sign", 1.0)
    label = exp.get("plot_label", "best feasible objective")
    opt = exp["optimum"]["objective"] if "optimum" in exp else None
    plots.convergence(curves, out_dir / "convergence.png", label, sign, opt, exp["name"])
    if tgt is not None:
        plots.reliability_plot(curves, tgt, out_dir / "reliability.png", exp["name"])
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("experiment", type=Path)
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()
    exp = load_experiment(args.experiment)
    if not args.report_only:
        run_all(exp)
    print(json.dumps(report(exp), indent=2))


if __name__ == "__main__":
    main()
