# Raw QuantLens Report

## Metadata
- Source URL: UNKNOWN_URL
- Video ID: UNKNOWN_VIDEO_2026-05-01_MULTI_EMA_CHANNEL_PULLBACK
- Title: Best EMA settings multi-EMA channel strategy
- Channel: UNKNOWN_CHANNEL
- Transcript hash: 5d9153e18dcba3ca94ec719f9f1be8fba1ba5ee3744f479198df6beae6bf3fa3
- Intake date: 2026-05-01
- Source type: user-provided transcript without URL/channel metadata

## Transcript-Derived Summary
The strategy builds three EMA channels. A slow `EMA(200)` high/close/low channel defines the major trend and trend-change zone. A fast `EMA(5)` high/low channel and a medium `EMA(13)` high/low channel define pullback momentum inside that larger trend.

For a short setup, price first crosses below the green `EMA(200)` channel. The trader waits for price to pull back into or to the green channel without crossing back above it. During the pullback, the white `EMA(5)` channel should move above the orange `EMA(13)` channel. The short trigger occurs when the white channel closes back below the orange channel.

For a long setup, price first crosses above the green `EMA(200)` channel. The trader waits for price to pull back into or to the green channel without crossing back below it. During the pullback, the white `EMA(5)` channel should move below the orange `EMA(13)` channel. The long trigger occurs when the white channel closes back above the orange channel.

Stops are placed beyond the pullback or the green channel, and targets use a fixed `2R` risk/reward.

## QuantLens Interpretation
This is a codable strategy candidate. It is more complete than a generic indicator list because it defines trend state, pullback state, trigger, stop placement, and target model. It is suitable for a deterministic Python prototype after edge-case semantics are defined.
