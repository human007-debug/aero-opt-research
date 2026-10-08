"""Single-phase BCC classifier for refractory compositions (feasibility constraint for the search).

    python -m problems.M3_rhea_oxidation.phase_model    # validation -> data/phase_validation.{json,md}

Data: MPEA dataset (Borg et al. 2020), alloys made only of the strength-model elements, one label per
(formula, processing) pair: 1 if the reported microstructure is "BCC", else 0 (BCC + second phases, B2,
Laves, HCP, ...). Conflicting labels for the same formula and processing are dropped.
Features: at. fractions plus standard descriptors computed from elemental data: rms atomic-volume misfit,
mean and spread of melting point, and mean shear modulus.
Validation: whole formulas held out (grouped folds). Reports ROC AUC, accuracy, and Brier score.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from . import properties as pr
from .oxidation_model import group_folds
from .strength_model import RAW, comp_matrix, parse_formula

HERE = Path(__file__).parent
EL = pr.STRENGTH_ELEMENTS


def descriptors(C: np.ndarray) -> np.ndarray:
    el = pr.elements()
    V = np.array([el[e]["atomic_volume_A3"] for e in EL])
    Tm = np.array([el[e]["melting_point_K"] for e in EL])
    G = np.array([el[e]["shear_modulus_GPa_used"] for e in EL])
    Vb = C @ V
    dV = np.sqrt(np.sum(C * (V[None, :] - Vb[:, None]) ** 2, 1)) / Vb
    Tmb = C @ Tm
    dTm = np.sqrt(np.sum(C * (Tm[None, :] - Tmb[:, None]) ** 2, 1))
    return np.column_stack([C, dV, Tmb / 1000, dTm / 1000, C @ G / 100])


def load() -> pd.DataFrame:
    df = pd.read_csv(RAW)
    df.columns = [c.split(": ")[1] if ": " in c else c for c in df.columns]
    df["comp"] = df["FORMULA"].map(parse_formula)
    df = df[df["comp"].map(lambda c: set(c) <= set(EL)) & df["Microstructure"].notna()].copy()
    df["bcc"] = (df["Microstructure"] == "BCC").astype(int)
    g = df.groupby(["FORMULA", "Processing method"])["bcc"]
    df = df[g.transform("nunique") == 1].drop_duplicates(["FORMULA", "Processing method"]).reset_index(drop=True)
    return df


MODELS = {
    "logistic": lambda: make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=2000)),
    "gbdt": lambda: HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, random_state=0),
}


def validation_study(repeats: int = 5, k: int = 5) -> dict:
    d = load()
    X = descriptors(comp_matrix(d["comp"]))
    y = d["bcc"].to_numpy()
    groups = pd.factorize(d["FORMULA"])[0]
    res = {"n": int(len(d)), "n_formulas": int(groups.max() + 1), "bcc_fraction": float(y.mean()), "results": []}
    for name, mk in MODELS.items():
        auc, acc, brier = [], [], []
        for rep in range(repeats):
            p = np.empty(len(y))
            for tr, te in group_folds(groups, k, np.random.default_rng(rep)):
                p[te] = mk().fit(X[tr], y[tr]).predict_proba(X[te])[:, 1]
            auc.append(roc_auc_score(y, p))
            acc.append(np.mean((p > 0.5) == y))
            brier.append(brier_score_loss(y, p))
        r = {"model": name, "auc": float(np.mean(auc)), "auc_sd": float(np.std(auc)), "accuracy": float(np.mean(acc)),
             "brier": float(np.mean(brier)), "brier_baseline": float(np.mean((y.mean() - y) ** 2))}
        res["results"].append(r)
        print(r, flush=True)
    return res


def fit(name: str = "logistic"):
    d = load()
    return MODELS[name]().fit(descriptors(comp_matrix(d["comp"])), d["bcc"].to_numpy())


if __name__ == "__main__":
    res = validation_study()
    (HERE / "data" / "phase_validation.json").write_text(json.dumps(res, indent=2))
    lines = ["# Single-phase BCC classifier validation", "",
             f"{res['n']} (formula, processing) records, {res['n_formulas']} formulas, BCC fraction {res['bcc_fraction']:.2f}. "
             "Grouped 5-fold CV by formula, 5 repeats.", "",
             "| Model | ROC AUC | Accuracy | Brier | Brier (base rate) |", "|---|---|---|---|---|"]
    for r in res["results"]:
        lines.append(f"| {r['model']} | {r['auc']:.3f} ± {r['auc_sd']:.3f} | {r['accuracy']:.3f} | {r['brier']:.3f} | {r['brier_baseline']:.3f} |")
    (HERE / "data" / "phase_validation.md").write_text("\n".join(lines) + "\n")
