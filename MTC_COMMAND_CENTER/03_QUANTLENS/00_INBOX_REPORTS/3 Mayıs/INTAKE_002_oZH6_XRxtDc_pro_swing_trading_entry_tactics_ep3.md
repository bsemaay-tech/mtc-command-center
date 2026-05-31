# QuantLens Transcript Intake Report — 002 / 068

## 1. Metadata

- **Report ID:** `INTAKE_002_oZH6_XRxtDc`
- **Source URL:** `https://youtu.be/oZH6_XRxtDc?si=ar7mxK0F7O5fbnBZ`
- **Normalized URL:** `https://www.youtube.com/watch?v=oZH6_XRxtDc`
- **Video ID:** `oZH6_XRxtDc`
- **Title:** `Pro Swing Trading Entry Tactics Ultimate Trading Guide Ep3`
- **Series / Theme:** Ultimate Trading Guide — Webinar 3, setups and entry tactics
- **Channel:** `UNKNOWN_CHANNEL`
  - Transcript içinde “TraderLion / Trader Land” benzeri ifade geçiyor gibi görünüyor, fakat kanal adı ve kanal id güvenilir metadata olarak verilmedi. Intake kuralına göre `UNKNOWN_CHANNEL` kullanıldı.
- **Source transcript file:** `Pro Swing Trading Entry Tactics Ultimate Trading Guide Ep3.md`
- **Prompt file used:** `00_quantlens_transcript_intake_prompt.md`
- **Generated date:** `2026-05-03`
- **Transcript hash method:** lowercase + whitespace-normalized SHA256 over full transcript text
- **Transcript hash:** `a4f5b49fbe115200d4c460faffc7d221a8bf24d050369eca3be0307cd09c41c8`

---

## 2. Intake Verdict

- **Classification:** `CANDIDATE`
- **Codex Status Önerisi:** `READY_FOR_PYTHON_PROTOTYPE`
- **Candidate Priority:** `P0 / P1 — High-value framework; implement as modular prototype first`
- **Usefulness Score:** `9.5 / 10`
- **Coding Readiness Score:** `8 / 10`
- **MTC_V2 Fit Score:** `8.5 / 10`
- **Wiki Note Also Valuable:** `YES`

### Verdict Summary

Bu transcript doğrudan **kodlanabilir entry tactic kütüphanesi** içeriyor. Bu nedenle `WIKI_ONLY` değil, net şekilde `CANDIDATE` olarak işlenmelidir.

Ana fikir tek bir basit indikatör değil; daha çok şu yapıdır:

> Önce güçlü bir **edge** gözlenir: High Volume Edge veya Relative Strength Edge. Sonra bu edge’in içinde, tight/logical stop üretmeye uygun kısa vadeli entry tactic aranır: High Volume Close, Volume Support, Whole Number Support, Range Breakout, Undercut & Rally, Oops Reversal, Opening Range Breakout veya Pullback to Support.

Bu video MTC_V2 için çok değerli çünkü mevcut MTC mimarisindeki “Signal Producer → Signal Transform → Entry Gates → Position Manager → Position Sizing → Exit Rules” akışına doğrudan oturabilecek modüller tarif ediyor. Ancak ilk aşamada Pine’a geçmek doğru değildir. Önce Python tarafında feature extraction + event labeling + backtest prototype yapılmalıdır.

---

## 3. Duplicate / Registry Check

### Current Environment Check

- `_registry/youtube_video_index.csv` dosyası bu konuşmada verilmedi.
- `channel_blacklist.yaml` dosyası bu konuşmada verilmedi.
- `channel_quality_registry.csv` dosyası bu konuşmada verilmedi.

### Result

- **Duplicate status:** `NOT_VERIFIED_AGAINST_REPO_REGISTRY`
- **Current conversation duplicate:** `NO_DUPLICATE_DETECTED`
- **Known current batch conflict:** `NO`, önceki işlenen video `Lot25-2fb-4` idi; bu video id `oZH6_XRxtDc`.
- **Action:** Bu rapor için yeni candidate önerisi üretildi; gerçek repo’ya işlenmeden önce Codex’in registry dosyalarını okuyup `video_id` ve `transcript_hash` üzerinden tekrar kontrol etmesi gerekir.

