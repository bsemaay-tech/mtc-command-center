# 12_PARITY_PINETS — migrated parity artifacts

Migrated 2026-07-05 (Barış approval, audit follow-up Q6) from the frozen legacy repo path
`C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\05_PARITY` (731 files, ~19 MB, byte-for-byte copy —
originals untouched). The dashboard `pinets_root` in `00_CONFIG/paths.local.json` now points here,
so the clean repo no longer depends on the frozen repo for parity status.

Treat contents as **protected parity evidence** (see `_AI_MEMORY/DO_NOT_TOUCH.md`): read-only,
no edits without explicit Barış approval. `parity_reader.py` consumes
`parity_results.json` / `_nightly/parity_results.json` from this root.
