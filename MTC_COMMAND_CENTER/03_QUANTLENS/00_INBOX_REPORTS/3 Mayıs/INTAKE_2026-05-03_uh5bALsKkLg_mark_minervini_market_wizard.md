# QuantLens Transcript Intake Report

## Metadata

- Intake ID: `INTAKE_2026-05-03_uh5bALsKkLg`
- Source URL: https://www.youtube.com/watch?v=uh5bALsKkLg
- Original URL: https://youtu.be/uh5bALsKkLg?si=D9l98HmuwtUWogwR
- Video ID: `uh5bALsKkLg`
- Title: `How Mark Minervini Became a Market Wizard`
- Channel: `UNKNOWN_CHANNEL`
  - Transcript icinde podcast/kanal markasi olarak `Trail Line / TraderLion` benzeri ifade geciyor; ancak resmi kanal id verilmedigi icin blacklist karari verilmedi.
- Transcript file: `/mnt/data/How Mark Minervini Became a Market Wizard.md`
- Generated date: `2026-05-03`
- Transcript hash SHA256: `34e97d5dbfb0d627f5f3cb950c0e753d421663bf45851281ed604b280b2d6147`
- Transcript hash short: `34e97d5dbfb0d627`

---

## Executive Verdict

- Classification: `CANDIDATE`
- Codex Status Onerisi: `READY_FOR_PYTHON_PROTOTYPE`
- Strategy Candidate ID: `YC_2026-05-03_uh5bALsKkLg_MINERVINI_TIGHT_PIVOT_BREAKOUT`
- Trader Wiki status: `NOT_WIKI_ONLY`
- Pine'a gecilsin mi?: `NO`
- Backtest / optimization calissin mi?: `NO`
- MTC_V2 core dosyalari degissin mi?: `NO`

Bu transcript sadece motivasyon veya genel trader psikolojisi degil. Kodlanabilir seviyede setup, entry, stop, exposure, violation ve post-breakout behavior kurallari iceriyor. Ana fikir Minervini tipi tight pivot / VCP breakout sisteminin choppy market kosullarinda daha kisa hedef, daha hizli stop ve progressive exposure ile uygulanmasi.

---

## Duplicate Video Check

### Kontrol Sonucu

- Current video ID: `uh5bALsKkLg`
- Current normalized URL: `https://www.youtube.com/watch?v=uh5bALsKkLg`
- Current transcript hash short: `34e97d5dbfb0d627`
- Known current-chat previously processed video:
  - `zw96qkUn9_g` — Clement Ang interview
- Result: `NOT_DUPLICATE_IN_CURRENT_CHAT`

### Sinir

Gercek repo dosyalari burada yok:

- `_registry/youtube_video_index.csv`
- `channel_blacklist.yaml`
- `channel_quality_registry.csv`

Bu nedenle repo seviyesinde kesin duplicate veya kanal blacklist kontrolu yapilmadi. Codex repo icinde calisirken bu dosyalari once okumali; ayni `video_id` veya ayni `transcript_hash` varsa yeni candidate olusturmamali.

---

## Channel Quality / Blacklist Check

- Channel supplied by file: `NO`
- Channel ID supplied by file: `NO`
- Effective channel for registry: `UNKNOWN_CHANNEL`
- Blacklist decision: `NO_BLACKLIST_DECISION`
- Suggested quality impact: `candidate_count +1`

Bu tek video kalite olarak iyi/faydali sayilir. Kanal resmi olarak bilinmedigi icin `GOOD`, `WATCHLIST` veya `BLACKLISTED` karari verilmemeli.

---

## Neden CANDIDATE?

### Kodlanabilir Olan Ana Unsurlar

1. **Tight pivot / VCP breakout**
   - Sag tarafta daralma.
   - Tercihen single-digit pivot width.
   - Volume contraction / dry-up.
   - Breakout gununde price level gecisi.
   - Breakout sonrasi ilk gunlerde confirmation / violation takibi.

2. **Squat reversal / reversal recovery**
   - Breakout denemesi squat yapar.
   - Sonra onceki squat high veya pivot high tekrar asilir.
   - Bu tekrar-asim entry trigger olarak kullanilabilir.

3. **Risk as selection tool**
   - Entry noktasi stop mesafesi kabul edilebilir kadar yakin olmali.
   - Normal swing trade stop araligi yaklasik 5–8%.
   - Stop mesafesi cok genisse setup elenir.

