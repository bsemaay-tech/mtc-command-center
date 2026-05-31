# QL_LINDA_5SMA_RS_PULLBACK_v0 Stage 2 Report

- Final classification: `STAGE2_WEAK`.
- Reason: drawdown high, parameter overfit risk.
- Aggregate PF: `1.6051`.
- 2x fee PF: `1.5480`.
- Holdout PF: `1.3026`.
- Parameter stability: `OVERFIT_RISK`.
- Best asset: `ETHUSDT`; worst asset: `XRPUSDT`; median asset: `SOLUSDT`.

## Asset Split
| strategy_id | asset | trade_count | profit_factor | net_return_pct | max_drawdown_pct | avg_trade_pct | win_rate | longest_losing_streak | source_summary_pf | source_summary_net_return_pct | source_summary_max_dd_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | BTCUSDT | 132 | 1.8341 | 181.2706 | -12.9904 | 0.8537 | 71.9697 | 2 | 1.8341 | 181.2706 | -12.9904 |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | ETHUSDT | 121 | 2.3538 | 621.9204 | -27.5066 | 1.8324 | 76.0331 | 2 | 2.3538 | 621.9204 | -27.5066 |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | SOLUSDT | 81 | 1.5012 | 92.4036 | -45.0518 | 1.0713 | 64.1975 | 4 | 1.5012 | 92.4036 | -45.0518 |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | BNBUSDT | 122 | 1.4778 | 89.6062 | -41.9776 | 0.7727 | 63.9344 | 3 | 1.4778 | 89.6062 | -41.9776 |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | XRPUSDT | 103 | 1.1648 | -9.2440 | -57.3299 | 0.4012 | 63.1068 | 5 | 1.1648 | -9.2440 | -57.3299 |

## Year Split
| strategy_id | year | trade_count | profit_factor | net_return_pct | max_drawdown_pct | avg_trade_pct | win_rate | longest_losing_streak |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 2024 | 133 | 1.3107 | 68.9425 | -47.6442 | 0.5553 | 65.4135 | 3 |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 2025 | 90 | 1.2533 | 24.9201 | -32.5406 | 0.3894 | 63.3333 | 6 |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 2026 | 2 | 0.1459 | -4.2647 | -4.9512 | -2.1145 | 50.0000 | 1 |

## Holdout
| strategy_id | train_assets | holdout_assets | selected_parameter_set | train_pf | train_net_return_pct | train_trade_count | holdout_pf | holdout_net_return_pct | holdout_max_drawdown_pct | holdout_trade_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | BTCUSDT,ETHUSDT,SOLUSDT | BNBUSDT,XRPUSDT | {"stop_mode": "none"} | 1.8923 | 3806.8501 | 334 | 1.3026 | 72.0790 | -59.2779 | 225 |

## Walk Forward
| strategy_id | train_start | train_end | test_start | test_end | selected_parameter_set | train_pf | test_pf | test_net_return_pct | test_trade_count | test_max_drawdown_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 2024-01-01 | 2024-07-01 | 2024-07-01 | 2024-10-01 | {"stop_mode": "none"} | 1.3234 | 0.5638 | -27.3744 | 20 | -38.8659 |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 2024-04-01 | 2024-10-01 | 2024-10-01 | 2025-01-01 | {"stop_mode": "none"} | 0.4444 | 2.2718 | 71.1835 | 35 | -13.5139 |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 2024-07-01 | 2025-01-01 | 2025-01-01 | 2025-04-01 | {"stop_mode": "none"} | 1.2954 | 0.6205 | -19.4754 | 16 | -22.7483 |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 2024-10-01 | 2025-04-01 | 2025-04-01 | 2025-07-01 | {"stop_mode": "none"} | 1.4568 | 2.0584 | 11.2117 | 21 | -4.4619 |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 2025-01-01 | 2025-07-01 | 2025-07-01 | 2025-10-01 | {"stop_mode": "none"} | 0.8882 | 2.2159 | 63.9781 | 43 | -14.8944 |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 2025-04-01 | 2025-10-01 | 2025-10-01 | 2026-01-01 | {"stop_mode": "none"} | 2.1862 | 0.6589 | -14.9318 | 10 | -19.1466 |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 2025-07-01 | 2026-01-01 | 2026-01-01 | 2026-04-01 | {"stop_mode": "none"} | 1.4994 | 0.1459 | -4.2647 | 2 | -4.9512 |

## Fee Stress
| strategy_id | fee_scenario | trade_count | profit_factor | net_return_pct | max_drawdown_pct | avg_trade_pct | win_rate | longest_losing_streak | fee_monotonic_check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | base | 559 | 1.6051 | 6622.8683 | -59.2779 | 0.9960 | 68.3363 | 6 | True |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 2x | 559 | 1.5480 | 4206.8013 | -60.9183 | 0.9160 | 67.2630 | 6 | True |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 3x | 559 | 1.4924 | 2658.0345 | -63.9652 | 0.8360 | 66.9052 | 6 | True |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 5x | 559 | 1.3861 | 1029.8537 | -69.7291 | 0.6760 | 66.5474 | 6 | True |

## Drawdown
| strategy_id | max_dd_pct | average_dd_pct | longest_dd_duration_trades | worst_losing_streak | trade_cluster_count_48h | tail_loss_top5_share_pct |
| --- | --- | --- | --- | --- | --- | --- |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | -67.4851 | -20.2539 | 148 | 6 | 280 | 18.1750 |

## Trade Distribution
| strategy_id | top5_wins_profit_share_pct | top5_losses_loss_share_pct | median_trade_pct | p10_trade_pct | p90_trade_pct | outlier_dependency_warning |
| --- | --- | --- | --- | --- | --- | --- |
| QL_LINDA_5SMA_RS_PULLBACK_v0 | 8.0425 | 18.1750 | 1.4346 | -5.6698 | 6.5435 | False |
