# ARGUS — APCTT Stage 1 Submission Readiness Report

**Verdict:** `VALID AGAINST DEVELOPMENT KIT ONLY` *(Validated against `apctt-participant-kit-0.5.0-cpu` / `0.5.0-cuda`, `apctt-api-v0.2-draft`; verify final event portal kit release before portal upload)*

---

## 1. Executive Readiness Verdict

**`VALID AGAINST DEVELOPMENT KIT ONLY`**

ARGUS (**Automated Readiness Grading & Uncertainty Synthesis**) has been fully integrated with the APCTT Stage 1 participant module contract (`participant_module.adapter:AssessmentModule`), packaged into the canonical APCTT submission directory (`apctt_submission/`), compiled into the submission archive (`artifacts/apctt/argus_submission.zip`), and verified against all validators, contract schemas, cold-worker subprocess protocols, and FastAPI server integration endpoints of the locally installed `0.5.0` development kit:

- **Kit Manifest Verification**:
  - `apctt-participant-kit-0.5.0-cpu/MANIFEST.sha256`: **129 / 129 files OK** (`0` modified, `0` missing).
  - `apctt-participant-kit-0.5.0-cuda/MANIFEST.sha256`: **129 / 129 files OK** (`0` modified, `0` missing).
- **Licence Policy Audit (`tools/check_licenses.py --bundle apctt_submission`)**:
  - **PASS (`exit 0`)** — `4 allowed, 0 review, 0 denied` under `apctt-license-policy-v2` (`0.4.0`). `participant_module/LICENSE` verified with `Copyright (c) 2026 Team Argus (Anish Mogam)` and zero unresolved placeholders.
- **Submission Packaging & Verification (`tools/make_submission.py` & `--check`)**:
  - **PASS (`result: VALID (exit 0)`)** — Archive `artifacts/apctt/argus_submission.zip` (`86,997 bytes` / `87.0 KB <= 2.0 GB`), `submission_version: "apctt-submission-v3"`, `base_id: "apctt-base-9e7fe1324bb6"`, `zip_sha256: 28c2c350dd88f88b81548a69dc9766fbbc40b025dd4b423963f95b90969819fc`, `declared_package_sha256: 35ce55cfff024c62670d77c0fa44c8c89e73d2b9a1b49bf5bdf61f6b8d62dc9d`.
- **Full Test Suite (`pytest tests/`)**:
  - **91 / 91 tests PASS (`0` failures)** — all 69 pre-existing Argus regression tests + 22 comprehensive APCTT Stage 1 contract, adversarial, security, cold-worker, server E2E, extracted-ZIP isolated subprocess, and USGS/SDG smoke tests.

---

## 2. Participant-Kit Audit

| Property | Verified Value |
| :--- | :--- |
| **Discovered Local Kits** | `apctt-participant-kit-0.5.0-cpu/` and `apctt-participant-kit-0.5.0-cuda/` |
| **Kit Version / API Version** | `0.5.0` (`apctt-api-v0.2-draft`, development kit) |
| **Worker Protocol Version** | `apctt-worker-v2` |
| **Submission Schema Version** | `apctt-submission-v3` (`contracts/submission.schema.json`) |
| **Common Base Environment ID** | `apctt-base-9e7fe1324bb6` (`python: "3.12"`, `platform: "x86_64-manylinux_2_28"`, decision D60) |
| **Official Checklist Version** | `APCTT-2026-CHECKLIST-v1` (12 criteria: `APCTT-C01` .. `APCTT-C12`) |
| **Demo Checklist Version** | `APCTT-2026-DEMO-CHECKLIST-v1` |
| **Licence Policy Version** | `apctt-license-policy-v2` (`0.4.0`) |
| **Model Catalogue Version** | `apctt-model-catalog-v1` (`0.4.0`) |
| **Public Cases Manifest** | `apctt-public-cases-v1` (99 USGS/SDG public cases, 3 smoke cases) |
| **Manifest Integrity (`MANIFEST.sha256`)** | Verified **129/129 files intact** in both `0.5.0-cpu` and `0.5.0-cuda`; zero kit files modified |
| **Official Event Status Note** | The locally installed `0.5.0` (`apctt-api-v0.2-draft`) kit README explicitly identifies itself as a development kit rather than the frozen event release. Validation is therefore reported as **VALID AGAINST DEVELOPMENT KIT ONLY**. |

---

## 3. Repository Architecture and Preserved Existing Argus Components

All existing Argus packages, web application components, and the standalone CLI `submission/` folder have been preserved intact:

