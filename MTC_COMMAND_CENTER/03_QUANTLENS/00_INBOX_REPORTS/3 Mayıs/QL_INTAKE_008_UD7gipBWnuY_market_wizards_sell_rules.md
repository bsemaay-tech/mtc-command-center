# QuantLens Transcript Intake Report — 008

## 1. Intake Verdict

- **Video ID:** `UD7gipBWnuY`
- **Normalized URL:** https://www.youtube.com/watch?v=UD7gipBWnuY
- **Original URL:** https://youtu.be/UD7gipBWnuY?si=C6iiZ7u_4SDwqSm3
- **Transcript file:** `When To Take Trading Profits - Market Wizards Share Their Sell Rules.md`
- **Transcript hash:** `4804e3dda96a256e801b9a1c359ff07da08c9fb5abaf5593f4ca12c80338e18a`
- **Primary classification:** `CANDIDATE`
- **Codex status recommendation:** `READY_FOR_PYTHON_PROTOTYPE`
- **Candidate type:** `EXIT_RULES / PROFIT_TAKING / RISK_GOVERNOR_OVERLAY`
- **Standalone entry producer?** Hayır. Bu transcript entry producer üretmekten çok exit, profit-taking, position management, risk-governor ve market-regime overlay içeriyor.
- **MTC_V2 relevance:** Çok yüksek. Özellikle `EXIT RULES`, `POSITION MANAGER`, `POSITION SIZING`, `PortfolioState guards`, `partial exits`, `trailing/BE`, `risk-off governor`, `monthly loss cap` ve `regime-aware exposure` katmanlarına bağlanabilir.
- **Usefulness score:** `9/10`
- **Implementation priority:** `P1`
- **Recommended candidate ID:** `CAND_008_MARKET_WIZARDS_SELL_RULES_MULTI_OVERLAY_V1`

## 2. Duplicate / Registry Decision

### Duplicate Check Result

- `video_id` önceki intake dosyalarındaki video_id’lerden farklı.
- Transcript hash yeni görünüyor.
- Başlık, URL ve transcript kombinasyonu önceki raporlarla aynı değil.
- **Duplicate status:** `NOT_DUPLICATE`

### Registry Recommendation

`_registry/youtube_video_index.csv` için önerilen kayıt:

```csv
video_id,normalized_url,title,channel,status,codex_status,transcript_hash,candidate_id,first_seen_at,last_seen_at,process_count
UD7gipBWnuY,https://www.youtube.com/watch?v=UD7gipBWnuY,When To Take Trading Profits - Market Wizards Share Their Sell Rules,UNKNOWN_CHANNEL,CANDIDATE,READY_FOR_PYTHON_PROTOTYPE,4804e3dda96a256e801b9a1c359ff07da08c9fb5abaf5593f4ca12c80338e18a,CAND_008_MARKET_WIZARDS_SELL_RULES_MULTI_OVERLAY_V1,2026-05-03,2026-05-03,1
```

> Kanal adı transcript içinde açık ve güvenilir metadata olarak verilmediği için `UNKNOWN_CHANNEL` kabul edildi. Blacklist kararı verilmemelidir.

## 3. High-Level Summary

Bu video, tek bir strateji değil; birkaç deneyimli trader’ın **kâr alma, trend bozulması, abnormal action, offensive/defensive selling, extension, progressive exposure ve drawdown governor** kurallarının birleşimidir.

Ana fikirler:

- **Stan Weinstein:** Hızlı ve volatil piyasada 50-day MA altında temiz kapanış, özellikle stage 3/4 dönüşte agresif satış sebebidir. Key reversal day ve liderlerin 50-day/200-day mesafesi önemli uyarı sinyalidir.
- **Mark Minervini:** Piyasa zayıflığı tek başına satış sebebi değildir; asıl lead indicator kendi pozisyonların ve watchlist’in davranışıdır. Sell into strength, progressive exposure ve “always improve worst case scenario” ana risk prensibidir.
- **Roy / Wesley Mattox:** Selling ikiye ayrılır: offensive selling ve defensive selling. Key reversal day, index extension, 20–25% profit target, moving average break, abnormal news ve expectation breaker olayları exit tetikler.
- **Oliver Kell:** Weekly chart setup seçimi; daily chart trade yönetimi için kullanılır. 20-week/10-week EMA, 5–8 week minimum base, 10-day/20-day MA respect, extension from 10-week ve mini-base execution önemlidir.
- **Christian Flanders:** Boom-and-bust trader için çözüm progressive exposure / anti-martingale, monthly loss cap ve kayıp geldikçe size küçültmedir.

