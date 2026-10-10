# M3X findings: oxidation-resistant, high-strength refractory alloys (working notes, 2026-10-08)

Status: data, surrogates and search pipeline built and validated on held-out alloys. All alloy
"results" below are surrogate predictions, not measurements. Nothing here is reportable as a
materials result until candidates are tested experimentally.

## 1. Data

| Dataset | Rows | Alloys | Use | Source |
|---|---|---|---|---|
| Gorsse et al. (2025) oxidation | 886 → 851 after audit | 155 | log10 mass gain vs composition, T, t | github.com/sgorsse/alloy_oxidation (CC BY 4.0) |
| MPEA (Borg et al. 2020) | 284 single-phase BCC compression records (duplicates removed) | 92 | yield strength vs composition, T | github.com/CitrineInformatics/MPEA_dataset (Apache-2.0) |
| MPEA phases | 168 (formula, processing) labels | 139 | P(single-phase BCC) | same |

Audit of the oxidation dataset (`data/oxidation_audit.md`): every formula was checked against its
composition columns under all plausible notations. 12 rows corrected, 2 excluded for a unit conflict (section 3b) (e.g. Cr-31Ta and Cr-9.5Ta entered
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

Oxidation surrogate, 5-fold CV, 3 repeats, 851 rows (`data/oxidation_validation.md`). R² on log10 mass gain:

| Split | Bayesian ridge | GBDT | GP (RBF) |
|---|---|---|---|
| random rows | 0.72 | **0.92** | **0.92** |
| unseen alloy | **0.65 (90% coverage 0.87)** | 0.56 | 0.58 (90% coverage 0.79) |
| unseen source paper | **0.56** | 0.44 | 0.42 |

What Gorsse et al. (2025) did (read from the open HAL version, hal-04746750): nested k-fold CV with
shuffling over rows (4 outer, 5 inner folds, 25 repeats), MAE 0.43 in ln(Δm); plus 5 arc-melted alloys
held out entirely, MAE 0.57 in ln. Their Fig. 4 R² 0.97 is the fit after retraining on all data. So they
did test on unseen alloys, and their error there is lower than our grouped-CV average (0.97 ln for GBDT).

Error vs distance from the held-out alloy to its nearest training alloy reconciles the two
(`data/oxidation_error_vs_distance.json`, MAE in ln units, grouped CV):

| Distance (at.%) | records | GBDT | Bayesian ridge |
|---|---|---|---|
| < 5 | 1221 | **0.68** | 0.78 |
| 5–10 | 497 | **0.75** | 0.87 |
| 10–15 | 285 | 1.12 | **0.90** |
| 15–20 | 161 | 1.49 | **0.94** |
| 20–30 | 310 | 1.58 | **1.27** |
| > 30 | 79 | 2.50 | **1.21** |

Close to known alloys GBDT is the better model, consistent with Gorsse et al.'s 0.57 on five test alloys
from well-sampled families. Beyond ~10 at.% it degrades steeply while the linear model degrades slowly.
Row-level CV (rows of one alloy on both sides of the split) measures the near-data regime only. For
design, the model choice should depend on distance; the search's trust limit (13.2 at.%) sits near the
crossover. Physics-motivated descriptors did not help any model.

## 3b. Independent external test: RefOxDB (added 2026-10-10)

Second dataset: Purdue's Refractory Oxidation Database (Mishra et al., arXiv:2310.15083; nanoHUB refoxdb
source r53, GPL-3.0), 407 digitised mass-gain curves (`refoxdb.py`, `data/refoxdb_audit.md`). Kept: air
exposures, the same 11 elements, read at 3–100 h by interpolation (units taken from the metadata; the curve
files are in mixed units: µg/cm², kg/m², min, s, …).

Data quality. 172 points were digitised independently by both groups (same paper, T, t,
composition). Agreement is close: median |Δlog10| 0.009, RMS 0.090, 2.3% differ
by more than ×2. One paper (J. Alloys Compd. 2022, 164180) differs by ×100: RefOxDB records its Fig. 2 in
mg/mm², the Gorsse values equal the raw numbers read as mg/cm². The paper is closed-access, so its 2 + 4
records are excluded from both datasets pending a check of the original figure.

External test: train on the full audited Gorsse dataset (851 rows), predict the 200 RefOxDB-only
points (30 compositions, 18 sources; median distance to the nearest training alloy
21 at.%). MAE in ln units:

| Distance (at.%) | points | GP | GBDT | Bayesian ridge |
|---|---|---|---|---|
| < 5 | 39 | 0.38 | 0.47 | 0.74 |
| 5–10 | 5 | 0.81 | 0.56 | 1.13 |
| 10–20 | 48 | 1.60 | 1.20 | 1.73 |
| > 20 | 108 | 1.57 | 1.57 | 2.26 |
| overall R² | | 0.24 | 0.29 | -0.49 |
| 90% interval coverage | | 0.94 | – | 0.69 |

Conclusions that survive the external test:
1. Error grows steeply with distance from known alloys for every model (≈4× from < 5 to > 20 at.%).
   Row-level CV, which keeps every alloy in training, measures only the near-data regime.
2. Model rankings from internal grouped CV did **not** transfer: within the Gorsse data Bayesian ridge was
   best on held-out alloys, but on independent data it is the worst (R² < 0) and overconfident. The GP is the
   most trustworthy (best near data, 90% intervals cover 94.5%). **Retraction:** the earlier statement that
   linear models extrapolate better (section 3) does not hold on independent data.
3. Even the best model explains little of the variance for alloys from other laboratories (R² ≈ 0.3).
The search now uses the GP for oxidation (calibration factor 1.70 from grouped CV, conservative).

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

## 4. Search (`runs/m3x_pareto*/`, rerun 2026-10-10 with the GP oxidation surrogate)

Objectives at 1000 °C: maximise predicted specific yield strength; minimise predicted log10 mass gain after
20 h. Constraints: P(BCC) ≥ 0.5; calibrated strength sd ≤ 0.166; distance to the nearest oxidation-tested
alloy ≤ 13.2 at.%. 20 000 evaluations × 10 seeds per optimizer.

- Random sampling almost never lands in the feasible region; NSGA-II's feasible fraction is ≈ 0.5.
- Final hypervolume medians (GP surrogate): NSGA-II 305, random 230, known feasible alloys 249.
- Shortlist (`runs/m3x_pareto/shortlist.md`): Al–Cr–Mo–Nb–Ta–Ti(–Zr) compositions with P(BCC) 0.8–0.93,
  e.g. Al5 Cr16 Mo25 Nb26 Ta5 Ti22: σ_y(1000 °C) ≈ 890 MPa ×/÷1.5, ρ 8.0 g/cm³, mass gain ≈ 1.1 mg/cm²
  ×/÷3.4. Predictions only.

## 4b. The predicted front depends on the surrogate (optimiser's curse)

Same search with three oxidation surrogates (`surrogate_dependence.py`, `data/surrogate_dependence.json`,
`runs/surrogate_dependence.png`). On the GP-driven front (654 points), GBDT predicts ≥3× higher
mass gain for 93% of points and Bayesian ridge for 98% (median disagreement
×4.3 and ×5.6); the rank correlation along the front with GBDT is 0.07. The fronts found
with the other surrogates are scored much more consistently by the remaining models. An optimiser
concentrates on compositions where its own surrogate is most optimistic, a known effect (the "optimiser's
curse", Smith & Winkler, Management Science 2006; TODO: verify citation). Expected external error at the
front's median distance to data (10.7 at.%) is ×4.9, about half of the front's predicted
mass-gain range, and the three fronts lie largely within each other's error bands. With these data, the
choice of surrogate moves the "optimal" compositions by more than the evidence can resolve.

Caveats:
1. Every candidate is within 13 at.% of an oxidation-tested alloy by construction: refinements of known
   families, not new chemistries. Purdue's two alloys (18 and 30 at.% away) would have been excluded.
2. P(BCC) is a data-driven estimate (AUC 0.84); no CALPHAD check yet.

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
and the finding that the two datasets barely overlap; (ii) distance-dependent accuracy of oxidation models,
confirmed on an independent dataset, and the finding that internal model rankings do not transfer to new
data; (iii) the size of the optimiser's curse in this design problem; (iv) an audit and cross-check of two
public oxidation datasets.

## 6. What would make this publishable

1. Verify the Maresca–Curtin constants and elemental inputs from the paper (upload or allow arxiv.org).
2. Read Gorsse et al. (2025) to state precisely how their validation differs (grouped vs row-level folds).
3. Turn the search into experiment design: choose the few compositions whose measurement most reduces
   uncertainty on the front (e.g. expected hypervolume improvement under the calibrated surrogates), and
   propose them to an experimental group.
4. Add a CALPHAD or literature-based phase check for the shortlisted candidates.
5. Compare LLM-guided search with NSGA-II here at equal budget (the trust-region constraints make random
   proposals almost always infeasible, which favours methods that use domain knowledge).
