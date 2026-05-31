# QUANTLENS TRANSCRIPT INTAKE REPORT — Anthony Shi / Profitable Momentum Swing Trader

**Generated:** 2026-05-03  
**Source URL:** https://youtu.be/_QewlGLBaeA?si=ZoVcYdRIch1Lx_Df  
**Normalized URL:** https://www.youtube.com/watch?v=_QewlGLBaeA  
**Video ID:** `_QewlGLBaeA`  
**Uploaded Transcript File:** `Trading Millions How I Finally Became a Profitable Swing Trader.md`  
**Transcript Status:** Provided by user  
**Primary Speaker:** Anthony Shi  
**Host / Context:** TraderLion podcast interview  
**Core Topic:** Momentum swing trading, relative strength, sector/theme rotation, situational awareness, market cycle phase, watchlist/backwatch process, low win-rate/high R execution, progressive exposure, emotional control  
**Transcript SHA256:** `e67a5c27525431d6a9eea759dbb0f0b16b96e71d1ce5f2d36fca2e7822920b63`  

---

## 1. Executive Verdict

```yaml
verdict: ACCEPT_AS_HIGH_VALUE_SWING_TRADING_PROCESS_SOURCE
production_ready: false
backtest_ready: partial
pine_ready: no
strategy_family:
  - momentum_swing_trading
  - relative_strength_leadership
  - sector_theme_rotation
  - episodic_pivot_breakout
  - breakout_pullback
  - undercut_reclaim
  - cycle_aware_progressive_exposure
  - low_win_rate_high_R
priority: HIGH_FOR_PROCESS_ENGINE_AND_FILTERS
recommended_stage: Python_research_plus_process_extraction
```

This is a high-value source, but it is **less of a single mechanical entry strategy** and more of a complete discretionary momentum swing-trading operating system.

The strongest extractable components are:

- outlier leader selection,
- relative strength comparison,
- sector/theme confirmation,
- breakout/backwatch list tracking,
- market cycle / situational awareness classification,
- progressive exposure based on current market evidence,
- and strict loss respect.

This should not go directly to Pine as a producer. It should first become a **research/process layer** that can score when MTC or QuantLens should be aggressive, cautious, or inactive.

---

## 2. Quality & Relevance Score

```yaml
source_quality_score: 8.9/10
strategy_idea_score: 8.2/10
process_value_score: 9.4/10
risk_management_score: 8.7/10
implementation_clarity_score: 7.5/10
mtc_relevance_score: 8.0/10
crypto_transferability_score: 7.0/10
us_equity_transferability_score: 9.2/10
position_trading_value: 8.1/10
swing_trading_value: 9.5/10
day_trading_value: 5.8/10
```

### Strong points

- Very strong explanation of why pattern-only trading is insufficient.
- Clear hierarchy: pattern → relative strength → sector/theme → situational awareness → emotional discipline.
- Concrete review workflow: watchlist, biggest movers, backwatch list, sector grouping, journal.
- Strong risk framework: respect losses, keep losses small, use high R winners.
- Useful for QuantLens because it can become a **market regime / exposure-control layer**.
- Good fit for MTC V2 as filters/gates rather than one isolated signal producer.

### Weak points / limitations

- Many components are discretionary and require judgment.
- The edge is strongly dependent on equity-market cycles and sector leadership.
- Requires daily review data, earnings/catalysts, sector classification, and relative strength.
- Pure OHLCV backtest may underrepresent the real process.
- Crypto proxy is possible but needs adapted “sector/theme” equivalents.

---

## 3. Core Thesis

```yaml
core_thesis:
  - big_money_is_made_in_few_momentum_windows_per_year
  - only_trade_outlier_leaders
  - pattern_alone_is_not_enough
  - best_setups_have_relative_strength_plus_sector_theme_plus_right_cycle_phase
  - market_cycle_phase_changes_the_meaning_of_the_same_pattern
  - early_cycle_breakouts_can_work_strongly
  - late_cycle_breakouts_can_fail_or_squat
  - review_best_opportunities_not_only_your_own_trades
  - low_win_rate_is_acceptable_if_winners_are_large_and_losses_respected
  - situational_awareness_is_more_important_than_pattern_shape
```

