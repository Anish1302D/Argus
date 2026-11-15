# 01 — Official APCTT Participant Kit Audit

## 1. Kit Discovery & Exact Paths
Both official APCTT Participant Kit distributions (`v0.5.0`) are installed locally in the workspace root and treated as strictly **READ-ONLY**:

- **CPU Distribution:** `d:\Projects\Argus\apctt-participant-kit-0.5.0-cpu` (129 files)
- **CUDA Distribution:** `d:\Projects\Argus\apctt-participant-kit-0.5.0-cuda` (143 files)

## 2. Version & Environment Identification
- **Kit Version:** `0.5.0`
- **API Version:** `apctt-api-v0.2-draft`
- **Worker Protocol Version:** `apctt-worker-v2`
- **Submission Schema Version:** `apctt-submission-v3`
- **Declaration Schema Version:** `apctt-declaration-v2`
- **License Policy Version:** `apctt-license-policy-v2` (`0.4.0`, incorporating Decisions D52, D53, D54, D59, D63, D64, D66, D72, D74, D77, D81)
- **Official Checklist Version:** `APCTT-2026-CHECKLIST-v1` (12 criteria: `APCTT-C01` through `APCTT-C12`)
- **Common Base Environment ID:** `apctt-base-9e7fe1324bb6` (Python 3.11+ base with `pypdf 6.19.0`, `pypdfium2 5.14.0`, `pdfplumber 0.11.10`, `pdfminer.six 20260107`, `numpy`, `scipy`, `scikit-learn`, `pydantic`, `fastapi`, `uvicorn`, `torch`, `transformers`, `sentence-transformers`)

## 3. MANIFEST.sha256 Verification
Every file listed in `MANIFEST.sha256` was verified against its SHA-256 cryptographic digest:
- `apctt-participant-kit-0.5.0-cpu/MANIFEST.sha256`: **129 / 129 files verified (`0` failures)**
- `apctt-participant-kit-0.5.0-cuda/MANIFEST.sha256`: **143 / 143 files verified (`0` failures)**

## 4. Official Documentation & Tools Inspected
- `README.md`
- `docs/participant/PROBLEM_DESCRIPTION.md`
- `docs/participant/MODULE_GUIDE.md`
- `docs/participant/DATA_CONTRACT.md`
- `docs/participant/CONFIGURATION.md`
- `docs/participant/SUBMISSION.md`
- `docs/participant/LICENSING.md`
- `docs/participant/MODEL_CATALOG.md`
- `contracts/checklist.official.json`, `contracts/submission.schema.json`, `contracts/license-policy.json`, `contracts/worker-protocol.json`, `contracts/public-cases.json`
- `tools/make_submission.py`, `tools/check_licenses.py`, `tools/get_public_cases.py`, `tools/make_env.py`, `tools/make_request.py`
