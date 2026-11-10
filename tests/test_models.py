"""
Unit Tests for Canonical Domain Models.
Validates constraints on TRL ranges, confidence scores, round limits, and implied prerequisite hierarchy.
"""

import pytest
from pydantic import ValidationError

from trl_core.models import (
    AgentAssessment,
    AgentType,
    Chunk,
    DebateMessage,
    Document,
    EvidenceCategory,
    EvidenceItem,
    EvidenceStrength,
    FinalAssessment,
    ImpliedPrerequisiteAudit,
)


def test_chunk_creation_valid():
    chunk = Chunk(
        id="chunk_001",
        document_id="doc_01",
        text="Valid chunk text",
        page_number=1,
        char_offset_start=0,
        char_offset_end=16,
        is_sanitized=True
    )
    assert chunk.id == "chunk_001"
    assert chunk.page_number == 1


def test_chunk_invalid_page_number():
    with pytest.raises(ValidationError):
        Chunk(
            id="chunk_001",
            document_id="doc_01",
            text="Valid chunk text",
            page_number=0,  # Page number must be >= 1
            char_offset_start=0,
            char_offset_end=16,
        )


def test_evidence_item_valid():
    item = EvidenceItem(
        id="EVID-001",
        document_id="doc_01",
        evidence_text="Thermal chamber test demonstrated operational reliability under -40C.",
        page_number=4,
        category=EvidenceCategory.RELEVANT_ENVIRONMENT_TESTING,
        strength=EvidenceStrength.STRONG_SUPPORTING,
        target_trl=5,
        confidence=0.88,
        source_reference={"char_start": 400, "char_end": 472}
    )
    assert item.target_trl == 5
    assert item.category == EvidenceCategory.RELEVANT_ENVIRONMENT_TESTING


def test_evidence_item_invalid_confidence():
    with pytest.raises(ValidationError):
        EvidenceItem(
            id="EVID-001",
            document_id="doc_01",
            evidence_text="Text",
            page_number=1,
            category=EvidenceCategory.CONCEPT,
            strength=EvidenceStrength.WEAK_SUPPORTING,
            confidence=1.5,  # Confidence must be <= 1.0
        )


def test_debate_message_author_validation():
    # Optimist and Skeptic are valid authors
    msg_opt = DebateMessage(
        round_number=2,
        agent_type=AgentType.OPTIMIST,
        argument="Evidence EVID-001 directly demonstrates relevant environment testing.",
        evidence_references=["EVID-001"]
    )
    assert msg_opt.round_number == 2

    # Referee cannot author debate messages in rounds 1-4 (referee only adjudicates)
    with pytest.raises(ValidationError):
        DebateMessage(
            round_number=2,
            agent_type=AgentType.REFEREE,
            argument="Invalid author for debate round",
        )


def test_implied_prerequisite_audit_hierarchy_rule():
    # Valid: inferred_from_trl (6) > target_level (3)
    audit = ImpliedPrerequisiteAudit(
        criterion_id="TRL-3.1",
        target_level=3,
        status="SATISFIED_INFERRED",
        inferred_from_trl=6,
        anchoring_evidence_id="EVID-010",
        inference_rationale="Field prototype demonstration at TRL 6 implies laboratory proof of concept.",
    )
    assert audit.target_level == 3
    assert audit.inferred_from_trl == 6

    # Invalid: inferred_from_trl (3) is NOT strictly higher than target_level (3)
    with pytest.raises(ValidationError):
        ImpliedPrerequisiteAudit(
            criterion_id="TRL-3.1",
            target_level=3,
            status="SATISFIED_INFERRED",
            inferred_from_trl=3,
            anchoring_evidence_id="EVID-010",
            inference_rationale="Invalid inference from equal level.",
        )


def test_final_assessment_trl_bounds():
    # Valid level between 1 and 9
    assessment = FinalAssessment(
        predicted_trl=5,
        confidence=0.85,
        justification="Verified testing in simulated relevant environment.",
        satisfied_criteria=["TRL-5.1: High fidelity testing"],
        missing_criteria=["TRL-6.1: Engineering prototype demonstration"],
        recommendations=["Build full engineering prototype for flight testing."],
    )
    assert assessment.predicted_trl == 5

    # Invalid TRL 0
    with pytest.raises(ValidationError):
        FinalAssessment(
            predicted_trl=0,
            confidence=0.5,
            justification="Invalid",
        )

    # Invalid TRL 10
    with pytest.raises(ValidationError):
        FinalAssessment(
            predicted_trl=10,
            confidence=0.5,
            justification="Invalid",
        )

