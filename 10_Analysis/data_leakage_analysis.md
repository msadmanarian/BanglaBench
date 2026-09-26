# Data Leakage & Benchmark Contamination Analysis
# Project: BanglaFactBench

This report details the automated data leakage and split contamination checks performed across all benchmark partitions using `ClaimDeduplicator`.

---

## 1. Split Leakage Audit Summary

| Split Setting | Training Size | Testing Size | Partitioning Strategy | Exact Overlaps Detected | Near-Duplicates Detected ($J > 0.80$) | Contamination Status |
|---|:---:|:---:|---|:---:|:---:|:---:|
| **Split A (Random)** | 42 | 12 | Stratified across domains & labels | **0** | **0** | **CLEAN / ZERO LEAKAGE** |
| **Split B (Cross-Domain)** | 40 | 10 | Domain-disjoint (Train: Health, Pol, Fin, Soc; Test: Disaster, Sci-Tech) | **0** | **0** | **CLEAN / ZERO LEAKAGE** |
| **Split C (Cross-Source)** | 41 | 19 | Source-disjoint (Train: Social, Press; Test: News Portal) | **0** | **0** | **CLEAN / ZERO LEAKAGE** |
| **Split D (Temporal)** | 25 | 35 | Chronological cut-off: 2023-07-01 | **0** | **0** | **CLEAN / ZERO LEAKAGE** |
| **Split E (Adversarial)** | N/A (Trained on Clean) | 72 | Controlled semantics-preserving perturbations | **0** | **0** | **CONTROLLED BEHAVIORAL SUITE** |

---

## 2. Contamination Prevention Verification

1. **Exact Claim Leakage**: Evaluated via canonical NFC Unicode text matching. Result: **0 exact overlaps** across all training and test split pairs.
2. **Near-Duplicate Overlap**: Evaluated via character 3-gram and word-level Jaccard similarity ($J \ge 0.80$). Result: **0 near-duplicate pairs** detected between train and test splits.
3. **Cross-Source Leakage**: In Split C, all test claims originate exclusively from formal news portal reporting (`news_portal`), with zero presence of `news_portal` in the training partition.
4. **Temporal Contamination**: In Split D, all training claims possess `publication_date` strictly before `2023-07-01`, and all evaluation claims possess `publication_date` on or after `2023-07-01`.
