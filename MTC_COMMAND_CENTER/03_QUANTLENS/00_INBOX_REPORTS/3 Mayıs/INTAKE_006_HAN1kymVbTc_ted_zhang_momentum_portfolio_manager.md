# QuantLens Transcript Intake Report — 006 / 068

## 1. Metadata

- **Report ID:** `INTAKE_006_HAN1kymVbTc`
- **Source URL:** `https://youtu.be/HAN1kymVbTc?si=phH70Py9VkhrRlBA`
- **Normalized URL:** `https://www.youtube.com/watch?v=HAN1kymVbTc`
- **Video ID:** `HAN1kymVbTc`
- **Title:** `Trading $30 Million at Age 25 - The Story of Ted Zhang, Momentum Portfolio Manager`
- **Series / Theme:** TraderLion / TraderLine podcast style interview — Ted Zhang, Rever Asset Management, thematic catalyst momentum, portfolio risk, daily journaling, super-stock selection
- **Channel:** `UNKNOWN_CHANNEL`
  - Transcript içinde host/podcast bağlamı var; fakat kanal adı ve kanal id güvenilir metadata olarak ayrıca verilmedi. Intake kuralına göre `UNKNOWN_CHANNEL` kullanıldı.
- **Source transcript file:** `Trading $30 Million at Age 25 - The Story of Ted Zhang, Momentum Portfolio Manager.md`
- **Prompt file used:** `00_quantlens_transcript_intake_prompt.md`
- **Generated date:** `2026-05-03`
- **Transcript hash method:** lowercase + whitespace-normalized SHA256 over full transcript text
- **Transcript hash:** `92de637e0df8bdcee95bebe1d44c9e3002596531b1ef452867c072d13cb30afa`

---

## 2. Intake Verdict

- **Classification:** `CANDIDATE`
- **Codex Status Önerisi:** `READY_FOR_PYTHON_PROTOTYPE`
- **Candidate Priority:** `P0 / P1 — High-value selection + portfolio-risk candidate`
- **Usefulness Score:** `9 / 10`
- **Coding Readiness Score:** `8 / 10`
- **MTC_V2 Fit Score:** `8 / 10`
- **Wiki Note Also Valuable:** `YES`

### Verdict Summary

Bu transcript `WIKI_ONLY` değildir. İçerikte çok sayıda psikoloji, kariyer ve kitap notu var; ancak ana değer doğrudan kodlanabilir bir sistem katmanı veriyor:

> **Liquid + high ADR + linear + hot theme/catalyst + absolute strength + stage/market context** filtrelerinden geçen momentum liderlerini seç; entry sonrası riskini portföy düzeyinde açık risk, correlation/theme bucket ve sell-rule disipliniyle kontrol et; günlük journal/routine ile karar kalitesini standartlaştır.

Bu video önceki raporlarla şu şekilde birleşir:

- `002` entry tactic library verir.
- `003` HV/RS setup framework verir.
- `004` VCP/correction leader ve progressive exposure katmanı verir.
- `005` RS/regime ve positive/negative feedback katmanı verir.
- `006` bunların üstüne **stock selection recipe + portfolio construction/risk + habit/journal process** ekler.

QuantLens açısından bu, tek başına “entry sinyali” değildir. Daha doğru kullanım:

```text
Universe Filter / Stock Selection Engine
+ Theme/Catalyst Scorer
+ Liquidity/ADR/Linearity Quality Gate
+ Portfolio Risk Guard
+ Journal/Routine Checklist Export
```

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
  - `003` video id: `NwgJQyoUAaI`
  - `004` video id: `M_tD6X0CSOI`
  - `005` video id: `jD4nynuWfEU` / transcript title match handled previously
  - Bu video id: `HAN1kymVbTc`
- **Action:** Gerçek repo'ya yazılmadan önce Codex registry dosyalarını okuyup `video_id` ve `transcript_hash` ile duplicate kontrolünü tekrar yapmalıdır.

### Registry Row Draft

```csv
video_id,normalized_url,title,channel,status,candidate_id,transcript_hash,first_seen_at,last_seen_at,process_count
HAN1kymVbTc,https://www.youtube.com/watch?v=HAN1kymVbTc,"Trading $30 Million at Age 25 - The Story of Ted Zhang, Momentum Portfolio Manager",UNKNOWN_CHANNEL,CANDIDATE,CAND_20260503_TED_ZHANG_MAGIC_ELIXIR_MOMENTUM_HAN1kymVbTc,92de637e0df8bdcee95bebe1d44c9e3002596531b1ef452867c072d13cb30afa,2026-05-03,2026-05-03,1
```

