# QUANTLENS TRANSCRIPT INTAKE REPORT — Charles Harris Perfect Pullback Trading Setup

**Generated:** 2026-05-03  
**Source URL:** https://youtu.be/ivL6E6Lc6gM?si=GNNGCxRmyNZYqNrJ  
**Normalized URL:** https://www.youtube.com/watch?v=ivL6E6Lc6gM  
**Video ID:** `ivL6E6Lc6gM`  
**Uploaded Transcript File:** `a Hedge Fund Manager Reveals his Perfect Pullback Trading Setup.md`  
**Transcript Status:** Provided by user  
**Primary Speaker:** Charles Harris  
**Speaker Context:** Portfolio manager at O'Neil Capital Management / O'Neil Global Advisors; CANSLIM/O'Neil methodology background  
**Content Type:** Pullback buying, buying weakness, core-position management, daily moving-average support, upside reversal, swing around core position  
**Transcript SHA256:** `4e7f8fd82d4a6bb0c94ae923185acecfbfbc8e3a2a8b9cb576e0f2349a3f5530`  

---

## 1. Executive Verdict

```yaml
verdict: ACCEPT_AS_HIGH_VALUE_PULLBACK_RESEARCH_CANDIDATE
production_ready: false
backtest_ready: yes_python_first
tradingview_pine_ready: later_only_after_python_validation
strategy_signal_value: high
process_value: very_high
risk_management_value: high
implementation_priority: high_for_position_trading_research
recommended_destination:
  - 06_QUANTLENS_LAB/intake/reports/
  - 06_QUANTLENS_LAB/research/pullback_models/
  - 06_QUANTLENS_LAB/research/position_trading/
  - 11_TRADER_WIKI/03_POSITION_TRADING/
```

Bu video QuantLens açısından değerli. Ana fikir basit ama profesyonel:

> Güçlü uptrend içindeki kaliteli/lider hisselerde, herkes satarken destek bölgelerinde kontrollü şekilde alım yapmak; bunu core pozisyon etrafında swing ederek uygulamak.

Bu bir “rastgele dip al” sistemi değildir. Harris’in modeli sadece şu şartlarda anlamlıdır:

```yaml
must_have_conditions:
  - general_market_defined_uptrend
  - stock_defined_uptrend
  - higher_highs_and_higher_lows
  - rising_50_day_moving_average
  - high_conviction_stock
  - strong_fundamentals_or_compelling_story
  - sufficient_liquidity
  - institutional_sponsorship
  - clearly_defined_support_level
  - predefined_loss_line
```

---

## 2. Strategy Classification

```yaml
classification:
  primary: DAILY_PULLBACK_BUYING_RESEARCH_CANDIDATE
  secondary:
    - CANSLIM_PULLBACK_EXTENSION
    - CORE_POSITION_SWING_AROUND_CORE
    - 21EMA_PULLBACK_ADD
    - 50DMA_FIRST_PULLBACK_ADD
    - PRIOR_BASE_TOP_SUPPORT_BUY
    - UPSIDE_REVERSAL_ENTRY
    - REVERSE_PYRAMID_PULLBACK_SCALE_IN
    - WEEKLY_CONFIRMATION_SHAKEOUT_GUARD
  not_recommended_as:
    - pure_intraday_strategy
    - 5m_scalping_strategy
    - crypto_high_leverage_system
    - standalone_signal_without_market_regime_filter
```

---

## 3. Source Quality Assessment

```yaml
source_quality_score: 9/10
strategy_idea_score: 8.5/10
implementation_clarity_score: 8/10
risk_management_score: 9/10
process_value_score: 9/10
crypto_transferability_score: 5.5/10
equity_position_trading_relevance_score: 9.5/10
mtc_relevance_score: 8/10
```

### Positive signs

- Speaker professional PM background has high process credibility.
- Rules are not vague motivational statements; there are clear support references:
  - 10-day MA
  - 21-day EMA
  - 50-day MA
  - prior base/consolidation top
  - upside reversal low
- Risk is explicitly defined before entry.
- Strong emphasis on market regime; pullbacks should be bought only in a strong general market.
- Scaling and reverse pyramiding are actionable position-management ideas.
- Strategy naturally complements Nick Schmidt weekly position-trading model.
- Useful for long-term portfolio bucket and swing-around-core module.

