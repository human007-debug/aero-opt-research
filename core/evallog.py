"""Evaluation logging. Every evaluated design is appended to a JSONL file.

Run layout::

    problems/<id>/runs/<run_name>/
        run.json          # config, seed, optimizer, budget, environment
        evaluations.jsonl # one line per evaluation
"""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .problem import EvalResult
from .repro import environment_info


def _jsonable(x: Any) -> Any:
    if hasattr(x, "tolist"):
        return x.tolist()
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, dict):
        return {k: _jsonable(v) for k, v in x.items()}
    return x


class EvalLogger:
    def __init__(self, run_dir: Path, run_info: dict[str, Any]):
        self.run_dir = Path(run_dir)
        self.run_dir.mkdir(parents=True, exist_ok=False)  # never overwrite a run
        self.n_evals = 0
        info = {
            **run_info,
            "started_utc": datetime.now(timezone.utc).isoformat(),
            "environment": environment_info(),
        }
        (self.run_dir / "run.json").write_text(json.dumps(_jsonable(info), indent=2))
        self._fh = open(self.run_dir / "evaluations.jsonl", "a")

    def wrap(self, evaluate: Callable[[Any], EvalResult], source: str = "") -> Callable[[Any], EvalResult]:
        """Return an evaluate function that logs every call."""

        def logged(design: Any) -> EvalResult:
            t0 = time.perf_counter()
            result = evaluate(design)
            self.log(design, result, time.perf_counter() - t0, source)
            return result

        return logged

    def log(self, design: Any, result: EvalResult, wall_time_s: float, source: str = "") -> None:
        self.n_evals += 1
        rec = {
            "eval_id": self.n_evals,
            "design": _jsonable(design),
            **_jsonable(result.to_dict()),
            "wall_time_s": wall_time_s,
            "source": source,
        }
        self._fh.write(json.dumps(rec) + "\n")
        self._fh.flush()

    def close(self) -> None:
        self._fh.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


def read_evaluations(run_dir: Path) -> list[dict[str, Any]]:
    with open(Path(run_dir) / "evaluations.jsonl") as f:
        return [json.loads(line) for line in f if line.strip()]
