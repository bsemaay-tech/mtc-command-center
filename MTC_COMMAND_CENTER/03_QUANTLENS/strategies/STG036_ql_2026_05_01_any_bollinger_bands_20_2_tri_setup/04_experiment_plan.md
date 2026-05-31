# Experiment Plan

## Prototype Scope
Do not prototype all three variants together. Start with one deterministic variant.

## Recommended First Variant
`Bollinger squeeze/range breakout`

## Deterministic Rules To Define
- Bollinger source and length: default `close`, length `20`.
- Standard deviation multiplier: `2`.
- Band-width threshold for "narrow" and "wide".
- Lookback window for sideways containment.
- Minimum percentage of candles contained inside bands.
- Breakout close rule above upper band or below lower band.
- Strong candle definition.
- Stop anchor and buffer.
- Target model.
- Directional filters or session filters if any.

## Alternative Variants
- Range reversal from upper/lower band in narrow-band regime.
- Middle-band trend pullback in wide-band/trending regime.

## Explicit Non-Goals
- No combined tri-setup system initially.
- No discretionary support/resistance or candlestick pattern dependence.
- No Pine patch.
- No production runner change.
- No optimization before deterministic event extraction.