The most important statement for QuantLens:

> The same entry pattern can be a buy signal early in a cycle and a warning/failure signal late in a cycle.

That means the main extract is not just “buy breakout.” The main extract is **cycle-aware breakout permission**.

---

## 4. Strategy Classification

```yaml
strategy_id: QL_ANTHONY_SHI_CYCLE_AWARE_MOMENTUM_SWING_v0
direction: long_biased
asset_class_native:
  - US_equities
  - growth_stocks
  - momentum_leaders
  - earnings_ep_stocks
  - thematic_sector_leaders
asset_class_proxy:
  - crypto_large_caps
  - crypto_sector_baskets
  - high_beta_crypto_tokens
timeframes:
  execution:
    - daily
    - intraday_for_entry_refinement
  context:
    - weekly
    - market_index_daily
    - sector_daily
holding_period:
  - days_to_weeks
  - sometimes_longer_if_trend_persists
```

This is not an intraday scalping strategy. It is a momentum swing framework that sometimes uses intraday entries to reduce risk and increase position size.

---

## 5. Key Framework — Four Layers of Edge

### Layer 1 — Pattern

```yaml
layer_1_pattern:
  examples:
    - bull_flag
    - breakout
    - breakout_pullback
    - episodic_pivot
    - undercut_reclaim
  weakness:
    - pattern_only_trading_has_unstable_results
    - same_pattern_has_different_meaning_by_cycle_phase
```

Pattern-only trading is the beginner layer. It is useful but insufficient.

### Layer 2 — Relative Strength

```yaml
layer_2_relative_strength:
  objective:
    - buy_the_strongest_stock
    - compare_stocks_against_each_other_daily
    - prefer_names_that_hold_up_when_market_pulls_back
  implementation:
    - rank_by_return_vs_index
    - rank_by_distance_from_high
    - rank_by_recovery_after_pullback
    - rank_by_breakout_followthrough
```

This can be directly converted into QuantLens filters.

### Layer 3 — Sector / Theme

```yaml
layer_3_sector_theme:
  objective:
    - trade_stocks_in_the_active_theme
    - identify_where_money_is_rotating
    - compare_leaders_inside_same_sector
  examples_from_transcript:
    - AI_semiconductors
    - Bitcoin_related_stocks
    - China_stocks
    - marijuana_regulation_theme
    - oil_or_war_headline_theme
```

In crypto, this can map to baskets:

```yaml
crypto_theme_proxy:
  - BTC_beta_names
  - ETH_beta_names
  - AI_tokens
  - DeFi_tokens
  - L1_L2_tokens
  - meme_tokens
  - exchange_tokens
```

### Layer 4 — Situational Awareness / Cycle Phase

```yaml
layer_4_situational_awareness:
  objective:
    - classify_where_the_market_is_in_the_momentum_cycle
    - adjust_entry_aggressiveness_and_position_size
    - avoid_late_cycle_breakout_failures
  phase_examples:
    - early_cycle
    - clear_momentum_expansion
    - euphoric_late_cycle
    - post_blowoff_cooling
    - chop_transition
```

This is the highest-value extraction for MTC.

---

## 6. Market Cycle Model

