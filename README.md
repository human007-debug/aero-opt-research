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

## Conventions

- Evaluators minimise. Maximisation problems return the negated quantity.
- Constraints are `g(x) <= 0`.
- Every run goes in `problems/<id>/runs/<run_name>/`, with `run.json` (config, seed, environment, git commit) and `evaluations.jsonl` (one line per evaluation). Use `core.evallog.EvalLogger`.
- In YAML, write exponents with a sign (`1.0e+9`). PyYAML reads `1.0e9` as a string.
