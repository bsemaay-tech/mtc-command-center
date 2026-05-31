# QuantLens Transcript Intake Report

## Source
- Original URL: UNKNOWN_URL
- Normalized URL: UNKNOWN_URL
- Video ID: UNKNOWN_VIDEO_2026-05-01_RSI_CONFLUENCE_PLAYBOOK
- Title: RSI indicator course with five setups and confluence filters
- Channel: UNKNOWN_CHANNEL
- Intake date: 2026-05-01
- Source type: user-provided transcript without URL/channel metadata

## Transcript Classification
- Status: CANDIDATE
- Codex status: READY_FOR_PYTHON_PROTOTYPE
- Candidate ID: QL_2026-05-01_ANY_1H_RSI_CONFLUENCE_PLAYBOOK
- Transcript hash: 02da9e6e234968aeea03f11d140ee6b46305d1608bd674ff685d72f1c755b09b

## Extracted Strategy Family
- Indicator: RSI, default zones `70` overbought and `30` oversold.
- Primary timeframe used in examples: `1h`.
- Claimed scope: any market/timeframe, but this must be validated separately.
- Base setups:
  - RSI `50` pullback continuation.
  - Regular RSI divergence reversal.
  - Hidden RSI divergence continuation.
  - RSI trendline breakout.
  - RSI cross of its `10` period moving average.
- Confluence filters:
  - Support/resistance levels.
  - Fibonacci golden zone `0.5` to `0.618`.
  - `50` period simple moving average.
- Risk model in examples: stop beyond level/golden zone/moving average and target fixed `2R`.

## Key Rules
- RSI pullback long: in uptrend, RSI usually stays above `50`; pullback below `50` must recover quickly above `50`; avoid if RSI stays below `50` for `8-10` candles.
- RSI pullback short: in downtrend, RSI usually stays below `50`; pullback above `50` must fall back below `50`.
- Regular bullish divergence: price lower low, RSI higher low.
- Regular bearish divergence: price higher high, RSI lower high.
- Hidden bullish divergence: uptrend, price higher low, RSI lower low.
- Hidden bearish divergence: downtrend, price lower high, RSI higher high.
- RSI trendline breakout: draw trendline on RSI swing structure; trade when RSI breaks the line.
- RSI MA crossover: RSI crosses above/below its `10` period moving average, with higher quality near/beyond `30/70`.

## Important Caveats
- URL/channel metadata was not provided.
- The transcript presents a large playbook, not one isolated setup.
- Divergence pivots, trendlines, support/resistance, Fibonacci swing selection, and candle entry timing must be made deterministic before prototype.
- No TradingView, Pine, Python runner, backtest, parity, or optimization work was performed.
