# 07 — Licensing & Data Provenance Audit

## 1. Team License Compliance (Decision D72)
Under APCTT Decision D72 (2026-10-13), the team's own work (Stage 1 bundle code/assets and Stage 2 web code) must be licensed exclusively under **MIT**:
- `my_submission/submission.json`: `"license": "MIT"`
- `my_submission/participant_module/LICENSE`: Full MIT License text matching `licenses/MIT.txt`
- `my_submission/participant_module/THIRD_PARTY_NOTICES.md`: Documents runtime base-environment dependencies
- `LICENSE` & `apps/api/LICENSE`: Full MIT License text
- `THIRD_PARTY_NOTICES.md` & `apps/api/THIRD_PARTY_NOTICES.md`: Documents open-source dependencies
- `pyproject.toml`: `license = { text = "MIT" }`

## 2. Official License Tool Verification (`tools/check_licenses.py`)
Command executed:
```bash
python apctt-participant-kit-0.5.0-cpu/tools/check_licenses.py --bundle my_submission --web apps/api
```
Result:
```text
APCTT licence check - policy apctt-license-policy-v2 0.4.0
status    kind     component                         version         licence   origin / reasons
allowed   team     participant_module                                MIT       submission.json
allowed   dataset  apctt-participant-kit-0.5.0 /...                  CC0-1.0   declaration.json
allowed   team     web system                                        -         LICENSE
summary: 3 allowed, 0 review, 0 denied -> exit 0
```

## 3. Data Provenance (`my_submission/declaration.json`)
- `declaration_version`: `"apctt-declaration-v2"`
- `no_team_training`: `true`
- `data_sources`: Public-domain USGS Scientific Investigations Reports (`CC0-1.0`) and official APCTT checklist used solely for diagnostic evaluation and schema verification.
