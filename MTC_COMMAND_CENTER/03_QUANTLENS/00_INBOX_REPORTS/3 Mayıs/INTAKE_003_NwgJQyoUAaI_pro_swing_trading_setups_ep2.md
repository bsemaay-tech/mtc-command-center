# QuantLens Transcript Intake Report — 003 / 068

## 1. Metadata

- **Report ID:** `INTAKE_003_NwgJQyoUAaI`
- **Source URL:** `https://youtu.be/NwgJQyoUAaI?si=IuOBlOwf_231Oftz`
- **Normalized URL:** `https://www.youtube.com/watch?v=NwgJQyoUAaI`
- **Video ID:** `NwgJQyoUAaI`
- **Title:** `Pro Swing Trading Setups For Consistent Gains Ultimate Trading Guide Ep 2`
- **Series / Theme:** Ultimate Trading Guide — Webinar 2, mindset, edges, setups
- **Channel:** `UNKNOWN_CHANNEL`
  - Transcript içinde webinar/TraderLion tarzı seri bağlamı var, fakat kanal adı ve kanal id güvenilir metadata olarak verilmedi. Intake kuralına göre `UNKNOWN_CHANNEL` kullanıldı.
- **Source transcript file:** `Pro Swing Trading Setups For Consistent Gains Ultimate Trading Guide Ep 2.md`
- **Prompt file used:** `00_quantlens_transcript_intake_prompt.md`
- **Generated date:** `2026-05-03`
- **Transcript hash method:** lowercase + whitespace-normalized SHA256 over full transcript text
- **Transcript hash:** `40629a31dc690de260df76521da2b7c448e06d06e32ec74553fdb71ef45aa407`

---

## 2. Intake Verdict

- **Classification:** `CANDIDATE`
- **Codex Status Önerisi:** `READY_FOR_PYTHON_PROTOTYPE`
- **Candidate Priority:** `P1 — Core framework; prototype after Ep3 entry-tactic primitives`
- **Usefulness Score:** `9 / 10`
- **Coding Readiness Score:** `7 / 10`
- **MTC_V2 Fit Score:** `8 / 10`
- **Wiki Note Also Valuable:** `YES`

### Verdict Summary

Bu transcript yalnızca psikoloji veya eğitim notu değil; **edge + setup + risk framework** içerdiği için `CANDIDATE` olarak işlenmelidir.

Video, tek bir mekanik indikatör stratejisinden çok şu çekirdek çerçeveyi anlatıyor:

> Başarılı trading framework'u; **mindset**, **edge** ve **setup** üçlüsünden oluşur. Edge; geçmiş lider hisselerde tekrarlayan kazanma karakteristiğidir. Setup; edge'i trade edilebilir, risk yönetilebilir formasyona dönüştürür. Amaç “para kazanmak” diye acele etmek değil; equity curve'ün aşağı gitmesini durdurup sistematik şekilde stage 1 → stage 2 → stage 3 ilerlemektir.

Kodlanabilir taraflar özellikle şunlardır:

- High Volume Edge / HVE
- Relative Strength Edge / RS
- Launchpad setup
- Gapper setup
- Up-the-right-side setup
- Pullback to support / moving average setup
- Setup-context scoring
- Equity-curve defensive mode / exposure throttle fikri

Bu nedenle rapor hem **strategy candidate** hem de **Trader Wiki** açısından değerlidir.

---

## 3. Duplicate / Registry Check

### Current Environment Check

- `_registry/youtube_video_index.csv` dosyası bu konuşmada verilmedi.
- `channel_blacklist.yaml` dosyası bu konuşmada verilmedi.
- `channel_quality_registry.csv` dosyası bu konuşmada verilmedi.

### Result

- **Duplicate status:** `NOT_VERIFIED_AGAINST_REPO_REGISTRY`
- **Current conversation duplicate:** `NO_DUPLICATE_DETECTED`
- **Known current batch conflict:** `NO`
  - `001` video id: `Lot25-2fb-4`
  - `002` video id: `oZH6_XRxtDc`
  - Bu video id: `NwgJQyoUAaI`
