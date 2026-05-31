# QuantLens Transcript Intake Report — 283% Gain in 1 Year: The Story of the 22-Year-Old Swing Trader

## 1. Intake Kararı

- **Final Classification:** `CANDIDATE`
- **Codex Status Önerisi:** `READY_FOR_PYTHON_PROTOTYPE`
- **Wiki Notu Önerisi:** `YES — 04_SYSTEM_DEVELOPMENT`, ayrıca `01_RISK_MANAGEMENT`, `02_TRADING_PSYCHOLOGY`, `03_MARKET_STRUCTURE`, `06_EXECUTION_AND_FEES`
- **Öncelik:** `VERY_HIGH`
- **Güven:** `0.93`
- **Karar Özeti:** Bu transcript, QuantLens/MTC_V2 için yüksek değerli bir swing trading strateji aday seti içeriyor. Video tek bir basit indikatör stratejisi değil; **tight-stop / low-win-rate / high-R breakout**, **prior-day-high / opening-range-high / intraday-range-high entry**, **inside-day/tight-range compression**, **9/21/50 EMA trend ve trailing**, **equity-curve feedback risk scaling**, **watchlist market health**, **parabolic volume exit** ve **short-side declining EMA setup** gibi birden fazla kodlanabilir bileşen veriyor. İlk etapta Pine’a geçmeden Python araştırma/prototype yapılmalı.

## 2. Metadata

- **Candidate ID:** `YT_lS9zbnLi1Gg_20260503_A`
- **Source URL:** `https://youtu.be/lS9zbnLi1Gg?si=vmGqb0X_iM3tCvw9`
- **Normalized URL:** `https://www.youtube.com/watch?v=lS9zbnLi1Gg`
- **Video ID:** `lS9zbnLi1Gg`
- **Title:** `283% Gain in 1 Year - The Story of the 22-Year-Old Swing Trader`
- **Channel:** `TraderLion / TraderLion Podcast inferred from transcript; channel ID not provided`
- **Speaker / Main Trader:** `Martin Luke`
- **Host:** `Richard Moglen / TraderLion`
- **Transcript File:** `283% Gain in 1 Year - The Story of the 22-Year-Old Swing Trader.md`
- **Transcript SHA256:** `d1789bb93b1df725fbd422476b6b3604e7417136e6fc8e9cb87773433fbe703c`
- **Report Date:** `2026-05-03`
- **Language:** English transcript; Turkish intake report
- **Detected Market Type:** US equities; mostly growth / momentum / small-cap / high-ADR stocks; some crypto-correlated equities such as COIN
- **Timeframe Focus:** Swing trading, mostly days to 1–3 weeks; entry timing may use 1-minute and 5-minute intraday structure
- **Primary Style:** Trend-following breakout trader with tight stops, low win rate, large R-multiple winners
- **Core Instruments / Examples Mentioned:** `SMCI`, `COIN`, `GME`, `AMC`, `SOFI`, `LMND`, `SOUN`, `QUBT`, `SMTC`, `SURF`, `Bitcoin-linked COIN context`

## 3. Duplicate / Registry Kontrolü

### Conversation İçi Kontrol

Bu conversation içinde daha önce işlenen video ID’leri:

- `lTiR1pc82EE`
- `QzzKqmPcB3A`
- `R1sNTB2Vh7w`

Bu transcript video ID:

- `lS9zbnLi1Gg`

**Sonuç:** Conversation içinde duplicate görünmüyor.

### Repo Registry Kontrolü

Aşağıdaki repo dosyaları bu chat ortamına yüklenmediği için gerçek registry kontrolü yapılamadı:

- `_registry/youtube_video_index.csv`
- `channel_blacklist.yaml`
- `channel_quality_registry.csv`
- Candidate registry dosyaları

**Registry Durumu:** `NOT_CHECKED_EXTERNAL_REGISTRY`

Codex repo içinde çalışırken önce registry dosyalarını okumalı; aynı `video_id` veya aynı `transcript_hash` varsa yeni candidate üretmemeli.

## 4. Channel Quality / Blacklist Kararı

