# STAGE2 MASTER REPORT

## Executive Summary
- Strategies tested: `3`.
- Stage 2 pass count: `0`.
- Pine stage: `NO`.
- MTC producer candidate: `NO_DIRECT_PROMOTION`.
- Scope: Python research robustness only; no Pine, production runner, TradingView/parity, broker, alert, or live trading code changed.

## Strategy Summary
| strategy_id | aggregate_pf | aggregate_net_return_pct | aggregate_max_dd_pct | trade_count | best_asset | worst_asset | median_asset | positive_assets | dominant_asset_profit_share_pct | asset_concentration_warning | holdout_pf | holdout_net_return_pct | fee_2x_pf | fee_3x_pf | fee_5x_pf | parameter_stability | tail_outlier_warning | final_classification | classification_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 2.0173 | 6800.7629 | -70.2176 | 208 | BNBUSDT | ETHUSDT | XRPUSDT | 4 | 29.7673 | False | 0.8928 | -70.7702 | 1.9897 | 1.9626 | 1.9103 | STABLE | True | STAGE2_WEAK | holdout weak, drawdown high, tail outlier concentration |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 1.6051 | 6622.8683 | -59.2779 | 559 | ETHUSDT | XRPUSDT | SOLUSDT | 4 | 26.1023 | False | 1.3026 | 72.0790 | 1.5480 | 1.4924 | 1.3861 | OVERFIT_RISK | False | STAGE2_WEAK | drawdown high, parameter overfit risk |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | 1.5858 | 3195.4076 | -89.4722 | 302 | XRPUSDT | ETHUSDT | BTCUSDT | 4 | 26.3594 | False | 1.5034 | 459.5672 | 1.5529 | 1.5206 | 1.4579 | STABLE | False | STAGE2_WEAK | drawdown high |

## Asset Split
| strategy_id | asset | trade_count | profit_factor | net_return_pct | max_drawdown_pct | avg_trade_pct | win_rate | longest_losing_streak | source_summary_pf | source_summary_net_return_pct | source_summary_max_dd_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | BTCUSDT | 47 | 1.9131 | 178.4026 | -43.5841 | 2.9747 | 34.0426 | 6 | 1.9131 | 178.4026 | -43.5841 |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | ETHUSDT | 46 | 0.9875 | -37.7622 | -65.3077 | -0.0713 | 26.0870 | 8 | 0.9875 | -37.7622 | -65.3077 |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | SOLUSDT | 29 | 2.3934 | 350.5893 | -40.6455 | 7.7108 | 44.8276 | 6 | 2.3934 | 350.5893 | -40.6455 |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | BNBUSDT | 46 | 2.9023 | 308.8934 | -51.2114 | 8.6736 | 30.4348 | 6 | 2.9023 | 308.8934 | -51.2114 |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | XRPUSDT | 40 | 2.1986 | 116.1617 | -67.7260 | 6.8029 | 22.5000 | 7 | 2.1986 | 116.1617 | -67.7260 |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | BTCUSDT | 132 | 1.8341 | 181.2706 | -12.9904 | 0.8537 | 71.9697 | 2 | 1.8341 | 181.2706 | -12.9904 |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | ETHUSDT | 121 | 2.3538 | 621.9204 | -27.5066 | 1.8324 | 76.0331 | 2 | 2.3538 | 621.9204 | -27.5066 |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | SOLUSDT | 81 | 1.5012 | 92.4036 | -45.0518 | 1.0713 | 64.1975 | 4 | 1.5012 | 92.4036 | -45.0518 |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | BNBUSDT | 122 | 1.4778 | 89.6062 | -41.9776 | 0.7727 | 63.9344 | 3 | 1.4778 | 89.6062 | -41.9776 |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | XRPUSDT | 103 | 1.1648 | -9.2440 | -57.3299 | 0.4012 | 63.1068 | 5 | 1.1648 | -9.2440 | -57.3299 |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | BTCUSDT | 71 | 1.7607 | 154.2939 | -47.1632 | 1.6876 | 66.1972 | 3 | 2.5935 | 176.3444 | -16.8987 |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | ETHUSDT | 63 | 0.9517 | -38.9075 | -67.1884 | -0.1884 | 50.7937 | 6 | 1.4465 | 57.5658 | -48.9277 |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | SOLUSDT | 63 | 1.6228 | 148.1513 | -71.7771 | 2.2892 | 60.3175 | 5 | 2.2239 | 281.6350 | -26.1939 |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | BNBUSDT | 56 | 1.7940 | 106.5963 | -32.5114 | 1.5652 | 57.1429 | 7 | 1.6081 | 56.6535 | -32.5114 |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | XRPUSDT | 49 | 2.2152 | 313.7578 | -33.0873 | 3.8119 | 63.2653 | 3 | 1.4808 | 43.4976 | -32.6433 |

