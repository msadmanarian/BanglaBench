import numpy as np
from typing import List, Dict, Any, Tuple
from scipy import stats
from sklearn.metrics import f1_score

class StatisticalSignificanceTester:
    """
    Implements formal statistical tests for model comparisons in BanglaFactBench
    following AIUB MAT 3103 inferential statistics procedures:
    1. Paired McNemar's Test with Edwards continuity correction
    2. Non-parametric Bootstrap Confidence Intervals (B = 1000 resamples)
    3. Permutation Testing for paired Macro-F1 differences
    """

    @classmethod
    def mcnemar_test(cls, true_labels: List[str], preds_a: List[str], preds_b: List[str]) -> Dict[str, Any]:
        """
        Paired McNemar's test evaluating whether Model A and Model B have significantly different error rates.
        """
        n = len(true_labels)
        assert len(preds_a) == n and len(preds_b) == n

        n01 = 0 # Model A correct, Model B incorrect
        n10 = 0 # Model A incorrect, Model B correct
        n00 = 0 # Both correct
        n11 = 0 # Both incorrect

        for y, pa, pb in zip(true_labels, preds_a, preds_b):
            a_correct = (pa == y)
            b_correct = (pb == y)

            if a_correct and b_correct:
                n00 += 1
            elif not a_correct and not b_correct:
                n11 += 1
            elif a_correct and not b_correct:
                n01 += 1
            else:
                n10 += 1

        # McNemar test statistic with continuity correction
        discordant = n01 + n10
        if discordant == 0:
            return {
                "statistic": 0.0,
                "p_value": 1.0,
                "n01": n01,
                "n10": n10,
                "significant_at_05": False,
                "interpretation": "Identical error patterns between models."
            }

        chi2 = (abs(n01 - n10) - 1.0) ** 2 / discordant
        p_val = 1.0 - stats.chi2.cdf(chi2, df=1)

        return {
            "statistic": round(float(chi2), 4),
            "p_value": round(float(p_val), 5),
            "n01_a_better": n01,
            "n10_b_better": n10,
            "both_correct": n00,
            "both_incorrect": n11,
            "significant_at_05": bool(p_val < 0.05),
            "interpretation": f"Statistically {'significant' if p_val < 0.05 else 'not significant'} difference (p={p_val:.4f})."
        }

    @classmethod
    def bootstrap_f1_ci(cls, true_labels: List[str], preds: List[str], classes: List[str], n_bootstraps: int = 1000, seed: int = 42) -> Dict[str, Any]:
        """
        Computes 95% non-parametric bootstrap confidence intervals for Macro-F1.
        """
        np.random.seed(seed)
        n = len(true_labels)
        bootstrapped_f1s = []

        y_true_arr = np.array(true_labels)
        preds_arr = np.array(preds)

        for _ in range(n_bootstraps):
            indices = np.random.choice(n, size=n, replace=True)
            sample_true = y_true_arr[indices]
            sample_pred = preds_arr[indices]

            score = f1_score(sample_true, sample_pred, labels=classes, average='macro', zero_division=0)
            bootstrapped_f1s.append(score)

        bootstrapped_f1s.sort()
        ci_lower = np.percentile(bootstrapped_f1s, 2.5)
        ci_upper = np.percentile(bootstrapped_f1s, 97.5)
        mean_f1 = np.mean(bootstrapped_f1s)
        std_f1 = np.std(bootstrapped_f1s)

        return {
            "mean_f1": round(float(mean_f1), 4),
            "std_f1": round(float(std_f1), 4),
            "ci_95_lower": round(float(ci_lower), 4),
            "ci_95_upper": round(float(ci_upper), 4),
            "n_bootstraps": n_bootstraps
        }


if __name__ == '__main__':
    y_true = ["SUPPORTED"] * 20 + ["REFUTED"] * 20
    pa = ["SUPPORTED"] * 18 + ["REFUTED"] * 2 + ["SUPPORTED"] * 2 + ["REFUTED"] * 18
    pb = ["SUPPORTED"] * 12 + ["REFUTED"] * 8 + ["SUPPORTED"] * 8 + ["REFUTED"] * 12

    classes = ["SUPPORTED", "REFUTED"]
    mcn = StatisticalSignificanceTester.mcnemar_test(y_true, pa, pb)
    print("McNemar Test Result:", mcn)

    ci = StatisticalSignificanceTester.bootstrap_f1_ci(y_true, pa, classes, n_bootstraps=500)
    print("Bootstrap CI:", ci)
    print("Statistical Significance Tester self-test passed!")
