"""Gradient-based baseline: multi-start SLSQP (scipy) with finite-difference gradients.

Continuous spaces only. Each finite-difference evaluation counts against the shared budget.
Restarts from random points until the budget is spent; the first start uses space['x0'].
"""
import numpy as np
from scipy.optimize import minimize


def optimize(f, space, rng: np.random.Generator, ftol: float = 1e-10, maxiter: int = 200):
    if space["type"] != "continuous":
        raise ValueError("local (SLSQP) baseline needs a continuous space")
    lo, hi = np.array(space["lower"]), np.array(space["upper"])
    cache = {}

    def ev(x):
        k = tuple(np.round(x, 15))
        if k not in cache:
            cache[k] = f(list(x), source="slsqp")
        return cache[k]

    x0 = np.array(space.get("x0", rng.uniform(lo, hi)), dtype=float)
    while True:
        names = list(ev(x0).constraints)
        cons = [{"type": "ineq", "fun": (lambda x, k=k: -ev(x).constraints[k])} for k in names]
        minimize(lambda x: ev(x).objective, x0, method="SLSQP", bounds=list(zip(lo, hi)),
                 constraints=cons, options={"ftol": ftol, "maxiter": maxiter})
        x0 = rng.uniform(lo, hi)
