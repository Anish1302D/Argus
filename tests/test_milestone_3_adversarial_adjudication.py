"""
Unit Tests for Milestone 3: Explainable Adversarial Adjudication (Issues 11-16).
Covers formal debate protocol, optimist argumentation, skeptic challenge,
referee decision ledger, reproducibility, and advancement gap analysis.
"""

import pytest
from agent_orchestration.optimist import OptimistReviewer
from agent_orchestration.skeptic import SkepticReviewer
from agent_orchestration.referee import RefereeAdjudicator
from agent_orchestration.protocol import ReviewProtocol
from trl_core.gap_analysis import AdvancementGapAnalyzer
from trl_core.criteria_mapper import CriteriaMapper
from trl_core.models import (
    AgentType,
    ContradictionItem,
    EvidenceCategory,
    EvidenceItem,
    EvidenceStrength,
    ModalityType,
    TechnicalClaim,
    TemporalStatus,
    ValidationEnvironment,
)


@pytest.fixture
def sample_tps_debate_data():
    claim_pos = TechnicalClaim(
        id="CLAIM-TPS-01",
        document_id="doc_tps",
        chunk_id="chunk_1",
        text="Arc-jet testing sustained 2,150 K in plasma facility simulating Mach 7 re-entry aerothermal conditions.",
        candidate_trl=6,
        achievement_category="Relevant Environment Testing",
        validation_environment=ValidationEnvironment.RELEVANT_ENVIRONMENT,
        verbatim_quote="arc-jet facility testing",
        char_offset_start=100,
        char_offset_end=205,
    )
    claim_neg = TechnicalClaim(
        id="CLAIM-TPS-02",
        document_id="doc_tps",
        chunk_id="chunk_3",
        text="The system has not yet undergone actual suborbital sounding rocket flight demonstration (TRL 7).",
        candidate_trl=7,
        achievement_category="Flight Demonstration",
        modality=ModalityType.NEGATED,
        temporal_status=TemporalStatus.PAST_VERIFIED,
        validation_environment=ValidationEnvironment.RELEVANT_ENVIRONMENT,
        verbatim_quote="flight demonstration",
        char_offset_start=800,
        char_offset_end=895,
    )
    ev_item = EvidenceItem(
        id="EVID-TPS-01",
        document_id="doc_tps",
        evidence_text="Arc-jet plasma testing at 2,150 K",
        page_number=1,
        category=EvidenceCategory.RELEVANT_ENVIRONMENT_TESTING,
        strength=EvidenceStrength.STRONG_SUPPORTING,
        target_trl=6,
        confidence=0.92,
    )
    contra = ContradictionItem(
        id="CONTRA-TPS-01",
        claim_id_a="CLAIM-TPS-01",
        claim_id_b="CLAIM-TPS-02",
        explanation="Conflict between asserted flight prototype and admitted absence of flight demonstration.",
        severity="HIGH",
        resolved_status="UNRESOLVED",
    )
    return [ev_item], [claim_pos, claim_neg], [contra]


def test_issue_11_and_15_formal_debate_protocol_and_reproducibility(sample_tps_debate_data):
    """Verify formal protocol execution and 100% deterministic reproducibility across multiple runs."""
    ev_items, claims, contras = sample_tps_debate_data
    mapper = CriteriaMapper()
    mappings = mapper.map_evidence_to_criteria(target_trl=6, evidence_items=ev_items, contradictions=contras)

    protocol = ReviewProtocol(methodology_version="2.0.0-argus")

    # Run 1
    transcript1, assessments1, trl1, just1, implied1, ledger1 = protocol.run_debate(
        candidate_trl=6,
        evidence_items=ev_items,
        claims=claims,
        contradictions=contras,
        criteria_mappings=mappings,
    )

    assert len(transcript1) == 4
    assert transcript1[0].round_number == 1
    assert transcript1[0].agent_type == AgentType.OPTIMIST
    assert transcript1[1].agent_type == AgentType.SKEPTIC
    assert transcript1[2].round_number == 2
    assert "referee" in assessments1
    assert trl1 == 6

    # Run 2: Exact duplicate run should produce bit-for-bit identical outputs
    transcript2, assessments2, trl2, just2, implied2, ledger2 = protocol.run_debate(
        candidate_trl=6,
        evidence_items=ev_items,
        claims=claims,
        contradictions=contras,
        criteria_mappings=mappings,
    )

    assert trl1 == trl2
    assert just1 == just2
    assert [m.argument for m in transcript1] == [m.argument for m in transcript2]
    assert ledger1["accepted_evidence_ids"] == ledger2["accepted_evidence_ids"]


