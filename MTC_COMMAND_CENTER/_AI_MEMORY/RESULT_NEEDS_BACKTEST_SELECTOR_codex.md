# RESULT_NEEDS_BACKTEST_SELECTOR_codex

Date: 2026-06-08
Model: Codex GPT-5

## Scope

Close W2/N5 as a read-only selector for objective backtest candidates. This does not launch backtests and does not change strategy logic.

## Files

- Script: `03_QUANTLENS/tools/build_needs_backtest_selector.py`
- JSON output: `03_QUANTLENS/05_BACKTEST_RESULTS/NEEDS_BACKTEST_SELECTOR.json`
- Markdown output: `03_QUANTLENS/05_BACKTEST_RESULTS/NEEDS_BACKTEST_SELECTOR.md`
- Test: `08_DASHBOARD_APP/apps/api/tests/test_needs_backtest_selector.py`

## Criteria

- `eligible_for_backtest == true`
- `scorecard_v2` is absent
- `expert_quantlens.decision` is not `SALVAGE`, `GARBAGE`, or `CLOSED_SOURCE_STOP`

## Result

- Current selector output: 89 candidates
- Priority bands: 88 `MEDIUM`, 1 `LOW`
- Expert verdict distribution in selected set: 89 `NEEDS_CLARIFICATION`

## Validation

- `python MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_needs_backtest_selector.py`: PASS
- `python -m py_compile MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_needs_backtest_selector.py`: PASS
- `python -m unittest tests.test_needs_backtest_selector`: PASS
- `python -m unittest discover -s tests`: 39 tests PASS

## Notes

- This is a selector/report only. It does not run MEGA, CPCV, PBO, Gate scorers, parity, Pine, MTC_V2, or live trading.
