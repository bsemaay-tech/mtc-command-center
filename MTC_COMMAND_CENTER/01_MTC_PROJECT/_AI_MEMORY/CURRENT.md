# CURRENT - MTC V2 Component

Last updated: (set by next session)
Updated by:
Current phase:
Current status:

## Active objective

(set by next session)

## Current blockers

(set by next session)

## Next 3 actions

1.
2.
3.

## Files changed this session

## Warnings

---

## SUPERSESSION NOTICE

Any legacy statement below that conflicts with the current root `AGENTS.md` or `DO_NOT_TOUCH.md` is superseded and must not be followed. The dated facts below are preserved as historical context only — verify before acting on any of them.

## LEGACY SNAPSHOT (2026-05-29) - may be stale; verify before acting

> Source: former `CLAUDE.md` dated 2026-05-29. Preserved as historical context.
> Status of each item below is UNVERIFIED. Do not act on these without checking current state.

- `case_110`, `case_111`, `case_134`, `case_153`, `case_154`: PineTS/Python PASS as of 2026-05-29.
- L22 `candle_pattern_lookback`: AUTO_061 PineTS/Python PASS. TW export for `case_163` was pending.
- `case_134` / `case_153`: PineTS/Python PASS; fresh TW re-export was needed (stale 2026-04-14 exports).
- `case_160` / `case_161`: MISSING_EXPORT as of that date.

### Legacy backlog (unverified - may be done or superseded)

1. [UNVERIFIED LEGACY] TW export for `case_163` (L22 candle pattern gate)
2. [UNVERIFIED LEGACY] TW re-export for `case_134` / `case_153`
3. [UNVERIFIED LEGACY] TW export for `case_160` / `case_161`
4. [UNVERIFIED LEGACY] Range Filter optimization smoke run

### Legacy notes (from 2026-05-29)

- No file is permanently untouchable; edit/delete intentionally when the task requires it.
- Do not commit generated report trees unless a specific evidence refresh is requested.
- Do not commit root-level parity bridge outputs (`data/mtc_signals.json`, `data/pine_trades.*`, `reports/*.json`).
- `MTC_V2_PORTABLE_HANDOFF/` is tracked in git; update intentionally when stale.
- `mtc_backtest/` is legacy - not the parity target for MTC V2 work.
