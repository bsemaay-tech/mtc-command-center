# QUANTLENS TRANSCRIPT INTAKE REPORT — Nick Schmidt Weekly Character Change / Trade Less Model

**Generated:** 2026-05-03  
**Source URL:** https://youtu.be/-JyH5PAJ4-Y?si=BqaSaOarsfJIutKk  
**Normalized URL:** https://www.youtube.com/watch?v=-JyH5PAJ4-Y  
**Video ID:** `-JyH5PAJ4-Y`  
**Uploaded Transcript File:** `I Stopped Trading So Much and My Profits Skyrocketed.md`  
**Transcript Status:** Provided by user  
**Primary Speaker:** Nick Schmidt  
**Topic:** Weekly charts, trading less, character change, controlled weakness, risk/reward, sell-decision framework  
**Transcript SHA256:** `d0a80743f3d5a33ef4de18850b32addc15c9b00f171ed21bfc02ef7844743428`  

---

## 1. Executive Verdict

```yaml
verdict: ACCEPT_AS_HIGH_VALUE_POSITION_TRADING_RESEARCH_CANDIDATE
production_ready: false
backtest_ready: yes_python_first
pine_ready: no_not_initially
strategy_family:
  - weekly_position_trading
  - character_change
  - controlled_weakness
  - base_breakout_retest
  - low_frequency_high_R_trend_following
  - risk_reward_asymmetric_model
priority: HIGH
recommended_stage: python_only_research
```

Bu video QuantLens açısından değerli. Ana fikir:

> Çok işlem yapmak yerine, haftalık grafikte büyük karakter değişimi gösteren hisseleri bul; düşük frekanslı ama büyük R potansiyeli olan pozisyonlara gir; risk yönetilebilir değilse trade alma; iyi giriş yaptıysan otur ve trendin çalışmasına izin ver.

Bu video özellikle portföyün **position trading / longer-term trend bucket** tarafı için önemlidir. MTC V2’nin intraday producer tarafına direkt taşınmamalı; önce ayrı Python research prototipi olarak test edilmelidir.

---

## 2. Quality & Relevance Score

```yaml
source_quality_score: 8.5/10
strategy_idea_score: 8.5/10
process_value_score: 9.5/10
implementation_clarity_score: 7.5/10
risk_management_score: 8.5/10
mtc_relevance_score: 7.5/10
crypto_transferability_score: 5/10
equity_position_trading_relevance_score: 9.5/10
```

### Strong points

- Net problem tanımı var: overtrading, kısa zaman dilimi stresi, düşük average gain / average loss farkı.
- Speaker kendi performans evrimini ölçüyor:
  - 2014: ~600+ trade, ortalama gain 9%, ortalama loss 6%, ortalama hold 2 gün, sonuç kötü.
  - 2024: ~35 trade, ortalama hold 43 gün, ortalama loss 9%, ortalama gain 131%.
- Ana edge “haftalık grafik + karakter değişimi + risk yönetilebilir entry” üçlüsüyle tanımlanıyor.
- “Risk yönetemiyorsan trade alma” kuralı çok güçlü.
- Controlled weakness ve base retest mantığı Charles Harris pullback modeliyle uyumlu.
- Portfolio performance cushion ve base stage ile sell decision mantığı değerli.

### Weak points / caution

- Sistem tam mekanik değil; “art vs science” yaklaşımı nedeniyle bazı kararlar discretionary.
- Fundamentals neredeyse dışarıda bırakılıyor; bu, CANSLIM/quality filtreleriyle desteklenmezse zayıf hisselerde yanlış sinyal üretebilir.
- Weekly sistemde trade count düşük olabilir; backtestte sample size problemi çıkabilir.
- Crypto proxy zayıf olabilir; model esasen US equities/growth stocks için daha uygun.
- Girişler haftalık olduğu için gecikmeli olabilir; stop mesafesi %8–10 gibi geniştir.
- TradingView/Pine producer’a direkt taşınırsa fazla yavaş kalabilir; önce portfolio bucket olarak düşünülmeli.

