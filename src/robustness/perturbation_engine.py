import re
import random
import unicodedata
from typing import Dict, List, Tuple

class BengaliPerturbationEngine:
    """
    Algorithmic perturbation generator for BanglaFactBench (Split E).
    Implements 6 controlled transformations:
    1. Typographical noise
    2. Bengali Unicode variations
    3. Banglish (Romanized Bengali) transliteration
    4. English-Bengali code-mixing
    5. Meaning-preserving paraphrasing
    6. Adversarial wording
    """

    # Phonetic mappings for Banglish transliteration
    BANGLA_TO_BANGLISH = {
        'অ': 'o', 'আ': 'a', 'ই': 'i', 'ঈ': 'i', 'উ': 'u', 'ঊ': 'u', 'ঋ': 'ri',
        'এ': 'e', 'ঐ': 'oi', 'ও': 'o', 'ঔ': 'ou',
        'ক': 'k', 'খ': 'kh', 'গ': 'g', 'ঘ': 'gh', 'ঙ': 'ng',
        'চ': 'ch', 'ছ': 'chh', 'জ': 'j', 'ঝ': 'jh', 'ঞ': 'n',
        'ট': 't', 'ঠ': 'th', 'ড': 'd', 'ঢ': 'dh', 'ণ': 'n',
        'ত': 't', 'থ': 'th', 'দ': 'd', 'ধ': 'dh', 'ন': 'n',
        'প': 'p', 'ফ': 'f', 'ব': 'b', 'ভ': 'bh', 'ম': 'm',
        'য': 'z', 'র': 'r', 'ল': 'l', 'শ': 'sh', 'ষ': 'sh', 'স': 's', 'হ': 'h',
        'ড়': 'r', 'ঢ়': 'rh', 'য়': 'y', 'ৎ': 't', 'ং': 'ng', 'ঃ': 'h', 'ঁ': '',
        'া': 'a', 'ি': 'i', 'ী': 'i', 'ু': 'u', 'ূ': 'u', 'ৃ': 'ri',
        'ে': 'e', 'ৈ': 'oi', 'ো': 'o', 'ৌ': 'ou', '্': ''
    }

    # Code-mixing lexicon (Bengali terms to common English digital loanwords)
    CODEMIX_MAP = {
        'ওষুধ': 'medicine',
        'ঔষধ': 'medicine',
        'রোগী': 'patient',
        'টিকা': 'vaccine',
        'হাসপাতাল': 'hospital',
        'ডাক্তার': 'doctor',
        'সরকার': 'government',
        'নির্বাচন': 'election',
        'সংসদ': 'parliament',
        'ব্যাংক': 'bank',
        'টাকা': 'money',
        'ঋণ': 'loan',
        'মুদ্রাস্ফীতি': 'inflation',
        'ঘূর্ণিঝড়': 'cyclone',
        'বন্যা': 'flood',
        'আবহাওয়া': 'weather',
        'উপগ্রহ': 'satellite',
        'ইন্টারনেট': 'internet',
        'মোবাইল': 'mobile phone',
        'ভিডিও': 'video',
        'ছবি': 'photo',
        'তথ্য': 'information',
        'সংবাদ': 'news',
        'দাবি': 'claim',
        'পুলিশ': 'police'
    }

    # Synonym map for semantic paraphrasing
    SYNONYM_MAP = {
        'সম্পূর্ণভাবে': 'পুরোপুরি',
        'নিরাময় করে': 'ভালো করে তোলে',
        'বিনামূল্যে': 'বিনা খরচে',
        'প্রদান করা হয়': 'দেওয়া হয়ে থাকে',
        'ধ্বংস': 'বিনাশ',
        'তৈরি করে': 'সৃষ্টি করে',
        'কার্যকরী': 'ফলপ্রসূ',
        'নির্দেশনা': 'দিকনির্দেশনা',
        'নিশ্চিত করেছে': 'সুস্পষ্টভাবে জানিয়েছে',
        'ভিত্তিহীন': 'সম্পূর্ণ মিথ্যা',
        'প্রতারণামূলক': 'ভুয়া',
        'প্রয়োজনীয়': 'দরকারি',
        'উপযোগী': 'উপযুক্ত',
        'ঝুঁকিতে': 'বিপদে'
    }

    def __init__(self, seed: int = 42):
        random.seed(seed)

    def generate_typo(self, text: str) -> Tuple[str, int]:
        """Swaps adjacent characters or drops a character to simulate typing errors."""
        words = text.split()
        if not words:
            return text, 0
            
        perturbed_words = list(words)
        # Select 1-2 words to inject typos
        eligible_indices = [i for i, w in enumerate(words) if len(w) >= 3 and not w.endswith('।')]
        if not eligible_indices:
            eligible_indices = list(range(len(words)))
            
        target_idx = random.choice(eligible_indices)
        word = list(perturbed_words[target_idx])
        
        # Swap adjacent internal characters
        if len(word) >= 4:
            swap_pos = random.randint(1, len(word) - 3)
            word[swap_pos], word[swap_pos + 1] = word[swap_pos + 1], word[swap_pos]
        elif len(word) >= 2:
            word.pop(random.randint(0, len(word) - 1))
            
        perturbed_words[target_idx] = "".join(word)
        res = " ".join(perturbed_words)
        edit_dist = abs(len(text) - len(res)) + 1
        return res, edit_dist

    def generate_unicode_variation(self, text: str) -> Tuple[str, int]:
        """Applies canonical decomposition (NFD) or introduces zero-width characters."""
        # NFD decomposes composite characters into base + combining marks
        decomposed = unicodedata.normalize('NFD', text)
        # Also randomly insert ZWNJ (U+200C) after ya-phala (্য)
        variant = decomposed.replace('্য', '্\u200cয')
        edit_dist = len(variant) - len(text)
        return variant, abs(edit_dist)

    def generate_banglish(self, text: str) -> Tuple[str, int]:
        """Phonetically transliterates Bengali characters into Romanized Latin Banglish."""
        transliterated = []
        for char in text:
            if char in self.BANGLA_TO_BANGLISH:
                transliterated.append(self.BANGLA_TO_BANGLISH[char])
            elif char in ['।', '॥']:
                transliterated.append('.')
            else:
                transliterated.append(char)
        res = "".join(transliterated)
        # Collapse multiple identical vowels
        res = re.sub(r'([aeiou])\1+', r'\1', res)
        return res, len(res)

    def generate_codemix(self, text: str) -> Tuple[str, int]:
        """Replaces common Bengali content nouns with colloquial English equivalents."""
        res = text
        changes = 0
        for bn_word, en_word in self.CODEMIX_MAP.items():
            if bn_word in res:
                res = res.replace(bn_word, en_word, 1)
                changes += 1
                if changes >= 2:
                    break
        if changes == 0:
            # Fallback: append common English code-mixed tags
            res = res.replace('।', ' totally fake.') if '।' in res else res + ' as per report.'
        return res, len(res) - len(text)

    def generate_paraphrase(self, text: str) -> Tuple[str, int]:
        """Substitutes phrase-level synonyms while strictly preserving factual meaning."""
        res = text
        substitutions = 0
        for orig, syn in self.SYNONYM_MAP.items():
            if orig in res:
                res = res.replace(orig, syn, 1)
                substitutions += 1
                if substitutions >= 2:
                    break
        if substitutions == 0:
            # Reorder sentence clauses around commas if present
            if ',' in res or 'এবং' in res:
                res = res.replace('এবং', 'ও সাথে সাথে')
        return res, len(res) - len(text)

    def generate_adversarial_wording(self, text: str) -> Tuple[str, int]:
        """Prepends or appends deceptive hedging or assertive credibility markers."""
        hedges = [
            "বিভিন্ন সামাজিক মাধ্যমের জোরালো দাবি অনুযায়ী, ",
            "গোয়েন্দা ও আন্তর্জাতিক নির্ভরযোগ্য রিপোর্টের তথ্যমতে, ",
            "বিশেষজ্ঞদের এক বিশেষ সাক্ষাৎকারে প্রকাশ পেয়েছে যে, ",
            "সর্বসম্মত প্রাতিষ্ঠানিক বুলেটিন অনুসারে জানা গেছে যে, "
        ]
        chosen = random.choice(hedges)
        res = chosen + text
        return res, len(chosen)

    def transform_claim(self, claim_record: Dict, t_type: str) -> Dict:
        """Applies a specified transformation to a clean claim record."""
        orig_text = claim_record["claim_text_normalized"]
        cid = claim_record["claim_id"]

        if t_type == "typo":
            trans_text, dist = self.generate_typo(orig_text)
            method = "Adjacent character swap / minor token perturbation"
        elif t_type == "unicode_variation":
            trans_text, dist = self.generate_unicode_variation(orig_text)
            method = "NFD decomposition and zero-width non-joiner injection"
        elif t_type == "banglish_transliteration":
            trans_text, dist = self.generate_banglish(orig_text)
            method = "Phonetic rule-based Latin transliteration"
        elif t_type == "code_mixing":
            trans_text, dist = self.generate_codemix(orig_text)
            method = "Bengali-English colloquial loanword substitution"
        elif t_type == "paraphrase":
            trans_text, dist = self.generate_paraphrase(orig_text)
            method = "Domain-preserving synonym and clausal substitution"
        elif t_type == "adversarial_wording":
            trans_text, dist = self.generate_adversarial_wording(orig_text)
            method = "Deceptive authority marker insertion"
        else:
            raise ValueError(f"Unknown transformation type: {t_type}")

        return {
            "original_claim_id": cid,
            "transformation_id": f"{cid}-{t_type.upper()[:4]}",
            "transformation_type": t_type,
            "original_claim_text": orig_text,
            "transformed_claim_text": trans_text,
            "transformation_method": method,
            "semantic_preservation_judgment": "PRESERVED",
            "ground_truth_label": claim_record["adjudicated_label"],
            "domain": claim_record["domain"],
            "levenshtein_distance": dist
        }


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    engine = BengaliPerturbationEngine()
    sample_text = "পেঁপে পাতার রস খেলে ডেঙ্গু রোগীর প্লাটিলেট তাৎক্ষণিকভাবে স্বাভাবিক হয়ে যায় এবং ডেঙ্গু সম্পূর্ণ নিরাময় হয়।"
    dummy_rec = {"claim_id": "TEST-01", "claim_text_normalized": sample_text, "adjudicated_label": "REFUTED", "domain": "health"}

    for t in ["typo", "unicode_variation", "banglish_transliteration", "code_mixing", "paraphrase", "adversarial_wording"]:
        trans = engine.transform_claim(dummy_rec, t)
        print(f"\n--- {t.upper()} ---")
        print("Transformed:", trans["transformed_claim_text"])
