# QuantLens Transcript Intake Report — The Million Dollar TQQQ Swing Trading Strategy / Vibha Jha

## 1. Intake Kararı

- **Final Classification:** `CANDIDATE`
- **Codex Status Önerisi:** `READY_FOR_PYTHON_PROTOTYPE`
- **Wiki Notu Önerisi:** `YES — 01_RISK_MANAGEMENT`, ayrıca `04_SYSTEM_DEVELOPMENT`, `05_BACKTESTING_AND_OPTIMIZATION`, `06_EXECUTION_AND_FEES`
- **Öncelik:** `VERY_HIGH`
- **Güven:** `0.90`
- **Karar Özeti:** Bu transcript QuantLens için iki güçlü araştırma hattı veriyor:  
  1. **TQQQ swing / leveraged index exposure strategy**: market dönüşlerinde TQQQ ile hızlı exposure alma, 20%+ swingleri yakalama, strength içine satış, distribution/MA/volume sinyalleriyle risk azaltma.  
  2. **True Market Leader / CANSLIM position trading process**: fundamental-first watchlist, 10-week / 50-day teknik stop, 12–18 ay hedefli winner hold, TQQQ’den individual stock’lara sermaye geçişi.

Bu video tek başına Pine’a çevrilmemeli. İlk etapta Python research prototipi + feature contract + case extraction yapılmalı. TQQQ stratejisi doğrudan backtest edilebilir; individual stock tarafı ise fundamental data gerektirdiği için ayrı equity scanner / research branch ister.

---

## 2. Metadata

- **Candidate ID:** `YT_aDRYV4mjlHA_20260503_A`
- **Source URL:** `https://youtu.be/aDRYV4mjlHA?si=3rtey_IW5W7-U_XR`
- **Normalized URL:** `https://www.youtube.com/watch?v=aDRYV4mjlHA`
- **Video ID:** `aDRYV4mjlHA`
- **Title:** `The Million Dollar TQQQ Swing Trading Strategy Vibha Jha`
- **Channel:** `UNKNOWN_CHANNEL`
- **Speaker / Main Trader:** `Vibha Jha`
- **Transcript File:** `The Million Dollar TQQQ Swing Trading Strategy Vibha Jha.md`
- **Transcript SHA256:** `bb8da7bc3981399723ff551422788907bc8852650f5f4d8c05c9def4fb738640`
- **Report Date:** `2026-05-03`
- **Language:** English transcript; Turkish intake report
- **Detected Market Type:** US equities, NASDAQ growth stocks, leveraged ETF `TQQQ`, CANSLIM / true market leader investing
- **Primary Timeframes:**  
  - TQQQ: daily / weekly swing; days to weeks; sometimes core exposure while Stage 2 uptrend persists  
  - Individual stocks: weekly-first position trading; 12–18 month target hold if acting right
- **Core Method Mentioned:** CANSLIM, IBD 50 / Sector Leaders / IPO Leaders, RS rating/line, quarterly earnings/sales growth, 10-week MA, 50-day MA, 21-day MA, 10-day MA, distribution days, 52-week high, TQQQ swing trading, selling into strength, technical stop-loss, stage/uptrend context

---

## 3. Duplicate / Registry Kontrolü

### Conversation İçi Kontrol

Bu conversation içinde daha önce işlenen video ID’leri:

- `lTiR1pc82EE`
- `QzzKqmPcB3A`
- `R1sNTB2Vh7w`
- `lS9zbnLi1Gg`
- `jLioqyVlRkE`

Bu transcript video ID:

- `aDRYV4mjlHA`

**Sonuç:** Conversation içinde duplicate görünmüyor.

### Repo Registry Kontrolü

Aşağıdaki repo dosyaları bu chat ortamına yüklenmediği için gerçek registry kontrolü yapılamadı:

- `_registry/youtube_video_index.csv`
- `channel_blacklist.yaml`
- `channel_quality_registry.csv`
- Candidate registry dosyaları

**Registry Durumu:** `NOT_CHECKED_EXTERNAL_REGISTRY`

Codex repo içinde çalışırken önce registry dosyalarını okumalı; aynı `video_id` veya aynı `transcript_hash` varsa yeni candidate üretmemeli.

---

## 4. Channel Quality / Blacklist Kararı

