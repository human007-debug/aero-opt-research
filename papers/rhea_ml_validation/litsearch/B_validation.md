# Related work B: validation methodology (extrapolation, OOD, grouped CV, applicability domain, redundancy, cross-dataset transfer)

Paper: "How far can data-driven models be trusted for designing oxidation-resistant refractory alloys? Distance-dependent accuracy, cross-dataset transfer and data quality"

Verification protocol: every entry below was checked against Crossref (`api.crossref.org/works/<DOI>`) for authors, title, journal, volume, issue, pages/article number and year (arXiv API for 2406.05143). Summaries are written from the actual abstract. Where Crossref had no abstract, it came from OpenAlex, Europe PMC, Semantic Scholar, the arXiv preprint or ChemRxiv; the source is noted for each. Checked 2026-10-12.

27 references verified. They are tagged **[core]** (recommended for the related-work section; 17) or **[optional]** (10).

---

## 1. Extrapolation and out-of-distribution (OOD) evaluation in materials ML

### meredig2018can [core]
```bibtex
@article{meredig2018can,
  author  = {Meredig, Bryce and Antono, Erin and Church, Carena and Hutchinson, Maxwell and Ling, Julia and Paradiso, Sean and Blaiszik, Ben and Foster, Ian and Gibbons, Brenna and Hattrick-Simpers, Jason and Mehta, Apurva and Ward, Logan},
  title   = {Can machine learning identify the next high-temperature superconductor? {E}xamining extrapolation performance for materials discovery},
  journal = {Molecular Systems Design \& Engineering},
  volume  = {3},
  number  = {5},
  pages   = {819--825},
  year    = {2018},
  doi     = {10.1039/c8me00012c}
}
```
Summary (abstract via Semantic Scholar; Crossref has only its first sentence): The paper argues that traditional ML metrics overestimate performance for materials discovery. It introduces leave-one-cluster-out cross-validation (LOCO-CV) and a simple nearest-neighbour benchmark, and shows that discovery performance depends strongly on the problem, the data sampling and the degree of extrapolation.
Relevance: C3 and C2. This is the canonical materials reference for replacing random CV with group-wise (cluster) CV and for nearest-neighbour baselines. LOCO clusters are formed in feature space. Our groups follow the physical data-generating structure instead: the same alloy (repeated time/temperature points) and the same source paper. We also go beyond a single LOCO score by reporting error as a continuous function of distance to the nearest training alloy.

### xiong2020evaluating [core]
```bibtex
@article{xiong2020evaluating,
  author  = {Xiong, Zheng and Cui, Yuxin and Liu, Zhonghao and Zhao, Yong and Hu, Ming and Hu, Jianjun},
  title   = {Evaluating explorative prediction power of machine learning algorithms for materials discovery using $k$-fold forward cross-validation},
  journal = {Computational Materials Science},
  volume  = {171},
  pages   = {109203},
  year    = {2020},
  doi     = {10.1016/j.commatsci.2019.109203}
}
```
Summary (abstract via Semantic Scholar): Standard k-fold CV and hold-out tests over-estimate how well a model explores toward "outlier" materials with extreme property values. The authors propose k-fold-m-step forward CV (sort by property, predict beyond the training range) and show that models that score well under traditional CV have very low explorative power for formation energy, band gap and superconducting Tc.
Relevance: C3. This is another case of CV design changing the conclusion, but here the split is by target value (extrapolation in y). We split by composition and source (extrapolation in x and across laboratories), which is the relevant mode for alloy design.

### kauwe2020can [optional]
```bibtex
@article{kauwe2020can,
  author  = {Kauwe, Steven K. and Graser, Jake and Murdock, Ryan and Sparks, Taylor D.},
  title   = {Can machine learning find extraordinary materials?},
  journal = {Computational Materials Science},
  volume  = {174},
  pages   = {109498},
  year    = {2020},
  doi     = {10.1016/j.commatsci.2019.109498}
}
```
Summary (from the ChemRxiv preprint abstract, doi:10.26434/chemrxiv.9396623.v1; the journal abstract could not be retrieved): Using DFT-computed properties (bulk and shear modulus, thermal conductivity, thermal expansion, band gap, Debye temperature), the authors train on the bottom 99% and test whether models identify the top-1% "extraordinary" materials. Models consistently recover about 3/4 of the top compounds with precision typically above 0.5, and classification gives fewer false positives than regression. The authors discuss cautions for record-breaking discovery.
Relevance: C2 (counterpoint). This is a more optimistic view of extrapolation in the target value, obtained on large computed datasets. Our setting is small, experimental and multi-source, and extrapolation is in composition space. It is useful to cite to show that conclusions about extrapolation depend on the data regime.

