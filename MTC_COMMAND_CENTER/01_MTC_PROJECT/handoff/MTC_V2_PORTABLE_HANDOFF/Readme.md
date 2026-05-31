# MTC V2 Portable Handoff

This tracked package is a portable continuation workspace for MTC V2 code, docs, parity factory, reference oracle, and optimization POC work.

## Current State - 2026-05-29

- Synced after commits `096c35c9`, `4af32d71`, `64e774c6`, and `b55068e9`.
- Range Filter local feature parity and independent reference oracle are green.
- Factory regression summaries now surface hidden lifecycle failures with `internal_fail_count` and `no_internal_failures`.
- Range Filter optimization POC seed regions and smoke job are included.
- `case_163` L22 Candle Pattern Lookback exists in the main repo, but TradingView XLSX audit exports are intentionally outside this main portable package.
- Legacy `mtc_backtest/parity_suite_350/tv_manual_inputs` was removed from the main repo and should not be treated as live data.

## Start Here

1. `03_DOCS/CLAUDE_CODE_HANDOFF_2026-05-29.md`
2. `03_DOCS/HANDOFF.md`
3. `03_DOCS/MTC_V2_ARCHITECTURE.md`
4. `03_DOCS/RUNBOOK.md`
5. `docs/PORTABLE_HANDOFF_PACKAGE_SCOPE.md`

Generated reports, caches, virtual environments, node_modules, and TradingView XLSX audit archives are excluded from this main portable package.
