# QuantLens Transcript Intake Report — 003

## 1. Metadata

- **Report ID:** QL_INTAKE_003
- **Candidate ID:** `QL_CAND_003_KWxhLIOchvY`
- **Source URL:** https://youtu.be/KWxhLIOchvY?si=d0XTJw2jmEY699x-
- **Normalized URL:** https://www.youtube.com/watch?v=KWxhLIOchvY
- **Video ID:** `KWxhLIOchvY`
- **Title:** `409% Return in 1 Year Aggressive Swing Trading Tactics and Setups`
- **Speaker / Trader:** Leos Mikulka, inferred from transcript
- **Host / Show:** Richard Moglen / TraderLion-style interview inferred from transcript
- **Channel:** `UNKNOWN_CHANNEL` for registry purposes because channel id is not provided in the transcript file
- **Transcript File:** `409% Return in 1 Year Aggressive Swing Trading Tactics and Setups.md`
- **Prompt File:** `00_quantlens_transcript_intake_prompt.md`
- **Generated At:** 2026-05-03
- **Transcript Hash SHA256:** `ed49638af65fc25ddba4e59c22ed1b830464a4fc91c4b7188b11d5cf88877b43`
- **Transcript Hash Short:** `ed49638af65fc25d`

---

## 2. Intake Verdict

- **Classification:** `CANDIDATE`
- **Codex Status Recommendation:** `READY_FOR_PYTHON_PROTOTYPE`
- **Usefulness Score:** `9 / 10`
- **Confidence:** `HIGH`
- **Primary Category:** Aggressive swing trading / CANSLIM-Minervini style momentum breakout
- **Secondary Categories:**
  - Volatility contraction pattern
  - IPO base breakout
  - Cheat entries / lower-handle entries
  - Theme rotation
  - Risk-multiple trade management
  - Free-rolling and partial-profit logic
  - Portfolio traction based exposure control
  - Revenge-trading failure analysis

### Decision

This transcript should be treated as a **strategy candidate**. It contains multiple concrete, codeable trade-management rules and several annotated trade examples. It is stronger than a pure psychology/wiki transcript because it repeatedly explains exact setup structure, stop distance, risk adjustment, position sizing, add-on logic, partial exits, earnings handling, and failure modes.

This is **not Pine-ready yet**. The correct next step is a Python prototype/specification layer that formalizes the setup families and runs dry validation on historical OHLCV data. No production runner, MTC_V2 Pine file, backtest, or optimization should be modified at this stage.

---

## 3. Duplicate / Registry Check

### Available Check

- Current uploaded-session duplicate by video ID: **not detected**
- Current uploaded-session duplicate by title: **not detected**
- Similarity with intake report 001: related Minervini/CANSLIM lineage, but **not duplicate**
- Similarity with intake report 002: related US Investing Championship / swing trading theme, but **not duplicate**
- Existing repo registry `_registry/youtube_video_index.csv`: **not accessible in this chat**
- Existing `channel_blacklist.yaml`: **not accessible in this chat**
- Existing `channel_quality_registry.csv`: **not accessible in this chat**

### Registry Action Recommendation for Codex

Before creating actual repo candidate files, Codex should perform the real duplicate check against:

```text
_registry/youtube_video_index.csv
_registry/channel_quality_registry.csv
_registry/channel_blacklist.yaml
```

Suggested index row:

```csv
video_id,normalized_url,title,channel,status,candidate_id,transcript_hash,first_seen_at,last_seen_at,process_count
KWxhLIOchvY,https://www.youtube.com/watch?v=KWxhLIOchvY,409% Return in 1 Year Aggressive Swing Trading Tactics and Setups,UNKNOWN_CHANNEL,CANDIDATE,QL_CAND_003_KWxhLIOchvY,ed49638af65fc25ddba4e59c22ed1b830464a4fc91c4b7188b11d5cf88877b43,2026-05-03,2026-05-03,1
```

---

## 4. Channel Quality Assessment

- **Channel ID:** `UNKNOWN_CHANNEL`
- **Blacklist Decision:** no blacklist decision can be made from this transcript alone
- **Quality State Recommendation:** `UNKNOWN -> positive evidence`
- **Reason:** The transcript includes practical chart examples, risk-management rules, position-sizing guidance, and losing-trade postmortems. This is useful strategy material, not generic motivational content.

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

