# Dataset Card for BanglaFactBench

## Dataset Summary
**BanglaFactBench** is a standardized, multi-domain benchmark for factual claim verification, misinformation detection, and adversarial robustness in Bengali. Comprising fine-grained, atomic claims across six critical societal domains (Politics, Public Health, Disaster Management, Finance, Science & Technology, and Social Media), the benchmark is designed to evaluate whether AI and NLP systems can verify factual claims under realistic domain shifts, source shifts, temporal drift, and linguistic/adversarial perturbations.

---

## 1. Dataset Motivation & Purpose
- **Why was this dataset created?** Previous Bengali misinformation datasets (e.g., BanFakeNews) focused on document-level binary classification, enabling models to exploit publisher styles and lexical shortcuts without verifying factual assertions against evidence. BanglaFactBench was created to provide the first claim-level, multi-domain evaluation benchmark with dedicated out-of-distribution splits and adversarial perturbation test suites.
- **Key Research Question**: Can current NLP and LLM systems reliably verify Bengali claims across domains, unseen sources, temporal horizons, and linguistic transformations?

---

## 2. Dataset Composition
- **Instances**: Atomic factual propositions with contextual descriptions and evidence citations.
- **Fields per Record**:
  - `claim_id`: Unique identifier (e.g., `BFB-CLM-0001`)
  - `claim_text_bn`: Verbatim Bengali / Banglish claim text
  - `claim_text_normalized`: Unicode NFC-normalized text
  - `domain`: One of `politics`, `health`, `finance`, `disaster`, `sci_tech`, `social`
  - `source_type`: Originating medium (`social_media`, `news_portal`, `press_release`, `public_speech`, `fact_check_archive`)
  - `source_name`: Specific platform or news outlet
  - `source_url`: URL of origin or archive
  - `publication_date`: Fact-check / publication date (YYYY-MM-DD)
  - `claim_date`: Approximate origin date of claim (YYYY-MM-DD)
  - `language`: `bn`, `en`, or `mixed`
  - `language_variant`: `standard_bengali`, `colloquial_bengali`, `banglish`, `code_mixed`
  - `context`: Minimal background context
  - `evidence_urls`: Authoritative verification sources
  - `evidence_text`: Excerpt of corroborating or refuting evidence
  - `label`: `SUPPORTED`, `REFUTED`, `UNVERIFIABLE`, `MISLEADING`, `OPINION`
  - `confidence`: Confidence score (0.0 to 1.0)
  - `adjudicated_label`: Final resolved label

---

## 3. Data Collection & Curation
- **Data Sources**: Sourced from certified fact-checking archives (Rumor Scanner, FactWatch, BOOM Bangladesh), mainstream Bengali investigative reporting, and public institutional announcements.
- **Quality Control**: Automated deduplication via character n-gram SimHash, Unicode NFC normalization, language validation, and manual claim atomization.

---

## 4. Benchmark Partitions & Splits
- **Split A (Random Split)**: Standard stratified 70/15/15 train/val/test partition for baseline comparison.
- **Split B (Cross-Domain Split)**: Domain-disjoint partitions evaluating out-of-domain transfer.
- **Split C (Cross-Source Split)**: Source-disjoint partitions to evaluate source shortcut exploitation.
- **Split D (Temporal Split)**: Chronological past $\rightarrow$ train, future $\rightarrow$ test split to measure temporal knowledge drift.
- **Split E (Adversarial Split)**: Semantics-preserving transformations (Typo, Unicode, Banglish, Code-Mixing, Paraphrase, Adversarial Wording).

---

## 5. Ethical Considerations & Limitations
- **Data Privacy**: Private personal details (phone numbers, private addresses, personal photos) are strictly excluded or redacted.
- **Political & Ideological Neutrality**: Veracity evaluations are grounded solely in authoritative public records without endorsing political views.
- **Health Disclaimer**: Factual labels on medical claims reflect published scientific and institutional consensus (WHO, DGHS) and do not constitute personal clinical guidance.
- **Intended Use**: Academic research on automated fact-checking, NLP robustness, and retrieval-augmented verification.
- **Prohibited Use**: Malicious generation of targeted misinformation, automated censorship without human oversight, or unauthorized commercial surveillance.
- **License**: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0).
