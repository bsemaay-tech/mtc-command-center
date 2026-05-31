# Raw QuantLens Report

## Metadata
- Source URL: https://www.youtube.com/watch?v=Gr2VDAOPRoc
- Original URL: https://youtu.be/Gr2VDAOPRoc?si=cqu6XcRmWZlekz0M
- Video ID: Gr2VDAOPRoc
- Title: UNKNOWN_TITLE - 8 EMA purple line Amazon trade
- Channel: UNKNOWN_CHANNEL
- Transcript hash: 0b06440a2fd70675b291564b9bb6e2e0c99a52fe159fe675aecc8612bf4d5554
- Intake date: 2026-05-01

## Transcript-Derived Summary
The speaker presents a simple trend-continuation options trading method using only an 8 EMA, described as a purple line on the chart. The EMA is treated as the scoreboard for buyer/seller control, trend direction, and dynamic support or resistance.

The main rules are:
- Price above the 8 EMA implies bullish bias and long/call setups.
- Price below the 8 EMA implies bearish bias and short/put setups.
- Enter as close as possible to the 8 EMA after a pullback in trend.
- Avoid chasing extended candles away from the EMA.
- Use the entry candle low as the long stop and entry candle high as the short stop.
- Take partial profits near high of day or low of day and leave a runner.
- Re-enter after a quick wick/recovery if the setup remains valid, but stop after two failed attempts.

## Example Discussed
- Symbol: Amazon
- Timeframe: 10 minute
- Direction: Long/calls
- Setup: strong open impulse, wait for pullback to rising 8 EMA, enter near EMA, risk entry candle low, target high of day, trail/hold runner while price remains above 8 EMA.

## QuantLens Interpretation
This is a codable strategy candidate, but it is not a complete production system. The core signal is simple enough for a Python prototype, while discretionary elements such as "as close as possible", exhaustion, high-of-day profit-taking, and runner sizing require explicit rules before backtesting.
