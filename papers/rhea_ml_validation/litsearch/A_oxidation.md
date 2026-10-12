# Related work A: oxidation of RHEAs/RCCAs and ML/data for oxidation

Paper: "How far can data-driven models be trusted for designing oxidation-resistant refractory alloys? Distance-dependent accuracy, cross-dataset transfer and data quality"

Claims: C1 entry errors / two digitisations agree except a x100 unit conflict; C2 error grows 3-4x with distance to nearest training alloy; C3 row-level CV optimistic vs grouped CV; C4 internal rankings don't transfer to an independent dataset; C5 strength and oxidation datasets barely overlap; C6 optimiser's curse on surrogate Pareto fronts.

## How the references were checked (12 Oct 2026)
- Every BibTeX entry below was checked against Crossref `api.crossref.org/works/<DOI>` (authors, title, journal, volume, issue, pages/article number, year) or the arXiv API (preprints).
- Summaries come from abstracts read from Crossref, Semantic Scholar, OpenAIRE, Europe PMC, DOAJ or the HAL API. **Full texts were read** for gorsse2025ml (author-hosted CC-BY PDF), lin2026dataset (PMC full text), mishra2024refoxdb, bejjipurapu2026descriptors and bejjipurapu2025active (arXiv PDFs). Those entries also carry details taken from the full text, marked [full text].
- In Section E, the metadata is verified but no abstract could be read (Elsevier and Springer pages were blocked). Those summaries are marked **summary not verified**.
- Section F lists **UNVERIFIED** candidates. Do not cite them as they stand.

---

## A. Reviews of RHEA/RCCA (and HEA) oxidation

### gorr2021review
```bibtex
@article{gorr2021review,
  author  = {Gorr, Bronislava and Schellert, Steven and M{\"u}ller, Franz and Christ, Hans-J{\"u}rgen and Kauffmann, Alexander and Heilmaier, Martin},
  title   = {Current Status of Research on the Oxidation Behavior of Refractory High Entropy Alloys},
  journal = {Advanced Engineering Materials},
  volume  = {23},
  number  = {5},
  pages   = {2001047},
  year    = {2021},
  doi     = {10.1002/adem.202001047}
}
```
Summary: Reviews the RHEA oxidation literature in terms of alloy composition, mass changes, corrosion products and scale constitution. Many RHEAs suffer pest oxidation, large weight changes, spallation or complete oxidation, like the pure refractory metals. A few are protective because they form α-Al2O3 or complex oxides such as CrTaO4.
Relevance: This is the standard mechanistic review. It sets out why mass change is such a heterogeneous, noisy target (volatile MoO3/CrO3, spallation, pesting), which supports C1 and the data-quality framing. It contains no ML.

### senkov2018review
```bibtex
@article{senkov2018review,
  author  = {Senkov, Oleg N. and Miracle, Daniel B. and Chaput, Kevin J. and Couzinie, Jean-Philippe},
  title   = {Development and exploration of refractory high entropy alloys---A review},
  journal = {Journal of Materials Research},
  volume  = {33},
  number  = {19},
  pages   = {3092--3128},
  year    = {2018},
  doi     = {10.1557/jmr.2018.153}
}
```
Summary: Reviews publications on RHEAs/RCCAs from 2010 to January 2018, covering 151 reported alloys. It treats composition, processing, microstructure, phases, mechanical properties, oxidation, corrosion and tribology.
Relevance: This is the canonical RHEA review, and its alloy set underlies the strength compilations. It treats oxidation only as one section, which supports C5 (strength and oxidation have been studied on largely different alloys).

### kumar2022review
```bibtex
@article{kumar2022review,
  author  = {Kumar, Poresh and Lam, Tu-Ngoc and Tripathi, Pawan Kumar and Singh, Sudhanshu Shekhar and Liaw, Peter K. and Huang, E-Wen},
  title   = {Recent progress in oxidation behavior of high-entropy alloys: A review},
  journal = {APL Materials},
  volume  = {10},
  number  = {12},
  pages   = {120701},
  year    = {2022},
  doi     = {10.1063/5.0116605}
}
```
Summary: A Research Update summarising recent findings on the oxidation behaviour of HEAs and high-entropy materials, including coatings. It highlights open challenges and controversies.
Relevance: General HEA oxidation background, cited by gorsse2025ml. It contains no ML or validation content.

### anne2021review
```bibtex
@article{anne2021review,
  author  = {Anne, Bhargavi Rani and Shaik, Shajahan and Tanaka, Masaki and Basu, Anindya},
  title   = {A crucial review on recent updates of oxidation behavior in high entropy alloys},
  journal = {SN Applied Sciences},
  volume  = {3},
  number  = {3},
  pages   = {366},
  year    = {2021},
  doi     = {10.1007/s42452-021-04374-1}
}
```
Summary: Reviews HEA oxidation from the standpoint of crystal structure (BCC versus FCC HEAs) and compares selected case studies with conventional alloys.
Relevance: General background, cited by gorsse2025ml. Optional.

