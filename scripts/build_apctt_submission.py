"""
Build and validate the official APCTT Stage 1 submission workspace (`apctt_submission/`)
and output archive (`artifacts/apctt/argus_submission.zip`).

Packages the existing Argus pure-Python reasoning engine modules (`trl_core`,
`document_processing`, `ml_inference`, `agent_orchestration`, `retrieval`,
`competition_engine`) into `apctt_submission/participant_module/argus_engine/`
so that `participant_module.adapter:AssessmentModule` executes completely
self-contained inside the isolated APCTT worker process.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
KIT_DIR = ROOT_DIR / "apctt-participant-kit-0.5.0-cpu"
SUBMISSION_DIR = ROOT_DIR / "apctt_submission"
MODULE_DIR = SUBMISSION_DIR / "participant_module"
ENGINE_DIR = MODULE_DIR / "argus_engine"
ASSETS_DIR = SUBMISSION_DIR / "assets"
ARTIFACTS_DIR = ROOT_DIR / "artifacts" / "apctt"

ENGINE_PACKAGES = [
    ("core", "trl_core"),
    ("document_processing", "document_processing"),
    ("ml_inference", "ml_inference"),
    ("agent_orchestration", "agent_orchestration"),
    ("retrieval", "retrieval"),
    ("competition_engine", "competition_engine"),
]


def _ignore_caches(directory: str, contents: list[str]) -> list[str]:
    return [
        name
        for name in contents
        if name in {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".DS_Store"}
        or name.endswith((".pyc", ".pyo"))
    ]


def build_submission_workspace() -> None:
    if SUBMISSION_DIR.exists():
        shutil.rmtree(SUBMISSION_DIR)

    MODULE_DIR.mkdir(parents=True, exist_ok=True)
    ENGINE_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Copy Argus engine packages into participant_module/argus_engine/
    (ENGINE_DIR / "__init__.py").write_text(
        '"""Self-contained Argus reasoning engine packages for APCTT Stage 1."""\n',
        encoding="utf-8",
    )
    for pkg_folder, import_name in ENGINE_PACKAGES:
        src_dir = ROOT_DIR / "packages" / pkg_folder / "src" / import_name
        dst_dir = ENGINE_DIR / import_name
        shutil.copytree(src_dir, dst_dir, ignore=_ignore_caches)

    # 2. Write participant_module/__init__.py and participant_module/adapter.py
    init_code = '''"""
ARGUS Official APCTT Stage 1 Participant Module.
Entrypoint: `participant_module.adapter:AssessmentModule`
"""

from pathlib import Path
import sys

_ENGINE_ROOT = Path(__file__).resolve().parent / "argus_engine"
if str(_ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(_ENGINE_ROOT))

from participant_module.adapter import AssessmentModule

__all__ = ["AssessmentModule"]
'''
    (MODULE_DIR / "__init__.py").write_text(init_code, encoding="utf-8")

    adapter_code = '''"""
Official APCTT Stage 1 Entrypoint (`participant_module.adapter:AssessmentModule`).

Connects the APCTT worker execution protocol directly to the packaged Argus
assessment engine (`participant_module/argus_engine/`).
"""

from pathlib import Path
import sys

_ENGINE_ROOT = Path(__file__).resolve().parent / "argus_engine"
if str(_ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(_ENGINE_ROOT))

from competition_engine.apctt_adapter import AssessmentModule

__all__ = ["AssessmentModule"]
'''
    (MODULE_DIR / "adapter.py").write_text(adapter_code, encoding="utf-8")

    # 3. Write participant_module/LICENSE (MIT text as required by Decision D72)
    mit_template = (KIT_DIR / "licenses" / "MIT.txt").read_text(encoding="utf-8")
    mit_text = mit_template.replace("[year]", "2026").replace("[fullname]", "Team Argus (Anish Mogam)")
    (MODULE_DIR / "LICENSE").write_text(mit_text, encoding="utf-8")

    # 4. Write participant_module/THIRD_PARTY_NOTICES.md (including upstream provenance)
    notices_text = """# Third-Party Notices & Upstream Provenance

## 1. Team Argus Participant Module (`participant_module/`)
- **Copyright**: Copyright (c) 2026 Team Argus (Anish Mogam)
- **License**: MIT License (per APCTT Decision D72; see `participant_module/LICENSE`)

## 2. Upstream Repository Provenance (`trl-debate-engine` / Argus Core)
- **Upstream Project**: `trl-debate-engine` / ARGUS (`ishaj306/trl-debate-engine`, forked to `Anish1302D/Argus`)
- **Upstream Copyright**: Copyright (c) 2026 Isha J & Contributors
- **Original Upstream License**: Apache License 2.0 (`Apache-2.0`)
- **Notice**: Foundational data models (`trl_core`), linguistic modality/claim extractors (`ml_inference`), and multi-agent debate abstractions (`agent_orchestration`) were adapted from the project's core repository and integrated with the MIT-licensed APCTT Stage 1 adapter (`competition_engine/apctt_adapter.py`) and hybrid BM25 retrieval engine (`retrieval/engine.py`). All original copyright and attribution notices are preserved herein.

