# ARGUS — Official APCTT Stage 1 Assessment Module (`argus-trl-assessor`)

**Team**: `argus`  
**Package ID**: `argus-trl-assessor` (`1.0.0`)  
**Entrypoint**: `participant_module.adapter:AssessmentModule`  
**Base Environment**: `apctt-base-2026.1-py312`  
**License**: `MIT`

## Overview

ARGUS (Automated Readiness Grading & Uncertainty Synthesis) is a domain-independent, deterministic Technology Readiness Level (TRL 1–9) assessment engine. This package connects the official APCTT Stage 1 worker protocol (`apctt-worker-v2`) to the packaged Argus reasoning engine (`participant_module/argus_engine/`):

1. **Multi-Backend Verbatim PDF Page Extraction (`document_processing`)**: Extracts 1-indexed page text via `pypdf`, `pypdfium2`, or `pdfplumber` while preserving exact on-page character substrings for `supporting_span` verification.
2. **Untrusted Input Sanitization (`trl_core.sanitizer`)**: Strips zero-width/bidirectional Unicode overrides and filters prompt-injection or output-forcing payloads embedded inside PDFs.
3. **Linguistic Modality, Negation, Simulation & Temporal Analysis (`ml_inference`)**: Distinguishes completed empirical achievements from negated, failed, planned/future, hypothetical, and simulation-only claims, preventing bare `"TRL X"` assertions or keyword stuffing from inflating readiness levels.
4. **Dynamic Checklist Profiling & Hybrid BM25 Retrieval (`retrieval` + `competition_engine`)**: Dynamically profiles every criterion in `config["checklist"]` (supporting both `apctt-trl-v1` `APCTT-C01`..`APCTT-C12` and custom/modified checklists) and ranks distinct `(document_id, page)` passages.
5. **Contradiction Detection & Multi-Agent Referee Review (`trl_core` + `agent_orchestration`)**: Executes `StructuredClaimExtractor`, `EvidenceQualityAssessor`, `ContradictionDetector`, `CriteriaMapper`, `ReviewProtocol` (`OptimistReviewer`, `SkepticReviewer`, `RefereeAdjudicator`), and `UncertaintyModel`.
