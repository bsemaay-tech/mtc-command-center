# PRE-REG — Crypto Paper Bridge (Hyperliquid) v1

Author: Claude Fable 5, 2026-07-05; **broker finalized to Hyperliquid 2026-07-06** (see
`07_BROKER_DECISION.md`). Approved scope: design docs only. Binding once Barış approves; changes
require a new dated section, never edits in place. "Paper" = **Hyperliquid testnet**.

## 1. Objective

Build execution plumbing + monitoring dashboard so that when a promotable strategy exists,
the pipeline from signal → risk → order → fill → log is already **validated on paper**.
Secondary objective (explicit, Barış 2026-07-05): seeing a strategy run live is a motivation
goal in itself — plumbing validation does NOT wait for a promotable strategy.

## 2. What this is NOT

- NOT a claim of edge. Paper P&L here is **plumbing evidence, not strategy evidence**.
  Promotion decisions stay in the MCC 4-gate pipeline (DSR, BH-FDR, CPCV, multi-window).
- NOT an LLM trading bot. LLM is veto/regime-only (see README principles).
- NOT connected to real money in v1. Mainnet support exists behind the triple-lock but is
  out of scope for v1 acceptance.

## 3. First strategy (plumbing test subject)

`Keltner breakout × trail_ema8 × BTC (perp) × 1h` — the FAZ 3B logic **ported to crypto**. Chosen
because its formal rules are already written; its use here is a *plumbing test*, NOT a promotion
statement — it has NOT passed the promotion ladder. (The open crypto research lead
`GEN_DONCHIAN_BREAKOUT` is an equally valid subject; the point is exercising the pipeline, not the
edge.)

Parameters are copied into `config/strategies/keltner_trail_ema8.yaml` at build time from the
QuantLens crypto run; the bridge never reads MCC files at runtime.

## 4. Gates (sequential; each needs Barış approval to advance)

| Gate | Name | Exit criteria |
|---|---|---|
| P0 | Smoke | Hyperliquid **testnet** connects (API wallet), account summary + live BTC candle retrieved, one entry + SL/TP trigger group placed AND cancelled on testnet, all steps in JSON log. |
| P1 | Dry-run loop | Full engine loop on **MockBroker** (no exchange): bars in → signal → risk → simulated fill → dashboard shows position/equity. Induced failures (disconnect, reject, LLM timeout) handled per §7. |
| P2 | Testnet single-coin | Strategy live on testnet BTC 1h for ≥10 days unattended (crypto 24/7 → ~10 calendar days). Reconnect survives WS drops. Zero unexplained order states. |
| P3 | Testnet evaluation | ≥30 days. Fill-vs-expected slippage report. Backtest-parity comparison of signals (bridge signal timestamps vs QuantLens engine on same bars). |

## 5. Pre-registered metrics (logged from P2 onward) — AMENDED 2026-07-06 (audit round)

Per trade (first-class columns in `trades`, not JSON archaeology): signal_ts, decision_ts,
submit_ts, first/last_fill_ts, expected_px, fill_px, slippage_bps, size, risk_at_entry_$,
SL, TP, exit_reason, llm_directive_at_entry.
Per day (`risk_days` + 60 s equity sampling): equity, realized/unrealized P&L, max intraday DD,
order rejects, disconnects, funding paid/received, LLM calls (count, latency, veto count, cost).

**Metrics glossary (binding definitions):**
- `expected_px` per order type: LMT ⇒ the limit price; MKT ⇒ next bar OPEN after signal
  (bar-close-signal → market-next semantics). Slippage on MKT therefore INCLUDES gap risk;
  a separate `execution_slippage` (fill vs first quote after submit) isolates execution quality.
  Note: on testnet, slippage measures plumbing consistency, NOT live execution quality — never
  quote it as an edge/cost estimate.
- `slippage_bps` = (fill_px − expected_px)/expected_px × 10⁴ × direction_sign.
- Timestamps: stored UTC; all day-bucketing on **UTC** dates (crypto 24/7).
- "Unexplained order state" taxonomy: any order ending outside
  {FILLED, CANCELLED_BY_ENGINE, CANCELLED_STALE, REJECTED_LOGGED} or any position-without-SL
  interval > 10 s that lacks a matching recovery event.
- Missing/late bars: a day with any missing 1h bar is excluded from parity denominators and
  counted in a `data_gap_days` tally (>20% gap days ⇒ data setup investigated).

## 6. Pre-registered decision rules

- **Signal parity rule (two-stage — AMENDED):**
  Stage 1 — *bar identity:* the offline engine replays the **bridge-logged bars** (from the
  `bars` table, NOT the original QuantLens bundle); bar boundaries (ts + OHLC) must match the
  bridge's record exactly, and the bar-alignment policy (UTC 1h, 24/7) must equal the golden run's
  policy. Bar mismatch ⇒ data bug, evaluated separately, blocks advancement on its own.
  Stage 2 — *signal parity:* ≥95% of bridge signals match the offline replay on those bars.
  Denominator = all bar-closes where either side signals; missing-bar days excluded (§5).
  Golden semantics note: the bridge port is close-confirmed→MKT-next; the golden list is
  generated from the SOURCE engine run with the documented "bridge execution transform"
  applied — the transform itself is written down before build day (02_BUILD_PLAN task 3b).
- **LLM veto audit (operationalized — AMENDED):** veto precision = share of vetoed trades whose
  counterfactual simulated P&L (logged at veto time from the would-be OrderPlan) would have been
  negative. Evaluated only at ≥20 vetoes; precision <40% ⇒ demote veto to flag-only. Under 20
  vetoes ⇒ no verdict, veto stays advisory.
- **Slippage rule:** median |slippage_bps| > 25 on BTC 1h ⇒ investigate order type before any
  live discussion — interpreted per the §5 glossary caveat (testnet = plumbing metric).

## 7. Abort / kill criteria (any one triggers DISARM + alert)

- Daily loss limit hit (config `risk.max_daily_loss_pct`, default 2% of testnet equity).
- Order in unknown state > 120 s after submit.
- 3 consecutive order rejects.
- N consecutive losing trades (config `risk.max_consecutive_losses`, default 3; loss = pnl<0 any
  exit reason) ⇒ auto-pause. Default policy `pause_auto_rearm`: auto re-ARM after cooldown, max
  2 auto-re-arms/day, then hard DISARM. (AMENDED — manual-only re-arm contradicted the P2
  "unattended ≥10 days" criterion; audit: Opus F-08.)
- Data staleness: no bar update for 2× bar period (24/7).
- Position exists with no SL trigger (naked position): if traceable to this app's cloid, FIRST
  re-submit the protective SL/TP trigger group; flatten only if re-protection fails. (Native
  triggers survive WS drops, so this is rare — but the guard stays.) Foreign/manual positions are
  never adopted or flattened — WARN only.
- Liquidation buffer breached: mark price within a configurable buffer of the liquidation price ⇒
  DISARM + alert (v1 leverage = 1 makes this remote, but the guard exists for any leverage change).

## 8. Out of scope for v1

Multi-strategy portfolio, mainnet/real money, spot markets, additional exchanges (Binance),
leverage > 1, sub-hour timeframes, mobile UI, auto-promotion from MCC, LLM-generated strategies.
