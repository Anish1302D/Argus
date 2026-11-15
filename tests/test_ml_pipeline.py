"""
Unit Tests for ML Pipeline: DocumentExtractor, FeatureExtractor, and TRLOrdinalClassifier.
"""

from pathlib import Path
import numpy as np
import pytest

from document_processing.extractor import DocumentExtractor
from ml_inference.classifier import TRLOrdinalClassifier
from ml_inference.features import FeatureExtractor
from trl_core.models import Chunk, Document, EvidenceCategory, EvidenceStrength


def test_document_extractor_pdf(sample_synthetic_pdf: Path):
    """Test PDF extraction on synthetic unit-test fixture."""
    assert sample_synthetic_pdf.exists()

    extractor = DocumentExtractor()
    doc = extractor.extract_from_file(sample_synthetic_pdf)

    assert doc.id == "synthetic_test_doc"
    assert doc.metadata["format"] == "pdf"
    assert doc.metadata["page_count"] == 1
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

    # 1. Test Pure Deterministic Rule-Based Adjudicator (Submission Mode)
    det_classifier = TRLOrdinalClassifier(enable_ml=False)
    det_assessment = det_classifier.adjudicate(doc, evidence_items, feat_vec)
    assert 1 <= det_assessment.predicted_trl <= 9
    assert 0.5 <= det_assessment.confidence <= 1.0
    assert "Deterministic rule-based adjudication" in det_assessment.justification
    assert len(det_assessment.satisfied_criteria) > 0
    assert len(det_assessment.recommendations) > 0

    # 2. Test ML-Enabled Adjudicator with synthetic unit test vectors
    ml_classifier = TRLOrdinalClassifier()
    fallback_score = ml_classifier.predict_score(feat_vec.reshape(1, -1))
    assert 1.0 <= fallback_score[0] <= 9.0

    X_train = np.vstack([feat_vec, feat_vec * 0.5, feat_vec * 1.5])
    y_train = np.array([4.0, 2.0, 6.0], dtype=np.float32)
    ml_classifier.fit(X_train, y_train)

    assert ml_classifier.is_fitted is True
    pred_score = ml_classifier.predict_score(feat_vec.reshape(1, -1))
    assert 1.0 <= pred_score[0] <= 9.0

    ml_assessment = ml_classifier.adjudicate(doc, evidence_items, feat_vec)
    assert 1 <= ml_assessment.predicted_trl <= 9
    assert 0.0 <= ml_assessment.confidence <= 1.0

def _document_from_text(text: str) -> Document:
    """Build a one-chunk document for focused evidence-mining regression tests."""
    chunk = Chunk(
        id="negation_chunk_001",
        document_id="negation_regression",
        text=text,
        page_number=1,
        section_name=None,
        char_offset_start=0,
        char_offset_end=len(text),
        is_sanitized=True,
    )
    return Document(
        id="negation_regression",
        name="negation-regression.txt",
        raw_content=text,
        chunks=[chunk],
        metadata={"format": "txt", "page_count": 1},
    )


def test_feature_extractor_ignores_negated_flight_demonstration():
    text = (
        "The system has not yet undergone actual suborbital sounding rocket "
        "flight demonstration (TRL 7)."
    )
    extractor = FeatureExtractor()
    document = _document_from_text(text)

    evidence = extractor.extract_evidence(document)
    feature_vector, feature_names = extractor.extract_features(document, evidence)

    assert not any(item.target_trl == 7 for item in evidence)
    assert feature_vector[feature_names.index("trl_7_keyword_freq")] == 0
    assert feature_vector[feature_names.index("highest_matched_trl")] == 1


def test_feature_extractor_ignores_absent_lab_and_breadboard_milestones():
    text = (
        "No laboratory experiment, simulation, breadboard, or hardware "
        "prototype has been constructed or tested."
    )
    extractor = FeatureExtractor()
    document = _document_from_text(text)

    evidence = extractor.extract_evidence(document)
    feature_vector, feature_names = extractor.extract_features(document, evidence)

    assert not any(item.target_trl in (3, 4) for item in evidence)
    assert feature_vector[feature_names.index("trl_3_keyword_freq")] == 0
    assert feature_vector[feature_names.index("trl_4_keyword_freq")] == 0


def test_feature_extractor_keeps_positive_flight_demonstration_evidence():
    text = (
        "A full system prototype completed a successful flight demonstration "
        "during the operational test campaign."
    )
    extractor = FeatureExtractor()
    document = _document_from_text(text)

    evidence = extractor.extract_evidence(document)

    assert any(item.target_trl == 7 for item in evidence)


def test_feature_extractor_detects_postposed_milestone_negation():
    text = "The flight demonstration was not performed; only a lab test was completed."
    extractor = FeatureExtractor()
    document = _document_from_text(text)

    evidence = extractor.extract_evidence(document)

    assert not any(item.target_trl == 7 for item in evidence)