- **Action:** Bu rapor yeni candidate olarak üretildi; gerçek repo'ya yazılmadan önce Codex registry dosyalarını okuyup `video_id` ve `transcript_hash` ile duplicate kontrolünü tekrar yapmalıdır.

### Registry Row Draft

```csv
video_id,normalized_url,title,channel,status,candidate_id,transcript_hash,first_seen_at,last_seen_at,process_count
NwgJQyoUAaI,https://www.youtube.com/watch?v=NwgJQyoUAaI,"Pro Swing Trading Setups For Consistent Gains Ultimate Trading Guide Ep 2",UNKNOWN_CHANNEL,CANDIDATE,CAND_20260503_SETUP_FRAMEWORK_NwgJQyoUAaI,40629a31dc690de260df76521da2b7c448e06d06e32ec74553fdb71ef45aa407,2026-05-03,2026-05-03,1
```

---

## 4. Channel Quality Check

- **Channel:** `UNKNOWN_CHANNEL`
- **Blacklist decision:** `NO_BLACKLIST_DECISION`
- **Reason:** Kanal adı / kanal id güvenilir şekilde verilmediği için blacklist veya watchlist kararı verilmedi.
- **Suggested quality update after repo check:** Eğer kanal daha önce işlenmemişse `UNKNOWN`; bu video sonucu faydalı ve candidate olduğu için `candidate_count += 1`.
- **Batch pattern note:** Bu seri içinde 002 ve 003 aynı eğitim zincirinin parçaları gibi görünüyor. Aynı kanal için ileride en az 3 faydalı çıktı oluşursa kanal `GOOD` durumuna aday olabilir.

---

## 5. Strategy Candidate

### Candidate ID

`CAND_20260503_SETUP_FRAMEWORK_NwgJQyoUAaI`

### Candidate Name

**HV/RS Setup Framework — Launchpad, Gapper, Up-the-Right-Side**

### Strategy Family

- Momentum leadership
- Breakout / continuation
- Relative strength
- High-volume catalyst continuation
- Setup-context scoring
- Risk-first discretionary system formalization

### Primary Market

- **Best native fit:** US equities
- **Reason:** Transcript; highest volume days, earnings gaps, leading stocks, group strength, moving averages and historical model-book examples üzerine kurulu.
- **Crypto adaptation:** Possible but secondary. Crypto'da earnings catalyst yoktur; HVE ve RS tarafı “abnormal volume + benchmark relative strength + regime” şeklinde uyarlanabilir. Launchpad / moving-average compression ise crypto OHLCV üzerinde daha doğrudan test edilebilir.

---

## 6. Candidate Structure — Framework Level

Bu video, 002 gibi entry tactic kütüphanesi değil; 002'nin üzerine oturacağı **framework / context layer** olarak düşünülmelidir.

```text
TRADING FRAMEWORK
  ├─ Mindset Layer
  │   ├─ Equity curve defense
  │   ├─ Stop losing money first
  │   ├─ Consistency of input/output
  │   ├─ Routine/habit discipline
  │   └─ Treat trading as business
  │
  ├─ Edge Layer
  │   ├─ High Volume Edge
  │   ├─ Relative Strength Edge
  │   ├─ Leadership stock behavior
  │   └─ Group / theme strength
  │
  ├─ Setup Layer
  │   ├─ Launchpad
  │   ├─ Gapper
  │   ├─ Up-the-right-side
  │   └─ Pullback to support / moving average
  │
  └─ Execution Layer
      ├─ Entry tactic selected from Ep3 library
      ├─ Tight/logical risk definition
      ├─ Position size from risk distance
      └─ Exit/invalidation if setup fails
```

MTC_V2 açısından bu yapı **Signal Producer'dan önceki context scorer** ve **Entry Gates** tarafında daha değerlidir.

---

## 7. Core Concepts Extracted

### 7.1 Three Pillars

Transcriptin ana öğretisi:

```text
1. Mindset
2. Edge
3. Setup
```

Bu üçlü olmadan trade mekanik hale getirilemez. Özellikle yeni trader için hedef, “hemen para kazanmak” değil; önce equity curve'ün aşağı gitmesini durdurmak ve tekrarlı davranış geliştirmektir.

