import re
from typing import List, Dict, Set, Tuple

class ClaimDeduplicator:
    """
    Detects exact and near-duplicate claims to prevent benchmark contamination and data leakage.
    Uses character 3-gram and word-level Jaccard similarity.
    """
    
    def __init__(self, jaccard_threshold: float = 0.80):
        self.jaccard_threshold = jaccard_threshold

    @staticmethod
    def get_char_ngrams(text: str, n: int = 3) -> Set[str]:
        cleaned = re.sub(r'\s+', '', text)
        if len(cleaned) < n:
            return {cleaned}
        return {cleaned[i:i+n] for i in range(len(cleaned) - n + 1)}

    @staticmethod
    def get_word_set(text: str) -> Set[str]:
        words = re.findall(r'\w+', text)
        return set(words)

    @classmethod
    def jaccard_similarity(cls, set_a: Set[str], set_b: Set[str]) -> float:
        if not set_a or not set_b:
            return 0.0
        intersection = len(set_a.intersection(set_b))
        union = len(set_a.union(set_b))
        return intersection / union if union > 0 else 0.0

    def find_near_duplicates(self, records: List[Dict]) -> List[Tuple[str, str, float, str]]:
        """
        Finds pairs of claims with Jaccard similarity exceeding threshold.
        Returns list of (id_1, id_2, similarity_score, reason)
        """
        duplicates = []
        n = len(records)
        for i in range(n):
            rec_i = records[i]
            id_i = rec_i.get('claim_id', f'item_{i}')
            text_i = rec_i.get('claim_text_normalized', rec_i.get('claim_text_bn', ''))
            ngrams_i = self.get_char_ngrams(text_i)
            words_i = self.get_word_set(text_i)

            for j in range(i + 1, n):
                rec_j = records[j]
                id_j = rec_j.get('claim_id', f'item_{j}')
                text_j = rec_j.get('claim_text_normalized', rec_j.get('claim_text_bn', ''))

                # Exact match check
                if text_i == text_j:
                    duplicates.append((id_i, id_j, 1.0, "Exact claim text match"))
                    continue

                # Character n-gram Jaccard
                ngrams_j = self.get_char_ngrams(text_j)
                char_sim = self.jaccard_similarity(ngrams_i, ngrams_j)
                
                # Word-level Jaccard
                words_j = self.get_word_set(text_j)
                word_sim = self.jaccard_similarity(words_i, words_j)
                
                max_sim = max(char_sim, word_sim)
                if max_sim >= self.jaccard_threshold:
                    duplicates.append((id_i, id_j, round(max_sim, 4), f"Near-duplicate (char_sim={char_sim:.2f}, word_sim={word_sim:.2f})"))
                    
        return duplicates

    def check_split_leakage(self, train_records: List[Dict], test_records: List[Dict]) -> List[Tuple[str, str, float, str]]:
        """
        Detects any overlap or near-duplicate leakage between training and testing splits.
        """
        leakages = []
        for rec_tr in train_records:
            id_tr = rec_tr.get('claim_id', 'train_item')
            text_tr = rec_tr.get('claim_text_normalized', '')
            ngrams_tr = self.get_char_ngrams(text_tr)
            words_tr = self.get_word_set(text_tr)

            for rec_te in test_records:
                id_te = rec_te.get('claim_id', 'test_item')
                text_te = rec_te.get('claim_text_normalized', '')

                if text_tr == text_te:
                    leakages.append((id_tr, id_te, 1.0, "EXACT LEAKAGE between train and test"))
                    continue

                ngrams_te = self.get_char_ngrams(text_te)
                char_sim = self.jaccard_similarity(ngrams_tr, ngrams_te)
                
                words_te = self.get_word_set(text_te)
                word_sim = self.jaccard_similarity(words_tr, words_te)
                
                max_sim = max(char_sim, word_sim)
                if max_sim >= self.jaccard_threshold:
                    leakages.append((id_tr, id_te, round(max_sim, 4), f"NEAR-LEAKAGE (char_sim={char_sim:.2f}, word_sim={word_sim:.2f})"))

        return leakages


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    dedup = ClaimDeduplicator(jaccard_threshold=0.75)
    sample_records = [
        {"claim_id": "C1", "claim_text_normalized": "পদ্মা সেতু বাংলাদেশের নিজস্ব অর্থায়নে নির্মিত হয়েছে।"},
        {"claim_id": "C2", "claim_text_normalized": "পদ্মা সেতু বাংলাদেশের নিজস্ব অর্থায়নে তৈরি হয়েছে।"},
        {"claim_id": "C3", "claim_text_normalized": "করোনা ভ্যাকসিনের কোনো মাইক্রোচিপ নেই।"}
    ]
    dups = dedup.find_near_duplicates(sample_records)
    print("Detected Duplicates:", dups)
    assert len(dups) >= 1
    print("Deduplication self-test passed!")
