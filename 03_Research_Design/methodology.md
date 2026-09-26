# Research Methodology & Experimental Blueprint
# Project: BanglaFactBench

---

## 1. Methodological Overview

The BanglaFactBench research methodology is structured as a closed-loop empirical pipeline adhering to AIUB Outcome-Based Education standards (`CSC 4232`, `MAT 3103`, `EE`).

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. Data Collection & Curation                               │
│    - Certified Fact-Check Archives (Rumor Scanner, FactWatch)│
│    - Mainstream Bengali Portals (Prothom Alo, Daily Star Bn) │
│    - Metadata extraction (date, domain, source, evidence)   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Data Cleaning & Normalization                            │
│    - Unicode NFC normalization & Bengali script filtering   │
│    - Deduplication & Near-duplicate removal via SimHash     │
│    - Atomic claim extraction & schema validation            │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Human Annotation & Quality Assurance                      │
│    - 5-class schema: SUPPORTED, REFUTED, UNVERIFIABLE,      │
│      MISLEADING, OPINION                                    │
│    - Independent dual annotation on core evaluation subset  │
│    - Cohen's Kappa calculation & expert adjudication        │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Leakage-Controlled Partitioning                           │
│    - Split A: Random Stratified Split                       │
│    - Split B: Cross-Domain Disjoint Split                   │
│    - Split C: Cross-Source Disjoint Split                   │
│    - Split D: Temporal Chronological Split                  │
│    - Split E: Adversarial Perturbation Suite                │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Multi-Family Model Benchmarking                           │
│    - Classical ML (TF-IDF + Naive Bayes, Linear SVM, RF)    │
│    - Multilingual Transformers (mBERT, XLM-RoBERTa)         │
│    - Native Pretrained Bengali Models (BanglaBERT)          │
│    - Controlled LLM Baselines (Zero-Shot, Few-Shot)         │
│    - Retrieval-Augmented Verification (BM25 + DPR + Verifier)│
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Rigorous Evaluation, Calibration & Error Analysis         │
│    - Macro-F1, Precision, Recall, Confusion Matrices        │
│    - Bootstrap 95% Confidence Intervals & McNemar's Tests   │
│    - Expected Calibration Error (ECE) & Reliability Plots   │
│    - Explanation Faithfulness (Sufficiency, Comprehensiveness│
│    - 10-category diagnostic error taxonomy                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Experimental Execution Framework

1. **Deterministic Reproducibility**: Fixed random seeds (e.g., `seed = 42, 123, 999`) across all model runs; reporting mean and standard deviations for non-deterministic operations.
2. **Traceability**: Every output log records the full configuration dictionary, software library versions, hardware specifications, and input dataset hash.
3. **Automated Quality Checks (`quality_check.py`)**: Pre-execution and post-execution checks verify that no split contamination, missing labels, corrupted characters, or invalid dates exist.
