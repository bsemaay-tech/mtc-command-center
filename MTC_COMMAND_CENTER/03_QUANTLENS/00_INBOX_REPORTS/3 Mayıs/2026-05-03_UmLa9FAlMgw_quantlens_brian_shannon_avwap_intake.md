# QUANTLENS TRANSCRIPT INTAKE REPORT — Brian Shannon / AVWAP Trading Indicator Secrets and Setups

**Generated:** 2026-05-03  
**Source URL:** https://youtu.be/UmLa9FAlMgw?si=bqyEc59JFMCVzcGH  
**Normalized URL:** https://www.youtube.com/watch?v=UmLa9FAlMgw  
**Video ID:** `UmLa9FAlMgw`  
**Uploaded Transcript File:** `The AVWAP Trading Indicator Secrets and Setups Brian Shannon, CMT.md`  
**Transcript Status:** Provided by user  
**Primary Speaker:** Brian Shannon, CMT  
**Host / Context:** TraderLion podcast interview  
**Core Topic:** Anchored VWAP, VWAP psychology, trend alignment, gap setups, AVWAP pinch, AVWAP handoff, risk management, multi-timeframe entry timing, 5-day MA, 20/50/200-day MA context  
**Transcript SHA256:** `3163f849dd96e25dc53ca8189341e454b9a4271b74b009049b603522740829e4`  

---

## 1. Executive Verdict

```yaml
verdict: ACCEPT_AS_HIGH_VALUE_AVWAP_FRAMEWORK
production_ready: false
backtest_ready: yes_python_first
pine_ready: no_not_initially
strategy_family:
  - anchored_vwap
  - multi_timeframe_trend_alignment
  - gap_pullback_strength_after_touch
  - avwap_pinch
  - avwap_handoff
  - stage_analysis
  - moving_average_confluence
  - breakout_pullback_entry
priority: VERY_HIGH
recommended_stage: python_research_signal_and_filter_suite
```

This transcript is a high-quality source. Brian Shannon’s AVWAP framework is not a single mechanical indicator rule like “buy when price touches AVWAP.” The useful edge is the **combination of:**

- meaningful anchor selection,
- multi-timeframe trend context,
- volume-weighted price memory,
- moving-average confluence,
- short-term momentum confirmation,
- stop placement under the most recent relevant higher low / lower high,
- and partial profit-taking in choppy markets.

This should be treated as a **QuantLens AVWAP research suite**, not a direct Pine integration yet.

---

## 2. Quality & Relevance Score

```yaml
source_quality_score: 9.3/10
strategy_idea_score: 8.8/10
risk_management_score: 9.0/10
implementation_clarity_score: 8.2/10
mtc_relevance_score: 9.0/10
crypto_transferability_score: 8.0/10
equity_transferability_score: 9.5/10
futures_transferability_score: 8.0/10
position_trading_value: 8.5/10
swing_trading_value: 9.5/10
day_trading_value: 8.0/10
```

### Strong points

- AVWAP combines price, volume, and time into one level.
- Framework explains *why* levels matter: average long/short participant psychology.
- Very compatible with Stage Analysis / Weinstein-style regime filtering.
- Very useful as an MTC V2 filter, producer, and stop/position management aid.
- Strong emphasis on not buying the touch blindly; instead buy strength after the touch.
- Strong emphasis on using AVWAP as a **level of interest**, not a magic signal.
- Good fit for crypto because Binance/crypto data has reliable volume, though volume structure differs from equities.

### Weak points / caution

- Anchor selection has discretionary elements.
- Backtest must define anchors objectively.
- Directly coding “important event” anchors requires reliable event data for equities; crypto has fewer clean fundamental events.
- AVWAP can overfit badly if every local high/low becomes an anchor.
- Brian’s framework is heavily visual and multi-timeframe; naive mechanical conversion may underperform.

---

## 3. Core Thesis

```yaml
core_thesis:
  - AVWAP_is_price_volume_time_memory
  - AVWAP_shows_average_participant_cost_basis_from_event
  - levels_are_not_signals_they_are_areas_of_interest
  - buy_strength_after_pullback_not_blind_touch
  - short_failure_after_rejection_not_blind_touch
  - use_shorter_timeframe_to_confirm_trade_near_higher_timeframe_level
  - trend_alignment_controls_trade_direction
  - stop_goes_below_recent_relevant_higher_low_for_longs
  - stop_goes_above_recent_relevant_lower_high_for_shorts
  - partial_profit_reduces_risk_in_choppy_market
  - 5_day_MA_is_key_intermediate_trend_tool
```

