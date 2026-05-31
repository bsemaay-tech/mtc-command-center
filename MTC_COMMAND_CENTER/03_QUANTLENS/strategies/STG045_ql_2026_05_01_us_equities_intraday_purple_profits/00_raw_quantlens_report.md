# Raw QuantLens Report

## Metadata
- Source URL: https://www.youtube.com/watch?v=wwbjYNV3vCY
- Original URL: https://www.youtube.com/watch?v=wwbjYNV3vCY
- Video ID: wwbjYNV3vCY
- Title: Purple Profits strategy summary
- Channel: EllyDTrades
- Channel ID: UNKNOWN_CHANNEL_ID
- Transcript hash: abe899137e17764d892684c77bbe6ca35fe47465022fa36a9a1d2eec12a0b5f2
- Intake date: 2026-05-01
- Source type: user-provided non-verbatim summary

## Transcript-Derived Summary
The source describes EllyDTrades' "Purple Profits" framework. The model uses four daily/session levels and the 8 EMA. The levels define the relevant support/resistance map, while the 8 EMA is used as the entry timing and invalidation line.

The workflow is sequential:
- Mark previous day high, previous day low, pre-market high, and pre-market low.
- Wait for price to clearly break one of those levels.
- Require a candle close beyond the level, not only a wick.
- Wait for the 8 EMA to catch up to price before entering.
- Enter bullish when price holds the 8 EMA after a valid upside break.
- Enter bearish when price rejects from the 8 EMA after a valid downside break.
- Exit when price crosses back through the 8 EMA against the position.

## QuantLens Interpretation
This is a codable strategy candidate. It is closely related to the existing 8 EMA pullback and LE model bull flag candidates, but it is worth tracking separately because it states the four-level framework and the required step order more explicitly.

The model is not ready for backtesting until the vague terms are converted into deterministic rules.