- **Channel:** `TraderLion inferred; exact channel ID unavailable`
- **Blacklist Kararı:** `NO_BLACKLIST`
- **Geçici Quality State:** `GOOD_CANDIDATE_SOURCE`
- **Neden:** İçerik çok detaylı, gerçek trade örnekleri, giriş/çıkış/stop kuralları, risk ve psikoloji hataları içeriyor. Kodlanabilir strateji fikri yoğunluğu yüksek.
- **Not:** Prompt kuralı gereği kanal ID net olmadığı için kalıcı blacklist/quality registry kararı Codex repo içindeki kanal metadata’sı ile verilmelidir.

## 5. İçerik Özeti

Video, 2024 US Investing Championship’te yüksek performans elde eden 22 yaşındaki Martin Luke’un swing trading sürecini, risk yönetimini, hatalarını, entry/exit taktiklerini ve piyasa koşulu değerlendirme yöntemini anlatıyor. Martin’in sistemi düşük win-rate’i kabul eden ama tight stop sayesinde büyük R-multiple kazananları yakalamaya çalışan momentum/breakout yaklaşımıdır.

Ana fikirler:

1. Büyük kazanan trade’ler çoğu zaman ideal girişten sonra breakout günü diplerini tekrar ziyaret etmez.
2. Trader her trade’in getirisini tahmin edemez; ama stop mesafesini, riskini ve pozisyon boyutunu kontrol edebilir.
3. Tight stop, win-rate’i düşürebilir; ancak büyük move yakalandığında R-multiple artışı doğrusal değil, çok kuvvetli şekilde büyür.
4. Entry kalitesi stop mesafesiyle ölçülür: stop çok genişse entry geç veya risk yönetilemez olabilir.
5. Prior day high, opening range high, intraday range high, inside day breakout ve 9/21 EMA çevresindeki tight range yapıları ana giriş noktalarıdır.
6. 9 EMA çoğu zaman hızlı trend trailing stop olarak; 21/50 EMA ise güçlü erken trendlerde daha geniş runner stop olarak kullanılır.
7. Equity curve, market condition filtresidir: kendi sistemin çalışıyorsa indeks zayıflığına rağmen tamamen likide olmak zorunda değilsin; sistem çalışmıyorsa risk azaltılmalı.
8. Watchlist içindeki liderlerin downgrade olması, piyasa sağlığının bozulduğunu gösterir.
9. Small/micro-cap gap risk nedeniyle position cap gerektirir.
10. En büyük gelişim alanları: revenge trading, losing streak sırasında risk artırma, stop’a uymama, random entries ve drawdown kontrolü.

## 6. Sınıflandırma Gerekçesi

### Neden `CANDIDATE`?

Bu transcriptte doğrudan kodlanabilir trade kuralları var:

- Prior-day-high breakout entry
- Opening range high breakout entry
- Intraday range high re-entry
- Inside day / pseudo-inside-day tightness
- Low of day veya 5-minute candle low stop
- Stop mesafesi maksimum yaklaşık 5%
- Stop mesafesini ADR’nin %50’sinden küçük tutma fikri
- High ADR stock universe filtresi
- 9/21/50 EMA trend ve trailing logic
- Sell into strength: 3R+, 6R, 7R, 8R, 12R gibi R-multiple seviyeleri
- Position cap: genel max ~35%, small/micro-cap için ~25–30%
- Equity-curve based risk scaling
- Watchlist-based market health
- Short setup: declining EMA + intraday resistance + failed reclaim / lower high

Bu nedenle `WIKI_ONLY` değil, net şekilde `CANDIDATE`.

### Neden `READY_FOR_PYTHON_PROTOTYPE`?

Çünkü strateji Pine’a direkt geçirilmeden önce aşağıdaki konular Python’da test edilmeli:

- Intraday 1m/5m entry verisi gereksinimi
- Daily-only backtest ile intraday ORH/IRH girişlerinin approximasyonu
- Stop mesafesi, gap, slippage, small-cap liquidity etkisi
- Low win-rate / high-R dağılımının komisyon ve slippage altında dayanıklılığı
- Equity-curve feedback risk scaling’in overfit riski
- ADR ve dollar volume filtrelerinin piyasa rejimine göre etkisi