---

## 4. Channel Quality Check

- **Channel:** `UNKNOWN_CHANNEL`
- **Blacklist decision:** `NO_BLACKLIST_DECISION`
- **Reason:** Kanal adı / kanal id güvenilir şekilde verilmediği için blacklist veya watchlist kararı verilmedi.
- **Suggested quality update after repo check:** Eğer aynı kanal önceki TraderLion/TraderLine içerikleriyle eşleşirse `GOOD` adaylığı güçlenir; çünkü mevcut batch içinde 002–006 arası videoların çoğu `CANDIDATE` kalitesinde.
- **Batch pattern note:** Bu seri şu ana kadar momentum / RS / VCP / entry tactic açısından yüksek sinyal yoğunluğu taşıyor. Kanal id doğrulanırsa kalite registry'de `candidate_count += 1` yazılmalıdır.

---

## 5. Strategy Candidate

### Candidate ID

`CAND_20260503_TED_ZHANG_MAGIC_ELIXIR_MOMENTUM_HAN1kymVbTc`

### Candidate Name

**Thematic Catalyst Momentum + Magic Elixir Stock Selection & Portfolio Risk Engine**

### Strategy Family

- Thematic momentum / catalyst momentum
- CANSLIM-inspired growth momentum, but not strict earnings/sales-only
- Stage analysis / trend-following
- Absolute strength ranking
- Liquidity + ADR quality screening
- Linearity / trend smoothness scoring
- Portfolio open-risk control
- Theme-bucket construction
- Journal/routine-based execution discipline

### Primary Market

- **Best native fit:** US equities
- **Reason:** Transcript; stocks, individual leadership, themes, catalysts, ADR, liquidity, AUM constraints, Rever Asset Management process, absolute strength ratings and staged trend structure üzerine kurulu.
- **Crypto adaptation:** Partial. Crypto’da earnings/sales yok; ama hot theme, catalyst, liquidity, ADR/ATR, absolute strength, linearity, stage/trend ve portfolio risk mantığı OHLCV + benchmark verisiyle uygulanabilir.
- **Futures adaptation:** Weak. Bu video ağırlıklı olarak single-stock momentum selection ve portfolio construction anlatıyor.

---

## 6. Core Thesis Extracted

### 6.1 Temporary Edges vs. Timeless Edges

Transcriptin ilk bölümü SPAC dönemindeki geçici edge ile başlıyor. $10 NAV tabanı ve hot-theme speculation, COVID sonrası likidite ortamında asimetrik görünmüş; ancak edge, makro/frothy koşullara bağlı olduğu için kaybolmuş.

Kodlanabilir çıkarım:

```text
Reject or downweight edges that depend only on temporary market microstructure / mania conditions.
Prefer candidates rooted in repeatable technical/fundamental behavior:
  liquidity
  trend
  relative/absolute strength
  catalyst
  market context
  risk-defined entry
```

### 6.2 Main Style: Thematic + Catalyst Momentum

Ted Zhang kendi stilini “thematic and catalyst momentum trading” veya genel çerçevede “trend following” olarak tanımlıyor. CANSLIM kökenli ama klasik CANSLIM kadar katı değil; bazı hot theme fırsatlarında earnings/sales yoksa bile işlem yapılabiliyor.

Kodlanabilir çıkarım:

```text
candidate_score = trend_score
                + theme_score
                + catalyst_score
                + liquidity_score
                + adr_score
                + linearity_score
                + absolute_strength_score
                + market_context_score
```

### 6.3 Risk Is Losing Money, Not Merely Volatility

Transcriptte risk, pratik açıdan “money loss / permanent loss potential” olarak ele alınıyor. Bu yaklaşım QuantLens için portföy düzeyi open-risk kontrolüne çevrilmelidir.

```text
open_risk = sum(position_qty * max(0, entry_or_current_price - stop_price))
open_risk_pct = open_risk / equity
```

Bu risk sadece tekil pozisyon stop mesafesi değil; aynı tema veya korelasyon bucket’ında yığılma varsa portföy şok riskini de hesaba katmalıdır.

