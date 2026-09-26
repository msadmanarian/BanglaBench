# BanglaFactBench Reproduction Guide

This guide outlines the exact, deterministic steps required to reproduce all findings, figures, splits, and tables reported in the BanglaFactBench research package.

---

## 1. System Requirements & Environment Setup
- **Operating System**: Windows 10/11, Ubuntu 20.04+, or macOS
- **Python Version**: Python 3.10+ (Tested on Python 3.14.2)
- **Virtual Environment**:
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: .\venv\Scripts\activate
  pip install -r requirements.txt
  ```

---

## 2. Step-by-Step Reproduction Pipeline

### Step 1: Verify Inter-Annotator Agreement
To verify the observed agreement ($93.33\%$) and Cohen's kappa ($\kappa = 0.9120$):
```bash
python scripts/compute_agreement.py
```

### Step 2: Generate Programmatic Dataset Statistics
To compute domain, label, source, and temporal distributions:
```bash
python scripts/compute_dataset_statistics.py
```

### Step 3: Generate All Evaluation Splits & Adversarial Suite
To deterministically partition the 60 claims into Splits A, B, C, D and generate the 72 adversarial perturbations in Split E:
```bash
python scripts/generate_all_splits.py
```

### Step 4: Run the Master Benchmark Suite
To execute training and evaluation across all 5 models (NB, SVM, LR, RF, RAG), compute calibration (ECE, Brier), run ERASER explanation faithfulness diagnostics, and calculate paired McNemar's tests:
```bash
python scripts/run_all_experiments.py
```
*Output*: Generates `08_Experiments/results/all_results.json` and `08_Experiments/results/summary_table.md`.

### Step 5: Render Publication Figures
To plot all 5 publication-ready charts in `11_Visualizations/figures/`:
```bash
python scripts/generate_figures.py
```

### Step 6: Automated Quality Assurance
To audit the entire repository for missing files, zero leakage, and valid citations:
```bash
python scripts/quality_check.py
```

---

## 3. Seed Stability
All splits and randomized procedures are fixed with seed `42`. To test variance across random seeds, pass `--seed <int>` to the baseline runners.
