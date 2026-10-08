# Computational Aerospace Optimization Research

## Purpose
Master's research (Aerospace Engineering, IIT Madras). The goal is to solve well-posed aerospace optimization problems purely computationally, using an LLM-guided search loop benchmarked against classical optimizers, and to produce publishable results.

## Core Rules for Claude Code
- Never report a result until the evaluator reproduces the published benchmark for that problem within tolerance.
- Never invent citations, data, or benchmark values. If a reference value is needed, write `TODO: verify from source` and ask me.
- Every run must be reproducible: fixed random seeds, config files, logged package versions.
- Log every evaluated design (inputs, objective, constraint values, wall time) to disk.
- Compare every LLM-guided search against at least one classical baseline with an equal evaluation budget.
- Re-evaluate top designs at higher fidelity before reporting them.
- Prefer open-source tools. Flag anything that needs a commercial license.
- Ask before running anything expected to take more than 1 hour of compute.

## The Search Loop
1. **Problem definition**: design variables, bounds, objective, constraints in `problems/<id>/problem.yaml`.
2. **Evaluator**: deterministic `evaluate(design) -> {objective, constraints, feasible, metadata}`.
3. **Validation**: `problems/<id>/tests/` reproduces the benchmark. No search until this passes.
4. **Search**:
   - Baselines: genetic algorithm (pymoo), gradient-based (scipy), Bayesian optimization (BoTorch).
   - LLM-guided: Claude proposes candidate designs, mutation operators, or heuristics as code. Each is scored, an elite archive is kept, and the loop repeats.
5. **Fidelity ladder**: fast model for search, higher-fidelity model to confirm the top 5 designs.
6. **Reporting**: convergence plots (best objective vs. number of evaluations), Pareto fronts where relevant, final design tables.

## Repository Structure
```
core/            # shared search loop, archive, logging, plotting
baselines/       # GA, gradient, Bayesian optimization wrappers
problems/
  C1_buckling_stacking/
    problem.yaml
    evaluator.py
    tests/
    runs/
  ...
papers/          # LaTeX drafts
```

## Execution Order
- **Phase 1** (millisecond evaluators, build the loop here): C1, A1, A2
- **Phase 2**: C2, C4, C5, A4, M2, M3
- **Phase 3** (expensive evaluators): C3, A3, A5, M1, M4, M5

---

## Composites

### C1 — Stacking Sequence for Maximum Buckling Load
- **Variables**: ply angles from {0, ±45, 90}; symmetric, balanced; fixed ply count.
- **Objective**: maximize critical buckling load factor of a simply supported rectangular plate under biaxial compression.
- **Constraints**: balance, symmetry, max 4 contiguous plies of same orientation; optional strength check.
- **Evaluator**: classical laminate theory + closed-form orthotropic plate buckling.
- **Benchmark**: Le Riche & Haftka (1993) GA stacking sequence results.
- **Cost**: milliseconds.

### C2 — Tow-Steered (Variable-Stiffness) Plates
- **Variables**: fibre angle variation parameters per layer (start with linear variation).
- **Objective**: maximize buckling load.
- **Constraints**: minimum tow steering radius.
- **Evaluator**: Rayleigh-Ritz or FEniCS.
- **Benchmark**: Gürdal & Olmedo linear-variation plates.
- **Cost**: seconds.

### C3 — Stiffened Panel Mass Minimization
- **Variables**: skin layup, stiffener geometry, spacing, stiffener layup.
- **Objective**: minimize mass.
- **Constraints**: global and local buckling, material strength.
- **Evaluator**: semi-analytical buckling; confirm with FE (CalculiX/FEniCS).
- **Benchmark**: TODO: identify published optimum.
- **Cost**: seconds to minutes.

### C4 — Near-Zero Thermal Expansion Laminates
- **Variables**: ply angles, ply count, material choice.
- **Objective**: minimize in-plane coefficient of thermal expansion (space structures).
- **Constraints**: minimum stiffness, symmetry.
- **Evaluator**: laminate theory with thermal terms.
- **Benchmark**: TODO: identify published benchmark.
- **Cost**: milliseconds.

### C5 — Aeroelastic Tailoring of a Composite Wing Box
- **Variables**: layup of wing box walls, sweep.
- **Objective**: maximize divergence and flutter speed via bend-twist coupling.
- **Constraints**: strength, mass.
- **Evaluator**: composite beam model + strip theory aerodynamics.
- **Benchmark**: classical forward-swept wing divergence results. TODO: verify source.
- **Cost**: milliseconds to seconds.