## Year Split
| strategy_id | year | trade_count | profit_factor | net_return_pct | max_drawdown_pct | avg_trade_pct | win_rate | longest_losing_streak |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 2024 | 50 | 2.4694 | 352.6802 | -47.5571 | 6.3810 | 34.0000 | 7 |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 2025 | 43 | 0.8029 | -43.9308 | -47.0957 | -0.8314 | 23.2558 | 7 |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 2026 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 2024 | 133 | 1.3107 | 68.9425 | -47.6442 | 0.5553 | 65.4135 | 3 |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 2025 | 90 | 1.2533 | 24.9201 | -32.5406 | 0.3894 | 63.3333 | 6 |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 2026 | 2 | 0.1459 | -4.2647 | -4.9512 | -2.1145 | 50.0000 | 1 |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | 2024 | 51 | 1.6401 | 94.8788 | -35.7743 | 1.7932 | 56.8627 | 3 |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | 2025 | 46 | 1.8287 | 112.1463 | -51.0466 | 2.2325 | 63.0435 | 4 |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | 2026 | 16 | 2.0184 | 47.7931 | -24.3525 | 3.0841 | 50.0000 | 4 |

## Holdout And Walk Forward
| strategy_id | train_start | train_end | test_start | test_end | selected_parameter_set | train_pf | test_pf | test_net_return_pct | test_trade_count | test_max_drawdown_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 2024-01-01 | 2024-07-01 | 2024-07-01 | 2024-10-01 | {"atr_filter": false, "direction_mode": "long_only", "mult": 0.5, "trend_filter": true} | 1.7166 | 0.7704 | -16.4434 | 15 | -22.2181 |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 2024-04-01 | 2024-10-01 | 2024-10-01 | 2025-01-01 | {"atr_filter": true, "direction_mode": "long_only", "mult": 0.5, "trend_filter": false} | 2.2831 | 5.8606 | 389.8475 | 21 | -27.2223 |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 2024-07-01 | 2025-01-01 | 2025-01-01 | 2025-04-01 | {"atr_filter": true, "direction_mode": "long_only", "mult": 0.5, "trend_filter": false} | 5.2436 | 0.4021 | -64.4258 | 28 | -68.0325 |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 2024-10-01 | 2025-04-01 | 2025-04-01 | 2025-07-01 | {"atr_filter": true, "direction_mode": "short_only", "mult": 0.5, "trend_filter": true} | 3.8909 | 0.9246 | -7.5218 | 6 | -28.9588 |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 2025-01-01 | 2025-07-01 | 2025-07-01 | 2025-10-01 | {"atr_filter": true, "direction_mode": "short_only", "mult": 0.6, "trend_filter": true} | 4.9291 | 0.0000 | -14.5263 | 2 | -5.7045 |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 2025-04-01 | 2025-10-01 | 2025-10-01 | 2026-01-01 | {"atr_filter": true, "direction_mode": "long_only", "mult": 0.5, "trend_filter": false} | 4.2446 | 0.0000 | -76.8921 | 27 | -76.0389 |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 2025-07-01 | 2026-01-01 | 2026-01-01 | 2026-04-01 | {"atr_filter": true, "direction_mode": "long_only", "mult": 0.5, "trend_filter": true} | 1.6254 | 0.0000 | 0.0000 | 0 | 0.0000 |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 2024-01-01 | 2024-07-01 | 2024-07-01 | 2024-10-01 | {"stop_mode": "none"} | 1.3234 | 0.5638 | -27.3744 | 20 | -38.8659 |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 2024-04-01 | 2024-10-01 | 2024-10-01 | 2025-01-01 | {"stop_mode": "none"} | 0.4444 | 2.2718 | 71.1835 | 35 | -13.5139 |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 2024-07-01 | 2025-01-01 | 2025-01-01 | 2025-04-01 | {"stop_mode": "none"} | 1.2954 | 0.6205 | -19.4754 | 16 | -22.7483 |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 2024-10-01 | 2025-04-01 | 2025-04-01 | 2025-07-01 | {"stop_mode": "none"} | 1.4568 | 2.0584 | 11.2117 | 21 | -4.4619 |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 2025-01-01 | 2025-07-01 | 2025-07-01 | 2025-10-01 | {"stop_mode": "none"} | 0.8882 | 2.2159 | 63.9781 | 43 | -14.8944 |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 2025-04-01 | 2025-10-01 | 2025-10-01 | 2026-01-01 | {"stop_mode": "none"} | 2.1862 | 0.6589 | -14.9318 | 10 | -19.1466 |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 2025-07-01 | 2026-01-01 | 2026-01-01 | 2026-04-01 | {"stop_mode": "none"} | 1.4994 | 0.1459 | -4.2647 | 2 | -4.9512 |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | 2024-01-01 | 2024-07-01 | 2024-07-01 | 2024-10-01 | {"atr_mult": 3.0, "pivot": 7} | 1.8026 | 1.0941 | -0.9099 | 21 | -21.0829 |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | 2024-04-01 | 2024-10-01 | 2024-10-01 | 2025-01-01 | {"atr_mult": 3.0, "pivot": 10} | 2.9667 | 3.8070 | 86.8596 | 21 | -9.2486 |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | 2024-07-01 | 2025-01-01 | 2025-01-01 | 2025-04-01 | {"atr_mult": 3.0, "pivot": 10} | 2.8146 | 1.6280 | 24.0189 | 20 | -30.8054 |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | 2024-10-01 | 2025-04-01 | 2025-04-01 | 2025-07-01 | {"atr_mult": 3.0, "pivot": 10} | 2.4022 | 8.6247 | 77.1086 | 12 | -4.1650 |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | 2025-01-01 | 2025-07-01 | 2025-07-01 | 2025-10-01 | {"atr_mult": 3.0, "pivot": 10} | 2.7185 | 1.6401 | 12.1160 | 8 | -20.0783 |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | 2025-04-01 | 2025-10-01 | 2025-10-01 | 2026-01-01 | {"atr_mult": 3.0, "pivot": 10} | 3.4199 | 1.0551 | -0.4181 | 11 | -15.6346 |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | 2025-07-01 | 2026-01-01 | 2026-01-01 | 2026-04-01 | {"atr_mult": 5.0, "pivot": 10} | 1.3377 | 2.2756 | 56.2341 | 14 | -21.8791 |

