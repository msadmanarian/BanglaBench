#!/usr/bin/env python3
"""
BanglaFactBench Transformer Training Runner
Allows training and evaluation of BanglaBERT, XLM-RoBERTa, and MuRIL.
"""

import os
import sys
import json
import argparse

sys.stdout.reconfigure(encoding='utf-8')
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(base_dir, 'src', 'models'))

from transformer_classifier import TransformerClaimClassifier

def main():
    parser = argparse.ArgumentParser(description="BanglaFactBench Transformer Trainer")
    parser.add_argument("--model", type=str, default="banglabert", choices=["banglabert", "xlm_roberta", "muril"], help="Model key")
    parser.add_argument("--split", type=str, default="split_a", help="Split name (split_a, split_b, split_c, split_d)")
    parser.add_argument("--epochs", type=int, default=3, help="Training epochs")
    parser.add_argument("--lr", type=float, default=2e-5, help="Learning rate")
    args = parser.parse_args()

    print(f"=== BanglaFactBench Transformer Pipeline: {args.model.upper()} ===")
    classifier = TransformerClaimClassifier(model_key=args.model, epochs=args.epochs, lr=args.lr)

    train_path = os.path.join(base_dir, '04_Dataset', 'train', f"{args.split}_train.json")
    if not os.path.exists(train_path):
        train_path = os.path.join(base_dir, '04_Dataset', 'temporal', 'split_d_train_past.json')

    with open(train_path, 'r', encoding='utf-8') as f:
        train_data = json.load(f)

    X_train = [c["claim_text_normalized"] for c in train_data]
    y_train = [c["adjudicated_label"] for c in train_data]

    print(f"Loaded {len(X_train)} training instances from {train_path}")
    res = classifier.train(X_train, y_train)
    print("Training Pipeline Result:", json.dumps(res, indent=2))

if __name__ == '__main__':
    main()
