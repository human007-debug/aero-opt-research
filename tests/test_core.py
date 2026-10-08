import json

from core.archive import EliteArchive
from core.evallog import EvalLogger, read_evaluations
from core.problem import EvalResult


def _r(obj, feasible=True):
    return EvalResult(objective=obj, constraints={}, feasible=feasible)


def test_archive_keeps_best_distinct_feasible():
    arc = EliteArchive(size=2)
    assert arc.add([1], _r(3.0))
    assert not arc.add([1], _r(1.0))          # duplicate design
    assert not arc.add([9], _r(-5.0, False))  # infeasible
    assert arc.add([2], _r(2.0))
    assert arc.add([3], _r(1.0))              # evicts objective 3.0
    assert not arc.add([4], _r(5.0))
    assert [d for d, _ in arc.best()] == [[3], [2]]


def test_logger_writes_every_evaluation(tmp_path):
    run = tmp_path / "run1"
    with EvalLogger(run, {"seed": 0, "optimizer": "test"}) as log:
        f = log.wrap(lambda x: _r(sum(x)), source="unit")
        f([1, 2]); f([3])
    recs = read_evaluations(run)
    assert [r["objective"] for r in recs] == [3, 3]
    assert all("wall_time_s" in r and r["source"] == "unit" for r in recs)
    info = json.loads((run / "run.json").read_text())
    assert info["seed"] == 0 and "numpy" in info["environment"]["packages"]