### veselkov2021review
```bibtex
@article{veselkov2021review,
  author  = {Veselkov, Sergey and Samoilova, Olga and Shaburova, Nataliya and Trofimov, Evgeny},
  title   = {High-Temperature Oxidation of High-Entropic Alloys: A Review},
  journal = {Materials},
  volume  = {14},
  number  = {10},
  pages   = {2595},
  year    = {2021},
  doi     = {10.3390/ma14102595}
}
```
Summary: Reviews high-temperature oxidation mechanisms of Al-Co-Cr-Fe-Ni, Mn-Co-Cr-Fe-Ni and refractory HEAs, and proposes directions for heat-resistant HEAs.
Relevance: Background. Optional.

---

## B. Key experimental papers on oxidation-resistant RCCA families

### muller2019mechanism
```bibtex
@article{muller2019mechanism,
  author  = {M{\"u}ller, Franz and Gorr, Bronislava and Christ, Hans-J{\"u}rgen and M{\"u}ller, Julian and Butz, Benjamin and Chen, Hans and Kauffmann, Alexander and Heilmaier, Martin},
  title   = {On the oxidation mechanism of refractory high entropy alloys},
  journal = {Corrosion Science},
  volume  = {159},
  pages   = {108161},
  year    = {2019},
  doi     = {10.1016/j.corsci.2019.108161}
}
```
Summary: Studied TaMoCrTiAl, NbMoCrTiAl, NbMoCrAl and TaMoCrAl at 1000 °C in air. In TaMoCrTiAl, a protective Al2O3/Cr2O3/CrTaO4 scale formed and CrTaO4 changed the kinetics from a parabolic to a quartic rate law; Ti promoted CrTaO4. In the Nb-containing alloys, Nb2O5 polytypes gave porous scales and severe spallation.
Relevance: Shows that swapping one element (Ta for Nb) flips the alloy from protective to non-protective. Such sharp, non-smooth composition-property cliffs explain why error grows away from the training data (C2).

### gorr2020crtao4
```bibtex
@article{gorr2020crtao4,
  author  = {Gorr, Bronislava and M{\"u}ller, Franz and Schellert, Steven and Christ, Hans-J{\"u}rgen and Chen, Hans and Kauffmann, Alexander and Heilmaier, Martin},
  title   = {A new strategy to intrinsically protect refractory metal based alloys at ultra high temperatures},
  journal = {Corrosion Science},
  volume  = {166},
  pages   = {108475},
  year    = {2020},
  doi     = {10.1016/j.corsci.2020.108475}
}
```
Summary: Proposes alloying with Cr and Ta so that CrTaO4 forms. On equiatomic Ta-Mo-Cr-Ti-Al, CrTaO4 forms easily between 500 and 1500 °C, adheres after cooling, grows slowly, and has a wide stoichiometry range that suppresses non-protective oxides.
Relevance: Defines the Al-Cr-Mo-Ta-Ti family, which is the main protective cluster in the public datasets and the region where gorsse2025ml did its final validation.

### lo2019crtao4
```bibtex
@article{lo2019crtao4,
  author  = {Lo, Kai-Chi and Chang, Yao-Jen and Murakami, Hideyuki and Yeh, Jien-Wei and Yeh, An-Chou},
  title   = {An oxidation resistant refractory high entropy alloy protected by {CrTaO4}-based oxide},
  journal = {Scientific Reports},
  volume  = {9},
  number  = {1},
  pages   = {7266},
  year    = {2019},
  doi     = {10.1038/s41598-019-43819-x}
}
```
Summary: TGA isothermal oxidation of a new RHEA at 1000 and 1100 °C for up to 200 h, which the authors call an unprecedented duration (most prior RHEA tests were 48 h or shorter). At 1000 °C no dense CrTaO4 layer formed and the weight gain grew exponentially. At 1100 °C the kinetics were two-stage parabolic and the mass gain was 4.03 mg/cm² after 200 h.
Relevance: Shows that the exposure time strongly changes the kinetic regime, and that most literature data are short exposures. This is a caveat for models that use time as a feature, and for comparing records across sources (C1 and C4).

