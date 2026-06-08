# RESULT_NIGHT_1M_MCC_TAIL_codex

Date: 2026-06-08
Model: Codex GPT-5

## Scope

Finish the remaining `night_1m_2026-06-07` MCC visibility work without changing trading, Pine, parity, or strategy behavior.

## Findings

- The run root `03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/` is an overnight container, not a direct MEGA result run.
- `SUMMARY_night_1m_2026-06-07.md` identifies `iter_05` as the final validation source.
- `iter_05` already had MEGA, CPCV/PBO, evaluation artifacts, and Gate2 scorecards, but lacked Gate3 and final `scorecard_v2`.
- `scorecard_reader.py` only scanned one directory level below `05_BACKTEST_RESULTS`, so nested scorecard runs such as `night_1m_2026-06-07/iter_05/scorecard_v2` were invisible even after tail completion.

## Work Done

- Ran `mcc_night_tail.sh` on `night_1m_2026-06-07/iter_05` using bundled Python via `MCC_PYTHON`.
- Added recursive scorecard run discovery to `08_DASHBOARD_APP/apps/api/mcc_readonly/scorecard_reader.py`.
- Added `tests/test_scorecard_reader.py` to lock nested `scorecard_v2` discovery.

## Result

- `iter_05` artifact counts:
  - `cpcv15`: 2
  - `pbo`: 2
  - `evaluation_artifacts`: 122
  - `gate2_scorecards`: 122
  - `all_gate`: 122
  - `all_gate_g3enriched`: 122
  - `gate3_scorecards`: 122
  - `scorecard_v2`: 122
- `build_scorecards()` now reports 715 total cards, 18 runs, 46 distinct strategies.
- `night_1m_2026-06-07` contributes 122 v2 scorecards from `iter_05`.
- Promotable count for this night run: 0.

## Validation

- `python -m py_compile MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/scorecard_reader.py`: PASS
- `python -m unittest tests.test_scorecard_reader` from `apps/api`: PASS
- `python -m unittest discover -s tests` from `apps/api`: 36 tests PASS
- Real-data scorecard smoke: `night_cards=122`, `versions=['v2']`, `promotable=0`

## Notes

- The legacy `mcc_night_tail.sh` final `dashboard visible: NO` line still checks an older backtest-reader path, not the dashboard scorecard reader. The API scorecard reader smoke is the authoritative verification for this task.
- No Pine, MTC_V2, parity, or trading logic files were changed.