### Registry Row Draft

```csv
video_id,normalized_url,title,channel,status,candidate_id,transcript_hash,first_seen_at,last_seen_at,process_count
oZH6_XRxtDc,https://www.youtube.com/watch?v=oZH6_XRxtDc,"Pro Swing Trading Entry Tactics Ultimate Trading Guide Ep3",UNKNOWN_CHANNEL,CANDIDATE,CAND_20260503_ENTRY_TACTICS_LIBRARY_oZH6_XRxtDc,a4f5b49fbe115200d4c460faffc7d221a8bf24d050369eca3be0307cd09c41c8,2026-05-03,2026-05-03,1
```

---

## 4. Channel Quality Check

- **Channel:** `UNKNOWN_CHANNEL`
- **Blacklist decision:** `NO_BLACKLIST_DECISION`
- **Reason:** Kanal adı / kanal id güvenilir şekilde verilmediği için blacklist veya watchlist kararı verilmedi.
- **Suggested quality update after repo check:** Eğer kanal daha önce işlenmemişse `UNKNOWN`; bu video sonucu çok faydalı olduğu için `candidate_count += 1`.

---

## 5. Strategy Candidate

### Candidate ID

`CAND_20260503_ENTRY_TACTICS_LIBRARY_oZH6_XRxtDc`

### Candidate Name

**HV/RS Edge Entry Tactics Library**

### Strategy Family

- Momentum
- Breakout
- Pullback continuation
- Relative strength
- High-volume catalyst continuation
- CANSLIM / Minervini-style leadership trading
- Discretionary setup formalization for systematic testing

### Primary Market

- **Best native fit:** US equities
- **Reason:** Video; earnings gaps, stock-specific volume shocks, relative strength, whole number liquidity, base pivots and leadership-stock behavior üzerine kurulu.
- **Crypto adaptation:** Possible but secondary. Crypto’da earnings gap ve stock-specific catalyst yoktur; bu yüzden doğrudan değil, “abnormal volume + breakout + market regime + relative strength basket” biçiminde uyarlanmalıdır.

---

## 6. Candidate Structure — Umbrella Module, Not Single Indicator

Bu transcriptten tek bir strateji çıkarmak yerine aşağıdaki modüler yapı çıkarılmalı:

```text
EDGE DETECTION
  ├─ High Volume Edge
  └─ Relative Strength Edge

SETUP CONTEXT
  ├─ Larger pattern / base context
  ├─ Strong stock / strong group / strong market
  ├─ Constructive consolidation
  └─ Not extended beyond logical risk range

ENTRY TACTIC LIBRARY
  ├─ High Volume Close reclaim / hold
  ├─ Volume Support pullback
  ├─ Whole Number Support
  ├─ Range Breakout / Consolidation Pivot
  ├─ Undercut & Rally
  ├─ Oops Reversal
  ├─ Opening Range Breakout
  └─ Pullback to Support

RISK / POSITION SIZING
  ├─ Tight and logical stop
  ├─ Stop equals invalidation, not arbitrary percentage
  ├─ Position size derived from risk distance
  └─ Confidence/edge quality affects risk tier only after validation
```

Bu yapı MTC_V2’de **producer** olarak değil, daha doğru şekilde **Signal Transform + Entry Gate + Position Sizing helper** paketi olarak düşünülmelidir.

---

## 7. Core Concepts Extracted

### 7.1 Edge First, Entry Second

Transcriptin en önemli prensibi şudur:

```text
No edge → no setup.
No setup → no entry tactic.
No tight/logical stop → no trade.
```

Entry tactic tek başına kullanılmaz. Önce edge gerekir:

1. **High Volume Edge**
   - Highest volume ever, highest volume in 1 year, highest volume since IPO, highest volume since last earnings gibi varyantlar.
   - Güçlü gap / güçlü close / yüksek relative dollar volume.