### omee2024structure [core]
```bibtex
@article{omee2024structure,
  author  = {Omee, Sadman Sadeed and Fu, Nihang and Dong, Rongzhi and Hu, Ming and Hu, Jianjun},
  title   = {Structure-based out-of-distribution ({OOD}) materials property prediction: a benchmark study},
  journal = {npj Computational Materials},
  volume  = {10},
  number  = {1},
  pages   = {144},
  year    = {2024},
  doi     = {10.1038/s41524-024-01316-4}
}
```
Summary (Crossref abstract): Random splitting of materials datasets gives artificially high performance because of the datasets' inherent redundancy. Across five categories of OOD splits on three Matbench datasets, state-of-the-art GNNs significantly underperform their Matbench (random-split) baselines, which shows a substantial generalization gap.
Relevance: C3 and C4. Its random-versus-OOD gap parallels our row-level versus grouped gap, and the OOD splits reorder the models (C4). The work covers structure-based GNNs on DFT/Matbench data. We show the same phenomena for composition-based models on experimental alloy oxidation data, where leakage comes from repeated measurements and shared source papers.

### li2023critical [core]
```bibtex
@article{li2023critical,
  author  = {Li, Kangming and DeCost, Brian and Choudhary, Kamal and Greenwood, Michael and Hattrick-Simpers, Jason},
  title   = {A critical examination of robustness and generalizability of machine learning prediction of materials properties},
  journal = {npj Computational Materials},
  volume  = {9},
  number  = {1},
  pages   = {55},
  year    = {2023},
  doi     = {10.1038/s41524-023-01012-9}
}
```
Summary (Crossref abstract): Models trained on Materials Project 2018 degrade severely on new compounds in Materials Project 2021 because of distribution shift, so an excellent benchmark score does not imply good generalization. UMAP feature-space projection and disagreement within a committee of models can flag OOD samples, and adding about 1% of well-chosen test data greatly improves accuracy.
Relevance: C4 (closest analogue). It tests transfer to newer data rather than reporting internal CV alone. However, the "external" set is a later release of the same DFT database, with the same workflow and no measurement noise. Our external test set is independently compiled from experiments, with different laboratories, protocols and test conditions. We also show that model rankings, not only absolute errors, fail to transfer.

### li2025probing [core]
```bibtex
@article{li2025probing,
  author  = {Li, Kangming and Rubungo, Andre Niyongabo and Lei, Xiangyun and Persaud, Daniel and Choudhary, Kamal and DeCost, Brian and Dieng, Adji Bousso and Hattrick-Simpers, Jason},
  title   = {Probing out-of-distribution generalization in machine learning for materials},
  journal = {Communications Materials},
  volume  = {6},
  number  = {1},
  pages   = {9},
  year    = {2025},
  doi     = {10.1038/s43246-024-00731-w}
}
```
Summary (Crossref abstract): Heuristic OOD tasks (unseen chemistry or structural symmetry) often show good performance, even for boosted trees. However, most such test data lie in regions of representation space well covered by training data. Only tasks that are truly outside the training domain perform poorly, and for those, scaling up data or training brings limited or adverse effects. Most OOD tests therefore reflect interpolation.
Relevance: C2 (strong support). It motivates measuring the actual feature-space distance to the training set instead of trusting split labels, which is exactly our distance-to-nearest-training-alloy analysis. We add experimental data and an external dataset, and we show the distance-error trend persists externally.

