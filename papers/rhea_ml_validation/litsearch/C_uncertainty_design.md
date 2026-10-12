# Related work C: UQ/calibration, optimiser's curse, trust regions, clustered bootstrap

Verification date: 2026-10-12. Every entry below was checked against Crossref (`api.crossref.org/works/<DOI>`), the arXiv API, or the official proceedings page (proceedings.mlr.press / papers.nips.cc), as noted. Summaries come from the abstract retrieved from Crossref, Semantic Scholar, arXiv or proceedings, unless marked "summary not verified".

Tiers: **[CORE]** means cite this. **[OPT]** means optional or supporting.

---

## 1. Uncertainty quantification and calibration for regression (materials ML)

### [CORE] kuleshov2018accurate
```bibtex
@inproceedings{kuleshov2018accurate,
  author    = {Kuleshov, Volodymyr and Fenner, Nathan and Ermon, Stefano},
  title     = {Accurate Uncertainties for Deep Learning Using Calibrated Regression},
  booktitle = {Proceedings of the 35th International Conference on Machine Learning},
  series    = {Proceedings of Machine Learning Research},
  volume    = {80},
  pages     = {2796--2804},
  year      = {2018},
  publisher = {PMLR},
  url       = {https://proceedings.mlr.press/v80/kuleshov18a.html},
  note      = {arXiv:1807.00263}
}
```
Verified via the PMLR page and arXiv. Summary: Bayesian and probabilistic regression models often produce miscalibrated uncertainty (for example, a 90% credible interval that does not contain the truth 90% of the time) because of model misspecification and approximate inference. The paper proposes a Platt-scaling-like recalibration procedure that applies to any regression model and gives calibrated intervals given enough data.
Relevance: This is the canonical definition of regression calibration and interval coverage. It motivates our check of 90% interval coverage and the post-hoc variance rescaling of the GP. Our 62% coverage for Bayesian ridge is exactly the miscalibration that Kuleshov et al. describe for Bayesian linear regression.

### [CORE] tran2020methods
```bibtex
@article{tran2020methods,
  author  = {Tran, Kevin and Neiswanger, Willie and Yoon, Junwoong and Zhang, Qingyang and Xing, Eric and Ulissi, Zachary W.},
  title   = {Methods for comparing uncertainty quantifications for material property predictions},
  journal = {Machine Learning: Science and Technology},
  volume  = {1},
  number  = {2},
  pages   = {025006},
  year    = {2020},
  doi     = {10.1088/2632-2153/ab7e1a}
}
```
Verified via Crossref. Summary: Proposes a suite of figures and metrics (accuracy, calibration, sharpness) for judging the UQ of surrogate models in materials and catalysis screening, demonstrated on DFT adsorption energies. A CNN combined with a Gaussian process performed best.
Relevance: Gives the materials-ML precedent for calibration and sharpness metrics, which we extend to an independent external dataset rather than in-distribution test splits.

### [CORE] palmer2022calibration
```bibtex
@article{palmer2022calibration,
  author  = {Palmer, Glenn and Du, Siqi and Politowicz, Alexander and Emory, Joshua Paul and Yang, Xiyu and Gautam, Anupraas and Gupta, Grishma and Li, Zhelong and Jacobs, Ryan and Morgan, Dane},
  title   = {Calibration after bootstrap for accurate uncertainty quantification in regression models},
  journal = {npj Computational Materials},
  volume  = {8},
  number  = {1},
  pages   = {115},
  year    = {2022},
  doi     = {10.1038/s41524-022-00794-8}
}
```
Verified via Crossref. Summary: Shows that the raw standard deviation of a bootstrap ensemble is not an accurate uncertainty estimate. A simple calibration step dramatically improves it on synthetic data and on many materials datasets.
Relevance: This is the closest precedent for our approach, which scales predictive std by a factor fitted in (grouped) CV. Our contribution is to test whether such a calibration holds on an independent dataset (GP about 94% versus Bayesian ridge 62%).

