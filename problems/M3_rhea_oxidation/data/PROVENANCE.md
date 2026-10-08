# Data provenance

Raw files are stored unmodified in `raw/` (checksums in `raw/SHA256SUMS`). All cleaning is done in code
(`problems/M3_rhea_oxidation/data_audit.py`), never by editing raw files.

| File | Source | Licence | Citation |
|---|---|---|---|
| `alloy_oxidation_886_202406.csv`, `alloy_oxidation_886_202406_with_metadata.json` | https://github.com/sgorsse/alloy_oxidation (`Data/`, branch `main`), downloaded 2026-10-08 | CC BY 4.0 | S. Gorsse et al., "Advancing refractory high entropy alloy development with AI-predictive models for high temperature oxidation resistance", Scripta Materialia 255 (2025) 116394, doi:10.1016/j.scriptamat.2024.116394 |
| `MPEA_dataset.csv` | https://github.com/CitrineInformatics/MPEA_dataset (`MPEA_dataset.csv`, branch `master`), downloaded 2026-10-08 | Apache-2.0 | C. K. H. Borg et al., "Expanded dataset of mechanical properties and observed phases of multi-principal element alloys", Scientific Data 7 (2020) 430. TODO: verify citation details from source (volume/article number) |

Not used: `XGBoost_retrainedmodel_oxidation_202406.pkl` from the oxidation repository. Loading a pickle
executes code, and this study trains its own models.

Not reachable from this environment (network policy): alloy.tattvasar.com, nanohub.org (Refractory
Oxidation Database, Mishra et al. 2024), arxiv.org, doi.org.
