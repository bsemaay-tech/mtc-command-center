# QuantLens Transcript Intake Report

## 1. Metadata

- Source Title: The Wedge Pop Trading Setup of Trading Champion Oliver Kell
- Source URL: https://www.youtube.com/watch?v=m8F3KkBDtC0
- Original URL: https://youtu.be/m8F3KkBDtC0?si=oiUeKyAkvkzAl5Bd
- Video ID: `m8F3KkBDtC0`
- Speaker / Main Trader: Oliver Kell
- Channel: TraderLion / UNKNOWN_CHANNEL in repo context
- Intake Date: 2026-05-03
- Transcript File: `The Wedge Pop Trading Setup of Trading Champion Oliver Kell.md`
- Transcript SHA256: `9e02b6849dcbd160af7ad50722dfdcedd9d96af3fd44e72ef696cc7650c56454`
- Language: English transcript
- Processing Mode: Transcript-only intake
- Repo Registry Access: Not available in this chat session; duplicate and blacklist checks must be re-run by Codex inside repo.

---

## 2. Final Classification

- Intake Verdict: `CANDIDATE`
- Codex Status Suggestion: `READY_FOR_PYTHON_PROTOTYPE`
- Candidate Type: `STRATEGY_CANDIDATE`
- Pine Migration Now: `NO`
- Trader Wiki Note: `YES`, secondary
- Main Candidate ID Suggestion: `YT_OLIVER_KELL_WEDGE_POP_PRICE_CYCLE_V1`
- Secondary Module Candidates:
  - `PRICE_CYCLE_REGIME_FILTER_V1`
  - `WICK_PLAY_CONTEXTUAL_ENTRY_V1`
  - `TREND_KNOCKOUT_RECOVERY_V1`

### Decision Rationale

This transcript contains a repeatable and partially mechanical swing-trading framework built around Oliver Kell's “cycle of price action.” It is stronger than a pure Trader Wiki note because it includes:

1. Objective 10/20 moving-average green/red light regime.
2. Wedge pop setup after volatility contraction.
3. EMA crossback and base-and-break continuation stages.
4. Exhaustion extension / wedge drop exit and risk-reduction logic.
5. Multi-timeframe alignment using weekly/monthly, daily, hourly/15-minute, and 5-minute charts.
6. Stop placement based on daily low / max-pain stop and lower-timeframe tightening.
7. Position sizing tiers for top ideas, core ideas, and volatile names.
8. Wick play as contextual entry enhancement, not standalone signal.

This is suitable for a Python research prototype before any Pine integration.

---

## 3. Duplicate / Registry / Blacklist Handling

### Duplicate Status

- `video_id` duplicate check: `UNKNOWN_REQUIRES_REPO_CHECK`
- `transcript_hash` duplicate check: `UNKNOWN_REQUIRES_REPO_CHECK`
- Same title / channel / similar transcript check: `UNKNOWN_REQUIRES_REPO_CHECK`

### Required Codex Repo Checks

Codex should check:

```text
_registry/youtube_video_index.csv
_registry/channel_quality_registry.csv
channel_blacklist.yaml
```

If `video_id = m8F3KkBDtC0` already exists, Codex must stop and return previous candidate/status/folder information without creating a duplicate.

### Channel Quality Decision

- Current chat-only decision: `UNKNOWN_CHANNEL`
- Blacklist action: `NO_BLACKLIST_DECISION`
- Reason: Channel registry not available here.

---

## 4. Strategy Extraction Summary

### Core Thesis

The strategy is a fractal trend-following / swing-trading framework. It uses 10/20 period moving averages to define whether price is in a constructive or defensive regime. The preferred entry is not the first bottom tick after a selloff, but the **wedge pop**: price contracts near/under the moving averages after a down move, then reclaims them with strength.

Core structure:

```text
Reversal Extension
→ Wedge Pop
→ EMA Crossback
→ Base-and-Break / Basin Break
→ Exhaustion Extension
→ Wedge Drop
→ Defensive / cash / short-bias regime
```