### 6.4 Do Not Just Pick the Leader; Build Theme Buckets When Needed

Özellikle profesyonel para yönetiminde tek hisse riskini azaltmak için tema bucket yaklaşımı değerli:

```text
AI bucket
  top 1-3 liquid/linear leaders
Rare earth / metals bucket
  ETF + top leaders
Space bucket
  top leaders + optional ETF proxy
Crypto equity bucket
  top leaders + BTC/ETH proxy if allowed
```

Bu, “ben lideri kesin biliyorum” varsayımını azaltır. Ancak bucket içindeki korelasyonun kriz anında 1’e yaklaşabileceği mutlaka risk guard olarak izlenmelidir.

---

## 7. Extracted System Modules

## 7.1 Magic Elixir / Super Stock Criteria Module

### Concept

Transcriptte ideal trade için “magic elixir / super stock criteria” adı verilen recipe anlatılıyor. Çekirdek maddeler:

1. Liquid
2. High ADR / ATR
3. Linear trend behavior
4. Previous history of big linear moves, unless recent IPO
5. Hot theme / narrative / story
6. Catalyst
7. Optional but valuable fundamentals
8. Market context + price/volume confirmation
9. Absolute strength across multiple lookbacks

### Candidate Logic

```text
liquidity_ok = avg_dollar_volume_20d >= threshold_by_account_size
adr_ok = adr_pct_20d >= min_adr_pct
linear_ok = linearity_score >= min_linearity
stage_ok = weekly_stage in [STAGE_2, EARLY_STAGE_2]
theme_ok = theme_score >= min_theme_score
catalyst_ok = recent_catalyst_detected OR hot_theme_active
strength_ok = abs_strength_1m >= 90 OR abs_strength_3m >= 90 OR abs_strength_6m >= 90
market_ok = market_regime != HOSTILE

candidate_ok = liquidity_ok
               AND adr_ok
               AND linear_ok
               AND stage_ok
               AND strength_ok
               AND market_ok
               AND (theme_ok OR catalyst_ok OR fundamentals_ok)
```

### Suggested Fields

```yaml
magic_elixir:
  liquidity_min_adv_usd: 300000000   # configurable; portfolio-size dependent
  adr_min_pct: 3.0
  adr_preferred_pct: 4.0
  abs_strength_min: 90
  abs_strength_preferred: 95
  linearity_min: 0.65
  stage_allowed: [EARLY_STAGE_2, STAGE_2]
  require_theme_or_catalyst: true
  require_fundamentals: false
```

### MTC_V2 Mapping

- `Entry Gate`: stock-level quality gate before strategy entry.
- `Position Sizing`: stronger candidate score can allow higher risk tier.
- `PortfolioState Guard`: if liquidity/ADR/theme concentration fails, cap or block entry.
- `Visualization`: candidate badges, reason codes, no-trade labels.

---

## 7.2 Liquidity Filter

### Concept

Transcriptte SPAC warrants örneği önemli risk dersi: illiquid enstrümanda büyüklük arttıkça çıkış yapılamaz; trader kendi ayak izine basar.

### Candidate Logic

```text
avg_dollar_volume = sma(close * volume, 20)
position_adv_pct = planned_notional / avg_dollar_volume
liquidity_ok = avg_dollar_volume >= min_adv_usd
               AND position_adv_pct <= max_position_adv_pct
```

### Suggested Thresholds

```yaml
liquidity:
  personal_small_account_min_adv_usd: 20000000
  professional_book_min_adv_usd: 300000000
  max_position_adv_pct: 0.005      # planned position <= 0.5% ADV
  reject_if_spread_pct_gt: 0.75
```

### Reason Codes

```text
NO_TRADE_ILLIQUID
NO_TRADE_POSITION_TOO_LARGE_FOR_ADV
NO_TRADE_SPREAD_TOO_WIDE
```

---

## 7.3 ADR / ATR Opportunity Filter

### Concept

Turbo/aggressive portfolio için 1% günlük hareket yapan hisse cazip değil; hedef 3–5% ADR/ATR veya yeterli oynaklık ve 2–8 haftada anlamlı move potansiyeli.

### Candidate Logic

```text
adr_pct_20 = mean((high - low) / close * 100, 20)
atr_pct_14 = atr(14) / close * 100

opportunity_ok = adr_pct_20 >= min_adr_pct
                 OR atr_pct_14 >= min_atr_pct
```

