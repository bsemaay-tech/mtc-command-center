# QuantLens Transcript Intake Report

## Metadata

- Intake ID: `INTAKE_2026-05-03_FtAshnE3MwM`
- Source URL: https://www.youtube.com/watch?v=FtAshnE3MwM
- Original URL: https://youtu.be/FtAshnE3MwM?si=ztrLynPPHiysn3FN
- Video ID: `FtAshnE3MwM`
- Title: `The Simple Stage Analysis Trading System - Exclusive Interview with Stan Weinstein`
- Channel: `UNKNOWN_CHANNEL`
  - Transcript icinde podcast/kanal markasi olarak `TradeLion / TradeLion Podcast` geciyor; ancak resmi kanal id verilmedigi icin blacklist karari verilmedi.
- Transcript file: `/mnt/data/The Simple Stage Analysis Trading System - Exclusive Interview with Stan Weinstein.md`
- Generated date: `2026-05-03`
- Transcript hash SHA256: `8d34cbf0c31d33c4b824474f21f935a88b67e2e3de694c01293bf062c0897518`
- Transcript hash short: `8d34cbf0c31d33c4`

---

## Executive Verdict

- Classification: `CANDIDATE`
- Codex Status Onerisi: `READY_FOR_PYTHON_PROTOTYPE`
- Strategy Candidate ID: `YC_2026-05-03_FtAshnE3MwM_STAGE_ANALYSIS_BREAKOUT`
- Trader Wiki status: `NOT_WIKI_ONLY`
- Pine'a gecilsin mi?: `NO`
- Backtest / optimization calissin mi?: `NO`
- MTC_V2 core dosyalari degissin mi?: `NO`

Bu transcript kodlanabilir bir trading sistemi iceriyor: Stan Weinstein Stage Analysis. Ana fikir; Stage 1 base, Stage 2 advancing phase, Stage 3 topping/distribution ve Stage 4 declining phase ayrimini 200-gun MA, support/resistance, volume ve group strength ile tanimlayip Stage 2 breakout aninda long adaylari secmek. Ek olarak trader/investor ayrimi, pozisyon yonetimi, 50-gun MA ciktisi, extension trim kurali ve market breadth warning kurallari strateji prototipine aktarilabilir.

---

## Duplicate Video Check

### Kontrol Sonucu

- Current video ID: `FtAshnE3MwM`
- Current normalized URL: `https://www.youtube.com/watch?v=FtAshnE3MwM`
- Current transcript hash short: `8d34cbf0c31d33c4`
- Known current-chat previously processed videos:
  - `zw96qkUn9_g` — Clement Ang interview
  - `uh5bALsKkLg` — Mark Minervini interview
  - `4-IjRmw7SZI` — TQQQ / Les Masonson interview
- Result: `NOT_DUPLICATE_IN_CURRENT_CHAT`

### Sinir

Gercek repo registry dosyalari burada yok:

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

Bu video kalite olarak faydali ve stratejiye donusturulebilir. Kanal resmi olarak bilinmedigi icin `GOOD`, `WATCHLIST` veya `BLACKLISTED` karari verilmemeli. Repo tarafinda resmi kanal bilgisi varsa kalite registry'sine bu video `CANDIDATE` olarak islenebilir.

---

## Neden CANDIDATE?

### Kodlanabilir Ana Unsurlar

1. **Stage classification**
   - Stage 1: uzun dususten sonra sideways base/foundation.
   - Stage 2: resistance ve 200-gun MA uzerine breakout; advancing phase.
   - Stage 3: buyuk yukselisten sonra sideways top/distribution; iyi haberle artik yukselememe.
   - Stage 4: support ve 200-gun MA altina kirilim; declining phase.

2. **Stage 2 breakout entry**
   - Base ust direncinin asilmasi.
   - 200-gun MA'nin base'e yakin olmasi.
   - Breakout ile fiyat 200-gun MA uzerine cikmali.
   - Volume breakout gununde belirgin artmali.

3. **Volume quality filter**
   - Breakout volume ideal olarak son 30 gun ortalamasinin en az 2 kati.
   - 3 kati daha guclu kalite sinyali.
   - Volume yoksa breakout `LOW_QUALITY_BREAKOUT` olarak isaretlenebilir.

4. **Group strength filter**
   - Ayni teknik setup iki hissede varsa hot group icindeki tercih edilmeli.
   - Market -> group -> stock filtreleme yaklasimi kullanilmali.
   - Guclu group icindeki iyi risk/reward stocklara oncelik verilmeli.

