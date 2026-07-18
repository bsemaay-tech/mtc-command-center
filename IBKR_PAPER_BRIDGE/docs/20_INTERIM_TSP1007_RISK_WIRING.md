# 20 — Interim TS-P1-007: realized-PnL / consecutive-loss risk wiring

Date: 2026-07-18. Authorization: Barış decision 2026-07-18 (expedite recorded in
`MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/05_IMPLEMENTATION_BACKLOG.md` amendment log;
execution approved same day). Built on post-PR-#23 master (`abda6717`), branch
`feature/interim-daily-loss-wiring`.

## Problem

`RiskEngine.evaluate` had working DAILY_LOSS and CONSECUTIVE_LOSS gate code, but the operational
path never supplied the inputs: the engine omitted `realized_today`/`consecutive_losses`
(defaults 0.0/0 — gates could never trigger), `OrderManager.reconcile` persisted
`realized_today=0.0` into every equity row, and `Store.upsert_risk_day` had no callers. Unit
tests passed only by injecting parameters directly into `evaluate`.

## Change (three call sites, no threshold or strategy change)

1. `bridge/store/db.py` — two new read-only queries:
   - `Store.realized_pnl_today(now=None)` — sum of closed-trade `pnl` with `exit_ts` ≥ UTC
     midnight, **across all run_ids** so a restart inside the trading day cannot reset the gate.
   - `Store.consecutive_closed_losses()` — most-recent consecutive closed trades with `pnl < 0`,
     across all run_ids, not day-scoped.
2. `bridge/engine/engine.py` — `on_bar` now passes both values into `risk_engine.evaluate(...)`.
3. `bridge/engine/orders.py` — `reconcile()` equity row now records the real
   `realized_pnl_today()` instead of the hardcoded `0.0`.

Config defaults untouched (`max_daily_loss_pct=0.02`, `max_consecutive_losses=3`). Existing
disarm plumbing (`RiskResult.disarm` → engine DISARM + `RISK_AUTO_DISARM` event) unchanged.

## Proof

`tests/test_interim_risk_wiring.py` — 8 tests, all engine-path (drive `run_replay`, no
parameter injection):

- Daily-loss trigger at exact boundary (−2%·equity) → no submit, DISARMED, `DAILY_LOSS_LIMIT`
  reject, `RISK_AUTO_DISARM` event.
- One dollar inside the boundary → entry submits, stays ARMED.
- Yesterday's loss excluded from the daily gate (UTC day scoping).
- Consecutive-loss trigger at `max_consecutive_losses` → no submit, DISARMED.
- A win resets the streak.
- **Restart persistence:** fresh `Store` + fresh engine on the same SQLite file still blocks.
- Reconcile equity row carries real `realized_today`.
- Store-helper units: empty DB → 0/0; open trades (NULL pnl) ignored.

Evidence: full suite **140 passed** post-fix (132 pre-existing + 8 new, zero regressions);
pre-fix proof by stashing the three production files → **5/8 FAIL** on old code (the three
pass-cases pass either way, as expected). No exchange, scheduler, credential, config, or
`C:\P2RT` action.

## Repairs after Codex audit BLOCK (2026-07-18, `CODEX_INTERIM_TSP1007_AUDIT_2026-07-18.md`)

1. **Environment isolation (F-01):** both helpers now take the current `run_id`, resolve its
   `runs.mode`/`runs.network`, and join `trades`→`runs` so only same-environment rows count.
   Cross-run restart behavior inside one environment is preserved; dry-run/replay rows sharing
   `data/bridge.db` can no longer trip or reset paper gates. Unknown `run_id` raises
   (fail closed).
2. **Net PnL (F-02):** `trades.pnl` is now NET: gross price delta minus
   `Store.trade_costs(decision_uid)` = SUM(fills.fee) + SUM(fills.funding) for the trade
   (entry + exit fills; the exit fill is persisted before the close computation). Sign
   convention: positive fee/funding = debit (Hyperliquid convention); negative = rebate/credit.
   `TRADE_CLOSED` decisions record `pnl` (net), `pnl_gross`, and `costs`.
3. **Fail-closed risk-input boundary (F-03):** failures reading either risk input DISARM
   in-memory first, then best-effort persist meta + `RISK_INPUT_FAILED` event, then notify
   (fail-silent Telegram). The latch is STICKY: `_app_state()` reports DISARMED while
   `risk_input_error` is set — even if the disarm meta write failed and the persisted value
   still says ARMED — and only an explicit human `arm()` clears it. `status()` exposes
   `risk_input_error` and falls back to in-memory state if meta reads fail. The failed bar is
   NOT retried (it stays in `_processed_bar_ts`); its signal is intentionally lost.
4. **Timestamp canonicalization (F-04):** `_to_iso` now parses string inputs via
   `datetime.fromisoformat` and always emits aware-UTC ISO (invalid strings raise; naive values
   are treated as UTC — including a naive `now` injected into `realized_pnl_today`). The daily
   query uses the bounded half-open interval `[UTC midnight, next midnight)`.
5. **Deterministic clock (F-06):** `Store(db_path, clock=...)` seam; engine-path tests freeze it.

## Interim semantics disclosed (audit F-05)

- The daily-loss percentage compares realized PnL against **current account equity at signal
  time**, not a persisted UTC day-start equity. `risk_days`/`day_start_equity` remain UNWIRED.
  If equity has risen intraday the gate triggers slightly late; if fallen, slightly early.
- PnL is **engine-derived** from fills; there is no broker-reconciled cross-check yet.
- Paper and dry-run share `data/bridge.db` by default; isolation is enforced at query level
  (repair 1). A dedicated per-environment DB path remains a TS-P2-007 concern.

## Status and follow-up

Interim only. Broker-reconciled PnL, equity-stop, drawdown, day-start equity, and the full
snapshot feed remain the FULL TS-P1-007 behind TS-P1-005/006, which supersedes this wiring when
it lands. Deploy of this fix is NOT authorized by this document — independent audit first, then
the standard deploy gate.
