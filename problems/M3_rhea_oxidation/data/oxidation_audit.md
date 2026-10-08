# Oxidation dataset audit

Raw rows: 886. Unique formulas: 163. Sources: 64.

| Flag | Rows | Action |
|---|---|---|
| ok | 844 | kept |
| formula_mismatch | 30 | excluded |
| corrected | 12 | kept after correction |

Repeated (composition, T, t) records: duplicates 0 rows, conflicting values 48 rows (kept; they measure experimental scatter).
Rows in series where mass gain decreases with time: 35 (kept; may be spallation or digitisation error).
Rows whose source is not a DOI: 45 (Tom_ini); kept but cannot be traced to a publication.

Cleaned rows: 853. Unique compositions: 157.

## Corrections and exclusions

| Row | Formula | Flag | Note | Source |
|---|---|---|---|---|
| 2 | Cr-31Ta | corrected | Nb -> Ta (formula Cr-31Ta) | http://dx.doi.org/10.1179/mht.2000.17.2.009 |
| 3 | Cr-9.5Ta | corrected | Nb -> Ta (formula Cr-9.5Ta) | http://dx.doi.org/10.1179/mht.2000.17.2.009 |
| 71 | NbMoWZr | formula_mismatch | formula NbMoWZr vs columns {'Mo': 2.0, 'Nb': 92.0, 'W': 5.0, 'Zr': 1.0} (closest reading 'ratio', max diff 67.0 at.%) | https://doi.org/10.1016/j.corsci.2021.109513 |
| 99 | Ta2TiCr | formula_mismatch | formula Ta2TiCr vs columns {'Cr': 31.0, 'Ta': 46.5, 'Ti': 22.5} (closest reading 'ratio', max diff 6.0 at.%) | https://doi.org/10.1016/j.jallcom.2023.169000 |
| 100 | WTaNbTiAl | corrected | filled missing W = 20.0 at.% (formula WTaNbTiAl) | https://doi.org/10.1016/j.corsci.2022.110377 |
| 107 | Al0.5NbTaTi | formula_mismatch | formula Al0.5NbTaTi vs columns {'Al': 8.6, 'Nb': 30.1, 'Ta': 35.2, 'Ti': 26.1} (closest reading 'ratio', max diff 6.6 at.%) | Tom_ini |
| 111 | CrNbTaTiZr-BCC | formula_mismatch | formula CrNbTaTiZr-BCC vs columns {'Cr': 12.6, 'Nb': 27.5, 'Ta': 36.2, 'Ti': 15.8, 'Zr': 7.9} (closest reading 'ratio', max diff 16.2 at.%) | Tom_ini |
| 113 | Al0.5CrNbTaTiZr-BCC | formula_mismatch | formula Al0.5CrNbTaTiZr-BCC vs columns {'Al': 7.49, 'Cr': 15.97, 'Nb': 23.86, 'Ta': 31.01, 'Ti': 14.05, 'Zr': 7.62} (closest reading 'at%+equimolar', max diff 12.3 at.%) | Tom_ini |
| 129 | Nb-12Si-15Mo | formula_mismatch | formula Nb-12Si-15Mo vs columns {'Mo': 15.0, 'Nb': 63.0, 'Si': 12.0} (closest reading 'balance at.%', max diff 10.0 at.%) | https://doi.org/10.1007/s11661-007-9398-9 |
| 130 | Nb-12Si-15Mo | formula_mismatch | formula Nb-12Si-15Mo vs columns {'Mo': 15.0, 'Nb': 63.0, 'Si': 12.0} (closest reading 'balance at.%', max diff 10.0 at.%) | https://doi.org/10.1007/s11661-007-9398-9 |
| 131 | Nb-12Si-15Mo | formula_mismatch | formula Nb-12Si-15Mo vs columns {'Mo': 15.0, 'Nb': 63.0, 'Si': 12.0} (closest reading 'balance at.%', max diff 10.0 at.%) | https://doi.org/10.1007/s11661-007-9398-9 |
| 134 | Cr-31Ta | corrected | Nb -> Ta (formula Cr-31Ta) | http://dx.doi.org/10.1179/mht.2000.17.2.009 |
| 135 | Cr-9.5Ta | corrected | Nb -> Ta (formula Cr-9.5Ta) | http://dx.doi.org/10.1179/mht.2000.17.2.009 |
| 199 | NbMoWZr | formula_mismatch | formula NbMoWZr vs columns {'Mo': 2.0, 'Nb': 92.0, 'W': 5.0, 'Zr': 1.0} (closest reading 'ratio', max diff 67.0 at.%) | https://doi.org/10.1016/j.corsci.2021.109513 |
| 234 | Ta2TiCr | formula_mismatch | formula Ta2TiCr vs columns {'Cr': 31.0, 'Ta': 46.5, 'Ti': 22.5} (closest reading 'ratio', max diff 6.0 at.%) | https://doi.org/10.1016/j.jallcom.2023.169000 |
| 240 | WMoTaNbTi | formula_mismatch | formula WMoTaNbTi vs columns {'Mo': 18.0, 'Nb': 17.1, 'Ta': 23.4, 'Ti': 15.1, 'W': 26.4} (closest reading 'ratio', max diff 6.4 at.%) | https://doi.org/10.3390/met12010041 |
| 250 | WTaNbTiAl | corrected | filled missing W = 20.0 at.% (formula WTaNbTiAl) | https://doi.org/10.1016/j.corsci.2022.110377 |
| 266 | Al0.5NbTaTi | formula_mismatch | formula Al0.5NbTaTi vs columns {'Al': 8.6, 'Nb': 30.1, 'Ta': 35.2, 'Ti': 26.1} (closest reading 'ratio', max diff 6.6 at.%) | Tom_ini |
| 270 | CrNbTaTiZr-BCC | formula_mismatch | formula CrNbTaTiZr-BCC vs columns {'Cr': 12.6, 'Nb': 27.5, 'Ta': 36.2, 'Ti': 15.8, 'Zr': 7.9} (closest reading 'ratio', max diff 16.2 at.%) | Tom_ini |
| 272 | Al0.5CrNbTaTiZr-BCC | formula_mismatch | formula Al0.5CrNbTaTiZr-BCC vs columns {'Al': 7.49, 'Cr': 15.97, 'Nb': 23.86, 'Ta': 31.01, 'Ti': 14.05, 'Zr': 7.62} (closest reading 'at%+equimolar', max diff 12.3 at.%) | Tom_ini |
| 277 | Cr-31Ta | corrected | Nb -> Ta (formula Cr-31Ta) | http://dx.doi.org/10.1179/mht.2000.17.2.009 |
| 278 | Cr-9.5Ta | corrected | Nb -> Ta (formula Cr-9.5Ta) | http://dx.doi.org/10.1179/mht.2000.17.2.009 |
| 382 | NbMoWZr | formula_mismatch | formula NbMoWZr vs columns {'Mo': 2.0, 'Nb': 92.0, 'W': 5.0, 'Zr': 1.0} (closest reading 'ratio', max diff 67.0 at.%) | https://doi.org/10.1016/j.corsci.2021.109513 |
| 435 | Ta2TiCr | formula_mismatch | formula Ta2TiCr vs columns {'Cr': 31.0, 'Ta': 46.5, 'Ti': 22.5} (closest reading 'ratio', max diff 6.0 at.%) | https://doi.org/10.1016/j.jallcom.2023.169000 |
| 436 | WTaNbTiAl | corrected | filled missing W = 20.0 at.% (formula WTaNbTiAl) | https://doi.org/10.1016/j.corsci.2022.110377 |
| 442 | Al0.5NbTaTi | formula_mismatch | formula Al0.5NbTaTi vs columns {'Al': 8.6, 'Nb': 30.1, 'Ta': 35.2, 'Ti': 26.1} (closest reading 'ratio', max diff 6.6 at.%) | Tom_ini |
| 446 | CrNbTaTiZr-BCC | formula_mismatch | formula CrNbTaTiZr-BCC vs columns {'Cr': 12.6, 'Nb': 27.5, 'Ta': 36.2, 'Ti': 15.8, 'Zr': 7.9} (closest reading 'ratio', max diff 16.2 at.%) | Tom_ini |
| 448 | Al0.5CrNbTaTiZr-BCC | formula_mismatch | formula Al0.5CrNbTaTiZr-BCC vs columns {'Al': 7.49, 'Cr': 15.97, 'Nb': 23.86, 'Ta': 31.01, 'Ti': 14.05, 'Zr': 7.62} (closest reading 'at%+equimolar', max diff 12.3 at.%) | Tom_ini |
| 464 | Nb-12Si-15Mo | formula_mismatch | formula Nb-12Si-15Mo vs columns {'Mo': 15.0, 'Nb': 63.0, 'Si': 12.0} (closest reading 'balance at.%', max diff 10.0 at.%) | https://doi.org/10.1007/s11661-007-9398-9 |
| 465 | Nb-12Si-15Mo | formula_mismatch | formula Nb-12Si-15Mo vs columns {'Mo': 15.0, 'Nb': 63.0, 'Si': 12.0} (closest reading 'balance at.%', max diff 10.0 at.%) | https://doi.org/10.1007/s11661-007-9398-9 |
| 466 | Nb-12Si-15Mo | formula_mismatch | formula Nb-12Si-15Mo vs columns {'Mo': 15.0, 'Nb': 63.0, 'Si': 12.0} (closest reading 'balance at.%', max diff 10.0 at.%) | https://doi.org/10.1007/s11661-007-9398-9 |
| 469 | Cr-31Ta | corrected | Nb -> Ta (formula Cr-31Ta) | http://dx.doi.org/10.1179/mht.2000.17.2.009 |
| 470 | Cr-9.5Ta | corrected | Nb -> Ta (formula Cr-9.5Ta) | http://dx.doi.org/10.1179/mht.2000.17.2.009 |
| 574 | NbMoWZr | formula_mismatch | formula NbMoWZr vs columns {'Mo': 2.0, 'Nb': 92.0, 'W': 5.0, 'Zr': 1.0} (closest reading 'ratio', max diff 67.0 at.%) | https://doi.org/10.1016/j.corsci.2021.109513 |
| 639 | Ta2TiCr | formula_mismatch | formula Ta2TiCr vs columns {'Cr': 31.0, 'Ta': 46.5, 'Ti': 22.5} (closest reading 'ratio', max diff 6.0 at.%) | https://doi.org/10.1016/j.jallcom.2023.169000 |
| 656 | WTaNbTiAl | corrected | filled missing W = 20.0 at.% (formula WTaNbTiAl) | https://doi.org/10.1016/j.corsci.2022.110377 |
| 672 | Al0.5NbTaTi | formula_mismatch | formula Al0.5NbTaTi vs columns {'Al': 8.6, 'Nb': 30.1, 'Ta': 35.2, 'Ti': 26.1} (closest reading 'ratio', max diff 6.6 at.%) | Tom_ini |
| 676 | CrNbTaTiZr-BCC | formula_mismatch | formula CrNbTaTiZr-BCC vs columns {'Cr': 12.6, 'Nb': 27.5, 'Ta': 36.2, 'Ti': 15.8, 'Zr': 7.9} (closest reading 'ratio', max diff 16.2 at.%) | Tom_ini |
| 678 | Al0.5CrNbTaTiZr-BCC | formula_mismatch | formula Al0.5CrNbTaTiZr-BCC vs columns {'Al': 7.49, 'Cr': 15.97, 'Nb': 23.86, 'Ta': 31.01, 'Ti': 14.05, 'Zr': 7.62} (closest reading 'at%+equimolar', max diff 12.3 at.%) | Tom_ini |
| 805 | Al0.5NbTaTi | formula_mismatch | formula Al0.5NbTaTi vs columns {'Al': 8.6, 'Nb': 30.1, 'Ta': 35.2, 'Ti': 26.1} (closest reading 'ratio', max diff 6.6 at.%) | Tom_ini |
| 809 | CrNbTaTiZr-BCC | formula_mismatch | formula CrNbTaTiZr-BCC vs columns {'Cr': 12.6, 'Nb': 27.5, 'Ta': 36.2, 'Ti': 15.8, 'Zr': 7.9} (closest reading 'ratio', max diff 16.2 at.%) | Tom_ini |
| 811 | Al0.5CrNbTaTiZr-BCC | formula_mismatch | formula Al0.5CrNbTaTiZr-BCC vs columns {'Al': 7.49, 'Cr': 15.97, 'Nb': 23.86, 'Ta': 31.01, 'Ti': 14.05, 'Zr': 7.62} (closest reading 'at%+equimolar', max diff 12.3 at.%) | Tom_ini |
