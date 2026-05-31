# QuantLens Transcript Intake Report — 004

## 1. Metadata

- **Report ID:** QL_INTAKE_004
- **Candidate ID:** `QL_CAND_004_Nq-p7Bu1YT0`
- **Source URL:** https://youtu.be/Nq-p7Bu1YT0?si=jA26J6RGZtMXyY4v
- **Normalized URL:** https://www.youtube.com/watch?v=Nq-p7Bu1YT0
- **Video ID:** `Nq-p7Bu1YT0`
- **Title:** `How A Day Trader Turned into a Super-Performance Swing Trader - Real Simple Ariel`
- **Speaker / Trader:** Ariel Hernandez / Real Simple Ariel, inferred from transcript
- **Host / Show:** Richard Moglen / TraderLion-style interview inferred from transcript
- **Channel:** `UNKNOWN_CHANNEL` for registry purposes because channel id is not provided in the transcript file
- **Transcript File:** `How A Day Trader Turned into a Super-Performance Swing Trader - Real Simple Ariel.md`
- **Prompt File:** `00_quantlens_transcript_intake_prompt.md`
- **Generated At:** 2026-05-03
- **Transcript Hash SHA256:** `49e27765d2616d6d8ff6dedd54106015395916e70c112821787058768f443f8d`
- **Transcript Hash Short:** `49e27765d2616d6d`

---

## 2. Intake Verdict

- **Classification:** `CANDIDATE`
- **Codex Status Recommendation:** `READY_FOR_PYTHON_PROTOTYPE`
- **Usefulness Score:** `9 / 10`
- **Confidence:** `HIGH`
- **Primary Category:** Relative-strength swing trading / leading-group momentum
- **Secondary Categories:**
  - Undercut-and-rally entries
  - Higher-low / flat-pivot entries
  - Earnings gap-up / high-volume close entries
  - Follow-through-day market regime confirmation
  - Relative strength during market pullbacks
  - Leading group and sympathy-play rotation
  - Fast de-risking and small-loss discipline
  - Swing-to-position trade transition
  - Short-side optionality in distribution regimes

### Decision

This transcript should be treated as a **strategy candidate**. It contains several codeable setup modules and risk-management rules, especially around:

1. tracking relative strength during market weakness,
2. entering only when the market starts to confirm upward,
3. buying prior-day-high / horizontal pivot breakouts,
4. using low-of-day or prior-day-low technical stops,
5. sizing by account-risk and ADR/stop distance,
6. de-risking within the first few days,
7. converting a swing trade into a position trade only after the stock proves itself,
8. avoiding favorite-stock bias by prioritizing leading groups.

This is **not Pine-ready yet**. The correct next step is to build one or more Python prototype modules and validate event traces on historical OHLCV data. No production runner, MTC_V2 Pine file, backtest, optimization, large CSV, or data bundle should be changed at this intake stage.

---

## 3. Duplicate / Registry Check

### Available Check

