# QuantLens Transcript Intake Report — 005 / 068

## 1. Metadata

- **Report ID:** `INTAKE_005_jD4nynuWfEU`
- **Source URL:** `https://www.youtube.com/watch?v=jD4nynuWfEU`
- **Normalized URL:** `https://www.youtube.com/watch?v=jD4nynuWfEU`
- **Video ID:** `jD4nynuWfEU`
- **Title:** `The Reality of Relative Strength Based Trading with Linda Raschke`
- **Series / Theme:** TraderLion / Market Wizards style presentation — Linda Raschke; relative strength; Janus Factor; positive/negative feedback regimes; trend-day preconditions
- **Channel:** `TraderLion` / `WEB_RESOLVED`
  - Transcript dosyasının ilk satırlarında URL görünmüyor. URL ve kanal bilgisi exact-title web aramasıyla eşleştirildi. Repo içine yazmadan önce Codex bu bilgiyi YouTube URL'si veya dosya metadata'sı ile tekrar doğrulamalıdır.
- **Source transcript file:** `The Reality of Relative Strength Based Trading with Linda Raschke.md`
- **Prompt file used:** `00_quantlens_transcript_intake_prompt.md`
- **Generated date:** `2026-05-03`
- **Transcript hash method:** lowercase + whitespace-normalized SHA256 over full transcript text
- **Transcript hash:** `e72f0c149d8d66a2fcaaf6c9d5d1f435d79dae885e7ba75ceadf53aeaf83b76d`

---

## 2. Intake Verdict

- **Classification:** `CANDIDATE`
- **Codex Status Önerisi:** `READY_FOR_PYTHON_PROTOTYPE`
- **Candidate Priority:** `P1 — High-value regime / relative-strength research candidate`
- **Usefulness Score:** `9 / 10`
- **Coding Readiness Score:** `8 / 10`
- **MTC_V2 Fit Score:** `8 / 10`
- **Wiki Note Also Valuable:** `YES`

### Verdict Summary

Bu transcript `WIKI_ONLY` değildir. İçerik; doğrudan kodlanabilir **relative strength regime filter**, **leader-laggard spread**, **positive / negative feedback market environment detector**, **multi-lookback RS scanner**, **2-period ROC / 3-10 oscillator momentum model** ve **trend-day precondition filter** fikirleri içeriyor.

Ana fikir:

> Relative strength tek başına sabit bir buy/sell stratejisi değildir. Lookback periyodu ve market environment değişince aynı RS prensibi farklı davranır. Güçlü pozitif feedback ortamında liderler lider kalır; negatif feedback / range ortamında laggard rotation ve mean-reversion daha iyi çalışabilir. Bu nedenle sistem önce marketin momentum environment'ını ölçmeli; sonra momentum mu contrarian mı çalıştırılacağına karar vermelidir.

QuantLens açısından bu video, önceki `002`, `003` ve `004` raporlarını tamamlayan bir **regime layer** sağlar:

- `002`: Entry tactic library
- `003`: HV / RS setup framework
- `004`: Correction leader + VCP + progressive exposure
- `005`: RS market environment / Janus regime filter + trend-day precondition model

Bu candidate doğrudan Pine'a geçirilmemeli. Önce Python tarafında feature detector ve regime classification olarak izole edilmelidir.

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
  - Bu video id: `jD4nynuWfEU`
- **Action:** Gerçek repo'ya yazılmadan önce Codex registry dosyalarını okuyup `video_id` ve `transcript_hash` ile duplicate kontrolünü tekrar yapmalıdır.

### Registry Row Draft

```csv
video_id,normalized_url,title,channel,status,candidate_id,transcript_hash,first_seen_at,last_seen_at,process_count
jD4nynuWfEU,https://www.youtube.com/watch?v=jD4nynuWfEU,"The Reality of Relative Strength Based Trading with Linda Raschke",TraderLion,CANDIDATE,CAND_20260503_RASCHKE_RS_JANUS_REGIME_jD4nynuWfEU,e72f0c149d8d66a2fcaaf6c9d5d1f435d79dae885e7ba75ceadf53aeaf83b76d,2026-05-03,2026-05-03,1
```

