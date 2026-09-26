# Table 2: Adversarial Robustness Degradation Matrix (Split E)
# Values: Macro-F1 (Percentage Relative Drop from Clean Baseline in parentheses)

| Model Pipeline | Clean F1 | Typo Perturbation | Bengali Unicode Variation | Banglish Transliteration | Code-Mixing (Bengali-English) | Paraphrase Substitution | Adversarial Wording | Mean Relative Drop |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Linear SVM** | 0.3250 | 0.3250 (-0.0%) | 0.3250 (-0.0%) | 0.1176 (-63.8%) | 0.3250 (-0.0%) | 0.3250 (-0.0%) | 0.3762 (+15.8%) | **-8.0%** |
| **Naive Bayes** | 0.3250 | 0.3250 (-0.0%) | 0.3250 (-0.0%) | 0.1176 (-63.8%) | 0.1176 (-63.8%) | 0.3250 (-0.0%) | 0.1176 (-63.8%) | **-42.6%** |
| **Logistic Regression**| 0.1176 | 0.1176 (-0.0%) | 0.1176 (-0.0%) | 0.1176 (-0.0%) | 0.1176 (-0.0%) | 0.1176 (-0.0%) | 0.1176 (-0.0%) | **0.0% (Floor)** |
| **Random Forest** | 0.2857 | 0.2857 (-0.0%) | 0.0800 (-72.0%) | 0.1176 (-58.8%) | 0.0800 (-72.0%) | 0.2857 (-0.0%) | 0.2143 (-25.0%) | **-38.0%** |
| **RAG Verifier** | 0.2667 | 0.2667 (-0.0%) | 0.4333 (+62.5%) | 0.1967 (-26.3%) | 0.2667 (-0.0%) | 0.1250 (-53.1%) | 0.2000 (-25.0%) | **-7.0%** |

*Note: Relative drop is calculated as $(F1_{clean} - F1_{perturbed}) / F1_{clean} \times 100\%$. Positive values denote performance improvement due to favorable token shifts, negative values denote degradation.*
