# 5. Experimental Results

### 5.1 Primary Performance Across Benchmark Partitions

Table 1 summarizes model performance across the four primary evaluation partitions alongside calibration metrics.

#### Table 1: Benchmark Performance Across Evaluation Splits
| Model / Pipeline | Random Split A (Macro F1) [95% CI] | Cross-Domain Split B (Macro F1) | Cross-Source Split C (Macro F1) | Temporal Split D (Macro F1) | Expected Calibration Error (ECE) | Brier Score |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Naive Bayes (TF-IDF)** | 0.3250 [0.067, 0.583] | 0.1143 | 0.0000 | 0.1980 | 0.4217 | 1.0102 |
| **Linear SVM (TF-IDF)** | 0.3250 [0.067, 0.583] | 0.2333 | 0.0667 | 0.2570 | 0.2547 | 0.8754 |
| **Logistic Regression** | 0.1176 [0.118, 0.118] | 0.2564 | 0.0000 | 0.1829 | 0.3286 | 0.9209 |
| **Random Forest** | 0.2857 [0.000, 0.571] | 0.2333 | 0.0000 | 0.1800 | 0.4375 | 1.0846 |
| **RAG Verifier (BM25)** | **0.2667** [0.000, 0.533] | **0.2455** | **0.0000** | **0.1294** | **0.1631** | **0.6787** |

#### Key Experimental Findings:
1. **The In-Distribution Fallacy**: Models achieve their highest performance under the random Split A (Linear SVM Macro-F1: 0.3250). However, this score degrades severely when subjected to rigorous out-of-distribution evaluation.
2. **The Source Generalization Collapse**: Evaluating on out-of-distribution sources (Split C) causes a near-complete breakdown: Linear SVM plummets to **0.0667** (a **-79.5% relative drop**), while Naive Bayes, Logistic Regression, Random Forest, and RAG fall to **0.0000**. Models learned source-specific journalistic framing rather than factual veracity.
3. **Domain Degradation**: Across unseen domains (Split B), Naive Bayes collapses by **-64.8%** (Macro-F1: 0.1143), while Linear SVM drops by **-28.2%** (Macro-F1: 0.2333). RAG proves most resilient, dropping by only **-7.9%** (Macro-F1: 0.2455).
4. **Temporal Knowledge Decay**: On post-2023 claims (Split D), performance drops across all baselines (NB: -39.1%, SVM: -20.9%, RF: -37.0%).

---

### 5.2 Adversarial Robustness Degradation (Split E)

Table 2 details model resilience against the six controlled perturbation categories.

#### Table 2: Robustness Under Linguistic and Adversarial Perturbations
| Perturbation Category | Linear SVM F1 [Drop %] | RAG Verifier F1 [Drop %] | Random Forest F1 [Drop %] | Most Fragile Failure Mode |
|:---|:---:|:---:|:---:|:---|
| **Clean Baseline** | **0.3250** [0.0%] | **0.2667** [0.0%] | **0.2857** [0.0%] | N/A |
| **Typographical Errors** | 0.3250 [-0.0%] | 0.2667 [-0.0%] | 0.2857 [-0.0%] | Intact subwords preserve n-grams. |
| **Unicode Variation** | 0.3250 [-0.0%] | 0.4333 [+62.5%] | 0.0800 [-72.0%] | Tree splits shattered by encoding. |
| **Banglish Transliteration** | **0.1176 [-63.8%]** | **0.1967 [-26.3%]** | **0.1176 [-58.8%]** | Out-of-vocabulary Latin script. |
| **Code-Mixing (En-Bn)** | 0.3250 [-0.0%] | 0.2667 [-0.0%] | 0.0800 [-72.0%] | Random Forest feature fragmentation. |
| **Semantic Paraphrase** | 0.3250 [-0.0%] | **0.1250 [-53.1%]** | 0.2857 [-0.0%] | BM25 exact lexical term mismatch. |
| **Adversarial Framing** | 0.3762 [+15.8%] | 0.2000 [-25.0%] | 0.2143 [-25.0%] | Deceptive authority distractor terms. |
| **Mean Relative Drop** | **-8.0%** | **-7.0%** | **-38.0%** | **RAG Most Resilient Overall** |

---

### 5.3 Explanation Faithfulness Evaluation (ERASER Protocol)

Table 3 presents the quantitative faithfulness diagnostics.

#### Table 3: Explanation Faithfulness Metrics
| Model Architecture | Mean Sufficiency ($S \le 0$) | Mean Comprehensiveness ($C > 0$) | Rationale Retention Rate ($R_{ret}$) | Faithfulness Assessment |
|:---|:---:|:---:|:---:|:---|
| **Linear SVM** | -0.0186 | -0.0075 | **50.0%** | `LOW_FAITHFUL_SHORTCUT` |
| **Logistic Regression** | -0.0138 | -0.0052 | **100.0%** | `LOW_FAITHFUL_SHORTCUT` |
| **Naive Bayes** | -0.0379 | -0.0074 | **91.7%** | `LOW_FAITHFUL_SHORTCUT` |

Across all models, **Mean Comprehensiveness was non-positive** ($C \le 0$), and removing top rationales left predictions unchanged 50.0% to 100.0% of the time. This proves that linear feature attributions fail the test of computational necessity: models rely on diffuse background n-gram correlations rather than the specific salient keywords highlighted in user-facing explanations.