### Weaknesses / implementation risks

- Still partly discretionary: conviction, sponsorship, story, and quality are hard to code.
- Works best in US growth equities; crypto transfer is imperfect.
- Buying weakness can become dangerous without market regime and trend filter.
- “First pullback to 50-day is almost always buyable” must be stress-tested; not accepted blindly.
- Gap risk, earnings risk, and macro selloff risk must be modeled.
- Pullback entries can create low win-rate if applied to low-quality/non-leading assets.

---

## 4. Core Philosophy

```yaml
core_philosophy:
  - trade_in_line_with_personality
  - buy_weakness_only_in_uptrend
  - swing_trade_around_core_position
  - sell_some_into_strength
  - recover_or_add_shares_on_pullbacks
  - define_loss_before_buying
  - discipline_trumps_conviction
```

Harris’in yaklaşımı:

1. Önce güçlü/lider bir hisse belirlenir.
2. İdeal olarak core pozisyon zaten vardır.
3. Hisse uzayınca parça parça kâr alınır.
4. Normal/constructive pullback geldiğinde destek bölgesinde tekrar alım yapılır.
5. Destek kırılırsa disiplinle zarar kesilir.
6. Eğer shakeout ise pozisyon korunur veya eklenir.

Bu nedenle bu video bir **entry producer** kadar, bir **position-management framework** olarak da değerlidir.

---

## 5. Candidate Strategy A — Upside Reversal Pullback Entry

### 5.1 Idea

Stock güçlü uptrend içindeyken birkaç günlük pullback yapar; destek bölgesine gelir; gün içinde aşağı sarkıp sonra yukarı döner ve güçlü kapanır. Bu upside reversal, zayıf ellerin silkelenip destek geldiğini gösterir.

```yaml
candidate_id: QL_CHARLES_UPSIDE_REVERSAL_PULLBACK_001
type: signal_producer_candidate
priority: HIGH
direction: long
timeframe:
  primary: 1D
  context: 1W
```

### 5.2 Objective v0

```yaml
setup_context:
  market_regime:
    required: general_market_uptrend
  stock_trend:
    required:
      - higher_highs_higher_lows
      - close_above_rising_50dma
      - 50dma_slope_positive
  pullback:
    min_days: [3, 4, 5, 8]
    min_depth_from_high_pct: [10, 12, 15]
    preferred_depth_pct: [12, 18, 20]
    max_depth_pct: [25, 30]
  support_area:
    any:
      - near_21ema
      - near_50dma
      - near_prior_base_top
      - near_prior_consolidation_top
  upside_reversal:
    required:
      - intraday_low_below_prior_day_low_or_near_support
      - close_above_open
      - close_position_in_range >= 0.60
    preferred:
      - volume > volume_sma50
      - volume > previous_day_volume
  entry:
    options:
      - close_of_reversal_day
      - reclaim_of_support_intraday
      - next_day_followthrough_above_reversal_high
  stop:
    primary: below_intraday_low_of_reversal_day
    alternatives:
      - below_support_zone
      - daily_close_below_support
      - next_day_confirmation_failure
```

### 5.3 Why this is useful

Bu modül, Harris’in en mekanik hale getirilebilir fikridir. Kodlanabilir ve backtest edilebilir.

---

## 6. Candidate Strategy B — First Pullback to 50DMA

### 6.1 Idea

Güçlü lider hisseler genellikle breakout sonrası ilk ciddi geri çekilmede 50-day MA / 10-week line civarında destek bulur. Harris bunu “almost always aggressively buy the first pullback to the 50-day” şeklinde anlatıyor; fakat QuantLens bunu hipotez olarak test etmeli.

```yaml
candidate_id: QL_CHARLES_FIRST_PULLBACK_50DMA_001
type: signal_producer_candidate
priority: HIGH
direction: long
timeframe: 1D
```

### 6.2 Objective v0