- **Channel:** `UNKNOWN_CHANNEL`
- **Blacklist Kararı:** Verilemez.
- **Neden:** Transcript içinde güvenilir kanal adı / kanal ID alanı yok.
- **Geçici Quality State:** `UNKNOWN`
- **Bu video kanal kalitesine etkisi:** Pozitif. İçerik detaylı, uygulanabilir ve test edilebilir trade/risk process bilgisi içeriyor. Kanal tespit edilirse bu video `CANDIDATE` olarak kalite skoruna pozitif yazılabilir.

---

## 5. İçerik Özeti

Video, Vibha Jha’nın CANSLIM tabanlı stock selection sürecini, farklı hesap türlerinde risk/tax yönetimini, individual true market leader pozisyonlarıyla TQQQ swing trading’i nasıl birleştirdiğini anlatıyor.

Ana mesajlar:

1. TQQQ, özellikle IRA gibi tax drag olmayan hesaplarda swing trading için kullanılıyor.
2. Individual stock tarafında hedef, potansiyel **true market leader** olan, double/triple yapma kapasitesi bulunan hisseleri bulmak.
3. Fundamental seçim genelde önce gelir: quarterly earnings/sales, projected earnings, EPS/Comp rating, RS rating/line, IBD 50 / Sector Leaders / IPO Leaders.
4. Teknik girişte haftalık büyük resim kullanılıyor; günlük chart execution için kullanılıyor.
5. Individual stocks için stop mantığı yüzde sabitinden çok teknik seviyeye bağlanıyor: 10-week MA / 50-day MA.
6. TQQQ’de amaç, individual stock setup az olduğunda veya mega-cap NASDAQ liderliği hakim olduğunda index momentumunu kaldıraçlı yakalamak.
7. TQQQ’de 20%+ swingler, önceki swing high/low, MA uzaklığı, distribution günleri ve sentiment/sell-signal cluster’ları ile takip ediliyor.
8. TQQQ’de satış daha çok **selling into strength** mantığında; individual stock’larda ise daha çok winner hold / technical-fundamental invalidation mantığında.
9. TQQQ stratejisinde sell signal tekil sinyal değil, sinyal kümesi mantığıyla çalışıyor.
10. Kendi trading planında “ne alacağım, ne zaman alacağım, ne kadar alacağım, ne zaman satacağım” sorularının hepsi cevaplanmalı.

---

## 6. Kodlanabilir Strateji / Sistem Çekirdekleri

Bu transcript üç ayrı araştırma modülüne bölünmelidir.

---

### Candidate A — TQQQ Swing Regime Strategy v1

**Amaç:** QQQ/NASDAQ uptrend veya dönüş dönemlerinde TQQQ ile hızlı ve likit exposure almak; 20%+ swingleri yakalayıp strength içine kademeli çıkmak.

**Neden Değerli:** Bu modül doğrudan OHLCV verisiyle backtest edilebilir. Fundamental data gerektirmez. Python prototipi için en hazır adaydır.

#### 6A.1. Universe

```yaml
tqqq_swing_regime_v1:
  primary_symbol: "TQQQ"
  reference_symbols:
    qqq: "QQQ"
    nasdaq_index_proxy: "QQQ"
    spy: "SPY"
  timeframe:
    execution: "1D"
    confirmation: "1W optional"
  data_required:
    - open
    - high
    - low
    - close
    - volume
    - adjusted_close
```

#### 6A.2. Core Entry Logic

Vibha’nın anlatımına göre entry çoğu zaman market turn / rally attempt / higher-high higher-low bağlamında geliyor.

Kodlanabilir yaklaşım:

```yaml
entry_conditions:
  regime_precondition_any:
    - qqq_close_above_sma_50
    - qqq_stage2_reclaim_candidate
    - qqq_higher_high_higher_low_after_correction
    - follow_through_day_recent
    - rally_day_4_or_5_with_higher_lows
  tqqq_entry_trigger_any:
    - tqqq_turns_up_after_pullback
    - tqqq_reclaims_21d_or_50d
    - tqqq_close_above_prior_day_high
    - tqqq_close_above_10d_after_pullback
    - tqqq_rally_attempt_low_holds
  preferred_pullback_depth:
    from_recent_high_pct: [10, 13, 15]
  initial_position_pct:
    conservative: 25
    aggressive: 50
  notes:
    - "Entry can start before official follow-through day if higher-high/higher-low structure appears."
    - "If rally day low is undercut, exit."
```

