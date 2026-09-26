# Table 1: Primary Benchmark Results Across Evaluation Partitions
# Metrics: Macro-F1, Expected Calibration Error (ECE), and Brier Score

| Model Architecture | Feature Representation | Split A: Random Stratified (Macro F1) [95% CI] | Split B: Cross-Domain (Macro F1) | Split C: Cross-Source (Macro F1) | Split D: Temporal Shift (Macro F1) | Expected Calibration Error (ECE) | Brier Score |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Naive Bayes** | Word + Char n-gram TF-IDF | 0.3250 [0.067, 0.583] | 0.1143 | 0.0000 | 0.1980 | 0.4217 | 1.0102 |
| **Linear SVM** | Word + Char n-gram TF-IDF | 0.3250 [0.067, 0.583] | 0.2333 | 0.0667 | 0.2570 | 0.2547 | 0.8754 |
| **Logistic Regression** | Word + Char n-gram TF-IDF | 0.1176 [0.118, 0.118] | 0.2564 | 0.0000 | 0.1829 | 0.3286 | 0.9209 |
| **Random Forest** | Word + Char n-gram TF-IDF | 0.2857 [0.000, 0.571] | 0.2333 | 0.0000 | 0.1800 | 0.4375 | 1.0846 |
| **RAG Verifier** | BM25 Lexical + Evidence Alignment | **0.2667** [0.000, 0.533] | **0.2455** | **0.0000** | **0.1294** | **0.1631** | **0.6787** |

*Note: All scores are empirically observed from executed benchmarks on BanglaFactBench (seed=42). Zero values represent complete breakdown where the model failed to correctly predict any instances of unseen classes/sources.*