```yaml
preconditions:
  - breakout_or_strong_advance_recently
  - price_above_50dma_for_N_days_after_breakout
  - 50dma_slope_positive
  - stock_return_since_breakout >= threshold
first_pullback_definition:
  - first_touch_or_near_touch_of_50dma_after_breakout
  - no_prior_50dma_test_since_breakout
  - pullback_depth_from_high >= 12_percent
entry_variants:
  A_wait_reversal:
    - enter_on_upside_reversal_near_50dma
  B_buy_at_support:
    - limit_buy_within_x_percent_of_50dma
  C_followthrough:
    - enter_next_day_if_price_reclaims_reversal_high
stop_variants:
  - below_50dma_by_buffer
  - below_reversal_day_low
  - close_below_50dma
  - next_day_lower_low_after_50dma_break
```

### 6.3 Important caution

Bu model sadece kaliteli/lider hisselerde ve güçlü genel piyasa rejiminde çalışabilir. Basitçe “fiyat 50DMA’ya geldi al” şeklinde test edilirse yanlış sonuç verir.

---

## 7. Candidate Strategy C — 21 EMA Pullback Add-On

### 7.1 Idea

Birçok güçlü primary advance 21-day EMA tarafından taşınır. 21 EMA, 10-day’den daha uzak olduğu için 10–15% civarı pullback fırsatı verir.

```yaml
candidate_id: QL_CHARLES_21EMA_PULLBACK_ADDON_001
type: add_on_entry_module
priority: MEDIUM_HIGH
direction: long
timeframe: 1D
```

### 7.2 Objective v0

```yaml
context:
  - existing_position_preferred
  - stock_in_primary_advance
  - price_above_21ema_for_N_days
  - 21ema_slope_positive
pullback:
  - price_touches_or_nears_21ema
  - pullback_depth_pct between 8_and_18
entry:
  preferred:
    - upside_reversal_at_21ema
  optional:
    - support_touch_with_limit_order
stop:
  - below_reversal_low
  - close_below_21ema
  - decisive_break_to_50dma
```

### 7.3 Role in MTC

Bu daha çok **position add-on module** olarak kullanılmalı; ilk entry producer olmaktan çok mevcut kazanan pozisyona ekleme mantığıdır.

---

## 8. Candidate Strategy D — Prior Base Top Support Pullback

### 8.1 Idea

Bir hisse kısa/orta vadeli konsolidasyondan yukarı kırıldıktan sonra, eski direnç bölgesi yeni destek olabilir. Harris Shopify örneğiyle bunu anlatıyor.

```yaml
candidate_id: QL_CHARLES_PRIOR_BASE_TOP_SUPPORT_PULLBACK_001
type: signal_producer_candidate
priority: MEDIUM_HIGH
direction: long
timeframe: 1D
```

### 8.2 Objective v0

```yaml
support_definition:
  prior_consolidation:
    min_length_days: [5, 10, 15, 20]
    max_depth_pct: [8, 12, 15]
  breakout:
    close_above_consolidation_high: true
    volume_confirmation: optional
  support_retest:
    price_returns_to_prior_consolidation_high_zone
    distance_to_support_pct <= [2, 3, 5]
entry:
  - upside_reversal_at_prior_resistance_now_support
  - limit_buy_near_support
  - followthrough_after_bounce
stop:
  - close_below_support_zone
  - below_intraday_low_of_reversal
  - structure_break
```

---

## 9. Candidate Module E — Reverse Pyramid Pullback Scale-In

### 9.1 Idea

Klasik pyramiding’de fiyat yükseldikçe daha az ekleme yapılır. Pullback alımında bunun tersi uygulanır: destek bölgesine yaklaştıkça risk azalır; bu yüzden küçük başlayıp destek yaklaştıkça daha fazla alınabilir.

```yaml
candidate_id: QL_CHARLES_REVERSE_PYRAMID_PULLBACK_SCALEIN_001
type: position_sizing_module
priority: HIGH
```

### 9.2 Objective v0

```yaml
reverse_pyramid:
  premise:
    - support_level_known
    - stop_level_known
    - max_position_size_known
  scale_plan:
    tranche_1:
      trigger: pullback_within_8_percent_of_support
      size: 10_to_20_percent_of_target_add
    tranche_2:
      trigger: pullback_within_5_percent_of_support
      size: 20_to_30_percent_of_target_add
    tranche_3:
      trigger: pullback_within_2_percent_of_support
      size: 30_to_40_percent_of_target_add
    tranche_4:
      trigger: upside_reversal_or_reclaim
      size: remainder
  hard_rule:
    - total_risk_after_all_tranches <= configured_account_risk
```

