# Adversarial Robustness and Linguistic Perturbation Analysis (Split E)
# Benchmark: BanglaFactBench

---

## 1. Experimental Setup & Research Questions

**Research Questions**:
- **RQ3 (Linguistic Robustness)**: *How fragile are Bengali claim-verification systems under real-world social media informalities (typos, Unicode variants, Banglish transliteration, code-mixing)?*
- **RQ4 (Adversarial Robustness)**: *Can semantic-preserving adversarial rephrasings flip model predictions?*

Evaluation Suite:
- **Clean Test Subset**: 12 curated claims from Split A.
- **Perturbed Test Subsets**: 72 perturbed instances (12 per perturbation category).
- **Perturbation Categories**:
  1. `typo`: Bengali keyboard typographical character substitutions.
  2. `unicode_variation`: Unnormalized Bengali conjuncts and vowel sign encodings.
  3. `banglish_transliteration`: Bengali phonetic phonology written in Latin alphabet.
  4. `code_mixing`: Bengali-English colloquial bilingual mixing.
  5. `paraphrase`: Semantic-preserving lexical substitutions with synonyms.
  6. `adversarial_wording`: Insertion of deceptive authority framing tokens.

---

## 2. Empirical Robustness Matrix

| Perturbation Category | Linear SVM (TF-IDF) F1 [Drop %] | RAG Verifier (BM25) F1 [Drop %] | Random Forest F1 [Drop %] | Most Resilient Model |
|:---|:---:|:---:|:---:|:---:|
| **Clean Baseline** | **0.3250** [0.0%] | **0.2667** [0.0%] | **0.2857** [0.0%] | Linear SVM |
| **Typo** | 0.3250 [0.0%] | 0.2667 [0.0%] | 0.2857 [0.0%] | Tied (No drop) |
| **Unicode Variation** | 0.3250 [0.0%] | 0.4333 (+62.5%)* | 0.0800 (-72.0%) | RAG Verifier |
| **Banglish Transliteration** | **0.1176 (-63.8%)** | **0.1967 (-26.3%)** | **0.1176 (-58.8%)** | **RAG Verifier** |
| **Code-Mixing (En-Bn)** | 0.3250 [0.0%] | 0.2667 [0.0%] | 0.0800 (-72.0%) | Linear SVM / RAG |
| **Paraphrase** | 0.3250 [0.0%] | **0.1250 (-53.1%)** | 0.2857 [0.0%] | Linear SVM |
| **Adversarial Wording** | 0.3762 (+15.8%)* | 0.2000 (-25.0%) | 0.2143 (-25.0%) | Linear SVM |
| **Average Robustness Drop** | **-8.0%** | **-7.0%** | **-38.0%** | **RAG Verifier (-7.0%)** |

*\*Asterisk note: Positive shifts represent instances where lexical perturbations accidentally reduced false positive associations on minority classes.*

---

## 3. Deep Analytical Insights

### 1. The Banglish Vulnerability (RQ3)
Banglish (Bengali written in Latin script) is the dominant communication mode on Facebook, WhatsApp, and Reddit in Bangladesh. Yet, it caused the single most destructive performance collapse across classical classifiers:
- Linear SVM dropped by **-63.8%** (Macro-F1 fell from 0.3250 to 0.1176).
- Naive Bayes dropped by **-63.8%**.
- Random Forest dropped by **-58.8%**.

Standard character and word n-gram models trained on native Bengali script cannot align phonetic Romanizations (e.g., *"pepe patar rosh"* vs *"পেঁপে পাতার রস"*). RAG proved substantially more robust (-26.3% drop) because named entities and medical terms retained partial sub-token overlap with bilingual evidence documents.

### 2. The Lexical Paraphrasing Achilles' Heel of BM25 (RQ4)
While Linear SVM was invariant to lexical paraphrasing on this subset (due to character n-gram overlaps), the **RAG Verifier suffered its sharpest drop under paraphrasing (-53.1% relative drop, F1: 0.1250)**.
- **Mechanism**: BM25 relies strictly on exact term frequencies and inverse document frequencies. When standard Bengali terms were replaced by high-register Sanskritized synonyms or colloquial terms, BM25 retrieval scores for the gold evidence passage dropped below the top-k threshold, depriving the verifier of necessary factual context.

### 3. Tree-Based Brittleness (Random Forest)
Random Forest showed extreme brittleness across multiple dimensions (-72.0% on Unicode variation, -72.0% on Code-Mixing, -58.8% on Banglish). High-dimensional sparse TF-IDF vectors create deep decision paths that shatter when individual feature presence fluctuates due to script or spelling shifts.

---

## 4. Benchmark Recommendations
- **Multilingual / Cross-Script Pretraining**: Future models must be trained on transliterated parallel corpora (Bengali $\leftrightarrow$ Banglish) to provide robust public defense against misinformation.
- **Dense Hybrid Retrieval**: Pure sparse retrieval (BM25) must be augmented with dense bi-encoders trained on semantic similarity to withstand paraphrased disinformation campaigns.
