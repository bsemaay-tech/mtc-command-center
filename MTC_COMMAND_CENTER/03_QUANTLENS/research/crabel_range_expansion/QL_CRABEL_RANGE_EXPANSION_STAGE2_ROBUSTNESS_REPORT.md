# QL Crabel Range Expansion Stage2 Robustness Report

## Executive Summary
- Final classification: **GATE_ONLY_CANDIDATE**.
- Reason: There is real breakout information, but standalone symbol-level drawdown, short-side weakness, and regime instability argue for gate/filter use first.
- Scope: Python-only research robustness; no Pine, no MTC production integration, no TradingView parity.

## 1. Existing Result Validation
- Stage1 aggregate net return recomputed as symbol-level mean: 1192.54%.
- Stage1 aggregate PF recomputed from primary trade rows: 1.35.
- Stage1 aggregate max DD recomputed as symbol-level mean: -37.75%.
- Stage1 primary trade count recomputed: 4178.
- Aggregate net return is a simple equal-weight mean of per-symbol compounded returns, not a single combined portfolio equity curve. Simple sum would be 5962.70%; one chronological all-trades stream would be 7366176.51%.

## 2. Per-Symbol Breakdown
| symbol  | net_return_pct | profit_factor | max_drawdown_pct | total_trades | win_rate | avg_win_pct | avg_loss_pct | expectancy_pct | buy_and_hold_return_pct | beats_buy_and_hold |
| ------- | -------------- | ------------- | ---------------- | ------------ | -------- | ----------- | ------------ | -------------- | ----------------------- | ------------------ |
| BTCUSDT | 584.40         | 1.33          | -33.75           | 953          | 48.16    | 2.04        | -1.42        | 0.25           | 593.46                  | False              |
| ETHUSDT | 2757.38        | 1.51          | -32.17           | 862          | 49.30    | 2.79        | -1.79        | 0.47           | 1405.92                 | True               |
| SOLUSDT | 118.00         | 1.14          | -39.52           | 737          | 49.80    | 3.14        | -2.72        | 0.20           | 2493.31                 | False              |
| BNBUSDT | 937.54         | 1.42          | -35.07           | 806          | 49.13    | 2.53        | -1.71        | 0.37           | 2374.77                 | False              |
| XRPUSDT | 1565.38        | 1.41          | -48.24           | 820          | 44.15    | 3.68        | -2.07        | 0.47           | 524.80                  | True               |

## 3. Long/Short Breakdown
| symbol  | direction | trades | net_return_pct_compounded | profit_factor | avg_trade_pct | win_rate |
| ------- | --------- | ------ | ------------------------- | ------------- | ------------- | -------- |
| BTCUSDT | long      | 474    | 540.13                    | 1.73          | 0.42          | 51.69    |
| BTCUSDT | short     | 479    | 6.92                      | 1.08          | 0.07          | 44.68    |
| ETHUSDT | long      | 417    | 1681.79                   | 2.07          | 0.76          | 55.16    |
| ETHUSDT | short     | 445    | 60.37                     | 1.18          | 0.20          | 43.82    |
| SOLUSDT | long      | 373    | 451.15                    | 1.47          | 0.54          | 54.69    |
| SOLUSDT | short     | 364    | -60.45                    | 0.90          | -0.16         | 44.78    |
| BNBUSDT | long      | 377    | 1048.60                   | 2.19          | 0.71          | 56.50    |
| BNBUSDT | short     | 429    | -9.67                     | 1.07          | 0.07          | 42.66    |
| XRPUSDT | long      | 374    | 3976.87                   | 2.28          | 1.14          | 50.00    |
| XRPUSDT | short     | 446    | -59.15                    | 0.93          | -0.10         | 39.24    |

