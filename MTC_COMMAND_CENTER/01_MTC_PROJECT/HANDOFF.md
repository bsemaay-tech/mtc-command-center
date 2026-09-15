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

## R35 current review closeout — 2026-09-11

This current checkpoint supersedes earlier P012 price-policy prebuild and R35 review-pending status. R34 PR176 was merged at e42fa192507d77e2d1765702a4a9f54e56ad793f. The owner ratified the completed R35 correction with "Approved, continue" and conditionally authorized integration after the required checks.

Fresh exact Opus 5 xhigh and native gpt-5.6-sol xhigh returned PASS-WITH-NITS on a593b29dca30c45bb8c183db04429e29d9b86e27. Each executed 558 full-gate checks and 113 focused tests successfully; Lead independently reproduced them. Gemini 3.7 completed mandatory supplementary corroboration without execution. Lead accepts the bounded correction with disclosed residual risks; protected current-head CI and normal merge remain pending at this checkpoint. Native Sol is an independent native review, not another subscription CLI worker.

Original reports, hashes, Lead reconciliation, the exact full-gate result, and source proof are in MTC_COMMAND_CENTER/04_REPORTS/ai_handoffs/P012_RECORD_PROSE_R35_REVIEW_20260911/. The closeout changes only those eight evidence files and these two status notes; the reviewed mtc_v2 tree must remain identical to a593. No executable core or economic scalar change; all 27 risks, 10 production OPEN rows, null-field production refusals and deferred R29 remain. Additional authorized support questions are NOT_SENT because the browser tool failed to load its request-header policy. No full P012 or production acceptance is claimed.

NEXT ACTION: normal guarded closeout commit, push the owned feature branch, verify protected CI on the up-to-date PR head, then normal merge under existing owner authority. Record actual integration identifiers in the final R35 integration receipt.

WAITING FOR OWNER: Nothing for R35.
