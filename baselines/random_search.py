"""Uniform random sampling. Sanity baseline: any useful optimizer must beat it."""
import numpy as np


def optimize(f, space, rng: np.random.Generator):
    while True:
        if space["type"] == "categorical":
            x = rng.integers(0, space["n_values"], space["n_vars"]).tolist()
        else:
            x = rng.uniform(space["lower"], space["upper"]).tolist()
        f(x, source="random")
