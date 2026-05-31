# Short-Side Research Scaffolding - 2026-05-31

This is the deferred short-side scaffold for promoted long-only strategies.
Do not reuse long-only metrics as short evidence.

## Current short-side candidates

| Candidate | Long-side family | Suggested short mirror | Status |
|---|---|---|---|
| `QL_ALPHA_ADA_TWO_CANDLE_SR_1H` | Two-candle support/resistance breakout | Strong lower-third close breaking prior low / support; stop at recent high; fixed-R or time exit | `SHORT_UNTESTED` |
| `QL_ALPHA_LTC_RSI_OVERSOLD_1H` | RSI oversold recovery mean reversion | RSI overbought fade; stop at recent high; fixed-R or time exit | `SHORT_UNTESTED` |

## Minimum scaffold for each short candidate

1. Define a separate short entry rule with no long-side reuse.
2. Define stop, target, and time-exit logic independently.
3. Run walk-forward / OOS on the short rule as its own candidate.
4. Compare only on short-side outcomes:
   - return
   - PF
   - drawdown
   - trade count
   - stability across symbols / timeframes

## Rule of thumb

If the short mirror cannot be written in one sentence without referring back to the long rule, it is not ready yet.
