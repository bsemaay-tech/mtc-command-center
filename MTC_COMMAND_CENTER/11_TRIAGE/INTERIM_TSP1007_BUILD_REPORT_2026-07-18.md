# Interim TS-P1-007 build report — 2026-07-18 (Claude Fable 5)

Authorization: Barış "start the interim TS-P1-007 fix" (2026-07-18); scope frozen in
`09_DOCS/ROADMAPS/TRADING_SYSTEM/05_IMPLEMENTATION_BACKLOG.md` amendment log.

- Worktree `C:\P1IF`, branch `feature/interim-daily-loss-wiring`, base `abda6717`
  (post-PR-#23 master — bridge tree byte-identical to deployed `74e0990b`).
- Commit: `6fa0c831` — exactly 5 files: `bridge/store/db.py` (+`realized_pnl_today`,
  `consecutive_closed_losses`, cross-run by design), `bridge/engine/engine.py` (evaluate() now
  receives both values), `bridge/engine/orders.py` (equity rows record real realized_today),
  `tests/test_interim_risk_wiring.py` (8 engine-path tests), `docs/20_INTERIM_TSP1007_RISK_WIRING.md`
  (contract + evidence).
- Test evidence: new tests 8/8 PASS; full suite **140 passed** (132 pre-existing + 8 new, zero
  regressions); pre-fix proof via stash of the 3 production files → **5/8 FAIL** on old code
  (3 pass-cases pass either way, expected). Exact commands and semantics in doc 20.
- No threshold, strategy, config, schema-version, scheduler, credential, exchange, or `C:\P2RT`
  action. `git -C C:\P2RT` untouched. Thresholds remain `max_daily_loss_pct=0.02`,
  `max_consecutive_losses=3` (pre-existing defaults; policy values remain Barış's).
- NOT pushed, NOT deployed. Next: independent audit (Codex Gate-style) on real code, then the
  standard deploy gate. Full TS-P1-007 (reconciled snapshot) still follows P1-005/006 and
  supersedes this wiring.

## Repair round after Codex audit BLOCK (same day)

Codex audit (`CODEX_INTERIM_TSP1007_AUDIT_2026-07-18.md`) returned **BLOCK** with findings
F-01..F-07. All required repairs implemented in commit **`066b49cc`** (same branch/worktree,
5 files):

- **F-01** environment isolation: helpers take `run_id`, join `trades`→`runs`, scope to
  mode+network; unknown run raises (fail closed); reconcile equity telemetry alone degrades to
  `0.0` on `LookupError` so pre-run reconciles keep working.
- **F-02** net PnL: `trades.pnl` = gross − `Store.trade_costs()` (fees+funding, debit-positive);
  `TRADE_CLOSED` records `pnl`/`pnl_gross`/`costs`.
- **F-03** fail-closed risk-input boundary: in-memory DISARM first; best-effort persist +
  `RISK_INPUT_FAILED` event + fail-silent notify; STICKY latch in `_app_state()` until human
  `arm()`; `status()` exposes `risk_input_error`, survives broken meta reads.
- **F-04** timestamp canonicalization (aware-UTC ISO at write, invalid raises, naive=UTC) +
  bounded `[midnight, next-midnight)` daily interval.
- **F-05** doc 20 amended: current-equity base, unwired `risk_days`, shared DB + query-level
  isolation, DB-failure behavior, non-retryable failed bar.
- **F-06** `Store(clock=...)` seam; all engine-path tests frozen-clock deterministic.
- **F-07** (NIT) index deferred to TS-P2-006 as the audit allowed.

Evidence: focused suite **18 passed**; full suite **150 passed in 17.38s** (regression the
repair initially exposed in `test_positions_and_reconcile_use_old_client_during_blocking_rebuild`
diagnosed — reconcile raising `LookupError` pre-run — and fixed); red-proof **18/18 FAIL** on
pre-repair `6fa0c831` production files via stash/pop, tree restored clean. Red-proof failures
are a mix of semantic and signature-level (`run_id`/`clock` params absent pre-repair) — stated
honestly. Still NOT pushed, NOT deployed. **Next: Codex re-audit** of `066b49cc`.

**Correction (per re-audit R-03):** the literal "18/18 FAIL" above was constructor-signature
level — every test stopped at the old `Store` lacking `clock=`. Codex's compatibility shim
showed the true semantic result was 14 failed / 4 passed. Recorded as inaccurate claim; the
round-2 red proof below is semantic by construction.

## Second repair round after re-audit BLOCK (same day)

Codex re-audit of `066b49cc` (`CODEX_INTERIM_TSP1007_REAUDIT_2026-07-18.md`) returned **BLOCK**
with R-01 (partial fills corrupt entry price/close state/PnL) and R-02 (production funding never
populated). Round-2 repair in commit **`3fa13f3e`** (4 files):

- **R-01:** cumulative fills-derived accounting — order FILLED only at full quantity (partials
  keep resting status), entry price = entry-fill VWAP, exits contribute actual quantity, close
  only at full flat (exit VWAP + net PnL + one idempotent `TRADE_CLOSED`), partial exits emit
  `TRADE_PARTIAL_EXIT` and contribute nothing to gates, duplicate fills coalesce on `fill_id`,
  order-row-only entry brokers fall back to prior behavior.
- **R-02:** code NOT changed (no fake funding source invented). Doc 20 now discloses production
  reality: gate PnL = gross − fees; funding ledger deferred. **Owner decision pending:** accept
  interim exclusion vs order a funding-ledger build (bigger scope, belongs with TS-P1-005).
- **R-03:** red-proof claims corrected here and in doc 20.

Evidence: 6 new tests; focused **24 passed from both CWDs**; full suite **156 passed**;
semantic red proof vs `066b49cc`: **5 failed / 19 passed** (half-exit engine-path case passes
both ways — old code's phantom full-close loss stayed inside the daily limit; stated honestly).
Process note: the red-proof `git restore` initially wiped the then-uncommitted repairs; they
were re-applied and re-verified before commit. NOT pushed, NOT deployed. **Next: Barış answers
the R-02 funding question → round-3 Codex re-audit of `3fa13f3e`.**
