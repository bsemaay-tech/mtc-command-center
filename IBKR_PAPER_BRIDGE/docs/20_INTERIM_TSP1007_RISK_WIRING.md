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

## Status and follow-up

Interim only. Engine-derived trade PnL is the source; broker-reconciled PnL, equity-stop,
drawdown, and the full snapshot feed remain the FULL TS-P1-007 behind TS-P1-005/006, which
supersedes this wiring when it lands. Deploy of this fix is NOT authorized by this document —
independent audit first, then the standard deploy gate.