- Current uploaded-session duplicate by video ID: **not detected**
- Current uploaded-session duplicate by title: **not detected**
- Similarity with intake report 001: shares Minervini/O'Neil lineage, but **not duplicate**
- Similarity with intake report 002: shares swing-trading/risk-management theme, but **not duplicate**
- Similarity with intake report 003: shares aggressive swing/leader-group concepts, but **not duplicate**
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
Nq-p7Bu1YT0,https://www.youtube.com/watch?v=Nq-p7Bu1YT0,How A Day Trader Turned into a Super-Performance Swing Trader - Real Simple Ariel,UNKNOWN_CHANNEL,CANDIDATE,QL_CAND_004_Nq-p7Bu1YT0,49e27765d2616d6d8ff6dedd54106015395916e70c112821787058768f443f8d,2026-05-03,2026-05-03,1
```

---

## 4. Channel Quality Assessment

- **Channel ID:** `UNKNOWN_CHANNEL`
- **Blacklist Decision:** no blacklist decision can be made from this transcript alone
- **Quality State Recommendation:** `UNKNOWN -> positive evidence`
- **Reason:** The transcript contains concrete process details, risk rules, market regime filters, entry tactics, trade case studies, and failure analysis. It is useful strategy material, not generic motivational content.

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

Ariel Hernandez describes the transition from 2020-2021 day-trading/scalping into a super-performance swing-trading framework. The core process is to trade leading stocks in leading groups, use relative strength as the watchlist filter during market weakness, and enter only after the market and the stock confirm.

The strategy is not a single rigid indicator system. It is a modular discretionary swing system that can be converted into testable prototypes:

1. **Relative-strength watchlist construction:** during market pullbacks, track stocks that resist the decline or quickly reclaim key lows.
2. **Market-regime activation:** avoid trading relative strength while the market is still falling; act only when the market begins pushing higher or follow-through behavior appears.
3. **Entry modules:** undercut-and-rally, higher-low setup, flat-pivot breakout, prior-day-high breakout, 200SMA reclaim, earnings gap-up high-volume close.
4. **Risk module:** low-of-day / prior-day-low stop, max account risk generally around 0.5% per trade, smaller sizing for high-ADR stocks.
5. **Trade management:** de-risk within 3-5 days if the trade works; move worst-case toward flat/breakeven; keep winners if the stock earns the right to become a position trade.
6. **Leadership filter:** do not trade favorite stocks; make leading-group stocks the favorites.

---

## 6. Strategy Candidate Name

Recommended strategy name:

```text
Ariel_RS_LeaderGroup_Swing_v1
```

Alternative names:

```text
RelativeStrength_HVC_Swing_v1
LeaderGroup_UnderCutRally_HVC_v1
Ariel_SwingToPosition_RiskFirst_v1
```

---

## 7. Extracted Strategy Hypothesis

### Core Hypothesis

A swing-trading strategy can achieve asymmetric performance by first identifying stocks that show relative strength during broad-market weakness, then entering when both the stock and market confirm via reclaim, prior-day-high breakout, flat pivot, high-volume close, or higher-low continuation.

The edge is expected to come from the combination of:

```text
market regime confirmation
+ relative strength during weakness
+ leading group participation
+ tight technical entry
+ low-of-day / prior-day-low stop
+ early de-risking
+ letting only proven trades become position trades
```

### Expected Holding Period

- Losers: often same day or less than 24 hours
- Normal winners: around several days to a few weeks
- Strong winners: may extend into position trades if they hold rising 10/20/50-day moving averages and continue showing leadership
- System character: swing trader first, position trader only if the stock proves itself

### Market Universe

Primary intended universe:

- US equities
- Liquid leading stocks
- Stocks above or reclaiming key moving averages, especially 200SMA in transition regimes
- Stocks in leading groups or emerging themes
- Earnings gap-up stocks with strong high-volume close behavior
- High relative-strength stocks during broad-market pullbacks

Recommended first-prototype universe:

```text
US equities, daily OHLCV, minimum price >= 10 or 12 USD, minimum average dollar volume enabled, earnings-gap candidates separated into their own test set
```

---

## 8. Codeable Components

### 8.1 Setup Family A — Market Pullback Relative-Strength Watchlist

Transcript concept:

```text
When the market is going down, do not immediately trade relative strength. Track it. When the market starts pushing higher, then trade the relative-strength names.
```

Candidate detection:

```yaml
setup_type: RS_PULLBACK_WATCHLIST
market_state:
  index_drawdown_from_recent_high: true
  index_below_short_ma_or_breadth_weak: true
stock_relative_strength:
  stock_above_prior_swing_low_while_index_breaks_low: true
  or stock_reclaims_prior_low_faster_than_index: true
  or stock_above_200sma_while_index_below_key_ma: true
  or stock_drawdown_pct < index_drawdown_pct * rs_threshold
watch_only_until:
  market_reclaim_signal: true