def test_issue_12_optimist_argumentation():
    """Verify Optimist constructs evidence-backed arguments citing verified evidence IDs."""
    optimist = OptimistReviewer()
    ev_item = EvidenceItem(
        id="EVID-OPT-01",
        document_id="doc_opt",
        evidence_text="Laser sensor breadboard tested for 120 hours with 42 dB SNR.",
        page_number=1,
        category=EvidenceCategory.LABORATORY_VALIDATION,
        strength=EvidenceStrength.STRONG_SUPPORTING,
        target_trl=4,
        confidence=0.90,
    )
    init_trl, assessment = optimist.evaluate_initial_position([ev_item], [])
    assert init_trl == 4
    assert "EVID-OPT-01" in assessment.evidence_references

    msg = optimist.generate_opening_argument(4, [ev_item])
    assert msg.agent_type == AgentType.OPTIMIST
    assert "EVID-OPT-01" in msg.evidence_references
    assert "TRL 4" in msg.argument


def test_issue_13_skeptic_evidence_challenge():
    """Verify Skeptic challenges unverified criteria and references document limitations."""
    skeptic = SkepticReviewer()
    contra = ContradictionItem(
        id="CONTRA-SK-01",
        claim_id_a="CL-1",
        claim_id_b="CL-2",
        explanation="Admitted lack of flight test",
        severity="HIGH",
    )
    skep_trl, assessment = skeptic.evaluate_initial_position(6, [], [contra])
    assert skep_trl <= 5  # Bounded lower than 6 due to high contradiction

    msg_open = skeptic.generate_opening_challenge(6, [])
    assert "TRL 7" in msg_open.argument  # Challenges advancement to TRL 7

    msg_counter = skeptic.generate_counter_rebuttal(6, [contra], [])
    assert "CONTRA-SK-01" in msg_counter.evidence_references
    assert "tension" in msg_counter.argument.lower() or "discloses" in msg_counter.argument.lower()


def test_issue_14_referee_adjudication_ledger(sample_tps_debate_data):
    """Verify Referee decision ledger records accepted/rejected claims and resolves contradictions."""
    ev_items, claims, contras = sample_tps_debate_data
    referee = RefereeAdjudicator()
    mapper = CriteriaMapper()
    mappings = mapper.map_evidence_to_criteria(target_trl=6, evidence_items=ev_items, contradictions=contras)

    final_trl, justification, implied, ref_assessment, ledger = referee.adjudicate_debate(
        candidate_trl=6,
        evidence_items=ev_items,
        claims=claims,
        contradictions=contras,
        criteria_mappings=mappings,
    )

    assert final_trl == 6
    assert len(ledger["accepted_evidence_ids"]) >= 1
    assert len(ledger["resolved_contradictions"]) >= 1
    assert ref_assessment.agent_type == AgentType.REFEREE
    assert len(implied) >= 2  # Implied prerequisites for TRL 2 to 5


def test_issue_16_advancement_gap_analysis():
    """Verify Advancement Gap Analyzer specifies concrete engineering tasks and testing environments."""
    analyzer = AdvancementGapAnalyzer()
    mapper = CriteriaMapper()
    ev_item = EvidenceItem(
        id="EVID-GAP-01",
        document_id="doc_gap",
        evidence_text="Lab breadboard verified",
        page_number=1,
        category=EvidenceCategory.LABORATORY_VALIDATION,
        strength=EvidenceStrength.STRONG_SUPPORTING,
        target_trl=4,
        confidence=0.88,
    )
    mappings = mapper.map_evidence_to_criteria(target_trl=4, evidence_items=[ev_item])

    gap_report = analyzer.analyze_gap(current_trl=4, criteria_mappings=mappings)
    assert gap_report.current_trl == 4
    assert gap_report.target_next_trl == 5
    assert len(gap_report.missing_criteria) > 0
    assert "relevant environment" in gap_report.required_environment.lower() or "simulated" in gap_report.required_environment.lower()
    assert len(gap_report.recommended_activities) >= 2
    assert any("thermal vacuum" in act.lower() or "chamber" in act.lower() or "enclosure" in act.lower() for act in gap_report.recommended_activities)
