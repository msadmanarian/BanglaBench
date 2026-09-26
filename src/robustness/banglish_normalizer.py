"""
BanglaFactBench Phonetic Banglish-to-Bengali Normalization Engine
Converts Latin-script Bengali ("Banglish") back into standard Bengali Unicode
to defend NLP classifiers against out-of-vocabulary transliteration collapse.
"""

import re
from typing import Dict, List

class BanglishNormalizer:
    """
    Rule-based and lexicon-backed phonetic reverser for Banglish text.
    Handles vowel digraphs, aspirated consonants, and common social media shorthand.
    """

    # Common Banglish word substitutions for high-frequency terms
    LEXICON_MAP = {
        "dengue": "ডেঙ্গু",
        "pepe": "পেঁপে",
        "patar": "পাতার",
        "rosh": "রস",
        "khele": "খেলে",
        "bhalo": "ভালো",
        "hoy": "হয়",
        "hobe": "হবে",
        "shob": "সব",
        "shorkar": "সরকার",
        "taka": "টাকা",
        "bank": "ব্যাংক",
        "shashtho": "স্বাস্থ্য",
        "odhidoptor": "অধিদপ্তর",
        "dabi": "দাবি",
        "bhua": "ভুয়া",
        "mittha": "মিথ্যা",
        "shotti": "সত্যি",
        "shompurno": "সম্পূর্ণ",
        "padma": "পদ্মা",
        "bridge": "সেতু",
        "setu": "সেতু",
        "nirman": "নির্মাণ",
        "khobor": "খবর",
        "desh": "দেশ",
        "manush": "মানুষ",
        "nirdeshona": "নির্দেশনা"
    }

    # Digraph and multi-character phonetic replacements
    PHONETIC_RULES = [
        (r'kkh', 'ক্ষ'),
        (r'chh', 'ছ'),
        (r'sh', 'শ'),
        (r'kh', 'খ'),
        (r'gh', 'ঘ'),
        (r'ch', 'চ'),
        (r'jh', 'ঝ'),
        (r'th', 'থ'),
        (r'dh', 'ধ'),
        (r'ph', 'ফ'),
        (r'bh', 'ভ'),
        (r'ng', 'ং'),
        (r'ou', 'ঔ'),
        (r'oi', 'ঐ'),
        (r'aa', 'া'),
        (r'ee', 'ী'),
        (r'oo', 'ূ'),
        (r'a', 'া'),
        (r'i', 'ি'),
        (r'u', 'ু'),
        (r'e', 'ে'),
        (r'o', 'ো'),
        (r'k', 'ক'),
        (r'g', 'গ'),
        (r't', 'ত'),
        (r'd', 'দ'),
        (r'p', 'প'),
        (r'f', 'ফ'),
        (r'b', 'ব'),
        (r'm', 'ম'),
        (r'j', 'জ'),
        (r'r', 'র'),
        (r'l', 'ল'),
        (r's', 'স'),
        (r'h', 'হ'),
        (r'y', 'য়'),
        (r'z', 'জ')
    ]

    @classmethod
    def normalize_banglish(cls, text: str) -> str:
        """
        Normalizes a Banglish input string into Bengali Unicode.
        """
        if not text:
            return ""

        words = text.split()
        normalized_words = []

        for w in words:
            clean_w = re.sub(r'[^\w\s]', '', w.lower())
            # 1. Exact lexicon lookup
            if clean_w in cls.LEXICON_MAP:
                normalized_words.append(cls.LEXICON_MAP[clean_w])
                continue

            # 2. Rule-based transliteration fallback
            transformed = clean_w
            for pattern, repl in cls.PHONETIC_RULES:
                transformed = re.sub(pattern, repl, transformed)
            
            # Post-cleanup: ensure vowel signs at word starts become independent vowels
            if transformed.startswith('া'):
                transformed = 'আ' + transformed[1:]
            elif transformed.startswith('ি'):
                transformed = 'ই' + transformed[1:]
            elif transformed.startswith('ু'):
                transformed = 'উ' + transformed[1:]
            elif transformed.startswith('ে'):
                transformed = 'এ' + transformed[1:]
            elif transformed.startswith('ো'):
                transformed = 'ও' + transformed[1:]

            normalized_words.append(transformed)

        return " ".join(normalized_words)