## Fee Stress
| strategy_id | fee_scenario | trade_count | profit_factor | net_return_pct | max_drawdown_pct | avg_trade_pct | win_rate | longest_losing_streak | fee_monotonic_check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | base | 208 | 2.0173 | 6800.7629 | -70.2176 | 4.9579 | 30.7692 | 8 | True |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 2x | 208 | 1.9897 | 5745.9503 | -71.9017 | 4.8779 | 30.7692 | 8 | True |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 3x | 208 | 1.9626 | 4851.6992 | -73.4917 | 4.7979 | 30.7692 | 8 | True |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 5x | 208 | 1.9103 | 3451.2033 | -76.4105 | 4.6379 | 30.7692 | 8 | True |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | base | 559 | 1.6051 | 6622.8683 | -59.2779 | 0.9960 | 68.3363 | 6 | True |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 2x | 559 | 1.5480 | 4206.8013 | -60.9183 | 0.9160 | 67.2630 | 6 | True |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 3x | 559 | 1.4924 | 2658.0345 | -63.9652 | 0.8360 | 66.9052 | 6 | True |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 5x | 559 | 1.3861 | 1029.8537 | -69.7291 | 0.6760 | 66.5474 | 6 | True |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | base | 302 | 1.5858 | 3195.4076 | -89.4722 | 1.7437 | 59.6026 | 7 | True |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | 2x | 302 | 1.5529 | 2491.3704 | -89.6871 | 1.6637 | 59.2715 | 9 | True |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | 3x | 302 | 1.5206 | 1937.3501 | -89.8978 | 1.5837 | 58.9404 | 9 | True |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | 5x | 302 | 1.4579 | 1158.5918 | -90.3069 | 1.4237 | 57.2848 | 9 | True |

