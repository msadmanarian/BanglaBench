# Machine Learning Foundations & Pipeline
## Context Derived from AIUB CSC 4232 (Machine Learning)

This document formalizes the machine learning principles drawn from the AIUB CSC 4232 course materials (`G:\AIUB\26 - 2 - Semester 9\ML`) and establishes how they are operationalized in the BanglaFactBench project.

---

## 1. End-to-End ML Pipeline Architecture

As formalized in AIUB lecture slide `ML 06 ML FLOW.pptx`, a defensible machine learning research project must follow a systematic 7-stage workflow:

```text
[1. Problem Formulation & Task Definition]
                      │
                      ▼
        [2. Data Acquisition & Curation]
                      │
                      ▼
   [3. Exploratory Data Analysis & Quality Control]
                      │
                      ▼
    [4. Text Preprocessing & Feature Extraction]
                      │
                      ▼
[5. Leakage-Controlled Data Partitioning (Splits A-E)]
                      │
                      ▼
  [6. Model Selection, Training & Fine-Tuning]
                      │
                      ▼
  [7. Evaluation, Significance Testing & Error Analysis]
```

---

## 2. Evaluation Metrics Protocol

Misinformation detection and fact verification datasets frequently suffer from class imbalance (e.g., true vs. false claims do not appear with equal frequency across social platforms). Following the AIUB course module `ML 05 Ensemble Learning, Performance Measures 2.pptx`, the evaluation protocol enforces the following mathematical measures:

### 2.1 Multi-Class Confusion Matrix Definitions
For each class $c \in \mathcal{C}$ where $\mathcal{C} = \{\text{SUPPORTED}, \text{REFUTED}, \text{UNVERIFIABLE}, \text{MISLEADING}, \text{OPINION}\}$:
- $\text{TP}_c$: True Positives for class $c$
- $\text{FP}_c$: False Positives (predicted as $c$ but ground truth was $\neq c$)
- $\text{FN}_c$: False Negatives (ground truth was $c$ but predicted $\neq c$)
- $\text{TN}_c$: True Negatives (ground truth $\neq c$ and predicted $\neq c$)

### 2.2 Per-Class and Averaged Metrics
$$\text{Precision}_c = \frac{\text{TP}_c}{\text{TP}_c + \text{FP}_c}, \quad \text{Recall}_c = \frac{\text{TP}_c}{\text{TP}_c + \text{FN}_c}$$

$$\text{F1}_c = 2 \cdot \frac{\text{Precision}_c \cdot \text{Recall}_c}{\text{Precision}_c + \text{Recall}_c}$$

**Macro-F1 (Primary Metric):**
$$\text{Macro-F1} = \frac{1}{|\mathcal{C}|} \sum_{c \in \mathcal{C}} \text{F1}_c$$
*Macro-F1 weights all classes equally regardless of class frequencies, preventing a model from achieving an artificially high score by merely exploiting majority-class bias.*

**Weighted-F1 (Secondary Metric):**
$$\text{Weighted-F1} = \sum_{c \in \mathcal{C}} \frac{N_c}{N} \cdot \text{F1}_c$$

---

## 3. Baseline Model Families Grounded in AIUB Syllabi

### 3.1 Classical Baselines (Linear & Non-Linear Classifiers)
- **Multinomial Naive Bayes (`Introduction to Classification - Naive Bayes_Spring_26.ppt`)**:
  Computes posterior probabilities assuming conditional independence:
  $$P(c \mid d) \propto P(c) \prod_{i=1}^{n} P(w_i \mid c)$$
  Uses Laplace smoothing ($\alpha = 1.0$) over TF-IDF n-gram vectors.
- **Linear Support Vector Classifier (`ML 05 Support Vector Machine 1.pptx`)**:
  Solves the convex quadratic optimization problem:
  $$\min_{\mathbf{w}, b, \xi} \frac{1}{2} \|\mathbf{w}\|^2 + C \sum_{i=1}^{N} \xi_i \quad \text{s.t. } y_i (\mathbf{w}^T \mathbf{x}_i + b) \ge 1 - \xi_i, \quad \xi_i \ge 0$$
- **Logistic Regression & Random Forest (`ML 05 Ensemble Learning`)**:
  Ensemble of $B$ bagged decision trees using randomized feature sub-spacing to lower variance without increasing bias.

### 3.2 Transformer Classifiers & Dense Encoders
- Fine-tuned contextual representations via cross-entropy loss:
  $$\mathcal{L} = -\sum_{c \in \mathcal{C}} y_c \log \hat{y}_c$$
- Pretrained multilingual transformers (`xlm-roberta-base`, `bert-base-multilingual-cased`) and Bengali-specific models (`sagorsarker/bangla-bert-base`).
