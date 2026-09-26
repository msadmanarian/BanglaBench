import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src', 'data'))
from normalizer import BengaliTextNormalizer

def test_unicode_nfc_normalization():
    # Bengali character with combining vowel sign
    raw_text = "বাংলাদেশ"
    normalized = BengaliTextNormalizer.normalize_text(raw_text)
    assert normalized == "বাংলাদেশ"
    assert len(normalized) > 0

def test_dari_punctuation_harmonization():
    text_with_pipe = "এটি একটি মিথ্যা দাবি | এটি সম্পূর্ণ ভিত্তিহীন ||"
    normalized = BengaliTextNormalizer.normalize_text(text_with_pipe)
    assert "।" in normalized
    assert "|" not in normalized

def test_whitespace_and_cleanup():
    messy_text = "  পদ্মা   সেতু    নির্মাণ   \nব্যয়  "
    normalized = BengaliTextNormalizer.normalize_text(messy_text)
    assert normalized == "পদ্মা সেতু নির্মাণ ব্যয়"

def test_zero_width_joiner_handling():
    # Handles ZWJ/ZWNJ gracefully
    raw_zwj = "যুক্ত\u200Dবর্ণ"
    normalized = BengaliTextNormalizer.normalize_text(raw_zwj)
    assert len(normalized) > 0
