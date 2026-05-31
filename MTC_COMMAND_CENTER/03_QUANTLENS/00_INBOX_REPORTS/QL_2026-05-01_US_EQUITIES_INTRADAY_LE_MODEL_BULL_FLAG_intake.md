# QuantLens Transcript Intake Report

## Source
- Original URL: https://youtu.be/mMwl4xAh_NI?si=uv_JmPnE2HjpDVS-
- Normalized URL: https://www.youtube.com/watch?v=mMwl4xAh_NI
- Video ID: mMwl4xAh_NI
- Title: The ONLY Pattern I've Used for 7 Years - Nothing Else (Full Strategy)
- Channel: UNKNOWN_CHANNEL
- Intake date: 2026-05-01
- Transcript source path: `06_QUANTLENS_LAB/00_INBOX_REPORTS/The ONLY Pattern I've Used for 7 Years - Nothing Else (Full Strategy).md`

## Transcript Classification
- Status: CANDIDATE
- Codex status: READY_FOR_PYTHON_PROTOTYPE
- Candidate ID: QL_2026-05-01_US_EQUITIES_INTRADAY_LE_MODEL_BULL_FLAG
- Transcript hash: 2d0a84db1fb32218ab6f59383a4597de92592b4b32c860d724cd93f6d4505b2b

## Extracted Strategy
- Context: lockout rally / short-squeeze environment after bullish news and trapped shorts.
- Pattern: bull flag after a large impulse, followed by a slow, controlled pullback.
- Key breakout filter: wait for price to break the relevant key level first.
- Bullish levels: previous day high and/or pre-market high.
- Bearish mirror levels: previous day low and/or pre-market low.
- Entry rule: after breakout, enter on the first valid retest of either the key level or the 8 EMA, whichever comes first.
- EMA rule: if the 8 EMA crosses through the key level before a level retest, use the 8 EMA retest.
- Stop: risk the entry candle low for longs; bearish mirror would use entry candle high.
- Partial exit: sell half at high of day for bullish setups or low of day for bearish setups.
- Runner exit: hold remaining position using the 8 EMA as trailing stop.
- Time filter: prioritize first two to three hours; avoid new entries during lunch/chop.

## Important Caveats
- The video is heavily options/0DTE framed; first prototype should use underlying OHLC only.
- Several terms remain discretionary: "large move", "slow controlled pullback", "fully out of range", and "good flag".
- HOD/LOD targets must be implemented without future leakage.
- No TradingView, Pine, Python runner, backtest, parity, or optimization work was performed.
