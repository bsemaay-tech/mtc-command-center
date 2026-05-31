# Raw QuantLens Report

## Metadata
- Source URL: UNKNOWN_URL
- Video ID: UNKNOWN_VIDEO_2026-05-01_TWO_CANDLE_THEORY_SR
- Title: Two candle theory sentiment with support and resistance
- Channel: UNKNOWN_CHANNEL
- Transcript hash: 742fbc7184cfe33487fe568b9c9ca695c5a33aaccd5d0028a1b299794f449203
- Intake date: 2026-05-01
- Source type: user-provided transcript without URL/channel metadata

## Transcript-Derived Summary
The transcript explains a two-candle sentiment reading process inspired by Lance Beggs' YTC Price Action Trader. Instead of memorizing named candlestick patterns, the method classifies every newly closed candle by two dimensions: where it closes inside its own range and where it closes relative to the previous candle range.

The first dimension is `close_position`: high close, mid close, or low close. The second dimension is `close_comparison`: bull candle, range candle, or bear candle. Combining them creates nine possible sentiment states. The strongest bullish state is a candle that closes above the previous candle high and in the upper third of its own range. The strongest bearish state is a candle that closes below the previous candle low and in the lower third of its own range.

The trade examples combine this candle-state process with support and resistance. A long example enters after a high-close bull candle breaks resistance, with stop below the candle low and a `1:1.5` target. A short example enters after repeated bearish evidence and a low-close bear candle breaks support, with stop above the candle high and active trade management.

## QuantLens Interpretation
This is a codable price-action sentiment module. The highest-value prototype is not discretionary candle narration, but a deterministic candle state machine that can be tested as an entry confirmation or guard around level breaks.
