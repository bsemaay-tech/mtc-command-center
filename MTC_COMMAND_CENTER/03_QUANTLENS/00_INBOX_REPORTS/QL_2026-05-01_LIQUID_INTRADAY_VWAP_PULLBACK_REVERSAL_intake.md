# QuantLens Transcript Intake Report

## Source
- Original URL: UNKNOWN_URL
- Normalized URL: UNKNOWN_URL
- Video ID: UNKNOWN_VIDEO_2026-05-01_VWAP_PULLBACK_REVERSAL
- Title: VWAP day trading pullback and reversal setups
- Channel: UNKNOWN_CHANNEL
- Intake date: 2026-05-01
- Source type: user-provided transcript without URL/channel metadata

## Transcript Classification
- Status: CANDIDATE
- Codex status: READY_FOR_PYTHON_PROTOTYPE
- Candidate ID: QL_2026-05-01_LIQUID_INTRADAY_VWAP_PULLBACK_REVERSAL
- Transcript hash: 3ddce69e11c578436f923a529fcad8e148e17830841991737ccdc6eb6ce44580

## Extracted Strategy
- Indicator: session VWAP, reset from each day's open.
- Bands: VWAP standard deviation bands, strategy settings use multipliers `2` and `3`.
- Timeframe: `5m`.
- Market scope: liquid day-trading assets; examples include S&P 500, Tesla, Apple, and Microsoft.
- Setup 1: VWAP pullback continuation.
- Setup 2: VWAP band reversal in sideways market.

## Setup 1 - VWAP Pullbacks
- Long bias: price stays above VWAP from open, or dips below VWAP then recovers above within first `5-6` candles and remains above; VWAP slopes upward.
- Long entry zone: pullback to VWAP with support confluence.
- Long confirmation: bullish candlestick pattern or strong bullish candle.
- Long stop: below recent swing low.
- Long target: fixed `2R`.
- Short bias: price trades below VWAP with VWAP sloping downward.
- Short entry zone: pullback to VWAP with resistance confluence.
- Short confirmation: strong red candle closing below VWAP.
- Short stop: above signal candle high or local resistance.
- Short target: fixed `2R`.

## Setup 2 - VWAP Reversals
- Regime: sideways market only.
- Time guard: avoid first hour.
- Sideways validation: during first hour, price reverses from VWAP bands instead of hugging one band.
- Short entry zone: near upper VWAP band plus resistance or bearish candle confirmation.
- Short stop: above signal candle high or resistance.
- Short target: VWAP.
- Long entry zone: near lower VWAP band plus support or bullish candle confirmation.
- Long stop: below signal candle or support.
- Long target: VWAP.
- Minimum R:R: `1:1` acceptable, but avoid trades where risk is larger than reward.

## Important Caveats
- URL/channel metadata was not provided.
- Support/resistance and candlestick confirmation need deterministic definitions.
- Sideways regime and "hugging the band" filters need deterministic rules.
- No TradingView, Pine, Python runner, backtest, parity, or optimization work was performed.
