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
| C1 buckling stacking | CLT + closed-form SS-plate buckling | passing | **no**: values in `problem.yaml` need verifying against Le Riche & Haftka (1993) | blocked |
| A2 lift distribution | Lifting line, Fourier circulation | passing | reproduces the closed-form bell optimum (b/b0 = sqrt(3/2), D/D_ell = 8/9). Attribution to Prandtl (1933) still to verify from source | unblocked |

**A2 note.** With only the integrated bending-moment constraint the problem is ill-posed. Negative tip loading beats the bell, and the bell is just a stationary inflection point. `nonnegative_lift: true` (the default) makes the bell the optimum. The root-bending-moment variant has a different optimum that uses all odd harmonics, and it has no verified reference yet.

## Conventions

- Evaluators minimise. Maximisation problems return the negated quantity.
- Constraints are `g(x) <= 0`.
- Every run goes in `problems/<id>/runs/<run_name>/`, with `run.json` (config, seed, environment, git commit) and `evaluations.jsonl` (one line per evaluation). Use `core.evallog.EvalLogger`.
- In YAML, write exponents with a sign (`1.0e+9`). PyYAML reads `1.0e9` as a string.