### 7.2 Edge Definition

Video edge'i şu şekilde ele alıyor:

```text
Edge = geçmiş kazananlarda tekrar eden kazanma karakteristiği.
```

Bu karakteristik teknik veya temel olabilir. Transcriptte öne çıkan iki görsel edge:

1. **High Volume Edge**
   - Highest volume ever / highest volume in 1 year / highest volume since IPO.
   - Büyük talep veya kurumsal ilgi izlenimi.
   - Lider hisselerin büyük hareketlerinden önce sık tekrar eden karakteristik.

2. **Relative Strength Edge**
   - Market düşerken veya sıkışırken hissenin daha güçlü kalması.
   - Hissenin veya grubun benchmark'a göre outperform etmesi.
   - Market toparlandığında baskının kalkmasıyla daha iyi follow-through potansiyeli.

### 7.3 Setup Definition

Setup; edge'in trade edilebilir formudur. Setup, tek başına entry değildir. Setup'ın görevi:

- Edge'i bağlama oturtmak.
- Risk seviyesini tanımlanabilir hale getirmek.
- Entry tactic uygulanabilir hale getirmek.
- Position sizing için risk mesafesi üretmek.

### 7.4 Ruthless Mastery / Model Book

Transcriptte defalarca vurgulanan fikir:

```text
Bir edge veya setup seç; yüzlerce/ binlerce örnek topla; aynı şeyi tekrar tekrar çalış; sonra gerçek zamanlı güven oluşur.
```

Bu, QuantLens için çok önemli. Çünkü video bir “hazır indikatör” değil, model-book mantığıyla sistematik feature extraction öneriyor.

---

## 8. Extracted Setup Modules

## 8.1 High Volume Edge / HVE Detector

### Concept

Bir hissenin geçmişine göre olağandışı yüksek hacim üretmesi. Video bunu winning characteristic olarak görüyor.

### Candidate Logic

```text
hve_ever = volume == max(volume, full_history)
hve_1y = volume >= rolling_max(volume, 252)
hve_since_earnings = volume >= rolling_max(volume, bars_since_last_earnings)
relative_volume = volume / sma(volume, 50)

high_volume_edge = hve_ever OR hve_1y OR relative_volume >= threshold
```

### Quality Filters

```text
close_range = (close - low) / max(high - low, tick_size)
gap_pct = open / close[1] - 1
price_change_pct = close / close[1] - 1
```

Preferred:

- strong close range, örn. `close_range >= 0.50`
- price above key moving averages
- market regime supportive
- dollar volume sufficient

### MTC_V2 Mapping

- `Entry Gate`: HVE event varsa setup quality yükselir.
- `Signal Producer helper`: HVE günü event olarak işaretlenebilir.
- `Position Sizing`: edge quality skoru risk tier'e etki edebilir; ancak ilk prototype'ta sabit risk kullanılmalı.

---

## 8.2 Relative Strength Edge Detector

### Concept

Hissenin benchmark'a göre daha güçlü davranması. Transcriptte market environment iyi olduğunda başarı olasılığının arttığı, kötü olduğunda düştüğü açıkça vurgulanıyor.

### Candidate Logic

```text
benchmark_return_n = benchmark_close / benchmark_close[n] - 1
symbol_return_n = close / close[n] - 1
rs_score_n = symbol_return_n - benchmark_return_n

rs_edge = rs_score_20d > threshold
          AND close_above_ma(symbol, 21 or 50)
          AND symbol_drawdown < benchmark_drawdown
```

### Extra Group Layer

```text
group_rs_edge = median(group_symbol_returns_20d) > benchmark_return_20d
```

### MTC_V2 Mapping

- `Entry Gate`: benchmark RS filter.
- `PortfolioState / external guard`: group/theme strength optional.
- `Market Regime`: supportive/neutral/hostile context.

---

## 8.3 Launchpad Setup

### Concept

Correction sonrası 21 SMA, 50 SMA ve 65 EMA gibi hareketli ortalamaların birbirine yaklaşması; fiyatın tight/consolidated davranması; sonra hacimle yukarı genişleme.

### Candidate Logic

