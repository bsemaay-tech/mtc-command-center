# QuantLens Transcript Intake Report

## Metadata

- **Intake Date:** 2026-05-03
- **Source URL:** https://www.youtube.com/watch?v=C9Pvd9UD0jM
- **Original URL in File:** https://youtu.be/C9Pvd9UD0jM?si=XgRD98I2o19JsA0i
- **Video ID:** `C9Pvd9UD0jM`
- **Title:** Mark Minervini's #1 Risk Management Secret to Grow Your Trading Profit
- **Main Topic:** Progressive Exposure / Risk Feedback Loop / Position Sizing
- **Speaker / Source Reference:** Mark Minervini discussion, with references to Brandon and Mark in the panel dialogue
- **Channel:** `UNKNOWN_CHANNEL`
- **Transcript File:** `Mark Minervini's #1 Risk Management Secret to Grow Your Trading Profit.md`
- **Transcript Hash SHA256:** `278a49287e4953510430237078eb5ba6e59938a0e5353ded36e95e7171ab6994`
- **Transcript Hash Short:** `278a49287e49`

---

## Final Classification

- **Workflow Verdict:** `SALVAGE`
- **Codex Status Recommendation:** `SALVAGE_ONLY`
- **Trader Wiki Status:** Also suitable for Trader Wiki under risk management / system development.
- **Standalone Strategy Candidate:** No.
- **Reusable MTC_V2 Module Candidate:** Yes.
- **Priority:** `HIGH` for position sizing and portfolio-state design.
- **Confidence:** `HIGH`
- **Reason:** The transcript does not provide a complete buy/sell entry strategy. It does provide a highly codable risk-management and exposure-scaling framework: progressive exposure, feedback-driven risk increase/decrease, open-vs-closed profit handling, worst-case scenario tracking, and the 2-for-1 exposure rotation rule.

---

## Duplicate / Registry Check

> Repo registries were not available inside this ChatGPT session. This section is therefore a best-effort conversation-local check, not a true repo-level registry check.

- **Video ID duplicate in current uploaded set:** No exact duplicate observed in current conversation.
- **Transcript hash duplicate in current uploaded set:** No exact duplicate observed in current conversation.
- **Thematic overlap:** Yes. This overlaps with prior Chris Flanders / Deepak risk-control material, but it is not a duplicate. It is specifically focused on progressive exposure and feedback-based portfolio scaling.
- **Required repo registry check before Codex ingestion:**
  - `_registry/youtube_video_index.csv`
  - `channel_quality_registry.csv`
  - `channel_blacklist.yaml`
- **Duplicate Decision:** `NOT_DETECTED_IN_SESSION`
- **Repo-Level Duplicate Status:** `UNVERIFIED`

---

## Channel Quality Check

- **Channel:** `UNKNOWN_CHANNEL`
- **Blacklist Status:** Cannot verify; channel metadata was not provided.
- **Automatic blacklist action:** None.
- **Recommended channel quality update:** Count this as useful / salvage-positive material because it provides precise risk-management concepts from a recognized growth-stock trading methodology context.
- **Quality Contribution:** `SALVAGE_ONLY` should count as useful but not as a full strategy candidate.

---

## Executive Summary

This transcript is not primarily an entry setup. It is a **portfolio exposure and risk-management module**.

The core idea is:

> Increase exposure only when your own trades are giving positive feedback; decrease or stay small when your trades are not working. The goal is to trade biggest when trading best, and smallest when trading worst.

For QuantLens and MTC_V2, this is valuable because MTC already has strategy producers, filters, SL/TP, position management, and portfolio-state concepts. This transcript can improve the **Position Sizing**, **Position Manager**, and **PortfolioState guard** layers without changing entry logic.

Do not treat this as a standalone profitable strategy. Treat it as a **risk overlay / exposure governor** to be tested on top of existing strategy candidates.

---

## Extracted Core Concepts

### 1. Progressive Exposure Is Multi-Dimensional

The transcript emphasizes that progressive exposure is not just position size. It includes:

- Total portfolio exposure.
- Individual position size.
- Number of stocks / active positions.
- Single-stock concentration risk.
- Whether profits are open or closed.
- Whether current positions are giving positive or negative feedback.