### Guard

```text
too_volatile_for_size = adr_pct_20 > max_adr_pct_for_current_position_size
```

Bu guard MTC_V2 position sizing ile bağlanmalıdır:

```text
if adr_pct_20 > 10:
  risk_pct_cap = min(risk_pct, high_volatility_cap)
```

---

## 7.4 Linearity / Trend Quality Score

### Concept

Ted’in en önemli ayrımlarından biri “linear” hisse. Eğer hisse bucking bronco gibi davranıyorsa yüzde olarak çok yükselse bile trader pozisyonda kalamayabilir.

### Proposed Linearity Features

```text
ma_respect_score:
  pct_closes_above_10ema during trend
  pct_closes_above_20ema during trend
  pct_closes_above_50sma during trend

pullback_quality_score:
  avg_pullback_depth_atr
  pullbacks_orderly = down_volume < up_volume or volume_contracts_on_pullbacks

trend_smoothness_score:
  r2 of log(close) over lookback
  normalized volatility around regression line
  max adverse excursion after breakout

gap_noise_penalty:
  count_large_down_gaps
  count_failed_breakouts
```

### Pseudocode

```text
linearity_score = 0.30 * ma_respect_score
                + 0.25 * trend_smoothness_score
                + 0.20 * pullback_quality_score
                + 0.15 * low_gap_noise_score
                + 0.10 * constructive_volume_score
```

### Thresholds

```text
linearity_score >= 0.75  -> A quality
linearity_score >= 0.60  -> tradable
linearity_score < 0.60   -> reject or smaller size
```

---

## 7.5 Stage Analysis Gate

### Concept

Stan Weinstein stage analysis, Ted’in chart okuma sürecinde ilk filtrelerden biri. İlk bakışta stage 1/2/3/4 ayrımı yapılıp, özellikle stage 2 veya early stage 2 trendler tercih ediliyor.

### Candidate Logic

```text
weekly_ma10 = sma(weekly_close, 10)
weekly_ma30 = sma(weekly_close, 30)
weekly_ma30_slope = slope(weekly_ma30, n=10)

stage2 = close > weekly_ma10 > weekly_ma30
         AND weekly_ma30_slope > 0
         AND relative_strength_rank improving

early_stage2 = base_breakout
               AND close crosses above weekly_ma30
               AND weekly_ma30_slope turning up
```

### Reason Codes

```text
NO_TRADE_NOT_STAGE2
NO_TRADE_STAGE3_TOPPING
NO_TRADE_STAGE4_DOWNTREND
```

---

## 7.6 Theme / Catalyst Scorer

### Concept

CANSLIM’in klasik earnings/sales şartı yumuşatılıyor. Crypto, quantum, AI, rare earth, space gibi temalarda geleneksel fundamentals eksik olabilir; yine de momentum fırsatı olabilir.

### Candidate Logic

```text
theme_score = sector_momentum_score
            + peer_group_breakout_score
            + news_frequency_score
            + social/narrative_attention_score
            + institutional_flow_proxy

catalyst_score = earnings_surprise_score
               + revenue_acceleration_score
               + guidance_revision_score
               + product_launch_score
               + regulatory_change_score
               + partnership_score
               + management_change_score
```

### Practical Implementation Notes

İlk Python prototype’da NLP/news zorunlu değildir. Basit, deterministic proxy ile başlanmalı:

```text
price_volume_catalyst_proxy:
  gap_up_pct >= X
  volume_ratio >= Y
  close_range >= Z
  abs_strength_rank >= threshold
```

Daha sonra web/news module opsiyonel eklenebilir.

---

## 7.7 Absolute Strength Multi-Lookback Rank

### Concept

Ted, “relative to S&P” yerine tüm evrene göre en güçlü hisseleri bulmak için absolute strength kullanmayı seviyor. 1m, 3m, 6m, 12m lookback değerlendiriliyor.

### Candidate Logic

```text
ret_1m = close / close_21 - 1
ret_3m = close / close_63 - 1
ret_6m = close / close_126 - 1
ret_12m = close / close_252 - 1

rank_1m = percentile_rank(ret_1m, universe)
rank_3m = percentile_rank(ret_3m, universe)
rank_6m = percentile_rank(ret_6m, universe)
rank_12m = percentile_rank(ret_12m, universe)

abs_strength_score = max(rank_1m, rank_3m, rank_6m, rank_12m)
strength_ok = abs_strength_score >= 90
```