4. **Post-breakout violation rules**
   - Low volume out, high volume in.
   - Close below 20MA / 50MA.
   - 4 lower lows.
   - Kotu close + artan volume.
   - Breakout sonrasi megaphone / engulfing davranisi.
   - Ilk 3, 5, 7, 10 gun icindeki behavior analizi.

5. **Progressive exposure**
   - Once pilot / test position.
   - Test pozisyonlari calisiyorsa hizli exposure artisi.
   - Setup sayisi ve mevcut trade performansi kotuyse exposure dusurme.
   - Market index yerine stock setup davranisini ana feedback olarak kullanma.

6. **Worst-case scenario improvement**
   - Pozisyon karda ilerledikce stopu breakeven'a tasima.
   - Parcali satisla risk finansmani.
   - Strength icine satis yaparak drawdown'u dusurme.

---

## Strategy Candidate: `MINERVINI_TIGHT_PIVOT_BREAKOUT_DAILY_V1`

### Kisa Tanim

Daily hisse grafikleri icin Minervini/SEPA uyumlu tight pivot breakout stratejisi. Strateji, buyable pivot olusumunu daralma + volume dry-up + trend kalitesi ile tespit eder; pivot kiriliminda girer; ilk 1–10 gun icindeki confirmation/violation davranisina gore pozisyonu buyutur, azaltir veya kapatir.

### Intended Market

- Primary: US growth stocks, daily timeframe.
- Secondary research only: liquid crypto daily / 4H marketlerde yapisal adaptasyon denenebilir.
- Intraday execution: sadece entry monitoring icin opsiyonel; ilk prototip daily OHLCV ile kalmali.

### Strategy Type

- Long-only breakout / continuation.
- Optional short module: MA rejection / downtrend shorting, ancak ilk prototipte ayrilmali.
- Portfolio style: concentrated swing / position trading.
- Signal frequency: dusuk-orta.
- Holding period target: kisa swing; choppy markette 1–7 gun, iyi environment'ta daha uzun.

---

## Entry Logic Draft

### Universe / Pre-filter

Minimum prototipte fundamentals data zorunlu olmasin. Fakat transcriptte Mark uc temel fundamental fokus veriyor:

- Earnings growth / acceleration
- Sales growth / acceleration
- Margins

Python prototype iki modlu tasarlanabilir:

1. `TECHNICAL_ONLY_MODE`
   - Sadece OHLCV.
   - Daha kolay veriyle test edilir.
2. `FUNDAMENTAL_AWARE_MODE`
   - Earnings, sales, margin score varsa kullanilir.
   - Veri yoksa signal iptal edilmez; sadece score eksik isaretlenir.

### Technical Setup Filters

Aday setup icin onerilen baslangic kurallari:

```text
trend_ok:
  close > sma_50
  close > sma_200
  sma_50 > sma_200
  optional: close within 0-25% above sma_50, not extremely extended

base_structure_ok:
  lookback_base_days = 20-120
  right_side_tightness_pct <= 10% preferred
  pivot_range_pct <= 5-10%
  recent volatility contraction visible through ATR compression or high-low range compression

volume_dryup_ok:
  recent_avg_volume < prior_avg_volume
  OR volume on tight days below 50-day average
```

### Trigger

```text
entry_trigger:
  close or intraday high crosses pivot_high
  breakout_gap_pct <= allowed_gap_pct
  price not more than max_extension_pct above pivot at entry
```

Baslangic prototipte `process_on_close` kullanilabilir:

```text
entry_price = close
trigger = close > pivot_high
```

Daha sonra intraday veya next-open fill modeli eklenebilir.

### Reversal Recovery Trigger

Transcriptteki SCHW ornegi icin alternatif trigger:

```text
squat_detected:
  prior breakout attempt crossed pivot
  same day or next days failed / closed weak
  price did not fully break structure

reversal_recovery_trigger:
  price reclaims squat_high / failed_breakout_high
```

Bu mod ana breakout trigger'ina opsiyonel ikinci entry tipi olarak eklenebilir:

- `entry_type = PIVOT_BREAKOUT`
- `entry_type = REVERSAL_RECOVERY`

---

## Initial Stop Logic Draft

### Normal Swing Stop

