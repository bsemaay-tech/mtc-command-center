# OVERNIGHT AGGREGATED REPORT — cross-iteration robustness

- Iterations aggregated: **1**
- Distinct (strategy × sym × tf) cells that PASSed at least once: **16**

## Methodology

Each row below is a (strategy, symbol, timeframe) cell. `iters_passed` counts how many of the 1 independent runs classified this cell as PASS or STRONG_PASS. True robustness = high iters_passed AND tight ret_stdev. Single-iter PASSes that don't repeat are likely noise.

## ROBUST winners (iters_passed >= 50% of runs)

| Strategy | Sym | TF | Pass×/N | Strong× | Ret median % | Ret stdev | Sharpe med | Boot p med | DSR p med | PF med | DD med % | Trades med |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `GEN_DONCHIAN_BREAKOUT` | TRXUSDT | 15m | **1/1** | 0 | 101.98 | 0.00 | 0.05 | 0.0000 | 0.0106 | 1.211 | -35.1 | 749 |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL` | LINKUSDT | 1h | **1/1** | 1 | 75.37 | 0.00 | 0.15 | 0.0255 | 0.1780 | 2.038 | -16.3 | 121 |
| `GEN_RSI_OVERSOLD_REVERSAL` | TRXUSDT | 2h | **1/1** | 1 | 49.73 | 0.00 | 0.12 | 0.0235 | 0.0878 | 1.401 | -16.8 | 155 |
| `GEN_DONCHIAN_BREAKOUT` | ETHUSDT | 2h | **1/1** | 0 | 46.29 | 0.00 | 0.09 | 0.1280 | 0.3414 | 1.248 | -47.3 | 90 |
| `GEN_RSI_OVERSOLD_REVERSAL` | LINKUSDT | 2h | **1/1** | 1 | 28.64 | 0.00 | 0.10 | 0.2150 | 0.1891 | 1.347 | -28.4 | 50 |
| `QL_2026-05-01_SP500_5M_TWO_CANDLE_SENTIMENT_SR` | ETHUSDT | 2h | **1/1** | 0 | 21.95 | 0.00 | 0.14 | 0.4195 | 0.3810 | 1.409 | -18.4 | 31 |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL` | NEARUSDT | 1h | **1/1** | 0 | 16.50 | 0.00 | 0.04 | 0.0555 | 0.0009 | 1.157 | -18.6 | 266 |
| `GEN_RSI_OVERSOLD_REVERSAL` | LINKUSDT | 1h | **1/1** | 0 | 14.87 | 0.00 | 0.11 | 0.4425 | 0.2506 | 1.334 | -13.4 | 33 |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL` | SOLUSDT | 2h | **1/1** | 0 | 12.32 | 0.00 | 0.07 | 0.4255 | 0.0836 | 1.316 | -19.4 | 69 |
| `GEN_RSI_OVERSOLD_REVERSAL` | TRXUSDT | 1h | **1/1** | 0 | 7.82 | 0.00 | 0.04 | 0.0200 | 0.0043 | 1.093 | -18.4 | 184 |
| `GEN_DONCHIAN_BREAKOUT` | SOLUSDT | 1h | **1/1** | 0 | 7.05 | 0.00 | 0.04 | 0.0900 | 0.1634 | 1.104 | -45.5 | 108 |
| `QL_2026-05-01_ANY_CANDLESTICK_7_PATTERN_PA_CONFLUENCE` | DOGEUSDT | 1h | **1/1** | 0 | 4.86 | 0.00 | 0.06 | 0.1715 | 0.0376 | 1.143 | -12.3 | 38 |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL` | ETHUSDT | 2h | **1/1** | 0 | 0.98 | 0.00 | 0.01 | 0.4215 | 0.0110 | 1.066 | -18.9 | 111 |
| `QL_2026-05-01_SP500_5M_TWO_CANDLE_SENTIMENT_SR` | TRXUSDT | 15m | **1/1** | 0 | 0.84 | 0.00 | 0.01 | 0.0150 | 0.0003 | 1.048 | -26.0 | 334 |
| `QL_2026-05-01_ANY_CANDLESTICK_7_PATTERN_PA_CONFLUENCE` | BNBUSDT | 1h | **1/1** | 0 | 0.50 | 0.00 | 0.02 | 0.3335 | 0.0280 | 1.041 | -10.7 | 34 |
| `GEN_RSI_OVERSOLD_REVERSAL` | ETHUSDT | 2h | **1/1** | 0 | 0.28 | 0.00 | 0.02 | 0.1975 | 0.0379 | 1.050 | -39.5 | 73 |

## All PASS cells (any iteration count)