### Enhancements

```text
prefer if:
  rank_1m > 95 OR rank_3m > 95
  AND rank_6m > 80
  AND stock is not > max_extension_from_20ema
```

---

## 7.8 Market Context Gate

### Concept

Market context, stock/theme/portfolio riskin üst filtresi. Güçlü hisse bile yanlış markette başarısız olabilir. Transcriptte “market context with price and volume characteristics of market, stock and theme” vurgusu var.

### Candidate Logic

```text
market_context_score = index_trend_score
                     + breadth_score
                     + leader_action_score
                     + theme_participation_score
                     - distribution_penalty
```

### States

```text
AGGRESSIVE_LONG:
  allow full candidate score usage
  allow progressive exposure

CAUTIOUS_LONG:
  pilot only
  reduce position size

DEFENSIVE:
  no new high-beta positions
  only existing winners with tight stop

CASH / RISK_OFF:
  block entries except test mode
```

---

## 7.9 Portfolio Open-Risk & Theme Bucket Guard

### Concept

Video, profesyonel para yönetimi tarafında tekil setup’tan daha önemli bir ders veriyor: correlation kriz anında 1’e yaklaşabilir. AI, data center, energy, rare earth gibi ayrı görünen temalar aynı macro shock’ta birlikte düşebilir.

### Candidate Logic

```text
position_risk_pct = abs(entry_price - stop_price) * qty / equity
bucket_risk_pct = sum(position_risk_pct for same theme bucket)
portfolio_open_risk_pct = sum(position_risk_pct for all positions)

if portfolio_open_risk_pct > max_open_risk:
  block_new_entries

if bucket_risk_pct > max_bucket_risk:
  block_or_reduce_same_bucket_entries
```

### Suggested Config

```yaml
portfolio_risk:
  max_initial_risk_per_trade_bps: 25
  preferred_initial_risk_per_trade_bps: 15
  max_open_risk_pct_aggressive: 3.0
  max_open_risk_pct_cautious: 1.0
  max_theme_bucket_risk_pct: 1.25
  max_single_name_weight_pct: 15
  max_bucket_weight_pct: 35
```

### MTC_V2 Mapping

- `PortfolioState`: add `theme_bucket`, `open_risk_pct`, `bucket_risk_pct`
- `Entry Gate`: `portfolio_risk_guard`
- `Position Sizing`: reduce size if bucket risk is high
- `Exit Rules`: tighten stops when portfolio stress expands

---

## 7.10 Habit / Journal / Routine Engine

### Concept

Transcriptin son bölümleri trade sinyali değil ama sistem kalitesi açısından çok değerli. Ted journal ile pre-market reminders, market acceptance, open/closed trade status, breadth/focus list, recent trade stats, frustration level, right-to-play-larger gibi kontroller yapıyor.

Bu, QuantLens’te doğrudan strategy signal değil; ama **research runner ve daily report template** için çok değerli.

### Daily Checklist Draft

```yaml
daily_journal:
  date:
  market_state:
  path_of_least_resistance:
  focus_list_breadth: GREEN_ORANGE_RED
  recent_closed_trade_quality:
  current_positions_health:
  am_i_frustrated: YES_NO
  have_i_earned_the_right_to_play_larger: YES_NO
  theme_inflows:
  theme_outflows:
  candidate_watchlist:
  tomorrow_focus_list:
  bottom_line_expectation:
```

### Weekly Checklist Draft

```yaml
weekly_review:
  review_biggest_20_winners:
  review_biggest_20_mistakes:
  update_theme_buckets:
  update_leaderboard:
  update_open_risk:
  update_model_book_examples:
  adjust_max_exposure_for_market_context:
```

### Codex Utility

Bu modül strategy backtest engine içine değil, `reports/` veya `workflow/` içine konmalıdır:

```text
research/reports/daily_momentum_journal_template.md
research/reports/weekly_superstock_review_template.md
```

---

## 8. Candidate System Design

### 8.1 Pipeline Overview

