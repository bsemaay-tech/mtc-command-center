# QuantLens Transcript Intake Report — Trade Like a Professional / Charles Harris

## 1. Intake Kararı

- **Final Classification:** `CANDIDATE`
- **Codex Status Önerisi:** `READY_FOR_PYTHON_PROTOTYPE`
- **Wiki Notu Önerisi:** `YES — 04_SYSTEM_DEVELOPMENT`, ayrıca `01_RISK_MANAGEMENT` ve `03_MARKET_STRUCTURE`
- **Öncelik:** `VERY_HIGH`
- **Güven:** `0.93`
- **Karar Özeti:** Bu transcript doğrudan kodlanabilir bir trade setup anlatıyor. Ana çekirdek **pullback üzerinde upside reversal ile giriş**, **pivot breakout ile güç alımı**, **21 günlük hareketli ortalamaya dönüşlerde ekleme**, **riskin reversal bar low / breakout day low ile tanımlanması** ve **50DMA ağır hacimli kırılımda pozisyon boşaltma**. MTC_V2 için entry producer + transform + exit/position-management prototipi üretmeye uygundur. Pine’a hemen taşınmamalı; önce Python tarafında OHLCV deterministic prototip ve parameter sweep yapılmalıdır.

---

## 2. Metadata

- **Candidate ID:** `YT_CtioOmc1Eig_20260503_A`
- **Source URL:** `https://youtu.be/CtioOmc1Eig?si=ISO4HKuamRbbh4ns`
- **Normalized URL:** `https://www.youtube.com/watch?v=CtioOmc1Eig`
- **Video ID:** `CtioOmc1Eig`
- **Title:** `Trade Like a Professional — Simple and Effective Trading Strategy with Charles Harris`
- **Channel:** `UNKNOWN_CHANNEL`
- **Speaker / Main Trader:** `Charles Harris`
- **Transcript File:** `Trade Like a Professional Simple and Effective Trading Strategy with Charles Harris.md`
- **Transcript SHA256:** `2931633c76574f95cd451271f0e820f66dc2c79fa71c9162a508e54b30322001`
- **Report Date:** `2026-05-03`
- **Language:** English transcript; Turkish intake report
- **Detected Market Type:** US equities, growth stocks, CANSLIM / O'Neill style, swing trading
- **Primary Timeframes:** Daily chart; optional intraday low handling for breakout/reversal day; 21DMA / 50DMA / 200DMA context
- **Core Concepts Mentioned:** buying strength, cup-with-handle pivot, rising RS line, pullback buying, upside reversal, base right side, 21-day moving average support, 50-day moving average exit, pyramiding, lower cost basis, support / resistance, heavy-volume breakdown

---

## 3. Duplicate / Registry Kontrolü

### Conversation İçi Kontrol

Bu conversation içinde daha önce işlenen video ID’leri:

- `lTiR1pc82EE`
- `QzzKqmPcB3A`
- `R1sNTB2Vh7w`
- `lS9zbnLi1Gg`
- `jLioqyVlRkE`
- `aDRYV4mjlHA`
- `2f5VfmlU90U`

Bu transcript video ID:

- `CtioOmc1Eig`

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
- **Bu video kanal kalitesine etkisi:** Çok pozitif. İçerik net kurallı, kodlanabilir, risk tanımlı ve örneklerle desteklenmiş. Kanal tespit edilirse kalite registry’ye `CANDIDATE` pozitif katkı olarak yazılabilir.

---

## 5. İçerik Özeti

Charles Harris, profesyonel trade timing için iki ana hedef tanımlıyor:

1. Trade’in kazanma ihtimalini artırmak.
2. Yanlış çıkarsa zararı açık şekilde tanımlamak.

Klasik yaklaşım olan **buying strength**; stock’un resistance/pivot üstüne çıkması, yeni zirveye gitmesi, rising RS line ve artan volume ile alınmasıdır. Bu güçlü bull marketlerde çalışır; fakat dezavantajı cost basis’in yüksek olması ve herkesin aynı obvious breakout noktasında alım yapmasıdır.