Brian’s most valuable rule for QuantLens:

> AVWAP is not a buy/sell trigger. It is a level where you study whether buyers or sellers are regaining control.

---

## 4. Key AVWAP Concepts Extracted

### 4.1 AVWAP definition

```yaml
indicator: Anchored VWAP
formula_concept:
  - cumulative_price_volume_from_anchor / cumulative_volume_from_anchor
preferred_price_input:
  - OHLC4
  - open_high_low_close_divided_by_4
purpose:
  - measure_average_participant_cost_basis
  - identify_buyer_or_seller_control
  - locate price_memory_from_event
```

Brian strongly prefers an inclusive price input, ideally OHLC4 for bar-based data, because open and close are high-liquidity parts of the session.

### 4.2 AVWAP is a psychology tool

```yaml
interpretation:
  price_above_AVWAP:
    - average_long_from_anchor_is_winning
    - average_short_from_anchor_is_losing
    - buyers_have_control
  price_below_AVWAP:
    - average_long_from_anchor_is_losing
    - average_short_from_anchor_is_winning
    - sellers_have_control
  slope_up:
    - motivated_buyers
    - strong_accumulation
  slope_down:
    - motivated_sellers
    - distribution_or_failed_demand
```

### 4.3 AVWAP is a level of interest, not a trade command

```yaml
wrong_use:
  - buy_because_price_touches_AVWAP
  - short_because_price_touches_AVWAP
  - assume_AVWAP_must_hold

correct_use:
  - mark_level_of_interest
  - drill_down_to_lower_timeframe
  - wait_for_strength_after_touch_for_longs
  - wait_for_failure_after_touch_for_shorts
  - define_stop_by_recent_structure
```

This is critical. QuantLens should avoid implementing “touch AVWAP = entry” as the main rule.

---

## 5. Anchor Selection Rules

```yaml
anchor_candidates:
  event_anchors:
    - earnings_report
    - major_gap
    - analyst_upgrade_or_downgrade
    - IPO
    - beginning_of_year
    - high_volume_catalyst
  price_structure_anchors:
    - major_swing_low
    - major_swing_high
    - breakdown_point
    - breakout_point
    - shakeout_low
    - failed_gap_low
    - recent_high_where_sellers_took_control
  trend_anchors:
    - year_to_date
    - covid_low_or_macro_low
    - cycle_high
    - cycle_low
```

### Backtest-safe anchor priority

For objective Python research, use these first:

```yaml
objective_anchor_priority:
  1: year_to_date_open
  2: rolling_n_day_high
  3: rolling_n_day_low
  4: gap_day_high_volume
  5: breakout_day
  6: breakdown_day
  7: earnings_event_if_equity_data_available
```

### Avoid initially

```yaml
avoid_initially:
  - manually_selected_visual_anchor
  - every_pivot_as_anchor
  - subjective_news_quality_anchor
  - unlimited_anchor_stack
```

---

## 6. Candidate Strategy A — AVWAP Gap Pullback Strength

```yaml
candidate_id: QL_BRIAN_SHANNON_AVWAP_GAP_PULLBACK_STRENGTH_v0
type: signal_producer_candidate
direction: long_primary
timeframes:
  primary:
    - 1D
  execution:
    - 30m
    - 65m
    - 15m
asset_classes:
  - equities
  - crypto_proxy
  - futures_proxy
priority: VERY_HIGH
```

### Concept

A stock gaps up on a meaningful catalyst. Do not chase the gap. Wait for price to settle, pull back, and then regain strength above VWAP/AVWAP while the higher-timeframe trend remains constructive.

### Objective v0 rules

```yaml
setup:
  - gap_up_percent >= [3, 5, 8]
  - volume_ratio >= [1.5, 2.0, 3.0]
  - close_above_gap_day_open_or_midpoint
  - daily_trend_not_stage_4

anchor:
  - gap_day_open
  - gap_day_low
  - gap_day_high
  - gap_day_start_bar

entry:
  - price_pulls_back_toward_gap_AVWAP_or_daily_VWAP
  - price_reclaims_short_term_AVWAP
  - 5_day_MA_flat_to_rising
  - lower_timeframe_higher_high_after_higher_low

stop:
  - below_recent_relevant_higher_low
  - or_below_AVWAP_cluster
  - optional_half_stop_under_morning_low_half_under_structural_low

exit:
  - first_third_at_prior_resistance_or_R_multiple
  - trail_balance_under_new_higher_lows
  - exit_if_price_loses_5_day_MA_and_AVWAP_cluster
```

