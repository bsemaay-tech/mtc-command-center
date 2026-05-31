# QUANTLENS TRANSCRIPT INTAKE REPORT — Linda Bradford Raschke / 5 Essential Sell Rules & Trade Management

**Generated:** 2026-05-03  
**Source URL:** https://youtu.be/kTqKRi-j9kM?si=99GgO3p0M-b25wBA  
**Normalized URL:** https://www.youtube.com/watch?v=kTqKRi-j9kM  
**Video ID:** `kTqKRi-j9kM`  
**Uploaded Transcript File:** `The 5 Essential Sell Rules from a Market Wizard - Linda Bradford Raschke.md`  
**Transcript Status:** Provided by user  
**Primary Speaker:** Linda Bradford Raschke  
**Host / Context:** TraderLion Conference interview  
**Core Topic:** Trade management, sell rules, position sizing, ATR-based risk, coils, range expansion, previous-day high/low structure, model discipline, daily homework, holding-time tradeoffs  
**Transcript SHA256:** `752160e7905999d4ceaf11291620312851e413e8cfd7108cb412f08b0aab4cd1`  

---

## 1. Executive Verdict

```yaml
verdict: ACCEPT_AS_HIGH_VALUE_TRADE_MANAGEMENT_AND_EXIT_FRAMEWORK
production_ready: false
backtest_ready: yes_python_first
pine_ready: no_not_initially
strategy_family:
  - linda_raschke_trade_management
  - atr_trailing_stop
  - coil_breakout_range_expansion
  - previous_day_high_low_reversal
  - taylor_buy_sell_short_day
  - box_range_and_point_of_control
  - two_period_rate_of_change
  - trade_sheets_and_process_discipline
priority: HIGH
recommended_stage: python_research_exit_modules_and_management_overlay
```

This transcript is not a single clean “buy here, sell here” strategy. Its strongest value is **trade management**:

- how to size,
- how to exit,
- how to trail winners,
- when to flatten mistakes,
- when not to force trades,
- and how to map holding time to win rate and frequency.

For QuantLens, this should primarily become an **exit-management / position-management research package**, not a direct Pine producer.

---

## 2. Quality & Relevance Score

```yaml
source_quality_score: 9.5/10
strategy_idea_score: 8/10
trade_management_score: 10/10
risk_management_score: 9.5/10
implementation_clarity_score: 8/10
mtc_relevance_score: 9/10
crypto_transferability_score: 7/10
equity_transferability_score: 8/10
futures_transferability_score: 9/10
position_trading_value: 7/10
short_term_trading_value: 9/10
```

### Strong points

- Speaker is Linda Bradford Raschke, a high-quality Market Wizard source.
- Strong emphasis on trade management rather than “magic setups.”
- Clear links to ATR stops, parabolic stops, volatility stops, previous-day levels, boxes, coils, range expansion, and holding-time statistics.
- Very useful for improving MTC V2 exit, sizing, and trade-management modules.
- Concepts are general enough to test on crypto, futures, equities, and indices.
- Good warning against overfitting and small sample extrapolation.

### Weak points / caution

- Some concepts are discretionary and pattern-recognition based.
- She uses context heavily; simple mechanical translation may lose edge.
- Several examples are futures/intraday-oriented, not directly compatible with daily position trading.
- “5 Essential Sell Rules” is more a framework than a numbered mechanical rule set.
- Requires careful implementation discipline to avoid subjective chart-reading.

---

## 3. Core Thesis

```yaml
core_thesis:
  - trade_management_makes_or_breaks_bottom_line
  - consistency_makes_strategy_scalable
  - shorter_holding_time_higher_frequency_higher_win_rate
  - longer_holding_time_lower_win_rate_bigger_outliers
  - do_not_sell_best_position_to_fund_losers
  - cut_crappy_positions_and_keep_outliers
  - use_models_not_intuition
  - homework_and_trade_sheets_reduce_cognitive_bias
  - use_horizontal_levels_not_complex_indicators
  - boxes_and_coils_show_balance_before_expansion
  - each_market_move_is_unique_context_matters
```

Linda’s key implementation message:

> Setup is not enough. The scalable edge comes from consistent trade management.

---

## 4. Extracted “5 Sell Rules” for QuantLens

The video title frames the topic as sell rules. The transcript does not present a simple numbered checklist, but the practical sell rules can be extracted as follows.

