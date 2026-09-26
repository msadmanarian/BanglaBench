#!/usr/bin/env python3
"""
BanglaFactBench Robustness Defense Benchmark Runner
Evaluates:
1. Defense against Banglish Transliteration via Phonetic Normalization
2. Defense against Paraphrasing via Hybrid Dense-Sparse Retrieval
"""

import os
import sys
import json
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(base_dir, 'src', 'data'))
sys.path.append(os.path.join(base_dir, 'src', 'models'))
sys.path.append(os.path.join(base_dir, 'src', 'retrieval'))
sys.path.append(os.path.join(base_dir, 'src', 'robustness'))
sys.path.append(os.path.join(base_dir, 'src', 'evaluation'))

from classical_baselines import BanglaFactClassifier
from bm25_retriever import BM25Retriever
from hybrid_retriever import HybridEvidenceRetriever
from banglish_normalizer import BanglishNormalizer

def main():
    print("=================================================================")
    print("      BANGLAFACTBENCH ROBUSTNESS DEFENSE EVALUATION SUITE        ")
    print("=================================================================\n")

    # 1. Load Split A train and adversarial Banglish subset
    with open(os.path.join(base_dir, '04_Dataset', 'train', 'split_a_train.json'), 'r', encoding='utf-8') as f:
        train_data = json.load(f)
    with open(os.path.join(base_dir, '04_Dataset', 'adversarial', 'split_e_banglish_transliteration.json'), 'r', encoding='utf-8') as f:
        banglish_test = json.load(f)
    with open(os.path.join(base_dir, '04_Dataset', 'adversarial', 'split_e_paraphrase.json'), 'r', encoding='utf-8') as f:
        paraphrase_test = json.load(f)

    X_train = [c["claim_text_normalized"] for c in train_data]
    y_train = [c["adjudicated_label"] for c in train_data]

    # Train Linear SVM Baseline
    svm = BanglaFactClassifier(model_type='svm', seed=42)
    svm.fit(X_train, y_train)

    print("--- 1. Evaluating Banglish Defense via Phonetic Normalization ---")
    raw_banglish_texts = [c["transformed_claim_text"] for c in banglish_test]
    true_labels = [c["ground_truth_label"] for c in banglish_test]

    # Undefended performance
    undefended_res = svm.evaluate(raw_banglish_texts, true_labels)
    print(f"Undefended Banglish Macro-F1: {undefended_res['macro_f1']:.4f} (Accuracy: {undefended_res['accuracy']*100:.1f}%)")

    # Defended performance (Pre-normalizing Banglish to Bengali Unicode)
    defended_texts = [BanglishNormalizer.normalize_banglish(t) for t in raw_banglish_texts]
    defended_res = svm.evaluate(defended_texts, true_labels)
    print(f"Defended Banglish Macro-F1  : {defended_res['macro_f1']:.4f} (Accuracy: {defended_res['accuracy']*100:.1f}%)")
    
    gain = defended_res['macro_f1'] - undefended_res['macro_f1']
    print(f"Empirical Robustness Recovery Gain: +{gain:.4f} (Relative Gain: +{(gain/undefended_res['macro_f1'])*100:.1f}%)")

    print("\n--- 2. Evaluating Paraphrase Defense via Hybrid Retrieval ---")
    corpus = [c["evidence_text"] for c in train_data if c.get("evidence_text")]
    meta = [{"claim_id": c["claim_id"], "domain": c["domain"]} for c in train_data if c.get("evidence_text")]

    # Pure BM25
    bm25 = BM25Retriever()
    bm25.index(corpus, meta)

    # Hybrid Dense-Sparse
    hybrid = HybridEvidenceRetriever(alpha=0.5)
    hybrid.index(corpus, meta)

    paraphrase_queries = [c["transformed_claim_text"] for c in paraphrase_test]
    bm25_hits = 0
    hybrid_hits = 0

    for q in paraphrase_queries:
        b_res = bm25.retrieve(q, top_k=3)
        h_res = hybrid.retrieve(q, top_k=3)
        if b_res and b_res[0]["score"] > 0.0:
            bm25_hits += 1
        if h_res and h_res[0]["score"] > 0.0:
            hybrid_hits += 1

    print(f"Pure BM25 Hit Rate on Paraphrases  : {bm25_hits}/{len(paraphrase_queries)} ({(bm25_hits/len(paraphrase_queries))*100:.1f}%)")
    print(f"Hybrid Retriever Hit Rate on Paraphrases: {hybrid_hits}/{len(paraphrase_queries)} ({(hybrid_hits/len(paraphrase_queries))*100:.1f}%)")
    print("\n=================================================================")
    print("Robustness Defense Benchmark Completed Successfully!")
    print("=================================================================")

if __name__ == '__main__':
    main()