```yaml
cycle_model:
  premise:
    - major_momentum_windows_happen_only_few_times_per_year
    - big_moves_may_last_one_to_two_months
    - aggressive_trading_should_be_concentrated_in_these_windows
  phases:
    phase_0_chop_or_bear:
      behavior:
        - breakouts_fail
        - relief_rallies_short
        - followthrough_low
      action:
        - stay_small
        - preserve_capital
        - observe
    phase_1_early_turn:
      behavior:
        - first_leaders_emerge
        - strong_stocks_start_holding_up
        - catalyst_or_EP_names_respond_well
      action:
        - small_to_medium_size
        - test_leaders
        - look_for_breakout_proliferation
    phase_2_expansion:
      behavior:
        - clear_theme
        - multiple_leaders_follow_through
        - breakouts_work
        - gaps_hold
      action:
        - get_aggressive
        - use_progressive_exposure
        - focus_only_on_outlier_leaders
    phase_3_euphoria:
      behavior:
        - lower_quality_names_start_running
        - bottom_of_barrel_stocks_join
        - extension_extreme
      action:
        - harvest_gains
        - avoid_new_chase
        - tighten_review
    phase_4_distribution_or_cooling:
      behavior:
        - reversals_after_breakouts
        - breakouts_squat
        - more_breakdowns_than_breakouts
        - full_stops_cluster
      action:
        - reduce_exposure
        - stop_new_adds
        - protect_gains
```

### Critical insight

```yaml
same_pattern_different_phase:
  early_cycle:
    gap_up_from_base: bullish
    short_tight_consolidation: buyable
    red_day_after_initial_move: often_normal
  late_cycle:
    gap_up_from_base: can_fail
    short_tight_consolidation: can_be_extended
    red_day_after_initial_move: caution_signal
```

---

## 7. Core Setup A — Outlier Leader Breakout

```yaml
candidate_id: QL_ANTHONY_OUTLIER_LEADER_BREAKOUT_v0
type: signal_producer_candidate
direction: long
timeframe: daily
priority: HIGH
```

### Concept

Buy only the leading stocks in the strongest market themes when they break out from constructive bases during a favorable cycle phase.

### Objective v0 rules

```yaml
universe:
  - US_equity_or_crypto_proxy
  - top_relative_strength_names
  - strong_sector_or_theme_membership
  - sufficient_dollar_volume

setup:
  - base_or_consolidation
  - price_near_highs
  - prior_uptrend_or_EP_catalyst
  - breakout_above_base_high
  - volume_expansion_preferred
  - market_phase_not_late_distribution

entry:
  - daily_breakout
  - or_intraday_opening_range_reclaim_for_tighter_risk

stop:
  - low_of_day
  - base_low
  - opening_range_low
  - intraday_refinement_stop

exit:
  - partial_into_extension
  - trail_remainder_with_10/20/50_MA_area
  - reduce_on_distribution_or_failed_followthrough
```

### MTC mapping

This can become a long producer only after market-phase filter exists. Without that filter, it is too generic.

---

## 8. Core Setup B — Breakout Pullback / Pullback Buy

```yaml
candidate_id: QL_ANTHONY_BREAKOUT_PULLBACK_RS_v0
type: signal_producer_candidate
direction: long
timeframe:
  - daily
  - intraday_for_entry
priority: HIGH
```

### Concept

After a strong breakout, price pulls back constructively without fully failing. A reclaim or tight pullback entry can provide better risk than chasing the initial breakout.

### Objective v0 rules

```yaml
setup:
  - recent_breakout_with_followthrough
  - pullback_to_key_area
  - pullback_does_not_destroy_structure
  - relative_strength_vs_market_remains_positive
  - sector_theme_still_active
  - market_not_in_distribution

entry:
  - reclaim_of_pullback_high
  - undercut_reclaim_of_breakout_level
  - intraday_range_break_after_pullback

stop:
  - under_pullback_low
  - under_breakout_failure_level

exit:
  - trail_if_resumes
  - cut_if_reclaim_fails
```

This is a better candidate for systematic testing than pure discretionary cycle reading.

---

## 9. Core Setup C — Undercut & Reclaim / Breakdown-Level Reclaim

```yaml
candidate_id: QL_ANTHONY_UNDERCUT_RECLAIM_LEADER_v0
type: signal_producer_candidate
direction: long
priority: MEDIUM_HIGH
```

### Concept

A strong leader undercuts a key level, shakes out weak holders, then reclaims the level. If the stock is still a leading name in an active theme, reclaim can trigger a strong move.

### Objective v0 rules

