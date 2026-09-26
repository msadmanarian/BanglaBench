# Inter-Annotator Agreement Report
# Project: BanglaFactBench

This report documents the empirical inter-annotator agreement statistics computed across the dual-annotated core benchmark of 60 claims. All values are calculated programmatically from verified human annotations.

---

## 1. Agreement Summary Statistics

| Metric | Measured Value | Standard Interpretation (Landis & Koch, 1977) |
|---|---|---|
| **Total Evaluated Claims ($N$)** | 60 | Core gold-standard benchmark |
| **Observed Proportional Agreement ($P_o$)** | **0.9333** (93.33%) | High raw consensus across annotators |
| **Expected Chance Agreement ($P_e$)** | **0.2422** (24.22%) | Marginal distribution baseline |
| **Cohen's Kappa ($\\kappa$)** | **0.9120** | **Substantial Agreement** ($\\kappa \\in [0.61, 0.80]$ to $0.81+$) |

---

## 2. Annotator Contingency Matrix

Rows represent **Annotator 1**; Columns represent **Annotator 2**:

| Annotator 1 \\ Annotator 2 | SUPPORTED | REFUTED | UNVERIFIABLE | MISLEADING | OPINION | Row Total |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **SUPPORTED** | 13 | 0 | 0 | 0 | 0 | **13** |
| **REFUTED** | 0 | 20 | 0 | 1 | 0 | **21** |
| **UNVERIFIABLE** | 0 | 0 | 8 | 0 | 0 | **8** |
| **MISLEADING** | 0 | 3 | 0 | 4 | 0 | **7** |
| **OPINION** | 0 | 0 | 0 | 0 | 11 | **11** |
| **Col Total** | **13** | **23** | **8** | **5** | **11** | **60** |

---

## 3. Discrepancy Breakdown & Adjudication

Of the 60 claims:
- **Full Agreement**: 56 claims (93.3%) received identical labels.
- **Disagreements**: 4 claims required expert adjudication under `05_Annotation/adjudication_protocol.md`.
- Primary disagreement boundary occurred between `MISLEADING` and `REFUTED` (e.g., claims containing authentic baseline statistics but misleading conclusions or exaggerated health claims like amla and bitter gourd).
