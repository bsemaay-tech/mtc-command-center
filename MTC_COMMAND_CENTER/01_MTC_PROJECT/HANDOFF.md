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
## [P012 continuation] 2026-09-10 checkpoint 13:24 UTC - Section16 R32 A5 accepting review exists; ratification pending (measured, no acceptance)

- Lead verified 13:24 UTC: F32 `12a2d49544523e0a8cc643421870ecb30b9bb30c` unchanged; source, seal32, baseline32 re-validated; 495/0 reuse valid. Old-Section16 identity mismatch remains sole full-gate refusal; C32, core unchanged; prior C31/C32 snapshots dated history. 2778 = packet FILES.
- Gemini 3.8 Section16: A4 strict-guard PASS, report rejected (impossible TASK19 citation, wrong prior-baseline citation, unlabeled digests). A5 same P032B source, strict-guard PASS, report PASS: six UNCHANGED, SUCCESSOR_REVIEW_CAN_CARRY_FORWARD, no unresolved items. A5 report SHA `8fba565033c623cc4d987fc3627e6dd86654a5cbee1fc574c13633f4ada90f51`; reviewer report unchanged, copies `outputs/SECTION16_R32_GEMINI_REPORT.md`. A1/A2/A3/A4 failures preserved as history; not all current attempts rejected.
- Independent verification: checker 0; 17 core modules, 6 consumers, 17 inputs, 17 goldens, 34 baseline outputs byte-identical; all cited line bounds valid. ONE disclosed non-blocking manifest input-range imprecision (range begins 2 entries late, includes later contract entries); named 17 fixture pairs verified unchanged; no disposition/authority change.
- UNRATIFIED receipt from actual A5 reasons: 8 measured content identities, 168 hunks/112 paths, exact 30-entry chain through #32; ratified FALSE, not installed. Receipt SHA `e9622b7dc46c706a265b56c4fb0f3f771f474241a6cf69e9d56c0e28dee4c048`.
- Runtime: Pro 22% USED/78% remaining dated 13:03 UTC account-wide; actual Astra x-high log 12:53; Standard configured, Fast OFF unverified. Native Astra ended; direct external CLIs. Claude Opus5 Pro scratch readiness PASS, no full suite. Exact Sol execution still BLOCKED; registered Python 3.13/3.14 plus bundled 3.12.14 do not establish a compatible Sol route; no identical retry/install/security/host change.
- Scope: prior owner decisions and protected roles stand; all ten Section19 closure-evidence items accepted HIST0026 with five residuals separate; strict reviews retained HIST0036, old-overrule history not waiver. No P012 acceptance; production facts, receipt29 FINAL-production redo remain. Worker state is not recorded in this static checkpoint.
- NEXT ACTION: owner ratification -> install actual receipt -> full gate -> exact Opus5/Sol xhigh + Gemini 3.7 audits as execution permits -> authorized integration. Detail: P012_ASTRA_CONTINUATION_20260910.md.
- WAITING FOR OWNER: actual Section16 R32 ratification only; no routine implementation permissions.