The method works across timeframes, but the main research version should begin with daily execution and weekly/daily context.

---

## 5. Candidate Strategy: `YT_OLIVER_KELL_WEDGE_POP_PRICE_CYCLE_V1`

## 5.1 Universe

Initial universe:

```text
U.S. equities
price > 10 or 15
avg_dollar_volume_20d > configurable threshold
avg_volume_20d > configurable threshold
exclude illiquid microcaps
prefer high-growth / high-RS names
```

Optional later filters:

```text
earnings growth
sales growth
new product / new issue flag
sector/group strength
IPO age
```

---

## 5.2 Timeframes

The transcript suggests the following hierarchy:

```text
Higher timeframe: weekly / monthly
Trading timeframe: daily
Execution / risk timeframe: hourly or 15-minute
Laser focus timeframe: 5-minute, only at important higher-timeframe levels
```

### Python Prototype Simplification

Start with:

```text
Phase 1: Daily-only prototype
Phase 2: Weekly + daily alignment
Phase 3: Daily signal + 60m/15m execution approximation
Phase 4: 5m open/reversal extension research only if intraday data quality is good
```

Do not start with the 5-minute chart. It creates many false trades unless anchored to a higher-timeframe level.

---

## 5.3 Green / Red Light Regime

Use 10/20 EMA on the active timeframe.

### Long Green Light

```text
close > ema10
ema10 > ema20
ema10 slope > 0
ema20 slope >= 0
or price coiling below ema10/ema20 and preparing to reclaim them
```

### Red Light / Defensive

```text
close < ema10 and close < ema20
ema10 <= ema20
ema10 slope <= 0
wedge drop confirmed
```

### Portfolio Behavior

```text
green_light: allow longs and increase exposure
red_light: reduce exposure, avoid new longs, optionally allow shorts
neutral/chop: smaller size or no trade
```

---

## 5.4 Price Cycle State Machine

Suggested state labels:

```python
PRICE_CYCLE_STATE = [
    "DOWNTREND",
    "REVERSAL_EXTENSION",
    "VOLATILITY_CONTRACTION",
    "WEDGE_POP",
    "EMA_CROSSBACK",
    "BASE_AND_BREAK",
    "EXHAUSTION_EXTENSION",
    "WEDGE_DROP",
    "RED_LIGHT"
]
```

### Reversal Extension

Potential bottoming sign after a downtrend:

```text
price stretched below ema10
large down move / high downside volatility
heavy volume capitulation optional
then sharp snapback toward ema20
```

This is mostly a watchlist trigger, not the preferred entry.

### Wedge Pop

Preferred first constructive entry after selloff:

```text
prior state: downtrend or reversal extension
price moves back toward 10/20 EMA
volatility contracts / tight bars / inside bars
price breaks above local pivot / mini trendline
price reclaims ema10/ema20
```

Candidate detection:

```python
ema10 = close.ewm(span=10).mean()
ema20 = close.ewm(span=20).mean()

vol_contract = atr_pct < atr_pct.rolling(20).median()
pivot_high = high.rolling(pivot_window).max().shift(1)
wedge_pop = (
    (close > ema10) &
    (close > ema20) &
    (ema10 >= ema20 * ema_tolerance) &
    (close > pivot_high) &
    vol_contract_recent
)
```

### EMA Crossback

First pullback to 10/20 EMA after wedge pop:

```text
price already in green light
pulls back to ema10/ema20
holds or undercuts briefly
then flips back up through pivot / prior bar high
```

### Base-and-Break / Basin Break

Continuation base after trend is underway:

```text
1-3 week base / consolidation
price stays mostly near or above ema10/ema20
volatility contracts
break above base pivot
```

### Exhaustion Extension

Potential sell / trim zone:

```text
price extended far above ema10/ema20 and/or 10-week MA
euphoria / large wide-range bars / multiple gaps
late in trend after one or more bases
```

### Wedge Drop

Defensive confirmation:

```text
after upside extension, price pulls back to moving averages
fails to regain power
drops through ema10/ema20 and a local pivot
```

---

## 5.5 Entry Rules

### Primary Long Entry: Wedge Pop

Minimum version:

```text
weekly trend not bearish
daily price was below / around ema10/ema20
daily volatility contracted for N bars
daily close breaks above local pivot and above ema10/ema20
stock shows relative strength vs index or is ahead of index cycle
entry on breakout close or next open
```

### Aggressive Version

```text
daily setup exists
hourly/15m wedge pop triggers before daily close
enter with tighter stop
```

### Gap-Up Version

For catalyst gaps:

```text
if high-conviction setup + earnings/catalyst gap:
    enter partial size early
    add after first 15-30 minutes if price holds
else:
    wait 15-30 minutes for settlement before entry
```

### No-Chase Rule

```text
if wedge_pop already missed:
    do not chase
    wait for EMA crossback
```

---

## 5.6 Wick Play Module: `WICK_PLAY_CONTEXTUAL_ENTRY_V1`

### Context

The wick play is not a standalone signal. It should only enhance an already valid broader setup.

### Raw Pattern

```text
Day 1: price trades up but closes off high, leaving an upper wick
Day 2: price gaps into / above prior wick
Day 2: price stays positive and does not go negative
Entry: price takes out top of prior wick
```

### Psychology

Sellers controlled the close on Day 1. If price gaps up into that wick and then clears the wick high, buyers have overpowered the prior-day sellers.

### Implementation

```python
prior_upper_wick = high.shift(1) - close.shift(1)
has_upper_wick = prior_upper_wick / close.shift(1) > wick_min_pct

gap_into_wick = open > close.shift(1) and open < high.shift(1)
stays_positive = low >= open * (1 - allowed_intraday_undercut)
wick_break = high > high.shift(1)

wick_play_long = broader_setup_valid & has_upper_wick & gap_into_wick & stays_positive & wick_break
```

### Important Guard

```text
Do not buy random wick plays.
Require base / wedge pop / breakout / higher-timeframe context.
```

---

## 5.7 Trend Knockout Recovery Module: `TREND_KNOCKOUT_RECOVERY_V1`

Oliver describes cases where price shakes out short-term moving averages, then recovers.

Candidate logic:

```text
prior uptrend / constructive weekly base
price loses 10/20 EMA or short-term pivot
does not fully break major support / 50-day
recovers above 10/20 EMA
flips a 1-3 day flag/pivot high
```

This should be a separate experiment because it can overfit to discretionary interpretation.

---

## 6. Relative Strength / Leadership Logic

Oliver uses the concept of a stock being “ahead of the indexes” in the price cycle.

Python proxy:

```text
index_state = price_cycle_state(index)
stock_state = price_cycle_state(stock)

stock_leadership = stock_state is more advanced/bullish than index_state
```

Example:

```text
If QQQ is only at wedge pop, but the stock is breaking out of a base at new highs, it has relative strength.
```

Additional filters:

```python
rs_line = stock_close / benchmark_close
rs_line_slope_20 > 0
rs_line near N-day high
```

---

## 7. Position Sizing / Portfolio Rules

### Top Ideas

```text
25-35% account allocation
requires strong weekly chart
requires strong story / catalyst / leadership
requires relative strength vs peers
avoid if highly volatile unless stop is tight
```

### Core Ideas

```text
15-20% allocation
good setup but not top-tier leader
```

### Smaller / Volatile Ideas

```text
5-15% allocation
higher volatility or less confirmed leadership
```

### Risk-Aware Rule

```text
if stop_distance_pct is large:
    reduce position size
```

---

## 8. Stop / Exit Rules

### Initial Stop

Common breakout stop:

```text
max pain stop = daily low of entry day
```

If using lower timeframe:

```text
use hourly/15m pivot low to tighten risk
```

### Opening Handling

```text
let first 20-30 minutes settle when needed
if price comes back up, adjust stop to new intraday low
```