## 4. ETHUSDT vs SOLUSDT
- ETHUSDT: net 2757.38%, PF 1.51, DD -32.17%, trades 862.
- SOLUSDT: net 118.00%, PF 1.14, DD -39.52%, trades 737.
- ETH works better because the same close-exit breakout captures larger average winners with lower DD. SOL is positive but weak versus its buy-and-hold, with lower PF and worse DD.
- Symbol sensitivity is material: all symbols are positive, but return dispersion is high and SOL/BNB/BTC fail buy-and-hold.

## 5. Parameter Robustness Sweep
| expansion_mult | aggregate_net_return_pct | aggregate_profit_factor | aggregate_max_drawdown_pct | aggregate_trade_count | positive_symbols |
| -------------- | ------------------------ | ----------------------- | -------------------------- | --------------------- | ---------------- |
| 0.50           | 1301427.48               | 1.86                    | -27.21                     | 7055                  | 5                |
| 0.60           | 107650.41                | 1.67                    | -30.13                     | 6301                  | 5                |
| 0.70           | 19624.51                 | 1.54                    | -34.16                     | 5510                  | 5                |
| 0.80           | 5636.42                  | 1.44                    | -37.73                     | 4786                  | 5                |
| 0.90           | 1192.54                  | 1.35                    | -37.75                     | 4178                  | 5                |
| 1.00           | 334.93                   | 1.24                    | -48.50                     | 3653                  | 4                |
| 1.10           | 68.24                    | 1.12                    | -61.06                     | 3186                  | 3                |
| 1.20           | 20.37                    | 1.09                    | -63.22                     | 2714                  | 3                |
| 1.30           | 16.10                    | 1.09                    | -61.76                     | 2340                  | 3                |
| 1.50           | -17.63                   | 1.03                    | -66.69                     | 1749                  | 1                |
- 0.80/0.90/1.00 PF>1.15 neighbor count: 3/3.
- OVERFIT_RISK: no.

## 6. Fee / Slippage Stress
| fee_label | exit_variant                 | aggregate_net_return_pct | aggregate_profit_factor | aggregate_max_drawdown_pct | aggregate_trade_count | positive_symbols |
| --------- | ---------------------------- | ------------------------ | ----------------------- | -------------------------- | --------------------- | ---------------- |
| 2x        | atr_stop_time_exit           | 129.97                   | 1.18                    | -70.87                     | 2611                  | 5                |
| 2x        | close_exit                   | 368.56                   | 1.22                    | -47.70                     | 4178                  | 4                |
| 2x        | next_bar_close_exit          | 226.31                   | 1.20                    | -72.87                     | 3322                  | 5                |
| 2x        | previous_extreme_target_stop | -100.00                  | 0.00                    | -100.00                    | 4178                  | 0                |
| 3x        | atr_stop_time_exit           | 20.47                    | 1.12                    | -74.39                     | 2611                  | 3                |
| 3x        | close_exit                   | 70.18                    | 1.10                    | -63.38                     | 4178                  | 3                |
| 3x        | next_bar_close_exit          | 48.24                    | 1.13                    | -77.95                     | 3322                  | 4                |
| 3x        | previous_extreme_target_stop | -100.00                  | 0.00                    | -100.00                    | 4178                  | 0                |
| base      | atr_stop_time_exit           | 339.37                   | 1.24                    | -67.35                     | 2611                  | 5                |
| base      | close_exit                   | 1192.54                  | 1.35                    | -37.75                     | 4178                  | 5                |
| base      | next_bar_close_exit          | 619.77                   | 1.28                    | -68.37                     | 3322                  | 5                |
| base      | previous_extreme_target_stop | -100.00                  | 0.00                    | -100.00                    | 4178                  | 0                |
- Stress note: 3x fee/slippage still positive.

