# MEGA Rolling Walk-Forward + Deflated Sharpe + Bootstrap-FDR — Overnight Audit

- Generated: `2026-07-05T15:35:21.920299+00:00`
- Runtime: `139.4s` (2.3 min) with `8` worker processes
- Symbols: 17 | Timeframes: ['15m', '1h', '2h', '4h', '1D']
- Strategies: 20 (11 prototyped + 6 generic patterns)
- Param sets total across grids: **1122**
- Total (strategy, symbol, tf) jobs: **420**
- Cost: `8.0 bps` round-trip | Lockbox: last 25% | Rolling folds: 3
- Classification counts: `{'NO_DATA': 21, 'FAIL': 299, 'STRONG_PASS': 16, 'PASS': 42, 'INSUFFICIENT_TRADES': 42}`
- PASS configurations: **58**
- Bootstrap-FDR family size (testable lockboxes): **357** | BH q=0.10 | threshold p≤0.00000
- BH-FDR survivors: **0** | DSR-robust (p≥0.95): **0**
- **FINAL ROBUST (PASS ∧ BH-FDR ∧ DSR): 0**

## Methodology note

Three independent gates must ALL pass for `robust_final`:
1. **Rolling walk-forward** — best param chosen on train folds; profitable on a 25% locked-box OOS slice never seen in selection; positive in ≥ half of forward folds.
2. **Bootstrap significance** — 2000-resample one-sided bootstrap that lockbox mean-R > 0, then **Benjamini-Hochberg FDR (q=0.10)** across ALL testable cells to control multiple-testing.
3. **Deflated Sharpe Ratio** — Bailey & López de Prado, per-trade Sharpe deflated by the expected max across the grid's parameter trials; p ≥ 0.95.

## FINAL ROBUST Survivors (all three gates)

| Strategy | Symbol | TF | Best Params | Lockbox Ret % | Sharpe | Boot p | DSR p | Trades | PF | Max DD % | Folds+ | Class |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| _(none survived all three gates)_ | | | | | | | | | | | | |

## Bootstrap-FDR Survivors (gate 1+2, DSR aside)

| Strategy | Sym | TF | Lockbox Ret % | Sharpe | Boot p | DSR p | Trades | PF | Folds+ | Class |
|---|---|---|---|---|---|---|---|---|---|---|

## All PASS / STRONG_PASS (no multiplicity filter)

