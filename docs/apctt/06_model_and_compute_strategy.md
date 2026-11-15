# 06 — Model, Retrieval & Compute Strategy

## 1. Compute Profile (`compute.device = "cpu"`)
- **Target Base Environment:** `apctt-base-9e7fe1324bb6` (CPU & CUDA compatible).
- **Declared Compute Device:** `"cpu"` in `my_submission/submission.json`.
- **Cold-Run Per-Case Latency:**
  - `DEMO-001` (2 pages): ~28 ms (`assess`), ~1.05 s total cold worker subprocess wall time.
  - `USGS-SDG-012` (24 pages): ~1,022 ms (`assess`), ~2.08 s total cold worker subprocess wall time.
  - `USGS-SDG-040` (22 pages): ~888 ms (`assess`), ~1.81 s total cold worker subprocess wall time.
  - `USGS-SDG-061` (52 pages): ~2,410 ms (`assess`), ~3.47 s total cold worker subprocess wall time.
  - All runs execute ~50x–150x faster than the 180,000 ms (3-minute) per-case timeout budget.

## 2. Offline & Air-Gapped Determinism
- Zero external HTTP/API calls, zero runtime downloads, and full compatibility with `HF_HUB_OFFLINE=1` and `TRANSFORMERS_OFFLINE=1`.
- Uses deterministic Okapi BM25 + morphological stem/phrase retrieval (`numpy` + Python stdlib) and rule-grounded evidence adjudication (`models: []` in `submission.json`, `no_team_training: true` in `declaration.json`).
- LightGBM in `packages/ml_inference` is made optional with a NumPy ridge fallback regressor so the codebase runs cleanly inside `apctt-base-9e7fe1324bb6` without unapproved wheel dependencies.

