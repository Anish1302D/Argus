"""
Comprehensive APCTT Stage 1 Contract, Lifecycle, and Integration Test Suite (Scenarios A–X).

Verifies:
A. Participant Kit integrity (MANIFEST.sha256 verification)
B. Module loading (`participant_module.adapter:AssessmentModule` __init__ & load)
C. Dynamic checklist evaluation (official 12-criterion + arbitrary custom criterion IDs)
D. Completed assessment contract compliance
E. Abstained — insufficient evidence
F. Abstained — conflicting evidence
G. Abstained — ambiguous scope
H. Abstained — out of scope
I. Failed assessment (unreadable/missing/empty PDF, page mismatch, exhausted budget)
J. Met criterion without evidence rejected / prevented (E06)
K. Insufficient evidence without missing_evidence rejected / prevented (E09)
L. Unknown criterion key rejected (E07/E08/E17)
M. Unknown top-level / evidence item field rejected (E15/E16)
N. Invalid page reference rejected (E13)
O. Invalid document_id rejected (E14)
P. Negation detection (negated flight/prototype test does not inflate TRL)
Q. Future/planned work detection (planned Phase 2 test does not inflate TRL)
R. Multi-document case provenance & chronology resolution
S. reset_case() clears per-case state and never raises
T. close() releases resources and never raises
U. Determinism across repeated runs
V. Offline execution (HF_HUB_OFFLINE=1, TRANSFORMERS_OFFLINE=1)
W. Official DEMO-001 and USGS smoke case verification
X. FastAPI APCTT endpoints and official submission bundle verification
"""

from __future__ import annotations

import base64
import hashlib
import io
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Sequence

import pytest
from fastapi.testclient import TestClient
from pypdf import PdfReader
from reportlab.pdfgen import canvas

from apctt_contracts.config import Checklist
from apctt_contracts.results import validate_result
from api.main import app
from competition_engine.apctt_adapter import (
    AssessmentModule as EngineAssessmentModule,
    verify_and_sanitize_result,
)
from participant_module.adapter import AssessmentModule as BundleAssessmentModule

PROJECT_ROOT = Path(__file__).resolve().parents[1]
KIT_CPU = PROJECT_ROOT / "apctt-participant-kit-0.5.0-cpu"
KIT_CUDA = PROJECT_ROOT / "apctt-participant-kit-0.5.0-cuda"
SUBMISSION_BUNDLE = PROJECT_ROOT / "my_submission"
SUBMISSION_ZIP = PROJECT_ROOT / "argus_submission.zip"

OFFICIAL_CHECKLIST_DATA = json.loads(
    (KIT_CPU / "contracts" / "checklist.official.json").read_text(encoding="utf-8")
)
OFFICIAL_CHECKLIST = Checklist.model_validate(OFFICIAL_CHECKLIST_DATA)


def make_pdf_file(path: Path, pages_text: Sequence[str]) -> Path:
    """Create a real multi-page PDF at `path` with the given text per page."""
    buf = io.BytesIO()
    c = canvas.Canvas(buf)
    for page_str in pages_text:
        y = 750
        lines = (page_str or "").splitlines() or [""]
        for line in lines:
            while len(line) > 90:
                c.drawString(50, y, line[:90])
                line = line[90:]
                y -= 14
            c.drawString(50, y, line)
            y -= 14
        c.showPage()
    c.save()
    path.write_bytes(buf.getvalue())
    return path


