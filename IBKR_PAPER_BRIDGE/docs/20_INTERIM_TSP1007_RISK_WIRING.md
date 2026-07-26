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

## Second repair round after re-audit BLOCK (2026-07-18, `CODEX_INTERIM_TSP1007_REAUDIT_2026-07-18.md`)

- **R-01 partial fills:** fill accounting is now cumulative and derived from persisted fills.
  Order `filled_qty`/`avg_fill_px` are cumulative; an order flips to `FILLED` only when its
  fills reach the ordered quantity (partial fills keep the resting status so pending/grace
  logic still sees a live order). Trade entry price is the entry-fill VWAP (first-fill
  timestamp preserved); each exit fill contributes its actual quantity; the trade closes only
  when cumulative exit quantity reaches the entry basis, and only then are exit VWAP, net PnL,
  and one `TRADE_CLOSED` decision persisted. Earlier partial exits persist a
  `TRADE_PARTIAL_EXIT` decision and contribute NOTHING to either gate. Close is idempotent
  (duplicate redelivered fills coalesce on `fill_id`; `TRADE_CLOSED` is not duplicated).
  Brokers that report the entry only on the order row (mock paths) fall back to the trade's
  planned quantity and recorded entry price, preserving prior behavior.
- **R-02 funding — honest production semantics:** the cost sum includes the `fills.funding`
  column, but **no production path populates funding today**: the Hyperliquid adapter maps
  `fee` only, and no funding-ledger subscription exists. In production, gate PnL is therefore
  **gross − fees**; funding events on the exchange are NOT captured. Wiring a real funding
  ledger (subscription, signed attribution, day boundaries) is deliberately deferred to the
  full TS-P1-007/TS-P1-005 work. **This exclusion was explicitly ACCEPTED by Barış on
  2026-07-18 — recorded as `_AI_MEMORY/DECISIONS.md` entry D017** (revisit before any paper
  evidence cites the daily-loss gate, or if funding costs become material). The synthetic
  funding tests prove the code path only.
- **R-03 red-proof honesty:** the first repair round's "18/18 FAIL pre-repair" was
  constructor-signature-level (old `Store` lacked `clock=`); Codex's compatibility shim showed
  the semantic result was 14 failed / 4 passed. This round's red proof restores production
  files to `066b49cc` with the test file unchanged, so failures are semantic by construction.

## Third repair round after round-3 BLOCK (2026-07-18,
`CODEX_INTERIM_TSP1007_REAUDIT2_2026-07-18.md`)

- **Immutable fill identity:** `fill_id` is now insert-once. An exact payload redelivery is
  idempotent; a changed payload or cross-order reuse preserves the first row, emits
  `FILL_ID_CONFLICT`, and DISARMS. Exact fills may replay idempotent accounting after a
  prior transaction failure, but cannot duplicate partial- or full-close decisions.
- **Canonical closes cannot be rewritten:** a distinct SL/TP/CLOSE fill received after
  `trades.exit_ts` is set is retained as raw evidence, emits `POST_CLOSE_FILL`, and DISARMS;
  it cannot change exit price, net PnL, daily PnL, loss streak, or the single
  `TRADE_CLOSED` decision. Per-order and cross-order exit overfills similarly quarantine
  with `ORDER_OVERFILL` or `TRADE_OVERFILL` and leave the trade unclosed for reconciliation.
- **Live entry remainder ownership:** an exit that flattens only the currently filled entry
  cannot close the trade while an owned entry order still has fillable quantity. The trade
  remains open, `ENTRY_REMAINDER_LIVE` DISARMS the bridge, and a later entry fill remains
  attached to that trade across manager restart. Reconcile therefore reprotects or flattens
  broker exposure instead of classifying it as `FOREIGN_POSITION_IGNORED`.
- **Atomic terminal state:** the guarded trade-row close and its `TRADE_CLOSED` decision are
  one SQLite transaction. A forced decision-insert abort rolls back the trade close; exact
  fill redelivery after restart completes it once without duplicating the immutable fill.
- **Semantic gate proof:** the half-exit engine test now uses quantity 100, so the old phantom
  close would breach the default 2% daily-loss boundary while the corrected partial exit
  contributes nothing.

Focused evidence is **32 passed from both required CWDs**. The complete suite is **164 passed,
1 pre-existing Starlette deprecation warning from both CWDs**. The independently reproducible
old-code semantic red result and exact restore commands are recorded in the round-4 Fable audit
handoff. Funding treatment and all other interim limitations remain unchanged, including owner
decision D017.

## Interim semantics disclosed (audit F-05)

- The daily-loss percentage compares realized PnL against **current account equity at signal
  time**, not a persisted UTC day-start equity. `risk_days`/`day_start_equity` remain UNWIRED.
  If equity has risen intraday the gate triggers slightly late; if fallen, slightly early.
- PnL is **engine-derived** from fills; there is no broker-reconciled cross-check yet.
- Paper and dry-run share `data/bridge.db` by default; isolation is enforced at query level
  (repair 1). A dedicated per-environment DB path remains a TS-P2-007 concern.

## D017 update — TS-P1-005 captures funding, and this gate still does not use it

TS-P1-005 (`26_FULL_RECONCILIATION_CONTRACT.md`, owner decision D3=A) closes the *capture* half
of R-02: a full reconciliation cycle now reads the authoritative Hyperliquid funding ledger
(`Info.user_funding_history`), keys each event by the exchange-provided `hash`, stores the signed
`delta.usdc` with its `delta.coin` symbol and `time` effective timestamp, and appends it to the
opt-in v6 `funding_events` table with an explicit `ATTRIBUTED` / `UNATTRIBUTED` class.

**The interim gate above is deliberately unchanged by that.**

- `Store.trade_costs(decision_uid)` still reads **only** the `fills` table
  (`SUM(fills.fee) + SUM(fills.funding)`). It does not read `funding_events`.
- No production path populates `fills.funding`, so production gate PnL remains **gross − fees**,
  exactly as decided in D017.
- `funding_events` is evidence, not a risk input. Nothing consumes it before TS-P1-006 / full
  TS-P1-007.
- Double counting is therefore structurally impossible: the two stores are disjoint, and the
  funding ledger is a separate signed event stream rather than a synthesized fill.
- Regression proof: `tests/test_reconciliation.py::test_funding_ledger_does_not_change_the_interim_risk_result`
  populates `funding_events` through a real accepted capture and asserts `trade_costs` is
  numerically identical before, after, and following a reopen.
- The v6 ledger is opt-in and is not active on the default v4 operational database, so this note
  describes a capability, not a live change.

D017 remains in force for the interim gate. Whether funding should enter the daily-loss
calculation — and with which day boundary — stays a TS-P1-006 / full TS-P1-007 decision.

## Status and follow-up

Interim only. Broker-reconciled PnL, equity-stop, drawdown, day-start equity, and the full
snapshot feed remain the FULL TS-P1-007 behind TS-P1-005/006, which supersedes this wiring when
it lands. TS-P1-005 has now landed the reconciliation evidence half (opt-in, not activated);
risk consumption of that evidence is still TS-P1-006. Deploy of this fix is NOT authorized by
this document — independent audit first, then the standard deploy gate.

## TS-P1-006 update

TS-P1-006 now supplies v6 entry risk with one immutable reconciled
positions/balances/margin snapshot and removes the v6 point-account input.
This does **not** supersede the interim realized-PnL or consecutive-loss
calculation. Funding remains evidence only, the current UTC-day behavior and
numeric thresholds are unchanged, and broker-reconciled PnL/equity-stop/
drawdown policy remains TS-P1-007.
