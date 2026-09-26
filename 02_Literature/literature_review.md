# Comprehensive Literature Review
# Project: BanglaFactBench: A Multi-Domain Benchmark for Misinformation Detection, Claim Verification, and Adversarial Robustness in Bengali

---

## 1. Introduction & Theoretical Overview

Misinformation on digital media has emerged as an acute global challenge with immediate consequences for democratic processes, public health adherence, financial stability, and communal peace. In low-resource and linguistically complex language ecosystems such as Bengali—spoken by over 270 million people worldwide across Bangladesh and eastern India—the problem is magnified by rapid smartphone penetration, high reliance on social platforms, and the historical scarcity of annotated Natural Language Processing (NLP) benchmarks (*Hasan et al., 2021*).

This literature review synthesizes 36 peer-reviewed academic studies across 15 thematic areas, providing the rigorous foundation upon which **BanglaFactBench** is constructed.

---

## 2. Synthesis Across the 15 Literature Categories

### 2.1 Misinformation Detection
Automated misinformation detection originated primarily as full-length news article classification. Early research relied on hand-crafted stylistic features, sentiment polarities, and psychological lexicons. With the release of **BanFakeNews** (*Hossain et al., 2020*), the first large-scale Bengali fake news dataset (~50,000 articles), researchers demonstrated that classical models (SVM, Random Forest) and shallow neural architectures (BiLSTM, CNN) achieved modest F1-scores due to severe class imbalance (only ~3% fake news prevalence in collected mainstream portals). More recently, **BanFakeNews-2.0** (*Shibu et al., 2025*) expanded the benchmark to 60,000 articles across 13 topical categories, demonstrating that modern Large Language Models (LLMs) with quantized parameter-efficient fine-tuning (QLoRA) achieve superior detection capabilities. However, article-level detection remains vulnerable to publisher-specific stylistic shortcuts (*Augenstein et al., 2019*).

### 2.2 Fact Checking Taxonomies
Fact checking is inherently more nuanced than binary truth-value classification. International fact-checking organizations (PolitiFact, Snopes, FactCheck.org) operate fine-grained rating systems such as "True", "Mostly True", "Half True", "Mostly False", "Pants on Fire", and "Unproven". In Bangladesh, certified signatories of the International Fact-Checking Network (IFCN)—including **Rumor Scanner**, **FactWatch**, and **BOOM Bangladesh**—classify claims into labels such as False, Misleading, Altered, Satire, and True (*Haque et al., 2023*; *Sarker et al., 2022*). Binary reductions lose critical distinctions, particularly for claims that are technically accurate in isolation but paired with deceptive framing or fabricated contexts (*Sarker et al., 2022*).

### 2.3 Claim Verification Frameworks
In contrast to document classification, claim verification evaluates whether an isolated, atomic proposition is factually substantiated by reliable evidence. The seminal **FEVER** benchmark (*Thorne et al., 2018*) formulated claim verification as a three-class textual entailment problem (`SUPPORTS`, `REFUTES`, `NOT ENOUGH INFO`) conditioned on retrieved Wikipedia passages. Later benchmarks, such as **SciFact** (*Wadden et al., 2020*) and **MultiFC** (*Augenstein et al., 2019*), extended this paradigm to scientific and multi-domain real-world web claims. In Indic languages, **IndicClaimBuster** (*Pal et al., 2025*) introduced a 9,000-instance claim-evidence dataset covering English, Hindi, Bengali, and code-mixed text. However, existing Indic claim verification resources remain limited in domain breadth and lack adversarial evaluation.

### 2.4 Bengali NLP Pretraining
The performance of NLP systems in Bengali has been transformed by transformer pretraining. While early research utilized static embeddings (FastText, Word2Vec), the development of **BanglaBERT** by BUET researchers (*Bhattacharjee et al., 2022*) established the state of the art. Pretrained on the 27.5 GB "Bangla2B+" corpus using an ELECTRA-style generator-discriminator objective, BanglaBERT consistently outperforms massive multilingual models across classification, named entity recognition, and question answering. For sequence generation, **BanglaNLG** (*Bhattacharjee et al., 2023*) introduced **BanglaT5**, demonstrating high-quality generative capabilities in summarization and paraphrasing.

