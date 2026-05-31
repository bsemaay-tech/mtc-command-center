# MTC Module Mapping

## Candidate Role
This candidate is best mapped as a candle-confirmation layer for existing level or trendline setups.

## Proposed Pattern Signals
- `bullish_pin_bar`.
- `bearish_pin_bar`.
- `doji`.
- `bullish_engulfing`.
- `bearish_engulfing`.
- `morning_star`.
- `evening_star`.

## Long Prototype Mapping
- Context: price near past-only support or reclaiming/breaking trendline.
- Trigger options:
  - `morning_star` at support.
  - `bullish_engulfing` near trendline/resistance break.
  - `bullish_pin_bar` after down move at support.
- Entry: break/close above signal pattern high.
- Stop: below pattern low or relevant doji/pin low.
- Target: next past-known resistance or fixed R substitute.

## Short Prototype Mapping
- Context: price near past-only resistance.
- Trigger options:
  - `evening_star` at resistance.
  - `bearish_engulfing` near resistance/trendline rejection.
  - `bearish_pin_bar` after up move at resistance.
- Entry: break/close below signal pattern low.
- Stop: above pattern high or relevant doji/pin high.
- Target: next past-known support or fixed R substitute.

## Integration Boundary
No Pine or production Python change should be made until one pattern family and one confluence type are selected and specified with past-only rules.
