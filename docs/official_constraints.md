# Official Competition Constraints: Stage 1 Evaluation

**Competition:** Techfest 2026–27 | 2nd APCTT Hackathon 2026  
**Track:** AI for Technology Readiness  
**Source Document:** `docs/official/APCTT_Hackathon_1_compressed.pdf` (4 pages)  
**Compilation Date:** November 10, 2026  
**Status:** Primary Source Extracted — Unspecified Items Marked Strict `UNKNOWN`

---

## 1. Primary Source Document Overview
- **File Name:** `APCTT_Hackathon_1_compressed.pdf`
- **Pages:** 4
- **Stated Objective (Page 1):**
  > *"To develop functional AI-powered, AI-assisted, or hybrid assessment tools capable of evaluating Technology Readiness Levels (TRL 1–9) from unstructured technical documentation, streamlining technology transfer workflows, and providing transparent, auditable evidence for innovation ecosystems across developing nations."*
- **Challenge Question (Page 1):**
  > *"How can an AI pipeline accurately parse raw technology documentation (e.g., patents, research papers, R&D reports), predict its correct Technology Readiness Level (TRL 1–9), synthesize supporting evidence, and output an auditable, actionable gap analysis to guide technology progression?"*

---

## 2. Extracted Constraints Matrix

| Dimension | Exact Official Quote | Status / Value |
|---|---|---|
| **Input Format** | *"raw technology documentation (e.g., patents, research papers, R&D reports)"* (Page 1) | **UNKNOWN** (Exact file extension, folder hierarchy, single vs batch argument, or manifest schema is not specified in the document). |
| **Output Schema** | *"Strict pass/fail compliance on output schema, execution speed, and dependency checks"* (Page 2)<br>*"predict its correct Technology Readiness Level (TRL 1–9), synthesize supporting evidence, and output an auditable, actionable gap analysis"* (Page 1)<br>*"Use of undisclosed private API keys, hardcoded output schemas, or plagiarism will result in immediate disqualification."* (Page 3, Rule 6) | **UNKNOWN** (Exact JSON/CSV column names, keys, and validation schema are not defined in the PDF). |
| **Approved Data Sources** | *"Teams develop their AI model using approved public data sources."* (Page 1)<br>*"The detailed problem statement instructions, specific dataset guidelines, assessment criteria checklist, and development sample cases will be officially released to all registered teams on October 10, 2026"* (Page 1) | **UNKNOWN** (Specific approved dataset list, repository links, or pre-labeled training corpora are not detailed in the document). |
| **Time & Hardware Limits** | *"Strict pass/fail compliance on output schema, execution speed, and dependency checks"* (Page 2) | **UNKNOWN** (Specific CPU/GPU specifications, RAM allocation, per-document timeout in seconds, and overall batch timeout are not defined). |
| **Network & Dependency Rules** | *"Strict pass/fail compliance on... dependency checks"* (Page 2)<br>*"Submissions are frozen at the Stage 1 deadline; no model retraining, fine-tuning, or replacement is permitted for Stage 2."* (Page 3, Rule 2)<br>*"Use of undisclosed private API keys, hardcoded output schemas, or plagiarism will result in immediate disqualification."* (Page 3, Rule 6)<br>*"The use of unauthorized external AI tools during live rounds is strictly prohibited unless explicitly allowed by the judges."* (Page 3, Rule 7)<br>*"Finalists must release their Stage 2 deployment package under the Apache License 2.0 for non-profit developmental use."* (Page 3, Rule 5) | **Network:** Prohibits undisclosed private API keys and unauthorized external tools (implies fully self-contained offline execution).<br>**Dependencies:** Must pass automated dependency checks.<br>**Licensing:** Apache 2.0 required for finalist package. |
| **Packaging Format** | *"Registered teams are allowed a maximum of 3 code submission attempts before the Stage 1 deadline."* (Page 2)<br>*"For the first 2 submissions, organizers will run automated testing on the code and provide diagnostic feedback, including operational execution status (whether the code runs successfully or fails) and benchmark performance scores."* (Page 2)<br>*"The 3rd submission serves as the final, immutable entry for official Stage 1 ranking and code freeze"* (Page 2) | **UNKNOWN** (Specific delivery mechanism—e.g., zip archive, GitHub repository tag, Docker container, or specific CLI entrypoint—is not specified in the document). |
| **Exact Metric Definition** | *"Evaluation Criteria (100% Performance-Based):*<br>*● Model Ordinal Accuracy & Precision on Hidden Evaluation Set (Primary Score)*<br>*● Strict pass/fail compliance on output schema, execution speed, and dependency checks"* (Page 2) | **UNKNOWN** (Mathematical formulation for "Ordinal Accuracy & Precision"—whether Quadratic Weighted Kappa, Mean Absolute Error, off-by-one tolerance, or Macro Precision—is not provided in the document). |

---

## 3. Official Timeline & Submission Rules Quoted

- **Final Model & Code Submission Deadline (Stage 1):**  
  > *"November 15, 2026 (23:59 IST)"* (Page 3)
- **Submission Quota & Diagnostics:**  
  > *"Registered teams are allowed a maximum of 3 code submission attempts before the Stage 1 deadline. For the first 2 submissions, organizers will run automated testing on the code and provide diagnostic feedback, including operational execution status (whether the code runs successfully or fails) and benchmark performance scores. The 3rd submission serves as the final, immutable entry for official Stage 1 ranking and code freeze"* (Page 2)
- **Originality & Intellectual Property:**  
  > *"Submissions must represent the team's original work. Pre-existing code and model weights remain the property of the participants."* (Page 3, Rule 4)
- **Strict Disqualification Triggers:**  
  > *"Use of undisclosed private API keys, hardcoded output schemas, or plagiarism will result in immediate disqualification."* (Page 3, Rule 6)
- **Official Queries & Channels:**  
  > *"Instructions for specific rounds will be communicated on time to registered email IDs, and official announcements will be posted on techfest.org. All contest queries must be submitted through the official portal's Doubt section."* (Page 3, Rules 8 & 9)

---

## 4. Open Discrepancies & Blocking Unknowns

The document states on Page 1:
> *"Note on Evaluation & Instructions: The detailed problem statement instructions, specific dataset guidelines, assessment criteria checklist, and development sample cases will be officially released to all registered teams on October 10, 2026, immediately after registrations close."*

Because this compressed PDF is the broad competition brief, the October 10 supplemental release containing:
1. The **exact dataset guidelines and sample development cases**
2. The **exact output schema definition**
3. The **exact packaging / CLI invocation format**
4. The **mathematical formula for "Ordinal Accuracy & Precision"**
must be acquired from the team portal / registered email or maintained strictly behind modular adapters without guessing.

### 4.1 Data Integrity & Adjudication Mode
- All agent-authored benchmark cases in `data/approved_benchmarks` have been deleted.
- `docs/local_validation_report.json` is retracted.
- No LightGBM model fitted on synthetic data will be shipped.
- The standalone engine runs in **deterministic rule-based adjudication mode only** until official labelled data with verifiable primary-source provenance is provided by the organizers.


