# Risks And Unknowns

## Main Risks
- Support/resistance selection can introduce lookahead if based on future pivots.
- "Follow-through" is described qualitatively and must be converted to exact candle counts.
- "Sentiment changes while in trade" is discretionary unless formalized.
- `1:1.5` target may not be robust across assets and volatility regimes.
- S&P 500 `5m` example does not prove cross-market validity.

## Unknowns
- Exact source video URL.
- Channel name and channel ID.
- Whether examples use cash index, ETF, CFD, or futures chart.
- Session handling and premarket inclusion.
- Whether gaps and doji/zero-range candles require special handling.

## Mitigations
- Use only closed candles.
- Use past-only rolling levels for support/resistance.
- Keep the first prototype as event extraction before performance claims.
- Label all outputs as research-only.