Bu nedenle video `CANDIDATE` olarak işlenmelidir; ancak entry sinyali değil, **exit/risk-management overlay paketi** olarak ele alınmalıdır.

## 4. Why This Is a Candidate

Bu transcript doğrudan kodlanabilir veya prototiplenebilir çok sayıda kural içeriyor:

1. **50-day MA defensive exit**
   - Stock 50-day MA altında temiz kapanış yaparsa satış.
   - Volatil piyasalarda eski “yarısını sat ve bekle” yaklaşımı yerine full exit seçeneği.

2. **Stage 3 / Stage 4 avoidance**
   - Rounding over + 50-day break = Stage 3 uyarısı.
   - 200-day break = kalan pozisyon için daha ciddi trend bozulması.

3. **Key reversal day offensive sell**
   - Yeni high yaptıktan sonra gün içinde terse dönme.
   - Önceki günün low’u altında kapanış.
   - Heavy volume ile oluşursa daha güçlü sinyal.

4. **Profit-taking into strength**
   - 20–25% klasik profit zone.
   - R-multiple bazlı partial exit.
   - Equity curve volatility azaltma.

5. **Improve worst case scenario rule**
   - Stop’u breakeven’a çekmek.
   - Partial alarak kalan pozisyonun original stop’a kadar gelse bile breakeven olması.
   - Kâr garantilemek için partial + stop sync.

6. **Offensive vs defensive sell taxonomy**
   - Offensive: strength/extension/key reversal/profit target.
   - Defensive: MA break, abnormal action, bad news reaction, gap-down, expectation breaker.

7. **Abnormal action / expectation breaker rule**
   - Haber etkisi net anlaşılmasa bile fiyat aksiyonu anormal ise önce risk azalt.
   - “Sell first, ask questions later” mantığı.

8. **Index extension governor**
   - QQQ/Nasdaq benzeri benchmark’ın 50-day MA’dan ~8%+ uzaklaşması risk uyarısı.
   - Özellikle pozisyonlar da extended ise exposure azaltma.

9. **Weekly-to-daily timeframe alignment**
   - Weekly chart setup/context.
   - Daily chart execution/management.
   - 20-week EMA / 10-week EMA trend ve extension değerlendirmesi.

10. **Monthly loss cap / anti-martingale sizing**
    - Ay içinde kayıp büyüdükçe pozisyon boyutu düşür.
    - 5%, 3%, 2%, 1% gibi aylık kayıp eşikleri prototiplenebilir.

## 5. Extracted Core Rules

## 5.1 Stan Weinstein — 50-Day / Stage-Based Defensive Exit

### Rule concept

Modern hızlı ve volatil tape koşullarında:

```text
if close < sma_50d and clean_break:
    exit_position()
```

Stan’in vurgusu:

- Eski piyasada 50-day break ile yarı satış ve bekleme düşünülebilirdi.
- Mevcut yüksek volatilite ortamında temiz 50-day break sonrası tamamen çıkmak daha uygun olabilir.
- 200-day break kalan pozisyon için son savunma değil; genelde çok geç olabilir.

### Prototype parameters

```yaml
ma50_exit_enabled: true
ma50_exit_mode: FULL_EXIT     # FULL_EXIT | HALF_EXIT | REDUCE_TO_CORE
ma50_clean_break_basis: CLOSE  # CLOSE | LOW
ma50_volume_confirm: optional
ma50_stage3_required: false
```

### Stage logic

```text
stage3_warning = rounding_over and close < sma_50d
stage4_risk = close < sma_200d
```

First prototype için `rounding_over` zor ve subjektif olabilir. Basit proxy:

```python
sma_50d_slope_down = sma_50d < sma_50d.shift(10)
price_below_50d = close < sma_50d
stage3_warning = price_below_50d and sma_50d_slope_down
```

## 5.2 Stan Weinstein — Key Reversal Day

Transcriptte verilen tanım mekanik hale getirilebilir:

```text
1. Price makes a new high for the move.
2. Price declines for the day.
3. Close is below prior session low.
4. Heavy volume confirms the reversal.
```

Prototype:

```python
new_high_for_move = high >= highest(high, lookback_n)
declines_for_day = close < open
close_below_prior_low = close < low.shift(1)
heavy_volume = volume > sma(volume, 50) * volume_mult
key_reversal_day = new_high_for_move and declines_for_day and close_below_prior_low and heavy_volume
```

Config:

```yaml
key_reversal_enabled: true
key_reversal_lookback: 50
key_reversal_volume_mult: 1.5
key_reversal_exit_mode: PARTIAL_OR_FULL
```

Suggested reason code:

```text
KEY_REVERSAL_DAY_HEAVY_VOLUME
```

## 5.3 Mark Minervini — Stocks and Watchlist as Lead Indicator

Mark’ın mantığı:

- Market correction başladı diye otomatik cash’e geçilmez.
- Eğer pozisyonlar ve watchlist hâlâ stopları tutuyor ve setup’lar çalışıyorsa elde tutulabilir.
- Market distribution + holdings deterioration + watchlist deterioration birlikte görünürse risk düşürülür.

Prototype için `portfolio_health_score`:

```python
portfolio_health_score = weighted_sum([
    pct_positions_above_stop,
    pct_positions_above_20d,
    pct_positions_up_from_entry,
    avg_unrealized_R,
    pct_watchlist_breakouts_following_through,
    pct_watchlist_above_key_ma,
])
```

Risk governor:

```python
if market_distribution_high and portfolio_health_score < threshold:
    exposure_cap = reduce_exposure_cap()
```

Reason code:

```text
PORTFOLIO_WATCHLIST_DETERIORATION
```

## 5.4 Mark Minervini — Sell Into Strength

Ana prensip:

- Strong move sırasında partial/full satış yaparak equity peak’te kâr hasat edilir.
- Büyük hareketten vazgeçme pahasına volatility ve drawdown düşürülür.
- Bu özellikle swing trader için uygundur.

Mechanic:

```python
if profit_pct >= profit_target_pct and extension_warning:
    partial_exit("SELL_INTO_STRENGTH_EXTENSION")
```

Alternatif R-multiple:

```python
if current_R >= partial_r_multiple:
    partial_exit("SELL_INTO_STRENGTH_R_MULTIPLE")
```

Config:

```yaml
sell_into_strength_enabled: true
profit_target_pct_min: 0.20
profit_target_pct_max: 0.25
partial_exit_pct: 0.50
r_multiple_partial: 2.0
extension_confirm_required: false
```

## 5.5 Mark Minervini — Improve Worst Case Scenario

Bu transcriptin en değerli cümlelerinden biri:

```text
Always improve your worst case scenario.
```

Codable interpretations:

### A) Move stop to breakeven after sufficient progress

```python
if profit_R >= breakeven_trigger_R:
    stop = max(stop, entry_price)
```

### B) Partial profit to finance original risk

Örnek:

- Entry: 100
- Stop: 92
- Risk: 8%
- Price reaches +8%
- Sell half
- Remaining half original stop’a gelse bile total trade yaklaşık breakeven olabilir.

Pseudo:

```python
if profit_pct >= initial_risk_pct:
    partial_exit(0.50)
    keep_or_raise_stop_based_on_mode()
```

### C) Guarantee profit after larger move

```python
if profit_pct >= guarantee_trigger_pct:
    partial_exit(0.50)
    stop = max(stop, entry_price)
```

Reason codes:

```text
MOVE_STOP_TO_BREAKEVEN
RISK_FINANCED_BY_PARTIAL
GUARANTEED_PROFIT_LOCK
```

## 5.6 Roy/Wesley Mattox — Offensive Selling Taxonomy

Offensive selling = işler iyi giderken kârı alma / risk azaltma.

Triggers:

1. Key reversal day
2. Index extension from 50-day MA
3. Leading stocks extended from key MAs
4. Profit target 20–25%
5. R-multiple target
6. Climactic move or extended action

Prototype:

```python
offensive_sell_score = sum([
    key_reversal_day,
    index_ext_above_50d >= 0.08,
    stock_ext_above_10d >= threshold,
    stock_ext_above_50d >= threshold,
    profit_pct >= 0.20,
    current_R >= 3.0,
])

if offensive_sell_score >= offensive_sell_threshold:
    partial_or_full_exit("OFFENSIVE_SELL_SCORE")
```

## 5.7 Roy/Wesley Mattox — Defensive Selling Taxonomy

Defensive selling = sermayeyi korumak için risk azaltma.

Triggers:

1. Break below 50-day MA, especially with volume
2. Two days below 21-day MA
3. Trailing stop
4. Abnormal action
5. Expectation breaker / black swan news
6. Gap-down in leader
7. Sell first, analyze later when price action is abnormal

Prototype:

```python
defensive_sell_score = sum([
    close < sma_50d and volume > avg_volume * 1.2,
    close_below_21d_consecutive >= 2,
    close <= trailing_stop,
    abnormal_gap_down,
    expectation_breaker_event,
    leader_large_range_down,
])

if defensive_sell_score >= defensive_sell_threshold:
    exit_or_reduce("DEFENSIVE_SELL_SCORE")
```

Reason codes:

```text
DEFENSIVE_MA50_BREAK_VOLUME
DEFENSIVE_TWO_DAYS_BELOW_21D
DEFENSIVE_TRAILING_STOP
DEFENSIVE_ABNORMAL_ACTION
DEFENSIVE_EXPECTATION_BREAKER
```

## 5.8 Abnormal Action / Expectation Breaker Rule

Transcriptte DeepSeek örneği üzerinden anlatılan fikir:

- Pozisyon iyi gidiyor olabilir.
- Büyük kârda olunabilir.
- Ama anlatıyı bozan haber / olay gelirse ve fiyat sert tepki verirse önce risk azaltılır.
- Haber detayını tam anlamaya çalışmak yerine price action takip edilir.

QuantLens için iki mod olabilir:

### Price-only abnormal action

```python
abnormal_down_day = (
    gap_down_pct <= -gap_threshold
    and range_pct >= adr_mult * adr_pct
    and close < sma_20d
    and volume > avg_volume * volume_mult
)
```

### Event-tagged abnormal action

Bu ilk etapta production’a alınmamalı; manuel event flag veya future NLP/news integration gerekir.

```yaml
expectation_breaker_event: true
source: manual_or_news_module
```

Recommended initial prototype:

```text
PRICE_ONLY_ABNORMAL_ACTION_V1
```

## 5.9 Index Extension Risk Governor

Transcriptte QQQ/Nasdaq 100 için 50-day MA’dan yaklaşık 8% extension’ın 90th percentile warning olduğundan bahsediliyor.

Prototype:

```python
index_ext_50d = (index_close / index_sma_50d) - 1
index_extension_warning = index_ext_50d >= 0.08
```

Exposure governor:

```python
if index_extension_warning and avg_position_extension_high:
    max_total_exposure = min(max_total_exposure, reduced_cap)
    allow_new_entries = false_or_restricted
```

Config:

```yaml
index_extension_governor_enabled: true
benchmark_symbol: QQQ
index_ext_50d_warn_pct: 0.08
on_warning:
  allow_new_entries: false
  reduce_extended_winners: true
  tighten_stops: true
```

Caveat:

- Transcriptte istatistik örnek olarak verilmiş; farklı evrenlerde doğrulanmalı.
- Crypto / leveraged ETF / high beta equities için eşik ayrı optimize edilmeli.

## 5.10 Oliver Kell — Weekly Context / Daily Management

Oliver’ın framework’ü:

- Weekly chart: setup kalitesi, base süresi, trend bağlamı.
- Daily chart: execution, mini-base, 10/20 EMA management.
- Best stocks trend sırasında genelde 20-week EMA’yı kaybetmez.
- 10-week / 20-week çevresinde base kuran hisseler daha sağlıklı.

