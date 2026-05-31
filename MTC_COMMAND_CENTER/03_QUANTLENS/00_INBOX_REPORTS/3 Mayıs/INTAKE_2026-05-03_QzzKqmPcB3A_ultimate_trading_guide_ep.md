# QuantLens Transcript Intake Report — 7 Steps to Beat the Market - Ultimate Trading Guide Ep

## 1. Intake Kararı

- **Final Classification:** `CANDIDATE`
- **Codex Status Önerisi:** `READY_FOR_PYTHON_PROTOTYPE`
- **Wiki Notu Önerisi:** `YES — 04_SYSTEM_DEVELOPMENT`, ayrıca `01_RISK_MANAGEMENT` ve `02_TRADING_PSYCHOLOGY` bağlantılı
- **Öncelik:** `MEDIUM`
- **Güven:** `0.72`
- **Karar Özeti:** Video tek bir net al-sat stratejisi vermiyor; fakat sistematik stratejiye dönüştürülebilecek birkaç açık yapı taşı içeriyor: closing range, weekly closing range, relative strength, moving-average stage analysis, tight base / volatility contraction, pivot breakout, pullback / drift-back entry ve post-analysis disiplinleri. Bu nedenle doğrudan tek strateji olarak değil, **multi-module strategy candidate** olarak alınmalı.

## 2. Metadata

- **Candidate ID:** `YT_QzzKqmPcB3A_20260503_A`
- **Source URL:** `https://youtu.be/QzzKqmPcB3A?si=gJB9Tj18DU75ZM8Y`
- **Normalized URL:** `https://www.youtube.com/watch?v=QzzKqmPcB3A`
- **Video ID:** `QzzKqmPcB3A`
- **Title:** `7 Steps to Beat the Market - Ultimate Trading Guide Ep`
- **Channel:** `UNKNOWN_CHANNEL`
- **Transcript File:** `7 Steps to Beat the Market - Ultimate Trading Guide Ep.md`
- **Transcript SHA256:** `c1fd46047b7ca1987aa1eea04634d281f9835921f129d7d152d131b94879d230`
- **Report Date:** `2026-05-03`
- **Language:** English transcript; Turkish intake report
- **Detected Market Type:** Stocks / equities primarily; concepts may transfer to any OHLCV market with caution
- **Timeframe Focus:** Daily and weekly charts; some concepts can be adapted to crypto daily/weekly or swing-trading timeframes

## 3. Duplicate / Registry Kontrolü

### Conversation İçi Kontrol

- Bu conversation içinde daha önce işlenen video: `lTiR1pc82EE`
- Bu transcript video ID: `QzzKqmPcB3A`
- **Sonuç:** Conversation içindeki önceki video ile aynı değil.

### Repo Registry Kontrolü

Aşağıdaki repo dosyaları bu chat ortamına yüklenmediği için gerçek registry kontrolü yapılamadı:

- `_registry/youtube_video_index.csv`
- `channel_blacklist.yaml`
- `channel_quality_registry.csv`
- Candidate registry dosyaları

**Registry Durumu:** `NOT_CHECKED_EXTERNAL_REGISTRY`

Codex repo içinde çalışırken önce registry dosyalarını okumalı; aynı `video_id` veya aynı `transcript_hash` varsa yeni candidate üretmemeli.

## 4. Channel Quality / Blacklist Kararı

- **Channel:** `UNKNOWN_CHANNEL`
- **Blacklist Kararı:** Verilemez.
- **Neden:** Transcript içinde kanal ID / kanal adı güvenilir şekilde bulunmuyor.
- **Geçici Quality State:** `UNKNOWN`
- **Bu video kanal kalitesine etkisi:** Eğer kanal sonradan tespit edilirse, bu video `CANDIDATE` / faydalı içerik olarak pozitif sayılabilir.

## 5. İçerik Özeti

Video, “Ultimate Trading Guide” serisinin ilk bölümü olarak trading temeli inşa etmeyi hedefliyor. Ana akış şu başlıklarda ilerliyor:

1. Trading öğreniminde iki yol: kör deneme-yanılma yerine kitaplar, geçmiş model örnekleri ve tecrübeli traderlardan bilgi toplayıp bunu piyasada deneyime çevirmek.
2. Trader gelişim aşamaları: Stage 1, Stage 2, Stage 3.
3. Stage 1 ve Stage 2 trader hataları: sistem atlama, oversizing, randomness, overtrading, late/extended buying, FOMO, post-analysis eksikliği.
4. Price & volume okuma: OHLC bar / candlestick psikolojisi, closing range, weekly closing range.
5. Trend tanımı: moving average slope, higher high / higher low yapısı, downtrend için lower high / lower low.
6. Stage Analysis: Stage 1 accumulation, Stage 2 uptrend, Stage 3 top/distribution, Stage 4 downtrend.
7. Base / consolidation / tightness: tight price action ve volume dry-up ile supply azalması.
8. Pivot points: fiyatın directional hale gelebileceği alanlar.
9. Pullback / drift-back setups: güçlü trend içinde kontrollü geri çekilme ve yeniden yukarı çözülme.
10. Post-analysis: kayıpları ve kazançları işaretleyip sistem hatalarını bulma.

## 6. Kodlanabilir Strateji Çekirdekleri

Bu video tek bir tamamlanmış strateji değil; ama aşağıdaki modüller MTC_V2 / Python parity altyapısına ayrık candidate olarak aktarılabilir.

### Candidate A — Weekly Closing Range Leadership Filter

**Amaç:** Piyasa düzeltmesi sırasında güçlü kapanış yapan ve relatif olarak dirençli kalan sembolleri bulmak.

**Mantık:**

- Market index correction mode aktif.
- Sembol haftalık bazda düşse bile weekly close, haftalık aralığın üst bölümünde kapanıyor.
- Relative strength line fiyat yeni zirve yapmadan önce yeni zirve yapıyor.
- Volume/price davranışı kurumsal destek işareti olarak yorumlanıyor.

**Kodlanabilir Kurallar:**

- `weekly_closing_range = (weekly_close - weekly_low) / max(weekly_high - weekly_low, tick)`
- Güçlü kapanış: `weekly_closing_range >= 0.70`
- Düzeltme sırasında direnç: son 4 haftanın en az 2 veya 3 tanesinde `weekly_closing_range >= 0.70`
- Relative strength filtresi: `rs_line > highest(rs_line, N)[1]` veya RS slope pozitif.
- Market regime: index below short/medium MA veya index drawdown threshold.

**MTC_V2 Bağlantısı:**

- `ENTRY GATES` içinde leadership / relative strength gate olarak denenebilir.
- Producer değil, daha çok filtre/gate katmanı.
- Crypto’da benchmark olarak BTC, TOTAL veya sector proxy kullanılabilir; equities tarafında SPY/QQQ benchmark daha doğal.

**Prototype Priority:** `MEDIUM`

### Candidate B — Stage Analysis Trend Regime Filter

**Amaç:** Sadece Stage 2 / uptrend rejiminde long sinyaller almak; Stage 4 veya corrective rejimde longları engellemek.

**Kodlanabilir Kurallar:**

- Weekly MA pair:
  - `ma_fast = SMA(close_weekly, 10)`
  - `ma_slow = SMA(close_weekly, 40)`
- Stage 2 candidate:
  - price above 10-week MA
  - 10-week MA rising
  - 40-week MA flat/rising
  - price making higher high / higher low over swing windows
- Stage 4 avoidance:
  - price below declining 10-week MA
  - lower high / lower low structure
  - 10-week and/or 40-week MA slope negative

**MTC_V2 Bağlantısı:**

- `HTF Trend Gate` veya `Market Regime Gate` olarak uygundur.
- Producer sinyallerini filtrelemek için kullanılmalı.
- MTC_V2 parity açısından weekly HTF verisi dikkatli kullanılmalı: prior-closed semantics zorunlu.

**Prototype Priority:** `HIGH`

### Candidate C — Tight Base / Pivot Breakout Producer

**Amaç:** Uptrend içinde daralan volatilite, düşük hacim ve pivot kırılımını giriş sinyali yapmak.

**Kodlanabilir Kurallar:**

