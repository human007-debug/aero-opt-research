"""Benchmark reproduction: Le Riche & Haftka (1993).

Skipped until problem.yaml's benchmark.cases are filled from the paper and marked
verified. Search on C1 must not start before this test passes.
"""
import copy

import pytest

from core.problem import load_config, load_evaluator

PID = "C1_buckling_stacking"
CFG = load_config(PID)
BENCH = CFG["benchmark"]

pytestmark = pytest.mark.skipif(
    not BENCH["verified"] or not BENCH["cases"],
    reason="TODO: verify benchmark cases from Le Riche & Haftka (1993) and set benchmark.verified",
)


@pytest.mark.parametrize("case", BENCH["cases"] or [None])
def test_reproduces_published_optimum(case):
    cfg = copy.deepcopy(CFG)
    cfg["plate"].update(case["plate"])
    cfg["loads"].update(case["loads"])
    result = load_evaluator(PID)(case["design"], cfg)
    assert result.feasible
    assert result.metadata["lambda_cr"] == pytest.approx(case["lambda_cr"], rel=BENCH["tolerance_rel"])