#### 6A.3. Initial Stop / Invalidation

```yaml
risk_model:
  hard_invalidation:
    - undercut_rally_day_low
    - failed_turn_after_entry
    - qqq_regime_failure
  technical_reference:
    - tqqq_50d
    - tqqq_21d
    - rally_day_low
  max_initial_risk_mode:
    type: "structure_based"
    fallback_pct: [5, 8, 10]
  caution:
    - "TQQQ is leveraged; gap risk and compounding decay must be modeled."
    - "Backtest must use adjusted data and real TQQQ history."
```

#### 6A.4. Sell Into Strength Logic

Transcriptte özellikle TQQQ için selling into strength vurgulanıyor. Kodlanabilir sinyaller:

```yaml
sell_into_strength_signals:
  signal_1_new_52w_high:
    enabled: true
    action: "watch_for_resistance_or_partial_trim"
  signal_2_new_high_declining_volume:
    enabled: true
    action: "partial_trim"
  signal_3_distribution_cluster:
    enabled: true
    market: "NASDAQ/QQQ"
    threshold_days: [4, 5]
    window_days: [20, 25]
    action: "increase_trim_aggression"
  signal_4_loss_of_10d_on_rising_volume:
    enabled: true
    action: "partial_or_major_reduce"
  signal_5_three_down_days_rising_volume:
    enabled: true
    action: "partial_reduce"
  signal_6_resistance_rejection_3x:
    enabled: true
    action: "partial_reduce"
  signal_7_poor_weekly_close_below_10w_on_rising_volume:
    enabled: true
    action: "major_reduce_or_exit"
  signal_8_sentiment_froth:
    enabled: false_for_v1
    note: "Bulls vs Bears > 60% mentioned; external sentiment data optional."
```

#### 6A.5. Cluster-Based Exit Engine

Tek sinyalde tüm pozisyonu kapatmak yerine sinyal sayısına göre kademeli satış:

```yaml
exit_cluster_engine:
  score_per_signal: 1
  score_actions:
    score_0_1: "hold_or_watch"
    score_2: "trim_10pct_of_position"
    score_3: "trim_25pct_of_position"
    score_4_plus: "major_reduce_or_exit"
  maintain_core_if:
    - qqq_stage2_uptrend
    - tqqq_above_key_weekly_ma
    - profit_cushion_positive
  core_position_floor_pct:
    default: 25
```

#### 6A.6. Profit Target / Swing Context

Vibha, yıl içindeki TQQQ swinglerini takip ederek 20%+ hareketleri yakalamaya çalışıyor.

```yaml
swing_tracking:
  measure_from_recent_swing_low_to_high: true
  target_swing_gain_pct:
    normal: [20, 25]
    strong_cycle: [30, 35]
  track_days_to_move: true
  if_price_up_pct_from_swing_low:
    - pct: 20
      action: "begin_watch_for_strength_sell"
    - pct: 25
      action: "partial_trim_if_any_sell_signal"
    - pct: 30
      action: "aggressive_trim_unless_strong_regime"
```

#### 6A.7. Backtest Research Questions

1. TQQQ’de 10–15% pullback sonrası 21D/50D reclaim entry gerçekten edge veriyor mu?
2. Rally-day-low stop, klasik 50D stop’tan daha iyi mi?
3. 20%+ swing hedefi ve sell-signal cluster kârı koruyor mu?
4. 4–5 distribution day filter drawdown’u azaltıyor mu?
5. TQQQ core position floor, pure swing trading’e göre daha iyi expectancy veriyor mu?
6. TQQQ stratejisi QQQ Stage 2 rejiminde mi çalışıyor, yoksa bear rally’lerde de işliyor mu?
7. 2022 gibi bear marketlerde false turn maliyeti ne?
8. Leveraged ETF decay nedeniyle uzun hold edilen core TQQQ, QQQ + margin proxy’ye göre nasıl davranıyor?

---

### Candidate B — True Market Leader Fundamental + Technical Watchlist v1

