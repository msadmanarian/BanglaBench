# 1. Introduction

Digital misinformation presents an acute societal challenge in Bengali-speaking regions, which encompass over 230 million native speakers across Bangladesh and West Bengal, India. During electoral periods, public health emergencies (such as dengue outbreaks and the COVID-19 pandemic), natural disasters (such as cyclones and monsoon flash floods), and economic shifts, false rumors propagate rapidly across platforms such as Facebook, WhatsApp, and YouTube.

Despite its societal importance, research into automated Bengali fact-checking faces four critical bottlenecks:
1. **The "Headline Classification" Formulation**: Prior works in Bengali NLP (e.g., BanFakeNews by Hossain et al., 2020) predominantly model misinformation as binary article or headline classification (`fake` vs. `real`), rather than verifiable claim extraction grounded in authoritative external evidence (Thorne et al., 2018).
2. **Artificial High Scores via Leakage**: Benchmark evaluations frequently rely on uniform random train/test splits. This setup allows models to memorize source-specific reporting styles, lexical markers, and journalist formatting, creating a false impression of high accuracy that shatters in production environments.
3. **Absence of Real-World Robustness Benchmarks**: Real-world Bengali internet text rarely follows standard Unicode NFC orthography. Users frequently communicate using Latin-script phonetics ("Banglish"), colloquial English-Bengali code-mixing, keyboard typos, and unstandardized Bengali conjuncts (যুক্তবর্ণ). No prior Bengali benchmark systematically evaluates adversarial or linguistic robustness across these dimensions.
4. **Unfaithful Rationales and Calibration Blindness**: Existing classifiers provide no verifiable citations or confidence calibration, presenting hallucinations and statistical guesses as objective fact.

To resolve these challenges, we introduce **BanglaFactBench**, a multi-domain benchmark and reliability framework for Bengali claim verification. Our core contributions are:
- **A High-Quality Curated Multi-Domain Corpus**: 60 claims meticulously extracted from primary fact-checking organizations and official sources across six diverse domains, categorized under a 5-class taxonomy with dual independent human annotations achieving Cohen's $\kappa = 0.9120$.
- **Leakage-Controlled Multi-Split Framework**: Five distinct evaluation splits (Random, Cross-Domain, Cross-Source, Temporal, and Adversarial) that systematically decouple genuine reasoning from memorized shortcuts.
- **Linguistic and Adversarial Perturbation Suite**: 72 controlled transformations evaluating typos, Unicode shifts, Banglish, code-mixing, paraphrase, and adversarial wording.
- **Evidence-Grounded Retrieval and Faithfulness Diagnostics**: An Okapi BM25 retrieval-augmented pipeline evaluating evidence recall, probability calibration (ECE), and explanation faithfulness under the ERASER framework.