---

## 4. Channel Quality Check

- **Channel:** `TraderLion` / `WEB_RESOLVED`
- **Blacklist decision:** `NO_BLACKLIST_DECISION_FROM_SINGLE_VIDEO`
- **Reason:** Tek başına bu video çok güçlü candidate. Ancak blacklist/watchlist/good kararı repo'daki kanal geçmişi okunmadan kesinleştirilmemeli.
- **Suggested quality update after repo check:** `candidate_count += 1`
- **Batch pattern note:** İlk beş videodan 002, 003, 004 ve 005 aynı eğitim ekosistemi / TraderLion çevresinden geliyorsa kanal büyük olasılıkla `GOOD` adayıdır. Fakat kanal id doğrulanmadan otomatik `GOOD` yazılmamalıdır.

---

## 5. Strategy Candidate

### Candidate ID

`CAND_20260503_RASCHKE_RS_JANUS_REGIME_jD4nynuWfEU`

### Candidate Name

**Raschke Janus Relative Strength Regime Engine**

### Strategy Family

- Relative strength / relative momentum
- Market regime classification
- Positive feedback / trend-following environment
- Negative feedback / mean-reversion environment
- Leader-laggard spread analysis
- Multi-lookback ranking
- Trend-day precondition detection
- Momentum oscillator / rate-of-change model
- Process and risk discipline

### Primary Market

- **Best native fit:** US equities + liquid futures
- **Reason:** Transcript hem stock relative strength scan'leri hem de futures momentum / trend-day uygulamalarını anlatıyor.
- **MTC_V2 fit:** MTC_V2'nin entry gate, market-regime filter, portfolio exposure guard ve position sizing katmanlarına çok iyi oturur.
- **Crypto adaptation:** Mümkün. Benchmark olarak BTC, TOTAL, TOTAL2, sector/index basketleri veya custom crypto universe kullanılabilir. Fakat leader/laggard universe kalitesi kritik olur.

---

## 6. Core Thesis Extracted

### 6.1 Relative Strength Is Environment-Dependent

Relative strength, “her zaman lideri al” şeklinde tek boyutlu bir kural değildir. Lookback ve market environment değiştiğinde farklı sonuçlar verir.

Kodlanabilir çıkarım:

```text
rs_signal_validity = f(lookback_period, market_environment, leader_laggard_spread_state)
```

### 6.2 Positive Feedback = Momentum / Trend Environment

Pozitif feedback ortamında lider-laggard spread'i açılır. Liderler daha fazla outperform eder; laggard'lar zayıf kalır. Bu ortam trend-following ve momentum continuation için daha uygundur.

```text
if leader_laggard_spread_slope > positive_threshold:
    regime = POSITIVE_FEEDBACK
    preferred_mode = MOMENTUM_LEADERS
```

### 6.3 Negative Feedback = Rotation / Mean-Reversion Environment

Leader-laggard spread daralıyorsa piyasa daha çok rotation / range / mean-reversion karakteri gösterir. Bu ortamda en güçlü lideri almak yerine, kaliteli ama aşırı satılmış laggard'ların alt banttan dönüşleri daha iyi performans verebilir.

```text
if leader_laggard_spread_slope < negative_threshold:
    regime = NEGATIVE_FEEDBACK
    preferred_mode = MEAN_REVERSION_OR_RANGE
```

### 6.4 Lookback Matters

Transcriptte birkaç farklı RS penceresi ayrıştırılıyor:

```text
1-day RS: short-term snap / hot potato / immediate rotation
cycle-low RS: recent cycle low sonrası güçlenen adayları izleme
start-of-quarter RS: institutional allocation flow proxy
~6-month RS / 120-day RS: longer-term portfolio leadership
```

Bu çok değerli bir tasarım kuralıdır. Tek bir RS lookback'i yerine multi-horizon RS features oluşturulmalıdır.