| Strategy | Sym | TF | Lockbox Ret % | Sharpe | Boot p | DSR p | Trades | PF | MaxDD % | Folds+ | Class |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `GEN_RSI_OVERSOLD_REVERSAL` | TSLA | 10m | 93.29 | 1.71 | 0.0905 | 0.0 | 290 | 1.45 | -16.40 | 2/2 | STRONG_PASS |
| `GEN_DONCHIAN_BREAKOUT` | NVDA | 10m | 79.39 | 1.77 | 0.028 | 0.2326 | 244 | 1.406 | -13.63 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_ANY_1H_RSI_CONFLUENCE_PL` | NVDA | 10m | 75.35 | 1.80 | 0.042 | 0.0723 | 266 | 1.462 | -16.03 | 2/2 | STRONG_PASS |
| `GEN_RSI_OVERSOLD_REVERSAL` | NVDA | 10m | 70.71 | 1.71 | 0.009 | 0.0 | 282 | 1.395 | -19.25 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_ANY_1H_RSI_CONFLUENCE_PL` | TSLA | 10m | 64.39 | 1.75 | 0.024 | 0.132 | 207 | 1.377 | -23.39 | 2/2 | STRONG_PASS |
| `GEN_DONCHIAN_BREAKOUT` | TSLA | 10m | 55.35 | 1.21 | 0.0825 | 0.1844 | 173 | 1.267 | -25.63 | 2/2 | PASS |
| `QL_2026-05-01_SP500_5M_TWO_CANDLE_SENT` | NVDA | 10m | 51.94 | 1.77 | 0.0805 | 0.3104 | 142 | 1.538 | -15.56 | 2/2 | STRONG_PASS |
| `GEN_MACD_BULL_CROSS` | NVDA | 10m | 51.54 | 1.53 | 0.037 | 0.2645 | 182 | 1.436 | -17.84 | 2/2 | STRONG_PASS |
| `GEN_ATR_PULLBACK_TREND` | NVDA | 10m | 51.33 | 1.44 | 0.022 | 0.0 | 234 | 1.352 | -19.01 | 2/2 | STRONG_PASS |
| `GEN_DONCHIAN_BREAKOUT` | TSLA | 10m | 49.17 | 1.15 | 0.009 | 0.1547 | 182 | 1.304 | -24.53 | 2/2 | STRONG_PASS |
| `GEN_GOLDEN_CROSS_PULLBACK` | NVDA | 10m | 42.54 | 1.38 | 0.004 | 0.0001 | 259 | 1.384 | -17.53 | 2/2 | STRONG_PASS |
| `GEN_MACD_BULL_CROSS` | TSLA | 10m | 41.20 | 1.10 | 0.0515 | 0.1585 | 173 | 1.35 | -15.72 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_ANY_1H_RSI_CONFLUENCE_PL` | AAPL | 10m | 38.48 | 1.42 | 0.0135 | 0.0299 | 274 | 1.346 | -13.70 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_ANY_BOLLINGER_BANDS_20_2` | NVDA | 10m | 35.05 | 1.23 | 0.05 | 0.3756 | 144 | 1.352 | -13.44 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_LIQUID_INTRADAY_VWAP_PUL` | NVDA | 10m | 30.98 | 1.06 | 0.005 | 0.0004 | 247 | 1.241 | -14.95 | 2/2 | PASS |
| `GEN_STOCH_OVERSOLD_CROSS` | TSLA | 10m | 25.07 | 0.83 | 0.049 | 0.1052 | 187 | 1.27 | -18.60 | 2/2 | PASS |
| `QL_2026-05-01_SP500_5M_TWO_CANDLE_SENT` | TSLA | 10m | 24.75 | 0.75 | 0.0615 | 0.0364 | 180 | 1.204 | -25.48 | 2/2 | PASS |
| `QL_2026-05-01_UNKNOWN_MULTI_EMA_CHANNE` | NVDA | 10m | 22.80 | 1.05 | 0.08 | 0.0 | 209 | 1.304 | -12.29 | 2/2 | STRONG_PASS |
| `GEN_STOCH_OVERSOLD_CROSS` | NVDA | 10m | 21.64 | 0.94 | 0.043 | 0.1236 | 190 | 1.268 | -15.22 | 2/2 | PASS |
| `QL_2026-05-01_US_EQUITIES_10M_8EMA_PUL` | NVDA | 10m | 20.98 | 0.76 | 0.02 | 0.0 | 383 | 1.15 | -22.15 | 2/2 | PASS |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_LE_` | NVDA | 10m | 20.98 | 0.76 | 0.0215 | 0.0 | 383 | 1.15 | -22.15 | 2/2 | PASS |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_PUR` | NVDA | 10m | 20.98 | 0.76 | 0.026 | 0.0 | 383 | 1.15 | -22.15 | 2/2 | PASS |
| `GEN_MACD_BULL_CROSS` | TSLA | 10m | 20.76 | 0.79 | 0.095 | 0.1092 | 159 | 1.175 | -14.21 | 2/2 | PASS |
| `GEN_DONCHIAN_BREAKOUT` | NVDA | 10m | 19.66 | 0.75 | 0.401 | 0.1733 | 111 | 1.199 | -17.98 | 2/2 | PASS |
| `GEN_KELTNER_BREAKOUT` | NVDA | 10m | 19.06 | 0.76 | 0.294 | 0.2271 | 127 | 1.201 | -27.98 | 2/2 | PASS |
| `QL_2026-05-01_ANY_CANDLESTICK_7_PATTER` | NVDA | 10m | 18.20 | 0.85 | 0.0975 | 0.0 | 142 | 1.313 | -12.04 | 2/2 | STRONG_PASS |
| `GEN_KELTNER_BREAKOUT` | AAPL | 10m | 17.54 | 0.86 | 0.1645 | 0.2197 | 149 | 1.236 | -12.03 | 2/2 | PASS |
| `GEN_GOLDEN_CROSS_PULLBACK` | TSLA | 10m | 16.84 | 0.61 | 0.237 | 0.0 | 228 | 1.187 | -20.57 | 2/2 | PASS |
| `GEN_GOLDEN_CROSS_PULLBACK` | QQQ | 10m | 16.25 | 1.49 | 0.021 | 0.0236 | 123 | 1.634 | -4.23 | 2/2 | STRONG_PASS |
| `GEN_DONCHIAN_BREAKOUT` | AAPL | 10m | 15.95 | 0.74 | 0.1095 | 0.0773 | 183 | 1.166 | -14.79 | 2/2 | PASS |
| `QL_2026-05-01_UNKNOWN_MULTI_EMA_CHANNE` | QQQ | 10m | 12.94 | 0.99 | 0.004 | 0.0 | 247 | 1.239 | -8.82 | 2/2 | PASS |
| `GEN_KELTNER_BREAKOUT` | NVDA | 10m | 11.71 | 0.56 | 0.387 | 0.1487 | 143 | 1.15 | -22.77 | 2/2 | PASS |
| `QL_2026-05-01_US_EQUITIES_10M_8EMA_PUL` | TSLA | 10m | 10.14 | 0.46 | 0.3045 | 0.0 | 257 | 1.116 | -23.13 | 2/2 | PASS |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_LE_` | TSLA | 10m | 10.14 | 0.46 | 0.3155 | 0.0 | 257 | 1.116 | -23.13 | 2/2 | PASS |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_PUR` | TSLA | 10m | 10.14 | 0.46 | 0.3115 | 0.0 | 257 | 1.116 | -23.13 | 2/2 | PASS |
| `QL_2026-05-01_SP500_5M_TWO_CANDLE_SENT` | TSLA | 10m | 9.95 | 0.59 | 0.2155 | 0.0318 | 166 | 1.152 | -12.31 | 2/2 | PASS |
| `QL_2026-05-01_UNKNOWN_MULTI_EMA_CHANNE` | TSLA | 10m | 9.70 | 0.49 | 0.1385 | 0.0 | 297 | 1.077 | -17.03 | 2/2 | PASS |
| `QL_2026-05-01_LIQUID_INTRADAY_VWAP_PUL` | NVDA | 10m | 8.76 | 0.52 | 0.4075 | 0.0612 | 55 | 1.194 | -10.09 | 2/2 | PASS |
| `GEN_TRIPLE_EMA_STACK` | NVDA | 10m | 8.73 | 0.51 | 0.1305 | 0.0385 | 157 | 1.155 | -17.21 | 2/2 | PASS |
| `QL_2026-05-01_ANY_BOLLINGER_BANDS_20_2` | QQQ | 10m | 8.65 | 0.78 | 0.0705 | 0.2866 | 109 | 1.242 | -7.05 | 2/2 | PASS |
| `QL_2026-05-01_UNKNOWN_MULTI_EMA_CHANNE` | AAPL | 10m | 8.42 | 0.55 | 0.022 | 0.0 | 230 | 1.137 | -7.80 | 2/2 | PASS |
| `QL_2026-05-01_ANY_BOLLINGER_BANDS_20_2` | NVDA | 10m | 7.70 | 0.50 | 0.2205 | 0.3359 | 52 | 1.22 | -9.94 | 2/2 | PASS |
| `QL_2026-05-01_US_EQUITIES_10M_8EMA_PUL` | AAPL | 10m | 6.82 | 0.39 | 0.312 | 0.0 | 432 | 1.072 | -13.96 | 2/2 | PASS |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_LE_` | AAPL | 10m | 6.82 | 0.39 | 0.3135 | 0.0 | 432 | 1.072 | -13.96 | 2/2 | PASS |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_PUR` | AAPL | 10m | 6.82 | 0.39 | 0.293 | 0.0 | 432 | 1.072 | -13.96 | 2/2 | PASS |
| `QL_2026-05-01_LIQUID_INTRADAY_VWAP_PUL` | MSFT | 10m | 5.97 | 0.58 | 0.0655 | 0.0457 | 66 | 1.184 | -7.92 | 2/2 | PASS |
| `GEN_GOLDEN_CROSS_PULLBACK` | AAPL | 10m | 5.54 | 0.39 | 0.059 | 0.0 | 249 | 1.099 | -13.83 | 2/2 | PASS |
| `QL_2026-05-01_ANY_BOLLINGER_BANDS_20_2` | SPY | 10m | 5.33 | 0.71 | 0.2515 | 0.2723 | 104 | 1.214 | -6.58 | 2/2 | PASS |
| `GEN_DONCHIAN_BREAKOUT` | QQQ | 10m | 4.73 | 0.36 | 0.164 | 0.0563 | 148 | 1.085 | -14.03 | 2/2 | PASS |
| `GEN_DONCHIAN_BREAKOUT` | AMZN | 10m | 3.78 | 0.27 | 0.163 | 0.0237 | 198 | 1.058 | -17.25 | 2/2 | PASS |
| `GEN_RSI_OVERSOLD_REVERSAL` | AMZN | 10m | 3.10 | 0.31 | 0.0865 | 0.0 | 66 | 1.103 | -8.53 | 2/2 | PASS |
| `GEN_DONCHIAN_BREAKOUT` | AMZN | 10m | 2.03 | 0.20 | 0.271 | 0.0223 | 190 | 1.038 | -15.56 | 2/2 | PASS |
| `GEN_RSI_OVERSOLD_REVERSAL` | AAPL | 10m | 1.87 | 0.21 | 0.1725 | 0.0 | 75 | 1.064 | -12.51 | 2/2 | PASS |
| `QL_2026-05-01_ANY_BOLLINGER_BANDS_20_2` | QQQ | 10m | 1.70 | 0.20 | 0.3545 | 0.126 | 109 | 1.056 | -9.14 | 2/2 | PASS |
| `QL_2026-05-01_SP500_5M_TWO_CANDLE_SENT` | SPY | 10m | 1.28 | 0.19 | 0.0925 | 0.0094 | 179 | 1.043 | -6.50 | 2/2 | PASS |
| `GEN_KELTNER_BREAKOUT` | NVDA | 10m | 0.73 | 0.12 | 0.23 | 0.102 | 108 | 1.033 | -14.01 | 2/2 | PASS |
| `QL_2026-05-01_SP500_5M_TWO_CANDLE_SENT` | TSLA | 10m | 0.64 | 0.17 | 0.1245 | 0.0282 | 120 | 1.042 | -20.25 | 2/2 | PASS |
| `GEN_KELTNER_BREAKOUT` | SPY | 10m | 0.46 | 0.10 | 0.0975 | 0.0593 | 153 | 1.023 | -9.58 | 2/2 | PASS |

## Per-Strategy Top 3 PASS configurations

### `GEN_ATR_PULLBACK_TREND`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| NVDA | 10m | `{"ema_len":20,"dist_atr":1.0,"slope_atr":0.25,"stop_lookback":10}` | 51.33 | 1.44 | 0.0 | 234 | 1.352 | 2/2 |

### `GEN_DONCHIAN_BREAKOUT`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| NVDA | 10m | `{"channel_len":10,"atr_buf":0.1,"stop_lookback":5}` | 79.39 | 1.77 | 0.2326 | 244 | 1.406 | 2/2 |
| TSLA | 10m | `{"channel_len":10,"atr_buf":0.5,"stop_lookback":5}` | 55.35 | 1.21 | 0.1844 | 173 | 1.267 | 2/2 |
| TSLA | 10m | `{"channel_len":10,"atr_buf":0.5,"stop_lookback":5}` | 49.17 | 1.15 | 0.1547 | 182 | 1.304 | 2/2 |

### `GEN_GOLDEN_CROSS_PULLBACK`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| NVDA | 10m | `{"fast_ema":20,"slow_ema":200,"pull_atr":0.6,"stop_lookback":5}` | 42.54 | 1.38 | 0.0001 | 259 | 1.384 | 2/2 |
| TSLA | 10m | `{"fast_ema":20,"slow_ema":200,"pull_atr":0.6,"stop_lookback":5}` | 16.84 | 0.61 | 0.0 | 228 | 1.187 | 2/2 |
| QQQ | 10m | `{"fast_ema":50,"slow_ema":150,"pull_atr":0.25,"stop_lookback":5}` | 16.25 | 1.49 | 0.0236 | 123 | 1.634 | 2/2 |

### `GEN_KELTNER_BREAKOUT`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| NVDA | 10m | `{"ema_len":50,"atr_len":20,"mult":1.5}` | 19.06 | 0.76 | 0.2271 | 127 | 1.201 | 2/2 |
| AAPL | 10m | `{"ema_len":50,"atr_len":20,"mult":1.5}` | 17.54 | 0.86 | 0.2197 | 149 | 1.236 | 2/2 |
| NVDA | 10m | `{"ema_len":50,"atr_len":10,"mult":2.0}` | 11.71 | 0.56 | 0.1487 | 143 | 1.15 | 2/2 |

### `GEN_MACD_BULL_CROSS`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| NVDA | 10m | `{"fast":8,"slow":34,"signal":5}` | 51.54 | 1.53 | 0.2645 | 182 | 1.436 | 2/2 |
| TSLA | 10m | `{"fast":8,"slow":21,"signal":5}` | 41.20 | 1.10 | 0.1585 | 173 | 1.35 | 2/2 |
| TSLA | 10m | `{"fast":8,"slow":26,"signal":5}` | 20.76 | 0.79 | 0.1092 | 159 | 1.175 | 2/2 |

### `GEN_RSI_OVERSOLD_REVERSAL`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| TSLA | 10m | `{"rsi_len":5,"oversold":35,"recovery":45}` | 93.29 | 1.71 | 0.0 | 290 | 1.45 | 2/2 |
| NVDA | 10m | `{"rsi_len":5,"oversold":35,"recovery":45}` | 70.71 | 1.71 | 0.0 | 282 | 1.395 | 2/2 |
| AMZN | 10m | `{"rsi_len":7,"oversold":25,"recovery":40}` | 3.10 | 0.31 | 0.0 | 66 | 1.103 | 2/2 |

### `GEN_STOCH_OVERSOLD_CROSS`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| TSLA | 10m | `{"stoch_n":14,"oversold":25,"smooth_d":5}` | 25.07 | 0.83 | 0.1052 | 187 | 1.27 | 2/2 |
| NVDA | 10m | `{"stoch_n":21,"oversold":25,"smooth_d":5}` | 21.64 | 0.94 | 0.1236 | 190 | 1.268 | 2/2 |

### `GEN_TRIPLE_EMA_STACK`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| NVDA | 10m | `{"touch_atr":0.3,"stop_lookback":10}` | 8.73 | 0.51 | 0.0385 | 157 | 1.155 | 2/2 |

### `QL_2026-05-01_ANY_1H_RSI_CONFLUENCE_PLAYBOOK`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| NVDA | 10m | `{"rsi_len":5,"sma_len":20,"cross_lvl":45}` | 75.35 | 1.80 | 0.0723 | 266 | 1.462 | 2/2 |
| TSLA | 10m | `{"rsi_len":9,"sma_len":20,"cross_lvl":45}` | 64.39 | 1.75 | 0.132 | 207 | 1.377 | 2/2 |
| AAPL | 10m | `{"rsi_len":5,"sma_len":20,"cross_lvl":45}` | 38.48 | 1.42 | 0.0299 | 274 | 1.346 | 2/2 |

### `QL_2026-05-01_ANY_BOLLINGER_BANDS_20_2_TRI_SETUP`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| NVDA | 10m | `{"width_quantile":0.35,"body_atr":0.2,"bb_len":20}` | 35.05 | 1.23 | 0.3756 | 144 | 1.352 | 2/2 |
| QQQ | 10m | `{"width_quantile":0.25,"body_atr":0.45,"bb_len":20}` | 8.65 | 0.78 | 0.2866 | 109 | 1.242 | 2/2 |
| NVDA | 10m | `{"width_quantile":0.05,"body_atr":0.1,"bb_len":20}` | 7.70 | 0.50 | 0.3359 | 52 | 1.22 | 2/2 |

### `QL_2026-05-01_ANY_CANDLESTICK_7_PATTERN_PA_CONFLUENCE`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| NVDA | 10m | `{"level_lookback":24,"tolerance_atr":0.5,"atr_stop_mult":0.05}` | 18.20 | 0.85 | 0.0 | 142 | 1.313 | 2/2 |

### `QL_2026-05-01_LIQUID_INTRADAY_VWAP_PULLBACK_REVERSAL`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| NVDA | 10m | `{"session_window":24,"prox_atr":0.75,"slope_window":3}` | 30.98 | 1.06 | 0.0004 | 247 | 1.241 | 2/2 |
| NVDA | 10m | `{"session_window":200,"prox_atr":0.55,"slope_window":3}` | 8.76 | 0.52 | 0.0612 | 55 | 1.194 | 2/2 |
| MSFT | 10m | `{"session_window":144,"prox_atr":0.75,"slope_window":3}` | 5.97 | 0.58 | 0.0457 | 66 | 1.184 | 2/2 |

### `QL_2026-05-01_SP500_5M_TWO_CANDLE_SENTIMENT_SR`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| NVDA | 10m | `{"level_lookback":24,"upper_third":0.85,"break_buf_atr":0.0}` | 51.94 | 1.77 | 0.3104 | 142 | 1.538 | 2/2 |
| TSLA | 10m | `{"level_lookback":24,"upper_third":0.66,"break_buf_atr":0.0}` | 24.75 | 0.75 | 0.0364 | 180 | 1.204 | 2/2 |
| TSLA | 10m | `{"level_lookback":48,"upper_third":0.66,"break_buf_atr":0.0}` | 9.95 | 0.59 | 0.0318 | 166 | 1.152 | 2/2 |

### `QL_2026-05-01_UNKNOWN_MULTI_EMA_CHANNEL_PULLBACK`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| NVDA | 10m | `{"touch_atr":0.55,"short_ema":5,"long_ema":13}` | 22.80 | 1.05 | 0.0 | 209 | 1.304 | 2/2 |
| QQQ | 10m | `{"touch_atr":1.0,"short_ema":8,"long_ema":13}` | 12.94 | 0.99 | 0.0 | 247 | 1.239 | 2/2 |
| TSLA | 10m | `{"touch_atr":1.0,"short_ema":3,"long_ema":13}` | 9.70 | 0.49 | 0.0 | 297 | 1.077 | 2/2 |

### `QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| NVDA | 10m | `{"pullback_atr":0.65,"impulse_atr":0.8,"slope_window":3}` | 20.98 | 0.76 | 0.0 | 383 | 1.15 | 2/2 |
| TSLA | 10m | `{"pullback_atr":0.65,"impulse_atr":1.3,"slope_window":3}` | 10.14 | 0.46 | 0.0 | 257 | 1.116 | 2/2 |
| AAPL | 10m | `{"pullback_atr":0.65,"impulse_atr":0.5,"slope_window":3}` | 6.82 | 0.39 | 0.0 | 432 | 1.072 | 2/2 |

