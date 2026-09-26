# Changelog: BanglaFactBench

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [v1.0.4] - 2026-09-26

### Added
- **Phonetic Banglish Normalization Defense (`src/robustness/banglish_normalizer.py`)**: Rule-based and lexicon-backed transliteration reverser mapping Latin-script Banglish into canonical Bengali Unicode script.
- **Dense-Sparse Hybrid Retriever (`src/retrieval/hybrid_retriever.py`)**: Interpolates sparse BM25 with character n-gram cosine similarity to bridge vocabulary gaps under paraphrased adversarial claims.
- **Empirical Defense Benchmark Suite (`scripts/run_defense_benchmarks.py`)**: Demonstrates a **+126.8% relative performance recovery** (Macro-F1 rising from 0.1176 to 0.2667) when defending classifiers against Banglish transliteration attacks.

---

## [v1.0.3] - 2026-09-26

### Added
- **Transformer Fine-Tuning Pipeline (`src/models/transformer_classifier.py`, `scripts/train_transformer.py`)**: Complete training harness for state-of-the-art Bengali and multilingual transformer architectures (`csebuetnlp/banglabert`, `xlm-roberta-base`, `google/muril-base-cased`).
- **Controlled LLM Evaluator (`src/models/llm_evaluator.py`)**: Zero-shot and few-shot prompt templates for LLM verification producing structured, auditable JSON verdicts without hidden chain-of-thought.
- **YAML Experiment Configurations (`configs/`)**: Added production configurations for BanglaBERT, XLM-RoBERTa, MuRIL, and LLM few-shot verification.

---

## [v1.0.2] - 2026-09-26

### Added
- **Interactive CLI Verifier (`src/cli/verify_claim.py`)**: Real-time terminal tool for automated claim normalization, evidence retrieval, calibrated confidence estimation, and live adversarial robustness stress testing.
- **Automated Test Suite (`tests/`, `scripts/run_tests.py`)**: 11 unit tests covering Unicode normalization, Dari harmonization, ZWJ handling, BM25 indexing, adversarial perturbation generators, ECE/Brier metrics, and split leakage verification.
- **Multimodal Extension Specification (`04_Dataset/multimodal_schema.json`)**: Formal schema for future multimodal meme, digital poster, and reverse-image fact verification.
- **Enhanced Normalizer & Retriever APIs**: Added `normalize_text` classmethod and empty query guardrails.

---

## [v1.0.1] - 2026-09-26

### Added
- **Complete Research Package**: 60 multi-domain curated Bengali claims with dual independent human annotations ($\kappa = 0.9120$) across 6 domains and 5 taxonomic classes.
- **Five Benchmark Splits**: Split A (Random), Split B (Cross-Domain), Split C (Cross-Source), Split D (Temporal Shift), and Split E (72 Adversarial variants).
- **Baselines & RAG Verifier**: Classical ML baselines (Naive Bayes, Linear SVM, Logistic Regression, Random Forest) and Okapi BM25 retrieval-augmented verifier.
- **Publication Figures & Paper**: 5 high-resolution figures in `11_Visualizations/figures/` and full academic paper in `12_Paper/paper.md`.
- **Quality Audit Suite**: Automated validation script `scripts/quality_check.py` with 100% test pass rate.