### Sell Rule 1 — Fix execution mistakes immediately

```yaml
rule_id: LBR_SELL_RULE_01_FLATTEN_MISTAKES
type: execution_risk_rule
trigger:
  - unintended_position
  - wrong_symbol
  - wrong_side
  - wrong_size
  - trade_not_matching_plan
action:
  - flatten_immediately
  - do_not_check_profit_or_loss_first
```

Interpretation:

If the position is not the intended trade, exit immediately. Do not rationalize. Do not convert an execution error into a discretionary gamble.

### Sell Rule 2 — Dump what is not working

```yaml
rule_id: LBR_SELL_RULE_02_DUMP_NOT_WORKING
type: position_management_rule
trigger:
  - position_not_following_expected_path
  - equity_curve_drawdown_or_trade_level_underperformance
  - better_positions_available
action:
  - reduce_or_flatten
  - keep_capital_for_positions_that_work
```

This aligns directly with her statement that with multiple positions, something is usually working somewhere, making it easier to “dump the crap that wasn’t working.”

### Sell Rule 3 — Do not sell your best outlier too early

```yaml
rule_id: LBR_SELL_RULE_03_KEEP_OUTLIERS
type: winner_management_rule
trigger:
  - strong_trend_day
  - range_expansion_from_coil
  - trailing_stop_not_hit
  - position_is_best_performer
action:
  - avoid_cutting_best_position_to_cover_losers
  - trail_with_ATR_or_volatility_stop
  - allow_outlier_to_develop
```

This is a major QuantLens lesson. Many traders create unforced errors by selling the best winner because it is green, while keeping weak losers.

### Sell Rule 4 — Use a defined trailing mechanism when the setup can produce an outlier

```yaml
rule_id: LBR_SELL_RULE_04_TRAIL_OUTLIER_SETUPS
type: exit_algorithm_rule
eligible_setups:
  - coil_breakout
  - range_expansion
  - trend_day
  - bear_trap_or_bull_trap_reversal
  - daily_weekly_alignment
tools:
  - ATR_trailing_stop
  - parabolic_stop
  - volatility_stop
  - moving_average_stop
action:
  - trail_until_stop_hit
  - do_not_cap_upside_with_premature_fixed_target
```

She specifically likes ATR functions and says one must “have something” for trade management.

### Sell Rule 5 — Match exit style to holding-time model

```yaml
rule_id: LBR_SELL_RULE_05_EXIT_STYLE_MATCHES_HOLDING_TIME
type: strategy_design_rule
principle:
  - shorter_holding_time_higher_win_rate
  - longer_holding_time_lower_win_rate_higher_outlier_dependency
required_validation:
  - frequency_of_occurrence
  - average_holding_time
  - win_rate
  - avg_win_loss
  - market_regime_performance
action:
  - do_not_mix_scalp_exit_with_trend_following_expectancy
  - do_not_expect_high_win_rate_from_long_holding_period
```

This is important for MTC V2. A strategy cannot mix a trend-following entry with a scalper’s profit-taking logic unless tested.

---

## 5. Candidate Strategy A — Coil Breakout / Range Expansion

```yaml
candidate_id: QL_LBR_COIL_BREAKOUT_RANGE_EXPANSION_v0
type: signal_producer_candidate
direction: long_short
timeframes:
  preferred:
    - 120m
    - 240m
    - 1D
asset_classes:
  - futures
  - crypto
  - indices
  - liquid_equities
priority: HIGH
```

### Concept

Linda likes “coils”: overlapping price action / balance areas that can lead to range expansion. She uses line charts to reduce noise and often combines the setup with ATR/volatility trailing stops.

### Objective v0 definition

```yaml
coil_definition:
  bars_overlap_min: [5, 6, 7, 8]
  compression:
    atr_percentile_below: [30, 40, 50]
    range_contracting: true
  structure:
    recent_highs_lower_or_equal: optional
    recent_lows_higher_or_equal: optional
    price_inside_box: true
trigger:
  long:
    - close_above_coil_high
    - or_stop_entry_above_coil_high
  short:
    - close_below_coil_low
    - or_stop_entry_below_coil_low
exit:
  primary:
    - ATR_trailing_stop
    - volatility_stop
  fail_fast:
    - close_back_inside_coil
    - stop_hit
```

