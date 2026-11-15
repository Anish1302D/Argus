# ARGUS

### Evidence-Grounded Technology Readiness Assessment & Adversarial Debate Intelligence

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://python.org)
[![Build Status](https://img.shields.io/badge/Tests-69%2F69%20Passing%20(100%25)-success.svg)]()
[![Air-Gap Certified](https://img.shields.io/badge/Air--Gap-100%25%20Offline%20Verified-blueviolet.svg)]()
[![Determinism](https://img.shields.io/badge/Reproducibility-100%25%20Bitwise%20SHA--256-orange.svg)]()

**Competition:** Techfest 2026–27 · 2nd APCTT Hackathon 2026  
**Canonical Repository:** [ishaj306/trl-debate-engine](https://github.com/ishaj306/trl-debate-engine) · Fork: [Anish1302D/Argus](https://github.com/Anish1302D/Argus)  
**Deployment Mode:** Local, Deterministic, 100% Air-Gapped Inference  

---

## Table of Contents
- [About ARGUS](#about-argus)
  - [Overview & Mission](#overview--mission)
  - [The Problem: Why Existing Approaches Fail](#the-problem-why-existing-approaches-fail)
  - [The ARGUS Solution](#the-argus-solution)
- [Key Capabilities & Innovations](#key-capabilities--innovations)
- [Canonical TRL 1–9 Framework](#canonical-trl-19-framework-operationalization)
- [System Architecture](#system-architecture)
- [Quickstart & Installation](#quickstart--installation)
- [Running the Web Application](#running-the-web-application)
- [Releases & Versioning](#releases--versioning)
- [Packages & Modular Architecture](#packages--modular-architecture)
- [Running the Standalone Air-Gapped CLI](#running-the-standalone-air-gapped-cli)
- [Scientific Evaluation & Benchmark Results](#scientific-evaluation--benchmark-results)
- [Methodological Integrity & Epistemic Disclosures](#methodological-integrity--epistemic-disclosures)
- [License](#license)

---

## About ARGUS

### Overview & Mission
**ARGUS** (Automated Readiness Grading & Uncertainty Synthesis) is an enterprise-grade scientific intelligence engine designed to autonomously, objectively, and rigorously evaluate the **Technology Readiness Level (TRL 1–9)** of complex aerospace, defense, energy, biotechnology, and deep-tech documentation.

In competitive government grants, defense procurement, dual-use technology diligence, and academic commercialization, accurately assessing how close a breakthrough technology is to real-world deployment is critical. However, conventional manual reviews are slow, prone to human cognitive bias, and struggle to cross-examine hundreds of pages of engineering disclosures.

### The Problem: Why Existing Approaches Fail
Existing automated assessment attempts fail because of two fundamental flaws:
1. **Keyword Overconfidence & Naive Pattern Matching:** Superficial keyword scrapers equate aspirational marketing prose or introductory literature reviews (e.g., *"this propulsion concept will enable orbital flight"*) with verified physical heritage, grossly overestimating maturity.
2. **Generative Hallucination & Epistemic Opacity:** Black-box Large Language Models (LLMs) hallucinate non-existent test results, fluctuate across runs, introduce severe non-deterministic variance, cannot trace claims to verifiable character offsets, and violate strict air-gapped security mandates required by defense and aerospace benchmarks.

### The ARGUS Solution
ARGUS 2.0.0 completely eliminates these vulnerabilities by replacing black-box guesswork with a **14-stage modular Evidence Intelligence Pipeline**:
- **Grammatical Modality & Temporal Decomposition:** Distinguishes completed physical tests from unperformed, negated, planned, hypothetical, and purely simulated milestones.
- **Granular Source Traceability:** Preserves exact document character slices, page numbers, and section headers with interactive visual inspection drawers.
- **Explainable Adversarial Adjudication:** Simulates a formal scientific review panel comprising **The Optimist** (evidence maximization with citations), **The Skeptic** (prerequisite enforcement and contradiction challenges), and **The Referee** (official rule-based adjudication ledger).
- **Decoupled Epistemic Uncertainty:** Separates linguistic extraction confidence from canonical criteria checklist coverage and document conflict penalties.
- **Actionable Advancement Gap Roadmaps:** Outlines the exact physical testing facilities, environmental parameters, and criteria required to graduate to TRL $N+1$.
- **100% Air-Gapped & Deterministic:** Operates fully offline without external APIs or downloaded model weights, producing identical, cryptographically sealed SHA-256 reproducibility hashes on every run.

---

## Key Capabilities & Innovations

```
[1. Input Sanitization] ───> [2. Structural Chunking] ───> [3. Claim Extraction]
                                                                     │
[6. Contradiction Detection] <── [5. Quality Scoring] <─── [4. Modality Analysis]
         │
         ▼
[7. Candidate TRL Gate] ───> [8. Criteria Mapping] ───> [9. Adversarial Review]
                                                                     │
[12. Uncertainty Profile] <── [11. Gap Analysis] <────── [10. Referee Adjudication]
         │
         ▼
[13. Relational Ledger] ───> [14. Audit Trail & SHA-256 Hash] ───> Final Assessment
```

| Innovation | Implementation | Scientific Value |
|---|---|---|
| **Structured Claim Extraction** | `StructuredClaimExtractor` | Extracts quantitative measurements with units, numerical tolerances ($\pm$), and validation environments. |
| **Modality & Negation Analysis** | `ModalityAnalyzer` | Grammatically isolates local negation scopes, distinguishing *"flight tests were completed"* from *"no flight tests were completed"*. |
| **Contradiction Detection** | `ContradictionDetector` | Identifies internal document tensions where marketing abstracts claim high TRLs but limitation sections disclose that only simulations or lab tests were executed. |
| **Granular Source Provenance** | `ProvenanceEngine` & `EvidenceLedger` | Preserves character offsets (`char_offset_start`, `char_offset_end`), page numbers, and verbatim quotes with bi-directional navigation. |
| **Adversarial Adjudication Protocol** | `ReviewProtocol` (Optimist, Skeptic, Referee) | Methodically subjects technical claims to adversarial peer review, challenging missing prerequisites and unverified hardware claims. |
| **Advancement Gap Analysis** | `AdvancementGapAnalyzer` | Formulates concrete engineering roadmaps and required test environments for progression to the next readiness level. |
| **Multi-Dimensional Uncertainty** | `UncertaintyModel` | Computes composite certainty ($C$) by decoupling extraction quality, criteria coverage, and conflict penalties. |
| **Immutable Cryptographic Audit** | `AuditTrailBuilder` | Computes a SHA-256 reproducibility hash over all evaluation stages and state transitions. |
| **Air-Gapped Standalone Inference** | `competition_engine` & `submission/` | Completely self-contained CLI and API running locally with zero internet access or GPU requirement. |
| **Prompt Injection Defenses** | `Sanitizer` | Sanitizes malicious prompt injections, role-play hijacks, and invisible Unicode zero-width evasion controls. |

---

## Canonical TRL 1–9 Framework Operationalization

ARGUS strictly aligns with NASA, U.S. Department of Defense (DoD), and ISO 16290 technical standards:

| Level | Official Title | Verification Environment | Core Milestone Criteria |
|:---:|---|---|---|
| **TRL 1** | Basic principles observed and reported | Mathematical / Theoretical | Scientific observations, peer-reviewed literature, theoretical formulations. |
| **TRL 2** | Technology concept and/or application formulated | Analytical Formulation | Practical applications identified, conceptual designs, analytical models. |
| **TRL 3** | Analytical and experimental critical function / characteristic proof-of-concept | Laboratory (Components) | Active R&D, bench-scale experiments, physical parameters measured. |
| **TRL 4** | Component and/or breadboard validation in laboratory environment | Controlled Laboratory | Low-fidelity system breadboard integrated and tested in laboratory. |
| **TRL 5** | Component and/or breadboard validation in relevant environment | Relevant Test Chamber | Fidelity increases significantly; tested in simulated operational environment (thermal vacuum, arc-jet). |
| **TRL 6** | System/subsystem model or prototype demonstration in a relevant environment | High-Fidelity Relevant | Representative engineering prototype tested in relevant field environment. |
| **TRL 7** | System prototype demonstration in an operational environment | Operational Environment | Actual system prototype demonstrated in operational vehicle or aircraft. |
| **TRL 8** | Actual system completed and qualified through test and demonstration | Developmental Flight / Field | Final developmental hardware completed, factory/site qualification tests passed. |
| **TRL 9** | Actual system proven through successful mission operations | Operational Spaceflight / Mission | Proven through repeated, documented successful operational missions. |

---

## System Architecture

```text
Argus
├── apps/
│   └── api/                        FastAPI gateway, service layer, and static research dashboard
│       └── static/
│           ├── index.html          High-density research workspace & provenance viewer
│           └── ...
├── packages/
│   ├── core/                       Domain models, TRL definitions, criteria mapper, ledger, audit, uncertainty, gaps, sanitizer
│   │   └── src/trl_core/
│   │       ├── models.py           Pydantic v2 domain models
│   │       ├── criteria_mapper.py  Checklist criteria mapping engine
│   │       ├── ledger.py           Relational Evidence Ledger & query helpers
│   │       ├── contradiction.py    Document tension & contradiction detector
│   │       ├── uncertainty.py      Decoupled epistemic uncertainty model
│   │       ├── gap_analysis.py     TRL N+1 advancement gap analyzer
│   │       ├── audit.py            Cryptographic audit trail & SHA-256 builder
│   │       └── sanitizer.py        Prompt injection & Unicode sanitizer
│   ├── document_processing/        PDF/TXT document extraction and structural chunking
│   ├── ml_inference/               Claim extraction, modality analysis, feature mining, ordinal classifier
│   │   └── src/ml_inference/
│   │       ├── claim_extractor.py  Structured measurement & milestone extractor
│   │       ├── modality.py         Linguistic modality & temporal analyzer
│   │       ├── features.py         Milestone regex automata & feature vectors
│   │       └── classifier.py       14-stage modular ordinal classifier
│   ├── agent_orchestration/        Deterministic adversarial review protocol
│   │   └── src/agent_orchestration/
│   │       ├── optimist.py         Evidence-grounded Optimist review agent
│   │       ├── skeptic.py          Challenge-driven Skeptic review agent
│   │       ├── referee.py          Referee adjudicator & implied prerequisite auditor
│   │       └── protocol.py         Turn-based review protocol orchestrator
│   ├── competition_engine/         Standalone air-gapped inference entry points
│   └── retrieval/                  Modular retrieval boundary
├── submission/                     Autonomous, isolated competition bundle (run_inference.py)
├── tests/                          Comprehensive unit, adversarial, API, and UI regression test suite (69 tests)
│   ├── data/adversarial_corpus/    12 distinct adversarial and edge-case test documents
│   ├── test_milestone_1_...        Evidence intelligence engine tests
│   ├── test_milestone_2_...        Evidence traceability tests
│   ├── test_milestone_3_...        Adversarial adjudication tests
│   ├── test_milestone_4_...        Scientific validation & corpus tests
│   └── test_milestone_5_...        Research workspace UI contract tests
├── docs/                           Comprehensive engineering specifications & reports
│   ├── methodology_specification.md Full 14-stage pipeline & mathematical formulations
│   ├── architecture_and_data_models.md System block diagrams & Pydantic schemas
│   ├── evaluation_guide.md         Reproducible commands, ablation studies & calibration
│   ├── demonstration_scenarios.md  5 end-to-end case studies (TRL 1 to TRL 9)
│   └── stage_2_release_verification_report.md Official audit & release sign-off
└── scripts/                        Ablation study, calibration analysis, packaging scripts
```

---

## Quickstart & Installation

### Requirements
- **Python:** Version 3.10 or newer (tested on Python 3.10, 3.11, 3.12, and 3.14)
- **Environment:** Compatible with Windows, Linux, and macOS
- **Network Requirement:** $0 \text{ bytes}$ external network I/O during runtime inference

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ishaj306/trl-debate-engine.git
   cd trl-debate-engine
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   ```
   - On Windows (PowerShell):
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   - On Linux / macOS:
     ```bash
     source .venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   python -m pip install -e ".[api,ml,dev]"
   ```

---

## Running the Web Application

Launch the local FastAPI gateway and interactive research workspace:

```bash
uvicorn api.main:app --app-dir apps/api/src --host 127.0.0.1 --port 8000
```

Open your browser to: **`http://127.0.0.1:8000`**

### REST API Endpoints

| Method | Endpoint | Description |
|:---:|---|---|
| `GET` | `/api/health` | Service health status and active component inventory |
| `GET` | `/api/trl-ladder` | Structured TRL 1–9 definitions and checklist criteria |
| `GET` | `/api/sample-documents` | Preloaded diverse demonstration document catalog |
| `POST` | `/api/sample-assess/{id}` | Run full 14-stage assessment on a sample scenario |
| `GET` | `/api/sample-assess/{id}/report` | Retrieve publication-ready exportable Markdown report |
| `POST` | `/api/assess-text` | Assess raw pasted technical text directly |
| `POST` | `/api/assess` | Ingest and evaluate an uploaded file (`.pdf`, `.txt`, `.md`) |

---

## Releases & Versioning

Official production and competition releases are cryptographically tagged and distributed via GitHub Releases:

- **Latest Release:** [v2.0.0-argus](https://github.com/Anish1302D/Argus/releases/tag/v2.0.0-argus)
- **Tag:** `v2.0.0-argus` | **Commit:** `main` (Verified)
- **Release Highlights:** Complete 14-stage assessment pipeline, adversarial multi-agent adjudication (Optimist, Skeptic, Referee), granular source provenance, advancement gap analysis, and 100% air-gapped deterministic reproducibility.
- **Standalone Submission Bundle:** Download the pre-packaged, offline-ready artifact [`argus-v2.0.0-submission.zip`](https://github.com/Anish1302D/Argus/releases/download/v2.0.0-argus/argus-v2.0.0-submission.zip) containing all required models, heuristics, and the standalone `run_inference.py` runner.

### Versioning Policy
ARGUS follows [Semantic Versioning 2.0.0](https://semver.org/):
- `MAJOR` (v2.x.x): Methodological paradigm upgrades, criteria ladder modifications, or breaking domain model alterations.
- `MINOR` (vx.1.x): New feature extraction heuristics, additional validation environments, UI enhancements, or diagnostic tooling.
- `PATCH` (vx.x.1): Pattern refinements, regex optimizations, security sanitizer patches, and non-breaking bug fixes.

---

## Packages & Modular Architecture

ARGUS is architected as an interconnected monorepo of five decoupled, strictly-typed Python packages:

| Package | Directory | Distribution Target | Key Responsibilities |
|---|---|---|---|
| **`trl-core`** | [`packages/core`](packages/core) | Core Domain Engine | Pydantic v2 data models (`TechnicalClaim`, `CriteriaMapping`, `UncertaintyProfile`, `AuditTrail`), canonical TRL 1–9 criteria definitions, criteria mapper, relational evidence ledger, advancement gap analyzer, input sanitizer. |
| **`ml-inference`** | [`packages/ml_inference`](packages/ml_inference) | Intelligence & Features | Quantitative measurement extraction, linguistic modality and temporal parsing, milestone feature extraction, 14-stage ordinal classifier. |
| **`agent-orchestration`** | [`packages/agent_orchestration`](packages/agent_orchestration) | Adversarial Review | Turn-based review protocol orchestrator, evidence-grounded Optimist reviewer, challenge-driven Skeptic scrutinizer, Referee adjudicator. |
| **`document-processing`**| [`packages/document_processing`](packages/document_processing) | Ingestion & Slicing | PDF and raw text extraction, structural context chunking, verbatim character offset preservation. |
| **`competition-engine`** | [`packages/competition_engine`](packages/competition_engine) | Air-Gapped Deployment | Isolated competition execution runtime, CLI adapters, and air-gapped verification harness. |

### Installing Individual Packages in Development
Each package can be imported independently or installed in editable mode:
```bash
python -m pip install -e packages/core
python -m pip install -e packages/ml_inference
python -m pip install -e packages/agent_orchestration
python -m pip install -e packages/document_processing
```

---

## Running the Standalone Air-Gapped CLI

The standalone competition inference path runs completely offline without network sockets or hosted LLM dependencies.

```bash
# Evaluate an arbitrary technical document
python submission/run_inference.py -i tests/data/adversarial_corpus/01_multiple_negations.txt

# Specify custom output path
python submission/run_inference.py -i document.pdf -o outputs/assessment.json

# Enable strict prompt-injection defense mode
python submission/run_inference.py -i document.txt --strict-security
```

**CLI Return Codes:**
- `0`: Successful evaluation.
- `1`: Invalid input, empty document, or strict-security injection rejection.
- `2`: Command-line argument syntax error.

---

## Scientific Evaluation & Benchmark Results

### Complete Test Suite (83/83 Passing)
```bash
python -m pytest -v
```
All 83 unit, regression, security, adversarial, API, and APCTT Stage 1 contract tests (`tests/test_apctt_adapter.py`, Scenarios A–X) pass with 100% reliability in ~7 seconds.

### Official APCTT Participant Kit (`v0.5.0`) Integration & Submission Bundle
ARGUS implements the exact official Stage 1 competition contract (`participant_module.adapter:AssessmentModule`, worker protocol `apctt-worker-v2`, base environment `apctt-base-9e7fe1324bb6`):

- **Submission Bundle Source:** [`my_submission/`](my_submission/)
- **Packaged Submission Archive:** `argus_submission.zip` (`VALID` via `tools/make_submission.py --check`)
- **License Audit:** `3 allowed, 0 review, 0 denied` via `tools/check_licenses.py --bundle my_submission --web apps/api`
- **Public Smoke Cases (`apctt_runtime/worker.py`):**
  - `DEMO-001`: `abstained` (`insufficient evidence`, `APCTT-C04` met, `0` contract issues, `28.4 ms`)
  - `USGS-SDG-012`: `completed` (`predicted_trl = 4`, 7/12 criteria met, `0` contract issues, `1,022 ms`)
  - `USGS-SDG-040`: `completed` (`predicted_trl = 7`, 10/12 criteria met, `0` contract issues, `888 ms`)
  - `USGS-SDG-061`: `completed` (`predicted_trl = 6`, 9/12 criteria met, `0` contract issues, `2,410 ms`)
- **APCTT Engineering Documentation:** [`docs/apctt/01_official_kit_audit.md`](docs/apctt/01_official_kit_audit.md) through [`docs/apctt/10_final_submission_guide.md`](docs/apctt/10_final_submission_guide.md)

### Ablation Study Benchmark (`scripts/run_ablation_study.py`)
Evaluated across the 12-document adversarial test corpus:

| Configuration | Exact Accuracy | Adjacent Acc ($\pm 1$) | Mean Absolute Error (MAE) | Quadratic Weighted Kappa (QWK) |
|---|:---:|:---:|:---:|:---:|
| **ARGUS Full Pipeline (Stage 2)** | **75.0%** | **91.7%** | **0.583** | **0.865** |
| Without Negation Analysis | 50.0% | 66.7% | 1.417 | 0.582 |
| Without Contradiction Detection | 66.7% | 83.3% | 0.833 | 0.749 |
| Without Multi-Agent Debate | 58.3% | 75.0% | 1.167 | 0.641 |
| Naive Keyword-Only Baseline | 33.3% | 50.0% | 2.250 | 0.312 |

### Epistemic Uncertainty & Calibration (`scripts/analyze_calibration.py`)
- **Expected Calibration Error (ECE):** **0.185** (demonstrates conservative, non-overconfident epistemic calibration)
- **Brier Reliability Score:** **0.142**
- **Average Prediction Certainty:** **68.8%** (appropriately bounded; reserves $>90\%$ certainty exclusively for multi-measurement empirical test reports)

---

## Methodological Integrity & Epistemic Disclosures

In adherence to strict scientific evaluation guidelines:
1. **Deterministic Multi-Agent Synthesis:** The Optimist, Skeptic, and Referee debate is generated via deterministic rule-based state synthesis rather than autonomous non-deterministic LLM agents. This guarantees 100% bitwise reproducibility and prevents hallucinations under air-gapped competition constraints.
2. **Epistemic Calibration Status:** Certainty percentages are bounded composite heuristics combining extraction specificity, checklist coverage, and conflict penalties, explicitly disclosed as `UNCALIBRATED_HEURISTIC_BOUNDED`.
3. **No Hidden Training Overfitting:** Evaluation metrics are computed strictly against the local adversarial corpus without fitting on hidden competition labels.

---

## License

This project is licensed under the **MIT License** (in compliance with APCTT Decision D72). See the [LICENSE](LICENSE) file for complete details.

---
*ARGUS — Engineered for the 2nd APCTT Hackathon 2026 / Techfest 2026–27.*
