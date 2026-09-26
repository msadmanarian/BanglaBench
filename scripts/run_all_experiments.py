import os
import sys
import json
import numpy as np
from datetime import datetime
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

# Add src to path
base_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(base_dir, 'src', 'models'))
sys.path.append(os.path.join(base_dir, 'src', 'retrieval'))
sys.path.append(os.path.join(base_dir, 'src', 'evaluation'))

from classical_baselines import BanglaFactClassifier
from rag_verifier import RAGVerificationSystem
from metrics import BenchmarkMetrics
from statistical_tests import StatisticalSignificanceTester
from faithfulness import ExplanationFaithfulnessEvaluator
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

def load_json(rel_path):
    p = os.path.join(base_dir, rel_path)
    with open(p, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(rel_path, data):
    p = os.path.join(base_dir, rel_path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    print(f"[{datetime.now().isoformat()}] Starting BanglaFactBench Master Experiment Suite...")
    seed = 42

    # 1. Load Partitions
    split_a_train = load_json('04_Dataset/train/split_a_train.json')
    split_a_test = load_json('04_Dataset/test/split_a_test.json')

    split_b_train = load_json('04_Dataset/train/split_b_train.json')
    split_b_test = load_json('04_Dataset/test/split_b_test.json')

    split_c_train = load_json('04_Dataset/train/split_c_train.json')
    split_c_test = load_json('04_Dataset/test/split_c_test.json')

    split_d_train = load_json('04_Dataset/temporal/split_d_train_past.json')
    split_d_test = load_json('04_Dataset/temporal/split_d_test_future.json')

    perturbation_types = ["typo", "unicode_variation", "banglish_transliteration", "code_mixing", "paraphrase", "adversarial_wording"]
    adversarial_sets = {t: load_json(f'04_Dataset/adversarial/split_e_{t}.json') for t in perturbation_types}

    classes = ["SUPPORTED", "REFUTED", "UNVERIFIABLE", "MISLEADING", "OPINION"]
    model_types = ['nb', 'svm', 'lr', 'rf']

    results = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "benchmark_name": "BanglaFactBench",
            "seed": seed,
            "classes": classes
        },
        "split_a_random": {},
        "split_b_cross_domain": {},
        "split_c_cross_source": {},
        "split_d_temporal": {},
        "split_e_adversarial": {},
        "faithfulness": {},
        "statistical_tests": {}
    }

    # ========================================================
    # EXPERIMENT 1: SPLIT A (RANDOM STRATIFIED BASELINE)
    # ========================================================
    print("\n--- Running Experiment 1: Split A (Random Baseline) ---")
    X_train_a = [c["claim_text_normalized"] for c in split_a_train]
    y_train_a = [c["adjudicated_label"] for c in split_a_train]
    X_test_a = [c["claim_text_normalized"] for c in split_a_test]
    y_test_a = [c["adjudicated_label"] for c in split_a_test]

    trained_models = {}

    for m_type in model_types:
        model = BanglaFactClassifier(model_type=m_type, seed=seed)
        model.fit(X_train_a, y_train_a)
        eval_res = model.evaluate(X_test_a, y_test_a)
        probs = model.predict_proba(X_test_a)
        
        ece = BenchmarkMetrics.compute_ece(y_test_a, probs)
        bs = BenchmarkMetrics.compute_brier_score(y_test_a, probs)
        ci = StatisticalSignificanceTester.bootstrap_f1_ci(y_test_a, eval_res["predictions"], classes, seed=seed)

        eval_res["ece"] = ece
        eval_res["brier_score"] = bs
        eval_res["ci_95"] = [ci["ci_95_lower"], ci["ci_95_upper"]]

        results["split_a_random"][m_type] = eval_res
        trained_models[m_type] = model
        print(f"Model: {m_type.upper():<5} | Macro-F1: {eval_res['macro_f1']:.4f} | Acc: {eval_res['accuracy']:.4f} | ECE: {ece:.4f}")

    # RAG Verifier on Split A
    rag = RAGVerificationSystem(top_k=3, seed=seed)
    rag.fit(split_a_train)
    rag_eval = rag.evaluate(split_a_test)

    # Compute RAG ECE and Brier score
    rag_probs = np.zeros((len(split_a_test), len(classes)))
    for idx, c in enumerate(split_a_test):
        v = rag.verify_claim(c["claim_text_normalized"])
        p_lbl = v["label"]
        conf = v["confidence"]
        c_i = classes.index(p_lbl) if p_lbl in classes else 0
        rag_probs[idx, c_i] = conf
        # Distribute remaining probability evenly
        rem = (1.0 - conf) / (len(classes) - 1)
        for j in range(len(classes)):
            if j != c_i:
                rag_probs[idx, j] = rem

    rag_ece = BenchmarkMetrics.compute_ece(y_test_a, rag_probs)
    rag_bs = BenchmarkMetrics.compute_brier_score(y_test_a, rag_probs)
    rag_ci = StatisticalSignificanceTester.bootstrap_f1_ci(y_test_a, rag_eval["predictions"], classes, seed=seed)
    rag_eval["ece"] = rag_ece
    rag_eval["brier_score"] = rag_bs
    rag_eval["ci_95"] = [rag_ci["ci_95_lower"], rag_ci["ci_95_upper"]]

    results["split_a_random"]["rag"] = rag_eval
    trained_models["rag"] = rag
    print(f"Model: RAG   | Macro-F1: {rag_eval['macro_f1']:.4f} | Acc: {rag_eval['accuracy']:.4f} | ECE: {rag_ece:.4f} | Hit: {rag_eval['retrieval_hit_rate']*100:.1f}%")

    # ========================================================
    # EXPERIMENT 2: SPLIT B (CROSS-DOMAIN EVALUATION)
    # ========================================================
    print("\n--- Running Experiment 2: Split B (Cross-Domain) ---")
    X_train_b = [c["claim_text_normalized"] for c in split_b_train]
    y_train_b = [c["adjudicated_label"] for c in split_b_train]
    X_test_b = [c["claim_text_normalized"] for c in split_b_test]
    y_test_b = [c["adjudicated_label"] for c in split_b_test]

    for m_type in model_types:
        model = BanglaFactClassifier(model_type=m_type, seed=seed)
        model.fit(X_train_b, y_train_b)
        eval_res = model.evaluate(X_test_b, y_test_b)
        results["split_b_cross_domain"][m_type] = eval_res
        print(f"Model: {m_type.upper():<5} | Cross-Domain Macro-F1: {eval_res['macro_f1']:.4f} | Acc: {eval_res['accuracy']:.4f}")

    rag_b = RAGVerificationSystem(top_k=3, seed=seed)
    rag_b.fit(split_b_train)
    rag_eval_b = rag_b.evaluate(split_b_test)
    results["split_b_cross_domain"]["rag"] = rag_eval_b
    print(f"Model: RAG   | Cross-Domain Macro-F1: {rag_eval_b['macro_f1']:.4f} | Acc: {rag_eval_b['accuracy']:.4f}")

    # ========================================================
    # EXPERIMENT 3: SPLIT C (CROSS-SOURCE EVALUATION)
    # ========================================================
    print("\n--- Running Experiment 3: Split C (Cross-Source) ---")
    X_train_c = [c["claim_text_normalized"] for c in split_c_train]
    y_train_c = [c["adjudicated_label"] for c in split_c_train]
    X_test_c = [c["claim_text_normalized"] for c in split_c_test]
    y_test_c = [c["adjudicated_label"] for c in split_c_test]

    for m_type in model_types:
        model = BanglaFactClassifier(model_type=m_type, seed=seed)
        model.fit(X_train_c, y_train_c)
        eval_res = model.evaluate(X_test_c, y_test_c)
        results["split_c_cross_source"][m_type] = eval_res
        print(f"Model: {m_type.upper():<5} | Cross-Source Macro-F1: {eval_res['macro_f1']:.4f} | Acc: {eval_res['accuracy']:.4f}")

    rag_c = RAGVerificationSystem(top_k=3, seed=seed)
    rag_c.fit(split_c_train)
    rag_eval_c = rag_c.evaluate(split_c_test)
    results["split_c_cross_source"]["rag"] = rag_eval_c
    print(f"Model: RAG   | Cross-Source Macro-F1: {rag_eval_c['macro_f1']:.4f} | Acc: {rag_eval_c['accuracy']:.4f}")

    # ========================================================
    # EXPERIMENT 4: SPLIT D (TEMPORAL EVALUATION)
    # ========================================================
    print("\n--- Running Experiment 4: Split D (Temporal Shift) ---")
    X_train_d = [c["claim_text_normalized"] for c in split_d_train]
    y_train_d = [c["adjudicated_label"] for c in split_d_train]
    X_test_d = [c["claim_text_normalized"] for c in split_d_test]
    y_test_d = [c["adjudicated_label"] for c in split_d_test]

    for m_type in model_types:
        model = BanglaFactClassifier(model_type=m_type, seed=seed)
        model.fit(X_train_d, y_train_d)
        eval_res = model.evaluate(X_test_d, y_test_d)
        results["split_d_temporal"][m_type] = eval_res
        print(f"Model: {m_type.upper():<5} | Temporal Macro-F1: {eval_res['macro_f1']:.4f} | Acc: {eval_res['accuracy']:.4f}")

    rag_d = RAGVerificationSystem(top_k=3, seed=seed)
    rag_d.fit(split_d_train)
    rag_eval_d = rag_d.evaluate(split_d_test)
    results["split_d_temporal"]["rag"] = rag_eval_d
    print(f"Model: RAG   | Temporal Macro-F1: {rag_eval_d['macro_f1']:.4f} | Acc: {rag_eval_d['accuracy']:.4f}")

    # ========================================================
    # EXPERIMENT 5: SPLIT E (ADVERSARIAL ROBUSTNESS SUITE)
    # ========================================================
    print("\n--- Running Experiment 5: Split E (Adversarial Robustness) ---")
    # Evaluate models trained on Split A against the 6 perturbation subsets
    for m_type in ['svm', 'nb', 'lr', 'rf']:
        model = trained_models[m_type]
        clean_f1 = results["split_a_random"][m_type]["macro_f1"]
        results["split_e_adversarial"][m_type] = {"clean_f1": clean_f1, "perturbations": {}}

        print(f"\nModel {m_type.upper()} Robustness Degradation:")
        for t_type, p_records in adversarial_sets.items():
            trans_texts = [r["transformed_claim_text"] for r in p_records]
            true_lbls = [r["ground_truth_label"] for r in p_records]
            eval_res = model.evaluate(trans_texts, true_lbls)
            
            perturbed_f1 = eval_res["macro_f1"]
            abs_drop = clean_f1 - perturbed_f1
            rel_drop = (abs_drop / clean_f1) * 100 if clean_f1 > 0 else 0.0

            results["split_e_adversarial"][m_type]["perturbations"][t_type] = {
                "perturbed_macro_f1": perturbed_f1,
                "accuracy": eval_res["accuracy"],
                "absolute_drop": round(abs_drop, 4),
                "relative_drop_pct": round(rel_drop, 2)
            }
            print(f"  {t_type:<25} | Perturbed F1: {perturbed_f1:.4f} | Drop: -{abs_drop:.4f} (-{rel_drop:.1f}%)")

    # RAG on Adversarial Split
    clean_rag_f1 = results["split_a_random"]["rag"]["macro_f1"]
    results["split_e_adversarial"]["rag"] = {"clean_f1": clean_rag_f1, "perturbations": {}}
    print(f"\nModel RAG Robustness Degradation:")
    for t_type, p_records in adversarial_sets.items():
        true_lbls = [r["ground_truth_label"] for r in p_records]
        preds = []
        for r in p_records:
            v = rag.verify_claim(r["transformed_claim_text"])
            preds.append(v["label"])
        
        acc = accuracy_score(true_lbls, preds)
        p_m, r_m, f1_m, _ = precision_recall_fscore_support(true_lbls, preds, labels=classes, average='macro', zero_division=0)
        abs_drop = clean_rag_f1 - f1_m
        rel_drop = (abs_drop / clean_rag_f1) * 100 if clean_rag_f1 > 0 else 0.0

        results["split_e_adversarial"]["rag"]["perturbations"][t_type] = {
            "perturbed_macro_f1": round(float(f1_m), 4),
            "accuracy": round(float(acc), 4),
            "absolute_drop": round(abs_drop, 4),
            "relative_drop_pct": round(rel_drop, 2)
        }
        print(f"  {t_type:<25} | Perturbed F1: {f1_m:.4f} | Drop: -{abs_drop:.4f} (-{rel_drop:.1f}%)")

    # ========================================================
    # EXPERIMENT 6: EXPLANATION FAITHFULNESS
    # ========================================================
    print("\n--- Running Experiment 6: Explanation Faithfulness Evaluation ---")
    for m_type in ['svm', 'lr', 'nb']:
        model = trained_models[m_type]
        faith = ExplanationFaithfulnessEvaluator.evaluate_model_faithfulness(model, X_test_a, y_test_a)
        results["faithfulness"][m_type] = faith
        print(f"Model: {m_type.upper():<5} | Sufficiency: {faith['mean_sufficiency']:+.4f} | Comprehensiveness: {faith['mean_comprehensiveness']:+.4f} | Grade: {faith['faithfulness_grade']}")

    # ========================================================
    # EXPERIMENT 7: STATISTICAL SIGNIFICANCE TESTING
    # ========================================================
    print("\n--- Running Experiment 7: Paired Statistical Tests ---")
    svm_preds = results["split_a_random"]["svm"]["predictions"]
    nb_preds = results["split_a_random"]["nb"]["predictions"]
    rag_preds = results["split_a_random"]["rag"]["predictions"]

    test_svm_vs_nb = StatisticalSignificanceTester.mcnemar_test(y_test_a, svm_preds, nb_preds)
    test_rag_vs_svm = StatisticalSignificanceTester.mcnemar_test(y_test_a, rag_preds, svm_preds)

    results["statistical_tests"]["mcnemar_svm_vs_nb"] = test_svm_vs_nb
    results["statistical_tests"]["mcnemar_rag_vs_svm"] = test_rag_vs_svm

    print(f"McNemar (SVM vs NB): chi2={test_svm_vs_nb['statistic']}, p={test_svm_vs_nb['p_value']} ({test_svm_vs_nb['interpretation']})")
    print(f"McNemar (RAG vs SVM): chi2={test_rag_vs_svm['statistic']}, p={test_rag_vs_svm['p_value']} ({test_rag_vs_svm['interpretation']})")

    # Save complete results
    save_json('08_Experiments/results/all_results.json', results)

    # Save summary tables to markdown
    summary_md = f"""# BanglaFactBench Experimental Benchmark Summary
# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 1. Primary Benchmark Results Across All Evaluation Splits

| Model / Pipeline | Random Split A (Macro F1) | Cross-Domain Split B (Macro F1) | Cross-Source Split C (Macro F1) | Temporal Split D (Macro F1) | Expected Calibration Error (ECE) | Brier Score |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Naive Bayes (TF-IDF)** | {results['split_a_random']['nb']['macro_f1']:.4f} | {results['split_b_cross_domain']['nb']['macro_f1']:.4f} | {results['split_c_cross_source']['nb']['macro_f1']:.4f} | {results['split_d_temporal']['nb']['macro_f1']:.4f} | {results['split_a_random']['nb']['ece']:.4f} | {results['split_a_random']['nb']['brier_score']:.4f} |
| **Linear SVM (TF-IDF)** | {results['split_a_random']['svm']['macro_f1']:.4f} | {results['split_b_cross_domain']['svm']['macro_f1']:.4f} | {results['split_c_cross_source']['svm']['macro_f1']:.4f} | {results['split_d_temporal']['svm']['macro_f1']:.4f} | {results['split_a_random']['svm']['ece']:.4f} | {results['split_a_random']['svm']['brier_score']:.4f} |
| **Logistic Regression** | {results['split_a_random']['lr']['macro_f1']:.4f} | {results['split_b_cross_domain']['lr']['macro_f1']:.4f} | {results['split_c_cross_source']['lr']['macro_f1']:.4f} | {results['split_d_temporal']['lr']['macro_f1']:.4f} | {results['split_a_random']['lr']['ece']:.4f} | {results['split_a_random']['lr']['brier_score']:.4f} |
| **Random Forest** | {results['split_a_random']['rf']['macro_f1']:.4f} | {results['split_b_cross_domain']['rf']['macro_f1']:.4f} | {results['split_c_cross_source']['rf']['macro_f1']:.4f} | {results['split_d_temporal']['rf']['macro_f1']:.4f} | {results['split_a_random']['rf']['ece']:.4f} | {results['split_a_random']['rf']['brier_score']:.4f} |
| **RAG Verifier (BM25 + Evidence)** | **{results['split_a_random']['rag']['macro_f1']:.4f}** | **{results['split_b_cross_domain']['rag']['macro_f1']:.4f}** | **{results['split_c_cross_source']['rag']['macro_f1']:.4f}** | **{results['split_d_temporal']['rag']['macro_f1']:.4f}** | **{results['split_a_random']['rag']['ece']:.4f}** | **{results['split_a_random']['rag']['brier_score']:.4f}** |

---

## 2. Adversarial Robustness Degradation Matrix (Split E)

Values denote Macro-F1 on each perturbation subset (parentheses indicate relative drop from clean F1):

| Model | Clean | Typo | Unicode Var | Banglish | Code-Mixing | Paraphrase | Adv Wording | Average Robustness Drop |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Linear SVM** | {results['split_e_adversarial']['svm']['clean_f1']:.4f} | {results['split_e_adversarial']['svm']['perturbations']['typo']['perturbed_macro_f1']:.4f} (-{results['split_e_adversarial']['svm']['perturbations']['typo']['relative_drop_pct']}%) | {results['split_e_adversarial']['svm']['perturbations']['unicode_variation']['perturbed_macro_f1']:.4f} (-{results['split_e_adversarial']['svm']['perturbations']['unicode_variation']['relative_drop_pct']}%) | {results['split_e_adversarial']['svm']['perturbations']['banglish_transliteration']['perturbed_macro_f1']:.4f} (-{results['split_e_adversarial']['svm']['perturbations']['banglish_transliteration']['relative_drop_pct']}%) | {results['split_e_adversarial']['svm']['perturbations']['code_mixing']['perturbed_macro_f1']:.4f} (-{results['split_e_adversarial']['svm']['perturbations']['code_mixing']['relative_drop_pct']}%) | {results['split_e_adversarial']['svm']['perturbations']['paraphrase']['perturbed_macro_f1']:.4f} (-{results['split_e_adversarial']['svm']['perturbations']['paraphrase']['relative_drop_pct']}%) | {results['split_e_adversarial']['svm']['perturbations']['adversarial_wording']['perturbed_macro_f1']:.4f} (-{results['split_e_adversarial']['svm']['perturbations']['adversarial_wording']['relative_drop_pct']}%) | -{np.mean([results['split_e_adversarial']['svm']['perturbations'][t]['relative_drop_pct'] for t in perturbation_types]):.1f}% |
| **RAG Verifier** | {results['split_e_adversarial']['rag']['clean_f1']:.4f} | {results['split_e_adversarial']['rag']['perturbations']['typo']['perturbed_macro_f1']:.4f} (-{results['split_e_adversarial']['rag']['perturbations']['typo']['relative_drop_pct']}%) | {results['split_e_adversarial']['rag']['perturbations']['unicode_variation']['perturbed_macro_f1']:.4f} (-{results['split_e_adversarial']['rag']['perturbations']['unicode_variation']['relative_drop_pct']}%) | {results['split_e_adversarial']['rag']['perturbations']['banglish_transliteration']['perturbed_macro_f1']:.4f} (-{results['split_e_adversarial']['rag']['perturbations']['banglish_transliteration']['relative_drop_pct']}%) | {results['split_e_adversarial']['rag']['perturbations']['code_mixing']['perturbed_macro_f1']:.4f} (-{results['split_e_adversarial']['rag']['perturbations']['code_mixing']['relative_drop_pct']}%) | {results['split_e_adversarial']['rag']['perturbations']['paraphrase']['perturbed_macro_f1']:.4f} (-{results['split_e_adversarial']['rag']['perturbations']['paraphrase']['relative_drop_pct']}%) | {results['split_e_adversarial']['rag']['perturbations']['adversarial_wording']['perturbed_macro_f1']:.4f} (-{results['split_e_adversarial']['rag']['perturbations']['adversarial_wording']['relative_drop_pct']}%) | -{np.mean([results['split_e_adversarial']['rag']['perturbations'][t]['relative_drop_pct'] for t in perturbation_types]):.1f}% |

---

## 3. Explanation Faithfulness Diagnostics (ERASER Protocol)

| Model | Mean Sufficiency (Lower is Better) | Mean Comprehensiveness (Higher is Better) | Rationale Prediction Retention | Faithfulness Classification |
|---|:---:|:---:|:---:|:---:|
| **Linear SVM** | {results['faithfulness']['svm']['mean_sufficiency']:+.4f} | {results['faithfulness']['svm']['mean_comprehensiveness']:+.4f} | {results['faithfulness']['svm']['rationale_prediction_retention_rate']*100:.1f}% | `{results['faithfulness']['svm']['faithfulness_grade']}` |
| **Logistic Regression** | {results['faithfulness']['lr']['mean_sufficiency']:+.4f} | {results['faithfulness']['lr']['mean_comprehensiveness']:+.4f} | {results['faithfulness']['lr']['rationale_prediction_retention_rate']*100:.1f}% | `{results['faithfulness']['lr']['faithfulness_grade']}` |
| **Naive Bayes** | {results['faithfulness']['nb']['mean_sufficiency']:+.4f} | {results['faithfulness']['nb']['mean_comprehensiveness']:+.4f} | {results['faithfulness']['nb']['rationale_prediction_retention_rate']*100:.1f}% | `{results['faithfulness']['nb']['faithfulness_grade']}` |
"""

    summary_path = os.path.join(base_dir, '08_Experiments', 'results', 'summary_table.md')
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary_md.strip() + '\n')

    print(f"\n[{datetime.now().isoformat()}] Master Experiment Suite Completed Successfully!")
    print(f"Results archived to: 08_Experiments/results/all_results.json and {summary_path}")

if __name__ == '__main__':
    main()
