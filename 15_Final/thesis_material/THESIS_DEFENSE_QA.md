# BanglaFactBench: Comprehensive Thesis Defense Q&A Preparation

This document prepares the researcher for rigorous academic thesis defense examination across all dimensions of BanglaFactBench.

---

## 1. Dataset & Annotation Questions

### Q1: Why did you formulate the benchmark at the CLAIM level rather than full articles or headlines?
**Answer**: Full articles contain extensive non-factual background narrative, editorial framing, and historical context. When a classifier operates on full articles (as in BanFakeNews; Hossain et al., 2020), it inadvertently learns to classify the writing style of the author or publisher rather than verifying the specific factual assertion. Claims are discrete, falsifiable propositions that can be directly mapped to external corroborating evidence passages, following the standard FEVER and MultiFC paradigms (Thorne et al., 2018; Augenstein et al., 2019).

### Q2: Why choose a 5-class taxonomic schema instead of binary (True/False)?
**Answer**: Real-world misinformation rarely exists in pure binary states. Viral rumors frequently contain a kernel of truth surrounded by distorted framing (`MISLEADING`), speculative statements lacking conclusive evidence (`UNVERIFIABLE`), or subjective political/moral judgments (`OPINION`). Collapsing these into binary labels forces annotators to make arbitrary decisions and deprives downstream verification systems of the nuance required for real-world deployment.

### Q3: How did you validate annotation reliability, and why is Cohen's kappa appropriate?
**Answer**: Two bilingual annotators independently labeled all 60 claims following detailed guidelines with concrete inclusion/exclusion criteria. We computed Cohen's kappa ($\kappa = 0.9120$) with an observed agreement of $93.33\%$ and chance agreement of $24.22\%$. Cohen's kappa is mathematically appropriate here because it accounts for agreement occurring strictly by chance in categorical classification with two independent raters. Disagreements were systematically resolved through structured adjudication.

---

## 2. Experimental Setup & Model Questions

### Q4: Why did classical models perform poorly on Split C (Cross-Source)?
**Answer**: In Split C, models achieved only 0.0000 to 0.0667 Macro-F1. This catastrophic collapse proves that classical text classifiers trained under random splits rely heavily on **source-specific lexical shortcuts**. Fact-checking portals (e.g., Rumor Scanner) and news outlets possess distinct stylistic vocabularies and reporting formats. When evaluated on unseen sources (e.g., BoomBD or Facebook posts), these superficial lexical anchors disappear, demonstrating that previous high scores reported under random splits were largely artifacts of source leakage.

### Q5: What is the primary advantage of the Retrieval-Augmented Generation (RAG) system?
**Answer**: The primary advantage of RAG is **superior probability calibration and auditable grounding**. RAG achieved an Expected Calibration Error (ECE) of **0.1631** (compared to 0.4217 for Naive Bayes and 0.2547 for SVM). By conditioning predictions on retrieved authoritative documents, the system avoids overconfident hallucinations and provides human fact-checkers with verifiable source URLs and relevant excerpts.

### Q6: What is the main vulnerability of the BM25 retrieval engine?
**Answer**: BM25 relies on exact lexical term frequencies. When tested on our adversarial paraphrase subset (Split E), the retrieval hit rate collapsed from 100.0% to 16.7%, causing a 53.1% relative drop in verification Macro-F1. Paraphrasing replaces exact terms with synonyms that exact-match sparse retrieval fails to retrieve.

---

## 3. Robustness & Linguistic Questions

### Q7: Why did Banglish transliteration cause such a severe drop (-63.8%)?
**Answer**: Standard Bengali NLP pipelines are trained strictly on Bengali Unicode script. Social media users in Bangladesh predominantly communicate in "Banglish" (Bengali phonetics rendered in Latin script). This script shift converts known Bengali words into out-of-vocabulary Latin tokens, destroying the TF-IDF feature space and causing models to collapse to majority-class guessing.

### Q8: What did the ERASER explanation faithfulness test reveal?
**Answer**: Applying the ERASER protocol revealed that Mean Comprehensiveness was non-positive ($C \le 0$) across all linear models, and removing the top 20% most influential tokens left predictions unchanged up to 100% of the time (in Logistic Regression). This proves mathematically that highlighted token rationales are unfaithful post-hoc artifacts: the models' computational predictions actually depend on diffuse background token correlations rather than the salient keywords shown in UI explanations.

---

## 4. Methodological & Ethical Questions

### Q9: How did you ensure zero data leakage between splits?
**Answer**: We implemented automated deduplication and leakage auditing (`deduplication.py` and `data_leakage_analysis.md`). We verified zero string overlap, character 3-gram Jaccard overlap $< 0.40$, strictly disjoint domain assignments in Split B, strictly disjoint source assignments in Split C, and strict temporal separation at January 1, 2024 for Split D.

### Q10: What are the main contributions of this thesis?
**Answer**:
1. First multi-domain, 5-class claim verification corpus in Bengali with high inter-annotator agreement ($\kappa = 0.9120$).
2. First leakage-controlled benchmark framework decoupling domain, source, temporal, and adversarial performance in Bengali.
3. First quantitative evaluation of explanation faithfulness (ERASER) and probability calibration (ECE) on Bengali claim verification.
4. An open, reproducible benchmark package establishing anti-fabrication standards for low-resource NLP research.
