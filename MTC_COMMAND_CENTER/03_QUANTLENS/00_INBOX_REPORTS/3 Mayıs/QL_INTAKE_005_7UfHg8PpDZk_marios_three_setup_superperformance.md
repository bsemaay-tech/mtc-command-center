# QuantLens Transcript Intake Report — 005

## 1. Metadata

- **Report ID:** QL_INTAKE_005
- **Candidate ID:** `QL_CAND_005_7UfHg8PpDZk`
- **Source URL:** https://youtu.be/7UfHg8PpDZk?si=0mLL1k1aOKmlfSS4
- **Normalized URL:** https://www.youtube.com/watch?v=7UfHg8PpDZk
- **Video ID:** `7UfHg8PpDZk`
- **Title:** `The 3 Powerful Trading Setups of a Top Super-performance Trader`
- **Speaker / Trader:** Marios Stamatoudis, inferred from transcript
- **Host / Show:** Richard Moglen / TraderLion-style interview inferred from transcript
- **Channel:** `UNKNOWN_CHANNEL` for registry purposes because channel id is not provided in the transcript file
- **Transcript File:** `The 3 Powerful Trading Setups of a Top Super-performance Trader.md`
- **Prompt File:** `00_quantlens_transcript_intake_prompt.md`
- **Generated At:** 2026-05-03
- **Transcript Hash SHA256:** `74706875e6d04c7075aea01ffb575765c8862b852f98db6eb29e9f89b92d6e85`
- **Transcript Hash Short:** `74706875e6d04c70`

---

## 2. Intake Verdict

- **Classification:** `CANDIDATE`
- **Codex Status Recommendation:** `READY_FOR_PYTHON_PROTOTYPE`
- **Usefulness Score:** `9 / 10`
- **Confidence:** `HIGH`
- **Primary Category:** Super-performance swing trading / momentum leader breakout system
- **Secondary Categories:**
  - Classic breakout / VCP-style tight consolidation
  - Episodic pivot / catalyst gap / post-earnings drift
  - Parabolic short / exhaustion short
  - Relative-strength momentum leader scan
  - Fundamental catalyst + price/volume confirmation
  - ADR-based partial profit logic
  - Low-of-day stop discipline
  - Small account-risk model
  - Progressive exposure and margin restraint
  - Watchlist breadth / breakout cluster regime detection

### Decision

This transcript should be treated as a **multi-module strategy candidate**. It contains three distinct but related setups:

1. classic momentum-leader breakouts from tight right-side accumulation,
2. episodic pivots / catalyst gaps where fundamentals provide the fuel and price-volume confirms institutional demand,
3. parabolic exhaustion shorts for overextended stocks.

The video is stronger than a generic trading interview because it includes several concrete design elements that can be translated into Python prototype logic:

- one-month / three-month / six-month relative-strength gainers scans,
- dense-volume scan for beaten-down names beginning to emerge,
- bulk list -> focus list workflow,
- premarket catalyst gap scan,
- low-of-day stop logic,
- no red position overnight rule,
- 0.25% to 0.4% account-risk baseline,
- maximum 25% to 30% single-name position target,
- partial profit around 2.5x to 3x ADR movement,
- breakout-cluster / watchlist-health market regime feedback,
- no overnight margin as default.

This is **not Pine-ready yet**. The correct next step is to create Python prototype modules and event traces. No `01_PINE/MTC_V2.pine`, production Python runner, optimization, backtest, large CSV, or data bundle should be changed at this intake stage.

---

## 3. Duplicate / Registry Check

### Available Check

