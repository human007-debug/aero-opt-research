"""Convergence and reliability plots for an experiment."""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from .metrics import reliability  # noqa: E402


def convergence(curves_by_opt: dict[str, np.ndarray], path: Path, ylabel: str, sign: float = 1.0,
                optimum: float | None = None, title: str = ""):
    """Median and inter-quartile band of best-so-far vs evaluations. sign=-1 plots maximised quantities.

    Runs without a feasible design yet count as +inf, so a quantile is drawn only once that fraction
    of runs is feasible (no interpolation across inf; the curves stay monotone).
    """
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    for name, c in curves_by_opt.items():
        q = np.quantile(c, [0.25, 0.5, 0.75], axis=0, method="inverted_cdf")
        y = sign * np.where(np.isfinite(q), q, np.nan)
        n = np.arange(1, c.shape[1] + 1)
        ax.plot(n, y[1], label=f"{name} (median, {c.shape[0]} runs)")
        ax.fill_between(n, y[0], y[2], alpha=0.25)
    if optimum is not None:
        ax.axhline(sign * optimum, color="k", ls="--", lw=1, label="global optimum")
    ax.set_xscale("log")
    ax.set_xlabel("evaluations")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def reliability_plot(curves_by_opt: dict[str, np.ndarray], target: float, path: Path, title: str = ""):
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    for name, c in curves_by_opt.items():
        ax.plot(np.arange(1, c.shape[1] + 1), reliability(c, target), label=name)
    ax.axhline(0.8, color="k", ls=":", lw=1, label="80% (price of search)")
    ax.set_xlabel("evaluations")
    ax.set_ylabel("reliability (fraction of runs at a practical optimum)")
    ax.set_ylim(0, 1.02)
    ax.set_title(title)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
