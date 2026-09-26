# 2. Related Work

Our research builds upon foundational literature across four key domains of Natural Language Processing:

### 2.1 Automated Fact-Checking and Claim Verification
The formulation of fact-checking as claim verification grounded in external evidence was established by the FEVER benchmark (Thorne et al., 2018), which evaluated systems on claim extraction, document retrieval, and natural language inference (NLI). Augenstein et al. (2019) extended this to MultiFC, introducing multi-domain real-world claims from fact-checking portals. More recently, Schlichtkrull et al. (2024) proposed AVeriTeC, demonstrating that real-world fact verification requires multi-hop web retrieval and question-answering strategies.

In multilingual settings, X-Fact (Gupta & Srikumar, 2021) established the largest cross-lingual claim verification benchmark spanning 25 languages. However, Bengali representation in cross-lingual datasets is typically limited to machine-translated snippets or small web-scraped subsets that lack cultural, regional, and dialectal nuances.

### 2.2 Bengali Misinformation and NLP Resources
The earliest substantial Bengali fake news dataset, BanFakeNews (Hossain et al., 2020), introduced 50,000 articles for binary detection. Subsequent iterations, such as BanFakeNews-2.0 (Kabir et al., 2023) and BanMANI (Khandokar et al., 2024), added domain categories and multimodal meme analysis. IndicClaimBuster (Nath et al., 2022) explored check-worthiness estimation for Indian regional languages. 

Concurrently, transformer models specialized for Bengali have emerged, most notably BanglaBERT (Bhattacharjee et al., 2022), pretrained on 27.5 GB of Bengali text, and multilingual encoders such as XLM-RoBERTa (Conneau et al., 2020) and MuRIL (Khanuja et al., 2021). Despite these advancements, existing Bengali datasets evaluate models predominantly under random train/test splits, leaving cross-domain, cross-source, and temporal generalization unmeasured.

### 2.3 Adversarial NLP and Robustness Benchmarking
Ribeiro et al. (2020) introduced CheckList, establishing behavioral testing of NLP models across vocabulary substitutions, typos, and negations. In misinformation research, adversarial framing and style transfer have been shown to drastically degrade detector accuracy (Schuster et al., 2020). For South Asian languages, code-mixing with English and transliteration into Latin script ("Banglish") present massive challenges to standard tokenizers and language models (Chakravarthi et al., 2021).

### 2.4 Retrieval-Augmented Verification and Explanation Faithfulness
Retrieval-Augmented Generation (RAG; Lewis et al., 2020) and Dense Passage Retrieval (Karpukhin et al., 2020) enable factual grounding by retrieving external reference texts. To ensure that models do not produce convincing yet misleading explanations, DeYoung et al. (2020) established the ERASER benchmark, introducing two quantitative criteria: *Sufficiency* (whether extracted rationales are sufficient to maintain predictions) and *Comprehensiveness* (whether removing rationales degrades predictions). BanglaFactBench bridges these fields by applying ERASER diagnostics to Bengali claim verification for the first time.