A portfolio can be 25% invested in one stock or 25% invested across five stocks. Both have the same total exposure, but the single-stock risk profile is different.

---

### 2. Start Small After a Correction

The transcript discusses coming back from 100% cash after a market correction. The first few trades should act as probes.

**Interpretation for research:**

- Start with reduced risk after a correction, cash state, or drawdown period.
- Increase only if the first trades begin to work.
- Avoid immediately returning to full exposure just because the market appears to have bounced.

---

### 3. Use Trade Feedback, Not Opinions, to Drive Exposure

The most important rule extracted:

```text
Trade largest when trading best.
Trade smallest when trading worst.
```

This means exposure should respond to actual strategy performance and current position traction, not to prediction, confidence, or outside commentary.

**Positive feedback examples:**

- Initial positions move in favor.
- Stops are not being hit.
- Open positions develop profit cushion.
- Breakouts hold and follow through.
- Multiple setups work at the same time.

**Negative feedback examples:**

- New buys fail quickly.
- Stops are hit repeatedly.
- Open profits reverse.
- Breakouts fail.
- Market or leadership becomes choppy.

---

### 4. Open Profits and Closed Profits Are Different

The transcript explicitly separates open profits from closed profits.

**Closed profit:**

- Risk is no longer in the portfolio.
- Can more safely be used as a profit buffer for new risk.

**Open profit:**

- Still exposed to market reversal.
- Can provide cushion, but should not be treated as fully secure.
- If new trades are added using open profits as justification, a correlated reversal can hit both existing winners and new positions.

**MTC implication:** PortfolioState should track open PnL and closed PnL separately.

---

### 5. Always Calculate Worst-Case Scenario

Before increasing exposure, the transcript says to ask:

```text
If I get knocked out of everything here, what am I down?
```

This is directly codable.

**Worst-case portfolio risk calculation:**

```text
worst_case_loss = sum(position_risk_to_stop for all open positions)
                + risk_to_stop_for_new_candidate
                + correlated_gap_buffer_optional
```

Exposure should only increase if worst-case loss remains inside the allowed risk budget.

---

### 6. The 2-for-1 Rule

If two existing positions are weak but have not hit their stops, and a stronger new setup appears:

```text
Sell half of each weak position.
Use the freed capital/risk budget to buy one full position in the stronger setup.
```

Purpose:

- Move capital toward the best current merchandise.
- Reduce laggards without fully exiting.
- Avoid increasing total exposure.
- Keep portfolio synchronized with what is working now.

This is useful for a future portfolio-level optimizer or discretionary-assist module.

---

## Strategy Candidate Decomposition

### Candidate A — Progressive Exposure Governor

**Type:** Portfolio risk overlay, not signal producer.

**Purpose:** Dynamically adjust allowed risk and exposure based on current feedback.

**Possible state tiers:**

```text
CASH_OR_RESET
PROBE
RAMP
NORMAL
ATTACK
DEFENSIVE
```

**Example behavior:**

- `CASH_OR_RESET`: no or minimal exposure.
- `PROBE`: small starter positions only.
- `RAMP`: increase risk after positive feedback.
- `NORMAL`: standard risk budget.
- `ATTACK`: larger exposure only when multiple positions are working.
- `DEFENSIVE`: cut risk after failed breakouts / drawdown / loss streak.

**Codability:** `HIGH`

**MTC_V2 mapping:**

- `POSITION MANAGER`
- `POSITION SIZING`
- `PortfolioState` guard
- `max_entries`
- `risk_pct`
- `max_total_risk`
- `cooldown_bars` / recovery logic

---

### Candidate B — Feedback-Based Risk Multiplier

**Type:** Risk sizing module.

**Purpose:** Convert recent trade and open-position feedback into a risk multiplier.

**Possible inputs:**

```text
recent_closed_R
recent_win_rate
consecutive_losses
open_pnl_R
open_positions_above_entry_pct
failed_breakout_count
market_regime
leader_breadth_proxy
current_drawdown_pct
```

**Example output:**

```text
risk_multiplier = 0.25 | 0.50 | 1.00 | 1.25 | 1.50
```

**Example rules:**