```yaml
setup:
  - prior_leader_or_theme_stock
  - recent_failed_pullback_or_undercut
  - reclaim_of_key_level
  - relative_strength_still_positive
  - sector_not_dead

entry:
  - reclaim_close_above_level
  - or_intraday_reclaim_with_range_confirmation

stop:
  - below_undercut_low
  - or below_reclaim_day_low

exit:
  - trail_under_short_MA
  - sell_if_reclaim_fails
```

This has good QuantLens value because it is more mechanical.

---

## 10. Core Setup D — Episodic Pivot / Earnings Gap

```yaml
candidate_id: QL_ANTHONY_EP_EARNINGS_THEME_BREAKOUT_v0
type: signal_producer_candidate
direction: long
priority: HIGH_NATIVE_US_EQUITY
```

### Concept

A strong earnings/catalyst gap can start or confirm a new momentum cycle. The key is not just the gap itself, but whether the stock and related sector/theme follow through.

### Objective v0 rules

```yaml
setup:
  - earnings_or_news_gap
  - gap_percent_above_threshold
  - closes_strong_or_holds_gap
  - sector_peers_confirm
  - market_reaction_positive
  - breakout_proliferation_optional

entry:
  - EP_day_intraday_entry_if_tight_risk
  - next_day_continuation
  - breakout_pullback_after_EP

stop:
  - low_of_EP_day
  - intraday_low_if_refined

exit:
  - trail_winner
  - reduce_if_EP_fails_or_sector_does_not_confirm
```

### Data limitation

For true EP testing, earnings dates and event classification are needed. Without event data, use large gap + volume as proxy.

---

## 11. Process Module — Backwatch List / Breakout Health Tracker

```yaml
candidate_id: QL_ANTHONY_BACKWATCH_BREAKOUT_HEALTH_ENGINE_v0
type: market_context_engine
priority: VERY_HIGH
```

### Concept

Maintain a sequential record of major breakouts and track whether they follow through or fail. This becomes a market-health indicator more relevant than generic breadth indicators.

### Objective v0 fields

```yaml
backwatch_row:
  - symbol
  - date
  - sector_or_theme
  - setup_type
  - breakout_day_return
  - breakout_day_volume_ratio
  - close_location
  - followthrough_1d
  - followthrough_3d
  - followthrough_5d
  - max_gain_after_breakout
  - max_drawdown_after_breakout
  - failed_breakout_boolean
  - breakdown_boolean
  - notes
```

### Derived metrics

```yaml
market_health_metrics:
  - breakout_count_5d
  - breakout_count_10d
  - breakout_success_rate_5d
  - median_followthrough_3d
  - failed_breakout_ratio
  - more_breakdowns_than_breakouts
  - number_of_active_themes
  - concentration_in_top_theme
```

### MTC use

```yaml
mtc_use:
  - exposure_gate
  - trade_frequency_gate
  - enable_long_gate
  - risk_pct_multiplier
  - no_new_long_gate_when_breakout_health_bad
```

This is one of the most valuable practical ideas from the transcript.

---

## 12. Process Module — Sector / Theme Leadership Engine

```yaml
candidate_id: QL_ANTHONY_THEME_LEADERSHIP_ENGINE_v0
type: filter_gate_candidate
priority: VERY_HIGH
```

### Concept

A strong stock is safer when it belongs to a strong theme. A random strong chart without a theme has lower priority.

### Objective v0 rules

```yaml
theme_detection:
  - group_symbols_by_sector_or_crypto_category
  - measure_rolling_group_return
  - measure_number_of_breakouts_in_group
  - measure_relative_strength_vs_market
  - rank_groups_by_momentum_and_followthrough

leader_detection:
  - top_return_within_theme
  - top_relative_strength_vs_theme
  - best_gap_hold_behavior
  - strongest_close_location
  - highest_dollar_volume_quality
```

### Entry permission

```yaml
entry_filter:
  allow_long_if:
    - symbol_RS_rank_high
    - theme_RS_rank_high
    - market_health_not_bad
  block_or_reduce_if:
    - random_stock_no_theme
    - theme_is_late_and_euphoric
    - more_breakdowns_than_breakouts
```