### [CORE] hirschfeld2020uncertainty
```bibtex
@article{hirschfeld2020uncertainty,
  author  = {Hirschfeld, Lior and Swanson, Kyle and Yang, Kevin and Barzilay, Regina and Coley, Connor W.},
  title   = {Uncertainty Quantification Using Neural Networks for Molecular Property Prediction},
  journal = {Journal of Chemical Information and Modeling},
  volume  = {60},
  number  = {8},
  pages   = {3770--3780},
  year    = {2020},
  doi     = {10.1021/acs.jcim.0c00502}
}
```
Verified via Crossref. Summary: Systematically compares several UQ methods on five molecular regression datasets with multiple metrics. No method is unequivocally best, and none ranks errors reliably across datasets.
Relevance: Supports our position that UQ quality depends on the dataset and has to be checked empirically, especially across datasets.

### [OPT] lookman2019active
```bibtex
@article{lookman2019active,
  author  = {Lookman, Turab and Balachandran, Prasanna V. and Xue, Dezhen and Yuan, Ruihao},
  title   = {Active learning in materials science with emphasis on adaptive sampling using uncertainties for targeted design},
  journal = {npj Computational Materials},
  volume  = {5},
  number  = {1},
  pages   = {21},
  year    = {2019},
  doi     = {10.1038/s41524-019-0153-8}
}
```
Verified via Crossref. Summary: A review of active learning and adaptive sampling for materials discovery. It covers surrogate models with uncertainties and the utility functions that use them to choose experiments.
Relevance: Background showing that surrogate uncertainties drive design decisions in materials, so miscalibration propagates directly into candidate selection.

### [OPT] ling2017high
```bibtex
@article{ling2017high,
  author  = {Ling, Julia and Hutchinson, Maxwell and Antono, Erin and Paradiso, Sean and Meredig, Bryce},
  title   = {High-Dimensional Materials and Process Optimization Using Data-Driven Experimental Design with Well-Calibrated Uncertainty Estimates},
  journal = {Integrating Materials and Manufacturing Innovation},
  volume  = {6},
  number  = {3},
  pages   = {207--217},
  year    = {2017},
  doi     = {10.1007/s40192-017-0098-z}
}
```
Verified via Crossref and Semantic Scholar. Summary: Sequential experimental design with uncertainty-aware data-driven models (random forests with calibrated uncertainty) balances exploring high-uncertainty candidates against exploiting high-performing regions. On four materials test cases it found the optimum with about 3x fewer measurements than random search.
Relevance: An early materials paper that argues calibrated uncertainty is a prerequisite for model-guided design.

### [OPT] rasmussen2006gaussian
```bibtex
@book{rasmussen2006gaussian,
  author    = {Rasmussen, Carl Edward and Williams, Christopher K. I.},
  title     = {Gaussian Processes for Machine Learning},
  publisher = {The MIT Press},
  address   = {Cambridge, MA},
  year      = {2006},
  doi       = {10.7551/mitpress/3206.001.0001}
}
```
Verified via Crossref (monograph record; Crossref "issued" date is 2005-11-23, the print edition is conventionally cited as 2006). Summary not verified (book, no abstract). It is the standard reference for GP regression.
Relevance: Standard citation for the GP surrogate and its predictive variance.

---

## 2. Distance-dependent accuracy, domain of applicability, grouped/cluster CV

### [CORE] janet2019quantitative
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
Verified via Crossref. The summary is taken from the abstract of the ChemRxiv preprint (10.26434/chemrxiv.7900277.v2); the published abstract is only one line. Summary: Introduces distance to the training data in the latent space of a neural network as a cheap, calibrated uncertainty metric. It outperforms ensembles and feature-space distances, and tightening the distance cutoff systematically reduces errors during chemical-space exploration.
Relevance: The most direct precedent for using distance to data both as an uncertainty proxy and as a constraint (cutoff) during design. It parallels our distance-dependent accuracy analysis and the distance trust region.

### [CORE] meredig2018can
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
Verified via Crossref and Semantic Scholar. Summary: Traditional ML metrics overestimate performance for materials discovery. The paper introduces leave-one-cluster-out CV (LOCO CV) and a nearest-neighbour benchmark, and shows that discovery performance depends strongly on extrapolation.
Relevance: Justifies our grouped (cluster-wise) CV and the framing of accuracy as a function of distance from the training data.

### [CORE] sutton2020identifying
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
Verified via Crossref. Summary: Uses subgroup discovery to identify domains of applicability (DA) within a materials class. Models with indistinguishable average error turn out to have distinct DAs with much better local performance.
Relevance: Supports reporting accuracy conditionally (by region or distance) rather than as one global CV score.