---

## 3. Core Thesis

```yaml
core_thesis:
  - overtrading_reduces_edge
  - higher_timeframes_increase_average_win_potential
  - weekly_charts_reduce_impulsive_decisions
  - big_winners_require_time
  - average_win_minus_average_loss_is_key
  - first_principles_matter_more_than_indicator_settings
  - controlled_weakness_after_character_change_is_entry_zone
  - manage_risk_first_then_think_about_upside
```

Nick’in ana çıkarımı:

```text
Daha az trade + daha uzun tutma + daha iyi risk/reward = daha az stres ve daha yüksek expectancy.
```

Bu, QuantLens için özellikle **position-trading allocation** fikrini güçlendiriyor.

---

## 4. Strategy Classification

```yaml
classification:
  primary: WEEKLY_CHARACTER_CHANGE_POSITION_TRADING
  secondary:
    - WEEKLY_BASE_BREAKOUT_RETEST
    - CONTROLLED_WEAKNESS_PULLBACK
    - 10_WEEK_30_WEEK_RESPECT_MODEL
    - LOW_FREQUENCY_HIGH_R_TREND_FOLLOWING
    - STAGE_1_BASE_BREAKOUT_MODEL
    - RISK_REWARD_FIRST_ENTRY_SELECTION
  not_recommended_as:
    - intraday_scalping_strategy
    - 5m_futures_strategy
    - pure_indicator_crossover
    - standalone_crypto_leverage_system
```

---

## 5. Candidate Strategy A — Weekly Character Change

### 5.1 Concept

Bir hisse uzun süre zayıf/dağınık davranış gösterdikten sonra haftalık grafikte karakter değiştirir. Nick’in temel üçlüsü:

1. Büyük volume + güçlü price action.
2. İlk higher low.
3. 10-week veya 30-week moving average’e yeni saygı / destek.

```yaml
candidate_id: QL_NICK_WEEKLY_CHARACTER_CHANGE_001
type: signal_producer_candidate
direction: long
timeframe:
  primary: 1W
  optional_context: 1M
priority: HIGH
```

### 5.2 Objective v0 Rules

```yaml
weekly_character_change:
  required:
    - weekly_volume_spike
    - strong_weekly_candle
    - first_higher_low_after_downtrend_or_base
    - risk_manageable_entry_zone
  volume_spike:
    options:
      - volume > sma(volume, 10) * 1.5
      - volume > sma(volume, 20) * 1.5
      - volume_rank_1y >= 80_percentile
  strong_price_action:
    options:
      - weekly_close_in_upper_50_percent_of_range
      - weekly_close_in_upper_60_percent_of_range
      - weekly_return_positive
      - close_above_prior_week_high
  higher_low:
    definitions:
      - swing_low_higher_than_previous_swing_low
      - pivot_low_confirmed_by_N_weeks
  ma_respect:
    options:
      - pullback_to_10w_sma_and_close_above
      - pullback_to_30w_sma_and_close_above
      - price_reclaims_10w_after_base
      - price_reclaims_30w_after_base
```

### 5.3 Entry variants

```yaml
entry_variants:
  A_character_change_close:
    description: "Enter on weekly close confirming volume + strong candle + higher low."
  B_controlled_weakness_after_character_change:
    description: "Wait for pullback/retest where risk can be defined."
  C_10w_or_30w_respect:
    description: "Enter when price pulls back to 10w/30w and holds."
  D_base_breakout_retest:
    description: "Enter on retest of prior multi-year resistance after breakout."
```

### 5.4 Stop variants

```yaml
stop_variants:
  - below_weekly_higher_low
  - below_breakout_retest_support
  - below_10w_or_30w_support_zone
  - fixed_max_loss_8_to_10_percent
  - weekly_close_below_support
```

---

## 6. Candidate Strategy B — Controlled Weakness Base Retest

### 6.1 Concept