Leos Mikulka explains an aggressive but risk-controlled swing-trading process based on CANSLIM/Minervini-style chart reading. The method focuses on strong technical setups, theme leadership, volume dry-up, breakout pivots, low-risk cheat entries, and active trade management through partial profits and stop tightening.

The transcript has four valuable dimensions:

1. **Winning trade examples:** ARM IPO base, SMR aggressive nuclear-theme setup, BAH clean VCP-style base, LUMN quick tactical trade.
2. **Position management:** free-rolling, moving stops, shaving profits, trailing around 10-day/20-day moving averages, holding earnings only with cushion.
3. **Exposure management:** full size only when recent portfolio traction and watchlist action are good; smaller size from cash or when volatility is high.
4. **Failure analysis:** revenge trading, oversized MSTR/SE positions, widening stops, wedging action into overhead supply, and rule-breaking compounding into portfolio damage.

The strategy is suitable for QuantLens intake because it can be converted into several prototype modules rather than one rigid setup.

---

## 6. Strategy Candidate Name

Recommended strategy name:

```text
LeosMikulka_AggressiveVCP_FreeRollSwing_v1
```

Alternative shorter names:

```text
AggressiveVCP_FreeRoll_v1
ThemeVCP_CheatEntrySwing_v1
PortfolioTractionSwing_v1
```

---

## 7. Extracted Strategy Hypothesis

### Core Hypothesis

A high-return swing strategy can be built by trading a small number of high-quality technical bases and theme leaders with tight initial risk, then aggressively managing open risk using partial profits, raised stops, and portfolio traction feedback.

The edge is not only in the entry pattern. The transcript repeatedly implies that the edge comes from the combination of:

```text
setup quality + low-risk entry + stop discipline + risk multiple management + exposure scaling by traction
```

### Expected Holding Period

- Some trades: 1 to 3 days
- Typical swing: several days to several weeks
- Large winners: can be held through base continuation, earnings, or 10-day/20-day trend if enough cushion exists
- Not a pure day-trading system
- Not a long-term passive trend-following system

### Market Universe

Primary intended universe:

- US stocks
- IPO leaders
- Liquid momentum stocks
- Theme leaders such as AI, nuclear, quantum, semiconductors, etc.
- Some low-price exceptions, but default filter should avoid very low-priced illiquid names

Recommended first-prototype universe:

```text
US equities, daily OHLCV, minimum price >= 12 USD, minimum average dollar volume filter enabled
```

Exception handling:

```text
allow_low_price_exception = true only if theme_strength and liquidity are high
```

For crypto adaptation:

- The setup logic can be tested on crypto, but the original examples are equity-specific.
- Earnings handling does not apply to crypto.
- Volume interpretation differs because crypto venues are fragmented.
- 24/7 session structure changes moving-average and gap behavior.

---

## 8. Codeable Components

### 8.1 Setup Family A — IPO Base Breakout

Example in transcript: ARM.

Candidate long conditions:

```text
recent_ipo_or_young_leader = true
price forms base after IPO move
clear overhead resistance exists
handle or tight contraction forms below resistance
volume dries up into handle
breakout occurs through pivot/resistance
breakout volume expands materially above average
initial stop distance ideally 3% to 7%
```

Suggested implementation fields:

```yaml
setup_type: IPO_BASE_BREAKOUT
base_lookback_bars: 20-80
handle_lookback_bars: 3-15
pivot: max_high(handle_or_base_window)
volume_dryup: handle_avg_volume < base_avg_volume * dryup_threshold
breakout_volume: current_volume > volume_sma_50 * breakout_vol_mult
max_initial_stop_pct: 7
preferred_initial_stop_pct: 3-5
```

Entry concept:

```text
long_entry = close > pivot and breakout_volume and acceptable_risk
```

Alternative entry:

```text
long_entry = intraday/next-day reclaim through previous day high after opening inside range
```

---

### 8.2 Setup Family B — Cheat Entry / Lower Handle Entry

Examples in transcript: SMR and lower handle below/near the 50-day moving average.

Core logic:

```text
price forms a lower handle or tight area below major resistance or near moving average
volume dries up in the handle
next day opens inside range and starts crossing previous day high
entry occurs before full breakout to reduce stop distance
```

Important risk note:

- If full handle risk is around 13%, the transcript says there is **no way** to enter full size at that wide risk.
- A reduced-size cheat entry can be considered only when the stock opens inside and crosses through a tighter trigger with a much tighter stop.

