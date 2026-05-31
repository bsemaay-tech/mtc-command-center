# Raw QuantLens Report

## Metadata
- Source URL: https://www.youtube.com/watch?v=mMwl4xAh_NI
- Original URL: https://youtu.be/mMwl4xAh_NI?si=uv_JmPnE2HjpDVS-
- Video ID: mMwl4xAh_NI
- Title: The ONLY Pattern I've Used for 7 Years - Nothing Else (Full Strategy)
- Channel: UNKNOWN_CHANNEL
- Transcript hash: 2d0a84db1fb32218ab6f59383a4597de92592b4b32c860d724cd93f6d4505b2b
- Intake date: 2026-05-01

## Transcript-Derived Summary
The speaker describes an intraday "LE model" bull flag strategy for lockout rallies. The thesis is that bullish news plus trapped shorts can produce a short-squeeze rally where classic level pullbacks may not appear. In that environment, the model waits for a breakout over key levels and then enters on a retest of either the level or the 8 EMA.

The model emphasizes avoiding breakout chasing. The preferred entry is a slow, controlled pullback into support after price has cleared the required level. Good entries are described as tight-risk flags; bad entries are large, violent pullbacks with reversal-looking candles.

## Rules Extracted From Transcript
- Wait for price to break a key level before considering an entry.
- Bullish key levels: previous day high and pre-market high.
- Bearish key levels: previous day low and pre-market low.
- Enter from the key level retest or 8 EMA retest, whichever comes first.
- If the 8 EMA crosses through the level before price retests the level, use the EMA retest.
- For long trades, risk the low of the entry candle.
- Take partial profits at high of day.
- Trail the runner with the 8 EMA.
- Avoid new entries during lunch/choppy periods.

## Examples Discussed
- SPY April 17, 2026: wait for pre-market high break, then enter on pre-market high retest or later 8 EMA pullback.
- SPY April 14, 2026: clear pre-market high, wait for pullback to the 8 EMA instead of chasing.
- SPY April 9, 2026: inside day turns into outside day after breaking previous day high; wait for 8 EMA to catch up, enter near EMA, risk candle low, target high of day.

## QuantLens Interpretation
This is a codable strategy candidate with a stronger rule set than a generic EMA pullback. It combines level breakout state, EMA retest routing, flag-quality filtering, partial exits, runner trailing, and a session time guard. It is still not ready for direct MTC_V2 integration because several discretionary conditions need deterministic definitions.