### Stop Raising

```text
when price confirms strength by taking out next pivot:
    move stop under latest relevant pivot low
```

### Scratch Rule

```text
if not in the money by end of day:
    optionally sell and rebuy next day if setup remains valid
```

### Profit Taking / Exit

```text
sell into strength at exhaustion extension
scale out rather than sell all at once
full exit if second extension from 10 EMA + extended from 10-week MA
exit/reduce on wedge drop
exit/reduce on loss of 20 EMA depending on trader style
```

---

## 9. Candidate Configuration YAML Sketch

```yaml
candidate_id: YT_OLIVER_KELL_WEDGE_POP_PRICE_CYCLE_V1

universe:
  asset_class: equities
  min_price: 10
  min_avg_dollar_volume_20d: 20000000

timeframes:
  context: weekly
  signal: daily
  execution: daily_first
  intraday_optional: [60m, 15m, 5m]

moving_averages:
  fast_ema: 10
  slow_ema: 20
  reference_sma: 50
  weekly_reference_ma: 10

regime:
  green_light:
    close_above_fast_ema: true
    close_above_slow_ema: true
    fast_above_or_near_slow: true
  red_light:
    close_below_fast_and_slow: true
    wedge_drop_confirmed: true

entry:
  primary_setup: wedge_pop
  require_volatility_contraction: true
  pivot_window: 3
  max_entry_extension_pct: 3.0
  no_chase: true
  allow_ema_crossback: true
  allow_base_and_break: true
  allow_wick_play_contextual: true

risk:
  initial_stop_mode: daily_low
  allow_intraday_tight_stop: true
  scratch_if_not_profitable_eod: optional
  move_stop_after_pivot_confirmation: true

position_sizing:
  top_idea_pct: [25, 35]
  core_idea_pct: [15, 20]
  volatile_or_lower_conviction_pct: [5, 15]
  scale_down_by_stop_distance: true

exits:
  reduce_on_exhaustion_extension: true
  exit_on_wedge_drop: true
  reduce_or_exit_on_loss_of_20ema: testable
  scale_out_not_all_at_once: true
```

---

## 10. Python Prototype Plan

### Phase 1 — Daily-Only Price Cycle

Implement:

```text
10/20 EMA state
green/red light state
wedge pop detector
EMA crossback detector
base-and-break detector
daily low stop
basic trailing stop by pivot lows
```

### Phase 2 — Weekly Context

Add:

```text
weekly 10MA extension
weekly base / consolidation context
higher-timeframe alignment guard
```

### Phase 3 — Relative Strength / Leadership

Add:

```text
stock price cycle ahead of benchmark
RS line slope / high filter
leader ranking
```

### Phase 4 — Wick Play

Add:

```text
contextual wick play module
gap-up handling
prior wick high trigger
```

### Phase 5 — Portfolio Simulation

Add:

```text
top/core/small idea sizing
green/red light exposure scaling
scratch trade handling
scale-out rules
```

---

## 11. MTC_V2 Mapping

### Producer

```text
Producer_KellWedgePopPriceCycle
```

Outputs:

```text
raw_long_pulse
price_cycle_state
green_light
red_light
wedge_pop
ema_crossback
base_and_break
exhaustion_extension
wedge_drop
wick_play_context
trend_knockout_recovery
```

### Signal Transform

```text
Confirmation transform for pivot break
Optional retest transform for EMA crossback
```

### Entry Gates

```text
MA trend gate
HTF alignment gate
RS leadership gate
No-chase extension guard
Market regime gate
Earnings/catalyst gate optional
```

### Position Manager

```text
Top idea / core idea / small idea sizing class
No new longs in red light
Allow exposure expansion only in green light
```

### Exit Rules

```text
INITIAL_SL: daily low / lower timeframe pivot low
TRAIL: pivot-low trail / 10 or 20 EMA trail
FILTER_BLOCK: wedge drop / red light
TIME_STOP: no EOD profit / no follow-through
PARTIAL: exhaustion extension / scale into strength
```