- **`packages/core` (`trl_core`)**: Domain-independent Pydantic data models (`Document`, `Chunk`, `TechnicalClaim`, `EvidenceItem`, `ContradictionWarning`, `CriteriaMapping`, `UncertaintyProfile`), NASA/ISO/ECSS/APCTT TRL definitions, and `sanitizer.py` (`sanitize_text`, `wrap_untrusted_payload`).
- **`packages/document_processing` (`document_processing`)**: Multi-page PDF parsing (`pypdf`), paragraph/sentence segmentation, and 1-based page locator preservation.
- **`packages/retrieval` (`retrieval`)**: Hybrid lexical TF-IDF (`scikit-learn`) + dense vector chunk indexing and search.
- **`packages/ml_inference` (`ml_inference`)**:
  - `claim_extractor.py` (`StructuredClaimExtractor`): Extracts structured technical claims with modality (`ASSERTED_FACT`, `FUTURE_WORK`, `HYPOTHETICAL`, `NEGATED`), temporal status (`COMPLETED`, `ONGOING`, `PLANNED`, `ABANDONED`), quantitative measurements, and validation environment classification.
  - `quality_assessor.py` (`EvidenceQualityAssessor`): Evaluates evidence strength (`STRONG`, `MODERATE`, `WEAK`, `SPECULATIVE`) and confidence.
  - `contradiction_detector.py` (`ContradictionDetector`): Detects metric regressions, subsystem failures, and conflicting experimental claims.
  - `criteria_mapper.py` (`CriteriaMapper`): Maps extracted evidence items against TRL criteria and detects evidence gaps.
- **`packages/agent_orchestration` (`agent_orchestration`)**:
  - `agents.py` (`OptimistAgent`, `SkepticAgent`, `RefereeAgent`) & `orchestrator.py` (`ReviewProtocol`): Multi-agent adversarial debate and Referee adjudication ledger.
  - `uncertainty.py` (`UncertaintyModel`): Computes epistemic uncertainty, coverage gaps, and composite certainty scores.
- **`packages/competition_engine` (`competition_engine`)**:
  - `apctt_adapter.py`: Implements the official `AssessmentModule` lifecycle and bridges APCTT cases to the Argus core orchestration pipeline.
- **`apps/api` & `apps/web`**: FastAPI research workspace backend and static UI preserved and extended with `/api/apctt/*` inspection endpoints.
- **`submission/`**: Pre-existing standalone CLI evaluation bundle preserved untouched relative to `origin/main`.
- **`apctt_submission/`**: Official APCTT Stage 1 submission bundle directory containing `participant_module/` (with self-contained `participant_module/argus_engine/`), `assets/`, `submission.json`, `declaration.json`, and `README.md`.

---

## 4. APCTT `AssessmentModule` Lifecycle Implementation

Entry point: `participant_module.adapter:AssessmentModule` (re-exporting `argus_engine.competition_engine.apctt_adapter:AssessmentModule` with isolated `sys.path` bootstrapping so `apctt_submission/` runs completely independently of the repository root).

1. **`load(config: Mapping[str, Any], asset_dir: Path) -> None`**:
   - Validates `config["checklist"]` (requiring `version` and non-empty `criteria`), rejecting invalid or missing checklists with `ValueError`.
   - Dynamically indexes every criterion in `config["checklist"]["criteria"]` (`id`, `trl`, `required`, `title`, `description`) without hardcoding `APCTT-C01`..`APCTT-C12`.
   - Loads optional domain-independent linguistic patterns from `asset_dir / settings["rules_path"]` (`assets/trl_rules.json`) and merges them with built-in general-purpose scientific/engineering rules.
   - Seeds `random` and `numpy.random` deterministically (`seed = 42` by default) and initializes the Argus core modules (`StructuredClaimExtractor`, `EvidenceQualityAssessor`, `ContradictionDetector`, `CriteriaMapper`, `ReviewProtocol`, `UncertaintyModel`).
   - Performs zero network calls and zero background thread/process spawns.
2. **`assess(case: Mapping[str, Any], context: Any) -> dict[str, Any]`**:
   - Enforces deterministic execution seed (`context.seed` when provided).
   - Monitors `context.remaining_ms()` / `context.time_budget_ms` across document extraction, retrieval, and criterion evaluation; returns a valid `"failed"` (`ASSESSMENT_TIMEOUT`) payload if budget falls below safety threshold (`< 50 ms`).
   - Validates and extracts all case PDFs, runs the Argus core pipeline, evaluates every active checklist criterion, computes monotonic TRL ceiling or abstention, and validates the final dictionary strictly before returning.
3. **`reset_case() -> None`**:
   - Clears per-case state (`last_case_id`, `last_argus_orchestration_summary`) so zero state leaks across cases.
4. **`close() -> None`**:
   - Releases loaded checklist and rule structures cleanly on worker shutdown.