Alternatif yaklaşım **buying pullbacks** olarak anlatılır. Burada amaç stock’u daha düşük cost basis ile, support bölgesinde zayıf eller satarken almak ve riski net bir seviyeye bağlamaktır. Harris özellikle **upside reversal** beklemeyi şart koşar. Çünkü reversal bar hem supporting action hem de weak-holder shakeout sinyali olarak yorumlanır.

Transcriptte SWKS ve LULU örnekleri üzerinden şu yapı anlatılır:

- Stock base’in sağ tarafında yükselirken multi-day pullback yapar.
- Pullback bir upside reversal ile biter.
- Entry reversal gününde alınabilir.
- Stop/reversal low, line in the sand olur.
- Sonra stock pivot breakout yaparsa position’a ekleme yapılır.
- Sonraki consolidation içinde 21DMA çevresinde yeni upside reversal’lar ekleme fırsatı olabilir.
- Sonunda heavy-volume 50DMA break veya belirgin dağıtım sinyalleri gelirse pozisyon unwind edilir.

Bu yapı MTC_V2’de hem producer hem de transform/position-management adayıdır.

---

## 6. Kodlanabilir Strateji / Sistem Çekirdekleri

---

### Candidate A — Upside Reversal Pullback Entry Producer v1

**Amaç:** Breakout öncesi veya breakout sonrası pullback sonundaki destekleyici reversal bar ile düşük riskli entry üretmek.

#### 6A.1. Setup Context

```yaml
upside_reversal_pullback_v1:
  market: "US equities / growth stocks"
  timeframe: "1D"
  direction: "long_only"
  context:
    price_building_right_side_of_base: true
    or_after_prior_breakout: true
    pullback_len_min: 2
    pullback_len_max: 7
    preferred_volume_on_reversal: "above prior day or above recent average"
    support_optional_pre_breakout: true
    support_preferred_post_breakout:
      - "21DMA"
      - "prior resistance / pivot retest"
      - "50DMA for deeper pullback"
```

#### 6A.2. Candidate Bar Definition

Bir upside reversal bar için ilk deterministic tanım:

```text
pullback_active =
    close[1] < close[2]
    OR recent_n_bar_lower_closes >= min_pullback_len

upside_reversal =
    low < low[1]
    AND close > close[1]
    AND close > open
    AND close_range >= 0.60

volume_confirmation =
    volume > volume[1]
    OR volume > SMA(volume, 20) * volume_mult
```

Daha katı alternatif:

```text
upside_reversal_strict =
    low < low[1]
    AND close > high[1]
    AND close_range >= 0.70
    AND volume > SMA(volume, 20)
```

#### 6A.3. Entry Logic

```text
long_signal =
    base_or_uptrend_context
    AND pullback_active
    AND upside_reversal
    AND optional_volume_confirmation
```

#### 6A.4. Stop Logic

```text
initial_stop = low_of_upside_reversal_bar - tick_buffer
```

Opsiyonel stop handling:

```yaml
stop_execution_modes:
  immediate_intraday_break:
    description: "Reversal low kırılırsa aynı gün stop."
  end_of_day_confirmation:
    description: "Harris kişisel olarak çoğu zaman gün sonuna yakın bekleyebildiğini söylüyor; bu daha discretionary olduğu için Python'da ayrı mod olmalı."
```

#### 6A.5. MTC_V2 Mapping

- **Layer:** `SIGNAL PRODUCER`
- **Producer output:** `raw_long_pulse`
- **Required gates:** trend context, volume context, market regime
- **Exit integration:** initial stop in `POSITION SIZING` and `EXIT RULES`
- **Reason Codes:**
  - `ENTRY_UPSIDE_REVERSAL_PULLBACK`
  - `NO_ENTRY_PULLBACK_NOT_CONFIRMED`
  - `NO_ENTRY_REVERSAL_VOLUME_WEAK`
  - `STOP_REVERSAL_LOW_BROKEN`