### Research notes

- Test as symmetric long/short.
- Must include false breakout diagnostics.
- Compare fixed target vs ATR trail vs parabolic trail.
- Do not over-optimize coil length.

---

## 6. Candidate Strategy B — Three-Bar / Inside-Two-Day Breakout

```yaml
candidate_id: QL_LBR_THREE_BAR_BREAKOUT_v0
type: signal_producer_candidate
direction: long_short
timeframes:
  - 1D
  - 240m
priority: MEDIUM_HIGH
```

### Concept

Linda describes a “three bar” pattern: a bar whose range is inside the prior two-day high/low range, then a breakout from that compression.

### Objective v0 definition

```yaml
three_bar_condition:
  bar_0_high < max(high_1, high_2)
  bar_0_low > min(low_1, low_2)
trigger:
  long:
    - break_above_three_bar_high
  short:
    - break_below_three_bar_low
filters:
  - ATR_compression_optional
  - market_regime_optional
  - avoid_major_news_optional
exit_variants:
  - next_day_exit
  - ATR_trail
  - close_back_inside_range
  - fixed_R_target
```

### Relevance

This is easy to code, test, and compare to simple inside-bar baselines. It can become a low-complexity QuantLens research candidate.

---

## 7. Candidate Strategy C — Previous-Day High/Low / Taylor Rhythm

```yaml
candidate_id: QL_LBR_PREV_DAY_HIGH_LOW_TAYLOR_RHYTHM_v0
type: intraday_trade_management_or_signal_module
direction: long_short
timeframes:
  - 5m
  - 15m
  - 30m
asset_classes:
  - index_futures
  - liquid_crypto
  - metals
priority: MEDIUM
```

### Concept

Linda uses previous day high/low and opening gaps heavily. A market may move away from the gap or toward the gap. After multi-day movement, she may define a “Z-day” with two-way trading, where one can buy dips or short rallies.

### Objective v0 components

```yaml
inputs:
  - previous_day_high
  - previous_day_low
  - current_open
  - gap_direction
  - daily_roc_2
  - prior_day_count_up_down
  - session_phase
patterns:
  gap_hold:
    - gap_up_holds_above_prev_high_or_open
    - gap_down_holds_below_prev_low_or_open
  gap_fade:
    - gap_fails_and_reenters_prior_day_range
  taylor_z_day:
    - after_large_trend_day
    - expect_two_way_trade
    - fade_first_morning_extension
entry:
  long:
    - reclaim_prev_day_low_after_flush
    - higher_low_after_gap_up
  short:
    - reject_prev_day_high_after_pop
    - lower_high_after_gap_down
exit:
  - prior_day_level_retest
  - intraday_swing_high_low
  - time_exit
  - ATR_stop
```

### Caution

This module is more discretionary. It should be tested as a level-based intraday framework, not blindly promoted to producer.

---

## 8. Candidate Strategy D — Box Range / Midpoint / Point of Control Proxy

```yaml
candidate_id: QL_LBR_BOX_MIDPOINT_RECLAIM_v0
type: signal_or_filter_module
direction: long_short
timeframes:
  - 15m
  - 30m
  - 120m
  - 240m
priority: MEDIUM_HIGH
```

### Concept

Linda likes boxes with two support data points and two resistance data points. The midpoint of the box behaves like a simplified point-of-control / value area.

### Objective v0 definition

```yaml
box_detection:
  support_touches_min: 2
  resistance_touches_min: 2
  max_box_height_atr: [1.0, 1.5, 2.0]
  min_box_duration_bars: [8, 12, 20]
signals:
  constructive_reclaim:
    - price_breaks_below_box
    - reclaims_box_midpoint_or_box_low
    - closes_back_inside_or_above_box
  breakout:
    - close_above_box_high
    - close_below_box_low
  failed_breakout:
    - break_outside_box
    - close_back_inside_box
exit:
  - opposite_box_boundary
  - midpoint_failure
  - ATR_stop
```

### Use

Can be tested as:
- standalone producer,
- filter for coil breakouts,
- failed-breakout reversal system.

---

## 9. Candidate Strategy E — Two-Period Rate of Change Reversal

```yaml
candidate_id: QL_LBR_ROC2_REVERSAL_v0
type: signal_or_timing_module
direction: long_short
timeframes:
  - 1D
  - 240m
priority: MEDIUM
```