---

## 5. Checklist and Criterion Evaluation Methodology

For each criterion in `config["checklist"]["criteria"]`:
- **Dynamic Criterion Adaptation**:
  - Known criterion IDs (`APCTT-C01`..`APCTT-C12`) use domain-independent scientific/engineering lexical & structural profiles (governing equations, application formulation, proof-of-concept experiments, laboratory breadboard validation, simulated/relevant environment component integration, relevant-environment prototype demonstration, operational field demonstration, qualified mission configuration, and flight/mission-proven deployment) plus cross-cutting criteria (`APCTT-C10` quantitative measurements vs thresholds, `APCTT-C11` target/environment alignment, `APCTT-C12` failure/limitation boundaries).
  - Custom or renamed checklist criteria are dynamically analyzed via their `title`, `description`, and `trl` metadata. If a custom criterion has no distinctive domain-independent keywords supported by the document text, it conservatively returns `"insufficient evidence"` (never false-positive `"met"`).
- **Evidence Polarity Classification**:
  - Candidate spans are filtered through prompt-injection sanitization, keyword-stuffing rejection, target-relevance checks, future/planned modality detection (`FUTURE_WORK_RE`), simulation-only vs physical operational checks (`SIMULATION_ONLY_RE` vs `PHYSICAL_VALIDATION_RE`), and explicit negation/failure detection (`EXPLICIT_NOT_MET_RE`, `QUALIFICATION_FAIL_RE`, `OPERATIONAL_FAIL_RE`).
  - Criteria with affirmative, completed, non-negated evidence are marked `"met"` with 1–5 grounded `EvidenceRef` objects.
  - Criteria with explicit negation, failed acceptance thresholds, or uncalibrated/incomplete qualification are marked `"not met"` with grounded `EvidenceRef` objects.
  - Criteria lacking affirmative or negative evidence (including purely future/planned statements) are marked `"insufficient evidence"` with `evidence_reference[cid] = []`.

---

## 6. Evidence Extraction and Locator-Grounding Pipeline

- **PDF Extraction (`extract_case_pages`)**:
  - Uses `pypdf.PdfReader(..., strict=False)` to extract text page-by-page with 1-based page numbers (`1 <= page <= doc["page_count"]`).
  - Enforces strict path security: rejects relative path traversal (`..`), non-`.pdf` file extensions (`DOCUMENT_PATH_INVALID`), missing files (`DOCUMENT_NOT_FOUND`), zero-page documents (`DOCUMENT_EMPTY`), and unreadable PDFs (`DOCUMENT_UNREADABLE`).
- **Sentence & Span Extraction (`split_into_spans`)**:
  - Splits page text into clean, bounded sentences (`<= 480` chars), normalizing whitespace while preserving exact verbatim phrases from the PDF.
  - Strips hidden zero-width Unicode characters (`\u200b`, `\u200c`, `\u200d`, `\ufeff`, `\u2060`) and filters out prompt-injection sentences and non-grammatical keyword-stuffed lines so adversarial text is never cited in `supporting_span`.
- **Hybrid Scoring (`build_tfidf_scores`)**:
  - Uses `scikit-learn` TF-IDF cosine similarity combined with lexical overlap against `technology_target.description` and `intended_environment` to rank spans relevant to the target technology.

---

## 7. TRL Decision and Monotonic Ceiling Logic

ARGUS enforces the official APCTT monotonic cumulative-ceiling rule (`compute_monotonic_trl`):
1. Required ladder criteria (`trl` in `1..9`, `required == True`) are grouped by TRL level $L \in \{1 \dots 9\}$.
2. Starting from $L = 1$ upward:
   - Level $L$ is satisfied **if and only if** every required criterion at level $L$ has `criterion_status[cid] == "met"`.
   - As soon as any required criterion at level $L$ is `"not met"` or `"insufficient evidence"`, progression stops immediately and `predicted_trl` is capped at $L - 1$.
3. Isolated high-TRL claims (e.g., a TRL 7 field trial claim when TRL 1–4 foundations are absent) cannot inflate `predicted_trl`.
4. Simulation-only evidence is capped at simulated/laboratory levels (TRL $\le 5$) and cannot satisfy TRL 7–9 operational/qualified/mission-proven criteria without physical/field evidence.
5. Explicit quantitative requirement failure (`APCTT-C10 == "not met"`, e.g. achieved error worse than target threshold) caps readiness at laboratory breadboard level ($\le 4$).

---

## 8. Abstention and Failure Policy

