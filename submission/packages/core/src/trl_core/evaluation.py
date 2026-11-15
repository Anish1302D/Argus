"""
Scientific Evaluation Framework & Reliability Metrics Engine.
Computes standard statistical and ordinal ranking evaluation metrics:
- Quadratic Weighted Kappa (QWK)
- Mean Absolute Error (MAE)
- Exact Accuracy & Adjacent-Level Accuracy
- Per-TRL Precision, Recall, and Confusion Matrix
- Expected Calibration Error (ECE) and Brier Score
"""

import math
from typing import Any, Dict, List, Tuple
import numpy as np


def mean_absolute_error(y_true: List[int], y_pred: List[int]) -> float:
    """Compute Mean Absolute Error."""
    if not y_true or len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must be non-empty lists of identical length")
    return float(np.mean(np.abs(np.array(y_true) - np.array(y_pred))))


def exact_accuracy(y_true: List[int], y_pred: List[int]) -> float:
    """Compute Exact Match Accuracy."""
    if not y_true or len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must be non-empty lists of identical length")
    return float(np.mean(np.array(y_true) == np.array(y_pred)))


def adjacent_accuracy(y_true: List[int], y_pred: List[int], tolerance: int = 1) -> float:
    """Compute Adjacent-Level Accuracy (|y_true - y_pred| <= tolerance)."""
    if not y_true or len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must be non-empty lists of identical length")
    diffs = np.abs(np.array(y_true) - np.array(y_pred))
    return float(np.mean(diffs <= tolerance))


def confusion_matrix(y_true: List[int], y_pred: List[int], num_classes: int = 9) -> np.ndarray:
    """Compute (num_classes x num_classes) confusion matrix for TRL 1 to num_classes."""
    matrix = np.zeros((num_classes, num_classes), dtype=int)
    for t, p in zip(y_true, y_pred):
        if 1 <= t <= num_classes and 1 <= p <= num_classes:
            matrix[t - 1, p - 1] += 1
    return matrix


def quadratic_weighted_kappa(y_true: List[int], y_pred: List[int], min_rating: int = 1, max_rating: int = 9) -> float:
    """
    Compute Quadratic Weighted Kappa (QWK) for ordinal TRL evaluation.
    Matches standard Cohen's kappa with quadratic penalty: w_ij = (i - j)^2 / (N - 1)^2.
    """
    if not y_true or len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must be non-empty lists of identical length")

    num_ratings = max_rating - min_rating + 1
    if len(set(y_true)) <= 1 and len(set(y_pred)) <= 1 and y_true[0] == y_pred[0]:
        return 1.0  # Perfect agreement on constant array

    # Build observed matrix
    O = confusion_matrix(y_true, y_pred, num_classes=num_ratings)

    # Marginal sums
    hist_true = np.sum(O, axis=1)
    hist_pred = np.sum(O, axis=0)
    total_samples = float(len(y_true))

    if total_samples == 0:
        return 0.0

    # Build expected matrix under chance agreement
    E = np.outer(hist_true, hist_pred) / total_samples

    # Build quadratic weight matrix
    W = np.zeros((num_ratings, num_ratings), dtype=float)
    denominator_norm = float((num_ratings - 1) ** 2) if num_ratings > 1 else 1.0
    for i in range(num_ratings):
        for j in range(num_ratings):
            W[i, j] = ((i - j) ** 2) / denominator_norm

    # Calculate weighted sums
    numerator = np.sum(W * O)
    denominator = np.sum(W * E)

    if denominator == 0:
        return 1.0 if numerator == 0 else 0.0

    qwk = 1.0 - (numerator / denominator)
    return float(np.clip(qwk, -1.0, 1.0))


def expected_calibration_error(
    y_true: List[int],
    y_pred: List[int],
    confidences: List[float],
    n_bins: int = 5,
) -> float:
    """
    Compute Expected Calibration Error (ECE) across confidence bins.
    """
    if not (len(y_true) == len(y_pred) == len(confidences)):
        raise ValueError("Lengths of y_true, y_pred, and confidences must match")

    n = len(y_true)
    if n == 0:
        return 0.0

    bin_boundaries = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0

    correct = (np.array(y_true) == np.array(y_pred)).astype(float)
    confs = np.array(confidences, dtype=float)

    for i in range(n_bins):
        in_bin = (confs > bin_boundaries[i]) & (confs <= bin_boundaries[i + 1])
        bin_size = np.sum(in_bin)
        if bin_size > 0:
            bin_acc = np.mean(correct[in_bin])
            bin_conf = np.mean(confs[in_bin])
            ece += (bin_size / n) * abs(bin_acc - bin_conf)

    return float(ece)


def brier_score(y_true: List[int], y_pred: List[int], confidences: List[float]) -> float:
    """Compute Brier Score for probability calibration."""
    if not (len(y_true) == len(y_pred) == len(confidences)):
        raise ValueError("Lengths of y_true, y_pred, and confidences must match")
    correct = (np.array(y_true) == np.array(y_pred)).astype(float)
    confs = np.array(confidences, dtype=float)
    return float(np.mean((confs - correct) ** 2))
