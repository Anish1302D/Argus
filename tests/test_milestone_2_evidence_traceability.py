"""
Unit Tests for Milestone 2: Evidence Traceability & Provenance (Issues 06-10).
Covers granular source provenance, evidence-to-criteria mapping, evidence ledger,
assessment audit trail, and source inspection.
"""

import pytest
from trl_core.audit import AuditTrailBuilder
from trl_core.criteria_mapper import CriteriaMapper
from trl_core.ledger import EvidenceLedger
from trl_core.models import (
    Chunk,
    ContradictionItem,
    Document,
    EvidenceCategory,
    EvidenceItem,
    EvidenceStrength,
    ModalityType,
    TechnicalClaim,
    TemporalStatus,
    ValidationEnvironment,
)
from trl_core.provenance import ProvenanceEngine


def test_issue_06_granular_source_provenance():
    """Verify that source provenance preserves exact character slices and context windows."""
    doc_text = "Introductory text. In our laboratory tests, the optical breadboard reached 42 dB SNR over 120 hours. Conclusion notes."
    doc = Document(
        id="doc_prov_01",
        name="test_paper.txt",
        raw_content=doc_text,
        chunks=[],
    )
    chunk = Chunk(
        id="chunk_01",
        document_id="doc_prov_01",
        text=doc_text[19:101],
        page_number=1,
        section_name="Validation",
        char_offset_start=19,
        char_offset_end=101,
    )
    claim = TechnicalClaim(
        id="CLAIM-001",
        document_id="doc_prov_01",
        chunk_id="chunk_01",
        text=chunk.text,
        candidate_trl=4,
        achievement_category="Laboratory Validation",
        validation_environment=ValidationEnvironment.LABORATORY,
        verbatim_quote="optical breadboard",
        char_offset_start=19,
        char_offset_end=101,
    )

    engine = ProvenanceEngine()
    provenance = engine.extract_provenance(doc, chunk, claim, context_padding=20)
    assert provenance.char_offset_start == 19
    assert provenance.char_offset_end == 101
    assert "optical breadboard" in provenance.verbatim_excerpt
    assert engine.verify_provenance_slice(doc_text, provenance)
    assert "Introductory text." in provenance.context_window


def test_issue_07_evidence_to_criteria_mapping():
    """Verify criteria mapping distinguishes directly satisfied from inferred and missing criteria."""
    mapper = CriteriaMapper()

    evidence_item_trl4 = EvidenceItem(
        id="EVID-004",
        document_id="doc_01",
        evidence_text="Optical breadboard validated in laboratory.",
        page_number=1,
        category=EvidenceCategory.LABORATORY_VALIDATION,
        strength=EvidenceStrength.STRONG_SUPPORTING,
        target_trl=4,
        confidence=0.90,
    )

    mappings = mapper.map_evidence_to_criteria(
        target_trl=4,
        evidence_items=[evidence_item_trl4],
    )

    # Level 4 criteria should be directly satisfied
    lvl4_crit = [m for m in mappings if m.trl_level == 4]
    assert len(lvl4_crit) > 0
    assert any(m.status == "DIRECTLY_SATISFIED" for m in lvl4_crit)

    # Levels 2 and 3 criteria should be inferred prerequisites
    lvl2_crit = [m for m in mappings if m.trl_level == 2]
    assert any(m.status == "SATISFIED_INFERRED" for m in lvl2_crit)
    assert lvl2_crit[0].inferred_from_trl == 4

    # Level 5 criteria should be missing
    lvl5_crit = [m for m in mappings if m.trl_level == 5]
    assert any(m.status == "MISSING" for m in lvl5_crit)


