# Pre-Submission Checklist: Stage 1 Candidate

**Competition:** Techfest 2026–27 | 2nd APCTT Hackathon 2026  
**Target Milestone:** Attempt 1 Diagnostic Candidate (Target: 12 Nov 2026)  
**Final Freeze Deadline:** 15 Nov 2026, 23:59 IST  
**Package Path:** `submission/`

---

## 1. Compliance & Disqualification Triggers

- [x] **Zero Private / Undisclosed API Keys:** Verified. The inference pipeline contains no API keys and makes no external network calls (complies with Rule 6: *"Use of undisclosed private API keys, hardcoded output schemas, or plagiarism will result in immediate disqualification"*).
- [x] **Zero Unauthorized External Tools:** Verified. Runs 100% locally on CPU without hosted endpoints or cloud model inference (complies with Rule 7: *"The use of unauthorized external AI tools during live rounds is strictly prohibited"*).
- [x] **Apache 2.0 License Compliance:** Verified. Every library in `submission/requirements.txt` is licensed under permissive Apache-2.0, MIT, or BSD-3. Strongly copyleft libraries (such as AGPL PyMuPDF) have been completely excluded and replaced with `pypdfium2` and `pdfminer.six`.
- [x] **Originality & Code Freeze:** Submissions are original work developed for the APCTT challenge. Ready to be frozen for Stage 1.

---

## 2. Technical Performance & Resource Limits

- [x] **Execution Speed:** Benchmarked locally at **8.36 ms** average per document on standard commodity CPU. Well within any execution speed limits.
- [x] **Memory Footprint:** Peak memory consumption is **~20 KB** above baseline Python process, well below any memory ceiling (< 16 GB).
- [x] **Supported Input Formats:** Seamlessly ingests both PDF files (via `pypdfium2`) and raw text/markdown documents (`.txt`, `.md`).
- [x] **Prompt Injection Defense:** Untrusted document payloads are neutralized: dangerous hidden zero-width unicode characters are stripped, and role-override payloads are flagged.

---

## 3. Schema & Adapter Decoupling

- [x] **Decoupled Output Schema:** Core pipeline emits canonical `FinalAssessment` objects. The output serialization is handled exclusively by `BaseOutputAdapter` / `InternalOutputAdapter`. If the competition organizers supply a distinct JSON or CSV schema, only the adapter format mapping requires an update.
- [x] **Graceful Failure Handling:** CLI returns clear exit codes (`0` for success, `1` for invalid input or security failure, `2` for syntax error) and writes structured errors to stderr rather than unhandled Python tracebacks.

---

## 4. Local Validation Metrics (Document-Level Split)

Evaluated across $n = 9$ approved NASA/DoD/ESA benchmark cases with certified TRL ground truth:
- **Evaluation Strategy:** Document-Level 3-Fold Cross-Validation (zero document leakage).
- **Quadratic Weighted Kappa (QWK):** **0.2930**
- **Mean Absolute Error (MAE):** **2.1111**
- **Exact Accuracy:** **44.4%**
- **Macro Precision:** **35.6%**
- **Statistical Note:** Sample size ($n = 9$) is small; per evaluation rigor rules, results are reported with exact sample size and marked as baseline benchmark indicators.

---

## 5. Submission Package Contents (`submission/`)

1. `submission/run_inference.py`: Standalone CLI executable.
2. `submission/packages/`:
   - `core/`: Canonical domain models, TRL definitions, and adapters.
   - `document_processing/`: `pypdfium2` PDF and text extractor.
   - `ml_inference/`: Feature extraction, keyword mining, and LightGBM ordinal adjudication.
   - `competition_engine/`: Standalone pipeline execution engine.
3. `submission/requirements.txt`: Minimal pinned dependencies (`lightgbm`, `pypdfium2`, `pdfminer.six`, `pdfplumber`, `pydantic`, `scikit-learn`, `numpy`, `rank-bm25`).
4. `submission/README.md`: Judge/organizer execution guide.

---

## 6. Submission Strategy (3 Attempts)

| Attempt | Date | Objective | Feedback Utilized |
|---|---|---|---|
| **Attempt 1** | **12 Nov 2026** | **Diagnostic Submission:** Submit standalone runnable package to test organizer automated test harness, execution speed, and dependency check pass/fail. | Receive operational execution status and benchmark score diagnostics. |
| **Attempt 2** | **13–14 Nov 2026** | **Refinement Submission:** Adjust thresholds, calibration, or schema adapters based on Attempt 1 diagnostics. | Verify improved benchmark score. |
| **Attempt 3** | **15 Nov 2026 (before 23:59 IST)** | **Final Code Freeze:** Final immutable submission for official Stage 1 ranking and code freeze. | Official competition ranking. |

