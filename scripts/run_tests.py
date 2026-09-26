import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
sys.path.append(os.path.join(base_dir, 'src', 'data'))
sys.path.append(os.path.join(base_dir, 'src', 'models'))
sys.path.append(os.path.join(base_dir, 'src', 'retrieval'))
sys.path.append(os.path.join(base_dir, 'src', 'robustness'))
sys.path.append(os.path.join(base_dir, 'src', 'evaluation'))

from tests.test_normalizer import (
    test_unicode_nfc_normalization,
    test_dari_punctuation_harmonization,
    test_whitespace_and_cleanup,
    test_zero_width_joiner_handling
)
from tests.test_retriever import (
    test_bm25_index_and_retrieve,
    test_empty_query_handling
)
from tests.test_perturbation import test_all_six_perturbations_generated
from tests.test_metrics import test_ece_computation, test_brier_score_computation
from tests.test_data_integrity import test_annotated_dataset_schema, test_split_leakage_absence

def run_all():
    tests = [
        ("Normalizer: Unicode NFC", test_unicode_nfc_normalization),
        ("Normalizer: Dari Harmonization", test_dari_punctuation_harmonization),
        ("Normalizer: Whitespace Cleanup", test_whitespace_and_cleanup),
        ("Normalizer: ZWJ Handling", test_zero_width_joiner_handling),
        ("Retriever: BM25 Index & Search", test_bm25_index_and_retrieve),
        ("Retriever: Empty Query", test_empty_query_handling),
        ("Perturbation: 6 Transformations", test_all_six_perturbations_generated),
        ("Metrics: ECE Computation", test_ece_computation),
        ("Metrics: Brier Score", test_brier_score_computation),
        ("Integrity: Dataset Schema", test_annotated_dataset_schema),
        ("Integrity: Zero Split Leakage", test_split_leakage_absence),
    ]

    print("=========================================================")
    print("           BANGLAFACTBENCH TEST SUITE EXECUTION           ")
    print("=========================================================\n")

    passed = 0
    failed = 0

    for name, func in tests:
        try:
            func()
            print(f"[PASS] {name}")
            passed += 1
        except Exception as e:
            print(f"[FAIL] {name} -> Error: {e}")
            failed += 1

    print("\n" + "="*57)
    print(f"TEST SUMMARY: {passed} PASSED, {failed} FAILED (TOTAL: {len(tests)})")
    print("="*57)

    if failed > 0:
        sys.exit(1)

if __name__ == '__main__':
    run_all()
