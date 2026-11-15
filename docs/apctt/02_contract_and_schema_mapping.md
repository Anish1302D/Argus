# 02 — Official Contract & Schema Mapping

## 1. Entrypoint & Lifecycle Contract (`MODULE_GUIDE.md`)
- **Entrypoint:** `participant_module.adapter:AssessmentModule`
- **Lifecycle Methods:**
  - `__init__(self) -> None`: Initializes lightweight instance state.
  - `load(self, config: Mapping[str, Any], asset_root: Path) -> None`: Reads `config["checklist"]` (`version`, `criteria`) dynamically and loads optional rule assets from `asset_root`.
  - `assess(self, case: Mapping[str, Any], context: Any) -> dict[str, Any]`: Evaluates `case` within `context.remaining_ms()` and returns a contract-compliant `AssessmentResult` dictionary.
  - `reset_case(self) -> None`: Clears per-case state between runs; never raises.
  - `close(self) -> None`: Releases resources on worker exit; never raises.

## 2. Dynamic Checklist Mapping (`APCTT-2026-CHECKLIST-v1` & Custom Checklists)
ARGUS never hardcodes criterion IDs (`APCTT-C01..C12`). Every criterion in `config["checklist"]["criteria"]` is profiled dynamically from its `criterion_id` and `description`:
- **TRL Milestone Criteria (TRL 1–9):** Inferred when description specifies TRL 1..9 or corresponding readiness stage semantics.
- **Quantified Results vs. Requirements (e.g., `APCTT-C10`):** Inferred when description requires quantitative/measured performance compared against requirements, targets, or baselines.
- **Environment & Test Article Defined (e.g., `APCTT-C11`):** Inferred when description requires test conditions and configuration/fidelity of the tested article relative to the intended application.
- **Evidence Matches Assessment Target (e.g., `APCTT-C12`):** Inferred when description requires cited evidence to concern the assessed target itself rather than a different element or parent project.
- **Arbitrary Custom Criteria:** Evaluated dynamically using lexical/semantic retrieval over the criterion's description and optional rule phrases.

## 3. Output Schema Rules (`src/apctt_contracts/results.py`)
| Field | Completed | Abstained | Failed |
|---|---|---|---|
| `schema_version` | Mirrors `case["schema_version"]` | Mirrors `case["schema_version"]` | Mirrors `case["schema_version"]` |
| `checklist_version` | Mirrors `config["checklist"]["version"]` | Mirrors `config["checklist"]["version"]` | Mirrors `config["checklist"]["version"]` |
| `case_id` | Mirrors `case["case_id"]` | Mirrors `case["case_id"]` | Mirrors `case["case_id"]` |
| `assessment_target` | Exact copy of `case["assessment_target"]` | Exact copy of `case["assessment_target"]` | Exact copy of `case["assessment_target"]` |
| `assessment_status` | `"completed"` | `"abstained"` | `"failed"` |
| `predicted_trl` | Strict `int` `1..9` (never `bool`/`float`) | `None` | `None` |
| `criterion_status` | Map of every checklist `criterion_id` -> `"met" \| "not met" \| "insufficient evidence"` | Same | Same (or `{}`) |
| `evidence_reference` | Map of every `criterion_id` -> list of `{"document_id", "page", "supporting_span"}` (non-empty for every `"met"` criterion) | Same | Same |
| `missing_evidence` | Map of `criterion_id` -> non-blank explanation (required for every `"insufficient evidence"` criterion) | Same | Same |
| `abstention_reason` | `None` | `"insufficient evidence" \| "conflicting evidence" \| "ambiguous scope" \| "out of scope"` | `None` |
| `error_code` | `None` | `None` | Non-blank string (e.g. `"DOCUMENT_UNREADABLE"`) |
| Optional fields (`confidence`, `uncertainty`, `trl_rationale`, `criterion_rationale`) | Included (`uncertainty` interval `1 <= lower <= predicted_trl <= upper <= 9`) | `trl_rationale` omitted (`E19`); `confidence` & `criterion_rationale` allowed | **All omitted** (`failed_omits_optional`) |

