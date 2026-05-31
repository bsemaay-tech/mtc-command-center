# Raw QuantLens Report

## Metadata
- Source URL: https://www.youtube.com/watch?v=rprQ4uo-mzE
- Original URL: https://youtu.be/rprQ4uo-mzE
- Video ID: rprQ4uo-mzE
- Title: The Only Exit Strategy You'll Ever Need... (Even When You're Scared)
- Channel: EllyDTrades
- Channel ID: UNKNOWN_CHANNEL_ID
- Transcript hash: 93e523c6635ab3647478648d92b9bb952ffa1d214177b49846c021df804042b6
- Intake date: 2026-05-01
- Source type: user-provided non-verbatim summary

## Transcript-Derived Summary
The source describes an exit-management framework for traders who close winning positions too early. The stated solution is to use the 8 EMA as the objective exit line and trailing stop.

For long trades, the rule is to stay in the trade while price remains above the 8 EMA and exit only when price breaks below it. For short trades, the rule is to stay in the trade while price remains below the 8 EMA and exit only when price breaks above it.

The summary frames most early exits as psychological errors: fear of giving back gains, watching too small a timeframe, lacking a technical exit rule, and interpreting normal pullbacks as reversals.

## QuantLens Interpretation
This is a codable exit-rule candidate. It should not be treated as a new producer or standalone strategy. It is best evaluated as a trailing exit module attached to existing EllyDTrades 8 EMA / level-breakout entry candidates.

The rule needs deterministic definitions for EMA break, trend timeframe, and intrabar versus close-based execution before any prototype or backtest.
