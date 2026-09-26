# BanglaFactBench Experimental Benchmark Summary
# Generated on: 2026-09-26 18:49:02

---

## 1. Primary Benchmark Results Across All Evaluation Splits

| Model / Pipeline | Random Split A (Macro F1) | Cross-Domain Split B (Macro F1) | Cross-Source Split C (Macro F1) | Temporal Split D (Macro F1) | Expected Calibration Error (ECE) | Brier Score |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Naive Bayes (TF-IDF)** | 0.3250 | 0.1143 | 0.0000 | 0.1980 | 0.4217 | 1.0102 |
| **Linear SVM (TF-IDF)** | 0.3250 | 0.2333 | 0.0667 | 0.2570 | 0.2547 | 0.8754 |
| **Logistic Regression** | 0.1176 | 0.2564 | 0.0000 | 0.1829 | 0.3286 | 0.9209 |
| **Random Forest** | 0.2857 | 0.2333 | 0.0000 | 0.1800 | 0.4375 | 1.0846 |
| **RAG Verifier (BM25 + Evidence)** | **0.2667** | **0.2455** | **0.0000** | **0.1294** | **0.1631** | **0.6787** |

---

## 2. Adversarial Robustness Degradation Matrix (Split E)

Values denote Macro-F1 on each perturbation subset (parentheses indicate relative drop from clean F1):

| Model | Clean | Typo | Unicode Var | Banglish | Code-Mixing | Paraphrase | Adv Wording | Average Robustness Drop |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Linear SVM** | 0.3250 | 0.3250 (-0.0%) | 0.3250 (-0.0%) | 0.1176 (-63.82%) | 0.3250 (-0.0%) | 0.3250 (-0.0%) | 0.3762 (--15.75%) | -8.0% |
| **RAG Verifier** | 0.2667 | 0.2667 (-0.01%) | 0.4333 (--62.48%) | 0.1967 (-26.26%) | 0.2667 (-0.01%) | 0.1250 (-53.13%) | 0.2000 (-25.01%) | -7.0% |

---

## 3. Explanation Faithfulness Diagnostics (ERASER Protocol)

| Model | Mean Sufficiency (Lower is Better) | Mean Comprehensiveness (Higher is Better) | Rationale Prediction Retention | Faithfulness Classification |
|---|:---:|:---:|:---:|:---:|
| **Linear SVM** | -0.0186 | -0.0075 | 50.0% | `LOW_FAITHFUL_SHORTCUT` |
| **Logistic Regression** | -0.0138 | -0.0052 | 100.0% | `LOW_FAITHFUL_SHORTCUT` |
| **Naive Bayes** | -0.0379 | -0.0074 | 91.7% | `LOW_FAITHFUL_SHORTCUT` |