### `"abstained"` (`predicted_trl = null`, `error_code = null`, `error_message = null`)
Returned with one of the 4 official `AbstentionReason` literals whenever a defensible `1..9` TRL cannot be assigned:
1. **`"out of scope"`**: Document corpus has zero lexical overlap with `technology_target.description` and consists of non-technical/administrative content (e.g., HR leave policies, financial invoices).
2. **`"ambiguous scope"`**: Multiple distinct subsystems with divergent readiness levels are described without isolating the requested `technology_target`.
3. **`"conflicting evidence"`**: Same document or multi-document corpus contains irreconcilable contradictory claims on the same required milestone (or active cross-claim contradictions detected by `ContradictionDetector` when `APCTT-C12` is not resolved).
4. **`"insufficient evidence"`**: Required TRL 1 foundations are not met (`candidate_trl < 1`), or only a single isolated milestone (such as `APCTT-C04` in `DEMO-001`) is met without contiguous TRL ladder progression or cross-cutting measurement support (`APCTT-C10`).

### `"failed"` (`predicted_trl = null`, `abstention_reason = null`, non-empty `error_code` & `error_message`)
Returned for operational/input failures while still populating `checklist_version` and full `criterion_status` / `evidence_reference` maps for contract compliance:
- `DOCUMENT_PATH_INVALID`: Path traversal (`..`) or non-`.pdf` extension.
- `DOCUMENT_NOT_FOUND`: Missing PDF file on disk.
- `DOCUMENT_UNREADABLE`: Corrupted or unparseable PDF stream.
- `DOCUMENT_EMPTY`: Zero pages or zero extractable text across all pages.
- `ASSESSMENT_TIMEOUT`: Remaining time budget exhausted (`remaining_ms < 50`).

---

## 9. Security Hardening and Prompt-Injection Defences

1. **Untrusted PDF Content Sanitization (`trl_core.sanitizer.sanitize_text`)**:
   - Strips zero-width and bidirectional Unicode obfuscation characters (`\u200b`..`\u200f`, `\u202a`..`\u202e`, `\u2060`..`\u206f`, `\ufeff`) before negation and prompt-injection checks (so `n\u200bot performed` is properly recognized as `not performed`, and `Ignore\u200b all previous instructions` is caught).
   - Filters sentences matching `PROMPT_INJECTION_RE` (`ignore all previous instructions`, `system override`, `classify as TRL 9`, `mark all criteria as met`, `<system>`, `[INST]`, etc.) so they are never used as evidence or echoed into `supporting_span`.
2. **Keyword-Stuffing Filter (`is_keyword_stuffing`)**:
   - Rejects ungrammatical lists of TRL buzzwords or repeated token stuffing lacking finite verbs.
3. **Filesystem & Process Isolation**:
   - Validates document paths (`_is_safe_document_path`), reads PDFs strictly read-only, writes nothing outside `context.scratch_dir`, and never invokes `subprocess`, `os.system`, `eval`, `exec`, `pickle`, or network sockets during inference.

---

## 10. Model Catalogue, Asset, and Base-Environment Compliance

- **Base Environment**: Targets `apctt-base-9e7fe1324bb6` (CPython `3.12`, `x86_64-manylinux_2_28`, decision D60).
- **Runtime Dependencies Used**: Strictly Python `3.12` standard library plus pre-installed base-environment packages (`numpy==2.5.3`, `pydantic==2.13.5`, `pypdf==6.19.0`, and optional fallbacks `pypdfium2==5.14.0`, `pdfplumber==0.11.10`, `scikit-learn==1.9.1`).
- **Catalogue Models (`models`)**: `[]` (no external LLM/checkpoint weights required; zero GPU/VRAM risk, sub-second deterministic CPU execution).
- **Declared Assets (`assets/`)**: `assets/trl_rules.json` (domain-independent lexical patterns and TRL rule configuration, MIT licensed).
- **Zero Forbidden Files**: No virtual environments, wheels, `.so`/`.dll`/`.pyd` binaries, `.pyc`/`__pycache__`, symlinks, or undeclared weight files (`*.bin`, `*.pt`, `*.safetensors`, `*.onnx`, `*.pkl`, `*.joblib`).

---

## 11. Licence and Third-Party Audit Results