## 7. Kodlanabilir Strateji / Sistem Çekirdekleri

## Candidate A — Martin Tight Range Breakout v1

**Amaç:** Güçlü momentum/hikâye taşıyan ve tight range içinde sıkışan hisselerde düşük stop mesafeli breakout yakalamak.

### Setup Universe

```yaml
universe_filters:
  market: "US equities"
  min_price: [3, 5, 10]
  min_dollar_volume_20d: [10_000_000, 20_000_000, 50_000_000]
  min_ADR_pct_20d: [4, 5, 6, 8]
  avoid_low_liquidity: true
  small_micro_cap_position_cap: true
```

### Trend / Context Filters

```yaml
trend_context:
  ema_fast: 9
  ema_mid: 21
  ema_slow: 50
  require_close_above_ema21: true
  prefer_ema9_above_ema21: true
  prefer_ema21_above_ema50: true
  weekly_context:
    prefer_large_base: true
    prefer_higher_lows: true
    prefer_weekly_21ema_support: true
    large_base_required: false
```

### Tightness / Compression

```yaml
tight_range:
  lookback_days: [2, 3, 5, 8]
  require_inside_day: [true, false]
  max_range_pct_of_ADR: [0.50, 0.75, 1.00]
  max_close_to_ema9_pct: [2, 4, 6]
  prefer_range_above_ema9_or_ema21: true
```

### Entry Trigger

```yaml
entry:
  primary_trigger: "break_prior_day_high"
  alternative_triggers:
    - "opening_range_high_1m"
    - "opening_range_high_5m"
    - "intraday_range_high_5m_reentry"
    - "anchor_vwap_reclaim_plus_range_break"
  require_range_expansion: true
  reject_if_entry_to_stop_pct_gt: [3, 4, 5]
```

### Stop Logic

```yaml
stop:
  preferred_stop: "low_of_day"
  if_low_of_day_too_wide:
    use: "5m_entry_candle_low"
  max_stop_pct: [3, 4, 5]
  max_stop_as_ADR_fraction: [0.33, 0.50, 0.67]
  hard_stop_required: true
```

### Exit Logic

```yaml
exit:
  trailing_ema_default: 9
  trailing_ema_runner_options: [21, 50]
  sell_into_strength:
    trim_size_pct: [10, 15]
    trigger_R: [3, 6, 8, 12]
    trigger_extended_from_ema9: true
    trigger_euphoria_manual_proxy: "parabolic_extension"
  weakness_exit:
    close_below_ema9: true
    break_swing_low: true
    break_bar_low: true
```

**MTC_V2 Bağlantısı:**

- `SIGNAL PRODUCER`: Tight Range Breakout producer
- `ENTRY GATES`: ADR, dollar volume, EMA stack, weekly context
- `POSITION SIZING`: tight-stop risk sizing + microcap cap
- `EXIT RULES`: 9 EMA / 21 EMA / swing low trailing; partial sells into strength

**Prototype Priority:** `VERY_HIGH`

## Candidate B — Opening Range High / Intraday Range Re-entry v1

**Amaç:** Günlük setup hazırken giriş riskini düşürmek için 1m/5m opening range veya intraday range breakout kullanmak.

### Entry Rules

```yaml
orh_irh_entry_v1:
  daily_setup_required: true
  opening_range_minutes: [1, 5]
  trigger:
    - break_opening_range_high
  stop:
    - opening_range_low
    - entry_candle_low
  reentry_if_orh_fails:
    enabled: true
    require_setup_intact: true
    require_hold_ema9_or_ema21_intraday: true
    trigger: break_intraday_range_high
    stop: new_intraday_range_low
```

### Daily-to-Intraday Bridge

Bu candidate için Python backtester iki modda çalışmalı:

1. **Intraday mode:** 1m/5m data ile gerçek ORH/IRH test.
2. **Daily approximation mode:** Entry `max(open, prior_high)` veya day high breakout olarak simüle edilir; stop `day_low` veya estimated intraday low olur. Bu mod yalnızca kaba tarama içindir.

**Risk:** Daily-only test intraday stop sırasını doğru bilemeyebilir. Parity için OHLC deterministic path varsayımı ayrıca belgelenmeli.

