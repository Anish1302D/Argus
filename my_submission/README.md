# ARGUS — APCTT Stage 1 Submission Bundle

**Team:** `argus`  
**Package ID:** `argus-trl-engine` (`v1.0.0`)  
**Base Environment:** `apctt-base-9e7fe1324bb6`  
**Entrypoint:** `participant_module.adapter:AssessmentModule`  
**License:** MIT (`participant_module/LICENSE`)  
**Compute Profile:** CPU (`compute.device = "cpu"`)  

---

## Architecture Overview

ARGUS is a domain-independent, evidence-grounded Technology Readiness Assessment engine:

1. **Page-Faithful Multi-PDF Extraction (`participant_module/pdf_extractor.py`)**:
   Extracts 1-based page text across single or multi-document cases using `pypdf`, `pypdfium2`, and `pdfplumber` from the common base environment while enforcing document/page provenance and verifying `page_count`.
2. **Dynamic Checklist Profiler (`participant_module/apctt_engine.py`)**:
   Reads `config["checklist"]["criteria"]` dynamically in `load(config, asset_root)`. Never hardcodes criterion IDs; infers TRL milestone levels (1–9), cross-cutting evidence quality criteria (quantified results vs requirements, test environment & article definition, assessment target match), and custom checklist criteria directly from their descriptions.
3. **Hybrid Okapi BM25 + Lexical-Semantic Retrieval (`participant_module/retrieval_engine.py`)**:
   Indexes candidate spans per case and scores them against each criterion profile, `assessment_target`, `intended_application`, and `intended_environment`.
4. **Modality, Negation & Contradiction Analysis (`participant_module/apctt_engine.py`)**:
   Distinguishes completed empirical work from negated, unperformed, failed, or planned/future work, resolves multi-document chronology (`document_date`), and filters out bare TRL number assertions.
5. **Calibrated TRL Adjudication & Contract Self-Verification**:
   Returns `"completed"` (with integer `predicted_trl` 1–9, `uncertainty` interval, `confidence`, `trl_rationale`, and `criterion_rationale`), `"abstained"` (with exact allowed `abstention_reason`), or `"failed"` (with controlled `error_code` and all optional fields omitted), ensuring every `"met"` criterion cites up to 3 distinct `(document_id, page)` references with verified verbatim `supporting_span`.

