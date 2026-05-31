# RUNBOOK

This file is the practical command reference for current MTC_V2 parity work.

## Canonical Boundary
- Pine: `01_MASTER TEMPLATE_V2/01_PINE/MTC_V2.pine`
- Python: `01_MASTER TEMPLATE_V2/00_PYTHON/mtc_v2/*`
- Default execution direction: `close_only_deterministic_v2`
- Legacy explicit-only profile: `raw_close_only_v1`
- `mtc_backtest/` is not the current parity owner

Session start reading order:
1. `03_DOCS/HANDOFF.md`
2. `03_DOCS/DEV_LOOP.md`
3. `03_DOCS/MTC_V2_ARCHITECTURE.md`
4. `05_PARITY/MTC_V2_TW_EXPORT_CASE_TRACKER.xlsx`
5. `05_PARITY/MTC_V2_TW_EXPORT_CASE_SUITE_V2.csv`

## Primary Command
Preferred full-year parity run:

```bash
python parity_compare.py --fetch-fresh --start 2025-01-01 --end 2025-12-31
```

This runs:
1. `node mtc_bridge.mjs`
2. `python pine_trades.py`
3. Python runner on the exact PineTS bars
4. PineTS vs Python comparison

## Tracker Case Run
```bash
python parity_compare.py --fetch-fresh --tracker-case CASE_ID
```

Rules:
- Use `--tracker-case` for tracker-owned cases.
- Do not mix tracker rows with unrelated manual overrides unless explicitly doing research.

## Manual TradingView XLSX Audit
TradingView export is a frozen oracle workflow, not the daily loop.

Contract:
- `Properties` sheet is source of truth.
- `manual_tw_futures_audit.py` rebuilds the shared config from workbook properties.
- Workbook `Properties > Symbol` and `Properties > Timeframe` must drive the local PineTS/Python `--symbol` and `--tf`; do not accept a local PASS on a different symbol/timeframe.
- PineTS and Python run on that same workbook-derived config.
- `List of trades` is the trade and outcome oracle.
- No legacy hidden overrides.
- No silent fallback when workbook properties are insufficient.

Required order for each export case:
1. verify workbook settings
2. verify local run symbol/timeframe matches workbook symbol/timeframe
3. verify expected trade-count and outcome effect versus baseline or the relevant previous case
4. run parity
5. update tracker

Margin rule:
- `TV Margin % = 100 / max_leverage_cap`
- Pine input `Max Lev` does not by itself change TradingView Strategy Tester margin; workbook `Properties` must show matching margin.

Examples:
- `Max Lev = 5 -> Margin = 20%`
- `Max Lev = 100 -> Margin = 1%`

Preferred single-file audit:

```bash
python "01_MASTER TEMPLATE_V2/05_PARITY/manual_tw_futures_audit.py" --xlsx-path "FULL_PATH_TO_WORKBOOK.xlsx" --case-name case_XXX --chart-timezone UTC+3
```

## Optional Lifecycle Audit
Use only for representative divergence debugging:

```bash
python "01_MASTER TEMPLATE_V2/05_PARITY/manual_tw_lifecycle_audit.py" --cases case_001 case_039 case_040 case_044 case_045 --chart-timezone UTC+3
```

## Main Artifacts
- `data/mtc_signals.json`
- `data/pine_trades.json`
- `data/parity_input_from_pinets.csv`
- `reports/parity_compare.json`
- `reports/parity_trade_report.csv`
- `reports/python_trades_v2.csv`
- `reports/parity_effective_config.json`
- `05_PARITY/MTC_V2_TW_EXPORT_CASE_TRACKER.xlsx`
- `05_PARITY/MTC_V2_TW_EXPORT_CASE_SUITE_V2.csv`

## PASS Criteria
- Trade count matches
- Entry and exit times match
- Entry and exit prices are within tolerance
- Qty matches or is within the accepted contract if evaluating soft pass
- `reports/parity_compare.json` verdict is consistent with the intended contract

## MISMATCH Triage
1. Read the first mismatch in `reports/parity_trade_report.csv`.
2. Check `reports/python_trades_v2.csv`.
3. Confirm effective config in `reports/parity_effective_config.json`.
4. If workbook-based, re-check the export settings first.
5. Fix semantic owner drift in Pine or Python.
6. Re-run parity.

## Session End Rule
At session end, update only what matters:
- `HANDOFF.md`
- tracker workbook
- directly relevant suite files if the observed case definition changed
## 12h Seed Extraction Resume Result Rule

- For `reports/optimization/12h_backtesting_session/`, do not assume `ranked/all_evaluations.csv` is cumulative after a resumed run.
- The 2026-05-01 resume completed the full registry (`378,000 / 378,000`) but the current ranked CSV contains the latest process slice (`95,745` rows).
- Use `reports/optimization/12h_backtesting_session/reports/RESUME_DEDUP_REPORT.md` and `resume_registry.sqlite` for completion status.
- Before final global seed decisions, regenerate a cumulative ranking from all completed worker result artifacts or a cumulative export.
- Keep final seed reporting split into high-average-return and defensive/worst-split views.
