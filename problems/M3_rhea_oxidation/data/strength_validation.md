# Strength surrogate validation

Data: 284 single-phase BCC compression records, 92 alloys (MPEA dataset). Target log10 sigma_y, std 0.332.

Physics model constants are unverified (see properties.py).

| Split | Model | RMSE (log10) | R² | 90% coverage | RMS z |
|---|---|---|---|---|---|
| rows | physics | 0.390 ± 0.000 | -0.386 |  | nan |
| rows | physics_cal | 0.379 ± 0.000 | -0.310 |  | nan |
| rows | ml | 0.103 ± 0.005 | 0.904 | 0.87 | 1.23 |
| rows | hybrid | 0.108 ± 0.006 | 0.893 | 0.88 | 1.24 |
| alloy | physics | 0.390 ± 0.000 | -0.386 |  | nan |
| alloy | physics_cal | 0.380 ± 0.001 | -0.316 |  | nan |
| alloy | ml | 0.148 ± 0.009 | 0.798 | 0.83 | 1.33 |
| alloy | hybrid | 0.171 ± 0.003 | 0.732 | 0.85 | 1.37 |