- Current uploaded-session duplicate by video ID: **not detected**
- Current uploaded-session duplicate by title: **not detected**
- Similarity with intake report 001: shares Minervini/O'Neil breakout and risk-management lineage, but **not duplicate**
- Similarity with intake report 002: shares strict small-loss / asymmetric return logic, but **not duplicate**
- Similarity with intake report 003: shares aggressive swing-trading and free-roll add concepts, but **not duplicate**
- Similarity with intake report 004: shares relative-strength and swing-first methodology, but **not duplicate**
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
7UfHg8PpDZk,https://www.youtube.com/watch?v=7UfHg8PpDZk,The 3 Powerful Trading Setups of a Top Super-performance Trader,UNKNOWN_CHANNEL,CANDIDATE,QL_CAND_005_7UfHg8PpDZk,74706875e6d04c7075aea01ffb575765c8862b852f98db6eb29e9f89b92d6e85,2026-05-03,2026-05-03,1
```

---

## 4. Channel Quality Assessment

- **Channel:** `UNKNOWN_CHANNEL`
- **Blacklist decision:** No blacklist decision can be made because channel id is not provided.
- **Quality contribution:** Positive
- **Suggested status contribution:** `CANDIDATE`
- **Reason:** The transcript contains concrete candidate strategy logic and repeatable process details rather than only motivational commentary.

No channel should be marked `BLACKLISTED`, `WATCHLIST`, or `GOOD` from this single transcript alone unless Codex finds prior channel records in the repo registry.

---

## 5. Short Summary

Marios describes his development from blowing up early accounts, reverse-engineering other traders, day trading catalyst names, burning out from high emotional volatility, and then transitioning into swing trading. His current process centers on three setup families:

1. **classic breakout** from tight consolidation in momentum leaders,
2. **episodic pivot / catalyst gap** with strong price-volume confirmation,
3. **parabolic short** on exhaustion after rapid overextension.

His core philosophy is that **fundamentals are the fuel**, but **price action confirms whether the fuel is actually being used by institutions**. He scans for relative-strength leaders, catalyst gappers, volume footprints, and parabolic extensions, then builds a daily focus list. He keeps risk intentionally small so that normal losing streaks do not emotionally or mathematically damage the account.

---

## 6. Strategy Candidate Name

`MARIOS_THREE_SETUP_SUPERPERFORMANCE_ENGINE_V1`

Alternative shorter internal names:

- `MARIOS_BREAKOUT_EP_PARABOLIC_SHORT_V1`
- `THREE_SETUP_MOMENTUM_ENGINE_V1`
- `RS_BREAKOUT_EP_EXHAUSTION_ENGINE_V1`

Recommended candidate folder name:

```text
10_CANDIDATES/QL_CAND_005_7UfHg8PpDZk_marios_three_setup_superperformance/
```

---

## 7. Extracted Strategy Hypothesis

### Core Hypothesis

A high-performance swing system can be built by combining:

1. **momentum-leader breakouts** where a stock has already shown strength, then tightens on the right side of a base,
2. **episodic pivots** where a catalyst causes a gap out of a meaningful range and institutional volume confirms demand,
3. **parabolic exhaustion shorts** where a stock has moved 100% to 200% or more in a short time and prints exhaustion behavior.

The edge is expected to come from:

- supply/demand compression before breakout,
- institutional repricing after catalyst,
- asymmetric upside from a small number of major winners,
- very small account risk per trade,
- fast exit of failed trades,
- regime awareness through watchlist breadth and breakout clusters.

### Expected Holding Period

- **Breakout module:** several days to several weeks; may extend if moving averages are respected.
- **Episodic pivot module:** same day to several weeks depending on follow-through.
- **Parabolic short module:** mostly short-term / tactical; potentially one to several days.
- **Losers:** often intraday or same-day exit; red positions are generally not held overnight.

### Market Universe

Primary universe implied by transcript:

- US-listed stocks,
- liquid names preferred,
- momentum leaders,
- recent IPOs where applicable,
- catalyst gappers,
- beaten-down names with new volume footprints,
- theme names such as AI, crypto, China names, biotech, and other rotating sectors.

---

## 8. Codeable Components

### 8.1 Setup Family A — Classic Momentum Breakout

**Intent:** Capture continuation from tight right-side accumulation after a prior momentum leg.

Candidate rules:

```text
Universe:
- US equities.
- Minimum liquidity filter.
- Relative strength in 1-month, 3-month, or 6-month gainers.
- Optional recent IPO inclusion.

Setup structure:
- Prior momentum leg up.
- Pullback / consolidation on right side.
- Tightening action.
- Higher lows or sideways compression.
- Volume contraction during consolidation.
- Price near resistance / pivot.
- Moving averages supporting the right side, commonly 10/20/50/100/150/200 MA context.