### 6.5 Trend-Day Trading Requires Preconditions

Trend-day veya range expansion için ön koşullar önemlidir. Raschke'nin yaklaşımında price, momentum ve oscillator ilişkileri birlikte okunur.

Basitleştirilmiş çıkarım:

```text
trend_day_candidate = price_structure_ready
                      AND roc_2_slope_positive
                      AND oscillator_slowline_slope_positive
                      AND breadth_or_group_urgency_visible
```

### 6.6 Do Not Average Down

Transcriptte açık risk disiplini var: losing trade üzerine ortalama düşürme yasak. Ayrıca çok küçük trade sloppy davranışa; çok büyük trade ise unforced error'a neden olabilir.

MTC_V2 için çıkarım:

```text
averaging_down_guard = forbidden
position_size_range = not_too_small_not_too_large
```

---

## 7. Extracted System Modules

## 7.1 Multi-Lookback Relative Strength Scanner

### Concept

RS skorları farklı lookbacklerde farklı adaylar çıkarır. Aynı universe için birden fazla RS penceresi hesaplanmalı.

### Candidate Features

```text
rs_1d      = symbol_return_1d - benchmark_return_1d
rs_5d      = symbol_return_5d - benchmark_return_5d
rs_21d     = symbol_return_21d - benchmark_return_21d
rs_63d     = symbol_return_63d - benchmark_return_63d
rs_120d    = symbol_return_120d - benchmark_return_120d
rs_cycle   = symbol_return_since_cycle_low - benchmark_return_since_cycle_low
rs_quarter = symbol_return_since_quarter_start - benchmark_return_since_quarter_start
```

### Output

```json
{
  "symbol": "EXAMPLE",
  "rs_1d_rank": 0,
  "rs_21d_rank": 0,
  "rs_120d_rank": 0,
  "rs_cycle_rank": 0,
  "rs_quarter_rank": 0,
  "rs_profile": "SHORT_TERM_ROTATION | LONG_TERM_LEADER | CYCLE_LEADER | MIXED"
}
```

### MTC_V2 Mapping

- `Entry Gate`: `relative_strength_profile_gate`
- `Setup score`: bonus for multi-horizon alignment
- `Market regime`: different lookback used depending on regime

---

## 7.2 Janus Leader-Laggard Spread Engine

### Concept

Universe içindeki en güçlü ve en zayıf hisselerin forward performans farkı market environment hakkında bilgi verir.

Transcriptteki ana mantık:

```text
1. Universe içindeki strongest ve weakest grupları belirle.
2. Her grubun forward değişimini ortalama al.
3. Leaders - laggards spread'ini takip et.
4. Spread açılıyorsa momentum / positive feedback.
5. Spread daralıyorsa rotation / negative feedback.
```

### Candidate Logic

```python
returns_lb = close / close.shift(lookback) - 1
rs_score = returns_lb - benchmark_returns_lb

leaders = top_decile(rs_score)
laggards = bottom_decile(rs_score)

leader_forward = mean(forward_return(leaders, horizon=1))
laggard_forward = mean(forward_return(laggards, horizon=1))
spread_return = leader_forward - laggard_forward
janus_line = cumulative_sum(spread_return)
janus_slope = slope(janus_line, window)
```

### Regime Interpretation

```text
janus_slope > +threshold:
  POSITIVE_FEEDBACK
  Momentum leadership favored.

janus_slope < -threshold:
  NEGATIVE_FEEDBACK
  Mean reversion / laggard recovery favored.

abs(janus_slope) <= threshold:
  TRANSITION / MIXED
  Smaller size; wait for confirmation.
```

### Research Variants

```text
Variant A: Leaders top 10%, laggards bottom 10%, lookback=120d
Variant B: Leaders top 10%, laggards bottom 10%, leaders lookback=3w, laggards lookback=5m
Variant C: Leaders/laggards by RS_21d during cycle-low recovery
Variant D: Crypto universe adaptation using BTC or TOTAL benchmark
```