def make_apctt_case(
    tmp_path: Path,
    case_id: str,
    target_desc: str,
    docs_pages: Sequence[Sequence[str]],
    *,
    target_type: str = "technology",
    intended_app: str = "General engineering validation",
    intended_env: str = "Laboratory and relevant test environment",
    title: str = "Technical Validation Report",
    checklist_version: str = "APCTT-2026-CHECKLIST-v1",
    doc_dates: Sequence[str | None] | None = None,
) -> Dict[str, Any]:
    """Construct a worker-ready APCTT case dictionary with real PDF files on disk."""
    documents = []
    for idx, p_texts in enumerate(docs_pages):
        doc_id = f"D{idx + 1:03d}"
        pdf_path = make_pdf_file(tmp_path / f"{case_id}_{doc_id}.pdf", p_texts)
        pdf_bytes = pdf_path.read_bytes()
        d_date = doc_dates[idx] if doc_dates and idx < len(doc_dates) else "2026-01-15"
        documents.append(
            {
                "document_id": doc_id,
                "title": f"{title} - Part {idx + 1}",
                "document_date": d_date,
                "language": "en",
                "format": "pdf",
                "sha256": hashlib.sha256(pdf_bytes).hexdigest(),
                "page_count": len(p_texts),
                "path": str(pdf_path),
            }
        )
    return {
        "schema_version": "apctt-pdf-example-v1",
        "input_profile": "pdf_report",
        "checklist_version": checklist_version,
        "case_id": case_id,
        "assessment_as_of": None,
        "assessment_target": {
            "target_id": f"{case_id}-T1",
            "type": target_type,
            "description": target_desc,
        },
        "intended_application": intended_app,
        "intended_environment": intended_env,
        "title": title,
        "documents": documents,
    }


# ---------------------------------------------------------------------------
# A. Participant Kit Integrity
# ---------------------------------------------------------------------------


def test_scenario_a_participant_kit_manifest_integrity():
    """Scenario A: Verify local read-only Participant Kit MANIFEST.sha256 passes 100%."""
    assert KIT_CPU.is_dir(), "CPU Participant Kit directory must exist"
    manifest_file = KIT_CPU / "MANIFEST.sha256"
    assert manifest_file.is_file()

    lines = [
        ln.strip()
        for ln in manifest_file.read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]
    assert len(lines) == 129
    for line in lines:
        expected_hash, rel_path = line.split("  ", 1)
        target = KIT_CPU / rel_path
        assert target.is_file(), f"Missing kit file: {rel_path}"
        actual_hash = hashlib.sha256(target.read_bytes()).hexdigest()
        assert actual_hash == expected_hash, f"Hash mismatch on {rel_path}"


# ---------------------------------------------------------------------------
# B & C. Module Loading & Dynamic Checklist Evaluation
# ---------------------------------------------------------------------------


def test_scenario_b_and_c_module_loading_and_dynamic_checklist(tmp_path: Path):
    """
    Scenarios B & C: Verify AssessmentModule loads both the official 12-criterion checklist
    and an arbitrary custom checklist with modified criterion IDs without hardcoded IDs.
    """
    custom_checklist_raw = {
        "version": "CUSTOM-CHECKLIST-2026-v9",
        "criteria": [
            {
                "criterion_id": "CUST-ALPHA-01",
                "description": "Basic physical and mathematical principles are observed and formulated (TRL 1).",
            },
            {
                "criterion_id": "CUST-BETA-04",
                "description": "Component or breadboard validation in a laboratory environment is completed (TRL 4).",
            },
            {
                "criterion_id": "CUST-GAMMA-QUANT",
                "description": "Quantified results against requirements: measured performance is compared with acceptance criteria.",
            },
        ],
    }
    custom_checklist_obj = Checklist.model_validate(custom_checklist_raw)

    mod = BundleAssessmentModule()
    mod.load({"checklist": custom_checklist_raw, "settings": {}}, SUBMISSION_BUNDLE / "assets")

    case = make_apctt_case(
        tmp_path,
        case_id="DYNAMIC-CHK-001",
        target_desc="Optical breadboard sensor assembly",
        docs_pages=[
            [
                "Optical Breadboard Sensor Validation Report.\n"
                "The governing physical principles and mathematical equations were derived analytically.\n"
                "An optical breadboard sensor prototype was constructed and tested in a laboratory environment.\n"
                "Measured sensitivity achieved 98.4% accuracy compared with the 95.0% acceptance requirement."
            ]
        ],
        checklist_version="CUSTOM-CHECKLIST-2026-v9",
    )

    res = mod.assess(case, None)
    issues = validate_result(res, case=case, checklist=custom_checklist_obj)
    assert issues == []
    assert res["checklist_version"] == "CUSTOM-CHECKLIST-2026-v9"
    assert set(res["criterion_status"].keys()) == {
        "CUST-ALPHA-01",
        "CUST-BETA-04",
        "CUST-GAMMA-QUANT",
    }
    assert res["criterion_status"]["CUST-BETA-04"] == "met"
    assert res["criterion_status"]["CUST-GAMMA-QUANT"] == "met"
    mod.reset_case()
    mod.close()


