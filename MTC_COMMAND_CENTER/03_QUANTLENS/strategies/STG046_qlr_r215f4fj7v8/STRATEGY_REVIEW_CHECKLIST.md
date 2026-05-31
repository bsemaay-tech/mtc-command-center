# Strategy Review Checklist

## First Load

1. Open TradingView.
2. Load `standalone_pine_strategy_REVIEW.pine`.
3. Start with `NVDA` on `5m`, matching the readable CLEAN indicator review.
4. Keep default signal inputs aligned with `standalone_pine_visual_review_CLEAN.pine`.

## First Settings

- `enable_long = true`
- `enable_short = true`
- `risk_mode = fixed_qty`
- `fixed_qty = 1`
- `stop_mode = prior_bar`
- `tp_mode = R_multiple`
- `tp_r_multiple = 2`
- `max_bars_in_trade = 0`
- `one_position_at_a_time = true`

## Visual Checks

1. Confirm strategy entries appear on filtered long/short signal bars.
2. Confirm no long and short entry is created on the same bar.
3. Confirm no repeated entry appears while a position is open when `one_position_at_a_time = true`.
4. Confirm active stop line appears only while a position is open.
5. Confirm active target line appears only when `tp_mode` is not `none`.
6. Confirm time exit behavior only after setting `max_bars_in_trade > 0`.
7. Compare marker locations against `standalone_pine_visual_review_CLEAN.pine`.

## PASS_REVIEW

Use PASS_REVIEW only if entries and exits mechanically correspond to the CLEAN filtered markers and wrapper exits behave as configured.

## FAIL_REVIEW

Use FAIL_REVIEW if strategy orders do not match filtered markers, same-bar conflicts enter, or position management creates unreadable or misleading behavior.

## NEEDS_RULE_CLARIFICATION

Use NEEDS_RULE_CLARIFICATION if signal placement looks reasonable but stop, target, or time-exit rules are too underspecified by source material.

## Important

Strategy Tester output is for wrapper inspection only. Do not use this file to claim profitability, robustness, or MTC readiness.