def test_issue_08_evidence_ledger_relational_queries():
    """Verify bi-directional query navigation across Document -> Claim -> Evidence -> Criterion."""
    claim = TechnicalClaim(
        id="CLAIM-101",
        document_id="doc_ledger",
        chunk_id="chunk_1",
        text="Bench breadboard test completed.",
        candidate_trl=4,
        achievement_category="Laboratory Validation",
        verbatim_quote="breadboard",
        char_offset_start=10,
        char_offset_end=42,
    )
    ev = EvidenceItem(
        id="EVID-101",
        claim_id="CLAIM-101",
        document_id="doc_ledger",
        evidence_text="Bench breadboard test completed.",
        page_number=1,
        category=EvidenceCategory.LABORATORY_VALIDATION,
        strength=EvidenceStrength.STRONG_SUPPORTING,
        target_trl=4,
        confidence=0.91,
    )
    mapper = CriteriaMapper()
    mappings = mapper.map_evidence_to_criteria(target_trl=4, evidence_items=[ev])

    ledger = EvidenceLedger(
        document_id="doc_ledger",
        claims=[claim],
        evidence_items=[ev],
        criteria_mappings=mappings,
        adjudicated_trl=4,
    )

    # Test bidirectional lookups
    claims_for_ev = ledger.get_claims_for_evidence("EVID-101")
    assert len(claims_for_ev) == 1
    assert claims_for_ev[0].id == "CLAIM-101"

    ev_for_crit = ledger.get_evidence_for_criterion("TRL-4.1")
    assert any(e.id == "EVID-101" for e in ev_for_crit)

    ledger_dict = ledger.to_dict()
    assert ledger_dict["total_claims"] == 1
    assert ledger_dict["total_evidence_items"] == 1
    assert "links" in ledger_dict


def test_issue_09_assessment_audit_trail_reproducibility():
    """Verify that audit trail captures rule events and produces deterministic reproducibility hashes."""
    builder = AuditTrailBuilder(methodology_version="2.0.0-argus")
    builder.record_stage(
        rule_id="RULE-INGEST",
        stage="INGESTION",
        inputs={"format": "txt", "pages": 1},
        outcome="SUCCESS",
        explanation="Document successfully ingested",
    )
    builder.record_stage(
        rule_id="RULE-ADJUDICATE",
        stage="ADJUDICATION",
        inputs={"target_trl": 4, "strong_evidence_count": 1},
        outcome="ADJUDICATED_TRL_4",
        explanation="Adjudicated TRL 4 with implied prerequisites",
    )

    trail1 = builder.build_audit_trail("doc_audit_1", adjudicated_trl=4)
    assert len(trail1.records) == 2
    assert trail1.methodology_version == "2.0.0-argus"
    assert len(trail1.reproducibility_hash) == 64  # SHA-256

    # Re-run identical build should produce identical hash
    builder2 = AuditTrailBuilder(methodology_version="2.0.0-argus")
    builder2.record_stage(
        rule_id="RULE-INGEST",
        stage="INGESTION",
        inputs={"format": "txt", "pages": 1},
        outcome="SUCCESS",
        explanation="Document successfully ingested",
    )
    builder2.record_stage(
        rule_id="RULE-ADJUDICATE",
        stage="ADJUDICATION",
        inputs={"target_trl": 4, "strong_evidence_count": 1},
        outcome="ADJUDICATED_TRL_4",
        explanation="Adjudicated TRL 4 with implied prerequisites",
    )
    trail2 = builder2.build_audit_trail("doc_audit_1", adjudicated_trl=4)
    assert trail1.reproducibility_hash == trail2.reproducibility_hash


def test_issue_10_evidence_source_context_inspection():
    """Verify source context inspection helper returns exact offsets and contextual text."""
    doc_text = "Alpha section header. The subsystem completed 120 hours of bench tests. Beta section follows."
    ev = EvidenceItem(
        id="EVID-CTX-01",
        document_id="doc_ctx",
        evidence_text="subsystem completed 120 hours of bench tests",
        page_number=1,
        category=EvidenceCategory.LABORATORY_VALIDATION,
        strength=EvidenceStrength.STRONG_SUPPORTING,
        target_trl=4,
        confidence=0.88,
        source_reference={"char_start": 22, "char_end": 71},
    )

    ledger = EvidenceLedger(
        document_id="doc_ctx",
        claims=[],
        evidence_items=[ev],
        criteria_mappings=[],
        adjudicated_trl=4,
    )

    inspection = ledger.inspect_source_context("EVID-CTX-01", document_text=doc_text, context_padding=25)
    assert inspection["evidence_id"] == "EVID-CTX-01"
    assert inspection["char_offset_start"] == 22
    assert inspection["char_offset_end"] == 71
    assert "Alpha" in inspection["context_window"]
    assert "Beta" in inspection["context_window"]
