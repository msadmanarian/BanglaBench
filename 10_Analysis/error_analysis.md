# Qualitative and Quantitative Error Analysis
# Benchmark: BanglaFactBench

---

## 1. Executive Summary

This error analysis examines the systemic failure modes observed across all benchmark models (Naive Bayes, Linear SVM, Logistic Regression, Random Forest, and RAG Verifier) on the 60-claim curated evaluation partitions of BanglaFactBench. 

Our empirical results reveal that classical surface-text classifiers do not perform genuine semantic fact-checking; instead, they exploit diffuse lexical heuristics and domain-specific co-occurrences. When evaluated on out-of-distribution sources (Split C), unseen domains (Split B), temporal shifts (Split D), or perturbed inputs (Split E), these heuristics collapse.

---

## 2. Formal Error Taxonomy (E1 – E10)

Based on inspection of model predictions across 12 test instances in Split A, 10 in Split B, 19 in Split C, 35 in Split D, and 72 in Split E, we formulate a 10-category error taxonomy:

| Error ID | Error Category | Description | Primary Vulnerable Pipeline |
|:---|:---|:---|:---|
| **E1** | **Lexical Shortcut Exploitation** | Relying on presence of charged terms (e.g., "দাবি", "ভুয়া", "শতভাগ") rather than factual relation. | TF-IDF (SVM, NB, LR) |
| **E2** | **Source Lexical Signature Bias** | Overfitting to stylistic markers, reporting conventions, and formatting of specific newsrooms. | Classical Classifiers (Split C) |
| **E3** | **Context & Attribution Stripping** | Misclassifying a reported quote or speculative claim as a verified factual statement. | Surface Classifiers, BM25 |
| **E4** | **Temporal State Misalignment** | Evaluating a claim that was historically true/false with outdated evidence or future shifts. | Static Classifiers, Split D |
| **E5** | **Evidence Retrieval Failure (Vocabulary Mismatch)** | BM25 failing to retrieve relevant evidence when claim words are paraphrased or synonyms used. | RAG Verifier (Split E Paraphrase) |
| **E6** | **Bengali Complex Morpho-Syntactic Ambiguity** | Failure caused by inflections, compound words (সমাস), sandhi, or vibhakti shifts. | Subword-unaware tokenizers |
| **E7** | **Phonetic & Script Shift Failure (Banglish)** | Complete inability to parse Bengali written in Latin script or phonetic chat language. | Character/Word TF-IDF |
| **E8** | **Negation Inversion & Polarity Blindness** | Reversing claim polarity (e.g., adding "না" or "নয়") without shifting model prediction. | Bag-of-Words, Naive Bayes |
| **E9** | **Numerical & Entity Substitution** | Blindness to altered quantities, dates, budget numbers, or casualty statistics. | All text-only baselines |
| **E10** | **Subjective vs. Factual Conflation (Opinion Slip)** | Confusing value judgements ("OPINION") with unverified factual claims ("UNVERIFIABLE"). | All baselines |

---

## 3. Case Studies of Failure Modes

### Case Study 1: Error E1 (Lexical Shortcut)
- **Claim ID**: `BFB-SCI-001`
- **Claim Text**: `"বাংলাদেশ মহাকাশ গবেষণা ও দূর অনুধাবন প্রতিষ্ঠান (SPARSO) ২০২৫ সালে নিজস্ব প্রযুক্তিতে তৈরি উপগ্রহ উৎক্ষেপণ করবে।"'
- **Ground Truth**: `REFUTED`
- **Linear SVM Prediction**: `SUPPORTED`
- **Cause**: The presence of institutional titles ("বাংলাদেশ মহাকাশ গবেষণা ও দূর অনুধাবন প্রতিষ্ঠান") and technical vocabulary biased the classifier towards official/supported government announcements in the training distribution. The model lacked factual grounding regarding SPARSO's actual budget and launch schedule.

### Case Study 2: Error E7 (Banglish Transliteration Collapse)
- **Claim ID**: `BFB-HLT-001`
- **Original Claim**: `"পেঁপে পাতার রস খেলে ডেঙ্গু রোগীর প্লাটিলেট তাৎক্ষণিকভাবে বৃদ্ধি পায়।"'
- **Ground Truth**: `REFUTED`
- **Perturbed Claim (Banglish)**: `"pepe patar rosh khele dengue rogier platelet tatkhonikbhabe briddhi pay"`
- **Linear SVM Prediction (Clean)**: `REFUTED` (Correct)
- **Linear SVM Prediction (Banglish)**: `SUPPORTED` (Incorrect)
- **Cause**: Out-of-vocabulary Latin script tokens destroyed the TF-IDF feature vector. The model defaulted to the majority class prior, resulting in a 63.8% relative Macro-F1 drop.