```text
ma21 = sma(close, 21)
ma50 = sma(close, 50)
ema65 = ema(close, 65)
ma_spread_pct = (max(ma21, ma50, ema65) - min(ma21, ma50, ema65)) / close

ma_compression = ma_spread_pct <= compression_threshold
price_constructive = close near_or_above ma cluster
volume_contracting = sma(volume, 5) < sma(volume, 20)
breakout = close > recent_range_high AND volume > sma(volume, 20)

launchpad_setup = ma_compression AND price_constructive AND volume_contracting
launchpad_trigger = launchpad_setup AND breakout
```

### Initial Stop Ideas

```text
stop = min(recent_swing_low, ma_cluster_low - buffer)
```

### Notes

- Çok iyi kodlanabilir.
- En güçlü setup adaylarından biri.
- Crypto dahil OHLCV olan her piyasada test edilebilir.

---

## 8.4 Gapper Setup

### Concept

Güçlü gap + yüksek hacim + iyi closing range. Özellikle hareketin erken aşamasındaki ilk güçlü gap tercih ediliyor.

### Candidate Logic

```text
gap_pct = open / close[1] - 1
rv = volume / sma(volume, 50)
close_range = (close - low) / max(high - low, tick_size)

gapper_setup = gap_pct >= min_gap_pct
               AND rv >= min_relative_volume
               AND close_range >= min_close_range
               AND price > ma50
```

### Edge Enhancers

- highest volume in 1y
- gap at/near 52-week high
- first gap after long base
- market in uptrend
- group/theme acting well

### Risks

- Earnings-gap edge US equities ağırlıklıdır.
- Daily data ile gapper tespit edilebilir; intraday entry için ayrıca 5m/15m veri gerekir.

---

## 8.5 Up-the-Right-Side Setup

### Concept

Stock büyük base'in sağ tarafında yükselirken veya breakout sonrası ilk tight pullback'lerde giriş fırsatları verir. Lider hisseler tek giriş değil, çoklu entry noktası üretir.

### Candidate Logic

```text
right_side_context = close > ma21 AND ma21 > ma50
recent_base_low = rolling_min(low, base_window)
base_recovery_pct = close / recent_base_low - 1

constructive_pullback = pullback_depth <= max_depth
                       AND volume_contracting
                       AND close holds above ma21 or prior_pivot

trigger = close > short_range_high
```

### Notes

- Tek başına producer olmamalı; HVE/RS sonrası continuation entry olarak kullanılmalı.
- Ep3'teki range breakout / pullback support entry taktikleriyle birleşir.

---

## 8.6 Pullback to Support / Moving Average

### Concept

Güçlü trend sonrası fiyatın 21 EMA, 50 SMA, base pivot, HVC veya anchored VWAP gibi destek bölgelerine düşük hacimle geri çekilmesi; sonra destekten güç göstermesi.

### Candidate Logic

```text
support_level = choose(ma21, ma50, prior_base_pivot, hvc_level, anchored_vwap)
distance_to_support = abs(close - support_level) / close
low_volume_pullback = sma(volume, 3) < sma(volume, 20)
support_hold = low <= support_level * (1 + tolerance) AND close > support_level
reclaim_trigger = close > high[1] OR close > short_range_high

pullback_support_setup = trend_context AND low_volume_pullback AND support_hold
```

### Stop

```text
stop = support_level - buffer
OR stop = pullback_swing_low - buffer
```

---

## 9. MTC_V2 Mapping

### Recommended Integration Layer

| Concept | MTC_V2 Layer | Notes |
|---|---|---|
| Equity-curve mindset | PortfolioState / risk guard | Use as exposure throttle, not signal |
| High Volume Edge | Entry Gate / setup context scorer | Event + quality score |
| Relative Strength Edge | Entry Gate | Benchmark-relative filter |
| Group strength | External market context / universe scanner | Optional later |
| Launchpad setup | Signal Producer or setup context | Good isolated detector candidate |
| Gapper setup | Signal Producer helper | US equities only unless adapted |
| Up-the-right-side | Signal Transform / Entry Gate | Requires prior edge state |
| Pullback to support | Signal Producer / Entry Gate | Needs support hierarchy |
| Model-book evidence | Research workflow | Build curated examples before optimization |