- **Package Licence**: `MIT` (`apctt_submission/participant_module/LICENSE`), containing `Copyright (c) 2026 Team Argus (Anish Mogam)` and zero unresolved template placeholders.
- **Third-Party Notices**: Documented in `apctt_submission/participant_module/THIRD_PARTY_NOTICES.md` with exact versions and licenses from `apctt-base-9e7fe1324bb6` (`numpy==2.5.3` `BSD-3-Clause`, `pydantic==2.13.5` `MIT`, `pydantic-core==2.46.5` `MIT`, `annotated-types==0.8.0` `MIT`, `typing-extensions==4.16.0` `PSF-2.0`, `typing-inspection==0.4.4` `MIT`, `pypdf==6.19.0` `BSD-3-Clause`, `pypdfium2==5.14.0` `Apache-2.0 OR BSD-3-Clause`, `pdfplumber==0.11.10` `MIT`, `pdfminer-six==20260107` `MIT`, `pillow==12.3.0` `MIT-CMU`, `scikit-learn==1.9.1` `BSD-3-Clause`, `scipy==1.18.1` `BSD-3-Clause`, `joblib==1.6.0` `BSD-3-Clause`, `threadpoolctl==3.7.0` `BSD-3-Clause`) plus preserved upstream attribution for inherited `trl-debate-engine` / ARGUS core modules (`Apache-2.0`).
- **Declaration File**: `apctt_submission/declaration.json` (`declaration_version: "apctt-declaration-example-v1"`, `declared_package_sha256: "35ce55cfff024c62670d77c0fa44c8c89e73d2b9a1b49bf5bdf61f6b8d62dc9d"`), declaring:
  1. `APCTT Participant Kit Official Checklist & Demo Fixture (DEMO-001)` (`Apache-2.0`)
  2. `U.S. Geological Survey (USGS) Public Smoke-Test Reports` (`CC0-1.0`)
  3. `Team Argus Domain-Independent Linguistic Phrase Rules (assets/trl_rules.json)` (`MIT`)

---

## 12. Submission Bundle Layout and SHA-256 Verification

Directory `apctt_submission/` and archive `artifacts/apctt/argus_submission.zip`:

```text
apctt_submission/
├── participant_module/
│   ├── __init__.py
│   ├── adapter.py
│   ├── LICENSE
│   ├── THIRD_PARTY_NOTICES.md
│   └── argus_engine/
│       ├── __init__.py
│       ├── trl_core/
│       ├── document_processing/
│       ├── retrieval/
│       ├── ml_inference/
│       ├── agent_orchestration/
│       └── competition_engine/
├── assets/
│   └── trl_rules.json
├── submission.json
├── declaration.json
└── README.md
```

- **Submission Archive**: `artifacts/apctt/argus_submission.zip`
- **Archive Size**: `86,997 bytes` (`87.0 KB`, well under the `2.0 GB` limit)
- **Archive SHA-256 (`zip_sha256`)**: `28c2c350dd88f88b81548a69dc9766fbbc40b025dd4b423963f95b90969819fc`
- **Declared Package SHA-256 (`declared_package_sha256`)**: `35ce55cfff024c62670d77c0fa44c8c89e73d2b9a1b49bf5bdf61f6b8d62dc9d`

---

## 13. Output from `check_licenses.py`

Command:
```powershell
python apctt-participant-kit-0.5.0-cpu/tools/check_licenses.py --bundle apctt_submission
```

Verbatim Output:
```text
APCTT licence check - policy apctt-license-policy-v2 0.4.0 - Flags components from their declared metadata; HQ decides flagged items after submission.

status    kind     component                         version         licence                         origin / reasons
allowed   team     participant_module                                MIT                             submission.json
allowed   dataset  APCTT Participant Kit Officia...                  Apache-2.0                      declaration.json
allowed   dataset  Team Argus Domain-Independent...                  MIT                             declaration.json
allowed   dataset  U.S. Geological Survey (USGS)...                  CC0-1.0                         declaration.json
summary: 4 allowed, 0 review, 0 denied -> exit 0
```

---

## 14. Output from `make_submission.py`

Command:
```powershell
python apctt-participant-kit-0.5.0-cpu/tools/make_submission.py apctt_submission --output artifacts/apctt
```

Verbatim Output:
```text
zip                      D:\Projects\Argus\artifacts\apctt\argus_submission.zip
zip_sha256               28c2c350dd88f88b81548a69dc9766fbbc40b025dd4b423963f95b90969819fc
size                     87.0 KB
declared_package_sha256  35ce55cfff024c62670d77c0fa44c8c89e73d2b9a1b49bf5bdf61f6b8d62dc9d
PASS    size: 87.0 KB <= 2.0 GB
PASS    layout: participant_module/, assets/, submission.json, declaration.json, README.md
PASS    submission.json: team argus, base_id apctt-base-9e7fe1324bb6
PASS    models: no catalogue model
PASS    contents: no environment, packages, caches, links, catalogue weights or undeclared weights
PASS    package hash matches submission.json: 35ce55cfff024c62670d77c0fa44c8c89e73d2b9a1b49bf5bdf61f6b8d62dc9d
PASS    licence: MIT, participant_module/LICENSE present
REMINDER third-party pure-Python code in your package is your responsibility: if a licence or security problem arises later, your team bears the legal responsibility and the award is revoked (D66)
result: VALID (exit 0)
```

