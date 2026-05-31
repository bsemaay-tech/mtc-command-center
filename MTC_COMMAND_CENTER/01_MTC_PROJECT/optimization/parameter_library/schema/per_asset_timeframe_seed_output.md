# Per-Asset/Timeframe Seed Output Schema

Research seed only; not Pine default; not production parameter.

This schema defines the granular seed-ranking output required for staged optimization. It is intentionally asset/timeframe scoped so exit, risk, filter, and regime-mitigation stages do not rely on aggregate candidate rows.

## Required Fields

- `strategy_id`
- `producer_id`
- `asset`
- `symbol`
- `timeframe`
- `rank`
- `parameter_set_id`
- `parameter_hash`
- `source_run_id`
- `source_output_path`
- `dataset_ids`
- `source_type_summary`
- `st_factor`
- `global_atr_length`
- `sl_atr_mult`
- `tp_mode`
- `tp_r_multiple`
- `risk_long`
- `risk_short`
- `train_net_profit_pct`
- `validation_net_profit_pct`
- `test_net_profit_pct`
- `profit_factor`
- `max_drawdown_pct`
- `win_rate`
- `trade_count`
- `walkforward_consistency`
- `positive_window_ratio`
- `regime_summary`
- `regime_warning`
- `status`
- `confidence`
- `notes`

## Status Values

- `RESEARCH_SEED`
- `MEDIUM_SEED`
- `STRICT_SEED`
- `REJECTED`
- `INSUFFICIENT_DATA`
- `SMOKE_RESEARCH_SEED`

## Confidence Values

- `LOW`
- `MEDIUM`
- `HIGH`

## Policy

All rows are research evidence only. They must not be written into Pine defaults, described as production parameters, or used to claim TradingView release parity.
