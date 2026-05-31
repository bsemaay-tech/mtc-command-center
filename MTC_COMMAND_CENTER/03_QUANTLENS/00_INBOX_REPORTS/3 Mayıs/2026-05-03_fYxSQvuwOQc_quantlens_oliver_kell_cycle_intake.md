# QUANTLENS TRANSCRIPT INTAKE REPORT — fYxSQvuwOQc

**Generated:** 2026-05-03  
**Source URL:** https://youtu.be/fYxSQvuwOQc?si=mZyENAdFJu8x7LKZ  
**Normalized URL:** https://www.youtube.com/watch?v=fYxSQvuwOQc  
**Video ID:** `fYxSQvuwOQc`  
**Transcript Status:** Provided by user in chat  
**Channel:** `UNKNOWN_CHANNEL`  
**Prompt Applied:** `00_quantlens_transcript_intake_prompt.md` intake logic

---

## 1. Executive Verdict

```yaml
classification: CANDIDATE
secondary_classification: TRADER_WIKI_RECOMMENDED
codex_status: READY_FOR_PYTHON_PROTOTYPE
overall_priority: HIGH
production_ready: false
backtest_ready: partially
primary_asset_class: equities/high_beta_growth
crypto_transferability: medium_high
```

This is a high-value QuantLens candidate. The system is not a single indicator trick; it is a repeatable trend-cycle framework based on:

- 10 EMA and 20 EMA.
- Weekly/daily/65-minute timeframe alignment.
- Reversal extension.
- Wedge Pop.
- EMA Crossback.
- Basin Break.
- Exhaustion Extension.
- Wedge Drop.
- Expansion/contraction price structure.
- High-beta leading stocks and in-play themes.
- Moving average riding for exits.

**Best first prototype:** `QL_KELL_WEDGE_POP_CROSSBACK_10_20EMA_v0`

---

## 2. Source Quality Assessment

```yaml
source_quality_score: 8/10
strategy_idea_score: 9/10
implementation_clarity_score: 8/10
process_value_score: 9/10
risk_management_value_score: 8/10
crypto_transferability_score: 7/10
```

### Positive signs

- Multiple clear setup definitions.
- Strong focus on price structure, not only moving average crossing.
- Multi-timeframe alignment is explicit.
- The system is fractal and can be adapted to crypto.
- The speaker warns about whipsaw and discretionary risk.
- The system clearly separates scan timeframe, management timeframe and execution timeframe.
- The framework gives both entries and exits.

### Limitations

- Some execution remains discretionary.
- “Tight mini base” and “extension” need objective thresholds.
- Best results depend heavily on stock selection / themes / high-beta leaders.
- 65-minute timeframe is equity-session-specific; crypto adaptation should use 1h or 4h.

---

## 3. Core System: Cycle of Price Action

```yaml
cycle_sequence:
  1: reversal_extension
  2: snapback_to_10_20EMA
  3: pullback / higher low
  4: volatility contraction / mini base
  5: wedge_pop
  6: EMA_crossback
  7: basin_break
  8: possible_second_or_third_basin_break
  9: exhaustion_extension
  10: lower_high
  11: wedge_drop
  12: downtrend / repeat cycle
```

The system is based on the idea that bottoms usually require a **higher low**, and tops usually require a **lower high**.

---

## 4. Indicators / References

```yaml
moving_averages:
  daily:
    ema10: primary fast trend guide
    ema20: primary swing trend guide
    ema5: optional faster guide
  weekly:
    ema5_week: roughly similar to daily EMA20
    ema10_week: weekly trend support
    ema20_week: major trend filter
```

Key principle:

```yaml
green_light_environment:
  condition:
    - price above 10 EMA and 20 EMA
  action:
    - long trades allowed

red_light_environment:
  condition:
    - price below 10 EMA and 20 EMA
  action:
    - cash or short bias
```

But the speaker explicitly warns that the **buy area is not simply crossing the moving averages**. The actual buy area is the break of a tight price structure / mini base.

---

## 5. Setup 1 — Wedge Pop

### Raw description

After capitulation/reversal extension:

1. Price snaps back to moving averages.
2. Pulls back again.
3. Volatility decreases.
4. Price tightens.
5. A higher low forms.
6. Price breaks through the mini-base swing high / wedge structure.

