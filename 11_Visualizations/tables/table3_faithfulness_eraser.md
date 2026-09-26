# Table 3: Explanation Faithfulness Diagnostics (ERASER Benchmark Protocol)
# Measures: Sufficiency, Comprehensiveness, and Prediction Retention Rate

| Model Architecture | Mean Sufficiency ($P(y|\hat{X}) - P(y|X)$) | Mean Comprehensiveness ($P(y|X) - P(y|X \setminus \hat{X})$) | Rationale Retention Rate (%) | Empirical Faithfulness Category |
|:---|:---:|:---:|:---:|:---:|
| **Linear SVM** | -0.0186 | -0.0075 | 50.0% | `LOW_FAITHFUL_SHORTCUT` |
| **Logistic Regression** | -0.0138 | -0.0052 | 100.0% | `LOW_FAITHFUL_SHORTCUT` |
| **Naive Bayes** | -0.0379 | -0.0074 | 91.7% | `LOW_FAITHFUL_SHORTCUT` |

*Theoretical Interpretation:*
- **Sufficiency**: Measures if the extracted rationale alone is sufficient to retain the model's prediction confidence. A value near zero indicates that the extracted rationale retains the original prediction probability.
- **Comprehensiveness**: Measures if removing the extracted rationale collapses the model's prediction confidence. Positive values indicate necessary rationales; negative/zero values indicate that the model relies on diffuse background token shortcuts rather than localized, faithful rationales.
- **Retention Rate**: The percentage of test instances where the predicted class remained completely unchanged even after the rationale tokens were deleted from the claim.
