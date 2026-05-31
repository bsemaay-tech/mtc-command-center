# YouTube Strategy Transcript Intake Report

## 1. Intake Metadata

- Intake No: 07 / 68
- Generated: 2026-05-03
- Source File: `The Dead Simple VWAP Swing Trading Setup With Brian Shannon.md`
- Original URL: `https://youtu.be/Jew-Algmi0k?si=HtYuBVZg6mN58Qt-`
- Normalized URL: `https://www.youtube.com/watch?v=Jew-Algmi0k`
- Video ID: `Jew-Algmi0k`
- Title: `The Dead Simple VWAP Swing Trading Setup With Brian Shannon`
- Channel: `TraderLion / TraLine conference format` *(transcriptte açık kanal ID yok; repo registry için `UNKNOWN_CHANNEL` veya mevcut kanal adı doğrulanmalı)*
- Speaker / Trader: `Brian Shannon`
- Transcript Hash SHA256: `7eadedaa71cbdbef0685ad92e91e4ccac293c7a56a58decf15ca384456c15cdb`
- Transcript Hash Short: `7eadedaa71cbdbef`
- Source Type: `YouTube transcript`
- Processing Scope: `intake only`
- Pine Edit: `NO`
- Production Python Runner Edit: `NO`
- Backtest / Optimization Run: `NO`

---

## 2. Final Classification

```text
Classification: CANDIDATE
Codex Status Suggestion: READY_FOR_PYTHON_PROTOTYPE
Candidate Type: ENTRY_SYSTEM_CANDIDATE + AVWAP_PULLBACK_MODULE + MTF_RISK_MANAGEMENT
Primary Edge Family: ANCHORED_VWAP_MULTI_TIMEFRAME_SWING
Pine Implementation Now: NO
Python Prototype First: YES
Trader Wiki Note: YES
```

### Decision

Bu transcript `CANDIDATE` olarak sınıflandırıldı.

Sebep: Video yalnızca genel piyasa yorumu veya psikoloji anlatımı değildir. Brian Shannon doğrudan kodlanabilir bir swing trading framework anlatıyor:

- daily trend context: rising 20/50 MA, rising 50-day MA, price above relevant moving averages
- multi-timeframe confirmation: weekly / daily / 65m / 30m / 15m / 2m
- true 5-day moving average on intraday charts
- anchored VWAP from swing high / swing low / IPO / event anchors
- AVWAP pinch / compression concept
- “buy after the dip, not the dip” rule
- shorter timeframe confirmation after pullback
- higher high above flat-to-rising 5-day MA trigger
- stop below recent relevant higher low
- heavy entry only when timing is precise
- sell first third into strength to reduce risk
- raise stops under higher lows
- avoid long trades when declining 5-day / declining 50-day structure remains guilty
- reverse-side short framework using declining 50-day and lower low below flat/declining 5-day MA

Bu kurallar MTC_V2'nin producer, entry gate, position sizing, stop management, partial exit ve trailing exit katmanlarına araştırma amaçlı bağlanabilecek kadar nettir. Ancak doğrudan Pine'a geçilmemelidir; önce Python prototype ve rule-ablation gerekir.

---

## 3. Duplicate Check

### Conversation-Level Check

Bu konuşmada daha önce işlenen video ID'leri:

| Intake | Video ID | Status |
|---:|---|---|
| 01 | `q43pkYBo1hU` | `CANDIDATE` |
| 02 | `VKNEJA5r8zw` | `CANDIDATE` |
| 03 | `Eb9FkLNJLzs` | `SALVAGE` |
| 04 | `oPeTkxTnooA` | `SALVAGE` |
| 05 | `q4TuaY-ccqA` | `WIKI_ONLY` |
| 06 | `DLlNDuOTUfQ` | `CANDIDATE` |
| 07 | `Jew-Algmi0k` | `CANDIDATE` |

Result:

```text
Duplicate Detected: NO
Same Video ID Seen Earlier: NO
Same Transcript Hash Seen Earlier: NOT_CHECKED_AGAINST_REPO
Possible Topic Overlap: YES
```

### Topic Overlap Note

Bu video, 06. intake olan Stan Weinstein Stage Analysis videosuyla doğal olarak örtüşür. İkisi de stage analysis ve moving-average structure kullanır. Ancak bu transcript ayrı bir adaydır çünkü Brian Shannon yaklaşımı özellikle:

- anchored VWAP,
- true 5-day intraday moving average,
- intraday trigger timing,
- first-third profit-taking,
- stop ratcheting,
- AVWAP pinch,
- “buy after the dip”

kurallarını ayrı ve daha teknik şekilde verir.

### Repo-Level Check Required

Bu ChatGPT oturumunda repo içindeki aşağıdaki dosyalara erişim yoktur:

- `_registry/youtube_video_index.csv`
- `channel_blacklist.yaml`
- `channel_quality_registry.csv`
- candidate registry dosyaları

Codex repo içinde şu kontrolü tekrar yapmalıdır:

```text
1. video_id = Jew-Algmi0k var mı?
2. transcript_hash = 7eadedaa71cbdbef0685ad92e91e4ccac293c7a56a58decf15ca384456c15cdb var mı?
3. aynı title + kanal + benzer transcript daha önce işlenmiş mi?
4. Brian Shannon / AVWAP / VWAP pinch konulu önceki candidate veya wiki note var mı?
```

Duplicate bulunursa yeni candidate oluşturulmayacak; önceki candidate path ve status raporlanacak.

---

## 4. Channel Quality / Blacklist Check

```text
Channel: UNKNOWN_CHANNEL_OR_TRADERLION
Blacklist State: UNKNOWN
Action: DO_NOT_BLACKLIST
Reason: Transcript yüksek değerli, kodlanabilir trading sistemi içeriyor.
```

Bu video kötü içerik değildir. Kanal için negatif kalite sinyali üretmez.

Suggested channel registry effect:

```text
processed_count += 1
candidate_count += 1
wiki_count += 1
last_status = CANDIDATE
quality_state = GOOD_OR_MANUAL_REVIEW
```

---

## 5. Short Summary

Brian Shannon bu videoda anchored VWAP odaklı, multi-timeframe swing trading yaklaşımını anlatıyor. Sistem, büyük zaman diliminde trendin doğru yönde olmasını, pullback sonrası kısa zaman diliminde alıcıların tekrar kontrolü aldığını kanıtlamasını ve riskin stop ile sıkı şekilde yönetilmesini temel alıyor.

Ana fikir:

```text
Strong daily trend + pullback to level of interest + AVWAP/MA compression + shorter timeframe buyer-control trigger + tight stop + partial into strength + higher-low trailing stop.
```

Bu yaklaşım özellikle discretionary görsel analizden mekanik bir prototype'a çevrilmeye uygundur. En kritik zorluk, anchored VWAP anchor noktalarının deterministik seçilmesidir.

---

## 6. Extracted Strategy Candidate

### Candidate ID Proposal

```text
YT_AVWAP_PULLBACK_BRIAN_SHANNON_V1
```

Alternative names:

```text
AVWAP_MTF_PULLBACK_V1
SHANNON_BUY_AFTER_DIP_V1
AVWAP_PINCH_SWING_V1
```

### Candidate Thesis

Bir hisse daha büyük zaman diliminde uptrend içindeyse ve pullback sonrası AVWAP / moving-average / support bölgesinde sıkışıyorsa, daha kısa zaman diliminde alıcıların tekrar kontrolü aldığı ilk moment, düşük riskli swing entry noktası olabilir.

Sistem breakout'u kör takip etmez. Pullback'i de kör almaz. Pullback bittikten sonra, kısa zaman diliminde momentumun tekrar yukarı döndüğünü kanıtlayan trigger bekler.

### Primary Setup Type

```text
Long continuation after pullback in existing uptrend
```

Secondary setup:

```text
Short continuation after bounce in existing downtrend
```

---

## 7. Mechanical Rule Extraction

### 7.1 Universe / Liquidity

Transcriptte belirtilen minimum likidite yaklaşımı:

```text
average_daily_volume_20d >= 500,000 shares
```

Notes:

- Brian Shannon 50 günlük hacim yerine kendi zaman dilimi için son 20 günü daha önemli görüyor.
- Çok küçük, haber odaklı biotech tarzı enstrümanlardan kaçınma eğilimi var.
- İlk prototype equities / liquid stocks üzerinde düşünülmelidir.

Potential mechanical filters:

```text
avg_volume_20d >= 500000
price > optional_min_price
exclude extreme biotech/news-driven microcaps if metadata available
```

MTC_V2 crypto/FX tarafına taşınacaksa volume filtresi doğrudan kopyalanmamalı; `dollar_volume`, `ATR%`, spread/slippage proxy ve liquidity proxy ile adapte edilmelidir.

---

### 7.2 Higher Timeframe Trend Context

Long side için:

```text
Daily 50MA rising
Price above daily 50MA
Prefer price above rising daily 20MA and 50MA
Weekly structure not bearish
Stock in Stage 2 or late Stage 1 -> Stage 2 transition
```

Brian Shannon'ın ifadesiyle rising 50-day MA olan hisse “innocent until proven guilty” olarak değerlendirilir. Declining 50-day MA olan hisse ise long için “guilty until proven innocent” sayılır.

Possible deterministic conditions:

```text
ma50_slope_n > 0
close > ma50
ma20 >= ma50 optional
ma20_slope_n >= 0 optional
recent_structure = higher_highs_higher_lows OR stage2_proxy = true
```

---

### 7.3 Pullback Zone / Level of Interest

Long için setup bölgesi:

```text
Pullback to a level of interest, not blind dip buy.
```

Possible levels of interest:

- rising 20-day MA
- rising 50-day MA
- anchored VWAP from prior swing low
- anchored VWAP from IPO / major low / event low
- prior resistance becoming support
- gap support
- AVWAP pinch between swing-low AVWAP and swing-high AVWAP

Important rule:

```text
Do not buy the dip directly.
Buy after the dip, when buyers regain control.
```

Prototype approximation:

```text
pullback_zone = abs(close - ma20_or_ma50_or_avwap) / close <= threshold
range_compression = rolling_range_n decreasing OR ATR_short < ATR_long
```

---

### 7.4 Intraday / Shorter-Timeframe Confirmation

Trigger logic:

```text
5-day intraday MA flattens or turns up
Price makes higher high above flat-to-rising 5-day MA
Buy when buyers regain control
```

True 5-day MA period calculation from transcript:

```text
Trading minutes per day = 390
5 trading days = 1950 minutes
true_5d_ma_period = 1950 / intraday_bar_minutes
```

Examples:

| Intraday TF | True 5-Day MA Period |
|---:|---:|
| 65m | 30 |
| 30m | 65 |
| 15m | 130 |
| 10m | 195 |
| 5m | 390 |
| 2m | 975 |
| 1m | 1950 |

Core long trigger:

```text
short_ma = SMA(close, true_5d_ma_period)
short_ma_slope >= 0
close crosses above recent trigger high
close > short_ma
higher_high_above_flat_to_rising_5d_ma = true
```

For gaps / fast opens, Brian also uses 1-minute VWAP and low-of-day logic. That should be a later extension, not first prototype.

---

### 7.5 AVWAP Pinch Logic

Anchor candidates:

```text
AVWAP_low = anchored VWAP from significant swing low
AVWAP_high = anchored VWAP from significant swing high after breakdown / pullback
```

Pinch definition:

```text
AVWAP_low and AVWAP_high converge tightly
Price compresses between them
Longer-term trend remains up
Break back above upper AVWAP implies buyers regain control
```

Possible deterministic prototype:

```text
avwap_gap_pct = abs(avwap_low - avwap_high) / close
pinch = avwap_gap_pct <= threshold
price_inside_pinch = close between min(avwap_low,avwap_high) and max(...)
trigger = close > max(avwap_low,avwap_high) AND close > true_5d_ma AND true_5d_ma_slope >= 0
```

Suggested threshold ranges for research only:

```text
avwap_gap_pct <= 0.5% to 2.0%
compression_bars >= 3 to 10 intraday bars
```

---

### 7.6 Entry Rule Candidate

Long entry draft:

```text
IF daily_ma50_slope > 0
AND close_daily > daily_ma50
AND avg_volume_20d >= 500000
AND pullback_to_level_of_interest = true
AND avwap_pinch_or_ma_pullback = true
AND intraday_true_5d_ma_slope >= 0
AND intraday_close > intraday_true_5d_ma
AND intraday_close breaks recent short-term trigger high
THEN long entry
```

Reject entry if:

```text
daily_ma50 declining
price very extended from daily 50MA or pullback level
intraday 5d MA still declining
no higher high confirmation
stop distance too wide
liquidity insufficient
```

---

### 7.7 Stop Placement

Initial long stop:

```text
below most recent relevant higher low on the execution timeframe
```

Alternative / gap-specific stop:

```text
below low of day
below entry candle low
split stop: half below tight higher low, half below wider low-of-day / structure low
```

Risk filter:

```text
stop_distance_pct <= max_allowed_stop_pct
position_risk <= configured portfolio risk
```

Important transcript concept:

```text
If stop is too far away, position size must shrink; if risk/reward no longer works, skip trade.
```

---

### 7.8 Profit Taking and Risk Reduction

Brian Shannon's discretionary rule:

```text
Enter heavy when timing is precise.
Sell first third quickly into strength.
Use partial sale as risk-mitigation tool.
Raise stop after price confirms.
```

Prototype alternatives:

```text
Partial_1: sell 1/3 at +1R or +quick_strength_threshold
Partial_2: optional at +2R or prior resistance
Runner: trail below relevant higher lows / true 5d MA structure
```

Important note:

The video does not give one universal fixed profit target. It emphasizes trade management and stop adjustment.

---

### 7.9 Exit / Invalidation

Long invalidation:

```text
Pattern stops making higher highs and higher lows
Price breaks below relevant higher low
Price moves below declining 5-day MA structure
Trade becomes stagnant beyond expected swing window
Daily trend deteriorates
```

Trailing stop:

```text
Raise stop under each new relevant higher low after each new higher high.
```

Time risk:

Brian explicitly treats time as a risk. Stagnant positions tie up capital. Prototype should include optional time stop:

```text
time_stop_bars = configurable
exit if no progress after N bars
exit if no +R progress after N bars
```

---

### 7.10 Short-Side Mirror

Short conditions:

```text
Daily 50MA declining
Price below declining 50MA
Shorter timeframe bounce into level of interest
5-day intraday MA flat-to-declining
Price makes lower low below flat/declining 5-day MA
Initial stop above recent relevant lower high
Trail stop lower above lower highs
```

For MTC_V2 first prototype, long-only is recommended. Short-side mirror can be phase 2.

---

## 8. Why This Is Candidate, Not WIKI_ONLY

This video contains enough concrete, testable rules for prototype work:

| Rule Area | Mechanical Enough? | Notes |
|---|---:|---|
| Trend filter | YES | rising/declining 50MA, price relation |
| Timeframe structure | YES | daily + intraday true 5-day MA |
| AVWAP level | PARTIAL | anchor selection needs deterministic definition |
| Entry trigger | YES | higher high above flat-to-rising 5d MA |
| Stop | YES | below relevant higher low |
| Partial exit | YES/PARTIAL | first-third into strength can be R-based |
| Trailing exit | YES | raise under higher lows |
| Risk management | YES | stop-based sizing and first-third risk reduction |

Bu nedenle `CANDIDATE` kararı uygundur.

---

## 9. Main Implementation Risk

