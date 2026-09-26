# Data Statement for BanglaFactBench
**Standard**: Bender & Friedman (2018) Data Statements for Natural Language Processing

---

## A. Curation Rationale
BanglaFactBench was curated to provide a high-quality, claim-level, multi-domain benchmark for fact verification and adversarial robustness in Bengali. Claims were selected from digital media in Bangladesh to reflect authentic societal misinformation across politics, public health, disaster management, economics, technology, and social rumors.

## B. Language Variety
- **Language**: Bengali (ISO 639-1: `bn`, ISO 639-3: `ben`).
- **Variants**:
  - Standard Bengali (Cholitobhasha)
  - Colloquial social media Bengali
  - Romanized Bengali (Banglish)
  - English-Bengali Code-Mixed text
- **Script**: Eastern Nagari (Bengali script) and Latin script for Banglish/code-mixed subsets.

## C. Speaker / Source Demographics
Claims originate from public digital discourse in Bangladesh (2020–2026), including social media posts, digital news portals, television broadcast transcripts, and political press conferences. Demographic representation reflects public figures, institutional spokespersons, and anonymous social media creators.

## D. Annotator Demographics
- **Number of Annotators**: Trained independent native Bengali speakers with university-level education in Computer Science, Linguistics, or Social Sciences.
- **Language Profile**: Native speakers of Bengali with professional working proficiency in English.
- **Geographic Location**: Bangladesh.

## E. Speech / Text Situation
Textual data consists of written digital posts, extracted headlines, transcribed public statements, and atomic propositions. Modality is written digital text.

## F. Text Characteristics
Texts range from short atomic propositions (8 to 45 words) to contextual explanatory passages. Vocabulary spans formal legislative terminology, colloquial slang, transliterated expressions, and medical/economic vocabulary.

## G. Provenance & Preprocessing
Sourced from certified fact-checking archives (Rumor Scanner, FactWatch, BOOM Bangladesh) and verified news archives under research fair use. Text was preprocessed with Unicode NFC normalization, deduplication via SimHash, and anonymization of private non-public citizens.
