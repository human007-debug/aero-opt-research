"""Audit and clean the Gorsse et al. (2025) oxidation dataset.

    python -m problems.M3_rhea_oxidation.data_audit

Raw data are never edited. Every row gets flags; the cleaned table keeps rows that pass, applies only
unambiguous corrections (each one recorded), and is written to data/oxidation_clean.csv together
with data/oxidation_audit.md.

Checks
  1. Formula vs composition columns. Formulas in two unambiguous notations are parsed:
       subscript  "NbTa0.5TiZr", "Ti38V15Nb23Hf24"  (element then optional amount; amounts are ratios)
       balance    "Cr-31Nb", "Nb-24Ti-18Si-5Cr", "Ti-43Al2W0.1Si"  (first element is the balance, at.%)
     Other notations (labels such as "AlTiCrMoNb-2", wt.% such as "AlTi-5wtMo") are only checked for
     element-set agreement where possible, else left unchecked.
  2. Composition sums to 100 at.% (rows below 99 contain elements outside the 11 columns).
  3. Repeated (composition, T, t) records: same value -> duplicate; different values -> conflict.
  4. Mass gain decreasing with time within one (source, alloy, T) series.
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
RAW = HERE / "data" / "raw" / "alloy_oxidation_886_202406.csv"
CLEAN = HERE / "data" / "oxidation_clean.csv"
REPORT = HERE / "data" / "oxidation_audit.md"

ELEMENTS = ["Al", "Cr", "Hf", "Mo", "Nb", "Si", "Ta", "Ti", "V", "W", "Zr"]
TOL_AT = 4.0  # at.%: nominal vs measured compositions differ by a few at.%
T_COL, t_COL, Y_COL = "Temperature (C)", "time (h)", "specific mass gain (mg/cm2)"
EL = r"(?:Al|Cr|Hf|Mo|Nb|Si|Ta|Ti|V|W|Zr|Fe|Ni|Co|Re|B|C|Y|Ge|Sn|Mn|Cu)"
NUM = r"\d+(?:\.\d+)?"


def _norm(d: dict[str, float]) -> dict[str, float]:
    tot = sum(d.values())
    return {k: 100 * v / tot for k, v in d.items()}


def wt_to_at(wt: dict[str, float]) -> dict[str, float]:
    import periodictable as pt
    return _norm({e: w / getattr(pt, e).mass for e, w in wt.items()})


def interpretations(f: str) -> list[tuple[str, dict[str, float]]]:
    """Every plausible at.% reading of a formula string. Empty if none applies."""
    s = re.sub(r"-(?:BCC|B2|FCC|HCP)$", "", f.strip())  # phase labels, not elements
    out: list[tuple[str, dict[str, float]]] = []
    if re.fullmatch(rf"(?:{EL}(?:{NUM})?)+", s):
        parts = re.findall(rf"({EL})({NUM})?", s)
        # (a) subscripts are ratios: NbTa0.5TiZr, Ti38V15Nb23Hf24
        amt: dict[str, float] = {}
        for el, n in parts:
            amt[el] = amt.get(el, 0.0) + (float(n) if n else 1.0)
        out.append(("ratio", _norm(amt)))
        # (b) numbers are at.%, unnumbered elements share the balance equally: Al5CrMoTaTi
        given = {el: float(n) for el, n in parts if n}
        free = [el for el, n in parts if not n]
        if given and free and sum(given.values()) < 100:
            out.append(("at%+equimolar", {**given, **{el: (100 - sum(given.values())) / len(free) for el in free}}))
        # (c) first element is the balance, numbers are at.%: Ti23Al -> Ti-23Al
        if not parts[0][1] or len(parts) == 2:
            rest = {el: float(n) for el, n in parts[1:] if n}
            if len(parts) == 2 and parts[0][1] and not parts[1][1]:
                rest = {parts[1][0]: float(parts[0][1])}
            if rest and sum(rest.values()) < 100 and len(rest) == len(parts) - 1:
                out.append(("balance", {parts[0][0]: 100 - sum(rest.values()), **rest}))
    m = re.fullmatch(rf"({EL})((?:-?{NUM}{EL})+)", s)
    if m:
        base = m.group(1)
        amt = {}
        for n, el in re.findall(rf"({NUM})({EL})", m.group(2)):
            amt[el] = amt.get(el, 0.0) + float(n)
        if sum(amt.values()) < 100 and base not in amt:
            bal = {**amt, base: 100 - sum(amt.values())}
            out.append(("balance at.%", bal))
            out.append(("balance wt.%", wt_to_at(bal)))
    return out


def parse_formula(f: str) -> tuple[str, dict[str, float] | None]:
    """First interpretation (kept for tests); see interpretations() for the full set."""
    it = interpretations(f)
    return (it[0][0], it[0][1]) if it else ("other", None)


def element_set_from_text(f: str) -> set[str] | None:
    """Element symbols named in a label-style formula, if every token is an element or a number/suffix."""
    f = re.sub(r"-(?:BCC|B2|FCC|HCP)$", "", f)
    if "wt" in f:
        return None
    els = re.findall(EL, f)
    rest = re.sub(EL, "", f)
    return set(els) if els and re.fullmatch(r"[\d.\-]*", rest) else None


def audit(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    comp = out[ELEMENTS]
    out["comp_sum"] = comp.sum(axis=1)
    notes, flags, corrected = [], [], []
    for i, row in out.iterrows():
        f = row["Alloy formula"]
        readings = interpretations(f)
        notation = "parsed" if readings else "other"
        cols = {e: row[e] for e in ELEMENTS if row[e] > 0}
        flag, note, fix = "ok", "", None
        if readings:
            foreign = set().union(*(set(r) for _, r in readings)) - set(ELEMENTS)
            if foreign:
                flag, note = "foreign_element", f"formula has {sorted(foreign)} outside the 11 columns"
            else:
                diffs = [(max(abs(r.get(e, 0.0) - row[e]) for e in ELEMENTS), name, r) for name, r in readings]
                diff, name, parsed = min(diffs, key=lambda d: d[0])
                if diff > TOL_AT:
                    # Unambiguous fix 1: one formula element has no column value and the columns sum short
                    # of 100 by exactly the amount the formula gives it.
                    for _, _, r in diffs:
                        missing = [e for e in r if row[e] == 0]
                        others_ok = all(abs(r[e] - row[e]) < 0.5 for e in r if e not in missing)
                        if len(missing) == 1 and others_ok and abs((100 - row["comp_sum"]) - r[missing[0]]) < 0.5:
                            flag, note, fix = "corrected", f"filled missing {missing[0]} = {r[missing[0]]:.1f} at.% (formula {f})", ("fill", missing[0], r[missing[0]])
                            break
                    # Unambiguous fix 2: same amounts, one element entered in the wrong column.
                    for _, _, r in ([] if fix else diffs):
                        wrong = {e for e in cols if r.get(e, 0) == 0}
                        missing = {e for e in r if row[e] == 0}
                        if len(wrong) == 1 and len(missing) == 1:
                            w, m_ = next(iter(wrong)), next(iter(missing))
                            if abs(row[w] - r[m_]) < 0.5:
                                flag, note, fix = "corrected", f"{w} -> {m_} (formula {f})", (w, m_)
                                break
                    if fix is None:
                        flag, note = "formula_mismatch", f"formula {f} vs columns {cols} (closest reading '{name}', max diff {diff:.1f} at.%)"
        else:
            es = element_set_from_text(f)
            if es is not None and es - set(ELEMENTS):
                flag, note = "foreign_element", f"formula names {sorted(es - set(ELEMENTS))}"
            elif es is not None and es != set(cols):
                flag, note = "element_set_mismatch", f"formula {f} names {sorted(es)}, columns {sorted(cols)}"
            elif notation == "other":
                note = "formula not parsed (label or wt.%); element set " + ("matches" if es else "unchecked")
        if flag == "ok" and abs(row["comp_sum"] - 100) > 1:
            flag, note = "composition_sum", f"columns sum to {row['comp_sum']:.1f} at.%"
        flags.append(flag)
        notes.append(note)
        corrected.append(fix)
    out["flag"], out["note"] = flags, notes
    for i, fix in zip(out.index, corrected):
        if fix and fix[0] == "fill":
            out.loc[i, fix[1]] = fix[2]
        elif fix:
            w, m_ = fix
            out.loc[i, m_], out.loc[i, w] = out.loc[i, w], 0.0
    out["comp_sum"] = out[ELEMENTS].sum(axis=1)
    out["source_is_doi"] = out["source"].astype(str).str.contains("doi", case=False)

    # Repeats of (composition, T, t)
    key = ELEMENTS + [T_COL, t_COL]
    grp = out.groupby(key, sort=False)[Y_COL]
    nuniq = grp.transform("nunique")
    size = grp.transform("size")
    out["repeat"] = np.where(size > 1, np.where(nuniq > 1, "conflict", "duplicate"), "")

    # Monotonicity within a series
    out["non_monotonic"] = False
    for _, g in out.groupby(["source", "Alloy formula", T_COL]):
        g = g.sort_values(t_COL)
        y = g[Y_COL].to_numpy()
        if len(y) > 1 and np.any(np.diff(y) < -1e-9):
            out.loc[g.index, "non_monotonic"] = True
    return out


def clean(aud: pd.DataFrame) -> pd.DataFrame:
    keep = aud["flag"].isin(["ok", "corrected"])
    c = aud[keep].copy()
    c = c.drop_duplicates(ELEMENTS + [T_COL, t_COL, Y_COL])  # exact repeats once
    return c


def report(aud: pd.DataFrame, cl: pd.DataFrame) -> str:
    lines = ["# Oxidation dataset audit", "",
             f"Raw rows: {len(aud)}. Unique formulas: {aud['Alloy formula'].nunique()}. Sources: {aud['source'].nunique()}.", "",
             "| Flag | Rows | Action |", "|---|---|---|"]
    act = {"ok": "kept", "corrected": "kept after correction", "formula_mismatch": "excluded",
           "element_set_mismatch": "excluded", "foreign_element": "excluded", "composition_sum": "excluded"}
    for k, v in aud["flag"].value_counts().items():
        lines.append(f"| {k} | {v} | {act.get(k, '')} |")
    lines += ["", f"Repeated (composition, T, t) records: duplicates {int((aud['repeat']=='duplicate').sum())} rows, "
              f"conflicting values {int((aud['repeat']=='conflict').sum())} rows (kept; they measure experimental scatter).",
              f"Rows in series where mass gain decreases with time: {int(aud['non_monotonic'].sum())} (kept; may be spallation or digitisation error).",
              f"Rows whose source is not a DOI: {int((~aud['source_is_doi']).sum())} "
              f"({', '.join(sorted(aud.loc[~aud['source_is_doi'], 'source'].astype(str).unique()))}); kept but cannot be traced to a publication.",
              "", f"Cleaned rows: {len(cl)}. Unique compositions: {cl[ELEMENTS].drop_duplicates().shape[0]}.", "",
              "## Corrections and exclusions", "", "| Row | Formula | Flag | Note | Source |", "|---|---|---|---|---|"]
    for i, r in aud[aud["flag"] != "ok"].iterrows():
        lines.append(f"| {i} | {r['Alloy formula']} | {r['flag']} | {r['note']} | {r['source']} |")
    return "\n".join(lines) + "\n"


def main():
    raw = pd.read_csv(RAW)
    aud = audit(raw)
    cl = clean(aud)
    cl.drop(columns=["comp_sum"]).to_csv(CLEAN, index=False)
    REPORT.write_text(report(aud, cl))
    print(REPORT.read_text()[:3000])


if __name__ == "__main__":
    main()