```text
0. Universe Load
   - US equities universe
   - liquidity data
   - sector/theme labels if available

1. Market Context
   - index trend
   - breadth
   - distribution/accumulation proxy
   - leader participation

2. Absolute Strength Ranking
   - 1m / 3m / 6m / 12m percentile ranks
   - top 5–10% focus list

3. Magic Elixir Quality Filter
   - liquidity
   - high ADR/ATR
   - linearity
   - stage analysis
   - theme/catalyst/fundamental proxy

4. Setup Detector
   - VCP/base
   - high-volume gap
   - reclaim/shakeout
   - up-the-right-side compression
   - pullback to moving average/support

5. Entry Tactic Selection
   - not this video’s primary edge; reuse 002/003 modules
   - range breakout
   - undercut & rally
   - HVC / volume support
   - whole-number support

6. Portfolio Risk Guard
   - per-trade risk bps
   - bucket risk
   - open risk
   - correlation shock flag

7. Position Sizing
   - candidate score tier
   - market context tier
   - risk cap

8. Exit Management
   - stop loss
   - moving average trail
   - abnormal action detector
   - sell-into-strength optional
   - climax / ATR extension optional

9. Reporting
   - daily candidate list
   - reason codes
   - no-trade reasons
   - journal export
```

---

## 9. Python Prototype Recommendation

### Do Not Start With Full NLP

İlk etapta hot theme / catalyst kısmını haber NLP ile değil, fiyat-hacim proxy ile kodlamak daha sağlamdır.

### Prototype v0.1

```text
Input:
  OHLCV parquet/csv bundle
  optional symbol metadata: sector, industry
  benchmark data: SPY/QQQ/IWM

Output:
  candidate_scores.csv
  daily_focus_list.csv
  rejected_with_reasons.csv
  portfolio_risk_sim.csv
```

### Minimum Features

```text
- avg_dollar_volume_20
- adr_pct_20
- atr_pct_14
- abs_strength_rank_1m/3m/6m/12m
- stage2 flag
- linearity_score
- high_volume_gap flag
- close_range
- ma_respect_score
- market_context_state
- open_risk_pct simulated
- bucket exposure if sector/theme metadata exists
```

### Candidate Score Formula v0.1

```text
score = 0
score += 20 if liquidity_ok else -999
score += 15 if adr_ok else -10
score += 20 * linearity_score
score += 15 if stage2 else -20
score += 15 * abs_strength_score_normalized
score += 10 if high_volume_or_catalyst_proxy else 0
score += 10 if market_context_supportive else -20
score -= 15 if extension_too_high
score -= 20 if bucket_risk_too_high
```

---

## 10. MTC_V2 Integration Notes

### 10.1 What Should Be Reused From MTC_V2

- Position manager
- Stop loss / TP / trailing infrastructure
- Risk pct sizing
- PortfolioState guards
- Entry gates
- Regime lock
- Cooldown / max entries
- Filter-block reason codes

### 10.2 What Should Not Be Forced Into Pine Initially

Do not immediately implement theme/catalyst/linearity universe-ranking in Pine. Pine is weak for universe ranking and portfolio-level scanning.

Correct split:

```text
Python:
  universe ranking
  candidate scoring
  theme/bucket risk
  research/backtest

Pine:
  only later, one-symbol execution/visualization
  selected candidate confirmation
  alerts
```

### 10.3 Suggested Future Pine Scope

Only after Python prototype proves value:

```text
- single-symbol Magic Elixir overlay
- stage gate
- ADR/liquidity display
- linearity badge
- entry/exit labels
- WunderTrading alert only for selected symbols
```

---

## 11. Backtest / Research Plan

### Stage A — Data Prep

```text
- US stock OHLCV universe
- split/dividend adjusted data preferred
- delisting/survivorship handling if possible
- benchmark SPY/QQQ/IWM
- sector/industry labels optional
```

### Stage B — Candidate Ranking Test

Test whether top-ranked symbols outperform low-ranked symbols after signal date.

```text
For each day:
  compute candidate_score
  bucket into deciles
  measure forward returns: 5d, 10d, 20d, 40d, 60d
  compare drawdown and hit rate
```

### Stage C — Setup + Entry Combination

Combine `006` stock selection with prior modules:

```text
006 selection gate
+ 003 setup detector
+ 002 entry tactic
+ 004 correction leader / VCP
+ 005 regime filter
```

### Stage D — Portfolio Simulation

```text
- max positions
- max theme bucket exposure
- max open risk
- per-trade risk 15–25 bps initial
- progressive exposure when recent trades work
- reduce risk after stop cluster / drawdown
```