This is highly relevant to MTC as a gate.

---

## 13. Process Module — Cycle-Aware Exposure Control

```yaml
candidate_id: QL_ANTHONY_CYCLE_AWARE_EXPOSURE_CONTROL_v0
type: portfolio_guard_candidate
priority: VERY_HIGH
```

### Concept

Risk should not be constant. Exposure should expand when leaders are working and contract when breakouts fail.

### Suggested v0 model

```yaml
risk_multiplier_by_phase:
  chop_or_bear:
    risk_multiplier: 0.0_to_0.25
    max_new_positions: 0_to_1
  early_turn:
    risk_multiplier: 0.25_to_0.50
    max_new_positions: 1_to_2
  expansion:
    risk_multiplier: 1.0
    max_new_positions: normal_or_high
  euphoria:
    risk_multiplier: 0.50_to_0.75
    action: harvest_and_be_selective
  distribution:
    risk_multiplier: 0.0_to_0.25
    action: protect_gains
```

### Bias change rules from transcript

```yaml
turn_more_bullish_if:
  - setup_or_breakout_proliferation_in_theme
  - news_catalyst_or_EP_stocks_act_well
  - bad_economic_news_does_not_make_market_drop
  - strong_stocks_gap_up_and_hold

turn_more_cautious_if:
  - significant_distribution_day
  - breakouts_reverse_hard_after_day_1_to_3
  - three_days_of_full_stops
  - strategy_drawdown_around_3_percent_or_more
  - more_breakdowns_than_breakouts
  - leading_names_top_or_fail
```

---

## 14. Performance / Expectancy Extract

```yaml
reported_metrics:
  hit_rate: approximately_20_percent
  win_loss_ratio: approximately_5.5_to_7.5
  best_week_win_loss_ratio: up_to_20_plus
  2024_ytd_unique_tickers: approximately_61
  2024_ytd_trades: approximately_217
  trades_per_ticker: approximately_3.5
  style:
    - low_win_rate
    - high_R_winners
    - aggressive_when_conditions_align
```

### Interpretation

The system is built around asymmetric payoff:

```yaml
expectancy_model:
  low_hit_rate: accepted
  small_losses: mandatory
  large_winners: required
  outlier_leaders: mandatory
  market_phase: decisive
```

This means backtests must not optimize for win rate. They must optimize for:

- maximum favorable excursion capture,
- average win / average loss,
- drawdown control,
- and whether the system catches the few true leaders.

---

## 15. Risk Management Extract

```yaml
risk_management:
  principles:
    - respect_losses_always
    - no_blowups_if_losses_are_respected
    - use_stops
    - reduce_when_not_calibrated
    - if_taking_full_stops_for_multiple_days_something_is_wrong
    - position_size_based_on_tight_risk_not_random_confidence

entry_risk:
  - intraday_entry_used_to_reduce_risk
  - limit_buy_plus_stop_possible
  - low_of_day_or_opening_range_low_as_stop
  - percent_from_high_to_low_of_day_checked_for_sizing

position_sizing:
  - use_bigger_size_when_tight_stop_and_leader_quality_align
  - add_when_risk_can_stay_same_or_lower
  - raise_stop_after_adds
  - be careful in volatile stocks because tight stops reduce win rate
```

### Important MTC adaptation

The transcript supports MTC’s idea of separating:

```yaml
mtc_separation:
  - signal_quality
  - entry_timing
  - position_sizing
  - exposure_state
  - exit_management
```

This source is especially valuable for **portfolio/exposure state**.

---

## 16. Tools / Indicators Mentioned

```yaml
indicators_and_context:
  moving_averages:
    - 10_SMA_EMA
    - 20_SMA_EMA
    - 50_SMA_EMA
  levels:
    - low_of_day
    - high_of_day
    - opening_range
    - prior_breakdown_range
    - horizontal_support_resistance
  metrics:
    - ADR
    - average_dollar_volume
    - float
    - relative_strength
    - percent_from_high_to_low_of_day
  chart_context:
    - daily
    - intraday
    - sector_ETFs
    - peers
```

