# MEGA Rolling Walk-Forward + Deflated Sharpe + Bootstrap-FDR — Overnight Audit

- Generated: `2026-07-05T15:36:32.604014+00:00`
- Runtime: `39.3s` (0.7 min) with `8` worker processes
- Symbols: 17 | Timeframes: ['15m', '1h', '2h', '4h', '1D']
- Strategies: 20 (11 prototyped + 6 generic patterns)
- Param sets total across grids: **1122**
- Total (strategy, symbol, tf) jobs: **560**
- Cost: `8.0 bps` round-trip | Lockbox: last 25% | Rolling folds: 3
- Classification counts: `{'NO_DATA': 28, 'INSUFFICIENT_TRADES': 266, 'FAIL': 187, 'PASS': 33, 'STRONG_PASS': 46}`
- PASS configurations: **79**
- Bootstrap-FDR family size (testable lockboxes): **266** | BH q=0.10 | threshold p≤0.00000
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
| `GEN_RSI_OVERSOLD_REVERSAL` | AAPL | 1h | 64.90 | 2.69 | 0.0045 | 0.9324 | 34 | 3.454 | -3.62 | 2/2 | STRONG_PASS |
| `GEN_RSI_OVERSOLD_REVERSAL` | AAPL | 1h | 61.23 | 1.92 | 0.0685 | 0.7542 | 42 | 2.684 | -6.60 | 2/2 | STRONG_PASS |
| `GEN_RSI_OVERSOLD_REVERSAL` | AAPL | 1h | 42.22 | 2.25 | 0.006 | 0.8376 | 43 | 2.382 | -5.99 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_ANY_1H_RSI_CONFLUENCE_PL` | NVDA | 1h | 42.17 | 1.84 | 0.245 | 0.4164 | 63 | 2.15 | -11.33 | 2/2 | PASS |
| `GEN_ATR_PULLBACK_TREND` | AAPL | 1h | 38.45 | 1.85 | 0.025 | 0.7818 | 35 | 3.378 | -3.85 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_US_EQUITIES_10M_8EMA_PUL` | QQQ | 1h | 36.34 | 1.34 | 0.022 | 0.781 | 56 | 2.096 | -9.40 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_LE_` | QQQ | 1h | 36.34 | 1.34 | 0.026 | 0.781 | 56 | 2.096 | -9.40 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_PUR` | QQQ | 1h | 36.34 | 1.34 | 0.0195 | 0.781 | 56 | 2.096 | -9.40 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_ANY_1H_RSI_CONFLUENCE_PL` | AMZN | 1h | 35.09 | 1.62 | 0.1975 | 0.5165 | 37 | 2.15 | -6.13 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_ANY_1H_RSI_CONFLUENCE_PL` | NVDA | 1h | 33.71 | 1.06 | 0.297 | 0.3305 | 34 | 1.73 | -12.41 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_UNKNOWN_MULTI_EMA_CHANNE` | AMZN | 1h | 32.66 | 1.16 | 0.114 | 0.2993 | 33 | 2.609 | -10.33 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_US_EQUITIES_10M_8EMA_PUL` | TSLA | 1h | 30.74 | 0.80 | 0.1665 | 0.5759 | 66 | 1.439 | -28.58 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_LE_` | TSLA | 1h | 30.74 | 0.80 | 0.1805 | 0.5759 | 66 | 1.439 | -28.58 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_PUR` | TSLA | 1h | 30.74 | 0.80 | 0.1855 | 0.5759 | 66 | 1.439 | -28.58 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_ANY_1H_RSI_CONFLUENCE_PL` | TSLA | 1h | 29.33 | 0.90 | 0.0425 | 0.0949 | 74 | 1.475 | -23.44 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_UNKNOWN_MULTI_EMA_CHANNE` | AMZN | 1h | 28.54 | 1.32 | 0.047 | 0.1783 | 58 | 2.634 | -6.27 | 2/2 | STRONG_PASS |
| `GEN_MACD_BULL_CROSS` | QQQ | 1h | 27.12 | 1.58 | 0.2395 | 0.7854 | 37 | 1.958 | -9.10 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_LIQUID_INTRADAY_VWAP_PUL` | AAPL | 1h | 26.25 | 1.39 | 0.0555 | 0.081 | 37 | 1.762 | -5.83 | 2/2 | STRONG_PASS |
| `GEN_DONCHIAN_BREAKOUT` | AAPL | 1h | 22.08 | 1.03 | 0.262 | 0.4302 | 31 | 1.545 | -10.84 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_SP500_5M_TWO_CANDLE_SENT` | TSLA | 1h | 21.96 | 0.89 | 0.238 | 0.1529 | 35 | 1.613 | -14.00 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_UNKNOWN_MULTI_EMA_CHANNE` | AAPL | 1h | 20.50 | 1.39 | 0.0975 | 0.3707 | 34 | 1.884 | -9.58 | 2/2 | STRONG_PASS |
| `GEN_ATR_PULLBACK_TREND` | SPY | 1h | 20.17 | 1.22 | 0.071 | 0.5873 | 32 | 2.262 | -9.12 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_SP500_5M_TWO_CANDLE_SENT` | QQQ | 1h | 20.02 | 1.94 | 0.002 | 0.4397 | 41 | 2.356 | -4.43 | 2/2 | STRONG_PASS |
| `GEN_KELTNER_BREAKOUT` | AAPL | 1h | 19.04 | 1.36 | 0.164 | 0.6201 | 49 | 1.873 | -6.83 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_UNKNOWN_MULTI_EMA_CHANNE` | SPY | 1h | 18.87 | 1.67 | 0.0155 | 0.4586 | 36 | 2.507 | -6.36 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_ANY_1H_RSI_CONFLUENCE_PL` | AAPL | 1h | 18.74 | 0.99 | 0.3505 | 0.3378 | 30 | 1.664 | -5.39 | 2/2 | STRONG_PASS |
| `GEN_KELTNER_BREAKOUT` | QQQ | 1h | 17.32 | 1.19 | 0.259 | 0.6302 | 32 | 1.767 | -6.76 | 2/2 | STRONG_PASS |
| `GEN_DONCHIAN_BREAKOUT` | NVDA | 1h | 17.24 | 0.64 | 0.3175 | 0.2871 | 31 | 1.32 | -25.32 | 2/2 | STRONG_PASS |
| `GEN_ATR_PULLBACK_TREND` | AMZN | 1h | 16.18 | 0.73 | 0.1225 | 0.1166 | 120 | 1.337 | -11.75 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_US_EQUITIES_10M_8EMA_PUL` | AAPL | 1h | 16.00 | 0.84 | 0.329 | 0.612 | 56 | 1.538 | -8.01 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_LE_` | AAPL | 1h | 16.00 | 0.84 | 0.311 | 0.612 | 56 | 1.538 | -8.01 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_PUR` | AAPL | 1h | 16.00 | 0.84 | 0.3065 | 0.612 | 56 | 1.538 | -8.01 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_US_EQUITIES_10M_8EMA_PUL` | NVDA | 1h | 15.48 | 0.66 | 0.066 | 0.4791 | 93 | 1.211 | -22.65 | 2/2 | PASS |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_LE_` | NVDA | 1h | 15.48 | 0.66 | 0.067 | 0.4791 | 93 | 1.211 | -22.65 | 2/2 | PASS |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_PUR` | NVDA | 1h | 15.48 | 0.66 | 0.073 | 0.4791 | 93 | 1.211 | -22.65 | 2/2 | PASS |
| `QL_2026-05-01_SP500_5M_TWO_CANDLE_SENT` | AAPL | 1h | 15.42 | 1.23 | 0.166 | 0.2543 | 34 | 1.904 | -6.84 | 2/2 | STRONG_PASS |
| `GEN_ATR_PULLBACK_TREND` | MSFT | 1h | 14.58 | 0.86 | 0.06 | 0.3968 | 41 | 1.511 | -10.76 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_UNKNOWN_MULTI_EMA_CHANNE` | AAPL | 1h | 13.47 | 1.12 | 0.21 | 0.2044 | 44 | 1.525 | -4.96 | 2/2 | STRONG_PASS |
| `GEN_KELTNER_BREAKOUT` | SPY | 1h | 13.23 | 1.40 | 0.094 | 0.7123 | 30 | 1.986 | -4.00 | 2/2 | STRONG_PASS |
| `GEN_STOCH_OVERSOLD_CROSS` | TSLA | 1h | 13.20 | 0.49 | 0.211 | 0.3632 | 30 | 1.531 | -14.03 | 2/2 | STRONG_PASS |
| `GEN_MACD_BULL_CROSS` | AAPL | 1h | 12.71 | 0.67 | 0.2675 | 0.4944 | 30 | 1.5 | -10.46 | 2/2 | STRONG_PASS |
| `GEN_ATR_PULLBACK_TREND` | QQQ | 1h | 12.27 | 0.76 | 0.054 | 0.4023 | 33 | 1.436 | -16.21 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_SP500_5M_TWO_CANDLE_SENT` | NVDA | 1h | 11.53 | 0.60 | 0.1285 | 0.061 | 44 | 1.311 | -12.39 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_ANY_1H_RSI_CONFLUENCE_PL` | AAPL | 1h | 11.26 | 0.70 | 0.31 | 0.1451 | 47 | 1.305 | -8.09 | 2/2 | PASS |
| `GEN_MACD_BULL_CROSS` | AMZN | 1h | 10.78 | 0.50 | 0.3075 | 0.4288 | 30 | 1.384 | -12.21 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_ANY_1H_RSI_CONFLUENCE_PL` | TSLA | 1h | 10.38 | 0.50 | 0.104 | 0.1549 | 35 | 1.228 | -13.18 | 2/2 | PASS |
| `QL_2026-05-01_SP500_5M_TWO_CANDLE_SENT` | SPY | 1h | 9.73 | 1.32 | 0.0635 | 0.2942 | 33 | 1.85 | -2.88 | 2/2 | STRONG_PASS |
| `GEN_STOCH_OVERSOLD_CROSS` | NVDA | 1h | 9.40 | 0.53 | 0.1935 | 0.3671 | 32 | 1.371 | -11.78 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_ANY_1H_RSI_CONFLUENCE_PL` | NVDA | 1h | 8.89 | 0.45 | 0.489 | 0.0827 | 51 | 1.165 | -15.12 | 2/2 | PASS |
| `GEN_GOLDEN_CROSS_PULLBACK` | AAPL | 1h | 8.81 | 1.13 | 0.0585 | 0.3057 | 55 | 1.709 | -3.42 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_SP500_5M_TWO_CANDLE_SENT` | QQQ | 1h | 8.67 | 1.09 | 0.0895 | 0.157 | 42 | 1.769 | -3.94 | 2/2 | STRONG_PASS |
| `GEN_ATR_PULLBACK_TREND` | AAPL | 1h | 7.88 | 0.71 | 0.103 | 0.279 | 55 | 1.354 | -3.85 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_US_EQUITIES_10M_8EMA_PUL` | QQQ | 1h | 7.78 | 0.65 | 0.0295 | 0.4557 | 105 | 1.249 | -8.62 | 2/2 | PASS |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_LE_` | QQQ | 1h | 7.78 | 0.65 | 0.0295 | 0.4557 | 105 | 1.249 | -8.62 | 2/2 | PASS |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_PUR` | QQQ | 1h | 7.78 | 0.65 | 0.026 | 0.4557 | 105 | 1.249 | -8.62 | 2/2 | PASS |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_8EM` | QQQ | 1h | 7.78 | 0.65 | 0.0235 | 0.6487 | 105 | 1.249 | -8.62 | 2/2 | PASS |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_8EM` | QQQ | 1h | 7.78 | 0.65 | 0.0235 | 0.6487 | 105 | 1.249 | -8.62 | 2/2 | PASS |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_8EM` | QQQ | 1h | 7.78 | 0.65 | 0.0235 | 0.6487 | 105 | 1.249 | -8.62 | 2/2 | PASS |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_8EM` | QQQ | 1h | 7.78 | 0.65 | 0.0235 | 0.6487 | 105 | 1.249 | -8.62 | 2/2 | PASS |
| `QL_2026-05-01_LIQUID_INTRADAY_VWAP_PUL` | MSFT | 1h | 7.55 | 0.57 | 0.0245 | 0.012 | 38 | 1.25 | -10.23 | 2/2 | PASS |
| `GEN_DONCHIAN_BREAKOUT` | AAPL | 1h | 6.75 | 0.46 | 0.396 | 0.0787 | 75 | 1.171 | -11.69 | 2/2 | PASS |
| `GEN_DONCHIAN_BREAKOUT` | NVDA | 1h | 6.70 | 0.36 | 0.307 | 0.0656 | 75 | 1.121 | -19.77 | 2/2 | PASS |
| `GEN_ATR_PULLBACK_TREND` | QQQ | 1h | 6.62 | 0.48 | 0.0995 | 0.257 | 42 | 1.235 | -16.21 | 2/2 | PASS |
| `GEN_MACD_BULL_CROSS` | QQQ | 1h | 6.60 | 0.68 | 0.1735 | 0.3711 | 65 | 1.309 | -7.46 | 2/2 | STRONG_PASS |
| `QL_2026-05-01_UNKNOWN_MULTI_EMA_CHANNE` | AAPL | 1h | 6.59 | 0.48 | 0.4375 | 0.1258 | 31 | 1.352 | -8.58 | 2/2 | PASS |
| `QL_2026-05-01_US_EQUITIES_10M_8EMA_PUL` | NVDA | 1h | 6.40 | 0.34 | 0.454 | 0.4008 | 64 | 1.185 | -21.22 | 2/2 | PASS |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_LE_` | NVDA | 1h | 6.40 | 0.34 | 0.422 | 0.4008 | 64 | 1.185 | -21.22 | 2/2 | PASS |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_PUR` | NVDA | 1h | 6.40 | 0.34 | 0.437 | 0.4008 | 64 | 1.185 | -21.22 | 2/2 | PASS |
| `GEN_MACD_BULL_CROSS` | NVDA | 1h | 5.60 | 0.33 | 0.435 | 0.3624 | 30 | 1.155 | -27.62 | 2/2 | PASS |
| `GEN_ATR_PULLBACK_TREND` | SPY | 1h | 5.34 | 0.47 | 0.212 | 0.2715 | 38 | 1.27 | -10.57 | 2/2 | PASS |
| `GEN_GOLDEN_CROSS_PULLBACK` | AAPL | 1h | 4.15 | 0.47 | 0.07 | 0.1651 | 43 | 1.214 | -9.20 | 2/2 | PASS |
| `GEN_DONCHIAN_BREAKOUT` | NVDA | 1h | 3.93 | 0.29 | 0.207 | 0.1376 | 41 | 1.145 | -25.30 | 2/2 | PASS |
| `GEN_ATR_PULLBACK_TREND` | NVDA | 1h | 3.46 | 0.26 | 0.42 | 0.0371 | 136 | 1.084 | -15.21 | 2/2 | PASS |
| `QL_2026-05-01_LIQUID_INTRADAY_VWAP_PUL` | MSFT | 1h | 1.81 | 0.21 | 0.073 | 0.0025 | 43 | 1.077 | -6.15 | 2/2 | PASS |
| `QL_2026-05-01_SP500_5M_TWO_CANDLE_SENT` | SPY | 1h | 1.76 | 0.28 | 0.3275 | 0.0409 | 39 | 1.144 | -6.00 | 2/2 | PASS |
| `GEN_STOCH_OVERSOLD_CROSS` | AAPL | 1h | 1.28 | 0.19 | 0.3285 | 0.1759 | 53 | 1.075 | -5.29 | 2/2 | PASS |
| `GEN_STOCH_OVERSOLD_CROSS` | NVDA | 1h | 0.78 | 0.12 | 0.4175 | 0.2291 | 32 | 1.056 | -13.40 | 2/2 | PASS |
| `GEN_RSI_OVERSOLD_REVERSAL` | QQQ | 1h | 0.40 | 0.11 | 0.4175 | 0.1456 | 40 | 1.06 | -13.54 | 2/2 | PASS |
| `QL_2026-05-01_SP500_5M_TWO_CANDLE_SENT` | SPY | 1h | 0.12 | 0.05 | 0.2195 | 0.0093 | 55 | 1.022 | -5.12 | 2/2 | PASS |

## Per-Strategy Top 3 PASS configurations

### `GEN_ATR_PULLBACK_TREND`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| AAPL | 1h | `{"ema_len":50,"dist_atr":1.0,"slope_atr":0.1,"stop_lookback":5}` | 38.45 | 1.85 | 0.7818 | 35 | 3.378 | 2/2 |
| SPY | 1h | `{"ema_len":20,"dist_atr":0.75,"slope_atr":0.25,"stop_lookback":10}` | 20.17 | 1.22 | 0.5873 | 32 | 2.262 | 2/2 |
| AMZN | 1h | `{"ema_len":20,"dist_atr":1.0,"slope_atr":0.1,"stop_lookback":5}` | 16.18 | 0.73 | 0.1166 | 120 | 1.337 | 2/2 |

### `GEN_DONCHIAN_BREAKOUT`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| AAPL | 1h | `{"channel_len":20,"atr_buf":0.25,"stop_lookback":5}` | 22.08 | 1.03 | 0.4302 | 31 | 1.545 | 2/2 |
| NVDA | 1h | `{"channel_len":20,"atr_buf":0.25,"stop_lookback":5}` | 17.24 | 0.64 | 0.2871 | 31 | 1.32 | 2/2 |
| AAPL | 1h | `{"channel_len":10,"atr_buf":0.0,"stop_lookback":5}` | 6.75 | 0.46 | 0.0787 | 75 | 1.171 | 2/2 |

### `GEN_GOLDEN_CROSS_PULLBACK`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| AAPL | 1h | `{"fast_ema":20,"slow_ema":100,"pull_atr":0.25,"stop_lookback":5}` | 8.81 | 1.13 | 0.3057 | 55 | 1.709 | 2/2 |
| AAPL | 1h | `{"fast_ema":20,"slow_ema":100,"pull_atr":0.4,"stop_lookback":5}` | 4.15 | 0.47 | 0.1651 | 43 | 1.214 | 2/2 |

### `GEN_KELTNER_BREAKOUT`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| AAPL | 1h | `{"ema_len":50,"atr_len":10,"mult":2.0}` | 19.04 | 1.36 | 0.6201 | 49 | 1.873 | 2/2 |
| QQQ | 1h | `{"ema_len":20,"atr_len":10,"mult":1.5}` | 17.32 | 1.19 | 0.6302 | 32 | 1.767 | 2/2 |
| SPY | 1h | `{"ema_len":50,"atr_len":10,"mult":2.0}` | 13.23 | 1.40 | 0.7123 | 30 | 1.986 | 2/2 |

### `GEN_MACD_BULL_CROSS`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| QQQ | 1h | `{"fast":8,"slow":21,"signal":5}` | 27.12 | 1.58 | 0.7854 | 37 | 1.958 | 2/2 |
| AAPL | 1h | `{"fast":8,"slow":21,"signal":5}` | 12.71 | 0.67 | 0.4944 | 30 | 1.5 | 2/2 |
| AMZN | 1h | `{"fast":12,"slow":26,"signal":5}` | 10.78 | 0.50 | 0.4288 | 30 | 1.384 | 2/2 |

### `GEN_RSI_OVERSOLD_REVERSAL`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| AAPL | 1h | `{"rsi_len":5,"oversold":35,"recovery":45}` | 64.90 | 2.69 | 0.9324 | 34 | 3.454 | 2/2 |
| AAPL | 1h | `{"rsi_len":5,"oversold":25,"recovery":35}` | 61.23 | 1.92 | 0.7542 | 42 | 2.684 | 2/2 |
| AAPL | 1h | `{"rsi_len":5,"oversold":35,"recovery":45}` | 42.22 | 2.25 | 0.8376 | 43 | 2.382 | 2/2 |

### `GEN_STOCH_OVERSOLD_CROSS`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| TSLA | 1h | `{"stoch_n":21,"oversold":20,"smooth_d":3}` | 13.20 | 0.49 | 0.3632 | 30 | 1.531 | 2/2 |
| NVDA | 1h | `{"stoch_n":14,"oversold":20,"smooth_d":3}` | 9.40 | 0.53 | 0.3671 | 32 | 1.371 | 2/2 |
| AAPL | 1h | `{"stoch_n":14,"oversold":20,"smooth_d":3}` | 1.28 | 0.19 | 0.1759 | 53 | 1.075 | 2/2 |

### `QL_2026-05-01_ANY_1H_RSI_CONFLUENCE_PLAYBOOK`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| NVDA | 1h | `{"rsi_len":7,"sma_len":20,"cross_lvl":45}` | 42.17 | 1.84 | 0.4164 | 63 | 2.15 | 2/2 |
| AMZN | 1h | `{"rsi_len":5,"sma_len":100,"cross_lvl":45}` | 35.09 | 1.62 | 0.5165 | 37 | 2.15 | 2/2 |
| NVDA | 1h | `{"rsi_len":7,"sma_len":20,"cross_lvl":45}` | 33.71 | 1.06 | 0.3305 | 34 | 1.73 | 2/2 |

### `QL_2026-05-01_LIQUID_INTRADAY_VWAP_PULLBACK_REVERSAL`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| AAPL | 1h | `{"session_window":24,"prox_atr":0.75,"slope_window":3}` | 26.25 | 1.39 | 0.081 | 37 | 1.762 | 2/2 |
| MSFT | 1h | `{"session_window":24,"prox_atr":0.55,"slope_window":3}` | 7.55 | 0.57 | 0.012 | 38 | 1.25 | 2/2 |
| MSFT | 1h | `{"session_window":24,"prox_atr":0.55,"slope_window":3}` | 1.81 | 0.21 | 0.0025 | 43 | 1.077 | 2/2 |

### `QL_2026-05-01_SP500_5M_TWO_CANDLE_SENTIMENT_SR`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| TSLA | 1h | `{"level_lookback":24,"upper_third":0.55,"break_buf_atr":0.0}` | 21.96 | 0.89 | 0.1529 | 35 | 1.613 | 2/2 |
| QQQ | 1h | `{"level_lookback":48,"upper_third":0.66,"break_buf_atr":0.0}` | 20.02 | 1.94 | 0.4397 | 41 | 2.356 | 2/2 |
| AAPL | 1h | `{"level_lookback":24,"upper_third":0.66,"break_buf_atr":0.0}` | 15.42 | 1.23 | 0.2543 | 34 | 1.904 | 2/2 |

### `QL_2026-05-01_UNKNOWN_MULTI_EMA_CHANNEL_PULLBACK`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| AMZN | 1h | `{"touch_atr":1.0,"short_ema":8,"long_ema":13}` | 32.66 | 1.16 | 0.2993 | 33 | 2.609 | 2/2 |
| AMZN | 1h | `{"touch_atr":0.75,"short_ema":8,"long_ema":13}` | 28.54 | 1.32 | 0.1783 | 58 | 2.634 | 2/2 |
| AAPL | 1h | `{"touch_atr":0.75,"short_ema":3,"long_ema":13}` | 20.50 | 1.39 | 0.3707 | 34 | 1.884 | 2/2 |

### `QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| QQQ | 1h | `{"pullback_atr":0.65,"impulse_atr":0.5,"slope_window":3}` | 36.34 | 1.34 | 0.781 | 56 | 2.096 | 2/2 |
| TSLA | 1h | `{"pullback_atr":0.65,"impulse_atr":0.5,"slope_window":3}` | 30.74 | 0.80 | 0.5759 | 66 | 1.439 | 2/2 |
| AAPL | 1h | `{"pullback_atr":0.65,"impulse_atr":1.0,"slope_window":3}` | 16.00 | 0.84 | 0.612 | 56 | 1.538 | 2/2 |