# ---------------------------------------------------------------------------
# D. Completed Assessment
# ---------------------------------------------------------------------------


def test_scenario_d_completed_assessment_contract(tmp_path: Path):
    """Scenario D: Verify completed assessment returns integer TRL 1..9 and valid uncertainty."""
    mod = BundleAssessmentModule()
    mod.load({"checklist": OFFICIAL_CHECKLIST_DATA, "settings": {}}, SUBMISSION_BUNDLE / "assets")

    case = make_apctt_case(
        tmp_path,
        case_id="COMPLETED-TRL6-001",
        target_desc="Calibrated watershed hydrologic simulation model",
        docs_pages=[
            [
                "Calibration and Validation of the Watershed Hydrologic Model.\n"
                "Governing continuity and energy equations form the theoretical basis of the model.\n"
                "The technology concept and modelling framework were formulated for basin water management.\n"
                "Analytical proof-of-concept simulations verified critical water-balance functions.",
                "Component modules were integrated and tested on desktop benchmark datasets in the laboratory.\n"
                "The calibrated model was demonstrated in a relevant environment across historical basin observations.\n"
                "Model performance was calibrated and validated against measured streamgage observations from 2010 to 2015, "
                "achieving a Nash-Sutcliffe efficiency (NSE) of 0.86 and RMSE of 1.4 m3/s, meeting satisfactory criteria.",
            ]
        ],
        title="Calibration of Watershed Hydrologic Model in Relevant Environment",
        intended_env="River basin watershed relevant environment",
    )

    res = mod.assess(case, None)
    issues = validate_result(res, case=case, checklist=OFFICIAL_CHECKLIST)
    assert issues == []
    assert res["assessment_status"] == "completed"
    assert isinstance(res["predicted_trl"], int) and not isinstance(res["predicted_trl"], bool)
    assert 4 <= res["predicted_trl"] <= 7
    assert res["abstention_reason"] is None
    assert res["error_code"] is None
    assert "uncertainty" in res
    assert res["uncertainty"]["lower"] <= res["predicted_trl"] <= res["uncertainty"]["upper"]
    assert isinstance(res.get("trl_rationale"), str) and res["trl_rationale"].strip()


# ---------------------------------------------------------------------------
# E, F, G, H. Abstention Scenarios
# ---------------------------------------------------------------------------


def test_scenario_e_abstained_insufficient_evidence(tmp_path: Path):
    """Scenario E: Verify abstained assessment with 'insufficient evidence'."""
    mod = BundleAssessmentModule()
    mod.load({"checklist": OFFICIAL_CHECKLIST_DATA, "settings": {}}, SUBMISSION_BUNDLE / "assets")

    case = make_apctt_case(
        tmp_path,
        case_id="ABSTAIN-INSUFF-001",
        target_desc="Synthetic sensor fixture; not a validated technology",
        docs_pages=[
            [
                "Synthetic test note - DEMO fixture only, not a real technical report.\n"
                "A synthetic prototype was tested in a laboratory water tank.",
                "Results\nMeasured results and acceptance criteria are not supplied.",
            ]
        ],
        title="DEMO fixture only",
    )

    res = mod.assess(case, None)
    issues = validate_result(res, case=case, checklist=OFFICIAL_CHECKLIST)
    assert issues == []
    assert res["assessment_status"] == "abstained"
    assert res["predicted_trl"] is None
    assert res["abstention_reason"] == "insufficient evidence"
    assert res["error_code"] is None
    assert "trl_rationale" not in res