He uses EMA/SMA clouds not as magic signals, but as trend/reference areas.

---

## 17. Native Data Requirements

```yaml
required_data_for_best_test:
  US_equity:
    - daily_OHLCV
    - intraday_OHLCV_for_entry_refinement
    - sector_or_industry_classification
    - earnings_dates
    - average_dollar_volume
    - float
    - index_data_QQQ_SPY
    - sector_ETF_or_peer_mapping
    - delisted_or_survivorship_bias_control_preferred

crypto_proxy:
  - daily_OHLCV
  - intraday_OHLCV_optional
  - category_mapping_AI_DeFi_L1_meme_exchange
  - BTC_ETH_market_context
  - volume_and_dollar_volume
```

### Crypto transferability

Crypto can test:

- relative strength leader selection,
- theme basket strength,
- breakout/pullback,
- undercut reclaim,
- exposure control by breakout health.

Crypto cannot directly test:

- earnings EP,
- equity sector catalysts,
- float,
- US market session effects,
- stock-specific institutional flows.

---

## 18. MTC V2 Mapping

```yaml
mtc_mapping:
  producer_candidates:
    - QL_ANTHONY_OUTLIER_LEADER_BREAKOUT_v0
    - QL_ANTHONY_BREAKOUT_PULLBACK_RS_v0
    - QL_ANTHONY_UNDERCUT_RECLAIM_LEADER_v0

  filter_gate_candidates:
    - relative_strength_rank_gate
    - sector_theme_strength_gate
    - breakout_health_gate
    - market_phase_gate
    - ADR_extension_gate
    - average_dollar_volume_gate

  portfolio_guards:
    - cycle_aware_exposure_multiplier
    - three_full_stop_caution_guard
    - strategy_drawdown_caution_guard
    - more_breakdowns_than_breakouts_guard

  signal_transform:
    - wait_for_pullback_after_breakout
    - undercut_reclaim_confirmation
    - intraday_entry_refinement

  exits:
    - trail_remainder_with_10/20/50_MA_area
    - partial_exit_into_extension
    - reduce_on_distribution
    - exit_failed_breakout
```

### Best MTC use

```yaml
best_mtc_use:
  primary: market_context_and_exposure_gate
  secondary: relative_strength_filter
  tertiary: long_breakout_producer
```

This is not primarily a Pine indicator idea. It is a **selection and regime framework**.

---

## 19. Recommended Research Order

```yaml
research_order:
  1:
    id: QL_ANTHONY_BACKWATCH_BREAKOUT_HEALTH_ENGINE_v0
    reason: highest_process_value_and_transferability
  2:
    id: QL_ANTHONY_THEME_LEADERSHIP_ENGINE_v0
    reason: improves_stock_or_asset_selection
  3:
    id: QL_ANTHONY_CYCLE_AWARE_EXPOSURE_CONTROL_v0
    reason: directly_maps_to_MTC_position_manager_and_guards
  4:
    id: QL_ANTHONY_BREAKOUT_PULLBACK_RS_v0
    reason: most_testable_entry_model
  5:
    id: QL_ANTHONY_UNDERCUT_RECLAIM_LEADER_v0
    reason: useful_second_entry_model
  6:
    id: QL_ANTHONY_OUTLIER_LEADER_BREAKOUT_v0
    reason: good_but_requires_phase_filter
  7:
    id: QL_ANTHONY_EP_EARNINGS_THEME_BREAKOUT_v0
    reason: high_value_but_requires_earnings_data
```

---

## 20. Python Research Plan

### Suggested folder

```text
06_QUANTLENS_LAB/research/anthony_shi_cycle_aware_momentum/
```

### Suggested files

