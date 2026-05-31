# QuantLens Transcript Intake Report — Lance Breitstein / Trend Trading, Right-Side-of-V & Catalyst Momentum

## 1. Metadata

- **Source URL:** https://youtu.be/R215f4fj7V8?si=L3wGYRC2vMT5Bjb_
- **Normalized URL:** https://www.youtube.com/watch?v=R215f4fj7V8
- **Video ID:** `R215f4fj7V8`
- **Title:** `The Simple Trading Setup That Made Lance Breitstein Millions`
- **Channel:** `UNKNOWN_CHANNEL`
- **Transcript file:** `The Simple Trading Setup That Made Lance Breitstein Millions.md`
- **Transcript SHA256:** `decebe552a5cbbf14ef9363c38b8e765d3122039eb86112d891a996e4e393f62`
- **Approx. word count:** `20,289`
- **Intake date:** 2026-05-03
- **Duplicate status:** `NOT_DUPLICATE_IN_CURRENT_SESSION`
- **Repo registry duplicate check:** `NOT_VERIFIED_REPO_NOT_AVAILABLE`
- **Channel blacklist check:** `NOT_VERIFIED_REPO_NOT_AVAILABLE`
- **Final classification:** `CANDIDATE`
- **Codex status suggestion:** `READY_FOR_PYTHON_PROTOTYPE`
- **Candidate ID suggestion:** `QL_CAND_2026-05-03_R215f4fj7V8_BREITSTEIN_TREND`

---

## 2. Executive Summary

Bu transcript Lance Breitstein'in ana trading prensibini çok net veriyor: **trendle birlikte işlem yapmak**, trendle savaşan işlemleri azaltmak, hatta mean-reversion/counter-trend işlemleri bile “trend başladıktan sonra” almak.

Video özellikle şu açılardan güçlü:

1. **Trend tanımı ve trend alignment:** slope, higher-high/higher-low, VWAP üstü/altı tutunma, moving average, trendline, reference price, prior-bar high/low ve multi-timeframe alignment.
2. **Right-side-of-V mean reversion:** panik/capitulation sonrası düşen trend kırılmadan long denememek; dönüş başladıktan sonra prior-bar high kırılımıyla işleme girmek.
3. **Catalyst momentum:** haber/earnings gibi katalizör sonrası unaffected/reference price üstünde/altında trend oluşursa trend yönünde işlem almak.
4. **No-man's-land filtresi:** range-bound / consolidation / volatility compression alanlarında gereksiz trade almamak.
5. **Risk tiering:** A/B/C setup kalitesine göre önceden belirlenmiş risk miktarı kullanmak.

Bu video doğrudan MTC_V2 Pine tarafına taşınmamalı. Önce **Python research prototype** olarak, özellikle 2m/5m intraday OHLCV üzerinde test edilmeli. Bunun nedeni, stratejinin önemli kısmının intraday VWAP, news catalyst, capitulation ve hızlı dönüş davranışlarına dayanmasıdır.

---

## 3. Decision

### Final Verdict: `CANDIDATE`

Bu transcript `CANDIDATE` olarak işlenmeli çünkü:

- Net kodlanabilir trend tanımları var.
- Net kodlanabilir no-trade guard var.
- Net kodlanabilir VWAP yön filtresi var.
- Net kodlanabilir right-side-of-V reversal trigger var.
- Net kodlanabilir trailing stop önerileri var.
- Setup kalitesine göre risk tiering mantığı var.

### Neden `SALVAGE` değil?

Sadece psikoloji veya risk dersi değil; doğrudan trade setup çıkarılabilecek kadar mekanik öğe içeriyor:

- `prior_bar_high` break ile right-side-of-V entry
- `prior_bar_low` trailing stop
- VWAP üstü/altı yön yasağı
- range-bound trade rejection
- catalyst reference price holding
- MTF trend alignment ile size/risk artırma

### Neden doğrudan Pine'a geçilmemeli?

- Ana setup intraday ve real-time davranışa dayanıyor.
- Katalizör kalitesi için news/earnings feed gerekir.
- “Capitulation”, “in play”, “euphoric”, “clean trend” gibi kavramların önce deterministik proxy'leri yazılmalı.
- 2m bar, VWAP, premarket gap, halted stock, intraday liquidity gibi konular Pine parity riskini artırır.
- Önce Python'da OHLCV-only ve sonra news-aware varyant test edilmeli.

