# Claude Handoff

- Version: `2026-05-29`
- Scope: `MTC V2` only
- Source of truth:
  - `03_DOCS/MTC_V2_ARCHITECTURE.md`
  - `03_DOCS/HANDOFF.md`  ← start here
  - `03_DOCS/RUNBOOK.md`

## Current State

- `case_110`, `case_111`, `case_134`, `case_153`, `case_154`: all PineTS/Python PASS as of 2026-05-29.
- L22 `candle_pattern_lookback`: AUTO_061 PineTS/Python PASS. TW export for `case_163` still pending.
- `case_134` / `case_153`: PineTS/Python PASS; need fresh TW re-export (stale 2026-04-14 exports).
- `case_160` / `case_161`: MISSING_EXPORT.

## Active Backlog (priority order)

1. TW export for `case_163` (L22 candle pattern gate)
2. TW re-export for `case_134` / `case_153`
3. TW export for `case_160` / `case_161`
4. Range Filter optimization smoke run

## Notes

- No file is permanently untouchable; edit/delete intentionally when the task requires it.
- Do not commit generated report trees unless a specific evidence refresh is requested.
- Do not commit root-level parity bridge outputs (`data/mtc_signals.json`, `data/pine_trades.*`, `reports/*.json`).
- `MTC_V2_PORTABLE_HANDOFF/` is tracked in git; update intentionally when stale.
- `mtc_backtest/` is legacy — not the parity target for MTC V2 work.