### 9.3 Why useful

Bu modül MTC V2 position sizing/add-on mantığına güçlü şekilde bağlanabilir. Özellikle long position-trading bucket için değerlidir.

---

## 10. Candidate Module F — Swing Around Core Position

### 10.1 Idea

Asıl büyük para core pozisyonda kazanılır; ama pozisyonun bir kısmı strength’te azaltılıp weakness’te geri alınabilir. Bu, trendden kopmadan cost basis ve psikolojiyi iyileştirir.

```yaml
candidate_id: QL_CHARLES_SWING_AROUND_CORE_001
type: portfolio_position_management_module
priority: HIGH
```

### 10.2 Objective v0

```yaml
core_swing_model:
  core_position:
    maintain_while:
      - trend_intact
      - above_50dma_or_10week
      - no_decisive_sell_signal
  trading_shares:
    sell_into_strength_when:
      - extension_from_10dma_or_21ema_above_threshold
      - climactic_move
      - multi_week_advance_without_pullback
    rebuy_on_weakness_when:
      - pullback_to_21ema
      - pullback_to_50dma
      - prior_base_top_retest
      - upside_reversal
  objective:
    - improve_cost_basis
    - reduce_emotional_pressure
    - avoid_full_exit_from_big_winner
```

---

## 11. Candidate Module G — Weekly Shakeout Confirmation Guard

### 11.1 Idea

Bir hisse hafta içinde 50DMA/10-week altına sarkabilir ama hafta sonunda güçlü kapanarak shakeout gösterebilir. Harris, büyük cushion varsa en azından pozisyonun bir kısmı için hafta kapanışını beklemenin büyük kazananlarda faydalı olabileceğini söylüyor.

```yaml
candidate_id: QL_CHARLES_WEEKLY_SHAKEOUT_CONFIRMATION_GUARD_001
type: exit_guard
priority: MEDIUM_HIGH
```

### 11.2 Objective v0

```yaml
weekly_shakeout_guard:
  applies_if:
    - position_has_large_profit_cushion
    - stock_is_leader
    - first_or_second_test_of_50dma
  intraday_break:
    - do_not_full_exit_immediately
    - reduce_partial_if_needed
  confirmation:
    bullish:
      - weekly_close_reclaims_50dma_or_10week
      - close_above_40_percent_from_weekly_low
      - next_day_strength_after_shakeout
    bearish:
      - next_day_breaks_lower_after_50dma_failure
      - weekly_close_near_low_below_50dma
      - heavy_volume_decisive_break
```

### 11.3 Caution

Bu modül küçük hesap/leveraged crypto futures için tehlikelidir. Daha çok büyük kazanan equity position-trade için kullanılmalı.

---

## 12. Market Regime Gate

Harris’in en önemli kurallarından biri: pullback buying sadece güçlü piyasa trendinde yapılmalı.

```yaml
market_regime_gate:
  candidate_id: QL_CHARLES_MARKET_UPTREND_REQUIRED_GATE_001
  type: entry_gate
  priority: CRITICAL
  rules:
    require_any:
      - index_above_50dma_and_200dma
      - index_50dma_slope_positive
      - index_higher_high_higher_low_structure
      - breadth_positive
      - up_on_volume_count_improving
  block_if:
    - general_market_downtrend
    - index_decisive_50dma_break
    - distribution_cluster
```

QuantLens notu:

> Bu gate olmadan pullback sistemi test edilmemeli. Yoksa ayı piyasasında düşen bıçağı yakalama sistemine dönüşür.

---

## 13. Implementation Fit — MTC V2

```yaml
mtc_integration:
  immediate_pine: false
  immediate_mtc_default_producer: false
  recommended_path:
    1: python_only_research
    2: daily_equity_pullback_model
    3: crypto_proxy_test_with_caution
    4: MTC_position_management_mapping
    5: only_then_pine_candidate
```

### MTC layer mapping

