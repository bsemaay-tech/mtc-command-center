# QuantLens Transcript Intake Report — 002

## 1. Metadata

- **Report ID:** QL_INTAKE_002
- **Candidate ID:** `QL_CAND_002_XOul_ECgHyA`
- **Source URL:** https://youtu.be/XOul-ECgHyA?si=lGRJSk2sTxtqli3v
- **Normalized URL:** https://www.youtube.com/watch?v=XOul-ECgHyA
- **Video ID:** `XOul-ECgHyA`
- **Title:** `100% Returns After Losing it all - Developing a Swing Trading System`
- **Speaker / Trader:** Sean Ryan
- **Host / Show:** Richard Moglen / TraderLion-style interview inferred from transcript
- **Channel:** `UNKNOWN_CHANNEL` for registry purposes because channel id is not provided in the transcript file
- **Transcript File:** `100% Returns After Losing it all - Developing a Swing Trading System.md`
- **Prompt File:** `00_quantlens_transcript_intake_prompt.md`
- **Generated At:** 2026-05-03
- **Transcript Hash SHA256:** `7ee2d1c705303ed78d79d18981ac2d2687bd13a7765ea3b8f356dd31dd1a6d8f`
- **Transcript Hash Short:** `7ee2d1c705303ed7`

---

## 2. Intake Verdict

- **Classification:** `CANDIDATE`
- **Codex Status Recommendation:** `READY_FOR_PYTHON_PROTOTYPE`
- **Usefulness Score:** `9 / 10`
- **Confidence:** `HIGH`
- **Primary Category:** Swing trading / momentum rotation / chart-only breakout system
- **Secondary Categories:**
  - Risk management
  - Position sizing
  - RSI divergence regime and exit filter
  - Breakout / platform / undercut-and-rally entries
  - Add-on position management
  - Post-trade analysis

### Decision

This transcript should be processed as a **strategy candidate**, not only Trader Wiki. It contains a codeable trading framework with identifiable entry logic, stop placement, account-risk sizing, add-on rules, exit triggers, and statistical expectations. It is not immediately Pine-ready, but it is strong enough for a Python prototype and later MTC_V2 integration review.

---

## 3. Duplicate / Registry Check

### Available Check

- Current uploaded-session duplicate by video ID: **not detected**
- Current uploaded-session duplicate by title: **not detected**
- Similarity with intake report 001: related trading school/style, but **not duplicate**
- Existing repo registry `_registry/youtube_video_index.csv`: **not accessible in this chat**
- Existing `channel_blacklist.yaml`: **not accessible in this chat**
- Existing `channel_quality_registry.csv`: **not accessible in this chat**

### Registry Action Recommendation for Codex

Before writing candidate files in repo, Codex should perform the real duplicate check against:

```text
_registry/youtube_video_index.csv
_registry/channel_quality_registry.csv
_registry/channel_blacklist.yaml
```

Suggested index row:

```csv
video_id,normalized_url,title,channel,status,candidate_id,transcript_hash,first_seen_at,last_seen_at,process_count
XOul-ECgHyA,https://www.youtube.com/watch?v=XOul-ECgHyA,100% Returns After Losing it all - Developing a Swing Trading System,UNKNOWN_CHANNEL,CANDIDATE,QL_CAND_002_XOul_ECgHyA,7ee2d1c705303ed78d79d18981ac2d2687bd13a7765ea3b8f356dd31dd1a6d8f,2026-05-03,2026-05-03,1
```

---

## 4. Channel Quality Assessment

- **Channel ID:** `UNKNOWN_CHANNEL`
- **Blacklist Decision:** no blacklist decision can be made from this transcript alone
- **Quality State Recommendation:** `UNKNOWN -> positive evidence`
- **Reason:** The transcript contains specific risk rules, entry/exit examples, statistics, and practical trade-management mechanics.

Suggested channel registry effect if Codex identifies the channel:

```yaml
channel_quality_delta:
  candidate_count: +1
  reject_count: +0
  stop_count: +0
  wiki_count: +0
  recommended_state: GOOD_CANDIDATE_SIGNAL_PENDING_MORE_SAMPLES
```

---

## 5. Short Summary

Sean Ryan describes how he lost most of a $75k account by overleveraging, chasing gaps, averaging down, and trying to make too much money too quickly. He then rebuilt his process around tiny losses, strict account-risk control, chart-based position sizing, repeated attempts on the same setup, and short-term rotation into the strongest two-week to two-month opportunities.

The core system is a discretionary but partially mechanizable swing strategy:

1. Find stocks or ETFs with strong chart structure.
2. Prefer bases, platforms, undercut-and-rally behavior, breakout areas, or major reversal structures.
3. Use the chart to define the stop.
4. Size position so the stop equals no more than 1% of account equity.
5. Add smaller amounts only after sufficient sideways rest and renewed breakout.
6. Exit on reversal days, high-volume exhaustion, RSI divergence, or three clean moves up.
7. Accept low win rate as long as losses are small and winners are allowed to pay for multiple failed attempts.

---

## 6. Strategy Candidate Name

Recommended strategy name:

```text
SeanRyan_ChartRisk_RSI_Divergence_Swing_v1
```

Alternative shorter names:

```text
ChartRiskSwing_v1
RSIDivSwingRotation_v1
SeanRyanSwingRotation_v1
```

---

## 7. Extracted Strategy Hypothesis

### Core Hypothesis

A trader can achieve positive expectancy with a low win rate by trading short-term momentum/base breakouts and reversals while capping each trade's account-level loss to about 1%, re-entering valid setups repeatedly when losses are small, and exiting winners on exhaustion signals.

### Expected Holding Period

- Target holding window: **2 weeks to 2 months**
- Some trades: a few days
- Large trade example: about 1.5 to 2 months
- Not a long-term CANSLIM hold strategy
- Not a day-trading strategy, despite occasional early entries

### Market Universe

Primary intended universe:

- US stocks
- Liquid growth/momentum stocks
- ETFs
- Leveraged ETFs in some examples

For MTC_V2 adaptation:

- Crypto spot/perp symbols can be tested, but the strategy was originally described on equities/ETFs.
- Crypto requires additional filters for 24/7 market, higher noise, funding/slippage, and no earnings/fundamentals.

---

## 8. Codeable Components

### 8.1 Entry Setup Families

The transcript suggests multiple related entry families rather than one single clean setup.

#### A. Small Base / Platform Breakout

Candidate long conditions:

```text
base_detected = sideways compression after prior impulse or after bottoming structure
pivot = highest high of recent base/platform
entry = close or intraday breakout above pivot
volume_confirmation = current volume > recent average volume
```

Potential implementation:

```text
base_window = 5 to 30 bars
base_range_pct <= configurable threshold
pivot = rolling_high(base_window)
entry_long = close > pivot[1] and volume > sma(volume, vol_len) * vol_mult
```

#### B. Undercut-and-Rally / Reclaim

Candidate long conditions:

```text
price undercuts recent support or body lows
price then reclaims support/pivot
RSI divergence may support reversal
entry = reclaim above short-term neckline or prior body-low area
```

Potential implementation:

```text
undercut = low < prior_swing_low
reclaim = close > prior_swing_low or close > neckline
bullish_rsi_div = price lower low and RSI higher low
entry_long = undercut_recently and reclaim and optional bullish_rsi_div
```

#### C. Early Pivot / Reverse Head-and-Shoulders Micro Entry

Transcript describes an early entry before full breakout when a small intraday or short-term reverse head-and-shoulders type structure appears.

For first prototype, treat this as optional and lower confidence.

```text
early_entry = close crosses micro neckline
stop = low of prior day / local structure low
```

#### D. Short Setup: Failed Breakout / Macro Weak Recovery

Short example uses a real estate ETF / inverse leveraged ETF structure:

```text
macro downtrend
weak recovery / wedge / shelf
base breaks upside then reverses on volume
short underlying or long inverse ETF
```

For prototype, implement only after long-side model is stable.

---

### 8.2 Market / Regime Filter

Transcript uses RSI divergence on index/market to decide when to get aggressive or defensive.

#### Bullish Regime Signal

```text
price makes lower low
RSI makes higher low
=> downside momentum weakening; prepare for long stock picking
```

#### Bearish / Exhaustion Signal

```text
price makes higher high or equal high
RSI makes lower high or flat high
=> upside momentum weakening; reduce long aggression or seek shorts
```

Recommended prototype:

```text
market_symbol = SPY/QQQ for equities; BTC/ETH benchmark for crypto tests
rsi_len = 14
div_lookback = 20 to 60 bars
bullish_market_div = lower_low(price) and higher_low(rsi)
bearish_market_div = higher_high(price) and lower_high(rsi)
regime_score:
  +1 if bullish divergence or benchmark above medium MA
  -1 if bearish divergence or benchmark below medium MA
```

For MTC_V2, this maps naturally into:

- `HTF Trend Gate`
- `Momentum Gate`
- `Regime Lock`
- `Filter Block Exit`, if long exposure should be reduced when market divergence turns bearish

---

### 8.3 Position Sizing

This is one of the strongest codeable parts.

Core rule:

```text
max_account_risk_per_trade = 1% of account equity
position_size is determined by chart stop distance
```

Formula:

```text
risk_amount = equity * 0.01
stop_distance_pct = abs(entry_price - stop_price) / entry_price
position_notional = risk_amount / stop_distance_pct
position_pct_of_equity = min(position_notional / equity, max_position_pct)
```

Example from transcript:

```text
If stop distance = 3%
and max account risk = 1%
then position size = 1% / 3% = 33.3% of account
```

Recommended MTC/Python sizing parameters:

```yaml
risk_pct: 1.0
max_position_pct: 75.0
max_total_exposure_pct: 100.0
allow_margin: false
allow_leverage_gt_1: false
stop_source: structure_low_or_pivot_low
```

Important: The speaker sometimes uses 50-75% position sizes and leveraged ETFs, but says he generally does not borrow beyond 100% account exposure. For crypto or leveraged instruments, impose stricter notional caps.

---

### 8.4 Stop Loss

Initial stop sources mentioned or implied:

- Low of previous day
- Body lows around platform
- Support/platform level
- Local structure low
- Breakdown/retrace below breakout area

Prototype stop options:

```text
stop_mode:
  1. previous_day_low
  2. structure_low
  3. platform_body_low
  4. pivot_reclaim_failure
```

Recommended first implementation:

```text
long_stop = min(low[1], recent_structure_low)
short_stop = max(high[1], recent_structure_high)
```

Risk rule:

```text
if calculated account risk > 1%, reduce size or reject trade
```

---

### 8.5 Add-On Rules

Transcript says add-ons are smaller than the first position and only after enough sideways rest.

Rules:

```text
initial_position = largest tranche
add_1 = smaller than initial, often +10% account if initial is ~30%
add_2 = smaller again, often +5%
do not add aggressively far above first buy
require sufficient sideways rest before add
```

Prototype add logic:

```text
can_add = position_open
          and unrealized_profit > 0
          and bars_since_entry >= min_rest_bars
          and recent_range_contracts_or_goes_sideways
          and breakout_above_add_pivot

add_size_pct = min(initial_position_pct * add_fraction, remaining_exposure_cap)
add_fraction schedule:
  add_1: 0.25 to 0.35 of initial notional
  add_2: 0.10 to 0.20 of initial notional
```

Safety for MTC_V2:

- Add-ons must respect `max_entries`
- Add-ons must not reset protective stops incorrectly
- Add-ons should use existing `Position Manager` and `Position Sizing`
- Do not allow same-bar add and exit conflicts unless explicitly modeled