| Strategy | Sym | TF | Pass×/N | Strong× | Ret med % | Ret stdev | Sharpe med | Boot p med | PF med | DD med % | Trades med |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `GEN_DONCHIAN_BREAKOUT` | TRXUSDT | 15m | 1/1 | 0 | 101.98 | 0.00 | 0.05 | 0.0000 | 1.211 | -35.1 | 749 |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL` | LINKUSDT | 1h | 1/1 | 1 | 75.37 | 0.00 | 0.15 | 0.0255 | 2.038 | -16.3 | 121 |
| `GEN_RSI_OVERSOLD_REVERSAL` | TRXUSDT | 2h | 1/1 | 1 | 49.73 | 0.00 | 0.12 | 0.0235 | 1.401 | -16.8 | 155 |
| `GEN_DONCHIAN_BREAKOUT` | ETHUSDT | 2h | 1/1 | 0 | 46.29 | 0.00 | 0.09 | 0.1280 | 1.248 | -47.3 | 90 |
| `GEN_RSI_OVERSOLD_REVERSAL` | LINKUSDT | 2h | 1/1 | 1 | 28.64 | 0.00 | 0.10 | 0.2150 | 1.347 | -28.4 | 50 |
| `QL_2026-05-01_SP500_5M_TWO_CANDLE_SENTIMENT_SR` | ETHUSDT | 2h | 1/1 | 0 | 21.95 | 0.00 | 0.14 | 0.4195 | 1.409 | -18.4 | 31 |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL` | NEARUSDT | 1h | 1/1 | 0 | 16.50 | 0.00 | 0.04 | 0.0555 | 1.157 | -18.6 | 266 |
| `GEN_RSI_OVERSOLD_REVERSAL` | LINKUSDT | 1h | 1/1 | 0 | 14.87 | 0.00 | 0.11 | 0.4425 | 1.334 | -13.4 | 33 |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL` | SOLUSDT | 2h | 1/1 | 0 | 12.32 | 0.00 | 0.07 | 0.4255 | 1.316 | -19.4 | 69 |
| `GEN_RSI_OVERSOLD_REVERSAL` | TRXUSDT | 1h | 1/1 | 0 | 7.82 | 0.00 | 0.04 | 0.0200 | 1.093 | -18.4 | 184 |
| `GEN_DONCHIAN_BREAKOUT` | SOLUSDT | 1h | 1/1 | 0 | 7.05 | 0.00 | 0.04 | 0.0900 | 1.104 | -45.5 | 108 |
| `QL_2026-05-01_ANY_CANDLESTICK_7_PATTERN_PA_CONFLUENCE` | DOGEUSDT | 1h | 1/1 | 0 | 4.86 | 0.00 | 0.06 | 0.1715 | 1.143 | -12.3 | 38 |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL` | ETHUSDT | 2h | 1/1 | 0 | 0.98 | 0.00 | 0.01 | 0.4215 | 1.066 | -18.9 | 111 |
| `QL_2026-05-01_SP500_5M_TWO_CANDLE_SENTIMENT_SR` | TRXUSDT | 15m | 1/1 | 0 | 0.84 | 0.00 | 0.01 | 0.0150 | 1.048 | -26.0 | 334 |
| `QL_2026-05-01_ANY_CANDLESTICK_7_PATTERN_PA_CONFLUENCE` | BNBUSDT | 1h | 1/1 | 0 | 0.50 | 0.00 | 0.02 | 0.3335 | 1.041 | -10.7 | 34 |
| `GEN_RSI_OVERSOLD_REVERSAL` | ETHUSDT | 2h | 1/1 | 0 | 0.28 | 0.00 | 0.02 | 0.1975 | 1.050 | -39.5 | 73 |

## Per-strategy summary

| Strategy | Cells PASSed ≥ 1× | Cells PASSed ≥ 50% iters | Best (sym/tf) | Best ret med % |
|---|---|---|---|---|
| `GEN_RSI_OVERSOLD_REVERSAL` | 5 | **5** | TRXUSDT 2h | 49.73 |
| `QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL` | 4 | **4** | LINKUSDT 1h | 75.37 |
| `GEN_DONCHIAN_BREAKOUT` | 3 | **3** | TRXUSDT 15m | 101.98 |
| `QL_2026-05-01_SP500_5M_TWO_CANDLE_SENTIMENT_SR` | 2 | **2** | ETHUSDT 2h | 21.95 |
| `QL_2026-05-01_ANY_CANDLESTICK_7_PATTERN_PA_CONFLUENCE` | 2 | **2** | DOGEUSDT 1h | 4.86 |