"""
Automated Standalone Packaging Script for Stage 1 Submission.
Packages standalone engine into `submission/` with zero dependency on development apps.
"""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
SUBMISSION_DIR = ROOT_DIR / "submission"


def package_submission():
    print(f"Creating clean standalone submission package in: {SUBMISSION_DIR}")

    if SUBMISSION_DIR.exists():
        shutil.rmtree(SUBMISSION_DIR)
    SUBMISSION_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Copy required core packages
    sub_pkg_dir = SUBMISSION_DIR / "packages"
    sub_pkg_dir.mkdir(parents=True, exist_ok=True)

    required_pkgs = [
        "core",
        "document_processing",
        "ml_inference",
        "retrieval",
        "agent_orchestration",
        "competition_engine",
    ]
    for pkg in required_pkgs:
        src = ROOT_DIR / "packages" / pkg
        dest = sub_pkg_dir / pkg
        shutil.copytree(src, dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache"))
        print(f"Copied packages/{pkg} -> submission/packages/{pkg}")

    # 2. Copy CLI runner
    shutil.copy2(ROOT_DIR / "run_inference.py", SUBMISSION_DIR / "run_inference.py")
    print("Copied run_inference.py -> submission/run_inference.py")

    # 3. Create standalone requirements.txt with exact pinned versions
    reqs_content = """# Standalone Stage 1 Competition Dependencies (Apache-2.0 / MIT / BSD-3 only)
pydantic==2.13.4
pypdfium2==5.15.2
pdfplumber==0.11.10
pdfminer.six==20260107
lightgbm==4.7.0
scikit-learn==1.9.0
numpy==2.5.2
rank-bm25==0.2.2
"""
    (SUBMISSION_DIR / "requirements.txt").write_text(reqs_content, encoding="utf-8")
    print("Generated submission/requirements.txt with exact pinned versions")

    # 4. Create standalone submission README
    readme_content = """# TRL Debate Engine — Stage 1 Standalone Submission

**Competition:** Techfest 2026–27 | 2nd APCTT Hackathon 2026  
**Challenge:** AI for Technology Readiness  
**License:** Apache License 2.0  
**Deployment:** Air-Gapped Standalone Inference Pipeline  

---

## 1. Operating Mode & Compliance
- **Adjudication Engine:** Deterministic rule-based criteria ladder with implied prerequisites.
- **Data Integrity:** Zero synthetic data or derived labels used for training. LightGBM fitting is disabled until official labelled benchmark training data is provided by the organizers.
- **Zero Hosted APIs:** No dependency on external web services, OpenAI, Anthropic, or external networks.
- **Licensing:** Uses only Apache-2.0, MIT, and BSD-3 compliant libraries. AGPL libraries (e.g. PyMuPDF) are strictly excluded.

---

## 2. Quick Start

### Installation
In an isolated Python 3.10+ environment:
```bash
pip install -r requirements.txt
```

### Running Inference
```bash
python run_inference.py --input <path_to_input_document> --output <path_to_output_json>
```

Example:
```bash
python run_inference.py --input sample_doc.pdf --output output.json
```
"""
    (SUBMISSION_DIR / "README.md").write_text(readme_content, encoding="utf-8")
    print("Generated submission/README.md")

    # 5. Create a sample document fixture in submission/samples
    samples_dir = SUBMISSION_DIR / "samples"
    samples_dir.mkdir(parents=True, exist_ok=True)
    sample_doc = samples_dir / "sample_synthetic_lab_report.txt"
    sample_doc.write_text(
        "Optical Quantum Sensor Prototype for Atmospheric Gas Analysis\n\n"
        "Abstract: We report on laboratory testing and experimental validation of an integrated quantum sensor. "
        "The prototype was constructed on a breadboard and subjected to controlled bench tests over 120 hours. "
        "The component assembly successfully demonstrated target sensitivity thresholds in laboratory environment.",
        encoding="utf-8"
    )

    test_out = SUBMISSION_DIR / "test_verification_output.json"

    print("Verifying standalone execution in submission directory...")
    res = subprocess.run(
        [sys.executable, str(SUBMISSION_DIR / "run_inference.py"), "--input", str(sample_doc), "--output", str(test_out)],
        capture_output=True,
        text=True,
        cwd=str(SUBMISSION_DIR)
    )

    if res.returncode == 0 and test_out.exists():
        print("[SUCCESS] Standalone submission package successfully verified!")
        print(f"Sample output: {test_out.read_text(encoding='utf-8')[:300]}...")
    else:
        print(f"[ERROR] Standalone verification failed:\n{res.stderr}")
        sys.exit(1)


if __name__ == "__main__":
    package_submission()

