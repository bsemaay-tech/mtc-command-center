# QUANTLENS TRANSCRIPT INTAKE REPORT — Jim Roppel AI Bull Market / Position Trading Framework

**Generated:** 2026-05-03  
**Source URL:** https://youtu.be/MnXQOt7_ZP0?si=OdvX4hI-qnjYMKZp  
**Normalized URL:** https://www.youtube.com/watch?v=MnXQOt7_ZP0  
**Video ID:** `MnXQOt7_ZP0`  
**Input Transcript File:** `+85% Return in 30 Days The AI Bull Market Can Change your Life Hedge Fund Manager.md`  
**Intake Prompt File:** `00_quantlens_transcript_intake_prompt.md`  
**Transcript Status:** Provided by user as markdown transcript  
**Title:** +85% Return in 30 Days The AI Bull Market Can Change your Life Hedge Fund Manager  
**Channel:** `UNKNOWN_CHANNEL`  
**Speaker / Host Mentioned:** Jim Roppel / Richard Moglen, Trailline-style podcast  
**Transcript Digest SHA256:** `7ed40b8b6d0d92136d077a29de1639ef6da60cfaee72818d89ba657b67e123a4`

---

## 1. Executive Verdict

```yaml
classification: CANDIDATE
secondary_classification: TRADER_WIKI_RECOMMENDED
codex_status: SPEC_FIRST_THEN_PYTHON_PROTOTYPE_FOR_SUBMODULES
quantlens_priority: HIGH_FOR_POSITION_TRADING_RESEARCH
production_ready: false
pine_ready: false
python_backtest_ready: partially
strategy_family:
  - position_trading
  - can_slim_style_growth_leaders
  - mega_trend_leadership
  - relative_strength_momentum
  - institutional_accumulation
  - 50_day_reclaim
  - staged_position_building
  - 3_5_7_risk_management
primary_direction: long
primary_asset_class: US_growth_equities
crypto_transferability: medium_for_trend_filtering_low_for_fundamentals
best_first_use: risk_and_position_management_modules
```

Bu transcript **tek başına basit bir TradingView stratejisi değildir**. Değeri; uzun vadeli lider hisse yakalama, tema/mega-trend seçimi, pozisyonu sabırla taşıma, 3-5-7 risk modeli, 50 günlük ortalama etrafında davranış ve aşırı uzama durumunda hedge mantığıdır.

QuantLens için doğru yaklaşım:

```yaml
recommended_decomposition:
  candidate_modules:
    - QL_ROPPEL_50D_RECLAIM_TIGHT_ACTION_v0
    - QL_ROPPEL_357_SCALEOUT_RISK_MODULE_v0
    - QL_ROPPEL_EXTENSION_OVER_50D_HEDGE_SIGNAL_v0
    - QL_ROPPEL_LEADERSHIP_THEME_SCORE_v0
    - QL_ROPPEL_POSITION_TRADING_HOLD_ENGINE_v0
  wiki_notes:
    - mega_trend_position_trading
    - patience_cushion_and_sizing
    - institutional_accumulation_signatures
```

**Final decision:** Candidate olarak kabul edilsin; fakat full sistem olarak değil, alt modüllere bölünerek araştırılsın. İlk Python prototipi risk/sizing ve 50D reclaim/tight-action modülleri olmalı. Doğrudan MTC producer entegrasyonu yapılmamalı.

---

## 2. Prompt Compliance Notes

```yaml
mtc_v2_pine_modified: false
production_python_runner_modified: false
backtest_run: false
optimization_run: false
secret_or_api_key_written: false
large_csv_or_data_bundle_created: false
duplicate_registry_available: false
channel_blacklist_registry_available: false
```

Bu rapor sadece transcript intake analizi olarak hazırlanmıştır. Repo içindeki resmi duplicate, blacklist ve channel-quality kontrolleri Codex tarafından gerçek repo ortamında tekrar yapılmalıdır.

---

## 3. Duplicate / Registry Kontrolü

```yaml
duplicate_check_mode: standalone_uploaded_file_only
repo_registry_checked: false
video_index_checked: false
channel_blacklist_checked: false
channel_quality_registry_checked: false
exact_video_id_duplicate_found_in_uploaded_context: false
status: NOT_DUPLICATE_WITHIN_AVAILABLE_CONTEXT
```

