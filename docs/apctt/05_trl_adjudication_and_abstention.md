# 05 — TRL Adjudication, Target Scope & Calibrated Abstention

## 1. Evidence-Backed TRL 1–9 Adjudication
ARGUS determines a defensible integer Technology Readiness Level (`1 <= predicted_trl <= 9`) from the progression of satisfied criteria, test environment fidelity, and target scope:
- **TRL 1–3 (Foundational & Proof-of-Concept):** Governing equations and physical principles (`TRL 1`), application concept formulation (`TRL 2`), and analytical/experimental proof of concept (`TRL 3`).
- **TRL 4 (Laboratory / Desktop Integration):** Functional integration of components or coupled software packages verified in a laboratory bench setup, water tank, or example-dataset environment.
- **TRL 5–6 (Relevant Environment Validation & Demonstration):** Validation in a relevant environment (`TRL 5`) and demonstration of a calibrated prototype or numerical model across multi-period empirical observations with statistical performance verification (`TRL 6`).
- **TRL 7 (Operational Environment Prototype Demonstration):** Demonstration in an operational environment (e.g., field-deployed system prototype or operational flood-inundation map library linked to real-time streamgages and high-water marks).
- **TRL 8–9 (Qualification & Mission Operations):** Actual system completed and qualified through formal test, demonstration, and release qualification (`TRL 8`), and actual system proven in successful mission operations across real events (`TRL 9`).

## 2. Target Scope & Environment Enforcement
- Respects `case["assessment_target"]["type"]` (`component`, `subsystem`, `system`, `technology`), `case["intended_application"]`, and `case["intended_environment"]`.
- If `target_type == "component"` and only component bench testing is reported without system-level mission operations, `predicted_trl` is capped appropriately.
- Explicit negative statements (e.g., `"flight demonstration was not performed"`) establish a strict upper maturity ceiling.

## 3. Calibrated Abstention & Controlled Failure Handling
- **Abstention (`assessment_status = "abstained"`, `predicted_trl = None`, `error_code = None`):**
  - `"out of scope"`: Zero lexical/topical overlap between `assessment_target` and document corpus.
  - `"ambiguous scope"`: Target definition leaves the assessed element unspecified or mixes incompatible targets.
  - `"conflicting evidence"`: Unresolved contradiction between positive maturity claims and global negations/retractions of equal or later `document_date`.
  - `"insufficient evidence"`: Synthetic fixtures (`DEMO-001`) or sparse notes lacking verifiable technical evidence.
- **Controlled Failure (`assessment_status = "failed"`, `predicted_trl = None`, `abstention_reason = None`):**
  - Triggered on missing/unreadable PDFs (`DOCUMENT_UNREADABLE`, `DOCUMENT_FILE_NOT_FOUND`), empty extracted text (`EMPTY_DOCUMENT_TEXT`), page count mismatch (`PAGE_COUNT_MISMATCH`), or exhausted time budget (`TIME_BUDGET_EXCEEDED`). All optional fields are omitted per `failed_omits_optional`.

