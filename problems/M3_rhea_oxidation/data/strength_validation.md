# Strength surrogate validation

Data: 284 single-phase BCC compression records, 92 alloys (MPEA dataset). Target log10 sigma_y, std 0.332.

Physics model: reduced Maresca-Curtin (2020) edge model with the paper's own inputs, applicable to Mo-Nb-Ta-V-W only (21 records, 4 alloys in the data). The Mo-Nb-Ta-V-W ml row is the all-alloy grouped CV scored on those records only (GP trained on all other alloys).

| Subset | Split | Model | RMSE (log10) | R² | 90% coverage | RMS z |
|---|---|---|---|---|---|---|
| all | rows | ml | 0.103 ± 0.005 | 0.904 | 0.87 | 1.23 |
| all | alloy | ml | 0.148 ± 0.009 | 0.798 | 0.83 | 1.33 |
| Mo-Nb-Ta-V-W | none (no fitting) | physics | 0.119 ± 0.000 | 0.666 |  | nan |
| Mo-Nb-Ta-V-W | alloy | ml | 0.085 ± 0.004 | 0.830 | 0.92 | 1.02 |