**Amaç:** Individual stock tarafında double/triple potansiyeli olan TML adaylarını watchlist’e almak.

Bu modül Python equity scanner gerektirir; MTC_V2 crypto parity engine içine doğrudan alınmamalı.

#### 6B.1. Fundamental Filters

```yaml
true_market_leader_watchlist_v1:
  source_lists:
    - IBD_50
    - Sector_Leaders
    - IPO_Leaders
    - New_America
  required_fundamentals:
    quarterly_eps_growth_pct_min: 25
    quarterly_sales_growth_pct_min: 25
    preferred_eps_sales_growth_pct_min: 35
    annual_eps_growth_pct_min: 25
    next_quarter_eps_growth_pct_min: 20
    next_year_eps_growth_pct_min: 20
  ratings:
    comp_rating_min: 95
    eps_rating_min: 95
    rs_rating_min: 95
  special_watch:
    triple_digit_eps_or_sales_growth: true
```

#### 6B.2. Watchlist Tiers

```yaml
watchlist_tiers:
  universal_list:
    description: "Emerging leaders, triple-digit sales/earnings, New America candidates; may not yet meet all filters."
  focus_list:
    description: "Meets core fundamentals; watch weekly/daily for setup."
  a_list:
    description: "Meets fundamental + technical setup; has trading plan. Ready to buy if trigger occurs."
```

#### 6B.3. Technical Setup

```yaml
technical_setup:
  weekly_first: true
  buy_execution_chart: "daily"
  preferred_base_context:
    - early_stage_base
    - stage_1_or_stage_2_reclaim
    - correction_recovery
    - retake_10w_or_50d
    - higher_lows_before_entry
  avoid:
    - extended_from_10w_or_50d
    - market_correction_without_turn
    - weak_fundamentals_even_if_chart_good
```

---

### Candidate C — 10-Week / 50-Day Technical Stop Position System v1

**Amaç:** Individual stock position trading’de sabit yüzde stop yerine teknik stop ve position sizing kullanmak.

```yaml
technical_stop_position_system_v1:
  initial_position_pct: 10
  buy_zone:
    max_distance_above_10w_or_50d_pct: 8
    preferred_distance_pct: [0, 5]
  stop_reference:
    - 10_week_ma
    - 50_day_ma
  stop_behavior:
    allow_orderly_undercut: true
    wait_until_week_end_if_profit_buffer: true
    immediate_exit_if:
      - severe_gap_down
      - knife_like_break
      - fundamental_thesis_broken
      - leadership_or_strategy_change
  add_rules:
    first_pullback_to_10w_or_50d_and_bounce: "add_10pct_of_position"
    first_3_weeks_tight: "add_10pct_of_position"
  target_number_of_individual_stocks: [6, 8]
  normal_initial_position_pct: 10
  grown_position_pct_range: [12.5, 15]
```

---

## 7. MTC_V2 / QuantLens İçin Uygunluk

### 7.1. En Uygun Katman

Bu transcriptin MTC_V2’deki en uygun karşılıkları:

- **PortfolioState / Regime Guard:** QQQ / NASDAQ market state, distribution day cluster, Stage 2 uptrend.
- **Position Manager:** TQQQ core vs swing exposure, partial trims, maintain-core logic.
- **Exit Rules:** Sell into strength cluster, loss of 10D on rising volume, weekly poor close below 10W.
- **Risk Manager:** Leveraged ETF gap risk, max exposure cap, cash buffer, account-type awareness.
- **Signal Producer:** TQQQ turn-up after pullback; 21D/50D reclaim; rally low hold.

### 7.2. MTC_V2 Crypto Adaptasyonu

TQQQ doğrudan crypto değildir. Ancak şu fikirler crypto trend sistemine aktarılabilir:

| Video Fikri | Crypto/MTC_V2 Uyarlaması |
|---|---|
| TQQQ = leveraged NASDAQ exposure | BTC/ETH beta exposure veya yüksek beta altcoin sepeti |
| QQQ Stage 2 guard | BTC/ETH trend regime guard |
| Distribution days | High-volume down days / market breadth proxy |
| Sell into strength after 20–30% swing | Crypto trend exhaustion / extension trim |
| 10D / 21D / 50D tracking | EMA/SMA distance extension filter |
| 52-week high / resistance rejection | N-bar high / all-time high / range high rejection |
| Maintain 25% core while Stage 2 persists | Core trend allocation + swing overlay |

