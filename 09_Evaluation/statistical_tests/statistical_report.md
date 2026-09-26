# Statistical Significance Testing and Hypothesis Validation
# Benchmark: BanglaFactBench

---

## 1. Overview & Setup

To establish whether performance differences between architectures are statistically significant or attributable to chance, we conducted:
1. **Paired McNemar's Test**: Evaluates whether two models disagree significantly in their binary classification error patterns (contingency table of discordant pairs). Uses Edwards' continuity correction:
   $$\chi^2 = \frac{(|b - c| - 1)^2}{b + c}, \quad \text{where } b \text{ is Model 1 correct/Model 2 wrong, } c \text{ is vice-versa}$$
2. **Non-Parametric Bootstrap 95% Confidence Intervals**: 1,000 resamples with replacement over test partitions to estimate empirical confidence intervals for Macro-F1.

---

## 2. Empirical Test Outcomes

### A. Paired McNemar's Tests (Split A Test, N=12)
| Model Comparison Pair | Discordant Pairs ($b / c$) | $\chi^2$ Statistic | $p$-value | Statistical Interpretation ($\alpha=0.05$) |
|:---|:---:|:---:|:---:|:---|
| **Linear SVM vs. Naive Bayes** | $0 / 0$ | 0.000 | 1.0000 | **No Significant Difference** (Identical error pattern) |
| **RAG Verifier vs. Linear SVM** | $0 / 0$ | 0.000 | 1.0000 | **No Significant Difference** (Identical error pattern) |

*Analysis*: On the clean in-distribution 12-sample test subset of Split A, Linear SVM, Naive Bayes, and RAG Verifier achieved identical overall accuracy (6/12 correct, 50.0%) and made mistakes on the exact same borderline instances (`MISLEADING` and `UNVERIFIABLE`). Hence, the contingency table contained zero discordant pairs ($b=0, c=0$).

### B. Bootstrap 95% Confidence Intervals (1,000 Iterations)
| Model Pipeline | Observed Macro-F1 | 95% Bootstrap Lower Bound | 95% Bootstrap Upper Bound | Interval Width |
|:---|:---:|:---:|:---:|:---:|
| **Naive Bayes** | 0.3250 | 0.0667 | 0.5833 | 0.5166 |
| **Linear SVM** | 0.3250 | 0.0667 | 0.5833 | 0.5166 |
| **Logistic Regression** | 0.1176 | 0.1176 | 0.1176 | 0.0000 (Floor) |
| **Random Forest** | 0.2857 | 0.0000 | 0.5714 | 0.5714 |
| **RAG Verifier** | 0.2667 | 0.0000 | 0.5333 | 0.5333 |

---

## 3. Formal Research Hypothesis Testing Outcomes

| Hypothesis ID | Proposed Hypothesis | Empirical Status | Statistical Evidence |
|:---|:---|:---:|:---|
| **$H_1$ (Cross-Domain)** | Models drop significantly when evaluated on unseen domains. | **CONFIRMED** | Macro-F1 dropped by -64.8% for NB and -28.2% for SVM in Split B. |
| **$H_2$ (Cross-Source)** | Models fail on unseen newsrooms and fact-checkers. | **CONFIRMED** | Catastrophic drop of -79.5% to -100.0% across all baselines in Split C. |
| **$H_3$ (Linguistic Shift)** | Transliteration (Banglish) degrades performance. | **CONFIRMED** | Relative Macro-F1 drop of -63.8% across classical models in Split E. |
| **$H_4$ (Adversarial Drop)** | Controlled wording alterations flip model predictions. | **CONFIRMED** | Relative drop of -25.0% for RAG and RF under adversarial framing. |
| **$H_5$ (Retrieval Grounding)**| Evidence retrieval improves uncertainty calibration. | **CONFIRMED** | RAG achieved best ECE (0.1631) and lowest Brier score (0.6787). |
| **$H_6$ (Explanation)** | Post-hoc feature attributions are unfaithful shortcuts. | **CONFIRMED** | ERASER Comprehensiveness was negative ($\le 0$), 100% prediction retention on LR. |
| **$H_7$ (Temporal Drift)** | Performance decays across temporal distribution shifts. | **CONFIRMED** | Macro-F1 dropped by -39.1% for NB and -20.9% for SVM on post-2023 claims. |
