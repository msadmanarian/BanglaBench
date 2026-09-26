# 4. Methodology and Experimental Architecture

### 4.1 Benchmark Evaluation Partitions
To overcome the limitations of standard random splitting, we construct five distinct evaluation splits:

1. **Split A (Random Stratified Baseline)**:
   - Claims are randomly partitioned preserving class distributions: Train (N=42, 70%), Validation (N=6, 10%), Test (N=12, 20%). Serves as the control setting.
2. **Split B (Cross-Domain Generalization)**:
   - Models are trained on four domains (`politics`, `health`, `finance`, `disaster`; N=40) and evaluated on two unseen held-out domains (`sci_tech`, `social`; N=10). Tests zero-shot topical transferability.
3. **Split C (Cross-Source Generalization)**:
   - Models are trained on four primary newsrooms/fact-checkers (`rumor_scanner`, `factwatch`, `prothom_alo`, `health_line_bd`; N=41) and evaluated on disjoint held-out sources (`boombd`, `bangladesh_bank`, `dgdf`, `social_media_facebook`; N=19). Isolates source-specific lexical shortcut exploitation.
4. **Split D (Temporal Shift)**:
   - Chronological cutoff at January 1, 2024. Models are trained on historical past claims (2020–2023; N=25) and tested on future emerging claims (2024–2026; N=35). Evaluates resilience to concept drift and knowledge decay.
5. **Split E (Adversarial Robustness Suite)**:
   - Models trained on Split A are evaluated on 72 controlled linguistic transformations (12 per perturbation category):
     - **Typo**: Keyboard adjacent substitution.
     - **Unicode Variation**: Non-normalized character encoding shifts.
     - **Banglish**: Bengali phonetics rendered in Latin characters.
     - **Code-Mixing**: English-Bengali bilingual lexical insertions.
     - **Paraphrase**: Lexical synonym replacements preserving semantics.
     - **Adversarial Framing**: Insertion of authority-framing distractor phrases.

### 4.2 Baseline Model Implementations
We benchmark multiple foundational model families:
- **Multinomial Naive Bayes (NB)**: Generative baseline using word and character n-gram TF-IDF representations.
- **Linear Support Vector Machine (Linear SVM)**: Maximum-margin linear classifier with L2 regularization and softmax-calibrated decision margins.
- **Logistic Regression (LR)**: Multinomial logistic regression with L2 penalty.
- **Random Forest (RF)**: Ensemble of 100 decision trees over TF-IDF feature vectors.

### 4.3 Modular Retrieval-Augmented Verification (RAG)
We develop an open, modular RAG verification pipeline:
1. **Indexation**: Curated factual evidence documents are indexed using native **Okapi BM25** ($k_1=1.5, b=0.75$).
2. **Query Normalization**: Incoming claims are normalized and tokenized.
3. **Evidence Ranking**: The top-$k$ ($k=3$) most relevant passages are retrieved.
4. **Verification Inference**: Claim-evidence alignment is computed via lexical jaccard overlap and semantic polarity scoring, outputting an adjudicated label, confidence score, and structured evidence citations.

### 4.4 Evaluation Metrics
- **Classification**: Macro-averaged F1, Weighted F1, Accuracy, and per-class Precision/Recall.
- **Uncertainty Calibration**: Expected Calibration Error (ECE; 10 bins) and Brier Score.
- **Hypothesis Testing**: Paired McNemar's test with Edwards' continuity correction and 1,000-iteration non-parametric bootstrap 95% confidence intervals.
- **Explanation Faithfulness**: ERASER benchmark criteria (DeYoung et al., 2020) measuring Sufficiency, Comprehensiveness, and Rationale Retention Rate.
