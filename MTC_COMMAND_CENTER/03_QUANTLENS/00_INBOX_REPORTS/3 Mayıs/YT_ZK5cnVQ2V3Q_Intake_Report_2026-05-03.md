# QuantLens Transcript Intake Report

## 1. Metadata

- Source Title: The Market Wizard Trading System
- Source URL: https://www.youtube.com/watch?v=ZK5cnVQ2V3Q
- Original URL: https://youtu.be/ZK5cnVQ2V3Q?si=7cL8AhQdK6X5Q_fg
- Video ID: `ZK5cnVQ2V3Q`
- Speaker / Main Trader: David Ryan
- Channel: TraderLion / UNKNOWN_CHANNEL in repo context
- Intake Date: 2026-05-03
- Transcript File: `The Market Wizard Trading System.md`
- Transcript SHA256: `a602938ecc2c9fc731ae4c6a045532ac68c3a8e51a2290e0230b4d1e3583983c`
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
- Main Candidate ID Suggestion: `YT_DAVID_RYAN_MAJORITY_BASE_BREAKOUT_V1`
- Secondary Module Candidate: `ANTS_ACCUMULATION_FILTER_V1`

### Decision Rationale

This transcript is not merely motivational or wiki-only. It contains a repeatable, partly mechanical growth-stock breakout process:

1. Search for strong stocks in clear uptrends.
2. Prefer longer bases / consolidations, not short shallow setups.
3. Use the “majority of the base” line as the breakout/buy point rather than overcomplicating pattern labels.
4. Avoid extended buys.
5. Require or strongly prefer RS-line confirmation.
6. Check CANSLIM-style fundamentals: earnings, sales, institutional sponsorship, group strength.
7. Start small, add only after confirmation, and never add to losers.
8. Use ANTS-style institutional accumulation as a possible leader filter.
9. Reduce size after multiple failed trades or negative market feedback.

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

If `video_id = ZK5cnVQ2V3Q` already exists, Codex must stop and return previous candidate/status/folder information without creating a duplicate.

### Channel Quality Decision

- Current chat-only decision: `UNKNOWN_CHANNEL`
- Blacklist action: `NO_BLACKLIST_DECISION`
- Reason: Channel registry not available here.

---

## 4. Strategy Extraction Summary

### Core Thesis

David Ryan describes a CANSLIM-style market leader breakout system refined around buying at the correct base breakout point, avoiding extended entries, confirming leadership through relative strength, and compounding only into positions that work immediately.

The most codable edge is not a generic “buy growth stocks” idea. It is the combination of:

```text
uptrend + base/tightness + majority-of-base breakout + RS line confirmation + strong fundamentals + group/theme confirmation + add-only-if-profit
```

---

## 5. Candidate Strategy: `YT_DAVID_RYAN_MAJORITY_BASE_BREAKOUT_V1`

### 5.1 Universe Filter

Candidate universe should initially be U.S. equities only.

Recommended first-pass filters:

```text
price > 15 or 20
avg_dollar_volume_20d > minimum threshold
avg_volume_20d > minimum threshold
market_cap optional
exclude illiquid microcaps
```

For clean testing, do not start with crypto or futures. This transcript is stock-specific.

### 5.2 Fundamental / CANSLIM-Inspired Filters

Codex should treat these as optional feature flags because fundamentals may not be available in the first research dataset.

Suggested filters:

```text
eps_growth_qoq > threshold
sales_growth_qoq > threshold
earnings_acceleration optional
institutional_sponsorship_trend >= neutral
industry_group_rank <= threshold
new_high_proximity true
```

If fundamentals are unavailable, create a price-only prototype first, then add fundamentals as enrichment.

### 5.3 Technical Trend Filter

Long-only candidate should require:

```text
close > sma50
close > sma200
sma50 slope > 0
sma200 slope >= 0 or close materially above sma200
price within X% of 52-week high
relative_strength_line trend positive
```

Potential implementation:

```python
sma50 = close.rolling(50).mean()
sma200 = close.rolling(200).mean()
sma50_slope = sma50 - sma50.shift(10)
sma200_slope = sma200 - sma200.shift(20)
```

### 5.4 Base / Consolidation Detection

The transcript emphasizes longer bases and price tightness.

Initial mechanical base detector:

```text
lookback window: 25-90 bars
base_depth_pct <= configurable max, e.g. 35%
base_duration >= configurable min, e.g. 25 bars
price has gone sideways after prior uptrend
volatility contraction preferred
recent close near upper half of base
```

Potential base range:

```python
base_high = high.rolling(base_len).max()
base_low = low.rolling(base_len).min()
base_depth = (base_high - base_low) / base_high
```

### 5.5 Majority-of-Base Buy Point

This is the most distinctive candidate rule.