- Ön koşul:
  - Stage 2 regime aktif.
  - Fiyat 10-week / 50-day gibi trend MA üstünde.
- Tightness:
  - son `N` bar range yüzdesi ATR veya close’a göre daralıyor.
  - `range_pct = (highest(high, N) - lowest(low, N)) / close`
  - `range_pct <= threshold`
  - volume, son `N` barda average volume altına düşüyor veya volume slope negatif.
- Pivot:
  - `pivot_high = highest(high, N)[1]`
  - Entry pulse: `close > pivot_high` veya `high > pivot_high` ve close strong.
- Confirmation:
  - breakout bar closing range >= 0.65 / 0.70
  - volume relative average üstünde.

**Stop / Risk:**

- Base low veya pivot bar low altında stop.
- Alternatif: ATR-based stop.
- Risk, position sizing için seçim aracı olarak kullanılmalı; stop çok genişse trade filtrelenmeli.

**MTC_V2 Bağlantısı:**

- Bu doğrudan producer olabilir.
- `SIGNAL PRODUCER` altında `tight_base_pivot_breakout_v1`.
- `ENTRY GATES` ile stage, RS, volume ve market regime filtreleri eklenebilir.
- `POSITION SIZING` risk_pct + calculated SL ile yapılabilir.

**Prototype Priority:** `HIGH`

### Candidate D — Pullback / Drift-Back Continuation Setup

**Amaç:** Güçlü trend içinde fiyatın kısa/orta MA’ya kontrollü geri çekilip yeniden yukarı dönmesini almak.

**Kodlanabilir Kurallar:**

- Stage 2 trend aktif.
- Öncesinde impulse/uptrend var.
- Pullback:
  - price pulls back toward 10-day, 20-day, 21 EMA veya 10-week MA.
  - range daralıyor; volatilite düşüyor.
  - kırmızı hacim barları aşırı değil.
- Trigger:
  - inside bar high break
  - prior short-term pivot break
  - price reclaims moving average
  - closing range strong.
- Stop:
  - pullback low
  - inside bar low
  - MA altı + ATR buffer.

**MTC_V2 Bağlantısı:**

- Producer olabilir veya existing producer sinyalini iyileştiren transform/gate olarak kullanılabilir.
- `Level Retest` ve `Confirmation` modülleriyle uyumlu.
- Özellikle MTC_V2 SL/TP ve trailing altyapısı ile test edilmeli.

**Prototype Priority:** `MEDIUM-HIGH`

### Candidate E — Expectation Breaker / Failed Bearish Reaction Signal

**Amaç:** Kötü haber, zayıf market veya negatif beklentiye rağmen fiyatın beklenen düşüşü yapmaması durumunda güç sinyali üretmek.

**Not:** Bu video daha çok price action örneği üzerinden anlatıyor; haber/event verisi olmadan saf OHLCV ile kodlamak daha zordur.

**OHLCV Yaklaşımı:**

- Negatif bar / gap / market weakness sonrası fiyat düşük kapanmıyor.
- Closing range yüksek.
- Sonraki bar low kırılmadan yukarı devam ediyor.
- Weakness expected, but failure to go lower.

**MTC_V2 Bağlantısı:**

- İlk etapta producer yerine research feature olarak kalmalı.
- Event/news data yoksa `low_close_failure_reversal_v1` gibi sadece OHLCV proxy ile denenebilir.

**Prototype Priority:** `LOW-MEDIUM`

## 7. MTC_V2 İçin En Faydalı Alınacak Parçalar

### Producer Adayları

1. `tight_base_pivot_breakout_v1`
2. `pullback_driftback_continuation_v1`

### Gate / Filter Adayları

1. `weekly_closing_range_leadership_gate_v1`
2. `stage2_trend_regime_gate_v1`
3. `relative_strength_new_high_gate_v1`
4. `avoid_extended_entry_gate_v1`

### Risk / Position Management Adayları

1. Stop mesafesi çok genişse trade’i reddet.
2. Base/pivot stop ile ATR stop’u karşılaştır.
3. Breakout sonrası follow-through yoksa erken cut logic.
4. Trade sayısı / overtrading guard.
5. Market cycle negatifse long entry kapatma veya risk azaltma.