```text
README.md
anthony_setup_definitions.yml
relative_strength.py
theme_leadership.py
breakout_health.py
cycle_phase.py
breakout_pullback.py
undercut_reclaim.py
run_anthony_shi_research.py
QL_ANTHONY_SHI_CYCLE_AWARE_MOMENTUM_REPORT.md
QL_ANTHONY_SHI_RESULTS.csv
QL_ANTHONY_SHI_TRADES.csv
QL_ANTHONY_BREAKOUT_HEALTH.csv
QL_ANTHONY_THEME_RANKS.csv
```

### Minimum initial crypto proxy test

```yaml
crypto_proxy_test:
  assets_minimum: 10
  preferred_assets:
    - BTCUSDT
    - ETHUSDT
    - SOLUSDT
    - BNBUSDT
    - XRPUSDT
    - DOGEUSDT
    - AVAXUSDT
    - LINKUSDT
    - NEARUSDT
    - OPUSDT
  timeframes:
    - 1D_for_core
    - 4H_optional
    - 1H_optional_entry_refinement
  labels:
    - all_results_must_be_CRYPTO_PROXY
```

### Native US equity test

```yaml
native_equity_test:
  assets_minimum: 50
  preferred_universe:
    - Nasdaq_growth
    - high_RS_stocks
    - earnings_gap_names
    - sector_ETF_constituents
  required:
    - QQQ_SPY_context
    - sector_grouping
    - earnings_dates_if_testing_EP
```

---

## 21. Backtest Metrics to Measure

```yaml
metrics:
  normal:
    - net_return
    - PF
    - max_drawdown
    - trade_count
    - win_rate
    - average_win
    - average_loss
    - avg_win_loss_ratio
  strategy_specific:
    - leader_rank_at_entry
    - theme_rank_at_entry
    - breakout_health_score_at_entry
    - cycle_phase_at_entry
    - followthrough_1d_3d_5d
    - failed_breakout_rate
    - MFE_capture_ratio
    - stops_cluster_count
    - return_concentration_top_10_trades
    - performance_by_cycle_phase
    - performance_by_theme_rank
```

### Very important diagnostic

```yaml
must_test:
  - same_breakout_rules_with_and_without_theme_filter
  - same_breakout_rules_with_and_without_market_phase_filter
  - same_breakout_rules_with_and_without_relative_strength_filter
```

If filters do not improve expectancy, the extracted thesis is not supported.

---

## 22. Acceptance / Rejection Criteria

```yaml
accept_as_stage_2_filter_if:
  - relative_strength_filter_improves_PF
  - theme_filter_improves_avg_win_loss
  - breakout_health_filter_reduces_drawdown
  - cycle_phase_filter_reduces_failed_breakouts
  - exposure_multiplier_improves_return_to_drawdown
  - works_across_multiple_assets_or_sectors

accept_as_signal_producer_if:
  - breakout_pullback_or_undercut_reclaim_has_PF_after_costs >= 1.25
  - trade_count_sufficient
  - outlier_dependence_not_extreme
  - works_in_at_least_5_assets_native_or_10_crypto_proxy_assets
  - cost_stress_monotonic
  - no_lookahead_bias

downgrade_to_process_only_if:
  - standalone_entries_weak
  - but_context_filters_improve_existing_strategies

reject_if:
  - only_works_on_one_theme
  - only_profitable_before_costs
  - uses_future_leader_information
  - uses_survivorship_biased_universe_without_warning
  - crypto_proxy_claims_native_equity_validity
```

---

## 23. Relationship to Existing QuantLens Reports

