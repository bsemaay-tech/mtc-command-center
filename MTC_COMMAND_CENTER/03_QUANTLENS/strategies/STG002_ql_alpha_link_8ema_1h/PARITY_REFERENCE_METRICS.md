# Parity Reference Metrics — QL_ALPHA_LINK_8EMA_1H

- Engine strategy: `QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL`  | Symbol/TF: LINKUSDT 1h  | direction: long-only
- Params: `{"pullback_atr":0.5,"impulse_atr":1.6,"slope_window":3,"ema_len":8,"atr_len":14,"stop_lookback_bars":3,"cost_bps_round_trip":8.0,"max_hold_bars":96}`
- Full-history trades emitted: 444  | lockbox bars: 13754

| Metric | Engine (recomputed) | Recorded (spec) | Match |
|---|---|---|---|
| compound_return_pct | 75.374 | 75.37 | OK |
| profit_factor | 2.038 | 2.038 | OK |
| trades | 121 | 121 | OK |
| max_drawdown_pct | -16.308 | -16.31 | OK |
| win_rate | 0.3554 | 0.3554 | OK |
| expectancy_R | 0.3376 | 0.338 | OK |

**Overall:** VERIFIED — reference reproduces recorded lockbox metrics.
