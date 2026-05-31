# QuantLens Transcript Intake Report

## Source
- Original URL: UNKNOWN_URL
- Normalized URL: UNKNOWN_URL
- Video ID: UNKNOWN_VIDEO_2026-05-01_MULTI_EMA_CHANNEL_PULLBACK
- Title: Best EMA settings multi-EMA channel strategy
- Channel: UNKNOWN_CHANNEL
- Intake date: 2026-05-01
- Source type: user-provided transcript without URL/channel metadata

## Transcript Classification
- Status: CANDIDATE
- Codex status: READY_FOR_PYTHON_PROTOTYPE
- Candidate ID: QL_2026-05-01_UNKNOWN_MULTI_EMA_CHANNEL_PULLBACK
- Transcript hash: 5d9153e18dcba3ca94ec719f9f1be8fba1ba5ee3744f479198df6beae6bf3fa3

## Extracted Strategy
- Green channel: three `EMA(200)` lines calculated on `high`, `close`, and `low`.
- White channel: two `EMA(5)` lines calculated on `high` and `low`.
- Orange channel: two `EMA(13)` lines calculated on `high` and `low`.
- Trend filter: price above green channel means uptrend; price below green channel means downtrend.
- Long setup: price crosses from below to above green channel, then pulls back to touch or enter the green channel without going below it.
- Long pullback state: white channel moves below orange channel during the pullback.
- Long trigger: white channel closes back above orange channel.
- Long stop: below pullback or below green channel.
- Short setup: price crosses from above to below green channel, then pulls back to touch or enter the green channel without going above it.
- Short pullback state: white channel moves above orange channel during the pullback.
- Short trigger: white channel closes back below orange channel.
- Short stop: above pullback or above green channel.
- Target: fixed `2R` risk/reward target.
- Risk note: use proper risk management, including 1% rule.

## Important Caveats
- URL/channel metadata was not provided.
- This is codable, but exact "touch", "inside channel", and "close back above/below" semantics must be frozen before prototype.
- No TradingView, Pine, Python runner, backtest, parity, or optimization work was performed.