**Prototype Priority:** `VERY_HIGH`

## Candidate C — Low Win Rate / High R Risk Engine v1

**Amaç:** Win-rate düşük olsa bile average win / average loss oranı yüksek bir sistemin test edilmesi.

### Transcriptten Çıkan Stat Profili

- Win rate yaklaşık `23%`
- Average winner yaklaşık `15%`
- Average loser yaklaşık `3%`
- Losers genellikle entry günü veya hızlı şekilde kesiliyor
- Winners daha uzun tutuluyor

### Model Rules

```yaml
low_winrate_high_R_engine_v1:
  expected_win_rate_range: [0.18, 0.30]
  min_avg_win_to_avg_loss_ratio: [3.0, 4.0, 5.0]
  max_avg_loss_pct: [2.0, 3.0, 4.0]
  risk_per_trade_pct_grid: [0.25, 0.50, 0.75, 1.00]
  martin_reported_risk_pct: 5.0
  note: "Reported 5% portfolio risk per trade is aggressive; QuantLens should test safer risk grids first."
```

**MTC_V2 Bağlantısı:**

- `POSITION SIZING` grid’e alınmalı.
- User’ın MTC parity-first disiplini gereği önce düşük risk grid ile test edilmeli.
- Çok agresif 5% risk doğrudan default yapılmamalı; sadece stress-test parametresi olmalı.

**Prototype Priority:** `HIGH`

## Candidate D — Equity Curve Feedback Risk Scaling v1

**Amaç:** Sistem kendi performansına göre risk azaltıp artırabilsin.

### Core Idea

Martin, piyasa koşullarını değerlendirirken sadece endekse değil, kendi trade’lerinin çalışıp çalışmadığına bakıyor. Kendi equity curve feedback’i sistemin o anki piyasada uyumlu olup olmadığını gösteriyor.

### Rules

```yaml
equity_curve_feedback_guard_v1:
  lookback_trades: [10, 20, 30]
  lookback_days: [10, 20, 40]
  metrics:
    - realized_R_sum
    - win_rate_recent
    - avg_loss_recent
    - equity_drawdown_from_peak
    - consecutive_losses
  risk_modes:
    normal:
      risk_multiplier: 1.0
    test_waters:
      risk_multiplier: 0.25
    drawdown_defense:
      risk_multiplier: 0.25
    hot_streak:
      risk_multiplier: [1.25, 1.50]
  triggers:
    if_drawdown_gt_pct: [5, 10, 15]
    if_consecutive_losses_gte: [3, 5, 7]
    if_recent_R_sum_lt: [-3, -5, -8]
  action:
    - reduce_risk
    - block_new_entries_after_max_loss_streak
    - require_A_plus_setup_only
```

**MTC_V2 Bağlantısı:**

- `ENTRY GATES` içinde externally-stateful guard.
- `PortfolioState` / performance ledger okunmalı.
- Optimization’da overfit riski yüksek olduğu için çok sınırlı parametre grid’i kullanılmalı.

**Prototype Priority:** `HIGH`

## Candidate E — Watchlist Market Health Gauge v1

**Amaç:** Market condition’ı yalnızca indekslerden değil, lider watchlist davranışından ölçmek.

### Rules

```yaml
watchlist_market_health_v1:
  watchlist_categories:
    - leader
    - setup_ready
    - extended
    - failed_breakout
    - broken
  daily_score:
    leader_count_weight: 2
    setup_ready_count_weight: 1
    failed_breakout_penalty: -2
    broken_penalty: -3
  downgrade_signal:
    if_many_leaders_move_to_failed_or_broken: true
  risk_action:
    strong_health: "normal_or_increase_risk"
    neutral_health: "normal_or_small_size"
    weak_health: "reduce_long_risk_or_block_low_quality_entries"
```

### Implementation Notu

Bu modül için gerçek watchlist verisi gerekiyorsa ilk etapta otomatik “leader universe” proxy kullanılabilir:

- Son 3–6 ay relative strength top decile
- Dollar volume yeterli
- Above EMA21/EMA50
- High ADR
- Recent breakout / tight setup count

**Prototype Priority:** `MEDIUM_HIGH`

