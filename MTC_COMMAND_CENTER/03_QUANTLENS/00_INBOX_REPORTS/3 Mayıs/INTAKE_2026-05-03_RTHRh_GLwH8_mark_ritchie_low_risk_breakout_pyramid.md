# QuantLens Transcript Intake Report

## 1. Metadata

- Report ID: `INTAKE_2026-05-03_RTHRh_GLwH8`
- Source URL: https://youtu.be/RTHRh_GLwH8?si=NyxT_vvKDrHwMv64
- Normalized URL: https://www.youtube.com/watch?v=RTHRh_GLwH8
- Video ID: `RTHRh_GLwH8`
- Title: `100% Trading Returns - How to become a Super Trade with Mark Ritchie`
- Speaker / Guest: Mark Ritchie II
- Channel: `TraderLion / Trailline Podcast` *(transcriptten çıkarım; channel_id yok)*
- Intake Date: `2026-05-03`
- Transcript Archive Path: `/mnt/data/100% Trading Returns - How to become a Super Trade with Mark Ritchie.md`
- Transcript Hash SHA256: `e3d7302c1dd615b941cda69b07647f6edcaa7744979d12bbe106ee83cd7fa9e6`

## 2. Intake Verdict

- Classification: `CANDIDATE`
- Codex Status Önerisi: `READY_FOR_PYTHON_PROTOTYPE`
- Candidate ID: `QC_2026-05-03_RTHRh_GLwH8_LOW_RISK_BREAKOUT_PYRAMID`
- Confidence: `HIGH`
- Usefulness Score: `9/10`
- Strategy Coding Potential: `HIGH`
- Trader Wiki Value: `HIGH`, fakat ana çıktı `WIKI_ONLY` değil; çünkü transcript içinde kodlanabilir strateji ve risk/pozisyon yönetimi kuralları var.

## 3. Duplicate / Registry Kontrolü

### Bu konuşma içinde kontrol

- Önceki işlenen transcript: `_AAX1ylNbIE` / Market Wizards & Trading Legends.
- Bu video: `RTHRh_GLwH8`.
- Sonuç: `DUPLICATE_DETECTED = false`.

### Repo registry kontrolü

- `_registry/youtube_video_index.csv` bu konuşmaya yüklenmedi.
- `channel_blacklist.yaml` bu konuşmaya yüklenmedi.
- `channel_quality_registry.csv` bu konuşmaya yüklenmedi.
- Bu yüzden gerçek repo duplicate ve kanal blacklist kontrolü `NOT_VERIFIED_IN_REPO` olarak işaretlenmelidir.

## 4. Channel Quality Kararı

- Channel Quality State: `UNKNOWN`
- Sebep: Kanal adı transcriptten çıkarılıyor ama repo içindeki kanal kalite geçmişi yok.
- Blacklist kararı verilmedi.
- Bu video tek başına kaliteli / faydalı içerik sayılır.
- Önerilen registry etkisi: `candidate_count += 1`.

## 5. Kısa Özet

Bu transcript Mark Ritchie II'nin swing / momentum trading yaklaşımını anlatıyor. Ana tema, “düşük riskli giriş + sıkı stop + sermayeyi çalışan pozisyonlara taşıma + işler iyi giderken agresifleşme, işler kötü giderken küçülme” sistemidir.

Video klasik bir tek indikatör stratejisi vermiyor; fakat MTC_V2 için çok değerli üç kodlanabilir fikir veriyor:

1. **Low-risk breakout / tight pivot entry**
2. **Success-feedback exposure throttle**
3. **Financed pyramid / add-on management**

Bu nedenle video yalnızca Trader Wiki notu olarak bırakılmamalı; Python prototip adayı olarak alınmalıdır.

## 6. Ana Strateji Adayı

### Candidate Name

`LOW_RISK_BREAKOUT_WITH_ADAPTIVE_EXPOSURE_AND_FINANCED_PYRAMID`

### Ana fikir

Güçlü trend / güçlü tema içindeki enstrümanlarda, fiyat daralan bir yapıdan veya net pivot seviyesinden çıkar. Giriş sadece stop mesafesi mantıklı ve düşükse yapılır. Pozisyon ilerledikçe:

- zarar eden veya ilerlemeyen trade hızlı azaltılır,
- kâra geçen trade'de kısmi kâr alınır,
- stop break-even veya daha iyi seviyeye çekilir,
- sadece çalışan pozisyona ekleme yapılır,
- son birkaç trade kötü ise yeni risk azaltılır,
- son birkaç trade ve equity curve iyi ise risk kontrollü şekilde artırılır.

