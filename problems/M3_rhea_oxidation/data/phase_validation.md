# Single-phase BCC classifier validation

168 (formula, processing) records, 139 formulas, BCC fraction 0.68. Grouped 5-fold CV by formula, 5 repeats.

| Model | ROC AUC | Accuracy | Brier | Brier (base rate) |
|---|---|---|---|---|
| logistic | 0.837 ± 0.011 | 0.781 | 0.144 | 0.218 |
| gbdt | 0.843 ± 0.010 | 0.798 | 0.153 | 0.218 |