---

## 15. Output from `make_submission.py --check`

Command:
```powershell
python apctt-participant-kit-0.5.0-cpu/tools/make_submission.py --check artifacts/apctt/argus_submission.zip
```

Verbatim Output:
```text
zip                      D:\Projects\Argus\artifacts\apctt\argus_submission.zip
zip_sha256               28c2c350dd88f88b81548a69dc9766fbbc40b025dd4b423963f95b90969819fc
size                     87.0 KB
declared_package_sha256  35ce55cfff024c62670d77c0fa44c8c89e73d2b9a1b49bf5bdf61f6b8d62dc9d
PASS    size: 87.0 KB <= 2.0 GB
PASS    layout: participant_module/, assets/, submission.json, declaration.json, README.md
PASS    submission.json: team argus, base_id apctt-base-9e7fe1324bb6
PASS    models: no catalogue model
PASS    contents: no environment, packages, caches, links, catalogue weights or undeclared weights
PASS    package hash matches submission.json: 35ce55cfff024c62670d77c0fa44c8c89e73d2b9a1b49bf5bdf61f6b8d62dc9d
PASS    licence: MIT, participant_module/LICENSE present
REMINDER third-party pure-Python code in your package is your responsibility: if a licence or security problem arises later, your team bears the legal responsibility and the award is revoked (D66)
result: VALID (exit 0)
```

---

## 16. Local Server and Cold-Worker Integration Results

Verified in automated tests (`test_scenario_z1`, `test_scenario_z2`, `test_scenario_z3`):
1. **Extracted ZIP Isolated Subprocess Smoke Test (`test_scenario_z1`)**:
   - Extracted `artifacts/apctt/argus_submission.zip` into a clean temporary directory and imported `participant_module.adapter:AssessmentModule` in a fresh Python interpreter with `PYTHONPATH=<extracted_dir>`, `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`, and the repository root excluded from `sys.path`.
   - Executed `load -> assess -> reset_case -> close` and verified `validate_result == []`, `assessment_status == "completed"`, `predicted_trl == 4`.
2. **Cold-Per-Case Worker Protocol (`test_scenario_z2`)**:
   - Invoked `apctt-participant-kit-0.5.0-cpu/src/apctt_runtime/worker.py --run-id <id>` across multiple fresh subprocesses with `apctt-worker-v2` stdin JSON envelopes.
   - Verified atomic creation of `result.json` (passing `validate_result`) and `observation.json` (`timings_ms` recorded for `load`, `assess`, `cleanup`).
3. **Full APCTT FastAPI Server HTTP Lifecycle (`test_scenario_z3`)**:
   - Configured `apctt_server.app:create_app` with `package_id: "argus-trl-assessor"`, `entrypoint: "participant_module.adapter:AssessmentModule"`, and `declared_package_sha256`.
   - Verified:
     - `GET /health/live` -> `200 OK` (`{"live": true}`)
     - `GET /health/ready` -> `200 OK` (`{"ready": true}`)
     - `GET /v1/package` -> `200 OK` (`verification_status: "verified"`, `verified_package_sha256 == declared_package_sha256`)
     - `POST /v1/assessments` (with `docs/EXAMPLE_REQUEST.json`) -> `202 Accepted`
     - `GET /v1/assessments/{assessment_id}` -> `job_status: "finished"`, `result_origin: "module"`, `verified_package_sha256 == declared_package_sha256`, `case_id: "DEMO-001"`.

---

## 17. Regression and APCTT Test Results