### MTC_V2 Implementation Warning

- `01_PINE/MTC_V2.pine` **değiştirilmemeli**.
- Production Python runner **değiştirilmemeli**.
- Backtest veya optimization **çalıştırılmamalı**.
- Önce isolated research folder ve detector stubs oluşturulmalı.

Suggested folder:

```text
06_QUANTLENS_LAB/research/setup_framework_003/
  README.md
  edge_definitions.md
  setup_taxonomy.md
  features_hve.py
  features_rs.py
  detect_launchpad.py
  detect_gapper.py
  detect_pullback_support.py
  event_label_schema.md
  tests/
```

---

## 10. Candidate Event Taxonomy Draft

```json
{
  "event_type": "SETUP_CONTEXT_SIGNAL",
  "video_id": "NwgJQyoUAaI",
  "candidate_id": "CAND_20260503_SETUP_FRAMEWORK_NwgJQyoUAaI",
  "symbol": "EXAMPLE",
  "timeframe": "1D",
  "edge_family": "HIGH_VOLUME_EDGE | RELATIVE_STRENGTH_EDGE | GROUP_RS_EDGE",
  "setup_family": "LAUNCHPAD | GAPPER | UP_RIGHT_SIDE | PULLBACK_SUPPORT",
  "trigger_type": "CONTEXT_READY | ENTRY_TRIGGER",
  "trigger_price": 0.0,
  "initial_stop": 0.0,
  "risk_distance_pct": 0.0,
  "setup_score": 0,
  "edge_score": 0,
  "market_regime": "SUPPORTIVE | NEUTRAL | HOSTILE",
  "invalidation_reason": "MA_CLUSTER_LOST | GAP_LOW_BROKEN | SUPPORT_LOST | RS_FAILED | REGIME_HOSTILE"
}
```

---

## 11. Backtest / Validation Plan

### Goal

İlk hedef “karlı strateji bulmak” değil; videodaki setup kavramlarının doğru etiketlenip etiketlenemediğini ölçmek.

### Step 1 — Manual Model Book

Örnek listesi transcriptte geçen ve önceki intake'lerle bağlantılı örneklerden kurulmalı:

- COUP / Coupa Software — Launchpad örneği
- TWLO — Gapper / HVE örneği
- SNAP — HVE continuation örneği
- UBER — Pullback support örneği
- NIO — Up-the-right-side / tight pullback örneği
- CELH — HVE + continuation / 002 ile bağlantılı
- NVDA / SMCI / TSLA — önceki intake'lerden leadership momentum bağlamı

### Step 2 — Detector Accuracy

Her detector için beklenen event tarihine yakın sinyal üretimi kontrol edilmeli.

```text
precision_sample = manually_confirmed_signals / all_detector_signals_sampled
recall_sample = detected_known_examples / known_examples
```

### Step 3 — Outcome Labels

```text
MFE_5d, MFE_10d, MFE_20d
MAE_5d, MAE_10d, MAE_20d
hit_stop_before_2R
reached_1R_2R_3R
```

### Step 4 — Regime Filter

```text
SPY_above_50d
QQQ_above_50d
benchmark_20d_return
breadth_proxy
market_closing_range
```

### Step 5 — No Optimization Yet

Önce detector ve event labels doğrulanmalı. Optimization ancak 10+ videodan gelen candidate havuzu birlikte değerlendirildikten sonra yapılmalı.

---

## 12. Risks / Suspicious or Non-Systematic Claims

### 12.1 Discretionary Experience Bias

Video çok güçlü framework anlatıyor; ancak anlatan kişiler patternleri görsel/discretionary şekilde tanıyor. Kod, bu sezgiyi basitleştireceği için false positive üretebilir.

### 12.2 Survivorship Bias

Örneklerin çoğu geçmiş lider hisselerden geliyor. Detector tüm likit universe üzerinde test edilmezse sonuçlar aşırı iyimser olur.

### 12.3 US Equity Specificity

HVE, earnings gap ve group leadership tarafı en doğal olarak US equities'e uygundur. Crypto/FX için adaptation gerekir.

