# QuantLens Transcript Intake Report

## Source
- Original URL: https://youtu.be/Gr2VDAOPRoc?si=cqu6XcRmWZlekz0M
- Normalized URL: https://www.youtube.com/watch?v=Gr2VDAOPRoc
- Video ID: Gr2VDAOPRoc
- Title: UNKNOWN_TITLE - 8 EMA purple line Amazon trade
- Channel: UNKNOWN_CHANNEL
- Intake date: 2026-05-01

## Transcript Classification
- Status: CANDIDATE
- Codex status: READY_FOR_PYTHON_PROTOTYPE
- Candidate ID: QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK
- Transcript hash: 0b06440a2fd70675b291564b9bb6e2e0c99a52fe159fe675aecc8612bf4d5554

## Extracted Strategy
- Use an 8-period EMA as the primary trend and dynamic support/resistance line.
- Long bias when price is above the 8 EMA; short bias when price is below the 8 EMA.
- Long entry: wait for a pullback close to the rising 8 EMA after a bullish impulse.
- Short entry: wait for a pop close to the falling 8 EMA after a bearish impulse.
- Stop: for longs, use the low of the entry candle; for shorts, use the high of the entry candle.
- Profit-taking: scale partials into high of day or low of day; leave a runner until the 8 EMA breaks.
- Re-entry: allowed after a quick wick and recovery, but stop trading that symbol after two failed attempts.

## Important Caveats
- The video is options-focused, but the codable logic is based on underlying price action.
- The claimed win-rate and return figures are unsupported by backtest evidence.
- Market, timeframe, and execution assumptions need normalization before any prototype.
- No TradingView, Pine, Python runner, backtest, or optimization work was performed.