Hisse uzun/multi-year base’den çıkar, eski direnç bölgesini kırar, sonra kontrollü şekilde eski direnç/yeni destek bölgesine geri çekilir. Bu retest, küçük riskle büyük potansiyel verir.

```yaml
candidate_id: QL_NICK_CONTROLLED_WEAKNESS_BASE_RETEST_001
type: signal_producer_candidate
direction: long
timeframe: 1W
priority: HIGH
```

### 6.2 Objective v0 Rules

```yaml
base_retest:
  base:
    min_length_weeks: [12, 26, 52, 104]
    max_depth_pct: [30, 50, 70]
    preferred:
      - long_base
      - clear_horizontal_resistance
      - tightening_near_right_side
      - higher_lows_inside_base
  breakout:
    weekly_close_above_resistance: true
    volume_confirmation: preferred
  retest:
    price_returns_to_resistance_zone:
      tolerance_pct: [2, 3, 5]
    weakness_quality:
      - controlled_pullback
      - not_wide_and_loose
      - closes_not_near_lows_repeatedly
  entry:
    - at_retest_support
    - weekly_close_reclaiming_support
    - next_week_followthrough
  stop:
    - below_retest_low
    - below_former_resistance_zone
    - fixed_risk_cap_4_to_8_percent_if_available
```

### 6.3 Notes from examples

The video gives SQ and Roblox-style examples:

```yaml
example_pattern:
  - multi_year_resistance
  - breakout_above_resistance
  - pullback_to_former_resistance
  - former_resistance_acts_as_support
  - entry_risk_around_3_to_5_percent
  - upside_potential_large_if_new_stage_1_uptrend_starts
```

This is one of the most actionable strategy candidates in the video.

---

## 7. Candidate Strategy C — 10W / 30W Respect After Character Change

### 7.1 Concept

Karakter değişimi görüldükten sonra hemen almak şart değil. Nick’in ONON örneğinde olduğu gibi risk yönetilebilir hale gelene kadar aylarca beklenebilir. Risk yönetilebilirlik genellikle 10-week veya 30-week moving average desteğiyle gelir.

```yaml
candidate_id: QL_NICK_10W_30W_RESPECT_ENTRY_001
type: signal_producer_candidate
direction: long
timeframe: 1W
priority: MEDIUM_HIGH
```

### 7.2 Objective v0 Rules

```yaml
setup:
  character_change_detected: true
  no_entry_until_risk_defined: true
entry_conditions:
  any:
    - first_clean_pullback_to_10w_after_character_change
    - first_clean_pullback_to_30w_after_character_change
    - trendline_or_horizontal_support_retest_after_character_change
risk:
  stop:
    - below_support_low
    - below_30w_for_slower_setup
    - below_weekly_swing_low
```

### 7.3 Why useful

Bu model acele etmeyi engeller. MTC/QuantLens içinde **Watchlist → Setup Matured → Entry Ready** pipeline’ı olarak uygulanabilir.

---

## 8. Candidate Strategy D — Up-on-Volume Watchlist / Radar

### 8.1 Concept

Nick günlük rutininde “up on volume” taraması yaptığını söylüyor. Bu doğrudan giriş değil; radar/aday havuzu üretir.

```yaml
candidate_id: QL_NICK_UP_ON_VOLUME_RADAR_001
type: watchlist_generator
direction: long
timeframe: 1W
priority: HIGH
```

### 8.2 Objective v0 Rules

```yaml
up_on_volume_radar:
  scan_frequency: weekly_or_daily_but_decision_weekly
  filters:
    - weekly_volume_above_average
    - weekly_close_positive
    - weekly_close_in_upper_half
    - price_above_key_base_level_or_forming_right_side
  output_buckets:
    - character_change_candidate
    - basing_no_action_yet
    - volume_trend_starter_watchlist
```

Bu, signal producer’dan önce gelen **research universe builder** modülüdür.

---

## 9. Candidate Module E — Sell Decision Framework

Nick’in sell decision yaklaşımı dört parçalı:

```yaml
sell_decision_inputs:
  - personal_portfolio_performance
  - general_market_condition
  - position_base_stage
  - position_performance
```

```yaml
candidate_id: QL_NICK_WEEKLY_SELL_DECISION_FRAMEWORK_001
type: exit_management_module
priority: HIGH
```

### 9.1 Personal portfolio performance

```yaml
portfolio_cushion_rule:
  idea:
    - early_year_large_gain_can_be_locked_to_create_psychological_and_performance_cushion
  example:
    - SMCI_trade_created_large_January_cushion
  implementation:
    if portfolio_ytd_gain_high_and_position_gain_large:
      allow_profit_booking_even_without_classic_sell_signal
```

### 9.2 General market condition

Nick’in basit piyasa değerlendirmesi çok değerli:

```yaml
market_condition_heuristic:
  healthy_market:
    - more_good_setups_than_cash_available
    - many_quality_breakouts_or_controlled_retests
  weak_market:
    - few_quality_setups
    - trader_forces_subpar_entries
    - everyone_talks_about_same_one_or_two_stocks
```

Bu, QuantLens için geniş breadth/participation filter’a çevrilebilir.

### 9.3 Position base stage

```yaml
base_stage_logic:
  wider_leeway:
    - first_stage_base
    - multi_year_base_breakout
    - early_in_new_uptrend
    - controlled_large_base
  tighter_leeway:
    - late_stage_base
    - small_consolidation_after_extended_run
    - entry_far_above_support
```

### 9.4 Position performance

```yaml
position_cushion_logic:
  if_gain_large:
    - allow_wider_stop
    - tolerate_10w_break_if_30w_support_likely
    - give_leader_benefit_of_doubt
  if_gain_small:
    - protect_profit_or_cap_loss
    - do_not_hold_through_major_risk_without_cushion
```

---

## 10. Candidate Module F — Earnings Cushion Rule

Nick’in earnings yaklaşımı:

```yaml
candidate_id: QL_NICK_EARNINGS_CUSHION_RULE_001
type: event_risk_guard
priority: MEDIUM_HIGH
```

```yaml
earnings_rule:
  hold_through_earnings_if:
    - open_profit_cushion >= expected_implied_move
  avoid_or_reduce_if:
    - open_profit_cushion_small
    - expected_move_exceeds_profit_cushion
    - loss_would_hit_own_capital_not_only_open_profit
```

Bu, position trading için güçlü risk filtresidir.

---

## 11. Candidate Module G — Trade Frequency Guard

### 11.1 Concept

Video ana mesajı “az işlem” olduğu için bunu sistem modülü olarak kaydetmek gerekir.

```yaml
candidate_id: QL_NICK_TRADE_FREQUENCY_GUARD_001
type: portfolio_guard
priority: HIGH
```

```yaml
trade_frequency_guard:
  objective:
    - reduce_overtrading
    - keep_strategy_on_weekly_timeframe
    - prevent_low_quality_entries
  rules:
    max_new_positions_per_week: [1, 2, 3]
    require_A_quality_setup: true
    block_if_setup_quality_below_threshold: true
    no_intraday_decision_for_weekly_strategy: true
```

---

## 12. Relationship to Charles Harris Pullback Report

```yaml
overlap_with_charles_harris:
  shared:
    - buying_weakness
    - controlled_pullbacks
    - support_retests
    - risk_defined_before_entry
    - patience
    - position_trading
    - larger_timeframe_noise_reduction
  difference:
    charles_harris:
      - daily_21ema_50dma_pullback
      - core_position_swing_around_core
      - upside_reversal
      - CANSLIM_quality_and_institutional_sponsorship
    nick_schmidt:
      - weekly_only_decision_model
      - character_change
      - 10w_30w_respect
      - trade_less_philosophy
      - base_stage_and_portfolio_cushion_sell_decisions
```

Combined research opportunity:

```yaml
combined_model:
  name: QL_WEEKLY_CHARACTER_CHANGE_WITH_DAILY_PULLBACK_EXECUTION
  idea:
    - weekly_chart_detects_character_change_and_base_stage
    - daily_chart_optionally_refines_pullback_entry
    - MTC_position_manager_handles_SL_TP_trailing
  caution:
    - Nick_prefers_weekly_only
    - daily_refinement_must_not_create_overtrading
```

---

## 13. MTC V2 Mapping

```yaml
mtc_mapping:
  signal_producer:
    - QL_NICK_WEEKLY_CHARACTER_CHANGE_001
    - QL_NICK_CONTROLLED_WEAKNESS_BASE_RETEST_001
    - QL_NICK_10W_30W_RESPECT_ENTRY_001
  watchlist_generator:
    - QL_NICK_UP_ON_VOLUME_RADAR_001
  entry_gates:
    - market_participation_gate
    - setup_quality_gate
    - base_stage_gate
    - risk_manageability_gate
  position_manager:
    - low_frequency_weekly_position_manager
    - max_new_positions_per_week
    - portfolio_cushion_aware_hold_rule
  exit_rules:
    - weekly_support_break_exit
    - 10w_break_warning
    - 30w_break_exit
    - base_stage_adjusted_stop
    - earnings_cushion_guard
```

Immediate MTC/Pine integration is not recommended. This should first be a separate Python research pipeline.

---

## 14. Backtest Design

### 14.1 Primary equity-native test

```yaml
primary_test:
  asset_class: US_equities
  timeframe: 1W
  universe:
    preferred:
      - liquid_US_growth_stocks
      - previous_leaders
      - high_relative_strength_names
      - stocks_with_large_base_structures
    minimum_examples:
      - ONON
      - SQ
      - RBLX
      - SMCI
      - APP
      - DAVE
      - PLTR
      - TSLA
      - NVDA
  data:
    - weekly_ohlcv
    - daily_ohlcv_for_resampling_validation
    - earnings_dates_optional
    - index_regime_data
```

### 14.2 Crypto proxy test

```yaml
crypto_proxy_test:
  caution: "Crypto lacks equity-style sponsorship and earnings, but weekly trend/base structure can still be tested."
  assets_minimum:
    - BTCUSDT
    - ETHUSDT
    - SOLUSDT
    - BNBUSDT
    - XRPUSDT
  timeframe: 1W
  variants:
    - weekly_volume_character_change
    - 10w_30w_support_retest
    - base_breakout_retest
  reject_if:
    - too_few_trades
    - edge_disappears_after_costs
    - results_depend_only_on_BTC_bull_market
```

### 14.3 Stage 2 robustness

```yaml
robustness_tests:
  - rolling_walk_forward
  - bull_vs_bear_regime_split
  - high_rate_vs_low_rate_environment
  - market_cap_bucket_split_for_equities
  - base_length_bucket_split
  - cost_stress_2x_3x
  - random_entry_baseline_comparison
  - buy_and_hold_benchmark_comparison
```

---

## 15. Objective Metrics

```yaml
required_metrics:
  - total_net_return
  - CAGR_proxy
  - max_drawdown
  - profit_factor
  - win_rate
  - average_win
  - average_loss
  - avg_win_to_avg_loss
  - median_holding_weeks
  - average_holding_weeks
  - trade_count
  - exposure_pct
  - return_per_trade
  - return_vs_buy_and_hold
  - return_vs_SPY_or_BTC_benchmark
  - max_consecutive_losses
  - average_R
  - best_trade_contribution_pct
  - top_5_trade_dependency
```

Nick’in sistemi düşük trade count üreteceği için “top 5 trade dependency” özellikle önemlidir. Büyük kazançların sadece 1–2 trade’den gelip gelmediği kontrol edilmeli.

---

## 16. Parameter Grid