## 7. Kodlanabilir Kurallar

### 7.1 Market / Regime Filter

İlk prototipte long-only başlanmalı.

Önerilen koşullar:

- `close > sma50`
- `sma50 > sma200` veya `close > sma200`
- `sma50_slope > 0`
- Piyasa rejimi filtresi:
  - Crypto için: BTC veya toplam market proxy trend pozitif.
  - Equity için: index trend pozitif, örn. SPY/QQQ close > 50MA.

### 7.2 Setup Filter — Tight Pivot / Low-Risk Breakout

OHLCV ile kodlanabilir ilk set:

- Son `N=10-30` bar içinde daralma:
  - `range_pct = (highest(high, N) - lowest(low, N)) / close`
  - `range_pct < threshold`
- Volatilite daralması:
  - `atr_pct = atr(14) / close`
  - `atr_pct` son `M` bar ortalamasından düşük
- Pivot:
  - `pivot_high = highest(high, N)`
  - Entry trigger: `close > pivot_high[1]` veya `high > pivot_high[1]`
- Low-risk stop:
  - `initial_stop = recent_swing_low` veya `entry - atr_mult * ATR`
  - `stop_distance_pct <= max_stop_pct`
  - öneri: günlük equity swing için `max_stop_pct = 7-8%`; crypto intraday için ATR/tick uyarlı daha küçük eşik.

### 7.3 Volume / Demand Confirmation

- Breakout bar volume > `sma(volume, 20)` veya `volume_zscore > 0`.
- Alternatif: OBV/volume accumulation gate.
- Crypto verisinde hacim kalitesi exchange'e göre değişebileceği için bu filter opsiyonel olmalı.

### 7.4 Fundamental / Theme Proxy

Transcript equity growth stocks için fundamentals ve tema vurguluyor. MTC_V2 / crypto prototipinde direkt fundamentals yoksa şu proxy'ler kullanılabilir:

- Relative strength:
  - `asset_return_20d > benchmark_return_20d`
  - `asset_return_60d > benchmark_return_60d`
- Market leadership:
  - Top `X%` momentum universe filtresi.
- Theme/sector yerine:
  - major coin vs altcoin group strength
  - BTC/ETH regime
  - asset liquidity / average dollar volume.

İlk Python prototipinde fundamentals zorunlu yapılmamalı; ayrı bir araştırma katmanı olarak bırakılmalı.

## 8. Position Sizing / Risk Model

### 8.1 Sabit risk başlangıcı

- `risk_per_trade = base_risk_pct * equity`
- Pozisyon miktarı:
  - `qty = risk_per_trade / abs(entry_price - initial_stop)`
- Notional cap:
  - `notional <= max_notional_pct * equity`
- Leverage cap MTC_V2 sizing mantığına bağlanmalı.

### 8.2 Adaptive Exposure Throttle

Mark Ritchie'nin en güçlü kodlanabilir fikri budur.

Önerilen state değişkenleri:

- `recent_trade_R_sum`
- `recent_win_loss_streak`
- `equity_slope`
- `current_drawdown_pct`
- `market_regime_score`

Risk multiplier:

```text
risk_mult = 1.0

if last_3_trades_R < 0:
    risk_mult = 0.50

if consecutive_losses >= 2:
    risk_mult = 0.35

if consecutive_losses >= 3:
    risk_mult = 0.20 or NO_NEW_ENTRIES

if equity_close_to_high and last_3_trades_R > 0 and market_regime_positive:
    risk_mult = 1.25 to 1.50
```

İlk prototipte agresif multiplier düşük tutulmalı. Amaç kârı maksimize etmek değil; “kötü dönemde küçülme / iyi dönemde kontrollü büyüme” etkisini ölçmektir.

## 9. Pyramiding / Add-On Logic

### 9.1 Add-on şartları

Add-on sadece şu durumlarda izinli:

- İlk pozisyon kârda.
- Fiyat daha yüksek pivot veya tight range breakout üretiyor.
- Add price >= previous entry price.
- Stop yukarı taşındığında toplam portföy riski artmıyor.
- `current_total_R_at_risk <= allowed_R_at_risk`.

### 9.2 Financed add-on mantığı

Transcriptteki önemli yapı:

1. Giriş düşük riskli yapılır.
2. Fiyat hızlıca `+1.5R / +2R` bölgesine giderse kısmi kâr alınabilir.
3. Stop break-even veya daha iyi seviyeye çekilir.
4. Kâr alınan parça veya yükseltilen stop sayesinde kalan pozisyon “finanse edilmiş” hale gelir.
5. Daha büyük hareket için runner bırakılır.

