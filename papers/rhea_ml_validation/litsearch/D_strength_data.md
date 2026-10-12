# Related work, part D: RHEA strength models and data, multi-objective design, ML phase prediction, reliability of digitised data

Verification method (2026-10-12): every DOI below was resolved through the Crossref REST API (`api.crossref.org/works/<DOI>`). Authors, title, venue, volume, pages or article number, and year are copied from the Crossref record. The software entry was checked through the DataCite API. Summaries are based on the abstract, taken from Crossref, Semantic Scholar, arXiv, or the first page of the publisher PDF / NSF-PAR accepted manuscript, with the source noted. Where no abstract could be retrieved, the entry says **"summary not verified"**.

Status tags: `[V]` means metadata and summary are both verified. `[V-meta]` means the metadata is verified but the summary is not.

---

## D1. Strength models and data for refractory HEAs / RCCAs

### maresca2020mechanistic [V]
```bibtex
@article{maresca2020mechanistic,
  author  = {Maresca, Francesco and Curtin, William A.},
  title   = {Mechanistic origin of high strength in refractory {BCC} high entropy alloys up to 1900{K}},
  journal = {Acta Materialia},
  volume  = {182},
  pages   = {235--249},
  year    = {2020},
  doi     = {10.1016/j.actamat.2019.10.015}
}
```
Summary (from the arXiv:1901.02100v3 abstract; that preprint is titled "...high retained strength..." and carries this DOI): The paper gives a parameter-free theory of edge-dislocation glide through the random solute field in BCC HEAs. It captures strength versus temperature for MoNbTaW and MoNbTaVW up to 1900 K. A reduced analytic version is used to screen more than 600,000 compositions in the Mo-Nb-Ta-V-W family for high retained strength and/or low density.
Relevance: This is the physics-based strength model used in our search. The abstract states the screening and validation only for Mo-Nb-Ta-V-W, which supports claim C5 that applying it outside that family is extrapolation.

### lee2021strength [V]
```bibtex
@article{lee2021strength,
  author  = {Lee, Chanho and Maresca, Francesco and Feng, Rui and Chou, Yi and Ungar, T. and Widom, Michael and An, Ke and Poplawsky, Jonathan D. and Chou, Yi-Chia and Liaw, Peter K. and Curtin, W. A.},
  title   = {Strength can be controlled by edge dislocations in refractory high-entropy alloys},
  journal = {Nature Communications},
  volume  = {12},
  number  = {1},
  pages   = {5474},
  year    = {2021},
  doi     = {10.1038/s41467-021-25807-w}
}
```
Summary (Crossref abstract): In-situ neutron diffraction, HRTEM and the edge theory together show that edge dislocations account for the high strength and strength retention of NbTaTiV and of the low-density CrMoNbV alloy. The theory is then used to search more than 10^7 BCC HEAs and identifies over 10^6 candidate ultra-strong high-T compositions.
Relevance: This is experimental support for the edge model **outside** Mo-Nb-Ta-V-W (Ti- and Cr-containing alloys). Claim C5 ("validated only for Mo-Nb-Ta-V-W") should be softened to something like "validated mainly on Mo-Nb-Ta-V-W and a small number of other BCC alloys". Cr is relevant to oxidation-resistant chemistries.

### baruffi2022screw [V]
```bibtex
@article{baruffi2022screw,
  author  = {Baruffi, C. and Maresca, F. and Curtin, W. A.},
  title   = {Screw vs. edge dislocation strengthening in body-centered-cubic high entropy alloys and implications for guided alloy design},
  journal = {MRS Communications},
  volume  = {12},
  number  = {6},
  pages   = {1111--1118},
  year    = {2022},
  doi     = {10.1557/s43579-022-00278-2}
}
```
Summary (Crossref/Semantic Scholar abstract): The authors apply the screw theory (one fitted parameter) and the parameter-free edge theory to many BCC alloys over a wide temperature range. The edge theory agrees with experiment only in non-dilute alloys with a sufficiently large misfit parameter, which implies a transition from screw-controlled to edge-controlled strengthening as misfit increases.
Relevance: This states the domain of validity of the edge model explicitly (large misfit, non-dilute). It supports our distance-dependent trust argument. Note that a Correction exists (doi:10.1557/s43579-023-00507-2, MRS Commun. 2024), found in a Crossref search; its contents were not read.

