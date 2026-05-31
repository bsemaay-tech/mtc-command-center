# QUANTLENS TRANSCRIPT INTAKE REPORT — VCP Breakout / Volatility Contraction Pattern

**Generated:** 2026-05-03  
**Source URL:** https://youtu.be/Tm0dkf8_giA?si=KeJv1-D-_CbJU-FK  
**Normalized URL:** https://www.youtube.com/watch?v=Tm0dkf8_giA  
**Video ID:** `Tm0dkf8_giA`  
**Input Transcript File:** `+50% in 20 Days - How to Trade Breakouts with The Volatility Contraction Pattern (VCP.md`  
**Intake Prompt File:** `00_quantlens_transcript_intake_prompt.md`  
**Transcript Status:** Provided by user as markdown transcript  
**Title:** +50% in 20 Days - How to Trade Breakouts with The Volatility Contraction Pattern (VCP)  
**Channel:** `UNKNOWN_CHANNEL`  
**Speaker / Host Mentioned:** Richard from “Trailline/TraderLion” as spoken in transcript  
**Transcript Digest SHA256:** `6e17a0534f2ae36cc341c7f3dc6cb5e3de04bb9becb606a812a19a2a35ff5de4`

---

## 1. Executive Verdict

```yaml
classification: CANDIDATE
codex_status: READY_FOR_PYTHON_PROTOTYPE
quantlens_priority: MEDIUM_HIGH
production_ready: false
pine_ready: false
python_backtest_ready: yes
strategy_family:
  - breakout
  - volatility_contraction_pattern
  - momentum_continuation
  - trend_following
  - relative_strength_base_breakout
primary_direction: long
primary_timeframe: daily
secondary_timeframes:
  - weekly_context
  - intraday_volume_confirmation_optional
```

Bu video **kodlanabilir bir strateji adayı** içeriyor. Ana fikir; güçlü trend sonrası oluşan fiyat bazında volatilitenin soldan sağa sıkışması, son kontraksiyonun daralması, pivot üstü hacimli kırılım ve hızlı kâr / küçük zarar mantığıdır.

Ancak bu aday **doğrudan MTC producer’a alınmamalı**. Önce Python-only araştırma modülü olarak test edilmeli. Sebep: VCP görsel/yorum ağırlıklı bir formasyon olduğu için mekanik tanım iyi yapılmazsa aşırı subjektif, geçmişe uyumlu ve düşük tekrar üretilebilir olur.

---

## 2. Duplicate / Registry Kontrolü

```yaml
duplicate_check_mode: standalone_uploaded_file_only
repo_registry_checked: false
video_index_checked: false
channel_blacklist_checked: false
channel_quality_registry_checked: false
exact_video_id_duplicate_found_in_uploaded_context: false
status: NOT_DUPLICATE_WITHIN_AVAILABLE_CONTEXT
```

Not: Bu ChatGPT oturumunda repo içindeki `_registry/youtube_video_index.csv`, `channel_blacklist.yaml` ve `channel_quality_registry.csv` dosyalarına erişim yok. Bu nedenle resmi duplicate/blacklist kararı Codex’in repo içinde çalıştıracağı intake workflow tarafından tekrar doğrulanmalı.

---

## 3. Channel Quality Kararı

```yaml
channel: UNKNOWN_CHANNEL
quality_state: UNKNOWN
blacklist_action: none
reason: channel metadata not provided; prompt rule says use UNKNOWN_CHANNEL when channel info is missing
```

Bu video tek başına blacklist gerekçesi oluşturmaz. İçerik düşük kalite veya bariz pazarlama ağırlıklı değil; teknik olarak anlamlı, klasik momentum / Minervini tarzı VCP eğitimidir.

---

## 4. Strateji Özeti

VCP, güçlü önceki trendden sonra oluşan baz içinde fiyat oynaklığının daralmasıdır. Video; VCP’yi arz-talep dengesi, kurumların birikimi, zayıf ellerin silkelenmesi ve pivot kırılımı üzerinden anlatıyor.

```yaml
core_idea:
  - strong_prior_uptrend
  - price_base_forms_under_resistance
  - contractions_get_smaller_left_to_right
  - volume_dries_up_during_pullbacks
  - final_contraction_is_tight
  - breakout_through_pivot_on_high_volume
  - stop_below_base_low_or_last_contraction_low
  - move_stop_to_breakeven_after_quick_profit
```

