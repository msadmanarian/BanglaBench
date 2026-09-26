import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src', 'robustness'))
from perturbation_engine import BengaliPerturbationEngine

def test_all_six_perturbations_generated():
    engine = BengaliPerturbationEngine(seed=42)
    claim = "পদ্মা সেতুর নির্মাণ ব্যয় সম্পূর্ণ নিজস্ব অর্থায়নে বহন করা হয়েছে।"
    perturbations = engine.generate_all_perturbations(claim)

    types_generated = {p["transformation_type"] for p in perturbations}
    expected_types = {
        "typo",
        "unicode_variation",
        "banglish_transliteration",
        "code_mixing",
        "paraphrase",
        "adversarial_wording"
    }
    assert types_generated == expected_types
    for p in perturbations:
        assert len(p["transformed_claim_text"]) > 0
        assert p["original_claim_text"] == claim
