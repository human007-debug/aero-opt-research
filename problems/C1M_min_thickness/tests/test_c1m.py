"""C1M evaluator and the 1995 GA, checked against statements in Le Riche & Haftka (1995)."""
import copy

import numpy as np
import pytest

from baselines import lrh95_ga as ga
from core.problem import EvalResult, load_config
from core.search import Problem, run
from problems.C1_buckling_stacking import evaluator as c1
from problems.C1M_min_thickness import evaluator as ev

CFG = load_config("C1M_min_thickness")
C1 = load_config("C1_buckling_stacking")


def string(c1_genes, L=16):
    """C1 stack codes -> canonical C1M string (E = 0 padding on the outer side)."""
    return [0] * (L - len(c1_genes)) + [g + 1 for g in c1_genes]


@pytest.mark.parametrize("stacks,nc", [([0, 0, 0, 2], 1), ([2, 2, 2, 0, 0], 2),  # p.148 examples
                                       ([1, 1, 1, 1, 1], 0), ([0, 0, 1, 0], 0), ([0, 0], 1), ([0], 0)])
def test_excess_contiguous_stacks(stacks, nc):
    assert ev.excess_contiguous_stacks(stacks) == nc


def test_nc_zero_iff_c1_contiguity_feasible():
    rng = np.random.default_rng(1)
    for _ in range(500):
        st = rng.integers(0, 3, rng.integers(1, 14)).tolist()
        full = c1.decode(st, C1["design"]["stack_alphabet"])
        assert (ev.excess_contiguous_stacks(st) == 0) == (c1.max_contiguous(full, "ply") <= 4)


@pytest.mark.parametrize("case", ["LC1", "LC2", "LC3", "MULT"])
def test_table2_designs_are_feasible_48_ply(case):
    cfg = copy.deepcopy(CFG)
    cfg["loads"]["case"] = case
    genes = C1["benchmark"]["table2"][case]["genes"]
    r = ev.evaluate(string(genes), cfg)
    assert r.feasible and r.objective == 48
    c1cfg = copy.deepcopy(C1)
    c1cfg["loads"]["case"] = case
    assert r.metadata["lambda_cr"] == pytest.approx(c1.evaluate(genes, c1cfg).metadata["lambda_cr"], rel=1e-12)


def test_empty_string_is_infeasible():
    r = ev.evaluate([0] * 16, CFG)
    assert not r.feasible and r.objective == 0


def _res(N, lam, nc=0):
    return EvalResult(objective=N, constraints={}, feasible=True, metadata={"n_plies": N, "lambda_cr": lam, "n_c": nc})


def test_phi_reproduces_fig6_fig7_orderings():
    # LC1 best designs A (44 plies, 0.879), B (48, 1.040), C (52, 1.201); delta = 0, eps = 6, n_c = 0 (p.149-150).
    A, B, C = _res(44, 0.879), _res(48, 1.040), _res(52, 1.201)
    kw = dict(Pc=ga.COMMON["Pc"], delta=0.0, eps=6.0)
    f = lambda r, Pl, S: ga.phi(r, Pl=Pl, S=S, **kw)
    assert f(B, 2, 1) < f(A, 2, 1) and f(B, 2, 1) < f(C, 2, 1)       # Fig. 6: B clearly best
    assert f(B, 0.5, 1) < f(A, 0.5, 1)                                # Fig. 7: B still best, marginally
    assert f(A, 0.5, 1) - f(B, 0.5, 1) < f(A, 2, 1) - f(B, 2, 1)
    assert f(A, 0.5, 0) < f(B, 0.5, 0)                                # "makes the infeasible design (A) ... lower"


def test_phi_contiguity_penalty_multiplies():
    assert ga.phi(_res(48, 1.04, 2), Pc=1.1, Pl=0.5, S=1, delta=0.005, eps=6) == pytest.approx(
        1.1**2 * ga.phi(_res(48, 1.04, 0), Pc=1.1, Pl=0.5, S=1, delta=0.005, eps=6))


@pytest.fixture
def gas():
    space = ev.search_space(CFG)
    return {v: ga.LRH95GA(None, space, np.random.default_rng(0), v) for v in ("new", "old")}


def _canonical(s, L=16):
    k = next((i for i, g in enumerate(s) if g != 0), L)
    return len(s) == L and all(g == 0 for g in s[:k]) and all(g != 0 for g in s[k:])


def test_operators_keep_strings_canonical(gas):
    for g in gas.values():
        for _ in range(300):
            a, b = g.random_string(), g.random_string()
            assert _canonical(a)
            for s in (g.crossover(a, b), g.mutate(a), g.permute(a)):
                assert _canonical(s)


def test_new_permutation_swaps_two_stacks(gas):
    g = gas["new"]
    for _ in range(100):
        a = g.random_string()
        b = g.permute(a)
        assert sorted(a) == sorted(b) and sum(x != y for x, y in zip(a, b)) in (0, 2)


def test_new_mutation_changes_thickness_by_at_most_one_stack(gas):
    g = gas["new"]
    for _ in range(300):
        a = g.random_string()
        assert abs(len(g.full(g.mutate(a))) - len(g.full(a))) <= 1


def test_x1_thick_break_point_in_thicker_full_part(gas):
    g = gas["new"]
    a = [0] * 10 + [1, 2, 3, 1, 2, 3]   # 6 full stacks
    b = [0] * 4 + [3] * 12               # 12 full stacks (thicker)
    for _ in range(200):
        child = g.crossover(a, b)
        # break point c >= 4, so the child starts with a's first c digits, then b's tail
        assert 6 <= len(g.full(child)) <= 12


@pytest.mark.parametrize("variant", ["new", "old"])
def test_ga_runs_with_exact_budget_and_is_reproducible(tmp_path, variant):
    p = Problem("C1M_min_thickness")
    designs = []
    for k in range(2):
        f = run(p, ga.optimize, 200, seed=3, run_dir=tmp_path / f"{variant}{k}", params={"variant": variant})
        assert f.n_evals == 200
        designs.append([l for l in open(tmp_path / f"{variant}{k}" / "evaluations.jsonl")])
    strip = lambda ls: [l.split('"wall_time_s"')[0] for l in ls]
    assert strip(designs[0]) == strip(designs[1])


def test_initial_population_options():
    space = ev.search_space(CFG)
    g1 = ga.LRH95GA(None, space, np.random.default_rng(0), "new", init="uniform_digits")
    g2 = ga.LRH95GA(None, space, np.random.default_rng(0), "new")  # default: uniform_thickness
    n1 = [len(g1.full(g1.random_string())) for _ in range(4000)]
    n2 = [len(g2.full(g2.random_string())) for _ in range(4000)]
    assert abs(np.mean(n1) - 12) < 0.2          # Binomial(16, 3/4): mean 12 stacks = 48 plies
    assert abs(np.mean(n2) - 8.5) < 0.3 and min(n2) == 1 and max(n2) == 16