### Why useful

This is the transcript’s strongest actionable setup. It maps well to gap/backfill/continuation patterns and can be coded with minimal ambiguity.

---

## 7. Candidate Strategy B — AVWAP Pinch Breakout

```yaml
candidate_id: QL_BRIAN_SHANNON_AVWAP_PINCH_BREAKOUT_v0
type: signal_producer_candidate
direction: long_short
timeframes:
  - 1D
  - 30m
  - 65m
priority: HIGH
```

### Concept

Price gets compressed between AVWAP from a significant low and AVWAP from a significant high, often with moving averages curling underneath. The “pinch” itself is not the signal; the signal is a confirmed break away from compression with trend alignment.

### Objective v0 rules

```yaml
pinch_definition:
  lower_AVWAP:
    - AVWAP_from_year_to_date_low_or_major_swing_low
  upper_AVWAP:
    - AVWAP_from_major_swing_high_or_gap_high
  compression:
    - distance_between_AVWAPs_as_ATR <= [0.5, 0.75, 1.0, 1.5]
    - price_between_AVWAPs_or_near_upper_break
  trend_context_long:
    - 20MA_rising_or_flat
    - 50MA_rising_or_flat
    - price_above_200MA_optional
  trigger_long:
    - close_above_upper_AVWAP
    - lower_timeframe_higher_high
    - 5_day_MA_rising
  trigger_short:
    - close_below_lower_AVWAP
    - lower_timeframe_lower_low
    - 5_day_MA_declining
```

### Caution

People often misuse the pinch by pointing to any AVWAP compression. The test must require trend context and post-pinch confirmation.

---

## 8. Candidate Strategy C — AVWAP Handoff Trend Continuation

```yaml
candidate_id: QL_BRIAN_SHANNON_AVWAP_HANDOFF_TREND_CONTINUATION_v0
type: trend_continuation_module
direction: long_short
timeframes:
  - 30m
  - 65m
  - 1D
priority: HIGH
```

### Concept

During an uptrend, AVWAP support shifts from an older anchor to a newer higher-low anchor. This “handoff” confirms that buyers remain motivated at progressively higher prices.

### Objective v0 rules

```yaml
long_handoff:
  trend:
    - price_above_20MA
    - 20MA_above_50MA_optional
    - 5_day_MA_rising
  anchors:
    - AVWAP_from_prior_swing_low
    - AVWAP_from_newer_higher_low
  support_behavior:
    - price_touches_or_nears_old_AVWAP
    - price_recovers
    - newer_AVWAP_becomes_support
  entry:
    - break_above_lower_timeframe_micro_high
    - after_successful_AVWAP_defense
  stop:
    - below_recent_higher_low
  exit:
    - trail_under_next_relevant_higher_low
```

### Why useful

This may work very well as an MTC V2 **trend continuation filter** or **exit trailing guide**.

---

## 9. Candidate Strategy D — 5-Day MA + AVWAP Momentum Entry

```yaml
candidate_id: QL_BRIAN_SHANNON_5DMA_AVWAP_MOMENTUM_ENTRY_v0
type: signal_or_filter_module
direction: long_short
timeframes:
  signal:
    - 30m
    - 65m
  trend:
    - 1D
priority: HIGH
```

### Concept

Brian treats the 5-day moving average as a key intermediate-term trend indicator. If the 5-day MA is declining, he avoids buying. If it is rising, he avoids shorting.

### Objective v0 rules

```yaml
long_filter:
  - 5DMA_slope > 0
  - price_above_5DMA
  - price_above_relevant_AVWAP
  - higher_low_confirmed

short_filter:
  - 5DMA_slope < 0
  - price_below_5DMA
  - price_below_relevant_AVWAP
  - lower_high_confirmed
```

### MTC use

This is a strong MTC V2 filter/gate candidate. It can be combined with existing MA slope, HTF trend, and level proximity filters.

---

## 10. Candidate Strategy E — AVWAP Breakaway Gap Continuation

```yaml
candidate_id: QL_BRIAN_SHANNON_BREAKAWAY_GAP_AVWAP_CONTINUATION_v0
type: signal_producer_candidate
direction: long_primary
timeframes:
  - 1D
  - 30m
  - 65m
priority: MEDIUM_HIGH
```

### Concept

Breakaway gaps can mark a major supply/demand shift. The edge is not to chase the gap immediately, but to observe whether the AVWAP from the gap is defended and whether the shorter-term trend resumes.

