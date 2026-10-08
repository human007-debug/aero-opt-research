"""Run an experiment file: every optimizer x every seed with an equal evaluation budget.

    python -m core.run experiments/<name>.yaml [--report-only] [--workers N]

Runs are written to problems/<id>/runs/<experiment>/<optimizer>/seed_<n>/ and a summary
(summary.json and plots) to problems/<id>/runs/<experiment>/. Existing seed directories are
skipped, so an interrupted experiment can be resumed (delete a partial seed directory first).

Scoring:
  success: {...}  -> reliability / price from first-hit times (core.metrics.make_success)
  optimum: {...}  -> reliability / price from best-so-far vs an objective threshold
"""
from __future__ import annotations

import argparse
import importlib
import json
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import yaml

from . import metrics, plots
from .problem import PROBLEMS_DIR
from .search import Problem, run


def load_experiment(path: Path) -> dict:
    with open(path) as f:
        exp = yaml.safe_load(f)
    if isinstance(exp["seeds"], list) and len(exp["seeds"]) == 2:
        exp["seeds"] = list(range(*exp["seeds"]))
    return exp


def experiment_dir(exp: dict) -> Path:
    return PROBLEMS_DIR / exp["problem"] / "runs" / exp["name"]


def _one(exp: dict, opt_name: str, seed: int) -> str:
    spec = exp["optimizers"][opt_name]
    problem = Problem(exp["problem"], exp.get("overrides"))
    optimize = importlib.import_module(spec["module"]).optimize
    success = metrics.make_success(exp["success"]) if "success" in exp else None
    d = experiment_dir(exp) / opt_name / f"seed_{seed:03d}"
    t0 = time.perf_counter()
    f = run(problem, optimize, exp["budget"], seed, d, opt_name, spec.get("params"), exp.get("overrides"),
            success, exp.get("stop_on_success", False))
    best = f.best[1].objective if f.best else float("inf")
    return (f"{opt_name:>10s} seed {seed:3d}: {f.n_evals} evals, best {best:.6g}, hit {f.hit_at}, "
            f"{time.perf_counter() - t0:.1f} s")


def run_all(exp: dict, workers: int = 1, verbose: bool = True) -> None:
    todo = [(o, s) for o in exp["optimizers"] for s in exp["seeds"]
            if not (experiment_dir(exp) / o / f"seed_{s:03d}" / "evaluations.jsonl").exists()]
    if workers <= 1:
        for o, s in todo:
            msg = _one(exp, o, s)
            if verbose:
                print(msg, flush=True)
        return
    with ProcessPoolExecutor(workers) as pool:
        for fut in as_completed([pool.submit(_one, exp, o, s) for o, s in todo]):
            if verbose:
                print(fut.result(), flush=True)


def report(exp: dict) -> dict:
    out_dir = experiment_dir(exp)
    B = exp["budget"]
    dirs = {o: sorted((out_dir / o).glob("seed_*")) for o in exp["optimizers"]}
    summary = {"experiment": exp["name"], "problem": exp["problem"], "budget": B, "optimizers": {}}

    if "success" in exp:
        ok = metrics.make_success(exp["success"])
        hits = {o: np.array([metrics.run_hit_time(d, ok) for d in ds]) for o, ds in dirs.items()}
        for o, h in hits.items():
            summary["optimizers"][o] = {
                "runs": int(len(h)), "price_80": metrics.price_from_hits(h, B),
                "reliability_at_budget": float(np.mean(h <= B)),
                "median_hit": float(np.median(h)), "evaluations_total": int(sum(
                    sum(1 for _ in open(d / "evaluations.jsonl")) for d in dirs[o]))}
        ref = exp.get("reference_price", {})
        plots.reliability_from_hits_plot(hits, B, out_dir / "reliability.png", exp["name"], ref)
        if ref:
            summary["reference_price"] = ref
    else:
        curves = {o: np.array([metrics.best_so_far(d, B) for d in ds]) for o, ds in dirs.items()}
        tgt = None
        if "optimum" in exp:
            tgt = metrics.target_from_optimum(exp["optimum"]["objective"], exp["optimum"]["rel_tol"])
            summary["target_objective"] = tgt
        for o, c in curves.items():
            final = c[:, -1]
            s = {"runs": int(c.shape[0]), "final_best_median": float(np.median(final)),
                 "final_best_min": float(np.min(final)), "final_best_max": float(np.max(final))}
            if tgt is not None:
                s["price_80"] = metrics.price(c, tgt)
                s["reliability_at_budget"] = float(metrics.reliability(c, tgt)[-1])
            summary["optimizers"][o] = s
        opt = exp["optimum"]["objective"] if "optimum" in exp else None
        plots.convergence(curves, out_dir / "convergence.png", exp.get("plot_label", "best feasible objective"),
                          exp.get("plot_sign", 1.0), opt, exp["name"])
        if tgt is not None:
            plots.reliability_plot(curves, tgt, out_dir / "reliability.png", exp["name"])

    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("experiment", type=Path)
    ap.add_argument("--report-only", action="store_true")
    ap.add_argument("--workers", type=int, default=1)
    args = ap.parse_args()
    exp = load_experiment(args.experiment)
    if not args.report_only:
        run_all(exp, args.workers)
    print(json.dumps(report(exp), indent=2))


if __name__ == "__main__":
    main()