### [CORE] schultz2025general
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
Verified via Crossref and Semantic Scholar. Summary: Defines model domain using a kernel-density-based dissimilarity in feature space. High dissimilarity is associated with both large residuals and unreliable uncertainty estimates, and the paper provides tools for setting in-domain/out-of-domain thresholds.
Relevance: Recent, closely aligned evidence that both accuracy and UQ reliability degrade with distance from the data. This supports our distance-dependent analysis and the distance trust region.

### [CORE] li2023critical
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
Verified via Crossref and Semantic Scholar. Summary: Models trained on Materials Project 2018 degrade severely on new compounds in MP 2021 because of distribution shift. UMAP and disagreement between multiple models can flag out-of-distribution samples.
Relevance: Precedent for cross-dataset transfer failures. Its use of disagreement between models as an OOD signal is conceptually close to our cross-surrogate evaluation of Pareto fronts.

### [OPT] roberts2017cross
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
Verified via Crossref. Summary: Random CV on structured (hierarchical, spatial and similar) data seriously underestimates predictive error because of residual dependence and overfitting to non-causal predictors. Block CV with a carefully chosen blocking strategy is the remedy.
Relevance: A general statistical justification for grouped CV, since our data are clustered by source study or alloy family. It is also the grounding for fitting the variance-calibration factor on grouped rather than random folds.

### [OPT] kauwe2020can
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
Verified via Crossref. The summary is from the ChemRxiv preprint abstract (10.26434/chemrxiv.9396623.v1); the published abstract was not retrieved. Summary: Tests whether ML trained on the bottom 99% of DFT property values can identify the top-1% ("extraordinary") materials. Regression and classification recover about 3/4 of them with precision typically above 0.5.
Relevance: A nuanced counterpoint. Extrapolation to the extremes is partly possible, but precision is imperfect, which is consistent with optimiser's-curse shrinkage at the top of a ranking.

---

## 3. Optimiser's curse, surrogate exploitation, offline model-based optimisation

### [CORE] smith2006optimizer
```bibtex
@article{smith2006optimizer,
  author  = {Smith, James E. and Winkler, Robert L.},
  title   = {The Optimizer's Curse: Skepticism and Postdecision Surprise in Decision Analysis},
  journal = {Management Science},
  volume  = {52},
  number  = {3},
  pages   = {311--322},
  year    = {2006},
  doi     = {10.1287/mnsc.1050.0451}
}
```
Verified via Crossref. Summary: If alternatives are selected by maximising noisy value estimates, the chosen alternative's realised value is expected to fall short of its estimate even when every estimate is unbiased. The disappointment comes from the selection itself, and the paper studies (Bayesian) corrections.
Relevance: This is the theoretical basis for claim C6. NSGA-II selects points where a single surrogate's errors are favourable, so independent surrogates predict them to be worse.

### [CORE] brookes2019conditioning
```bibtex
@inproceedings{brookes2019conditioning,
  author    = {Brookes, David and Park, Hahnbeom and Listgarten, Jennifer},
  title     = {Conditioning by adaptive sampling for robust design},
  booktitle = {Proceedings of the 36th International Conference on Machine Learning},
  series    = {Proceedings of Machine Learning Research},
  volume    = {97},
  pages     = {773--782},
  year      = {2019},
  publisher = {PMLR},
  url       = {https://proceedings.mlr.press/v97/brookes19a.html},
  note      = {arXiv:1901.10060}
}
```
Verified via the PMLR page and arXiv. Summary: In design problems that maximise the output of predictive "oracles" (for example, protein fluorescence), the models have pathologies far from the training data. CbAS constrains the search with a prior over realistic inputs so that optimisation stays where the oracle is trustworthy.
Relevance: An ML-side statement of surrogate exploitation, with a remedy (staying close to the data distribution) that is analogous to our distance trust region.