### schellert2021al
```bibtex
@article{schellert2021al,
  author  = {Schellert, S. and Gorr, B. and Christ, H.-J. and Pritzel, C. and Laube, S. and Kauffmann, A. and Heilmaier, M.},
  title   = {The Effect of {Al} on the Formation of a {CrTaO4} Layer in Refractory High Entropy Alloys {Ta-Mo-Cr-Ti-xAl}},
  journal = {Oxidation of Metals},
  volume  = {96},
  number  = {3-4},
  pages   = {333--345},
  year    = {2021},
  doi     = {10.1007/s11085-021-10046-7}
}
```
Summary: Ta-Mo-Cr-Ti-xAl (x = 5, 10, 15, 20 at.%) was oxidised for 24 h at 1200 °C. At 5 % Al the kinetics were dominated by volatile MoO3/CrO3. At 15–20 % Al a dense CrTaO4 layer formed, whereas 5–10 % Al gave thick, porous Ta2O5 scales.
Relevance: Volatilisation produces net mass loss or ambiguous mass change. This is a physical reason why sign and unit conventions for Δm/A get mixed up in compilations (C1).

### sheikh2018pesting
```bibtex
@article{sheikh2018pesting,
  author  = {Sheikh, Saad and Bijaksana, Muhammad Kurnia and Motallebzadeh, Amir and Shafeie, Samrand and Lozinko, Adrianna and Gan, Lu and Tsao, Te-Kang and Klement, Uta and Canadinc, Demircan and Murakami, Hideyuki and Guo, Sheng},
  title   = {Accelerated oxidation in ductile refractory high-entropy alloys},
  journal = {Intermetallics},
  volume  = {97},
  pages   = {58--66},
  year    = {2018},
  doi     = {10.1016/j.intermet.2018.04.001}
}
```
Summary: The ductile Hf0.5Nb0.5Ta0.5Ti1.5Zr RHEA pests (disintegrates to powder) between 600 and 1000 °C, because no protective scale forms and internal oxidation is accelerated. Removing Zr and Hf eliminates the pesting. The authors argue that the currently known ductile Hf-Nb-Ta-Ti-Zr-type RHEAs are susceptible in general.
Relevance: Direct evidence that the mechanically attractive and the oxidation-resistant regions of RHEA composition space are largely disjoint. Supports C5 and motivates why joint strength–oxidation Pareto fronts force extrapolation (C6).

### butler2022crnb
```bibtex
@article{butler2022crnb,
  author  = {Butler, T.M. and Senkov, O.N. and Daboiku, T.I. and Velez, M.A. and Schroader, H.E. and Ware, L.G. and Titus, M.S.},
  title   = {Oxidation behaviors of {CrNb}, {CrNbTi}, and {CrNbTaTi} concentrated refractory alloys},
  journal = {Intermetallics},
  volume  = {140},
  pages   = {107374},
  year    = {2022},
  doi     = {10.1016/j.intermet.2021.107374}
}
```
Summary: Oxidation at 1200 °C. CrNb and CrNbTi showed nearly parabolic kinetics, while CrNbTaTi was worse and showed mixed-mode behaviour. All three formed multi-phase simple and complex oxides, and the results were compared with ab initio (DFT) predictions.
Relevance: Source of the oxide-layer thermodynamic model that bejjipurapu2026descriptors used for descriptors. Optional.

---

## C. ML / data-driven oxidation of RHEAs/RCCAs (core prior work)

### gorsse2025ml
```bibtex
@article{gorsse2025ml,
  author  = {Gorsse, St{\'e}phane and Lin, Wei-Chih and Murakami, Hideyuki and Rignanese, Gian-Marco and Yeh, An-Chou},
  title   = {Advancing refractory high entropy alloy development with {AI}-predictive models for high temperature oxidation resistance},
  journal = {Scripta Materialia},
  volume  = {255},
  pages   = {116394},
  year    = {2025},
  doi     = {10.1016/j.scriptamat.2024.116394}
}
```
Summary (abstract): A GBDT (XGBoost) model predicts specific mass gain from a literature dataset. It was trained with Iterated Nested k-fold CV with Shuffling (INKCVS) and validated experimentally on selected alloys.
Details [full text]:
- Data: 886 observations and 163 unique alloys, from 11 elements (Al, Cr, Hf, Mo, Nb, Si, Ta, Ti, V, W, Zr). The 13 features are the 11 compositions plus temperature (600–1400 °C) and time (3–100 h). The target is ln(Δm*).
- Validation: the outer CV has 4 folds and the inner 5, repeated 25 times with shuffling, giving 100 models. The CV parity plot uses 861 rows. The paper describes rows as unique (composition, T, t) combinations. There is no grouping by alloy or source.
- Unseen test: 9 "random" alloys were arc-melted from a sparsely sampled central region of composition space. 4 went into training and 5 (25 observations) were held out. The paper says the unseen-test MAE is "slightly higher" than the INKCVS MAE.
- Final check: 3 Al-Cr-Mo-Ta-Ti alloys aimed at target mass gains of 1, 3 and 7 mg/cm² (20 h at 1000 °C) fell close to the 1:1 line.
- SHAP ranking: temperature > Nb > time > Al.
- The authors plan to combine this model with strength and ductility models into a 3-D Pareto front.

