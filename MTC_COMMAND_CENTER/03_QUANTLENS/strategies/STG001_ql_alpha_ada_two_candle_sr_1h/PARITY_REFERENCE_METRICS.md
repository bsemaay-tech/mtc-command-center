# Parity Reference Metrics — QL_ALPHA_ADA_TWO_CANDLE_SR_1H

- Engine strategy: `QL_2026-05-01_SP500_5M_TWO_CANDLE_SENTIMENT_SR`  | Symbol/TF: ADAUSDT 1h  | direction: long-only
- Params: `{"level_lookback":200,"upper_third":0.6,"break_buf_atr":0.0,"atr_len":14,"stop_lookback_bars":2,"target_R":2.0,"cost_bps_round_trip":8.0,"max_hold_bars":96}`
- Full-history trades emitted: 235  | lockbox bars: 13670

| Metric | Engine (recomputed) | Recorded (spec) | Match |
|---|---|---|---|
| compound_return_pct | 79.233 | 79.23 | OK |
| profit_factor | 1.721 | 1.721 | OK |
| trades | 53 | 53 | OK |
| max_drawdown_pct | -14.156 | -14.16 | OK |
| win_rate | 0.4906 | 0.4906 | OK |
| expectancy_R | 0.4401 | 0.44 | OK |

**Overall:** VERIFIED — reference reproduces recorded lockbox metrics.