### [CORE] fannjiang2020autofocused
```bibtex
@inproceedings{fannjiang2020autofocused,
  author    = {Fannjiang, Clara and Listgarten, Jennifer},
  title     = {Autofocused oracles for model-based design},
  booktitle = {Advances in Neural Information Processing Systems},
  volume    = {33},
  pages     = {12945--12956},
  year      = {2020},
  url       = {https://papers.nips.cc/paper_files/paper/2020/hash/972cda1e62b72640cb7ac702714a115f-Abstract.html},
  note      = {arXiv:2006.08052}
}
```
Verified via the NeurIPS proceedings page and arXiv. Summary: Data-driven design (proteins, molecules, materials such as superconductors) has to move beyond the region where the regression model was trained. The paper formalises design as a non-zero-sum game and retrains ("autofocuses") the oracle as the search moves, without new data.
Relevance: Explicitly names materials design as a setting where the surrogate is queried out of distribution during optimisation. This is the mechanism behind our C6 cross-surrogate disagreement.

### [CORE] trabucco2021conservative
```bibtex
@inproceedings{trabucco2021conservative,
  author    = {Trabucco, Brandon and Kumar, Aviral and Geng, Xinyang and Levine, Sergey},
  title     = {Conservative Objective Models for Effective Offline Model-Based Optimization},
  booktitle = {Proceedings of the 38th International Conference on Machine Learning},
  series    = {Proceedings of Machine Learning Research},
  volume    = {139},
  pages     = {10358--10368},
  year      = {2021},
  publisher = {PMLR},
  url       = {https://proceedings.mlr.press/v139/trabucco21a.html},
  note      = {arXiv:2107.06882}
}
```
Verified via the PMLR page and arXiv. Summary: In offline MBO, optimising directly against a learned model finds designs that "fool" it into predicting high values because of distribution shift. COMs learn a model that lower-bounds the true objective out of distribution.
Relevance: A clear statement of the adversarial-exploitation failure mode, together with a conservative remedy. Our trust region (distance plus predicted std) is a simpler conservative constraint, and we show it only partly prevents exploitation.

### [OPT] trabucco2022design
```bibtex
@inproceedings{trabucco2022design,
  author    = {Trabucco, Brandon and Geng, Xinyang and Kumar, Aviral and Levine, Sergey},
  title     = {Design-Bench: Benchmarks for Data-Driven Offline Model-Based Optimization},
  booktitle = {Proceedings of the 39th International Conference on Machine Learning},
  series    = {Proceedings of Machine Learning Research},
  volume    = {162},
  pages     = {21658--21676},
  year      = {2022},
  publisher = {PMLR},
  url       = {https://proceedings.mlr.press/v162/trabucco22a.html},
  note      = {arXiv:2202.08450}
}
```
Verified via the PMLR page and arXiv; the summary was read from the first part of the arXiv abstract. Summary: Introduces standardised benchmarks for offline MBO, where only a static dataset is available, across domains such as proteins, DNA, materials and robots.
Relevance: Positions our setting (fixed literature datasets, no new experiments) as offline MBO.

### [OPT] kumar2020model
```bibtex
@inproceedings{kumar2020model,
  author    = {Kumar, Aviral and Levine, Sergey},
  title     = {Model Inversion Networks for Model-Based Optimization},
  booktitle = {Advances in Neural Information Processing Systems},
  volume    = {33},
  pages     = {5126--5137},
  year      = {2020},
  url       = {https://papers.nips.cc/paper_files/paper/2020/hash/373e4c5d8edfa8b74fd4b6791d0cf6dc-Abstract.html},
  note      = {arXiv:1912.13464}
}
```
Verified via the NeurIPS proceedings page and arXiv. Summary: For data-driven optimisation from logged data, MINs learn an inverse map from scores to inputs so that the search avoids out-of-distribution and invalid inputs.
Relevance: Another offline-MBO approach motivated by the need to avoid OOD inputs. Cite only if there is space.

---

## 4. Trust regions and distance constraints in surrogate-based optimisation

### [CORE] eriksson2019scalable
```bibtex
@inproceedings{eriksson2019scalable,
  author    = {Eriksson, David and Pearce, Michael and Gardner, Jacob and Turner, Ryan D. and Poloczek, Matthias},
  title     = {Scalable Global Optimization via Local {B}ayesian Optimization},
  booktitle = {Advances in Neural Information Processing Systems},
  volume    = {32},
  pages     = {5497--5508},
  year      = {2019},
  url       = {https://papers.nips.cc/paper_files/paper/2019/hash/6c990b7aca7bc7058f5e98ea909e924b-Abstract.html},
  note      = {arXiv:1910.01739}
}
```
Verified via the NeurIPS proceedings page and arXiv. The page range comes from the arXiv journal-ref, because the NeurIPS page metadata lists no pages. Summary: Argues that global GP models with global acquisition over-explore in high dimensions. TuRBO fits local models inside trust regions and allocates samples across them with a bandit approach.
Relevance: The canonical trust-region BO reference. Note the difference: TuRBO's trust region exists for search efficiency and is adapted with new evaluations, while ours is a static constraint (distance to data and predicted std) meant to limit extrapolation in an offline setting.