## Candidate F — Parabolic Volume Exhaustion Exit v1

**Amaç:** Çok hızlı yükselmiş pozisyonda hacim/dollar volume zirvesi, EMA’dan aşırı uzaklaşma ve direnç bölgesi birleştiğinde long pozisyonu azaltmak veya tamamen çıkmak.

### Rules

```yaml
parabolic_volume_exit_v1:
  trigger_conditions_any:
    - R_multiple_gte: [6, 8, 10, 12]
    - price_gain_from_entry_pct_gte: [30, 50, 75, 100]
    - extension_from_ema9_pct_gte: [10, 15, 20, 30]
    - intraday_dollar_volume_runrate_gt_prior_52w_max: true
    - near_weekly_or_monthly_resistance: true
  actions:
    - trim_10_to_15_pct
    - trim_50_pct_if_extreme
    - full_exit_if_parabolic_plus_major_resistance
```

**MTC_V2 Bağlantısı:**

- `EXIT RULES` içinde strength-exit / partial-exit modülü.
- MTC’de partial exits ve trailing stop sync karmaşık olduğundan ilk etapta Python-only test edilmeli.
- Pine’a taşınırsa working exits ve stop owner kuralları korunmalı.

**Prototype Priority:** `HIGH`

## Candidate G — Small/Micro-Cap Gap Risk Cap v1

**Amaç:** Small/micro-cap hisselerde gap-down riskinden kaynaklı aşırı tek gün drawdown’larını azaltmak.

### Rules

```yaml
small_microcap_gap_risk_cap_v1:
  classify_small_microcap_by:
    - market_cap_if_available
    - dollar_volume_threshold
    - price_threshold
    - ADR_threshold
  position_cap:
    normal_cap_pct: 35
    small_micro_cap_cap_pct: [20, 25, 30]
  additional_guards:
    avoid_before_binary_event: true
    reduce_if_spread_wide: true
    reduce_if_overnight_gap_risk_high: true
  emergency_exit:
    if_gap_down_against_position_gt_pct: [10, 20, 30]
    use_opening_range_low_break_as_exit_trigger: true
```

**Prototype Priority:** `HIGH`

## Candidate H — Short Setup: Declining EMA + Intraday Resistance v1

**Amaç:** Long momentum sisteminin tersinde, zayıf trendde bounce/reclaim failure üzerinden short fırsatı aramak.

### Transcriptteki Yaklaşım

Martin short setup bölümünde declining EMA, zayıf yapı, intraday resistance, failed bounce/reclaim ve market condition ile short tarafını değerlendiriyor. Long sistem kadar olgun değil; bu nedenle ayrı ve daha düşük riskli araştırılmalı.

### Rules

```yaml
short_declining_ema_rejection_v1:
  trend_filter:
    close_below_ema21: true
    ema9_below_ema21: true
    ema21_slope_down: true
  setup:
    bounce_into_declining_ema9_or_ema21: true
    lower_high_structure: true
    intraday_resistance_range: true
  entry:
    break_intraday_range_low: true
    fail_reclaim_vwap_or_ema: true
  stop:
    intraday_range_high
  exit:
    cover_into_weakness_R: [2, 3, 5]
    trail_above_ema9_or_swing_high: true
```

**MTC_V2 Bağlantısı:**

- Separate short producer veya short-side transform olarak denenebilir.
- Long producer ile aynı anda aktif edilirse conflict normalization gerekir.
- İlk testte only-short standalone yapılmalı.

**Prototype Priority:** `MEDIUM`

## Candidate I — Hesitation / Confusion No-Trade Gate v1

**Amaç:** Belirsiz setup’larda düşük kaliteli girişleri azaltmak.

### Kaynak Fikir

Martin, “trade alıp almama konusunda kararsızsan çoğu zaman alma” yaklaşımını vurguluyor. Bu doğrudan kodlanabilir olmasa da setup skoru düşükse trade bloklanabilir.

### Rules

```yaml
no_trade_confusion_gate_v1:
  setup_score_components:
    - tightness_score
    - trend_score
    - liquidity_score
    - stop_manageability_score
    - market_health_score
    - catalyst_or_theme_score
  min_score_to_trade: [70, 80, 90]
  if_score_between_50_70:
    action: "watch_only"
  if_stop_not_manageable:
    action: "reject"
```

