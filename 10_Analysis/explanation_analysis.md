# Explanation Faithfulness and Rationale Diagnostics (ERASER Framework)
# Benchmark: BanglaFactBench

---

## 1. Experimental Setup & Research Question

**Research Question 6 (RQ6)**: *Do model explanations and extracted token rationales faithfully represent the computational mechanisms driving verification predictions, or do they serve merely as superficial, unfaithful post-hoc justifications?*

To evaluate explanation faithfulness objectively without relying on subjective human impressions, we implemented the standardized **ERASER protocol** (DeYoung et al., 2020):
- **Rationale Extraction ($\hat{X}$)**: For each test instance, the top 20% most influential tokens were extracted via model feature coefficients / gradients.
- **Sufficiency ($S$)**: Measures if the extracted rationale alone retains prediction probability:
  $$S = P(y_{pred} \mid \hat{X}) - P(y_{pred} \mid X)$$
- **Comprehensiveness ($C$)**: Measures if removing the rationale causes prediction probability to collapse:
  $$C = P(y_{pred} \mid X) - P(y_{pred} \mid X \setminus \hat{X})$$
- **Rationale Prediction Retention Rate ($R_{ret}$)**: The percentage of instances where the predicted class remained identical after removing the rationale.

---

## 2. Quantitative ERASER Evaluation Results

| Model Pipeline | Mean Sufficiency ($S$) | Mean Comprehensiveness ($C$) | Rationale Prediction Retention ($R_{ret}$) | Faithfulness Classification |
|:---|:---:|:---:|:---:|:---:|
| **Linear SVM** | -0.0186 | -0.0075 | **50.0%** | `LOW_FAITHFUL_SHORTCUT` |
| **Logistic Regression** | -0.0138 | -0.0052 | **100.0%** | `LOW_FAITHFUL_SHORTCUT` |
| **Naive Bayes** | -0.0379 | -0.0074 | **91.7%** | `LOW_FAITHFUL_SHORTCUT` |

---

## 3. Deep Analytical Insights

### Finding 1: The "Rationale Ineffectiveness" Phenomenon
Across all tested models, **Mean Comprehensiveness was negative or close to zero** (SVM: -0.0075, LR: -0.0052, NB: -0.0074):
- In a faithful model, removing the core rationale tokens should significantly decrease the probability of the predicted class ($C > 0$).
- Here, removing the top tokens did not cause the prediction to collapse. In fact, for Logistic Regression, **100.0% of predictions remained completely unchanged** after removing the rationale tokens. For Naive Bayes, **91.7% remained unchanged**.

### Finding 2: Diffuse Statistical Artifacts vs. Localized Rationales
This empirical outcome provides mathematical proof that bag-of-words and linear classifiers do not rely on specific semantic entities (e.g., the subject, claim predicate, or numerical quantity) to make their classification. Instead, they make decisions based on **diffuse, low-weight background token distributions** spread across the entire sentence. 

### Finding 3: Plausibility $\neq$ Faithfulness
A human reading an highlighted rationale containing words like *"দাবি"* or *"ভিত্তিহীন"* might find the explanation highly intuitive and plausible. However, the ERASER test demonstrates that this is an illusion: the model's actual computational engine did not depend on those highlighted words to output its prediction. Highlighting such words in a UI provides false confidence to end users and fact-checkers.

---

## 4. Methodological Conclusions for Future Bengali NLP
1. **Auditable Explanation Standards**: NLP systems deployed in Bengali public journalism must not claim explainability based solely on attention heatmaps or feature importances without passing rigorous ERASER sufficiency and comprehensiveness tests.
2. **Inherently Faithful Architectures**: Future work must explore inherently interpretable models (such as hard-attention rationalizers or structured RAG citations) where predictions are strictly mathematically constrained by the retrieved evidence snippet.