### Objective v0 rules

```yaml
breakaway_gap:
  gap_percent: [5, 8, 10]
  volume_ratio: [2, 3, 5]
  close_location_value: >= 0.5
  prior_base_or_range: true

confirmation:
  - price_holds_above_gap_AVWAP
  - higher_low_after_gap
  - 5DMA_turns_up
  - short_term_higher_high

entry:
  - buy_strength_after_pullback
  - not_gap_chase

stop:
  - below_higher_low
  - below_gap_AVWAP_cluster

exit:
  - partial_at_prior_resistance
  - partial_at_measuring_gap_target_optional
  - trail_final_third
```

### Caution

Crypto does not have earnings gaps in the same way. For crypto, proxy gaps may use high-volume impulse candles or session breaks, but this must be labeled as a proxy.

---

## 11. Candidate Strategy F — Failed AVWAP / Breakdown Trap

```yaml
candidate_id: QL_BRIAN_SHANNON_FAILED_AVWAP_TRAP_v0
type: reversal_or_filter_module
direction: long_short
timeframes:
  - 15m
  - 30m
  - 65m
  - 1D
priority: MEDIUM
```

### Concept

If price breaks below a key AVWAP and then quickly reclaims it, shorts may be trapped. Conversely, if price breaks above AVWAP and fails, longs may be trapped.

### Objective v0 rules

```yaml
long_trap:
  - price_breaks_below_key_AVWAP
  - closes_back_above_AVWAP_within_N_bars
  - 5DMA_flat_or_rising
  - higher_timeframe_not_bearish
  - entry_on_reclaim_or_micro_higher_high

short_trap:
  - price_breaks_above_key_AVWAP
  - closes_back_below_AVWAP_within_N_bars
  - 5DMA_flat_or_declining
  - higher_timeframe_not_bullish
  - entry_on_rejection_or_micro_lower_low
```

### Use

This is useful as both:
- a standalone failed-breakout idea,
- and a filter to avoid shorting/longing into traps.

---

## 12. Risk Management Rules Extracted

### 12.1 Stop placement

```yaml
long_stop:
  primary:
    - below_most_recent_relevant_higher_low
  secondary:
    - below_AVWAP_cluster
    - below_morning_low
    - below_gap_day_low

short_stop:
  primary:
    - above_most_recent_relevant_lower_high
  secondary:
    - above_AVWAP_cluster
    - above_intraday_rejection_high
```

### 12.2 Trade invalidation

```yaml
long_invalid_if:
  - higher_low_breaks
  - price_loses_AVWAP_cluster
  - 5DMA_rolls_over
  - expected_strength_does_not_appear

short_invalid_if:
  - lower_high_breaks
  - price_reclaims_AVWAP_cluster
  - 5DMA_turns_up
  - expected_failure_does_not_appear
```

### 12.3 Partial exits

```yaml
partial_exit_model:
  first_third:
    - sell_into_initial_strength
    - especially_in_choppy_market
    - target_prior_resistance_or_near_R_multiple
  second_third:
    - sell_on_next_extension_or_trailing_stop
  final_third:
    - trail_under_higher_lows_for_longs
    - trail_above_lower_highs_for_shorts
```

Brian is clear that in choppy markets he takes partials quicker. In stronger stage-2 markets, he gives trades more room.

---

## 13. MTC V2 Mapping

```yaml
mtc_mapping:
  signal_producers:
    - QL_BRIAN_SHANNON_AVWAP_GAP_PULLBACK_STRENGTH_v0
    - QL_BRIAN_SHANNON_AVWAP_PINCH_BREAKOUT_v0
    - QL_BRIAN_SHANNON_BREAKAWAY_GAP_AVWAP_CONTINUATION_v0

  filters_gates:
    - 5DMA_slope_filter
    - AVWAP_above_below_filter
    - AVWAP_cluster_support_resistance_filter
    - trend_alignment_filter
    - no_chase_after_extension_filter

  signal_transform:
    - wait_for_pullback_to_AVWAP
    - wait_for_strength_after_touch
    - wait_for_higher_low_confirmation
    - wait_for_lower_high_confirmation

  exits:
    - structure_stop_under_higher_low
    - structure_stop_above_lower_high
    - partial_exit_first_third
    - AVWAP_cluster_loss_exit
    - 5DMA_slope_failure_exit

  position_management:
    - partials_in_choppy_market
    - hold_final_third_in_stage_2
    - no_entry_if_stop_distance_too_wide

  portfolio_guards:
    - reduce_size_in_choppy_market
    - avoid_heavy_short_against_rising_20_50_daily_MA
```

