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

## What is implemented

1. **Document ingestion** — extracts text and structural chunks from PDF, TXT, and Markdown files.
2. **Input sanitization** — removes selected hidden Unicode controls and detects common prompt-injection patterns.
3. **Evidence mining** — matches technical milestone phrases to candidate TRL levels and retains document/chunk offsets for traceability.
4. **Negation-aware matching** — filters milestone mentions when bounded nearby language explicitly denies that milestone.
5. **Deterministic adjudication** — evaluates extracted evidence against the structured TRL 1–9 criteria ladder.
6. **Prerequisite audit** — records lower-level criteria inferred from higher-level strong evidence as inferred, not as directly quoted evidence.
7. **API and research interface** — a FastAPI service exposes the assessment workflow and serves the Argus browser interface.
8. **Standalone submission CLI** — a local inference entry point intended for air-gapped competition execution.

## Architecture

~~~text
Argus
├── apps/
│   └── api/                 FastAPI routes, service layer, static browser UI
├── packages/
│   ├── core/                Domain models, TRL definitions, sanitization, adapters
│   ├── document_processing/ PDF/text extraction and chunking
│   ├── ml_inference/        Feature extraction and deterministic adjudication
│   ├── competition_engine/  Standalone inference runner
│   ├── agent_orchestration/ Package boundary reserved for future orchestration
│   └── retrieval/           Package boundary reserved for future retrieval
├── submission/              Isolated competition bundle
├── tests/                   Unit and API regression tests
└── scripts/                 Packaging and performance utilities
~~~

The current active assessment path is deterministic and local. Hybrid BM25/vector retrieval, a dedicated Next.js frontend, Supabase persistence, and autonomous multi-agent orchestration are **not represented as implemented capabilities** in this release.

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
