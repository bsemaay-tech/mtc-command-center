# MTC Module Mapping

## Candidate Role
This candidate is best treated as an entry confirmation and guard, not as a standalone strategy.

## Proposed Signals
- `close_position`: `HIGH`, `MID`, `LOW`.
- `close_comparison`: `BULL`, `RANGE`, `BEAR`.
- `two_candle_state`: one of nine combined states.
- `bias_state`: `BULLISH`, `BEARISH`, `NEUTRAL`.
- `follow_through_count`: number of same-direction strong states after a bias cue.

## Long Prototype Mapping
- Context: price near or breaking resistance.
- Trigger: `HIGH_CLOSE_BULL` closes above resistance.
- Confirmation: prior candle sequence has bullish or neutral-to-bullish bias.
- Stop: below signal candle low.
- Target: `1.5R`.
- Early exit: confirmed bearish state sequence or support failure.

## Short Prototype Mapping
- Context: price near or breaking support.
- Trigger: `LOW_CLOSE_BEAR` closes below support.
- Confirmation: prior candle sequence has bearish or neutral-to-bearish bias.
- Stop: above signal candle high.
- Target: `1.5R`.
- Early exit: confirmed bullish state sequence or resistance reclaim.

## Integration Boundary
No Pine or production Python change should be made until the prototype spec is written and checked against existing MTC_V2 candle and level modules.