```text
if current_drawdown_pct > dd_limit:
    risk_multiplier = 0.25
elif consecutive_losses >= 3:
    risk_multiplier = 0.25 or 0.50
elif recent_closed_R > threshold and open_pnl_R > threshold:
    risk_multiplier = 1.25 or 1.50
else:
    risk_multiplier = 1.00
```

**Codability:** `HIGH`

**Important:** Start conservative. A risk multiplier can improve results in trending regimes but can also amplify drawdowns if feedback is noisy.

---

### Candidate C — Open vs Closed Profit Cushion Rule

**Type:** Portfolio accounting / risk guard.

**Purpose:** Prevent over-leveraging based only on unrealized gains.

**Rules to test:**

```text
closed_profit_buffer = max(0, closed_pnl_since_reset)
open_profit_buffer = max(0, open_pnl)
adjusted_profit_cushion = closed_profit_buffer + open_profit_haircut * open_profit_buffer
```

Where:

```text
open_profit_haircut = 0.25 to 0.50
```

This means open profits can support increased exposure, but only partially.

**Codability:** `HIGH`

**MTC_V2 mapping:** PortfolioState.

---

### Candidate D — 2-for-1 Position Rotation Rule

**Type:** Position management / reallocation module.

**Purpose:** Reallocate capital from weak current holdings into stronger new setup without increasing total exposure.

**Candidate conditions:**

- New setup has stronger score than existing weak positions.
- Existing positions have weak traction but have not hit stops.
- Total portfolio exposure is already near allowed cap.
- New entry would otherwise exceed exposure cap.

**Action:**

```text
Reduce two weakest positions by 50% each.
Open one full position in the new stronger setup.
Keep total exposure approximately unchanged.
```

**Codability:** `MEDIUM-HIGH`

**MTC_V2 caution:** This is multi-position/multi-symbol logic and may belong in Python portfolio backtester first, not in Pine.

---

## Data Requirements

Minimum:

- OHLCV for traded symbols.
- Trade ledger with entry, exit, stop, R, realized PnL, unrealized PnL.
- Current open positions.
- Risk-to-stop per open position.
- Portfolio equity.
- Available exposure/margin.

Recommended:

- Market regime signal from index.
- Symbol score / setup quality score.
- Leader breadth / watchlist breadth.
- Correlation or sector concentration estimate.
- Slippage and gap risk model.

---

## Python Prototype Plan

### Phase 1 — Isolated Risk Overlay Simulation

Do not change strategy entry/exit rules yet.

Add a wrapper that can run on top of an existing trade stream:

```text
input: raw_strategy_signals + stop levels + trade results
output: adjusted position size / allow-block decision / exposure tier
```

Test overlays:

1. `BASELINE_FIXED_RISK`
2. `PROGRESSIVE_EXPOSURE_SIMPLE`
3. `PROGRESSIVE_EXPOSURE_OPEN_CLOSED_PNL`
4. `PROGRESSIVE_EXPOSURE_WITH_LOSS_STREAK_THROTTLE`
5. `PROGRESSIVE_EXPOSURE_WITH_2_FOR_1_ROTATION`

Metrics:

- CAGR
- Max drawdown
- MAR
- Net profit
- Profit factor
- Win rate
- Average R
- R-multiple distribution
- Exposure over time
- Number of trades blocked
- Number of risk increases
- Number of risk decreases
- Drawdown after exposure increase
- Performance by market regime

---

### Phase 2 — PortfolioState Integration Design

Add explicit state fields:

```text
portfolio_state.current_exposure_pct
portfolio_state.current_risk_to_stop_pct
portfolio_state.open_pnl_R
portfolio_state.closed_pnl_since_reset_R
portfolio_state.consecutive_losses
portfolio_state.recent_signal_failure_count
portfolio_state.exposure_tier
portfolio_state.risk_multiplier
portfolio_state.last_risk_tier_change_bar
```

---

### Phase 3 — MTC_V2 Candidate Integration

Only after Python validation:

- Add optional `Progressive Exposure Guard`.
- Add optional `Dynamic Risk Multiplier`.
- Keep default behavior unchanged.
- Feature-gate all new behavior.
- Do not alter existing fixed-risk parity tests unless explicitly enabled.