### 9.1 Anchor Selection Ambiguity

Anchored VWAP stratejilerinde en büyük problem anchor seçiminin discretionary olmasıdır. Brian Shannon görsel olarak swing high, swing low, IPO low, earnings/event low gibi anchorlar kullanıyor.

Mekanik prototype için anchor seçimleri netleştirilmelidir:

```text
Option A: pivot high/low using left/right bars
Option B: highest high / lowest low over lookback
Option C: gap day high/low anchor
Option D: IPO anchor if metadata available
Option E: major volume spike anchor
```

First prototype recommendation:

```text
Use deterministic pivot anchors only:
- swing_low_anchor = most recent confirmed pivot low on daily or 65m
- swing_high_anchor = most recent confirmed pivot high after the swing low
```

### 9.2 Intraday Data Requirement

Bu sistem daily-only backtest için eksik kalır. İdeal prototype en az 15m veya 30m OHLCV ister.

Minimum viable prototype:

```text
Daily trend context + 30m execution timeframe
```

Preferred:

```text
Daily + 65m + 30m + 15m
```

MTC_V2 crypto tarafında 5m/15m veri mevcutsa, true 5-day MA hesapları crypto 24/7 olduğu için yeniden uyarlanmalıdır. Hisse senetleri için 390 dakika/gün; crypto için 1440 dakika/gün mantığı ayrı olmalıdır.

### 9.3 Discretionary Partial Exit Translation

“Sell first third into strength” net ama tam sayısal değil. Prototype için R-based alternatif gerekir:

```text
Partial 1 at +1R, +1.5R, or intraday extension threshold
```

Ablation yapılmalı:

```text
A: no partial, only trailing
B: 1/3 at +1R
C: 1/3 at +1.5R
D: 1/3 at prior resistance / daily R2 proxy
```

---

## 10. MTC_V2 Mapping

### Suggested MTC_V2 Layer Mapping

| MTC_V2 Layer | Mapping |
|---|---|
| Signal Producer | `producer_avwap_pullback_v1` |
| Signal Transform | optional confirmation: range compression / higher-high trigger |
| Entry Gates | daily 50MA trend gate, liquidity gate, extension guard, AVWAP pinch gate |
| Position Manager | signal pulse entry, no blind re-entry after stop unless setup reforms |
| Position Sizing | stop-distance based risk sizing; cap for tight-stop high-size trades |
| Exit Rules | initial SL below higher low; partial TP; trailing below higher lows; time stop |
| Visualization | AVWAP anchors, pinch zone, trigger high, stop line, partial markers |

### Candidate Module Names

```text
producer_avwap_pullback_v1
entry_gate_true_5d_ma_confirmation_v1
entry_gate_avwap_pinch_v1
exit_trail_higher_lows_v1
partial_first_third_strength_v1
```

### Existing MTC_V2 Relevance

Bu aday özellikle şu mevcut MTC_V2 özellikleriyle uyumlu olabilir:

- MA / MA slope filter
- HTF trend filter
- ATR volatility floor
- session filter for equities adaptation
- SL based on structure / ATR / percentage
- TP multi-leg partial exit
- trailing stop
- time stop
- position sizing from stop distance

---

## 11. Python Prototype Plan

### Prototype Goal

Brian Shannon AVWAP swing setup'ını Pine'a geçmeden önce deterministic Python araştırma adayı olarak test etmek.

### Data Requirement

```text
Required:
- OHLCV intraday data: 30m preferred, 15m acceptable
- Daily resample from intraday OR separate daily OHLCV
- Volume available

Optional:
- earnings date
- sector / industry metadata
- gap detection
- stock universe liquidity metadata
```

### Step 1 — Feature Contract

Create draft contract:

```text
feature_contracts/drafts/producer_avwap_pullback_v1.yml
```

Fields:

```yaml
name: producer_avwap_pullback_v1
side: long_first
inputs:
  trend_tf: daily
  exec_tf: 30m
  ma_daily_fast: 20
  ma_daily_slow: 50
  true_5d_ma_enabled: true
  avwap_anchor_mode: pivot_low_high
  min_avg_volume_20d: 500000
  max_stop_pct: 5.0
  pinch_threshold_pct: 1.5
  compression_bars_min: 3
  partial_mode: first_third_at_R
  partial_r: 1.0
  trail_mode: relevant_higher_low
outputs:
  raw_long_pulse
  setup_state
  anchor_low_ts
  anchor_high_ts
  avwap_low
  avwap_high
  trigger_price
  initial_stop
  reject_reason
```

### Step 2 — Deterministic Anchors

Implement helper:

```text
research/features/avwap.py
```

Functions:

```python
anchored_vwap(df, anchor_index)
find_confirmed_pivot_low(df, left, right)
find_confirmed_pivot_high(df, left, right)
select_recent_anchor_pair(df, lookback)
```

### Step 3 — Setup Detector

Implement:

```text
research/producers/producer_avwap_pullback_v1.py
```

Core state:

```text
NO_SETUP
DAILY_TREND_OK
PULLBACK_TO_LEVEL
PINCH_FORMING
TRIGGER_ARMED
LONG_PULSE
INVALIDATED
```

### Step 4 — Risk / Exit Model

Use research-only exit model:

```text
initial_stop = recent_relevant_higher_low - buffer
partial_1 = +1R or +1.5R
trail_stop = latest relevant higher low after each new higher high
fail_exit = close below true 5d MA and lower-low confirmation
optional_time_stop = N bars
```

### Step 5 — Ablation Matrix

Run only after implementation, not during intake.

Suggested experiments:

| Experiment | Description |
|---|---|
| A | MA pullback only, no AVWAP |
| B | AVWAP pinch only |
| C | AVWAP pinch + true 5-day MA trigger |
| D | C + first-third partial |
| E | D + higher-low trailing stop |
| F | D + fixed R exit |
| G | C with no partial / full trailing |

### Step 6 — Metrics

Minimum metrics:

```text
trade_count
win_rate
avg_R
median_R
profit_factor
max_drawdown
expectancy_R
avg_hold_bars
time_in_market
MAE/MFE
partial contribution
stop_distance_distribution
anchor_age_distribution
```

### Step 7 — Manual Chart Audit

Before any Pine implementation:

```text
Export 30 to 50 sample trades.
Inspect charts manually.
Confirm anchor selection is sane.
Confirm no lookahead in pivot anchors.
Confirm trigger is not buying random extended moves.
Confirm stop is realistic.
```

---

## 12. Anti-Repaint / Lookahead Notes

Important for MTC_V2 parity discipline:

```text
Confirmed pivots must not use future bars in live simulation.
Daily MA values must use prior closed daily bar if executing intraday before daily close.
AVWAP anchor must be known at the time of trade.
Intraday trigger must be bar-close confirmed unless explicitly modeling intrabar execution.
Stop movement must be monotonic and based only on closed bars unless intrabar path model is defined.
```

Potential lookahead traps:

- using future-confirmed pivot before confirmation time
- using same-day daily close while entering intraday
- selecting the “obvious” anchor after seeing the whole chart
- using future high/low to define relevant higher low
- filling stops/partials without deterministic OHLC ordering

---

## 13. Trader Wiki Note

This video should also create a Trader Wiki note because it contains durable trading-system principles.

Suggested path:

```text
11_TRADER_WIKI/04_SYSTEM_DEVELOPMENT/TW_2026-05-03_AVWAP_MTF_SWING_BRIAN_SHANNON.md
```

Suggested tags:

```text
AVWAP, VWAP, Brian Shannon, swing trading, multi-timeframe, risk management, pullback, stage analysis, higher lows, partial exits
```

Wiki usefulness score:

```text
9 / 10
```

Main lessons:

- Do not buy the dip blindly; buy after buyers regain control.
- Use larger timeframe for context and shorter timeframe for precise execution.
- Rising 50-day MA defines a healthier long environment.
- Declining 50-day MA means long setups are suspect.
- AVWAP is a price-volume-time reference that can reveal institutional battle zones.
- First partial into strength can reduce risk quickly.
- Winners do not automatically take care of themselves; stops must be managed.
- Time, price, and leverage are all forms of risk.

---

## 14. Candidate Registry Draft

Suggested row for candidate registry:

```csv
candidate_id,source_video_id,title,status,family,prototype_first,notes
YT_AVWAP_PULLBACK_BRIAN_SHANNON_V1,Jew-Algmi0k,The Dead Simple VWAP Swing Trading Setup With Brian Shannon,READY_FOR_PYTHON_PROTOTYPE,ANCHORED_VWAP_MULTI_TIMEFRAME_SWING,true,Needs deterministic anchor selection and intraday data; no Pine before Python chart audit
```

Suggested row for video index:

```csv
video_id,normalized_url,title,channel,status,candidate_id,transcript_hash,processed_at
Jew-Algmi0k,https://www.youtube.com/watch?v=Jew-Algmi0k,The Dead Simple VWAP Swing Trading Setup With Brian Shannon,UNKNOWN_CHANNEL,CANDIDATE,YT_AVWAP_PULLBACK_BRIAN_SHANNON_V1,7eadedaa71cbdbef0685ad92e91e4ccac293c7a56a58decf15ca384456c15cdb,2026-05-03
```

---

## 15. Files To Create In Repo

Codex should create only if duplicate checks pass:

```text
YOUTUBE_STRATEGY_INTAKE/reports/YT_Jew-Algmi0k_Intake_Report_2026-05-03.md
YOUTUBE_STRATEGY_INTAKE/transcripts/Jew-Algmi0k.md
11_TRADER_WIKI/04_SYSTEM_DEVELOPMENT/TW_2026-05-03_AVWAP_MTF_SWING_BRIAN_SHANNON.md
research/ideas/YT_AVWAP_PULLBACK_BRIAN_SHANNON_V1/README.md
feature_contracts/drafts/producer_avwap_pullback_v1.yml
```

Do not create during intake:

```text
01_PINE/MTC_V2.pine changes
production Python runner changes
optimization outputs
large CSV files
cache files
broker/exchange/webhook configs
```

---

## 16. Files / Systems Explicitly Not Touched

```text
01_PINE/MTC_V2.pine: NOT TOUCHED
Production Python runner: NOT TOUCHED
Backtest engine: NOT TOUCHED
Optimization runner: NOT TOUCHED
CSV/data bundles/cache: NOT CREATED
Secrets/API keys/webhooks: NOT TOUCHED
```

---

## 17. Next Action

Recommended next action for Codex:

```text
1. Run repo-level duplicate check for video_id and transcript_hash.
2. If not duplicate, register this as CANDIDATE.
3. Create Trader Wiki note under system development.
4. Create research idea folder for YT_AVWAP_PULLBACK_BRIAN_SHANNON_V1.
5. Draft feature contract only; do not implement yet if tonight's job is only intake.
6. In later research phase, implement Python prototype with deterministic AVWAP anchors.
7. Do not touch Pine until Python sample-chart audit passes.
```

---

## 18. Final Verdict

```text
FINAL_VERDICT: CANDIDATE
CODEX_STATUS: READY_FOR_PYTHON_PROTOTYPE
CONFIDENCE: HIGH
PINE_NOW: NO
PYTHON_RESEARCH_NEXT: YES
WIKI_NOTE: YES
DUPLICATE_STATUS: NOT_DUPLICATE_IN_CONVERSATION__REPO_CHECK_REQUIRED
```

Bu transcript 68 video içinde yüksek öncelikli adaylardan biridir. Özellikle 06. intake Stan Weinstein Stage Analysis ile birleştirildiğinde, MTC_V2 için güçlü bir `Stage 2 + AVWAP Pullback + MTF Confirmation + Tight Stop` araştırma hattı oluşturabilir.