Ana mesaj:

> İyi VCP kırılımı programına göre çalışmalı: ya hızlıca kâra geçer ya da küçük zararla çıkılır.

---

## 5. Kodlanabilir Candidate

```yaml
candidate_id: QL_VCP_BREAKOUT_DAILY_BASE_001
candidate_name: Daily VCP Breakout With Volume Expansion
candidate_type: signal_producer_research
candidate_scope: python_only_first
mtc_direct_integration: false
```

### 5.1 Market / Asset Uygunluğu

```yaml
best_fit:
  - US momentum stocks
  - high_relative_strength_equities
  - liquid high_beta equities
possible_crypto_proxy:
  - BTCUSDT
  - ETHUSDT
  - SOLUSDT
  - BNBUSDT
  - XRPUSDT
crypto_transferability: medium
```

Crypto’da VCP mantığı test edilebilir ama video esasen hisse senedi momentumuna dayanıyor. Crypto proxy testte hacim ve relative strength kavramları yeniden tanımlanmalı.

---

## 6. Mekanik Kurallar v0

### 6.1 Ön Trend Filtresi

Amaç: VCP’yi zayıf, yatay veya düşen varlıklarda değil; güçlü trendin mola verdiği yapılarda aramak.

```yaml
prior_trend_filter:
  required:
    - close > ema_50
    - ema_20 > ema_50
    - close is in upper half of last 120d range
  optional:
    - close > ema_150
    - relative_strength_vs_market > 0 over lookback
    - prior_60d_return > threshold
```

Önerilen ilk parametreler:

```yaml
prior_trend_params:
  ema_fast: 20
  ema_mid: 50
  ema_long: 150
  range_lookback: 120
  min_prior_60d_return:
    conservative: 20%
    aggressive: 35%
```

---

### 6.2 Base Detection

VCP bazını mekanik yakalamak için rolling high/low ve daralan swing aralıkları kullanılmalı.

```yaml
base_detection:
  base_lookback_days:
    min: 15
    max: 80
  base_depth_max:
    default: 35%
    strict: 25%
  base_position:
    close_in_upper_third_of_base: preferred
  pivot:
    highest_high_last_N_days_or_local_resistance
```

Video özellikle pivotun önceki high, aylık high, haftalık high veya tüm zamanların zirvesi gibi karar noktası olabileceğini vurguluyor. Mekanik v0’da pivot şu şekilde tanımlanabilir:

```yaml
pivot_v0:
  pivot_price = rolling_high(base_lookback)
  breakout_condition = close > pivot_price_previous_day
```

---

### 6.3 Volatility Contraction Logic

Video en az iki kontraksiyon, soldan sağa sıkışma ve son kontraksiyonun idealde %10’dan küçük olmasını anlatıyor.

```yaml
contraction_logic_v0:
  contraction_count_min: 2
  swing_method:
    - local_high_low_zigzag
    - or rolling_pullback_depth_sequence
  required:
    - contraction_2_depth < contraction_1_depth
  preferred:
    - contraction_3_depth < contraction_2_depth
  final_contraction_max_depth:
    strict: 10%
    loose: 15%
```

Daha basit ilk prototip:

```yaml
simple_vcp_proxy:
  - rolling_20d_atr_pct < rolling_60d_atr_pct
  - last_10d_high_low_range < prior_20d_high_low_range
  - last_5d_range <= 0.6 * prior_20d_range
  - close_near_pivot: close >= pivot * 0.95
```

Bu basit proxy, görsel VCP’yi tam yakalamaz ama ilk Python araştırması için daha deterministik ve hızlıdır.

---

### 6.4 Volume Confirmation

Video; pullbacklerde hacim kuruması, pivot kırılımında ise yüksek hacim / volume buzz beklenmesini söylüyor.

```yaml
volume_filters:
  dry_up_before_breakout:
    - avg_volume_last_5d < avg_volume_last_20d
    - or down_day_volume_declining
  breakout_volume:
    - volume_today > avg_volume_20d * 1.5
    - strict: volume_today > avg_volume_50d * 2.0
```

Intraday volume buzz crypto veya 5m data ile test edilecekse:

```yaml
intraday_volume_buzz_optional:
  first_30m_volume_runrate > daily_avg_volume_20d * expected_fraction_threshold
```