## 8. Python Prototype İçin Önerilen Minimum Deney Seti

### Deney 1 — Stage Filter Only

- Baseline producer: mevcut Supertrend veya Range Filter sinyali.
- Ek gate: weekly Stage 2 filter.
- Amaç: Stage 4 / downtrend dönemlerinde long zararlarını azaltıyor mu?

### Deney 2 — Tight Base Pivot Breakout

- Yeni producer: tight base + pivot breakout.
- Filtreler:
  - Stage 2 weekly trend
  - Volume confirmation
  - Closing range confirmation
- Exit:
  - ATR SL
  - R multiple TP
  - Time stop
  - Trend trailing

### Deney 3 — Pullback Drift-Back

- Giriş:
  - Trend aktif
  - Pullback MA civarına geliyor
  - Volatility contraction
  - Reclaim / inside bar break
- Exit:
  - Pullback low stop
  - ATR trailing
  - Opposite signal
  - Time stop.

### Deney 4 — Weekly Closing Range Leadership as Gate

- Piyasa düzeltmeleri sırasında güçlü kalan sembolleri işaretle.
- Bu gate açık/kapalı karşılaştır.
- Ölçümler:
  - trade count
  - win rate
  - average R
  - max drawdown
  - post-correction breakout performance.

## 9. Backtest / Optimization Uyarıları

Bu transcript doğrudan parametre seti vermiyor. Bu nedenle optimize edilecek parametreler dikkatli ve dar tutulmalı.

### Riskli Overfit Alanları

- Tightness threshold
- Closing range threshold
- Moving average period choice
- Relative strength lookback
- Pivot lookback
- Volume confirmation threshold
- Pullback depth

### Önerilen Parametre Aralıkları

```yaml
stage_filter:
  weekly_fast_ma: [10]
  weekly_slow_ma: [30, 40]
  fast_slope_lookback: [2, 3, 4]
  slow_slope_lookback: [3, 5]

closing_range:
  min_dcr: [0.60, 0.70, 0.80]
  min_wcr: [0.60, 0.70, 0.80]
  correction_weeks_required: [2, 3]
  correction_window: [4, 6]

tight_base:
  base_len: [8, 13, 21]
  max_range_pct: [0.06, 0.10, 0.15]
  atr_contraction_ratio: [0.60, 0.75, 0.90]
  volume_dryup_ratio: [0.60, 0.80, 1.00]

pivot_breakout:
  breakout_mode: ["close_above_pivot", "high_cross_with_strong_close"]
  min_breakout_dcr: [0.60, 0.70]
  min_rel_volume: [1.0, 1.2, 1.5]

pullback:
  ma_period: [10, 20, 21]
  max_pullback_depth_atr: [1.0, 1.5, 2.0]
  trigger: ["inside_bar_break", "ma_reclaim", "short_pivot_break"]
```

## 10. Video İçindeki Faydalı Ama Doğrudan Kodlanmaması Gereken Öğretiler

Bunlar Trader Wiki’ye alınmalı:

- Bilgi + deneyim ayrımı: kitaplardan ve model örneklerden gelen bilgi, piyasada uygulanarak deneyime dönüşür.
- Stage 1 / Stage 2 / Stage 3 trader gelişim modeli.
- Sistem atlama, randomness ve oversizing davranışları.
- FOMO’nun tamamen yok edilemeyeceği; sadece azaltılabileceği.
- Post-analysis’in Stage 1 ve Stage 2 trader için opsiyonel değil, zorunlu olması.
- Başkasının pivotuna körü körüne güvenmek yerine kendi watchlist ve routine sistemini kurmak.
- Trading’i iş gibi yönetmek: amaç, ölçüm, risk ve tekrar edilebilir süreç.

## 11. Red Flags / Şüpheli veya Eksik Noktalar

