# DISPOSITION_FIX2

Lane P14FIX2G (Grok). Input audit: `C:/tmp/CLAUDE_P0_RUN_20260913/laneGKP14B_grok_audit/GROK_P14B_REPORT.md`. Scope unchanged: exactly Q-A and Q-B; fixture data only; read-only; no product code. Nothing here is a decision, acceptance, or authorization.

| # | severity | disposition FIXED / REBUTTED (with evidence) | what changed (file:line) |
| --- | --- | --- | --- |
| prior-9 | CORRECTION | FIXED | P014_READONLY_REPORT.md:19 now cites the executable json_extract command that returns 1/1/1; reproduce_report.py:312 is the SQL executed at reproduce_report.py:321; reproduce_report.py:371 prints that command; REPORT.md:33 pastes live stdout |
| new-1 | CORRECTION | FIXED | Same event-count command defect as prior-9. P014_READONLY_REPORT.md:19 cites `SELECT json_extract(canonical_event, '$.next_state') AS next_state, COUNT(*) FROM lifecycle_events GROUP BY 1` on `file:C:/tmp/P014_RO_20260914/fixture-ledger.sqlite?mode=ro`; reproduce_report.py:329 uses that query; old `SELECT next_state, COUNT(*) FROM lifecycle_events GROUP BY next_state` removed |
| new-2 | CORRECTION | FIXED | P014_READONLY_REPORT.md:85 now cites trial_catalog.py:75 (`RESERVED_BOUNDARY_KEY = "RESERVED_BOUNDARY_KEY"`); :76 is blank |
| new-3 | NIT | FIXED | P014_READONLY_REPORT.md:3 is the first paragraph and now contains recorded `accepted=false` (P031_M1_SCOPE_AND_STATUS.md:718), `authoritative: false` (fixture-status-report.json:10), and the START_HERE.md:54 sequencing quote |
