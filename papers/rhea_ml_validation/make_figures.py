"""Figures for the methods paper. Reads problems/M3_rhea_oxidation/data/paper_stats.json and the datasets.

    python papers/rhea_ml_validation/make_figures.py

Writes figures/fig{1..5}_*.{png,pdf} and, for each, a CSV of the plotted numbers (the table view).
Palette: reference categorical slots 1-3 (blue, orange, aqua), validated all-pairs for colour-vision
deficiency; aqua is below 3:1 contrast, so every series also has a marker shape and a direct label.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from problems.M3_rhea_oxidation import oxidation_model as ox  # noqa: E402
from problems.M3_rhea_oxidation import refoxdb as rx  # noqa: E402
from problems.M3_rhea_oxidation import strength_model as st  # noqa: E402

OUT = Path(__file__).parent / "figures"
STATS = ROOT / "problems" / "M3_rhea_oxidation" / "data" / "paper_stats.json"

SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e1"
S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"
SHORT = {"gp": "GP", "gbdt": "GBDT", "bayes_ridge": "Ridge"}
MODEL_STYLE = {"gp": (S1, "o", "Gaussian process"), "gbdt": (S2, "s", "Gradient-boosted trees"),
               "bayes_ridge": (S3, "^", "Bayesian ridge")}
LN10 = np.log(10)


def style():
    plt.rcParams.update({
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK,
        "xtick.color": INK2, "ytick.color": INK2, "text.color": INK, "axes.linewidth": 0.8,
        "axes.grid": True, "grid.color": GRID, "grid.linestyle": "-", "grid.linewidth": 0.6,
        "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False,
        "lines.linewidth": 2, "lines.markersize": 6, "errorbar.capsize": 0})


def direct_labels(ax, items, min_gap_px=11, dx_px=7, align=False):
    """items: (x, y, text). Place labels right of each end point, nudged apart vertically so none overlap.
    align=True puts every label in one column right of the rightmost point, clear of offset markers."""
    fig = ax.figure
    fig.canvas.draw()
    trans = ax.transData
    pts = sorted(((trans.transform((x, y)), t) for x, y, t in items), key=lambda q: q[0][1])
    ys = []
    for (px, py), _ in pts:
        y = py if not ys or py - ys[-1] >= min_gap_px else ys[-1] + min_gap_px
        ys.append(y)
    inv = trans.inverted()
    px_max = max(p[0][0] for p in pts)
    for ((px, py), t), y in zip(pts, ys):
        xd, yd = inv.transform(((px_max if align else px) + dx_px, y))
        ax.annotate(t, xy=inv.transform((px, py)), xytext=(xd, yd), textcoords="data", fontsize=7.5, color=INK2,
                    va="center", ha="left", annotation_clip=False)


def save(fig, name, table: pd.DataFrame):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}.png", dpi=200, bbox_inches="tight")
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight")
    table.to_csv(OUT / f"{name}.csv", index=False)
    plt.close(fig)


# ---------------------------------------------------------------- Fig 1: data map
def fig1_data_map():
    g = ox.load()
    r = pd.read_csv(rx.OUT)
    s = st.load()
    G = np.unique(g[ox.ELEMENTS].to_numpy() / 100, axis=0)
    R = np.unique(r.loc[~r.in_gorsse, ox.ELEMENTS].to_numpy(float) / 100, axis=0)
    S = np.unique(np.array([[c.get(e, 0.0) for e in ox.ELEMENTS] for c in s["comp"]], float), axis=0)
    S = S / S.sum(1, keepdims=True)
    allc = np.vstack([G, R, S])
    mu = allc.mean(0)
    _, sv, vt = np.linalg.svd(allc - mu, full_matrices=False)
    var = sv**2 / np.sum(sv**2)
    proj = lambda X: (X - mu) @ vt[:2].T
    both = sum(np.abs(S[:, None, :] - G[None]).sum(-1).min(1) * 50 <= 1.0)
    fig, ax = plt.subplots(figsize=(6.2, 4.6))
    sets = [("Oxidation, Gorsse et al. 2025", G, S1, "o"), ("Oxidation, RefOxDB only", R, S2, "s"),
            ("Yield strength, MPEA (single-phase BCC)", S, S3, "^")]
    rows = []
    for name, X, col, mk in sets:
        P = proj(X)
        ax.scatter(P[:, 0], P[:, 1], s=26, c=col, marker=mk, label=f"{name} ({len(X)} alloys)",
                   edgecolors=SURFACE, linewidths=0.6, alpha=0.9)
        rows += [{"dataset": name, "pc1": a, "pc2": b} for a, b in P]
    # element directions
    for j, e in enumerate(ox.ELEMENTS):
        v = vt[:2, j] * 0.55
        if np.hypot(*v) > 0.12:
            ax.annotate(e, xy=(v[0], v[1]), xytext=(v[0] * 1.08, v[1] * 1.08), color=INK2, fontsize=8, ha="center", va="center")
            ax.plot([0, v[0]], [0, v[1]], color=GRID, lw=1, zorder=0)
    ax.set_xlabel(f"PC1 of composition ({var[0]:.0%} of variance)")
    ax.set_ylabel(f"PC2 of composition ({var[1]:.0%} of variance)")
    ax.set_title(f"Strength and oxidation data cover different alloys: {both} compositions appear in both",
                 fontsize=9, loc="left", color=INK)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=1, fontsize=8, markerscale=1.2)
    save(fig, "fig1_data_map", pd.DataFrame(rows))


# ---------------------------------------------------------------- Fig 2: digitisation agreement
def fig2_agreement(stats):
    g = ox.load()
    r = pd.read_csv(rx.OUT)
    gk = g.assign(k=g["source"].map(rx.doi_key))
    pairs = []
    for _, row in r[r["in_gorsse"]].iterrows():
        c = gk[(gk["k"] == rx.doi_key(row["source"])) & (abs(gk[ox.T_COL] - row[ox.T_COL]) < 5) & (gk[ox.t_COL] == row[ox.t_COL])]
        c = c[np.abs(c[ox.ELEMENTS].to_numpy() - row[ox.ELEMENTS].to_numpy(float)).max(1) <= 2.0]
        if len(c):
            pairs.append({"gorsse_mg_cm2": c[ox.Y_COL].mean(), "refoxdb_mg_cm2": row[ox.Y_COL], "curve": row["curve"]})
    p = pd.DataFrame(pairs)
    a = stats["agreement"]
    fig, ax = plt.subplots(figsize=(4.6, 4.4))
    lo, hi = 0.05, 500
    ax.plot([lo, hi], [lo, hi], color=INK2, lw=1, zorder=0)
    for f in (2, 0.5):
        ax.plot([lo, hi], [lo * f, hi * f], color=GRID, lw=1, zorder=0)
    ax.scatter(p.gorsse_mg_cm2, p.refoxdb_mg_cm2, s=22, c=S1, edgecolors=SURFACE, linewidths=0.6)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
    ax.set_xlabel("Gorsse et al. dataset, mass gain (mg/cm²)")
    ax.set_ylabel("RefOxDB, same figure re-digitised (mg/cm²)")
    ax.text(0.04, 0.96, f"{a['pairs']} matched points, {a['curves']} curves\n"
                        f"median |Δlog10| {a['median_abs_log10']:.3f} (95% CI {a['median_abs_log10_ci'][0]:.3f}–{a['median_abs_log10_ci'][1]:.3f})\n"
                        f"beyond ×2: {a['frac_over_x2']:.1%} (95% CI {a['frac_over_x2_ci'][0]:.1%}–{a['frac_over_x2_ci'][1]:.1%})",
            transform=ax.transAxes, va="top", fontsize=8, color=INK2)
    ax.text(hi * 0.8, hi * 0.8 * 0.5, "×0.5", color=INK2, fontsize=7, ha="right", va="top")
    ax.text(hi * 0.4, hi * 0.8, "×2", color=INK2, fontsize=7, ha="right", va="top")
    save(fig, "fig2_digitisation_agreement", p)


# ---------------------------------------------------------------- Fig 3: error vs distance
def fig3_distance(stats):
    fig, axs = plt.subplots(1, 2, figsize=(9.0, 3.9), sharey=True)
    rows, items = [], {}
    for ax, (title, data) in zip(axs, [("Within one dataset (alloy-grouped CV)", stats["internal"]["by_distance"]),
                                       ("Independent dataset (RefOxDB, trained on Gorsse)",
                                        {m: v["by_distance"] for m, v in stats["external"]["models"].items()})]):
        for k, m in enumerate(("gp", "gbdt", "bayes_ridge")):
            col, mk, lab = MODEL_STYLE[m]
            b = data[m]
            x = np.arange(len(b)) + (k - 1) * 0.12
            y = np.array([v["mae_ln"] for v in b])
            lo_ = np.array([v["ci"][0] for v in b]); hi_ = np.array([v["ci"][1] for v in b])
            ax.errorbar(x, y, yerr=[y - lo_, hi_ - y], color=col, marker=mk, lw=1.6, elinewidth=1.2, label=lab)
            items.setdefault(id(ax), (ax, []))[1].append((x[-1], y[-1], SHORT[m]))
            rows += [{"panel": title, "model": m, "bin_at_pct": f"{v['lo']}-{v['hi']}", "n": v["n"], "mae_ln": v["mae_ln"],
                      "ci_lo": v["ci"][0], "ci_hi": v["ci"][1]} for v in b]
        labels = [f"{v['lo']}–{v['hi']}" if v["hi"] < 100 else f"> {v['lo']}" for v in data["gp"]]
        ns = [v["n"] for v in data["gp"]]
        ax.set_xticks(range(len(labels)), [f"{l}\n(n={n})" for l, n in zip(labels, ns)], fontsize=7.5)
        ax.set_xlabel("composition distance to nearest training alloy (at.%)")
        ax.set_title(title, fontsize=9, loc="left")
        ax.set_xlim(-0.4, len(labels) - 0.4 + 0.7)
    axs[0].set_ylabel("mean absolute error, ln(mass gain)")
    axs[0].legend(loc="upper left", fontsize=8)
    for ax in axs:
        ax.set_ylim(0, None)
    sec = axs[1].secondary_yaxis("right", functions=(np.exp, np.log))
    sec.set_ylabel("typical error factor (×)")
    sec.set_yticks([1.5, 2, 3, 5, 10, 20])
    sec.set_yticklabels(["1.5", "2", "3", "5", "10", "20"])
    fig.tight_layout()
    for ax, its in items.values():
        direct_labels(ax, its, min_gap_px=12, dx_px=10, align=True)
    save(fig, "fig3_error_vs_distance", pd.DataFrame(rows))


# ---------------------------------------------------------------- Fig 4: R² by validation scheme
def fig4_schemes(stats):
    schemes = [("Random rows", stats["internal"]["rows"]), ("Unseen alloy", stats["internal"]["alloy"]),
               ("Unseen source paper", stats["internal"]["source"]), ("Independent dataset", stats["external"]["models"])]
    fig, ax = plt.subplots(figsize=(7.6, 3.9))
    rows, items = [], []
    for k, m in enumerate(("gp", "gbdt", "bayes_ridge")):
        col, mk, lab = MODEL_STYLE[m]
        x = np.arange(len(schemes)) + (k - 1) * 0.18
        y = np.array([s[m]["r2"] for _, s in schemes])
        lo_ = np.array([s[m]["r2_ci"][0] for _, s in schemes]); hi_ = np.array([s[m]["r2_ci"][1] for _, s in schemes])
        ax.errorbar(x, y, yerr=[y - lo_, hi_ - y], fmt=mk, color=col, ms=7, elinewidth=1.4, label=lab)
        items.append((x[-1], y[-1], SHORT[m]))
        rows += [{"scheme": n, "model": m, "r2": s[m]["r2"], "ci_lo": s[m]["r2_ci"][0], "ci_hi": s[m]["r2_ci"][1]}
                 for n, s in schemes]
    ax.axhline(0, color=INK2, lw=0.8)
    ax.set_xticks(range(len(schemes)), [n for n, _ in schemes])
    ax.set_ylabel("R², log mass gain (95% CI)")
    ax.set_title("R² falls as validation gets stricter; ridge looks best on unseen source papers but is worst on independent data", fontsize=9, loc="left")
    ax.legend(loc="lower left", fontsize=8)
    ax.set_xlim(-0.5, len(schemes) - 0.5 + 0.25)
    direct_labels(ax, items, min_gap_px=12, dx_px=10, align=True)
    save(fig, "fig4_r2_by_validation_scheme", pd.DataFrame(rows))


# ---------------------------------------------------------------- Fig 5: fronts by surrogate
def fig5_fronts(stats):
    from problems.M3_rhea_oxidation.surrogate_dependence import RUNS, expected_error_log10, front
    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    rows, items = [], []
    for m in ("gp", "gbdt", "bayes_ridge"):
        col, mk, lab = MODEL_STYLE[m]
        f = front(RUNS[m])
        err = expected_error_log10(f.ox_distance_at_pct.to_numpy())
        ax.fill_between(f.specific_strength, f.log10_mass_gain - err, f.log10_mass_gain + err, color=col, alpha=0.10, lw=0)
        ax.plot(f.specific_strength, f.log10_mass_gain, color=col, lw=2, label=f"front found with {lab}")
        items.append((f.specific_strength.iloc[-1], f.log10_mass_gain.iloc[-1], SHORT[m]))
        rows += [{"surrogate": m, "specific_strength": a, "log10_mass_gain": b, "expected_error_log10": e}
                 for a, b, e in zip(f.specific_strength, f.log10_mass_gain, err)]
    c = stats["curse_frac_other_3x_worse"]["gp"]
    ax.text(0.02, 0.97, "On the Gaussian-process front, the other models predict ≥3× higher mass gain for\n"
                        f"{c['gbdt']['mean']:.0%} (seed range {c['gbdt']['min']:.0%}–{c['gbdt']['max']:.0%}, GBDT) and "
                        f"{c['bayes_ridge']['mean']:.0%} ({c['bayes_ridge']['min']:.0%}–{c['bayes_ridge']['max']:.0%}, ridge) of points",
            transform=ax.transAxes, va="top", fontsize=7.5, color=INK2)
    ax.set_xlabel("predicted specific yield strength at 1000 °C (MPa cm³/g)")
    ax.set_ylabel("predicted log10 mass gain, 1000 °C, 20 h")
    ax.legend(loc="lower right", fontsize=8)
    ax.set_title("Predicted Pareto fronts depend on the surrogate (bands: expected external error)", fontsize=9, loc="left")
    direct_labels(ax, items)
    save(fig, "fig5_fronts_by_surrogate", pd.DataFrame(rows))


def main():
    style()
    stats = json.loads(STATS.read_text())
    fig1_data_map()
    fig2_agreement(stats)
    fig3_distance(stats)
    fig4_schemes(stats)
    fig5_fronts(stats)
    print("figures written to", OUT)


if __name__ == "__main__":
    main()