### 2.5 Low-Resource Language Challenges
Despite having hundreds of millions of native speakers, Bengali has historically been categorized as a low-resource language in computational linguistics due to data fragmentation and lack of task-specific annotations (*Hasan et al., 2021*). Key linguistic challenges include:
- **Complex Morphological Inflection**: Bengali is an agglutinative Indo-Aryan language where nouns take case endings (vibhakti), verbs undergo complex tense-aspect-mood conjugations, and clitics attach directly to word stems.
- **Complex Conjuncts (*Juktakkhor*) & Diacritics (*Kar*)**: Non-standard keyboard inputs frequently produce conflicting Unicode byte sequences (e.g., ya-phala variations, hasanta placement).
- **Dialectal and Regional Diversity**: Variations between standard Bangladeshi Bengali (*Cholitobhasha*), West Bengal idioms, and colloquial regional dialects (*Chittagonian, Sylheti, Noakhali*).

### 2.6 Multilingual Transformers & Cross-Lingual Transfer
Multilingual foundation models, particularly **mBERT** (*Devlin et al., 2019*) and **XLM-RoBERTa** (*Conneau et al., 2020*), provide zero-shot and few-shot cross-lingual transfer capabilities by pretraining on Common Crawl corpora spanning 100 languages. In the multilingual fact-checking benchmark **X-Fact** (*Gupta & Srikumar, 2021*), multilingual transformers were evaluated on 25 languages. The authors discovered that while models transfer moderately well between typologically similar European languages, zero-shot transfer to Bengali yielded low macro F-scores (~40%), proving that multilingual pretraining alone cannot substitute for native language benchmarks grounded in local evidence.

### 2.7 LLM Fact Checking & Reasoning
Recent frontier LLMs (GPT-3.5, GPT-4, LLaMA-3) demonstrate impressive general knowledge and zero-shot reasoning. However, empirical studies reveal substantial vulnerabilities when applied to fact-checking in low-resource languages. In **BanMANI** (*Kamruzzaman et al., 2023*), GPT-3 and GPT-3.5 struggled to reliably identify subtle social media claim manipulations in Bengali without task-specific fine-tuning. Furthermore, LLMs deployed without retrieval tend to hallucinate convincing justifications for false claims, underscoring that raw model weights cannot serve as an authoritative knowledge base.

### 2.8 Retrieval-Augmented Generation (RAG)
To address parametric hallucinations, Retrieval-Augmented Generation (*Lewis et al., 2020*) decouples the factual knowledge repository from the reasoning model. By combining an external retriever with an entailment/generation model, RAG enables auditable citations. Sparse lexical retrieval using **BM25** (*Robertson & Zaragoza, 2009*) relies on inverted term indices, offering strong baseline performance but suffering from vocabulary mismatch in morphologically inflected languages. **Dense Passage Retrieval (DPR)** (*Karpukhin et al., 2020*) and late-interaction architectures like **ColBERT** (*Khattab & Zaharia, 2020*) project queries and passages into dense semantic spaces, retrieving relevant evidence based on contextual embeddings. In recent real-world benchmarks like **AVeriTeC** (*Schlichtkrull et al., 2023*), open-web retrieval is shown to be the single most critical component in preventing verification errors.

### 2.9 Adversarial NLP & Vulnerabilities
Neural NLP architectures exhibit extreme fragility under subtle input perturbations that do not alter human comprehension. As demonstrated by **TextFooler** (*Jin et al., 2020*) and **AdvGLUE** (*Wang et al., 2021*), meaning-preserving word substitutions and synonym attacks reduce classifier accuracy by over 40-50%. In character-level analysis, **Pruthi et al. (2019)** revealed that subword tokenizers (WordPiece, BPE) catastrophically fragment words subjected to single-character typos, leading out-of-vocabulary representations to mislead downstream attention heads.

### 2.10 Behavioral & Robustness Evaluation
Moving beyond aggregate test-set accuracy, the **CheckList** methodology (*Ribeiro et al., 2020*) established behavioral testing principles for NLP: Minimum Functionality Tests (MFT), Invariance Tests (INV), and Directional Expectation Tests (DIR). Applying behavioral testing to fact-checking is vital: if a model verifies "এই ওষুধটি ডেঙ্গু নিরাময় করে" (This medicine cures dengue) as false, but flips its prediction to true when the claim contains a minor spelling mistake or phonetic transliteration, the model has learned superficial lexical shortcuts rather than factual verification.

