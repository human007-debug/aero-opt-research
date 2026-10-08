"""Write reference_optima.yaml: exhaustive global optima for each load case at 48 plies.

    python -m problems.C1_buckling_stacking.reference_optima
"""
from pathlib import Path

import numpy as np
import yaml

from core.problem import load_config
from core.search import deep_update
from problems.C1_buckling_stacking import evaluator as ev

OUT = Path(__file__).with_name("reference_optima.yaml")


def compute(plies: int = 48) -> dict:
    base = load_config("C1_buckling_stacking")
    out = {}
    G = ev.enumerate_designs(plies // 4)
    for case in base["load_cases"]:
        if case == "verified":
            continue
        cfg = deep_update(base, {"loads": {"case": case}, "design": {"n_plies_total": plies}})
        r = ev.batch_evaluate(G, cfg)
        lam = np.where(r["contiguity_ok"], r["lambda_cr"], -np.inf)
        i = int(np.argmax(lam))
        out[case] = {"lambda_cr": float(lam[i]), "genes": G[i].tolist(),
                     "n_practical_optima_0.1pct": int((lam >= lam[i] * (1 - 1e-3)).sum()),
                     "n_contiguity_feasible": int(r["contiguity_ok"].sum())}
    return {"plies": plies, "method": "exhaustive enumeration of all 3^12 stack sequences", "cases": out}


if __name__ == "__main__":
    OUT.write_text(yaml.safe_dump(compute(), sort_keys=False))
    print(OUT.read_text())