### Stage E — Walk-Forward

```text
Train / calibrate thresholds on prior period
Validate on next period
Repeat by market regime:
  2020 momentum mania
  2021 choppy momentum
  2022 bear market
  2023 recovery
  2024 AI leadership
```

---

## 12. Key Rules Extracted

### Rule 1 — Avoid Illiquidity

```text
IF avg_dollar_volume < threshold
OR planned_position_notional > max_position_adv_pct * avg_dollar_volume
THEN reject.
```

### Rule 2 — Prefer High ADR But Cap Risk

```text
IF adr_pct between 3 and 8:
  opportunity quality improves.
IF adr_pct too high:
  cap size.
```

### Rule 3 — Prefer Linear Trends

```text
IF price respects 10/20 EMA or 10/20-week MA
AND pullbacks are controlled
AND trend smoothness is high
THEN candidate quality improves.
```

### Rule 4 — Theme/Catalyst Can Substitute for Fundamentals

```text
IF fundamentals_missing
BUT theme_score high
AND catalyst/price-volume confirmation present
THEN still tradable as momentum candidate.
```

### Rule 5 — Top 1–2 Leaders Preferred

```text
Within each theme/group:
  rank by absolute strength + liquidity + linearity
  prefer top 1–2 names
  avoid laggards unless special contrarian module is active.
```

### Rule 6 — Bucket Instead of Overconfidence

```text
IF theme strong but exact leader uncertain:
  build controlled bucket
  cap total bucket risk
  avoid false diversification.
```

### Rule 7 — Do Not Confuse Diversification With Protection

```text
IF all positions share same macro/theme risk:
  treat as correlated bucket.
```

### Rule 8 — Journal Before Trading

```text
Before session:
  review market expectation
  review focus list
  review current open risk
  review emotional state
  review whether larger sizing is earned.
```

---

## 13. Expected Failure Modes

### 13.1 Temporary Edge Decay

SPAC-like edges can disappear quickly.

Mitigation:

```text
Add edge half-life monitoring:
  if last N signals show expectancy decay, reduce score or disable module.
```

### 13.2 Overfitting Linearity

Linearity score can become hindsight-biased.

Mitigation:

```text
Use only pre-signal lookback.
Walk-forward validation only.
No future trend quality leakage.
```

### 13.3 Theme Label Subjectivity

Manual theme labels may create narrative bias.

Mitigation:

```text
Start with price/volume/sector proxies.
Only add NLP later with audit trail.
```

### 13.4 Correlation Shock

Different themes can collapse together in risk-off moves.

Mitigation:

```text
Use rolling correlation + market stress proxy.
If stress high, treat all high-beta momentum as one bucket.
```

### 13.5 High ADR Over-Sizing

High ADR stocks produce opportunity but also emotional and portfolio pressure.

Mitigation:

```text
risk_pct = base_risk_pct * volatility_adjustment
volatility_adjustment = min(1, target_adr / current_adr)
```

---

## 14. Suggested Files for Repo Implementation

```text
06_QUANTLENS_LAB/research/thematic_momentum_magic_elixir/
  README.md
  config/
    magic_elixir_v0.yml
    portfolio_risk_v0.yml
  src/
    universe_loader.py
    absolute_strength.py
    liquidity_filters.py
    adr_atr_filters.py
    stage_analysis.py
    linearity_score.py
    theme_bucket_risk.py
    candidate_scoring.py
    portfolio_risk_guard.py
    report_writer.py
  tests/
    test_liquidity_filters.py
    test_absolute_strength.py
    test_linearity_score.py
    test_portfolio_risk_guard.py
  reports/
    INTAKE_006_IMPLEMENTATION_PLAN.md
    daily_journal_template.md
    weekly_review_template.md
```

---

## 15. Candidate Registry Draft