### Objective v0

```yaml
candidate_id: QL_KELL_WEDGE_POP_001
direction: long
timeframe:
  stock_original: daily + 65m
  crypto_adaptation: daily + 4h or 1h

setup:
  reversal_extension:
    - close < EMA20 * (1 - extension_threshold)
    - or distance_from_ema20_zscore < negative_threshold
  snapback:
    - price returns to EMA10/EMA20 zone
  higher_low:
    - recent swing low > prior capitulation low
  contraction:
    - ATR_percentile declining
    - range_N / range_M below threshold
    - mini_base_duration >= 3 bars
  trigger:
    - close breaks above mini_base_high
    - preferably close > EMA10 and close > EMA20
  entry:
    - next_bar_open
    - or stop entry above mini_base_high
  stop:
    - below mini_base_low
    - or below higher_low
```

### Verdict

```yaml
verdict: READY_FOR_PYTHON_PROTOTYPE
priority: HIGH
```

---

## 6. Setup 2 — EMA Crossback

### Raw description

After Wedge Pop and initial move, price pulls back into the 10/20 EMA zone and forms the next higher low.

### Objective v0

```yaml
candidate_id: QL_KELL_EMA_CROSSBACK_001
direction: long

setup:
  prior_state:
    - recent wedge_pop occurred
    - price above daily EMA10/EMA20
  pullback:
    - low touches or approaches EMA10/EMA20 zone
    - price remains above prior major low
  structure:
    - 65m or 1h forms higher low
  trigger:
    - lower timeframe breaks local swing high
    - or daily closes back above EMA10
  stop:
    - below pullback low
  exit:
    - break of selected MA after repeated holds
```

### Verdict

```yaml
verdict: READY_FOR_PYTHON_PROTOTYPE
priority: HIGH
```

---

## 7. Setup 3 — Basin Break

### Raw description

A 1-3 week consolidation back into moving averages after the trend has already started.

### Objective v0

```yaml
candidate_id: QL_KELL_BASIN_BREAK_001
direction: long

setup:
  trend:
    - price above EMA10/EMA20
    - weekly above EMA10/EMA20
  consolidation:
    - duration 5 to 15 trading days
    - range contracts
    - pullback into EMA10/EMA20 zone
  trigger:
    - break above consolidation high
  stop:
    - below consolidation low
```

### Verdict

```yaml
verdict: CANDIDATE
priority: MEDIUM_HIGH
```

---

## 8. Setup 4 — Exhaustion Extension / Wedge Drop Exit

### Raw description

After a strong trend, price gets extended from the 10-day and/or weekly 10-week moving average. It flushes back, bounces, forms a lower high, then loses the moving averages / structure.

### Objective v0

```yaml
candidate_id: QL_KELL_WEDGE_DROP_EXIT_001
type: exit_or_short_setup

warning:
  - use first as exit module, not short module

conditions:
  exhaustion_extension:
    - close far above EMA10/EMA20
    - daily and weekly both extended
  lower_high:
    - bounce fails below prior high
  trigger:
    - close below EMA10/EMA20
    - or break below lower_high structure support
  action:
    - reduce or exit long
```

### Verdict

```yaml
verdict: HIGH_VALUE_EXIT_RESEARCH
priority: HIGH
```

---

## 9. Multi-Timeframe Architecture

```yaml
timeframe_stack_original:
  higher_timeframe:
    - weekly
    - monthly
  trade_management:
    - daily
    - 65-minute
  execution:
    - 30-minute
    - 10-minute
    - 15-minute

crypto_adaptation:
  higher_timeframe:
    - weekly
  trade_management:
    - daily
    - 4h
  execution:
    - 1h
    - 30m
```

Important rule:

```yaml
do_not_create_trades_on_lower_timeframe:
  meaning: >
    Lower timeframe is for execution only. Weekly/daily structure must drive
    the trade idea.
```

---

## 10. Stock / Asset Selection

The speaker emphasizes:

```yaml
selection:
  - strongest stocks
  - in-play themes
  - liquid high-beta names
  - names ahead of indexes in the cycle
  - stocks forming higher lows while index forms lower lows
```