### Concept

Linda says 2-period ROC has better signal-to-noise than 1-period and 3-period ROC. She uses it as part of a daily worksheet and often combines it with filters.

### Objective v0 definition

```yaml
roc2_reversal:
  long_setup:
    - roc2_negative
    - roc2_slope_turning_up
    - price_down_2_or_3_days
    - support_or_prior_low_nearby
  short_setup:
    - roc2_positive
    - roc2_slope_turning_down
    - price_up_2_or_3_days
    - resistance_or_prior_high_nearby
filters:
  - avoid_narrow_inside_bar_continuation
  - require_level_context
  - require_ATR_not_extreme
exit:
  - next_bar_or_next_day
  - previous_day_high_low_target
  - ATR_stop
```

### Caution

Do not test this alone as a magic oscillator. It is a **timing filter**, not a complete strategy.

---

## 10. Candidate Module F — ATR / Volatility Exit Overlay

```yaml
candidate_id: QL_LBR_ATR_VOLATILITY_EXIT_OVERLAY_v0
type: exit_module
priority: VERY_HIGH
mtc_relevance: VERY_HIGH
```

### Concept

Linda repeatedly emphasizes ATR functions, volatility stops, parabolic stops, and trailing only when the initial condition can lead to a larger move.

### Exit variants to test

```yaml
exit_variants:
  fixed_exit:
    - exit_after_N_bars
    - exit_next_day_open_or_close
  atr_trail:
    atr_len: [10, 14, 20]
    atr_mult: [1.5, 2.0, 2.5, 3.0]
  chandelier:
    lookback: [10, 20, 30]
    atr_mult: [2.0, 3.0, 4.0]
  parabolic:
    step: [0.01, 0.02]
    max_step: [0.1, 0.2]
  ma_exit:
    ma_len: [5, 10, 20]
```

### Key diagnostic

```yaml
diagnostics:
  - which_setups_should_trail
  - which_setups_should_time_exit
  - outlier_capture_ratio
  - premature_exit_cost
  - giveback_ratio
```

This may be one of the highest-value MTC V2 improvements from the transcript.

---

## 11. Candidate Module G — ADTR / Volatility-Normalized Position Sizing

```yaml
candidate_id: QL_LBR_ADTR_POSITION_SIZING_v0
type: position_sizing_module
priority: VERY_HIGH
```

### Concept

Linda calculates average daily range multiplied by point value to normalize unit size across futures. Equivalent concept for crypto/equities:

```yaml
sizing_basis:
  - average_daily_true_range_dollar
  - ATR_percent
  - volatility_dollar_risk
  - account_equity
  - max_risk_per_trade
```

### Objective v0 formula

```yaml
position_size:
  risk_budget = account_equity * risk_pct
  stop_distance = ATR * atr_mult
  qty = risk_budget / stop_distance
caps:
  - max_notional_pct
  - max_leverage
  - max_correlated_exposure
  - max_symbol_exposure
```

### Correlation adjustment

Linda mentions that correlated markets should be treated as partial units.

```yaml
correlation_rule:
  if_correlation_high:
    trade_half_unit_each
  examples:
    - SP500_and_NASDAQ
    - gold_and_silver
    - BTC_and_ETH
```

This maps very well to MTC V2 position sizing and portfolio-level exposure control.

---

## 12. Candidate Module H — Equity Curve Risk Throttle

```yaml
candidate_id: QL_LBR_EQUITY_CURVE_RISK_THROTTLE_v0
type: portfolio_risk_module
priority: HIGH
```

### Concept

Linda manages risk partly by the equity curve: if drawdown or “funky” behavior appears, she gets smaller.

```yaml
risk_throttle:
  trigger:
    - equity_curve_below_sma
    - drawdown_exceeds_threshold
    - consecutive_losses
    - expectancy_degradation
  action:
    - reduce_risk_pct
    - reduce_max_positions
    - block_new_trades_temporarily
    - allow_only_A_plus_setups
```

### Suggested parameters

```yaml
parameters:
  equity_sma_len_trades: [20, 30, 50]
  drawdown_thresholds: [5, 10, 15]
  risk_multiplier_when_bad: [0.25, 0.5, 0.75]
```

