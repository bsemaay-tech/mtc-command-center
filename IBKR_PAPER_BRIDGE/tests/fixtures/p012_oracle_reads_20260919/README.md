# P012 oracle reads — FIXTURE SELECTION (not a real admission record)

Byte-exact copies of completed outputs of the Lead-owned oracle reader run
`C:/tmp/CLAUDE_P0_RUN_20260913/P012_ORACLE_CAPTURE_20260919/reads/`, vendored so
`test_capture_oracle_at_funding.py` can verify real bytes offline. Precedent:
`tests/fixtures/p012_path1_r2_capture/`.

## What this directory is NOT

- **Not** a new real admission record and **not** an accepted economic record. It admits nothing.
- **Not** a replacement for the reader's own directory. Copying here never altered, trimmed, locked
  or re-hashed the source; the source manifest still carries all of its rows.
- `ORACLE_READS_MANIFEST.jsonl` here is a **subset** of the reader's manifest — a *fixture
  selection*. `FIXTURE_SELECTION.json` carries the same rows plus, per row,
  `_fixture_source_line` = the 1-based line of that row in the original manifest, so every row can
  be traced back to the original evidence.

## Origin

| | |
|---|---|
| Source directory | `C:/tmp/CLAUDE_P0_RUN_20260913/P012_ORACLE_CAPTURE_20260919/reads/` |
| Source manifest | `ORACLE_READS_MANIFEST.jsonl` (12 rows at copy time; the reader was still running) |
| Selected hours | `H20260919T150000Z`, `H20260919T160000Z` (18:00 / 19:00 UTC+3) — the two complete brackets named by G2 §10 |
| Selected rows | original manifest lines 1-6 |
| Copied | 2026-09-19, by the P012 O-1 Phase-A implementer |

Only **completed, immutable** reads were taken. Hours the reader had not finished were left alone.

## Copied files and independently verified digests

Each file's SHA-256 was measured here from the copied bytes and equals both the `.sha256` sidecar and
the manifest `sha256`; the byte length equals the manifest `bytes`.

| Line | File | sha256 | bytes |
|---|---|---|---|
| 1 | `H20260919T150000Z_pre_metaAndAssetCtxs.json` | `cac54ab01162ced997db2be4bdd510071399d074e7cbf8ad4c9376240bdc01d4` | 72350 |
| 2 | `H20260919T150000Z_post_metaAndAssetCtxs.json` | `afa49abca2239f5b042b2b01bd55eef09d5b1791b60960e10063e69f9ef7a9c4` | 72266 |
| 3 | `H20260919T150000Z_state_clearinghouseState.json` | `8e6ead7ff2aa55f8fd5f51a30791df294e554f95f7bc4491deefe38b6f01508a` | 710 |
| 4 | `H20260919T160000Z_pre_metaAndAssetCtxs.json` | `b1db9643a05b04e3...` (see sidecar) | 72460 |
| 5 | `H20260919T160000Z_post_metaAndAssetCtxs.json` | `9cdf68edafa912ec...` (see sidecar) | 72293 |
| 6 | `H20260919T160000Z_state_clearinghouseState.json` | `f04d55884bb7d707...` (see sidecar) | 709 |

The `.sha256` sidecars are the authoritative per-file digests and are copied verbatim.

## Capture times (host wall clock — the limitation that never goes away)

| Hour | `pre` interval | `post` interval | `oraclePx` pre / post |
|---|---|---|---|
| `2026-09-19T15:00:00Z` | 14:59:58.000 → 14:59:58.589 | 15:00:02.001 → 15:00:02.907 | `81581.4` / `81581.4` |
| `2026-09-19T16:00:00Z` | 15:59:58.000 → 15:59:58.571 | 16:00:02.00x → 16:00:02.xxx | `81636.0` / `81628.0` |

**`started_utc`/`ended_utc` are the reader host's Windows wall clock, not the venue's**, exactly as
the manifest's own `clock` field states. These are bracketing observations of a public endpoint.
They **do not** identify the price the venue used at settlement: the official funding page documents
the formula but publishes no per-event settlement-oracle price and no immutable pointer
(`C:/P012_PUBLIC_DOCS_20260919/FINDINGS.md` Q1, F-19 still open). Nothing in this directory may be
read as a settlement oracle.

The `state` rows are a **position witness for context only**. A position witness is not a funding
event and never substitutes for a `userFunding` row.

## Use in tests

Rejection classes are exercised on **modified copies written into `tmp_path`** — one change at a
time. The bytes in this directory are never mutated in place.
