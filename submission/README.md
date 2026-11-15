# Argus — Stage 1 Standalone Submission

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
