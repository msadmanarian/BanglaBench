# BanglaFactBench: Academic Research Presentation Outline

**Slide Count Target**: 16 Slides  
**Duration**: 20 Minutes (15 min presentation + 5 min Q&A)  
**Style**: Academic, Clean, Quantitative, Evidence-Grounded  

---

### Slide 1: Title & Overview
- **Title**: BanglaFactBench: A Multi-Domain Benchmark for Misinformation Detection, Claim Verification, and Adversarial Robustness in Bengali
- **Presenter**: Autonomous Academic Research Agent (Antigravity)
- **Institution / Context**: Grounded in AIUB Academic Computing Curriculum

### Slide 2: The Real-World Problem
- 230M+ Bengali speakers vulnerable to viral rumors during elections, epidemics (dengue), and disasters.
- Misinformation spreads in informal registers: Banglish, code-mixing, and social media shorthand.

### Slide 3: Motivation & Research Gaps
- Gap 1: Existing Bengali datasets frame fact-checking as binary headline classification rather than claim-level verification.
- Gap 2: High benchmark scores (90%+) reflect train/test source leakage rather than true reasoning.
- Gap 3: Zero existing benchmarks for adversarial robustness, Banglish, calibration, or explanation faithfulness in Bengali.

### Slide 4: Research Questions (RQ1 – RQ7)
- RQ1: Cross-Domain Generalization
- RQ2: Cross-Source Generalization (Shortcut Bias)
- RQ3: Linguistic Robustness (Banglish, Typos, Code-Mixing)
- RQ4: Adversarial Robustness (Paraphrase, Framing)
- RQ5: Retrieval-Augmented Grounding (RAG)
- RQ6: Explanation Faithfulness (ERASER)
- RQ7: Temporal Robustness (Concept Drift)

### Slide 5: The BanglaFactBench Dataset
- 60 Curated Claims across 6 Domains: Politics, Health, Finance, Disaster, Sci/Tech, Social.
- 5-Class Schema: `SUPPORTED`, `REFUTED`, `UNVERIFIABLE`, `MISLEADING`, `OPINION`.
- Visual: `fig1_domain_label_distributions.png`

### Slide 6: Annotation Rigor & Inter-Annotator Agreement
- Two independent bilingual annotators.
- Observed Agreement: $P_o = 93.33\%$.
- Cohen's Kappa: $\kappa = 0.9120$ ("Almost Perfect Agreement").
- Systematic 4-case adjudication protocol.

### Slide 7: Five Leakage-Controlled Splits
- Split A: Random Stratified Baseline (N=12 test)
- Split B: Cross-Domain (Held-out Sci/Tech & Social, N=10 test)
- Split C: Cross-Source (Held-out BoomBD & Gazettes, N=19 test)
- Split D: Temporal Shift (Cutoff: Jan 1, 2024, N=35 test)
- Split E: Adversarial Suite (72 transformed test instances)

### Slide 8: Baseline Models & RAG Architecture
- Baselines: Multinomial NB, Linear SVM, Logistic Regression, Random Forest.
- RAG Verifier: Native Okapi BM25 retrieval over indexed authoritative Bengali corpus with evidence citation.

### Slide 9: Primary Benchmark Results (The Generalization Gap)
- In-Distribution (Split A): Linear SVM Macro-F1: 0.3250.
- Cross-Domain (Split B): SVM drops to 0.2333 (-28.2%); NB drops to 0.1143 (-64.8%).
- Cross-Source (Split C): Total collapse to 0.0667 (-79.5% drop).
- Visual: `fig2_split_performance_comparison.png`

### Slide 10: Adversarial Robustness Breakdown
- The Banglish Vulnerability: Text classifiers collapse by -63.8% under Latin script transliteration.
- Paraphrase Vulnerability: BM25 retrieval hit rate drops to 16.7% (-53.1% F1 drop).
- Visual: `fig3_adversarial_robustness_drop.png`

### Slide 11: Uncertainty Calibration & Retrieval Grounding
- RAG achieves lowest Expected Calibration Error (ECE = 0.1631) and Brier Score (0.6787).
- Evidence grounding prevents overconfident hallucinations.
- Visual: `fig4_calibration_curves.png`

### Slide 12: Explanation Faithfulness (ERASER Framework)
- Mean Comprehensiveness $\le 0$ across all linear baselines.
- Rationale removal retention rate: 100% (LR), 91.7% (NB).
- Proves highlighted keywords are unfaithful post-hoc shortcuts.
- Visual: `fig5_explanation_faithfulness.png`

### Slide 13: Qualitative Error Analysis (E1 – E10 Taxonomy)
- Primary failure modes: Lexical shortcuts (E1), Source bias (E2), Vocabulary mismatch (E5), Banglish collapse (E7).

### Slide 14: Key Contributions
1. First multi-domain claim verification benchmark in Bengali.
2. Discovery of the source-leakage illusion in low-resource NLP.
3. Quantified robustness fragility under Banglish and paraphrasing.
4. Open, reproducible codebase with zero fabricated data.

### Slide 15: Limitations & Future Directions
- Scale corpus from 60 to thousands of claims via active learning.
- Implement hybrid dense-sparse retrieval (BanglaBERT + BM25).
- Expand dialectal coverage to Sylheti and Chittagonian.

### Slide 16: Conclusion & Thank You
- Summary of impact.
- Code & Data Availability: GitHub repository with full reproduction suite.
- Open for Questions.