## 3. Organizer Common Base Environment Dependencies (`apctt-base-2026.1-py312`)
`participant_module` ships zero third-party wheels, binaries, or copied base packages. At runtime it imports only from the Python standard library and packages pre-installed in the organizer's read-only base environment (`apctt-base-2026.1-py312`):
- **NumPy** (`numpy`): BSD-3-Clause
- **Pydantic** (`pydantic`): MIT
- **pypdf** (`pypdf`): BSD-3-Clause
- **pypdfium2** (`pypdfium2`): Apache-2.0 OR BSD-3-Clause
- **pdfplumber** (`pdfplumber`) / **pdfminer.six** (`pdfminer.six`): MIT
"""
    (MODULE_DIR / "THIRD_PARTY_NOTICES.md").write_text(notices_text, encoding="utf-8")

    # 5. Write assets/trl_rules.json
    rules_payload = {
        "methodology_version": "argus-apctt-stage1-v1.0",
        "description": "Domain-independent phrase anchors supplementing dynamic checklist profiling.",
        "criteria": {
            "APCTT-C01": {"phrases": ["basic principles", "governing equations", "theoretical formulation"]},
            "APCTT-C02": {"phrases": ["technology concept", "intended application", "conceptual framework"]},
            "APCTT-C03": {"phrases": ["proof of concept", "feasibility study", "analytical verification"]},
            "APCTT-C04": {"phrases": ["laboratory test", "laboratory environment", "breadboard", "coupled simulation"]},
            "APCTT-C05": {"phrases": ["relevant environment", "representative conditions", "field observations"]},
            "APCTT-C06": {"phrases": ["demonstrated in a relevant environment", "calibrated model", "prototype demonstration"]},
            "APCTT-C07": {"phrases": ["operational environment", "field deployment", "flood-inundation map library", "streamgage"]},
            "APCTT-C08": {"phrases": ["completed and qualified", "qualification testing", "user guide"]},
            "APCTT-C09": {"phrases": ["mission operations", "proven in successful", "monitoring storm tide"]},
            "APCTT-C10": {"phrases": ["quantified results", "acceptance criteria", "statistically satisfactory", "Nash-Sutcliffe", "RMSE"]},
            "APCTT-C11": {"phrases": ["test conditions", "study area", "model configuration", "boundary conditions"]},
            "APCTT-C12": {"phrases": ["assessment target", "evaluated system", "coupled model"]},
        },
    }
    (ASSETS_DIR / "trl_rules.json").write_text(
        json.dumps(rules_payload, indent=2) + "\n",
        encoding="utf-8",
    )

    # 6. Write submission.json (declared_package_sha256 will be populated by tools/make_submission.py)
    base_env = json.loads((KIT_DIR / "contracts" / "base-environment.json").read_text(encoding="utf-8"))
    base_id = str(base_env["base_id"])
    submission_payload = {
        "submission_version": "apctt-submission-v3",
        "team": "argus",
        "package_id": "argus-trl-assessor",
        "package_version": "1.0.0",
        "base_id": base_id,
        "entrypoint": "participant_module.adapter:AssessmentModule",
        "declared_package_sha256": None,
        "license": "MIT",
        "compute": {
            "device": "cpu",
        },
        "settings": {
            "rules_path": "trl_rules.json",
        },
        "models": [],
    }
    (SUBMISSION_DIR / "submission.json").write_text(
        json.dumps(submission_payload, indent=2) + "\n",
        encoding="utf-8",
    )

    # 7. Write declaration.json
    declaration_payload = {
        "declaration_version": "apctt-declaration-example-v1",
        "team": "argus",
        "package_id": "argus-trl-assessor",
        "package_version": "1.0.0",
        "declared_package_sha256": "0" * 64,
        "team_training": "no_team_training",
        "no_team_training": True,
        "training": None,
        "data_sources": [
            {
                "source": "U.S. Geological Survey (USGS) Public Smoke-Test Reports (SIR 2020-5002 / SIR 2019-5142 / OFR 2019-1096)",
                "version": "public-cases-v1",
                "date": "2026-10-15",
                "role": "local smoke-test validation only; not bundled and not memorized",
                "label_origin": "no labels used; evaluated purely via general-purpose evidence extraction",
                "linked_project": "APCTT Stage 1 Public Smoke Cases (USGS-SDG-012, USGS-SDG-040, USGS-SDG-061)",
                "license": "CC0-1.0",
            },
            {
                "source": "APCTT Participant Kit Official Checklist & Demo Fixture (DEMO-001)",
                "version": "0.5.0",
                "date": "2026-10-15",
                "role": "contract schema verification and lifecycle smoke testing",
                "label_origin": "organizer reference kit fixture",
                "linked_project": "apctt-participant-kit-0.5.0-cpu",
                "license": "Apache-2.0",
            },
            {
                "source": "Team Argus Domain-Independent Linguistic Phrase Rules (assets/trl_rules.json)",
                "version": "1.0.0",
                "date": "2026-11-15",
                "role": "supplementary phrase anchors for dynamic checklist criterion profiling",
                "label_origin": "authored by Team Argus",
                "linked_project": "argus-trl-assessor",
                "license": "MIT",
            },
        ],
        "inference_assets": {
            "source_code": "participant_module/ (adapter.py + argus_engine/ pure-Python packages)",
            "weights": [],
            "prompts_or_rules": ["assets/trl_rules.json"],
            "reference_assets": [],
            "dependency_declarations": [
                "apctt-base-2026.1-py312 common base environment (numpy, pydantic, pypdf, pypdfium2, pdfplumber)",
            ],
        },
        "notes": "Deterministic CPU-only hybrid retrieval, claim/modality analysis, contradiction detection, and multi-agent Referee TRL adjudication module. No external or team-trained model weights are used.",
    }
    (SUBMISSION_DIR / "declaration.json").write_text(
        json.dumps(declaration_payload, indent=2) + "\n",
        encoding="utf-8",
    )

    # 8. Write README.md
    readme_text = """# ARGUS — Official APCTT Stage 1 Assessment Module (`argus-trl-assessor`)