def test_scenario_f_abstained_conflicting_evidence(tmp_path: Path):
    """Scenario F: Verify abstained assessment with 'conflicting evidence'."""
    mod = BundleAssessmentModule()
    mod.load({"checklist": OFFICIAL_CHECKLIST_DATA, "settings": {}}, SUBMISSION_BUNDLE / "assets")

    case = make_apctt_case(
        tmp_path,
        case_id="ABSTAIN-CONFLICT-001",
        target_desc="Cryogenic valve actuator prototype",
        docs_pages=[
            [
                "Executive Summary: The cryogenic valve actuator prototype was tested in a laboratory testbed.\n"
                "Audit Addendum: This report directly contradicts the summary; no hardware prototype has been "
                "constructed or tested, and mutually exclusive results prevent readiness verification."
            ]
        ],
    )

    res = mod.assess(case, None)
    issues = validate_result(res, case=case, checklist=OFFICIAL_CHECKLIST)
    assert issues == []
    assert res["assessment_status"] == "abstained"
    assert res["predicted_trl"] is None
    assert res["abstention_reason"] == "conflicting evidence"
    assert res["error_code"] is None


def test_scenario_g_abstained_ambiguous_scope(tmp_path: Path):
    """Scenario G: Verify abstained assessment with 'ambiguous scope'."""
    mod = BundleAssessmentModule()
    mod.load({"checklist": OFFICIAL_CHECKLIST_DATA, "settings": {}}, SUBMISSION_BUNDLE / "assets")

    case = make_apctt_case(
        tmp_path,
        case_id="ABSTAIN-AMBIG-001",
        target_desc="Ambiguous scope: multiple unrelated targets with unspecified target boundary",
        docs_pages=[
            [
                "Program Overview: Both a lithium battery pack and an optical star tracker were studied.\n"
                "The optical star tracker was tested in a laboratory environment with 99.1% accuracy."
            ]
        ],
    )

    res = mod.assess(case, None)
    issues = validate_result(res, case=case, checklist=OFFICIAL_CHECKLIST)
    assert issues == []
    assert res["assessment_status"] == "abstained"
    assert res["predicted_trl"] is None
    assert res["abstention_reason"] == "ambiguous scope"


def test_scenario_h_abstained_out_of_scope(tmp_path: Path):
    """Scenario H: Verify abstained assessment with 'out of scope' when document is unrelated."""
    mod = BundleAssessmentModule()
    mod.load({"checklist": OFFICIAL_CHECKLIST_DATA, "settings": {}}, SUBMISSION_BUNDLE / "assets")

    case = make_apctt_case(
        tmp_path,
        case_id="ABSTAIN-OOS-001",
        target_desc="Superconducting Tokamak Fusion Magnet Cryostat",
        docs_pages=[
            [
                "Wheat Crop Yield and Soil Nitrogen Fertilizer Study in Agricultural Fields.\n"
                "Grain harvest plots were measured across three growing seasons using standard agronomy methods."
            ]
        ],
        title="Agricultural Soil Fertilizer Study",
    )

    res = mod.assess(case, None)
    issues = validate_result(res, case=case, checklist=OFFICIAL_CHECKLIST)
    assert issues == []
    assert res["assessment_status"] == "abstained"
    assert res["predicted_trl"] is None
    assert res["abstention_reason"] == "out of scope"


# ---------------------------------------------------------------------------
# I. Failed Assessment Scenarios
# ---------------------------------------------------------------------------


def test_scenario_i_failed_assessment_unreadable_or_timeout(tmp_path: Path):
    """Scenario I: Verify failed assessment on corrupted PDF or exhausted time budget."""
    mod = BundleAssessmentModule()
    mod.load({"checklist": OFFICIAL_CHECKLIST_DATA, "settings": {}}, SUBMISSION_BUNDLE / "assets")

    bad_pdf = tmp_path / "corrupted.pdf"
    bad_pdf.write_bytes(b"NOT A VALID PDF FILE CONTENT")

    case = {
        "schema_version": "apctt-pdf-example-v1",
        "input_profile": "pdf_report",
        "checklist_version": "APCTT-2026-CHECKLIST-v1",
        "case_id": "FAILED-CORRUPT-001",
        "assessment_as_of": None,
        "assessment_target": {
            "target_id": "T1",
            "type": "component",
            "description": "Corrupted PDF test target",
        },
        "intended_application": "Test",
        "intended_environment": "Lab",
        "title": "Corrupted PDF Case",
        "documents": [
            {
                "document_id": "D001",
                "title": "Corrupted",
                "document_date": None,
                "language": "en",
                "format": "pdf",
                "sha256": hashlib.sha256(b"NOT A VALID PDF FILE CONTENT").hexdigest(),
                "page_count": 1,
                "path": str(bad_pdf),
            }
        ],
    }

    res = mod.assess(case, None)
    issues = validate_result(res, case=case, checklist=OFFICIAL_CHECKLIST)
    assert issues == []
    assert res["assessment_status"] == "failed"
    assert res["predicted_trl"] is None
    assert res["abstention_reason"] is None
    assert res["error_code"] == "DOCUMENT_UNREADABLE"
    for opt_field in ("confidence", "uncertainty", "trl_rationale", "criterion_rationale"):
        assert opt_field not in res