## 7. Time Split / Walk-Forward-Like Test
| segment        | aggregate_net_return_pct | aggregate_profit_factor | aggregate_max_drawdown_pct | aggregate_trade_count | positive_symbols |
| -------------- | ------------------------ | ----------------------- | -------------------------- | --------------------- | ---------------- |
| first_50pct    | 681.34                   | 1.50                    | -32.16                     | 2040                  | 5                |
| last_12_months | 23.59                    | 1.21                    | -20.97                     | 701                   | 4                |
| last_6_months  | 5.51                     | 1.12                    | -16.85                     | 341                   | 3                |
| second_50pct   | 61.40                    | 1.17                    | -34.72                     | 2136                  | 5                |
| year_2019      | 6.45                     | 1.30                    | -7.74                      | 52                    | 1                |
| year_2020      | 122.52                   | 1.81                    | -23.65                     | 591                   | 5                |
| year_2021      | 100.68                   | 1.41                    | -29.74                     | 638                   | 4                |
| year_2022      | 54.24                    | 1.36                    | -21.30                     | 634                   | 4                |
| year_2023      | 24.27                    | 1.27                    | -18.58                     | 671                   | 4                |
| year_2024      | 8.90                     | 1.10                    | -23.76                     | 684                   | 3                |
| year_2025      | 13.01                    | 1.13                    | -26.80                     | 686                   | 4                |
| year_2026      | 18.98                    | 1.62                    | -9.99                      | 222                   | 5                |
- Segment-level CSV includes first half, second half, yearly segments, last 12 months, and last 6 months with long/short counts.

## 8. Drawdown Diagnosis
| scope     | symbol                | dd_start   | dd_end     | drawdown_pct | trade_count_in_dd | long_net_pct_sum | short_net_pct_sum | trend_regime | volatility_regime | diagnosed_cause                             |
| --------- | --------------------- | ---------- | ---------- | ------------ | ----------------- | ---------------- | ----------------- | ------------ | ----------------- | ------------------------------------------- |
| symbol    | BNBUSDT               | 2023-06-10 | 2025-02-06 | -35.07       | 212               | 39.79            | -70.63            | up           | low               | short_side_failure                          |
| symbol    | BTCUSDT               | 2024-11-11 | 2026-01-12 | -33.75       | 183               | -5.28            | -28.70            | sideways     | low               | short_side_failure                          |
| symbol    | ETHUSDT               | 2020-03-12 | 2020-03-13 | -32.17       | 2                 | -32.17           | 64.38             | up           | high              | excessive_trade_frequency                   |
| symbol    | SOLUSDT               | 2021-01-03 | 2021-05-16 | -39.52       | 44                | 0.66             | -37.51            | up           | high              | short_side_failure                          |
| symbol    | XRPUSDT               | 2023-08-17 | 2024-07-05 | -48.24       | 127               | 10.64            | -64.07            | down         | low               | short_side_failure                          |
| aggregate | EQUAL_WEIGHT_5_SYMBOL | 2025-01-15 | 2025-02-23 | -22.54       | 79                | 5.66             | -101.81           | mixed        | mixed             | mixed_symbol_drawdowns_high_trade_frequency |
- Main diagnosis: drawdown is driven by high trade frequency plus side-specific failures in volatile regime shifts. No trend or volatility filter exists in the base model.

