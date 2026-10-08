"""M3X data audit, property models and surrogates."""
import numpy as np
import pandas as pd
import pytest

from problems.M3_rhea_oxidation import data_audit as da
from problems.M3_rhea_oxidation import properties as pr
from problems.M3_rhea_oxidation import strength_model as st


# ---------------------------------------------------------------- data audit
@pytest.mark.parametrize("formula,expected", [
    ("NbTa0.5TiZr", {"Nb": 100 / 3.5, "Ta": 50 / 3.5, "Ti": 100 / 3.5, "Zr": 100 / 3.5}),
    ("Cr-31Nb", {"Cr": 69.0, "Nb": 31.0}),
    ("Ti-43Al2W0.1Si", {"Ti": 54.9, "Al": 43.0, "W": 2.0, "Si": 0.1}),
])
def test_formula_readings(formula, expected):
    readings = [r for _, r in da.interpretations(formula)]
    assert any(all(abs(r.get(k, 0) - v) < 1e-6 for k, v in expected.items()) for r in readings)


def test_ambiguous_notations_have_matching_reading():
    for f, cols in [("Ti23Al", {"Ti": 77, "Al": 23}), ("Al5CrMoTaTi", {"Al": 5, "Cr": 23.75, "Mo": 23.75, "Ta": 23.75, "Ti": 23.75})]:
        assert any(all(abs(r.get(k, 0) - v) < 0.01 for k, v in cols.items()) for _, r in da.interpretations(f))


def test_wt_percent_conversion_ti64():
    at = da.wt_to_at({"Ti": 90, "Al": 6, "V": 4})
    assert at["Al"] == pytest.approx(10.2, abs=0.1) and at["V"] == pytest.approx(3.6, abs=0.1)


@pytest.fixture(scope="module")
def audit():
    return da.audit(pd.read_csv(da.RAW))


def test_known_errors_are_corrected(audit):
    r = audit[audit["Alloy formula"] == "Cr-31Ta"].iloc[0]
    assert r["flag"] == "corrected" and r["Ta"] == 31 and r["Nb"] == 0
    w = audit[audit["Alloy formula"] == "WTaNbTiAl"].iloc[0]
    assert w["flag"] == "corrected" and w["W"] == 20 and w["comp_sum"] == pytest.approx(100)


def test_phase_composition_records_excluded(audit):
    assert (audit.loc[audit["Alloy formula"].str.endswith("-BCC"), "flag"] == "formula_mismatch").all()


def test_clean_dataset_matches_committed_file(audit):
    cl = da.clean(audit).drop(columns=["comp_sum"]).reset_index(drop=True)
    committed = pd.read_csv(da.CLEAN)
    assert len(cl) == len(committed) == 853
    np.testing.assert_allclose(cl[da.ELEMENTS].to_numpy(), committed[da.ELEMENTS].to_numpy())


# ---------------------------------------------------------------- properties
@pytest.mark.parametrize("e", ["Nb", "Mo", "Ta", "W", "V", "Cr"])
def test_density_of_pure_bcc_element_matches_listed(e):
    listed = pr.elements()[e]["density_kg_m3"] / 1000
    assert pr.density({e: 1.0}) == pytest.approx(listed, rel=0.02)


def test_density_against_measured_alloys():
    df = pd.read_csv(st.RAW)
    df.columns = [c.split(": ")[1] if ": " in c else c for c in df.columns]
    df["comp"] = df["FORMULA"].map(st.parse_formula)
    m = df["comp"].map(lambda c: set(c) <= set(pr.STRENGTH_ELEMENTS)) & df["Exp. Density (g/cm$^3$)"].notna()
    d = df[m].drop_duplicates("FORMULA")
    err = (d["comp"].map(pr.density) - d["Exp. Density (g/cm$^3$)"]) / d["Exp. Density (g/cm$^3$)"]
    assert len(d) >= 25 and np.sqrt(np.mean(err**2)) < 0.02


def test_pure_element_has_no_solid_solution_strength():
    assert pr.strength({"W": 1.0}, 300)["sigma_y_MPa"] == pytest.approx(0.0, abs=1e-9)


def test_strength_decreases_with_temperature():
    c = {"Nb": 1, "Mo": 1, "Ta": 1, "W": 1}
    s = [pr.strength(c, T)["sigma_y_MPa"] for T in (300, 800, 1300, 1800)]
    assert all(a > b for a, b in zip(s, s[1:]))


def test_mo_shear_modulus_uses_consistent_value():
    assert pr.elements()["Mo"]["shear_modulus_GPa_used"] == pytest.approx(125.57, abs=0.1)


def test_strength_model_rejects_si():
    with pytest.raises(ValueError):
        pr.strength({"Nb": 0.9, "Si": 0.1}, 300)


# ---------------------------------------------------------------- search problem
@pytest.fixture(scope="module")
def cfg():
    import yaml
    from pathlib import Path
    return yaml.safe_load((Path(__file__).parents[1] / "problem.yaml").read_text())


def test_normalise_drops_minor_components():
    from problems.M3_rhea_oxidation import evaluator as ev
    x = ev.normalise([0.5, 0.02, 0.48] + [0] * 7, 0.05)
    assert x[1] == 0 and x.sum() == pytest.approx(1)


def test_evaluator_on_known_alloy_is_in_trust_region(cfg):
    from problems.M3_rhea_oxidation import evaluator as ev
    # Cr Mo Nb Ti equimolar: tested for strength (MPEA) and close to oxidation-tested AlCrMoNbTi alloys
    design = [0, 0.25, 0, 0.25, 0.25, 0, 0.25, 0, 0, 0]
    r = ev.evaluate(design, cfg)
    assert r.constraints["trust_strength"] <= 0
    assert r.metadata["density"] == pytest.approx(pr.density({"Cr": 1, "Mo": 1, "Nb": 1, "Ti": 1}))
    assert r.objective == pytest.approx(-r.metadata["sigma_MPa"] / r.metadata["density"])


def test_distance_to_oxidation_data_is_zero_for_tested_alloy():
    from problems.M3_rhea_oxidation import evaluator as ev
    U = ev.oxidation_alloys()
    assert ev.distance_to_oxidation_data(U[:5]).max() == pytest.approx(0, abs=1e-9)


def test_far_composition_violates_trust(cfg):
    from problems.M3_rhea_oxidation import evaluator as ev
    r = ev.evaluate([0, 0, 0.5, 0, 0, 0, 0, 0.5, 0, 0], cfg)  # Hf-V: not near any tested alloy
    assert not r.feasible