Not: Bu oturumda repo içindeki `_registry/youtube_video_index.csv`, `channel_blacklist.yaml` ve `channel_quality_registry.csv` dosyalarına erişim yok. Bu nedenle resmi duplicate/blacklist kararı repo içinde çalışan Codex intake workflow tarafından doğrulanmalı.

---

## 4. Channel Quality Kararı

```yaml
channel: UNKNOWN_CHANNEL
quality_state: UNKNOWN
blacklist_action: none
reason: channel metadata not provided; prompt rule says use UNKNOWN_CHANNEL when channel info is missing
```

İçerik düşük kaliteli “magic indicator” videosu gibi görünmüyor. Ancak konuşma bir röportaj/podcast olduğu için kuralların bir bölümü subjektif ve deneyim temelli. Bu yüzden **CANDIDATE + TRADER_WIKI_RECOMMENDED** sınıfı daha doğru.

---

## 5. Source Quality Assessment

```yaml
source_quality_score: 8/10
strategy_idea_score: 7/10
implementation_clarity_score: 6/10
risk_management_value_score: 9/10
position_sizing_value_score: 9/10
trend_following_value_score: 8/10
fundamental_dependency_score: high
crypto_transferability_score: 5/10
```

### Positive signs

- Gerçek piyasa döngüsü, lider hisse, tema ve kurumsal alım mantığı anlatılıyor.
- Sadece giriş değil; pozisyon taşıma, stop, hedge, trimming ve position sizing anlatılıyor.
- “Fundamental hikâye doğru olsa bile teknikler doğrulamazsa dead money olur” yaklaşımı sistematik test için değerlidir.
- Risk yönetiminde 3-5-7 kademeli çıkış gibi açık bir modül var.
- Aşırı uzama durumunda hedge/volatilite azaltma mantığı var.
- Aşırı al-sat yerine uzun vadeli liderleri taşıma vurgusu QuantLens position-trading katmanı için değerli.

### Limitations

- Temel analiz, haber akışı, sektör teması ve kurumsal kalite gibi dış veriye ihtiyaç duyar.
- ABD büyüme hisselerine çok bağlıdır; crypto’ya direkt taşınmaz.
- “Mega trend”, “lider”, “kurumsal birikim”, “tight action” gibi kavramlar objektif proxy kurallara çevrilmeli.
- Options hedge bölümü MTC spot/futures tarafına doğrudan uymaz.
- Backtest survivorship bias riski yüksektir; gerçek hisse evreni ve delisted/history verisi gerekir.

---

## 6. Core System Summary

Transcriptteki ana sistem, yüksek büyüme / mega trend liderlerini seçip teknik doğrulama geldikten sonra pozisyonu büyütme ve sabırla taşıma üzerine kurulu.

```yaml
core_framework:
  universe:
    - AI_infrastructure
    - semiconductors
    - energy_for_AI
    - obesity_drugs
    - biotech
    - crypto_related
    - strong_growth_leaders
  selection_filters:
    - high_relative_strength
    - high_average_daily_dollar_volume
    - strong_sales_or_earnings_growth
    - clear_mega_trend_story
    - institutional_accumulation_signature
  entry_context:
    - breakout_from_base
    - 50_day_reclaim
    - tight_action_near_50d
    - explosive_volume_on_news_or_gap
    - market_in_confirmed_bull_mode
  risk:
    - initial_scale_out_at_minus_3_percent
    - further_scale_out_at_minus_5_percent
    - final_exit_by_minus_7_percent
  holding:
    - allow_stock_to_breathe
    - avoid_suffocating_great_opportunities
    - position_size_must_match_temperament
  hedge:
    - hedge_when_historically_extended_over_50d
    - hedge_40_to_60_percent_of_position
```

Ana mesaj:

> Büyük getiriler; doğru temadaki doğru lideri anlamlı pozisyon büyüklüğüyle yakalayıp, pozisyon boyutu ve risk yönetimi bozulmadan sabırla taşıyabilmekten geliyor.

---

## 7. Candidate 1 — 50D Reclaim + Tight Action Position Entry

```yaml
candidate_id: QL_ROPPEL_50D_RECLAIM_TIGHT_ACTION_v0
candidate_name: 50-Day Reclaim After Tight Action
candidate_type: signal_producer_research
mtc_direct_integration: false
python_first: true
asset_class:
  - US_growth_equities
  - high_beta_equities
  - crypto_proxy_optional
primary_timeframe: daily
```

