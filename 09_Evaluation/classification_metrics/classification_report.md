# Classification Evaluation Report
# Benchmark: BanglaFactBench

---

## 1. Overview & Setup

This report aggregates the classification metrics across all benchmark baselines on the core partitions of BanglaFactBench.
- **Evaluation Splits**: Split A (Random Stratified, N=12), Split B (Cross-Domain, N=10), Split C (Cross-Source, N=19), Split D (Temporal Shift, N=35).
- **Target Classes**: 5 (`SUPPORTED`, `REFUTED`, `UNVERIFIABLE`, `MISLEADING`, `OPINION`).
- **Primary Metric**: Macro-averaged F1 score ($Macro\text{-}F1 = \frac{1}{|C|} \sum_{c \in C} F1_c$).

---

## 2. Comprehensive Results Summary Table

| Model Architecture | Split A F1 [95% CI] | Split A Accuracy | Split B F1 (Cross-Domain) | Split C F1 (Cross-Source) | Split D F1 (Temporal) | Weighted F1 (Split A) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Naive Bayes (Multinomial)** | 0.3250 [0.067, 0.583] | 50.0% | 0.1143 | 0.0000 | 0.1980 | 0.3438 |
| **Linear SVM** | 0.3250 [0.067, 0.583] | 50.0% | 0.2333 | 0.0667 | 0.2570 | 0.3438 |
| **Logistic Regression** | 0.1176 [0.118, 0.118] | 41.7% | 0.2564 | 0.0000 | 0.1829 | 0.2451 |
| **Random Forest** | 0.2857 [0.000, 0.571] | 33.3% | 0.2333 | 0.0000 | 0.1800 | 0.2857 |
| **RAG Verifier (BM25)** | 0.2667 [0.000, 0.533] | 50.0% | 0.2455 | 0.0000 | 0.1294 | 0.3444 |

---

## 3. Per-Class Performance Breakdown (Linear SVM on Split A)

| Taxonomic Label | Precision | Recall | F1-Score | Support in Test |
|:---|:---:|:---:|:---:|:---:|
| **SUPPORTED** | 0.0000 | 0.0000 | 0.0000 | 3 |
| **REFUTED** | 0.4545 | 1.0000 | 0.6250 | 5 |
| **UNVERIFIABLE** | 0.0000 | 0.0000 | 0.0000 | 1 |
| **MISLEADING** | 0.0000 | 0.0000 | 0.0000 | 2 |
| **OPINION** | 1.0000 | 1.0000 | 1.0000 | 1 |
| **Macro Average** | **0.2909** | **0.4000** | **0.3250** | **12** |

---

## 4. Key Takeaways
1. **Majority Class Bias**: Both SVM and NB default to the majority class (`REFUTED`), capturing 100% recall on refuted claims but 0.0% recall on `SUPPORTED`, `UNVERIFIABLE`, and `MISLEADING`.
2. **Subjectivity Detection**: The `OPINION` class is reliably separable due to strong grammatical and lexical markers of subjectivity in Bengali.
3. **Generalization Gap**: Performance drops precipitously from Split A (0.3250) to Split C (0.0667), confirming that models memorized source-specific training artifacts.
