"""
Competition Inference Runner.
Execution logic for standalone, air-gapped inference on technical documentation.
Wires together DocumentExtractor, FeatureExtractor, and TRLOrdinalClassifier.
"""

from pathlib import Path
from typing import Optional, Union

from document_processing.extractor import DocumentExtractor
from ml_inference.classifier import TRLOrdinalClassifier
from ml_inference.features import FeatureExtractor
from trl_core.adapters.internal_adapter import InternalOutputAdapter
from trl_core.models import FinalAssessment
from trl_core.sanitizer import sanitize_text


# Shared singleton classifier instance
_CLASSIFIER: Optional[TRLOrdinalClassifier] = None


def get_classifier() -> TRLOrdinalClassifier:
    """Retrieve or initialize the ordinal classifier instance."""
    global _CLASSIFIER
    if _CLASSIFIER is None:
        _CLASSIFIER = TRLOrdinalClassifier()
    return _CLASSIFIER


def run_pipeline(
    input_path: Union[str, Path],
    output_path: Optional[Union[str, Path]] = None,
    strict_security: bool = False
) -> FinalAssessment:
    """
    Execute the standalone competition inference pipeline:
    Official Input -> Ingestion -> Evidence & Keyword Features -> Embeddings / Features -> Ordinal Classifier + Deterministic Rules -> Output Adapter.
    """
    path = Path(input_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Input path does not exist: {path}")

    # 1. Ingestion via pypdfium2 / plain text extractor
    extractor = DocumentExtractor()
    document = extractor.extract_from_file(path)

    # 2. Untrusted Data Security Inspection
    detected_threats = []
    for chunk in document.chunks:
        sanitized = sanitize_text(chunk.text)
        if not sanitized.is_safe:
            detected_threats.extend(sanitized.detected_threats)

    if detected_threats and strict_security:
        raise ValueError(f"Security Alert: Document rejected due to detected prompt injection threats: {set(detected_threats)}")

    # 3. Evidence Mining & Feature Extraction
    feat_extractor = FeatureExtractor()
    evidence_items = feat_extractor.extract_evidence(document)
    feature_vector, _ = feat_extractor.extract_features(document, evidence_items)

    # 4. Ordinal Classification & Deterministic Rule Adjudication
    classifier = get_classifier()
    assessment = classifier.adjudicate(
        document=document,
        evidence_items=evidence_items,
        feature_vector=feature_vector
    )

    # 5. Output via Adapter
    if output_path is not None:
        out_adapter = InternalOutputAdapter()
        out_adapter.write_assessment(assessment, output_path)

    return assessment