**Prototype Priority:** `MEDIUM_HIGH`

## 8. MTC_V2 Mimarisine En Uygun Entegrasyon Haritası

### 1. SIGNAL PRODUCER

Yeni producer adayları:

- `producer_tight_range_breakout_martin_v1`
- `producer_orh_irh_breakout_v1`
- `producer_short_declining_ema_rejection_v1`

İlk etapta sadece Python research layer’da denenmeli. Pine’a hemen geçilmemeli.

### 2. SIGNAL TRANSFORM PIPELINE

Uygun transformlar:

- Inside day confirmation
- Prior-day-high retest / reclaim
- Intraday range re-entry
- Failed ORH re-entry logic

### 3. ENTRY GATES

Uygun gates:

- ADR floor
- Dollar volume floor
- EMA trend gate
- Weekly context gate
- Stop manageability gate
- Market health gate
- Equity curve feedback guard
- Small/micro-cap risk cap

### 4. POSITION MANAGER

Özellikle önemli:

- Losing streak sırasında risk azaltma
- Drawdown defense mode
- A+ setup only mode
- Same-day re-entry limit
- Max trades per day / week

### 5. POSITION SIZING

Öneri:

- Reported 5% risk doğrudan kullanılmamalı.
- QuantLens araştırma grid’i: `0.25%`, `0.50%`, `0.75%`, `1.00%`
- Small/micro-cap position cap ayrı olmalı.
- Stop distance çok genişse position açma veya size düşürme.

### 6. EXIT RULES

Uygun exit modülleri:

- Initial SL: LOD / 5m candle low / intraday range low
- Break-even after R
- 9 EMA trailing
- 21/50 EMA runner trailing
- Sell into strength partials
- Parabolic volume full/partial exit
- Emergency gap-down exit

### 7. VISUALIZATION

Pine’a ileride taşınırsa marker taxonomy net olmalı:

- `RAW_TIGHT_RANGE_SIGNAL`
- `ENTRY_ORH_CONFIRMED`
- `ENTRY_PRIOR_DAY_HIGH_CONFIRMED`
- `ENTRY_IRH_REENTRY_CONFIRMED`
- `STOP_LOD`
- `STOP_5M_CANDLE_LOW`
- `SELL_STRENGTH_TRIM`
- `TRAIL_EMA9_EXIT`
- `MARKET_HEALTH_BLOCK`
- `EQUITY_DRAWDOWN_BLOCK`

## 9. Backtest / Research Planı

### Phase 0 — Data Requirements

Gerekli minimum veri:

- Daily OHLCV
- 1m veya 5m intraday OHLCV, özellikle ORH/IRH için
- Dollar volume
- ADR calculation
- Optional: market cap, sector, earnings/catalyst dates, news headline metadata

### Phase 1 — Daily-Only Approximation

Amaç hızlı screening:

```yaml
daily_approximation:
  entry_proxy:
    - prior_day_high_break
    - open_above_upper_half_prior_day_and_break_high
  stop_proxy:
    - day_low
    - prior_day_low
    - fixed_pct_stop
  exits:
    - ema9_close_break
    - ema21_runner
    - R_multiple_trim
```

Risk: Intraday path bilinmediği için ORH/IRH doğruluğu sınırlıdır.

### Phase 2 — Intraday Accurate Prototype

Amaç gerçek entry/stop sırasını test etmek:

```yaml
intraday_accurate:
  timeframes: ["1m", "5m"]
  triggers:
    - break_first_1m_high
    - break_first_5m_high
    - break_5m_intraday_range_high_after_failed_orh
  stops:
    - first_1m_low
    - first_5m_low
    - entry_5m_candle_low
    - lod
```

### Phase 3 — Regime / Market Health Layer

Test edilecek filtreler:

- Index EMA9/EMA21 relationship
- Index near resistance
- Own equity curve feedback
- Watchlist leader deterioration proxy
- Recent breakout success rate

### Phase 4 — Robustness

Ölçülecek metrikler:

- CAGR / total return değil, öncelik R-distribution
- Profit factor
- Average win / average loss
- Max drawdown
- Max monthly drawdown
- Consecutive losses
- Tail loss / gap loss
- Slippage sensitivity
- Commission sensitivity
- Win rate by regime
- Top 10 trades contribution
- Median trade R
- Pareto concentration

## 10. Edge Hipotezi

### Ana Hipotez

Tight range’den çıkan yüksek ADR’li momentum hisselerinde, entry stop mesafesi küçük tutulursa, düşük win-rate’e rağmen büyük kazananların R-multiple katkısı sistemi pozitif expectancy’ye taşıyabilir.

### Beklenen Davranış

- Win rate düşük olabilir: `18–30%`
- Average loser küçük kalmalı: `-1R` veya daha az
- Büyük kazananlar sistemin çoğu kârını oluşturmalı
- ORH/IRH entry, traditional breakout entry’ye göre daha iyi R-multiple verebilir
- Piyasa sağlığı bozulduğunda death-by-thousand-cuts artar
- Drawdown defense modu performans eğrisini yumuşatabilir

## 11. Riskler / Şüpheli veya Dikkat Gerektiren Noktalar

1. **5% per-trade risk çok agresif:** Martin bunu kendi yarışma/personality bağlamında kullanmış. QuantLens default’u olmamalı.
2. **Intraday data gerektirir:** ORH/IRH daily data ile doğru test edilemez.
3. **Small-cap slippage/gap riski yüksek:** Backtest optimistic olabilir.
4. **Survivorship bias:** Videodaki örnekler büyük kazananlardan seçilmiş olabilir.
5. **News/catalyst filter eksik:** EP veya meme-stock move’ları sadece chart ile yakalamak riskli olabilir.
6. **Low win-rate psikolojik olarak zor:** Strategy canlı kullanımda çok sayıda küçük kayıp üretebilir.
7. **Equity curve feedback overfit olabilir:** Çok parametreli yapılırsa geçmişe aşırı uyum riski var.
8. **Pine parity zorluğu:** 1m/5m intraday entry ile daily strategy parity kolay değildir.
9. **Partial exit complexity:** MTC_V2’de partial exit ve trailing sync dikkat gerektirir.
10. **Manual observation içeren kurallar:** “Euphoria”, “looks extended”, “confidence” gibi ifadeler proxy’lere dönüştürülmeli.

## 12. Trader Wiki Notu Önerisi

Bu video aynı zamanda güçlü bir Trader Wiki notu olmalı.

### Wiki ID

`TW_2026-05-03_04_SYSTEM_DEVELOPMENT_martin_luke_tight_stop_high_r.md`

### Topic

- Primary: `04_SYSTEM_DEVELOPMENT`
- Secondary: `01_RISK_MANAGEMENT`
- Secondary: `02_TRADING_PSYCHOLOGY`
- Secondary: `06_EXECUTION_AND_FEES`

### Usefulness Score

`9/10`

### Wiki Ana Dersler

- Büyük trader gelişimi tek bir yılda değil, uzun süreli hata azaltma sürecinde oluşur.
- Low win-rate sistemler çalışabilir; ancak ancak average winner / average loser oranı çok güçlü ise.
- Stop mesafesi sadece risk kontrolü değil, aynı zamanda entry kalitesi filtresidir.
- Kendi equity curve’ün piyasa koşulu hakkında çoğu sosyal medya yorumundan daha değerlidir.
- En iyi loss, hatayı kalıcı olarak öğreten loss olabilir.
- Gap risk, özellikle small/micro-cap hisselerde pozisyon boyutuyla yönetilmelidir.
- Büyük fırsatı kaçırmak sorun değildir; random trade ile equity curve bozmak daha büyük sorundur.

## 13. Codex İçin Net Uygulama Talimatı

Codex bu videodan sonra aşağıdaki işleri yapmalı:

1. Repo registry dosyalarını oku.
2. Aynı video ID veya transcript hash varsa duplicate olarak dur.
3. Yeni candidate klasörü oluştururken production Pine veya production runner dosyalarına dokunma.
4. Bu videoyu tek strateji gibi değil, modüler candidate seti olarak işle.
5. İlk araştırma hedefini `producer_tight_range_breakout_martin_v1` olarak seç.
6. ORH/IRH için data gereksinimini açıkça belirt.
7. Daily-only approximation ile intraday-accurate prototype’ı ayrı tut.
8. Aggressive risk settings’i default yapma; 5% risk sadece reference/stress-test olarak kalsın.
9. Small/micro-cap gap risk cap’i candidate ile beraber tasarla.
10. Finalde hangi dosyaların oluşturulduğunu ve hangi dosyalara dokunulmadığını raporla.

## 14. Candidate Registry Önerisi

```csv
candidate_id,video_id,title,status,priority,primary_module,secondary_modules,notes
YT_lS9zbnLi1Gg_20260503_A,lS9zbnLi1Gg,"283% Gain in 1 Year - The Story of the 22-Year-Old Swing Trader",READY_FOR_PYTHON_PROTOTYPE,VERY_HIGH,producer_tight_range_breakout_martin_v1,"orh_irh_entry_v1; equity_curve_feedback_guard_v1; parabolic_volume_exit_v1; small_microcap_gap_risk_cap_v1","High-value tight stop / high-R swing trading framework; needs intraday data for accurate ORH/IRH test."
```

## 15. Video Index Önerisi

```csv
video_id,normalized_url,title,channel,status,candidate_id,transcript_hash,first_seen_at,last_seen_at,process_count
lS9zbnLi1Gg,https://www.youtube.com/watch?v=lS9zbnLi1Gg,"283% Gain in 1 Year - The Story of the 22-Year-Old Swing Trader","TraderLion inferred",CANDIDATE,YT_lS9zbnLi1Gg_20260503_A,d1789bb93b1df725fbd422476b6b3604e7417136e6fc8e9cb87773433fbe703c,2026-05-03,2026-05-03,1
```

## 16. Channel Quality Registry Önerisi

```csv
channel,channel_id,quality_state,total_processed,candidate_count,wiki_count,salvage_count,reject_count,stop_count,last_video_id,notes
"TraderLion inferred",UNKNOWN_CHANNEL_ID,GOOD,1,1,0,0,0,0,lS9zbnLi1Gg,"High-quality interview with detailed executable swing trading rules; exact channel metadata should be filled by repo workflow."
```

## 17. Önerilen Dosya Çıktıları

Codex repo içinde aşağıdaki gibi dosyalar oluşturabilir:

```text
YOUTUBE_STRATEGY_INTAKE/
  candidates/
    YT_lS9zbnLi1Gg_20260503_A_martin_luke_tight_range_breakout/
      INTAKE.md
      STRATEGY_SPEC.md
      PYTHON_PROTOTYPE_PLAN.md
      RISK_NOTES.md
      DATA_REQUIREMENTS.md
      README.md
  11_TRADER_WIKI/
    04_SYSTEM_DEVELOPMENT/
      TW_2026-05-03_04_SYSTEM_DEVELOPMENT_martin_luke_tight_stop_high_r.md
```

## 18. MTC_V2 Dosyalarına Dokunma Durumu

Bu intake raporu kapsamında:

- `01_PINE/MTC_V2.pine` dosyasına dokunulmamalı.
- Production Python runner dosyalarına dokunulmamalı.
- Backtest veya optimization çalıştırılmamalı.
- Büyük CSV / cache / data bundle oluşturulmamalı.
- Secret, API key, webhook veya broker bilgisi yazılmamalı.

## 19. Sonuç

Bu transcript, şu ana kadar işlenen videolar içinde en kodlanabilir ve doğrudan prototipe çevrilebilir kaynaklardan biridir. Özellikle `tight range breakout + ORH/IRH entry + low stop distance + high R exit + equity curve feedback` kombinasyonu QuantLens/MTC_V2 araştırma hattı için çok değerlidir.

**Final Next Action:**

`CREATE_CANDIDATE_FOLDER_AND_PYTHON_PROTOTYPE_PLAN_ONLY`

Önce Python’da modüler test planı hazırlanmalı. Pine/MTC_V2 entegrasyonu ancak Python tarafında anlamlı expectancy, slippage dayanıklılığı ve drawdown davranışı görüldükten sonra düşünülmeli.