---

## 7.3 Positive Feedback Momentum Mode

### Concept

Pozitif feedback modunda trend continuation ve range expansion olasılığı artar. MTC_V2 tarafında bu mod, trend-following producer ve breakout entry'lere izin veren bir regime filter olabilir.

### Conditions

```text
positive_feedback_mode = janus_slope > positive_threshold
                         AND leader_forward_avg > laggard_forward_avg
                         AND breadth_or_index_trend_not_hostile
```

### Allowed Strategy Modes

```text
- VCP breakout continuation
- RS leader pullback to support
- High volume edge continuation
- Opening range / trend-day continuation
- Trail longer; avoid premature mean-reversion exits
```

### Blocked or Reduced Modes

```text
- low-quality bottom fishing
- averaging down
- random laggard catch-up trades
```

---

## 7.4 Negative Feedback / Rotation Mode

### Concept

Negatif feedback modunda lider-laggard spread daralır. Trend-following sinyaller daha fazla whipsaw üretebilir. Bu ortamda mean-reversion, lower-range buying ve range exit mantığı daha uygun olabilir.

### Conditions

```text
negative_feedback_mode = janus_slope < negative_threshold
                         OR leader_laggard_spread_converging == true
```

### Candidate Modes

```text
- oversold but quality laggard bounce
- range lower-bound reversal
- buy bottom of range / sell upper range
- faster profit-taking
- smaller position size
```

### Important Risk Note

Bu, “çöp hisse al” demek değildir. Transcript özellikle batmış pandemic winners gibi kalitesiz/destroyed isimlere körlemesine girmemeyi ima ediyor. QuantLens'te quality filter gerekir.

```text
quality_laggard = large_cap_or_liquid
                  AND not_structurally_broken
                  AND drawdown_extreme_but_stabilizing
                  AND market_in_negative_feedback
```

---

## 7.5 2-Period ROC Momentum Tool

### Concept

Raschke, 2-period rate of change'i ana trading tool olarak anlatıyor. 1-day ROC'a göre biraz daha az noisy olduğunu söylüyor.

### Formula

```text
roc_2 = close - close.shift(2)
roc_2_pct = close / close.shift(2) - 1
roc_2_slope = roc_2 - roc_2.shift(1)
```

### Signal Ideas

```text
roc_2_slope_positive = roc_2 > roc_2.shift(1)
roc_2_new_high_30 = roc_2 >= rolling_max(roc_2, 30)
roc_2_new_low_30 = roc_2 <= rolling_min(roc_2, 30)
```

### MTC_V2 Mapping

- `Momentum Gate`: confirm momentum impulse
- `Trend-Day Precondition`: require positive slope for long trend day setups
- `Exit Diagnostic`: momentum loss / short-term stall

---

## 7.6 3/10 Oscillator + Slowline Model

### Concept

3/10 oscillator, 3-period SMA ile 10-period SMA farkıdır. 16-period smoothing line momentum trendini temsil eder.

### Formula

```text
osc_3_10 = sma(close, 3) - sma(close, 10)
osc_3_10_slow = sma(osc_3_10, 16)
```

### Signal Ideas

```text
osc_fast_slope = osc_3_10 - osc_3_10.shift(1)
osc_slow_slope = osc_3_10_slow - osc_3_10_slow.shift(1)

pf_long = close > ema(close, 20)
          AND roc_2_slope > 0
          AND osc_slow_slope > 0
          AND osc_fast_slope > 0
```

### Alternative

Transcriptte stochastic alternatifi de ima ediliyor:

```text
stoch_k = stochastic(7)
stoch_d = sma(stoch_k, 3 or 4)
stoch_slow = sma(stoch_d, 12 to 16)
```

İlk prototype'ta 3/10 oscillator tercih edilmeli; daha sonra stochastic varyantı diagnostic olarak eklenebilir.

---

## 7.7 Multi-ROC Slope Flip Detector

