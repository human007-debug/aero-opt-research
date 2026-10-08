"""Diverse shortlist of Pareto-front candidates for experimental testing.

    python -m problems.M3_rhea_oxidation.shortlist [--k 6]

Clusters the predicted front (runs/m3x_pareto/front_candidates.csv) by composition with k-means and
takes, from each cluster, the member closest to the cluster centre. Reports the nearest tested alloys
so an experimentalist can see how far each candidate is from known data. Candidates are predictions.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

from . import evaluator as ev
from . import oxidation_model as ox
from . import strength_model as st

HERE = Path(__file__).parent
RUN = HERE / "runs" / "m3x_pareto"


def comp_vec(s: str) -> np.ndarray:
    d = {m[0]: float(m[1]) for m in re.findall(r"([A-Z][a-z]?)([\d.]+)", s)}
    return np.array([d.get(e, 0.0) for e in ev.ELEMENTS]) / 100


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=6)
    args = ap.parse_args()
    front = pd.read_csv(RUN / "front_candidates.csv")
    C = np.array([comp_vec(s) for s in front.composition])
    km = KMeans(args.k, n_init=20, random_state=0).fit(C)
    pick = [int(np.argmin(np.where(km.labels_ == j, np.linalg.norm(C - km.cluster_centers_[j], axis=1), np.inf)))
            for j in range(args.k)]
    S = st.load(); SC = st.comp_matrix(S["comp"]); Sf = S["FORMULA"].to_numpy()
    O = ox.load(); OC = O[ox.ELEMENTS].to_numpy() / 100; Of = O["Alloy formula"].to_numpy()
    rows = []
    for i in sorted(pick, key=lambda i: front.specific_strength[i]):
        r, c = front.iloc[i], C[i]
        co = np.zeros(len(ox.ELEMENTS))
        for j, e in enumerate(ev.ELEMENTS):
            co[ox.ELEMENTS.index(e)] = c[j]
        ds, do = np.abs(SC - c).sum(1) * 50, np.abs(OC - co).sum(1) * 50
        rows.append({
            "composition (at.%)": " ".join(f"{e}{v*100:.0f}" for e, v in zip(ev.ELEMENTS, c) if v > 0),
            "pred. sigma_y 1000C (MPa)": f"{r.sigma_MPa:.0f} (x/÷{10**r.log_sigma_sd:.2f})",
            "density (g/cm3)": f"{r.density:.2f}",
            "pred. mass gain 1000C/20h (mg/cm2)": f"{10**r.log10_mass_gain:.1f} (x/÷{10**r.log_mass_gain_sd:.1f})",
            "P(BCC)": f"{r.p_bcc:.2f}",
            "nearest oxidation-tested": f"{Of[do.argmin()]} ({do.min():.0f} at.%)",
            "nearest strength-tested": f"{Sf[ds.argmin()]} ({ds.min():.0f} at.%)",
        })
    out = pd.DataFrame(rows)
    out.to_csv(RUN / "shortlist.csv", index=False)
    md = ["# Shortlist for experimental testing (surrogate predictions, not measurements)", "",
          f"{args.k} compositions spread along the predicted Pareto front (k-means on composition, member nearest each "
          "centre). Ranges are ×/÷ one calibrated standard deviation.", "",
          "| " + " | ".join(out.columns) + " |", "|" + "---|" * len(out.columns)]
    md += ["| " + " | ".join(str(v) for v in row) + " |" for row in out.itertuples(index=False)]
    (RUN / "shortlist.md").write_text("\n".join(md) + "\n")
    print((RUN / "shortlist.md").read_text())


if __name__ == "__main__":
    main()
