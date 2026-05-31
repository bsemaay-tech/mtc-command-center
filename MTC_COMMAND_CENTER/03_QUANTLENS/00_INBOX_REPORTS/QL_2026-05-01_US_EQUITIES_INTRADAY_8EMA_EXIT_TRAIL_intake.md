# QuantLens Transcript Intake Report

## Source
- Original URL: https://youtu.be/rprQ4uo-mzE
- Normalized URL: https://www.youtube.com/watch?v=rprQ4uo-mzE
- Video ID: rprQ4uo-mzE
- Title: The Only Exit Strategy You'll Ever Need... (Even When You're Scared)
- Channel: EllyDTrades
- Channel ID: UNKNOWN_CHANNEL_ID
- Intake date: 2026-05-01
- Source type: user-provided non-verbatim summary / QuantLens notes

## Transcript Classification
- Status: CANDIDATE
- Codex status: READY_FOR_PYTHON_PROTOTYPE
- Candidate ID: QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL
- Transcript hash: 93e523c6635ab3647478648d92b9bb952ffa1d214177b49846c021df804042b6

## Extracted Strategy
- Strategy focus: exit and trade management, not a new producer.
- Core exit line: 8 EMA.
- Long management: when price is above the 8 EMA, hold the position until price breaks below the 8 EMA.
- Short management: when price is below the 8 EMA, hold the position until price breaks above the 8 EMA.
- Intended purpose: remove emotional early exits and use the EMA as a trailing stop.
- Psychological rule: do not exit a 10m/30m trend because of small 1m pullback candles.
- Review exercise: analyze the last 10 early exits and compare actual reversal points against the 8 EMA break.

## Important Caveats
- This is not a verbatim transcript; it is a user-provided structured summary.
- The rule is an exit/trailing module candidate, not a complete standalone entry strategy.
- "Breaks the 8 EMA" must be defined mechanically before testing: wick break, close break, multi-bar confirmation, or ATR buffer.
- No TradingView, Pine, Python runner, backtest, parity, or optimization work was performed.