---

## 7. Entry / Exit / Risk Rules

### 7.1 Entry

```yaml
entry_v0:
  trigger: daily_close_breakout
  condition:
    - close > prior_pivot
    - volume_confirmed
    - prior_vcp_proxy_valid
```

Alternatif daha erken / daha gerçekçi execution:

```yaml
entry_v1_intraday:
  trigger: price_crosses_pivot_intraday
  confirmation:
    - volume_runrate_above_average
    - price_holds_above_pivot_after_breakout
  data_required:
    - 5m or 15m OHLCV
```

İlk test için `daily_close_breakout` daha temizdir. Intraday pivot cross ikinci aşamaya bırakılmalı.

---

### 7.2 Stop Loss

Video iki pratik stop verir: son konsolidasyonun low’u veya daha sıkı yaklaşımda günün low’u.

```yaml
stop_loss_options:
  option_a_last_contraction_low:
    stop = low_of_final_contraction
  option_b_breakout_day_low:
    stop = breakout_day_low
  option_c_atr_safety:
    stop = entry - atr_14 * multiplier
```

MTC tarafında bu stop mantığı `SL = Swing Low + ATR buffer` veya `Initial SL = final contraction low` şeklinde producer metadata’sı olarak taşınabilir.

---

### 7.3 Take Profit / Trade Management

Video sabit TP sisteminden çok, hızlı kâra geçince stop’u break-even’a çekmeyi ve devamında kâr korumayı anlatıyor.

```yaml
management_v0:
  breakeven_trigger:
    - unrealized_gain >= 5%
    - or unrealized_R >= 1.0R
  protective_action:
    - move_stop_to_entry
  trailing_options:
    - ema_10_or_ema_20_trail
    - atr_trailing_stop
    - close_below_10sma_or_20ema
```

İlk araştırma exit varyantları:

```yaml
exit_variants:
  - close_below_10sma
  - close_below_20ema
  - fixed_2R
  - fixed_3R
  - breakeven_then_20ema_trail
  - time_stop_20_bars_if_no_1R
```

---

## 8. MTC_V2 ile Bağlantı

Bu strateji MTC_V2 içinde doğrudan bütün sistemi değiştirmeden bir **signal producer** veya **setup gate** olarak araştırılmalı.

```yaml
mtc_mapping:
  signal_producer:
    name: producer_vcp_breakout_v0
    output:
      - long_pulse_on_breakout
      - setup_quality_score
      - pivot_price
      - final_contraction_low
      - suggested_initial_sl
  gates:
    useful_existing_gates:
      - MA trend gate
      - MA slope gate
      - HTF trend gate
      - Volume gate
      - ATR volatility floor
      - Level proximity gate
      - Daily extension anti-chase gate
  position_manager:
    use_existing:
      - cooldown_bars
      - max_entries
      - allow_flip=false_for_this_producer
  exits:
    use_existing:
      - initial SL
      - breakeven
      - trailing
      - time stop
```

Önemli: VCP entry tek başına yeterli olmayabilir. MTC’nin mevcut SL/TP, BE, trailing ve filtre katmanları özellikle bu strateji için değerlidir.

---

## 9. Research Plan — Python Only First

```yaml
stage_1_goal: verify whether deterministic VCP proxy has positive expectancy
no_pine: true
no_mtc_modification: true
no_live_trading: true
```

### 9.1 Test Edilecek Assetler

İlk minimum set:

```yaml
crypto_proxy_5_assets:
  - BTCUSDT
  - ETHUSDT
  - SOLUSDT
  - BNBUSDT
  - XRPUSDT
```

Hisse senedi için daha uygun set:

```yaml
us_equity_preferred:
  - high_beta_growth
  - CANSLIM-style leaders
  - high_ADR_liquid_names
  - historical examples: PLTR, NIO, TSM, SPT, SHOP
```

### 9.2 Zaman Dilimi

```yaml
timeframes:
  primary: 1D
  optional_execution: 5m or 15m
history:
  crypto: 2021-01-01 to latest_available
  equities: at_least_2018_to_latest_available
```

### 9.3 Parametre Grid

