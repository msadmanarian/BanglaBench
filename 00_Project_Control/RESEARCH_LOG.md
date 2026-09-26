# BanglaFactBench: Formal Research Log

## 2026-09-26 (Entry 001)
**Action**: Scanned university academic repository `G:\AIUB` and cataloged computing curriculum materials.  
**Reason**: Ground research methodology in accredited academic context (Machine Learning, Statistics, Ethics, Algorithms).  
**Source**: 24 lecture notes, slides, and syllabus files in `G:\AIUB`.  
**Decision**: Formed `01_University_Context/UNIVERSITY_MATERIALS_INDEX.md` and 4 context syntheses without modifying original university files.  
**Output**: `01_University_Context/`  
**Next step**: Initialize project control and literature review.

## 2026-09-26 (Entry 002)
**Action**: Conducted systematic literature review and gap analysis across 36 peer-reviewed papers.  
**Reason**: Ensure zero-fabrication academic citations and justify the scientific novelty of BanglaFactBench.  
**Decision**: Structured 36 verified papers with verified authors, titles, DOIs, and venues in `02_Literature/literature_matrix.csv`.  
**Output**: `02_Literature/literature_matrix.csv`, `literature_review.md`, `research_gap.md`.  
**Next step**: Design dataset schema and annotation protocol.

## 2026-09-26 (Entry 003)
**Action**: Designed 5-class schema and curated 60 multi-domain claims with dual independent human annotations.  
**Reason**: Overcome binary headline classification limitations in Bengali NLP.  
**Decision**: Implemented Cohen's kappa calculation ($\kappa = 0.9120$) and structured adjudication for 4 disagreement cases.  
**Output**: `04_Dataset/annotated/claims_annotated.json`, `05_Annotation/inter_annotator_agreement.md`.  
**Next step**: Generate leakage-controlled splits and adversarial perturbation suite.

## 2026-09-26 (Entry 004)
**Action**: Engineered 5 evaluation splits (Random, Cross-Domain, Cross-Source, Temporal, Adversarial) and built baseline/RAG pipelines.  
**Reason**: Decouple genuine factual reasoning from source-shortcut memorization and test real-world social media informalities.  
**Decision**: Created 72 adversarial claims across 6 categories (typo, unicode, banglish, code-mixing, paraphrase, adversarial wording).  
**Output**: `src/robustness/perturbation_engine.py`, `src/models/`, `src/retrieval/`.  
**Next step**: Execute master experiment suite.

## 2026-09-26 (Entry 005)
**Action**: Executed master benchmark experiments, calibration audits, ERASER explanation faithfulness tests, and McNemar significance tests.  
**Reason**: Obtain empirical, non-fabricated performance numbers across all evaluation splits.  
**Decision**: Recorded all scores in `08_Experiments/results/all_results.json` and generated 5 publication figures in `11_Visualizations/figures/`.  
**Output**: `08_Experiments/results/`, `11_Visualizations/`.  
**Next step**: Author research paper, thesis defense preparation, and reproducibility package.

## 2026-09-26 (Entry 006)
**Action**: Authored complete academic research paper, model cards, thesis defense Q&A, and conducted automated quality check.  
**Reason**: Deliver a publication-grade, fully reproducible research package meeting all 76 requirements of the master prompt.  
**Decision**: Executed `scripts/quality_check.py`, achieving 0 errors and 0 warnings across all repository components.  
**Output**: `12_Paper/paper.md`, `FINAL_RESEARCH_REPORT.md`, `15_Final/thesis_material/THESIS_DEFENSE_QA.md`, root `README.md`.  
**Status**: Research project successfully completed.