Kodlanabilir versiyon:

```text
if unrealized_R >= 2.0:
    take_profit_partial = 0.33 to 0.50
    stop = max(stop, entry_price)

if add_signal and position_in_profit and risk_after_add <= original_risk:
    add_position()
```

## 10. Exit Model

### 10.1 Initial Stop

- Swing low stop:
  - `stop = lowest(low, stop_lookback)`
- ATR stop:
  - `stop = entry - atr_mult * ATR`
- Hybrid:
  - `stop = min/logical` değil; long için daha yakın ama mantıklı stop seçilmeli.
  - Çok yakın stop whipsaw yaratır; çok uzak stop low-risk entry mantığını bozar.

### 10.2 Failure-to-Progress Exit

Trade girişten sonra hızlı ilerlemiyorsa:

- `bars_since_entry >= X`
- `unrealized_R < min_progress_R`
- Exit veya partial reduce.

Örnek:

```text
if bars_since_entry >= 5 and max_unrealized_R < 0.75:
    reduce_or_exit
```

### 10.3 Partial Profit

- `TP1 = +2R`
- `TP1 qty = 33-50%`
- Stop break-even.

### 10.4 Runner Exit

- 50MA / 21EMA trail
- ATR trailing stop
- swing-low trailing stop
- trend break / close below moving average
- optional time stop.

## 11. MTC_V2 Mapping

### Signal Producer

Yeni producer olarak öneri:

`producer_low_risk_breakout_v1`

Alternatif olarak ilk aşamada mevcut RangeFilterHybrid / Supertrend producer değiştirilmeden yalnızca gate+position manager prototipi denenebilir.

### Entry Gates

- MA trend gate
- MA slope gate
- ATR volatility floor
- Volume gate
- Momentum / relative strength gate
- Level proximity / pivot gate
- Session gate, crypto için opsiyonel.

### Position Manager

- `max_entries` pyramiding için kullanılabilir.
- `allow_flip = false` ilk prototipte önerilir.
- `regime_lock = long_only` ilk prototipte önerilir.
- Add-on için `same_bar_reentry_allowed = false`.

### Position Sizing

MTC_V2'nin mevcut risk_pct, max_leverage_cap, notional check ve fallback sizing katmanları kullanılmalı.

Eklenmesi önerilen araştırma-only state:

- `adaptive_risk_multiplier`
- `consecutive_losses`
- `recent_R_window`
- `equity_near_high`
- `risk_after_add`.

### Exit Rules

Mevcut MTC_V2 exit altyapısına çok uygun:

- INITIAL_SL
- PARTIAL_TP
- BREAK_EVEN
- TRAIL
- TIME_STOP
- FILTER_BLOCK veya regime exit.

## 12. Python Prototype Planı

### Aşama 1 — OHLCV-only baseline

Amaç: Strategy idea saf fiyat verisiyle çalışıyor mu?

- Universe: likit crypto veya equity OHLCV dataset.
- Timeframe: günlük ve 4H ayrı test edilmeli.
- Entry:
  - trend positive
  - tight range
  - breakout above pivot
  - max stop distance cap
- Exit:
  - initial stop
  - 2R partial
  - BE
  - 21/50MA trail.

### Aşama 2 — Adaptive exposure

Baseline üzerine:

- Son 3-5 trade R toplamı
- Consecutive loss throttle
- Equity-high throttle
- Drawdown risk cut.

### Aşama 3 — Pyramiding

- Add-on only when profitable.
- Risk after add must not exceed original risk budget.
- Add-on stop layers ayrı takip edilmeli.
- Partial profit and runner state açık loglanmalı.

### Aşama 4 — Robustness

- Walk-forward
- Cross-market validation
- Commission/slippage sensitivity
- Regime split:
  - bull
  - bear
  - chop
  - high volatility
  - low volatility.

## 13. Backtest / Optimization Uyarısı

Bu intake aşamasında backtest veya optimization çalıştırılmadı.

Prompt gereği:

- `01_PINE/MTC_V2.pine` değiştirilmedi.
- Production Python runner değiştirilmedi.
- Backtest çalıştırılmadı.
- Optimization çalıştırılmadı.
- Büyük CSV / cache / data bundle oluşturulmadı.
- Secret / API key / webhook yazılmadı.

## 14. Riskli veya Şüpheli İddialar