```yaml
parameter_grid_v0:
  base_lookback: [20, 40, 60, 80]
  base_depth_max: [0.25, 0.35, 0.45]
  final_contraction_max: [0.08, 0.10, 0.15]
  atr_contraction_ratio_max: [0.60, 0.75, 0.90]
  breakout_volume_mult: [1.2, 1.5, 2.0]
  stop_type:
    - final_contraction_low
    - breakout_day_low
    - atr_2x
  exit_type:
    - close_below_10sma
    - close_below_20ema
    - fixed_2R
    - fixed_3R
    - breakeven_then_20ema_trail
```

---

## 10. Beklenen Edge ve Zayıf Noktalar

### Artılar

- Mantık piyasa yapısına dayanıyor: trend + sıkışma + hacimli kırılım.
- Stop seviyesi doğal olarak tanımlanabiliyor.
- MTC’nin mevcut risk yönetimiyle uyumlu.
- Crypto proxy ve hisse senedi momentum evreninde test edilebilir.
- VCP / CANSLIM / Minervini tarzı sistemler uzun vadeli literatür ve trader pratiğinde bilinen bir çerçeveye sahip.

### Zayıflıklar

- Görsel formasyon mekanik hale getirilirken aşırı uyarlama riski yüksek.
- Basit EMA/volume breakout baseline ile karşılaştırılmazsa edge abartılabilir.
- Hisse stratejisi crypto’ya doğrudan taşınırsa sonuç yanıltıcı olabilir.
- Volume confirmation crypto perpetual piyasasında hisse senedi volume yorumuyla birebir aynı değildir.
- Pivot tanımı geçmişe bakarak “en iyi görünen high” seçilirse lookahead bias doğar.

---

## 11. Baseline Karşılaştırmaları

Bu aday tek başına test edilmemeli; aşağıdaki baseline’larla kıyaslanmalı.

```yaml
required_baselines:
  - simple_20_50_ema_trend_breakout
  - donchian_20d_breakout
  - donchian_55d_breakout
  - close_above_20d_high_with_volume
  - CANSLIM_style_breakout_baseline
  - random_entry_same_trade_count_baseline
```

VCP adayı ancak bu baseline’lara karşı anlamlı fark yaratırsa Stage 2’ye geçmeli.

---

## 12. Sınıflandırma

```yaml
classification: CANDIDATE
codex_status: READY_FOR_PYTHON_PROTOTYPE
candidate_registry_action: add_as_research_candidate_after_repo_duplicate_check
trader_wiki_action: optional_secondary_note_under_market_structure
next_action: python_only_backtest_module
```

Karar:

> Bu video CANDIDATE. Fakat “klasik VCP eğitimi” olduğu için yüksek kalitede olsa da tek başına yeni/özgün edge varsayılmamalı. En doğru adım; Python’da deterministik VCP proxy üretmek, baseline breakout sistemleriyle kıyaslamak ve ancak sonra MTC producer/gate kararına gitmektir.

---

## 13. Codex İçin Net Sonraki İş

```text
Repo içinde önce duplicate ve channel registry kontrolünü yap.
Eğer video daha önce işlenmemişse QL_VCP_BREAKOUT_DAILY_BASE_001 candidate kaydını oluştur.
MTC_V2.pine ve production runner dosyalarına dokunma.
Backtest çalıştırılacaksa ayrı research klasörü aç:
06_QUANTLENS_LAB/research/vcp_breakout_daily_base_YYYY_MM_DD/
İlk aşamada sadece Python-only prototype yaz.
En az 5 assette test et.
VCP proxy performansını Donchian breakout, EMA breakout ve volume breakout baseline ile karşılaştır.
Lookahead bias, volume bias, delisted equity bias ve transaction cost etkisini raporla.
Pine veya MTC entegrasyonuna geçme; sadece rapor üret.
```

---

## 14. Dokunulmaması Gerekenler

```yaml
not_touched:
  - 01_PINE/MTC_V2.pine
  - production_python_runner
  - live_trading_alerts
  - broker_or_exchange_keys
  - existing_backtest_outputs
  - optimization_bundles
```

---

## 15. Final Intake Decision

```yaml
final_decision: KEEP_AS_CANDIDATE
reason: codable VCP breakout setup with explicit trend, contraction, pivot, volume and stop concepts
priority: MEDIUM_HIGH
first_research_action: deterministic_python_proxy_with_baseline_comparison
pine_stage: wait_until_python_results
```
