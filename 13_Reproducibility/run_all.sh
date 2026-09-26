#!/usr/bin/env bash
# BanglaFactBench Master Reproduction Script
# Executes end-to-end data validation, benchmark evaluation, and visualization

set -e

echo "=== [1/5] Computing Inter-Annotator Agreement ==="
python scripts/compute_agreement.py

echo "=== [2/5] Generating Dataset Statistics ==="
python scripts/compute_dataset_statistics.py

echo "=== [3/5] Generating Benchmark Splits & Adversarial Suite ==="
python scripts/generate_all_splits.py

echo "=== [4/5] Executing Benchmark Experiments across All Splits ==="
python scripts/run_all_experiments.py

echo "=== [5/5] Generating Publication-Quality Figures ==="
python scripts/generate_figures.py

echo "=== All BanglaFactBench Reproduction Steps Completed Successfully! ==="