### Weekly setup rules

```python
weekly_trend_ok = close_w > ema_20w
base_length_ok = base_weeks >= 5
ideal_base = 5 <= base_weeks <= 8 or multi_month_base
weekly_ma_aligned = ema_10w >= ema_20w or close_w > ema_10w
```

### Daily execution rules

- 3–6 gün mini-base.
- Inside bar / tight range.
- 10/20 EMA civarında contraction.
- Wedge pop veya EMA crossback early-cycle entry.

Prototype entry context can be stored but this intake remains exit-focused.

## 5.11 Oliver Kell — Moving Average Respect Rule

Fikir:

- Hisse trend içinde hangi MA’yı “respect” ediyor?
- 10-day’e üç temas edip tutuyorsa 10-day primary guide olabilir.
- Daha yavaş hisseler için 20-day daha iyi olabilir.
- 10-day shakeout sonrası 20-day’e pivot edilebilir.

Prototype:

```python
ma10_respect_count = count_successful_touches(close, low, ema_10d, lookback)
ma20_respect_count = count_successful_touches(close, low, ema_20d, lookback)

if ma10_respect_count >= 3 and ma20_respect_count == 0:
    active_trend_ma = "EMA_10D"
elif ma20_respect_count >= 2:
    active_trend_ma = "EMA_20D"
```

Exit:

```python
if active_trend_ma == "EMA_10D" and close < ema_10d:
    reduce_or_exit("ACTIVE_MA_10D_LOST")

if active_trend_ma == "EMA_20D" and close < ema_20d:
    reduce_or_exit("ACTIVE_MA_20D_LOST")
```

## 5.12 Oliver Kell — Extension From 10-Week

Oliver’ın sell-side uyarısı:

- Weekly 10-week’ten çok uzaklaşınca dikkat.
- Aynı anda daily 10-day/20-day extension varsa offensive partial mantıklı.

Prototype:

```python
ext_10w = close / ema_10w - 1
ext_10d = close / ema_10d - 1

dual_extension_warning = ext_10w > ext_10w_threshold and ext_10d > ext_10d_threshold
```

Config:

```yaml
weekly_extension_enabled: true
ext_10w_threshold: 0.25   # asset-dependent; validate
ext_10d_threshold: 0.10
exit_mode: PARTIAL_EXIT
```

## 5.13 Christian Flanders — Anti-Martingale / Monthly Loss Cap

Christian’ın ana problemi “boom and bust” davranışı:

- Kazanırken fazla büyümek.
- Kaybedince aynı veya daha büyük size ile devam etmek.
- Çok sayıda 1% riskli trade’in aynı anda stop olmasıyla aylık drawdown’ın kontrolden çıkması.

Çözüm:

- Kayıp geldikçe size düşür.
- Monthly loss cap uygula.
- 5%, 4%, 3% gibi aylık kayıp cap’leri test et.
- Önceki ay kayıpsa sonraki ay cap daha düşük olabilir: 5 → 2 → 1 gibi.

Prototype:

```python
if month_pnl_pct <= -monthly_loss_cap:
    allow_new_entries = false
    max_position_risk_pct = 0

elif month_pnl_pct <= -monthly_warning_level:
    max_position_risk_pct *= size_down_factor
    max_total_exposure *= exposure_down_factor
```

Config:

```yaml
monthly_loss_governor_enabled: true
monthly_loss_cap_pct: 0.05
monthly_soft_warning_pct: 0.03
risk_after_soft_warning_mult: 0.50
risk_after_losing_prev_month_mult: 0.50
sequential_month_caps: [0.05, 0.02, 0.01]
```

Reason codes:

```text
MONTHLY_LOSS_CAP_REACHED
MONTHLY_SOFT_WARNING_SIZE_DOWN
PREVIOUS_MONTH_LOSS_SIZE_DOWN
ANTI_MARTINGALE_RISK_REDUCTION
```

## 6. Strategy Candidate Design

## Candidate Name

`multi_source_sell_rules_overlay_v1`

## Purpose

Bu overlay, entry producer’dan bağımsız olarak çalışan bir exit/risk katmanıdır. Amaç:

- Kârdaki pozisyonları sistematik olarak korumak.
- Kötüleşen pozisyonları ve abnormal action’ı hızlı azaltmak.
- Portfolio-level drawdown’ı sınırlamak.
- Overtrading / revenge / boom-bust davranışını monthly loss governor ile kontrol etmek.
- Weekly/daily multi-timeframe exit kuralları ile MTC_V2 exit pipeline’ını zenginleştirmek.

## Intended Inputs

```yaml
symbol
entry_price
entry_date
position_size_pct
current_close
current_open
current_high
current_low
previous_low
volume
avg_volume_50d
sma_21d
sma_50d
sma_200d
ema_10d
ema_20d
ema_10w
ema_20w
weekly_close
weekly_base_weeks
highest_high_since_entry
profit_pct
current_R
initial_risk_pct
benchmark_close
benchmark_sma_50d
month_pnl_pct
previous_month_pnl_pct
portfolio_health_score
watchlist_health_score
abnormal_event_flag
```

## Intended Outputs

```yaml
exit_decision:
  should_exit: bool
  exit_type: FULL_EXIT | PARTIAL_EXIT | REDUCE_TO_CORE | HOLD | BLOCK_NEW_ENTRIES | SIZE_DOWN
  reason_code: string
  confidence_score: float
  stop_update: float | null
  exposure_cap_update: float | null
  evidence:
    - metric_name
    - metric_value
```

## Reason Code Dictionary

```text
MA50_CLEAN_BREAK_FULL_EXIT
STAGE3_ROUNDING_50D_BREAK
STAGE4_200D_BREAK
KEY_REVERSAL_DAY_HEAVY_VOLUME
SELL_INTO_STRENGTH_20_25
SELL_INTO_STRENGTH_R_MULTIPLE
MOVE_STOP_TO_BREAKEVEN
RISK_FINANCED_BY_PARTIAL
GUARANTEED_PROFIT_LOCK
OFFENSIVE_SELL_SCORE
DEFENSIVE_MA50_BREAK_VOLUME
DEFENSIVE_TWO_DAYS_BELOW_21D
DEFENSIVE_TRAILING_STOP
DEFENSIVE_ABNORMAL_ACTION
DEFENSIVE_EXPECTATION_BREAKER
INDEX_EXTENSION_RISK_GOVERNOR
WEEKLY_20W_LOST
ACTIVE_MA_10D_LOST
ACTIVE_MA_20D_LOST
DUAL_DAILY_WEEKLY_EXTENSION
MONTHLY_LOSS_CAP_REACHED
MONTHLY_SOFT_WARNING_SIZE_DOWN
ANTI_MARTINGALE_RISK_REDUCTION
NO_EXIT_RULE_TRIGGERED
```

## 7. MTC_V2 Integration Notes

### Best integration layer

Bu video için en doğru katman:

```text
7. EXIT RULES
```

İkinci ve üçüncü etki alanı:

```text
4. POSITION MANAGER
5. POSITION SIZING
PortfolioState / Guards
```

### Suggested modules

```text
exit_profit_harvest_overlay
exit_ma_defensive_overlay
exit_key_reversal_overlay
risk_monthly_loss_governor
risk_index_extension_governor
position_worst_case_improver
```

### Pipeline priority proposal

MTC_V2 exit-first canonical rule ile uyumlu öneri:

```text
1. HARD_SL / initial protective SL
2. ABNORMAL_ACTION / expectation breaker
3. MONTHLY_LOSS_CAP portfolio block / forced risk-off
4. MA50 / MA21 defensive exits
5. KEY_REVERSAL_DAY offensive exit
6. INDEX_EXTENSION risk governor / exposure trim
7. SELL_INTO_STRENGTH profit harvest
8. WORST_CASE_IMPROVER stop/partial update
9. ACTIVE_MA trend guide exit
10. OPP_SIGNAL / FILTER_BLOCK / TIME_STOP
```

Not:

- `WORST_CASE_IMPROVER` her zaman exit üretmez; bazen sadece stop günceller veya partial tetikler.
- Portfolio-level governors tek pozisyon exit’inden ayrı değerlendirilmelidir.

