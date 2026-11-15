"""Tests for Milestone 5: Research Intelligence Experience (Issues 22-27)."""

import pytest
from fastapi.testclient import TestClient
from api.main import app
from api.service import SAMPLE_DOCUMENTS, get_service


@pytest.fixture
def client():
    return TestClient(app)


def test_issue_22_sample_documents_catalog_and_diversity(client):
    """
    Issue 22: Verify 5+ diverse sample document scenarios are present,
    covering the spectrum from foundational research (TRL 1) to flight operational (TRL 9),
    including tension/contradiction and advancement gap cases.
    """
    res = client.get("/api/sample-documents")
    assert res.status_code == 200
    samples = res.json()["samples"]
    assert len(samples) >= 5
    sample_ids = {s["id"] for s in samples}
    assert "hypersonic_tps" in sample_ids
    assert "quantum_cascade_sensor" in sample_ids
    assert "cubesat_transponder" in sample_ids
    assert "contradictory_thermal_report" in sample_ids
    assert "missing_milestones_gap_case" in sample_ids


def test_issue_23_evidence_ledger_inspection_contract(client):
    """
    Issue 23: Verify evidence ledger items return source provenance metadata
    (page, section, exact offset, strength, text excerpt) allowing bidirectional inspection.
    """
    res = client.post("/api/sample-assess/quantum_cascade_sensor")
    assert res.status_code == 200
    data = res.json()
    assert "evidence_ledger" in data
    ledger = data["evidence_ledger"]
    assert len(ledger) > 0
    first = ledger[0]
    assert "id" in first
    assert "text" in first
    assert "category" in first
    assert "strength" in first
    assert "page" in first
    assert "section" in first


def test_issue_24_explainable_adjudication_dossier_contract(client):
    """
    Issue 24: Verify assessment dossier returns full uncertainty profile,
    criteria mappings with explicit status, and contradiction records.
    """
    res = client.post("/api/sample-assess/contradictory_thermal_report")
    assert res.status_code == 200
    data = res.json()
    ass = data["assessment"]
    assert ass["uncertainty_profile"] is not None
    unc = ass["uncertainty_profile"]
    assert "extraction_confidence" in unc
    assert "criteria_coverage" in unc
    assert "conflict_penalty" in unc
    assert "composite_certainty" in unc
    assert "calibration_status" in unc

    # Check criteria mappings
    mappings = ass.get("criteria_mappings", [])
    assert len(mappings) > 0
    assert any(m["status"] in ("SATISFIED", "PARTIALLY_SUPPORTED", "CONTRADICTORY", "MISSING") for m in mappings)

    # Check contradictions presence
    assert len(ass.get("contradictions", [])) > 0


def test_issue_25_advancement_gap_visualizer_contract(client):
    """
    Issue 25: Verify gap report provides target next TRL, required environment,
    missing criteria, and concrete engineering recommendations.
    """
    res = client.post("/api/sample-assess/missing_milestones_gap_case")
    assert res.status_code == 200
    data = res.json()
    ass = data["assessment"]
    assert ass["gap_report"] is not None
    gap = ass["gap_report"]
    assert gap["target_next_trl"] > ass["predicted_trl"]
    assert len(gap["missing_criteria"]) > 0
    assert len(gap["recommended_activities"]) > 0


def test_issue_26_exportable_assessment_report_endpoint(client):
    """
    Issue 26: Verify publication-ready technical assessment report endpoint
    returns formatted Markdown dossier.
    """
    res = client.get("/api/sample-assess/hypersonic_tps/report")
    assert res.status_code == 200
    assert "text/html" in res.headers["content-type"]
    text = res.text
    assert "ARGUS TECHNICAL ASSESSMENT REPORT" in text
    assert "Executive Summary" in text
    assert "Canonical Criteria Mapping Checklist" in text
    assert "Advancement Gap Analysis" in text
    assert "Technical Evidence Ledger" in text
    assert "Reproducibility Hash:" in text


def test_issue_27_static_ui_integration_contract():
    """
    Issue 27: Verify static HTML dashboard contains all Stage 2 UI elements:
    export button, provenance drawer triggers, contradiction folio, uncertainty card.
    """
    from pathlib import Path
    html_path = Path("apps/api/src/api/static/index.html")
    assert html_path.exists()
    content = html_path.read_text(encoding="utf-8")
    assert "exportReport()" in content
    assert "toggleEvInspection" in content
    assert "Document Tensions & Contradictions" in content
    assert "Uncertainty Profile & Calibration" in content
    assert "Inspect Provenance" in content