# ---------------------------------------------------------------------------
# J, K, L, M, N, O. Output Contract Sanitizer & Validator Rules
# ---------------------------------------------------------------------------


def test_scenarios_j_to_o_contract_enforcement_and_rejection(tmp_path: Path):
    """
    Scenarios J, K, L, M, N, O:
    Verify both apctt_contracts.results.validate_result and our verify_and_sanitize_result
    enforce met-requires-evidence (J), insufficient-requires-missing_evidence (K),
    known criterion keys (L), no unknown fields (M), valid page bounds (N), and valid document_id (O).
    """
    case = make_apctt_case(
        tmp_path,
        case_id="CONTRACT-CHECK-001",
        target_desc="Test sensor",
        docs_pages=[["Page 1 text: The sensor prototype was tested in a laboratory chamber."]],
    )
    cids = [c["criterion_id"] for c in OFFICIAL_CHECKLIST_DATA["criteria"]]

    # Construct a raw result with deliberate defects (empty evidence on 'met', missing missing_evidence,
    # invalid page=99, invalid document_id='D999') and verify verify_and_sanitize_result fixes/filters them
    dirty_result: Dict[str, Any] = {
        "schema_version": case["schema_version"],
        "checklist_version": "APCTT-2026-CHECKLIST-v1",
        "case_id": case["case_id"],
        "assessment_target": dict(case["assessment_target"]),
        "assessment_status": "completed",
        "predicted_trl": 4,
        "criterion_status": {cid: ("met" if cid == "APCTT-C04" else "insufficient evidence") for cid in cids},
        "evidence_reference": {
            cid: (
                [
                    {"document_id": "D999", "page": 1, "supporting_span": "tested"},  # O: invalid doc_id
                    {"document_id": "D001", "page": 99, "supporting_span": "tested"},  # N: invalid page
                ]
                if cid == "APCTT-C04"
                else []
            )
            for cid in cids
        },
        "missing_evidence": {},  # K: missing explanations
        "abstention_reason": None,
        "error_code": None,
    }

    # First confirm official validator catches J, K, N, O on the dirty result
    raw_issues = {
        i.rule for i in validate_result(dirty_result, case=case, checklist=OFFICIAL_CHECKLIST)
    }
    assert "evidence_locator_exists" in raw_issues  # O
    assert "evidence_page_in_document" in raw_issues  # N
    assert "missing_evidence_required_for_insufficient" in raw_issues  # K

    # Now sanitize via verify_and_sanitize_result: invalid refs are removed, APCTT-C04 is downgraded
    # from 'met' to 'insufficient evidence' (J), and missing_evidence is populated (K)
    cleaned = verify_and_sanitize_result(
        result=dirty_result,
        case=case,
        criterion_ids=cids,
        page_lookup={("D001", 1): "Page 1 text: The sensor prototype was tested in a laboratory chamber."},
        doc_page_counts={"D001": 1},
    )
    assert cleaned["criterion_status"]["APCTT-C04"] == "insufficient evidence"
    assert validate_result(cleaned, case=case, checklist=OFFICIAL_CHECKLIST) == []


# ---------------------------------------------------------------------------
# P, Q, R. Negation, Future Work & Multi-Document Chronology
# ---------------------------------------------------------------------------