---

## 4. Extracted Strategy Components

## 4.1 Trend Alignment Engine — `BREITSTEIN_TREND_ALIGNMENT_V1`

### Amaç

Bir enstrümanın gerçekten trendde mi, range-bound mı olduğunu ayırmak ve sadece trendle uyumlu işlemlere izin vermek.

### Kaynak Fikirler

- Trend, yukarı veya aşağı eğimli fiyat hareketidir.
- Higher highs / higher lows güçlü uptrend göstergesidir.
- VWAP üzerinde tutunan hisseye short açmamak; VWAP altında tutunan hisseye long açmamak.
- Moving average üzerinde tutunma trend proxy'si olabilir.
- Trendline kırılımı trend dönüş sinyali olabilir.
- Prior-bar high/low yapısı çok kısa vadeli trend takibi için kullanılabilir.
- Multi-timeframe alignment olduğunda edge ve position size artabilir.

### Kodlanabilir Trend Proxy'leri

**Daily/Intraday slope:**

```text
trend_slope = linreg_slope(close, lookback)
uptrend = trend_slope > slope_threshold
downtrend = trend_slope < -slope_threshold
range_bound = abs(trend_slope) <= slope_threshold
```

**Structure trend:**

```text
uptrend_structure = higher_highs_count >= min_hh and higher_lows_count >= min_hl
downtrend_structure = lower_highs_count >= min_lh and lower_lows_count >= min_ll
```

**VWAP trend:**

```text
vwap_uptrend = close > session_vwap for N of last M bars
vwap_downtrend = close < session_vwap for N of last M bars
```

**Prior-bar trend:**

```text
strong_intraday_uptrend = low >= low[1] for N consecutive bars
strong_intraday_downtrend = high <= high[1] for N consecutive bars
```

### Output

```text
trend_state:
  UP_TREND
  DOWN_TREND
  RANGE_BOUND
  CAPITULATION_DOWN
  CAPITULATION_UP
  RIGHT_SIDE_REVERSAL_UP
  RIGHT_SIDE_REVERSAL_DOWN
```

### MTC_V2 Mapping

- `ENTRY GATES`: trend alignment gate
- `SIGNAL PRODUCER`: trend continuation / reversal trigger
- `EXIT RULES`: prior-bar trailing stop
- `Position Sizing`: MTF alignment risk multiplier

---

## 4.2 VWAP Direction Guard — `BREITSTEIN_VWAP_GUARD_V1`

### Amaç

Trendle savaşan intraday işlemleri engellemek.

### Long Rules

```text
reject_long_if:
    price_steadily_below_vwap
    and not downside_capitulation_detected
```

### Short Rules

```text
reject_short_if:
    price_steadily_above_vwap
    and not upside_capitulation_detected
```

### `steadily_below_vwap` Proxy

```text
below_vwap_ratio = count(close < vwap, last M bars) / M
price_steadily_below_vwap = below_vwap_ratio >= 0.75 and vwap_slope <= 0
```

### `capitulation_detected` Proxy

```text
capitulation_down =
    close < lower_band
    and volume > volume_ma * 2
    and range > atr * 1.5
    and distance_from_vwap_pct > threshold
```

### Yorum

Bu modül tek başına trade üretmez. Entry gate / no-trade guard olarak kullanılmalıdır.

---

## 4.3 Right-Side-of-V Reversal — `BREITSTEIN_RIGHT_SIDE_V_V1`

### Amaç

Panik satıştan sonra dip tahmini yapmadan, dönüş teyidi geldikten sonra counter-trend long almak.

### Core Thesis

Trend çok sert aşağı inerken sol tarafta long denenirse heat ve drawdown büyür. Edge, trend kırılıp sağ taraf oluşmaya başladıktan sonra ortaya çıkar.

### Setup Context

```text
prior_down_capitulation =
    intraday_downtrend_clean
    and price_extension_down >= min_extension
    and volume_spike >= 2x prior_bar_or_volume_ma
    and broad_market_or_symbol_panic
```

