# QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 Stage 2 Report

- Final classification: `STAGE2_WEAK`.
- Reason: drawdown high.
- Aggregate PF: `1.5858`.
- 2x fee PF: `1.5529`.
- Holdout PF: `1.5034`.
- Parameter stability: `STABLE`.
- Best asset: `XRPUSDT`; worst asset: `ETHUSDT`; median asset: `BTCUSDT`.

## Asset Split
| strategy_id | asset | trade_count | profit_factor | net_return_pct | max_drawdown_pct | avg_trade_pct | win_rate | longest_losing_streak | source_summary_pf | source_summary_net_return_pct | source_summary_max_dd_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | BTCUSDT | 71 | 1.7607 | 154.2939 | -47.1632 | 1.6876 | 66.1972 | 3 | 2.5935 | 176.3444 | -16.8987 |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | ETHUSDT | 63 | 0.9517 | -38.9075 | -67.1884 | -0.1884 | 50.7937 | 6 | 1.4465 | 57.5658 | -48.9277 |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | SOLUSDT | 63 | 1.6228 | 148.1513 | -71.7771 | 2.2892 | 60.3175 | 5 | 2.2239 | 281.6350 | -26.1939 |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | BNBUSDT | 56 | 1.7940 | 106.5963 | -32.5114 | 1.5652 | 57.1429 | 7 | 1.6081 | 56.6535 | -32.5114 |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | XRPUSDT | 49 | 2.2152 | 313.7578 | -33.0873 | 3.8119 | 63.2653 | 3 | 1.4808 | 43.4976 | -32.6433 |

## Year Split
| strategy_id | year | trade_count | profit_factor | net_return_pct | max_drawdown_pct | avg_trade_pct | win_rate | longest_losing_streak |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | 2024 | 51 | 1.6401 | 94.8788 | -35.7743 | 1.7932 | 56.8627 | 3 |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | 2025 | 46 | 1.8287 | 112.1463 | -51.0466 | 2.2325 | 63.0435 | 4 |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | 2026 | 16 | 2.0184 | 47.7931 | -24.3525 | 3.0841 | 50.0000 | 4 |

## Holdout
| strategy_id | train_assets | holdout_assets | selected_parameter_set | train_pf | train_net_return_pct | train_trade_count | holdout_pf | holdout_net_return_pct | holdout_max_drawdown_pct | holdout_trade_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | BTCUSDT,ETHUSDT,SOLUSDT | BNBUSDT,XRPUSDT | {"atr_mult": 3.0, "pivot": 7} | 1.4396 | 1724.6803 | 359 | 1.5034 | 459.5672 | -50.7957 | 190 |

## Walk Forward
| strategy_id | train_start | train_end | test_start | test_end | selected_parameter_set | train_pf | test_pf | test_net_return_pct | test_trade_count | test_max_drawdown_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
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
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | base | 302 | 1.5858 | 3195.4076 | -89.4722 | 1.7437 | 59.6026 | 7 | True |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | 2x | 302 | 1.5529 | 2491.3704 | -89.6871 | 1.6637 | 59.2715 | 9 | True |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | 3x | 302 | 1.5206 | 1937.3501 | -89.8978 | 1.5837 | 58.9404 | 9 | True |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | 5x | 302 | 1.4579 | 1158.5918 | -90.3069 | 1.4237 | 57.2848 | 9 | True |

## Drawdown
| strategy_id | max_dd_pct | average_dd_pct | longest_dd_duration_trades | worst_losing_streak | trade_cluster_count_48h | tail_loss_top5_share_pct |
| --- | --- | --- | --- | --- | --- | --- |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | -63.0086 | -23.6197 | 99 | 6 | 106 | 17.3893 |

## Trade Distribution
| strategy_id | top5_wins_profit_share_pct | top5_losses_loss_share_pct | median_trade_pct | p10_trade_pct | p90_trade_pct | outlier_dependency_warning |
| --- | --- | --- | --- | --- | --- | --- |
| QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0 | 12.5017 | 17.3893 | 1.3792 | -9.6918 | 13.8074 | False |
