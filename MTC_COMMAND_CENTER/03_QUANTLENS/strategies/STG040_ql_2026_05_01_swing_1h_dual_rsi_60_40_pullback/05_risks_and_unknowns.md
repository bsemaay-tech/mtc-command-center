# Risks And Unknowns

## Main Risks
- Daily RSI can leak future information if the current daily candle is used before close.
- Swing high/low stop can be lookahead-biased if future pivots are used.
- Support/resistance and candlestick confirmations are discretionary in the transcript.
- Large signal-candle rejection is described qualitatively.
- Broad market claims are unvalidated.

## Unknowns
- Exact source video URL.
- Channel name and channel ID.
- Exact TradingView RSI settings beyond length and levels.
- Whether the daily RSI uses completed daily bars only.
- Which assets and sessions were used in examples.

## Mitigations
- Use completed higher-timeframe bars only.
- Use past-only swing stop logic.
- Separate core RSI logic from optional price-action confluence.
- Keep first prototype research-only.