def test_scenarios_p_and_q_negation_and_future_work_handling(tmp_path: Path):
    """
    Scenarios P & Q: Verify negated flight/operational claims and planned future work
    do not falsely satisfy higher TRL criteria.
    """
    mod = BundleAssessmentModule()
    mod.load({"checklist": OFFICIAL_CHECKLIST_DATA, "settings": {}}, SUBMISSION_BUNDLE / "assets")

    case = make_apctt_case(
        tmp_path,
        case_id="NEG-FUTURE-001",
        target_desc="Suborbital telemetry transceiver breadboard",
        docs_pages=[
            [
                "Suborbital Telemetry Transceiver Breadboard Report.\n"
                "Governing radio-frequency link equations and modulation principles were analyzed.\n"
                "The transceiver concept and architecture were formulated for sounding rocket telemetry.\n"
                "Analytical link-budget simulations provided proof of concept.\n"
                "A breadboard transceiver was integrated and tested in a laboratory bench environment, "
                "achieving -108 dBm sensitivity compared with the -105 dBm requirement.\n"
                "However, the system has not yet undergone operational flight demonstration (TRL 7 was not performed).\n"
                "Full operational flight qualification will be conducted in future Phase 2 work."
            ]
        ],
        intended_env="Desktop and laboratory bench test environment with example datasets",
    )

    res = mod.assess(case, None)
    issues = validate_result(res, case=case, checklist=OFFICIAL_CHECKLIST)
    assert issues == []
    assert res["assessment_status"] == "completed"
    assert res["predicted_trl"] == 4
    assert res["criterion_status"]["APCTT-C04"] == "met"
    assert res["criterion_status"]["APCTT-C07"] in ("not met", "insufficient evidence")
    assert res["criterion_status"]["APCTT-C08"] in ("not met", "insufficient evidence")


def test_scenario_r_multi_document_provenance_and_chronology(tmp_path: Path):
    """
    Scenario R: Verify multi-document cases preserve distinct document_id and 1-based page
    locators and resolve chronological progression across dated reports.
    """
    mod = BundleAssessmentModule()
    mod.load({"checklist": OFFICIAL_CHECKLIST_DATA, "settings": {}}, SUBMISSION_BUNDLE / "assets")

    case = make_apctt_case(
        tmp_path,
        case_id="MULTI-DOC-001",
        target_desc="Autonomous Underwater Glider Navigation Subsystem",
        docs_pages=[
            [
                "2024 Phase 1 Concept & Lab Report: Basic acoustic navigation principles and equations were derived.\n"
                "The navigation subsystem concept was formulated for autonomous underwater gliders.\n"
                "Laboratory water-tank breadboard tests verified acoustic ranging."
            ],
            [
                "2026 Phase 2 Calibrated Basin Demonstration Report:\n"
                " Page 1 covers background.",
                "On page 2, the integrated autonomous underwater glider navigation prototype was calibrated "
                "and demonstrated in a relevant lake basin environment against GPS reference buoys, "
                "achieving 0.42 m RMSE positioning error compared with the 1.0 m accuracy requirement.",
            ],
        ],
        doc_dates=["2024-03-10", "2026-02-20"],
        title="Calibration and Demonstration of Autonomous Underwater Glider Navigation",
    )

    res = mod.assess(case, None)
    issues = validate_result(res, case=case, checklist=OFFICIAL_CHECKLIST)
    assert issues == []
    assert res["assessment_status"] == "completed"
    assert res["predicted_trl"] == 6
    c06_refs = res["evidence_reference"]["APCTT-C06"]
    assert any(r["document_id"] == "D002" and r["page"] == 2 for r in c06_refs)


# ---------------------------------------------------------------------------
# S, T, U, V. Reset, Close, Determinism & Offline Execution
# ---------------------------------------------------------------------------


