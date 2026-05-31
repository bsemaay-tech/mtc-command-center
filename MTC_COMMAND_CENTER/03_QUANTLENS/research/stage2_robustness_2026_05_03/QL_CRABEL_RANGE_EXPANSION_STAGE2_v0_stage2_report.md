# QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 Stage 2 Report

- Final classification: `STAGE2_WEAK`.
- Reason: holdout weak, drawdown high, tail outlier concentration.
- Aggregate PF: `2.0173`.
- 2x fee PF: `1.9897`.
- Holdout PF: `0.8928`.
- Parameter stability: `STABLE`.
- Best asset: `BNBUSDT`; worst asset: `ETHUSDT`; median asset: `XRPUSDT`.

## Asset Split
| strategy_id | asset | trade_count | profit_factor | net_return_pct | max_drawdown_pct | avg_trade_pct | win_rate | longest_losing_streak | source_summary_pf | source_summary_net_return_pct | source_summary_max_dd_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | BTCUSDT | 47 | 1.9131 | 178.4026 | -43.5841 | 2.9747 | 34.0426 | 6 | 1.9131 | 178.4026 | -43.5841 |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | ETHUSDT | 46 | 0.9875 | -37.7622 | -65.3077 | -0.0713 | 26.0870 | 8 | 0.9875 | -37.7622 | -65.3077 |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | SOLUSDT | 29 | 2.3934 | 350.5893 | -40.6455 | 7.7108 | 44.8276 | 6 | 2.3934 | 350.5893 | -40.6455 |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | BNBUSDT | 46 | 2.9023 | 308.8934 | -51.2114 | 8.6736 | 30.4348 | 6 | 2.9023 | 308.8934 | -51.2114 |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | XRPUSDT | 40 | 2.1986 | 116.1617 | -67.7260 | 6.8029 | 22.5000 | 7 | 2.1986 | 116.1617 | -67.7260 |

## Year Split
| strategy_id | year | trade_count | profit_factor | net_return_pct | max_drawdown_pct | avg_trade_pct | win_rate | longest_losing_streak |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 2024 | 50 | 2.4694 | 352.6802 | -47.5571 | 6.3810 | 34.0000 | 7 |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 2025 | 43 | 0.8029 | -43.9308 | -47.0957 | -0.8314 | 23.2558 | 7 |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 2026 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 |

## Holdout
| strategy_id | train_assets | holdout_assets | selected_parameter_set | train_pf | train_net_return_pct | train_trade_count | holdout_pf | holdout_net_return_pct | holdout_max_drawdown_pct | holdout_trade_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | BTCUSDT,ETHUSDT,SOLUSDT | BNBUSDT,XRPUSDT | {"atr_filter": false, "direction_mode": "short_only", "mult": 0.6, "trend_filter": true} | 1.9752 | 3423.5872 | 171 | 0.8928 | -70.7702 | -81.9893 | 133 |

## Walk Forward
| strategy_id | train_start | train_end | test_start | test_end | selected_parameter_set | train_pf | test_pf | test_net_return_pct | test_trade_count | test_max_drawdown_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 2024-01-01 | 2024-07-01 | 2024-07-01 | 2024-10-01 | {"atr_filter": false, "direction_mode": "long_only", "mult": 0.5, "trend_filter": true} | 1.7166 | 0.7704 | -16.4434 | 15 | -22.2181 |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 2024-04-01 | 2024-10-01 | 2024-10-01 | 2025-01-01 | {"atr_filter": true, "direction_mode": "long_only", "mult": 0.5, "trend_filter": false} | 2.2831 | 5.8606 | 389.8475 | 21 | -27.2223 |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 2024-07-01 | 2025-01-01 | 2025-01-01 | 2025-04-01 | {"atr_filter": true, "direction_mode": "long_only", "mult": 0.5, "trend_filter": false} | 5.2436 | 0.4021 | -64.4258 | 28 | -68.0325 |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 2024-10-01 | 2025-04-01 | 2025-04-01 | 2025-07-01 | {"atr_filter": true, "direction_mode": "short_only", "mult": 0.5, "trend_filter": true} | 3.8909 | 0.9246 | -7.5218 | 6 | -28.9588 |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 2025-01-01 | 2025-07-01 | 2025-07-01 | 2025-10-01 | {"atr_filter": true, "direction_mode": "short_only", "mult": 0.6, "trend_filter": true} | 4.9291 | 0.0000 | -14.5263 | 2 | -5.7045 |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 2025-04-01 | 2025-10-01 | 2025-10-01 | 2026-01-01 | {"atr_filter": true, "direction_mode": "long_only", "mult": 0.5, "trend_filter": false} | 4.2446 | 0.0000 | -76.8921 | 27 | -76.0389 |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 2025-07-01 | 2026-01-01 | 2026-01-01 | 2026-04-01 | {"atr_filter": true, "direction_mode": "long_only", "mult": 0.5, "trend_filter": true} | 1.6254 | 0.0000 | 0.0000 | 0 | 0.0000 |

## Fee Stress
| strategy_id | fee_scenario | trade_count | profit_factor | net_return_pct | max_drawdown_pct | avg_trade_pct | win_rate | longest_losing_streak | fee_monotonic_check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | base | 208 | 2.0173 | 6800.7629 | -70.2176 | 4.9579 | 30.7692 | 8 | True |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 2x | 208 | 1.9897 | 5745.9503 | -71.9017 | 4.8779 | 30.7692 | 8 | True |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 3x | 208 | 1.9626 | 4851.6992 | -73.4917 | 4.7979 | 30.7692 | 8 | True |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 5x | 208 | 1.9103 | 3451.2033 | -76.4105 | 4.6379 | 30.7692 | 8 | True |

## Drawdown
| strategy_id | max_dd_pct | average_dd_pct | longest_dd_duration_trades | worst_losing_streak | trade_cluster_count_48h | tail_loss_top5_share_pct |
| --- | --- | --- | --- | --- | --- | --- |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | -86.6249 | -47.0165 | 86 | 15 | 67 | 9.5929 |

## Trade Distribution
| strategy_id | top5_wins_profit_share_pct | top5_losses_loss_share_pct | median_trade_pct | p10_trade_pct | p90_trade_pct | outlier_dependency_warning |
| --- | --- | --- | --- | --- | --- | --- |
| QL_CRABEL_RANGE_EXPANSION_STAGE2_v0 | 44.1155 | 9.5929 | -4.6352 | -10.7853 | 27.7262 | True |
