"""Run-level metrics computed from evaluations.jsonl (independent of the optimizer).

Le Riche & Haftka (1995) measures, used for every problem with a known optimum:
  reliability(n) = fraction of independent runs that have found a practical optimum within n evaluations
  price          = smallest n with reliability(n) >= 0.8
A practical optimum is a feasible design within ``rel_tol`` of the global optimum's objective.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

from .evallog import read_evaluations


def best_so_far(run_dir: Path, budget: int | None = None) -> np.ndarray:
    """Best feasible objective after each evaluation (+inf until the first feasible design)."""
    recs = read_evaluations(run_dir)
    obj = np.array([r["objective"] if r["feasible"] else np.inf for r in recs], dtype=float)
    out = np.minimum.accumulate(obj) if len(obj) else obj
    if budget is not None and len(out) < budget:  # optimizer stopped early: carry the last value
        out = np.concatenate([out, np.full(budget - len(out), out[-1] if len(out) else np.inf)])
    return out[:budget] if budget is not None else out


def hit_times(curves: np.ndarray, target: float) -> np.ndarray:
    """1-based evaluation count at which each run first reached objective <= target (inf if never)."""
    hit = curves <= target
    first = np.where(hit.any(1), hit.argmax(1) + 1, np.inf)
    return first.astype(float)


def reliability(curves: np.ndarray, target: float) -> np.ndarray:
    """reliability[n-1] = fraction of runs that reached target within n evaluations."""
    return (curves <= target).mean(0)


def price(curves: np.ndarray, target: float, level: float = 0.8) -> float:
    rel = reliability(curves, target)
    idx = np.flatnonzero(rel >= level)
    return float(idx[0] + 1) if len(idx) else float("inf")


def target_from_optimum(opt_objective: float, rel_tol: float) -> float:
    """Objective threshold for a practical optimum (objectives are minimised)."""
    return opt_objective + abs(opt_objective) * rel_tol


def make_success(spec: dict):
    """Success predicate from an experiment's `success:` block, applied to a logged record:
        feasible: true            -> record must be feasible
        objective_max: v          -> objective <= v
        metadata_min: {key: v}    -> metadata[key] >= v
        metadata_max: {key: v}    -> metadata[key] <= v
    """
    def ok(rec: dict) -> bool:
        if spec.get("feasible", True) and not rec["feasible"]:
            return False
        if "objective_max" in spec and rec["objective"] > spec["objective_max"]:
            return False
        md = rec.get("metadata", {})
        if any(md.get(k, -np.inf) < v for k, v in spec.get("metadata_min", {}).items()):
            return False
        if any(md.get(k, np.inf) > v for k, v in spec.get("metadata_max", {}).items()):
            return False
        return True
    return ok


def run_hit_time(run_dir: Path, success) -> float:
    """1-based evaluation count of the first successful record (inf if none)."""
    for i, rec in enumerate(read_evaluations(run_dir), 1):
        if success(rec):
            return float(i)
    return float("inf")


def reliability_from_hits(hits: np.ndarray, budget: int) -> np.ndarray:
    n = np.arange(1, budget + 1)
    return (hits[:, None] <= n[None, :]).mean(0)


def price_from_hits(hits: np.ndarray, budget: int, level: float = 0.8) -> float:
    rel = reliability_from_hits(hits, budget)
    idx = np.flatnonzero(rel >= level)
    return float(idx[0] + 1) if len(idx) else float("inf")
