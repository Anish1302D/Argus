# 10 — Final Submission & Reproducibility Guide

## 1. Running the Full Test Suite
```bash
python -m pytest -q
```
All 83 tests (69 original Argus unit/milestone/API/CLI/frontend tests + 14 APCTT Stage 1 contract and lifecycle tests A–X) pass.

## 2. Running the Official License Audit
```bash
python apctt-participant-kit-0.5.0-cpu/tools/check_licenses.py --bundle my_submission --web apps/api
```

## 3. Building and Verifying the Stage 1 Submission ZIP
```bash
python apctt-participant-kit-0.5.0-cpu/tools/make_submission.py my_submission
python apctt-participant-kit-0.5.0-cpu/tools/make_submission.py --check argus_submission.zip
```

## 4. Running the Web Application & APCTT Validation Centre
```bash
python -m uvicorn api.main:app --app-dir apps/api/src --host 127.0.0.1 --port 8000
```
Open `http://127.0.0.1:8000/#apctt` to access the **08 APCTT Validation Centre** view.