Relevance:
- C3: rows of the same alloy at different (T, t) can sit in both training and test folds, so INKCVS is row-level CV. It is exactly the optimistic protocol we quantify.
- C2: the test that comes closest to an out-of-distribution check is only 5 alloys.
- C4: the work uses one dataset and has no cross-dataset test.
- C5/C6: the planned strength–oxidation Pareto front is the use case where our C5 and C6 apply.

### lin2026dataset
```bibtex
@article{lin2026dataset,
  author  = {Lin, Wei-Chih and Gorsse, St{\'e}phane and Yeh, An-Chou},
  title   = {Dataset of oxidation properties of refractory alloys},
  journal = {Data in Brief},
  volume  = {68},
  pages   = {113105},
  year    = {2026},
  doi     = {10.1016/j.dib.2026.113105}
}
```
Summary (abstract): A curated dataset of isothermal air-oxidation experiments on refractory alloys and RHEAs. It draws on 62 publications from 1956–2023 plus in-house data, and gives composition (at.%), T (°C), t (h), specific mass change (mg/cm²) and source. The data are on Zenodo (doi:10.5281/zenodo.21412476).
Details [full text]:
- Files: alloy_oxidation_886_202406.csv, i.e. the 886-row gorsse2025ml dataset.
- Coverage: Δm ranges from 0.02 to 345 mg/cm². Coverage of composition space is very uneven, and points are especially sparse and isolated between 1000 and 1200 °C (UMAP figures).
- Extraction: figure-only data were digitised with WebPlotDigitizer at fixed times (3, 4, 10, 20, 50, 100 h), without error bars.
- Curation: two curators extracted the data independently and conflicts were traced back to the sources. "Apparent order-of-magnitude inconsistencies, such as suspected factor-of-ten errors arising from unit conversion or transcription mistakes, were flagged and checked." Duplicate alloy–T–t rows from different sources were kept on purpose.
- Stated limitations: volatilisation (Mo, V, Ta, W) means low or negative Δm need not mean good resistance.

Relevance:
- C1: this is one of the two independent public digitisations. The curators acknowledge factor-of-ten unit and transcription errors, but no cross-dataset audit has been done; our x100 conflict finding extends this.
- C3: the deliberate duplicate rows and the Alloy_ID/Source_Alloy_ID fields make alloy- and source-grouped CV both possible and necessary.
- C4: this is the natural "independent dataset" to set against RefOxDB.

### mishra2024refoxdb
```bibtex
@article{mishra2024refoxdb,
  author  = {Mishra, Saswat and Karumuri, Sharmila and Mika, Vincent and Scott, Collin and Choy, Chadwick and Sandhage, Kenneth H. and Bilionis, Ilias and Titus, Michael S. and Strachan, Alejandro},
  title   = {Mass uptake during oxidation of metallic alloys: Literature data collection, analysis, and {FAIR} sharing},
  journal = {Computational Materials Science},
  volume  = {233},
  pages   = {112671},
  year    = {2024},
  doi     = {10.1016/j.commatsci.2023.112671},
  note    = {arXiv:2310.15083}
}
```
Summary (abstract): Mass-change-versus-time curves for 407 alloys were digitised from the literature. The curves are fitted to several kinetic models with Bayesian model selection (BIC) and shared through the nanoHUB tool RefOxDB. The model chosen by the original authors disagreed with the BIC-best model in 71 % of cases, and was not even in the BIC top 3 in 56 % (at an assumed noise of 2.5 % of the mass-gain range).
Details [full text]:
- Contents: 330 continuous and 77 interrupted experiments, covering 145 unique elements/alloys from 68 sources, digitised with WebPlotDigitizer.
- Data-quality remark: "units for surface area-normalized mass gain and oxidation rate coefficients are varied, and raw data is rarely available."

Relevance:
- C1: this is the second independent digitisation, and the paper itself warns about unit heterogeneity. Published kinetic interpretations are also often inconsistent with the data.
- RefOxDB is the training source for bejjipurapu2026descriptors and bejjipurapu2025active.

### bejjipurapu2026descriptors
```bibtex
@article{bejjipurapu2026descriptors,
  author  = {Bejjipurapu, Akhil and Strachan, Alejandro and Sandhage, Kenneth H. and Titus, Michael S.},
  title   = {Machine learning descriptors for predicting the high temperature oxidation of refractory complex concentrated alloys},
  journal = {Materials Advances},
  volume  = {7},
  number  = {16},
  pages   = {8364--8377},
  year    = {2026},
  doi     = {10.1039/d6ma00714g},
  note    = {arXiv:2511.01095}
}
```
Summary (abstract): A GPR model with physics-informed oxidation-product descriptors predicts the 24 h specific mass change at 1000 °C. It was trained on 77 compositions oxidised at 900–1000 °C, from RefOxDB. The test MAE is 5.78 mg/cm² with oxide descriptors, against 7.18 mg/cm² with alloy descriptors only (the latter figure is in the full text). The model screened more than 5,100 quaternary RCCAs.
Details [full text]:
- Validation: a random 80/20 split, plus repeated stratified 5-fold CV (3 repeats). The CV MAE was 12.04 without and 11.08 mg/cm² with oxide descriptors, so the CV MAE is about twice the reported test MAE.
- The SI says predictions "remain concentrated in the low mass-gain regime, indicating similar challenges in extrapolation."

