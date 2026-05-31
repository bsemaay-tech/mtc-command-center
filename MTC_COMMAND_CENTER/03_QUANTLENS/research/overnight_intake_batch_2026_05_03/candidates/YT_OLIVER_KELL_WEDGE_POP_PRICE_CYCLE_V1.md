# Candidate: YT_OLIVER_KELL_WEDGE_POP_PRICE_CYCLE_V1

**candidate_id**: YT_OLIVER_KELL_WEDGE_POP_PRICE_CYCLE_V1

**source_file**: YT_m8F3KkBDtC0_Intake_Report_2026-05-03.md

**source_url**: https://www.youtube.com/watch?v=m8F3KkBDtC0

**video_id**: m8F3KkBDtC0

**asset_class**: unknown

**timeframe**: unknown

**direction**: unknown

**priority**: MEDIUM

**verdict**: UNKNOWN

**rules**: {'candidate_id': 'YT_OLIVER_KELL_WEDGE_POP_PRICE_CYCLE_V1', 'universe': {'asset_class': 'equities', 'min_price': 10, 'min_avg_dollar_volume_20d': 20000000}, 'timeframes': {'context': 'weekly', 'signal': 'daily', 'execution': 'daily_first', 'intraday_optional': ['60m', '15m', '5m']}, 'moving_averages': {'fast_ema': 10, 'slow_ema': 20, 'reference_sma': 50, 'weekly_reference_ma': 10}, 'regime': {'green_light': {'close_above_fast_ema': True, 'close_above_slow_ema': True, 'fast_above_or_near_slow': True}, 'red_light': {'close_below_fast_and_slow': True, 'wedge_drop_confirmed': True}}, 'entry': {'primary_setup': 'wedge_pop', 'require_volatility_contraction': True, 'pivot_window': 3, 'max_entry_extension_pct': 3.0, 'no_chase': True, 'allow_ema_crossback': True, 'allow_base_and_break': True, 'allow_wick_play_contextual': True}, 'risk': {'initial_stop_mode': 'daily_low', 'allow_intraday_tight_stop': True, 'scratch_if_not_profitable_eod': 'optional', 'move_stop_after_pivot_confirmation': True}, 'position_sizing': {'top_idea_pct': [25, 35], 'core_idea_pct': [15, 20], 'volatile_or_lower_conviction_pct': [5, 15], 'scale_down_by_stop_distance': True}, 'exits': {'reduce_on_exhaustion_extension': True, 'exit_on_wedge_drop': True, 'reduce_or_exit_on_loss_of_20ema': 'testable', 'scale_out_not_all_at_once': True}}

