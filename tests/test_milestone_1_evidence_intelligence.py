"""
Unit Tests for Milestone 1: Evidence Intelligence Engine (Issues 01-05).
Covers technical claim extraction, quantitative measurements, modality, negation,
evidence quality evaluation, contradiction detection, and uncertainty modeling.
"""

import pytest
from trl_core.evidence_quality import EvidenceQualityAssessor
from trl_core.contradiction import ContradictionDetector
from trl_core.models import (
    Chunk,
    ContradictionItem,
    EvidenceCategory,
    EvidenceItem,
    EvidenceStrength,
    EvidenceType,
    ModalityType,
    QuantitativeMeasurement,
    TechnicalClaim,
    TemporalStatus,
    ValidationEnvironment,
)
from trl_core.uncertainty import UncertaintyModel
from ml_inference.claim_extractor import StructuredClaimExtractor
from ml_inference.modality import ModalityAnalyzer


def test_issue_01_structured_claim_and_measurement_extraction():
    """Verify structured claim extraction with quantitative measurements and scientific units."""
    extractor = StructuredClaimExtractor()

    text = "Signal-to-noise ratio exceeded 42 dB across 50 discrete test runs with sensitivity of 0.5 ppb."
    measurements = extractor.extract_measurements(text)
    assert len(measurements) >= 2

    units = [m.unit for m in measurements]
    assert "db" in units
    assert "ppb" in units

    chunk = Chunk(
        id="chunk_test_01",
        document_id="doc_test",
        text="Bench-scale laboratory experiments were performed over 120 hours of continuous operation with 340 MPa flexural strength.",
        page_number=1,
        section_name="Results",
        char_offset_start=0,
        char_offset_end=125,
    )
    claims = extractor.extract_claims_from_chunk(chunk)
    assert len(claims) >= 1
    claim = claims[0]
    assert claim.candidate_trl in (3, 4, 6)
    assert len(claim.measurements) >= 1
    assert claim.validation_environment == ValidationEnvironment.LABORATORY
    assert claim.verbatim_quote != ""


def test_issue_02_negation_and_modality_classification():
    """Verify linguistic classification of completed vs planned vs negated milestones."""
    analyzer = ModalityAnalyzer()

    # 1. Negated milestone
    sentence_neg = "the system has not yet undergone actual suborbital sounding rocket flight demonstration (TRL 7)."
    mod, temp = analyzer.analyze_claim_modality(sentence_neg, "flight demonstration")
    assert mod == ModalityType.NEGATED
    assert not analyzer.is_claim_satisfiable(mod, temp)

    # 2. Planned future milestone
    sentence_plan = "Future work will focus on integrating components into a compact enclosure for flight testing (TRL 5)."
    mod, temp = analyzer.analyze_claim_modality(sentence_plan, "flight testing")
    assert mod == ModalityType.PLANNED
    assert temp == TemporalStatus.FUTURE_PROPOSED
    assert not analyzer.is_claim_satisfiable(mod, temp)

    # 3. Hypothetical milestone
    sentence_hypo = "This architecture could theoretically achieve operational satellite deployment."
    mod, temp = analyzer.analyze_claim_modality(sentence_hypo, "operational")
    assert mod == ModalityType.HYPOTHETICAL
    assert not analyzer.is_claim_satisfiable(mod, temp)

    # 4. Completed verified milestone
    sentence_comp = "Optical breadboard bench-scale validation was completed over 120 hours in a laboratory environment."
    mod, temp = analyzer.analyze_claim_modality(sentence_comp, "laboratory")
    assert mod == ModalityType.COMPLETED
    assert temp == TemporalStatus.PAST_VERIFIED
    assert analyzer.is_claim_satisfiable(mod, temp)


