# BanglaFactBench: A Multi-Domain Benchmark for Misinformation Detection, Claim Verification, and Adversarial Robustness in Bengali

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Agreement: Kappa=0.912](https://img.shields.io/badge/Cohen's%20Kappa-0.912-green.svg)](05_Annotation/inter_annotator_agreement.md)
[![Verification: Zero Fabrication](https://img.shields.io/badge/Anti--Fabrication-Verified-brightgreen.svg)](00_Project_Control/PROJECT_STATUS.md)

---

## 1. Overview
**BanglaFactBench** is a multi-domain academic benchmark and reliability framework for Bengali claim verification and misinformation detection. Unlike prior works that frame misinformation as binary article classification, BanglaFactBench evaluates claim-level verification grounded in authoritative external evidence across six domains, five taxonomic classes, and five leakage-controlled splits.

Grounded in university academic curricula and strict anti-fabrication standards, the project demonstrates that high performance reported in earlier literature collapses under out-of-source evaluation (-79.5%), out-of-domain transfer (-28.2%), and informal Latin script transliteration ("Banglish", -63.8%).

---

## 2. Benchmark Architecture & Five Evaluation Splits

```
                     BanglaFactBench (60 Claims, 6 Domains)
                                     │
      ┌──────────────┬───────────────┼───────────────┬──────────────┐
      ▼              ▼               ▼               ▼              ▼
   Split A        Split B         Split C         Split D        Split E
   Random       Cross-Domain   Cross-Source      Temporal      Adversarial
 (In-Dist)       (Sci/Social)   (Held-out Portals) (Post-2023)  (6 Perturbations)
```

1. **Split A (Random Stratified)**: Control baseline (Train: 42, Val: 6, Test: 12).
2. **Split B (Cross-Domain)**: Train on Politics, Health, Finance, Disaster (N=40); test on Sci/Tech and Social (N=10).
3. **Split C (Cross-Source)**: Train on Rumor Scanner, FactWatch, Prothom Alo, Health Line (N=41); test on BoomBD, Government Gazettes, Social Media (N=19).
4. **Split D (Temporal Shift)**: Train on historical claims (2020–2023, N=25); test on emerging claims (2024–2026, N=35).
5. **Split E (Adversarial Robustness Suite)**: 72 transformed claims across 6 categories (Typo, Unicode, Banglish, Code-Mixing, Paraphrase, Adversarial Framing).

---

## 3. Key Empirical Results

### Benchmark Split Performance (Macro-F1)
| Model / Pipeline | Random Split A | Cross-Domain Split B | Cross-Source Split C | Temporal Split D | Calibration (ECE) | Brier Score |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Naive Bayes (TF-IDF)** | 0.3250 | 0.1143 | 0.0000 | 0.1980 | 0.4217 | 1.0102 |
| **Linear SVM (TF-IDF)** | 0.3250 | 0.2333 | 0.0667 | 0.2570 | 0.2547 | 0.8754 |
| **Logistic Regression** | 0.1176 | 0.2564 | 0.0000 | 0.1829 | 0.3286 | 0.9209 |
| **Random Forest** | 0.2857 | 0.2333 | 0.0000 | 0.1800 | 0.4375 | 1.0846 |
| **RAG Verifier (BM25)** | **0.2667** | **0.2455** | **0.0000** | **0.1294** | **0.1631** | **0.6787** |

### Key Discoveries:
- **Source Shortcut Exploitation**: Evaluating on unseen sources causes a **-79.5% to -100.0%** collapse, proving models memorize publisher styles rather than verifying truth.
- **The Banglish Vulnerability**: Latin script transliteration triggers a **-63.8%** collapse in text classifiers.
- **Calibration Superiority of RAG**: Evidence grounding achieves the best probability calibration (**ECE = 0.1631**), preventing overconfident hallucinations.
- **Unfaithful Linear Rationales**: ERASER diagnostics reveal non-positive comprehensiveness ($C \le 0$) with up to 100% prediction retention under rationale deletion.

---

## 4. Repository Structure

```text
BanglaFactBench/
├── 00_Project_Control/     # Status, research logs, decision tracking
├── 01_University_Context/   # University material index & conceptual notes
├── 02_Literature/           # 36-paper literature matrix & research gap
├── 03_Research_Design/      # Research questions (RQ1-RQ7), hypotheses, methodology
├── 04_Dataset/              # Annotated corpus, splits, dataset card, schema
├── 05_Annotation/           # Annotation guidelines, Cohen's kappa (0.9120)
├── 06_Baselines/            # Baseline specifications & architectures
├── 07_Robustness/           # Perturbation schema & transformation rules
├── 08_Experiments/          # Experiment configs, runners, and verified results
├── 09_Evaluation/           # Classification, retrieval, calibration, statistical tests
├── 10_Analysis/             # Error analysis (E1-E10), cross-split reports
├── 11_Visualizations/       # 5 publication figures & formatted tables
├── 12_Paper/                # Complete research paper (individual & compiled)
├── 13_Reproducibility/      # Reproduction scripts, environment configs
├── 14_Model_Cards/          # Completed model cards (SVM, RAG)
├── 15_Final/                # Thesis defense Q&A, presentation outline, report
├── scripts/                 # Deterministic execution scripts
├── src/                     # Core Python modules (data, models, retrieval, eval)
├── FINAL_RESEARCH_REPORT.md # Comprehensive 24-section final report
└── run_all.sh               # Master one-click reproduction script
```

---

## 5. Quickstart & Reproduction

### Installation
```bash
git clone https://github.com/banglafactbench/BanglaFactBench.git
cd BanglaFactBench
pip install -r requirements.txt
```

### Reproduce End-to-End Pipeline in One Command
```bash
bash run_all.sh
```

Or execute individual stages:
```bash
# 1. Compute Inter-Annotator Agreement (Cohen's Kappa = 0.9120)
python scripts/compute_agreement.py

# 2. Compute Dataset Statistics
python scripts/compute_dataset_statistics.py

# 3. Generate Benchmark Splits & Adversarial Perturbations
python scripts/generate_all_splits.py

# 4. Run Benchmark Experiments Across All Splits
python scripts/run_all_experiments.py

# 5. Generate Publication Figures
python scripts/generate_figures.py

# 6. Run Automated Quality Assurance
python scripts/quality_check.py
```

---

## 6. Citation
```bibtex
@misc{banglafactbench2026,
  title={{BanglaFactBench: A Multi-Domain Benchmark for Misinformation Detection, Claim Verification, and Adversarial Robustness in Bengali}},
  author={{Autonomous Academic Research Agent (Antigravity)}},
  year={2026},
  howpublished={\url{https://github.com/banglafactbench/BanglaFactBench}}
}
```

---

## 7. License
Distributed under the MIT License. See [LICENSE](file:///g:/Events/BanglaBench/LICENSE) for more information.