### Concept

3, 4, 5, 6 period ROC slope'ları aynı yöne döndüğünde kısa vadeli swing impulse oluşabilir.

### Candidate Logic

```text
roc_n = close / close.shift(n) - 1
roc_n_slope = roc_n - roc_n.shift(1)

multi_roc_up = all(roc_n_slope > 0 for n in [3,4,5,6])
multi_roc_down = all(roc_n_slope < 0 for n in [3,4,5,6])
```

### Trend Filter

```text
long_signal = multi_roc_up AND close > ema(close, 20)
short_signal = multi_roc_down AND close < ema(close, 20)
```

### Risk

Transcriptte choppy / range ortamında çok sayıda false signal uyarısı var. Bu yüzden bu detector tek başına producer olmamalı; regime filter ile kullanılmalı.

---

## 7.8 Momentum High Scan

### Concept

30-day momentum high scan, fiyat kırılmadan momentumun önce canlandığı adayları yakalayabilir.

### Candidate Logic

```text
momentum = roc_2_pct OR close / close.shift(n) - 1
new_momentum_high_30 = momentum >= rolling_max(momentum, 30)
```

### Use Case

```text
if new_momentum_high_30 AND price_structure_constructive:
    add_to_watchlist
```

Bu doğrudan al sinyali değil; watchlist/radar sinyalidir.

---

## 7.9 Trend Balance / 3-Bar Overlap Detector

### Concept

Trend bittiğinde piyasa balance/equilibrium noktasına iner. Transcriptte üç bar overlap, trendin balance'a geldiğini gösteren basit bir yapı olarak anlatılıyor.

### Candidate Logic Draft

```text
bar_overlap_3 = max(low[-3:]) <= min(high[-3:])
range_contracting = atr_pct < rolling_median(atr_pct, 20)
trend_balance = bar_overlap_3 AND range_contracting
```

### Use Case

```text
if trend_balance:
    do_not_predict_direction
    wait_for_break_above_first_hour_range_or_below_first_hour_range
```

Pine tarafında intraday first-hour logic ağır olabilir. İlk Python prototype günlük OHLCV + optional intraday fixture ile test edilmeli.

---

## 7.10 Risk / Position Discipline Guard

### Concept

Transcriptte üç açık risk dersi var:

```text
1. Never average down.
2. Do not trade too small; sloppy behavior risk.
3. Do not trade too big; unforced error risk.
```

### MTC_V2 Mapping

```text
averaging_down_guard = block_add_if_position_unrealized_R < 0
min_meaningful_size_guard = optional diagnostic only
max_heat_guard = cap position/account risk to avoid forced emotional errors
```

Recommended first implementation:

```python
def can_add_to_position(position, proposed_add, current_state):
    if position.unrealized_R < 0:
        return False, "BLOCK_AVERAGING_DOWN"
    if current_state.portfolio_heat + proposed_add.risk_pct > max_heat:
        return False, "BLOCK_HEAT_TOO_HIGH"
    return True, "ALLOW_ADD"
```

---

## 8. Candidate Architecture

```text
UNIVERSE + BENCHMARK DATA
  ├─ Multi-Lookback RS Scanner
  │   ├─ RS_1D
  │   ├─ RS_cycle_low
  │   ├─ RS_quarter_start
  │   ├─ RS_120D / 6M
  │   └─ RS profile classification
  │
  ├─ Janus Regime Engine
  │   ├─ top 10% leaders
  │   ├─ bottom 10% laggards
  │   ├─ forward return spread
  │   ├─ cumulative Janus line
  │   └─ positive/negative feedback state
  │
  ├─ Momentum Feedback Detector
  │   ├─ ROC_2 slope
  │   ├─ 3/10 oscillator slope
  │   ├─ 20 EMA context
  │   ├─ multi-ROC slope flip
  │   └─ new momentum high scan
  │
  ├─ Strategy Selector
  │   ├─ POSITIVE_FEEDBACK -> momentum / RS leaders
  │   ├─ NEGATIVE_FEEDBACK -> range / selective contrarian
  │   └─ MIXED -> reduce risk / wait
  │
  └─ Risk Guard
      ├─ no averaging down
      ├─ max heat cap
      ├─ mode-specific sizing
      └─ fast exit if no follow-through
```