```text
initial_stop_candidates:
  - pivot_low
  - previous_day_low
  - breakout_day_low
  - mathematical_stop_pct = 5-8%
  - max_stop_pct = 8-10%
```

Baslangic icin:

```text
stop_pct = min(max_allowed_stop_pct, structural_stop_pct)
reject_trade_if_stop_pct > max_allowed_stop_pct
```

### Risk as Selection Tool

Setup teknik olarak guzel olsa bile stop mesafesi cok genisse trade alinmaz. Bu kural MTC_V2 tarafinda `risk sizing + entry gate` ayrimi icin onemli:

```text
if abs(entry_price - initial_stop) / entry_price > max_stop_pct:
    reject_signal(reason="STOP_TOO_WIDE")
```

---

## Position Sizing / Progressive Exposure Draft

### First Prototype

Pine'a gecmeden once Python tarafinda basit risk-based sizing:

```text
risk_per_trade_pct = 0.25% to 1.00%
max_total_open_risk_pct = 2% to 6%
max_positions = 4 to 12
```

### Progressive Exposure State Machine

Mark'in anlattigi mekanik tamamen siyah-kutu degil; bu yuzden ilk prototipte state machine olarak modellenmeli:

```text
exposure_state:
  COLD:
    pilot positions only
    risk multiplier = 0.25x
  TESTING:
    1-3 pilot trades working
    risk multiplier = 0.50x
  ACTIVE:
    recent trades positive and watchlist expanding
    risk multiplier = 1.00x
  HOT:
    many setups + breakouts following through
    risk multiplier = 1.25x to 2.00x
  DEFENSIVE:
    failed breakouts / multiple stops
    risk multiplier = 0.10x to 0.25x
```

### Feedback Inputs

```text
recent_trade_feedback:
  last_n_trades_win_rate
  last_n_trades_avg_R
  number_of_valid_setups_today
  breakout_followthrough_score
  failed_breakout_count
```

---

## Exit Logic Draft

### Fast Loss Cut / Violation Exit

Breakout sonrasi ilk gunlerde abnormal action varsa pozisyon hizli kapatilir.

Violation signals:

```text
violation_low_volume_out_high_volume_in:
  breakout_day_volume <= avg_volume
  pullback_day_volume > breakout_day_volume
  close weak

violation_four_lower_lows:
  count_consecutive_lower_lows >= 4

violation_ma_close:
  close < sma_20 OR close < sma_50 after breakout

violation_bad_close:
  close_position_in_bar_range < 25%
  and volume rising

violation_engulfing_megaphone:
  breakout day or early post-breakout day forms bearish outside/engulfing behavior
```

Action:

```text
if severe_violation:
    exit_full(reason="POST_BREAKOUT_VIOLATION")
elif warning_violation:
    reduce_position(reason="WARNING_VIOLATION")
```

### Time Stop

Ozellikle buyuk pozisyon veya breakout trade icin:

```text
if bars_since_entry <= 1-3 and max_favorable_excursion < min_expected_move:
    exit_or_reduce(reason="NO_IMMEDIATE_PROGRESS")
```

### Profit Protection / Worst-Case Improvement

```text
if unrealized_gain_pct >= initial_risk_pct:
    move_stop_to_breakeven

if unrealized_gain_pct >= 2 * initial_risk_pct:
    sell_partial_50pct
    stop_remaining_at_breakeven_or_trailing_level

if strength_spike:
    sell_into_strength_partial
```

### Stop Merge With MTC_V2 Concepts

MTC_V2 ile uyumlu semantik:

- `INITIAL_SL`: structural/mathematical stop.
- `BE`: risk financed after progress.
- `TRAIL`: strength/profit protection.
- `TIME_STOP`: no progress.
- `FILTER_BLOCK`: environment deteriorates / failed breakouts increasing.
- `OPP_SIGNAL`: optional, not priority in first prototype.

---

## Confirmation Rules

Mark'in kritik fikri: breakout sonrasi ilk 3–10 gun stokun davranisi “train on schedule” mi, yoksa abnormal mi?

### Positive Confirmation

```text
confirmation_good:
  price holds above pivot
  closes in upper part of daily range
  volume supports up days
  pullbacks on lower volume
  no deep close below short moving averages
  follow-through within 1-5 days
```

### Negative Confirmation / Violation

```text
confirmation_bad:
  multiple lower lows
  high volume down days
  close below breakout level
  close below 20MA/50MA
  bearish engulfing after breakout
  failed gap / pop-and-drop
```