Relevance:
- C3: the work uses only row-level random splits with no grouping. The 2x gap between CV and test MAE shows the split variance at n = 77.
- C2: the authors acknowledge an extrapolation problem.
- C4: there is no independent-dataset test.

### bejjipurapu2025active
```bibtex
@misc{bejjipurapu2025active,
  author        = {Bejjipurapu, Akhil and Karumuri, Sharmila and Flanagan, Joseph C. and Tucker, Victoria and Bilionis, Ilias and Strachan, Alejandro and Sandhage, Kenneth H. and Titus, Michael S.},
  title         = {Active Learning Discovery of High Temperature Oxidation Resistant Refractory Complex Concentrated Alloys},
  year          = {2025},
  eprint        = {2512.15958},
  archivePrefix = {arXiv},
  primaryClass  = {cond-mat.mtrl-sci},
  note          = {Also posted as SSRN preprint doi:10.2139/ssrn.6829501 (2026)}
}
```
Summary (abstract): GPR combined with batch Bayesian optimisation (expected improvement, 5 alloys per batch) started from 81 literature RCCAs and ran six iterations. It found Al30Mo5Ti15Cr50 and Al40Mo5Ti30Cr25, both under 1 mg/cm² after 24 h at 1000 °C, with α-Al2O3 scales and parabolic kinetics, and with high specific hardness and CTE compatibility with TBCs.
Details [full text, arXiv v1 SI Table 2]: the first batches show large prediction misses (predicted → measured, mg/cm²):
- Al5Nb65Zr5Ti25: 3.3 → 69.5
- Al15V35Ti20Cr30 (batch 3): 2.3 → 121.2
- Al15Mo35Ti35Cr15 (batch 4): 1.2 → 70.3
- The two best 5-component extrapolations were predicted at 0.93 and 0.79 but measured 4.76 and 5.87.

Relevance:
- C6 and C2: this is the most direct published evidence of the optimiser's curse. Candidates chosen for low predicted mass gain often measured 10–50x worse, especially away from the training data (5-component extrapolation).
- It is still a preprint, so cite the arXiv version.

### sauceda2022landscape
```bibtex
@article{sauceda2022landscape,
  author  = {Sauceda, D. and Singh, P. and Ouyang, G. and Palasyuk, O. and Kramer, M. J. and Arr{\'o}yave, R.},
  title   = {High throughput exploration of the oxidation landscape in high entropy alloys},
  journal = {Materials Horizons},
  volume  = {9},
  number  = {10},
  pages   = {2644--2663},
  year    = {2022},
  doi     = {10.1039/d2mh00729k}
}
```
Summary (Crossref graphical abstract, one sentence): A high-throughput finite-temperature phase-prediction framework that characterises the oxidation resistance of HEAs for arbitrary temperature and oxygen concentration. Further details are not verified.
Relevance: A thermodynamics-based, not data-driven, screening alternative. gorsse2025ml contrasts its compositional scope (under 10,000 alloys) with its own. Optional.

---

## D. ML oxidation of other alloy classes (verified abstracts)

### taylor2021ml
```bibtex
@article{taylor2021ml,
  author  = {Taylor, Christopher D. and Tossey, Brett M.},
  title   = {High temperature oxidation of corrosion resistant alloys from machine learning},
  journal = {npj Materials Degradation},
  volume  = {5},
  number  = {1},
  pages   = {38},
  year    = {2021},
  doi     = {10.1038/s41529-021-00184-3}
}
```
Summary: Parabolic rate constants kp were tabulated for 75 alloys (steels, Ni superalloys, aluminides) at about 800–2000 K in air, CO2, supercritical water and steam. Supervised ML gave the lowest errors. Ni, Cr, Al and Fe (then Mo and Co) were the most significant elements.
Relevance: An early literature-compiled oxidation-kinetics ML study across alloy classes. Its validation protocol is not described in the abstract.

### peng2021nicr
```bibtex
@article{peng2021nicr,
  author  = {Peng, Jian and Pillai, Rishi and Romedenne, Marie and Pint, Bruce A. and Muralidharan, Govindarajan and Allen Haynes, J. and Shin, Dongwon},
  title   = {Data analytics approach to predict high-temperature cyclic oxidation kinetics of {NiCr}-based Alloys},
  journal = {npj Materials Degradation},
  volume  = {5},
  number  = {1},
  pages   = {41},
  year    = {2021},
  doi     = {10.1038/s41529-021-00188-z}
}
```
Summary: ML models predict experimental kp of NiCr-based alloys from composition and temperature. They were trained on a "highly consistent and well-curated" single-laboratory dataset using correlation-ranked features.
Relevance: Contrast for C1 and C4. A consistent single-source dataset is presented as what made the ML work, whereas RHEA datasets are multi-source literature compilations.