---

### Candidate B — Pivot Breakout Strength Entry Producer v1

**Amaç:** Klasik cup-with-handle / resistance breakout entry’yi baseline olarak kodlamak.

#### 6B.1. Setup

```yaml
pivot_breakout_strength_v1:
  direction: long_only
  required:
    resistance_line_defined: true
    close_or_high_breaks_pivot: true
    volume_increase: true
    rs_line_rising: preferred
    price_near_new_highs: preferred
```

#### 6B.2. Entry Logic

```text
pivot_breakout =
    high > pivot_high
    AND close > pivot_high * breakout_close_buffer
    AND volume > SMA(volume, 50) * volume_mult
```

Varsayılan ilk prototip:

```yaml
params:
  pivot_lookback: 20
  min_base_len: 15
  max_base_depth_pct: 35
  volume_mult: 1.20
  close_above_pivot_required: false
```

#### 6B.3. Stop Logic

```text
initial_stop =
    breakout_day_low
    OR pivot_high * (1 - max_stop_pct)
```

#### 6B.4. MTC_V2 Mapping

- **Layer:** `SIGNAL PRODUCER`
- **Relationship to Candidate A:** Baseline / comparison producer
- **Research Role:** Pullback entry’nin breakout entry’ye göre cost basis ve R multiple avantajını ölçmek.

---

### Candidate C — 21DMA Pullback Add / Pyramid Module v1

**Amaç:** Çalışan pozisyona, stock 21DMA çevresinde kontrollü pullback + upside reversal verdiğinde ekleme yapmak.

#### 6C.1. Context

```yaml
pyramid_21dma_pullback_v1:
  requires_existing_long: true
  trend_context:
    close_above_50dma: true
    ma21_rising: true
    ma50_rising: preferred
  pullback_support:
    price_touches_or_undercuts_21dma: true
    then_upside_reversal: true
```

#### 6C.2. Add Logic

```text
can_add =
    position_is_profitable
    AND add_count < max_adds
    AND close > ma21
    AND low <= ma21 * (1 + support_tolerance_pct)
    AND upside_reversal
```

#### 6C.3. Add Risk Control

```yaml
risk_controls:
  max_total_position_risk_pct: configurable
  max_adds: 2 or 3
  add_size_mode:
    - fixed_fraction_of_initial
    - risk_equalized_to_new_stop
  stop_for_add_leg: "upside_reversal_bar_low"
```

#### 6C.4. MTC_V2 Mapping

- **Layer:** `POSITION MANAGER` / `POSITION SIZING`
- **Needs:** existing long state, add count, blended risk, max entries
- **Potential conflict:** MTC_V2 `max_entries` / pyramiding must own permission.
- **Reason Codes:**
  - `ADD_21DMA_PULLBACK_REVERSAL`
  - `NO_ADD_MAX_ENTRIES`
  - `NO_ADD_TOTAL_RISK_CAP`
  - `NO_ADD_PRICE_NOT_AT_SUPPORT`

---

### Candidate D — Resistance Break Add / Pyramid Module v1

**Amaç:** Position zaten çalışıyorsa, kısa consolidation resistance üstü kırılımlarında ekleme yapmak.

#### 6D.1. Logic

```text
short_resistance_break =
    existing_long
    AND consolidation_len between 3 and 20
    AND high > recent_resistance
    AND volume_confirms
```

#### 6D.2. Use Case

Harris, SWKS/LULU örneklerinde hem pullback reversal’larda hem de resistance breakout’larda ekleme yaptığını anlatır. Bu iki add mantığı birlikte test edilmeli.

#### 6D.3. Research Note

Bu modül tek başına producer değil; ana alpha, iyi stock + iyi market + iyi base context içindedir. Bu nedenle random assets üzerinde test edilirse edge görünmeyebilir.

