# Data provenance

Raw files are stored unmodified in `raw/` (checksums in `raw/SHA256SUMS`). All cleaning is done in code
(`problems/M3_rhea_oxidation/data_audit.py`), never by editing raw files.

| File | Source | Licence | Citation |
|---|---|---|---|
| `alloy_oxidation_886_202406.csv`, `alloy_oxidation_886_202406_with_metadata.json` | https://github.com/sgorsse/alloy_oxidation (`Data/`, branch `main`), downloaded 2026-10-08 | CC BY 4.0 | S. Gorsse et al., "Advancing refractory high entropy alloy development with AI-predictive models for high temperature oxidation resistance", Scripta Materialia 255 (2025) 116394, doi:10.1016/j.scriptamat.2024.116394 |
| `MPEA_dataset.csv` | https://github.com/CitrineInformatics/MPEA_dataset (`MPEA_dataset.csv`, branch `master`), downloaded 2026-10-08 | Apache-2.0 | C. K. H. Borg et al., "Expanded dataset of mechanical properties and observed phases of multi-principal element alloys", Scientific Data 7 (2020) 430. TODO: verify citation details from source (volume/article number) |
| `refoxdb_r53/` (`refoxdb-r53.tar.gz`, `compiled_metadata.xlsx`, `oxidation_curves_data/`) | nanoHUB tool refoxdb, source release r53 (https://nanohub.org/resources/sourcecode?tool=refoxdb_r53), downloaded 2026-10-10 | GPL-3.0 | S. Mishra et al., "Mass uptake during oxidation of metallic alloys: literature data collection, analysis, and FAIR sharing", arXiv:2310.15083 (Comput. Mater. Sci. 2024); tool doi:10.21981/KPD9-VJ03 |

Papers used to verify models (not redistributed): Maresca & Curtin, arXiv:1901.02100v3 (Acta Mater. 182 (2020)
235-249); Gorsse et al., open version hal-04746750 (Scripta Mater. 255 (2025) 116394).

Not used: `XGBoost_retrainedmodel_oxidation_202406.pkl` from the oxidation repository. Loading a pickle
executes code, and this study trains its own models.

Network access was widened on 2026-10-10; arXiv, nanoHUB and HAL were then reachable.
