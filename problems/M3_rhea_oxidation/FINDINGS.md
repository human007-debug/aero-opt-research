# M3X findings: oxidation-resistant, high-strength refractory alloys (working notes, 2026-10-08)

Status: data, surrogates and search pipeline built and validated on held-out alloys. All alloy
"results" below are surrogate predictions, not measurements. Nothing here is reportable as a
materials result until candidates are tested experimentally.

## 1. Data

| Dataset | Rows | Alloys | Use | Source |
|---|---|---|---|---|
| Gorsse et al. (2025) oxidation | 886 → 853 after audit | 157 | log10 mass gain vs composition, T, t | github.com/sgorsse/alloy_oxidation (CC BY 4.0) |
| MPEA (Borg et al. 2020) | 284 single-phase BCC compression records (duplicates removed) | 92 | yield strength vs composition, T | github.com/CitrineInformatics/MPEA_dataset (Apache-2.0) |
| MPEA phases | 168 (formula, processing) labels | 139 | P(single-phase BCC) | same |

Audit of the oxidation dataset (`data/oxidation_audit.md`): every formula was checked against its
composition columns under all plausible notations. 12 rows corrected (e.g. Cr-31Ta and Cr-9.5Ta entered
as Nb; W missing from WTaNbTiAl, composition summing to 80 at.%), 30 excluded (records giving the BCC
*phase* composition instead of the alloy composition; Nb-12Si-15Mo summing to 90 at.%; a label
contradicting its composition). 45 rows cite "Tom_ini" instead of a DOI. 18 repeated
(composition, T, t) groups give a measurement-noise floor of 0.18 in log10 mass gain.

Elemental data (`data/elements.yaml`, from pymatgen-core): the listed Mo shear modulus (20 GPa) is
inconsistent with its own E, ν and bulk modulus (≈126 GPa); Zr and Hf listed/derived values disagree.

## 2. The datasets barely overlap

Only **10 alloys** have both a single-phase BCC compression strength and oxidation data. The median
oxidation-tested alloy is **23 at.%** away from the nearest strength-tested alloy. Any claim of an alloy
that is optimal for both properties rests on at least one surrogate extrapolating.

## 3. Random-row validation overstates accuracy; flexible models generalise worst

Oxidation surrogate, 5-fold CV, 3 repeats (`data/oxidation_validation.md`). R² on log10 mass gain:

| Split | Bayesian ridge | GBDT | GP (RBF) |
|---|---|---|---|
| random rows | 0.71 | **0.92** | **0.92** |
| unseen alloy | **0.64** (90% coverage 0.88) | 0.55 | 0.61 (coverage 0.81) |
| unseen source paper | **0.56** | 0.45 | 0.40 |

Rows of one alloy (different T, t) land in both training and test sets under a random split, so it
measures interpolation within known alloys. The model ranking reverses for new alloys. Physics-motivated
descriptors (scale-former / volatile-oxide / non-protective group sums, Cr×Ta) did not help any model.
TODO: verify from source how Gorsse et al. (2025) grouped their cross-validation folds before comparing.

Strength surrogate (`data/strength_validation.md`), unseen alloy: GP on composition and T, R² 0.80
(RMSE ×1.41). The Maresca–Curtin edge model as implemented here gives R² < 0 and lowers accuracy when
added as a feature. It fails systematically for low-misfit alloys (NbTaTi: 7 MPa predicted vs 573 MPa
measured), Al-bearing alloys (×0.5) and Ti–V–Zr–Hf alloys above 1000 °C (over-predicted). Its constants
are unverified (paper not retrievable from this environment), so this is not yet a conclusion about the
model.

Phase classifier (`data/phase_validation.md`), unseen formula: ROC AUC 0.84, Brier 0.144 (base rate 0.218).

## 4. Search (`runs/m3x_pareto/`)

Objectives at 1000 °C: maximise predicted specific yield strength; minimise predicted log10 mass gain
after 20 h. Constraints: P(BCC) ≥ 0.5; calibrated strength sd ≤ 0.166; distance to the nearest
oxidation-tested alloy ≤ 13.2 at.%. Both trust limits are the 75th percentile of the same quantity for
known alloys held out in cross-validation. 20 000 evaluations × 10 seeds per optimizer.

- Random sampling almost never lands in the feasible region (feasible fraction ≈ 0.000); NSGA-II's is 0.36–0.49.
- Final hypervolume: NSGA-II median 259 (range 208–267), random median 200, known feasible alloys 203.
- The predicted front runs from Al–Cr–Mo–Ti(–Nb) (lowest mass gain, σ/ρ ≈ 70 MPa cm³/g) to
  Al–Mo–Nb–Ta–Ti–Zr (σ ≈ 1100 MPa, σ/ρ ≈ 138, highest mass gain). Al + Cr content falls monotonically
  along the front as specific strength rises.

Caveats that limit what the front means:
1. 65% of front points sit at P(BCC) < 0.55: the phase constraint is binding, and Cr-rich candidates may
   form Laves phases, where the single-phase strength surrogate does not apply.
2. Oxidation sd is ±0.51 in log10 (×3.2) everywhere, comparable to the spread along much of the front.
3. Every candidate is within 13 at.% of an oxidation-tested alloy by construction, so these are
   refinements of known families, not new chemistries.

## 5. What would make this publishable

1. Verify the Maresca–Curtin constants and elemental inputs from the paper (upload or allow arxiv.org).
2. Read Gorsse et al. (2025) to state precisely how their validation differs (grouped vs row-level folds).
3. Turn the search into experiment design: choose the few compositions whose measurement most reduces
   uncertainty on the front (e.g. expected hypervolume improvement under the calibrated surrogates), and
   propose them to an experimental group.
4. Add a CALPHAD or literature-based phase check for the shortlisted candidates.
5. Compare LLM-guided search with NSGA-II here at equal budget (the trust-region constraints make random
   proposals almost always infeasible, which favours methods that use domain knowledge).
