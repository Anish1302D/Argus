"""
Unit Tests for Internal Input and Output Adapters.
Verifies input ingestion, paragraph chunking, error handling, and JSON serialization.
"""

import json
from pathlib import Path
import pytest

from trl_core.adapters.internal_adapter import InternalInputAdapter, InternalOutputAdapter
from trl_core.models import (
    EvidenceCategory,
    EvidenceItem,
    EvidenceStrength,
    FinalAssessment,
    ImpliedPrerequisiteAudit,
)


def test_internal_input_adapter_loads_document(sample_valid_paper: Path):
    adapter = InternalInputAdapter()
    doc = adapter.load_document(sample_valid_paper)

    assert doc.id == sample_valid_paper.stem
    assert len(doc.chunks) >= 3
    assert "Quantum Cascade Sensor" in doc.raw_content
    # Check that chunks retain offsets and are marked sanitized
    assert doc.chunks[0].char_offset_start == 0
    assert doc.chunks[0].is_sanitized is True


def test_internal_input_adapter_missing_file():
    adapter = InternalInputAdapter()
    with pytest.raises(FileNotFoundError):
        adapter.load_document(Path("non_existent_paper_12345.txt"))


def test_internal_input_adapter_empty_file(empty_file: Path):
    adapter = InternalInputAdapter()
    with pytest.raises(ValueError, match="Input document is empty"):
        adapter.load_document(empty_file)


def test_internal_output_adapter_formatting():
    adapter = InternalOutputAdapter()

    evidence = EvidenceItem(
        id="EVID-001",
        document_id="doc_01",
        evidence_text="Sensor bench testing completed over 120 hours.",
        page_number=1,
        category=EvidenceCategory.LABORATORY_VALIDATION,
        strength=EvidenceStrength.STRONG_SUPPORTING,
        target_trl=4,
        confidence=0.85,
    )

    audit = ImpliedPrerequisiteAudit(
        criterion_id="TRL-3.1",
        target_level=3,
        status="SATISFIED_INFERRED",
        inferred_from_trl=4,
        anchoring_evidence_id="EVID-001",
        inference_rationale="Lab validation confirms proof of concept.",
    )

    assessment = FinalAssessment(
        predicted_trl=4,
        confidence=0.85,
        justification="Laboratory prototype validation established.",
        satisfied_criteria=["Components integrated into laboratory breadboard."],
        implied_prerequisites_audit=[audit],
        missing_criteria=["Testing in relevant environmental chamber."],
        contradictions=[],
        recommendations=["Subject sensor to thermal vacuum chamber testing."],
        supporting_evidence=[evidence],
    )

    formatted = adapter.format_assessment(assessment)
    assert formatted["predicted_trl"] == 4
    assert formatted["confidence"] == 0.85
    assert formatted["reasoning_summary"] == "Laboratory prototype validation established."
    assert len(formatted["supporting_evidence"]) == 1
    assert formatted["supporting_evidence"][0]["evidence_id"] == "EVID-001"
    assert len(formatted["implied_prerequisites_audit"]) == 1
    assert formatted["implied_prerequisites_audit"][0]["criterion_id"] == "TRL-3.1"


def test_internal_output_adapter_writes_file(tmp_path: Path):
    adapter = InternalOutputAdapter()
    assessment = FinalAssessment(
        predicted_trl=3,
        confidence=0.72,
        justification="Proof of concept demonstrated.",
        satisfied_criteria=["Bench-scale testing complete."],
        missing_criteria=["Integrated component testing."],
        recommendations=["Integrate components."],
    )

    out_file = tmp_path / "assessment_output.json"
    written_path = adapter.write_assessment(assessment, out_file)

    assert written_path.exists()
    data = json.loads(written_path.read_text(encoding="utf-8"))
    assert data["predicted_trl"] == 3
    assert data["confidence"] == 0.72