High MTC relevance: this belongs in PortfolioState / Guard layer, not signal producer.

---

## 13. MTC V2 Mapping

```yaml
mtc_mapping:
  signal_producer_candidates:
    - QL_LBR_COIL_BREAKOUT_RANGE_EXPANSION_v0
    - QL_LBR_THREE_BAR_BREAKOUT_v0
    - QL_LBR_BOX_MIDPOINT_RECLAIM_v0
  timing_filters:
    - QL_LBR_ROC2_REVERSAL_v0
    - QL_LBR_PREV_DAY_HIGH_LOW_TAYLOR_RHYTHM_v0
  exit_modules:
    - QL_LBR_ATR_VOLATILITY_EXIT_OVERLAY_v0
    - fixed_time_exit_by_holding_model
    - close_back_inside_box_exit
    - failed_breakout_exit
  position_sizing:
    - QL_LBR_ADTR_POSITION_SIZING_v0
  portfolio_guards:
    - QL_LBR_EQUITY_CURVE_RISK_THROTTLE_v0
    - correlation_adjusted_position_units
  process_layer:
    - trade_plan_required
    - unintended_position_flatten_rule
    - no_trade_if_mental_state_bad
```

### Where it should not go yet

```yaml
avoid_initially:
  - do_not_directly_convert_to_pine
  - do_not_merge_into_live_MTC
  - do_not_create_alerts
  - do_not_use_as_discretionary_chart_pattern_without_tests
```

---

## 14. Backtest Plan

### 14.1 First research folder

```text
06_QUANTLENS_LAB/research/linda_raschke_trade_management/
```

### 14.2 Suggested files

```text
README.md
lbr_coil_breakout.py
lbr_three_bar_breakout.py
lbr_box_midpoint.py
lbr_roc2_reversal.py
lbr_exit_overlays.py
lbr_position_sizing.py
run_lbr_backtests.py
LBR_TRADE_MANAGEMENT_REPORT.md
LBR_RESULTS.csv
LBR_TRADES.csv
```

### 14.3 Minimum asset set

```yaml
crypto_proxy:
  - BTCUSDT
  - ETHUSDT
  - SOLUSDT
  - BNBUSDT
  - XRPUSDT
  - DOGEUSDT
  - LINKUSDT
  - AVAXUSDT

futures_native_if_data_available:
  - ES
  - NQ
  - CL
  - GC
  - SI
  - ZB
  - ZN
  - ZS
  - ZC
```

### 14.4 Timeframes

```yaml
timeframes:
  primary:
    - 240m
    - 1D
  secondary:
    - 120m
    - 15m
    - 5m
```

### 14.5 Required comparisons

```yaml
compare_against:
  - simple_breakout_baseline
  - inside_bar_breakout_baseline
  - fixed_N_bar_exit
  - ATR_trailing_exit
  - parabolic_exit
  - moving_average_exit
  - buy_and_hold_for_long_only_context
```

---

## 15. Metrics

```yaml
required_metrics:
  - net_return_after_costs
  - profit_factor
  - max_drawdown
  - win_rate
  - avg_win
  - avg_loss
  - avg_win_to_avg_loss
  - expectancy_R
  - trade_count
  - average_holding_bars
  - median_holding_bars
  - outlier_capture_ratio
  - top_5_trade_dependency
  - false_breakout_loss
  - giveback_ratio
  - cost_sensitivity_2x_3x
  - performance_by_market_regime
  - performance_by_timeframe
```

### Trade-management diagnostics

```yaml
trade_management_diagnostics:
  - fixed_exit_vs_trailing_exit
  - best_exit_by_setup_type
  - what_percent_of_setups_should_trail
  - premature_exit_penalty
  - max_favorable_excursion_capture
  - max_adverse_excursion
```

---

## 16. Acceptance / Rejection Criteria

```yaml
accept_for_stage_2_if:
  - PF_after_costs >= 1.20
  - trade_count_sufficient_by_timeframe
  - fee_stress_monotonic_and_still_positive_or_acceptable
  - exit_overlay_improves_baseline_expectancy
  - works_on_at_least_5_assets
  - not_dependent_on_one_outlier_asset
  - drawdown_reduction_vs_baseline
  - outlier_capture_ratio_improves

reject_or_downgrade_if:
  - edge_only_from_one_or_two_outlier_trades
  - no_improvement_over_simple_breakout
  - trail_exit_gives_back_too_much
  - fixed_exit_beats_all_trails_consistently
  - sample_size_too_low
  - strategy_breaks_under_2x_or_3x_costs
  - parameters_too_sensitive
```