### Logic

Transcriptte önemli kavramlardan biri: kaliteli lider hisse 50 günlük ortalama altında/etrafında dar aralıkta, düşük hacimli ve desteklenen bir yapı kurarsa; 50D reclaim veya 50D üstü güçlenme actionable olabilir.

```yaml
entry_setup:
  trend_context:
    - close > sma_150
    - sma_50 > sma_150
    - prior_3m_return > threshold
    - relative_strength_vs_market > 0
  tight_action:
    - last_5_to_10_day_range_pct < threshold
    - realized_volatility_declining
    - volume_below_20d_average
    - closes_near_daily_high_preferred
  reclaim_trigger:
    - close_crosses_above_sma_50
    - or high_crosses_above_sma_50_with_volume_expansion
  confirmation:
    - volume_today > volume_sma_20
    - close_in_upper_40_percent_of_daily_range
```

### Initial parameters

```yaml
parameters_v0:
  ma_reference: SMA50
  long_ma: SMA150
  tight_lookback_days: [5, 7, 10]
  max_tight_range_pct: [4, 6, 8]
  max_atr_pct_contraction_ratio: [0.6, 0.75]
  min_volume_dryup_ratio: [0.5, 0.75, 1.0]
  min_prior_60d_return: [15, 25, 40]
  close_strength_min: [0.6, 0.75]
```

### Risk

```yaml
stop_variants:
  - below_tight_range_low
  - below_sma50_minus_atr_buffer
  - 3_5_7_scaleout
exit_variants:
  - break_sma50_confirmed
  - close_below_sma50_2_days
  - fixed_R_multiple
  - trailing_ema21_or_sma50
```

### QuantLens verdict

```yaml
verdict: ACCEPT_AS_RESEARCH_CANDIDATE
priority: HIGH
reason: codable entry context; useful as position-trading entry module
```

---

## 8. Candidate 2 — 3-5-7 Scale-Out Risk Module

```yaml
candidate_id: QL_ROPPEL_357_SCALEOUT_RISK_MODULE_v0
candidate_name: 3-5-7 Loss-Control Scale-Out Module
candidate_type: risk_management_module
mtc_direct_integration: possible_later
python_first: true
asset_class:
  - equities
  - crypto
  - futures
primary_use: position_sizing_and_loss_control
```

### Logic

Bu transcriptteki en mekanik ve yüksek değerli bölüm risk modülüdür. Pozisyon ters giderse tamamını tek noktada kapatmak yerine kademeli azaltma yapılır:

```yaml
scaleout_rule:
  initial_position_units: 3
  if unrealized_loss_pct <= -3:
    close_fraction: 1/3
  if unrealized_loss_pct <= -5:
    close_fraction: 1/3
  if unrealized_loss_pct <= -7:
    close_fraction: remaining_all
```

Not: Röportajda konuşmacı artık çoğu zaman -7’ye kadar beklemediğini, genellikle -5/-6 civarında tamamen çıkabildiğini söylüyor. Bu yüzden test varyantları gerekli.

```yaml
variants:
  classic_357:
    levels: [-3, -5, -7]
    fractions: [0.333, 0.333, 1.0]
  tighter_235:
    levels: [-2, -3.5, -5]
    fractions: [0.333, 0.333, 1.0]
  adaptive_atr:
    levels_as_atr_multiple: [1.0, 1.5, 2.0]
```

### QuantLens / MTC fit

```yaml
mtc_fit:
  position_manager: high
  exit_rules: high
  risk_module: very_high
  signal_producer: no
```

Bu modül direkt sinyal üretmez; ancak MTC V2’nin position management ve exit katmanında test edilebilir.

---

## 9. Candidate 3 — Leadership Theme Score

```yaml
candidate_id: QL_ROPPEL_LEADERSHIP_THEME_SCORE_v0
candidate_name: Mega Trend Leadership Score
candidate_type: universe_filter_or_ranking_model
mtc_direct_integration: false
python_first: true
asset_class:
  - US_equities
  - crypto_sector_proxy
```

### Logic

