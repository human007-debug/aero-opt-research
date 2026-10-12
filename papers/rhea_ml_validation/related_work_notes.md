# Related work: sources, checks and open items (2026-10-12)

## How the references were checked

1. Four literature searches (oxidation, validation methods, uncertainty and design, strength and data quality)
   proposed candidates with summaries. Their notes are in `litsearch/`. They are model-written; where they
   conflict with this file, this file wins.
2. `verify_refs.py` checks every `refs.bib` entry against Crossref (DOI) or the arXiv API: title, year, first
   author, volume, first page. Result on 2026-10-12: 68/68 pass. Exceptions:
   - `rasmussen2006gaussian`: Crossref date 2005, cited as 2006 (print edition).
   - `rohatgi2018webplotdigitizer`: Zenodo DOI, checked by hand on DataCite.
   - PMLR/NeurIPS entries are matched by title on arXiv; their page numbers come from the proceedings
     pages (TuRBO pages from the arXiv journal-ref).
3. Statements in `related_work.tex` that carry numbers or strong wording were re-checked against the source
   itself, not only against the search notes:

| Statement | Checked against |
|---|---|
| Lin et al.: two curators, factor-of-ten errors flagged, unconfirmed points removed, 886 records, 62 publications, WebPlotDigitizer | full text (Europe PMC PMC13452336) |
| RefOxDB: 407 curves, 68 sources, units "are varied", 71% kinetic-law mismatch, WebPlotDigitizer | arXiv:2310.15083 full text |
| Bejjipurapu (descriptors): 77 compositions, random 80/20 split, repeated stratified 5-fold CV, test MAE 5.78, CV MAE 12.04 / 11.08 | arXiv:2511.01095 full text |
| Bejjipurapu (active learning): misses 3.3→69.5, 2.3→121.2, 1.2→70.3; five-component 0.93/0.79 → 4.76/5.87 | arXiv:2512.15958v1 SI Table 2 and Sec. on 5-component alloys |
| Gorsse et al.: nested k-fold CV with shuffling over records; 5 unseen alloys (25 records) "slightly higher" error; 3 designed alloys | full text (HAL hal-04746750): "Each of the 861 data point[s] represents a unique combination of alloy composition, temperature, and [time]"; 5 test alloys, 25 observations |
| Lee 2021 (NbTaTiV, CrMoNbV edge control); Baruffi 2022 (edge theory only for non-dilute, large misfit) | Crossref / Semantic Scholar abstracts |
| Senkov 2019 (0.6 Tm; multi-phase above 1000 °C); Huang 2019 (68.6/64.3/74.3%); Ren 2018; Hirschfeld 2020; Palmer 2022; Kapoor 2023 (294 papers, 17 fields); Li 2023 (up to 95% redundant); Li 2025; Omee 2024; Sheridan 2013; Burda 2017 (0.23–30.35%); Smith & Winkler 2006 | abstracts (Crossref, Semantic Scholar, OpenAlex) |

**Correction to the search notes:** the descriptor paper has one record per composition, so its random split
already tests unseen alloys. It is not a record-level leakage case. Only the Gorsse et al. protocol splits
records of the same alloy across folds.

**Summaries taken from the search notes without a second check** (abstracts not retrievable here): Vela 2023
(constraints; no oxidation), Khatamsaz 2022, Vela 2023 data-augmented model, Giles 2026, Pei 2020, Drevon 2017,
Moeyaert 2016, Court & Cole 2018, Polak & Morgan 2024, Afflerbach 2022, Zech 2018 numbers (not quoted), Peng 2021
("highly consistent and well-curated" confirmed from abstract). Re-read before submission.

## Open items (need you or library access)

1. **Possible competitor:** Ajimshad & Sekhar, J. Phase Equilib. Diffus. (2026), doi:10.1007/s11669-026-01273-z,
   ML plus edge theory for NbMoTiVZr. Online 2026-09-28; abstract not available here. Read it.
2. **Loli et al., Oxid. Met. 98 (2022) 429** (earliest ML oxidation model across multi-principal-element alloys)
   and **Dewangan et al. 2022 / 2025**: metadata verified, abstracts not readable here. Read the full texts and
   note their validation protocol; probably cite Loli in "Data-driven oxidation models".
3. **WebPlotDigitizer version:** the cited record is v4.1; neither dataset paper states the version.
4. **Bejjipurapu et al. active learning** is a preprint (arXiv:2512.15958; SSRN 10.2139/ssrn.6829501). Check for
   the journal version before submission.
5. **Gorsse et al. "slightly higher" error on unseen alloys:** quote their number from the paper if you want it
   in the text.
6. Related-work length is about 1800 words. Journals such as IMMI or Comput. Mater. Sci. usually accept this;
   trim the "Validation beyond random splits" subsection first if needed.
