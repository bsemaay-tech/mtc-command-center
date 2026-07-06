# PRE-REG — IBKR Paper Bridge (v1)

Author: Claude Fable 5, 2026-07-05. Approved scope: design docs only (this file).
Binding once Barış approves; changes require a new dated section, never edits in place.

## 1. Objective

Build execution plumbing + monitoring dashboard so that when a promotable strategy exists,
the pipeline from signal → risk → order → fill → log is already **validated on paper**.
Secondary objective (explicit, Barış 2026-07-05): seeing a strategy run live is a motivation
goal in itself — plumbing validation does NOT wait for a promotable strategy.

## 2. What this is NOT

- NOT a claim of edge. Paper P&L here is **plumbing evidence, not strategy evidence**.
  Promotion decisions stay in the MCC 4-gate pipeline (DSR, BH-FDR, CPCV, multi-window).
- NOT an LLM trading bot. LLM is veto/regime-only (see README principles).
- NOT connected to real money in v1. Live port support exists behind double-lock but is
  out of scope for v1 acceptance.

## 3. First strategy (plumbing test subject)

`KELTNER_STOP_V1 × trail_ema8 × AAPL × 1h` — the FAZ 3B Stage-1 STRONG_PASS variant
(H1 confirmed, union-DSR 0.581, PR #15). Chosen because its formal rules are already
written and evidenced. Its use here is *plumbing test*, not a promotion statement —
it has NOT passed the full promotion ladder.

Parameters are copied into `config/strategies/keltner_trail_ema8.yaml` at build time from
the FAZ 3B run artifacts; the bridge never reads MCC files at runtime.

## 4. Gates (sequential; each needs Barış approval to advance)

| Gate | Name | Exit criteria |
|---|---|---|
| P0 | Smoke | TWS paper API connects (7497), account summary + delayed quote for AAPL retrieved, one bracket order placed AND cancelled on paper, all steps in JSON log. |
| P1 | Dry-run loop | Full engine loop on **MockBroker** (no TWS): bars in → signal → risk → simulated fill → dashboard shows position/equity. Induced failures (disconnect, reject, LLM timeout) handled per §7. |
| P2 | Paper single-symbol | Strategy live on paper AAPL 1h for ≥10 trading days unattended. Reconnect survives TWS nightly restart. Zero unexplained order states. |
| P3 | Paper evaluation | ≥30 trading days. Fill-vs-expected slippage report. Pine/backtest-parity comparison of signals (bridge signal timestamps vs backtest engine on same bars). |

## 5. Pre-registered metrics (logged from P2 onward) — AMENDED 2026-07-06 (audit round)

Per trade (first-class columns in `trades`, not JSON archaeology): signal_ts, decision_ts,
submit_ts, first/last_fill_ts, expected_px, fill_px, slippage_bps, size, risk_at_entry_$,
SL, TP, exit_reason, llm_directive_at_entry.
Per day (`risk_days` + 60 s RTH equity sampling): equity, realized/unrealized P&L,
max intraday DD, order rejects, disconnects, LLM calls (count, latency, veto count, cost).

**Metrics glossary (binding definitions):**
- `expected_px` per order type: LMT ⇒ the limit price; MKT ⇒ next bar OPEN after signal
  (bar-close-signal → market-next semantics). Slippage on MKT therefore INCLUDES gap risk;
  a separate `execution_slippage` (fill vs first quote after submit) isolates broker quality.
  Note: under delayed data + paper simulated fills, slippage measures plumbing consistency,
  NOT live execution quality — never quote it as an edge/cost estimate.
- `slippage_bps` = (fill_px − expected_px)/expected_px × 10⁴ × direction_sign.
- Timestamps: stored UTC; all day-bucketing on America/New_York dates.
- "Unexplained order state" taxonomy: any order ending outside
  {FILLED, CANCELLED_BY_ENGINE, CANCELLED_STALE, REJECTED_LOGGED} or any position-without-SL
  interval > 10 s that lacks a matching recovery event.
- Missing/late bars: a session with any missing RTH bar is excluded from parity denominators
  and counted in a `data_gap_days` tally (>20% gap days ⇒ data setup investigated).

## 6. Pre-registered decision rules

- **Signal parity rule (two-stage — AMENDED):**
  Stage 1 — *bar identity:* the offline engine replays the **bridge-logged bars** (from the
  `bars` table, NOT the original Alpaca bundle); bar boundaries (ts + OHLC) must match the
  bridge's record exactly (they will — same source), and the bar-alignment policy (RTH 1h,
  30-min tail discarded) must equal the golden run's policy. Bar mismatch ⇒ data bug, evaluated
  separately, blocks advancement on its own.
  Stage 2 — *signal parity:* ≥95% of bridge signals match the offline replay on those bars.
  Denominator = all bar-closes where either side signals; missing-bar sessions excluded (§5).
  Golden semantics note: the bridge port is close-confirmed→MKT-next; the golden list is
  generated from the SOURCE engine run with the documented "bridge execution transform"
  applied — the transform itself is written down before build day (02_BUILD_PLAN task 3b).
- **LLM veto audit (operationalized — AMENDED):** veto precision = share of vetoed trades whose
  counterfactual simulated P&L (logged at veto time from the would-be OrderPlan) would have been
  negative. Evaluated only at ≥20 vetoes; precision <40% ⇒ demote veto to flag-only. Under 20
  vetoes ⇒ no verdict, veto stays advisory.
- **Slippage rule:** median |slippage_bps| > 25 on AAPL 1h ⇒ investigate order type before any
  live discussion — interpreted per the §5 glossary caveat (paper+delayed = plumbing metric).

## 7. Abort / kill criteria (any one triggers DISARM + alert)

- Daily loss limit hit (config `risk.max_daily_loss_pct`, default 2% of paper equity).
- Order in unknown state > 120 s after submit.
- 3 consecutive order rejects.
- N consecutive losing trades (config `risk.max_consecutive_losses`, default 3; loss = pnl<0 any
  exit reason) ⇒ auto-pause. Default policy `pause_auto_rearm`: auto re-ARM after cooldown, max
  2 auto-re-arms/day, then hard DISARM. (AMENDED — manual-only re-arm contradicted the P2
  "unattended ≥10 days" criterion; audit: Opus F-08.)
- Data staleness: no bar update for 2× bar period during market hours.
- Position exists with no SL working order (naked position): if the position is traceable to this
  app's orderRef, FIRST re-submit a protective bracket (TWS nightly restart drops paper orders —
  audit: Kimi F-01); flatten only if re-protection fails. Foreign/manual positions are never
  adopted or flattened — WARN only.

## 8. Out of scope for v1

Multi-strategy portfolio, live account, options/futures, sub-hour timeframes, mobile UI,
auto-promotion from MCC, LLM-generated strategies.