2. **Relative Strength Edge**
   - Market geri çekilirken hissenin ayakta kalması.
   - Market kötü kapanırken hissenin daha iyi closing range üretmesi.
   - Büyük base içinde üst bölgede sıkışma.

3. **Context Edge**
   - Stock güçlü olmalı.
   - Grup / sektör tercihen güçlü olmalı.
   - Market environment setup tipini desteklemeli.
   - Bear market içinde klasik breakout entry’leri daha düşük kalite kabul edilmeli.

### 7.2 Tight and Logical Stop

Bu transcriptteki en kodlanabilir risk kavramı budur:

```text
Tight stop alone is not enough.
Logical stop alone is not enough.
Entry tactic valid only if stop is both tight and logical.
```

Tight = risk mesafesi küçük.  
Logical = pattern invalidation seviyesi net.

Yanlış örnek:

```text
Stock zaten pivotundan %10 yukarıdadır.
Trader rastgele entry yapar.
Stop'u %3 koyar.
Normal reaction stop'u patlatır.
Bu tight ama logical değildir.
```

Doğru örnek:

```text
Stock 2-3 günlük tight range yapar.
Entry range high üstündedir.
Stop range low / higher low / low of day altındadır.
Stop çalışırsa entry tactic invalid olmuştur.
```

---

## 8. Extracted Entry Tactics

## 8.1 High Volume Close / HVC

### Concept

High Volume Edge günü sonrası, o günün kapanış seviyesi veya yüksek hacimli kapanış bölgesi referans alınır. Fiyat bu seviyenin üzerinde kalırsa demand devam ediyor kabul edilir; altına kalıcı sarkarsa yeni consolidation beklenir.

### Candidate Logic

```text
IF high_volume_edge_day == true:
    hvc_level = close[edge_day]

LONG interest IF:
    price > hvc_level
    AND pullback does not deeply violate HVC structure
    AND market regime supportive
```

### Possible Stop

```text
initial_stop = min(edge_day_low, recent_pullback_low)
OR stop = hvc_level - buffer
```

### Coding Difficulty

`Medium`

### Risks

- HVC seviyesi tek başına alınırsa çok fazla false trigger üretir.
- Gap-up sonrası poor closing range varsa daha uzun consolidation gerekebilir.
- Stock-specific liquidity / spread filtreleri şarttır.

---

## 8.2 Volume Support Pullback

### Concept

High-volume edge günü oluştuğunda, intraday grafikte hacmin çoğunun geçtiği zone bulunur. Fiyat sonraki günlerde o zone’a geri çekilip tutunursa entry fırsatı oluşur.

### Candidate Logic

```text
Detect edge_day.
On edge_day intraday bars:
    compute volume_profile_proxy
    volume_support_zone = price zone with highest traded volume / dollar volume

LONG interest IF:
    price pulls back into volume_support_zone
    AND selling volume dries up or reversal appears
    AND price reclaims zone high or forms expectation breaker
```

### Possible Stop

```text
initial_stop = volume_support_zone_low - buffer
```

### Coding Difficulty

`Medium-High`

### Notes for Python Prototype

Gerçek volume profile şart değil. İlk prototipte şu proxy yeterli olabilir:

```text
For edge_day 5m/15m bars:
    bar_dollar_volume = close * volume
    select top N bars by dollar volume
    support_zone_low = min(low of selected bars)
    support_zone_high = max(high of selected bars)
```

---

## 8.3 Whole Number Support

### Concept

Özellikle ilk kez 20, 25, 30, 50, 100 gibi psikolojik / likidite seviyelerine gelen güçlü hisse, bu seviyeyi pullback sırasında tutarsa entry fırsatı doğar.

### Candidate Logic

```text
whole_levels = [10, 20, 25, 30, 40, 50, 75, 100, 150, 200, ...]

LONG interest IF:
    stock has recent high volume edge
    AND price recently crossed important whole number upward
    AND pullback tests / undercuts / reclaims whole number
    AND price shows positive response
```

### Possible Stop

```text
initial_stop = whole_number_level - buffer
```

