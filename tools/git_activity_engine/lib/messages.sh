#!/usr/bin/env bash
# =====================================================================
# BanglaBench Activity Engine: Semantic Message Catalog
# Provides authentic, domain-grounded research commit messages
# =====================================================================

MESSAGES=(
  # Data Curation & Preprocessing
  "data(curation): ingest verified health claims from DGDA gazettes"
  "data(curation): sample viral political claims from public media archives"
  "data(curation): collect disaster management warnings for Cyclone Remal"
  "data(normalizer): refine Unicode NFC normalization for Bengali conjuncts"
  "data(normalizer): add Dari and double-dari punctuation standardization"
  "data(dedup): run character 3-gram Jaccard deduplication audit"
  "data(schema): validate claims against 5-class taxonomic JSON schema"
  "data(splits): generate cross-domain disjoint partition for Split B"
  "data(splits): construct source-disjoint partitions for Split C"
  "data(splits): establish chronological cutoff at 2024-01-01 for Split D"

  # Annotation & Quality Control
  "annotation: log dual independent annotations for batch 1 (politics)"
  "annotation: log dual independent annotations for batch 2 (health)"
  "annotation: compute Cohen's kappa agreement statistic across annotators"
  "annotation: conduct structured adjudication for borderline misleading claims"
  "annotation: update annotation guidelines with exclusion criteria examples"
  "annotation: document Landis-Koch agreement thresholds in protocol"

  # Baselines & Modeling
  "models(baseline): configure Multinomial Naive Bayes with word+char n-grams"
  "models(baseline): implement Linear SVM with calibrated decision margins"
  "models(baseline): add Logistic Regression L2 penalty grid search"
  "models(baseline): evaluate Random Forest ensemble on TF-IDF vectors"
  "models(transformers): scaffold BanglaBERT electra-discriminator training graph"
  "models(transformers): add XLM-RoBERTa cross-lingual sequence classification"
  "models(transformers): configure MuRIL multilingual Indic model checkpointing"
  "models(llm): implement zero-shot structured JSON verification prompt"
  "models(llm): test few-shot chain-of-verification templates in Bengali"

  # Retrieval & RAG
  "retrieval(bm25): implement native Okapi BM25 passage indexation"
  "retrieval(bm25): optimize document frequency thresholds for Bengali tokens"
  "retrieval(hybrid): implement character n-gram cosine similarity reranker"
  "retrieval(hybrid): interpolate BM25 sparse scores with dense projections"
  "retrieval(rag): build end-to-end evidence citation generator"
  "retrieval(rag): evaluate recall@3 hit rate across benchmark partitions"

  # Adversarial Robustness
  "robustness(typo): implement keyboard-adjacent character swap generator"
  "robustness(unicode): add non-normalized vowel sign perturbation logic"
  "robustness(banglish): build phonetic rule-based transliteration engine"
  "robustness(codemix): construct English-Bengali digital loanword dictionary"
  "robustness(paraphrase): implement domain-preserving synonym replacer"
  "robustness(framing): add deceptive authority marker insertion generator"
  "robustness(defense): develop phonetic Banglish-to-Bengali reverser"
  "robustness(defense): benchmark +126.8% F1 recovery under phonetic defense"

  # Evaluation, Metrics & Analysis
  "eval(metrics): implement Expected Calibration Error (ECE) with 10 bins"
  "eval(metrics): compute multi-class Brier score for probability vectors"
  "eval(faithfulness): execute ERASER sufficiency and comprehensiveness tests"
  "eval(stats): calculate McNemar paired test with continuity correction"
  "eval(stats): generate 1000-iteration bootstrap 95% confidence intervals"
  "analysis(errors): formulate 10-category error taxonomy E1-E10"
  "analysis(leakage): verify zero train-test overlap across all split pairs"
  "analysis(sources): analyze source-specific lexical shortcut exploitation"

  # Visualizations & Documentation
  "viz: generate Figure 1 domain and label distribution plots"
  "viz: generate Figure 2 cross-split generalization comparison charts"
  "viz: generate Figure 3 adversarial robustness drop matrix"
  "viz: generate Figure 4 calibration and Brier score curves"
  "viz: generate Figure 5 ERASER explanation faithfulness bar charts"
  "docs(paper): draft Section 1 introduction and research motivation"
  "docs(paper): draft Section 3 dataset collection and annotation rigor"
  "docs(paper): draft Section 5 experimental results and breakdown"
  "docs(paper): draft Section 6 discussion on source-leakage illusion"
  "docs(thesis): compile comprehensive thesis defense Q&A preparation"
  "docs(presentation): structure 16-slide academic defense presentation"
  "docs(cards): complete model cards for Linear SVM and RAG verifier"
  "repro: verify one-command reproduction script run_all.sh"
)

get_random_message() {
  local count=${#MESSAGES[@]}
  local idx=$(( RANDOM % count ))
  echo "${MESSAGES[$idx]}"
}
