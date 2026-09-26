# Project TODO & Milestone Roadmap: BanglaFactBench

---

## Completed Tasks
- [x] **Step 1**: Scan `G:\AIUB` and build `01_University_Context/UNIVERSITY_MATERIALS_INDEX.md`.
- [x] **Step 2**: Create complete 16-module research workspace structure under `g:\Events\BanglaBench`.
- [x] **Step 3**: Establish foundational context notes on ML pipeline, statistical testing, AI ethics, and OBE alignment.
- [x] **Step 4**: Initialize project control documentation (`PROJECT_STATUS.md`, `RESEARCH_LOG.md`, `DECISION_LOG.md`, `TODO.md`, `RISKS.md`, `CHANGELOG.md`).

---

## Active & Upcoming Tasks

### Stage 1: Literature Review & Gap Analysis (Steps 3–6)
- [ ] Systematic web & academic repository search for Bengali misinformation, fact-checking, and NLP literature (ACL, arXiv, IEEE).
- [ ] Catalog and inspect existing Bengali datasets: BanFakeNews, BanglaCheck, ClaimCheck, BE-Fact, etc.
- [ ] Compile `02_Literature/literature_matrix.csv` with 35+ verified references (no fabricated citations).
- [ ] Author `02_Literature/literature_review.md` and `02_Literature/research_gap.md`.
- [ ] Document search queries in `02_Literature/systematic_search_log.md`.

### Stage 2: Research Design & Formalization (Steps 7–9)
- [ ] Formalize problem statement, motivation, scope, and contributions in `03_Research_Design/`.
- [ ] Specify Research Questions RQ1 through RQ7 with formal hypotheses.
- [ ] Design dataset schema in `04_Dataset/annotation_schema.json`.
- [ ] Draft comprehensive annotation guidelines in `04_Dataset/annotation_guidelines.md`.
- [ ] Establish annotation and adjudication protocol in `05_Annotation/`.

### Stage 3: Dataset Acquisition & Annotation (Steps 10–16)
- [ ] Identify ethically and legally permissible Bengali fact-checking data sources (Rumor Scanner, FactWatch, Boom BD, verified archives).
- [ ] Implement data collection and normalization pipeline in `src/data/`.
- [ ] Collect verified claim records with metadata and evidence URLs.
- [ ] Run automated quality checks: deduplication, Unicode normalization, language filtering.
- [ ] Conduct pilot annotation and compute inter-annotator agreement (Cohen's Kappa).
- [ ] Refine guidelines and finalize annotated benchmark dataset.

### Stage 4: Benchmark Splits & Adversarial Suite (Steps 17, 23)
- [ ] Partition dataset into Splits A (Random), B (Cross-Domain), C (Cross-Source), and D (Temporal).
- [ ] Implement perturbation suite in `src/robustness/`: Typo, Transliteration, Banglish, Code-Mixing, Paraphrase, Adversarial Wording.
- [ ] Generate Split E (Adversarial test sets) with semantic preservation verification.

### Stage 5: Baseline Implementations & Experiments (Steps 18–27)
- [ ] Implement classical ML baselines (TF-IDF + Naive Bayes, Linear SVM, Logistic Regression, Random Forest).
- [ ] Implement multilingual transformer baselines (`xlm-roberta-base`, `bert-base-multilingual-cased`).
- [ ] Implement Bengali-specific pretrained models (`sagorsarker/bangla-bert-base`, `csebuetnlp/banglabert`).
- [ ] Implement controlled zero-shot and few-shot LLM baselines.
- [ ] Implement Retrieval-Augmented Verification (BM25 + Dense Retrieval + Reranking).
- [ ] Run experimental grid across all splits and record traceable outputs in `08_Experiments/results/`.

### Stage 6: Evaluation, Analysis & Reproducibility (Steps 28–36)
- [ ] Calculate classification, calibration (ECE, Brier Score), and retrieval metrics (MRR, Recall@k).
- [ ] Conduct hypothesis testing (McNemar's test, bootstrap 95% CIs).
- [ ] Perform systematic error taxonomy and diagnostic analysis.
- [ ] Conduct explanation faithfulness analysis (rationales, sufficiency, comprehensiveness).
- [ ] Generate publication-quality figures and tables in `11_Visualizations/`.
- [ ] Write complete academic research paper in `12_Paper/`.
- [ ] Create Model Cards, Dataset Card, Reproducibility Package, and Thesis Defense Q&A in `15_Final/`.