### `QL_2026-05-01_US_EQUITIES_INTRADAY_LE_MODEL_BULL_FLAG`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| NVDA | 10m | `{"pullback_atr":0.65,"impulse_atr":0.8,"slope_window":3}` | 20.98 | 0.76 | 0.0 | 383 | 1.15 | 2/2 |
| TSLA | 10m | `{"pullback_atr":0.65,"impulse_atr":1.3,"slope_window":3}` | 10.14 | 0.46 | 0.0 | 257 | 1.116 | 2/2 |
| AAPL | 10m | `{"pullback_atr":0.65,"impulse_atr":0.5,"slope_window":3}` | 6.82 | 0.39 | 0.0 | 432 | 1.072 | 2/2 |

### `QL_2026-05-01_US_EQUITIES_INTRADAY_PURPLE_PROFITS`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| NVDA | 10m | `{"pullback_atr":0.65,"impulse_atr":0.8,"slope_window":3}` | 20.98 | 0.76 | 0.0 | 383 | 1.15 | 2/2 |
| TSLA | 10m | `{"pullback_atr":0.65,"impulse_atr":1.3,"slope_window":3}` | 10.14 | 0.46 | 0.0 | 257 | 1.116 | 2/2 |
| AAPL | 10m | `{"pullback_atr":0.65,"impulse_atr":0.5,"slope_window":3}` | 6.82 | 0.39 | 0.0 | 432 | 1.072 | 2/2 |