---

## 9. MTC_V2 Mapping

| Concept | MTC_V2 Layer | Recommended Treatment |
|---|---|---|
| Janus leader-laggard spread | Global Regime / External scanner | Compute in Python first; Pine later only as imported regime flag if needed |
| Multi-lookback RS | Entry Gate / Universe prefilter | Use as precomputed features for selected symbols |
| Positive feedback mode | Entry Gate + Position Sizing | Allow momentum signals; allow wider trend-following behavior |
| Negative feedback mode | Entry Guard | Reduce breakout entries; optionally enable range / mean-reversion research branch |
| ROC_2 | Momentum Gate | Lightweight and Pine-compatible |
| 3/10 oscillator | Momentum Gate | Pine-compatible; validate parity first |
| Multi-ROC slope flip | Signal diagnostic / entry filter | Must be regime-filtered to avoid chop false positives |
| Momentum high scan | Watchlist builder | Not direct entry signal in phase 1 |
| No averaging down | Position Manager / Guard | Block add when unrealized R < 0 |
| Too-large position warning | Position Sizing | Max heat / max position caps |

### Important Pine Warning

Janus spread engine requires a universe of symbols and top/bottom decile calculations. This is not Pine-friendly at first. MTC_V2 Pine should not be modified until Python research proves which simplified features matter.

---

## 10. Prototype Plan

### Phase 0 — Isolated Folder Only

Rules:

- `01_PINE/MTC_V2.pine` değiştirilmez.
- Production Python runner değiştirilmez.
- Backtest / optimization çalıştırılmaz.
- Büyük CSV / data bundle oluşturulmaz.

Suggested folder:

```text
06_QUANTLENS_LAB/research/raschke_rs_janus_005/
  README.md
  intake_notes.md
  feature_schema.md
  rs_multi_lookback.py
  janus_spread.py
  feedback_regime.py
  roc_momentum.py
  oscillator_310.py
  trend_balance.py
  risk_guards.py
  tests/
    test_rs_multi_lookback.py
    test_janus_spread.py
    test_feedback_regime.py
    test_roc_momentum.py
    test_oscillator_310.py
    test_risk_guards.py
```

### Phase 1 — Feature Detectors Only

Implement pure functions:

```python
def calc_relative_strength(symbol_close, benchmark_close, lookback): ...
def rank_universe_rs(close_matrix, benchmark_close, lookback): ...
def calc_janus_spread(close_matrix, benchmark_close, leader_lb, laggard_lb, q=0.10): ...
def classify_feedback_regime(janus_line, slope_window, threshold): ...
def calc_roc(close, n): ...
def detect_roc2_momentum_high(close, lookback=30): ...
def calc_oscillator_310(close, slow=16): ...
def detect_multi_roc_slope_flip(close, periods=(3,4,5,6)): ...
def detect_three_bar_overlap(high, low): ...
def block_averaging_down(position_state): ...
```

### Phase 2 — Manual Fixture Tests

Use synthetic fixtures first:

```text
1. leader basket outperforming laggards -> POSITIVE_FEEDBACK
2. laggards catching up -> NEGATIVE_FEEDBACK
3. flat/choppy spread -> MIXED
4. ROC_2 new momentum high after consolidation
5. 3/10 oscillator + ROC_2 aligned long
6. multi-ROC flips in trend vs false flips in range
7. add-to-loser blocked by risk guard
```

### Phase 3 — Event Label Schema