Trigger:
- Breakout through manually or algorithmically detected horizontal/diagonal pivot.
- Prefer volume confirmation.
- Prefer names that are part of broader market theme or group strength.
```

Prototype interpretation:

- Start with simple horizontal pivots and range compression before trying complex trendline detection.
- Add VCP-like contraction logic later.
- Use minimum range contraction and volume dry-up metrics.

### 8.2 Setup Family B — Episodic Pivot / Catalyst Gap

**Intent:** Enter a stock after a major catalyst causes repricing out of an existing range.

Candidate rules:

```text
Premarket scan:
- Gap up > 5%, preferably escaping a multi-month range.
- Catalyst exists:
  - earnings surprise,
  - raised guidance,
  - new CEO / restructuring,
  - FDA approval or biotech event,
  - business model change,
  - major news tied to current market theme.

Fundamental/fuel filter:
- Sales acceleration preferred.
- EPS acceleration or large EPS estimate change useful.
- Big surprise / guidance raise preferred.
- Theme relevance positive.

Price/volume confirmation:
- Gap holds.
- High relative volume.
- Break above prior range or meaningful resistance.
- Institutional footprint visible in volume.

Trigger:
- Intraday entry after confirmation.
- Low-of-day or tighter stop.
- Optional second-day entry for biotech or if first day fails but structure remains valid.
```

Prototype interpretation:

- Use daily OHLCV first.
- If intraday data exists, model 5-minute opening range and low-of-day stop.
- Catalyst text classification may initially be manual / metadata-driven.

### 8.3 Setup Family C — Parabolic Exhaustion Short

**Intent:** Short a stock after an extreme multi-day vertical move when exhaustion criteria appear.

Candidate rules:

```text
Candidate scan:
- Stock has moved > 100% over a short window.
- Prefer 100% to 200%+ moves in a few days.
- IPO / low float / highly shorted / theme stocks may qualify.
- Overextended from moving averages.

Exhaustion trigger:
- Big gap / blow-off behavior.
- Exhaustion day after multiple consecutive up days.
- Large volume.
- Failed continuation or intraday reversal.
- Optional close below key intraday level.

Risk:
- High danger setup.
- Tight stop mandatory.
- Do not average against a parabolic move.
- Retry count limited.
```

Prototype interpretation:

- This module should be isolated from long breakout modules.
- It should be tested separately because short-side borrow, gap risk, and asymmetric upside risk differ from long-side modules.
- This is not the first module to implement unless the research focus specifically includes short-side alpha.

### 8.4 Relative Strength and Momentum Leader Scan

Candidate rules:

```text
Daily scans:
- 1-month gainers.
- 3-month gainers.
- 6-month gainers.
- Weekly gainers.
- Dense volume / volume footprint scan.
- Fresh IPO scan.

Selection:
- Quickly review charts.
- Add promising names to broad "bulk list".
- From bulk list, select tight / near-trigger names for daily focus list.
```

Prototype metrics:

- 20-day return rank.
- 63-day return rank.
- 126-day return rank.
- Dollar volume rank.
- Relative volume vs 20-day / 50-day baseline.
- Distance to 52-week high or recent pivot.
- Compression score.

### 8.5 Focus List / Trigger List Workflow

The transcript describes a two-stage watchlist process:

1. **Bulk list:** all names that look interesting from scans.
2. **Intraday focus list:** names close enough to breakout / trigger that they may be actionable today or tomorrow.

Prototype representation:

```text
BULK_LIST_EVENT:
- ticker
- scan_source
- date_added
- reason_code
- rs_score
- volume_score
- theme_tag

FOCUS_LIST_EVENT:
- ticker
- trigger_level
- setup_family
- stop_reference
- catalyst_flag
- theme_tag
- confidence_score
```

### 8.6 Breakout Cluster / Market Regime Feedback

The transcript says breakouts happen in clusters. This can be converted into a regime filter.

Candidate logic:

```text
Bullish regime confirmation:
- Number of focus-list names increasing.
- More names triggering breakouts.
- More breakouts following through.
- Fewer focus-list names breaking down.
- Current trades providing positive feedback.