### Coding Difficulty

`Medium`

### Risks

- Whole number tek başına edge değildir.
- Sadece HV / RS / setup context üstüne overlay edilmelidir.
- Crypto’da round number behavior çalışabilir ama equity’deki catalyst/liquidity context olmadan kalitesi düşer.

---

## 8.4 Range Breakout / Consolidation Pivot

### Concept

Kısa vadeli tight range, daha büyük constructive setup içinde oluşur. Range high kırıldığında entry; stop range low / higher low altıdır.

### Candidate Logic

```text
Detect constructive parent setup:
    trend up or right side of base
    stock above key MA or near base pivot
    volume contraction during range

Detect short range:
    range_length = 1 to 5 daily bars
    range_pct <= max_range_pct
    volume decreasing or below average

LONG trigger:
    close > range_high
    OR intraday break above range_high with volume confirmation
```

### Possible Stop

```text
initial_stop = range_low - buffer
OR initial_stop = higher_low - buffer
```

### Coding Difficulty

`Medium`

### Best MTC_V2 Fit

Bu modül MTC_V2’ye en temiz şekilde eklenebilir. Çünkü range high / low ve ATR-normalized range kolay test edilir.

---

## 8.5 Undercut & Rally

### Concept

Fiyat kurulmuş range’in altını kırarak stopları temizler; sonra hızlı şekilde tekrar range içine döner. Entry reclaim anında veya range high kırılımında alınabilir.

### Candidate Logic

```text
Setup:
    established_range == true
    stock has strong context

Trigger:
    low < range_low
    AND close > range_low
    AND reclaim happens quickly

Aggressive long:
    entry = reclaim of range_low

Conservative long:
    entry = break above range_high after reclaim
```

### Possible Stop

```text
initial_stop = shakeout_low - buffer
```

### Coding Difficulty

`Medium`

### Notes

Whippy market koşullarında klasik breakout yerine daha kullanışlı olabilir. Ancak kötü markette “failed breakdown” ile “devam eden breakdown” ayrımı için market regime filtresi gerekir.

---

## 8.6 Oops Reversal

### Concept

Larry Williams tarzı oops reversal: fiyat önceki günün low’u altına gap / sarkma yapar, sonra o low seviyesini yukarı reclaim eder.

### Candidate Logic

```text
LONG trigger IF:
    open < prior_low
    AND price crosses back above prior_low
    AND stock is strong / setup context positive
```

### Possible Stop

```text
initial_stop = current_day_low - buffer
```

### Coding Difficulty

`Low-Medium`

### Important Filter

Bu yapı yalnızca güçlü stock / güçlü group / güçlü larger setup içinde değerlidir. 52-week low yapan zayıf hissede tek başına kullanılmamalıdır.

---

## 8.7 Opening Range Breakout / ORB

### Concept

Gap-up veya güçlü açılış sonrası ilk 1m / 3m / 5m range oluşur. Fiyat opening range high üstüne çıkarsa entry; stop opening range low / higher low / anchored VWAP altıdır.

### Candidate Logic

```text
session_open = regular market open
opening_range_minutes = 5
OR_high = high of first N minutes
OR_low = low of first N minutes

LONG trigger IF:
    price > OR_high
    AND gap_up_pct >= threshold OR high_volume_open == true
    AND daily/weekly context positive
```

### Possible Stop

```text
initial_stop = OR_low
OR initial_stop = intraday higher_low
OR trailing reference = anchored_vwap_from_open
```

### Coding Difficulty

`Medium`

### Relation to INTAKE_001

Bu modül önceki videodaki Episodic Pivot / Opening Range High fikriyle güçlü şekilde örtüşüyor. Birleştirilmiş prototype şu olabilir:

```text
Episodic Pivot ORB = Catalyst / abnormal gap + abnormal volume + ORB entry + tight stop + adaptive risk sizing
```

---

## 8.8 Pullback to Support

### Concept

