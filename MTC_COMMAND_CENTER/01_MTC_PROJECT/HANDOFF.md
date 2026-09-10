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

## [P012 price policy] 2026-09-10 - approved, in prebuild

- Scheduling policy PR174 already installed.
- R32 bounded correction PR175 integrated (merge 3e86faec); current-head gate 495 passed / 0 failed with provenance MATCH; protected Bridge CI passed.
- Price alignment policy implementation is owner-approved and in prebuild in worktree C:/tmp/P012_PRICE_20260910 (branch feature/p012-price-policy-20260910, base 3e86faec). No full acceptance and no production acceptance.
- A new Section 16 review and genuine owner ratification remain required later.

NEXT ACTION: continue the approved prebuild; run the separate Section 16 review before any acceptance.

WAITING FOR OWNER: Nothing now; later Section 16 ratification only.