5. **Position management**
   - Investor: breakoutta yarim pozisyon; breakout basariliysa pullbackte ikinci yarim.
   - Trader: daha aktif; 50-gun MA altina inerse tamamen cikis.
   - Investor: 50-gun MA altinda azaltir, fakat tamamen cikmayabilir.

6. **Profit trimming / extension rule**
   - Stock 200-gun MA uzerinde cok uzarsa trim/reduce.
   - Ornek extension: 50–60% above 200-day MA.
   - Profit taking “dirty word” degil; extended durumda azaltma savunma mekanizmasi.

7. **Market breadth warning**
   - Ana endeks yeni zirve yapsa bile diger endeksler ve breadth teyit etmiyorsa dikkat.
   - Advance/decline line yeni zirveyi teyit etmiyorsa negative divergence.
   - Buy/sell onerileri dengeleniyorsa market split/narrowing kabul edilmeli.

---

## Strategy Candidate: `STAGE_ANALYSIS_BREAKOUT_DAILY_V1`

### Kisa Tanim

Daily OHLCV hisse verilerinde Weinstein Stage Analysis kullanarak Stage 1 base'den Stage 2 advancing phase'e gecen hisseleri tespit eden long-only breakout stratejisi. Kalite skoru; base yapisi, 200-gun MA konumu, breakout volume, group strength, risk/reward ve market breadth ile belirlenir.

### Intended Market

- Primary: US equities, daily timeframe.
- Secondary: ETF veya crypto daily chartlarda uyarlama denenebilir, ancak ilk prototip hisse evreni icin tasarlanmali.
- Timeframe: Daily.
- Holding style:
  - `INVESTOR_MODE`: daha uzun Stage 2 trend takibi.
  - `TRADER_MODE`: 50-gun MA ve extension trim kurallariyla daha aktif yonetim.

### Strategy Type

- Long-only stage breakout / trend transition.
- Optional short module: Stage 4 breakdown / weak group short, fakat ilk prototipte ayri tutulmali.
- Portfolio style: moderate diversification.
- Signal frequency: orta/dusuk.
- Core edge hypothesis: Stage 1 base'den yuksek volume ile Stage 2'ye gecis yapan ve guclu group icinde olan hisseler, rastgele breakoutlara gore daha yuksek follow-through olasiligi tasir.

---

## Stage Classification Draft

### Stage 1 — Base / Accumulation

```text
stage_1_base:
  prior_decline_pct >= threshold
  price_sideways_days >= min_base_days
  range_contraction_or_flat_range == true
  sma_200_slope <= 0 initially, then flattening
  distance_between_base_top_and_sma_200 <= max_distance_pct
  close oscillates around support/resistance band
```

Yorum:

- Base cok erkenken 200-gun MA hala cok yukaridaysa entry yok.
- 200-gun MA base'e yaklastiginda breakout daha actionable olur.

### Stage 2 — Advancing Phase

```text
stage_2_trigger:
  close > base_resistance
  close > sma_200
  sma_200_flat_or_rising == true
  breakout_volume >= 2.0 * avg_volume_30
```

Kalite artiran kosullar:

```text
quality_boosters:
  breakout_volume >= 3.0 * avg_volume_30
  group_strength_rank in top_quantile
  relative_strength_vs_market rising
  pullback_after_breakout holds prior_resistance_as_support
  price stays above rising sma_200
```

### Stage 3 — Topping / Distribution

```text
stage_3_warning:
  prior_stage_2_advance == true
  price_sideways_near_highs == true
  good_news_no_longer_pushes_price_higher == proxy_unavailable
  support_floor_defined == true
  sma_200 close below price and rising/flattening
```

Not:

- Haber reaksiyonu algoritmik olarak dogrudan kullanilmayacaksa, fiyat/volume proxy gerekir.
- Stage 3 tespitinde `failed_breakout`, `churning`, `range expansion without progress`, `declining breadth/group weakness` gibi teknik proxy'ler denenebilir.

### Stage 4 — Declining Phase

```text
stage_4_trigger:
  close < stage_3_support
  close < sma_200
  sma_200_flat_or_falling == true
```

Action:

- Long pozisyon kapat.
- Long yeni entry yasak.
- Optional future short module icin weak group + Stage 4 breakdown adayi olarak isaretle.

---

## Entry Logic Draft

### Universe / Pre-filter

```text
universe_filter:
  min_price >= 5
  min_avg_dollar_volume >= configurable_threshold
  sufficient_history_days >= 260
  no_extreme_spread_or_liquidity_issue
```

### Market Filter

Basit prototip:

```text
market_ok:
  benchmark_close > benchmark_sma_200
  benchmark_sma_200_slope >= 0
```

Gelismis prototip:

```text
market_health_score:
  index_trend_score
  advance_decline_confirmation_score
  percent_stocks_above_200dma
  percent_stocks_in_stage_2_proxy
  buy_signal_count_vs_sell_signal_count
```

### Group Filter

```text
group_ok:
  group_relative_strength_rank <= top_30_percent
  group_trend_above_sma_200 == true
  group_stage_2_proxy == true
```

Veri yoksa:

```text
if group_data_missing:
  allow_trade = true
  quality_penalty = true
  reason = GROUP_DATA_MISSING
```

### Stock Setup

```text
base_ok:
  prior_downtrend_or_large_correction == true
  base_duration_days between 30 and 250
  base_high = max(high, base_window)
  base_low = min(low, base_window)
  base_range_pct <= configurable_max
  close_near_base_top == true
  sma_200_distance_to_base_top <= max_distance_pct
```

### Breakout Trigger

```text
entry_trigger:
  close > base_high
  close > sma_200
  volume >= 2.0 * avg_volume_30
```

Optional intraday future mode:

```text
entry_trigger_intraday:
  high > base_high
  projected_volume_run_rate >= 2.0 * avg_volume_30
  close_position_model != required_for_v1
```

Ilk prototipte close-based OHLCV deterministic model tercih edilmeli.

---

## Position Sizing Draft

### Default Weinstein Diversification Guidance

Transcriptte 15–20 pozisyon ve pozisyon basina yaklasik 4–5% sermaye gibi daha muhafazakar bir ornek veriliyor. Bu nedenle ilk prototip agresif concentrated mode degil, kontrollu diversification mode ile baslamali.

```text
portfolio_defaults:
  max_positions = 20
  target_position_pct = 5%
  max_single_position_pct = 5%
  investor_initial_fraction = 50% of target_position
  trader_initial_fraction = 100% of target_position or configurable
```

### Investor Mode

```text
investor_entry:
  first_buy = 0.5 * target_position at Stage2 breakout
  second_buy = 0.5 * target_position if:
    pullback_to_breakout_area
    old_resistance_holds_as_support
    pullback_volume_declines
```

### Trader Mode

```text
trader_entry:
  first_buy = target_position at Stage2 breakout
  no_add_if_false_breakout
  faster_reduce_if_extended_or_50dma_break
```

---

## Exit / Risk Logic Draft

### Initial Failure Exit

```text
false_breakout_exit:
  close back below base_high
  OR close below breakout_day_low
  OR close below sma_200 shortly after breakout
```

### Trader Exit

```text
trader_exit:
  close < sma_50 -> full_exit
```

### Investor Reduction

```text
investor_reduce:
  close < sma_50 -> reduce_position
  close < sma_200 OR stage_4_trigger -> full_exit
```

### Extension Trim

```text
extension_trim:
  distance_from_sma_200_pct >= 50% -> trim 20-40%
  distance_from_sma_200_pct >= 60% -> stronger trim/reduce
```

### Stage 4 Full Exit

```text
stage4_full_exit:
  close < major_support
  close < sma_200
  stage_4_confirmed == true
```

---

## MTC_V2 / Python Prototype Mapping

### Signal Producer

Yeni producer adayi:

```text
producer_stage_analysis_breakout_v1
```

Outputs:

```text
SignalEvent:
  side = LONG
  signal_type = STAGE2_BREAKOUT
  stage_before = STAGE1
  stage_after = STAGE2
  base_high
  base_low
  sma_200
  volume_ratio_30
  group_strength_score
  market_health_score
  quality_score
```

### Signal Transform Pipeline

Opsiyonel transformlar:

- `breakout_confirmation_transform`
  - Breakout sonrasi pullback support hold bekler.
- `volume_quality_transform`
  - 2x volume altini downgrade eder.
- `group_strength_transform`
  - Weak group sinyallerini SALVAGE veya lower-rank yapar.

### Entry Gates

MTC_V2 gate eslesmeleri:

- MA gate:
  - `close > sma_200`
  - optional `close > sma_50`
- Volume gate:
  - `volume_ratio_30 >= 2.0`
- HTF/market regime gate:
  - benchmark stage filter.
- Relative strength / group gate:
  - group rank veya stock RS rank.
- ATR volatility gate:
  - extreme volatility setup eleme.

### Position Manager

```text
allow_long = true
allow_short = false for v1
max_entries = 1 or staged add mode
same_bar_reentry_allowed = false
cooldown_after_false_breakout = configurable
```

### Position Sizing

