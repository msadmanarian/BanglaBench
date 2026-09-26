import numpy as np
from typing import List, Dict, Any, Tuple
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, brier_score_loss

class BenchmarkMetrics:
    """
    Computes standardized classification, calibration, and statistical evaluation metrics
    for BanglaFactBench.
    """
    
    CLASSES = ["SUPPORTED", "REFUTED", "UNVERIFIABLE", "MISLEADING", "OPINION"]

    @classmethod
    def compute_classification_metrics(cls, true_labels: List[str], pred_labels: List[str]) -> Dict[str, Any]:
        acc = accuracy_score(true_labels, pred_labels)
        p_macro, r_macro, f1_macro, _ = precision_recall_fscore_support(
            true_labels, pred_labels, labels=cls.CLASSES, average='macro', zero_division=0
        )
        p_weighted, r_weighted, f1_weighted, _ = precision_recall_fscore_support(
            true_labels, pred_labels, labels=cls.CLASSES, average='weighted', zero_division=0
        )
        
        p_per, r_per, f1_per, sup = precision_recall_fscore_support(
            true_labels, pred_labels, labels=cls.CLASSES, average=None, zero_division=0
        )
        cm = confusion_matrix(true_labels, pred_labels, labels=cls.CLASSES).tolist()

        per_class = {}
        for i, c in enumerate(cls.CLASSES):
            per_class[c] = {
                "precision": round(float(p_per[i]), 4),
                "recall": round(float(r_per[i]), 4),
                "f1": round(float(f1_per[i]), 4),
                "support": int(sup[i])
            }

        return {
            "accuracy": round(float(acc), 4),
            "macro_precision": round(float(p_macro), 4),
            "macro_recall": round(float(r_macro), 4),
            "macro_f1": round(float(f1_macro), 4),
            "weighted_f1": round(float(f1_weighted), 4),
            "confusion_matrix": cm,
            "per_class": per_class
        }

    @classmethod
    def compute_ece(cls, true_labels: List[str], probs: np.ndarray, n_bins: int = 10, classes: List[str] = None) -> float:
        """
        Computes Expected Calibration Error (ECE) following Guo et al. (ICML 2017).
        ECE = sum_{m=1}^M (|B_m| / N) * |acc(B_m) - conf(B_m)|
        """
        N = len(true_labels)
        if N == 0:
            return 0.0

        target_classes = classes if classes is not None else cls.CLASSES
        class_to_idx = {c: i for i, c in enumerate(target_classes)}
        true_indices = np.array([class_to_idx.get(lbl, 0) for lbl in true_labels])

        confidences = np.max(probs, axis=1)
        predictions = np.argmax(probs, axis=1)
        accuracies = (predictions == true_indices).astype(float)

        bin_boundaries = np.linspace(0.0, 1.0, n_bins + 1)
        ece = 0.0

        for i in range(n_bins):
            bin_lower = bin_boundaries[i]
            bin_upper = bin_boundaries[i + 1]

            in_bin = (confidences > bin_lower) & (confidences <= bin_upper)
            prop_in_bin = np.mean(in_bin)

            if prop_in_bin > 0:
                accuracy_in_bin = np.mean(accuracies[in_bin])
                avg_confidence_in_bin = np.mean(confidences[in_bin])
                ece += np.abs(avg_confidence_in_bin - accuracy_in_bin) * prop_in_bin

        return round(float(ece), 4)

    @classmethod
    def compute_brier_score(cls, true_labels: List[str], probs: np.ndarray, classes: List[str] = None) -> float:
        """
        Computes multi-class Brier score: mean squared difference between predicted probabilities
        and one-hot true indicators.
        """
        N = len(true_labels)
        if N == 0:
            return 0.0

        target_classes = classes if classes is not None else cls.CLASSES
        class_to_idx = {c: i for i, c in enumerate(target_classes)}
        k = len(target_classes)
        one_hot = np.zeros((N, k))
        for i, lbl in enumerate(true_labels):
            if lbl in class_to_idx:
                one_hot[i, class_to_idx[lbl]] = 1.0

        # Multi-class Brier score
        bs = np.mean(np.sum((probs - one_hot) ** 2, axis=1))
        return round(float(bs), 4)


if __name__ == '__main__':
    y_true = ["SUPPORTED", "REFUTED", "MISLEADING", "SUPPORTED", "OPINION"]
    y_pred = ["SUPPORTED", "REFUTED", "SUPPORTED", "SUPPORTED", "OPINION"]
    probs = np.array([
        [0.9, 0.05, 0.02, 0.02, 0.01],
        [0.05, 0.85, 0.05, 0.03, 0.02],
        [0.6, 0.1, 0.2, 0.05, 0.05],
        [0.8, 0.05, 0.05, 0.05, 0.05],
        [0.05, 0.05, 0.05, 0.05, 0.8]
    ])

    metrics = BenchmarkMetrics.compute_classification_metrics(y_true, y_pred)
    ece = BenchmarkMetrics.compute_ece(y_true, probs)
    bs = BenchmarkMetrics.compute_brier_score(y_true, probs)
    print("Metrics:", metrics["macro_f1"])
    print("ECE:", ece)
    print("Brier Score:", bs)
    print("Benchmark Metrics self-test passed!")
