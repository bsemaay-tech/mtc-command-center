# Intake Inventory Diff vs First Run

- Audited valid intake count: 56
- First-run valid count (best-effort parse, schema may differ): 73
- User expectation reference: ~66 — actual valid intake count differs because the inbox holds 90+ structured reports across two date cohorts (15 QL_*.md at root for 2026-05-01 + 50+ in `3 Mayıs/` subfolder for 2026-05-03). Not an error.

## Counts by classification (audited)
- DUPLICATE_STRATEGY: 30
- DUPLICATE_VIDEO_ID: 1
- EMPTY_OR_CORRUPT: 3
- RAW_TRANSCRIPT_BY_MISTAKE: 65
- UNKNOWN: 4
- VALID_INTAKE_REPORT: 56

## Skipped raw transcripts under `Transcrips/`
Count: 65 — correctly skipped per spec (raw transcripts are secondary reference only).