### Best MTC integration path

```yaml
best_integration_path:
  stage_1:
    - Python-only AVWAP research
    - no Pine
  stage_2:
    - add AVWAP as filter/gate
    - compare existing producers with and without AVWAP filter
  stage_3:
    - implement AVWAP producer only if standalone tests pass
  stage_4:
    - Pine parity implementation
```

---

## 14. Backtest Plan

### 14.1 Recommended folder

```text
06_QUANTLENS_LAB/research/brian_shannon_avwap/
```

### 14.2 Suggested files

```text
README.md
avwap_core.py
avwap_anchor_detection.py
avwap_gap_pullback_strength.py
avwap_pinch_breakout.py
avwap_handoff_trend.py
avwap_failed_trap.py
avwap_5dma_filter.py
run_avwap_research.py
QL_BRIAN_SHANNON_AVWAP_REPORT.md
QL_BRIAN_SHANNON_AVWAP_RESULTS.csv
QL_BRIAN_SHANNON_AVWAP_TRADES.csv
```

### 14.3 Asset universe

```yaml
crypto_proxy_minimum:
  - BTCUSDT
  - ETHUSDT
  - SOLUSDT
  - BNBUSDT
  - XRPUSDT
  - DOGEUSDT
  - LINKUSDT
  - AVAXUSDT

equity_native_recommended_if_data_available:
  - NVDA
  - META
  - AAPL
  - MSFT
  - TSLA
  - AMD
  - SMCI
  - COIN
  - ROKU
  - SHOP
```

### 14.4 Timeframes

```yaml
timeframes:
  daily_context:
    - 1D
  execution:
    - 65m
    - 30m
    - 15m
  crypto_proxy:
    - 4h
    - 1h
    - 15m
```

### 14.5 Required comparison baselines

```yaml
baselines:
  - simple_20_50_MA_trend_pullback
  - daily_breakout_without_AVWAP
  - gap_pullback_without_AVWAP
  - AVWAP_touch_naive_entry
  - AVWAP_strength_after_touch
  - 5DMA_filter_only
  - buy_and_hold_long_only_context
```

The most important baseline is:

```yaml
critical_test:
  compare:
    - naive_buy_AVWAP_touch
    - buy_strength_after_AVWAP_touch
  expected:
    - strength_after_touch_should_reduce_false_entries
```

---

## 15. Required Metrics

```yaml
required_metrics:
  - net_return_after_costs
  - profit_factor
  - max_drawdown
  - win_rate
  - avg_win
  - avg_loss
  - expectancy_R
  - trade_count
  - average_holding_bars
  - median_holding_bars
  - max_adverse_excursion
  - max_favorable_excursion
  - first_third_profit_effect
  - final_third_outlier_capture
  - stop_distance_distribution
  - missed_trade_due_to_no_chase_filter
  - false_breakout_rate
  - performance_by_anchor_type
  - performance_by_market_regime
  - performance_by_timeframe
  - cost_sensitivity_2x_3x
```

### Anchor-specific diagnostics

```yaml
anchor_diagnostics:
  - ytd_anchor_performance
  - major_swing_low_anchor_performance
  - major_swing_high_anchor_performance
  - gap_day_anchor_performance
  - rolling_high_low_anchor_performance
  - anchor_age_effect
  - AVWAP_slope_effect
  - distance_from_AVWAP_effect
```

---

## 16. Acceptance / Rejection Criteria

```yaml
accept_for_stage_2_if:
  - PF_after_costs >= 1.20
  - works_on_at_least_5_assets
  - trade_count_sufficient
  - strength_after_touch_beats_naive_touch
  - AVWAP_filter_improves_existing_producer
  - no_single_asset_dependency
  - drawdown_not_excessive
  - parameters_not_overfit
  - cost_stress_monotonic
  - objective_anchor_rules_are_stable

downgrade_to_filter_if:
  - standalone_AVWAP_entries_are_weak
  - but_existing_strategy_with_AVWAP_filter_improves_PF_or_DD

reject_if:
  - naive_touch_only_is_required_to_show_profit
  - edge_depends_on_manual_anchor_selection
  - crypto_proxy_results_fail_but_equity_data_unavailable
  - AVWAP_rules_underperform_basic_MA_baseline
  - fee_stress_breaks_edge
```

---