```

Possible RS score:

```text
rs_score = weighted_sum(
  stock_return_5d - index_return_5d,
  stock_return_10d - index_return_10d,
  stock_distance_from_200sma,
  stock_reclaim_speed_after_market_low,
  group_relative_strength_rank
)
```

Prototype note:

This component is a **watchlist gate**, not a direct entry trigger.

---

### 8.2 Setup Family B — Undercut and Rally / Reclaim

Examples mentioned: Netflix, Hood, Palantir, Uber, CrowdStrike, Tesla-like relative strength behavior.

Candidate long conditions:

```yaml
setup_type: UNDERCUT_AND_RALLY_RECLAIM
lookback_swing_low: 20-80 bars
condition_1: low < prior_swing_low
condition_2: close > prior_swing_low within N bars
condition_3: stock_rs_score high
condition_4: market no longer in active breakdown
optional_condition: stock reclaims 200sma or 50sma
```

Entry variants:

```text
Variant 1: enter on close reclaiming prior swing low.
Variant 2: enter next day above prior-day high after reclaim.
Variant 3: enter after reclaim + tight inside day / higher-low consolidation.
```

Stop variants:

```text
initial_stop = reclaim_day_low
or initial_stop = prior_day_low
or initial_stop = undercut_low
```

Preferred QuantLens implementation:

Use Variant 2 first because it is less likely to enter while the market is still falling.

---

### 8.3 Setup Family C — Higher-Low / Flat Pivot on Right Side of Base

Transcript concept:

After a valid undercut/reclaim or market bottom attempt, wait for a push, digestion, and a higher-low setup on a flattening or rising moving average.

Candidate long conditions:

```yaml
setup_type: HIGHER_LOW_FLAT_PIVOT
condition_1: stock has recent impulse/reclaim
condition_2: pullback low > prior swing low
condition_3: pullback occurs near rising or flattening 5/10/20/50-day MA
condition_4: narrow range / tight candle appears
condition_5: horizontal pivot is clear
condition_6: breakout above prior-day high or pivot
```

Entry:

```text
long_entry = high > prior_day_high and close/pivot context valid
```

Stop:

```text
initial_stop = low_of_day
or initial_stop = prior_day_low if prior day is tight
```

Preferred filters:

```text
stock above 200SMA unless mega-cap exception
group strength positive
market follow-through or short-term market reclaim present
```

---

### 8.4 Setup Family D — Flat Pivot / Prior-Day-High Breakout

Transcript concept:

Ariel prefers simple horizontal levels over subjective downtrend lines. The entry is usually over prior-day high or a horizontal pivot; below the line is bad, above the line is good.

Candidate long conditions:

```yaml
setup_type: FLAT_PIVOT_PRIOR_DAY_HIGH
pivot_type: horizontal_resistance
pivot_lookback_bars: 3-20
price_tightness: true
stock_above_key_ma: true
group_strength: true
market_confirmed_or_recovering: true
entry_trigger: high > prior_day_high or high > horizontal_pivot
```

Stop:

```text
initial_stop = current_day_low
or initial_stop = previous_day_low if previous day candle is tight
```

Implementation detail:

In Python daily OHLCV, exact intraday entry is not knowable unless intraday data is available. Prototype should support two modes:

```yaml
entry_mode_daily_approx:
  entry_price: max(pivot, prior_high)
  fill_rule: if high >= entry_price then filled
  stop_same_bar_policy: conservative_ohlc_path

entry_mode_intraday_optional:
  timeframe: 5m
  entry: first 5m breakout above pivot/prior-day-high
```

---

### 8.5 Setup Family E — Earnings Gap-Up / High-Volume Close

Transcript concept:

For large earnings gap-up names, he often lets the first day complete and then uses the high-volume close as the key level. Day 2 is traded as good above the HVC level, bad below.

Candidate long conditions:

```yaml
setup_type: EARNINGS_GAP_HIGH_VOLUME_CLOSE
condition_1: gap_up_pct >= min_gap_pct
condition_2: volume >= avg_volume_50 * high_volume_mult
condition_3: close in upper portion of range or constructive close
condition_4: next day trades above high_volume_close_level
condition_5: group or theme strength positive
```

Key level:

```text
hvc_level = close_of_gap_day
```

Entry variants:

```text
Variant 1: next day buy if price reclaims hvc_level from below.
Variant 2: next day buy opening-range breakout while price remains above hvc_level.
Variant 3: daily approximation buy if high > max(opening_range_high, hvc_level).
```

Stop variants:

```text
initial_stop = gap_day_low
or initial_stop = day2_low
or initial_stop = hvc_level - small_buffer
```

Prototype note:

This is one of the most codeable modules in the transcript, but accurate testing is materially better with intraday data.

---

### 8.6 Setup Family F — Leading Group / Birds-of-a-Feather Filter

Transcript concept:

Multiple stocks in the same group moving together validates the theme. The trader should not choose favorite stocks first; instead, make the strongest leading-group stocks the favorites.

Candidate filter:

```yaml
filter_type: LEADING_GROUP_CONFIRMATION
requirements:
  min_group_members_above_20d_high: 2-3
  min_group_members_above_50sma: 3
  group_relative_strength_rank_improving: true
  group_return_10d_vs_market_positive: true
