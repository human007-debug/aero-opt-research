"""C1M evaluator: minimum-thickness formulation on top of the verified C1 physics.

objective   = number of plies N (minimised)
constraints = failure:    (1 - delta) - lambda_cr <= 0
              contiguity: n_c <= 0, n_c = stacks in excess of the 4-ply contiguity limit,
                          counted as in the 1995 paper (p.148)
"""
from __future__ import annotations

from functools import lru_cache
from typing import Any, Sequence

from core.problem import EvalResult, load_config
from problems.C1_buckling_stacking import evaluator as c1


@lru_cache(maxsize=4)
def _base(problem_id: str) -> dict:
    return load_config(problem_id)


def full_stacks(design: Sequence[int], empty: int = 0) -> list[int]:
    """Non-empty digits in C1 stack codes (0 = 0_2, 1 = +-45, 2 = 90_2), outer -> mid-plane."""
    return [int(g) - 1 for g in design if int(g) != empty]


def excess_contiguous_stacks(stacks: Sequence[int]) -> int:
    """n_c of the 1995 paper. +-45 stacks never count. A run of k identical 0_2 or 90_2 stacks
    adds max(0, k - 2); the run at the mid-plane is mirrored, so it adds max(0, k - 1).
    Examples from p.148: (0_6/90_2)_s -> 1, (90_6/0_4)_s -> 2."""
    nc, i, n = 0, 0, len(stacks)
    while i < n:
        j = i
        while j + 1 < n and stacks[j + 1] == stacks[i]:
            j += 1
        k = j - i + 1
        if stacks[i] != 1:
            nc += max(0, k - 1) if j == n - 1 else max(0, k - 2)
        i = j + 1
    return nc


def evaluate(design: Sequence[int], config: dict[str, Any]) -> EvalResult:
    if len(design) != config["design"]["string_length"]:
        raise ValueError(f"expected {config['design']['string_length']} digits, got {len(design)}")
    stacks = full_stacks(design, config["design"]["empty_code"])
    N = 4 * len(stacks)
    nc = excess_contiguous_stacks(stacks)
    if N == 0:
        lam, mode = 0.0, "none"
    else:
        base = _base(config["base_problem"])
        cfg = {**base, "loads": {"case": config["loads"]["case"]},
               "design": {**base["design"], "n_plies_total": N}}
        r = c1.evaluate(stacks, cfg)
        lam, mode = r.metadata["lambda_cr"], r.metadata["failure_mode"]
    delta = config["constraints"]["feasibility_delta"]
    constraints = {"failure": (1 - delta) - lam, "contiguity": float(nc)}
    return EvalResult(
        objective=float(N),
        constraints=constraints,
        feasible=all(v <= 0 for v in constraints.values()),
        metadata={"n_plies": N, "lambda_cr": lam, "n_c": nc, "failure_mode": mode},
    )


def search_space(config: dict[str, Any]) -> dict[str, Any]:
    d = config["design"]
    return {"type": "categorical", "n_vars": d["string_length"], "n_values": d["n_values"],
            "empty_code": d["empty_code"]}
