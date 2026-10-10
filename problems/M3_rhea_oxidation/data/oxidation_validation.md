# Oxidation surrogate validation

Data: 851 rows, 155 alloys, 62 sources (audited Gorsse et al. 2025 dataset). Target: log10 specific mass gain (mg/cm²), std 0.844.
Noise floor (pooled scatter of 18 repeated composition/T/t groups): 0.188 log10.

5-fold cross-validation, groups randomly assigned to folds, mean ± sd over repeats.

| Split | Features | Model | RMSE (log10) | R² | 90% interval coverage | RMS z |
|---|---|---|---|---|---|---|
| rows | base | ridge | 0.447 ± 0.003 | 0.719 |  |  |
| rows | base | bayes_ridge | 0.447 ± 0.003 | 0.720 | 0.90 | 1.01 |
| rows | base | gbdt | 0.234 ± 0.008 | 0.923 |  |  |
| rows | base | gp | 0.235 ± 0.005 | 0.922 | 0.92 | 0.94 |
| rows | physics | ridge | 0.441 ± 0.002 | 0.726 |  |  |
| rows | physics | bayes_ridge | 0.441 ± 0.002 | 0.726 | 0.90 | 1.01 |
| rows | physics | gbdt | 0.245 ± 0.008 | 0.916 |  |  |
| rows | physics | gp | 0.238 ± 0.007 | 0.920 | 0.92 | 0.95 |
| alloy | base | ridge | 0.495 ± 0.010 | 0.655 |  |  |
| alloy | base | bayes_ridge | 0.495 ± 0.010 | 0.655 | 0.87 | 1.13 |
| alloy | base | gbdt | 0.559 ± 0.021 | 0.559 |  |  |
| alloy | base | gp | 0.547 ± 0.014 | 0.579 | 0.79 | 1.70 |
| alloy | physics | ridge | 0.495 ± 0.008 | 0.655 |  |  |
| alloy | physics | bayes_ridge | 0.492 ± 0.008 | 0.659 | 0.86 | 1.13 |
| alloy | physics | gbdt | 0.505 ± 0.012 | 0.641 |  |  |
| alloy | physics | gp | 0.534 ± 0.021 | 0.598 | 0.80 | 1.61 |
| source | base | ridge | 0.557 ± 0.040 | 0.562 |  |  |
| source | base | bayes_ridge | 0.556 ± 0.040 | 0.563 | 0.82 | 1.28 |
| source | base | gbdt | 0.628 ± 0.019 | 0.445 |  |  |
| source | base | gp | 0.642 ± 0.024 | 0.419 | 0.79 | 1.74 |
| source | physics | ridge | 0.574 ± 0.048 | 0.533 |  |  |
| source | physics | bayes_ridge | 0.570 ± 0.048 | 0.540 | 0.81 | 1.33 |
| source | physics | gbdt | 0.570 ± 0.002 | 0.543 |  |  |
| source | physics | gp | 0.651 ± 0.044 | 0.401 | 0.79 | 1.68 |