### bhattacharya2020ti
```bibtex
@article{bhattacharya2020ti,
  author  = {Bhattacharya, Somesh Kr. and Sahara, Ryoji and Narushima, Takayuki},
  title   = {Predicting the Parabolic Rate Constants of High-Temperature Oxidation of {Ti} Alloys Using Machine Learning},
  journal = {Oxidation of Metals},
  volume  = {94},
  number  = {3-4},
  pages   = {205--218},
  year    = {2020},
  doi     = {10.1007/s11085-020-09986-3}
}
```
Summary: A literature dataset for Ti alloys, with composition, phase, temperature, time, atmosphere and test mode as features, was used to predict kp. Gradient boosting reached R² = 0.92.
Relevance: Another literature-compiled oxidation ML study that reports a single aggregate R². The abstract does not describe the validation grouping.

### kim2021ni
```bibtex
@article{kim2021ni,
  author  = {Kim, Hee-Soo and Park, Si-Jun and Seo, Seong-Moon and Yoo, Young-Soo and Jeong, Hi-Won and Jang, HeeJin},
  title   = {Regression analysis of high-temperature oxidation of {Ni}-based superalloys using artificial neural network},
  journal = {Corrosion Science},
  volume  = {180},
  pages   = {109207},
  year    = {2021},
  doi     = {10.1016/j.corsci.2020.109207}
}
```
Summary: An ANN maps the composition of Ni-(0–15)Co-(8–15)Cr-(0–5)Mo-(0–10)W-(3–8)Al-(0–5)Ti-(0–10)Ta-0.1C-0.01B alloys to cyclic-oxidation weight change, with "highly accurate" regression. It was compared with response-surface methodology and used to find an optimum composition.
Relevance: An in-house, single-protocol dataset inside a bounded composition box, so it is interpolative by design (C2 contrast).

### tan2025nicocralfe
```bibtex
@article{tan2025nicocralfe,
  author  = {Tan, Xingru and Trehern, William and Sundar, Aditya and Wang, Yi and San, Saro and Lu, Tianwei and Zhou, Fan and Sun, Ting and Zhang, Youyuan and Wen, Yuying and Liu, Zhichao and Gao, Michael and Hu, Shanshan},
  title   = {Machine learning and high-throughput computational guided development of high temperature oxidation-resisting {Ni-Co-Cr-Al-Fe} based high-entropy alloys},
  journal = {npj Computational Materials},
  volume  = {11},
  number  = {1},
  pages   = {93},
  year    = {2025},
  doi     = {10.1038/s41524-025-01568-8}
}
```
Summary: Combines ML with a thermodynamics-informed, ranking-based selection to explore non-equiatomic Ni-Co-Cr-Al-Fe HEAs. Several candidates that outperform the MCrAlY bond coat were identified and confirmed experimentally.
Relevance: An HEA (non-refractory) ML oxidation design study with experimental confirmation. It shows the field's focus on discovery rather than on calibrating error out of distribution.

### boakye2025nicocral
```bibtex
@misc{boakye2025nicocral,
  author        = {Boakye, Dennis and Deng, Chuang},
  title         = {Machine-learned accelerated discovery of oxidation-resistant {NiCoCrAl} high-entropy alloys},
  year          = {2025},
  eprint        = {2512.15517},
  archivePrefix = {arXiv},
  primaryClass  = {cond-mat.mtrl-sci}
}
```
Summary: A data-driven analysis of experimental oxidation data for NiCoCrAl HEAs. It finds a temperature-dependent switch: Al-rich alloys are best at 1150 °C and above, mixed Al-Cr in between, and Cr-rich low-Al alloys at 850 °C. It also finds composition-dependent effects of Hf and Y.
Relevance: Peripheral (non-refractory HEA preprint). Optional.

---

## E. Metadata verified (Crossref), abstract NOT read: "summary not verified"

### loli2022mpea
```bibtex
@article{loli2022mpea,
  author  = {Loli, Jose A. and Chovatiya, Amish R. and He, Yining and Ulissi, Zachary W. and de Boer, Maarten P. and Webler, Bryan A.},
  title   = {Predicting Oxidation Behavior of Multi-Principal Element Alloys by Machine Learning Methods},
  journal = {Oxidation of Metals},
  volume  = {98},
  number  = {5-6},
  pages   = {429--450},
  year    = {2022},
  doi     = {10.1007/s11085-022-10129-z}
}
```
Summary not verified. Secondary description from bejjipurapu2026descriptors: an automated ML pipeline (TPOT) predicting mass change at 1000 °C across MPEAs. Semantic Scholar TLDR: "ML-based methods can be useful for predicting composition-dependent oxidation behavior."
Relevance: The earliest MPEA-wide oxidation ML. **Read the full text before citing** to check its CV protocol (C3).

