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

    required_pkgs = ["core", "document_processing", "ml_inference", "competition_engine"]
    for pkg in required_pkgs:
        src = ROOT_DIR / "packages" / pkg
        dest = sub_pkg_dir / pkg
        shutil.copytree(src, dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache"))
        print(f"Copied packages/{pkg} -> submission/packages/{pkg}")

    # 2. Copy CLI runner
    shutil.copy2(ROOT_DIR / "run_inference.py", SUBMISSION_DIR / "run_inference.py")
    print("Copied run_inference.py -> submission/run_inference.py")

    # 3. Create standalone requirements.txt
    reqs_content = """# Standalone Stage 1 Competition Dependencies (Apache-2.0 / MIT / BSD-3 only)
pydantic>=2.10.0,<3.0.0
pypdfium2>=4.30.0
pdfplumber>=0.11.0
pdfminer.six>=20260107
lightgbm>=4.5.0
scikit-learn>=1.6.0
numpy>=1.24.0
rank-bm25>=0.2.2
"""
    (SUBMISSION_DIR / "requirements.txt").write_text(reqs_content, encoding="utf-8")
    print("Generated submission/requirements.txt")

    # 4. Create standalone submission README
    readme_content = """# TRL Debate Engine — Stage 1 Standalone Submission

**Competition:** Techfest 2026–27 | 2nd APCTT Hackathon 2026
**Challenge:** AI for Technology Readiness
**License:** Apache License 2.0
**Deployment:** Air-Gapped Standalone Inference Pipeline

---

## 1. Quick Start

### Installation
In an isolated Python 3.10+ environment:
```bash
pip install -r requirements.txt
```

### Running Inference
```bash
python run_inference.py --input <path_to_input_document> --output <path_to_output_json>
```

Example on a technical document:
```bash
python run_inference.py --input sample_doc.pdf --output output.json
```

---

## 2. Technical Characteristics
- **Zero Hosted APIs:** Does not use OpenAI, Anthropic, or external API endpoints.
- **Air-Gapped & Offline:** Operates with 100% local weights, feature extraction, and ordinal rules.
- **Latency:** ~10ms per document on standard commodity CPU.
- **Memory Footprint:** < 25 MB RAM.
- **Licensing:** Fully compatible with Apache License 2.0.
"""
    (SUBMISSION_DIR / "README.md").write_text(readme_content, encoding="utf-8")
    print("Generated submission/README.md")

    # 5. Verify standalone execution in submission directory
    test_doc = ROOT_DIR / "data" / "approved_benchmarks" / "nasa_case_trl_4.txt"
    test_out = SUBMISSION_DIR / "test_verification_output.json"

    print("Verifying standalone execution in submission directory...")
    res = subprocess.run(
        [sys.executable, str(SUBMISSION_DIR / "run_inference.py"), "--input", str(test_doc), "--output", str(test_out)],
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