---

## 12. Backtest Cautions

- Many rules are discretionary; define strict state-machine variants to avoid hindsight bias.
- 10/20 EMA creates more whipsaws than slower moving averages.
- Intraday execution needs reliable intraday data; daily-only approximation may understate or overstate the edge.
- “Story,” “top idea,” and “growth leader” are qualitative; first prototype should use RS/volume/fundamental proxies.
- Gap-up entries and wick plays are sensitive to open/high/low sequencing.
- Avoid survivorship bias in equity universe.

---

## 13. Trader Wiki Note

Suggested wiki path:

```text
11_TRADER_WIKI/04_SYSTEM_DEVELOPMENT/TW_2026-05-03_OLIVER_KELL_WEDGE_POP_PRICE_CYCLE.md
```

### Key Lessons

- Use 10/20 moving averages as objective green/red light framework.
- Prefer wedge pop after volatility contraction, not random bottom picking.
- Buy strength on the lower timeframe even when the daily is pulling back.
- The setup is fractal but lower timeframes create more whipsaws.
- If you miss the wedge pop, wait for EMA crossback; do not chase.
- Top ideas need story, weekly structure, relative strength, and manageable volatility.
- The wick play is useful only inside a larger pattern.
- Scale out into strength; avoid selling the whole leader too early.
- In red-light market conditions, protect capital.

---

## 14. Files To Create In Repo

Suggested candidate folder:

```text
06_QUANTLENS_LAB/strategy_candidates/YT_OLIVER_KELL_WEDGE_POP_PRICE_CYCLE_V1/
```

Suggested files:

```text
README.md
candidate_spec.md
rules.yaml
research_notes.md
prototype_plan.md
transcript_notes.md
```

Suggested module subnotes:

```text
modules/WICK_PLAY_CONTEXTUAL_ENTRY_V1.md
modules/TREND_KNOCKOUT_RECOVERY_V1.md
modules/PRICE_CYCLE_REGIME_FILTER_V1.md
```

Suggested wiki file:

```text
11_TRADER_WIKI/04_SYSTEM_DEVELOPMENT/TW_2026-05-03_OLIVER_KELL_WEDGE_POP_PRICE_CYCLE.md
```

Registry update required:

```text
_registry/youtube_video_index.csv
_registry/channel_quality_registry.csv
```

---

## 15. Do Not Touch

Per intake prompt:

```text
Do not modify 01_PINE/MTC_V2.pine
Do not modify production Python runner files
Do not run backtest
Do not run optimization
Do not create big CSV/data/cache/result bundles
Do not overwrite existing files before reading them
Do not write secrets/API keys/webhooks
```

---

## 16. Next Action For Codex

Recommended next action:

```text
1. Check duplicate registry for video_id m8F3KkBDtC0 and transcript hash.
2. If not duplicate, create candidate folder YT_OLIVER_KELL_WEDGE_POP_PRICE_CYCLE_V1.
3. Create candidate_spec.md and rules.yaml only.
4. Create separate module notes for wick play, price-cycle regime, and trend-knockout recovery.
5. Do not code Pine.
6. Do not run backtest yet.
7. Prepare Python prototype task plan for later review.
```

---

## 17. Final Verdict

```text
VERDICT: CANDIDATE
CODEX_STATUS: READY_FOR_PYTHON_PROTOTYPE
PRIMARY_CANDIDATE: YT_OLIVER_KELL_WEDGE_POP_PRICE_CYCLE_V1
SECONDARY_MODULES:
  - PRICE_CYCLE_REGIME_FILTER_V1
  - WICK_PLAY_CONTEXTUAL_ENTRY_V1
  - TREND_KNOCKOUT_RECOVERY_V1
PINE_NOW: NO
WIKI_NOTE: YES
DUPLICATE_STATUS: REQUIRES_REPO_CHECK
BLACKLIST_STATUS: REQUIRES_REPO_CHECK
```