Fiyat base pivot, 21 EMA, 50 SMA, 65 EMA veya önceki breakout seviyesi gibi izlenen support seviyesine constructive şekilde geri gelir. Sert dump değil; daha çok low-volume drift istenir. Pozitif tepki veya reclaim ile entry oluşur.

### Candidate Logic

```text
support_candidates:
    prior_base_pivot
    21ema
    50sma
    65ema
    anchored_vwap
    prior_high_volume_zone

LONG trigger IF:
    price pulls back into support_zone
    AND pullback volume contracts or selling pressure fades
    AND price reclaims support OR forms tight range above support OR breaks minor pivot
```

### Possible Stop

```text
initial_stop = support_zone_low - buffer
OR initial_stop = pullback_low - buffer
```

### Coding Difficulty

`Medium-High`

### Notes

Bu modül discretionary tradingde çok işe yarar; systematic prototipte fazla varyasyon üretir. Önce `range breakout` ve `oops reversal` daha kolaydır.

---

## 9. Recommended Candidate Development Order

### Phase 1 — Cleanest Backtestable Modules

1. **Range Breakout / Consolidation Pivot**
2. **Oops Reversal**
3. **Opening Range Breakout**
4. **High Volume Close reclaim**

### Phase 2 — More Context-Aware Modules

5. **Undercut & Rally**
6. **Whole Number Support**
7. **Pullback to Support**
8. **Volume Support Zone**

### Phase 3 — Composite Strategy

Combine into a scoring model:

```text
setup_score = edge_score + context_score + entry_tactic_score - extension_penalty - market_risk_penalty
```

Trade only if:

```text
setup_score >= threshold
AND risk_distance_pct <= max_allowed_risk
AND liquidity_ok
AND market_regime_ok
```

---

## 10. Python Prototype Specification

### 10.1 Data Requirements

Minimum daily OHLCV:

```text
date, open, high, low, close, volume
```

Preferred intraday OHLCV:

```text
1m or 5m OHLCV for ORB and volume support modules
```

Optional market data:

```text
SPY / QQQ / IWM OHLCV
Sector ETF OHLCV
Universe breadth metrics
```

### 10.2 Derived Features

```text
atr_14
adr_20
sma_10, sma_20, sma_50, sma_150, sma_200
ema_21, ema_65
volume_sma_20, volume_sma_50
relative_volume = volume / volume_sma_50
dollar_volume = close * volume
closing_range = (close - low) / (high - low)
range_pct = (range_high - range_low) / close
near_52w_high
near_all_time_high if full history available
market_relative_strength
```

### 10.3 Edge Detection Draft

```python
high_volume_edge = (
    volume >= max(volume_lookback_252) or
    volume / volume_sma_50 >= 2.5
) and dollar_volume >= min_dollar_volume

relative_strength_edge = (
    stock_return_20d > market_return_20d and
    stock_close_position_in_range > market_close_position_in_range
)
```

### 10.4 Range Breakout Prototype

```python
range_len = 3
range_high = max(high[-range_len:])
range_low = min(low[-range_len:])
range_pct = (range_high - range_low) / close
volume_contracting = volume[-1] < volume_sma_20[-1]

valid_range = (
    range_pct <= 0.08 and
    volume_contracting and
    close > sma_50 and
    near_52w_high
)

entry = close > range_high
stop = range_low
risk_pct = (entry_price - stop) / entry_price
```

### 10.5 Oops Reversal Prototype

```python
oops_long = (
    open < low_prev_day and
    high > low_prev_day and
    close > low_prev_day and
    close > open and
    context_score >= threshold
)
entry = low_prev_day
stop = day_low
```

### 10.6 ORB Prototype

```python
or_high = first_5m_high
or_low = first_5m_low

orb_long = (
    price_crosses_above(or_high) and
    gap_up_pct >= 3 and
    opening_relative_volume >= threshold and
    daily_context_score >= threshold
)
entry = or_high
stop = or_low
```

---

## 11. MTC_V2 Mapping

### Recommended Integration Layer

