# Argus

### Evidence-Grounded Technology Readiness Assessment & Debate Intelligence

**Competition:** Techfest 2026–27 · 2nd APCTT Hackathon 2026  
**License:** Apache License 2.0  
**Submission mode:** Local, deterministic, air-gapped inference

Argus analyzes technical documents and produces an auditable Technology Readiness Level (TRL 1–9) assessment. It combines document extraction, prompt-injection-aware sanitization, milestone evidence mining, a deterministic criteria-based adjudicator, and a structured adversarial review transcript.

The review experience uses three explicit perspectives:

- **Optimist:** surfaces the strongest maturity evidence found in the document.
- **Skeptic:** challenges unsupported or incomplete milestone claims.
- **Referee:** presents the final criteria-based determination and advancement gaps.

These perspectives are currently generated through deterministic application logic and templates. They are **not independent autonomous LLM agents**. Argus does not make external model/API calls in its competition inference path.

---

## What is implemented in Stage 2

1. **Structured Technical Claim Extraction** — extracts quantitative measurements, units, engineering tolerances ($\pm$), validation environments, and candidate TRL levels beyond keyword matching.
2. **Modality & Temporal Classification** — grammatically separates completed milestones from unperformed, negated, planned, hypothetical, and purely simulated achievements.
3. **Contradiction Detection** — flags document tensions between abstract claims and limitation disclosures, preserving both sides for adjudication.
4. **Granular Source Provenance & Inspection** — preserves verbatim text excerpts, page numbers, section headers, and exact character offsets with interactive inspection drawers.
5. **Canonical Criteria Mapping** — maps evidence directly against official NASA/DoD/ISO TRL 1–9 criteria checklists with explicit status categorization (`DIRECTLY_SATISFIED`, `PARTIALLY_SUPPORTED`, `SATISFIED_INFERRED`, `CONTRADICTORY`, `MISSING`).
6. **Formal Adversarial Review Protocol** — deterministic multi-perspective argumentation:
   - **Optimist:** constructs strongest defensible maturity evidence with citations.
   - **Skeptic:** challenges unsupported milestones, missing prerequisites, and contradictions.
   - **Referee:** adjudicates final TRL and produces an auditable adjudication ledger.
7. **Advancement Gap Analysis** — provides concrete, actionable engineering recommendations and required testing environments for progressing to TRL N+1.
8. **Decoupled Uncertainty Profiling** — independently computes extraction confidence, criteria coverage, conflict penalties, and composite certainty with epistemic calibration disclosures.
9. **Cryptographic Audit Trail** — hashes every state transition into an immutable SHA-256 reproducibility hash ensuring 100% deterministic reproducibility.
10. **Research Workspace & Report Exporter** — high-density web UI with interactive evidence drawers and one-click Markdown technical report export (`/api/sample-assess/{sample_id}/report`).
11. **Adversarial & Scientific Validation Suite** — 12-case adversarial evaluation corpus, scientific metric calculators (QWK, MAE, Exact & Adjacent Acc, ECE, Brier Score), and reproducible ablation tooling.
12. **100% Air-Gapped Standalone Inference** — runs completely offline with zero network connectivity or external LLM dependencies.

## Architecture

~~~text
Argus
├── apps/
│   └── api/                 FastAPI routes, service layer, static research dashboard
├── packages/
│   ├── core/                Domain models, TRL definitions, criteria mapper, ledger, audit, uncertainty, gaps, sanitizer
│   ├── document_processing/ PDF/text extraction and chunking
│   ├── ml_inference/        Structured claim extraction, modality analyzer, feature mining, ordinal classifier
│   ├── agent_orchestration/ Deterministic review protocol (Optimist, Skeptic, Referee)
│   ├── competition_engine/  Standalone inference runner
│   └── retrieval/           Modular retrieval package boundary
├── submission/              Isolated, air-gapped competition bundle
├── tests/                   Unit, adversarial, API, and regression test suite (69 tests)
├── docs/                    Methodology, architecture, evaluation guide, scenarios, and verification report
└── scripts/                 Ablation studies, calibration analysis, packaging utilities
~~~

The active assessment path is 100% deterministic, local, and air-gapped. The multi-perspective review transcript is deterministic rule-based synthesis, explicitly designed to eliminate LLM hallucinations, token costs, and non-reproducible variance.

---

## Requirements

- Python 3.10 or newer
- pip
- A supported local environment for the optional LightGBM dependency

## Installation

From the repository root:

~~~bash
python -m venv .venv
~~~

Activate the environment, then install the API, inference, and development dependencies:

~~~powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
python -m pip install -e ".[api,ml,dev]"
~~~

~~~bash
# macOS / Linux
source .venv/bin/activate
python -m pip install -e ".[api,ml,dev]"
~~~

## Run the web application

From the repository root:

~~~bash
uvicorn api.main:app --app-dir apps/api/src --host 127.0.0.1 --port 8000
~~~

Open http://127.0.0.1:8000.

Useful endpoints:

| Endpoint | Purpose |
| --- | --- |
| GET /api/health | Service health and active layer inventory |
| GET /api/trl-ladder | Structured TRL 1–9 definitions |
| GET /api/sample-documents | Preloaded demonstration documents |
| POST /api/sample-assess/{sample_id} | Assess a preloaded sample |
| POST /api/assess-text | Assess pasted technical text |
| POST /api/assess | Assess an uploaded PDF, TXT, or MD file |

## Run the standalone CLI

The competition path is designed to operate locally without hosted LLMs or external inference APIs.

~~~bash
python run_inference.py --input path/to/document.txt
python run_inference.py --input path/to/document.pdf --output assessment.json
python run_inference.py --input path/to/document.txt --strict-security
~~~

Exit codes:

- 0 — successful assessment.
- 1 — invalid input, unreadable/empty document, or strict-security rejection.
- 2 — command-line argument error.

For the isolated competition bundle, follow submission/README.md and use only files contained in submission/.

## Tests and quality checks

~~~bash
python -m pytest
~~~

Optional local checks, when installed:

~~~bash
ruff check .
python -m pytest --cov
~~~

Do not report a benchmark, test count, or accuracy score unless it has been reproduced against the current commit and its environment.

## Important evaluation limitations

- Milestone matching is heuristic. Negation handling is bounded and rule-based; it is not full natural-language understanding.
- Pattern matches are candidate evidence, not a substitute for expert review of source context.
- Official predictive metrics require a legitimate labelled evaluation dataset. No accuracy, QWK, or MAE claims are made without that dataset.
- The role-based review transcript is deterministic synthesis, not proof of three separately running AI agents.
- The standalone submission bundle must be regenerated and independently verified whenever source inference code changes.

## Project identity

**Argus** is the project name across the repository, browser experience, API, command-line tooling, and submission documentation.

## License

Apache License 2.0. See the LICENSE file when present in the repository.
