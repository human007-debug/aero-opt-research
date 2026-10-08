# aero-opt-research

LLM-guided vs. classical optimisation of aerospace design problems. See `CLAUDE.md` for the full research plan and rules.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest
```

## Status

| Problem | Evaluator | Physics tests | Benchmark reproduced | Search |
|---|---|---|---|---|
| C1 buckling stacking | CLT + closed-form SS-plate buckling + max-strain | passing | **yes**: Le Riche & Haftka (1995). Exhaustive enumeration of all 3^12 designs matches the best 44/48-ply λcr and all four Table 2 optima | unblocked |
| C2 tow-steered plate | Two-step Rayleigh-Ritz: in-plane prebuckling on the quarter plate, then buckling | passing | **yes**: Gürdal, Tatting & Wu (2008). Case II-a ⟨0\|75⟩ = 3.144 (paper 3.14), I-b ⟨0\|50⟩ = 1.437 (1.44), straight optima, stiffnesses and optimum locations | unblocked |
| C1M minimum thickness | C1 physics, 1995 formulation (empty stacks, ply count minimised) | passing | 1995 GA reimplemented: price LC1 425 / LC2 1178 reproduce the paper (440 / 1180); LC3 908 vs 1490 and MULT (reliability 0.72 vs 1.00) not reproduced, operator details pending the 1993 paper | baseline |
| M3X oxidation-resistant refractory alloys | Data-driven surrogates (strength GP, oxidation Bayesian ridge, phase classifier) + density model, validated on held-out alloys | passing | n/a (no single benchmark). Audited datasets; see `problems/M3_rhea_oxidation/FINDINGS.md` | NSGA-II Pareto search done; outputs are predictions only |
| A2 lift distribution | Lifting line, Fourier circulation | passing | reproduces the closed-form bell optimum (b/b0 = sqrt(3/2), D/D_ell = 8/9). Attribution to Prandtl (1933) still to verify from source | unblocked |

**A2 note.** With only the integrated bending-moment constraint the problem is ill-posed. Negative tip loading beats the bell, and the bell is just a stationary inflection point. `nonnegative_lift: true` (the default) makes the bell the optimum. The root-bending-moment variant has a different optimum that uses all odd harmonics, and it has no verified reference yet.

## Running experiments

```bash
python -m core.run experiments/c1_lc1_baselines.yaml          # all optimizers x seeds, equal budget
python -m core.run experiments/c1_lc1_baselines.yaml --report-only
```

Each optimizer sees the problem only through `core.search.BudgetedEvaluator`, which enforces the budget and logs every evaluation. Per-seed logs stay local. `summary.json`, `convergence.png` and `reliability.png` are committed.

Metrics follow Le Riche & Haftka (1995). A *practical optimum* is a feasible design within 0.1% of the global optimum. *Reliability(n)* is the fraction of runs that have found one within n evaluations. *Price* is the n at which reliability reaches 80%.

## Conventions

- Evaluators minimise. Maximisation problems return the negated quantity.
- Constraints are `g(x) <= 0`.
- Every run goes in `problems/<id>/runs/<run_name>/`, with `run.json` (config, seed, environment, git commit) and `evaluations.jsonl` (one line per evaluation). Use `core.evallog.EvalLogger`.
- In YAML, write exponents with a sign (`1.0e+9`). PyYAML reads `1.0e9` as a string.