def test_issue_03_evidence_quality_and_strength_assessment():
    """Verify evidence strength grading downweights ungrounded claims."""
    assessor = EvidenceQualityAssessor()

    # Quantitative claim with measurements
    claim_strong = TechnicalClaim(
        id="CLAIM-001",
        document_id="doc_1",
        chunk_id="chunk_1",
        text="Bench tests ran for 120 hours with 42 dB SNR in controlled laboratory environment.",
        candidate_trl=4,
        achievement_category="Laboratory Validation",
        measurements=[
            QuantitativeMeasurement(metric="Time", value=120.0, unit="hours", raw_text="120 hours"),
            QuantitativeMeasurement(metric="SNR", value=42.0, unit="db", raw_text="42 dB"),
        ],
        validation_environment=ValidationEnvironment.LABORATORY,
        modality=ModalityType.COMPLETED,
        temporal_status=TemporalStatus.PAST_VERIFIED,
        evidence_type=EvidenceType.EMPIRICAL,
        verbatim_quote="laboratory",
        char_offset_start=0,
        char_offset_end=85,
    )
    strength = assessor.assess_claim_quality(claim_strong)
    assert strength == EvidenceStrength.STRONG_SUPPORTING
    assert assessor.score_extraction_confidence(claim_strong, strength) >= 0.90

    # Vague claim without numbers
    claim_weak = TechnicalClaim(
        id="CLAIM-002",
        document_id="doc_1",
        chunk_id="chunk_1",
        text="System prototype might be useful for flight demonstration.",
        candidate_trl=7,
        achievement_category="Operational Demonstration",
        measurements=[],
        validation_environment=ValidationEnvironment.UNSPECIFIED,
        modality=ModalityType.HYPOTHETICAL,
        temporal_status=TemporalStatus.FUTURE_PROPOSED,
        evidence_type=EvidenceType.SPECIFICATION,
        verbatim_quote="flight demonstration",
        char_offset_start=0,
        char_offset_end=58,
    )
    strength_weak = assessor.assess_claim_quality(claim_weak)
    assert strength_weak == EvidenceStrength.UNVERIFIED_CLAIM


def test_issue_04_contradictory_evidence_detection():
    """Verify detection of conflicting statements between abstract claims and limitation disclosures."""
    detector = ContradictionDetector()

    claim_pos = TechnicalClaim(
        id="CLAIM-POS-01",
        document_id="doc_tps",
        chunk_id="chunk_0",
        text="Demonstrated flight demonstration capability for hypersonic re-entry.",
        candidate_trl=7,
        achievement_category="Flight Demonstration",
        measurements=[],
        validation_environment=ValidationEnvironment.OPERATIONAL_SPACE_OR_FLIGHT,
        modality=ModalityType.COMPLETED,
        temporal_status=TemporalStatus.PAST_VERIFIED,
        evidence_type=EvidenceType.EMPIRICAL,
        verbatim_quote="flight demonstration",
        char_offset_start=0,
        char_offset_end=70,
    )

    claim_neg = TechnicalClaim(
        id="CLAIM-NEG-01",
        document_id="doc_tps",
        chunk_id="chunk_4",
        text="The system has not yet undergone actual suborbital sounding rocket flight demonstration.",
        candidate_trl=7,
        achievement_category="Flight Demonstration",
        measurements=[],
        validation_environment=ValidationEnvironment.RELEVANT_ENVIRONMENT,
        modality=ModalityType.NEGATED,
        temporal_status=TemporalStatus.PAST_VERIFIED,
        evidence_type=EvidenceType.EMPIRICAL,
        verbatim_quote="flight demonstration",
        char_offset_start=1200,
        char_offset_end=1285,
    )

    contradictions = detector.detect_contradictions([claim_pos, claim_neg])
    assert len(contradictions) >= 1
    assert contradictions[0].severity == "HIGH"
    assert contradictions[0].resolved_status == "UNRESOLVED"
    assert "Conflict detected" in contradictions[0].explanation


def test_issue_05_uncertainty_profile_computation():
    """Verify decoupled multi-dimensional uncertainty model."""
    uncertainty_engine = UncertaintyModel()

    ev_item = EvidenceItem(
        id="EVID-001",
        document_id="doc_1",
        evidence_text="Tested in laboratory breadboard",
        page_number=1,
        category=EvidenceCategory.LABORATORY_VALIDATION,
        strength=EvidenceStrength.STRONG_SUPPORTING,
        target_trl=4,
        confidence=0.88,
    )

    contra = ContradictionItem(
        id="CONTRA-001",
        claim_id_a="CLAIM-01",
        claim_id_b="CLAIM-02",
        explanation="Test contradiction",
        severity="HIGH",
        resolved_status="UNRESOLVED",
    )

    profile = uncertainty_engine.compute_profile(
        target_trl=4,
        evidence_items=[ev_item],
        contradictions=[contra],
        required_criteria_count=2,
    )

    assert 0.0 <= profile.extraction_confidence <= 1.0
    assert 0.0 <= profile.criteria_coverage <= 1.0
    assert profile.conflict_penalty > 0.0
    assert profile.calibration_status == "UNCALIBRATED_HEURISTIC"
    assert len(profile.notes) >= 3
