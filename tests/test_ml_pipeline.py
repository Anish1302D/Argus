"""
Unit Tests for ML Pipeline: DocumentExtractor, FeatureExtractor, and TRLOrdinalClassifier.
"""

from pathlib import Path
import numpy as np
import pytest

from document_processing.extractor import DocumentExtractor
from ml_inference.classifier import TRLOrdinalClassifier
from ml_inference.features import FeatureExtractor
from trl_core.models import Document, EvidenceCategory, EvidenceStrength


def test_document_extractor_pdf():
    pdf_path = Path("docs/official/APCTT_Hackathon_1_compressed.pdf")
    assert pdf_path.exists()

    extractor = DocumentExtractor()
    doc = extractor.extract_from_file(pdf_path)

    assert doc.id == "APCTT_Hackathon_1_compressed"
    assert doc.metadata["format"] == "pdf"
    assert doc.metadata["page_count"] == 4
    assert len(doc.chunks) > 0
    assert "Technology Readiness Levels" in doc.raw_content


def test_feature_extractor_mining(sample_valid_paper: Path):
    extractor = DocumentExtractor()
    doc = extractor.extract_from_file(sample_valid_paper)

    feat_extractor = FeatureExtractor()
    evidence_items = feat_extractor.extract_evidence(doc)

    assert len(evidence_items) >= 1
    # Check that at least one evidence item has target_trl >= 3 (lab experiment or validation)
    target_trls = [e.target_trl for e in evidence_items if e.target_trl is not None]
    assert any(t in [3, 4] for t in target_trls)

    feat_vec, feat_names = feat_extractor.extract_features(doc, evidence_items)
    assert feat_vec.shape == (25,)
    assert len(feat_names) == 25
    assert "highest_matched_trl" in feat_names


def test_ordinal_classifier_fit_and_predict(sample_valid_paper: Path):
    extractor = DocumentExtractor()
    doc = extractor.extract_from_file(sample_valid_paper)

    feat_extractor = FeatureExtractor()
    evidence_items = feat_extractor.extract_evidence(doc)
    feat_vec, _ = feat_extractor.extract_features(doc, evidence_items)

    classifier = TRLOrdinalClassifier()
    # Test heuristic fallback before fitting
    fallback_score = classifier.predict_score(feat_vec.reshape(1, -1))
    assert 1.0 <= fallback_score[0] <= 9.0

    # Fit on synthetic calibration batch
    X_train = np.vstack([feat_vec, feat_vec * 0.5, feat_vec * 1.5])
    y_train = np.array([4.0, 2.0, 6.0], dtype=np.float32)
    classifier.fit(X_train, y_train)

    assert classifier.is_fitted is True
    pred_score = classifier.predict_score(feat_vec.reshape(1, -1))
    assert 1.0 <= pred_score[0] <= 9.0

    # Test adjudication
    assessment = classifier.adjudicate(doc, evidence_items, feat_vec)
    assert 1 <= assessment.predicted_trl <= 9
    assert 0.0 <= assessment.confidence <= 1.0
    assert len(assessment.satisfied_criteria) > 0
    assert len(assessment.recommendations) > 0
