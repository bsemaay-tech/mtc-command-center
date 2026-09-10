# MTC build handoff

## Current state — 2026-08-25

- WP-P0-05 makes no Pine, Python strategy, parity, or MTC behavior change.
- Last carried local status: cases 110, 111, 134, 153, and 154 passed PineTS/Python; case 163 still
  needs a TradingView export; cases 134/153 need fresh exports; cases 160/161 are missing exports.
- Treat those statements as dated 2026-05-29 until re-executed; they are not current PASS evidence.
- Next authorized MTC task must name exact cases/files and explicitly approve any protected change.

## [Claude lane C] 2026-09-06 — seed-region YAML files parse again (D3)

- Changed: `tools/extract_parameter_library_seeds.py` now emits the research warning as a
  `# ` comment in `write_seed_regions`/`write_rejected` (the Markdown report writer is untouched);
  line 2 of the 7 affected `optimization/parameter_library/**/*.yml` files got the same `# ` prefix.
  No key or numeric value changed; no Pine/MTC_V2/parity file touched.
- Evidence: RED — 7/8 files failed `yaml.safe_load` ("mapping values are not allowed here", line 4);
  GREEN — all 8 parse; writer output from a scratch `write_seed_regions`/`write_rejected` call parses.
  No tracked code consumer loads these files as YAML (grep); job specs only reference them by path.
- NEXT ACTION: none for this defect; a real extractor run remains unauthorized.
- WAITING FOR OWNER: Nothing.
## [P012 continuation] 2026-09-10 17:19 UTC - accepted R32 bounded correction ready for CI

Lead bounded acceptance completed at 16:56 UTC for source `ddfb30e2d605cec3b8154527270d019ac04333ed` from `C:/tmp/P0R32V`; packet `C:/tmp/P0R32W` includes the preserved T/U evidence. This accepts only the bounded correction, not full P012 or production. The current continuation repository is branch `feature/p012-astra-continuation-20260910` at `0508ce5775767f64fe9dbd6e5ad53a5b6463a339`, tracked clean at preparation.

- R1: Lead reproduced GREEN exit 0, intentional RED exit 1, and full gate exit 0 with 495 passed / 0 failed.
- R2-R3: Sol S5 PASS-WITH-NITS accepted the whole bounded correction; Opus O3 PASS-WITH-NITS accepted within its recorded limits; Gemini 3.7 successor guard passed and returned guarded PASS. S4 timed out without a verdict. S5's first invalid-cache receipt remains preserved beside the corrected passing receipt (495 passed / 0 failed).
- Windows execution used the existing stronger elevated sandbox plus the 15-byte temporary-directory repair and forward cache. No bypass occurred.
- R4: exact-current-head protected CI, PR integration, and normal merge remain pending under existing authority. No push, PR, or merge was performed here.
- R5-R7: all ten Section 19 closure-evidence items are accepted, while 27 production risks and five integration obligations remain. Full production is unaccepted. HIST0029 receipt redo, capture, deferred work, refusals, and real human review remain required in their recorded scopes.
- Scheduling policy: Lead acceptance follows Opus/Sol/Gemini R2 accepting reviews. Policy commit `87bf895` has completed required review and remains separate and not installed; protected integration and global pointer installation remain pending.

Local-only production checklist and next-actions material was prepared but is not a public-repository deliverable. No account facts, quotas, private financial metadata, or C10 observations are included in this writeback.

NEXT ACTION: Run exact-current-head protected CI and complete authorized PR integration without bypass.

WAITING FOR OWNER: Nothing.
