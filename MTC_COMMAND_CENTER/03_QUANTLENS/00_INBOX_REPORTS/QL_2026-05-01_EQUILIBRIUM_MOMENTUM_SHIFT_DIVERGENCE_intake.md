# QuantLens Transcript Intake Report

## Source
- Original URL: UNKNOWN_URL
- Normalized URL: UNKNOWN_URL
- Video ID: UNKNOWN_VIDEO_2026-05-01_EQUILIBRIUM_MOMENTUM_SHIFT_DIVERGENCE
- Title: Equilibrium Momentum Shift divergence strategy
- Channel: UNKNOWN_CHANNEL
- Intake date: 2026-05-01
- Source type: user-provided transcript without URL/channel metadata

## Transcript Classification
- Status: SALVAGE
- Codex status: SALVAGE_ONLY
- Candidate ID: QL_2026-05-01_EQUILIBRIUM_MOMENTUM_SHIFT_DIVERGENCE
- Transcript hash: a8d8a34767386c74006dd71d3bbcc0265f95a301b706930f549bf5d1c4d36857

## Intake Decision
This transcript contains a useful divergence and price-action confirmation concept, but it depends on the external TradingView indicator `Equilibrium Momentum Shift` by BigBeluga. The transcript describes the formula at a high level, but not enough to reproduce the oscillator exactly.

For that reason, this is stored as `SALVAGE_ONLY`, not `READY_FOR_PYTHON_PROTOTYPE`.

## Salvageable Strategy Logic
- Indicator base: selected range, default length `50`.
- Equilibrium price: midpoint between highest high and lowest low in the selected range.
- Momentum oscillator: deviation from equilibrium, double EMA smoothing, range normalization, nonlinear compression to `[-1, +1]`.
- Signal line: moving average of momentum line, length `9`.
- Histogram: momentum line versus signal line, similar usage pattern to MACD.
- Bearish divergence: price makes equal/higher high while momentum line makes lower high.
- Bearish confirmation: mark swing low between divergence highs and enter short only after candle closes below that low.
- Bearish stop: above highest high in divergence pattern.
- Bullish divergence: price makes lower low while momentum line makes higher low.
- Bullish confirmation: mark swing high between divergence lows and enter long only after candle closes above that high.
- Bullish stop: below previous low.
- Risk note: do not trade indicator alone; use price-action confirmation and risk management.

## Blockers For Prototype
- Exact TradingView script/source is not provided.
- Exact nonlinear compression function is not specified.
- Exact double EMA lengths/settings are not specified.
- Divergence pivot definitions are discretionary.
- Target/exit model is not defined.

## No-Touch Confirmation
- `01_PINE/MTC_V2.pine` was not modified.
- Production Python runner files were not modified.
- No backtest, optimization, parity run, or TradingView automation was performed.