---

## MTC_V2 / QuantLens Integration Notes

### Pine'a Simdi Gecme

Bu video Pine implementation icin yeterli fikir veriyor; ancak once Python prototip gerekir. Sebep:

- Setup discretionary unsurlar iceriyor.
- Pivot detection ve violation scoring parametreleri optimize edilmeden Pine'a gecerse UI kalabaligi ve repaint/parity riski dogar.
- Hisse daily data ve fundamentals baglantisi henuz net degil.

### MTC_V2'den Yararlanilabilecek Moduller

- Signal producer:
  - `producer_minervini_tight_pivot_v1`
- Entry gates:
  - MA trend gate
  - Volume gate
  - ATR volatility compression gate
  - Market/environment gate
- Position manager:
  - max entries
  - cooldown
  - progressive exposure / portfolio guard
- Position sizing:
  - stop-distance based risk sizing
  - max total open risk
- Exit rules:
  - initial SL
  - BE
  - trailing
  - time stop
  - filter block
  - post-breakout violation exit as new module

### Yeni Reason Codes Onerisi

```text
ENTRY_MINERVINI_PIVOT_BREAKOUT
ENTRY_REVERSAL_RECOVERY
NO_TRADE_STOP_TOO_WIDE
NO_TRADE_PIVOT_NOT_TIGHT
NO_TRADE_VOLUME_DRYUP_MISSING
NO_TRADE_EXTENDED_ABOVE_PIVOT
EXIT_POST_BREAKOUT_VIOLATION
EXIT_LOW_VOLUME_OUT_HIGH_VOLUME_IN
EXIT_FOUR_LOWER_LOWS
EXIT_BEARISH_ENGULFING_MEGAPHONE
EXIT_NO_IMMEDIATE_PROGRESS
REDUCE_SELL_INTO_STRENGTH
RISK_MOVE_STOP_TO_BREAKEVEN
EXPOSURE_STATE_DEFENSIVE
EXPOSURE_STATE_ACTIVE
```

---

## Candidate Scoring

| Category | Score | Notes |
|---|---:|---|
| Kodlanabilirlik | 8/10 | Entry, stop, violation ve exposure kurallari net parcali hale getirilebilir. |
| Veri ihtiyaci | 6/10 | Technical-only mumkun; fundamentals ve intraday volume run-rate icin ek veri faydali. |
| MTC_V2 uyumu | 8/10 | SL/BE/trail/time-stop/position management ile iyi eslesiyor. |
| Repaint riski | 3/10 | Daily close prototype kullanilirsa dusuk; intraday trigger eklenirse dikkat gerekir. |
| Overfit riski | 7/10 | Pivot/violation parametreleri fazla optimize edilirse yuksek. |
| Portfolio risk riski | 8/10 | Leverage/concentration vurgusu ciddi riskli; once konservatif prototip sart. |
| Research priority | 9/10 | QuantLens icin yuksek degerli strateji adayi. |

---

## Riskli veya Supheli Iddialar

1. **277% championship return dogrudan kopyalanamaz.**
   - Bu return agresif turnover, concentration ve leverage baglaminda anlatiliyor.
   - Normal portfoy icin ayni risk profili uygun degil.

2. **Discretionary feel tam otomatiklestirilemez.**
   - “Stocks are acting right/wrong” kismi skorlanabilir ama birebir replike edilemez.

3. **Fundamentals data eksikse edge azalabilir.**
   - Earnings/sales/margins filtresi olmadan pure technical breakout daha fazla false positive uretebilir.

4. **Survivorship bias tehlikesi var.**
   - US growth stocks backtestinde delisted/failed names veri setine dahil edilmezse sonuc sisme riski yuksek.

5. **Gap ve liquidity modellemesi onemli.**
   - Daily OHLCV ile pivot close entry yapmak gercek slippage ve gap riskini eksik yansitabilir.

---

## Trader Wiki Extract

Bu video `WIKI_ONLY` degil; ancak Trader Wiki icin de faydali notlar iceriyor.

### Topic Mapping

- `04_SYSTEM_DEVELOPMENT`
- `05_BACKTESTING_AND_OPTIMIZATION`
- `01_RISK_MANAGEMENT`
- `02_TRADING_PSYCHOLOGY`

### Kisa Wiki Notu

