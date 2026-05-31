# DISCRETIONARY_ELEMENTS — Slingshot

| Element | Mechanical? | Safe approximation | Previous LLM choice |
|---|---|---|---|
| EMA(high, 4) | Fully | exact | Correct |
| "Prior strength" | Approximable | OR of 4 proxies | Only `close > SMA50` (one of four) |
| "Real pullback" | Approximable | ≥1 close < EMA(high,4) within N bars + depth cap | Coded |
| "No obvious resistance" | Discretionary | Optional check vs prior swing high above | Skipped |
| "Strength after weakness" | Captured by trigger | OK | OK |
| Exit mode choice | Mechanical | sweep | Single mode picked per variant |

## Producer / filter / process classification
- **Producer candidate** — clean, stateless, easy to gate. Lowest discretion of the six candidates.
- Closest to MTC-ready of all six.
