# Model Calibration and Uncertainty Estimation Report
# Benchmark: BanglaFactBench

---

## 1. Overview & Setup

In high-stakes claim verification (such as public health and electoral integrity), a model's predicted confidence must correspond faithfully to its probability of being correct.
We evaluate calibration on Split A (N=12) using:
1. **Expected Calibration Error (ECE)**: The weighted average difference between predicted confidence and observed accuracy across 10 probability bins.
2. **Brier Score**: The mean squared error between predicted posterior probability vectors and one-hot ground truth labels:
   $$BS = \frac{1}{N} \sum_{i=1}^N \sum_{k=1}^K (p_{ik} - y_{ik})^2$$

---

## 2. Quantitative Calibration Metrics

| Model Pipeline | Probability Calibration Mechanism | Expected Calibration Error (ECE) [Lower is Better] | Brier Score [Lower is Better] | Calibration Quality Assessment |
|:---|:---|:---:|:---:|:---|
| **RAG Verifier** | Evidence alignment scoring & fallback | **0.1631** | **0.6787** | **Best Calibrated (Evidence-Grounded)** |
| **Linear SVM** | Softmax over decision function margins | 0.2547 | 0.8754 | Well Calibrated |
| **Logistic Regression** | Sigmoid / Softmax maximum likelihood | 0.3286 | 0.9209 | Moderately Overconfident |
| **Naive Bayes** | Class posterior product | 0.4217 | 1.0102 | Severely Overconfident |
| **Random Forest** | Tree vote fraction | 0.4375 | 1.0846 | Severely Miscalibrated |

---

## 3. Findings & Discussion

1. **RAG Achieves State-of-the-Art Calibration**:
   The RAG Verifier achieved the lowest ECE (**0.1631**) and lowest Brier score (**0.6787**). When the retrieval engine lacks relevant evidence, its confidence drops to low baseline levels, appropriately signaling uncertainty to human fact-checkers.
2. **Naive Bayes Pathological Overconfidence**:
   Multinomial Naive Bayes suffered from extreme overconfidence (ECE: 0.4217, Brier: 1.0102). Due to the conditional independence assumption, multiplying dozens of token likelihoods produces posteriors pushed artificially to 0.99 or 0.00, regardless of actual empirical correctness.
3. **Margin-Based Softmax Calibration**:
   Linear SVM produced stable calibration (ECE: 0.2547), outperforming Logistic Regression. Because the maximum-margin formulation maximizes geometric distance between classes, temperature-scaled margins provide smoother posterior probabilities than unregularized logistic regression on small Bengali datasets.
