import json

import numpy as np
import pytest

from baselines import ga, random_search
from core import metrics
from core.search import BudgetedEvaluator, BudgetExhausted, Problem, deep_update, run


def test_deep_update_does_not_mutate():
    base = {"a": {"b": 1, "c": 2}}
    out = deep_update(base, {"a": {"b": 5}})
    assert out == {"a": {"b": 5, "c": 2}} and base == {"a": {"b": 1, "c": 2}}


def test_budget_is_enforced():
    f = BudgetedEvaluator(Problem("A2_lift_distribution"), budget=3)
    for _ in range(3):
        f([1.0] + [0.0] * 10)
    with pytest.raises(BudgetExhausted):
        f([1.0] + [0.0] * 10)


@pytest.mark.parametrize("opt", [random_search, ga])
def test_runs_use_exact_budget_and_are_reproducible(tmp_path, opt):
    p = Problem("C1_buckling_stacking")
    logs = []
    for k in range(2):
        d = tmp_path / f"r{k}"
        f = run(p, opt.optimize, 120, seed=7, run_dir=d, optimizer_name=opt.__name__)
        assert f.n_evals == 120
        logs.append([json.loads(l)["design"] for l in open(d / "evaluations.jsonl")])
    assert logs[0] == logs[1]


def test_metrics_on_synthetic_curves():
    curves = np.array([[3, 2, 1, 1], [3, 3, 3, 1], [np.inf, 2, 2, 2]], dtype=float)
    np.testing.assert_array_equal(metrics.hit_times(curves, 1.0), [3, 4, np.inf])
    np.testing.assert_allclose(metrics.reliability(curves, 1.0), [0, 0, 1 / 3, 2 / 3])
    assert metrics.price(curves, 1.0, level=0.6) == 4
    assert metrics.price(curves, 1.0, level=0.8) == float("inf")
    assert metrics.target_from_optimum(-2.0, 1e-3) == pytest.approx(-1.998)