## 9. Simple Filter Tests
| filter_mode         | direction_mode | aggregate_net_return_pct | aggregate_profit_factor | aggregate_max_drawdown_pct | aggregate_trade_count | avg_return_dd_ratio |
| ------------------- | -------------- | ------------------------ | ----------------------- | -------------------------- | --------------------- | ------------------- |
| atr_above_median    | both           | 60.87                    | 1.17                    | -44.97                     | 1767                  | 1.57                |
| atr_above_median    | long_only      | 100.73                   | 1.43                    | -27.05                     | 909                   | 4.23                |
| atr_above_median    | short_only     | -69.50                   | 0.70                    | -76.69                     | 998                   | -0.90               |
| atr_band            | both           | 97.41                    | 1.29                    | -32.70                     | 1370                  | 3.52                |
| atr_band            | long_only      | 80.36                    | 1.46                    | -23.86                     | 716                   | 3.60                |
| atr_band            | short_only     | -45.57                   | 0.75                    | -59.49                     | 770                   | -0.72               |
| atr_below_extreme   | both           | 967.49                   | 1.40                    | -32.88                     | 3609                  | 31.79               |
| atr_below_extreme   | long_only      | 259.79                   | 1.41                    | -32.72                     | 1932                  | 8.27                |
| atr_below_extreme   | short_only     | -60.29                   | 0.83                    | -76.84                     | 2029                  | -0.76               |
| none                | both           | 1192.54                  | 1.35                    | -37.75                     | 4178                  | 33.04               |
| none                | long_only      | 360.70                   | 1.42                    | -34.15                     | 2211                  | 10.76               |
| none                | short_only     | -72.66                   | 0.83                    | -85.31                     | 2359                  | -0.84               |
| regime_ema50_ema200 | both           | 124.22                   | 1.26                    | -39.13                     | 2064                  | 3.32                |
| regime_ema50_ema200 | long_only      | 203.90                   | 1.57                    | -27.67                     | 1255                  | 7.80                |
| regime_ema50_ema200 | short_only     | -19.36                   | 0.89                    | -42.53                     | 809                   | -0.14               |
| trend_ema200        | both           | 73.24                    | 1.17                    | -43.65                     | 2127                  | 2.22                |
| trend_ema200        | long_only      | 168.22                   | 1.52                    | -28.37                     | 1226                  | 5.99                |
| trend_ema200        | short_only     | -32.30                   | 0.83                    | -48.06                     | 901                   | -0.54               |
- Goal was DD reduction, not return maximization. Filters are simple and past-only via shifted close/EMA/ATR inputs.

