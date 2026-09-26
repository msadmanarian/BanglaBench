# Formal Hypotheses & Statistical Testing Framework
# Project: BanglaFactBench

---

## 1. Overview of Hypotheses

All experimental investigations in BanglaFactBench test explicitly stated Null ($H_0$) and Alternative ($H_1$) hypotheses using inferential statistical tests grounded in AIUB course MAT 3103 (`G:\AIUB\24 - 3 - Semester 4\Math 6 Mortuza Sir\MAT 3103 Computational Statistics & Probability (FALL_24-25).docx`).

---

## 2. Hypothesis Specifications

### Hypothesis 1: Cross-Domain Generalization (RQ1)
- **$H_{0,1}$**: The Macro-F1 score of a verification model on an unseen domain is statistically indistinguishable from its score on seen domains ($\mu_{\text{in-domain}} - \mu_{\text{cross-domain}} = 0$).
- **$H_{1,1}$**: Out-of-domain evaluation results in a statistically significant degradation ($\mu_{\text{in-domain}} - \mu_{\text{cross-domain}} > 0$).
- **Test**: Paired permutation test and Bootstrap 95% Confidence Intervals on Macro-F1 differences ($p < 0.05$).

### Hypothesis 2: Cross-Source Generalization (RQ2)
- **$H_{0,2}$**: There is no significant difference in verification accuracy between random source splits and source-disjoint splits ($\mu_{\text{random}} - \mu_{\text{cross-source}} = 0$).
- **$H_{1,2}$**: Source-disjoint evaluation significantly degrades model performance ($\mu_{\text{random}} - \mu_{\text{cross-source}} > 0$).
- **Test**: Paired McNemar's test on categorical prediction correctness across test claims ($p < 0.05$).

### Hypothesis 3: Linguistic Robustness to Banglish and Code-Mixing (RQ3)
- **$H_{0,3}$**: Subword tokenizers and multilingual encoders exhibit equal performance on native Bengali script, Romanized Banglish, and English-Bengali code-mixed claims ($\mu_{\text{clean}} = \mu_{\text{banglish}} = \mu_{\text{codemix}}$).
- **$H_{1,3}$**: Romanized Banglish and code-mixing cause significant performance degradation ($\mu_{\text{clean}} > \mu_{\text{banglish}}$ and $\mu_{\text{clean}} > \mu_{\text{codemix}}$).
- **Test**: Repeated measures ANOVA / Friedman test across perturbation subsets with post-hoc pairwise tests.

### Hypothesis 4: Adversarial Semantic Vulnerability (RQ4)
- **$H_{0,4}$**: Meaning-preserving adversarial rewritings do not alter the predicted veracity label of claims ($\text{Flip Rate} = 0$).
- **$H_{1,4}$**: Adversarial rewritings induce significant label flip rates ($\text{Flip Rate} > 25\%$, $p < 0.01$).
- **Test**: Exact Binomial test comparing observed flip rate against chance flip rate.

### Hypothesis 5: Retrieval-Augmented Grounding Advantage (RQ5)
- **$H_{0,5}$**: Retrieval-augmented verification provides no significant improvement in Macro-F1 or Expected Calibration Error (ECE) compared to parametric-only models ($\mu_{\text{RAG}} - \mu_{\text{Parametric}} = 0$).
- **$H_{1,5}$**: RAG verification yields significantly higher Macro-F1 and significantly lower ECE ($p < 0.01$).
- **Test**: Paired McNemar's test for accuracy/F1; bootstrap difference test for ECE.

### Hypothesis 6: Disconnect Between Explanation Plausibility and Faithfulness (RQ6)
- **$H_{0,6}$**: Human plausibility ratings of explanations correlate strongly with quantitative faithfulness metrics ($r_{\text{plausibility, faithfulness}} \approx 1.0$).
- **$H_{1,6}$**: Plausibility ratings do not correlate significantly with quantitative sufficiency and comprehensiveness scores ($r < 0.30$, $p > 0.05$).
- **Test**: Spearman's rank correlation coefficient ($\rho$) between human Likert ratings and ERASER sufficiency/comprehensiveness metrics.

### Hypothesis 7: Temporal Knowledge Degradation (RQ7)
- **$H_{0,7}$**: Model verification performance remains invariant across temporal evaluation splits ($\mu_{\text{past}} - \mu_{\text{future}} = 0$).
- **$H_{1,7}$**: Evaluating on future claims yields statistically significant performance decay ($\mu_{\text{past}} - \mu_{\text{future}} > 0$).
- **Test**: Linear regression trend analysis of monthly Macro-F1 degradation and paired t-test between historical and forward test partitions.