```yaml
layer_mapping:
  signal_producer:
    - QL_CHARLES_UPSIDE_REVERSAL_PULLBACK_001
    - QL_CHARLES_FIRST_PULLBACK_50DMA_001
    - QL_CHARLES_PRIOR_BASE_TOP_SUPPORT_PULLBACK_001
  entry_gate:
    - QL_CHARLES_MARKET_UPTREND_REQUIRED_GATE_001
    - liquidity_gate
    - trend_quality_gate
    - extension_not_chase_gate
  position_sizing:
    - QL_CHARLES_REVERSE_PYRAMID_PULLBACK_SCALEIN_001
  position_manager:
    - QL_CHARLES_SWING_AROUND_CORE_001
  exit_rules:
    - upside_reversal_low_stop
    - 21ema_failure_stop
    - 50dma_decisive_break_exit
    - weekly_shakeout_confirmation_guard
```

---

## 14. Backtest Design

### 14.1 Stage 1 — Equity-native daily backtest

```yaml
stage_1_equity_native:
  purpose: "Test in the asset class where the system was designed."
  data:
    - adjusted_daily_ohlcv
    - weekly_resample_optional
    - benchmark_index
  universe:
    minimum:
      - TSLA
      - ZM
      - SHOP
      - LULU
      - COUP
      - SE
      - PDD
      - DKNG
      - SWKS
    recommended:
      - liquid_growth_stock_universe
      - high_RS_universe
      - CANSLIM_like_universe
  timeframe:
    - daily
  context:
    - weekly
```

### 14.2 Stage 2 — Crypto proxy

```yaml
stage_2_crypto_proxy:
  purpose: "Check if pullback-to-MA + upside reversal logic transfers to crypto."
  caution: "Crypto lacks equity fundamentals/sponsorship; use only as proxy."
  assets_minimum:
    - BTCUSDT
    - ETHUSDT
    - SOLUSDT
    - BNBUSDT
    - XRPUSDT
  timeframe:
    - 1D
  variants:
    - pullback_to_21ema_upside_reversal
    - pullback_to_50dma_upside_reversal
    - first_pullback_to_50dma
    - prior_range_top_support_retest
  costs:
    - spot_fee
    - futures_fee
    - 2x_fee_stress
    - 3x_fee_stress
```

### 14.3 Stage 3 — MTC module test

```yaml
stage_3_mtc:
  only_if:
    - positive_expectancy_after_costs
    - stable_across_assets
    - acceptable_maxDD
    - not_one_name_dependency
  tests:
    - MTC_SL_ATR
    - MTC_TP_R_multiple
    - MTC_trailing
    - MTC_partial_exit
    - MTC_market_regime_gate
```

---

## 15. Metrics Required

```yaml
required_metrics:
  - net_return
  - CAGR_proxy
  - max_drawdown
  - profit_factor
  - win_rate
  - avg_win
  - avg_loss
  - avg_win_to_avg_loss
  - expectancy_R
  - trade_count
  - average_holding_days
  - median_holding_days
  - first_pullback_success_rate
  - support_break_failure_rate
  - upside_reversal_failure_rate
  - gap_down_after_entry_rate
  - regime_filtered_vs_unfiltered_comparison
```

---

## 16. Parameter Grid

```yaml
parameters:
  trend_filter:
    ma_fast: [10]
    ma_mid: [21]
    ma_slow: [50]
    ma_long: [200]
    require_50dma_slope_positive: [true, false]
    require_above_200dma: [true, false]
  pullback:
    min_pullback_days: [3, 4, 5, 8]
    min_pullback_pct: [8, 10, 12, 15]
    preferred_pullback_pct: [12, 15, 18, 20]
    max_pullback_pct: [25, 30, 35]
  support_distance:
    near_21ema_pct: [1, 2, 3, 5]
    near_50dma_pct: [1, 2, 3, 5]
    near_prior_base_top_pct: [1, 2, 3, 5]
  reversal:
    close_range_min: [0.55, 0.60, 0.70]
    volume_multiple: [1.0, 1.2, 1.5]
  stops:
    stop_mode:
      - reversal_low
      - support_minus_buffer
      - close_below_support
      - next_day_confirmation_failure
    support_buffer_pct: [1, 2, 3, 5]
  exits:
    exit_mode:
      - 10dma_break
      - 21ema_break
      - 50dma_break
      - MTC_ATR_trail
      - partial_strength_sell_plus_core
```