### durdy2022random [optional]
```bibtex
@article{durdy2022random,
  author  = {Durdy, Samantha and Gaultois, Michael W. and Gusev, Vladimir V. and Bollegala, Danushka and Rosseinsky, Matthew J.},
  title   = {Random projections and kernelised leave one cluster out cross validation: universal baselines and evaluation tools for supervised machine learning of material properties},
  journal = {Digital Discovery},
  volume  = {1},
  number  = {6},
  pages   = {763--778},
  year    = {2022},
  doi     = {10.1039/d2dd00039c}
}
```
Summary (from the arXiv:2206.08841 abstract; Crossref has only the graphical abstract): Materials datasets contain bias and skew from the research process, so LOCO-CV is used to measure prediction of unseen groups, but cluster-size effects complicate it. The authors compare composition representations (domain knowledge rarely helps except for band gap), show that an RBF kernel improves cluster separability on all 10 datasets, and recommend kernelised LOCO-CV for measuring extrapolatory power.
Relevance: C3. It refines LOCO-CV for composition-based models. Our grouping uses provenance (alloy, source paper) rather than unsupervised clusters, which targets the leakage that actually occurs in literature-compiled experimental data.

### bartel2020critical [optional]
```bibtex
@article{bartel2020critical,
  author  = {Bartel, Christopher J. and Trewartha, Amalie and Wang, Qi and Dunn, Alexander and Jain, Anubhav and Ceder, Gerbrand},
  title   = {A critical examination of compound stability predictions from machine-learned formation energies},
  journal = {npj Computational Materials},
  volume  = {6},
  number  = {1},
  pages   = {97},
  year    = {2020},
  doi     = {10.1038/s41524-020-00362-y}
}
```
Summary (Crossref abstract): Seven formation-energy models (five compositional) predict formation energy well on 85,014 Materials Project compositions, but all compositional models perform poorly on stability (the downstream design quantity), especially in sparse chemical spaces. Accurate formation-energy prediction does not imply accurate stability prediction.
Relevance: C4 (by analogy). Good headline metrics on one evaluation do not carry over to the task that matters. In our case, internal-CV rank does not carry over to independent-data rank.

---

## 2. Applicability domain and error versus distance to the training data (C2)

### sheridan2004similarity [core]
```bibtex
@article{sheridan2004similarity,
  author  = {Sheridan, Robert P. and Feuston, Bradley P. and Maiorov, Vladimir N. and Kearsley, Simon K.},
  title   = {Similarity to molecules in the training set is a good discriminator for prediction accuracy in {QSAR}},
  journal = {Journal of Chemical Information and Computer Sciences},
  volume  = {44},
  number  = {6},
  pages   = {1912--1928},
  year    = {2004},
  doi     = {10.1021/ci049782w}
}
```
Summary (abstract via OpenAlex): Across 20 in-house QSAR activity sets, the best discriminators of prediction error were similarity to the nearest training molecule and the number of training neighbours above a similarity cutoff. The most similar molecules are predicted best, regardless of QSAR method or descriptor.
Relevance: C2 (direct precedent). This is the original demonstration that error depends on nearest-neighbour distance to training data, from cheminformatics. We quantify the same effect (3-4x error growth) for experimental refractory-alloy oxidation data and show that it holds on an independent external dataset, not only in retrospective CV.

### janet2019quantitative [core]
```bibtex
@article{janet2019quantitative,
  author  = {Janet, Jon Paul and Duan, Chenru and Yang, Tzuhsiung and Nandy, Aditya and Kulik, Heather J.},
  title   = {A quantitative uncertainty metric controls error in neural network-driven chemical discovery},
  journal = {Chemical Science},
  volume  = {10},
  number  = {34},
  pages   = {7913--7922},
  year    = {2019},
  doi     = {10.1039/c9sc02298h}
}
```
Summary (abstract via Europe PMC, PMC6764470): The authors introduce distance to available data in a neural network's latent space as a low-cost uncertainty metric for inorganic and organic chemistry. It is better calibrated than widely used alternatives, and tightening latent-distance cutoffs systematically drives predicted errors below training errors.
Relevance: C2. Distance to the training data is a usable error and applicability-domain signal. We use a simple, model-agnostic composition-space distance, which is interpretable for alloy designers, and validate it externally.

