# Experiment Plan

## Prototype Scope
Build a research-only Python prototype after deterministic rules are frozen. Use liquid intraday OHLCV data and `5m` candles.

## Deterministic Rules To Define
- VWAP reset session and timezone.
- VWAP calculation from OHLCV.
- Standard deviation band calculation and multipliers `2` and `3`.
- VWAP slope threshold.
- First `5-6` candle recovery rule for trend pullbacks.
- Pullback proximity to VWAP.
- Support/resistance confluence definition.
- Candlestick confirmation definitions: strong close, hammer, bearish hammer, doji rejection.
- Sideways regime detection after first hour.
- Band-hugging trend-day exclusion.
- Reversal band proximity threshold.
- Pullback setup stop and `2R` target.
- Reversal setup stop and VWAP target.
- Minimum reward/risk filter.

## Validation Gates
- First pass: static spec.
- Second pass: one symbol/timeframe prototype.
- Third pass: separate trend-pullback and sideways-reversal reports.
- Fourth pass: multi-symbol sanity only if each setup behaves coherently.

## Explicit Non-Goals
- No MTC_V2 integration.
- No Pine patch.
- No production runner change.
- No optimization before pilot evidence.