Defensive regime:
- Few focus-list names.
- Names fail to trigger.
- Triggered breakouts fail quickly.
- Multiple stop-outs.
- Watchlist deteriorates.
```

Possible metric:

```text
watchlist_health_score =
  + triggered_breakouts
  + followthrough_count
  - failed_breakouts
  - stopped_same_day_count
  + avg_post_trigger_return_3d
```

---

## 9. Risk / Position Sizing Rules

### 9.1 Account Risk Per Trade

The transcript gives a small-risk framework:

```text
Baseline risk per trade: 0.25% to 0.4% of account.
Favorable market / safe existing positions: can increase toward 0.5% to 0.6%.
Avoid 1% risk per trade because 10 consecutive losses are statistically plausible with a 30%-35% win rate.
```

This is highly codeable and should be prioritized.

### 9.2 Max Single-Name Exposure

Candidate rule:

```text
Max single-name position: 25% to 30% of account.
Avoid 50% to 60% position sizes even if stop is tight.
```

This prevents tight-stop sizing from creating oversized concentration.

### 9.3 Stop-Based Position Sizing

Candidate formula:

```text
position_pct = account_risk_pct / stop_distance_pct
position_pct = min(position_pct, max_position_pct)
```

Example:

```text
account_risk_pct = 0.35%
stop_distance_pct = 2.0%
raw_position_pct = 17.5%
max_position_pct = 30%
final_position_pct = 17.5%
```

### 9.4 Low-of-Day Stop

Marios describes replacing wider VCP-last-contraction stops with **low-of-day** or even tighter stops.

Candidate implementation:

```text
For breakout / episodic pivot:
- Initial stop = entry day's low.
- If intraday available, initial stop can be intraday low after entry signal.
- If no intraday data, use daily low approximation.
```

Caveat:

- Daily OHLC backtests can overstate or distort low-of-day stop behavior because entry timing matters.
- For parity-grade testing, intraday data is preferable.

### 9.5 No Red Position Overnight

Candidate guard:

```text
If position unrealized P&L < 0 near close:
    exit before close
```

This is a strong rule and should be prototype-tested separately because it can reduce drawdowns but may also remove valid pullback trades.

### 9.6 Margin / Exposure Rules

Transcript says:

- no overnight margin for most/all of the year,
- intraday margin may be used tactically,
- margin must be earned,
- if open risk is already around 2% to 3%, do not add margin,
- progressive exposure first; let one trade finance the next.

Candidate rule:

```text
overnight_exposure_cap = 100%
intraday_exposure_cap = configurable
if total_open_risk_pct >= 2.0%:
    block_new_margin_entries = true
if watchlist_health_score weak:
    reduce_exposure_cap
```

---

## 10. Exit / Trade Management Rules

### 10.1 Initial Failure Exit

```text
If breakout / EP fails and violates low-of-day stop:
    exit immediately.
```

### 10.2 Move Stop to Breakeven

```text
If trade moves enough in favor:
    stop = max(stop, average_entry_price) for longs
```

This supports asymmetric returns and reduces emotional pressure.

### 10.3 ADR-Based First Partial

Marios describes using ADR to normalize extension:

```text
If favorable move >= 2.5x to 3.0x ADR:
    sell 25% to 33% of position
```

This is better than a fixed percentage target because a 20% move in a high-ADR small cap is not the same as a 20% move in a mega-cap.

### 10.4 Moving Average Trail

Candidate trend-hold logic:

```text
For strong names:
- Respect 10-day MA first.
- If large cushion exists, allow pullback toward 20-day MA.
- Sell / reduce on moving-average violation depending on cushion and action.
```

### 10.5 Free-Roll Adds

When adding:

```text
Only add if new stop on total position can be placed above blended average entry.
Keep total position within 25%-30% max.
Do not turn a winning trade into a risky oversized trade.
```

### 10.6 Retry Limit

Transcript indicates that if an entry fails too many times, he abandons the idea.

Candidate rule:

```text
max_retries_per_symbol_setup = 3
if retry_count > 3:
    block setup for symbol for N bars/days
