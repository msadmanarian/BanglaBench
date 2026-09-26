# Scientific Contributions
# Project: BanglaFactBench

---

The completed research and artifacts of **BanglaFactBench** provide eight distinct contributions to Natural Language Processing, low-resource language understanding, and automated fact-checking:

### Contribution 1: A Dedicated Multi-Domain Bengali Claim Verification Benchmark
The creation of the first fine-grained, claim-level benchmark in Bengali spanning six diverse societal domains (Politics, Health, Disaster, Finance, Science/Tech, and Social Media), addressing the historical limitation of document-level datasets that conflate stylistic cues with factual veracity.

### Contribution 2: A Documented 5-Class Annotation Schema & Guidelines
A rigorous, mutually exclusive annotation protocol and taxonomy (`SUPPORTED`, `REFUTED`, `UNVERIFIABLE`, `MISLEADING`, `OPINION`) with explicit inclusion criteria, boundary decision rules, real-world examples, and documented inter-annotator agreement metrics.

### Contribution 3: Out-of-Distribution Generalization Benchmarks (Splits B & C)
The formal release of domain-disjoint and source-disjoint evaluation partitions, providing the research community with standardized testbeds to assess whether models generalize beyond publisher-specific shortcuts and narrow topical vocabularies.

### Contribution 4: A Systematic Bengali Adversarial Robustness Suite (Split E)
The first algorithmic perturbation framework for Bengali NLP evaluating six distinct linguistic failure modes: typographical errors, Bengali Unicode variants, phonetic Banglish (Romanized Bengali), English-Bengali code-mixing, meaning-preserving paraphrases, and adversarial wording.

### Contribution 5: First Systematic Banglish & Code-Mixing Veracity Evaluation
A dedicated evaluation of how subword tokenizers and multilingual encoders fail when processing colloquial South Asian digital text, providing concrete error diagnostics for social media monitoring.

### Contribution 6: Retrieval-Augmented Verification Pipeline for Low-Resource News
An empirical comparison of parametric-only classifiers versus retrieval-grounded architectures (sparse BM25, dense retrieval, and reranking), quantifying the degree to which external evidence grounding prevents model hallucinations.

### Contribution 7: Quantitative Explanation Faithfulness & Calibration Analysis
The first study in Bengali NLP to quantitatively evaluate the faithfulness of model rationales using Sufficiency and Comprehensiveness perturbation tests (following ERASER principles), alongside confidence calibration metrics (Expected Calibration Error).

### Contribution 8: Fully Open, Reproducible Research & Evaluation Package
A comprehensive reproducibility repository featuring automated training and evaluation scripts, modular configuration files, programmatic data validation suites, model cards, and dataset documentation.
