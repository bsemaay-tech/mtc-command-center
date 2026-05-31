# Strategy Review Notes

## Scope

`standalone_pine_strategy_REVIEW.pine` is a TradingView strategy wrapper for manual review of candidate `QLR_R215f4fj7V8`.

This is not production integration:
- It does not modify `MTC_V2.pine`.
- It does not modify Python production runners.
- It does not create alerts.
- It is not optimized.
- It must not be used to claim profitability.

## Source Logic

The signal producer is copied from `standalone_pine_visual_review_CLEAN.pine` as closely as practical:
- VWAP side and slope guard.
- Trend continuation range break.
- No-man's-land suppression.
- Capitulation proxy.
- Right-side-of-V confirmation.
- Same-bar long/short conflict suppression.
- Signal cooldown.

## Review Wrapper Behavior

The wrapper adds TradingView Strategy Tester mechanics only to inspect order placement:
- Long entry on filtered long signal.
- Short entry on filtered short signal.
- Optional one-position-at-a-time guard.
- Protective stop.
- Optional take profit.
- Optional max-bars-in-trade time exit.

Strategy Tester metrics in this wrapper are diagnostic only. They are not optimization output and should not be interpreted as evidence of edge.

## Risk Inputs

- `risk_mode = fixed_qty`: uses `fixed_qty`.
- `risk_mode = percent_equity`: placeholder sizing estimate using equity percentage divided by close.
- `stop_mode = prior_bar`: uses the current/prior bar extreme.
- `stop_mode = ATR`: uses ATR stop distance.
- `stop_mode = percent`: uses a fixed percent stop distance.
- `tp_mode = R_multiple`: uses stop distance times `tp_r_multiple`.
- `tp_mode = ATR`: uses ATR target distance.
- `tp_mode = none`: no limit target is submitted.

## Review Boundary

Use this file only after the CLEAN indicator view looks visually sensible. If order markers disagree with the CLEAN filtered markers, inspect the wrapper behavior before changing any source signal logic.