- Başlıktaki “100% Trading Returns” ifadesi pazarlama dili olabilir; doğrudan getiri beklentisi olarak alınmamalı.
- Strateji büyük ölçüde discretionary chart reading içeriyor; tamamen mekanik hale getirmek overfit riski taşır.
- Equity growth-stock mantığı crypto piyasasına birebir taşınmayabilir.
- Fundamentals ve tema filtresi OHLCV-only backtestte eksik kalabilir.
- “Büyük pozisyon” fikri yanlış uygulanırsa risk artar; burada amaç pozisyon büyütmek değil, toplam R riskini artırmadan timing iyi olduğunda notional artırmaktır.
- Pyramiding ve partial exits Pine/Python parity açısından karmaşık olabilir; önce Python araştırma prototipi yapılmalı.

## 15. QuantLens İçin Değer

### Neden önemli?

Bu video tek bir indikatörden çok daha değerli bir sistem mantığı veriyor:

- giriş kalitesi
- risk kalitesi
- exposure yönetimi
- başarısız dönemde küçülme
- başarılı dönemde kontrollü agresifleşme
- trade sonrası analiz
- strategy-as-employee yaklaşımı.

### QuantLens / MTC_V2 açısından en iyi kullanım

Bu transcript doğrudan “bir strateji” değil, MTC_V2'nin position management ve risk engine katmanını iyileştirecek bir modeldir.

Özellikle şu modüller için değerlidir:

- Adaptive risk sizing
- Portfolio-level guard
- Add-on / pyramiding rules
- Partial TP + BE + runner logic
- Low-risk entry gate
- Failure-to-progress exit.

## 16. Önerilen Dosya / Registry Çıktıları

Bu rapor repo içinde işlenecekse önerilen kayıtlar:

### Candidate folder

```text
06_QUANTLENS_LAB/candidates/QC_2026-05-03_RTHRh_GLwH8_LOW_RISK_BREAKOUT_PYRAMID/
```

### Candidate note

```text
06_QUANTLENS_LAB/candidates/QC_2026-05-03_RTHRh_GLwH8_LOW_RISK_BREAKOUT_PYRAMID/INTAKE.md
```

### Registry row önerisi

```csv
video_id,normalized_url,title,channel,status,candidate_id,transcript_hash,first_seen_at,last_seen_at,process_count
RTHRh_GLwH8,https://www.youtube.com/watch?v=RTHRh_GLwH8,"100% Trading Returns - How to become a Super Trade with Mark Ritchie","TraderLion / UNKNOWN_CHANNEL_ID",CANDIDATE,QC_2026-05-03_RTHRh_GLwH8_LOW_RISK_BREAKOUT_PYRAMID,e3d7302c1dd615b941cda69b07647f6edcaa7744979d12bbe106ee83cd7fa9e6,2026-05-03,2026-05-03,1
```

### Channel registry önerisi

```csv
channel,quality_state,candidate_count,wiki_count,reject_count,stop_count,last_video_id,last_status
"TraderLion / UNKNOWN_CHANNEL_ID",UNKNOWN,1,0,0,0,RTHRh_GLwH8,CANDIDATE
```

## 17. Codex Next Action

Bu transcript için önerilen sonraki adım:

1. Repo registry duplicate kontrolünü gerçek dosyalardan yap.
2. Duplicate değilse `QC_2026-05-03_RTHRh_GLwH8_LOW_RISK_BREAKOUT_PYRAMID` candidate klasörü oluştur.
3. Bu raporu candidate klasörüne `INTAKE.md` olarak koy.
4. Python araştırma prototipi için draft spec oluştur:
   - producer_low_risk_breakout_v1
   - adaptive_risk_multiplier_v1
   - financed_pyramid_manager_v1
5. İlk etapta Pine'a geçme.
6. Production runner değiştirme.
7. Backtest/optimization sadece ayrı onaylı araştırma aşamasında çalıştır.

## 18. Final Karar

```text
VERDICT: CANDIDATE
CODEX_STATUS: READY_FOR_PYTHON_PROTOTYPE
PRIMARY_EDGE: Low-risk breakout + adaptive exposure + financed pyramiding
PINE_NOW: NO
PYTHON_RESEARCH_NOW: YES, but only after repo duplicate check and in isolated research path
MTC_V2_RELEVANCE: HIGH
WIKI_ONLY: NO
DUPLICATE: NOT_DETECTED_IN_CURRENT_BATCH
REPO_DUPLICATE_CHECK: NOT_VERIFIED
```