---

### Candidate E — Heavy Volume 50DMA Break Exit v1

**Amaç:** Uptrend bitişinde pozisyonu azaltmak / kapatmak.

#### 6E.1. Exit Conditions

```text
exit_warning =
    close < ma50
    AND volume > SMA(volume, 50) * 1.20

exit_decisive =
    close < ma50
    AND close < ma50 * (1 - break_buffer_pct)
    AND volume > SMA(volume, 50) * 1.50
```

Ek ominous sell signals:

```yaml
sell_signals:
  - heavy_volume_down_day
  - decisive_50dma_break
  - multiple_one_day_large_losses
  - failed_breakout_after_pivot
  - repeated shakeout without recovery
```

#### 6E.2. MTC_V2 Mapping

- **Layer:** `EXIT RULES`
- **Priority:** Protective price exits sonrası, discretionary structural exit öncesi test edilmeli.
- **Reason Codes:**
  - `EXIT_HEAVY_VOLUME_50DMA_BREAK`
  - `EXIT_DISTRIBUTION_CLUSTER`
  - `EXIT_FAILED_PIVOT_BREAKOUT`

---

## 7. Strategy Blueprint — İlk Python Prototip

```yaml
strategy_name: "CH_UpRev_Pullback_Pyramid_v1"
universe:
  initial: "high liquidity US equities / QQQ constituents / growth watchlist"
  later: "crypto adaptation only after equity validation"
timeframe: "1D"
long_only: true

entries:
  primary:
    - upside_reversal_pullback
  secondary:
    - pivot_breakout_strength

adds:
  - 21dma_pullback_upside_reversal
  - short_resistance_break

initial_stop:
  - reversal_bar_low
  - breakout_day_low

exits:
  - stop_loss
  - heavy_volume_50dma_break
  - optional_21dma_fail_for_fast_mode
  - optional_time_stop_if_no_followthrough

filters:
  - market_regime_guard
  - volume_confirmation
  - trend_context
  - relative_strength_proxy_optional

position_sizing:
  mode: risk_based
  max_initial_risk_pct: 0.25_to_1.00
  max_total_risk_pct: configurable
  max_entries: 3
```

---

## 8. MTC_V2 ile Entegrasyon Planı

### 8.1. Uygun Katmanlar

| MTC_V2 Katmanı | Bu videodan gelen modül |
|---|---|
| Signal Producer | Upside Reversal Pullback, Pivot Breakout |
| Signal Transform | Pullback confirmation / base context validation |
| Entry Gates | Market regime, volume, trend, RS proxy |
| Position Manager | Pyramiding / add permission |
| Position Sizing | Reversal-low stop distance ile risk-based sizing |
| Exit Rules | 50DMA heavy-volume break, initial stop, failed breakout |
| Visualization | Raw reversal marker vs actual entry marker ayrımı |

### 8.2. Anti-Repaint / Parity Notları

- Entry sinyalleri bar kapanışında doğrulanmalı.
- Intraday low stop seviyesi OHLC deterministic şekilde kullanılmalı.
- Eğer “end-of-day stop confirmation” modu test edilecekse Pine ve Python’da aynı davranış açıkça tanımlanmalı.
- 21DMA / 50DMA hesapları warmup ve seeding açısından Python/Pine parity testine alınmalı.
- Volume SMA seeding farkları toleranslı test edilmeli.

---

## 9. Backtest / Research Planı

### Phase 1 — Baseline

1. Pivot Breakout producer tek başına test edilir.
2. Upside Reversal Pullback producer tek başına test edilir.
3. Aynı universe/timeframe üzerinde entry price, stop distance, R multiple ve win-rate karşılaştırılır.

### Phase 2 — Context Filters

Test varyasyonları:

```yaml
filters_to_test:
  - no_filter
  - close_above_50dma
  - close_above_21dma_and_50dma
  - ma50_rising
  - ma21_rising_and_ma50_rising
  - volume_confirmation
  - QQQ_market_regime_guard
```