```yaml
candidate_id: CAND_20260503_TED_ZHANG_MAGIC_ELIXIR_MOMENTUM_HAN1kymVbTc
name: Thematic Catalyst Momentum + Magic Elixir Stock Selection & Portfolio Risk Engine
source_video_id: HAN1kymVbTc
source_url: https://www.youtube.com/watch?v=HAN1kymVbTc
classification: CANDIDATE
codex_status: READY_FOR_PYTHON_PROTOTYPE
priority: P0/P1
market: US_EQUITIES
family:
  - thematic_momentum
  - catalyst_momentum
  - stage_analysis
  - absolute_strength
  - portfolio_risk
modules:
  - liquidity_filter
  - adr_atr_opportunity_filter
  - linearity_score
  - stage_analysis_gate
  - theme_catalyst_scorer
  - absolute_strength_rank
  - market_context_gate
  - portfolio_open_risk_guard
  - theme_bucket_guard
  - journal_routine_template
requires_python_prototype: true
requires_pine_now: false
uses_mtc_v2_components:
  - entry_gates
  - portfolio_state_guards
  - position_sizing
  - stop_loss
  - trailing_stop
  - reason_codes
```

---

## 16. Trader Wiki Note Draft

Bu transcript ayrıca `11_TRADER_WIKI` için değerlidir.

### Suggested Wiki Path

```text
11_TRADER_WIKI/04_SYSTEM_DEVELOPMENT/TW_2026-05-03_magic_elixir_ted_zhang_process.md
```

### Wiki Topics

- Habit systems and trading routines
- Risk management habits
- Journaling before pre-market
- Professional money management vs. personal trading
- Temporary edge decay
- Liquidity lesson from SPAC warrants
- Theme bucket construction
- “Do not rise to goals; fall to systems” style process thinking

### Usefulness Score

`9 / 10`

---

## 17. Decision: Candidate vs Wiki Only

### Why Not `WIKI_ONLY`

`WIKI_ONLY` olsaydı içerik sadece psikoloji, kariyer veya genel trading tavsiyelerinden oluşurdu. Bu transcriptte ise doğrudan kodlanabilir sistem parçaları var:

- liquidity threshold
- ADR/ATR opportunity threshold
- linearity score
- stage analysis gate
- theme/catalyst scorer
- absolute strength rank
- portfolio open-risk cap
- theme bucket exposure cap
- routine/journal templates

Bu nedenle ana sınıflandırma `CANDIDATE`, ikincil değer `Trader Wiki` olmalıdır.

---

## 18. Codex Next Action

### Immediate Next Action

```text
Create a Python-only research prototype folder for CAND_20260503_TED_ZHANG_MAGIC_ELIXIR_MOMENTUM_HAN1kymVbTc.
Do not modify 01_PINE/MTC_V2.pine.
Do not modify production Python runner files.
Do not run heavy backtests or optimization.
First implement deterministic feature calculations and candidate scoring on a small sample dataset.
```

### First Implementation Sprint

1. Implement liquidity filter.
2. Implement ADR/ATR filter.
3. Implement absolute strength rank.
4. Implement stage analysis gate.
5. Implement simple linearity score.
6. Implement candidate score output CSV.
7. Implement portfolio open-risk calculation on sample positions.
8. Produce report with top candidates and rejection reason codes.

### Do Not Do Yet

- Do not add Pine code.
- Do not automate broker execution.
- Do not add AI/news NLP as first version.
- Do not run overnight optimization.
- Do not overwrite existing registries before reading them.

---

## 19. Files Created / Not Touched

### Created by this intake step

```text
INTAKE_006_HAN1kymVbTc_ted_zhang_momentum_portfolio_manager.md
```

### Not touched

```text
01_PINE/MTC_V2.pine
Production Python runner files
Backtest outputs
Optimization outputs
Large CSV/data bundles/cache
Registry files inside repo
Secrets/API/webhook/broker/exchange keys
```

---

## 20. Final Summary

Bu video, QuantLens için yüksek değerli bir **selection + risk + process** candidate’dır. Önceki videolar daha çok entry/setup tarafını güçlendirirken, bu transcript şu eksik katmanı tamamlıyor:

```text
Hangi hisseyi seçmeliyim?
Hangi temada yoğunlaşmalıyım?
Pozisyonu ne kadar büyütmeliyim?
Portföy korelasyonunu nasıl kontrol etmeliyim?
Günlük karar kalitemi nasıl stabilize etmeliyim?
```

En promising kodlanabilir aday:

```text
Thematic Catalyst Momentum + Magic Elixir Stock Selection & Portfolio Risk Engine
```

Bu candidate, MTC_V2’nin entry/exit/position management kabiliyetlerine ileride bağlanabilir; fakat ilk aşamada kesinlikle Python research prototype olarak kalmalıdır.