```yaml
related_reports:
  Gon_Gajala_Low_Float_Momentum:
    relation:
      - both_focus_on_leaders_and_low_win_rate_high_R
      - Gon_is_intraday_low_float_day_trading
      - Anthony_is_swing_cycle_and_sector_theme_process
      - both_emphasize_cutting_losses_and_big_winners

  CANSLIM:
    relation:
      - overlaps_growth_stock_leadership
      - Anthony_process_more_tactical_and_cycle_aware
      - CANSLIM_can_supply_fundamental_quality_layer

  Oliver_Kell_Cycle:
    relation:
      - strong_overlap_on_market_cycle_phase
      - Anthony_adds_process_for_breakout_health_and_theme_tracking

  Brian_Shannon_AVWAP:
    relation:
      - AVWAP_can_help_refine_pullback_reclaim_entries
      - Anthony_uses_horizontal_breakdown_ranges_and_MA_clouds

  Daily_Extension_Anti_Chase:
    relation:
      - useful_to_avoid_late_cycle_chase
      - Anthony_warns_late_cycle_breakouts_squat_or_fail

  EMA20_50_Retest:
    relation:
      - Anthony_MA_use_is_context_not_crossover
      - generic_MA_crossover_less_valuable_than_RS_theme_cycle_filter
```

---

## 24. Best Combined QuantLens Model

```yaml
combined_model:
  name: QL_CYCLE_AWARE_RELATIVE_STRENGTH_MOMENTUM_ENGINE_v0
  components:
    - Anthony_breakout_health_tracker
    - Anthony_theme_leadership_ranker
    - Anthony_cycle_phase_gate
    - CANSLIM_quality_optional
    - Oliver_Kell_cycle_context
    - Daily_Extension_Anti_Chase
    - MTC_position_sizing_and_exposure_guard
    - MTC_partial_exit_and_trailing
```

### Intended use

```yaml
intended_use:
  - decide_when_to_enable_long_momentum_strategies
  - rank_best_assets_or_stocks
  - prevent_pattern_only_entries
  - scale_risk_by_cycle_phase
  - protect_account_when_breakouts_stop_working
```

This combined model is likely more valuable than coding an isolated Anthony-style breakout producer.

---

## 25. Key Implementation Hazards

```yaml
hazards:
  lookahead_bias:
    - cannot_rank_leaders_using_future_performance
    - theme_membership_must_be_known_at_time_of_trade
  survivorship_bias:
    - equity_tests_need_delisted_or_historical_universe_warning
  event_bias:
    - EP_tests_need_actual_earnings_dates_or_gap_proxy_label
  discretion_gap:
    - human_process_may_not_map_cleanly_to_code
  overfitting:
    - too_many_filters_can_curve_fit
  crypto_proxy_mislabeling:
    - crypto_proxy_can_validate_structure_not_US_equity_edge
```

---

## 26. Final Rating

```yaml
final_rating:
  research_value: 9.0/10
  process_engine_value: 9.5/10
  standalone_signal_value: 7.2/10
  filter_gate_value: 9.0/10
  market_regime_value: 9.2/10
  position_sizing_value: 8.4/10
  mtc_v2_relevance: 8.0/10
  crypto_proxy_value: 7.0/10
  native_US_equity_value: 9.2/10
  pine_priority_now: 2/10
  python_research_priority: 8.8/10
  live_readiness: 2/10
```

---

## 27. Final Decision

```yaml
final_decision:
  action: ACCEPT_AS_PROCESS_AND_FILTER_SOURCE
  classification: HIGH_VALUE_CYCLE_AWARE_MOMENTUM_SWING_FRAMEWORK
  best_use:
    - market_phase_gate
    - relative_strength_filter
    - theme_leadership_ranker
    - breakout_health_tracker
    - exposure_control_guard
    - long_momentum_context_layer
  next_step:
    - do_not_convert_to_Pine_now
    - build_Python_research_modules_first
    - test_context_filters_against_existing_momentum_entries
    - test_crypto_proxy_but_label_it_clearly
    - later_test_native_US_equity_if_data_available
  do_not_do:
    - do_not_reduce_this_to_simple_breakout
    - do_not_ignore_cycle_phase
    - do_not_claim_pattern_only_edge
    - do_not_use_future_leader_info
```

Final conclusion:

> This is one of the strongest process-level transcripts so far. The immediate value is not a single strategy; it is a **cycle-aware relative-strength and theme-leadership engine** that can decide when breakout/pullback strategies deserve exposure. For MTC V2, this should be treated primarily as a **market context + exposure gate**, then secondarily as a long momentum producer candidate.