### [OPT] jones1998efficient
```bibtex
@article{jones1998efficient,
  author  = {Jones, Donald R. and Schonlau, Matthias and Welch, William J.},
  title   = {Efficient Global Optimization of Expensive Black-Box Functions},
  journal = {Journal of Global Optimization},
  volume  = {13},
  number  = {4},
  pages   = {455--492},
  year    = {1998},
  doi     = {10.1023/a:1008306431147}
}
```
Verified via Crossref. Summary not verified (abstract not retrievable from Crossref or Semantic Scholar). It is the standard reference for EGO, which is GP surrogate optimisation using expected improvement.
Relevance: Background on GP-surrogate optimisation that uses predictive uncertainty. Cite it only if the paper discusses acquisition functions.

### [OPT] deb2002fast
```bibtex
@article{deb2002fast,
  author  = {Deb, K. and Pratap, A. and Agarwal, S. and Meyarivan, T.},
  title   = {A fast and elitist multiobjective genetic algorithm: {NSGA-II}},
  journal = {IEEE Transactions on Evolutionary Computation},
  volume  = {6},
  number  = {2},
  pages   = {182--197},
  year    = {2002},
  doi     = {10.1109/4235.996017}
}
```
Verified via Crossref. Summary not verified (abstract not retrieved). It is the standard NSGA-II reference.
Relevance: The optimiser we use in C6, likely needed in the Methods section anyway.

---

## 5. Materials design where ML-predicted candidates differ from experiment

### [CORE] ren2018accelerated
```bibtex
@article{ren2018accelerated,
  author  = {Ren, Fang and Ward, Logan and Williams, Travis and Laws, Kevin J. and Wolverton, Christopher and Hattrick-Simpers, Jason and Mehta, Apurva},
  title   = {Accelerated discovery of metallic glasses through iteration of machine learning and high-throughput experiments},
  journal = {Science Advances},
  volume  = {4},
  number  = {4},
  pages   = {eaaq1566},
  year    = {2018},
  doi     = {10.1126/sciadv.aaq1566}
}
```
Verified via Crossref and Semantic Scholar. Summary: An ML model trained on prior metallic-glass data guided high-throughput experiments in Co-V-Zr. The predictions agreed qualitatively but showed quantitative discrepancies in composition, and retraining on these discrepancies improved accuracy before two further glass-forming ternaries were discovered.
Relevance: Concrete alloy evidence that first-pass ML predictions in a new composition region are quantitatively off and need experimental feedback. This supports treating our Pareto fronts as candidates rather than validated optima.

### [OPT] rao2022machine
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
Verified via Crossref and Semantic Scholar. Summary: A closed-loop active-learning strategy (ML, DFT, thermodynamics, experiments) for high-entropy Invar alloys starting from sparse data. After 17 new alloys were synthesised, two with very low thermal expansion (about 2e-6 per K at 300 K) were identified.
Relevance: A high-profile HEA example showing that ML-guided design is iterative and that most proposed candidates do not reach the target (2 of 17). This motivates experimental validation loops rather than single-shot surrogate optimisation. Do not overstate it: the paper presents a success.

---

## 6. Statistics: (clustered) bootstrap

### [CORE] field2007bootstrapping
```bibtex
@article{field2007bootstrapping,
  author  = {Field, C. A. and Welsh, A. H.},
  title   = {Bootstrapping Clustered Data},
  journal = {Journal of the Royal Statistical Society Series B: Statistical Methodology},
  volume  = {69},
  number  = {3},
  pages   = {369--390},
  year    = {2007},
  doi     = {10.1111/j.1467-9868.2007.00593.x}
}
```
Verified via Crossref. Summary: Analyses bootstraps for clustered (one-way) data. The cluster bootstrap, which resamples whole clusters, gives consistent variance estimates under both the transformation and the random-effect model, while the residual bootstrap is consistent only under the transformation model.
Relevance: Theoretical justification for our clustered (group) bootstrap that resamples source groups rather than individual alloys.