```

---

## 11. MTC_V2 Mapping

### Producer Candidates

1. `producer_momentum_breakout_v1`
2. `producer_episodic_pivot_v1`
3. `producer_parabolic_exhaustion_short_v1`

Recommended order:

```text
Phase 1: producer_momentum_breakout_v1
Phase 2: producer_episodic_pivot_v1
Phase 3: producer_parabolic_exhaustion_short_v1
```

### Entry Gates

Useful MTC_V2 gates:

- MA alignment gate
- Volume / relative volume gate
- ATR / ADR volatility gate
- Momentum / relative strength gate
- Level proximity / pivot gate
- Session gate for intraday prototypes
- HTF trend / market regime gate

### Position Manager

Relevant MTC_V2 features:

- progressive exposure
- max entries
- cooldown after failed setup
- allow / block same-symbol retries
- long/short enable flags
- regime lock for long-only or short-enabled states
- account open-risk cap

### Position Sizing

Required sizing module:

```text
risk_pct_per_trade = 0.25% to 0.4%
max_single_position_pct = 25% to 30%
stop_distance = entry_price - stop_price
position_size = risk_budget / stop_distance
```

### Exits

Required exit modules:

- low-of-day stop
- same-day failure stop
- no-red-overnight exit
- breakeven stop
- ADR-multiple partial profit
- MA trail exit
- failed add / failed breakout exit
- retry limiter

---

## 12. Python Prototype Plan

### Phase 1 — Data and Event Extraction

Build event extractors for:

```text
RS_1M_GAINER
RS_3M_GAINER
RS_6M_GAINER
DENSE_VOLUME_FOOTPRINT
RIGHT_SIDE_TIGHTENING
PIVOT_BREAKOUT
CATALYST_GAP
HIGH_RELATIVE_VOLUME
PARABOLIC_EXTENSION
EXHAUSTION_REVERSAL
WATCHLIST_HEALTH
```

### Phase 2 — Long Breakout Prototype

Test only the classic breakout first:

```text
Universe -> RS scan -> compression filter -> pivot trigger -> low-of-day stop -> ADR partial -> MA trail
```

Metrics:

- win rate,
- average R,
- median R,
- max drawdown,
- consecutive losses,
- average holding time,
- percent of trades stopped same day,
- percent of trades reaching 2.5x ADR,
- contribution of top 5 winners.

### Phase 3 — Episodic Pivot Prototype

Add catalyst gap rules:

```text
gap_up_pct > 5%
relative_volume high
price escapes prior range
low-of-day stop
no red overnight
ADR partial
```

If no fundamental news data is available initially, use price/volume gap proxy and mark it as `CATALYST_UNKNOWN`.

### Phase 4 — Watchlist Health / Regime Filter

Build a regime metric from focus-list candidates and follow-through.

Test:

```text
without regime filter
with watchlist_health_score filter
with own-trade feedback filter
```

### Phase 5 — Parabolic Short Prototype

Only after long modules are stable:

```text
extension > 100%
multi-day vertical move
high relative volume
intraday/daily reversal
tight stop
max retries
```

This module must account for borrow, gap, and slippage assumptions. It should remain experimental until validated.

---

## 13. Event Taxonomy Draft

```json
{
  "event_id": "QL005_<symbol>_<date>_<event_type>",
  "candidate_id": "QL_CAND_005_7UfHg8PpDZk",
  "event_type": "MOMENTUM_BREAKOUT | EP_CATALYST_GAP | PARABOLIC_SHORT | ADR_PARTIAL | LOW_OF_DAY_STOP | NO_RED_OVERNIGHT_EXIT | FREE_ROLL_ADD",
  "symbol": "<SYMBOL>",
  "timeframe": "1D",
  "date": "YYYY-MM-DD",
  "side": "LONG | SHORT",
  "entry_price": 0.0,
  "stop_price": 0.0,
  "risk_pct_account": 0.0035,
  "position_pct_account": 0.20,
  "adr_pct": 0.06,
  "relative_volume": 0.0,
  "rs_1m_rank": 0.0,
  "rs_3m_rank": 0.0,
  "setup_context": {
    "theme_tag": "AI | CRYPTO | BIOTECH | CHINA | UNKNOWN",
    "catalyst_known": true,
    "price_escaped_range": true,
    "right_side_tight": true,
    "watchlist_health_score": 0.0
  },
  "management": {
    "no_red_overnight": true,
    "partial_after_adr_multiple": 2.5,
    "breakeven_after_favorable_move": true,
    "max_retries": 3
  }
}
```

---

## 14. Strengths

- Multiple setup modules are clearly identified.
- Risk model is unusually concrete and codeable.
- Account-risk logic is mathematically grounded in expected losing streaks.
- Low-of-day stop and no-red-overnight behavior can be tested directly.
- Watchlist breadth / breakout cluster idea provides a useful market regime filter.
- ADR-based partial profit rule is more robust than fixed-percentage targets.
- Fundamental catalyst is framed as “fuel,” with price/volume as confirmation; this is suitable for hybrid quantitative/manual research.
- The transcript contains useful guardrails around margin and overexposure.

---

## 15. Weaknesses / Ambiguities

- Some entries rely on discretionary chart reading and manually drawn trendlines.
- Catalyst quality is difficult to automate without news/fundamental data.
- Intraday entry and low-of-day stop logic may not be accurately represented with daily OHLC alone.
- Parabolic short module is dangerous and may have hidden real-world frictions:
  - borrow availability,
  - locate cost,
  - short squeezes,
  - gap risk,
  - hard-to-model intraday reversals.
- ADR partial rule needs exact definition:
  - ADR lookback,
  - use high-low range or close-to-close range,
  - whether move is measured from entry or prior close.
- “No red overnight” is powerful but may overfit to momentum swing style and should be tested independently.
- Fundamental screen details are not fully specified.

---

## 16. Risky or Suspicious Claims

No obvious scam-like claims are present. The most aggressive claims relate to high annual returns and large single-year performance, but the transcript also explains substantial effort, drawdowns, risk controls, losing trades, and mistakes.

The riskiest practical element is the parabolic short setup. It should not be copied directly into live trading logic without separate validation and friction modeling.

---

## 17. Recommended Next Action

### Recommended Codex Next Step

Create a candidate research folder only; do **not** patch MTC_V2 yet.

Suggested folder:

```text
10_CANDIDATES/QL_CAND_005_7UfHg8PpDZk_marios_three_setup_superperformance/
```

Suggested initial files:

```text
README.md
INTAKE_REPORT.md
SPEC_momentum_breakout_v1.md
SPEC_episodic_pivot_v1.md
SPEC_parabolic_short_v1.md
EVENT_SCHEMA_v1.json
PYTHON_PROTOTYPE_PLAN.md
RISK_RULES_v1.md
```

Priority order:

1. Momentum breakout prototype.
2. Episodic pivot prototype.
3. Watchlist health / regime filter.
4. Parabolic short prototype only after long modules are stable.

### Do Not Do Yet

- Do not edit `01_PINE/MTC_V2.pine`.
- Do not modify production Python runner files.
- Do not run optimization.
- Do not create large CSVs or data bundles.
- Do not merge all three setups into one monolithic strategy.
- Do not implement parabolic short before validating long-side modules.

---

## 18. Final Classification

```text
Classification: CANDIDATE
Codex Status: READY_FOR_PYTHON_PROTOTYPE
Candidate ID: QL_CAND_005_7UfHg8PpDZk
Primary Next Step: Build Python prototype specs and event extractors.
Pine Action: None.
Production Runner Action: None.
Optimization Action: None.
```

---

## 19. Files Created / Not Touched

### Created in this chat

```text
QL_INTAKE_005_7UfHg8PpDZk_marios_three_setup_superperformance.md
```

### Not touched

```text
01_PINE/MTC_V2.pine
Production Python runner files
Backtest outputs
Optimization outputs
CSV/data bundle/cache files
Repo registry files
Broker/exchange/API/webhook secrets
```