```json
{
  "event_type": "RASCHKE_RS_JANUS_REGIME",
  "video_id": "jD4nynuWfEU",
  "candidate_id": "CAND_20260503_RASCHKE_RS_JANUS_REGIME_jD4nynuWfEU",
  "symbol": "EXAMPLE",
  "benchmark": "SPY",
  "timeframe": "1D",
  "rs_1d_rank": null,
  "rs_21d_rank": null,
  "rs_120d_rank": null,
  "rs_cycle_rank": null,
  "rs_quarter_rank": null,
  "janus_regime": "POSITIVE_FEEDBACK | NEGATIVE_FEEDBACK | MIXED",
  "leader_laggard_spread": 0.0,
  "janus_slope": 0.0,
  "roc_2": 0.0,
  "roc_2_new_high_30": false,
  "osc_310": 0.0,
  "osc_310_slow_slope": 0.0,
  "multi_roc_flip": "UP | DOWN | NONE",
  "trend_balance": false,
  "preferred_strategy_mode": "MOMENTUM | RANGE_REVERSION | WAIT",
  "reason_codes": []
}
```

### Phase 4 — Validation Metrics

```text
Regime metrics:
  - Janus regime vs realized leader outperformance
  - false positive momentum mode rate
  - breakout success by regime
  - mean-reversion success by regime

Signal metrics:
  - ROC_2 new high -> next 1/2/3 day MFE
  - 3/10 oscillator alignment -> next day trend probability
  - multi-ROC flip false-signal density in range regimes

Risk metrics:
  - averaging-down block effect on drawdown
  - max heat cap effect on max drawdown
  - mode-specific sizing vs fixed sizing
```

---

## 11. Potential Ruleset Draft

### Momentum Mode Long Candidate

```text
janus_regime == POSITIVE_FEEDBACK
AND rs_120d_rank >= top_quantile
AND close > ema(close, 20)
AND roc_2_slope > 0
AND osc_310_slow_slope > 0
AND entry_setup_from_other_module == true
```

This should not be standalone; it should enable or score existing setup modules from 002/003/004.

### Negative Feedback Mean-Reversion Candidate

```text
janus_regime == NEGATIVE_FEEDBACK
AND rs_1d_rank improving
AND quality_filter_pass == true
AND price_near_lower_range == true
AND no_structural_breakdown == true
```

This is research-only. It should not be mixed directly into MTC_V2 production until separately validated.

### Wait / Reduce Mode

```text
janus_regime == MIXED
OR multi_roc_signal_conflicts_with_price_structure
OR range_noise_high == true
```

Action:

```text
reduce_position_size
block new aggressive entries
only allow A+ setups from other modules
```

---

## 12. Risks / Suspicious or Non-Systematic Claims

### 12.1 Universe Sensitivity

Leader-laggard spread depends heavily on chosen universe. A random 200-stock list can distort the regime.

Mitigation:

```text
Use stable liquid universe; document universe selection; test sensitivity.
```

### 12.2 Look-Ahead Bias Risk

Janus calculation uses leaders/laggards identified at day D and forward returns at D+1. Implementation must avoid selecting with future data.

Mitigation:

```text
rank at close[D]; apply to returns[D+1]; log timestamp explicitly.
```

### 12.3 Regime Overfitting

Thresholds for Janus slope and ROC alignment can be overfit. Use broad buckets first, not optimized magic numbers.

### 12.4 Mixing Momentum and Mean-Reversion

This candidate can easily become two conflicting strategies. MTC_V2 must select exactly one active mode per bar or impose strict priority.

Suggested priority:

```text
if regime == POSITIVE_FEEDBACK: momentum only
elif regime == NEGATIVE_FEEDBACK: range/contrarian research branch only
else: wait/reduce
```

### 12.5 Short-Term Options / Hot Potato Caution

Transcript mentions very short-duration options/gap strategies but does not provide enough deterministic exit logic. Do not implement options logic in first prototype.

### 12.6 Futures vs Stocks Noise Difference

Raschke says principles apply across futures/stocks but stocks are noisier. For QuantLens, validate separately by asset class.

### 12.7 Daily vs Intraday Ambiguity

Trend-day preconditions sometimes rely on intraday behavior. First prototype should remain daily-feature-only; intraday expansion can be later.