Suggested implementation:

```yaml
setup_type: CHEAT_ENTRY_LOWER_HANDLE
trigger: high > prior_day_high
entry_reference: prior_day_high or local micro-pivot
stop_reference: handle_low or intraday structure low
max_full_setup_risk_pct: 7
wide_risk_reject_threshold_pct: 10-13
reduced_size_when_wide: true
reduced_position_factor: 0.50
```

Entry rule:

```text
if setup_risk_pct > wide_risk_reject_threshold:
    reject_full_size_entry
    allow_reduced_entry only if micro_stop_pct <= 5
```

---

### 8.3 Setup Family C — Clean VCP / Symmetrical Base

Example in transcript: BAH.

Candidate conditions:

```text
prior gap or impulse
base forms with symmetry
shakeout occurs and is met by buying
supply dries up near resistance
proper handle forms on top of main supply/resistance area
breakout occurs with volume expansion around 40% above average
stop can be very tight, around 2% to 3%
```

Suggested implementation:

```yaml
setup_type: CLEAN_VCP_BASE
contractions_required: 2-4
base_symmetry_required: optional
handle_volume_dryup_required: true
shakeout_required: optional_positive
breakout_volume_mult: 1.4
max_stop_pct: 5
ideal_stop_pct: 2-3
```

---

### 8.4 Setup Family D — Pullback / Moving-Average Support Entry

Examples in transcript: LUMN 50-day touch, SMR 10-day pullback touch, CPNG 20-day touch.

Candidate long conditions:

```text
stock is already in an uptrend or recent leader behavior exists
price pulls back to 10-day, 20-day, or 50-day moving average
support is visible near moving average or prior demand area
entry occurs when price starts reclaiming from support
risk is defined by support low
```

Suggested implementation:

```yaml
setup_type: MA_SUPPORT_PULLBACK
allowed_ma: [10, 20, 50]
trend_filter: close > sma_50 or sma_50 rising
support_confirmation: close > ma or reclaim of prior support
stop_reference: recent_low_below_ma
max_stop_pct: 6
```

Risk caveat:

- Lower-quality bases and low-priced names require faster de-risking.
- These should be tagged as **aggressive entries**, not primary high-confidence breakouts.

---

## 9. Position Sizing and Risk Rules

### 9.1 Full Position Size

The transcript gives the following sizing logic:

```text
If full traction exists and setup risk is acceptable, full position may be around 25% of account.
```

Recommended prototype rule:

```yaml
base_position_pct: 25
```

But this should only be allowed when:

```text
recent portfolio traction is positive
watchlist is acting well
setup quality is high
stop distance is acceptable
market tape is favorable
```

### 9.2 Reduced Starting Size

If starting from cash or market/watchlist traction is not strong:

```text
start position may be around 6% of account
```

Prototype rule:

```yaml
starter_position_pct: 6
```

### 9.3 High-Volatility / Wide-Risk Setup Size

For volatile names where a normal setup stop is too wide:

```text
full size rejected
reduced size may be half of normal size, e.g. 12.5% instead of 25%
```

Prototype rule:

```yaml
reduced_position_pct: 12.5
```

### 9.4 Account Risk

Unlike transcript 002, this transcript discusses stop percentage and position percentage more than a universal account-risk cap. For QuantLens compatibility, account risk should still be calculated explicitly:

```text
account_risk_pct = position_pct * stop_pct
```

Examples:

```text
25% position with 5% stop = 1.25% account risk
12.5% position with 5% stop = 0.625% account risk
6% position with 5% stop = 0.30% account risk
```

Recommended first prototype cap:

```yaml
max_account_risk_per_trade_pct: 1.25
soft_target_account_risk_pct: 0.30-1.00
```

---

## 10. Free-Roll / De-Risking Logic

The transcript clearly defines “free rolling” as de-risking through one or more of:

1. moving stops higher,
2. staggering stops,
3. shaving partial profits,
4. reducing worst-case outcome so a stopped trade is break-even or better.

### 10.1 Free-Roll Trigger

Potential trigger:

```text
when unrealized R >= 1.5R to 2R
```

Transcript-specific behavior:

- If a breakout acts well, stops can be moved quickly.
- In ARM, stop moved to around 1.5% after strong action.
- First profits were taken around roughly 3R in one example.

Suggested implementation:

```yaml
freeroll_enabled: true
freeroll_trigger_r: 1.5
partial_profit_trigger_r: 2.0
first_partial_pct: 25
move_stop_to: breakeven_or_structure
```

### 10.2 Partial Profit Logic

General rules from transcript:

```text
sell into strength after at least 2R when possible
peel 25% to 33% pieces on climactic or extended action
sometimes leave 2% to 3% tracking position to keep contact with name
```

Suggested implementation:

```yaml
partial_profit_rules:
  - trigger: r_multiple >= 2
    sell_pct: 25
  - trigger: climactic_extension
    sell_pct: 25-33
  - trigger: high_volume_reversal
    sell_pct: 50-100 depending on severity
  - optional_runner_pct: 2-3
```

---

## 11. Stop and Exit Rules

### 11.1 Initial Stop

Stop reference candidates:

```text
handle low
prior day low
local pullback low
moving-average support low
body lows under support
```

Reject rule:

```text
If required stop is too wide, reject full position.
```

Suggested values:

```yaml
ideal_stop_pct: 2-5
acceptable_stop_pct: 3-7
wide_stop_warning_pct: 8-10
wide_stop_reject_pct: 10-13
```

### 11.2 Trailing Stops

The transcript repeatedly references:

```text
10-day moving average break
20-day moving average break
trailing along key points / technical areas
```

Suggested prototype:

```yaml
trail_stop_modes:
  - structure_low
  - sma_10_close_break
  - sma_20_close_break
```

Initial prototype should avoid too many simultaneous stop owners. For MTC_V2 parity discipline, use one canonical stop basket with deterministic precedence.

### 11.3 Sell Into Strength

Triggers:

```text
climactic run
large extension from pivot
big intraday reversal
break of low after strong breakout day
high-volume reversal
multiple days of acceleration
approaching earnings without enough cushion
```

Suggested implementation:

```yaml
sell_strength_triggers:
  min_r_before_strength_sell: 2.0
  daily_gain_extension_pct: configurable
  intraday_reversal_pct: configurable
  volume_spike_mult: 1.5-2.0
```

### 11.4 Failed Breakout / Squat Exit

The losing MSTR example shows a key rule:

```text
If breakout is not working, there is no reason to hold full size overnight.
```

Prototype rule:

```text
failed_breakout = entry_bar_or_next_bar closes below pivot or reverses badly
exit_or_reduce = true
```

Suggested implementation:

```yaml
failed_breakout_exit:
  enabled: true
  lookahead_bars: 1-2
  close_below_pivot: exit_or_reduce
  big_upper_wick_or_reversal: reduce_or_exit
```

---

## 12. Earnings / Binary Event Handling

Transcript rule:

```text
Check implied move before earnings.
Hold only if profit cushion is sufficient.
If implied move is 8% and current cushion is 6%, 10%, or 15%, trader may hold a portion, not necessarily full position.
```

Recommended prototype:

```yaml
earnings_filter:
  enabled_for_equities: true
  hold_through_earnings_only_if_profit_cushion_gt_implied_move: true
  max_position_through_earnings_pct_of_original: 25-50
  no_cushion_action: exit_before_earnings
```

Data caveat:

- Historical earnings calendar and options implied move data may not be available in basic OHLCV datasets.
- First prototype can use a placeholder or disable earnings holding until data exists.

For crypto:

```text
earnings_filter = not applicable
```

---

## 13. Portfolio Exposure / Traction Logic

This is one of the most important parts of the transcript.

### 13.1 Increase Exposure Only When Both Are True

```text
portfolio traction is positive
watchlist action is strong
```

Watchlist action means:

```text
names are finding support
breakouts follow through
themes are working
volume confirms moves
```

Portfolio traction means:

```text
recent trades are working
current positions are profitable or de-risked
stops are not being repeatedly hit
```

Suggested implementation:

```yaml
portfolio_traction_score:
  recent_trades_window: 5-20
  metrics:
    - recent_win_rate
    - avg_r_multiple
    - open_position_unrealized_r
    - stopout_count
    - followthrough_count
```

Exposure mapping:

```yaml
exposure_mode:
  defensive:
    max_position_pct: 6-12.5
    max_total_exposure_pct: 30-50
  normal:
    max_position_pct: 25
    max_total_exposure_pct: 75-100
  aggressive:
    max_position_pct: 25
    max_total_exposure_pct: 100-150
    margin_allowed: true
```

### 13.2 Margin Logic