**Team**: `argus`  
**Package ID**: `argus-trl-assessor` (`1.0.0`)  
**Entrypoint**: `participant_module.adapter:AssessmentModule`  
**Base Environment**: `apctt-base-2026.1-py312`  
**License**: `MIT`

## Overview

ARGUS (Automated Readiness Grading & Uncertainty Synthesis) is a domain-independent, deterministic Technology Readiness Level (TRL 1–9) assessment engine. This package connects the official APCTT Stage 1 worker protocol (`apctt-worker-v2`) to the packaged Argus reasoning engine (`participant_module/argus_engine/`):

1. **Multi-Backend Verbatim PDF Page Extraction (`document_processing`)**: Extracts 1-indexed page text via `pypdf`, `pypdfium2`, or `pdfplumber` while preserving exact on-page character substrings for `supporting_span` verification.
2. **Untrusted Input Sanitization (`trl_core.sanitizer`)**: Strips zero-width/bidirectional Unicode overrides and filters prompt-injection or output-forcing payloads embedded inside PDFs.
3. **Linguistic Modality, Negation, Simulation & Temporal Analysis (`ml_inference`)**: Distinguishes completed empirical achievements from negated, failed, planned/future, hypothetical, and simulation-only claims, preventing bare `"TRL X"` assertions or keyword stuffing from inflating readiness levels.
4. **Dynamic Checklist Profiling & Hybrid BM25 Retrieval (`retrieval` + `competition_engine`)**: Dynamically profiles every criterion in `config["checklist"]` (supporting both `apctt-trl-v1` `APCTT-C01`..`APCTT-C12` and custom/modified checklists) and ranks distinct `(document_id, page)` passages.
5. **Contradiction Detection & Multi-Agent Referee Review (`trl_core` + `agent_orchestration`)**: Executes `StructuredClaimExtractor`, `EvidenceQualityAssessor`, `ContradictionDetector`, `CriteriaMapper`, `ReviewProtocol` (`OptimistReviewer`, `SkepticReviewer`, `RefereeAdjudicator`), and `UncertaintyModel`.
"""
    (SUBMISSION_DIR / "README.md").write_text(readme_text, encoding="utf-8")


def main() -> int:
    build_submission_workspace()
    check_licenses_script = KIT_DIR / "tools" / "check_licenses.py"
    make_sub_script = KIT_DIR / "tools" / "make_submission.py"

    print("--- Running check_licenses.py --bundle apctt_submission ---")
    res_lic = subprocess.run(
        [sys.executable, str(check_licenses_script), "--bundle", str(SUBMISSION_DIR)],
        capture_output=True,
        text=True,
    )
    print(res_lic.stdout)
    if res_lic.stderr:
        print(res_lic.stderr, file=sys.stderr)
    if res_lic.returncode != 0:
        return res_lic.returncode

    print("--- Running make_submission.py apctt_submission --output artifacts/apctt ---")
    res_pack = subprocess.run(
        [
            sys.executable,
            str(make_sub_script),
            str(SUBMISSION_DIR),
            "--output",
            str(ARTIFACTS_DIR),
        ],
        capture_output=True,
        text=True,
    )
    print(res_pack.stdout)
    if res_pack.stderr:
        print(res_pack.stderr, file=sys.stderr)
    if res_pack.returncode != 0:
        return res_pack.returncode

    zip_path = ARTIFACTS_DIR / "argus_submission.zip"
    print(f"--- Running make_submission.py --check {zip_path} ---")
    res_check = subprocess.run(
        [sys.executable, str(make_sub_script), "--check", str(zip_path)],
        capture_output=True,
        text=True,
    )
    print(res_check.stdout)
    if res_check.stderr:
        print(res_check.stderr, file=sys.stderr)
    return res_check.returncode


if __name__ == "__main__":
    raise SystemExit(main())
