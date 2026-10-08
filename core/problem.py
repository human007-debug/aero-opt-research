"""Problem definition loading.

Each problem lives in problems/<id>/ with a problem.yaml and an evaluator.py
exposing ``evaluate(design, config) -> EvalResult``.
"""
from __future__ import annotations

import importlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
PROBLEMS_DIR = REPO_ROOT / "problems"


@dataclass
class EvalResult:
    """Return type of every evaluator. ``objective`` is always minimised;
    maximisation problems return the negated quantity and say so in metadata."""

    objective: float
    constraints: dict[str, float]  # g(x) <= 0 means satisfied
    feasible: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "objective": self.objective,
            "constraints": self.constraints,
            "feasible": self.feasible,
            "metadata": self.metadata,
        }


def load_config(problem_id: str) -> dict[str, Any]:
    with open(PROBLEMS_DIR / problem_id / "problem.yaml") as f:
        return yaml.safe_load(f)


def load_evaluator(problem_id: str) -> Callable[..., EvalResult]:
    return importlib.import_module(f"problems.{problem_id}.evaluator").evaluate