### sutton2020identifying [core]
```bibtex
@article{sutton2020identifying,
  author  = {Sutton, Christopher and Boley, Mario and Ghiringhelli, Luca M. and Rupp, Matthias and Vreeken, Jilles and Scheffler, Matthias},
  title   = {Identifying domains of applicability of machine learning models for materials science},
  journal = {Nature Communications},
  volume  = {11},
  number  = {1},
  pages   = {4428},
  year    = {2020},
  doi     = {10.1038/s41467-020-17112-9}
}
```
Summary (Crossref abstract): Average test error can make models look indistinguishable or uniformly poor while their performance differs substantially across materials. A subgroup-discovery method identifies domains of applicability. For three formation-energy models of transparent conducting oxides with similar, unsatisfactory average errors, it finds distinct domains with notably better performance.
Relevance: C2 and C4. A single averaged CV score hides where a model can be trusted. The work uses DFT data from a single source. We characterise trust as a function of distance to the nearest training alloy and test it on independent experimental data.

### schultz2025general [core]  (= arXiv:2406.05143)
```bibtex
@article{schultz2025general,
  author  = {Schultz, Lane E. and Wang, Yiqi and Jacobs, Ryan and Morgan, Dane},
  title   = {A general approach for determining applicability domain of machine learning models},
  journal = {npj Computational Materials},
  volume  = {11},
  number  = {1},
  pages   = {95},
  year    = {2025},
  doi     = {10.1038/s41524-025-01573-x}
}
```
Note: arXiv:2406.05143 (v1 28 May 2024, v2 22 Mar 2025; same authors and title) is the preprint of this paper. Cite the journal version above. (This is also the "Wang et al. / Schultz et al." applicability-domain candidate.)
Summary (arXiv and OpenAlex abstracts, identical): The authors propose a general applicability-domain method that measures dissimilarity in feature space by kernel density estimation. Chemically unrelated groups show high dissimilarity, and high dissimilarity is associated with large residuals and unreliable uncertainty estimates, across several model types and materials-property datasets. Tools are provided to set in-domain/out-of-domain thresholds.
Relevance: C2. This is the most current materials applicability-domain method, and its finding (dissimilarity relates to large error) is what we observe. We add a direct test on an independently compiled experimental dataset, and we look at source-paper effects, which a density-based domain measure cannot see (two sources can sit at the same composition yet disagree).

---

## 3. Grouped or structured cross-validation and data leakage (C3)

### roberts2017cross [core]
```bibtex
@article{roberts2017cross,
  author  = {Roberts, David R. and Bahn, Volker and Ciuti, Simone and Boyce, Mark S. and Elith, Jane and Guillera-Arroita, Gurutzeta and Hauenstein, Severin and Lahoz-Monfort, Jos{\'e} J. and Schr{\"o}der, Boris and Thuiller, Wilfried and Warton, David I. and Wintle, Brendan A. and Hartig, Florian and Dormann, Carsten F.},
  title   = {Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure},
  journal = {Ecography},
  volume  = {40},
  number  = {8},
  pages   = {913--929},
  year    = {2017},
  doi     = {10.1111/ecog.02881}
}
```
Summary (Crossref abstract): Ignoring temporal, spatial, hierarchical or phylogenetic dependence in random CV seriously underestimates predictive error and allows overfitting to non-causal predictors. Block CV is nearly always more appropriate when predicting to new data. However, blocking can also induce extrapolation and so overestimate interpolation error.
Relevance: C3. This is the general methodological basis for grouping hierarchically structured data (rows nested in alloys nested in source papers). Its caveat that blocking can be pessimistic is useful when interpreting source-grouped R2 (0.24 externally, versus 0.42-0.65 grouped internally).

### sheridan2013time [core]
```bibtex
@article{sheridan2013time,
  author  = {Sheridan, Robert P.},
  title   = {Time-split cross-validation as a method for estimating the goodness of prospective prediction},
  journal = {Journal of Chemical Information and Modeling},
  volume  = {53},
  number  = {4},
  pages   = {783--790},
  year    = {2013},
  doi     = {10.1021/ci400084k}
}
```
Summary (abstract via OpenAlex): How test compounds are selected determines whether CV is optimistic or pessimistic relative to true prospective prediction. Random selection is too optimistic and a leave-class-out analogue too pessimistic, while time-split R2 most closely resembles prospective R2.
Relevance: C3 and C4. It directly parallels our hierarchy of row-level CV, alloy-grouped CV, source-grouped CV and independent data, and it supports reporting several split types rather than one.