### Phase 3 — Pyramiding

```yaml
pyramid_variants:
  - no_pyramid
  - add_on_21dma_reversal_only
  - add_on_resistance_break_only
  - both_add_modes
```

### Phase 4 — Exit Variants

```yaml
exit_variants:
  - initial_stop_only
  - initial_stop_plus_50dma_break
  - initial_stop_plus_21dma_fast_exit
  - initial_stop_plus_distribution_cluster
```

### Phase 5 — Robustness

- Bull market subset
- Choppy market subset
- Bear market subset
- High RS universe vs broad universe
- Liquidity buckets
- Earnings gap stocks ayrı subset
- Walk-forward validation

---

## 10. Parametre Başlangıç Önerileri

```yaml
params_initial:
  pullback_len_min: 2
  pullback_len_max: 7
  reversal_close_range_min: 0.60
  reversal_requires_close_above_prev_close: true
  reversal_requires_low_below_prev_low: true
  volume_sma_len: 20
  volume_mult_reversal: 1.00
  volume_mult_breakout: 1.20
  ma_fast_len: 21
  ma_mid_len: 50
  ma_long_len: 200
  support_tolerance_pct: 1.50
  max_stop_pct: 8.00
  break_buffer_50dma_pct: 1.00
  heavy_volume_mult: 1.50
  max_entries: 3
```

---

## 11. Reject / Caution Bulguları

Bu video güçlü bir candidate olsa da şu riskler var:

1. **Chart context discretionary.** Base right side, proper handle, constructive support gibi kavramlar doğrudan kodlanırken hatalı sadeleşebilir.
2. **Survivorship bias riski.** SWKS/LULU örnekleri başarılı örnekler; başarısız reversal örnekleri ayrıca toplanmalı.
3. **Universe bağımlılığı yüksek.** Bu setup random düşük kaliteli hisselerde çalışmayabilir; growth/leader universe gerekir.
4. **Volume confirmation yoruma açık.** “Slight increase in volume” veya “heavy volume” için deterministic thresholds seçilmeli.
5. **Stop handling discretionary.** Intraday kırılımda hemen mi çıkılacak, gün sonu mu beklenecek? Parity için net seçilmeli.
6. **Pyramiding riski.** Eklemeler yanlış market regime’de drawdown’u büyütebilir.
7. **Crypto adaptasyonu doğrudan yapılmamalı.** 21DMA/50DMA equity mantığı BTC/altcoinlerde farklı davranabilir.

---

## 12. QuantLens İçin En Değerli Dersler

1. **Entry, stop ile birlikte tanımlanmalı.** Sadece sinyal değil, risk seviyesi de producer çıktısının parçası olmalı.
2. **Breakout entry obvious olduğu için alternatif entry aranmalı.** Pullback/upside reversal, daha düşük cost basis ve daha iyi R multiple verebilir.
3. **Upside reversal bir confirmation event olarak kullanılabilir.** Pullback sırasında zayıf ellerin shakeout sonrası destek bulduğunu temsil eder.
4. **21DMA aktif pozisyon yönetiminde merkezi role sahip.** Çalışan trendlerde pullback/add bölgesi olarak test edilmeli.
5. **50DMA heavy-volume break yapısal exit adayıdır.** Sadece stop/TP değil, trend sağlığı exit’i olarak MTC_V2’ye uygun.
6. **Pyramiding iki tip olmalı:** weakness/support add ve strength/resistance break add.
7. **Raw setup marker ile actual entry marker ayrılmalı.** MTC_V2 görselleştirmesinde reversal görüldü diye entry gerçekleşmiş gibi gösterilmemeli.
8. **Bu strateji market regime ile birlikte test edilmeli.** Harris’in diğer videosundaki market trend guard bu producer ile doğal eşleşir.

---

## 13. Suggested Candidate Split