| Concept | MTC_V2 Layer | Notes |
|---|---|---|
| High Volume Edge | Entry Gate / Signal Producer helper | Can score or permit entry only after abnormal volume event |
| Relative Strength Edge | Entry Gate | Compare symbol vs market / benchmark |
| Range Breakout | Signal Producer or Signal Transform | Clean candidate for direct pulse generation |
| Undercut & Rally | Signal Producer | Generates long pulse on reclaim |
| Oops Reversal | Signal Producer | Simple daily pattern |
| ORB | Separate intraday producer | Needs intraday data/session semantics |
| Pullback to Support | Signal Transform / Entry Gate | Needs context and support hierarchy |
| Tight/logical stop | Position Sizing + Exit Rules | Stop must be created from pattern invalidation, not arbitrary pct |
| Whole Number Support | Entry Gate / Level Proximity module | Existing Level Proximity concept can be extended |
| Volume Support | Entry Gate / custom feature | Needs intraday zone calculation |

### MTC_V2 Implementation Warning

- `01_PINE/MTC_V2.pine` **değiştirilmemeli**.
- Production Python runner **değiştirilmemeli**.
- Önce isolated research module oluşturulmalı:

```text
06_QUANTLENS_LAB/research/entry_tactics_002/
  README.md
  features.py
  detect_range_breakout.py
  detect_oops_reversal.py
  detect_orb.py
  event_label_schema.md
  tests/
```

---

## 12. Candidate Event Taxonomy Draft

```json
{
  "event_type": "ENTRY_TACTIC_SIGNAL",
  "video_id": "oZH6_XRxtDc",
  "candidate_id": "CAND_20260503_ENTRY_TACTICS_LIBRARY_oZH6_XRxtDc",
  "symbol": "EXAMPLE",
  "timeframe": "1D",
  "edge_family": "HIGH_VOLUME_EDGE | RELATIVE_STRENGTH_EDGE",
  "entry_tactic": "RANGE_BREAKOUT | HVC_RECLAIM | VOLUME_SUPPORT | WHOLE_NUMBER_SUPPORT | UNDERCUT_RALLY | OOPS_REVERSAL | ORB | PULLBACK_SUPPORT",
  "trigger_price": 0.0,
  "initial_stop": 0.0,
  "risk_pct": 0.0,
  "context_score": 0,
  "setup_score": 0,
  "market_regime": "SUPPORTIVE | NEUTRAL | HOSTILE",
  "invalidation_reason": "PATTERN_LOW_BROKEN | RANGE_RECLAIM_FAILED | SUPPORT_LOST | MARKET_REGIME_FAIL"
}
```

---

## 13. Backtest / Validation Plan

### Do Not Start With Optimization

Bu video optimization için değil, önce **event definition validation** için kullanılmalıdır. İlk hedef “karlı mı?” değil; “bu pattern doğru tespit ediliyor mu?” olmalı.

### Validation Steps

1. Manual model examples collect:
   - CELH
   - UBER
   - ARLO
   - SPLK
   - ANF
   - CEIX
   - APP
   - NVDA
   - ABNB
   - TSLA

2. Python detector output:
   - Her örnekte expected event date yakınında signal üretmeli.
   - False positive rate not edilmeli.
   - Risk distance mantıklı mı kontrol edilmeli.

3. Add market regime filter:
   - QQQ / SPY above 20d / 50d
   - market closing range
   - breadth proxy

4. Add liquidity filter:
   - dollar volume threshold
   - minimum price
   - spread proxy if available

5. Only then run simple outcome labels:
   - `MFE_5d`, `MFE_10d`, `MFE_20d`
   - `MAE_5d`, `MAE_10d`, `MAE_20d`
   - stop hit before +1R?
   - reached +2R / +3R?

### Suggested Labeling

```text
outcome_5d_R = max_high_next_5d - entry / risk_per_share
adverse_5d_R = entry - min_low_next_5d / risk_per_share
hit_stop_before_2R = true/false
```

---

## 14. Risks / Suspicious or Non-Systematic Claims

### 14.1 Discretionary Bias Risk

Video deneyimli discretionary trader anlatımıdır. Patternlerin elle görülmesi kolay; kodlaması daha zordur. Bu yüzden her fikir doğrudan strategy.entry kuralına çevrilmemelidir.