### kaufman2011leakage [optional]
```bibtex
@inproceedings{kaufman2011leakage,
  author    = {Kaufman, Shachar and Rosset, Saharon and Perlich, Claudia},
  title     = {Leakage in data mining},
  booktitle = {Proceedings of the 17th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining},
  pages     = {556--563},
  year      = {2011},
  doi       = {10.1145/2020408.2020496}
}
```
Note: Crossref gives only the main title "Leakage in data mining". The paper's commonly cited subtitle, "formulation, detection, and avoidance", is not in the Crossref record.
Summary (abstract via OpenAlex): Leakage, meaning information about the target that should not legitimately be available, is pervasive in competitions and real projects, including cases where the i.i.d. assumption is violated. The authors formalise it and propose a learn-predict separation and ways to detect it.
Relevance: C3. This is the general definition of leakage. Repeated time/temperature points of one alloy appearing on both sides of a split is a non-i.i.d. leak of this kind.

### kapoor2023leakage [core]
```bibtex
@article{kapoor2023leakage,
  author  = {Kapoor, Sayash and Narayanan, Arvind},
  title   = {Leakage and the reproducibility crisis in machine-learning-based science},
  journal = {Patterns},
  volume  = {4},
  number  = {9},
  pages   = {100804},
  year    = {2023},
  doi     = {10.1016/j.patter.2023.100804}
}
```
Summary (abstract via OpenAlex): A literature survey finds leakage in 17 fields, affecting 294 papers, sometimes with wildly over-optimistic conclusions. The authors propose a taxonomy of eight leakage types and "model info sheets". A reproducibility case study (civil-war prediction) shows that complex ML no longer beats logistic regression once the errors are corrected.
Relevance: C3 and C4. It places our row-level CV finding (R2 0.92 to 0.42-0.65) within a cross-disciplinary leakage problem, including the reversal of model comparisons once leakage is removed (analogous to our C4 ranking instability). Materials and alloy data are not among its surveyed case studies.

### afflerbach2022machine [core]
```bibtex
@article{afflerbach2022machine,
  author  = {Afflerbach, Benjamin T. and Francis, Carter and Schultz, Lane E. and Spethson, Janine and Meschke, Vanessa and Strand, Elliot and Ward, Logan and Perepezko, John H. and Thoma, Dan and Voyles, Paul M. and Szlufarska, Izabela and Morgan, Dane},
  title   = {Machine learning prediction of the critical cooling rate for metallic glasses from expanded datasets and elemental features},
  journal = {Chemistry of Materials},
  volume  = {34},
  number  = {7},
  pages   = {2945--2954},
  year    = {2022},
  doi     = {10.1021/acs.chemmater.1c03542}
}
```
Summary (abstract via OpenAlex and arXiv:2305.15390): A random-forest model of critical cooling rate is trained on over 2000 values merged from multiple direct and indirect sources. The error is 0.66 log units (K/s) under 5-fold CV and 0.59 log units under leave-out-one-group CV on alloy-system groups when the target's constituents appear more than 500 times in training. The model is most useful for identifying promising alloy systems rather than precise composition regions.
Relevance: C3 (closest alloy-specific precedent). It uses alloy-system grouping on a multi-source experimental alloy dataset. Its group-CV result is conditioned on well-represented constituents. We go further: we group by source paper as well as alloy, quantify the optimism of row-level CV, and add an independent external dataset.

---

## 4. Dataset redundancy and benchmark design