```yaml
candidate_split:
  parent_candidate: "YT_CtioOmc1Eig_20260503_A"
  children:
    - id: "CH_UPSIDE_REVERSAL_PULLBACK_V1"
      type: "signal_producer"
      priority: "VERY_HIGH"
    - id: "CH_PIVOT_BREAKOUT_STRENGTH_V1"
      type: "baseline_signal_producer"
      priority: "HIGH"
    - id: "CH_21DMA_PULLBACK_ADD_V1"
      type: "position_manager_add_module"
      priority: "HIGH"
    - id: "CH_RESISTANCE_BREAK_ADD_V1"
      type: "position_manager_add_module"
      priority: "MEDIUM"
    - id: "CH_HEAVY_VOLUME_50DMA_EXIT_V1"
      type: "exit_rule"
      priority: "HIGH"
```

---

## 14. Beklenen Dosya / Registry Güncellemeleri

Codex repo içinde çalışırken önerilen kayıt:

### youtube_video_index.csv

```csv
video_id,normalized_url,title,channel,status,candidate_id,transcript_hash,first_seen_at,last_seen_at,process_count
CtioOmc1Eig,https://www.youtube.com/watch?v=CtioOmc1Eig,Trade Like a Professional Simple and Effective Trading Strategy with Charles Harris,UNKNOWN_CHANNEL,CANDIDATE,YT_CtioOmc1Eig_20260503_A,2931633c76574f95cd451271f0e820f66dc2c79fa71c9162a508e54b30322001,2026-05-03,2026-05-03,1
```

### channel_quality_registry.csv

Kanal bilinmediği için otomatik blacklist/quality kararı verilmemeli. Kanal sonradan tespit edilirse:

```yaml
quality_update:
  candidate_count_increment: 1
  useful_count_increment: 1
  suggested_state: GOOD_after_more_confirming_videos
```

---

## 15. Oluşturulan / Dokunulmayan Dosyalar

### Bu raporda oluşturulan dosya

```text
INTAKE_2026-05-03_CtioOmc1Eig_charles_harris_trade_like_professional.md
```

### Dokunulmaması gereken dosyalar

Aşağıdakilere dokunulmadı / dokunulmamalı:

```text
01_PINE/MTC_V2.pine
Production Python runner dosyaları
Backtest / optimization result dosyaları
Büyük CSV / cache / data bundle dosyaları
Secret / API key / broker / webhook ayarları
```

---

## 16. Next Action

1. Repo registry’de duplicate kontrolü yap.
2. Duplicate değilse video index’e `CANDIDATE` olarak kaydet.
3. İlk prototipi Python’da `CH_UPSIDE_REVERSAL_PULLBACK_V1` olarak üret.
4. Baseline karşılaştırma için `CH_PIVOT_BREAKOUT_STRENGTH_V1` üret.
5. İki producer’ı aynı universe üzerinde karşılaştır: entry distance, stop distance, R multiple, win-rate, maxDD, profit factor.
6. Sonra `21DMA Pullback Add` ve `50DMA Heavy Volume Exit` modüllerini sırayla ekle.
7. Pozitif sonuç yoksa Pine’a taşıma.
8. Pozitif sonuç varsa MTC_V2’ye feature-gated ve debug export destekli olarak planla.

---

## 17. Final Verdict

```text
VERDICT: CANDIDATE
CODEX_STATUS: READY_FOR_PYTHON_PROTOTYPE
PINE_NOW: NO
PRIMARY_VALUE: Pullback/upside-reversal entry producer with risk-defined stop and pyramid/exit modules
BEST_FIRST_TEST: CH_UPSIDE_REVERSAL_PULLBACK_V1 vs CH_PIVOT_BREAKOUT_STRENGTH_V1
WIKI_NOTE: YES
DUPLICATE: NOT_DETECTED_IN_CONVERSATION
REGISTRY_CHECK: NOT_CHECKED_EXTERNAL_REGISTRY
```
