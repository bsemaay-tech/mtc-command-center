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

## 5. Pre-registered metrics (logged from P2 onward)

Per trade: signal_ts, decision_ts, submit_ts, fill_ts, expected_px (bar close at signal),
fill_px, slippage_bps, size, risk_at_entry_$, SL, TP, exit_reason, llm_directive_at_entry.
Per day: equity, realized/unrealized P&L, max intraday DD, order rejects, disconnects,
LLM gate calls (count, latency, veto count).

## 6. Pre-registered decision rules

- **Signal parity rule:** ≥95% of bridge signals must match offline engine replay on identical
  bars over the P3 window; mismatch >5% ⇒ plumbing bug, block advancement.
- **LLM veto audit:** after P3, veto precision reviewed; if vetoes are noise (no measurable
  harm avoided), LLM gate demoted to flag-only.
- **Slippage rule:** median |slippage| > 25 bps on AAPL 1h ⇒ investigate order type before
  any live discussion.

## 7. Abort / kill criteria (any one triggers DISARM + alert)

- Daily loss limit hit (config `risk.max_daily_loss_pct`, default 2% of paper equity).
- Order in unknown state > 120 s after submit.
- 3 consecutive order rejects.
- N consecutive losing trades (config `risk.max_consecutive_losses`, default 3) ⇒ auto-DISARM;
  re-arm is manual after cooldown (`risk.cooldown_minutes_after_loss`).
- Data staleness: no bar update for 2× bar period during market hours.
- Position exists with no SL working order (naked position) — flatten immediately.

## 8. Out of scope for v1

Multi-strategy portfolio, live account, options/futures, sub-hour timeframes, mobile UI,
auto-promotion from MCC, LLM-generated strategies.