---

### 8.6 Exit Rules

Exit rules are fairly codeable but require prioritization.

#### A. Initial Stop / Structure Failure

```text
exit if price hits initial stop
exit if breakout/reclaim area fails
exit if stock starts going down even slightly after entry and setup no longer acts right
```

#### B. Reversal Day on High Volume

Transcript gives a strong sell example:

```text
price opens/high-trades strongly, then reverses and closes near lows
volume is among highest / materially above average
large gain already achieved
```

Prototype:

```text
reversal_day = high > high[1]
               and close <= low + range * close_near_low_threshold
               and volume > sma(volume, vol_len) * volume_mult
```

Possible thresholds:

```yaml
close_near_low_threshold: 0.25
volume_mult: 1.5
min_profit_for_reversal_exit_pct: 10.0
```

#### C. RSI Bearish Divergence

Exit long when:

```text
price makes higher high
RSI makes lower high or flat high
```

Prototype:

```text
bearish_rsi_div = price_pivot_high_2 > price_pivot_high_1
                  and rsi_pivot_high_2 < rsi_pivot_high_1
```

#### D. Three Clean Moves Up

Exit or reduce when:

```text
stock has completed 3 upward legs from base/bottom
and RSI weakens
and/or volume climaxes
```

This is harder to code deterministically. Treat as second-phase feature after baseline.

#### E. Time Value / Rotation Exit

If initial rapid move is over and position stalls:

```text
exit if no progress after N bars
exit if opportunity cost rises
```

Prototype:

```text
time_stop = bars_in_trade > max_hold_bars and unrealized_profit < min_required_profit
```

---

## 9. Expected Performance Profile

Transcript gives a rare useful statistics section.

Reported stats:

```text
Trades per year: ~577
Trade win rate: ~27%
Average gain per trade: ~5.7%
Average loss per trade: ~3.71%
Stocks traded: 47
Winning stock selections: 21
Stock-selection win rate: ~45%
Annual result discussed: ~150%
```

Important interpretation:

- Low trade win rate is acceptable because failed attempts are cut quickly.
- Same symbol may be tried multiple times before one successful breakout.
- The edge is not “always be right”; the edge is small losses plus occasional large move.
- Candidate likely has high turnover and may be fee/slippage sensitive.

Backtest warning:

```text
A naive backtest may look bad if it does not allow re-entry after small failed attempts.
A naive backtest may overfit RSI divergence pivot logic.
Fees/slippage and spread must be modeled carefully.
```

---

## 10. MTC_V2 Mapping

### Signal Producer

Potential producer:

```text
Producer: ChartRiskSwingBreakout
Raw signals:
  LONG_BREAKOUT_PLATFORM
  LONG_UNDERCUT_RECLAIM
  SHORT_FAILED_BREAKOUT
```

### Signal Transform Pipeline

Useful optional transforms:

```text
confirmation:
  - breakout close confirmation
  - volume confirmation
  - retest/reclaim confirmation

level_retest:
  - prior pivot reclaim
  - platform body low support hold
```

### Entry Gates

Recommended MTC_V2 gates:

```text
- HTF Trend Gate
- Momentum Gate / RSI Divergence Gate
- Volume Gate
- ATR Vol Floor
- ADX / Chop filter
- Session filter only if non-crypto
```

### Position Manager

```text
entry_mode: SIGNAL_PULSE
allow_flip: false for long-only prototype
max_entries: 2 or 3
cooldown_bars: small, because repeated attempts are part of the method
same_bar_reentry_allowed: false initially
```

### Position Sizing

Directly relevant:

```text
risk_pct = 1.0
stop_distance from chart structure
max_position_pct cap
max_total_exposure_pct cap
```

### Exit Rules

```text
1. Protective stop first
2. RSI divergence / reversal-day discretionary exit converted to signal exit
3. Time stop / rotation exit
4. Optional filter-block exit when market regime deteriorates
```

