# Validation Report

| check | status | evidence |
|---|---|---|
| py_compile | PASS | python -m py_compile python_signal_model.py mtc_compatible_risk_adapter.py python_visual_backtest_harness.py exited 0 |
| pytest | PASS | python -m pytest -q: 6 passed |
| debug CSV export | PASS | outputs/signals_debug.csv, outputs/trades_debug.csv, outputs/equity_debug.csv created from synthetic sample |
| Pine file exists | PASS | standalone_pine_visual_review.pine has Pine v6, standalone strategy(), no request.security, no alerts |
| MTC_V2.pine untouched | PASS | no diff entry |
| production runner untouched by this sandbox | PASS_PREEXISTING_DIFF_UNCHANGED_IN_STATUS | runner diff was already present before sandbox; before count=2 after count=2 |
| git status before/after | PASS | git_status_before.txt and git_status_after.txt captured |

No strategy optimization or profitability backtest was run. Debug trades are marker/exit inspection only.