## 8. Backtest / Prototype Hypotheses

## H1 — 50-Day MA Clean Break Exit

Compare:

```text
A) No MA50 exit
B) Half exit at close < 50d
C) Full exit at close < 50d
D) Full exit only if close < 50d and volume > 1.2x avg
```

Metrics:

- max drawdown
- average giveback from peak open profit
- false exit rate
- re-entry opportunity count
- net CAGR / MAR

## H2 — Key Reversal Offensive Sell

Compare:

```text
A) Ignore key reversal
B) 50% partial on key reversal
C) full exit on key reversal
D) tighten stop only
```

Metrics:

- avoided drawdown after signal
- missed upside after signal
- signal precision
- signal recall for major tops

## H3 — Sell Into Strength vs Hold

Compare:

```text
A) Hold until stop/trend exit
B) sell 50% at +20%
C) sell 100% at +25%
D) sell 50% at 2R/3R with extension confirmation
```

Metrics:

- equity curve volatility
- max drawdown
- right-tail capture
- median trade expectancy
- turnover and exposure efficiency

## H4 — Improve Worst Case Scenario Rule

Compare:

```text
A) Original stop unchanged
B) move stop to breakeven after +1R
C) partial at +1R and keep original stop
D) partial at +2R and stop to breakeven
```

Metrics:

- percent trades turning winner to loser
- stopped-before-big-move rate
- average R
- expectancy
- max adverse excursion after +1R

## H5 — Monthly Loss Governor

Compare:

```text
A) no monthly cap
B) 5% hard cap
C) 3% soft cap + 5% hard cap
D) sequential caps: 5%, then 2%, then 1% after losing months
```

Metrics:

- annual return
- max drawdown
- ulcer index
- longest recovery period
- number of blocked trades
- opportunity cost after cap

## H6 — Index Extension Governor

Compare:

```text
A) no extension governor
B) block new entries if QQQ > 8% above 50d
C) trim winners if QQQ > 8% above 50d and positions extended
D) tighten stops only
```

Metrics:

- avoided corrections
- missed melt-up gains
- drawdown reduction
- CAGR impact

## 9. Data / Feature Requirements

Minimum OHLCV:

```text
symbol daily OHLCV
benchmark daily OHLCV, e.g. QQQ or SPY
weekly resampled OHLCV
entry records and position lifecycle
portfolio equity curve
monthly PnL state
watchlist or universe health stats, optional but useful
```

Derived features:

```text
sma_21d
sma_50d
sma_200d
ema_10d
ema_20d
ema_10w
ema_20w
avg_volume_50d
ADR / ATR
extension from moving averages
R-multiple
profit_pct
highest_high_since_entry
month_pnl_pct
consecutive closes below MA
key reversal flag
abnormal action flag
```

## 10. Implementation Warnings / Ambiguities

### 1. Multi-speaker transcript

Bu transcript tek bir sistem değildir. Kurallar farklı trader stillerine aittir. Hepsini aynı anda açmak overfit ve conflict riski yaratır.

Öneri:

- Önce modüler flags.
- Her modül ayrı test.
- Sonra ensemble/score yaklaşımı.

### 2. Timeframe conflict

- Stan 50-day clean break ile hızlı çıkmayı savunuyor.
- Oliver weekly 10/20 week trend context’e daha çok önem veriyor.
- Ajay Jani gibi long-hold yaklaşımıyla bazı kurallar çelişebilir.

Bu nedenle config profile gerekli:

```yaml
profile: SWING_FAST | POSITION_LEADER | HYBRID
```

### 3. Abnormal action event detection

Transcriptte haber/narrative kırılması anlatılıyor. Saf OHLCV ile haberin ne olduğu bilinemez.

İlk prototype:

- Event flag olmadan price-only abnormal action.
- Sonraki aşama: news/NLP/event tagging.

### 4. Monthly loss governor opportunity cost

Loss cap drawdown’ı azaltabilir ama recovery fırsatlarını kaçırabilir. Bu nedenle sadece net return değil, MAR ve recovery period ölçülmeli.

### 5. Extension thresholds asset-dependent