Risk-based sizing yerine ilk prototipte percentage-of-equity sizing daha uygun:

```text
sizing_mode = PCT_EQUITY
initial_position_pct = 2.5% in investor staged mode
full_position_pct = 5%
```

### Exit Rules

Exit priority MTC_V2 canonical exit-first mantigiyla uyumlu olmali:

1. Stage 4 / major support break
2. Stop / false breakout
3. 50-day MA trader exit
4. Extension trim / partial profit taking
5. Time stop if no progress after breakout

---

## Research Questions for Codex / Python Prototype

### Stage Detection

1. Stage 1 base nasil sayisal tanimlanacak?
   - Base duration?
   - Range width?
   - 200-gun MA distance?
   - Prior decline requirement?

2. Stage 2 breakout hangi fiyatla tetiklenecek?
   - Close above base high?
   - Intraday high above base high?
   - Next-open fill?

3. Volume ratio threshold optimize edilmeli mi?
   - Fixed 2x vs 1.5x/2x/3x buckets.
   - 30-day average vs 50-day average.

4. Group strength dataseti yoksa ne yapilacak?
   - Sector ETF proxy?
   - Industry mapping yoksa market-relative stock RS proxy?

5. 50-gun MA trader exit performansi nasil?
   - Full exit at close below SMA50.
   - Confirmed 2-day close below SMA50.
   - Intraday stop under SMA50.

6. Extension trim kuralinin etkisi nedir?
   - 40%, 50%, 60% distance from SMA200 buckets.
   - Trim percent 20%, 25%, 33%, 50%.

---

## Suggested Prototype Files

Codex repo icinde yeni dosya olusturacaksa, mevcut production runner ve MTC_V2 Pine dosyasina dokunmadan draft/lab klasorunde kalmali.

```text
06_QUANTLENS_LAB/
  strategy_candidates/
    stage_analysis_breakout/
      README.md
      candidate_spec.md
      stage_analysis_breakout_rules.yaml
      notes_from_transcript.md
      prototype_plan.md
```

Python prototip icin daha sonra:

```text
research/strategies/stage_analysis_breakout.py
research/tests/test_stage_analysis_breakout.py
```

Ancak bu intake asamasinda kod yazilmaz, backtest calistirilmaz.

---

## Trader Wiki Extraction

Bu video `WIKI_ONLY` degil; fakat trader wiki icin de yuksek degerli notlar var.

### Suggested Wiki Topic

- Topic folder: `11_TRADER_WIKI/03_MARKET_STRUCTURE`
- Secondary tags:
  - `stage-analysis`
  - `market-breadth`
  - `technical-analysis`
  - `risk-management`
  - `group-strength`

### Wiki Note Candidate

```text
TW_2026-05-03_03_MARKET_STRUCTURE_stage_analysis_stan_weinstein.md
```

### Kisa Ozet

- Tape/price action haberden daha onemli.
- Stage 1 base sabir ister; Stage 2 breakout asil buy pointtir.
- Volume breakout kalitesini belirler.
- Hot group icindeki breakout daha yuksek olasiliklidir.
- Stage 3 iyi habere ragmen yukselememe ile karakterize olabilir.
- Stage 4'te fundamental hikaye guzel olsa bile long kalmak savunmasizdir.
- Breadth narrowing ve negative divergence marketin yuzey altindaki zayifligini gosterir.

---

## Riskli veya Supheli Iddialar

1. **75–80% win rate iddiasi**
   - Transcriptte iyi calisma ile yuksek dogruluk orani mumkun oldugu belirtiliyor.
   - Bu iddia dogrudan alinmamali; dataset uzerinde test edilmeden strateji varsayimi yapilmamali.

2. **Stage detection subjektif olabilir**
   - Base, support, resistance ve Stage 3 tanimi insani chart reading'de kolay, algoritmik tespitte zor.
   - Prototipte explicit numeric thresholds kullanilmali.

3. **Market breadth verisi gerektirir**
   - Advance/decline line, percent stocks in bear market, buy/sell signal count gibi datalar her ortamda mevcut olmayabilir.
   - Ilk prototipte basit benchmark ve sector/group proxy ile baslanmali.

4. **200-gun MA tek basina yeterli degil**
   - Transcript 200-gun MA'yi ana yapisal arac olarak anlatsa da volume, base, group strength ve risk/reward birlikte kullaniliyor.
   - Basit `close > SMA200` sistemi bu videonun tam mantigini temsil etmez.

5. **Extension trim threshold context-sensitive**
   - 50–60% above SMA200 ornegi her volatilite rejimi ve hisse icin ayni sonucu vermeyebilir.
   - ATR-normalized extension alternatifi denenmeli.

