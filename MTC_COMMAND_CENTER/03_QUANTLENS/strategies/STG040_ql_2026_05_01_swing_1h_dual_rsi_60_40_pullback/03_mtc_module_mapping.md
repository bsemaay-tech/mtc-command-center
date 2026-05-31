# MTC Module Mapping

## Candidate Role
This candidate can act as a multi-timeframe regime filter plus pullback entry module.

## Proposed Signals
- `htf_rsi`: daily `RSI(7)`.
- `ltf_rsi`: entry timeframe `RSI(7)`.
- `htf_regime`: `BULL` if `htf_rsi > 60`, `BEAR` if `htf_rsi < 40`, otherwise `SIDEWAYS`.
- `long_pullback_ready`: `htf_regime == BULL` and `ltf_rsi < 40`.
- `long_entry`: `long_pullback_ready` followed by `ltf_rsi` crossing above `40`.
- `short_pullback_ready`: `htf_regime == BEAR` and `ltf_rsi > 60`.
- `short_entry`: `short_pullback_ready` followed by `ltf_rsi` crossing below `60`.

## Long Prototype Mapping
- Context: daily `RSI(7) > 60`.
- Trigger: `1h RSI(7)` recovers above `40` after being below `40`.
- Optional confirmation: support proximity or bullish reversal candle.
- Stop: below recent swing low.
- Target: `2R`.

## Short Prototype Mapping
- Context: daily `RSI(7) < 40`.
- Trigger: `1h RSI(7)` drops below `60` after being above `60`.
- Optional confirmation: resistance proximity or bearish reversal candle.
- Stop: above recent swing high.
- Target: `2R`.

## Integration Boundary
No Pine or production Python change should be made until MTF alignment and swing-stop rules are specified in a lookahead-safe way.