---

## MTC_V2 Integration Notes

This transcript maps strongly to MTC_V2 architecture:

### Best-fit MTC layers

1. **PortfolioState**
   - Track realized/open PnL, current exposure, risk-to-stop, recent losses, and current risk tier.

2. **Position Manager**
   - Decide whether new entries are allowed based on exposure tier and feedback.

3. **Position Sizing**
   - Apply dynamic risk multiplier to base `risk_pct`.

4. **Entry Gates / Guards**
   - Add a portfolio-state guard that blocks or reduces entries when recent feedback is poor.

### Not a good fit as Signal Producer

This transcript does not define a buy/sell signal such as breakout, pullback, ORB, VCP, EP, or trend-following trigger. It should not be implemented as a producer.

---

## Suggested IDs

```text
SALVAGE_2026_05_03_C9Pvd9UD0jM_PROGRESSIVE_EXPOSURE_GOVERNOR
SALVAGE_2026_05_03_C9Pvd9UD0jM_FEEDBACK_RISK_MULTIPLIER
SALVAGE_2026_05_03_C9Pvd9UD0jM_OPEN_CLOSED_PROFIT_CUSHION
SALVAGE_2026_05_03_C9Pvd9UD0jM_TWO_FOR_ONE_ROTATION_RULE
```

---

## Trader Wiki Extraction

Suggested wiki path:

```text
11_TRADER_WIKI/01_RISK_MANAGEMENT/TW_2026-05-03_PROGRESSIVE_EXPOSURE_MARK_MINERVINI.md
```

Suggested wiki topics:

- Progressive exposure is not just position size; it includes total exposure, concentration, and number of active positions.
- Good trading feedback should increase exposure slowly; poor feedback should reduce exposure quickly.
- Open and closed profits should not be treated the same.
- Always calculate worst-case scenario before increasing risk.
- The 2-for-1 rule reallocates exposure from weak positions to stronger setups without increasing total exposure.
- Trading has an art/discretion component; not every part of progressive exposure can be reduced to a fixed formula.

---

## Risky / Suspicious Claims

- The transcript argues that trading cannot be fully captured by spreadsheets, algorithms, or AI. Treat this as a discretionary trading opinion, not as a testable system rule.
- Progressive exposure can amplify gains, but it can also amplify losses if the feedback signal is noisy or delayed.
- The transcript does not provide exact numerical rules for when to move from probe to full exposure.
- The 2-for-1 rule requires multi-position portfolio logic and may not be directly expressible in TradingView Pine for a single-chart strategy.
- If open profits are treated too aggressively as cushion, correlated reversals can cause fast drawdowns.

---

## Final Recommendation

Do **not** create a standalone strategy candidate from this transcript.

Do create a **salvage module package** for risk management and position sizing:

```text
1. Progressive Exposure Governor
2. Feedback-Based Risk Multiplier
3. Open vs Closed Profit Cushion Rule
4. 2-for-1 Position Rotation Rule
5. Worst-Case Portfolio Risk Calculator
```

Recommended immediate Codex task:

```text
Create a Python-only design/prototype plan for a ProgressiveExposureGovernor that consumes an existing trade stream and PortfolioState, then outputs dynamic risk_multiplier, max_total_exposure, and entry allow/block decisions. Do not modify 01_PINE/MTC_V2.pine. Do not modify production Python runner files. Do not run backtests or optimization yet.
```

---

## Files Touched / Not Touched

### Created

- `INTAKE_2026-05-03_C9Pvd9UD0jM_mark_minervini_progressive_exposure.md`

### Read / Referenced

- `Mark Minervini's #1 Risk Management Secret to Grow Your Trading Profit.md`

### Not Touched

- `01_PINE/MTC_V2.pine`
- Production Python runner files
- Backtest engine
- Optimization engine
- Large CSV/data/cache outputs
- Broker/API/exchange/secrets

---

## Next Action

Add this report to the QuantLens transcript intake folder as `SALVAGE_ONLY`. It should inform the future MTC_V2 position sizing / portfolio risk layer, but it should not be entered into the strategy candidate registry as a standalone entry setup.
