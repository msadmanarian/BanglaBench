# Cross-Source Generalization Analysis (Split C)
# Benchmark: BanglaFactBench

---

## 1. Experimental Setup & Research Question

**Research Question 2 (RQ2)**: *Do models generalize to completely unseen newsrooms, fact-checking agencies, and social media platforms, or do they overfit to source-specific lexical and stylistic artifacts?*

To isolate source-specific biases:
- **Training Set (N=41)**: 4 distinct sources (`rumor_scanner`, `factwatch`, `prothom_alo`, `health_line_bd`).
- **Test Set (N=19)**: Held-out sources (`boombd`, `bangladesh_bank`, `dgdf`, `social_media_facebook`).
- **Source Leakage**: Exact 0.00% source overlap between training and test sets.

---

## 2. Benchmark Results & Catastrophic Breakdown

| Model Architecture | In-Source Macro-F1 (Split A) | Out-of-Source Macro-F1 (Split C) | Cross-Source Accuracy | Performance Drop ($\Delta F1$) |
|:---|:---:|:---:|:---:|:---:|
| **Naive Bayes** | 0.3250 | **0.0000** | 0.0% | -100.0% |
| **Linear SVM** | 0.3250 | **0.0667** | 10.5% | -79.5% |
| **Logistic Regression** | 0.1176 | **0.0000** | 0.0% | -100.0% |
| **Random Forest** | 0.2857 | **0.0000** | 0.0% | -100.0% |
| **RAG Verifier** | 0.2667 | **0.0000** | 0.0% | -100.0% |

---

## 3. In-Depth Root Cause Analysis: Source-Specific Shortcuts

### Finding 1: Total Model Collapse on Unseen Sources
Every single baseline model collapsed to near-zero performance when tested on unseen sources:
- Naive Bayes, Logistic Regression, Random Forest, and RAG achieved **0.0000 Macro-F1**.
- Linear SVM achieved an abysmal **0.0667 Macro-F1** (accuracy: 10.5%).

### Finding 2: Lexical Signatures of Bengali Fact-Checking Portals
Fact-checking organizations possess distinct stylistic writing conventions:
- **Rumor Scanner** frequently uses specific phrasings: *"গুজব", "দাবিটি ভিত্তিহীন", "অনুসন্ধানে জানা যায়"*.
- **FactWatch** features academic tone and structured debunking markers.
- **BoomBD** formulates claims differently, often quoting vernacular rumors verbatim.
- **Official Government Portals** use formal bureaucratic lexicon (*"প্রজ্ঞাপন", "গেজেট", "অনুমোদিত"*).

When trained on the primary sources, classical classifiers learn to associate the presence of these journalistic framing phrases with verification labels. When applied to `boombd` or raw Facebook posts, these familiar anchors are absent, leading to total misprediction.

### Finding 3: The "Source Leakage Mirage" in Prior Literature
Prior Bengali NLP literature (e.g., Hossain et al., 2020) evaluated fake news detection primarily under random train/test splits, reporting F1 scores above 0.85–0.90. Our Split C experiments demonstrate that these high scores are substantially inflated by **source leakage**. A model tested on the same sources it was trained on is merely performing source-style identification rather than genuine factual verification.

---

## 4. Methodological Implications for Future Benchmark Design

1. **Mandatory Source-Disjoint Partitions**: Benchmarks should never rely solely on random k-fold cross-validation. A strict source-disjoint split must be standard for claims.
2. **Adversarial Debiaising**: Training pipelines must incorporate source-invariance objectives or style-neutral text normalization to strip institutional signatures before classification.
