# CODEX PROMPT — Independent adversarial audit of interim TS-P1-007 (risk-gate wiring)

> **ROUND 3 (2026-07-18, after second BLOCK):** target commit is now **`b11a2e36`**
> (= `3fa13f3e` R-01 cumulative partial-fill accounting, 4 files, plus one docs-only commit
> recording D017; expected diff vs `066b49cc` = same 4 files).
> **R-02 is RESOLVED BY OWNER DECISION, not code:** Barış accepted the interim funding
> exclusion on 2026-07-18 — recorded as `_AI_MEMORY/DECISIONS.md` **D017** and in doc 20.
> Audit that the disclosure matches production reality (gross − fees); a funding ledger is
> explicitly OUT of this interim scope and its absence is no longer a BLOCK condition.
> Focused suite now **24 tests**; full suite now **156 tests**. Red proof: restore
> `bridge/store/db.py` + `bridge/engine/orders.py` to `066b49cc` → expect **5 failed / 19
> passed** semantically (split entry/exit, fees, duplicate, restart; the half-exit engine-path
> case passes both ways — verify why and confirm that is benign). R-02 note: production funding
> remains unpopulated BY DESIGN pending Barış's decision (doc 20 §"Second repair round"
> discloses gross−fees semantics); audit the DISCLOSURE's accuracy, not a funding ledger,
> unless Barış has ordered one. Verify R-01 against your own split-entry/split-exit
> reproductions, attack VWAP/duplicate/restart/mixed-role edges, and re-verify that partial
> order status preservation does not break reprotect/grace logic. Report:
> `CODEX_INTERIM_TSP1007_REAUDIT2_2026-07-18.md`.
>
> **RE-AUDIT ROUND (2026-07-18, after BLOCK):** target commit was **`066b49cc`**
> (repairs for F-01..F-06 on top of `6fa0c831`; expected diff = 5 files). Verify every
> "Required repair set" item from your own `CODEX_INTERIM_TSP1007_AUDIT_2026-07-18.md`
> against real code and rerun all evidence: focused suite now **18 tests**, full suite now
> **150 tests**, red-proof = stash the three production files to `6fa0c831` state → expect
> 18/18 FAIL → restore. Sections A–F below still apply with these updated numbers. Also verify
> the repair of the regression in
> `tests/test_hyperliquid_broker.py::test_positions_and_reconcile_use_old_client_during_blocking_rebuild`
> (pre-run reconcile must tolerate a missing run row via telemetry fallback ONLY — the engine
> risk path must still fail closed on unknown `run_id`). Write the new report as
> `CODEX_INTERIM_TSP1007_REAUDIT_2026-07-18.md`.

Date: 2026-07-18. Requested by Barış. Builder was Claude Fable 5, so YOU (Codex) are the
independent auditor this round. Audit on real code and real test runs — never on the builder's
report alone. Assume the report may overstate; your job is to try to break the change.

## Context (read first, in this order)

1. `MTC_COMMAND_CENTER/11_TRIAGE/INTERIM_TSP1007_BUILD_REPORT_2026-07-18.md` — build claims.
2. `C:\P1IF\IBKR_PAPER_BRIDGE\docs\20_INTERIM_TSP1007_RISK_WIRING.md` — contract + evidence.
3. `MTC_COMMAND_CENTER/09_DOCS/ROADMAPS/TRADING_SYSTEM/05_IMPLEMENTATION_BACKLOG.md` — amendment
   log at the end = the approved scope (Barış decision 2026-07-18).
4. `_AI_MEMORY/GLOBAL_HANDOFF.md` entries dated 2026-07-18.

## What was built

