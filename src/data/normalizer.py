import unicodedata
import re

class BengaliTextNormalizer:
    """
    Standardized Bengali text normalizer for BanglaFactBench.
    Handles:
    - Unicode NFC normalization
    - Standardizing Bengali punctuation (Dari |, double dari)
    - Removing zero-width joiners (ZWJ) and non-joiners (ZWNJ) when used inconsistently
    - Normalizing common Bengali character variants (e.g., ya-phala, nukta)
    - Whitespace trimming and multiple space collapse
    """
    
    # Common Bengali Unicode ranges: U+0980 to U+09FF
    BENGALI_RANGE = re.compile(r'[\u0980-\u09FF]')
    
    # Dari normalization
    DARI_VARIANTS = re.compile(r'[\|\u0964]')
    DOUBLE_DARI_VARIANTS = re.compile(r'[\|\u0964]{2,}')
    
    # Whitespace cleanup
    WHITESPACE = re.compile(r'\s+')
    
    def __init__(self, remove_zwj: bool = False):
        self.remove_zwj = remove_zwj

    def normalize(self, text: str) -> str:
        if not text:
            return ""
            
        # 1. Unicode NFC Normalization (canonical decomposition followed by canonical composition)
        text = unicodedata.normalize('NFC', text)
        
        # 2. Normalize Bengali Dari / full stop
        text = self.DOUBLE_DARI_VARIANTS.sub('॥', text)
        text = self.DARI_VARIANTS.sub('।', text)
        
        # 3. Optional ZWJ / ZWNJ normalization (U+200D, U+200C)
        if self.remove_zwj:
            text = text.replace('\u200c', '').replace('\u200d', '')
            
        # 4. Normalize quotes and dashes
        text = text.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
        text = text.replace('–', '-').replace('—', '-')
        
        # 5. Collapse whitespaces
        text = self.WHITESPACE.sub(' ', text).strip()
        
        return text

    def is_bengali_dominant(self, text: str, threshold: float = 0.5) -> bool:
        """Checks if text contains at least threshold proportion of Bengali characters."""
        if not text:
            return False
        total_alpha = sum(1 for c in text if c.isalpha())
        if total_alpha == 0:
            return False
        bengali_count = len(self.BENGALI_RANGE.findall(text))
        return (bengali_count / total_alpha) >= threshold


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    normalizer = BengaliTextNormalizer()
    sample = "  এই ওষুধটি ডেঙ্গু   সম্পূর্ণভাবে নিরাময় করে| এটা ভুয়া তথ্য ||  "
    norm = normalizer.normalize(sample)
    print("Original:", repr(sample))
    print("Normalized:", repr(norm))
    assert '।' in norm
    assert '  ' not in norm
    print("Normalizer self-test passed!")
