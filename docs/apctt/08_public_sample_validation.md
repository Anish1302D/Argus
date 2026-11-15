# 08 — Public Sample & Smoke Case Validation Report

## 1. Official Smoke Cases Executed via `apctt_runtime/worker.py`
The 3 official diagnostic smoke cases (`USGS-SDG-012`, `USGS-SDG-040`, `USGS-SDG-061`) were downloaded and verified via `tools/get_public_cases.py --download --smoke` and `--make-requests --smoke`, and executed alongside `docs/EXAMPLE_REQUEST.json` (`DEMO-001`) through the cold worker subprocess (`apctt_runtime/worker.py`).

| Case ID | Pages | Organizer Reference | Argus `assessment_status` | Argus `predicted_trl` | Met Criteria | `validate_result` Issues | Worker `assess_ms` |
|---|---:|---|---|:---:|---:|---:|---:|
| `DEMO-001` | 2 | Abstained (`insufficient evidence`) | `abstained` (`insufficient evidence`) | `null` | 1 / 12 (`APCTT-C04`) | `0` | 28.4 ms |
| `USGS-SDG-012` | 24 | TRL 4 (Coupled PRMS/SNTemp software + example datasets) | `completed` | `4` | 7 / 12 (`C01–C04, C10–C12`) | `0` | 1,022.1 ms |
| `USGS-SDG-040` | 22 | TRL 7 (Meramec River inundation map library calibrated to gages & high-water marks) | `completed` | `7` | 10 / 12 (`C01–C07, C10–C12`) | `0` | 887.6 ms |
| `USGS-SDG-061` | 52 | TRL 6 (PRMS model calibrated prefire 2007–2012 & postfire 2014–2015) | `completed` | `6` | 9 / 12 (`C01–C06, C10–C12`) | `0` | 2,410.1 ms |

## 2. Evidence Quality Verification
- Every `"met"` criterion across all 4 cases cites between 1 and 3 distinct `(document_id, page)` references.
- Every `supporting_span` is verified to be an exact verbatim substring of its cited page text and never a bare TRL assertion.
- Every `"insufficient evidence"` criterion provides a specific, non-blank `missing_evidence` explanation.

