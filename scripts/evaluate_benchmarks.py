"""
Benchmark Evaluation Script.
Evaluates the minimal runnable submission using a document-level cross-validation split
on the approved benchmark dataset with documented provenance.
Computes: QWK, MAE, Exact Accuracy, Macro Precision, Latency per document, Memory per document.
"""

import json
from pathlib import Path
import sys
import time
import tracemalloc
import numpy as np
from sklearn.metrics import cohen_kappa_score, mean_absolute_error, accuracy_score, precision_score
from sklearn.model_selection import KFold

# Add all package src directories to Python path
ROOT_DIR = Path(__file__).resolve().parents[1]
for pkg in ["core", "document_processing", "ml_inference", "retrieval", "agent_orchestration", "competition_engine"]:
    pkg_src = ROOT_DIR / "packages" / pkg / "src"
    if pkg_src.exists() and str(pkg_src) not in sys.path:
        sys.path.insert(0, str(pkg_src))

from document_processing.extractor import DocumentExtractor
from ml_inference.classifier import TRLOrdinalClassifier
from ml_inference.features import FeatureExtractor


def load_benchmark_dataset(provenance_path: Path):
    """Load benchmark documents and verified ground-truth TRL labels."""
    with open(provenance_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    extractor = DocumentExtractor()
    feat_extractor = FeatureExtractor()

    documents = []
    features_list = []
    y_labels = []
    doc_ids = []

    for item in records:
        file_path = provenance_path.parent / item["filename"]
        doc = extractor.extract_from_file(file_path)
        evidence_items = feat_extractor.extract_evidence(doc)
        feat_vec, _ = feat_extractor.extract_features(doc, evidence_items)

        documents.append(doc)
        features_list.append(feat_vec)
        y_labels.append(int(item["certified_trl"]))
        doc_ids.append(item["document_id"])

    X = np.vstack(features_list)
    y = np.array(y_labels, dtype=np.int32)
    return doc_ids, documents, X, y, records


def evaluate_system():
    provenance_file = ROOT_DIR / "data" / "approved_benchmarks" / "provenance.json"
    if not provenance_file.exists():
        raise FileNotFoundError(f"Provenance file not found: {provenance_file}")

    doc_ids, documents, X, y, records = load_benchmark_dataset(provenance_file)
    n_samples = len(y)

    print(f"Loaded {n_samples} approved benchmark documents with verified provenance.")

    # Document-level 3-Fold Cross-Validation to guarantee no document leakage
    kf = KFold(n_splits=3, shuffle=True, random_state=42)

    y_true_all = []
    y_pred_all = []
    evaluated_doc_ids = []
    latencies_ms = []
    peak_memories_kb = []

    feat_extractor = FeatureExtractor()

    for fold, (train_idx, test_idx) in enumerate(kf.split(X)):
        X_train, y_train = X[train_idx], y[train_idx]
        X_test, y_test = X[test_idx], y[test_idx]

        # Train ordinal model on train split
        classifier = TRLOrdinalClassifier()
        classifier.fit(X_train, y_train)

        # Evaluate on test split
        for idx in test_idx:
            doc = documents[idx]
            feat_vec = X[idx]

            # Measure latency and memory per document
            tracemalloc.start()
            t0 = time.perf_counter()

            evidence_items = feat_extractor.extract_evidence(doc)
            assessment = classifier.adjudicate(doc, evidence_items, feat_vec)

            t1 = time.perf_counter()
            _, peak_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            latency_ms = (t1 - t0) * 1000.0
            memory_kb = peak_mem / 1024.0

            latencies_ms.append(latency_ms)
            peak_memories_kb.append(memory_kb)

            y_true_all.append(y[idx])
            y_pred_all.append(assessment.predicted_trl)
            evaluated_doc_ids.append(doc_ids[idx])

    y_true_all = np.array(y_true_all)
    y_pred_all = np.array(y_pred_all)

    # Compute metrics
    qwk = cohen_kappa_score(y_true_all, y_pred_all, weights="quadratic")
    mae = mean_absolute_error(y_true_all, y_pred_all)
    exact_acc = accuracy_score(y_true_all, y_pred_all)
    macro_prec = precision_score(y_true_all, y_pred_all, average="macro", zero_division=0)
    avg_latency = float(np.mean(latencies_ms))
    avg_memory = float(np.mean(peak_memories_kb))

    results = {
        "n_documents": n_samples,
        "evaluation_strategy": "Document-Level 3-Fold Cross-Validation",
        "qwk": round(float(qwk), 4),
        "mae": round(float(mae), 4),
        "exact_accuracy": round(float(exact_acc), 4),
        "macro_precision": round(float(macro_prec), 4),
        "avg_latency_ms": round(avg_latency, 2),
        "avg_memory_kb": round(avg_memory, 2),
        "per_document_predictions": [
            {
                "doc_id": evaluated_doc_ids[i],
                "ground_truth_trl": int(y_true_all[i]),
                "predicted_trl": int(y_pred_all[i]),
                "latency_ms": round(latencies_ms[i], 2),
                "memory_kb": round(peak_memories_kb[i], 2),
            }
            for i in range(n_samples)
        ]
    }

    report_path = ROOT_DIR / "docs" / "local_validation_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\n================ LOCAL VALIDATION REPORT ================")
    print(f"Sample Count (n):       {results['n_documents']}")
    print(f"Quadratic Weighted Kappa (QWK): {results['qwk']}")
    print(f"Mean Absolute Error (MAE):      {results['mae']}")
    print(f"Exact Accuracy:                 {results['exact_accuracy'] * 100:.1f}%")
    print(f"Macro Precision:                {results['macro_precision'] * 100:.1f}%")
    print(f"Avg Latency per Document:       {results['avg_latency_ms']} ms")
    print(f"Avg Memory per Document:        {results['avg_memory_kb']} KB")
    print("=========================================================\n")
    return results


if __name__ == "__main__":
    evaluate_system()