---

## Aerodynamics

### A1 — Nonplanar Induced Drag Minimization
- **Variables**: circulation distribution on box wing / winglet geometries; height-to-span ratio.
- **Objective**: minimize induced drag at fixed lift and span.
- **Evaluator**: Trefftz-plane analysis (discrete vortex).
- **Benchmark**: Prandtl's box-wing efficiency results. TODO: verify reference values.
- **Cost**: milliseconds.

### A2 — Lift Distribution Under Bending Moment Constraint
- **Variables**: spanwise lift distribution, span.
- **Objective**: minimize induced drag.
- **Constraints**: fixed total lift, fixed root bending moment (extend later: structural weight, gust loads).
- **Evaluator**: lifting-line theory.
- **Benchmark**: Prandtl (1933) bell-shaped distribution.
- **Cost**: milliseconds.

### A3 — Transonic Airfoil Drag Minimization
- **Variables**: shape parameters (FFD or CST).
- **Objective**: minimize drag at fixed lift.
- **Constraints**: thickness, area.
- **Evaluator**: SU2 RANS with adjoint gradients.
- **Benchmark**: AIAA ADODG RAE 2822 transonic case.
- **Cost**: minutes per evaluation.

### A4 — Wingtip-Mounted Propeller Placement
- **Variables**: propeller position, inclination, rotation direction.
- **Objective**: maximize swirl and tip-vortex energy recovery (net drag reduction).
- **Evaluator**: vortex lattice + actuator disk model.
- **Benchmark**: TODO: select (e.g., TU Delft tip-mounted propeller experiments).
- **Cost**: seconds.

### A5 — Blended Wing Body Planform and Twist
- **Variables**: planform parameters, twist distribution.
- **Objective**: maximize L/D.
- **Constraints**: trim, internal volume.
- **Evaluator**: vortex lattice for search; SU2 to confirm.
- **Benchmark**: AIAA ADODG blended-wing-body case.
- **Cost**: seconds (VLM) to hours (SU2).

---

## Turbine Blade Materials

### M1 — Ni-Superalloy γ′ Fraction
- **Variables**: alloy composition (Al, Ti, Ta, W, Re, Cr, Co, Mo, Ni balance).
- **Objective**: maximize γ′ volume fraction at operating temperature.
- **Constraints**: no TCP phases (σ, μ, P); density limit.
- **Evaluator**: pycalphad. Needs a Ni thermodynamic database. TODO: confirm Thermo-Calc access at IITM.
- **Benchmark**: reproduce known alloys (e.g., CMSX-4).
- **Cost**: seconds.

### M2 — Lattice Misfit vs. Density Pareto Front
- **Variables**: alloy composition.
- **Objectives**: optimize γ/γ′ misfit (creep) and minimize density (centrifugal load).
- **Evaluator**: CALPHAD phase compositions + empirical misfit models.
- **Benchmark**: TODO: compare against published alloy data.
- **Cost**: seconds.

### M3 — Refractory High-Entropy Alloy Strength
- **Variables**: composition of BCC refractory elements.
- **Objective**: maximize high-temperature yield strength per unit density.
- **Evaluator**: Maresca–Curtin analytic solid-solution strengthening model.
- **Benchmark**: Senkov's experimentally measured refractory high-entropy alloys.
- **Cost**: milliseconds.

### M4 — Thermal Barrier Coating Conductivity
- **Variables**: dopant type and concentration in zirconia / rare-earth zirconates.
- **Objective**: minimize thermal conductivity.
- **Evaluator**: ML interatomic potential (e.g., MACE) molecular dynamics, Green-Kubo method.
- **Benchmark**: yttria-stabilized zirconia (YSZ) conductivity. TODO: verify reference value.
- **Cost**: hours per candidate.

### M5 — ML Creep-Rupture Surrogate
- **Variables**: alloy composition, heat treatment.
- **Objective**: maximize predicted creep-rupture life.
- **Evaluator**: ML model trained on NIMS Creep Data Sheets.
- **Caveat**: extrapolation is unreliable. Report results as candidates for experiments, with uncertainty estimates.
- **Cost**: milliseconds (after training).