The transcript allows aggressive intraday exposure, sometimes ramping to 1.5x or 2x, but with end-of-day evaluation.

Prototype rule:

```yaml
margin:
  enabled: false in v1 dry prototype unless explicitly testing aggressive mode
  intraday_only: optional future feature
  hold_overnight_only_if:
    - portfolio_traction_positive
    - watchlist_traction_positive
    - open_positions_de_risked
```

For MTC_V2 integration, margin behavior should be handled by Position Manager / PortfolioState, not by signal logic.

---

## 14. Theme Rotation Logic

The trader repeatedly references themes such as:

```text
nuclear
AI
semiconductors
quantum computing
IPO leadership
```

He identifies themes by doing screening and watching which names are acting well. He warns against style drift and too many unrelated watchlists.

Prototype theme scoring:

```yaml
theme_strength_score:
  group_members_breaking_out: count
  group_members_above_50ma: percentage
  group_members_with_volume_expansion: count
  relative_strength_vs_market: optional
```

First prototype can use a simpler proxy:

```text
sector/theme filter optional; do not block entries in v1 unless reliable metadata exists
```

---

## 15. Bad-Trade Pattern Extraction

The transcript is valuable because it explains losing-trade mechanics. These should become guardrails.

### 15.1 Overhead Supply + Wide Pivot + Wedging Up

Avoid or down-rank setups with:

```text
large overhead resistance
13% pivot risk
wedging up into pivot
increasing selling volume
decreasing buying volume
lagging relative strength
compressed time without enough base repair
```

Guard rule:

```yaml
bad_setup_guard:
  overhead_supply_penalty: high
  wedge_up_penalty: high
  wide_pivot_risk_penalty: high
  selling_volume_penalty: high
```

### 15.2 Revenge Trading Guard

Failure pattern from MSTR/SE:

```text
recent losses -> trader increases size -> ignores failed breakout -> holds overweight through violation -> large account loss
```

Prototype guard:

```yaml
revenge_trading_guard:
  if_recent_drawdown_pct_gt: configurable
  reduce_max_position_size_by: 50-75%
  block_margin: true
  require_clean_setup_score: high
  require_failed_breakout_exit: strict
```

### 15.3 Do Not Increase Size After Losses

Rule:

```text
After losses, decrease size; do not increase size.
```

Implementation:

```yaml
size_after_loss_policy:
  consecutive_losses_2: reduce_position_size_50_percent
  consecutive_losses_3: starter_size_only
  daily_drawdown_limit_hit: no_new_entries
```

---

## 16. MTC_V2 Mapping

### 16.1 Producer Candidate

Recommended new producer family:

```text
producer_vcp_cheat_breakout_v1
```

Subtypes:

```text
IPO_BASE_BREAKOUT
CHEAT_ENTRY_LOWER_HANDLE
CLEAN_VCP_BASE
MA_SUPPORT_PULLBACK
```

### 16.2 Signal Transform Pipeline

Possible transforms:

```text
confirmation = breakout follow-through / close above pivot
level_retest = optional support reclaim after shakeout
```

### 16.3 Entry Gates

Useful existing/future MTC_V2 gates:

```text
MA Trend Gate: close above/rising 50MA/200MA
Volume Gate: breakout volume expansion
ATR/Volatility Gate: avoid too-wide stop setups unless reduced size
Session Gate: not applicable to daily equities unless intraday extension is built
Level Proximity Gate: pivot/resistance/handle proximity
Momentum Gate: relative strength / new high behavior
Chop Gate: avoid messy non-directional action
```

### 16.4 Position Manager

Recommended MTC_V2 integration later:

```text
max_entries and add-ons controlled by Position Manager
allow add-on only after rest/consolidation and existing position de-risked
exposure mode controlled by PortfolioState/traction guard
```

### 16.5 Sizing

Map to existing sizing module:

```text
risk_pct derived from account risk target
stop distance derived from structure stop
position_pct capped by exposure mode
```

Important:

```text
Position sizing must not be hardcoded inside producer.
Producer emits setup and structure stop; sizing layer calculates size.
```

### 16.6 Exit Rules

Map to Exit Rules layer:

```text
protective stop = structure stop / MA trailing stop
partial TP = R-multiple partials
strength exit = climactic/high-volume reversal
failed breakout exit = early reduce/exit
binary event exit = earnings guard, equity-only
```

MTC_V2 parity note:

```text
Use exit-first canonical rule. If failed breakout / stop / partial TP and new signal occur same bar, exit logic owns the bar first.
```

---

## 17. Python Prototype Recommendation

### 17.1 First Prototype Scope

Do **not** try to model every discretionary nuance immediately. Start with three testable variants:

```text
Variant A: Clean VCP / pivot breakout with volume expansion
Variant B: Cheat entry after lower handle / prior-day high reclaim
Variant C: MA support pullback entry with tight stop
```

### 17.2 Required OHLCV Features

```text
sma_10
sma_20
sma_50
sma_200
volume_sma_50
atr_14
rolling_high / rolling_low
base_range_pct
handle_range_pct
volume_dryup_score
breakout_volume_score
structure_stop_pct
r_multiple
```

### 17.3 Suggested Prototype Output Columns

```csv
timestamp,symbol,setup_type,entry_price,stop_price,stop_pct,position_pct,account_risk_pct,pivot,volume_ratio,base_range_pct,setup_score,traction_mode,exit_reason,r_multiple
```

### 17.4 Suggested Setup Score

```yaml
setup_score:
  volume_dryup: 0-2
  breakout_volume: 0-2
  stop_tightness: 0-2
  ma_trend_alignment: 0-2
  overhead_supply_cleanliness: 0-2
  theme_strength_optional: 0-2
```

First acceptance threshold:

```text
setup_score >= 7 / 10 for normal mode
setup_score >= 9 / 10 for aggressive/margin mode
```

---

## 18. Research Value for QuantLens

### Why This Candidate Is Valuable

- It gives practical variants of VCP and cheat entries.
- It explains sizing by stop distance and portfolio traction.
- It has both winners and losers, which is important for robust rule extraction.
- It provides concrete guardrails against revenge trading and wide-risk entries.
- It maps naturally to MTC_V2’s position manager, risk sizing, filter gates, and exit rules.

### Main Weaknesses

- Many entries are discretionary and chart-reading heavy.
- Some examples rely on intraday behavior, but transcript mostly describes daily charts.
- Theme classification requires metadata not always available in OHLCV.
- Earnings implied move requires options data.
- “Free rolling” can be implemented in multiple ways; exact parameters need controlled experiments.

### Risk of Overfitting

High if prototype tries to encode every chart nuance. Moderate if first version limits itself to:

```text
base compression + volume dry-up + pivot breakout + structure stop + R-multiple exits
```

---

## 19. Final Classification Details

```yaml
classification: CANDIDATE
codex_status: READY_FOR_PYTHON_PROTOTYPE
candidate_id: QL_CAND_003_KWxhLIOchvY
strategy_family: Aggressive Swing / VCP / Cheat Entry / Portfolio Traction
wiki_only: false
salvage_only: false
duplicate: false_with_current_session_evidence
blacklist_blocked: false
recommended_next_action: Create Python prototype spec and candidate folder after repo registry duplicate check
```

---

## 20. Files Created / Not Touched

### Created in this Chat

```text
QL_INTAKE_003_KWxhLIOchvY_leos_aggressive_swing_tactics.md
```

### Not Touched

```text
01_PINE/MTC_V2.pine
production Python runner files
backtest outputs
optimization outputs
large CSV/data/cache files
API keys / secrets / broker configuration
```

---

## 21. Next Action for Codex

Recommended Codex instruction:

```text
1. Read this intake report.
2. Check _registry/youtube_video_index.csv for video_id KWxhLIOchvY and transcript_hash ed49638af65fc25ddba4e59c22ed1b830464a4fc91c4b7188b11d5cf88877b43.
3. If not duplicate, create a candidate folder for QL_CAND_003_KWxhLIOchvY.
4. Do not modify 01_PINE/MTC_V2.pine.
5. Do not modify production Python runner files.
6. Do not run backtest or optimization.
7. Draft a Python prototype specification only, focused on:
   - Clean VCP breakout
   - Cheat entry / lower handle prior-day-high reclaim
   - MA support pullback entry
   - Free-roll/partial profit logic
   - Portfolio traction exposure guard
   - Revenge-trading drawdown guard
8. Produce a validation checklist for later backtesting.
```

---

## 22. One-Line Verdict

This is a high-value strategy candidate: extract it as an aggressive VCP/cheat-entry swing system with strict risk-multiple management, portfolio traction exposure control, and explicit anti-revenge-trading guards.