## Parameter Stability
| strategy_id | best_parameter_set | best_mean_pf | near_parameter_count | near_parameter_median_pf | near_parameters_pf_gt_1_10 | parameter_stability |
| --- | --- | --- | --- | --- | --- | --- |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | {"atr_filter": true, "direction_mode": "long_only", "mult": 0.7, "trend_filter": true} | 2.0790 | 6 | 1.9269 | 6 | STABLE |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | {"stop_mode": "none"} | 1.6663 | 0 | 0.0000 | 0 | OVERFIT_RISK |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | {"atr_mult": 5.0, "pivot": 10} | 2.0653 | 10 | 1.5309 | 10 | STABLE |

## Drawdown And Distribution
| strategy_id | max_dd_pct | average_dd_pct | longest_dd_duration_trades | worst_losing_streak | trade_cluster_count_48h | tail_loss_top5_share_pct |
| --- | --- | --- | --- | --- | --- | --- |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | -86.6249 | -47.0165 | 86 | 15 | 67 | 9.5929 |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | -67.4851 | -20.2539 | 148 | 6 | 280 | 18.1750 |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | -63.0086 | -23.6197 | 99 | 6 | 106 | 17.3893 |

| strategy_id | top5_wins_profit_share_pct | top5_losses_loss_share_pct | median_trade_pct | p10_trade_pct | p90_trade_pct | outlier_dependency_warning |
| --- | --- | --- | --- | --- | --- | --- |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 44.1155 | 9.5929 | -4.6352 | -10.7853 | 27.7262 | True |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 8.0425 | 18.1750 | 1.4346 | -5.6698 | 6.5435 | False |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | 12.5017 | 17.3893 | 1.3792 | -9.6918 | 13.8074 | False |

## Baseline Comparison
| strategy_id | strategy_pf | strategy_net_return_pct | random_same_exit_pf | random_same_exit_net_return_pct | ema20_50_baseline_mean_pf | ema20_50_baseline_mean_net_return_pct | beats_ema_pf | beats_random_return |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 2.0173 | 6800.7629 | 0.0000 | -15.3349 | 1.2041 | 31.1390 | True | True |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 1.6051 | 6622.8683 | 0.0000 | -36.0698 | 1.2041 | 31.1390 | True | True |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | 1.5858 | 3195.4076 | 0.0000 | -21.4706 | 1.2041 | 31.1390 | True | True |

## Validation
- `STAGE2_METRIC_RECOMPUTE_CHECK.csv` produced.
- Fee monotonic check is stored in `STAGE2_FEE_STRESS.csv`.

## Commands Run
- `python -m py_compile 06_QUANTLENS_LAB/research/stage2_robustness_2026_05_03/run_stage2_robustness.py`
- `python 06_QUANTLENS_LAB/research/stage2_robustness_2026_05_03/run_stage2_robustness.py`
- Output existence check for all required CSV/MD files.
- Pytest check: no `test_*.py` files exist in the Stage 2 folder, so no pytest suite was run for this folder.

## Scope Safety
- `MTC_V2.pine` was not modified by this Stage 2 task.
- Production Python runner was not modified by this Stage 2 task.
- TradingView/parity/live trading/broker/alert code was not touched.