### Entry Trigger

```text
right_side_v_long_trigger =
    prior_down_capitulation
    and high > high[1]
    and close > high[1] optional
```

Alternatif daha konservatif tetik:

```text
trigger = close > max(high[1], high[2])
```

### Stop

```text
initial_stop = recent_pivot_low
or low_of_trigger_bar
or prior_bar_low_trailing
```

### Trailing Stop

```text
while in_long:
    stop = max(stop, low[1])
```

### Exit

- Prior 2m/5m bar low kırılırsa çık.
- Euphoric upside capitulation olursa partial veya full exit.
- VWAP rejection varsa çık.
- Trendline break aşağıysa çık.

### MTC_V2 Mapping

- `SIGNAL PRODUCER`: reversal producer
- `EXIT RULES`: bar-low trailing stop
- `ENTRY GATES`: capitulation + market context

### Test Timeframes

- Primary: 2m / 5m
- Secondary: 15m
- Daily-only proxy önerilmez; setup intraday karakterlidir.

---

## 4.4 Catalyst Reference Price Trend — `BREITSTEIN_CATALYST_REF_PRICE_V1`

### Amaç

Haber/earnings gibi katalizör sonrası piyasanın haber fiyatlamasını trend filtresi olarak kullanmak.

### Reference Price

```text
reference_price = last_price_before_news
```

Örnekler:

- Earnings after-hours ise önceki kapanış.
- Intraday breaking news ise haberden hemen önceki fiyat.
- Premarket news ise önceki regular-session close veya premarket base level.

### Bullish News Behavior

```text
bullish_ref_hold = close > reference_price and intraday_vwap > reference_price
```

### Bearish News Behavior

```text
bearish_ref_fail = close < reference_price and intraday_vwap < reference_price
```

### Entry Logic Draft

```text
long_catalyst_trend =
    catalyst_direction == BULLISH
    and price_holds_above_reference
    and intraday_trend_up
    and not_extended_or_after_micro_pullback
```

```text
short_catalyst_trend =
    catalyst_direction == BEARISH
    and price_holds_below_reference
    and intraday_trend_down
    and not_late_after_capitulation
```

### Data Requirement

- OHLCV-only version: use gap as catalyst proxy.
- News-aware version: requires news timestamp and sentiment/category.
- Earnings-aware version: requires earnings date/time.

### Risk

Without real news data, this module can become look-ahead biased if “good/bad catalyst” is inferred from future price action.

---

## 4.5 Range-Bound / No-Man's-Land Filter — `BREITSTEIN_NO_MANS_LAND_GUARD_V1`

### Amaç

Consolidation içinde gereksiz trade alarak hesabı “paper cut” ile yıpratmayı engellemek.

### Range-Bound Proxy

```text
range_bound =
    abs(linreg_slope(close, lookback)) < slope_threshold
    and bollinger_band_width_percentile < compression_threshold
    and close within recent_high_low_range
```

### Reject Rule

```text
if range_bound and not range_breakout:
    reject_trade(reason="NO_MANS_LAND_RANGE_BOUND")
```

### Breakout Permission

```text
range_breakout =
    close > range_high
    or close < range_low
```

### MTC_V2 Mapping

- `ENTRY GATES`: chop/range no-trade guard
- Similar to Chop / ADX filters but more structure-based.

---

## 4.6 Trend Exhaustion / Capitulation Exit — `BREITSTEIN_CAPITULATION_EXIT_V1`

### Amaç

Trend yönünde yakalanan harekette, trend artık euphoric/capitulative hale geldiyse kâr almak.

### Upside Exhaustion Proxy

```text
upside_exhaustion =
    close > upper_band
    and volume > volume_ma * 2
    and bar_range > atr * 1.5
    and distance_from_vwap_pct > threshold
    and move_from_entry_R >= min_R
```

### Downside Exhaustion Proxy

```text
downside_exhaustion =
    close < lower_band
    and volume > volume_ma * 2
    and bar_range > atr * 1.5
    and distance_from_vwap_pct > threshold
```

### Exit Behavior

