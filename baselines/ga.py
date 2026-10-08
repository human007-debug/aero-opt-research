"""Genetic algorithm baseline (pymoo).

Categorical spaces use integer variables with rounding repair; continuous spaces use SBX and
polynomial mutation. Constraints are passed to pymoo (feasibility-first comparison). The run stops
when the shared budget raises BudgetExhausted, so the final generation may be partial.
"""
import numpy as np
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.core.problem import Problem as PymooProblem
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair
from pymoo.operators.sampling.rnd import FloatRandomSampling, IntegerRandomSampling
from pymoo.optimize import minimize


class _Wrapped(PymooProblem):
    def __init__(self, f, space, n_constr):
        if space["type"] == "categorical":
            xl, xu, vtype = 0, space["n_values"] - 1, int
            n = space["n_vars"]
        else:
            xl, xu, vtype = np.array(space["lower"]), np.array(space["upper"]), float
            n = len(space["lower"])
        super().__init__(n_var=n, n_obj=1, n_ieq_constr=n_constr, xl=xl, xu=xu, vtype=vtype)
        self.f = f

    def _evaluate(self, X, out, *args, **kwargs):
        F, G = [], []
        for x in X:
            r = self.f(x.tolist(), source="ga")
            F.append(r.objective)
            G.append(list(r.constraints.values()))
        out["F"] = np.array(F)
        if self.n_ieq_constr:
            out["G"] = np.array(G)


def optimize(f, space, rng: np.random.Generator, pop_size: int = 50, crossover_eta: float = 15.0,
             mutation_eta: float = 20.0, crossover_prob: float = 0.9):
    probe = f(_initial(space, rng), source="ga-probe")  # also learns the number of constraints
    problem = _Wrapped(f, space, len(probe.constraints))
    if space["type"] == "categorical":
        algo = GA(pop_size=pop_size, sampling=IntegerRandomSampling(),
                  crossover=SBX(prob=crossover_prob, eta=crossover_eta, vtype=float, repair=RoundingRepair()),
                  mutation=PM(eta=mutation_eta, vtype=float, repair=RoundingRepair()),
                  eliminate_duplicates=True)
    else:
        algo = GA(pop_size=pop_size, sampling=FloatRandomSampling(),
                  crossover=SBX(prob=crossover_prob, eta=crossover_eta), mutation=PM(eta=mutation_eta),
                  eliminate_duplicates=True)
    seed = int(rng.integers(0, 2**31 - 1))
    minimize(problem, algo, termination=("n_eval", 10**9), seed=seed, verbose=False)


def _initial(space, rng):
    if space["type"] == "categorical":
        return rng.integers(0, space["n_values"], space["n_vars"]).tolist()
    return rng.uniform(space["lower"], space["upper"]).tolist()
