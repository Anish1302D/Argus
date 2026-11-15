# 09 — Submission Packaging Report

## 1. Submission Source Directory (`my_submission/`)
```text
my_submission/
├── participant_module/
│   ├── __init__.py
│   ├── adapter.py
│   ├── apctt_engine.py
│   ├── pdf_extractor.py
│   ├── retrieval_engine.py
│   ├── LICENSE
│   └── THIRD_PARTY_NOTICES.md
├── assets/
│   └── trl_rules.json
├── submission.json
├── declaration.json
└── README.md
```

## 2. Official Packaging & Verification Output (`tools/make_submission.py`)
Commands executed:
```bash
python apctt-participant-kit-0.5.0-cpu/tools/make_submission.py my_submission
python apctt-participant-kit-0.5.0-cpu/tools/make_submission.py --check argus_submission.zip
```
Verification summary:
- **Archive Path:** `D:\Projects\Argus\argus_submission.zip`
- **Archive Size:** `27.3 KB` (`<= 2.0 GB` limit)
- **Declared Package SHA-256:** `7b0d9d351578a757456b0fca017bc55d594f9d32cf420d35597daeadd26643d8`
- **Archive ZIP SHA-256:** `a689492bbdb469851f02f6405c5bac067a5ee111de22b0a8adfb258e14a3519b`
- **Checks Passed:**
  - `PASS size: 27.3 KB <= 2.0 GB`
  - `PASS layout: participant_module/, assets/, submission.json, declaration.json, README.md`
  - `PASS submission.json: team argus, base_id apctt-base-9e7fe1324bb6`
  - `PASS models: no catalogue model`
  - `PASS contents: no environment, packages, caches, links, catalogue weights or undeclared weights`
  - `PASS package hash matches submission.json`
  - `PASS licence: MIT, participant_module/LICENSE present`
  - `result: VALID (exit 0)`