- Long trend trade: upside exhaustion -> partial/full profit.
- Short trend trade: downside exhaustion -> partial/full profit.
- Counter-trend reversal setup: downside exhaustion can be prerequisite for entry, not exit.

### Önemli Ayrım

Aynı “capitulation” kavramı iki farklı yerde kullanılır:

1. **Trend exhaustion:** mevcut pozisyondan çıkış.
2. **Right-side-of-V:** karşı yönde yeni setup hazırlığı.

Bu iki bağlam kodda ayrı state olarak tutulmalıdır.

---

## 4.7 Setup Quality Risk Tiering — `BREITSTEIN_SETUP_RISK_TIERS_V1`

### Amaç

Her setup'a aynı risk miktarını vermemek; A/B/C kalite sınıfına göre risk belirlemek.

### Quality Factors

| Factor | High-quality condition |
|---|---|
| Trend alignment | intraday + daily + weekly aynı yönde |
| Catalyst quality | güçlü haber/earnings/gap catalyst |
| Liquidity / in-play | yüksek relative volume, yüksek range |
| Reference price | entry reference price'a yakın |
| Stop quality | tight, structural, obvious invalidation |
| Range state | no-man's-land değil, gerçek trend veya breakout |
| Sentiment | capitulation/euphoria belirgin |
| Extension | entry çok geç değil |

### Risk Tiers

```yaml
A_PLUS:
  risk_multiplier: 1.25-1.50
A:
  risk_multiplier: 1.00
B:
  risk_multiplier: 0.50
C:
  risk_multiplier: 0.25
NO_TRADE:
  risk_multiplier: 0.00
```

### MTC_V2 Mapping

- `Position Sizing`: risk multiplier
- `ENTRY GATES`: minimum quality score
- `PortfolioState`: reduce size after drawdown / failed attempts

---

## 5. Potential Candidate Architectures

## Candidate A — `BREITSTEIN_INTRADAY_TREND_CONTINUATION`

### Classification

`CANDIDATE`

### Core Thesis

In-play stocks that trend cleanly above VWAP / moving average / prior-bar lows can continue far longer than expected. Fighting them creates large losses; riding them creates positive skew.

### Required Data

- Intraday OHLCV: 2m, 5m, or 15m
- Session VWAP
- Dollar volume / relative volume
- Optional daily trend context
- Optional catalyst metadata

### Entry Logic Draft

```text
long_setup =
    in_play_symbol
    and session_trend == UP_TREND
    and close > vwap
    and vwap_slope > 0
    and prior_bar_lows_holding
    and not_upside_capitulation
    and optional_pullback_or_breakout_trigger
```

### Exit Logic Draft

```text
exit_long_if:
    close < prior_bar_low_trailing
    or close < vwap
    or upside_exhaustion
    or trendline_break_down
```

### Primary Risk

Momentum chasing if entry is too extended. Must include extension guard.

---

## Candidate B — `BREITSTEIN_RIGHT_SIDE_V_REVERSAL`

### Classification

`CANDIDATE`

### Core Thesis

Extreme intraday panic can create asymmetric reversal setups, but only after the falling trend breaks. The right-side-of-V entry reduces heat versus guessing the bottom.

### Required Data

- Intraday OHLCV
- Relative volume
- Daily extension context
- Broad market panic proxy optional
- News filter optional: prefer no fresh negative company-specific news for broad panic bounce.

### Entry Logic Draft

```text
precondition =
    stock_down_large_pct
    and intraday_clean_downtrend
    and volume_capitulation
    and extension_from_vwap_or_ma

trigger =
    high > high[1]
    and close_optional > high[1]

entry = trigger_price
stop = recent_low
trail = prior_bar_low
```

### Best Use Cases

- Market-wide panic days.
- No-stock-specific bad news, only broad liquidation.
- Large-cap/high-beta/in-play names.
- Extreme extension + 2x volume capitulation.

### Avoid

- Fresh catastrophic company-specific news unless specifically testing news reversal variant.
- Illiquid small caps.
- Weak capitulation without clean prior trend.

---

## Candidate C — `BREITSTEIN_CATALYST_REFERENCE_TREND`

### Classification

`CANDIDATE_WITH_EXTERNAL_DATA`

### Core Thesis

