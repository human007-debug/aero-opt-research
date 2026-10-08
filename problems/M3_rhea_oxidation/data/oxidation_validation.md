# Oxidation surrogate validation

Data: 853 rows, 157 alloys, 63 sources (audited Gorsse et al. 2025 dataset). Target: log10 specific mass gain (mg/cm²), std 0.846.
Noise floor (pooled scatter of 18 repeated composition/T/t groups): 0.188 log10.

5-fold cross-validation, groups randomly assigned to folds, mean ± sd over repeats.

| Split | Features | Model | RMSE (log10) | R² | 90% interval coverage | RMS z |
|---|---|---|---|---|---|---|
| rows | base | ridge | 0.459 ± 0.000 | 0.706 |  |  |
| rows | base | bayes_ridge | 0.459 ± 0.000 | 0.706 | 0.91 | 1.00 |
| rows | base | gbdt | 0.240 ± 0.005 | 0.919 |  |  |
| rows | base | gp | 0.243 ± 0.004 | 0.917 | 0.92 | 0.96 |
| rows | physics | ridge | 0.457 ± 0.000 | 0.709 |  |  |
| rows | physics | bayes_ridge | 0.456 ± 0.000 | 0.709 | 0.91 | 1.01 |
| rows | physics | gbdt | 0.258 ± 0.006 | 0.907 |  |  |
| rows | physics | gp | 0.244 ± 0.002 | 0.917 | 0.91 | 0.95 |
| alloy | base | ridge | 0.510 ± 0.005 | 0.636 |  |  |
| alloy | base | bayes_ridge | 0.510 ± 0.005 | 0.637 | 0.88 | 1.12 |
| alloy | base | gbdt | 0.564 ± 0.030 | 0.554 |  |  |
| alloy | base | gp | 0.524 ± 0.043 | 0.614 | 0.81 | 1.63 |
| alloy | physics | ridge | 0.511 ± 0.005 | 0.635 |  |  |
| alloy | physics | bayes_ridge | 0.509 ± 0.005 | 0.638 | 0.88 | 1.13 |
| alloy | physics | gbdt | 0.520 ± 0.015 | 0.622 |  |  |
| alloy | physics | gp | 0.529 ± 0.028 | 0.608 | 0.81 | 1.59 |
| source | base | ridge | 0.564 ± 0.040 | 0.553 |  |  |
| source | base | bayes_ridge | 0.562 ± 0.039 | 0.556 | 0.84 | 1.24 |
| source | base | gbdt | 0.628 ± 0.031 | 0.448 |  |  |
| source | base | gp | 0.655 ± 0.032 | 0.400 | 0.81 | 1.69 |
| source | physics | ridge | 0.585 ± 0.044 | 0.520 |  |  |
| source | physics | bayes_ridge | 0.575 ± 0.045 | 0.535 | 0.83 | 1.27 |
| source | physics | gbdt | 0.586 ± 0.036 | 0.519 |  |  |
| source | physics | gp | 0.668 ± 0.041 | 0.373 | 0.81 | 1.62 |