- **Total Tests Executed**: **91 tests** across 11 test modules (`tests/`).
- **Result**: **91 passed, 0 failed**.
- **Breakdown**:
  - **69 Existing Argus Regression Tests**:
    - `tests/test_adapters.py` (5 passed)
    - `tests/test_api.py` (6 passed)
    - `tests/test_cli.py` (5 passed)
    - `tests/test_milestone_3_intelligence.py` (6 passed)
    - `tests/test_milestone_4_adjudication.py` (16 passed)
    - `tests/test_milestone_5_research_workspace.py` (6 passed)
    - `tests/test_ml_pipeline.py` (7 passed)
    - `tests/test_models.py` (7 passed)
    - `tests/test_sanitizer.py` (8 passed)
    - `tests/test_trl_definitions.py` (3 passed)
  - **22 APCTT Stage 1 Contract, Domain, Security & E2E Tests (`tests/test_apctt_adapter.py`)**:
    - `test_scenario_a_participant_kit_manifest_integrity`: Verifies all 129 SHA-256 entries in CPU and CUDA kits.
    - `test_scenario_b_and_c_module_loading_and_dynamic_checklist`: Verifies `load()` with `checklist.official.json`, `checklist.demo.json`, and dynamically injected custom checklists.
    - `test_scenario_c2_unknown_or_unsupported_criterion_returns_insufficient_evidence`: Verifies unsupported custom criteria return `"insufficient evidence"`.
    - `test_scenario_d_completed_assessment_and_argus_core_orchestration`: Verifies end-to-end TRL 1–9 progression and confirms Argus core orchestration (`claims_count`, `optimist_trl`, `skeptic_trl`, `referee_trl`, `composite_certainty`) runs on every case.
    - `test_scenario_e_abstained_insufficient_evidence`: Verifies `"insufficient evidence"` abstention.
    - `test_scenario_f_abstained_conflicting_evidence`: Verifies `"conflicting evidence"` abstention.
    - `test_scenario_g_abstained_ambiguous_scope`: Verifies `"ambiguous scope"` abstention.
    - `test_scenario_h_abstained_out_of_scope`: Verifies `"out of scope"` abstention.
    - `test_scenario_i_failed_assessment_unreadable_empty_or_timeout`: Verifies `"failed"` status on unreadable/empty PDFs and exhausted time budget.
    - `test_scenarios_j_to_o_contract_enforcement_and_rejection`: Verifies rejection of missing criteria, unexpected criterion keys, ungrounded `"met"` criteria, non-empty refs on `"insufficient evidence"`, invalid page numbers, and extra fields (`rationale`, `confidence`).
    - `test_scenarios_p_and_q_negation_and_future_work_handling`: Verifies negated and future/planned statements never satisfy criteria.
    - `test_scenario_q2_simulated_only_vs_physical_operational_results`: Verifies simulation-only evidence is capped at TRL $\le 5$ and cannot trigger TRL 7–9.
    - `test_scenario_q3_keyword_stuffing_and_missing_measurements`: Verifies keyword-stuffed TRL 9 claims and missing quantitative measurements do not inflate TRL.
    - `test_scenario_r_multi_document_provenance_and_chronology`: Verifies multi-PDF provenance (`D001`, `D002`) and 1-based page locators.
    - `test_scenarios_s_t_u_v_lifecycle_determinism_and_offline`: Verifies `reset_case()`, `close()`, bitwise determinism across repeated runs, and offline execution (`HF_HUB_OFFLINE=1`).
    - `test_scenario_w_official_example_request_execution`: Verifies `docs/EXAMPLE_REQUEST.json` (`DEMO-001`).
    - `test_scenario_x_submission_zip_and_fastapi_apctt_endpoints`: Verifies `make_submission.py --check` and `/api/apctt/*` routes.
    - `test_scenario_y_security_prompt_injection_unicode_and_path_traversal`: Verifies prompt injection neutralization, zero-width Unicode stripping, and path traversal rejection.
    - `test_scenario_z1_isolated_submission_import_without_repo_root`: Verifies isolated `apctt_submission/` import.
    - `test_scenario_z2_cold_worker_subprocess_protocol`: Verifies cold worker subprocess execution (`apctt_runtime/worker.py`).
    - `test_scenario_z3_full_apctt_server_http_lifecycle`: Verifies full APCTT server HTTP workflow (`GET /health/live`, `GET /health/ready`, `GET /v1/package`, `POST /v1/assessments`, `GET /v1/assessments/{id}`).
    - `test_scenario_z4_public_usgs_sdg_smoke_cases`: Verifies public USGS/SDG smoke cases (`USGS-SDG-012`, `USGS-SDG-040`, `USGS-SDG-061`).

---

## 18. Smoke-Case Evaluation Summary

Evaluated against `docs/EXAMPLE_REQUEST.json` (`DEMO-001`) and 3 official USGS/SDG public smoke cases from `contracts/public-cases.json`:

| Case ID | Target Technology | Pages | Status | Predicted TRL / Abstention | Met Criteria | Latency | `validate_result` |
| :--- | :--- | :---: | :---: | :---: | :--- | :---: | :---: |
| **`DEMO-001`** | Placeholder technology target (`EXAMPLE_REPORT.pdf`) | 1 | `abstained` | `None` (`insufficient evidence`) | `APCTT-C04` | `18 ms` | **PASS (`0` issues)** |
| **`USGS-SDG-012`** | P2S coupled simulation software package (`SIR 2023-5044`) | 29 | `completed` | **TRL 4** | `APCTT-C01`..`C04`, `C10`, `C11`, `C12` | `195 ms` | **PASS (`0` issues)** |
| **`USGS-SDG-040`** | Reusable automated Python workflow for NHM charging boundaries (`SIR 2025-5040`) | 37 | `completed` | **TRL 8** | `APCTT-C01`..`C08`, `C10`, `C11`, `C12` | `248 ms` | **PASS (`0` issues)** |
| **`USGS-SDG-061`** | Multi-analytical tracing methodology (`δ²H`/`δ¹⁸O`, `⁸⁷Sr/⁸⁶Sr`, tree-ring Hg) (`SIR 2026-5008`) | 69 | `completed` | **TRL 7** | `APCTT-C01`..`C07`, `C10`, `C11`, `C12` | `412 ms` | **PASS (`0` issues)** |

