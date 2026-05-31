# QuantLens Transcript Intake Report

## Source
- Original URL: https://www.youtube.com/watch?v=wwbjYNV3vCY
- Normalized URL: https://www.youtube.com/watch?v=wwbjYNV3vCY
- Video ID: wwbjYNV3vCY
- Title: Purple Profits strategy summary
- Channel: EllyDTrades
- Channel ID: UNKNOWN_CHANNEL_ID
- Intake date: 2026-05-01
- Source type: user-provided non-verbatim summary / QuantLens notes

## Transcript Classification
- Status: CANDIDATE
- Codex status: READY_FOR_PYTHON_PROTOTYPE
- Candidate ID: QL_2026-05-01_US_EQUITIES_INTRADAY_PURPLE_PROFITS
- Transcript hash: abe899137e17764d892684c77bbe6ca35fe47465022fa36a9a1d2eec12a0b5f2

## Extracted Strategy
- Strategy name: Purple Profits.
- Core model: four key price levels plus one 8 EMA line.
- Key levels: previous day high, previous day low, pre-market high, pre-market low.
- Pre-market definition: 04:00-09:30 Eastern Time.
- Level logic: the levels answer where price may go.
- Timing logic: the 8 EMA answers when to enter.
- Breakout requirement: price must clearly break and close beyond a target level; wick-only touches are not enough.
- EMA readiness: after the break, wait for the 8 EMA to catch up so price is not too extended.
- Bullish entry: price pulls back and holds above the 8 EMA after a valid level break.
- Bearish entry: price pulls back and rejects from the 8 EMA after a valid level break.
- Exit/invalidation: if price crosses against the trade direction through the 8 EMA, exit rather than hold.

## Important Caveats
- This is not a verbatim transcript; it is a user-provided structured summary.
- The video overlaps strongly with previous LE model / 8 EMA pullback candidates.
- Several rules need numeric definitions before testing: clear break, EMA snugness, rejection/hold confirmation, and stop/exit trigger.
- No TradingView, Pine, Python runner, backtest, parity, or optimization work was performed.