A true catalyst creates a new reference price. If the market holds above/below the unaffected price and trends in the catalyst direction, traders across timeframes align.

### OHLCV-only Proxy

- Gap up/down with high relative volume.
- First 15–30 minute range establishes reference zone.
- Long if price holds above opening range/VWAP after gap-up.
- Short if price holds below opening range/VWAP after gap-down.

### News-aware Version

- Use news timestamp and classify catalyst direction.
- Reference price = pre-news price.
- Trade only when price action confirms catalyst direction.

---

## Candidate D — `BREITSTEIN_NO_MANS_LAND_GUARD`

### Classification

`SALVAGE_MODULE` / `ENTRY_GATE`

### Core Thesis

Do not trade inside compression/range unless there is a confirmed break into a new price range.

### Use

Add to existing MTC_V2 filters as optional structure-based chop filter.

---

## 6. Backtest Prototype Plan

### Phase 1 — OHLCV-only Intraday Prototype

Use 5m data first for practical research speed.

Test modules:

- VWAP trend guard
- Prior-bar high/low reversal trigger
- Prior-bar trailing stop
- Range-bound no-trade guard
- Capitulation proxy
- MTF daily context filter

Do not use:

- News sentiment
- Manual catalyst labels
- Hand-picked winner list
- Future-aware in-play selection

### Phase 2 — In-Play Universe Construction

Define in-play symbols without look-ahead:

```text
in_play =
    premarket_gap_abs_pct >= threshold
    or first_30min_relative_volume >= threshold
    or first_30min_range_pct >= threshold
    or daily_ATR_percentile >= threshold
```

### Phase 3 — Right-Side-of-V Tests

Test separately:

1. Broad market panic days only.
2. Stock-specific gap-down days.
3. High-beta names only.
4. Large-cap liquid names only.
5. Crypto-related equities / semis / AI names as thematic subsets.

### Phase 4 — News-aware Catalyst Version

Only after OHLCV proxy shows promise:

- Add earnings/news timestamp.
- Add catalyst direction.
- Add reference price.
- Compare with OHLCV-only gap proxy.

### Phase 5 — Integration Decision

Only consider Pine/MTC integration if:

- Positive expectancy survives symbol/time split.
- Slippage sensitivity is acceptable.
- Entry/exit timing is not too dependent on sub-5m bars.
- News-free proxy is robust enough or external event data pipeline exists.

---

## 7. Parameter Draft

```yaml
strategy_id: BREITSTEIN_RIGHT_SIDE_V_V1
classification: CANDIDATE
primary_timeframe: 5m
secondary_timeframes: [15m, daily]
direction: long_and_short_possible

universe:
  min_price: 10
  min_avg_dollar_volume: 20000000
  require_in_play: true
  in_play_methods:
    - gap_pct
    - relative_volume
    - first_30m_range
    - daily_atr_percentile

trend:
  use_vwap: true
  vwap_hold_bars: 5
  vwap_hold_ratio: 0.75
  use_linreg_slope: true
  slope_lookback: 20
  use_prior_bar_structure: true
  prior_bar_sequence_min: 3

capitulation:
  volume_spike_multiplier: 2.0
  range_atr_multiplier: 1.5
  distance_from_vwap_pct_min: 2.0
  extension_from_daily_ma_min: optional

entry:
  right_side_v_trigger: prior_bar_high_break
  require_close_confirmation: false
  max_entry_distance_from_trigger_pct: 0.5
  reject_if_range_bound: true

risk:
  setup_quality_tiers: true
  base_risk_bps: 25-50
  A_plus_multiplier: 1.25
  B_multiplier: 0.50
  C_multiplier: 0.25
  max_loss_per_trade_bps: 50

exits:
  initial_stop: recent_intraday_low
  trailing_stop: prior_bar_low
  vwap_fail_exit: true
  exhaustion_partial_exit: true
  time_stop_bars: optional
```

---

## 8. MTC_V2 Integration Notes

### Do Not Touch Yet

- `01_PINE/MTC_V2.pine`
- Production Python runner
- Existing parity harness
- Existing optimization loop
- Existing data bundle

### Future Integration Candidate

Best integration path:

