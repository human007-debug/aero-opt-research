"""Benchmark reproduction for linear-variation VAT plates.

Skipped until problem.yaml's benchmark.cases are filled from the source papers and marked
verified. Search on C2 must not start before this test passes.
"""
import copy

import pytest

from core.problem import load_config
from problems.C2_tow_steered import evaluator as ev

CFG = load_config("C2_tow_steered")
BENCH = CFG["benchmark"]

pytestmark = pytest.mark.skipif(
    not BENCH["verified"] or not BENCH["cases"],
    reason="TODO: verify benchmark cases from Gurdal & Olmedo / Gurdal, Tatting & Wu and set benchmark.verified",
)


@pytest.mark.parametrize("case", BENCH["cases"] or [None])
def test_reproduces_published_buckling_load(case):
    cfg = copy.deepcopy(CFG)
    for section in ("material", "plate", "layup", "boundary_conditions"):
        cfg[section].update(case.get(section, {}))
    r = ev.analyse(case["T0"], case["T1"], cfg)
    ref = ev.analyse(case["reference_angle"], case["reference_angle"], cfg)  # normalising plate
    assert r["buckling_load"] / ref["buckling_load"] == pytest.approx(case["normalised_load"], rel=BENCH["tolerance_rel"])