### 7.3. Direkt Pine’a Alınmamalı

**Neden:**

- TQQQ stratejisinin leveraged ETF davranışı özel veri gerektirir.
- “Distribution day” ve “Bulls vs Bears” gibi bazı sinyaller external data ister.
- Fundamental watchlist modülü Pine içinde uygun değildir.
- İlk olarak Python’da clean feature extraction + walk-forward test yapılmalı.

---

## 8. Python Prototype Önerisi

### 8.1. Dosya Önerisi

```text
06_QUANTLENS_LAB/
  youtube_strategy_intake/
    candidates/
      YT_aDRYV4mjlHA_vibha_jha_tqqq/
        README.md
        source_transcript.md
        intake_report.md
        feature_contract_tqqq_swing_v1.yml
        feature_contract_tml_watchlist_v1.yml
        research_notes.md
        cases/
          tqqq_2011_2026_daily_cases.csv
        prototype/
          tqqq_swing_features.py
          tqqq_swing_backtest.py
          tqqq_swing_report.py
```

### 8.2. Feature Contract — TQQQ Swing v1

```yaml
contract_id: tqqq_swing_regime_v1
source_video_id: aDRYV4mjlHA
symbol: TQQQ
reference_symbol: QQQ
timeframe: 1D
features:
  price_ma:
    - sma_10
    - sma_21
    - sma_50
    - sma_200
    - sma_10w
  distance:
    - pct_from_sma_10
    - pct_from_sma_21
    - pct_from_sma_50
    - pct_from_sma_10w
  swing:
    - recent_swing_low
    - recent_swing_high
    - pct_from_recent_swing_low
    - pct_from_recent_swing_high
    - days_since_swing_low
    - days_since_swing_high
  volume:
    - volume_vs_50d_avg
    - rising_volume_down_day
    - declining_volume_new_high
  regime:
    - qqq_above_50d
    - qqq_above_200d
    - qqq_higher_high_higher_low
    - qqq_distribution_day_count_25d
  trigger:
    - rally_day_low_hold
    - reclaim_21d
    - reclaim_50d
    - new_52w_high
    - failed_resistance_3x
signals:
  long_entry:
    - turn_up_after_10pct_pullback
    - reclaim_21d_or_50d
    - qqq_regime_positive
  partial_exit:
    - new_52w_high_and_extension
    - new_high_declining_volume
    - distribution_cluster
    - loss_of_10d_rising_volume
  full_exit:
    - undercut_rally_day_low
    - qqq_regime_failure
    - poor_weekly_close_below_10w_rising_volume
```

### 8.3. Backtest Assumptions

```yaml
backtest_assumptions:
  data: "adjusted OHLCV required"
  slippage_bps: [2, 5, 10]
  commission_bps: [0, 1]
  position_sizing:
    entry_pct: [25, 50]
    max_pct: [50, 100]
    core_floor_pct: [0, 25]
  rebalance:
    partial_trim_pct: [10, 25, 50]
  tax_model:
    ignored_for_IRA_scenario: true
    taxable_scenario_optional: true
  leverage_decay_note: "Use real TQQQ adjusted data; do not synthesize 3x QQQ unless explicitly testing proxy." 
```

---

## 9. Test Edilecek Varyasyonlar

### Variant 1 — Conservative TQQQ Swing

```yaml
variant: conservative_tqqq_swing
entry:
  require_qqq_above_50d: true
  require_tqqq_reclaim_21d_or_50d: true
  pullback_from_recent_high_min_pct: 10
position:
  initial_pct: 25
  max_pct: 50
exit:
  trim_at_pct_from_swing_low: 20
  trim_if_exit_score_gte: 2
  full_exit_if_undercut_rally_low: true
```

### Variant 2 — Aggressive Early Turn

```yaml
variant: aggressive_early_turn
entry:
  allow_before_followthrough_day: true
  require_day_4_or_5_rally: true
  require_higher_low: true
position:
  initial_pct: 25
  add_on_reclaim_21d: 25
  max_pct: 100
exit:
  hard_exit_rally_low_undercut: true
  trim_at_20pct_swing_gain: true
```

