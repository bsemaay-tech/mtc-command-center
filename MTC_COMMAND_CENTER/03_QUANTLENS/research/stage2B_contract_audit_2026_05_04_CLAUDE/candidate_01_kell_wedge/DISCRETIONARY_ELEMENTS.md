# DISCRETIONARY_ELEMENTS — Kell Wedge Pop

| Element | Source phrase | Mechanical approximation | Safe? | Dangerous approximation | Previous LLM choice |
|---|---|---|---|---|---|
| Leadership | "in-play themes, leader, ahead of index" | RS-rank vs SPY 60d top decile + sector basket RS | Yes (proxy) | Skip → trade any asset | DANGEROUS (skipped, used crypto majors) |
| Reversal extension | "capitulation/reversal extension" | distance-from-EMA20 z-score < −1.5 within 30 bars | Yes | Skip (assume any uptrend qualifies) | DANGEROUS (skipped) |
| Higher-low | "bottoms require higher low" | confirmed swing-low(left2/right2) > flush low | Yes | Skip; or use any local low | DANGEROUS (skipped) |
| Tightness | "volatility decreases, price tightens" | ATR percentile + range/range_median ratio | Yes | Fixed % cap with no context | PARTIAL (8% cap only) |
| Mini base | "≥3-bar mini base, swing high break" | ≥3 bars range-bound + Donchian-mini break | Yes | 1-bar Donchian break | PARTIAL |
| MA selection (10 vs 20) | "if stock holds EMA20… use EMA20, else EMA10" | Switch after N successful holds | Yes | Always EMA20 or always EMA10 | DANGEROUS (always EMA20) |
| Blowoff / exhaustion | "obvious blowoff" | %extension above EMA10 + 2-bar reversal | Partial only; needs research | Ignore → ride forever | DANGEROUS (no exit added) |
| Theme / story | "in-play themes" | sector relative-strength bucket | Partial; external data | Skip | DANGEROUS (skipped) |

## Producer / filter / process classification
- Mechanically codable kernel (with proxies for leadership): **producer candidate**.
- Theme / story scoring: **needs external data** (sector RS or news event tags).
- Blowoff exit: **process-only** until research done.
- Without RS-rank data + earnings calendar, this strategy is **not fairly testable**.