---

## 13. Trader Wiki Note Also Recommended

Bu video Trader Wiki'ye ayrıca alınmalı. Çünkü stratejiden bağımsız olarak relative strength, market environment, cognitive bias, homework discipline ve process design açısından yüksek değerli dersler içeriyor.

### Suggested Wiki Entry

- **Wiki status:** `ALSO_CREATE_WIKI_NOTE`
- **Topic:** `03_MARKET_STRUCTURE` + `04_SYSTEM_DEVELOPMENT` + `05_BACKTESTING_AND_OPTIMIZATION` + `01_RISK_MANAGEMENT`
- **Suggested file name:** `TW_2026-05-03_03_MARKET_STRUCTURE_raschke_relative_strength_janus_factor.md`

### Wiki Themes

- Relative strength lookback'e bağlıdır.
- Liderlerin outperform ettiği ortam momentum; laggard'ların yetiştiği ortam rotation / mean reversion olabilir.
- Market “tek karakterli” değildir; Janus gibi iki yüzü vardır.
- Kendi çalışmanı yap; başkasının sheet'i ile aynı conviction oluşmaz.
- Failed signals incelenmeden gerçek edge anlaşılmaz.
- Averaging down büyük risk hatasıdır.
- Strateji geliştirmede walk-forward gözlem şarttır.

---

## 14. Codex Next Action

### Immediate Task

```text
Create isolated research folder for INTAKE_005 Raschke Janus relative-strength regime candidate.
Do not modify MTC_V2 Pine.
Do not modify production Python runner.
Do not run backtests or optimization.
Implement pure detector stubs and unit-test fixtures only for:
1. Multi-lookback relative strength scanner
2. Janus leader-laggard spread
3. Positive/negative feedback regime classifier
4. ROC_2 momentum high detector
5. 3/10 oscillator model
6. Multi-ROC slope flip detector
7. 3-bar overlap / trend balance detector
8. No-averaging-down risk guard
```

### Suggested Codex Prompt

```text
Read INTAKE_005_jD4nynuWfEU_raschke_relative_strength_janus_factor.md.
Before making changes, inspect repo registry files for duplicate video_id=jD4nynuWfEU and transcript_hash=e72f0c149d8d66a2fcaaf6c9d5d1f435d79dae885e7ba75ceadf53aeaf83b76d.
If duplicate exists, stop and report duplicate details.
If not duplicate, create an isolated research folder under 06_QUANTLENS_LAB/research/raschke_rs_janus_005/.
Do not modify 01_PINE/MTC_V2.pine.
Do not modify production Python runner files.
Do not run backtests or optimization.
Implement feature-detector stubs and synthetic unit-test fixtures only for multi-lookback RS, Janus leader-laggard spread, feedback regime classification, ROC_2, 3/10 oscillator, multi-ROC slope flip, trend balance, and no-averaging-down risk guard.
Prepare README.md with formulas, assumptions, event schema, limitations, and next steps.
Also draft a Trader Wiki note for relative strength environment, Janus Factor, market regime selection, and risk discipline.
```

---

## 15. Files Created / Not Touched

### Created by this intake step

```text
INTAKE_005_jD4nynuWfEU_raschke_relative_strength_janus_factor.md
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
Candidate Type: Relative strength regime engine + Janus leader-laggard spread + momentum feedback filters
Primary Implementation Target: Python research prototype
Pine Implementation: Later, only after detector validation and simplification
Registry Update Needed: Yes, after repo duplicate check
Trader Wiki Note: Yes, also recommended
```

Bu transcript, QuantLens için doğrudan bir “entry signal” videosu olmaktan çok daha değerli bir şey sağlar: **hangi market environment'ta hangi strateji ailesinin çalıştırılacağını seçen üst seviye regime engine**. MTC_V2 için en doğru kullanım; VCP/HV/RS entry'leri doğrudan değiştirmek değil, onların önüne **Janus / feedback regime gate** koymaktır.