### Variant 3 — Core + Swing Overlay

```yaml
variant: core_plus_swing_overlay
entry:
  core_entry_on_stage2_reclaim: true
  swing_entry_on_10pct_pullback_turn: true
position:
  core_floor_pct: 25
  swing_layer_pct: [25, 50]
exit:
  keep_core_if_stage2: true
  sell_swing_layer_on_exit_score_gte_2: true
  exit_all_on_stage2_failure: true
```

### Variant 4 — Individual TML Position Strategy

```yaml
variant: individual_tml_position
universe: "US equities with fundamentals"
entry:
  fundamental_filter: true
  buy_near_10w_or_50d: true
  max_distance_from_support_pct: 8
position:
  initial_pct: 10
  add_first_10w_bounce: true
  add_first_3_weeks_tight: true
exit:
  weekly_close_below_10w_bad_action: true
  fundamental_thesis_break: true
  severe_earnings_gap_down: true
```

---

## 10. QuantLens Scoring Önerisi

```yaml
candidate_scoring:
  codability: 8.5
  backtestability: 8.0
  novelty: 7.5
  robustness_potential: 7.0
  mtc_v2_fit: 6.5
  standalone_research_value: 9.0
  immediate_python_priority: 9.0
  immediate_pine_priority: 4.0
```

**Yorum:** TQQQ kısmı backtest edilebilir ve çok net. Individual stock/fundamental kısmı ise daha yüksek veri ihtiyacı nedeniyle scanner projesidir. MTC_V2’ye en güçlü katkı doğrudan producer değil, **regime guard + risk/position management + partial exit logic** olacaktır.

---

## 11. Riskler / Şüpheli veya Dikkat Gerektiren Noktalar

1. **TQQQ leveraged ETF risklidir.** Uzun süreli hold ve gap-down riski çok yüksek olabilir.
2. **Tax context stratejiyi etkiliyor.** Vibha özellikle IRA içinde TQQQ swing trading yaptığını belirtiyor. Taxable account davranışı farklı olabilir.
3. **Bulls vs Bears gibi sentiment sinyalleri external data ister.** İlk v1’de opsiyonel bırakılmalı.
4. **Bazı kararlar sezgisel/tecrübeye dayalı.** “Gut feel” kısımları doğrudan kodlanmamalı; ölçülebilir proxy bulunmalı.
5. **Fundamental data şart.** TML stock selection için reliable EPS/sales/RS data gerekir.
6. **TQQQ survivorship yok ama leveraged product history sınırlı.** Test başlangıç yılı TQQQ inception ile sınırlı olmalı.
7. **Adjusted OHLCV zorunlu.** Split/decay/ETF adjustment hatası sonucu tamamen bozabilir.
8. **Market cycle bağımlılığı yüksek.** 2023 gibi mega-cap driven NASDAQ döneminde iyi; 2022 gibi bear trendde yanlış sinyaller üretebilir.
9. **Position size agresif olabilir.** 50–100% TQQQ exposure çoğu portföy için uygun değildir; researchte conservative sizing varsayılan olmalı.

---

## 12. Trader Wiki Notu Önerisi

Bu video için ayrıca Trader Wiki notu oluşturulması faydalı olur.

```yaml
wiki_note:
  wiki_id: TW_2026-05-03_01_RISK_MANAGEMENT_vibha_jha_tqqq
  topic: "01_RISK_MANAGEMENT"
  secondary_topics:
    - "04_SYSTEM_DEVELOPMENT"
    - "05_BACKTESTING_AND_OPTIMIZATION"
    - "06_EXECUTION_AND_FEES"
  usefulness_score: 9
  tags:
    - TQQQ
    - CANSLIM
    - true-market-leader
    - technical-stop
    - 10-week-ma
    - 50-day-ma
    - swing-trading
    - sell-into-strength
    - distribution-days
    - leveraged-etf-risk
```

### Wiki Ana Dersler

