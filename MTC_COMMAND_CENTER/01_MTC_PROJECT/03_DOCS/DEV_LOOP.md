# DEV_LOOP

## Goal
Current MTC_V2 development is parity-first.

- Pine owner: `01_MASTER TEMPLATE_V2/01_PINE/MTC_V2.pine`
- Python owner: `01_MASTER TEMPLATE_V2/00_PYTHON/mtc_v2/*`
- Layer order owner: `03_DOCS/MTC_V2_ARCHITECTURE.md`, `Layer Order`

Never move to the next layer while parity is broken.

## Mandatory Files Before Work
1. `03_DOCS/HANDOFF.md`
2. `03_DOCS/DEV_LOOP.md`
3. `03_DOCS/RUNBOOK.md`
4. `05_PARITY/MTC_V2_TW_EXPORT_CASE_TRACKER.xlsx`
5. `05_PARITY/MTC_V2_TW_EXPORT_CASE_SUITE_V2.csv`
6. `reports/parity_compare.json` if the last run matters

## Continuity Rule
- No agent should rely on chat memory when the docs and tracker already exist.
- Before stopping, always update:
  - `03_DOCS/HANDOFF.md`
  - `05_PARITY/MTC_V2_TW_EXPORT_CASE_TRACKER.xlsx`
  - any directly relevant suite or parity files

## Standard Development Loop
1. Read `HANDOFF.md`.
2. Confirm target layer from architecture section `9`.
3. Run current baseline:
   - `python parity_compare.py --fetch-fresh --start 2025-01-01 --end 2025-12-31`
4. If baseline is not `PASS`, stop feature work and fix parity first.
5. Implement the feature in Pine.
6. Implement the same feature in Python.
7. Run parity again.
8. If mismatch exists, inspect:
   - `reports/parity_trade_report.csv`
   - `reports/python_trades_v2.csv`
   - `reports/parity_effective_config.json`
9. Fix semantic drift.
10. Only after parity is stable, move to the next layer.

## Manual TradingView Export Loop
TradingView export is audit-oracle work, not the daily dev loop.

If a user provides or requests an export case:
1. Read the workbook.
2. Treat `Properties` as source of truth.
3. Compare the observed export against baseline or the relevant previous case.
4. Decide whether the changed setting produced the expected:
   - trade-count effect
   - outcome effect
5. Only then run parity.
6. Update tracker and handoff.

## Tracker Rule
- Tracker owner:
  - `05_PARITY/MTC_V2_TW_EXPORT_CASE_TRACKER.xlsx`
- Suite mirrors:
  - `05_PARITY/MTC_V2_TW_EXPORT_CASE_SUITE_V2.csv`
  - `05_PARITY/MTC_V2_TW_EXPORT_CASE_SUITE_V2.json`
- Tracker rows should only be updated when PineTS and Python were run on the same observed case inputs.
- Export-faithful tracker updates must use the actual latest workbook in the case folder.

## Current Baseline
- Current refreshed observed baseline workbook:
  - `TW_EXPORT_CASES_V2/case_001/MTC_V2_BINANCE_BTCUSDT.P_2026-04-05_f6b77.xlsx`
- Working observed settings:
  - `Max Lev = 5`
  - `SL Mode = ATR`
  - `Margin long/short = 20% / 20%`

## Current Focus
- Drift-only cases are lower priority.
- Main active engineering targets are HTF lifecycle mismatches:
  - `case_039`
  - `case_040`
  - `case_044`
  - `case_045`

## Session Close Rule
Before stopping, write only the essentials:
- current parity verdict
- remaining mismatch
- next exact task
- tracker status changes

If that is missing, the session is not handoff-safe.
