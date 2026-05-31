# Decisions and Decision Requests

## Approved Decisions
- D001: Phase 0 is audit and planning only.
- D002: The only Phase 0 write location is `C:\LAB\MIGRATION_PLANNING_DRAFTS\Tradingview_LAB_CLEAN_PHASE0`.
- D003: Do not create `C:\LAB\Tradingview_LAB_CLEAN` during Phase 0.
- D004: Do not edit or create temporary files in `C:\LAB\tradingview-lab`.
- D005: Exclude `SECONDBRAIN`, `SECONDBRAIN_TEMP`, and `BUDGET APP`.
- D006: `MTC_COMMAND_CENTER` is canonical source-of-truth for the clean command center.
- D007: Pine/parity/backtest `MIGRATE_AS_IS` files require byte-level preservation and checksum verification.
- D008: QuantLens STG folders must represent one real strategy, not pipeline buckets.

## Unresolved Questions

### Q001: Git Strategy
- Options: A) fresh git init; B) preserve selected history; C) keep clean folder outside git until manual review.
- Recommended answer: A.
- Risk: Wrong choice either loses useful history or imports old noise.
- Required Barış response: Choose A, B, or C.

### Q002: Dashboard Canonical Source
- Options: A) `MTC_COMMAND_CENTER\08_DASHBOARD_APP`; B) `external\traderspost-command-dash`; C) Phase 0B relation audit first.
- Recommended answer: C.
- Risk: Choosing wrong dashboard source can migrate stale app code.
- Required Barış response: Choose A, B, or C.

### Q003: Root Script Placement
- Options: A) `02_MTC_BACKTEST`; B) `04_SHARED`; C) split by dependency role.
- Recommended answer: C.
- Risk: Incorrect placement breaks relative paths.
- Required Barış response: Approve placement rule.

### Q004: QuantLens STG Naming
- Options: A) approve proposed STG table; B) preserve source folder names temporarily; C) manually assign STG IDs.
- Recommended answer: B unless Barış wants stable IDs now.
- Risk: Wrong STG identity pollutes registry.
- Required Barış response: Approve table or provide replacements.

### Q005: Old Memory and Reports
- Options: A) summarize current items only; B) archive all; C) exclude old reports.
- Recommended answer: A.
- Risk: Copying too much defeats the clean workspace objective.
- Required Barış response: Choose A, B, or C.
