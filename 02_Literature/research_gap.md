# Research Gap Analysis
# Project: BanglaFactBench

This document provides a systematic, literature-supported analysis of the empirical and methodological gaps in Bengali misinformation detection, claim verification, and robustness benchmarking.

---

## 1. Summary of Existing Bengali Resources and Their Boundaries

A thorough examination of existing literature reveals that while research on Bengali misinformation has emerged over the past five years, current resources exhibit severe structural limitations:

| Existing Benchmark / Dataset | Primary Task | Key Contributions | Empirical Limitations & Literature-Supported Gaps |
|---|---|---|---|
| **BanFakeNews** (*Hossain et al., LREC 2020*) | Article-level fake news classification | First large corpus (~50k articles) | 1. Extreme class imbalance (~97% authentic, 3% fake).<br>2. Full-document classification promotes topic/style shortcut learning rather than factual verification.<br>3. No evidence retrieval or claim-level grounding.<br>4. Evaluated only on random split; no cross-domain, cross-source, or adversarial tests. |
| **BanFakeNews-2.0** (*Shibu et al., IndoNLP 2025*) | Topic-wise news classification | Expanded to 60k articles across 13 topics; introduced QLoRA LLM baselines | 1. Remains full-article classification; cannot verify individual factual claims.<br>2. Does not incorporate external evidence retrieval (no RAG pipeline).<br>3. No evaluation of linguistic perturbations, Banglish, or code-mixing.<br>4. No explanation faithfulness evaluation. |
| **BanMANI** (*Kamruzzaman et al., ConTeNTS 2023*) | Manipulated social media post detection | Evaluated subtle semantic divergences between social posts and reference articles | 1. Limited sample size (1,491 pairs).<br>2. Requires pre-paired reference articles; does not evaluate open evidence retrieval.<br>3. Narrow domain coverage; lacks systematic cross-domain and temporal splitting. |
| **IndicClaimBuster** (*Pal et al., IJCNLP-AACL 2025*) | Multilingual claim verification (En, Hi, Bn, Hi-En) | 9k claim-evidence pairs; two-stage retrieval and veracity modeling | 1. Bengali is only a minority subset.<br>2. Restricted to only 3 domains (politics, law, health).<br>3. No adversarial robustness or Banglish/transliteration testing.<br>4. No explanation faithfulness or calibration analysis. |
| **X-Fact** (*Gupta & Srikumar, ACL-IJCNLP 2021*) | Multilingual fact checking across 25 languages | Benchmark evaluating out-of-domain and zero-shot transfer | 1. Bengali is tested primarily under zero-shot transfer without in-language evidence, yielding poor performance (~40% F1).<br>2. Evaluates multilingual models (mBERT, XLM-R) but ignores native Bengali transformers (`BanglaBERT`).<br>3. Lacks fine-grained analysis of Bengali linguistic variations. |
| **BD-FakeDetect** (*Sarker et al., Mendeley Data 2022*) | Multimodal fake news detection | 5,929 posts from Rumor Scanner, FactWatch, BOOM BD, Jachai with 8 decision labels | 1. Focuses on multimodal classification without atomic claim extraction.<br>2. Lacks standardized out-of-distribution benchmark splits (evaluated only on random splits).<br>3. No retrieval-augmented evaluation. |

---

## 2. Six Critical Research Gaps

Supported by the verified literature matrix (`02_Literature/literature_matrix.csv`), BanglaFactBench addresses six specific, unaddressed gaps:

### Gap 1: Absence of a Dedicated Multi-Domain Bengali Claim Verification Benchmark
- **Evidence**: Established international benchmarks such as FEVER (*Thorne et al., 2018*), MultiFC (*Augenstein et al., 2019*), and AVeriTeC (*Schlichtkrull et al., 2023*) operate on atomic claims rather than entire articles. In Bengali, existing datasets (*BanFakeNews*, *BanFakeNews-2.0*) predominantly evaluate document-level classification. When models classify entire news articles, they exploit stylistic cues, publisher vocabulary, or sensationalism rather than verifying whether specific factual assertions are supported by evidence (*Augenstein et al., 2019*).
- **BanglaFactBench Solution**: Construct a claim-level benchmark spanning multiple vital societal domains: politics, public health, finance, disaster/emergency information, science/technology, and social media.

