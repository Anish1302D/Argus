# ARGUS Evaluation & Benchmark Guide
**Version:** 2.0.0-argus  
**System:** ARGUS Research Intelligence Engine  
**Target Environment:** 100% Air-Gapped Python 3.10+ Environment  

---

## 1. Quick Verification Commands

All evaluations, benchmarks, and regression tests run completely locally without internet access or GPU acceleration.

### 1.1 Complete Test Suite Execution
Execute the full 69-test regression and contract suite:
```bash
python -m pytest -v
```
Expected output: `69 passed in ~60-70s`.

### 1.2 Milestone-Specific Regression Suites
```bash
# Milestone 1: Evidence Intelligence Engine (5 tests)
pytest tests/test_milestone_1_evidence_intelligence.py

# Milestone 2: Evidence Traceability & Provenance (5 tests)
pytest tests/test_milestone_2_evidence_traceability.py

# Milestone 3: Explainable Adversarial Adjudication (5 tests)
pytest tests/test_milestone_3_adversarial_adjudication.py

# Milestone 4: Scientific Validation & Adversarial Corpus (4 tests)
pytest tests/test_milestone_4_scientific_validation.py

# Milestone 5: Research Intelligence Experience (6 tests)
pytest tests/test_milestone_5_research_workspace.py
```

### 1.3 Standalone Air-Gapped Inference
Evaluate an arbitrary technical document offline via the submission bundle:
```bash
python submission/run_inference.py -i tests/data/adversarial_corpus/01_multiple_negations.txt -o output_assessment.json
```

---

## 2. Experimental Ablation Studies

To quantify the empirical contribution of each subsystem in the 14-stage pipeline, ARGUS provides an automated ablation evaluation script:

```bash
python scripts/run_ablation_study.py
```

The script evaluates the adversarial benchmark corpus across 5 experimental configurations:
1. `FULL_PIPELINE`: Complete 14-stage architecture with all intelligence layers active.
2. `NO_NEGATION_ANALYSIS`: Disables grammatical negation and modality filters.
3. `NO_CONTRADICTION_DETECTION`: Disables cross-section tension analysis between abstracts and limitations.
4. `NO_MULTI_AGENT_DEBATE`: Disables adversarial challenge and referee prerequisite audit.
5. `KEYWORD_ONLY_BASELINE`: Simulates naive keyword matching without structural claim extraction.

### Summary Results Matrix (`docs/ablation_study_results.json`)

| Configuration | Exact Acc | Adjacent Acc ($\pm 1$) | Mean Abs Error (MAE) | Quadratic Weighted Kappa (QWK) |
|---|---|---|---|---|
| **ARGUS Full Pipeline (Stage 2)** | **75.0%** | **91.7%** | **0.583** | **0.865** |
| Without Negation Analysis | 50.0% | 66.7% | 1.417 | 0.582 |
| Without Contradiction Detection | 66.7% | 83.3% | 0.833 | 0.749 |
| Without Multi-Agent Debate | 58.3% | 75.0% | 1.167 | 0.641 |
| Keyword-Only Naive Baseline | 33.3% | 50.0% | 2.250 | 0.312 |

#### Key Ablation Findings:
- Disabling **Negation Analysis** causes MAE to spike from $0.583$ to $1.417$, because negated milestones are mistakenly treated as completed achievements.
- Disabling **Contradiction Detection** causes overconfidence in documents where marketing abstracts claim flight heritage but disclaimers clarify that only arc-jet ground tests occurred.
- The **Multi-Agent Referee** provides an essential conservative check, enforcing prerequisite compliance before granting high TRL ratings.

---

## 3. Epistemic Calibration & Uncertainty Benchmark

To verify that ARGUS confidence estimates are well-calibrated and avoid statistical overconfidence, execute:

```bash
python scripts/analyze_calibration.py
```

### Calibration Metrics Summary (`docs/calibration_analysis_report.json`)

| Metric | Computed Value | Scientific Interpretation |
|---|---|---|
| **Expected Calibration Error (ECE)** | **0.185** | Bounded epistemic deviation across confidence bins; demonstrates conservative calibration. |
| **Brier Reliability Score** | **0.142** | Mean squared difference between predicted certainty and observed accuracy. Low values signify high calibration accuracy. |
| **Average Prediction Confidence** | **0.688** | Avoids pathological extreme confidence (0.0 or 1.0), properly reserving high certainty only for multi-measurement empirical papers. |
| **Average Prediction Accuracy** | **0.750** | Outperforms baseline estimators on complex adversarial edge cases. |

---

## 4. Hardware Profiles & Resource Consumption

ARGUS was engineered to execute within strict competition hardware constraints:

- **CPU Architecture:** Standard x86_64 or ARM64 multi-core processor (single-core minimum).
- **RAM Footprint:** $<180 \text{ MB}$ resident memory during full pipeline execution.
- **Inference Latency:** $<85 \text{ ms}$ per 10-page technical document.
- **GPU Acceleration:** $0 \text{ MB}$ VRAM required. No CUDA/ROCm dependencies.
- **Network I/O:** $0 \text{ bytes}$. Operates in completely isolated network environments (loopback-only HTTP server).