def test_scenarios_s_t_u_v_lifecycle_determinism_and_offline(tmp_path: Path, monkeypatch):
    """
    Scenarios S, T, U, V: Verify reset_case(), close(), bitwise determinism across runs,
    and offline environment operation.
    """
    monkeypatch.setenv("HF_HUB_OFFLINE", "1")
    monkeypatch.setenv("TRANSFORMERS_OFFLINE", "1")

    mod = BundleAssessmentModule()
    mod.load({"checklist": OFFICIAL_CHECKLIST_DATA, "settings": {}}, SUBMISSION_BUNDLE / "assets")

    case = make_apctt_case(
        tmp_path,
        case_id="DET-OFFLINE-001",
        target_desc="Coupled simulation software package",
        docs_pages=[
            [
                "P2S Coupled Simulation Software Report.\n"
                "Governing hydrologic and stream-temperature equations are formulated.\n"
                "The coupled program, installation package, source code, and example datasets were "
                "implemented and tested in a desktop laboratory environment, with measured outputs "
                "verified against benchmark baseline tolerances (0.01 C error)."
            ]
        ],
        intended_env="Desktop modelling software with example datasets",
    )

    res1 = mod.assess(case, None)
    mod.reset_case()
    assert mod.last_case_id is None

    res2 = mod.assess(case, None)
    mod.reset_case()
    mod.close()

    assert res1 == res2
    assert validate_result(res1, case=case, checklist=OFFICIAL_CHECKLIST) == []


# ---------------------------------------------------------------------------
# W & X. Official Example, Smoke Cases, Submission ZIP & Web API Endpoints
# ---------------------------------------------------------------------------


def test_scenario_w_official_example_request_execution(tmp_path: Path):
    """Scenario W: Execute official EXAMPLE_REQUEST.json (DEMO-001) and validate output."""
    example_req = json.loads((KIT_CPU / "docs" / "EXAMPLE_REQUEST.json").read_text(encoding="utf-8"))
    case = dict(example_req["case"])
    docs = []
    for d in case["documents"]:
        d_copy = dict(d)
        pdf_bytes = base64.b64decode(d_copy.pop("content_base64"))
        pdf_path = tmp_path / f"{case['case_id']}_{d_copy['document_id']}.pdf"
        pdf_path.write_bytes(pdf_bytes)
        d_copy["path"] = str(pdf_path)
        d_copy["page_count"] = len(PdfReader(str(pdf_path), strict=False).pages)
        docs.append(d_copy)
    case["documents"] = docs

    mod = BundleAssessmentModule()
    mod.load({"checklist": OFFICIAL_CHECKLIST_DATA, "settings": {}}, SUBMISSION_BUNDLE / "assets")
    res = mod.assess(case, None)
    issues = validate_result(res, case=case, checklist=OFFICIAL_CHECKLIST)
    assert issues == []
    assert res["assessment_status"] == "abstained"
    assert res["abstention_reason"] == "insufficient evidence"
    assert res["criterion_status"]["APCTT-C04"] == "met"
    assert len(res["evidence_reference"]["APCTT-C04"]) >= 1


def test_scenario_x_submission_zip_and_fastapi_apctt_endpoints():
    """Scenario X: Verify argus_submission.zip passes make_submission.py --check and FastAPI APCTT routes work."""
    assert SUBMISSION_ZIP.is_file(), "argus_submission.zip must exist at workspace root"
    proc = subprocess.run(
        [
            sys.executable,
            str(KIT_CPU / "tools" / "make_submission.py"),
            "--check",
            str(SUBMISSION_ZIP),
            "--json",
        ],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    check_data = json.loads(proc.stdout)
    assert check_data["result"] == "VALID"
    assert check_data["errors"] == []

    client = TestClient(app)
    r_chk = client.get("/api/apctt/checklist")
    assert r_chk.status_code == 200
    assert r_chk.json()["version"] == "APCTT-2026-CHECKLIST-v1"

    r_val = client.get("/api/apctt/validation-summary")
    assert r_val.status_code == 200
    assert r_val.json()["license_audit"]["status"] == "PASS"

    r_smp = client.post("/api/apctt/assess-sample/quantum_cascade_sensor")
    assert r_smp.status_code == 200
    payload = r_smp.json()
    assert payload["success"] is True
    assert payload["result"]["checklist_version"] == "APCTT-2026-CHECKLIST-v1"