### `QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| QQQ | 1h | `{"pullback_atr":0.65,"impulse_atr":0.5,"slope_window":3}` | 7.78 | 0.65 | 0.6487 | 105 | 1.249 | 2/2 |
| QQQ | 1h | `{"pullback_atr":0.65,"impulse_atr":0.5,"slope_window":3}` | 7.78 | 0.65 | 0.6487 | 105 | 1.249 | 2/2 |
| QQQ | 1h | `{"pullback_atr":0.65,"impulse_atr":0.5,"slope_window":3}` | 7.78 | 0.65 | 0.6487 | 105 | 1.249 | 2/2 |

### `QL_2026-05-01_US_EQUITIES_INTRADAY_LE_MODEL_BULL_FLAG`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| QQQ | 1h | `{"pullback_atr":0.65,"impulse_atr":0.5,"slope_window":3}` | 36.34 | 1.34 | 0.781 | 56 | 2.096 | 2/2 |
| TSLA | 1h | `{"pullback_atr":0.65,"impulse_atr":0.5,"slope_window":3}` | 30.74 | 0.80 | 0.5759 | 66 | 1.439 | 2/2 |
| AAPL | 1h | `{"pullback_atr":0.65,"impulse_atr":1.0,"slope_window":3}` | 16.00 | 0.84 | 0.612 | 56 | 1.538 | 2/2 |

### `QL_2026-05-01_US_EQUITIES_INTRADAY_PURPLE_PROFITS`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| QQQ | 1h | `{"pullback_atr":0.65,"impulse_atr":0.5,"slope_window":3}` | 36.34 | 1.34 | 0.781 | 56 | 2.096 | 2/2 |
| TSLA | 1h | `{"pullback_atr":0.65,"impulse_atr":0.5,"slope_window":3}` | 30.74 | 0.80 | 0.5759 | 66 | 1.439 | 2/2 |
| AAPL | 1h | `{"pullback_atr":0.65,"impulse_atr":1.0,"slope_window":3}` | 16.00 | 0.84 | 0.612 | 56 | 1.538 | 2/2 |

