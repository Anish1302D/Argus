# Third-Party Notices & Upstream Provenance

## 1. Team Argus Participant Module (`participant_module/`)
- **Component**: `argus-trl-assessor` (`participant_module/adapter.py`, `competition_engine/apctt_adapter.py`, `retrieval/engine.py`)
- **Version**: `1.0.0`
- **Copyright**: Copyright (c) 2026 Team Argus (Anish Mogam)
- **License**: `MIT` (per APCTT Decision D72; see `participant_module/LICENSE`)
- **Distribution**: Copied into `participant_module/`

## 2. Inherited & Adapted Upstream ARGUS Code (`participant_module/argus_engine/`)
- **Component**: `trl-debate-engine` / ARGUS Core (`trl_core`, `document_processing`, `ml_inference`, `agent_orchestration`, `competition_engine/runner.py`)
- **Upstream Repository**: `ishaj306/trl-debate-engine` (forked to `Anish1302D/Argus`, version `0.1.0`)
- **Upstream Copyright**: Copyright (c) 2026 Isha J & Contributors
- **Original Upstream License**: `Apache-2.0`
- **Distribution**: Copied into `participant_module/argus_engine/`
- **Attribution Notice**: Foundational data models (`trl_core`), linguistic modality/claim extractors (`ml_inference`), PDF extraction utilities (`document_processing`), and multi-agent debate abstractions (`agent_orchestration`) were inherited and adapted from the upstream ARGUS / `trl-debate-engine` repository and integrated with the MIT-licensed APCTT Stage 1 adapter (`competition_engine/apctt_adapter.py`) and hybrid BM25 retrieval engine (`retrieval/engine.py`). All upstream copyright and attribution notices are preserved herein.

## 3. Runtime Dependencies from Organizer Common Base Environment (`apctt-base-9e7fe1324bb6`)
`participant_module` ships zero third-party wheels, compiled binaries, or copied base-environment packages. At runtime it imports only from the Python `3.12` standard library and packages pre-installed in the organizer's read-only common base environment (`apctt-base-9e7fe1324bb6`, `x86_64-manylinux_2_28`, pinned in `requirements-base.lock` / `constraints-base.txt` of `apctt-participant-kit-0.5.0-cpu`):

| Component / Package | Exact Version (`apctt-base-9e7fe1324bb6`) | License | Origin / Supply Method |
| :--- | :--- | :--- | :--- |
| `numpy` | `2.5.3` | `BSD-3-Clause` | Supplied by organizer's common base (`apctt-base-9e7fe1324bb6`), not bundled |
| `pydantic` | `2.13.5` | `MIT` | Supplied by organizer's common base (`apctt-base-9e7fe1324bb6`), not bundled |
| `pydantic-core` | `2.46.5` | `MIT` | Supplied by organizer's common base (`apctt-base-9e7fe1324bb6`), not bundled |
| `annotated-types` | `0.8.0` | `MIT` | Supplied by organizer's common base (`apctt-base-9e7fe1324bb6`), not bundled |
| `typing-extensions` | `4.16.0` | `PSF-2.0` | Supplied by organizer's common base (`apctt-base-9e7fe1324bb6`), not bundled |
| `typing-inspection` | `0.4.4` | `MIT` | Supplied by organizer's common base (`apctt-base-9e7fe1324bb6`), not bundled |
| `pypdf` | `6.19.0` | `BSD-3-Clause` | Supplied by organizer's common base (`apctt-base-9e7fe1324bb6`), not bundled |
| `pypdfium2` *(optional fallback PDF reader)* | `5.14.0` | `Apache-2.0 OR BSD-3-Clause` (with bundled PDFium notices) | Supplied by organizer's common base (`apctt-base-9e7fe1324bb6`), not bundled |
| `pdfplumber` *(optional fallback PDF reader)* | `0.11.10` | `MIT` | Supplied by organizer's common base (`apctt-base-9e7fe1324bb6`), not bundled |
| `pdfminer-six` *(transitive via `pdfplumber`)* | `20260107` | `MIT` | Supplied by organizer's common base (`apctt-base-9e7fe1324bb6`), not bundled |
| `pillow` *(transitive via `pdfplumber`)* | `12.3.0` | `MIT-CMU` | Supplied by organizer's common base (`apctt-base-9e7fe1324bb6`), not bundled |
| `scikit-learn` *(optional ML feature utility)* | `1.9.1` | `BSD-3-Clause` | Supplied by organizer's common base (`apctt-base-9e7fe1324bb6`), not bundled |
| `scipy` *(transitive via `scikit-learn`)* | `1.18.1` | `BSD-3-Clause` | Supplied by organizer's common base (`apctt-base-9e7fe1324bb6`), not bundled |
| `joblib` *(transitive via `scikit-learn`)* | `1.6.0` | `BSD-3-Clause` | Supplied by organizer's common base (`apctt-base-9e7fe1324bb6`), not bundled |
| `threadpoolctl` *(transitive via `scikit-learn`)* | `3.7.0` | `BSD-3-Clause` | Supplied by organizer's common base (`apctt-base-9e7fe1324bb6`), not bundled |