Canonical MTC caution:

```text
Keep exit-first ordering. Do not allow an exhaustion exit and a new same-bar long entry to conflict.
```

---

## 11. Python Prototype Recommendation

### Stage 1 — Long-Only Prototype

Implement only long side first:

```yaml
strategy_id: SeanRyan_ChartRisk_RSI_Divergence_Swing_v1
side: long_only
timeframe: daily first; later 4h/1h for crypto adaptation
universe: equities/ETF if data available; crypto proxy later
entry_families:
  - platform_breakout
  - undercut_reclaim
risk:
  max_account_risk_pct: 1.0
  max_position_pct: 50.0 initially; test 75.0 as aggressive profile
exit:
  - initial_structure_stop
  - high_volume_reversal_day
  - bearish_rsi_divergence
  - time_stop
```

### Stage 2 — Add-On Logic

Add after Stage 1 is stable:

```yaml
adds:
  enabled: true
  max_adds: 2
  add_requires_sideways_rest: true
  add_size_schedule: [0.30, 0.15] # fractions of initial or equity cap, test both
```

### Stage 3 — Short / Inverse ETF Logic

Only after long prototype:

```yaml
short_setup:
  - failed_breakout
  - weak_recovery_after_downtrend
  - bearish_index_rsi_divergence
```

For crypto, short side may map better than inverse ETFs.

---

## 12. Backtest / Optimization Warnings

Do **not** run optimization during intake. For later Codex work:

1. Test baseline rules before parameter search.
2. Separate entry edge from exit edge.
3. Use walk-forward or year-split validation.
4. Include fees, spread, and slippage.
5. Avoid overfitting RSI divergence lookback.
6. Track trade attempts per symbol, not only total trades.
7. Evaluate whether repeated re-entry creates churn on crypto.
8. Compare daily vs 4h vs 1h behavior.
9. Test “no leverage” and “max 100% exposure” variants.
10. Include drawdown duration, not only max drawdown.

---

## 13. Candidate Scorecard

| Dimension | Score | Notes |
|---|---:|---|
| Codeable entry logic | 7/10 | Multiple setup families; needs formalization |
| Codeable exit logic | 8/10 | Reversal day, RSI divergence, stop, time stop can be coded |
| Risk sizing clarity | 10/10 | 1% account risk rule is very clear |
| MTC_V2 fit | 9/10 | Strong fit with sizing, exits, filters, and position manager |
| Anti-repaint feasibility | 8/10 | Use confirmed pivots / bar-close confirmation |
| Overfit risk | 7/10 | RSI divergence and pattern detection can overfit |
| Expected turnover risk | 8/10 | High churn; fees matter |
| Crypto transferability | 6/10 | Needs adaptation; equity examples dominate |
| Overall candidate quality | 9/10 | Strong candidate for prototype |

---

## 14. Risky / Suspicious Claims

These points should not be accepted blindly:

- Reported annual performance and competition results are testimonial, not independently verified inside transcript.
- Leveraged ETF examples can exaggerate returns and drawdowns.
- “Chart-only” style may underperform in regimes where liquidity and macro rotation dominate.
- RSI divergence can be visually convincing but fragile when coded.
- Very low win-rate systems can be psychologically difficult and fee-sensitive.
- High concentration, 50-75% positions, and repeated re-entry may be unsuitable for small illiquid symbols.
- Equity-specific setups may not transfer directly to 24/7 crypto.

---

## 15. Trader Wiki Extraction

Even though this is a `CANDIDATE`, it also contains strong wiki lessons.

Suggested wiki topic:

```text
05_BACKTESTING_AND_OPTIMIZATION / 01_RISK_MANAGEMENT
```

Suggested note title:

```text
TW_2026-05-03_01_RISK_MANAGEMENT_sean_ryan_1pct_account_risk.md
```

Main wiki lessons:

- Account-level risk matters more than raw stop percentage.
- Low win rate can be profitable if average win/loss and position sizing are controlled.
- Repeated failed attempts are acceptable if losses are tiny.
- Do not average down.
- Do not chase large gap-up moves from FOMO.
- Chart-based stop distance should determine position size.
- Public accountability improved discipline for this trader.

---

## 16. Proposed Candidate Folder

Suggested repo location:

```text
06_QUANTLENS_LAB/candidates/QL_CAND_002_XOul_ECgHyA_SeanRyan_ChartRiskSwing/
```

Suggested files Codex may create later:

```text
README.md
intake_report.md
strategy_spec.yaml
prototype_plan.md
event_schema_v1.json
research_notes.md
```

Do **not** create or modify:

```text
01_PINE/MTC_V2.pine
production Python runner files
large data bundles
optimization results
secret/config files
```

---

## 17. Minimal Event Taxonomy Draft

```yaml
events:
  - SETUP_PLATFORM_BREAKOUT
  - SETUP_UNDERCUT_RECLAIM
  - SETUP_FAILED_BREAKOUT_SHORT
  - ENTRY_LONG
  - ENTRY_SHORT
  - ADD_POSITION
  - EXIT_INITIAL_STOP
  - EXIT_REVERSAL_DAY
  - EXIT_RSI_DIVERGENCE
  - EXIT_TIME_STOP
  - EXIT_REGIME_BLOCK
  - NO_TRADE_RISK_TOO_LARGE
  - NO_TRADE_VOLUME_FAIL
  - NO_TRADE_CHOP_FILTER
```

---

## 18. Prototype Parameters Draft

```yaml
strategy:
  id: SeanRyan_ChartRisk_RSI_Divergence_Swing_v1
  timeframe_primary: 1D
  direction: long_only_initial

risk:
  account_risk_pct: 1.0
  max_position_pct: 50.0
  max_total_exposure_pct: 100.0
  allow_leverage: false

entry:
  base_window_min: 5
  base_window_max: 30
  base_range_pct_max: 15.0
  volume_len: 20
  volume_mult: 1.5
  allow_undercut_reclaim: true
  allow_platform_breakout: true

stop:
  mode: structure_low
  fallback_atr_mult: 2.0
  reject_if_stop_distance_pct_gt: 12.0

rsi_divergence:
  enabled: true
  rsi_len: 14
  pivot_left: 3
  pivot_right: 3
  lookback_bars: 60

exits:
  initial_stop: true
  reversal_day: true
  rsi_divergence_exit: true
  time_stop: true
  max_hold_bars: 45
  min_profit_after_max_hold_pct: 5.0

adds:
  enabled: false_initially
  max_adds: 2
  add_requires_rest_bars: 5
  add_size_fraction_schedule: [0.30, 0.15]
```

---

## 19. Final Recommendation

Proceed to **Python prototype planning**, not Pine implementation yet.

Best next Codex instruction:

```text
Create an isolated Python research prototype for QL_CAND_002_XOul_ECgHyA_SeanRyan_ChartRiskSwing.
Do not modify MTC_V2 Pine or production runners.
Implement long-only daily strategy first with:
- platform breakout
- undercut/reclaim
- structure stop
- 1% account-risk sizing
- high-volume reversal-day exit
- RSI divergence exit
- time stop
Produce only spec, prototype module, unit tests, and a no-data dry-run harness.
Do not run optimization.
```

---

## 20. Files Created / Not Touched

### Created in this chat

```text
QL_INTAKE_002_XOul_ECgHyA_sean_ryan_swing_system.md
```

### Not touched

```text
01_PINE/MTC_V2.pine
Production Python runner files
Backtest datasets
Optimization results
Broker/exchange/API configuration
```

---

## 21. Next Action

- Give this report to Codex together with the transcript file.
- Let Codex first check repo registries for duplicates.
- Then create an isolated candidate folder and prototype spec.
- Do not move to Pine until Python behavior and edge hypothesis are reviewed.