### senkov2010refractory [V-meta]
```bibtex
@article{senkov2010refractory,
  author  = {Senkov, O. N. and Wilks, G. B. and Miracle, D. B. and Chuang, C. P. and Liaw, P. K.},
  title   = {Refractory high-entropy alloys},
  journal = {Intermetallics},
  volume  = {18},
  number  = {9},
  pages   = {1758--1765},
  year    = {2010},
  doi     = {10.1016/j.intermet.2010.05.014}
}
```
Summary: **summary not verified.** The publisher has withheld the abstract from Crossref and Semantic Scholar. A web-search snippet of the AFRL preprint describes near-equiatomic W-Nb-Mo-Ta and W-Nb-Mo-Ta-V made by vacuum arc-melting, both single-phase BCC. Check this against the paper.
Relevance: This is the founding RHEA paper, introducing the Mo-Nb-Ta-W(-V) family on which the Maresca-Curtin model was validated.

### senkov2011mechanical [V-meta]
```bibtex
@article{senkov2011mechanical,
  author  = {Senkov, O. N. and Wilks, G. B. and Scott, J. M. and Miracle, D. B.},
  title   = {Mechanical properties of {Nb25Mo25Ta25W25} and {V20Nb20Mo20Ta20W20} refractory high entropy alloys},
  journal = {Intermetallics},
  volume  = {19},
  number  = {5},
  pages   = {698--706},
  year    = {2011},
  doi     = {10.1016/j.intermet.2011.01.004}
}
```
Summary: **summary not verified** (abstract withheld). Vela et al. 2023 (Acta Mater 261, 119351, intro) state that this work reports 1600 °C yield strengths of 405 MPa (NbMoTaW) and 477 MPa (VNbMoTaW). That is a secondary report only.
Relevance: This is the canonical high-T compression data used as the benchmark for the edge model (Maresca & Curtin), and part of the MPEA strength database.