---

## Classification Matrix

| Alan | Degerlendirme |
|---|---|
| Kodlanabilir setup var mi? | Evet |
| Entry tanimi yeterli mi? | Orta-yuksek |
| Exit tanimi yeterli mi? | Orta |
| Position sizing tanimi yeterli mi? | Orta |
| Risk management var mi? | Evet |
| Backtest icin veri ihtiyaci | Daily OHLCV + volume; opsiyonel sector/group breadth |
| MTC_V2 ile uyum | Yuksek; producer + gates + exit rules olarak ayrilabilir |
| Ilk prototip zorlugu | Orta |
| Pine'a hemen gecmeli mi? | Hayir |
| Wiki-only mi? | Hayir |

---

## Expected Registry Updates for Repo Run

### `_registry/youtube_video_index.csv`

Onerilen satir alanlari:

```csv
video_id,normalized_url,title,channel,status,candidate_id,transcript_hash,first_seen_at,last_seen_at,process_count
FtAshnE3MwM,https://www.youtube.com/watch?v=FtAshnE3MwM,The Simple Stage Analysis Trading System - Exclusive Interview with Stan Weinstein,UNKNOWN_CHANNEL,CANDIDATE,YC_2026-05-03_FtAshnE3MwM_STAGE_ANALYSIS_BREAKOUT,8d34cbf0c31d33c4b824474f21f935a88b67e2e3de694c01293bf062c0897518,2026-05-03,2026-05-03,1
```

### `channel_quality_registry.csv`

```text
channel = UNKNOWN_CHANNEL
candidate_count += 1
wiki_count unchanged or optional +1 if separate wiki note is created
reject_count unchanged
stop_count unchanged
quality_state unchanged because channel id unknown
```

### Candidate Registry

```text
candidate_id = YC_2026-05-03_FtAshnE3MwM_STAGE_ANALYSIS_BREAKOUT
family = STAGE_ANALYSIS_TREND_TRANSITION_FAMILY
status = READY_FOR_PYTHON_PROTOTYPE
source_video_id = FtAshnE3MwM
source_title = The Simple Stage Analysis Trading System - Exclusive Interview with Stan Weinstein
```

---

## Files Created by This Intake

This downloadable report only:

```text
/mnt/data/INTAKE_2026-05-03_FtAshnE3MwM_stan_weinstein_stage_analysis.md
```

Repo tarafinda Codex calisirken onerilen fakat bu intake asamasinda olusturulmayan dosyalar:

```text
06_QUANTLENS_LAB/strategy_candidates/stage_analysis_breakout/candidate_spec.md
06_QUANTLENS_LAB/strategy_candidates/stage_analysis_breakout/prototype_plan.md
11_TRADER_WIKI/03_MARKET_STRUCTURE/TW_2026-05-03_03_MARKET_STRUCTURE_stage_analysis_stan_weinstein.md
```

---

## Files Explicitly Not Touched

- `01_PINE/MTC_V2.pine`
- Production Python runner files
- Existing workflow files
- Existing registries
- Any CSV/data bundle/cache/optimization result
- Any secret/API/webhook/broker/exchange configuration

---

## Next Action

1. Repo icinde once `_registry/youtube_video_index.csv` ve kanal registry dosyalarinda duplicate/blacklist kontrolu yap.
2. Duplicate degilse candidate spec'i `stage_analysis_breakout` klasorune yaz.
3. Ilk Python prototipte sadece daily OHLCV ile calis:
   - Stage 1 base detection
   - Stage 2 breakout trigger
   - volume ratio filter
   - 50-day trader exit
   - 200-day Stage 4 full exit
4. Group strength ve breadth filtrelerini ikinci iterasyona birak.
5. Pine'a gecme; once Python tarafinda kural netligi ve small-sample sanity check yap.

---

## Final Status

- Final Classification: `CANDIDATE`
- Codex Status: `READY_FOR_PYTHON_PROTOTYPE`
- Candidate ID: `YC_2026-05-03_FtAshnE3MwM_STAGE_ANALYSIS_BREAKOUT`
- Duplicate Status: `NOT_DUPLICATE_IN_CURRENT_CHAT`
- Blacklist Status: `NO_BLACKLIST_DECISION_UNKNOWN_CHANNEL`
- Recommended Action: `CREATE_STRATEGY_CANDIDATE_SPEC_ONLY`
- Forbidden Action: `DO_NOT_EDIT_MTC_V2_PINE_OR_RUN_BACKTEST`