### 2.11 Explanation Faithfulness & Interpretability
In automated verification, an explanation is as important as the veracity verdict. However, **Jacovi & Goldberg (2020)** formalized the critical distinction between **plausibility** (how convincing an explanation appears to a human) and **faithfulness** (whether the explanation accurately reflects the features responsible for the model's decision). As shown by **Jain & Wallace (2019)** and **Wiegreffe & Pinter (2019)**, raw attention weights often fail to provide faithful rationales. The **ERASER** benchmark (*DeYoung et al., 2020*) formalized two quantitative metrics for faithfulness:
- **Sufficiency**: Can the model achieve the same prediction when provided only with the extracted rationale?
- **Comprehensiveness**: Does the model's prediction confidence drop significantly when the extracted rationale is removed from the input?

### 2.12 Dataset Construction & Curation Standards
Constructing robust evaluation benchmarks requires disciplined collection and verification protocols. Rather than indiscriminately scraping social media feeds, reliable benchmarks document source provenance, extraction methods, and licensing terms (*Gebru et al., Datasheets for Datasets, 2021*). Quality control procedures must enforce strict deduplication, Unicode normalization, language identification, and entity-overlap checking between splits (*Gorman & Bedrick, 2019*).

### 2.13 Annotation Protocols & Inter-Annotator Agreement
Human annotation of controversial claims requires formal operational definitions to avoid individual subjectivity. Inter-annotator agreement metrics—chiefly **Cohen's Kappa ($\kappa$)** for paired annotators (*Landis & Koch, 1977*) or Fleiss' Kappa for multiple annotators—measure whether observed agreement exceeds chance agreement under marginal distributions. Following rigorous annotation frameworks (*Thorne et al., 2018*; *Augenstein et al., 2019*), ambiguous cases must undergo independent adjudication by a senior researcher. Fabricating or reporting unmeasured agreement statistics violates fundamental academic integrity.

### 2.14 Temporal Fact Checking & Knowledge Drift
World knowledge is dynamic. As established by **Lazaridou et al. (ICLR 2021)** and **Dhingra et al. (TACL 2022)**, language models trained on historical text suffer progressive performance degradation when evaluated on subsequent temporal streams. In fact-checking, **Müller et al. (EMNLP 2022)** proved that classifiers evaluated on future claims experience severe F1 drops (12-18%) due to emerging named entities and changing ground realities. Claim-level benchmarks must therefore preserve temporal metadata (`claim_date`, `publication_date`, `evidence_date`) and incorporate temporal evaluation splits.

### 2.15 Misinformation in Social Media: Banglish & Code-Mixing
In South Asia, digital communication is characterized by widespread language mixing and script alternation. Social media users in Bangladesh frequently express Bengali concepts using the Latin alphabet—a practice known as **Banglish** or Romanized Bangla (*Roy et al., 2020*). Additionally, English-Bengali **code-mixing** (*Banerjee et al., EMNLP 2021*) is pervasive across platforms like Facebook, WhatsApp, and TikTok. Standard Bengali tokenizers fail completely on Banglish, fracturing words into unnatural sub-character tokens. A realistic Bengali misinformation benchmark must systematically test model robustness against Banglish and code-mixed inputs.

---

## 3. Summary of Literature Implications for BanglaFactBench

The literature leads directly to seven foundational design decisions:
1. **Focus on Atomic Claims**: Avoid document-level shortcuts by evaluating claim-level verification (*Thorne et al., 2018*; *Augenstein et al., 2019*).
2. **5-Class Fine-Grained Taxonomy**: Capture misleading claims and opinion statements distinct from direct refutations (*Sarker et al., 2022*).
3. **Multi-Domain & Cross-Source Evaluation**: Evaluate true generalization via domain-disjoint and source-disjoint splits (*Augenstein et al., 2019*; *Gorman & Bedrick, 2019*).
4. **Behavioral Perturbation Suite**: Test model robustness across typos, Unicode variations, Banglish transliteration, and code-mixing (*Ribeiro et al., 2020*; *Roy et al., 2020*).
5. **RAG Architecture**: Ground verification predictions in external evidence using hybrid sparse and dense retrieval (*Lewis et al., 2020*; *Schlichtkrull et al., 2023*).
6. **Quantitative Faithfulness Testing**: Measure sufficiency and comprehensiveness to ensure rationales genuinely support predictions (*DeYoung et al., 2020*; *Jacovi & Goldberg, 2020*).
7. **Temporal Sensitivity**: Test robustness to temporal knowledge drift using date-stamped claim partitions (*Dhingra et al., 2022*; *Müller et al., 2022*).