## 10. Best / Worst Trades
- Full best/worst trade lists are in the report CSV outputs; top rows are shown here.
### Worst 10 By Symbol
| symbol  | direction | entry_timestamp           | exit_timestamp            | net_return_pct | exit_reason |
| ------- | --------- | ------------------------- | ------------------------- | -------------- | ----------- |
| BNBUSDT | short     | 2022-06-15 00:00:00+00:00 | 2022-06-15 00:00:00+00:00 | -15.23         | close_exit  |
| BNBUSDT | short     | 2021-02-23 00:00:00+00:00 | 2021-02-23 00:00:00+00:00 | -14.32         | close_exit  |
| BNBUSDT | short     | 2024-03-15 00:00:00+00:00 | 2024-03-15 00:00:00+00:00 | -14.18         | close_exit  |
| BNBUSDT | short     | 2021-02-22 00:00:00+00:00 | 2021-02-22 00:00:00+00:00 | -10.09         | close_exit  |
| BNBUSDT | short     | 2025-02-03 00:00:00+00:00 | 2025-02-03 00:00:00+00:00 | -9.35          | close_exit  |
| BNBUSDT | short     | 2020-09-11 00:00:00+00:00 | 2020-09-11 00:00:00+00:00 | -8.88          | close_exit  |
| BNBUSDT | long      | 2021-02-10 00:00:00+00:00 | 2021-02-10 00:00:00+00:00 | -8.88          | close_exit  |
| BNBUSDT | short     | 2025-04-07 00:00:00+00:00 | 2025-04-07 00:00:00+00:00 | -8.09          | close_exit  |
| BNBUSDT | short     | 2020-07-27 00:00:00+00:00 | 2020-07-27 00:00:00+00:00 | -6.79          | close_exit  |
| BNBUSDT | short     | 2021-12-15 00:00:00+00:00 | 2021-12-15 00:00:00+00:00 | -6.76          | close_exit  |
| BTCUSDT | short     | 2021-05-21 00:00:00+00:00 | 2021-05-21 00:00:00+00:00 | -9.61          | close_exit  |
| BTCUSDT | short     | 2020-03-16 00:00:00+00:00 | 2020-03-16 00:00:00+00:00 | -9.02          | close_exit  |
| BTCUSDT | short     | 2025-02-03 00:00:00+00:00 | 2025-02-03 00:00:00+00:00 | -8.49          | close_exit  |
| BTCUSDT | short     | 2021-08-05 00:00:00+00:00 | 2021-08-05 00:00:00+00:00 | -8.38          | close_exit  |
| BTCUSDT | short     | 2021-01-11 00:00:00+00:00 | 2021-01-11 00:00:00+00:00 | -7.79          | close_exit  |
| BTCUSDT | short     | 2021-02-23 00:00:00+00:00 | 2021-02-23 00:00:00+00:00 | -7.61          | close_exit  |
| BTCUSDT | long      | 2021-01-29 00:00:00+00:00 | 2021-01-29 00:00:00+00:00 | -7.35          | close_exit  |
| BTCUSDT | long      | 2019-10-26 00:00:00+00:00 | 2019-10-26 00:00:00+00:00 | -7.30          | close_exit  |
| BTCUSDT | short     | 2019-09-30 00:00:00+00:00 | 2019-09-30 00:00:00+00:00 | -6.73          | close_exit  |
| BTCUSDT | long      | 2022-09-21 00:00:00+00:00 | 2022-09-21 00:00:00+00:00 | -6.51          | close_exit  |
| ETHUSDT | long      | 2020-03-13 00:00:00+00:00 | 2020-03-13 00:00:00+00:00 | -32.17         | close_exit  |
| ETHUSDT | short     | 2022-06-15 00:00:00+00:00 | 2022-06-15 00:00:00+00:00 | -16.65         | close_exit  |
| ETHUSDT | short     | 2025-02-03 00:00:00+00:00 | 2025-02-03 00:00:00+00:00 | -13.80         | close_exit  |
| ETHUSDT | short     | 2021-12-04 00:00:00+00:00 | 2021-12-04 00:00:00+00:00 | -12.04         | close_exit  |
| ETHUSDT | short     | 2021-01-08 00:00:00+00:00 | 2021-01-08 00:00:00+00:00 | -10.27         | close_exit  |
| ETHUSDT | short     | 2021-02-23 00:00:00+00:00 | 2021-02-23 00:00:00+00:00 | -9.56          | close_exit  |
| ETHUSDT | short     | 2020-08-02 00:00:00+00:00 | 2020-08-02 00:00:00+00:00 | -8.66          | close_exit  |
| ETHUSDT | short     | 2021-12-06 00:00:00+00:00 | 2021-12-06 00:00:00+00:00 | -7.95          | close_exit  |
| ETHUSDT | long      | 2022-09-06 00:00:00+00:00 | 2022-09-06 00:00:00+00:00 | -7.65          | close_exit  |
| ETHUSDT | short     | 2024-04-13 00:00:00+00:00 | 2024-04-13 00:00:00+00:00 | -7.13          | close_exit  |
| SOLUSDT | short     | 2025-02-03 00:00:00+00:00 | 2025-02-03 00:00:00+00:00 | -17.21         | close_exit  |
| SOLUSDT | long      | 2020-11-07 00:00:00+00:00 | 2020-11-07 00:00:00+00:00 | -15.48         | close_exit  |
| SOLUSDT | short     | 2022-12-29 00:00:00+00:00 | 2022-12-29 00:00:00+00:00 | -15.17         | close_exit  |
| SOLUSDT | short     | 2020-10-08 00:00:00+00:00 | 2020-10-08 00:00:00+00:00 | -14.96         | close_exit  |
| SOLUSDT | long      | 2023-07-14 00:00:00+00:00 | 2023-07-14 00:00:00+00:00 | -14.09         | close_exit  |
| SOLUSDT | short     | 2024-04-13 00:00:00+00:00 | 2024-04-13 00:00:00+00:00 | -12.98         | close_exit  |
| SOLUSDT | short     | 2022-11-22 00:00:00+00:00 | 2022-11-22 00:00:00+00:00 | -12.38         | close_exit  |
| SOLUSDT | short     | 2021-02-28 00:00:00+00:00 | 2021-02-28 00:00:00+00:00 | -12.33         | close_exit  |
| SOLUSDT | short     | 2022-06-18 00:00:00+00:00 | 2022-06-18 00:00:00+00:00 | -12.28         | close_exit  |
| SOLUSDT | short     | 2021-12-04 00:00:00+00:00 | 2021-12-04 00:00:00+00:00 | -11.12         | close_exit  |
| XRPUSDT | short     | 2025-02-03 00:00:00+00:00 | 2025-02-03 00:00:00+00:00 | -21.36         | close_exit  |
| XRPUSDT | short     | 2020-12-29 00:00:00+00:00 | 2020-12-29 00:00:00+00:00 | -20.37         | close_exit  |
| XRPUSDT | short     | 2025-04-07 00:00:00+00:00 | 2025-04-07 00:00:00+00:00 | -13.00         | close_exit  |
| XRPUSDT | short     | 2024-12-20 00:00:00+00:00 | 2024-12-20 00:00:00+00:00 | -12.53         | close_exit  |
| XRPUSDT | short     | 2024-04-13 00:00:00+00:00 | 2024-04-13 00:00:00+00:00 | -9.48          | close_exit  |
| XRPUSDT | short     | 2021-02-23 00:00:00+00:00 | 2021-02-23 00:00:00+00:00 | -8.72          | close_exit  |
| XRPUSDT | short     | 2021-05-23 00:00:00+00:00 | 2021-05-23 00:00:00+00:00 | -8.44          | close_exit  |
| XRPUSDT | long      | 2026-02-15 00:00:00+00:00 | 2026-02-15 00:00:00+00:00 | -8.34          | close_exit  |
| XRPUSDT | long      | 2021-09-10 00:00:00+00:00 | 2021-09-10 00:00:00+00:00 | -8.30          | close_exit  |
| XRPUSDT | short     | 2021-06-20 00:00:00+00:00 | 2021-06-20 00:00:00+00:00 | -8.11          | close_exit  |
### Best 10 By Symbol
| symbol  | direction | entry_timestamp           | exit_timestamp            | net_return_pct | exit_reason |
| ------- | --------- | ------------------------- | ------------------------- | -------------- | ----------- |
| BNBUSDT | short     | 2020-03-12 00:00:00+00:00 | 2020-03-12 00:00:00+00:00 | 62.14          | close_exit  |
| BNBUSDT | long      | 2021-02-19 00:00:00+00:00 | 2021-02-19 00:00:00+00:00 | 45.03          | close_exit  |
| BNBUSDT | short     | 2021-05-19 00:00:00+00:00 | 2021-05-19 00:00:00+00:00 | 41.34          | close_exit  |
| BNBUSDT | long      | 2021-02-17 00:00:00+00:00 | 2021-02-17 00:00:00+00:00 | 20.40          | close_exit  |
| BNBUSDT | long      | 2021-02-09 00:00:00+00:00 | 2021-02-09 00:00:00+00:00 | 16.66          | close_exit  |
| BNBUSDT | long      | 2021-03-09 00:00:00+00:00 | 2021-03-09 00:00:00+00:00 | 15.63          | close_exit  |
| BNBUSDT | short     | 2021-06-21 00:00:00+00:00 | 2021-06-21 00:00:00+00:00 | 15.13          | close_exit  |
| BNBUSDT | short     | 2022-05-09 00:00:00+00:00 | 2022-05-09 00:00:00+00:00 | 14.80          | close_exit  |
| BNBUSDT | short     | 2021-09-07 00:00:00+00:00 | 2021-09-07 00:00:00+00:00 | 13.34          | close_exit  |
| BNBUSDT | long      | 2024-03-13 00:00:00+00:00 | 2024-03-13 00:00:00+00:00 | 11.60          | close_exit  |
| BTCUSDT | short     | 2020-03-12 00:00:00+00:00 | 2020-03-12 00:00:00+00:00 | 59.01          | close_exit  |
| BTCUSDT | long      | 2019-10-25 00:00:00+00:00 | 2019-10-25 00:00:00+00:00 | 14.38          | close_exit  |
| BTCUSDT | long      | 2021-02-08 00:00:00+00:00 | 2021-02-08 00:00:00+00:00 | 13.26          | close_exit  |
| BTCUSDT | long      | 2020-04-29 00:00:00+00:00 | 2020-04-29 00:00:00+00:00 | 11.90          | close_exit  |
| BTCUSDT | short     | 2022-06-13 00:00:00+00:00 | 2022-06-13 00:00:00+00:00 | 10.11          | close_exit  |
| BTCUSDT | short     | 2021-05-12 00:00:00+00:00 | 2021-05-12 00:00:00+00:00 | 9.93           | close_exit  |
| BTCUSDT | short     | 2019-09-24 00:00:00+00:00 | 2019-09-24 00:00:00+00:00 | 9.55           | close_exit  |
| BTCUSDT | short     | 2022-08-19 00:00:00+00:00 | 2022-08-19 00:00:00+00:00 | 9.07           | close_exit  |
| BTCUSDT | short     | 2026-02-05 00:00:00+00:00 | 2026-02-05 00:00:00+00:00 | 8.89           | close_exit  |
| BTCUSDT | short     | 2021-09-07 00:00:00+00:00 | 2021-09-07 00:00:00+00:00 | 8.86           | close_exit  |
| ETHUSDT | short     | 2020-03-12 00:00:00+00:00 | 2020-03-12 00:00:00+00:00 | 64.38          | close_exit  |
| ETHUSDT | short     | 2021-05-19 00:00:00+00:00 | 2021-05-19 00:00:00+00:00 | 25.91          | close_exit  |
| ETHUSDT | long      | 2025-05-08 00:00:00+00:00 | 2025-05-08 00:00:00+00:00 | 18.01          | close_exit  |
| ETHUSDT | long      | 2021-01-03 00:00:00+00:00 | 2021-01-03 00:00:00+00:00 | 16.45          | close_exit  |
| ETHUSDT | long      | 2024-05-20 00:00:00+00:00 | 2024-05-20 00:00:00+00:00 | 16.36          | close_exit  |
| ETHUSDT | long      | 2020-04-06 00:00:00+00:00 | 2020-04-06 00:00:00+00:00 | 16.29          | close_exit  |
| ETHUSDT | short     | 2022-11-08 00:00:00+00:00 | 2022-11-08 00:00:00+00:00 | 13.18          | close_exit  |
| ETHUSDT | long      | 2022-07-18 00:00:00+00:00 | 2022-07-18 00:00:00+00:00 | 12.50          | close_exit  |
| ETHUSDT | long      | 2020-01-14 00:00:00+00:00 | 2020-01-14 00:00:00+00:00 | 12.04          | close_exit  |
| ETHUSDT | short     | 2020-03-08 00:00:00+00:00 | 2020-03-08 00:00:00+00:00 | 11.83          | close_exit  |
| SOLUSDT | short     | 2021-05-19 00:00:00+00:00 | 2021-05-19 00:00:00+00:00 | 27.65          | close_exit  |
| SOLUSDT | long      | 2020-11-06 00:00:00+00:00 | 2020-11-06 00:00:00+00:00 | 20.92          | close_exit  |
| SOLUSDT | long      | 2023-01-14 00:00:00+00:00 | 2023-01-14 00:00:00+00:00 | 18.51          | close_exit  |
| SOLUSDT | short     | 2020-12-23 00:00:00+00:00 | 2020-12-23 00:00:00+00:00 | 16.63          | close_exit  |
| SOLUSDT | short     | 2021-06-21 00:00:00+00:00 | 2021-06-21 00:00:00+00:00 | 16.47          | close_exit  |
| SOLUSDT | long      | 2021-08-15 00:00:00+00:00 | 2021-08-15 00:00:00+00:00 | 16.11          | close_exit  |
| SOLUSDT | long      | 2021-02-19 00:00:00+00:00 | 2021-02-19 00:00:00+00:00 | 15.36          | close_exit  |
| SOLUSDT | long      | 2025-03-02 00:00:00+00:00 | 2025-03-02 00:00:00+00:00 | 15.15          | close_exit  |
| SOLUSDT | short     | 2025-02-24 00:00:00+00:00 | 2025-02-24 00:00:00+00:00 | 14.06          | close_exit  |
| SOLUSDT | long      | 2025-01-18 00:00:00+00:00 | 2025-01-18 00:00:00+00:00 | 13.45          | close_exit  |
| XRPUSDT | long      | 2023-07-13 00:00:00+00:00 | 2023-07-13 00:00:00+00:00 | 68.85          | close_exit  |
| XRPUSDT | short     | 2020-03-12 00:00:00+00:00 | 2020-03-12 00:00:00+00:00 | 44.86          | close_exit  |
| XRPUSDT | long      | 2021-01-30 00:00:00+00:00 | 2021-01-30 00:00:00+00:00 | 32.43          | close_exit  |
| XRPUSDT | long      | 2021-04-05 00:00:00+00:00 | 2021-04-05 00:00:00+00:00 | 30.50          | close_exit  |
| XRPUSDT | short     | 2021-05-19 00:00:00+00:00 | 2021-05-19 00:00:00+00:00 | 30.22          | close_exit  |
| XRPUSDT | short     | 2020-12-23 00:00:00+00:00 | 2020-12-23 00:00:00+00:00 | 29.64          | close_exit  |
| XRPUSDT | long      | 2025-03-02 00:00:00+00:00 | 2025-03-02 00:00:00+00:00 | 28.83          | close_exit  |
| XRPUSDT | long      | 2020-11-21 00:00:00+00:00 | 2020-11-21 00:00:00+00:00 | 27.86          | close_exit  |
| XRPUSDT | long      | 2021-04-10 00:00:00+00:00 | 2021-04-10 00:00:00+00:00 | 23.31          | close_exit  |
| XRPUSDT | long      | 2023-03-21 00:00:00+00:00 | 2023-03-21 00:00:00+00:00 | 19.50          | close_exit  |