- Video eğitim/foundation formatında; tek bir strategy card gibi kesin entry/exit verilmiyor.
- Örnekler büyük ölçüde hisse senedi / growth stock odaklı. Crypto’ya doğrudan taşınırsa volume, benchmark ve fundamental context değişir.
- “Institutional accumulation” yorumu sadece OHLCV ile kesin kanıtlanamaz; proxy olarak kullanılmalı.
- Closing range ve tightness tek başına edge değildir; market regime ve risk yönetimi olmadan zayıf kalabilir.
- Relative strength line için benchmark seçimi kritik.
- Stage Analysis weekly HTF gerektirdiği için Pine/Python parity’de HTF alignment riski yüksek.

## 12. Kabul / Ret Kararı

### Neden Reject Değil?

- İçerik düşük kalite değil.
- Kodlanabilir teknik bileşenler var.
- Risk yönetimi, market regime, price/volume, post-analysis gibi QuantLens açısından değerli başlıklar içeriyor.

### Neden Sadece WIKI_ONLY Değil?

- Video sadece psikoloji veya genel tavsiye değil; closing range, stage filter, tight base, pivot, pullback gibi OHLCV tabanlı kodlanabilir yapılar içeriyor.

### Neden Direct Strategy Değil?

- Tek ve tamamlanmış entry/exit sistemi yok.
- Çok sayıda kavram var; doğrudan Pine’a geçmek yerine Python prototipte modül ayrıştırması yapılmalı.

## 13. Önerilen Dosya / Registry Kayıtları

Codex repo içinde çalışırken aşağıdaki kayıtları üretmeli veya güncellemeli:

```text
_registry/youtube_video_index.csv
  video_id = QzzKqmPcB3A
  normalized_url = https://www.youtube.com/watch?v=QzzKqmPcB3A
  status = CANDIDATE
  codex_status = READY_FOR_PYTHON_PROTOTYPE
  candidate_id = YT_QzzKqmPcB3A_20260503_A
  transcript_hash = c1fd46047b7ca1987aa1eea04634d281f9835921f129d7d152d131b94879d230
```

```text
research/youtube_intake/YT_QzzKqmPcB3A_20260503_A/
  intake_report.md
  transcript.md
  strategy_modules.md
  prototype_plan.md
```

Opsiyonel Trader Wiki:

```text
11_TRADER_WIKI/04_SYSTEM_DEVELOPMENT/TW_2026-05-03_system_foundation_ultimate_trading_guide.md
11_TRADER_WIKI/01_RISK_MANAGEMENT/TW_2026-05-03_risk_and_post_analysis_ultimate_trading_guide.md
```

## 14. Next Action

**Codex için önerilen sıradaki iş:**

1. Repo registry dosyalarını oku.
2. Duplicate değilse transcripti arşivle.
3. Bu videoyu tek strateji olarak değil, dört ayrı modül olarak işle:
   - `stage2_trend_regime_gate_v1`
   - `weekly_closing_range_leadership_gate_v1`
   - `tight_base_pivot_breakout_v1`
   - `pullback_driftback_continuation_v1`
4. İlk prototipi Python’da yap; Pine’a geçme.
5. MTC_V2 production dosyalarına dokunma.
6. Backtest/optimization bu intake aşamasında çalıştırma.
7. Sonraki batch analizinde bu video ile `5 Simple & Effective Trading Setups of Market Wizards` videosunu birlikte değerlendir; çünkü ikisi price/volume, tightness, pivot ve trend continuation konularında tamamlayıcı.

## 15. Dokunulmayan Dosyalar

Bu chat ortamında aşağıdaki dosyalara dokunulmadı:

- `01_PINE/MTC_V2.pine`
- Production Python runner dosyaları
- Backtest / optimization dosyaları
- Büyük CSV / data bundle / cache
- Secret veya API key içeren herhangi bir dosya

## 16. Final Verdict

```text
VERDICT: CANDIDATE
CODEX_STATUS: READY_FOR_PYTHON_PROTOTYPE
PRIMARY_EDGE_TYPE: PRICE_VOLUME_STAGE_ANALYSIS
IMPLEMENTATION_MODE: PYTHON_RESEARCH_FIRST
PINE_ALLOWED_NOW: NO
WIKI_NOTE: YES
DUPLICATE_STATUS: NOT_DUPLICATE_IN_CONVERSATION__EXTERNAL_REGISTRY_NOT_CHECKED
```
