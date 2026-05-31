# Parity Reference Metrics — QL_ALPHA_LTC_RSI_OVERSOLD_1H

- Engine strategy: `GEN_RSI_OVERSOLD_REVERSAL`  | Symbol/TF: LTCUSDT 1h  | direction: long-only
- Params: `{"rsi_len":5,"oversold":35,"recovery":45,"stop_lookback_bars":5,"target_R":2.0,"cost_bps_round_trip":8.0,"max_hold_bars":96}`
- Full-history trades emitted: 1256  | lockbox bars: 13802

| Metric | Engine (recomputed) | Recorded (spec) | Match |
|---|---|---|---|
| compound_return_pct | 95.81 | 95.81 | OK |
| profit_factor | 1.23 | 1.23 | OK |
| trades | 329 | 329 | OK |
| max_drawdown_pct | -21.983 | -21.98 | OK |
| win_rate | 0.3799 | 0.3799 | OK |
| expectancy_R | 0.107 | 0.107 | OK |

**Overall:** VERIFIED — reference reproduces recorded lockbox metrics.
