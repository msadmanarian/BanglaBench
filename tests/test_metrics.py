import pytest
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src', 'evaluation'))
from metrics import BenchmarkMetrics

def test_ece_computation():
    y_true = ["REFUTED", "SUPPORTED", "REFUTED", "SUPPORTED"]
    # Model probabilities for 5 classes
    classes = ["SUPPORTED", "REFUTED", "UNVERIFIABLE", "MISLEADING", "OPINION"]
    # Perfectly confident & correct
    probs = np.zeros((4, 5))
    probs[0, 1] = 1.0  # REFUTED
    probs[1, 0] = 1.0  # SUPPORTED
    probs[2, 1] = 1.0  # REFUTED
    probs[3, 0] = 1.0  # SUPPORTED

    ece = BenchmarkMetrics.compute_ece(y_true, probs, classes=classes, n_bins=5)
    assert ece >= 0.0
    assert ece <= 1.0

def test_brier_score_computation():
    y_true = ["REFUTED", "SUPPORTED"]
    classes = ["SUPPORTED", "REFUTED", "UNVERIFIABLE", "MISLEADING", "OPINION"]
    probs = np.zeros((2, 5))
    probs[0, 1] = 1.0
    probs[1, 0] = 1.0
    bs = BenchmarkMetrics.compute_brier_score(y_true, probs, classes=classes)
    assert bs == 0.0  # Perfect Brier score is 0.0
