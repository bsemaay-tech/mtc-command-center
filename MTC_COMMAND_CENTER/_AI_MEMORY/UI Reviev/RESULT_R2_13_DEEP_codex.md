# RESULT_R2_13_DEEP_codex

Date: 2026-06-08
Model: Codex GPT-5

## Scope

Add short per-sub-score "why points were deducted" explanations without changing scoring math.

## Work Done

- `scorecard_reader.py` now normalizes gate `sub_scores`:
  - adds `max_points` from existing `points_max` when needed
  - adds `deduction_reason` when absent
- `app.js` gate detail rows now show metric, value, points, and the short reason.
- `test_scorecard_reader.py` now asserts nested scorecard discovery plus sub-score reason normalization.

## Validation

- `python -m py_compile mcc_readonly/scorecard_reader.py`: PASS
- `python -m unittest tests.test_scorecard_reader`: PASS
- `python -m unittest discover -s tests`: 39 tests PASS
- `node --check MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/app.js`: PASS
- Real scorecard smoke: 73,645/73,645 sub-scores have `deduction_reason`; 73,645/73,645 have `max_points`.

## Notes

- No scoring, threshold, Pine, MTC_V2, parity, backtest engine, or trading behavior changed.
- Reasons are explanatory metadata derived from existing sub-score status/points.
