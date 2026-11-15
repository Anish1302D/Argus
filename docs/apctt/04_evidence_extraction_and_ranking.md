# 04 — Evidence Extraction, Modality & Criterion-Aware Ranking

## 1. Page-Faithful Multi-PDF Extraction
- Each document in `case["documents"]` is read from `doc["path"]` with strict verification of `doc["page_count"]`.
- Every extracted page retains `(document_id, page, document_date, title)` where `page` is 1-based (`1 <= page <= page_count`).
- `pypdf` is used as the primary page text extractor (matching the APCTT base environment reference reader), with automatic fallback to `pypdfium2` and `pdfplumber`.

## 2. Verbatim `supporting_span` Extraction & Anti-Fabrication Guarantee
- Every candidate span is extracted as a contiguous single-line substring directly from `page.text` (`supporting_span in page.text` is literally `True`).
- Spans that merely state a bare TRL number (e.g., `"The system is at TRL 6"`, which scores `0` under Part C of `MODULE_GUIDE.md`) are automatically filtered out by `is_bare_trl_assertion()`.
- Dotted table-of-contents lines are filtered out so citations point to substantive technical body pages.

## 3. Modality & Negation Intelligence
Each candidate sentence is analyzed by `analyze_span_modality()`:
- **Negated (`NEGATED`):** Matches pre-posed and post-posed negation patterns (`"was not tested"`, `"has not yet undergone"`, `"no hardware prototype has been constructed"`, `"measured results and acceptance criteria are not supplied"`).
- **Failed (`FAILED`):** Matches test failure or retraction markers (`"failed to meet"`, `"qualification failed"`, `"retracted"`).
- **Planned / Hypothetical (`PLANNED`):** Matches future/conditional work (`"will be tested in Phase 2"`, `"planned for future work"`, `"could potentially"`).
- **Completed (`COMPLETED`):** Matches empirical action verbs (`"tested"`, `"calibrated"`, `"validated"`, `"demonstrated"`, `"measured"`, `"implemented"`, `"coupled"`).

## 4. Top-3 Distinct `(document_id, page)` Ranking
Under Part B of `MODULE_GUIDE.md` (40% of score), only the first 3 distinct `(document_id, page)` items per `"met"` criterion are evaluated against gold pages. `rank_spans_for_criterion()` deduplicates by `(document_id, page)` and returns at most 3 distinct page references ordered by descending hybrid BM25 + criterion-profile + target-alignment score.