QQQ 8% above 50-day uyarısı equity index için mantıklı olabilir; crypto, leveraged ETFs ve low-float stocks için farklıdır.

## 11. Recommended Python Prototype Plan

### Phase 1 — Feature Calculator

Create isolated feature functions:

```text
calc_ma_breaks()
calc_key_reversal_day()
calc_extension_metrics()
calc_profit_r_metrics()
calc_abnormal_action_price_only()
calc_monthly_loss_state()
calc_active_ma_respect()
```

### Phase 2 — Rule Modules

Implement separately:

```text
rule_ma50_clean_break_exit()
rule_key_reversal_exit()
rule_sell_into_strength()
rule_worst_case_improver()
rule_index_extension_governor()
rule_monthly_loss_governor()
rule_active_ma_exit()
```

### Phase 3 — Reason-code logging

Every decision must output:

```yaml
reason_code
thresholds_used
observed_values
position_state_before
position_state_after
```

### Phase 4 — Ablation Backtests

Run each module individually before combining.

Required combinations:

```text
BASELINE
BASELINE + MA50
BASELINE + SELL_INTO_STRENGTH
BASELINE + WORST_CASE_IMPROVER
BASELINE + MONTHLY_LOSS_GOVERNOR
BASELINE + ALL_EXIT_OVERLAYS
```

### Phase 5 — Profile configs

Test at least:

```yaml
SWING_FAST:
  sell_into_strength: aggressive
  ma50_exit: full
  monthly_loss_cap: strict

POSITION_LEADER:
  sell_into_strength: partial
  ma50_exit: reduce_to_core
  weekly_trend_context: enabled

HYBRID:
  sell_into_strength: partial
  ma50_exit: full_if_volume_confirmed
  worst_case_improver: enabled
```

## 12. Candidate Registry Recommendation

`strategy_candidate_registry.csv` için önerilen satır:

```csv
candidate_id,source_video_id,name,type,status,priority,usefulness_score,primary_modules,needs_web_research,notes
CAND_008_MARKET_WIZARDS_SELL_RULES_MULTI_OVERLAY_V1,UD7gipBWnuY,multi_source_sell_rules_overlay_v1,EXIT_RULES_AND_RISK_GOVERNOR,READY_FOR_PYTHON_PROTOTYPE,P1,9,"ma50_exit;key_reversal;sell_into_strength;worst_case_improver;monthly_loss_governor;index_extension_governor",false,"Multi-speaker sell rules package. Entry producer değil; MTC_V2 exit/position/risk overlay için prototiplenmeli."
```

## 13. Final Decision

### Verdict

```text
CANDIDATE / READY_FOR_PYTHON_PROTOTYPE
```

### Why not WIKI_ONLY?

Çünkü transcriptte doğrudan kodlanabilir kurallar var:

- 50-day MA clean break exit
- key reversal day definition
- 20–25% profit harvest
- R-multiple partial
- breakeven / worst-case improvement
- two days below 21-day
- index extension governor
- monthly loss cap
- anti-martingale sizing

### Why not direct Pine implementation yet?

- Çok sayıda farklı trader kuralı var; önce Python’da modüler ablation gerekli.
- Kuralların bazıları birbiriyle çelişebilir.
- Abnormal action için haber/event tagging yok.
- Weekly/daily alignment ve MTC/Python parity dikkat ister.

### Recommended Next Action

1. `multi_source_sell_rules_overlay_v1` için Python-only prototype spec oluştur.
2. MTC_V2’ye veya Pine’a dokunma.
3. İlk testte sadece existing entry producer trade’lerinin çıkışını bu overlay ile yeniden simüle et.
4. Her rule için ayrı ablation raporu üret.
5. En iyi 2–3 rule setini daha sonra MTC_V2 exit layer’a aday olarak taşı.

## 14. Files / Safety Notes

- Created report only: `QL_INTAKE_008_UD7gipBWnuY_market_wizards_sell_rules.md`
- `01_PINE/MTC_V2.pine`: **not modified**
- Production Python runner: **not modified**
- Backtest / optimization: **not run**
- Secrets / API keys / broker credentials: **not touched**
- Large CSV / data bundle / cache: **not created**
