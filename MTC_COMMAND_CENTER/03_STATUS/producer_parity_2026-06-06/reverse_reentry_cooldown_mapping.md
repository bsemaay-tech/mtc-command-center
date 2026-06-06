# Reverse / Re-entry / Cooldown Mapping Evidence

Generated: 2026-06-06 by Codex GPT-5.

Scope: `QL_FAM_MOMENTUM_CONTINUATION|TRXUSDT|4h` producer-level Gate3 evidence.

## Mapping

- The QuantLens momentum-continuation producer emits raw long entries only and always emits `raw_short=false`; reverse logic is therefore not producer-owned for this family.
- `MTCRunner` owns position lifecycle after raw signals. The runner has explicit config-driven paths for `allow_flip`, pending opposite entries when flip is disabled, same-bar re-entry after exits, signal-mode cooldown, cooldown guard blocking, and single-position/pyramiding constraints.
- The MEV run uses `strategy.pyramiding=1` and MTC single-position behavior. The producer does not add pyramiding, exits, stops, cooldown, or broker lifecycle logic.

## Code Evidence

- `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/mtc_runner.py`:
  - config guard rejects unsupported `strategy.pyramiding != 1` and `same_bar_reentry_max_per_bar != 1`.
  - cooldown guard path emits `cooldown_guard`.
  - pending queue handles opposite raw edges when `allow_flip=false`.
  - same-bar re-entry gate is config-driven and separates exit reason from fresh entry.
  - in-position/no-add-on blocks prevent accidental pyramiding when the config does not allow it.
- `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/config/defaults.py`:
  - exposes `allow_flip`, `max_pyramid_positions`, `signal_mode_cooldown_bars`, `allow_same_bar_reentry`, `same_bar_reentry_requires_exit`, and `same_bar_reentry_max_per_bar`.

## Test Evidence Attempt

Focused engine tests exist for the lifecycle controls:

- `tests/test_opp_signal_same_bar_flip.py`
- `tests/test_pending_queue.py`
- `tests/test_runner_daily_and_mae_guards.py`
- `tests/test_same_bar_reentry_and_capital_guard.py`
- `tests/test_runner_config_guards.py`

Command run:

```powershell
python -m pytest tests\test_opp_signal_same_bar_flip.py tests\test_pending_queue.py tests\test_runner_daily_and_mae_guards.py tests\test_same_bar_reentry_and_capital_guard.py tests\test_runner_config_guards.py -q
```

Result: 16 passed, 5 failed.

Failing tests:

- `tests/test_pending_queue.py::test_pending_queue_opens_opposite_after_flat_when_allow_flip_false`
- `tests/test_runner_daily_and_mae_guards.py::test_time_stop_eod_closes_position_at_day_boundary`
- `tests/test_runner_daily_and_mae_guards.py::test_time_stop_eow_closes_position_at_week_boundary`
- `tests/test_runner_daily_and_mae_guards.py::test_consec_loss_reset_daily_allows_new_day_entry`
- `tests/test_runner_config_guards.py::test_runner_rejects_non_enforced_trade_limits[trade.max_pyramid_positions-2]`

Because this lifecycle test set is not clean, this evidence does **not** support clearing `reverse_reentry_cooldown_mappable` to OK. The readiness artifact must keep that field non-OK until engine lifecycle behavior is repaired or a narrower approved mapping proof is defined.

## Limit

This does not approve live trading and does not prove broker fill behavior. It shows why the producer should not own reverse/re-entry/cooldown logic, but the current engine lifecycle evidence is insufficient for a Gate3 pass.