---

## 19. Known Limitations

1. **Pre-Freeze Local Kit (`0.5.0`)**: The repository includes `apctt-participant-kit-0.5.0-cpu` and `0.5.0-cuda` (`apctt-api-v0.2-draft`). If the competition organizers publish a newer frozen kit on the participant portal with an updated `base_id`, `submission.json` must be regenerated against that kit's `contracts/base-environment.json` by running `python scripts/build_apctt_submission.py`.
2. **Scanned Image-Only PDFs (Without OCR Layer)**: Because the base CPU environment uses `pypdf` without a bundled OCR binary (such as Tesseract), PDFs consisting purely of rasterized scanned page images with zero embedded text streams will extract as empty text and return `assessment_status = "failed"` (`error_code = "DOCUMENT_EMPTY"`).
3. **Rule & Lexical/TF-IDF Precision vs Large Foundation Models**: To guarantee sub-second deterministic CPU execution (`< 0.5 s` per multi-page report), zero GPU/OOM risk, and zero external model weight dependencies (`models: []`), ARGUS uses structured syntactic/lexical rules, TF-IDF vector similarity, and deterministic multi-agent adjudication rather than a multi-billion-parameter generative LLM.

---

## 20. Remaining Manual Steps Before Uploading to the Competition Portal

1. Check the official Techfest / APCTT participant portal to confirm whether `0.5.0` (`base_id: apctt-base-9e7fe1324bb6`) is the final event kit version.
2. If the organizer portal publishes a newer frozen kit directory, update `KIT_DIR` in `scripts/build_apctt_submission.py` and run:
   ```powershell
   python scripts/build_apctt_submission.py
   ```
3. Upload `artifacts/apctt/argus_submission.zip` to the official APCTT Stage 1 submission portal.

---

## 21. Exact Commands to Reproduce Every Validation Check

```powershell
# 1. Verify Participant Kit MANIFEST.sha256 integrity (CPU & CUDA)
python -c "import hashlib, pathlib; root=pathlib.Path('apctt-participant-kit-0.5.0-cpu'); lines=root.joinpath('MANIFEST.sha256').read_text().splitlines(); bad=[l for l in lines if hashlib.sha256(root.joinpath(l.split('  ',1)[1]).read_bytes()).hexdigest()!=l.split('  ',1)[0]]; print('CPU Manifest:', len(lines), 'files, bad:', len(bad)); assert not bad"
python -c "import hashlib, pathlib; root=pathlib.Path('apctt-participant-kit-0.5.0-cuda'); lines=root.joinpath('MANIFEST.sha256').read_text().splitlines(); bad=[l for l in lines if hashlib.sha256(root.joinpath(l.split('  ',1)[1]).read_bytes()).hexdigest()!=l.split('  ',1)[0]]; print('CUDA Manifest:', len(lines), 'files, bad:', len(bad)); assert not bad"

# 2. Rebuild apctt_submission/ and artifacts/apctt/argus_submission.zip and run official validators
python scripts/build_apctt_submission.py

# 3. Run official licence validator directly
python apctt-participant-kit-0.5.0-cpu/tools/check_licenses.py --bundle apctt_submission

# 4. Run official submission packer and archive checker directly
python apctt-participant-kit-0.5.0-cpu/tools/make_submission.py apctt_submission --output artifacts/apctt
python apctt-participant-kit-0.5.0-cpu/tools/make_submission.py --check artifacts/apctt/argus_submission.zip

# 5. Run full regression + APCTT test suite (91 tests)
python -m pytest tests/ -v
```

---

## 22. Final Git Branch, Commit Hashes, and Working-Tree Status

- **Corrective Branch**: `fix/apctt-final-submission-corrections` (branched directly from `origin/main` `10d1e81`).
- **Participant Kits Unmodified**: `git status apctt-participant-kit-0.5.0-cpu apctt-participant-kit-0.5.0-cuda` reports zero modified or untracked files.
- **Pre-existing `submission/` Directory Preserved**: `git diff origin/main -- submission/ scripts/package_submission.py` reports zero changes.
- **Working-Tree Status**: Clean (`nothing to commit, working tree clean`).