### li2023exploiting [core]
```bibtex
@article{li2023exploiting,
  author  = {Li, Kangming and Persaud, Daniel and Choudhary, Kamal and DeCost, Brian and Greenwood, Michael and Hattrick-Simpers, Jason},
  title   = {Exploiting redundancy in large materials datasets for efficient machine learning with less data},
  journal = {Nature Communications},
  volume  = {14},
  number  = {1},
  pages   = {7283},
  year    = {2023},
  doi     = {10.1038/s41467-023-42992-y}
}
```
Summary (Crossref abstract): Up to 95% of the data in several large materials datasets can be removed with little effect on in-distribution performance. The redundant data relate to over-represented material types and do not mitigate severe degradation on OOD samples. Uncertainty-based active learning builds much smaller, equally informative datasets.
Relevance: C3 and C2. Redundancy inflates in-distribution scores without improving OOD performance. In our data the redundancy is structural: many time/temperature rows per alloy and clusters of similar alloys from the same paper. That is why row-level CV looks good (R2 0.92) while distant alloys are poorly predicted.

### wallach2018most [optional]
```bibtex
@article{wallach2018most,
  author  = {Wallach, Izhar and Heifets, Abraham},
  title   = {Most ligand-based classification benchmarks reward memorization rather than generalization},
  journal = {Journal of Chemical Information and Modeling},
  volume  = {58},
  number  = {5},
  pages   = {916--932},
  year    = {2018},
  doi     = {10.1021/acs.jcim.7b00403}
}
```
Summary (abstract via OpenAlex): Train-validation redundancy causes undetected overfitting. The proposed AVE bias measure correlates strongly with reported performance across seven virtual-screening benchmarks, so much previously reported ligand-based performance may reflect overfitting to benchmarks rather than prospective accuracy.
Relevance: C3 (cross-field analogue). Benchmark scores track train-test similarity, which is the mechanism behind our row-level versus grouped gap.

### dunn2020benchmarking [optional]
```bibtex
@article{dunn2020benchmarking,
  author  = {Dunn, Alexander and Wang, Qi and Ganose, Alex and Dopp, Daniel and Jain, Anubhav},
  title   = {Benchmarking materials property prediction methods: the {M}atbench test set and {A}utomatminer reference algorithm},
  journal = {npj Computational Materials},
  volume  = {6},
  number  = {1},
  pages   = {138},
  year    = {2020},
  doi     = {10.1038/s41524-020-00406-3}
}
```
Summary (Crossref abstract): Matbench comprises 13 supervised tasks (312 to 132k samples) from 10 DFT-derived and experimental sources. The Automatminer AutoML pipeline is best on 8 of 13 tasks, and crystal-graph methods outperform traditional ML at about 10^4 or more data points.
Relevance: C4 (context). It is the standard materials benchmark and is evaluated with nested CV within each dataset. OOD studies (omee2024structure) show that its rankings change under OOD splits. Our paper tests ranking transfer to an independent experimental dataset.

### wu2018moleculenet [optional]
```bibtex
@article{wu2018moleculenet,
  author  = {Wu, Zhenqin and Ramsundar, Bharath and Feinberg, Evan N. and Gomes, Joseph and Geniesse, Caleb and Pappu, Aneesh S. and Leswing, Karl and Pande, Vijay},
  title   = {{MoleculeNet}: a benchmark for molecular machine learning},
  journal = {Chemical Science},
  volume  = {9},
  number  = {2},
  pages   = {513--530},
  year    = {2018},
  doi     = {10.1039/c7sc02664a}
}
```
Summary (abstract via OpenAlex/Europe PMC): MoleculeNet is a large molecular-ML benchmark that curates public datasets, metrics, featurizations and algorithms in DeepChem. Learnable representations generally perform best but struggle with data scarcity and imbalance. The abstract does not mention scaffold splits. The full text (PMC5868307) describes scaffold splitting (separating molecules by 2-D framework), which "offers a greater challenge for learning algorithms than the random split", and recommends it for some datasets.
Relevance: C3 (analogue). The scaffold split is the cheminformatics counterpart of our alloy/source-grouped split. Cite the full text for the scaffold-split point, not the abstract.