### 12.4 Market-Regime Dependence

Transcriptte market environment vurgusu güçlüdür. Aynı setup bear markette düşük başarı verebilir. MTC tarafında regime gate olmadan bu candidate test edilmemeli.

### 12.5 Overfitting Risk

Launchpad, HVE, RS, gapper, moving average compression, close range ve pullback support birlikte optimize edilirse overfit riski artar. İlk aşama: tekil detector doğrulama.

---

## 13. Trader Wiki Note Also Recommended

Bu video Trader Wiki'ye ayrıca alınmalı. Çünkü strateji adayı yanında sistem tasarımı, psikoloji ve trader gelişim süreci açısından çok güçlü.

### Suggested Wiki Entry

- **Wiki status:** `ALSO_CREATE_WIKI_NOTE`
- **Topic:** `04_SYSTEM_DEVELOPMENT` + `02_TRADING_PSYCHOLOGY` + `01_RISK_MANAGEMENT`
- **Suggested file name:** `TW_2026-05-03_04_SYSTEM_DEVELOPMENT_three_pillars_edges_setups_ep2.md`

### Wiki Themes

- Para kazanmak hedef değil; para iyi prosesin yan ürünüdür.
- Önce equity curve aşağı gitmeyi bırakmalı.
- Edge, geçmiş liderlerde tekrar eden winning characteristic'tir.
- Setup, edge'i risk yönetilebilir trade formuna dönüştürür.
- Başarılı trader aynı şeyi tekrar eder; sürekli sistem değiştirmez.
- Model book ve binlerce örnek, confidence üretir.
- Longevity, excitement'tan daha önemlidir.

---

## 14. Codex Next Action

### Immediate Task

```text
Create isolated research folder for INTAKE_003 setup framework.
Do not modify MTC_V2 Pine.
Do not modify production Python runner.
Do not run backtests or optimization.
Implement detector stubs and unit-test fixtures only for:
1. High Volume Edge
2. Relative Strength Edge
3. Launchpad
4. Gapper
5. Pullback to Support
```

### Suggested Codex Prompt

```text
Read INTAKE_003_NwgJQyoUAaI_pro_swing_trading_setups_ep2.md.
Before making changes, inspect repo registry files for duplicate video_id=NwgJQyoUAaI and transcript_hash=40629a31dc690de260df76521da2b7c448e06d06e32ec74553fdb71ef45aa407.
If duplicate exists, stop and report duplicate details.
If not duplicate, create an isolated research folder under 06_QUANTLENS_LAB/research/setup_framework_003/.
Do not modify 01_PINE/MTC_V2.pine.
Do not modify production Python runner files.
Do not run backtests or optimization.
Implement feature-detector stubs and unit-test fixtures only for High Volume Edge, Relative Strength Edge, Launchpad, Gapper, and Pullback to Support.
Prepare README.md with formulas, assumptions, validation examples, and next steps.
Also draft a Trader Wiki note for three pillars / edge / setup / equity curve mindset.
```

---

## 15. Files Created / Not Touched

### Created by this intake step

```text
INTAKE_003_NwgJQyoUAaI_pro_swing_trading_setups_ep2.md
```

### Not touched

```text
01_PINE/MTC_V2.pine
Production Python runner files
Backtest data bundles
Optimization result folders
Broker / webhook / API key files
```

---

## 16. Final Decision

```text
Classification: CANDIDATE
Codex Status: READY_FOR_PYTHON_PROTOTYPE
Candidate Type: Setup/context framework + detector library
Primary Implementation Target: Python research prototype
Pine Implementation: Later, only after detector validation
Registry Update Needed: Yes, after repo duplicate check
Trader Wiki Note: Yes, also recommended
```

Bu transcript 002 ile birlikte düşünülmeli: 003, **hangi edge ve setup bağlamında işlem aranacağını** tanımlar; 002 ise **bu bağlam içinde nasıl entry yapılacağını** detaylandırır. İlk videodaki episodic pivot / progressive exposure fikriyle birleştirildiğinde QuantLens için güçlü bir momentum leadership research backbone'u oluşur.