- Worktree: `C:\P1IF`, branch `feature/interim-daily-loss-wiring`, base `abda6717`
  (post-PR-#23 master; bridge tree byte-identical to deployed `74e0990b`).
- Commit under audit: `6fa0c831` — claimed scope exactly 5 files:
  `bridge/store/db.py`, `bridge/engine/engine.py`, `bridge/engine/orders.py`,
  `tests/test_interim_risk_wiring.py`, `docs/20_INTERIM_TSP1007_RISK_WIRING.md`.
- Claim: previously-inert DAILY_LOSS and CONSECUTIVE_LOSS gates now receive real persisted
  values through the operational engine path; equity rows record real `realized_today`;
  no threshold/strategy/config/schema change.

## Mandatory verifications (each with evidence in your report)

**A. Scope integrity.**
`git -C C:\P1IF show --stat 6fa0c831` — confirm exactly the 5 files, nothing else. Confirm no
change to `RiskConfig` defaults, strategy files, `bridge.yaml`, schema version, or protected
paths. Confirm branch base is `abda6717`.

**B. Pre-fix inertness (independently reproduce).**
On base `abda6717` (use `git show abda6717:<path>`): confirm `engine.py` called
`risk_engine.evaluate()` without `realized_today`/`consecutive_losses`; `orders.py` hardcoded
`realized_today=0.0`; `Store.upsert_risk_day` had zero callers; `tests/test_risk.py` exercised
DAILY_LOSS only via direct parameter injection.

**C. Attack the new store queries (`Store.realized_pnl_today`, `Store.consecutive_closed_losses`).**
Try to construct failing inputs, at minimum:
1. ISO-string comparison: `exit_ts` is stored via `_to_iso` (UTC isoformat). Is lexicographic
   `exit_ts >= day_start_iso` correct for every value the code can persist — including strings
   passed through unchanged by `_to_iso(value: str)` (callers could store non-UTC or
   differently-formatted strings)? Check every `update_trade_exit` call site for what it
   actually passes.
2. Timezone: naive datetimes, DST-irrelevant UTC handling, `now` injection.
3. NULL semantics: open trades (NULL exit_ts/pnl), pnl exactly 0.0 (must break the loss streak,
   must count toward the daily sum).
4. Cross-run inclusion is BY DESIGN (restart-proofing). Adversarial question: in the production
   `bridge.db`, could non-paper rows (dry_run/replay/test runs sharing the same DB file) pollute
   the daily sum or streak? Inspect how run modes and DB paths are separated in deployed config
   and state your conclusion.
5. Performance: both queries run per accepted signal. Full-table scan on `trades` — bound the
   cost at realistic row counts and state whether an index is needed now or is a NIT.

**D. Attack the engine wiring.**
Gate order in `RiskEngine.evaluate` vs the new inputs; `RiskResult.disarm` path still produces
DISARM + `RISK_AUTO_DISARM`; DB failure inside the two new store calls during `on_bar` — what
happens (exception propagation, engine state), and is that acceptable fail-closed behavior?

**E. Reproduce all test evidence yourself (do not trust reported numbers).**
From `C:\P1IF\IBKR_PAPER_BRIDGE`:
1. `python -m pytest tests/test_interim_risk_wiring.py -q` → expect 8 passed.
2. `python -m pytest tests -q` → expect 140 passed, zero failures.
3. Repeat both from repo root `C:\P1IF` (CWD-fragility convention of this repo).
4. Pre-fix proof: stash the 3 production files, rerun the new tests, expect 5 FAIL / 3 PASS,
   `git stash pop`, confirm working tree restored and `git status` clean afterward.
5. Boundary math: independently verify the test constants (equity 100000, default
   `max_daily_loss_pct=0.02` → limit 2000; trigger uses `<=`).
6. Midnight flake: assess `_today_base()` for a UTC-midnight race; classify severity honestly.

**F. Gaps the interim fix intentionally leaves (confirm they are DOCUMENTED, not hidden).**
Engine-derived PnL only (no broker-reconciled cross-check), no equity-stop/drawdown, no
`risk_days`/day-start-equity wiring, full TS-P1-007 still owed behind P1-005/006. If any
undocumented gap materially weakens the two gates, that is a finding, not a note.

## Hard boundaries

Read-only plus test execution. NO deploy, NO push, NO edits to any file (if you find defects,
list REQUIRED EDITS — do not fix them yourself), NO `C:\P2RT` access, NO scheduler / credential /
exchange / testnet / paper / ARM action, NO threshold changes. `SESSION_LOG.md` is retired — do
not write it.

## Report

Write `MTC_COMMAND_CENTER/11_TRIAGE/CODEX_INTERIM_TSP1007_AUDIT_2026-07-18.md`:

- Verdict: **PASS** / **PASS-WITH-NITS** / **BLOCK** (BLOCK = any defect that lets either gate
  fail to trigger, trigger wrongly, or corrupt state).
- Findings ranked by severity, each with `file:line`, concrete failure scenario, and the
  smallest required edit.
- Exact commands run and raw pass/fail counts for every item in E.
- Explicit statement of anything you skipped and why.

Update `_AI_MEMORY/GLOBAL_HANDOFF.md`, `NEXT_STEPS.md`, `ACTIVE_FILES.md` (D/M/R discipline).
Deploy remains a separate Barış-gated step after your verdict; do not recommend skipping it.