### [CORE] cameron2008bootstrap
```bibtex
@article{cameron2008bootstrap,
  author  = {Cameron, A. Colin and Gelbach, Jonah B. and Miller, Douglas L.},
  title   = {Bootstrap-Based Improvements for Inference with Clustered Errors},
  journal = {The Review of Economics and Statistics},
  volume  = {90},
  number  = {3},
  pages   = {414--427},
  year    = {2008},
  doi     = {10.1162/rest.90.3.414}
}
```
Verified via Crossref. The summary is from the abstract of the SSRN working-paper version (10.2139/ssrn.956890); the journal abstract is elided by the publisher. Summary: With few clusters (5-30), standard cluster-robust inference over-rejects. Cluster bootstrap-t procedures, especially the wild cluster bootstrap, restore near-nominal test size.
Relevance: Important caveat for our setting if the number of source groups is small. Cite it when stating the limitations of the group bootstrap CIs.

### [OPT] davison1997bootstrap
```bibtex
@book{davison1997bootstrap,
  author    = {Davison, A. C. and Hinkley, D. V.},
  title     = {Bootstrap Methods and their Application},
  publisher = {Cambridge University Press},
  address   = {Cambridge},
  year      = {1997},
  doi       = {10.1017/CBO9780511802843}
}
```
Verified via Crossref (monograph record). Summary not verified (book). It is a standard bootstrap reference that includes resampling for hierarchical data.
Relevance: General bootstrap and CI methodology reference.

### [OPT] efron1993introduction
```bibtex
@book{efron1993introduction,
  author    = {Efron, Bradley and Tibshirani, Robert J.},
  title     = {An Introduction to the Bootstrap},
  publisher = {Chapman \& Hall},
  address   = {New York},
  year      = {1993},
  doi       = {10.1007/978-1-4899-4541-9}
}
```
Verified via Crossref: the DOI 10.1007/978-1-4899-4541-9 record gives authors, title and year 1993, with publisher listed as "Springer US" (Springer's record of the Chapman & Hall edition). A later CRC record also exists (10.1201/9780429246593, dated 1994). Use whichever publisher field the journal style prefers. Summary not verified (book).
Relevance: Foundational bootstrap reference (percentile CIs).

---

## UNVERIFIED / dropped

- **Thaler, "winner's curse"**: the Crossref search did not return the intended reference. Not listed. If a winner's-curse citation is wanted, a candidate is Thaler (1988), J. Econ. Perspect. 2(1) 191-202, "Anomalies: The Winner's Curse". TODO: verify from source.
- **Levi, Gispan, Giladi, Fetaya (2022), "Evaluating and Calibrating Uncertainty Prediction in Regression Tasks", Sensors 22, 5540, doi:10.3390/s22155540**: metadata confirmed via a Crossref search, but the abstract was not read. Summary not verified, so it is not included above. It is an optional calibration-metric (ENCE) reference.
- **Musil, Willatt, Langovoy, Ceriotti (2019), "Fast and Accurate Uncertainty Estimation in Chemical Machine Learning", J. Chem. Theory Comput. 15, 906-915, doi:10.1021/acs.jctc.8b00959**: metadata confirmed via a Crossref search, but the abstract was not read. It is an optional reference on calibrated GP/ensemble UQ in chemistry.
- **Xiong et al. (2020), "Evaluating explorative prediction power of machine learning algorithms for materials discovery using k-fold forward cross-validation", Comput. Mater. Sci. 171, 109203, doi:10.1016/j.commatsci.2019.109203**: metadata confirmed, abstract not read.
- **Borg et al. (2023), "Quantifying the performance of machine learning models in materials discovery", Digital Discovery**: the Crossref query failed, so it was not verified.
- **Bayesian ridge reference (Tipping 2001 / MacKay 1992)**: not checked here. TODO: verify if needed.
- I found no peer-reviewed paper specifically showing that ML-optimal *oxidation-resistant refractory HEA* candidates failed experimental validation. TODO: search the RHEA oxidation literature (this may be covered by another related-work topic).