---

## 17. Overlap With Previous QuantLens Reports

```yaml
overlap:
  Nick_Schmidt_weekly:
    - buying_weakness
    - holding_big_winners
    - weekly_noise_reduction
    - low_risk_entries
    - position_trading
  CANSLIM:
    - strong_fundamentals
    - institutional_sponsorship
    - market_regime
    - leaders
    - pivots_and_bases
  Martin_Luke_pullback:
    - pullback_entry
    - trend_continuation
    - risk_defined
  Oliver_Kell_cycle:
    - stage_transitions
    - moving_average_support
  Daily_Extension_Anti_Chase:
    - do_not_chase_extension
    - buy_after_reset
```

Unique value:

```yaml
unique_value:
  - explicit_pullback_buying_framework_from_O_Neil_PM
  - 21ema_and_50dma_support_buy_rules
  - upside_reversal_as_support_confirmation
  - reverse_pyramid_on_weakness
  - swing_around_core_position
  - weekly_shakeout_confirmation_guard
```

---

## 18. Critical Rejection Conditions

```yaml
reject_if:
  - no_market_regime_filter
  - no_stock_uptrend_filter
  - no_support_level_defined
  - no_stop_defined_before_entry
  - applied_to_downtrending_assets
  - applied_to_illiquid_assets
  - works_only_before_costs
  - maxDD_unacceptable
  - profit_factor_below_1_after_fee_stress
  - not_robust_across_assets_or_periods
```

---

## 19. Recommended Codex Action

```yaml
codex_action:
  immediate:
    - save_this_intake_report
    - add_to_position_trading_research_backlog
    - group_with_Nick_Schmidt_weekly_and_Martin_Luke_pullback
  do_not:
    - do_not_modify_MTC_V2_pine
    - do_not_add_live_alerts
    - do_not_force_5m_rerun
    - do_not_treat_as_simple_buy_the_dip
  next_build:
    - create_python_only_research_folder
    - implement_daily_pullback_to_21ema
    - implement_first_pullback_to_50dma
    - implement_upside_reversal_detector
    - implement_prior_base_top_support_detector
    - implement_reverse_pyramid_scalein_simulation
    - compare_market_regime_filtered_vs_unfiltered
```

Suggested folder:

```text
06_QUANTLENS_LAB/research/charles_harris_pullback_buying/
```

Suggested files:

```text
README.md
charles_pullback_buying.py
run_charles_pullback_backtest.py
CHARLES_HARRIS_PULLBACK_BUYING_REPORT.md
CHARLES_HARRIS_RESULTS.csv
CHARLES_HARRIS_TRADES.csv
```

---

## 20. Final Rating

```yaml
final_rating:
  research_value: 9/10
  process_value: 9/10
  direct_strategy_value: 8.5/10
  equity_native_value: 9.5/10
  crypto_transfer_value: 5.5/10
  position_trading_value: 9/10
  intraday_value: 3/10
  pine_priority_now: 4/10
  python_research_priority: 9/10
  live_readiness: 3/10
```

---

## 21. Final Decision

```yaml
final_decision:
  action: ACCEPT
  classification: HIGH_VALUE_DAILY_PULLBACK_POSITION_TRADING_CANDIDATE
  priority: HIGH
  best_next_step: "Python-only daily/weekly research prototype; equity-native if data exists; crypto proxy only secondary."
  key_use_case: "Uzun vadeli/position trading portföy bucket içinde güçlü liderlerde weakness buy ve core etrafında swing."
```

Final conclusion:

> Bu video güçlü bir QuantLens adayıdır. En iyi kullanım alanı, MTC V2’nin hızlı intraday tarafı değil; portföyün uzun vadeli/position-trading kısmında güçlü trend içindeki pullback’leri yakalamaktır. İlk aşamada Pine’a geçilmemeli; Python-only research ile 21 EMA pullback, ilk 50DMA pullback, upside reversal ve reverse-pyramid scale-in modülleri test edilmelidir.