Transcriptte güçlü temalar örnekleniyor: AI, semiconductors, AI energy infrastructure, obesity drugs, biotech, crypto, gold, international leadership. Mekanik sistem için bu doğrudan “tema tahmini” olarak değil, **fiyat + hacim + relative strength + fundamental growth** skoru olarak ele alınmalı.

```yaml
score_components:
  price_strength:
    - 3m_return_rank
    - 6m_return_rank
    - close_vs_52w_high
  trend_quality:
    - close_above_sma50
    - sma50_above_sma150
    - low_volatility_tightness_after_move
  liquidity:
    - average_daily_dollar_volume
  accumulation:
    - up_volume_vs_down_volume
    - weekly_blue_bar_count_proxy
    - gap_up_on_volume
  fundamentals_equity_only:
    - sales_growth
    - eps_growth
    - margin_expansion
```

### Crypto proxy

Crypto’da fundamentals eksik olduğu için skor şu proxy’lerle test edilebilir:

```yaml
crypto_proxy_components:
  - relative_strength_vs_BTC
  - relative_strength_vs_ETH
  - 20d_and_60d_volume_growth
  - distance_to_90d_high
  - trend_ma_alignment
  - volatility_contraction_after_impulse
```

### QuantLens verdict

```yaml
verdict: ACCEPT_AS_FILTER_OR_RANKING_LAYER
priority: MEDIUM_HIGH
reason: useful for asset selection; not enough as standalone entry system
```

---

## 10. Candidate 4 — Extension Over 50D Hedge / De-Risk Signal

```yaml
candidate_id: QL_ROPPEL_EXTENSION_OVER_50D_HEDGE_SIGNAL_v0
candidate_name: Historical Extension Over 50D Hedge Signal
candidate_type: risk_overlay
mtc_direct_integration: partial
python_first: true
asset_class:
  - equities
  - crypto
  - futures
```

### Logic

Konuşmacı, elit liderlerin yılda birkaç kez 50 günlük ortalamaya geri dönebileceğini; bu yüzden tarihsel olarak aşırı uzama durumunda pozisyonun bir kısmını hedge ederek volatiliteyi azaltmayı anlatıyor.

```yaml
extension_signal:
  reference_ma: SMA50
  extension_pct: (close / sma50 - 1) * 100
  trigger:
    - extension_pct > historical_percentile_90
    - or extension_pct > fixed_threshold
  fixed_threshold_candidates:
    - 20
    - 30
    - 40
  action_equity_options:
    - hedge_40_to_60_percent_with_short_calls_or_puts
  action_crypto_proxy:
    - reduce_position_fraction
    - tighten_trailing_stop
    - add_inverse_hedge_small_fraction
```

### Warning

Options hedge kısmı doğrudan MTC stratejisine çevrilmemeli. MTC/crypto tarafında bu daha çok **position de-risk / trailing stop tighten / partial profit lock** modülü olarak test edilmeli.

```yaml
verdict: ACCEPT_AS_RISK_OVERLAY_NOT_SIGNAL_PRODUCER
priority: MEDIUM
```

---

## 11. Candidate 5 — Position Trading Hold Engine

```yaml
candidate_id: QL_ROPPEL_POSITION_TRADING_HOLD_ENGINE_v0
candidate_name: Let Winners Breathe Hold Engine
candidate_type: exit_management_module
mtc_direct_integration: possible_later
python_first: true
```

### Logic

Transcriptin ana felsefesi: Lider pozisyonu, küçük wiggle/jiggle hareketleriyle erken satılmamalı. Ancak bu körü körüne HODL değil; position size, 50D davranışı, teknik doğrulama ve fundamental hikâye birlikte takip edilir.

```yaml
hold_conditions:
  continue_hold_if:
    - close_above_sma50_or_reclaims_quickly
    - no_major_distribution_cluster
    - relative_strength_not_breaking_down
    - stock_not_15_to_20pct_off_high_and_5pct_below_sma50
    - fundamental_story_still_valid_equity_only
  warning_conditions:
    - close_below_sma50_multiple_days
    - down_volume_expansion
    - relative_strength_breakdown
    - failed_reclaim_after_50d_break
  exit_or_hedge_conditions:
    - decisive_sma50_break
    - new_position_fails_3_5_7
    - position_size_becomes_too_large_after_gain
```

### QuantLens verdict

```yaml
verdict: ACCEPT_AS_EXIT_MANAGEMENT_RESEARCH
priority: HIGH_FOR_POSITION_TRADING
```

