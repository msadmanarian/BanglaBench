# Model Card: BanglaFact RAG Verification System

## 1. Model Details
- **Model Name**: BanglaFact-RAG-BM25
- **Model Version**: v1.0
- **Architecture**: Modular Retrieval-Augmented Generation pipeline consisting of Okapi BM25 retrieval over authoritative Bengali knowledge corpora and factual alignment scoring.
- **Target Language**: Bengali (bn)
- **Training Source**: BanglaFactBench Curated Evidence Corpus
- **License**: MIT License

## 2. Intended Use
- **Primary Intended Use**: Evidence-grounded claim verification providing auditable external citations and well-calibrated confidence scores.
- **Out-of-Scope Use Cases**: Black-box automated decision making without human adjudicator inspection.

## 3. Training & Evaluation Data
- **Corpus**: 42 curated, authoritative evidence passages in Split A; 40 in Split B; 41 in Split C; 25 in Split D.
- **Evaluation Partitions**: All five BanglaFactBench benchmark partitions.
- **Retrieval Engine**: Native Okapi BM25 ($k_1=1.5, b=0.75$, top-$k=3$).

## 4. Performance Metrics (Empirically Observed)
- **Split A (Random Stratified F1)**: 0.2667 (Accuracy: 50.0%)
- **Split B (Cross-Domain F1)**: 0.2455 (Superior cross-domain retention: -7.9% drop)
- **Split C (Cross-Source F1)**: 0.0000 (Requires indexing held-out source portals)
- **Split D (Temporal Shift F1)**: 0.1294 (Requires updating index with post-2023 evidence)
- **Split E (Adversarial Mean Relative Drop)**: -7.0% (Most resilient baseline overall)
- **Expected Calibration Error (ECE)**: **0.1631** (Best calibration across all models)
- **Brier Score**: **0.6787** (Lowest mean squared probability error)

## 5. Strengths & Limitations
- **Strengths**: Provides structured, auditable evidence citations; state-of-the-art probability calibration; strong resilience against Unicode variations and Banglish entities.
- **Known Biases**: Relies strictly on corpus completeness; cannot verify claims absent from the knowledge base.
- **Robustness Limitations**: Severely vulnerable to semantic paraphrasing (-53.1% drop) due to exact lexical matching in BM25.