- En onemli edge sadece entry degil; hazirlik, post-analysis ve risk kontroludur.
- Trader kendi average gain, batting average ve average loss metriklerini bilmeden stop politikasini dogru kuramaz.
- Buy / when buy / how much buy / when sell dort kontrol edilebilir degiskendir.
- Market indexleri yerine individual stock setup davranisi daha dogrudan feedback saglayabilir.
- Worst-case scenario her bar iyilestirilmeye calisilmalidir.
- Progressive exposure, sadece karli feedback geldikce risk artirma prensibidir.
- Kotu markette stratejiyi degistirmek yerine reward/risk hedefi kisaltilabilir.

---

## Proposed Registry Row

### `_registry/youtube_video_index.csv`

```csv
video_id,normalized_url,title,channel,status,candidate_id,transcript_hash,first_seen_at,last_seen_at,process_count,notes
uh5bALsKkLg,https://www.youtube.com/watch?v=uh5bALsKkLg,"How Mark Minervini Became a Market Wizard",UNKNOWN_CHANNEL,CANDIDATE,YC_2026-05-03_uh5bALsKkLg_MINERVINI_TIGHT_PIVOT_BREAKOUT,34e97d5dbfb0d627f5f3cb950c0e753d421663bf45851281ed604b280b2d6147,2026-05-03,2026-05-03,1,"Tight pivot breakout + progressive exposure + violation exits"
```

### `channel_quality_registry.csv`

```csv
channel,quality_state,total_processed,candidate_count,wiki_count,salvage_count,reject_count,stop_count,last_video_id,last_updated
UNKNOWN_CHANNEL,UNKNOWN,1,1,0,0,0,0,uh5bALsKkLg,2026-05-03
```

---

## Recommended Python Prototype Plan

### Phase 1 — Feature Extraction Only

Create isolated feature module, no production runner change:

```text
research/strategy_candidates/minervini_tight_pivot_breakout_v1/
  README.md
  intake_report.md
  feature_spec.md
  minervini_features.py
  signal_debug_export.py
  tests/
    test_pivot_width.py
    test_volume_dryup.py
    test_violation_rules.py
```

### Phase 2 — Signal Prototype

Implement:

- pivot detection
- tightness score
- volume dry-up score
- breakout trigger
- stop-too-wide rejection
- early violation detector
- simple BE / partial exit simulation

### Phase 3 — Portfolio State Prototype

Implement progressive exposure:

- `COLD`
- `TESTING`
- `ACTIVE`
- `DEFENSIVE`

Do not add leverage in first version.

### Phase 4 — Validation

Use out-of-sample and cross-market checks:

- 2020 bull
- 2021 choppy breakout market
- 2022 bear
- 2023 recovery
- 2024–2025 momentum periods

Metrics:

- expectancy
- average gain / average loss
- win rate
- max drawdown
- failed breakout rate
- time in trade
- profit factor by environment state
- slippage sensitivity
- gap-down sensitivity

---

## Do Not Touch

Bu intake raporu uretilirken asagidakilere dokunulmadi:

- `01_PINE/MTC_V2.pine`
- Production Python runner dosyalari
- Backtest engine
- Optimization runner
- CSV/data bundle/cache
- Broker/API/exchange key dosyalari
- WunderTrading alert payloadlari
- Mevcut registry dosyalari

---

## Final Next Action

1. Bu videoyu candidate olarak batch registry'ye ekle.
2. Pine'a gecmeden once Python research folder ac.
3. `MINERVINI_TIGHT_PIVOT_BREAKOUT_DAILY_V1` icin feature-level prototype hazirla.
4. Ilk testte technical-only mode kullan.
5. Fundamentals ve intraday execution sonraki iterasyona birak.
6. Clement Ang videosundaki VCP/volume breakout fikirleriyle bu videoyu ayni research family altinda grupla:
   - `GROWTH_MOMENTUM_BREAKOUT_FAMILY`
7. MTC_V2 integration sadece Python prototype pozitif sonuc verirse planlansin.

---

## Created Files

- This report:
  - `INTAKE_2026-05-03_uh5bALsKkLg_mark_minervini_market_wizard.md`

## Files Not Created

- Strategy candidate registry row was proposed but not physically written.
- Trader Wiki standalone note was not created because classification is `CANDIDATE`, not `WIKI_ONLY`.
- Python prototype files were not created.
- Pine files were not created or modified.
