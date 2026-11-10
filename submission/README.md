# TRL Debate Engine — Stage 1 Standalone Submission

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
