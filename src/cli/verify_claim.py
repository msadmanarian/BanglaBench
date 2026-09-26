#!/usr/bin/env python3
"""
BanglaFactBench Interactive Claim Verification CLI
Allows researchers and fact-checkers to input arbitrary Bengali claims
and receive instant evidence retrieval, classification, calibrated confidence,
and explanation rationales.
"""

import os
import sys
import json
import argparse

sys.stdout.reconfigure(encoding='utf-8')

# Add src directories
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(base_dir, 'src', 'data'))
sys.path.append(os.path.join(base_dir, 'src', 'models'))
sys.path.append(os.path.join(base_dir, 'src', 'retrieval'))
sys.path.append(os.path.join(base_dir, 'src', 'robustness'))

from normalizer import BengaliTextNormalizer
from bm25_retriever import BM25Retriever
from rag_verifier import RAGVerificationSystem
from perturbation_engine import BengaliPerturbationEngine

def load_default_corpus():
    corpus_path = os.path.join(base_dir, '04_Dataset', 'annotated', 'claims_annotated.json')
    if os.path.exists(corpus_path):
        with open(corpus_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def main():
    parser = argparse.ArgumentParser(description="BanglaFactBench Interactive CLI Verifier")
    parser.add_argument("--claim", type=str, help="Bengali claim text to verify")
    parser.add_argument("--top_k", type=int, default=3, help="Number of evidence passages to retrieve")
    parser.add_argument("--json", action="store_true", help="Output verification result as raw JSON")
    parser.add_argument("--stress_test", action="store_true", help="Run real-time adversarial perturbation stress test on the input claim")
    args = parser.parse_args()

    if not args.claim:
        print("BanglaFactBench Interactive Claim Verification System (v1.0.2)")
        print("Usage: python src/cli/verify_claim.py --claim \"<Bengali Claim Text>\"")
        print("\nExample:")
        print("  python src/cli/verify_claim.py --claim \"পেঁপে পাতার রস খেলে ডেঙ্গু ভালো হয়\" --stress_test")
        sys.exit(0)

    # 1. Normalization
    raw_claim = args.claim
    norm_claim = BengaliTextNormalizer.normalize_text(raw_claim)

    # 2. Initialize RAG system
    corpus = load_default_corpus()
    verifier = RAGVerificationSystem(top_k=args.top_k, seed=42)
    verifier.fit(corpus)

    # 3. Verify Claim
    res = verifier.verify_claim(norm_claim)

    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return

    # Formatted Terminal Output
    print("\n" + "="*65)
    print("      BANGLAFACTBENCH CLAIM VERIFICATION REPORT (CLI)")
    print("="*65)
    print(f"Original Input  : {raw_claim}")
    print(f"Normalized Text : {norm_claim}")
    print(f"\nVerdict Label   : [{res['label']}]")
    print(f"Confidence Score: {res['confidence'] * 100:.1f}%")
    print(f"Retrieval Status: {res.get('retrieval_status', 'SUCCESS')}")
    print(f"Retrieved Passages: {len(res.get('evidence', []))}")
    
    print("\n--- Corroborating Evidence Passages ---")
    if res.get('evidence'):
        for i, ev in enumerate(res['evidence'], 1):
            print(f"[{i}] BM25 Score: {ev.get('bm25_score', 0.0):.2f} | Source: {ev.get('source', 'Curated Archive')}")
            print(f"    Excerpt: {ev['relevant_text']}")
            if ev.get('url'):
                print(f"    Citation URL: {ev['url']}")
    else:
        print("  No matching evidence passages found in verified knowledge base.")

    # 4. Stress Test (if requested)
    if args.stress_test:
        print("\n--- Real-Time Adversarial Robustness Stress Test ---")
        p_engine = BengaliPerturbationEngine(seed=42)
        perturbations = p_engine.generate_all_perturbations(norm_claim)
        print(f"Evaluating {len(perturbations)} controlled linguistic variations:")
        for p in perturbations:
            p_res = verifier.verify_claim(p["transformed_claim_text"])
            status = "STABLE" if p_res["label"] == res["label"] else "FLIPPED"
            print(f"  [{p['transformation_type']:<24}] {status:<7} -> New Label: {p_res['label']:<12} (Conf: {p_res['confidence']*100:.1f}%)")
            print(f"    Text: {p['transformed_claim_text'][:55]}...")

    print("="*65 + "\n")

if __name__ == '__main__':
    main()