---

## 17. Relationship to Prior QuantLens Reports

```yaml
related_reports:
  stan_weinstein_stage_analysis:
    relation:
      - both_emphasize_discipline
      - both_use_chart_structure
      - Weinstein_better_for_stage_and_stock_selection
      - Raschke_better_for_trade_management_and_exits
  nick_schmidt_character_change:
    relation:
      - Nick_better_for_weekly_position_selection
      - Raschke_better_for_holding_time_and_exit_logic
  crabel_range_expansion:
    relation:
      - strong_overlap_with_range_expansion
      - Raschke_coil_model_can_be_tested_against_Crabel
  MTC_V2:
    relation:
      - ATR_trailing_stop_and_position_sizing_directly_relevant
      - equity_curve_throttle_can_be_portfolio_guard
```

Best combined route:

```yaml
combined_model:
  name: QL_STAGE_COIL_TRADE_MANAGEMENT_SUITE
  components:
    - Weinstein market_stage_filter
    - Nick weekly_character_change_filter
    - Raschke coil_or_three_bar_entry
    - Raschke ATR_exit_overlay
    - Raschke ADTR_position_sizing
    - Raschke equity_curve_throttle
```

---

## 18. Critical Implementation Warnings

```yaml
warnings:
  - do_not_turn_every_visual_pattern_into_overfit_parameters
  - do_not_assume_coil_breakouts_always_trend
  - do_not_ignore_false_breakouts
  - do_not_mix_scalp_win_rate_expectations_with_position_trading
  - do_not_use_small_sample_seasonality_claims
  - do_not_sell_winners_to_keep_losers
  - do_not_promote_to_pine_before_exit_overlay_tests
```

The most important warning:

> Trade management must be tested per setup type. Some setups should be trailed; others should be exited quickly. One universal exit may degrade performance.

---

## 19. Recommended Codex Task

```yaml
codex_action:
  immediate:
    - create_python_only_research_folder
    - implement_coil_breakout_v0
    - implement_three_bar_breakout_v0
    - implement_box_midpoint_reclaim_v0
    - implement_roc2_timing_filter_v0
    - implement_ATR_parabolic_MA_exit_overlay_comparison
    - implement_ADTR_position_sizing_module
    - run_on_minimum_5_assets
    - compare_exit_management_variants
    - generate_csv_and_markdown_reports
  avoid:
    - do_not_modify_MTC_V2_pine
    - do_not_touch_live_alerts
    - do_not_claim_strategy_ready_from_single_timeframe
    - do_not_ignore_cost_sensitivity
```

---

## 20. Final Rating

```yaml
final_rating:
  research_value: 9/10
  trade_management_value: 10/10
  signal_producer_value: 7.5/10
  exit_module_value: 10/10
  position_sizing_value: 9.5/10
  portfolio_guard_value: 8.5/10
  crypto_proxy_value: 7/10
  futures_native_value: 9/10
  equity_native_value: 8/10
  pine_priority_now: 4/10
  python_research_priority: 9/10
  live_readiness: 3/10
```

---

## 21. Final Decision

```yaml
final_decision:
  action: ACCEPT
  classification: HIGH_VALUE_TRADE_MANAGEMENT_EXIT_AND_RISK_FRAMEWORK
  best_use:
    - MTC_V2_exit_overlay_research
    - ATR_volatility_trailing_stop_comparison
    - coil_breakout_research
    - three_bar_breakout_research
    - ADTR_volatility_normalized_sizing
    - equity_curve_risk_throttle
  next_step:
    - Python-only research
    - compare exit variants against existing MTC exits
    - test at least 5 assets and multiple timeframes
  do_not_do:
    - do not convert directly to Pine yet
    - do not treat as a single fixed setup
    - do not skip trade-management diagnostics
```

Final conclusion:

> This transcript is one of the best QuantLens inputs so far for **exit logic, trade management, volatility sizing, and range-expansion research**. The strongest immediate value is not a new entry signal; it is improving how existing and future strategy candidates manage winners, losers, mistakes, volatility, and position sizing.
