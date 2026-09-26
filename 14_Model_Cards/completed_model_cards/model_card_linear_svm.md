# Model Card: BanglaFact Linear SVM Baseline

## 1. Model Details
- **Model Name**: BanglaFact-LinearSVM-TFIDF
- **Model Version**: v1.0
- **Architecture**: Maximum-Margin Linear Support Vector Classifier with Word (1-2) and Character (2-4) n-gram TF-IDF representations.
- **Target Language**: Bengali (bn)
- **Training Source**: BanglaFactBench Curated Core Partitions
- **License**: MIT License

## 2. Intended Use
- **Primary Intended Use**: Linear discriminative baseline for Bengali claim verification research and lexical shortcut diagnosis.
- **Out-of-Scope Use Cases**: Automated censorship, production fact-checking without human review, legal judgments.

## 3. Training & Evaluation Data
- **Training Dataset**: BanglaFactBench Split A Train (N=42)
- **Evaluation Partitions**: Split A Test (N=12), Split B Cross-Domain (N=10), Split C Cross-Source (N=19), Split D Temporal (N=35), Split E Adversarial (N=72).
- **Preprocessing Pipeline**: Unicode NFC normalization, dari harmonization, whitespace stripping.

## 4. Performance Metrics (Empirically Observed)
- **Split A (Random Stratified F1)**: 0.3250 [95% CI: 0.0667, 0.5833]
- **Split B (Cross-Domain F1)**: 0.2333 (-28.2% relative degradation)
- **Split C (Cross-Source F1)**: 0.0667 (-79.5% relative degradation)
- **Split D (Temporal Shift F1)**: 0.2570 (-20.9% relative degradation)
- **Split E (Adversarial Mean Relative Drop)**: -8.0% (Worst drop: -63.8% on Banglish transliteration)
- **Expected Calibration Error (ECE)**: 0.2547
- **Brier Score**: 0.8754

## 5. Strengths & Limitations
- **Strengths**: Fast deterministic training, robust against Unicode encoding variance, high recall on majority class (`REFUTED`).
- **Known Biases**: Extreme bias toward predicting `REFUTED` (0.00 recall on `SUPPORTED`, `UNVERIFIABLE`, `MISLEADING`).
- **Robustness Limitations**: Collapses under Banglish transliteration (-63.8% drop); zero ability to transfer to unseen news sources.