Crypto adaptation:

```yaml
crypto_candidate_universe:
  - BTCUSDT
  - ETHUSDT
  - SOLUSDT
  - BNBUSDT
  - XRPUSDT
  - COIN-related proxy not crypto pair
  - sector basket if available
```

For crypto, “themes” can be approximated with relative strength against BTC or TOTAL market index.

---

## 11. Trade Management

```yaml
management:
  default_exit:
    - hold while price respects EMA10 or EMA20
  moving_average_selection:
    - if stock repeatedly holds EMA20, use EMA20
    - if after 3-4 holds price shifts to EMA10 support, use EMA10
  take_profit:
    - sell obvious blowoff / exhaustion extension
    - otherwise let MA break decide
  add_positions:
    - build during mini-base / pullback into MA zone
    - raise stop as base progresses
```

Position sizing observations from transcript:

```yaml
position_sizing:
  top_liquid_names:
    max_position: 30_to_35_percent
  liquid_core_names:
    max_position: 15_to_20_percent
  volatile_lower_price_names:
    max_position: around_7_percent
  volatile_higher_price_names:
    max_position: around_12_percent
```

For QuantLens research, do not copy these sizes directly. Use risk-based sizing first.

---

## 12. QuantLens Implementation Recommendation

Do not attempt the full discretionary system first. Build the objective skeleton:

```yaml
first_python_prototype:
  name: QL_KELL_WEDGE_POP_CROSSBACK_10_20EMA_v0
  modules:
    - ema_state_engine
    - extension_detector
    - contraction_detector
    - mini_base_detector
    - wedge_pop_trigger
    - ema_crossback_trigger
    - ma_ride_exit
```

### Base parameters

```yaml
parameters:
  ema_fast: 10
  ema_slow: 20
  contraction_lookback: [3, 5, 8]
  max_base_range_pct: [5, 8, 12]
  extension_threshold_atr: [2.0, 2.5, 3.0]
  ma_touch_tolerance_pct: [0.5, 1.0, 2.0]
  stop_mode:
    - mini_base_low
    - higher_low
    - ATR_2
  exit_ma:
    - EMA10
    - EMA20
```

---

## 13. MTC / QuantLens Fit

```yaml
mtc_fit:
  producer:
    - wedge_pop
    - ema_crossback
    - basin_break
  gates:
    - weekly trend alignment
    - relative strength
    - volatility contraction
    - liquidity/high_beta proxy
  exits:
    - MA ride exit
    - exhaustion extension exit
    - lower high / wedge drop exit
  sizing:
    - stop-distance based sizing
```

This is much more relevant to crypto than the full CANSLIM video, because the core mechanics are price/EMA/structure based.

---

## 14. Candidate Ranking Inside This Video

```yaml
ranked_candidates:
  1:
    name: QL_KELL_WEDGE_POP_CROSSBACK_10_20EMA_v0
    priority: HIGH
    next_action: python_prototype
  2:
    name: QL_KELL_MA_RIDE_EXIT_v0
    priority: HIGH
    next_action: exit_module_spec
  3:
    name: QL_KELL_BASIN_BREAK_v0
    priority: MEDIUM_HIGH
    next_action: after first prototype
  4:
    name: QL_KELL_EXHAUSTION_EXTENSION_EXIT_v0
    priority: MEDIUM_HIGH
    next_action: exit research
```

---

## 15. Final Decision

```yaml
final_decision:
  classification: CANDIDATE
  best_first_test: QL_KELL_WEDGE_POP_CROSSBACK_10_20EMA_v0
  codex_status: READY_FOR_PYTHON_PROTOTYPE
  priority: HIGH
  reason: >
    The transcript provides a coherent multi-timeframe trend-cycle framework
    with objective moving-average state, codable contraction/trigger logic,
    and practical exit logic.
```

---

## 16. Suggested Repo Paths

```text
06_QUANTLENS_LAB/intake/reports/2026-05-03_fYxSQvuwOQc_quantlens_oliver_kell_cycle_intake.md
06_QUANTLENS_LAB/research/kell_wedge_pop_crossback/README.md
11_TRADER_WIKI/03_MARKET_STRUCTURE/TW_2026-05-03_kell_cycle_price_action.md
```
