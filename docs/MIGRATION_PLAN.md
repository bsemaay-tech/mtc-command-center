# Migration Plan

## Target Structure
`C:\LAB\Tradingview_LAB_CLEAN` remains conceptual until Phase 1 approval. It will contain root AI stubs, `docs`, and `MTC_COMMAND_CENTER` with `_AI_MEMORY`, `01_MTC_PROJECT`, `02_MTC_BACKTEST`, `03_QUANTLENS`, `04_SHARED`, and `99_ASSETS`.

## Source-of-Truth Rules
- Source-of-truth: legacy `C:\LAB\tradingview-lab\MTC_COMMAND_CENTER` is canonical and should be copied byte-for-byte to the clean `MTC_COMMAND_CENTER` after approval.
- `01_MASTER TEMPLATE_V2\MTC_V2_PORTABLE_HANDOFF` is not canonical when byte-identical duplicates exist; it should be used as handoff/archive input and condensed into AI memory.
- Duplicate files such as `Agents.md`, `Claude.md`, and `SETUP_WINDOWS.md` between V2 and portable handoff should resolve to the V2/current command-center version unless hashes prove the portable copy is uniquely newer.
- `external\traderspost-command-dash` and `MTC_COMMAND_CENTER\08_DASHBOARD_APP` require a Phase 0B relation check before either is treated as canonical dashboard code.

## Phase Plan
- Phase 0: audit and planning only.
- Phase 0B: deeper conflict/detail audit only if Barış replies `APPROVE_PHASE_0B_DETAIL`.
- Phase 1: create clean repo and copy approved files only after `APPROVE_PHASE_1_MIGRATION`.
- Phase 2: validate and clean after Phase 1 review.

## Copy Rules
- `MTC_COMMAND_CENTER` is copied byte-for-byte as canonical source after approval.
- `.pine`, parity reference files, and `MIGRATE_AS_IS` files require pre/post SHA256 comparison.
- No formatting, encoding normalization, line-ending conversion, or trading behavior change is allowed.

## Exclusion Rules
- Exclude unrelated projects and generated/cache folders automatically.
- Exclude old V1 unless Barış explicitly requests archive material.

## Classification Rules
- Last commit older than 180 days and no reference signal: `EXCLUDE_OUTDATED`.
- Last commit within 90 days and reference/import signal: `ACTIVE_KEEP`.
- `.pine` files: `MIGRATE_AS_IS`.
- Generated/cache folders: `EXCLUDE_GENERATED`.
- Only real ambiguity remains `NEEDS_BARIS_DECISION`.

## Conflict Rules
- Prefer canonical current `MTC_COMMAND_CENTER` over older duplicates.
- Use V2/portable handoff duplicates only as archive or memory source unless uniquely newer.
- Do not decide `external\traderspost-command-dash` vs `MTC_COMMAND_CENTER\08_DASHBOARD_APP` without Phase 0B relation check.

## Future `apply_migration.ps1` Plan
- Copy only approved files from an approved manifest.
- Preserve byte-level content.
- Exclude generated/cache/unrelated folders.
- Produce copy and hash manifests.

## Future `verify_migration.ps1` Plan
- Verify target structure, AI memory files, root stubs, absence of excluded folders, file counts/sizes, and checksums.
- Verify no Pine/parity/MTC behavior files changed.
- Verify legacy repo remains untouched.

## Rollback Plan
Delete or rename the clean target. Legacy remains intact.

## Approval Gates
- No target creation before `APPROVE_PHASE_1_MIGRATION`.
- No path rewrites before explicit approval.
- No Phase 2 before Phase 1 review.
