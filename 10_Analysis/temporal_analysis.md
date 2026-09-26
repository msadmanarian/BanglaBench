# Temporal Generalization and Concept Drift Analysis (Split D)
# Benchmark: BanglaFactBench

---

## 1. Experimental Setup & Research Question

**Research Question 7 (RQ7)**: *How does temporal distribution shift affect the reliability of Bengali claim verification when models trained on past historical claims encounter emerging claims with evolving factual realities?*

To investigate temporal degradation without future lookahead:
- **Temporal Cutoff**: January 1, 2024.
- **Training Set (Past: 2020 – 2023, N=25)**: Claims concerning earlier COVID-19 protocols, historical events, 2022 flood disasters, and initial infrastructure phases.
- **Test Set (Future: 2024 – 2026, N=35)**: Emerging claims concerning recent political transitions, 2024 economic inflation, generative AI deepfakes, and recent dengue strains.
- **Temporal Leakage**: Strict chronologically disjoint partitioning.

---

## 2. Benchmark Performance Across Temporal Horizon

| Model Pipeline | In-Distribution Clean F1 (Split A) | Future Test Set F1 (Split D) | Absolute Change ($\Delta F1$) | Relative Performance Degradation |
|:---|:---:|:---:|:---:|:---:|
| **Naive Bayes** | 0.3250 | 0.1980 | -0.1270 | **-39.1%** |
| **Linear SVM** | 0.3250 | 0.2570 | -0.0680 | **-20.9%** |
| **Logistic Regression** | 0.1176 | 0.1829 | +0.0653 | *+55.5% (Class Redistribution)* |
| **Random Forest** | 0.2857 | 0.1800 | -0.1057 | **-37.0%** |
| **RAG Verifier** | 0.2667 | 0.1294 | -0.1373 | **-51.5%** |

---

## 3. Key Findings on Temporal Dynamics

### 1. Factual Knowledge Decay (Concept Drift)
Models trained exclusively on pre-2024 data experienced significant performance degradation:
- Naive Bayes dropped by **-39.1%**.
- Random Forest dropped by **-37.0%**.
- Linear SVM dropped by **-20.9%**.

The primary driver is **vocabulary drift and entity evolution**:
- New political entities, institutional leadership changes, and policy terminology emerged post-2023 that had zero representation in the 2020–2023 training corpora.
- Static classifiers cannot adjust to facts whose truth value evolves over time (e.g., project completion dates, foreign currency reserves, statutory interest rates).

### 2. Temporal Knowledge Gap in RAG Systems
The RAG Verifier experienced a **-51.5% drop** (Macro-F1 fell to 0.1294) when its knowledge base was restricted to past evidence documents:
- Because the RAG system lacked indexed evidence from 2024–2026, claims about recent events returned either empty or completely irrelevant past documents.
- When an RAG system retrieves temporally mismatched evidence, it hallucinates or misaligns context, falsely categorizing emerging true events as `UNVERIFIABLE` or `REFUTED`.

---

## 4. Recommendations for Production Verification Systems
1. **Dynamic Knowledge Updating**: Fact-checking indices must be continuously refreshed via live crawler APIs from verified newsfeeds and government gazettes.
2. **Timestamp-Aware Retrieval**: Retrieval models must condition queries on document publication dates and claim occurrence dates to prevent historical contamination of current claims.