## 17. Relationship to Existing QuantLens Work

```yaml
related_reports:
  Linda_Raschke_trade_management:
    relation:
      - AVWAP_entries_pair_well_with_LBR_trade_management
      - LBR_ATR_trail_can_manage_AVWAP_breakouts
      - LBR_partial_exits_fit_Brian_choppy_market_exit_style

  Stan_Weinstein_stage_analysis:
    relation:
      - AVWAP_can_add_cost_basis_and_psychology_to_stage_2_entries
      - 20_50_200MA_context_overlaps_with_stage_analysis

  Nick_Schmidt_character_change:
    relation:
      - AVWAP_can_confirm_who_controls_after_character_change
      - failed_AVWAP_reclaim_can_be_character_change_trigger

  Crabel_range_extension:
    relation:
      - AVWAP_can_filter_chasing_after_range_extension
      - AVWAP_can_define_pullback_after_expansion

  Daily_Extension_Anti_Chase:
    relation:
      - Brian_explicitly_warns_against_chasing_extended_breakouts
      - AVWAP_pullback_strength_is_anti_chase_entry_model
```

Best combined candidate:

```yaml
combined_model:
  name: QL_STAGE_AVWAP_LBR_TRADE_MANAGEMENT_v0
  components:
    - Weinstein_stage_2_filter
    - Brian_Shannon_AVWAP_pullback_strength_entry
    - 5DMA_slope_filter
    - Linda_Raschke_ATR_or_structure_trailing_exit
    - partial_first_third_in_choppy_market
```

---

## 18. Critical Implementation Warnings

```yaml
warnings:
  - do_not_buy_AVWAP_touch_blindly
  - do_not_use_unlimited_subjective_anchors
  - do_not_assume_AVWAP_is_support_or_resistance
  - do_not_skip_lower_timeframe_confirmation
  - do_not_chase_after_large_gap_or_extension
  - do_not_promote_crypto_proxy_results_as_equity_gap_results
  - do_not_ignore_market_regime
  - do_not_short_strong_daily_uptrend_just_because_intraday_pattern_breaks
```

The main research danger is **anchor overfitting**. Codex must define deterministic anchors before testing.

---

## 19. Recommended Codex Task

```yaml
codex_action:
  immediate:
    - create_python_only_research_folder
    - implement_OHLC4_AVWAP_core
    - implement_objective_anchor_detection
    - implement_AVWAP_gap_pullback_strength
    - implement_AVWAP_pinch_breakout
    - implement_AVWAP_handoff_trend
    - implement_AVWAP_failed_trap
    - implement_5DMA_slope_filter
    - compare_naive_touch_vs_strength_after_touch
    - run_on_minimum_5_assets
    - generate_markdown_and_csv_outputs

  avoid:
    - do_not_modify_MTC_V2_pine
    - do_not_modify_production_runner
    - do_not_use_manual_anchors
    - do_not_claim_edge_without_baseline_comparison
```

---

## 20. Final Rating

```yaml
final_rating:
  research_value: 9.3/10
  signal_producer_value: 8.5/10
  filter_gate_value: 9.5/10
  trade_management_value: 8.5/10
  position_sizing_value: 7.0/10
  mtc_v2_relevance: 9.0/10
  crypto_proxy_value: 8.0/10
  equity_native_value: 9.5/10
  pine_priority_now: 5/10
  python_research_priority: 9.5/10
  live_readiness: 3/10
```

---

## 21. Final Decision

```yaml
final_decision:
  action: ACCEPT
  classification: HIGH_VALUE_AVWAP_SIGNAL_FILTER_AND_TRADE_MANAGEMENT_FRAMEWORK
  best_use:
    - AVWAP filter/gate for existing strategies
    - AVWAP pullback strength producer research
    - AVWAP pinch breakout research
    - AVWAP handoff trend continuation
    - AVWAP failed trap filter
    - anti_chase entry timing
  next_step:
    - Python-only research
    - deterministic anchor rules
    - compare against MA and non-AVWAP baselines
    - test at least 5 assets
  do_not_do:
    - do not convert directly to Pine yet
    - do not rely on visual/manual anchors
    - do not treat AVWAP touch as entry
```

Final conclusion:

> This is one of the strongest QuantLens inputs so far for a **systematic filter/producer research module**. The most promising path is not “AVWAP touch trading,” but **AVWAP + 5DMA trend alignment + pullback + renewed strength + structure-based stop**. It should be researched Python-first and only later considered for MTC V2 Pine parity.