### zhang2018strategy [optional, weak]
```bibtex
@article{zhang2018strategy,
  author  = {Zhang, Ying and Ling, Chen},
  title   = {A strategy to apply machine learning to small datasets in materials science},
  journal = {npj Computational Materials},
  volume  = {4},
  number  = {1},
  pages   = {25},
  year    = {2018},
  doi     = {10.1038/s41524-018-0081-z}
}
```
Note: the title is "A strategy to apply machine learning to small datasets..." (not "Strategies ... small data sets").
Summary (Crossref abstract): In small materials datasets, the effect of data size is mediated by the model's degrees of freedom. A precision-DoF association signals underfitting and large bias, which restricts accurate prediction in unknown domains. Adding a crude physical estimate of the property as a feature improves accuracy in three case studies.
Relevance: Weak, as general small-data context. It concerns model construction, not validation. Cite only if a small-data framing is needed; otherwise drop.

---

## 5. Discovery-oriented metrics and prospective or external evaluation (C4)

### borg2023quantifying [core]
```bibtex
@article{borg2023quantifying,
  author  = {Borg, Christopher K. H. and Muckley, Eric S. and Nyby, Clara and Saal, James E. and Ward, Logan and Mehta, Apurva and Meredig, Bryce},
  title   = {Quantifying the performance of machine learning models in materials discovery},
  journal = {Digital Discovery},
  volume  = {2},
  number  = {2},
  pages   = {327--338},
  year    = {2023},
  doi     = {10.1039/d2dd00113f}
}
```
Summary (from the arXiv:2210.13587 abstract; Crossref has only the graphical abstract): In simulated sequential-learning discovery, static metrics (RMSE, r2) are decoupled from a model's ability to guide discovery. Discovery performance depends on the target decile, use of uncertainty, the number of targets and the number of iterations. The authors propose Discovery Yield and Discovery Probability.
Relevance: C4. Low CV error does not imply usefulness for design. We show a complementary failure: CV-based model selection does not transfer across datasets.

### riebesell2025framework [optional]
```bibtex
@article{riebesell2025framework,
  author  = {Riebesell, Janosh and Goodall, Rhys E. A. and Benner, Philipp and Chiang, Yuan and Deng, Bowen and Ceder, Gerbrand and Asta, Mark and Lee, Alpha A. and Jain, Anubhav and Persson, Kristin A.},
  title   = {A framework to evaluate machine learning crystal stability predictions},
  journal = {Nature Machine Intelligence},
  volume  = {7},
  number  = {6},
  pages   = {836--847},
  year    = {2025},
  doi     = {10.1038/s42256-025-01055-1}
}
```
Summary (Crossref abstract): Matbench Discovery addresses the disconnect between retrospective and prospective benchmarking and between formation energy and stability. It highlights a misalignment between regression metrics and task-relevant classification metrics: accurate regressors can have high false-positive rates near the hull.
Relevance: C4 (context). It is a prospective-style benchmark in which test data differ from training data. It is DFT-only, whereas our external set is experimental.

### zech2018variable [core]
```bibtex
@article{zech2018variable,
  author  = {Zech, John R. and Badgeley, Marcus A. and Liu, Manway and Costa, Anthony B. and Titano, Joseph J. and Oermann, Eric Karl},
  title   = {Variable generalization performance of a deep learning model to detect pneumonia in chest radiographs: A cross-sectional study},
  journal = {PLOS Medicine},
  volume  = {15},
  number  = {11},
  pages   = {e1002683},
  year    = {2018},
  doi     = {10.1371/journal.pmed.1002683}
}
```
Summary (abstract via OpenAlex): CNNs trained on radiographs from one or two hospital systems performed worse on other hospitals than on internal test sets. The best internal model (AUC 0.931) dropped to 0.815 externally, and models could exploit site-specific prevalence, since sorting by hospital alone gave AUC 0.861.
Relevance: C4 and the source-paper effect (cross-field analogue). Each site, like each source paper, carries its own systematic signal. Internal validation, even when pooled across sites, overstates external performance. This supports both our source-grouped CV and the independent-dataset test.

---

## 6. High-entropy alloy specific