### Gap 2: Lack of Out-of-Distribution (Cross-Domain and Cross-Source) Generalization Testing
- **Evidence**: As demonstrated by Gorman & Bedrick (*ACL 2019*) and Augenstein et al. (*2019*), standard random train/test splits overestimate real-world model reliability because training and test sets share identical source distributions, author writing styles, and overlapping events. In Bengali misinformation research, models have almost exclusively been evaluated on random splits.
- **BanglaFactBench Solution**: Establish Split B (Cross-Domain) and Split C (Cross-Source) where models are trained on specific domains/sources and evaluated on strictly unseen domains and news organizations.

### Gap 3: Complete Lack of Adversarial and Linguistic Robustness Evaluation (Banglish, Code-Mixing, Typos)
- **Evidence**: Real-world misinformation in Bangladesh propagates heavily on social media (Facebook, WhatsApp, YouTube) where users write in informal Bengali, Romanized Bengali (**Banglish**), and English-Bengali code-mixed text (*Haque et al., 2023*; *Roy et al., 2020*; *Banerjee et al., 2021*). Furthermore, NLP models are known to suffer severe performance degradation under character substitutions and typos (*Pruthi et al., 2019*; *Ribeiro et al., CheckList 2020*). No existing Bengali misinformation dataset evaluates model vulnerability to such linguistic variations.
- **BanglaFactBench Solution**: Design Split E (Adversarial Robustness Suite) evaluating 6 controlled, semantics-preserving perturbation transformations: typographical noise, Bengali Unicode variation, phonetic Banglish transliteration, English-Bengali code-mixing, paraphrasing, and adversarial wording.

### Gap 4: Underexplored Retrieval-Augmented Verification in Low-Resource Bengali News
- **Evidence**: Parametric-only language models hallucinate factual assertions when verifying claims without external grounding (*Lewis et al., RAG 2020*; *Schlichtkrull et al., AVeriTeC 2023*). While dense retrieval has been extensively explored for English (*Karpukhin et al., DPR 2020*), retrieval-augmented claim verification over unstructured Bengali news remains largely unbenchmarked.
- **BanglaFactBench Solution**: Build and benchmark a modular RAG verification pipeline comparing sparse lexical retrieval (BM25) and dense multilingual representations (mContriever / fine-tuned multilingual SBERT) coupled with verification models.

### Gap 5: Absence of Explanation Faithfulness and Calibration Studies
- **Evidence**: As emphasized by Jacovi & Goldberg (*ACL 2020*) and DeYoung et al. (*ERASER, ACL 2020*), an explanation that appears convincing to humans (plausibility) does not necessarily reflect the true reasoning features driving model predictions (faithfulness). In automated fact-checking, unfaithful or hallucinated rationales present serious societal hazards (*Atanasova et al., 2020*). Furthermore, neural networks are frequently miscalibrated and overconfident in erroneous predictions (*Guo et al., ICML 2017*).
- **BanglaFactBench Solution**: Conduct the first quantitative evaluation of explanation faithfulness (evaluating rationale sufficiency and comprehensiveness via input perturbation) and model calibration (Expected Calibration Error, Brier Score) for Bengali claim verification.

### Gap 6: Neglect of Temporal Knowledge Drift
- **Evidence**: Factual veracity is temporally sensitive; claims accurate at time $t_1$ may become refuted or outdated at time $t_2$ (*Dhingra et al., TACL 2022*; *Müller et al., EMNLP 2022*). Fact-checking models trained on historical data degrade significantly when deployed on subsequent streams (*Lazaridou et al., ICLR 2021*).
- **BanglaFactBench Solution**: Integrate temporal metadata (`claim_date`, `publication_date`, `evidence_date`) and establish Split D (Temporal Split) to quantify performance degradation when models trained on past claims are evaluated on future claims.