```yaml
parameter_grid:
  weekly_volume:
    volume_sma_len: [10, 20, 30]
    volume_multiple: [1.25, 1.5, 2.0]
    volume_percentile_1y: [70, 80, 90]
  candle_strength:
    close_range_min: [0.50, 0.60, 0.70]
    weekly_return_min_pct: [0, 3, 5, 10]
  moving_averages:
    fast_week_ma: [8, 10]
    slow_week_ma: [30, 40]
    ma_type: [SMA, EMA]
  higher_low:
    pivot_left_right: [1, 2, 3]
    min_low_separation_weeks: [2, 4, 6]
  base:
    min_base_weeks: [8, 12, 26, 52]
    resistance_break_buffer_pct: [0, 2, 5]
    retest_tolerance_pct: [2, 3, 5, 8]
  stops:
    fixed_max_loss_pct: [6, 8, 10, 12]
    support_buffer_pct: [2, 3, 5]
    weekly_close_confirm: [true, false]
  exits:
    exit_on_10w_break: [true, false]
    exit_on_30w_break: [true, false]
    trailing_week_ma: [10, 30]
    profit_cushion_hold_threshold_pct: [20, 50, 100]
```

---

## 17. Acceptance / Rejection Criteria

```yaml
accept_for_stage_2_if:
  - profit_factor_after_costs >= 1.25
  - avg_win_to_avg_loss >= 3.0
  - max_drawdown_acceptable
  - trade_count_sufficient_for_weekly_system
  - results_not_one_trade_dependency
  - beats_benchmark_on_risk_adjusted_basis
  - works_in_multiple_assets_or_subperiods

reject_if:
  - only_works_in_2020_or_2024_momentum_boom
  - too_few_trades_to_validate
  - average_loss_uncontrolled
  - character_change_detection_too_subjective
  - no_clear_stop_level
  - crypto_proxy_only_works_on_BTC_beta
  - weekly_signals_enter_too_late_without_edge
```

---

## 18. Recommended Codex Task

```yaml
codex_action:
  immediate:
    - create_python_only_research_folder
    - implement_weekly_resampler
    - implement_character_change_detector
    - implement_base_breakout_retest_detector
    - implement_10w_30w_respect_entry
    - implement_trade_frequency_guard
    - implement_sell_decision_simulation_v0
  avoid:
    - do_not_modify_MTC_V2_pine
    - do_not_add_alerts
    - do_not_force_to_5m_timeframe
    - do_not_use_as_direct_crypto_scalping_strategy
```

Suggested folder:

```text
06_QUANTLENS_LAB/research/nick_schmidt_weekly_character_change/
```

Suggested files:

```text
README.md
weekly_character_change.py
run_weekly_character_change_backtest.py
NICK_SCHMIDT_WEEKLY_CHARACTER_CHANGE_REPORT.md
NICK_SCHMIDT_RESULTS.csv
NICK_SCHMIDT_TRADES.csv
```

---

## 19. Final Rating

```yaml
final_rating:
  research_value: 9/10
  process_value: 9.5/10
  direct_strategy_value: 8.5/10
  equity_native_value: 9.5/10
  crypto_transfer_value: 5/10
  position_trading_value: 9.5/10
  intraday_value: 2/10
  pine_priority_now: 3/10
  python_research_priority: 9/10
  live_readiness: 3/10
```

---

## 20. Final Decision

```yaml
final_decision:
  action: ACCEPT
  classification: HIGH_VALUE_WEEKLY_POSITION_TRADING_CANDIDATE
  best_use: "Portfolio position-trading bucket; weekly character-change radar; controlled weakness entries."
  next_step: "Python-only weekly research prototype, preferably equity-native first."
  do_not_do: "Do not convert directly to Pine or 5m strategy."
```

Final conclusion:

> Bu video QuantLens için yüksek değerli bir position-trading girdisidir. Ana fikir, haftalık grafikte karakter değişimi gösteren ve risk yönetilebilir kontrollü zayıflık sunan hisselerde düşük frekanslı, yüksek R potansiyelli pozisyonlar almaktır. Bu model, Charles Harris pullback sistemiyle birleştirilerek “weekly character change + controlled weakness + risk-defined support retest” araştırma hattına dönüştürülmelidir.