### senkov2018development [V]
```bibtex
@article{senkov2018development,
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
Summary (Semantic Scholar abstract): The review covers 151 RHEAs/RCCAs reported from 2010 to January 2018 by composition, processing, microstructure and phases. It summarises mechanical properties, strengthening mechanisms, **oxidation and corrosion**, and tribology, and discusses future directions.
Relevance: This is the standard RHEA review. It covers both strength and oxidation, but as separate literatures. Cite it for the field and for the definitions of RHEA and RCCA.

### miracle2017critical [V]
```bibtex
@article{miracle2017critical,
  author  = {Miracle, D. B. and Senkov, O. N.},
  title   = {A critical review of high entropy alloys and related concepts},
  journal = {Acta Materialia},
  volume  = {122},
  pages   = {448--511},
  year    = {2017},
  doi     = {10.1016/j.actamat.2016.08.081}
}
```
Summary (Crossref abstract): This is a critical review of the HEA/CCA field, covering terminology, thermodynamics, alloy families, microstructures and properties. It compares an experimental dataset of 408 alloys with CALPHAD datasets, finds that the "entropy effect" and "sluggish diffusion" hypotheses are not supported by the data, and recommends high-throughput experiments and computation.
Relevance: Background on the composition-space size and the limits of thermodynamic rules of thumb, which motivates ML phase classifiers and data-driven search.

### senkov2019high [V]
```bibtex
@article{senkov2019high,
  author  = {Senkov, O. N. and Gorsse, S. and Miracle, D. B.},
  title   = {High temperature strength of refractory complex concentrated alloys},
  journal = {Acta Materialia},
  volume  = {175},
  pages   = {394--405},
  year    = {2019},
  doi     = {10.1016/j.actamat.2019.06.032}
}
```
Summary (Semantic Scholar abstract): The authors analyse 15 single-phase and 11 multi-phase RCCAs, with CALPHAD solidus temperatures and secondary-phase fractions. They correlate the strength drop at 1000 and 1200 °C with composition, T_m and phase content, and examine specific yield strength. Single-phase BCC alloys lose strength once diffusion-controlled mechanisms activate (T ≥ 0.6 T_m). Multi-phase alloys lose strength above 1000 °C, probably because secondary phases dissolve.
Relevance: This directly motivates our objective (specific yield strength at 1000 °C) and the single-phase BCC constraint.

### miracle2024strength [V]
```bibtex
@article{miracle2024strength,
  author  = {Miracle, D. B. and Senkov, O. N. and Frey, C. and Rao, S. and Pollock, T. M.},
  title   = {Strength vs temperature for refractory complex concentrated alloys ({RCCAs}): A critical comparison with refractory {BCC} elements and dilute alloys},
  journal = {Acta Materialia},
  volume  = {266},
  pages   = {119692},
  year    = {2024},
  doi     = {10.1016/j.actamat.2024.119692}
}
```
Summary (from the first part of the Crossref abstract): The paper asks whether the temperature dependence of yield stress in RCCAs differs from that of BCC refractory elements and dilute alloys. It evaluates σ_y(T) for 61 RCCAs using data curated from the literature and finds that σ_y increases progressively from elements to dilute alloys to RCCAs. The remainder of the abstract was not retrieved.
Relevance: This is a recent curated analysis of high-T strength data, i.e. the same data class we use. Useful context for how sparse the 1000 °C data are.

### couzinie2018comprehensive [V]
```bibtex
@article{couzinie2018comprehensive,
  author  = {Couzini{\'e}, J.-P. and Senkov, O. N. and Miracle, D. B. and Dirras, G.},
  title   = {Comprehensive data compilation on the mechanical properties of refractory high-entropy alloys},
  journal = {Data in Brief},
  volume  = {21},
  pages   = {1622--1641},
  year    = {2018},
  doi     = {10.1016/j.dib.2018.10.071}
}
```
Summary (Crossref abstract): A compilation of mechanical properties for 122 RHEAs/RCCAs reported from 2010 to January 2018. It gives composition, microstructure, metallurgical state, computed density, loading type and yield stress as a function of test temperature.
Relevance: This is the RHEA-specific precursor of the Borg et al. dataset and the source of temperature-dependent yield stress.

### gorsse2018database [V]
```bibtex
@article{gorsse2018database,
  author  = {Gorsse, S. and Nguyen, M. H. and Senkov, O. N. and Miracle, D. B.},
  title   = {Database on the mechanical properties of high entropy alloys and complex concentrated alloys},
  journal = {Data in Brief},
  volume  = {21},
  pages   = {2664--2678},
  year    = {2018},
  doi     = {10.1016/j.dib.2018.11.111}
}
```
Summary (Crossref abstract): Mechanical properties of 370 HEAs/CCAs (2004–2016), including composition, microstructure, density, hardness, room-temperature tensile and compression properties, and modulus. Temperature-dependent yield stress and elongation are given for 27 RHEAs.
Relevance: This is a precursor of the MPEA database. A **corrigendum** exists (doi:10.1016/j.dib.2020.106216, Data in Brief 2020, confirmed in a Crossref search), which is a concrete example of errors in curated literature datasets (claim C1).

### borg2020expanded [V]
```bibtex
@article{borg2020expanded,
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
Summary (Crossref abstract): Mechanical properties of 630 MPEAs, built on earlier databases "with minor error corrections" and extended with post-2019 literature. Fields include composition, processing, microstructure, density, hardness, yield and ultimate strength, elongation and modulus, plus new descriptors such as grain size. Hosted on Citrination.
Relevance: This is the strength data source in our paper (claim C5). The explicit error corrections in this release support our data-quality theme (C1).

### gorr2021current [V]
```bibtex
@article{gorr2021current,
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
Summary (Crossref/Semantic Scholar abstract): Reviews RHEA high-temperature oxidation by composition, mass change, corrosion products and scales. Many RHEAs oxidise as badly as pure refractory metals (pesting, spallation, complete oxidation). Some form protective α-Al2O3 or complex oxides such as CrTaO4.
Relevance: Context for the oxidation objective. Shows that the oxidation literature is reported as mass change, which is our oxidation target.

---

## D2. Multi-objective / multi-property computational design of RHEAs (including oxidation)

### vela2023high [V]
```bibtex
@article{vela2023high,
  author  = {Vela, Brent and Acemi, Cafer and Singh, Prashant and Kirk, Tanner and Trehern, William and Norris, Eli and Johnson, Duane D. and Karaman, Ibrahim and Arr{\'o}yave, Raymundo},
  title   = {High-throughput exploration of the {WMoVTaNbAl} refractory multi-principal-element alloys under multiple-property constraints},
  journal = {Acta Materialia},
  volume  = {248},
  pages   = {118784},
  year    = {2023},
  doi     = {10.1016/j.actamat.2023.118784}
}
```
Summary (abstract, publisher PDF via NSF-PAR): The paper treats alloy design as a composition-agnostic constraint-satisfaction problem over WMoVTaNbAl. The constraints are single-phase stability, density, solidus, 1300 °C yield strength and DBTT, and 214 MoNbV-rich alloys satisfy them. Three alloys were checked by DFT, CALPHAD and experiment, and Mo30Nb35Ta5V25W5 outperforms 1546 MPEAs in a public database. From the body text: yield strength comes from the Maresca-Curtin model with rule-of-mixtures inputs, and oxidation is **not** a constraint. The authors note that Al, normally added for oxidation resistance, destabilises BCC.
Relevance: This is the closest methodological precedent (Maresca-Curtin plus a BCC-phase constraint in multi-property screening). It omits oxidation, which is the gap we address.

### khatamsaz2022multi [V]
```bibtex
@article{khatamsaz2022multi,
  author  = {Khatamsaz, Danial and Vela, Brent and Singh, Prashant and Johnson, Duane D. and Allaire, Douglas and Arr{\'o}yave, Raymundo},
  title   = {Multi-objective materials bayesian optimization with active learning of design constraints: Design of ductile refractory multi-principal-element alloys},
  journal = {Acta Materialia},
  volume  = {236},
  pages   = {118133},
  year    = {2022},
  doi     = {10.1016/j.actamat.2022.118133}
}
```
Summary (abstract, publisher PDF via NSF-PAR): Presents a multi-information Bayesian optimisation framework that actively learns design constraints while optimising several objectives. It is demonstrated on Mo-Nb-Ti-V-W, optimising two DFT ductility indicators (Pugh's ratio, Cauchy pressure) under manufacturing-relevant constraints.
Relevance: A precedent for multi-objective, constraint-aware RHEA search. The objectives are ductility, not oxidation.

### vela2023data [V]
```bibtex
@article{vela2023data,
  author  = {Vela, Brent and Khatamsaz, Danial and Acemi, Cafer and Karaman, Ibrahim and Arr{\'o}yave, Raymundo},
  title   = {Data-augmented modeling for yield strength of refractory high entropy alloys: A {Bayesian} approach},
  journal = {Acta Materialia},
  volume  = {261},
  pages   = {119351},
  year    = {2023},
  doi     = {10.1016/j.actamat.2023.119351}
}
```
Summary (abstract, publisher PDF via NSF-PAR): Combines ML, simple physics models and cheap proxy data through Bayesian updating. Specifically it fuses the Borg et al. (2020) database with the Maresca-Curtin (2020) model into a compact yield-strength model that is more accurate than the state of the art. The model is cross-validated, tested for physics-informed extrapolation, and benchmarked against standard GPRs in a toy BO problem.
Relevance: This uses the **same two ingredients** we use (Borg data plus Maresca-Curtin) and tests extrapolation, so it is the key comparator for our distance-dependent accuracy analysis of strength. It does not address oxidation.

### acemi2024multi [V-meta]
```bibtex
@article{acemi2024multi,
  author  = {Acemi, Cafer and Vela, Brent and Norris, Eli and Trehern, William and Atli, Kadri Can and Cleek, Conner and Arr{\'o}yave, Raymundo and Karaman, Ibrahim},
  title   = {Multi-objective, multi-constraint high-throughput design, synthesis, and characterization of tungsten-containing refractory multi-principal element alloys},
  journal = {Acta Materialia},
  volume  = {281},
  pages   = {120379},
  year    = {2024},
  doi     = {10.1016/j.actamat.2024.120379}
}
```
Summary: **summary not verified** (abstract not retrievable). The title indicates experimental follow-up of multi-objective, multi-constraint design of W-containing refractory MPEAs.
Relevance: An experimental validation example from the same design framework. Cite only after reading the abstract.

### giles2026yield [V]
```bibtex
@article{giles2026yield,
  author  = {Giles, Stephen A. and Shortt, Hugh and Liaw, Peter K. and Sengupta, Debasis},
  title   = {Yield Strength-Plasticity Trade-Off and Uncertainty Quantification for Machine-Learning-Based Design of Refractory High-Entropy Alloys},
  journal = {High Entropy Alloys \& Materials},
  volume  = {4},
  number  = {1},
  pages   = {58--70},
  year    = {2026},
  doi     = {10.1007/s44210-025-00074-2},
  note    = {Published online 2025-12-19; preprint arXiv:2304.13932}
}
```
Summary (Semantic Scholar abstract of the journal version): Builds ML models for RHEA yield strength and plasticity to define trade-off criteria. Uses probabilistic uncertainty quantification and explainability analysis, and validates predictions on two newly synthesised RHEAs.
Relevance: A prior example of uncertainty quantification in ML strength models for RHEA design. We go further by quantifying how error grows with distance from the training data.

### bejjipurapu2026machine [V]
```bibtex
@article{bejjipurapu2026machine,
  author  = {Bejjipurapu, Akhil and Strachan, Alejandro and Sandhage, Kenneth H. and Titus, Michael S.},
  title   = {Machine learning descriptors for predicting the high temperature oxidation of refractory complex concentrated alloys},
  journal = {Materials Advances},
  volume  = {7},
  number  = {16},
  pages   = {8364--8377},
  year    = {2026},
  doi     = {10.1039/d6ma00714g},
  note    = {Preprint arXiv:2511.01095}
}
```
Summary (arXiv abstract): Builds a database of 77 compositions (elements, binaries and higher-order alloys) with specific mass change after 24 h in air at 900–1000 °C. A GPR with oxidation-product descriptors reaches a test MAE of 5.78 mg/cm², better than alloy-only descriptors. The model is used to screen more than 5100 quaternary RCCAs.
Relevance: This is the most directly comparable oxidation-ML work (same target quantity). It covers oxidation only, with no strength objective and no cross-dataset or distance-dependent accuracy analysis. **Must be cited and differentiated.**

### bejjipurapu2026active [V]
```bibtex
@misc{bejjipurapu2026active,
  author       = {Bejjipurapu, Akhil and Karumuri, Sharmila and Flanagan, Joseph C. and Tucker, Victoria and Bilionis, Ilias and Strachan, Alejandro and Sandhage, Kenneth H. and Titus, Michael S.},
  title        = {Active Learning Discovery of High Temperature Oxidation Resistant Refractory Complex Concentrated Alloys},
  howpublished = {SSRN preprint},
  year         = {2026},
  doi          = {10.2139/ssrn.6829501}
}
```
Summary (Crossref abstract): Active learning (GPR plus Bayesian global optimisation) on Al-containing quaternary RCCAs, starting from 81 experimentally validated alloys, to predict oxidation at 1000 °C. Five alloys are selected per iteration for experiments, and after six iterations two alloys are identified (e.g. nominal Al30Mo5Ti15Cr50; the abstract was truncated here).
Relevance: Shows closed-loop experimental oxidation design. Again oxidation only, not jointly with strength. Cite as a preprint and check whether it has since been published.

### rao2022machine [V]
```bibtex
@article{rao2022machine,
  author  = {Rao, Ziyuan and Tung, Po-Yen and Xie, Ruiwen and Wei, Ye and Zhang, Hongbin and Ferrari, Alberto and Klaver, T. P. C. and K{\"o}rmann, Fritz and Sukumar, Prithiv Thoudden and Kwiatkowski da Silva, Alisson and Chen, Yao and Li, Zhiming and Ponge, Dirk and Neugebauer, J{\"o}rg and Gutfleisch, Oliver and Bauer, Stefan and Raabe, Dierk},
  title   = {Machine learning--enabled high-entropy alloy discovery},
  journal = {Science},
  volume  = {378},
  number  = {6615},
  pages   = {78--85},
  year    = {2022},
  doi     = {10.1126/science.abo4940}
}
```
Summary (Crossref abstract): A closed-loop active-learning strategy combining ML, DFT, thermodynamic calculations and experiments, applied to high-entropy Invar alloys from very sparse data. Of 17 new alloys made, two have thermal expansion of about 2×10⁻⁶ K⁻¹ at 300 K.
Relevance: The landmark example of ML-driven HEA discovery from sparse data. It contrasts with our setting, where the two property datasets barely overlap.

---

## D3. ML phase prediction for HEAs (solid solution / BCC)

### islam2018machine [V]
```bibtex
@article{islam2018machine,
  author  = {Islam, Nusrat and Huang, Wenjiang and Zhuang, Houlong L.},
  title   = {Machine learning for phase selection in multi-principal element alloys},
  journal = {Computational Materials Science},
  volume  = {150},
  pages   = {230--235},
  year    = {2018},
  doi     = {10.1016/j.commatsci.2018.04.003}
}
```
Summary (Semantic Scholar abstract): A neural network classifies MPEA phases (solid solution, amorphous, intermetallic) from elemental features. Accuracy is above 99% on the full dataset and above 80% on average in cross-validation, with valence electron concentration the most important feature.
Relevance: An early ML phase classifier. The gap between training and cross-validation accuracy is a reminder that in-distribution accuracy overstates reliability.

### huang2019machine [V]
```bibtex
@article{huang2019machine,
  author  = {Huang, Wenjiang and Martin, Pedro and Zhuang, Houlong L.},
  title   = {Machine-learning phase prediction of high-entropy alloys},
  journal = {Acta Materialia},
  volume  = {169},
  pages   = {225--236},
  year    = {2019},
  doi     = {10.1016/j.actamat.2019.03.012}
}
```
Summary (Semantic Scholar abstract): Uses 401 HEAs (174 SS, 54 IM, 173 SS+IM) with KNN, SVM and ANN. Three-class test accuracy is 68.6%, 64.3% and 74.3% respectively. ANN binary accuracies are 86.7% (SS vs IM), 94.3% (SS+IM vs IM) and 78.9% (SS vs SS+IM).
Relevance: A standard baseline for HEA phase classifiers. The moderate cross-validated accuracies justify treating our BCC classifier constraint as uncertain.

### zhou2019machine [V]
```bibtex
@article{zhou2019machine,
  author  = {Zhou, Ziqing and Zhou, Yeju and He, Quanfeng and Ding, Zhaoyi and Li, Fucheng and Yang, Yong},
  title   = {Machine learning guided appraisal and exploration of phase design for high entropy alloys},
  journal = {npj Computational Materials},
  volume  = {5},
  number  = {1},
  pages   = {128},
  year    = {2019},
  doi     = {10.1038/s41524-019-0265-1}
}
```
Summary (Crossref abstract): Critically evaluates empirical HEA phase-design rules with several ML algorithms. An ANN sensitivity matrix quantifies how each design parameter affects the formation of solid solution, intermetallic or amorphous phases, and the authors test new parameters with Fe-Cr-Ni-Zr-Cu experiments.
Relevance: Phase-classifier background. It also shows that empirical rules are tested against new alloys mainly in non-refractory systems.

### pei2020machine [V]
```bibtex
@article{pei2020machine,
  author  = {Pei, Zongrui and Yin, Junqi and Hawk, Jeffrey A. and Alman, David E. and Gao, Michael C.},
  title   = {Machine-learning informed prediction of high-entropy solid solution formation: Beyond the {Hume-Rothery} rules},
  journal = {npj Computational Materials},
  volume  = {6},
  number  = {1},
  pages   = {50},
  year    = {2020},
  doi     = {10.1038/s41524-020-0308-7}
}
```
Summary (Crossref abstract): On 1252 multicomponent alloys, ML predicts solid-solution formation with 93% accuracy. A derived thermodynamics-based rule reaches 73% accuracy, and its FCC/BCC/HCP predictions agree 94% with CALPHAD.
Relevance: A large-data solid-solution classifier, and an alternative or cross-check for our BCC-phase constraint.

---

## D4. Reliability of digitised and literature-extracted data

### rohatgi2018webplotdigitizer [V] (software)
```bibtex
@software{rohatgi2018webplotdigitizer,
  author    = {Rohatgi, Ankit and Rehberg, Steffen and Stanojevic, Zlatan},
  title     = {{WebPlotDigitizer}: Version 4.1 of {WebPlotDigitizer}},
  version   = {4.1},
  publisher = {Zenodo},
  year      = {2018},
  doi       = {10.5281/zenodo.1137880},
  url       = {https://automeris.io}
}
```
Summary: Software record verified on DataCite (title "ankitrohatgi/WebPlotDigitizer: Version 4.1 of WebPlotDigitizer", v4.1, Zenodo, 2018; creators Rohatgi, Ankit; Rehberg, Steffen; "ZlatanStanojevic" (third author given as a GitHub handle; the given/family split is our inference)). automeris.io is live.
Relevance: Cite the tool. **TODO: replace v4.1 with the version the two groups actually used.** No other version's Zenodo DOI was verified here.

### drevon2017intercoder [V]
```bibtex
@article{drevon2017intercoder,
  author  = {Drevon, Daniel and Fursa, Sophie R. and Malcolm, Allura L.},
  title   = {Intercoder Reliability and Validity of {WebPlotDigitizer} in Extracting Graphed Data},
  journal = {Behavior Modification},
  volume  = {41},
  number  = {2},
  pages   = {323--339},
  year    = {2017},
  doi     = {10.1177/0145445516673998}
}
```
Summary (Crossref abstract): Two coders independently extracted 3,596 data points from 168 series in 36 graphs across 18 studies with WebPlotDigitizer. Intercoder reliability and validity were high.
Relevance: Direct precedent for our two-independent-group agreement check (C1). Their setting is single-case design plots, not materials property figures.

### moeyaert2016reliability [V]
```bibtex
@article{moeyaert2016reliability,
  author  = {Moeyaert, Mariola and Maggin, Daniel and Verkuilen, Jay},
  title   = {Reliability, Validity, and Usability of Data Extraction Programs for Single-Case Research Designs},
  journal = {Behavior Modification},
  volume  = {40},
  number  = {6},
  pages   = {874--900},
  year    = {2016},
  doi     = {10.1177/0145445516645763}
}
```
Summary (Crossref abstract): Compares Ungraph, DataThief, WebPlotDigitizer and XYit at the level of individual data points. Reliability and validity did not depend on the program but did depend on the individual graph. WebPlotDigitizer was the best option overall (usability, time, cost).
Relevance: Supports our claim that digitisation error depends on the figure (graph quality and scale) rather than the tool, which motivates per-figure agreement checks.

### burda2017estimating [V]
```bibtex
@article{burda2017estimating,
  author  = {Burda, Brittany U. and O'Connor, Elizabeth A. and Webber, Elizabeth M. and Redmond, Nadia and Perdue, Leslie A.},
  title   = {Estimating data from figures with a Web-based program: Considerations for a systematic review},
  journal = {Research Synthesis Methods},
  volume  = {8},
  number  = {3},
  pages   = {258--262},
  year    = {2017},
  doi     = {10.1002/jrsm.1232}
}
```
Summary (Crossref abstract): Participants used WebPlotDigitizer to estimate data from two figures. ICC exceeded 0.95, but the percent difference from the true values ranged from 0.23% to 30.35% for a continuous outcome and from 0.22% to 8.92% for event rates. The authors recommend transparency and sensitivity analyses.
Relevance: Shows that **high inter-rater agreement does not guarantee accuracy** (errors up to about 30%). This is an important caveat for our C1 claim: agreement between the two groups bounds precision, not bias.

### aydin2022validity [V]
```bibtex
@article{aydin2022validity,
  author  = {Aydin, Orhan and Yassikaya, Muhammed Yasin},
  title   = {Validity and Reliability Analysis of the {PlotDigitizer} Software Program for Data Extraction from Single-Case Graphs},
  journal = {Perspectives on Behavior Science},
  volume  = {45},
  number  = {1},
  pages   = {239--257},
  year    = {2022},
  doi     = {10.1007/s40614-021-00284-0}
}
```
Summary (Semantic Scholar abstract): 6,846 data points were digitised on three computers from 15 hypothetical graphs and 186 published graphs. Intercoder and intracoder correlations, plus recomputed effect sizes, were nearly perfect.
Relevance: Additional evidence on digitisation reliability, including the use of synthetic graphs with known ground truth. That design could be borrowed to estimate the absolute error in our figures.

### court2018auto [V]
```bibtex
@article{court2018auto,
  author  = {Court, Callum J. and Cole, Jacqueline M.},
  title   = {Auto-generated materials database of {Curie} and {N{\'e}el} temperatures via semi-supervised relationship extraction},
  journal = {Scientific Data},
  volume  = {5},
  number  = {1},
  pages   = {180111},
  year    = {2018},
  doi     = {10.1038/sdata.2018.111}
}
```
Summary (Crossref abstract): ChemDataExtractor plus a modified Snowball algorithm extracted 39,822 records of compounds and their Curie/Néel temperatures from 68,078 articles. Estimated overall precision is 73%.
Relevance: Quantifies error rates of automated literature extraction for materials databases (about 27% imprecision). This contrasts with our manual double digitisation.

### kim2017materials [V]
```bibtex
@article{kim2017materials,
  author  = {Kim, Edward and Huang, Kevin and Saunders, Adam and McCallum, Andrew and Ceder, Gerbrand and Olivetti, Elsa},
  title   = {Materials Synthesis Insights from Scientific Literature via Text Extraction and Machine Learning},
  journal = {Chemistry of Materials},
  volume  = {29},
  number  = {21},
  pages   = {9436--9444},
  year    = {2017},
  doi     = {10.1021/acs.chemmater.7b03500}
}
```
Summary (Crossref abstract): An NLP pipeline compiles synthesis parameters from more than 12,000 papers on metal oxides. ML then predicts critical parameters, for example for hydrothermal synthesis of titania nanotubes.
Relevance: Background on literature-mined materials data. Cite briefly in the data-provenance discussion.

### polak2024extracting [V]
```bibtex
@article{polak2024extracting,
  author  = {Polak, Maciej P. and Morgan, Dane},
  title   = {Extracting accurate materials data from research papers with conversational language models and prompt engineering},
  journal = {Nature Communications},
  volume  = {15},
  number  = {1},
  pages   = {1569},
  year    = {2024},
  doi     = {10.1038/s41467-024-45914-8}
}
```
Summary (Crossref abstract): ChatExtract uses engineered prompts with follow-up verification questions on conversational LLMs. Precision and recall are close to 90% (GPT-4) on materials data, and the method is used to build databases including **yield strengths of high-entropy alloys**.
Relevance: An alternative, automated route to HEA strength data, with quantified extraction error. It extracts from text, not figures, so it is a complement to digitisation.

---

## UNVERIFIED / not included
- **Ajimshad, A. & Sekhar, R. A. (2026)**, "Machine Learning and Edge Dislocation Theory Enabled Accelerated Design of High-Strength, BCC, Non-Equimolar NbMoTiVZr Refractory High Entropy Alloys," *J. Phase Equilib. Diffus.*, doi:10.1007/s11669-026-01273-z. The DOI, title and authors are confirmed in Crossref, but there is no volume or pages yet (online 2026-09-28) and no abstract was available. It is possibly a close competitor (ML plus the edge model outside Mo-Nb-Ta-V-W). Read it before citing.
- **Senkov et al., NbMoCrTiAl / Al-Cr-containing oxidation-resistant RHEAs**: no Senkov-authored NbMoCrTiAl oxidation paper was found in Crossref searches. Related Gorr-group papers exist (e.g. Müller et al., Oxid. Met. 2020, doi:10.1007/s11085-020-09983-6, on Y additions to NbMoCrTiAl at 1000 °C; Gorr et al., Oxid. Met. 2017, doi:10.1007/s11085-016-9696-y; Müller et al., Corros. Sci. 2019, doi:10.1016/j.corsci.2019.108161). These DOIs appeared in Crossref search results but their full records and abstracts were not checked.
- **"Islam et al. 2018" in the candidate list** is the Islam, Huang & Zhuang Comput. Mater. Sci. paper above (verified). No separate Islam 2018 paper was found.
- **Rohatgi WebPlotDigitizer, other versions** (e.g. 4.x/5.x): not verified. Only the v4.1 Zenodo DOI was confirmed.
- No peer-reviewed study was found that quantifies WebPlotDigitizer error specifically on **materials-science** property plots (log axes, error bars, overlapping symbols). The quantitative studies above are all from the behavioural and medical sciences. This is worth stating as a gap our C1 check partly fills. This is a negative search result, not proof of absence.