```

Examples from transcript:

```text
cybersecurity group: Rubrik, CrowdStrike, Zscaler, Net, Okta, etc.
space/sympathy theme: AST SpaceMobile leading, Rocket Lab follow-on.
AI/data center theme: CoreWeave influence on related names.
```

Implementation note:

Requires sector/industry/group mapping. If not available, first prototype can approximate by correlation clusters or manually defined symbol baskets.

---

### 8.7 Setup Family G — Sympathy Play / Lead Runner Follow-On

Transcript concept:

Ariel's day-trading background included sympathy plays. In the Rocket Lab example, a lead runner in the same story/theme moved strongly, and he looked for a related stock with constructive setup and prior-day-high breakout.

Candidate conditions:

```yaml
setup_type: SYMPATHY_LEADER_FOLLOW_ON
lead_symbol:
  return_1d_or_5d >= strong_leader_threshold
  volume_expansion: true
follower_symbol:
  same_theme_or_group: true
  constructive_base_or_gap: true
  breaks_prior_day_high: true
  acceptable_risk: true
```

Risk warning:

- Often lower-priced / higher-ADR names.
- Position size must be materially smaller than large-cap liquid leaders.
- Use account-risk sizing and max ADR constraints.

---

### 8.8 Optional Short-Side Module — Weak Stocks During Strong Market

Transcript concept:

When the market is very strong, Ariel begins to focus on the weakest names because he is comfortable playing short if distribution appears.

Candidate short-watchlist conditions:

```yaml
setup_type: WEAKNESS_SHORT_WATCHLIST
market_state: strong_or_extended_uptrend
stock_relative_weakness:
  stock_below_200sma: true
  stock_lagging_index_return: true
  failed_reclaim_or_failed_breakout: true
  below_key_ma_while_market_above_key_ma: true
entry_trigger:
  distribution_day_or_breakdown_below_prior_low: true
```

Recommendation:

Keep this as a **v2 module**. The long-side candidate is stronger and more directly supported by the transcript.

---

## 9. Risk / Position Sizing Rules

### 9.1 Account Risk Cap

Transcript-implied rule:

```text
max_account_risk_per_trade ≈ 0.5% under normal conditions
```

Suggested config:

```yaml
risk:
  max_account_risk_pct: 0.50
  starter_account_risk_pct: 0.10-0.25
  first_trade_after_drawdown_risk_pct: 0.10-0.25
  reduce_size_if_high_adr: true
```

### 9.2 Stop-Based Sizing

Formula:

```text
position_notional_pct = account_risk_pct / stop_distance_pct
```

Example:

```text
If account risk cap = 0.50% and stop distance = 2.00%, max position ≈ 25% of account.
If account risk cap = 0.50% and stop distance = 5.00%, max position ≈ 10% of account.
```

### 9.3 ADR / Volatility Adjustment

Transcript-implied idea:

High-ADR, lower-priced stocks cannot be sized the same as large liquid leaders.

Suggested rule:

```yaml
adr_adjustment:
  if adr_pct > 8:
    max_position_pct: 5-10
  elif adr_pct > 5:
    max_position_pct: 10-15
  else:
    max_position_pct: derived_by_stop_risk
```

### 9.4 Exposure Scaling / Progressive Exposure

Rules:

```yaml
exposure_control:
  start_small_after_market_damage: true
  increase_only_after_open_positions_show_traction: true
  do_not_add_if_current_positions_fail: true
  max_new_positions_per_day: configurable
  max_clicks_or_attempts_per_symbol: configurable
```

A key concept is that exposure is earned by current positions. Do not get bigger until existing trades are working.

---

## 10. Exit / Trade Management Rules

### 10.1 Initial Stop

Primary stops:

```text
low_of_day
prior_day_low if prior day is tight
undercut/reclaim low for U&R setups
HVC day or Day-2 low for earnings gap-up HVC setups
```

### 10.2 Same-Day Failed Breakout Exit

If a stock breaks the pivot intraday but closes weak/red/below pivot, candidate should exit or reduce.

Suggested rule:

```yaml
failed_breakout_exit:
  if entered_today and close < entry_price:
    exit_at_close: true
  if close < pivot_level:
    exit_or_reduce: true