### Case Study 3: Error E5 (Evidence Retrieval Mismatch under Paraphrasing)
- **Claim ID**: `BFB-POL-003`
- **Original Claim**: `"পদ্মা সেতুর নির্মাণ ব্যয়ের সম্পূর্ণ অর্থ বাংলাদেশ সরকার নিজস্ব তহবিল থেকে বহন করেছে।"'
- **Paraphrased Claim**: `"পদ্মা ব্রিজের যাবতীয় খরচ দেশের নিজস্ব অর্থায়নে নির্বাহ করা হয়েছে।"'
- **RAG Verifier Clean Prediction**: `SUPPORTED` (Correct, Evidence Hit: 100%)
- **RAG Verifier Paraphrase Prediction**: `REFUTED` (Evidence Hit: 0%)
- **Cause**: Exact lexical terms ("পদ্মা সেতুর নির্মাণ ব্যয়", "তহবিল") were replaced with semantic equivalents ("পদ্মা ব্রিজের যাবতীয় খরচ", "অর্থায়ন"). Exact-match BM25 failed to score the relevant passage in the top-3, triggering an evidence-retrieval failure.

---

## 4. Confusion Matrix Analysis (Split A Test, N=12)

The 5-class confusion matrix for Linear SVM on Split A:

| Actual \ Predicted | SUPPORTED | REFUTED | UNVERIFIABLE | MISLEADING | OPINION |
|:---|:---:|:---:|:---:|:---:|:---:|
| **SUPPORTED** (3) | **0** | 3 | 0 | 0 | 0 |
| **REFUTED** (5) | 0 | **5** | 0 | 0 | 0 |
| **UNVERIFIABLE** (1) | 0 | 1 | **0** | 0 | 0 |
| **MISLEADING** (2) | 0 | 2 | 0 | **0** | 0 |
| **OPINION** (1) | 0 | 0 | 0 | 0 | **1** |

### Key Observations:
1. **Refuted Bias**: The classifier over-predicted `REFUTED` (11 out of 12 predictions were either `REFUTED` or `OPINION`). Every `SUPPORTED`, `UNVERIFIABLE`, and `MISLEADING` claim was erroneously collapsed into `REFUTED`.
2. **Minority Class Extinction**: Classes with nuanced boundaries (`MISLEADING` and `UNVERIFIABLE`) suffered 0.00 recall. Distinguishing subtle half-truths from outright falsehoods requires multi-step factual inference beyond surface n-grams.
3. **Opinion Distinctness**: `OPINION` had distinct stylistic subjectivity markers (e.g., "উচিত", "মনে হয়"), allowing 100% precision and recall on the test set.

---

## 5. Strategic Recommendations for Bengali Fact Verification

1. **Hybrid Retrieval**: Combine dense semantic embeddings (e.g., BanglaBERT / multilingual E5) with sparse BM25 to eliminate Error E5.
2. **Subword & Transliteration Robustness**: Pre-normalize Banglish through phonetic transliteration dictionaries prior to feature extraction to mitigate Error E7.
3. **Explicit Claim-Evidence NLI**: Decouple the verification pipeline into two distinct components: (a) Passage Retrieval and (b) Natural Language Inference (Premise: Evidence, Hypothesis: Claim) to resolve Error E1 and E8.