### dewangan2022ann
```bibtex
@article{dewangan2022ann,
  author  = {Dewangan, Sheetal Kumar and Kumar, Vinod},
  title   = {Application of artificial neural network for prediction of high temperature oxidation behavior of {AlCrFeMnNiW}$_x$ ($x$ = 0, 0.05, 0.1, 0.5) high entropy alloys},
  journal = {International Journal of Refractory Metals and Hard Materials},
  volume  = {103},
  pages   = {105777},
  year    = {2022},
  doi     = {10.1016/j.ijrmhm.2022.105777}
}
```
Summary not verified. Secondary description from bejjipurapu2026descriptors: an ANN on composition, time and temperature, with Pearson r > 0.999 between predicted and measured mass gains.
Relevance: An example of near-perfect in-distribution fit on time-series rows from four alloys. This is a row-level evaluation (C3), to be confirmed from the full text.

### dewangan2025w
```bibtex
@article{dewangan2025w,
  author  = {Dewangan, Sheetal Kumar and Baghel, Vivek Singh and Lee, Hansung and Nagarjuna, Cheenepalli and Youn, Gyosik and Kumar, Vinod and Ahn, Byungmin},
  title   = {Decoding weight-gain patterns in tungsten-containing refractory high-entropy alloys under high-temperature oxidation through machine learning},
  journal = {Journal of Materials Research and Technology},
  volume  = {39},
  pages   = {5251--5261},
  year    = {2025},
  doi     = {10.1016/j.jmrt.2025.10.189}
}
```
Summary not verified. A web-search snippet, not the abstract, said random forest performed best (r ≈ 0.999) on in-house W-containing RHEA oxidation data.
Relevance: A probable further example of row-level fits on a few alloys. Check before citing.

### li2024ni
```bibtex
@article{li2024ni,
  author  = {Li, Changheng and Xu, Kai and Lou, Ming and Wang, Linjing and Chang, Keke},
  title   = {Machine learning-enabled prediction of high-temperature oxidation resistance for {Ni}-based alloys},
  journal = {Corrosion Science},
  volume  = {234},
  pages   = {112152},
  year    = {2024},
  doi     = {10.1016/j.corsci.2024.112152}
}
```
Summary not verified (Ni alloys, ln kp target according to a secondary news digest).

### duan2023ni
```bibtex
@article{duan2023ni,
  author  = {Duan, Xingjun and Xu, Hui and Wang, Enhui and Guo, Chunyu and Fang, Zhi and Yang, Tao and Zhao, Yunsong and Hou, Xinmei},
  title   = {Design of novel {Ni}-based superalloys with better oxidation resistance with the aid of machine learning},
  journal = {Journal of Materials Science},
  volume  = {58},
  number  = {27},
  pages   = {11100--11114},
  year    = {2023},
  doi     = {10.1007/s10853-023-08712-z}
}
```
Summary not verified. Semantic Scholar TLDR: Ti, Cr and Al are the most important elements, and the screened alloys beat commercial alloys.

### lo2022elemental
```bibtex
@article{lo2022elemental,
  author  = {Lo, Kai-Chi and Murakami, Hideyuki and Glatzel, Uwe and Yeh, Jien-Wei and Gorsse, St{\'e}phane and Yeh, An-Chou},
  title   = {Elemental effects on the oxidation of refractory compositionally complex alloys},
  journal = {International Journal of Refractory Metals and Hard Materials},
  volume  = {108},
  pages   = {105918},
  year    = {2022},
  doi     = {10.1016/j.ijrmhm.2022.105918}
}
```
Summary not verified. Cited by gorsse2025ml for the harmful effects of Zr and V and the beneficial rutile-type complex oxides that form with low Ti.

### gorr2017composition
```bibtex
@article{gorr2017composition,
  author  = {Gorr, Bronislava and M{\"u}ller, Franz and Azim, Maria and Christ, Hans-J{\"u}rgen and M{\"u}ller, Torsten and Chen, Hans and Kauffmann, Alexander and Heilmaier, Martin},
  title   = {High-Temperature Oxidation Behavior of Refractory High-Entropy Alloys: Effect of Alloy Composition},
  journal = {Oxidation of Metals},
  volume  = {88},
  number  = {3-4},
  pages   = {339--349},
  year    = {2017},
  doi     = {10.1007/s11085-016-9696-y}
}
```
Summary not verified.