### 14.2 Stock Universe Bias

Örnekler genellikle geçmişte başarılı olmuş güçlü hisselerden seçiliyor. Survivorship bias riski yüksektir. Prototype mutlaka tüm likit universe üzerinde test edilmelidir.

### 14.3 Market Environment Dependence

Transcriptte de vurgulandığı gibi environment setup’tan güçlü olabilir. Bear market içinde range breakout modülleri çok fazla fail üretebilir.

### 14.4 Overfitting Risk

Çok sayıda entry tactic aynı anda optimize edilirse overfit riski yüksek olur. Önce tek tek pattern detector doğrulanmalı, sonra composite score kurulmalıdır.

### 14.5 Intraday Data Dependency

ORB ve volume support için intraday data gerekir. Sadece daily OHLCV ile bu iki modül zayıf proxy ile test edilebilir.

---

## 15. Trader Wiki Note Also Recommended

Bu video ayrıca Trader Wiki’ye de alınmalı; çünkü strategy candidate yanında çok güçlü sistem tasarım dersleri var.

### Suggested Wiki Entry

- **Wiki status:** `ALSO_CREATE_WIKI_NOTE`
- **Topic:** `04_SYSTEM_DEVELOPMENT` + `01_RISK_MANAGEMENT`
- **Suggested file name:** `TW_2026-05-03_04_SYSTEM_DEVELOPMENT_entry_tactics_framework_ep3.md`

### Wiki Themes

- Edge olmadan entry tactic kullanılmaz.
- Stop arbitraj değil, invalidation seviyesidir.
- Entry tactic, position sizing yapabilmek için risk mesafesi üretir.
- Her stop loss “iş maliyeti” gibi görülmelidir.
- Market maker / stop hunter bahanesi disiplin yerine geçmez.
- Kendi geçmiş trade’lerini yazdırıp stop planı ile gerçek exit’i karşılaştırmak gerekir.

---

## 16. Codex Next Action

### Immediate Task

```text
Create isolated research folder for INTAKE_002 entry tactics library.
Do not modify MTC_V2 Pine.
Do not modify production runner.
Do not run optimization.
Implement only feature detectors and tests for:
1. Range Breakout
2. Oops Reversal
3. High Volume Edge
4. High Volume Close / HVC
```

### Suggested Codex Prompt

```text
Read INTAKE_002_oZH6_XRxtDc_pro_swing_trading_entry_tactics_ep3.md.
Before making changes, inspect repo registry files for duplicate video_id=oZH6_XRxtDc and transcript_hash=a4f5b49fbe115200d4c460faffc7d221a8bf24d050369eca3be0307cd09c41c8.
If duplicate exists, stop and report duplicate details.
If not duplicate, create an isolated research folder under 06_QUANTLENS_LAB/research/entry_tactics_002/.
Do not modify 01_PINE/MTC_V2.pine.
Do not modify production Python runner files.
Do not run backtests or optimization.
Implement feature-detector stubs and unit-test fixtures only for Range Breakout, Oops Reversal, High Volume Edge, and High Volume Close.
Prepare README.md with formulas, assumptions, and next validation steps.
```

---

## 17. Files Created / Not Touched

### Created by this intake step

```text
INTAKE_002_oZH6_XRxtDc_pro_swing_trading_entry_tactics_ep3.md
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

## 18. Final Decision

```text
Classification: CANDIDATE
Codex Status: READY_FOR_PYTHON_PROTOTYPE
Candidate Type: Modular entry tactic library
Primary Implementation Target: Python research prototype
Pine Implementation: Later, only after detector validation
Registry Update Needed: Yes, after repo duplicate check
Trader Wiki Note: Yes, also recommended
```

Bu transcript 68 videoluk batch içinde yüksek öncelikli olmalı. İlk videodaki episodic pivot / progressive exposure fikriyle birleştiğinde, QuantLens için güçlü bir “momentum leadership entry framework” çekirdeği çıkarabilir.
