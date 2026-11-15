# 03 — Architecture & APCTT Adapter Design

## 1. Layered System Architecture
ARGUS preserves its modular, domain-independent architecture while adding a first-class APCTT Stage 1 adapter layer:

1. **Core Assessment Layer (`packages/core/src/trl_core/`)**:
   Canonical TRL 1–9 definitions, evidence quality rubrics, contradiction detection, uncertainty quantification, and SHA-256 audit provenance.
2. **Document Intelligence Layer (`packages/document_processing/src/document_processing/`)**:
   Multi-backend page-faithful PDF extraction (`pypdf`, `pypdfium2`, `pdfplumber`) with 1-based page indexing, document isolation, and prompt-injection sanitization.
3. **Hybrid Retrieval Layer (`packages/retrieval/src/retrieval/`)**:
   Deterministic Okapi BM25 ($k_1 = 1.5, b = 0.75$) + morphological stem & phrase scoring over page-anchored candidate spans.
4. **APCTT Competition Adapter (`packages/competition_engine/src/competition_engine/apctt_adapter.py` & `my_submission/participant_module/`)**:
   - `infer_criterion_profile()`: Dynamic checklist profiler.
   - `extract_candidate_spans()`: Page-level sentence segmentation with verbatim substring extraction and bare-TRL-assertion filtering.
   - `analyze_span_modality()`: Distinguishes `COMPLETED`, `NEGATED`, `FAILED`, `PLANNED`, and `BACKGROUND` statements.
   - `determine_case_maturity_and_conflicts()`: Evaluates target scope (`component`, `subsystem`, `system`, `technology`), intended environment, multi-document chronology (`document_date`), and readiness ceiling.
   - `evaluate_criterion_for_case()`: Ranks top 3 distinct `(document_id, page)` references per criterion and determines `met`, `not met`, or `insufficient evidence`.
   - `verify_and_sanitize_result()`: Enforces all 20 official output validation rules (`E01`–`E20`) and verifies verbatim substring presence on each cited page before returning.