### wei2021review
```bibtex
@article{wei2021review,
  author  = {Wei, Ya and Fu, Yu and Pan, Zhi-min and Ma, Yi-chong and Cheng, Hong-xu and Zhao, Qian-cheng and Luo, Hong and Li, Xiao-gang},
  title   = {Influencing factors and mechanism of high-temperature oxidation of high-entropy alloys: A review},
  journal = {International Journal of Minerals, Metallurgy and Materials},
  volume  = {28},
  number  = {6},
  pages   = {915--930},
  year    = {2021},
  doi     = {10.1007/s12613-021-2257-7}
}
```
Summary not verified.

---

## D'. Property databases (relevant to C5: strength vs oxidation overlap)

### borg2020mpea
```bibtex
@article{borg2020mpea,
  author  = {Borg, Christopher K. H. and Frey, Carolina and Moh, Jasper and Pollock, Tresa M. and Gorsse, St{\'e}phane and Miracle, Daniel B. and Senkov, Oleg N. and Meredig, Bryce and Saal, James E.},
  title   = {Expanded dataset of mechanical properties and observed phases of multi-principal element alloys},
  journal = {Scientific Data},
  volume  = {7},
  number  = {1},
  pages   = {430},
  year    = {2020},
  doi     = {10.1038/s41597-020-00768-9}
}
```
Summary: Mechanical properties of 630 MPEAs: composition, processing, microstructure, density, hardness, YS, UTS or compressive strength, elongation and Young's modulus. Records from earlier reviews are included "with minor error corrections".
Relevance:
- C5: this is the main strength dataset, and it has no oxidation fields.
- C1: even curated compilations need error corrections.

### couzinie2018rhea
```bibtex
@article{couzinie2018rhea,
  author  = {Couzini{\'e}, J.-P. and Senkov, O.N. and Miracle, D.B. and Dirras, G.},
  title   = {Comprehensive data compilation on the mechanical properties of refractory high-entropy alloys},
  journal = {Data in Brief},
  volume  = {21},
  pages   = {1622--1641},
  year    = {2018},
  doi     = {10.1016/j.dib.2018.10.071}
}
```
Summary: Mechanical properties of 122 RHEAs/RCCAs reported from 2010 to January 2018: composition, microstructure, metallurgical state, density, loading mode, and yield stress as a function of test temperature.
Relevance: C5. This is the RHEA strength-versus-temperature compilation to intersect with the oxidation datasets.

### gorsse2018db
```bibtex
@article{gorsse2018db,
  author  = {Gorsse, S. and Nguyen, M.H. and Senkov, O.N. and Miracle, D.B.},
  title   = {Database on the mechanical properties of high entropy alloys and complex concentrated alloys},
  journal = {Data in Brief},
  volume  = {21},
  pages   = {2664--2678},
  year    = {2018},
  doi     = {10.1016/j.dib.2018.11.111}
}
```
Summary: Mechanical properties of 370 HEAs/CCAs reported from 2004 to 2016, mostly at room temperature. Yield stress and elongation against temperature are given for 27 RHEAs.
Relevance: C5.

---

## F. UNVERIFIED (do not cite without checking)
- "Design of high temperature oxidation-resistant high-entropy alloys via machine learning and natural mixing process", Corrosion Science (2025?), ScienceDirect PII S0010938X25003749. Found only as a search-result title; DOI and authors not confirmed.
- "Predicting the parabolic growth rate constant for high-temperature oxidation of steels using machine learning models", Corrosion Science (2023?), PII S0010938X23003517. Only the SSRN preprint DOI 10.2139/ssrn.4341076 was matched; the journal version was not verified.
- "High-Temperature Oxidation Behaviors of AlCoCrFeNi2.1 and CoCrFeNiNb0.5 Eutectic High-Entropy Alloys: A Machine Learning-Assisted Design and Mechanism Study", J. Mater. Eng. Perform. (2026), doi 10.1007/s11665-026-14531-5 (from a URL only). Not verified in Crossref.
- Lin, Gorsse, Lo, Murakami, Yeh, "Machine learning-driven exploration of high-temperature oxidation-resistant refractory high entropy alloys", IMRC 2024 conference communication (HAL hal-04753817). Exists in HAL, but there is no DOI and it is not peer reviewed.
- "Dong et al." random-forest oxidation of Al-Cr alloys, mentioned without a reference in arXiv:2511.01095. Not identified.
- Cui et al. 2021, Metall. Mater. Trans. A 52(9):4112–4124 (oxide-scale thickness ML in hot rolling of steels), seen only in a reference list. Not checked in Crossref, and peripheral.
- A recent dedicated RHEA-oxidation review from 2023–2026 (Gorsse, Senkov, Miracle or Lo) was searched for and **not found**. Only Gorr et al. 2021 is RHEA-specific.
- Miracle & Senkov, Acta Mater 122 (2017) 448–511, doi:10.1016/j.actamat.2016.08.081. Crossref metadata is verified but the abstract was not read. It is a general HEA review, not about oxidation.