---

## 12. MTC V2 Architecture Fit

```yaml
mtc_v2_fit:
  signal_producer:
    - QL_ROPPEL_50D_RECLAIM_TIGHT_ACTION_v0
  signal_transform:
    - confirmation_after_reclaim
    - retest_of_50d_or_pivot
  entry_gates:
    - leadership_theme_score
    - relative_strength_gate
    - liquidity_gate
    - trend_alignment_gate
    - volatility_contraction_gate
  position_manager:
    - 3_5_7_scaleout
    - max_position_size_by_volatility
    - add_only_after_profit_cushion
  exits:
    - decisive_50d_break
    - extension_de_risk
    - trailing_ma_exit
    - distribution_cluster_exit
```

**Önemli:** Bu sistem MTC’nin short-term crypto producer mantığına doğrudan eklenmemeli. Daha uygun yer:

```yaml
recommended_destination:
  - QuantLens position_trading_research
  - MTC optional long_horizon_mode_later
  - risk_management_module_library
  - trader_wiki
```

---

## 13. Backtest Feasibility

### Equity backtest için gerekli veri

```yaml
required_equity_data:
  price_ohlcv: daily_adjusted
  survivorship_bias_free_universe: strongly_required
  dollar_volume: required
  sector_theme_mapping: optional_but_useful
  fundamentals:
    - sales_growth
    - eps_growth
    - market_cap
    - institutional_ownership_optional
```

### Crypto proxy test için gerekli veri

```yaml
required_crypto_data:
  symbols:
    - BTCUSDT
    - ETHUSDT
    - SOLUSDT
    - BNBUSDT
    - XRPUSDT
    - plus_high_beta_alts
  timeframes:
    - 1d
    - 4h_optional
  proxy_rules:
    - relative_strength_vs_BTC
    - trend_ma_alignment
    - volatility_contraction_after_impulse
    - 50d_reclaim
```

### Backtest riskleri

```yaml
backtest_risks:
  - survivorship_bias
  - lookahead_bias_in_theme_selection
  - fundamentals_availability_bias
  - discretionary_story_selection_bias
  - options_hedge_not_equivalent_to_crypto_futures
  - regime_dependency
```

---

## 14. Suggested Python Prototype Order

```yaml
prototype_order:
  1:
    module: QL_ROPPEL_357_SCALEOUT_RISK_MODULE_v0
    reason: most mechanical; directly useful across strategies
  2:
    module: QL_ROPPEL_50D_RECLAIM_TIGHT_ACTION_v0
    reason: codable entry model; good for equity and crypto proxy
  3:
    module: QL_ROPPEL_POSITION_TRADING_HOLD_ENGINE_v0
    reason: helps avoid premature exits; aligns with position trading goal
  4:
    module: QL_ROPPEL_EXTENSION_OVER_50D_HEDGE_SIGNAL_v0
    reason: risk overlay; useful after baseline entry/exit works
  5:
    module: QL_ROPPEL_LEADERSHIP_THEME_SCORE_v0
    reason: highest data requirement; avoid first-pass complexity
```

---

## 15. First Prototype Specification — Minimal v0

İlk araştırma için full fundamental CANSLIM benzeri sistem kurmak yerine basit, deterministic fiyat/hacim prototipi önerilir.

```yaml
strategy_name: QL_ROPPEL_50D_RECLAIM_TIGHT_ACTION_v0
universe:
  equity_first:
    - NVDA
    - META
    - LLY
    - CAVA
    - PLTR
    - TSLA
    - COIN
    - MSTR
  crypto_proxy:
    - BTCUSDT
    - ETHUSDT
    - SOLUSDT
    - BNBUSDT
    - XRPUSDT
timeframe: 1d
entry:
  - close_above_sma150
  - sma50_above_sma150
  - prior_60d_return_positive
  - last_7d_range_pct <= threshold
  - close_crosses_above_sma50_or_breaks_tight_range_high
  - volume_above_20d_average_optional
risk:
  - use_357_scaleout
  - initial_stop_below_tight_range_low
exit:
  - decisive_close_below_sma50
  - fixed_max_holding_optional
  - trailing_sma50
metrics:
  - net_return
  - max_drawdown
  - profit_factor
  - win_rate
  - average_R
  - exposure_days
  - turnover
```

