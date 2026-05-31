# Raw QuantLens Report

## Metadata
- Source URL: UNKNOWN_URL
- Video ID: UNKNOWN_VIDEO_2026-05-01_DUAL_RSI_60_40_SWING
- Title: Dual RSI 60/40 swing pullback strategy
- Channel: UNKNOWN_CHANNEL
- Transcript hash: 0085bb9a34bfa64ce8e0d99b3532a28da703023088af74d8171f22417860337a
- Intake date: 2026-05-01
- Source type: user-provided transcript without URL/channel metadata

## Transcript-Derived Summary
The transcript describes a dual-RSI swing trading strategy. The first RSI is `RSI(7)` on the daily timeframe with `60/40` regime bands. It acts as a higher-timeframe trend filter: above `60` means uptrend and buy-only; below `40` means downtrend and sell-only; between `40` and `60` means sideways/no clear trend.

The second RSI is `RSI(7)` on the `1h` trading chart, also using `60/40` bands. In a daily uptrend, the strategy waits for the `1h` RSI to move below `40` during a corrective pullback, then enter when the `1h` RSI recovers back above `40`, ideally near support and with bullish price action. In a daily downtrend, the strategy waits for the `1h` RSI to move above `60` during a pullback, then enter short when it crosses back below `60`, ideally near resistance and with bearish price action.

Stops are placed beyond the recent swing low/high. The target used in examples is `2R`.

## QuantLens Interpretation
This is a focused and codable multi-timeframe RSI pullback candidate. The RSI regime and pullback rules are deterministic. The support/resistance and candlestick confirmations require a separate mechanical definition before prototype testing.
