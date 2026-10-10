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

## 3. Oxidation model accuracy depends on distance from known alloys (revised 2026-10-10)

Oxidation surrogate, 5-fold CV, 3 repeats (`data/oxidation_validation.md`). R² on log10 mass gain:

| Split | Bayesian ridge | GBDT | GP (RBF) |
|---|---|---|---|
| random rows | 0.71 | **0.92** | **0.92** |
| unseen alloy | **0.64** (90% coverage 0.88) | 0.55 | 0.61 (coverage 0.81) |
| unseen source paper | **0.56** | 0.45 | 0.40 |

What Gorsse et al. (2025) did (read from the open HAL version, hal-04746750): nested k-fold CV with
shuffling over rows (4 outer, 5 inner folds, 25 repeats), MAE 0.43 in ln(Δm); plus 5 arc-melted alloys
held out entirely, MAE 0.57 in ln. Their Fig. 4 R² 0.97 is the fit after retraining on all data. So they
did test on unseen alloys, and their error there is lower than our grouped-CV average (0.97 ln for GBDT).

Error vs distance from the held-out alloy to its nearest training alloy reconciles the two
(`data/oxidation_error_vs_distance.json`, MAE in ln units, grouped CV):

| Distance (at.%) | records | GBDT | Bayesian ridge |
|---|---|---|---|
| < 5 | 1206 | **0.66** | 0.77 |
| 5–10 | 505 | **0.85** | 0.93 |
| 10–15 | 304 | 1.13 | **0.94** |
| 15–20 | 136 | 1.56 | **1.00** |
| 20–30 | 312 | 1.36 | **1.27** |
| > 30 | 96 | 2.79 | **1.17** |

Close to known alloys GBDT is the better model, consistent with Gorsse et al.'s 0.57 on five test alloys
from well-sampled families. Beyond ~10 at.% it degrades steeply while the linear model degrades slowly.
Row-level CV (rows of one alloy on both sides of the split) measures the near-data regime only. For
design, the model choice should depend on distance; the search's trust limit (13.2 at.%) sits near the
crossover. Physics-motivated descriptors did not help any model.

Strength surrogate (`data/strength_validation.md`), unseen alloy: GP on composition and T, R² 0.80
(RMSE ×1.41), used in the search.

Physics model (corrected 2026-10-10). The reduced Maresca–Curtin edge model is now checked against the paper
(arXiv:1901.02100v3): constants, α = 1/12 (not 0.123 as first written from memory), M = 3.067, and alloy
elastic constants from rule-of-mixtures single-crystal C_ij. Elemental C_ij and BCC volumes for Mo, Nb, Ta,
V, W are recovered from the paper's Table 2 (residual ≤ 1.2 GPa). With these inputs the code reproduces the
paper's reduced-theory τ_y0 and ΔE_b (Fig. 7) within 5% and its 1873 K strengths (Fig. 1) within 15%
(tests in `tests/test_m3.py`). Against the 21 MPEA records for Mo–Nb–Ta–V–W alloys, with no fitting:
RMSE ×1.32 (log10 0.119), Spearman 0.97, under-predicting at high T as the paper itself reports. The GP
trained on all other alloys is more accurate on those records (log10 0.085), but this is 4 alloys.
**Retraction:** the earlier statement that the physics model gives R² < 0 came from wrong inputs (α and
polycrystal moduli), not from the model. The real limitation is scope: the paper provides validated inputs
only for Mo–Nb–Ta–V–W, while oxidation-resistant designs need Al, Cr and Ti, so the physics model cannot be
used across the M3X design space.

Phase classifier (`data/phase_validation.md`), unseen formula: ROC AUC 0.84, Brier 0.144 (base rate 0.218).

External check (not in the training data). Bejjipurapu et al. (Purdue, arXiv:2512.15958, Dec 2025) found
Al30Mo5Ti15Cr50 and Al40Mo5Ti30Cr25 by experimental active learning, both < 1 mg/cm² after 24 h at
1000 °C. They lie 30 and 18 at.% from our oxidation data. Predictions at 1000 °C / 24 h: Bayesian ridge
1.3 and 1.7 mg/cm² (×/÷3.2, consistent with the measurements); GBDT 3.2 and 3.7 mg/cm² (more than 3× too
high). Two alloys and an inequality only, but consistent with the distance analysis. Both lie outside the
search's trust region (13.2 at.%), so that limit would have excluded these discoveries.

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

Shortlist for experiments (`runs/m3x_pareto/shortlist.md`, `python -m problems.M3_rhea_oxidation.shortlist`):
six compositions spread along the front by k-means. The most balanced is Al9 Cr16 Mo23 Nb30 Ta6 Ti16
(predicted σ_y(1000 °C) ≈ 930 MPa ×/÷1.5, ρ 8.0 g/cm³, mass gain ≈ 6 mg/cm² ×/÷3.2 after 20 h,
P(BCC) 0.82). The four Al–Cr–Mo–Ti–Nb candidates sit at P(BCC) ≈ 0.50.

## 5. Related work (positioning)

- Gorsse et al., Scripta Mater. 255 (2025) 116394: GBDT on the dataset used here; row-level nested CV plus
  5 held-out alloys; designed and tested three Al-Cr-Mo-Ta-Ti alloys.
- Mishra et al., arXiv:2310.15083 (Comput. Mater. Sci. 2024): Refractory Oxidation Database, mass-change
  curves for 407 alloys (nanohub.org/tools/refoxdb).
- Bejjipurapu et al., arXiv:2511.01095: GPR with oxide-based descriptors, 77 compositions, MAE 5.78 mg/cm².
- Bejjipurapu et al., arXiv:2512.15958: experimental active learning (GPR + Bayesian optimisation, 6 rounds
  of 5 alloys) in Al-containing quaternaries; Al-Cr-Mo-Ti alumina formers < 1 mg/cm²; multi-objective with
  specific hardness and thermal expansion for bond coats.
Experimental active-learning discovery of oxidation-resistant RCCAs is therefore done (Purdue). What this
work adds that those do not: (i) joint yield strength at 1000 °C and oxidation with explicit trust regions,
and the finding that the two datasets barely overlap; (ii) distance-dependent accuracy of oxidation models
(row-level CV measures only the near-data regime); (iii) an audit of a public dataset with documented errors.

## 6. What would make this publishable

1. Verify the Maresca–Curtin constants and elemental inputs from the paper (upload or allow arxiv.org).
2. Read Gorsse et al. (2025) to state precisely how their validation differs (grouped vs row-level folds).
3. Turn the search into experiment design: choose the few compositions whose measurement most reduces
   uncertainty on the front (e.g. expected hypervolume improvement under the calibrated surrogates), and
   propose them to an experimental group.
4. Add a CALPHAD or literature-based phase check for the shortlisted candidates.
5. Compare LLM-guided search with NSGA-II here at equal budget (the trust-region constraints make random
   proposals almost always infeasible, which favours methods that use domain knowledge).
