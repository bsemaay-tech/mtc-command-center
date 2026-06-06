# Reverse / Re-entry / Cooldown Mapping Evidence

Generated: 2026-06-06 by Codex GPT-5.

Scope: `QL_FAM_MOMENTUM_CONTINUATION|TRXUSDT|4h` Gate3 lifecycle evidence after approved MTC lifecycle fixes.

## Fixes Applied

- Restored fail-fast config guard for `trade.max_pyramid_positions != 1`, preserving single-position behavior.
- Restored legacy-compatible bar-count time-stop semantics: `time_stop.enabled=true` implies bar-count exit even when `use_bars=false`.
- EOD/EOW time-stop boundary exits now record the prior boundary bar timestamp and close instead of the first bar of the new day/week.
- `consec_loss_reset_daily=true` now clears the guard streak before evaluating the new day's entry guard.
- Added public `_is_end_of_day` / `_is_end_of_week` helpers for UTC calendar boundary contracts.
- `TRAIL` exits now fill at bar close because Pine `strategy.close()` is a bar-close order, not a trailing-stop-price fill.
- The once-per-bar equity update branch now uses explicit unrealized PnL while preserving the flat balance branch.

## Test Evidence

Command:

```powershell
python -m pytest tests\test_opp_signal_same_bar_flip.py tests\test_pending_queue.py tests\test_runner_daily_and_mae_guards.py tests\test_same_bar_reentry_and_capital_guard.py tests\test_runner_config_guards.py -q
```

Result: 21 passed.

Final focused regression command:

```powershell
python -m pytest tests\test_producer_adapter.py tests\test_mtc_engine_validate_cli.py tests\test_signal_parity.py tests\test_opp_signal_same_bar_flip.py tests\test_pending_queue.py tests\test_runner_daily_and_mae_guards.py tests\test_same_bar_reentry_and_capital_guard.py tests\test_runner_config_guards.py tests\test_timezone_session_contract.py tests\test_trailing_exit_semantics.py tests\test_equity_curve_update_contract.py -q
```

Result: 36 passed.

## Mapping

- The QuantLens momentum-continuation producer emits raw long entries only and always emits `raw_short=false`; reverse logic is therefore not producer-owned for this family.
- `MTCRunner` owns lifecycle after raw signals: pending opposite entries, same-bar flip/re-entry, cooldown guard, daily guard reset, time-stop boundaries, and single-position config guards.
- The producer does not add pyramiding, exits, stops, cooldown, or broker lifecycle logic.

## Limit

This evidence clears the MTC lifecycle mapping criterion for the selected producer. It does not approve live trading and does not prove broker fills, exchange execution, webhook delivery, or future live data-feed drift.
