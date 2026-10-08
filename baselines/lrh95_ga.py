"""Le Riche & Haftka (1995) genetic algorithm for minimum-thickness laminate design.

Reimplemented from: Le Riche, R. & Haftka, R. T. (1995). Improved genetic algorithm for minimum
thickness composite laminate design. Composites Engineering 5(2), 143-161.

Design string: digits of the half laminate, outer -> mid-plane, 0 = E (empty), 1 = 0_2, 2 = +-45,
3 = 90_2. Strings are kept canonical: empty digits at the outer end (left), full stacks against the
mid-plane, so the "full part" of a string is its right-hand end.

Variants (p.155):
  new: no-duplicate-parents selection, X1-thick crossover, new mutation (p_add = p_del = 0.05,
       p_cfo = 0.01), new permutation (swap two stacks, probability 1), P_l = 0.5, S = 1.
  old: rank selection, X2 crossover, old mutation (0.01 per digit), old permutation (probability 1),
       P_l = 2, S = 0.
  Both: population 8, elitist (best design cloned), crossover probability 1,
        P_c = sqrt(10/9), delta = 0.005.

Assumptions where the paper is not explicit (flagged so they can be checked against the 1993 paper):
  - eps = 6 in the objective Phi (the value used in Fig. 6; p.149 shows eps <= 6 is admissible).
  - Old permutation inverts the stack order of a random substring of the full part ("the two stacks at
    the two extremities of the central substring are then flipped about the center point").
    TODO: verify from source (Le Riche & Haftka 1993, AIAA J. 31(5)); the Fig. 5 scan is not legible
    enough to confirm.
  - The initial population is not described. init="uniform_digits" (default) draws each digit uniformly
    from {E, 0_2, +-45, 90_2}, so starting thicknesses are Binomial(16, 3/4) stacks (mean 48 plies, the
    optimal thickness for all four load cases). init="uniform_thickness" draws the number of full stacks
    uniformly from 1..16 (4 to 64 plies) and the orientations uniformly.
  - Each new child is one analysis. The cloned elite is not re-analysed.
"""
from __future__ import annotations

import math

import numpy as np

VARIANTS = {
    "new": dict(selection="no_duplicate_parents", crossover="X1-thick", mutation="new", permutation="swap",
                p_add=0.05, p_del=0.05, p_cfo=0.01, p_perm=1.0, Pl=0.5, S=1.0),
    "old": dict(selection="rank", crossover="X2", mutation="old", permutation="invert",
                p_mut=0.01, p_perm=1.0, Pl=2.0, S=0.0),
}
COMMON = dict(pop_size=8, Pc=math.sqrt(10 / 9), delta=0.005, eps=6.0, init="uniform_digits")


def phi(result, Pc: float, Pl: float, S: float, delta: float, eps: float) -> float:
    """Objective Phi, Eq. (4) (minimised)."""
    m = result.metadata
    N, lam, nc = m["n_plies"], m["lambda_cr"], m["n_c"]
    pen = Pc**nc
    if lam >= 1 - delta:
        return pen * (N + eps * ((1 - delta) - lam))
    if lam <= 0:
        return math.inf
    return pen * (N / lam**Pl) + S


class LRH95GA:
    def __init__(self, f, space, rng: np.random.Generator, variant: str = "new", **overrides):
        self.f, self.rng = f, rng
        self.L, self.E = space["n_vars"], space["empty_code"]
        self.orients = [v for v in range(space["n_values"]) if v != self.E]
        self.p = {**COMMON, **VARIANTS[variant], **overrides}

    # ------------------------------------------------------------ representation
    def full(self, s):
        return [g for g in s if g != self.E]

    def canon(self, full):
        return [self.E] * (self.L - len(full)) + list(full)

    def random_string(self):
        if self.p["init"] == "uniform_thickness":
            n = int(self.rng.integers(1, self.L + 1))
            return self.canon([int(self.rng.choice(self.orients)) for _ in range(n)])
        return self.canon(self.full(self.rng.integers(0, len(self.orients) + 1, self.L).tolist()))

    # ------------------------------------------------------------ operators
    def select_pair(self, pop, phis):
        m = len(pop)
        order = np.argsort(phis, kind="stable")
        fitness = np.empty(m)
        fitness[order] = [2 * (m + 1 - i) / (m * m + m) for i in range(1, m + 1)]  # p.145
        i = int(self.rng.choice(m, p=fitness))
        j = int(self.rng.choice(m, p=fitness))
        if self.p["selection"] == "no_duplicate_parents":  # p.150
            for _ in range(100):
                if pop[j] != pop[i]:
                    break
                j = int(self.rng.choice(m, p=fitness))
        return pop[i], pop[j]

    def crossover(self, a, b):
        L = self.L
        if self.p["crossover"] == "X2":  # two-point anywhere in the string (p.146)
            c1, c2 = sorted(self.rng.choice(np.arange(1, L), 2, replace=False))
            child = a[:c1] + b[c1:c2] + a[c2:]
        elif self.p["crossover"] == "X1-thick":  # one point in the full part of the thicker parent (p.151)
            start = L - max(len(self.full(a)), len(self.full(b)))
            c = int(self.rng.integers(max(start, 1), L)) if start < L else int(self.rng.integers(1, L))
            child = a[:c] + b[c:]
        else:
            raise ValueError(self.p["crossover"])
        return self.canon(self.full(child))

    def mutate(self, s):
        if self.p["mutation"] == "old":  # each digit changes with probability p_mut (p.146)
            s = list(s)
            for k in range(self.L):
                if self.rng.random() < self.p["p_mut"]:
                    s[k] = int(self.rng.choice([v for v in range(len(self.orients) + 1) if v != s[k]]))
            return self.canon(self.full(s))
        full = self.full(s)  # new mutation (p.152)
        if self.rng.random() < self.p["p_add"] and len(full) < self.L:
            full.insert(int(self.rng.integers(0, len(full) + 1)), int(self.rng.choice(self.orients)))
        if self.rng.random() < self.p["p_del"] and full:
            full.pop(int(self.rng.integers(0, len(full))))
        for k in range(len(full)):
            if self.rng.random() < self.p["p_cfo"]:
                full[k] = int(self.rng.choice([o for o in self.orients if o != full[k]]))
        return self.canon(full)

    def permute(self, s):
        full = self.full(s)
        if len(full) < 2 or self.rng.random() >= self.p["p_perm"]:
            return s
        i, j = sorted(self.rng.choice(len(full), 2, replace=False))
        if self.p["permutation"] == "swap":  # new permutation (p.152)
            full[i], full[j] = full[j], full[i]
        else:  # old permutation: invert a substring (see module docstring)
            full[i:j + 1] = full[i:j + 1][::-1]
        return self.canon(full)

    # ------------------------------------------------------------ main loop
    def evaluate(self, s):
        r = self.f(s, source="lrh95-ga")
        return phi(r, self.p["Pc"], self.p["Pl"], self.p["S"], self.p["delta"], self.p["eps"])

    def run(self):
        m = self.p["pop_size"]
        pop = [self.random_string() for _ in range(m)]
        phis = [self.evaluate(s) for s in pop]
        while True:
            best = int(np.argmin(phis))
            children = []
            for _ in range(m - 1):
                a, b = self.select_pair(pop, phis)
                children.append(self.permute(self.mutate(self.crossover(a, b))))
            child_phis = [self.evaluate(c) for c in children]
            pop, phis = [pop[best]] + children, [phis[best]] + child_phis


def optimize(f, space, rng: np.random.Generator, variant: str = "new", **overrides):
    LRH95GA(f, space, rng, variant, **overrides).run()