```

### 10.3 De-Risk Within 3-5 Days

Transcript-implied rule:

```text
If a trade moves favorably within the first 3-5 days, improve worst-case scenario.
```

Actions:

```text
sell 1/3 to 1/2 into fast strength
or raise stop from low-of-day to average/breakeven
or both
```

### 10.4 Breakeven / Average Stop After Fast Move

Rule:

```yaml
breakeven_shift:
  if unrealized_gain_pct >= 5-7 within 1-2 days:
    new_stop = entry_avg
```

### 10.5 Trend Hold for Swing-to-Position Transition

A trade may become a position trade only if it continues to hold key moving averages and leadership remains intact.

Suggested logic:

```yaml
swing_to_position:
  require_profit_cushion: true
  hold_if_above_10sma_or_20sma: true
  allow_deeper_hold_to_50sma_for_large_leader: optional
  exit_if_group_leadership_breaks: optional
```

### 10.6 Trim / Partial Profit

Suggested default:

```yaml
partial_profit:
  first_trim_fraction: 0.33-0.50
  trigger_fast_move_pct: 10-20
  trigger_r_multiple: 2-4R
  also_trim_on_distribution_or_extension: true
```

---

## 11. MTC_V2 Mapping

This candidate can map to MTC_V2 as a modular strategy only after Python validation.

### Producer Candidates

```text
PRODUCER_RS_RECLAIM
PRODUCER_FLAT_PIVOT_BREAKOUT
PRODUCER_HVC_EARNINGS_GAP
PRODUCER_HIGHER_LOW_BREAKOUT
PRODUCER_SYMPATHY_FOLLOW_ON
```

### Entry Gates

```text
GATE_MARKET_FOLLOW_THROUGH
GATE_RELATIVE_STRENGTH
GATE_LEADING_GROUP
GATE_ABOVE_200SMA_OR_RECLAIM
GATE_VOLUME_EXPANSION
GATE_ADR_POSITION_CAP
GATE_NO_ACTIVE_MARKET_BREAKDOWN
```

### Position Manager

Useful MTC concepts:

```text
progressive exposure
cooldown after failed breakouts
max attempts per symbol
re-entry allowed after clean reset
portfolio traction gate
```

### Position Sizing

Use MTC position sizing but add candidate-specific constraints:

```text
account_risk_pct <= 0.50
position size derived from technical stop distance
max_position_pct reduced by ADR
starter sizing after drawdown or first signal after correction
```

### Exits

Candidate-specific exits:

```text
LOW_OF_DAY_STOP
PRIOR_DAY_LOW_STOP
FAILED_BREAKOUT_CLOSE_EXIT
BREAKEVEN_AFTER_FAST_MOVE
PARTIAL_PROFIT_FAST_MOVE
MA_TRAIL_10_20_50
GROUP_LEADERSHIP_BREAK_EXIT_OPTIONAL
```

---

## 12. Python Prototype Plan

### Phase 1 — Event Extractor

Create event detections only; do not optimize.

```yaml
events:
  MARKET_FOLLOW_THROUGH_DAY
  STOCK_RELATIVE_STRENGTH_DURING_MARKET_PULLBACK
  UNDERCUT_AND_RECLAIM
  HIGHER_LOW_SETUP
  FLAT_PIVOT_BREAKOUT
  EARNINGS_GAP_HVC
  HVC_DAY2_RECLAIM
  PRIOR_DAY_HIGH_BREAKOUT
  LOW_OF_DAY_STOP_HIT
  FAILED_BREAKOUT_CLOSE
  FAST_MOVE_DERISK_TRIGGER
```

### Phase 2 — Dry Trade Simulator

Rules:

```text
entry at pivot/prior-day-high if high crosses trigger
initial stop set to low-of-day / prior-day-low approximation
conservative same-bar stop handling
partial profit after 2R/3R or fast % move
move stop to breakeven after fast favorable movement
```

### Phase 3 — Scorecard

Metrics:

```text
win rate
average win / average loss
median hold time winners vs losers
max adverse excursion
same-day failure rate
gap risk after entry
group filter contribution
market-regime filter contribution
HVC setup contribution
U&R setup contribution
```

### Phase 4 — Reject/Promote Criteria

Promote if:

```text
positive expectancy before optimization
losses remain small in adverse regimes
market-regime filter improves drawdown
RS filter improves average gain or win rate
HVC or U&R modules show independent edge
```

Reject or downgrade to SALVAGE if:

```text
edge only appears after overfitting
too dependent on unavailable intraday data
same-bar assumptions dominate results
signals are too rare without manual stock selection
high-ADR names create unmanageable gap/stop risk
```

---

## 13. Event Taxonomy Draft

```yaml
event_schema_version: 1
candidate_id: QL_CAND_004_Nq-p7Bu1YT0
source_video_id: Nq-p7Bu1YT0
producer_family: RS_LEADERGROUP_SWING