1. Build isolated Python research module under a new experimental folder.
2. Implement `BREITSTEIN_VWAP_GUARD_V1` first because it is a clean entry gate.
3. Implement `BREITSTEIN_NO_MANS_LAND_GUARD_V1` as a generic filter.
4. Implement `BREITSTEIN_RIGHT_SIDE_V_V1` as a standalone intraday signal producer.
5. Implement `BREITSTEIN_SETUP_RISK_TIERS_V1` later as a position sizing overlay.
6. Only if robust, consider Pine version with limited scope.

### Pine / Parity Risk

High. Reasons:

- Intraday VWAP and prior-bar trailing are Pine-compatible, but news/reference price is not native.
- Multi-timeframe alignment can repaint if not carefully prior-closed.
- Session handling, premarket inclusion/exclusion, gaps, halts, and news timing can create parity mismatches.
- If MTC_V2 is mainly bar-close strategy, this setup must be adapted to bar-close deterministic execution.

---

## 9. Red Flags / Caution

- Speaker discusses professional intraday prop-trading context; execution quality may not transfer directly to slower retail systems.
- Some examples rely on real-time news flow and scanners.
- “In play” selection can become look-ahead biased if defined using full-day range/volume.
- 2-minute bar behavior may be too noisy or slippage-sensitive.
- Hype around large P&L examples should not be treated as statistical proof.
- Transcript has some transcription corruption around the Tesla loss section; use the clear surrounding logic rather than exact corrupted text.

---

## 10. Trader Wiki Value

Even if strategy testing fails, this video has high Trader Wiki value under:

- `03_MARKET_STRUCTURE`
- `06_EXECUTION_AND_FEES`
- `01_RISK_MANAGEMENT`
- `04_SYSTEM_DEVELOPMENT`

Potential wiki note themes:

- Trend with multiple definitions.
- How to avoid fighting VWAP.
- Right-side-of-V reversal concept.
- Why range-bound stocks cause paper cuts.
- Setup grading and risk tiering.
- How to systemize discretionary trading observations.

---

## 11. Final Output Summary

### Files that would be created in repo later

```text
02_RESEARCH/YOUTUBE_STRATEGY_INTAKE/...
  intake_report.md

03_CANDIDATES/QL_CAND_2026-05-03_R215f4fj7V8_BREITSTEIN_TREND/
  candidate_summary.md
  prototype_plan.md
  parameter_draft.yaml

11_TRADER_WIKI/03_MARKET_STRUCTURE/
  TW_2026-05-03_trend_right_side_v_breitstein.md
```

### Files not touched

```text
01_PINE/MTC_V2.pine
production Python runner files
existing backtest/optimization output
existing data bundles
existing registries
```

### Next Action

**Recommended next step:** Build an isolated Python prototype for `BREITSTEIN_RIGHT_SIDE_V_V1` and `BREITSTEIN_VWAP_GUARD_V1` using 5m intraday OHLCV. Do not implement in Pine until the capitulation, in-play universe, VWAP guard, range-bound filter, and trailing-stop behavior are fully deterministic and validated across multiple symbols.

---

## 12. Final Classification Block

```text
classification: CANDIDATE
codex_status: READY_FOR_PYTHON_PROTOTYPE
candidate_type: INTRADAY_TREND_PLUS_RIGHT_SIDE_V_REVERSAL
primary_modules:
  - BREITSTEIN_TREND_ALIGNMENT_V1
  - BREITSTEIN_VWAP_GUARD_V1
  - BREITSTEIN_RIGHT_SIDE_V_V1
  - BREITSTEIN_CATALYST_REF_PRICE_V1
  - BREITSTEIN_NO_MANS_LAND_GUARD_V1
  - BREITSTEIN_CAPITULATION_EXIT_V1
  - BREITSTEIN_SETUP_RISK_TIERS_V1
wiki_value: HIGH
duplicate: NOT_DUPLICATE_IN_CURRENT_SESSION
repo_duplicate_check: NOT_VERIFIED_REPO_NOT_AVAILABLE
channel_quality_check: NOT_VERIFIED_REPO_NOT_AVAILABLE
pine_touched: NO
python_runner_touched: NO
backtest_run: NO
optimization_run: NO
```