- Sabit yüzde stop yerine chart yapısına uygun teknik stop kullanmak bazı trader stilleri için daha mantıklı olabilir.
- Daha uzun vadeli winner hold için girişin 10-week / 50-day gibi ana desteklere yakın olması önemli.
- Individual stock setup yokken zorla trade almak yerine, index/ETF exposure ile market momentumuna katılmak bir alternatif olabilir.
- TQQQ gibi leveraged araçlarda kârı koruma, normal stock position trading’den farklı yönetilmeli.
- Trading plan eksikse sistem eksiktir: ne alınır, ne zaman alınır, ne kadar alınır, ne zaman satılır.

---

## 13. Codex İçin Uygulama Planı

### Aşama 1 — Intake Kaydı

- `_registry/youtube_video_index.csv` kontrol et.
- `video_id = aDRYV4mjlHA` varsa duplicate raporu üret ve dur.
- `transcript_hash = bb8da7bc3981399723ff551422788907bc8852650f5f4d8c05c9def4fb738640` varsa possible duplicate olarak dur.
- Yoksa candidate folder oluştur.

### Aşama 2 — Feature Contract

- `feature_contract_tqqq_swing_v1.yml` oluştur.
- Fundamental stock scanner contract ayrı dosyada tutulmalı.
- TQQQ contract, pure OHLCV + QQQ reference ile çalışabilmeli.

### Aşama 3 — Python Prototype

- `tqqq_swing_features.py`: MA, distance, swing high/low, distribution count, volume patterns.
- `tqqq_swing_signals.py`: entry/exit score.
- `tqqq_swing_backtest.py`: partial trim + core floor engine.
- `tqqq_swing_report.py`: CAGR, max DD, exposure time, average trade, worst trade, years contribution.

### Aşama 4 — Robustness

- Walk-forward by year.
- Bear / bull / sideways regime split.
- Slippage and gap stress.
- Entry lag test: next open vs close.
- Exit lag test: same close vs next open.
- Core floor sensitivity: 0%, 25%, 50%.

### Aşama 5 — MTC_V2 Integration Kararı

Sadece şu durumlarda MTC_V2’ye taşınmalı:

- TQQQ/QQQ prototype multi-year robust sonuç verirse.
- Exit cluster logic farklı assetlerde de çalışırsa.
- Regime guard, existing MTC_V2 PortfolioState / Entry Gates yapısıyla uyumluysa.
- Pine tarafında external fundamental/sentiment data gerektirmeyen sade versiyon çıkarılabiliyorsa.

---

## 14. Final Karar

```yaml
final_decision:
  classification: CANDIDATE
  codex_status: READY_FOR_PYTHON_PROTOTYPE
  priority: VERY_HIGH
  first_research_module: TQQQ_Swing_Regime_v1
  second_research_module: Technical_Stop_Position_System_v1
  third_research_module: True_Market_Leader_Watchlist_v1
  pine_now: false
  python_now: true
  wiki_note: true
```

**Next Action:** Codex, bu transcripti önce `TQQQ_Swing_Regime_v1` olarak Python’da prototiplemeli. Individual true market leader / CANSLIM tarafı ayrı equity scanner işidir. MTC_V2 core dosyalarına ve production runner’a dokunulmamalıdır.

---

## 15. Dokunulmaması Gerekenler

Bu intake raporu kapsamında aşağıdakilere dokunulmadı ve Codex de bu aşamada dokunmamalı:

- `01_PINE/MTC_V2.pine`
- Production Python runner dosyaları
- Mevcut workflow dosyaları
- Büyük CSV / data bundle / optimization result dosyaları
- API key, webhook, broker/exchange secret dosyaları

---

## 16. Oluşturulacak Repo Kayıtları İçin Öneri

```csv
video_id,normalized_url,title,channel,status,candidate_id,transcript_hash,first_seen_at,last_seen_at,process_count
"aDRYV4mjlHA","https://www.youtube.com/watch?v=aDRYV4mjlHA","The Million Dollar TQQQ Swing Trading Strategy Vibha Jha","UNKNOWN_CHANNEL","CANDIDATE","YT_aDRYV4mjlHA_20260503_A","bb8da7bc3981399723ff551422788907bc8852650f5f4d8c05c9def4fb738640","2026-05-03","2026-05-03",1
```

```csv
channel,status,total_processed,candidate_count,wiki_count,reject_count,stop_count,last_video_id,last_decision
"UNKNOWN_CHANNEL","UNKNOWN",1,1,1,0,0,"aDRYV4mjlHA","CANDIDATE"
```
