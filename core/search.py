"""Budgeted, logged evaluation shared by every optimizer.

All optimizers (classical baselines and the LLM-guided loop) see a problem only through
``BudgetedEvaluator``: it counts every call against a fixed budget, logs every evaluation to
disk, and raises ``BudgetExhausted`` when the budget is spent, so budgets are equal by construction.
"""
from __future__ import annotations

import copy
import importlib
import time
from pathlib import Path
from typing import Any, Callable

from .evallog import EvalLogger
from .problem import EvalResult, load_config
from .repro import seed_everything


class BudgetExhausted(Exception):
    pass


class TargetReached(BudgetExhausted):
    """Raised after the first evaluation that satisfies the experiment's success criterion."""


def deep_update(base: dict, overrides: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in (overrides or {}).items():
        out[k] = deep_update(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out


class Problem:
    """A problem instance: config (problem.yaml + overrides), evaluator and search space."""

    def __init__(self, problem_id: str, overrides: dict | None = None):
        self.id = problem_id
        self.config = deep_update(load_config(problem_id), overrides or {})
        self.module = importlib.import_module(f"problems.{problem_id}.evaluator")
        self.space = self.module.search_space(self.config)

    def evaluate(self, design) -> EvalResult:
        return self.module.evaluate(design, self.config)


class BudgetedEvaluator:
    def __init__(self, problem: Problem, budget: int, logger: EvalLogger | None = None,
                 success: Callable[[dict], bool] | None = None, stop_on_success: bool = False):
        self.problem, self.budget, self.logger = problem, budget, logger
        self.success, self.stop_on_success = success, stop_on_success
        self.hit_at: int | None = None  # evaluation count at the first success
        self.n_evals = 0
        self.best: tuple[Any, EvalResult] | None = None  # best feasible

    @property
    def remaining(self) -> int:
        return self.budget - self.n_evals

    def __call__(self, design, source: str = "") -> EvalResult:
        if self.n_evals >= self.budget:
            raise BudgetExhausted
        design = [v.item() if hasattr(v, "item") else v for v in design]
        t0 = time.perf_counter()
        result = self.problem.evaluate(design)
        dt = time.perf_counter() - t0
        self.n_evals += 1
        if self.logger:
            self.logger.log(design, result, dt, source)
        if result.feasible and (self.best is None or result.objective < self.best[1].objective):
            self.best = (design, result)
        if self.success and self.hit_at is None and self.success(result.to_dict()):
            self.hit_at = self.n_evals
            if self.stop_on_success:
                raise TargetReached
        return result


def run(problem: Problem, optimizer: Callable, budget: int, seed: int, run_dir: Path,
        optimizer_name: str = "", params: dict | None = None, overrides: dict | None = None,
        success: Callable[[dict], bool] | None = None, stop_on_success: bool = False) -> BudgetedEvaluator:
    """Run one optimizer for one seed. Every evaluation is logged under run_dir.

    With stop_on_success the run ends at the first successful evaluation; reliability and price
    depend only on that first-hit time, so later evaluations would not change them.
    """
    rng = seed_everything(seed)
    info = {"problem": problem.id, "overrides": overrides or {}, "optimizer": optimizer_name,
            "params": params or {}, "budget": budget, "seed": seed, "stop_on_success": stop_on_success}
    with EvalLogger(run_dir, info) as log:
        f = BudgetedEvaluator(problem, budget, log, success, stop_on_success)
        try:
            optimizer(f, problem.space, rng, **(params or {}))
        except BudgetExhausted:
            pass
    return f