---

## 16. Trader Wiki Note Recommendation

```yaml
wiki_recommended: true
wiki_topic:
  - 01_RISK_MANAGEMENT
  - 02_TRADING_PSYCHOLOGY
  - 03_MARKET_STRUCTURE
  - 04_SYSTEM_DEVELOPMENT
suggested_wiki_file:
  - 11_TRADER_WIKI/01_RISK_MANAGEMENT/TW_2026-05-03_roppel_357_position_sizing.md
  - 11_TRADER_WIKI/02_TRADING_PSYCHOLOGY/TW_2026-05-03_roppel_patience_cushion.md
  - 11_TRADER_WIKI/03_MARKET_STRUCTURE/TW_2026-05-03_roppel_institutional_accumulation.md
```

### Wiki ana dersleri

- Pozisyon boyutu trader’ın psikolojik toleransına uymalıdır.
- Büyük liderlerde küçük düzeltmeler normaldir; pozisyon çok büyükse trader kaliteli hareketten silkelenir.
- Fundmental hikâye teknik doğrulama olmadan yeterli değildir.
- “Price will hurt you, size will kill you” risk modülü olarak korunmalı.
- Yeni pozisyonda 3-5-7 kademeli zarar kesme, hesabı oyunda tutar.
- Mevcut büyük cushion varsa sistemin görevi erken çıkmak değil, lideri kontrollü taşımaktır.

---

## 17. Critical Warnings

```yaml
not_live_ready_reasons:
  - no backtest performed
  - fundamentals and theme selection are subjective
  - transcript contains market opinions specific to a historical period
  - symbols mentioned are not automatic buy recommendations
  - options hedge logic does not map directly to all users or markets
  - position trading requires larger drawdown tolerance than short-term systems
```

Bu video “şimdi NVDA/LLY/PLTR al” şeklinde kullanılmamalı. İçerikteki hisse isimleri örnek/bağlamdır. QuantLens için değerli olan şey; lider seçimi, tight-action, 50D davranışı, 3-5-7 risk ve pozisyonu erken boğmama prensiplerinin modüllere ayrılmasıdır.

---

## 18. Final Classification

```yaml
final_decision:
  classification: CANDIDATE
  secondary_classification: TRADER_WIKI_RECOMMENDED
  codex_status: SPEC_FIRST_THEN_PYTHON_PROTOTYPE_FOR_SUBMODULES
  priority: HIGH_FOR_RISK_AND_POSITION_TRADING_RESEARCH
  best_first_test: QL_ROPPEL_357_SCALEOUT_RISK_MODULE_v0
  second_test: QL_ROPPEL_50D_RECLAIM_TIGHT_ACTION_v0
  do_not_do_yet:
    - pine_conversion
    - production_runner_integration
    - live_alerts
    - full_fundamental_backtest_without_clean_data
```

---

## 19. Suggested Repo Paths

```text
06_QUANTLENS_LAB/intake/reports/2026-05-03_MnXQOt7_ZP0_quantlens_jim_roppel_ai_bull_market_intake_report.md
06_QUANTLENS_LAB/research/roppel_357_risk_module/README.md
06_QUANTLENS_LAB/research/roppel_50d_reclaim_tight_action/README.md
06_QUANTLENS_LAB/research/roppel_position_trading_hold_engine/README.md
11_TRADER_WIKI/01_RISK_MANAGEMENT/TW_2026-05-03_roppel_357_position_sizing.md
11_TRADER_WIKI/02_TRADING_PSYCHOLOGY/TW_2026-05-03_roppel_patience_cushion.md
11_TRADER_WIKI/03_MARKET_STRUCTURE/TW_2026-05-03_roppel_institutional_accumulation.md
```

---

## 20. Codex Next Action

```yaml
next_action_for_codex:
  1: check_duplicate_registry_by_video_id_and_transcript_hash
  2: update_youtube_video_index_if_not_duplicate
  3: create_candidate_report_under_intake_reports
  4: create_trader_wiki_notes_for_risk_and_position_trading
  5: create_python_only_spec_for_357_risk_module
  6: create_python_only_spec_for_50d_reclaim_tight_action
  7: do_not_modify_MTC_V2_pine
  8: do_not_modify_production_runner
  9: do_not_run_backtest_until_user_requests_batch_research
```