events:
  - MARKET_PULLBACK_ACTIVE
  - MARKET_FOLLOW_THROUGH_CONFIRMED
  - RS_WATCHLIST_ADD
  - GROUP_LEADERSHIP_CONFIRMED
  - UNDERCUT_RECLAIM_SIGNAL
  - HIGHER_LOW_FLAT_PIVOT_SIGNAL
  - PRIOR_DAY_HIGH_BREAKOUT_SIGNAL
  - EARNINGS_GAP_HVC_SIGNAL
  - HVC_RECLAIM_SIGNAL
  - SYMPATHY_FOLLOW_ON_SIGNAL
  - LOW_OF_DAY_STOP_SET
  - FAILED_BREAKOUT_EXIT
  - FAST_DERISK_PARTIAL
  - STOP_MOVED_TO_AVERAGE
  - SWING_TO_POSITION_ELIGIBLE
  - MA_TRAIL_EXIT
```

---

## 14. Strengths

- Several concrete, codeable setup modules.
- Strong emphasis on market regime and relative strength, not blind breakout buying.
- Clear risk model using stop distance and max account-risk cap.
- Good compatibility with MTC position sizing and exit architecture.
- Good bridge between swing trading and position trading.
- Strong relevance to existing MTC concepts: progressive exposure, risk-first trade management, partial exits, and portfolio feedback.

---

## 15. Weaknesses / Ambiguities

- Some entries rely on intraday 5-minute opening-range context.
- Leading-group detection requires a group/sector mapping dataset or manual baskets.
- Earnings date data is needed for accurate HVC prototype.
- Follow-through day and market-breadth context require index volume and optionally breadth data.
- Short-side process is mentioned but less fully defined than long-side process.
- The system has discretionary components: group judgment, theme recognition, and deciding whether a trade has earned position-trade treatment.

---

## 16. Risky or Suspicious Claims

- The $100k to $3M story appears as historical anecdote and should not be treated as an expected return model.
- 2020-2021 scalping results depended partly on broker liquidity/fill behavior and should **not** be used as a prototype target.
- Some examples are from unusually favorable market environments; prototype must explicitly separate regime effects.
- Lower-priced sympathy plays can produce large percentage gains but require strict position-size caps due to high ADR and gap risk.

---

## 17. Recommended Next Action

### Recommended Codex Next Step

Create a candidate research folder only after real repo duplicate checks:

```text
06_QUANTLENS_LAB/candidates/QL_CAND_004_Nq-p7Bu1YT0_Ariel_RS_LeaderGroup_Swing_v1/
```

Suggested files:

```text
README.md
source_transcript_summary.md
strategy_spec.md
event_taxonomy.yml
prototype_plan.md
risk_model.md
research_notes.md
```

### Do Not Do Yet

```text
Do not edit 01_PINE/MTC_V2.pine.
Do not edit production Python runner files.
Do not run backtests.
Do not run optimization.
Do not create large CSV/data bundles/cache files.
Do not add TradingView alerts.
```

---

## 18. Final Classification

```yaml
classification: CANDIDATE
codex_status: READY_FOR_PYTHON_PROTOTYPE
candidate_id: QL_CAND_004_Nq-p7Bu1YT0
strategy_name: Ariel_RS_LeaderGroup_Swing_v1
usefulness_score: 9
confidence: HIGH
primary_reason: Contains multiple codeable swing-trading modules with clear risk, entry, relative-strength, market-regime, and de-risking logic.
next_action: Build Python event/prototype spec after duplicate and registry checks.
```

---

## 19. Files Created / Not Touched

### Created in this chat

```text
QL_INTAKE_004_Nq_p7Bu1YT0_ariel_rs_leadergroup_swing.md
```

### Not touched

```text
01_PINE/MTC_V2.pine
Production Python runner files
Backtest outputs
Optimization outputs
Registry CSV/YAML files
Secrets / API keys / broker credentials
Large CSV / data bundle / cache files
```
