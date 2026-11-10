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

## 2. Technical Performance & Resource Limits (Empirically Measured)

Measured across realistic 30–100+ page technical PDFs (arXiv public technical papers, 361 total pages):

- [x] **Execution Speed:** Average end-to-end latency of **2.77 s** per document (**38.42 ms** per page) on standard commodity CPU.
  - 47-page paper (`mllm_survey.pdf`): 2.28 s
  - 68-page paper (`instruct_gpt_paper.pdf`): 1.78 s
  - 75-page paper (`gpt3_paper.pdf`): 1.89 s
  - 144-page paper (`llm_survey_zhao.pdf`): 6.92 s
- [x] **Memory Footprint (Peak Process RSS):**
  - Baseline Python Process: **18.82 MB**
  - Post-Import & Model/Package Load: **146.82 MB**
  - Overall Peak Process RSS during extraction & inference: **179.35 MB** (well within standard 2 GB–16 GB competition execution limits).
- [x] **Supported Input Formats:** Seamlessly ingests both PDF files (via `pypdfium2`) and raw text/markdown documents (`.txt`, `.md`).
- [x] **Prompt Injection Defense:** Untrusted document payloads are neutralized: dangerous hidden zero-width unicode characters are stripped, and role-override payloads are flagged.

---

## 3. Schema & Adapter Decoupling

- [x] **Decoupled Output Schema:** Core pipeline emits canonical `FinalAssessment` objects. The output serialization is handled exclusively by `BaseOutputAdapter` / `InternalOutputAdapter`. If the competition organizers supply a distinct JSON or CSV schema, only the adapter format mapping requires an update.
- [x] **Graceful Failure Handling:** CLI returns clear exit codes (`0` for success, `1` for invalid input or security failure, `2` for syntax error) and writes structured errors to stderr rather than unhandled Python tracebacks.

---

## 4. Local Validation Metrics Status

- **Status:** **PENDING OFFICIAL LABELLED DATASET**
- In strict adherence to competition data integrity rules:
  - All prior agent-authored benchmark cases in `data/approved_benchmarks` have been permanently deleted.
  - Prior synthetic validation metrics (`local_validation_report.json`) have been retracted.
  - Machine learning model fitting (LightGBM) is disabled; the pipeline currently runs in pure deterministic rule-based adjudication mode.
  - Official metrics (QWK, MAE, exact accuracy, macro precision) will be evaluated strictly on the official dataset once released by the organizers. Zero synthetic labels or invented metrics are reported.

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
| --- | --- | --- | --- |
| **Attempt 1** | **12 Nov 2026** | **Diagnostic Submission:** Submit standalone runnable package to test organizer automated test harness, execution speed, and dependency check pass/fail. | Receive operational execution status and benchmark score diagnostics. |
| **Attempt 2** | **13–14 Nov 2026** | **Refinement Submission:** Adjust thresholds, calibration, or schema adapters based on Attempt 1 diagnostics. | Verify improved benchmark score. |
| **Attempt 3** | **15 Nov 2026 (before 23:59 IST)** | **Final Code Freeze:** Final immutable submission for official Stage 1 ranking and code freeze. | Official competition ranking. |

