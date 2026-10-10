"""Refractory Oxidation Database (RefOxDB, Purdue) as a second, independent oxidation dataset.

    python -m problems.M3_rhea_oxidation.refoxdb     # build data/refoxdb_points.csv + data/refoxdb_audit.md

Source: S. Mishra et al., "Mass uptake during oxidation of metallic alloys: literature data collection,
analysis, and FAIR sharing", arXiv:2310.15083; nanoHUB tool refoxdb (doi:10.21981/KPD9-VJ03), source
release r53 (GPL-3.0), files bin/compiled_metadata.xlsx and bin/oxidation_curves_data/*.csv.

The curve files are in the units given by the metadata (Time_Unit, MassGain_Unit), as the tool's own schema
states; their column headers are generic labels and are not used for units. Processing:
  1. Convert time to h and mass gain to mg/cm^2; oxygen partial pressure to atm.
  2. Keep air exposures (0.15 <= p_O2 <= 0.25 atm) and alloys made only of the 11 Gorsse-dataset elements.
  3. Convert wt.% formulas to at.%.
  4. Read each curve at t in {3, 4, 10, 20, 50, 100} h by linear interpolation, only inside the measured
     time range (no extrapolation); drop non-positive mass gains (volatilisation / spallation) and count them.
  5. Mark records that duplicate the Gorsse dataset (same source DOI, composition within 2 at.%, same T).
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

from .data_audit import UNIT_CONFLICTS, wt_to_at
from .oxidation_model import ELEMENTS, T_COL, Y_COL, t_COL, load

HERE = Path(__file__).parent
RAW = HERE / "data" / "raw" / "refoxdb_r53"
OUT = HERE / "data" / "refoxdb_points.csv"
REPORT = HERE / "data" / "refoxdb_audit.md"
TIMES_H = [3, 4, 10, 20, 50, 100]
TIME_TO_H = {"hr": 1.0, "min": 1 / 60, "s": 1 / 3600}
MASS_TO_MG_CM2 = {"mg/cm**2": 1.0, "ug/cm**2": 1e-3, "g/cm**2": 1e3, "kg/m**2": 100.0, "g/m**2": 0.1,
                  "mg/mm**2": 100.0}
P_TO_ATM = {"atm": 1.0, "mmHg": 1 / 760, "Torr": 1 / 760, "cmHg": 1 / 76, "Pa": 1 / 101325}


def parse_formula(s: str) -> dict[str, float]:
    return {m[0]: float(m[1]) for m in re.findall(r"([A-Z][a-z]?)(\d+(?:\.\d+)?)", s)}


def temperature_C(row) -> tuple[float, str]:
    """Metadata Temp is documented in C; file names carry an explicit unit, which wins if it says K."""
    m = re.search(r"_(\d+(?:\.\d+)?)(C|K)_", str(row["Mass_gain_vs_time_file"]) + "_")
    if m and m.group(2) == "K" and abs(float(m.group(1)) - row["Temp"]) < 1:
        return row["Temp"] - 273.15, "K in file name"
    return float(row["Temp"]), ""


def build(raw: Path = RAW) -> tuple[pd.DataFrame, dict]:
    md = pd.read_excel(raw / "compiled_metadata.xlsx")
    stats = {"curves": len(md)}
    rows, notes = [], {"non_air": 0, "other_elements": 0, "unknown_units": 0, "nonpositive": 0, "no_overlap_times": 0,
                       "temperature_from_kelvin": 0, "unit_conflict": 0}
    for _, r in md.iterrows():
        if r["Time_Unit"] not in TIME_TO_H or r["MassGain_Unit"] not in MASS_TO_MG_CM2 or r["p_O2_Unit"] not in P_TO_ATM:
            notes["unknown_units"] += 1
            continue
        pO2 = r["p_O2"] * P_TO_ATM[r["p_O2_Unit"]]
        if not 0.15 <= pO2 <= 0.25:
            notes["non_air"] += 1
            continue
        if any(d in str(r["Ref"]).lower() for d in UNIT_CONFLICTS):
            notes["unit_conflict"] += 1
            continue
        comp = parse_formula(str(r["Chemical_Formula"]))
        if not comp or set(comp) - set(ELEMENTS):
            notes["other_elements"] += 1
            continue
        if str(r["Formula_ID"]).strip() == "wt%":
            comp = wt_to_at(comp)
        tot = sum(comp.values())
        comp = {e: 100 * v / tot for e, v in comp.items()}
        T, tnote = temperature_C(r)
        notes["temperature_from_kelvin"] += bool(tnote)
        c = pd.read_csv(raw / "oxidation_curves_data" / f"{r['Mass_gain_vs_time_file']}.csv")
        t = c.iloc[:, 0].to_numpy(float) * TIME_TO_H[r["Time_Unit"]]
        y = c.iloc[:, 1].to_numpy(float) * MASS_TO_MG_CM2[r["MassGain_Unit"]]
        o = np.argsort(t)
        t, y = t[o], y[o]
        got = False
        for tq in TIMES_H:
            if t[0] <= tq <= t[-1]:
                v = float(np.interp(tq, t, y))
                if v <= 0:
                    notes["nonpositive"] += 1
                    continue
                rows.append({**{e: comp.get(e, 0.0) for e in ELEMENTS}, T_COL: T, t_COL: tq, Y_COL: v,
                             "source": str(r["Ref"]).strip(), "curve": r["Mass_gain_vs_time_file"],
                             "formula": r["Chemical_Formula"]})
                got = True
        notes["no_overlap_times"] += not got
    df = pd.DataFrame(rows)
    stats.update(notes)
    return df, stats


def doi_key(s: str) -> str:
    m = re.search(r"10\.\d{4,9}/\S+", str(s))
    return m.group(0).lower().rstrip(".") if m else str(s).lower()


def mark_overlap(r: pd.DataFrame, g: pd.DataFrame | None = None, tol_at: float = 2.0) -> pd.DataFrame:
    """in_gorsse: same DOI, same T (within 5 C) and composition within tol_at at.% (max element diff)."""
    g = load() if g is None else g
    gk = g.assign(k=g["source"].map(doi_key))
    r = r.copy()
    r["in_gorsse"] = False
    for i, row in r.iterrows():
        cand = gk[(gk["k"] == doi_key(row["source"])) & (abs(gk[T_COL] - row[T_COL]) < 5)]
        if len(cand) and (np.abs(cand[ELEMENTS].to_numpy() - row[ELEMENTS].to_numpy(float)).max(1) <= tol_at).any():
            r.loc[i, "in_gorsse"] = True
    return r


def digitisation_agreement(r: pd.DataFrame, g: pd.DataFrame | None = None) -> dict:
    """Compare points present in both datasets (same DOI, T within 5 C, same t, composition within 2 at.%)."""
    g = load() if g is None else g
    gk = g.assign(k=g["source"].map(doi_key))
    pairs = []
    for _, row in r[r["in_gorsse"]].iterrows():
        c = gk[(gk["k"] == doi_key(row["source"])) & (abs(gk[T_COL] - row[T_COL]) < 5) & (gk[t_COL] == row[t_COL])]
        c = c[np.abs(c[ELEMENTS].to_numpy() - row[ELEMENTS].to_numpy(float)).max(1) <= 2.0]
        if len(c):
            pairs.append(np.log10(row[Y_COL]) - np.log10(c[Y_COL].to_numpy()).mean())
    d = np.array(pairs)
    return {"pairs": int(len(d)), "median_log10_diff": float(np.median(d)), "mad_log10": float(np.median(np.abs(d))),
            "rms_log10": float(np.sqrt(np.mean(d**2))), "frac_over_x2": float(np.mean(np.abs(d) > np.log10(2))),
            "frac_over_x10": float(np.mean(np.abs(d) > 1))}


def external_test(models=("bayes_ridge", "gbdt", "gp"), bins=(0, 5, 10, 20, 100)) -> dict:
    """Train on the full audited Gorsse dataset; predict RefOxDB-only points. Errors in ln units."""
    from .oxidation_model import PROBABILISTIC, make_model, xy
    g = load()
    r = pd.read_csv(OUT)
    new = r[~r["in_gorsse"]].reset_index(drop=True)
    Xg, yg = xy(g, "base")
    Xn, yn = xy(new, "base")
    U = np.unique(g[ELEMENTS].to_numpy() / 100, axis=0)
    dist = np.abs(new[ELEMENTS].to_numpy(float)[:, None, :] / 100 - U[None]).sum(-1).min(1) * 50
    res = {"n_points": int(len(new)), "n_compositions": int(new[ELEMENTS].round(1).drop_duplicates().shape[0]),
           "n_sources": int(new["source"].nunique()), "distance_quantiles_25_50_75": np.quantile(dist, [.25, .5, .75]).tolist(),
           "models": {}}
    for name in models:
        m = make_model(name, Xg.shape[1]).fit(Xg, yg)
        if name in PROBABILISTIC:
            p, sd = m.predict(Xn, return_std=True)
            if name == "bayes_ridge":
                sd = sd * 1.12  # calibration factor from grouped CV (problem.yaml)
        else:
            p, sd = m.predict(Xn), None
        ae = np.abs(p - yn) * np.log(10)
        by = []
        for lo, hi in zip(bins[:-1], bins[1:]):
            sel = (dist >= lo) & (dist < hi)
            if sel.any():
                by.append({"lo": lo, "hi": hi, "n": int(sel.sum()), "mae_ln": float(ae[sel].mean())})
        out = {"mae_ln": float(ae.mean()), "r2": float(1 - np.mean((p - yn) ** 2) / yn.var()), "by_distance": by}
        if sd is not None:
            out["coverage90"] = float(np.mean(np.abs(p - yn) <= 1.645 * sd))
        res["models"][name] = out
    return res


def main():
    df, st = build()
    df = mark_overlap(df)
    df.to_csv(OUT, index=False)
    alloys = df[ELEMENTS].round(1).drop_duplicates()
    new = df[~df["in_gorsse"]]
    lines = ["# RefOxDB processing audit", "",
             f"Curves in metadata: {st['curves']}. Excluded: not air {st['non_air']}, elements outside the 11 "
             f"{st['other_elements']}, unknown units {st['unknown_units']}, unit conflict with Gorsse data {st['unit_conflict']}, "
             f"no curve point inside 3-100 h "
             f"{st['no_overlap_times']}. Non-positive interpolated mass gains dropped: {st['nonpositive']}. "
             f"Temperatures converted from K (file name): {st['temperature_from_kelvin']}.", "",
             f"Points kept: {len(df)} from {df['curve'].nunique()} curves, {len(alloys)} compositions, "
             f"{df['source'].nunique()} sources.",
             f"Points duplicating the Gorsse dataset (same DOI, T, composition within 2 at.%): {int(df['in_gorsse'].sum())}.",
             f"RefOxDB-only points (external test set): {len(new)} from {new['curve'].nunique()} curves, "
             f"{new[ELEMENTS].round(1).drop_duplicates().shape[0]} compositions, {new['source'].nunique()} sources."]
    ag = digitisation_agreement(df)
    lines += ["", f"Independent digitisations of the same figures ({ag['pairs']} matched points): median log10 difference "
              f"{ag['median_log10_diff']:+.3f}, median |difference| {ag['mad_log10']:.3f}, RMS {ag['rms_log10']:.3f}; "
              f"{ag['frac_over_x2']:.1%} differ by more than x2, {ag['frac_over_x10']:.1%} by more than x10."]
    REPORT.write_text("\n".join(lines) + "\n")
    import json
    ext = external_test()
    (HERE / "data" / "refoxdb_external_test.json").write_text(json.dumps({"digitisation_agreement": ag, "external": ext}, indent=2))
    print(REPORT.read_text())
    print(json.dumps(ext, indent=1))


if __name__ == "__main__":
    main()