## 11. Buy & Hold Benchmark
- Crabel beats buy-and-hold on ETHUSDT and XRPUSDT only; BTCUSDT, SOLUSDT, and BNBUSDT underperform buy-and-hold over their available windows.
- The model is not simply a superior long-volatility substitute across all symbols; it extracts two-sided breakout edge but pays with high turnover and DD.

## 12. Final Classification
**GATE_ONLY_CANDIDATE**
- Pine stage: do not move directly to Pine producer integration.
- MTC producer: not yet; standalone DD and regime instability are too high.
- Gate/filter idea: worth preserving if later used as a volatility breakout confirmation gate for another producer.
- Archive: keep as research unless a separate gate-only experiment is explicitly approved.

## 13. Files Created
- `C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\research\crabel_range_expansion\QL_CRABEL_RANGE_EXPANSION_STAGE2_ROBUSTNESS_REPORT.md`
- `C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\research\crabel_range_expansion\QL_CRABEL_STAGE2_PARAMETER_SWEEP.csv`
- `C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\research\crabel_range_expansion\QL_CRABEL_STAGE2_FEE_STRESS.csv`
- `C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\research\crabel_range_expansion\QL_CRABEL_STAGE2_TIME_SPLIT.csv`
- `C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\research\crabel_range_expansion\QL_CRABEL_STAGE2_FILTER_TESTS.csv`
- `C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\research\crabel_range_expansion\QL_CRABEL_STAGE2_DRAWDOWN_DIAGNOSIS.csv`

## 14. Commands Run
- `python -m py_compile 06_QUANTLENS_LAB/research/crabel_range_expansion/run_stage2_robustness.py`
- `python 06_QUANTLENS_LAB/research/crabel_range_expansion/run_stage2_robustness.py`

## 15. Verification
- Existing Stage1 report and CSVs were read before Stage2 analysis.
- Stage2 CSV outputs were regenerated from repo-local data and existing Stage1 trade/result files.
- No Pine or production MTC files were modified.
