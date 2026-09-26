# 6. Discussion

### 6.1 Why Real-World Fact-Checking Fails in Bengali NLP
Our findings challenge the prevailing paradigm in low-resource misinformation detection. In benchmark literature, models frequently report accuracy and F1 scores exceeding 90%. However, our multi-split evaluation reveals that such performance is largely an artifact of **leakage**:
- When models are evaluated on unseen sources (Split C), performance collapses by over **79%**.
- When models encounter phonetic transliteration ("Banglish"), performance plummets by **63.8%**.
- When models face temporal concept drift (Split D), performance degrades by up to **39.1%**.

These results demonstrate that existing models are not verifying claims; they are performing **source and dialect classification**. A model trained on a specific fact-checking portal memorizes the stylistic tone of that portal's debunking articles. When presented with a raw rumor from an unseen Facebook page or local newspaper, the model's learned stylistic heuristics become useless.

### 6.2 The Promise and Peril of Retrieval-Augmented Verification
Our RAG verification experiments offer two critical lessons for system architects:
1. **Calibration Superiority**: The RAG verifier achieved an Expected Calibration Error of **0.1631** (compared to 0.4217 for Naive Bayes and 0.2547 for SVM). Grounding predictions in retrieved evidence prevents the overconfident hallucinations characteristic of purely parametric classifiers. When no evidence is found, the system refrains from guessing.
2. **Lexical Retrieval Brittleness**: The reliance on sparse lexical matching (BM25) creates an acute vulnerability: under semantic paraphrasing, retrieval recall collapsed from 100% to 16.7%, causing a 53.1% drop in verification F1. To build robust production systems, hybrid retrieval combining dense multilingual bi-encoders (e.g., multilingual E5 or BanglaBERT) with sparse BM25 is essential.

### 6.3 Rethinking Explainability for Public Trust
Highlighting keywords in a graphical user interface creates an illusion of interpretability. Our ERASER faithfulness diagnostics prove that in linear and bag-of-words models, removing these supposedly critical rationales leaves model predictions unchanged up to **100% of the time**. Relying on unfaithful post-hoc rationales in high-stakes domains (such as public health or election monitoring) is hazardous. Future Bengali fact-checking systems must adopt inherently faithful architectures, where predictions are strictly mathematically conditioned on verifiable evidence citations.