Instead of using only the highest high of the base, define the buy point as the resistance line that caps the majority of base price action.

Approximation ideas:

#### Option A — Percentile resistance
```python
majority_base_line = high_in_base.quantile(0.90)
entry_trigger = close > majority_base_line
```

#### Option B — Clustered resistance
Find the price level where approximately 80-90% of base highs are below it.

```text
majority_base_line = 90th percentile of highs during base window
buy when price breaks above majority_base_line by buffer
```

#### Option C — Pivot with overhead-supply guard
```text
buy point = max(highs where at least 80-90% of base bars are below)
reject if too much overhead supply remains within next 3-5%
```

This should be compared against classic highest-high breakout.

### 5.6 Avoid Extended Entries

Ryan’s key mistake was buying extended stocks; his correction was buying exactly at/near the buy point.

Suggested rule:

```text
entry_extension_pct = (entry_price / majority_base_line - 1)
allow only if entry_extension_pct <= 2-3%
```

Config idea:

```yaml
max_entry_extension_pct: [1.0, 2.0, 3.0, 5.0]
```

### 5.7 Relative Strength Line Confirmation

Do not rely only on a 12-month RS rating because a stock can still have a high RS rating after a large correction. Use the RS line directly.

Suggested RS line:

```python
rs_line = stock_close / benchmark_close
```

Filters:

```text
rs_line > rs_line_sma20
rs_line near 52-week high
rs_line making new high before or with price breakout
no bearish divergence: price new high while rs_line lower high
```

Candidate options:

```yaml
rs_confirm_mode:
  - off
  - rs_line_above_sma
  - rs_line_20d_high
  - rs_line_52w_high_before_price
  - no_rs_divergence
```

### 5.8 Volume Confirmation

The transcript repeatedly connects large winners to visible institutional demand.

Initial filters:

```text
breakout volume > avg_volume_50d * 1.2
or breakout dollar volume > avg_dollar_volume_50d * 1.2
volume dry-up in base optional
```

More advanced:

```text
up_volume_days in base > down_volume_days
accumulation/distribution score positive
```

---

## 6. Secondary Candidate: `ANTS_ACCUMULATION_FILTER_V1`

Ryan describes an ANTS-style institutional accumulation idea.

### 6.1 Raw ANTS Criteria

A stock may be under strong institutional accumulation if:

```text
up days >= 12 out of last 15 trading days
price gain over 15 days >= 25%
volume increase over same period >= 25%
```

### 6.2 Important Warning

ANTS can appear near:

1. Beginning of a large move.
2. End of an extended/climactic move.

Therefore, ANTS should not be used as a blind entry signal.

### 6.3 Safer First Implementation

Use ANTS as a filter / regime label only:

```text
ANTS_ACCUMULATION = true if criteria met after fresh base breakout and not too extended
ANTS_CLIMAX_RISK = true if criteria met after long prior advance and price is extended from sma50/sma200
```

Suggested features:

```python
up_days_15 = (close > close.shift(1)).rolling(15).sum()
price_gain_15 = close / close.shift(15) - 1
volume_gain_15 = volume.rolling(15).mean() / volume.shift(15).rolling(15).mean() - 1
```

Prototype flags:

```text
ants_accumulation_filter
ants_climax_warning
```

---

## 7. Position Management Rules

### 7.1 Initial Position

Ryan discusses starting with small-to-moderate initial exposure and scaling only if the trade confirms.

Suggested prototype:

```text
initial_position_pct = 2.5% to 5%
add_1_pct = up to 10% if same-day or next-day confirmation
add only if position is profitable
never add to losing position
```

### 7.2 Add Rules

Possible add triggers:

```text
entry day closes strong
next day follows through
price remains above breakout line
RS line confirms
volume remains constructive
new base forms and breaks out again
```

### 7.3 No Add to Losers

Hard rule:

```text
if unrealized_pnl <= 0:
    block_add = true
```

### 7.4 Fast Feedback Rule

Ryan expects correct trades to work quickly.

Codable proxy:

```text
if bars_since_entry <= N and trade does not move at least M% or M*ATR in favor:
    no_add
    optionally reduce or exit
```

Do not make this too strict in first prototype. Start with “no add” only, not forced exit.

---

## 8. Exit / Risk Rules

The transcript gives less mechanical sell rules than buy rules, so first prototype should use conservative generic exits.

Suggested first-pass exits:

```text
initial stop below base/pivot low or recent swing low
max loss guard: 7-8% from entry
sell/reduce if breakout fails back into base
sell/reduce if close below sma50 or sma10w
sell/reduce if RS line breaks down materially
take partial if stock stalls after sharp advance
```

MTC_V2 can later map this into:

```text
INITIAL_SL
TIME_STOP
TRAIL
FILTER_BLOCK exit
OPP_SIGNAL not needed initially
```

---

## 9. Market / Sector Context

The video highlights group rotation and group strength.

Suggested implementation:

```text
benchmark trend: SPY/QQQ above 50/200 or market regime filter
sector/group relative strength positive
stock belongs to leading group
avoid buying if broad growth regime is deteriorating
```

If sector data is hard, use ETF proxy mapping later.

---

## 10. Python Prototype Plan

### Phase 1 — Price-Only Prototype

Implement:

```text
universe filter
SMA50/SMA200 trend
base detector
majority-of-base breakout
entry extension guard
RS line vs benchmark
basic volume confirmation
simple stop/exit
```

### Phase 2 — ANTS Filter

Add:

```text
ANTS accumulation flag
ANTS climax-risk flag
test with and without ANTS
```

### Phase 3 — Fundamental Enrichment

Add:

```text
EPS growth
sales growth
institutional sponsorship proxy
group strength
earnings date exclusion
```

### Phase 4 — Portfolio Simulation

Add:

```text
position sizing
pyramiding only winners
max positions
market regime exposure scaling
```

---

## 11. MTC_V2 Mapping

### Signal Producer

Potential producer:

```text
Producer_DavidRyanMajorityBaseBreakout
```

Outputs:

```text
raw_long_pulse
base_high
base_low
majority_base_line
entry_extension_pct
rs_confirmed
volume_confirmed
ants_flag
```

### Signal Transform

Useful transform:

```text
confirmation after breakout close
optional retest of breakout line
```

### Entry Gates

Relevant gates:

```text
MA trend gate
RS line gate
volume gate
market regime gate
sector/group strength gate
earnings blackout gate
chase/extension guard
```

### Position Manager

Relevant controls:

```text
allow pyramiding only if unrealized_pnl > 0
max entries per symbol
cooldown after failed breakout
reduce size after loss streak
```

### Exit Rules

Relevant exits:

```text
INITIAL_SL below base/swing low
TRAIL below 50SMA/10WMA or swing low
TIME_STOP if no follow-through
FILTER_BLOCK if RS or market regime deteriorates
```

---

## 12. Backtest Cautions

- Avoid survivorship bias in U.S. equities universe.
- Fundamental data availability may distort results if point-in-time data is not available.
- RS line requires a benchmark series aligned by date.
- Earnings date handling matters because Ryan avoids some earnings-adjacent entries.
- Majority-of-base line detection can overfit if tuned too tightly.
- ANTS can mark both accumulation and climax; do not treat it as a standalone buy signal.
- This is a stock strategy; direct transfer to crypto/perpetual futures is not assumed.

---

## 13. Trader Wiki Note

Suggested wiki path:

```text
11_TRADER_WIKI/04_SYSTEM_DEVELOPMENT/TW_2026-05-03_DAVID_RYAN_MARKET_WIZARD_SYSTEM.md
```

### Key Lessons

- Do not buy extended stocks.
- Master one setup before mixing styles.
- The RS line is often more informative than the RS rating.
- Add only to profitable trades.
- Study mistakes with chart screenshots.
- Reduce size after several failed trades.
- Weekly charts reduce noise.
- Institutional accumulation at the start of a move can produce the biggest winners.

---

## 14. Files To Create In Repo

Suggested candidate folder:

```text
06_QUANTLENS_LAB/strategy_candidates/YT_DAVID_RYAN_MAJORITY_BASE_BREAKOUT_V1/
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

Suggested wiki file:

```text
11_TRADER_WIKI/04_SYSTEM_DEVELOPMENT/TW_2026-05-03_DAVID_RYAN_MARKET_WIZARD_SYSTEM.md
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
1. Check duplicate registry for video_id ZK5cnVQ2V3Q and transcript hash.
2. If not duplicate, create candidate folder YT_DAVID_RYAN_MAJORITY_BASE_BREAKOUT_V1.
3. Create candidate_spec.md and rules.yaml only.
4. Create secondary ANTS_ACCUMULATION_FILTER_V1 notes as optional module.
5. Do not code Pine.
6. Do not run backtest yet.
7. Prepare Python prototype task plan for later review.
```

---

## 17. Final Verdict

```text
VERDICT: CANDIDATE
CODEX_STATUS: READY_FOR_PYTHON_PROTOTYPE
PRIMARY_CANDIDATE: YT_DAVID_RYAN_MAJORITY_BASE_BREAKOUT_V1
SECONDARY_MODULE: ANTS_ACCUMULATION_FILTER_V1
PINE_NOW: NO
WIKI_NOTE: YES
DUPLICATE_STATUS: REQUIRES_REPO_CHECK
BLACKLIST_STATUS: REQUIRES_REPO_CHECK
```
