# 9. Conclusion

We presented **BanglaFactBench**, a multi-domain benchmark for claim verification, misinformation detection, and adversarial robustness in Bengali. Grounded in university research methodologies and rigorous anti-fabrication standards, BanglaFactBench addresses key blind spots in low-resource NLP through:
1. A carefully curated 60-claim corpus spanning six domains and five taxonomic classes with high inter-annotator agreement ($\kappa = 0.9120$);
2. Five leakage-controlled evaluation splits that expose catastrophic vulnerabilities under cross-source shifts (-79.5%), cross-domain shifts (-28.2%), and temporal drift (-20.9% to -39.1%);
3. An adversarial robustness suite demonstrating that phonetic transliteration ("Banglish") causes a severe -63.8% performance collapse in surface text classifiers;
4. An evidence-grounded RAG verification pipeline that significantly improves probability calibration (ECE = 0.1631) while uncovering lexical retrieval brittleness under semantic paraphrasing;
5. Diagnostic ERASER evaluations proving that post-hoc linear feature attributions fail the test of computational necessity.

By establishing an open, fully reproducible resource package—complete with audited dataset cards, evaluation scripts, and statistical significance tests—BanglaFactBench provides a rigorous foundation to advance trustworthy, robust, and verifiable NLP systems for the global Bengali-speaking community.
