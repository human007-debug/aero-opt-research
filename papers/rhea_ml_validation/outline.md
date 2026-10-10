# Paper outline (working draft)

**Working title:** How far can data-driven models be trusted for designing oxidation-resistant refractory alloys?
Distance-dependent accuracy, cross-dataset transfer and data quality

**Type:** methods / data paper (materials informatics). Candidate venues: Integrating Materials and
Manufacturing Innovation; Computational Materials Science; Data-Centric Engineering. TODO: decide with supervisor.

## Claims and evidence (every number traceable to a file in problems/M3_rhea_oxidation/)

| # | Claim | Evidence | Status |
|---|---|---|---|
| C1 | Public oxidation data contain correctable entry errors; two independent digitisations of the same figures agree closely, except for a unit conflict | `data/oxidation_audit.md`, `data/refoxdb_audit.md`, `refoxdb_external_test.json` (digitisation_agreement) | done; unit conflict needs the original figure |
| C2 | Accuracy on a new alloy falls steeply with its composition distance to the training alloys (≈4× in ln-MAE from < 5 to > 20 at.%), for every model, within and across datasets | `data/oxidation_error_vs_distance.json`, `data/refoxdb_external_test.json` | done |
| C3 | Row-level CV (each alloy's time/temperature points on both sides) reports only the near-data regime (R² 0.92 vs 0.42–0.65 on held-out alloys) | `data/oxidation_validation.md` | done |
| C4 | Model rankings from internal grouped CV do not transfer to an independent dataset (Bayesian ridge best internally, worst externally; GP best-calibrated externally) | validation + external test | done; needs a second external set or bootstrap CIs on rankings |
| C5 | Strength and oxidation data barely overlap (10 alloys), so joint-property design necessarily extrapolates; the physics strength model (Maresca–Curtin) is validated only for Mo–Nb–Ta–V–W | FINDINGS §2, `data/strength_validation.md`, tests | done |
| C6 | Consequence for design (optimiser's curse): on the GP-driven front, GBDT and Bayesian ridge predict ≥3× worse oxidation for 93–98% of points; expected external error at the front is about half the front's predicted range | `data/surrogate_dependence.json`, `runs/surrogate_dependence.png` | done; add seeds-level CIs |

## Not claimed
- No new alloy is claimed. Shortlisted compositions are predictions.
- The general principle (random CV overstates extrapolation) is known: Meredig et al., Mol. Syst. Des. Eng.
  3 (2018) 819 (leave-one-cluster-out CV); applicability-domain work (e.g. arXiv:2406.05143). This paper
  quantifies it for RHEA/RCCA oxidation and shows the consequences for design. TODO: verify full citations.

## Figures
1. Data map: compositions of the Gorsse, RefOxDB and MPEA strength datasets (overlap).
2. Digitisation agreement scatter (172 matched points) with the unit-conflict outliers.
3. Error vs distance: grouped CV (Gorsse) and external (RefOxDB) on one plot, per model.
4. R² by validation scheme (rows / alloy / source / external) per model: the ranking reversal.
5. Pareto fronts from different surrogates, coloured by distance to data.

## Remaining work
- C6 experiment (above).
- Bootstrap confidence intervals for all R²/MAE and for the model ranking (C4).
- Check the J. Alloys Compd. 2022, 164180 Fig. 2 unit through the institute library.
- Related-work section (Gorsse 2025; Mishra 2024; Bejjipurapu 2025 ×2; Meredig 2018; applicability-domain papers).
- Make the processed datasets and audit public with the paper (licences: CC BY 4.0, GPL-3.0, Apache-2.0).
