# Third-Party Notices & Upstream Provenance

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