### li2024efficient [optional]
```bibtex
@article{li2024efficient,
  author  = {Li, Kangming and Choudhary, Kamal and DeCost, Brian and Greenwood, Michael and Hattrick-Simpers, Jason},
  title   = {Efficient first principles based modeling via machine learning: from simple representations to high entropy materials},
  journal = {Journal of Materials Chemistry A},
  volume  = {12},
  number  = {21},
  pages   = {12412--12422},
  year    = {2024},
  doi     = {10.1039/d4ta00982g}
}
```
Summary (from the arXiv:2403.15579 abstract; Crossref has only the graphical abstract): An open DFT dataset of 84k ordered and disordered alloy structures with up to seven components. ML models generalize from ordered to disordered structures, from low-order to high-order alloys and from equimolar to non-equimolar compositions, and the authors conclude that models can generalize from cheaper, simpler systems to more complex ones. Using unrelaxed structures can significantly degrade generalization.
Relevance: C2 (contrast). This is an explicit HEA generalization study, but on noise-free DFT energies, where it finds favourable transfer. Our experimental oxidation data show strong distance-dependent degradation. Data type (computed versus experimental, multi-source) is likely a key factor, and that is a positioning point for our paper.

---

## UNVERIFIED / not included

- **High-entropy-alloy ML validation with leave-one-system-out (HEA phase or hardness):** no verifiable paper found whose central contribution is grouped or out-of-system validation for HEA phase or hardness models. The literature found uses random k-fold or leave-one-out CV. This is itself a gap our paper can state, worded cautiously as "to our knowledge".
- **Gorsse et al., GBDT model for RHEA oxidation mass gain with "iterated nested k-fold CV with shuffling" (reported as Scripta Materialia 2024/25):** seen only in a web-search snippet. Crossref was NOT checked and there is no DOI. It is likely in the topic-A (oxidation ML) list; verify there before citing.
- **Bejjipurapu et al., arXiv 2511.01095 (Gaussian process for RCCA oxidation) and an alphaxiv-reported 2025 study on HEAs with unseen elements:** seen only in search snippets and NOT verified.
- **Kauwe et al. 2020:** metadata verified via Crossref. The summary is from the ChemRxiv preprint abstract because the journal abstract was inaccessible (ScienceDirect unreachable).
- **Kaufman et al. 2011:** the subtitle "formulation, detection, and avoidance" is not in Crossref. The extended journal version (ACM TKDD, 2012) was not checked.
- **Candidates checked and resolved:** "Wang et al. / Schultz et al. applicability domain" and arXiv:2406.05143 are the same work (schultz2025general). "Zhang & Ling, Strategies..." is the paper titled "A strategy..." (zhang2018strategy).

---

## Positioning summary (for drafting)

1. **The distance-error dependence is known, but mostly for molecules or DFT data and not tested externally.** sheridan2004similarity, janet2019quantitative, sutton2020identifying, schultz2025general and li2025probing show that error rises with dissimilarity to the training data. We quantify it (3-4x) for experimental refractory-alloy oxidation data, both on grouped CV and on an independent dataset.
2. **Random/row-level CV is optimistic under structured or redundant data; the remedies are group, cluster or block CV.** See roberts2017cross, meredig2018can, durdy2022random, sheridan2013time, kaufman2011leakage, kapoor2023leakage, li2023exploiting, omee2024structure and wallach2018most. Our data have a nested structure (row, alloy, source paper), and we show the optimism step by step (R2 0.92, then 0.42-0.65, then 0.24 externally). The only close alloy precedent groups by alloy system only (afflerbach2022machine).
3. **"OOD" splits are often interpolation** (li2025probing). Reporting error against an explicit nearest-neighbour composition distance is therefore more informative than a split label.
4. **Cross-dataset transfer has been tested mainly within one DFT database** (li2023critical: MP2018 to MP2021) or in other fields (zech2018variable, external hospitals). We test transfer to an independently compiled experimental dataset with different laboratories and protocols, and we show that model rankings from internal CV, even source-grouped, do not transfer (C4). This complements findings that good benchmark metrics do not imply good discovery performance (borg2023quantifying, bartel2020critical, riebesell2025framework).
5. **Experimental, multi-source alloy data with source-paper effects are under-studied.** Most validation benchmarks are DFT-derived (dunn2020benchmarking, omee2024structure, li2023exploiting, li2024efficient), and the HEA-specific generalization study we found (li2024efficient) uses DFT data and reports favourable transfer. We found no HEA/RHEA study centred on grouped or external validation (see UNVERIFIED), so the paper should state this gap cautiously.
