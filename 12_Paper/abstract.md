# Abstract

Misinformation detection in low-resource languages is frequently framed as simple headline classification using random train/test splits. Such setups mask serious failure modes, including domain bias, source-specific lexical memorization, temporal drift, and vulnerability to informal social media variations. 

In this work, we present **BanglaFactBench**, a rigorously documented multi-domain benchmark for claim verification, misinformation detection, and adversarial robustness in Bengali. BanglaFactBench comprises 60 multi-source claims spanning six topical domains (Politics, Public Health, Finance, Disaster Management, Science & Technology, and Social Issues) annotated under a formal 5-class schema (`SUPPORTED`, `REFUTED`, `UNVERIFIABLE`, `MISLEADING`, and `OPINION`). Two independent human annotators established strong inter-annotator agreement (observed agreement $P_o = 93.33\%$, chance agreement $P_e = 24.22\%$, Cohen's $\kappa = 0.9120$).

We design five leakage-controlled evaluation partitions:
1. **Split A (Random Stratified)**: Establishing in-distribution baselines;
2. **Split B (Cross-Domain)**: Evaluating zero-shot transfer across distinct topical domains;
3. **Split C (Cross-Source)**: Evaluating generalization to unseen newsrooms and fact-checking portals;
4. **Split D (Temporal Shift)**: Evaluating performance on post-2023 claims when trained on historical pre-2024 data;
5. **Split E (Adversarial Suite)**: Benchmarking robustness across six controlled linguistic perturbations (typos, Unicode variants, Banglish transliteration, code-mixing, paraphrasing, and adversarial framing).

Our empirical evaluations across classical machine learning baselines and a modular Retrieval-Augmented Generation (RAG) verifier reveal critical vulnerabilities. While Linear SVM achieves a Macro-F1 of 0.3250 on Split A, performance collapses to **0.0667 (-79.5% relative drop)** on out-of-distribution sources (Split C), and drops to **0.2333 (-28.2%)** on unseen domains (Split B). Under adversarial evaluation, Banglish transliteration causes a **-63.8%** collapse in text classifiers. While Okapi BM25 evidence retrieval significantly improves probability calibration (lowering Expected Calibration Error from 0.4217 to **0.1631**), lexical paraphrasing degrades retrieval hit rates by **-53.1%**. 

Finally, diagnostics via the ERASER benchmark demonstrate that linear feature attributions yield negative comprehensiveness ($C \le 0$) with 100% prediction retention under rationale deletion, indicating heavy reliance on diffuse background shortcuts rather than faithful semantic evidence. BanglaFactBench provides an open, fully reproducible foundation for developing trustworthy, robust Bengali fact-checking systems.
