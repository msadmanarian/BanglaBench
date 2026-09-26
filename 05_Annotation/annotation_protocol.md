# Human Annotation & Adjudication Protocol
# Project: BanglaFactBench

---

## 1. Overview of Protocol

To guarantee scientific rigor, repeatability, and high inter-annotator agreement, the annotation process follows a structured four-stage protocol:

```text
[Stage 1: Annotator Training & Calibration (Pilot Batch of 50 Claims)]
                               │
                               ▼
[Stage 2: Independent Dual Annotation of Core Evaluation Benchmark]
                               │
                               ▼
[Stage 3: Statistical Agreement Calculation (Cohen's Kappa κ)]
                               │
                               ▼
[Stage 4: Expert Adjudication & Consensus Resolution]
```

---

## 2. Annotator Qualifications & Training

1. **Language Proficiency**: All annotators must be native Bengali speakers with fluent academic comprehension of English (for assessing cross-lingual and code-mixed evidence).
2. **Academic Background**: Minimum undergraduate-level education in Computer Science, Linguistics, Journalism, or Social Sciences.
3. **Training Phase**: Each annotator completes a mandatory 2-hour orientation on `04_Dataset/annotation_guidelines.md` and independently annotates a pilot batch of 50 calibration claims. Discrepancies during the pilot phase are discussed in detail to establish unified boundary standards.

---

## 3. Independent Dual Annotation

1. Annotators receive claims in randomized, anonymized order through standardized JSON interface files.
2. Annotators do NOT communicate or discuss specific claims during the active annotation window.
3. For each claim, the annotator must record:
   - `assigned_label`: Chosen from the 5 classes.
   - `confidence`: Confidence score in the decision (0.50 to 1.00).
   - `annotation_notes`: Concise explanation of the rationale.
   - `retrieved_evidence`: Verified URLs or textual excerpts consulted.

---

## 4. Agreement Measurement Protocol

Following AIUB MAT 3103 inferential statistics procedures, inter-annotator agreement is computed using **Cohen's Kappa ($\kappa$)**:

$$\kappa = \frac{P_o - P_e}{1 - P_e}$$

Where:
- $P_o = \frac{1}{N} \sum_{i=1}^N \mathbb{I}(y_{1,i} == y_{2,i})$ is the observed proportion of agreement.
- $P_e = \sum_{c \in \mathcal{C}} P(y_1 = c) \cdot P(y_2 = c)$ is the expected agreement by chance under empirical marginal distributions.

### Operational Thresholds:
- $\kappa \ge 0.70$: High agreement. Proceed to adjudication of discrepancies.
- $0.55 \le \kappa < 0.70$: Moderate agreement. Conduct targeted guideline refinement on ambiguous classes before adjudication.
- $\kappa < 0.55$: Low agreement. Halt process, revise guidelines, retrain annotators, and re-annotate.

*Strict Scientific Integrity Rule: Kappa is calculated solely on completed human annotations; synthetic or estimated kappa values are never reported as verified findings.*
