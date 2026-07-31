# Codex independent adversarial re-audit — interim TS-P1-007 risk-gate wiring

Date: 2026-07-18  
Auditor: Codex GPT-5  
Builder: Claude Fable 5  
Audited worktree: `C:\P1IF`  
Audited branch: `feature/interim-daily-loss-wiring`  
Audited commit: `066b49cc1e40457169a32a26c6624005cba740ab`  
Repair parent: `6fa0c83153a79d5e43ca5c5f27ae6840163a2b57`  
Base: `abda67173964bb3dd0ce303ef07a699c691da7b9`

## Verdict: **BLOCK**

The six repairs requested by the first audit are substantially present and their stated green suites reproduce. Environment isolation, sticky fail-closed risk reads, canonical bounded timestamps, current-equity disclosure, the frozen clock, and the missing-run reconcile regression all passed direct inspection and execution.

The interim gate is still unsafe to deploy because its production PnL source is not correct for partial fills and does not receive real Hyperliquid funding. Both defects can make DAILY_LOSS or CONSECUTIVE_LOSS trigger wrongly or fail to trigger, which meets the prompt's mandatory BLOCK definition.

No deploy, push, runtime, scheduler, credential, network, exchange, testnet, paper, ARM/DISARM/KILL, threshold, config, schema, strategy, Pine, parity, or `C:\P2RT` action occurred.

## Findings

### R-01 — CRITICAL / BLOCK: partial fills corrupt persisted PnL and close state

Evidence:

- `IBKR_PAPER_BRIDGE/bridge/engine/orders.py:281-286` marks an order `FILLED` after every individual `FillEvent` and stores only that fill's quantity/price as the order totals.
- `orders.py:289-290` overwrites `trades.entry_px` with the latest entry fill; `bridge/store/db.py:669-677` does not calculate a quantity-weighted entry price.
- `orders.py:291-302` treats every exit fill as a complete close, calculates price PnL using the trade's full planned `qty`, and overwrites `exit_ts`/`pnl` on every later exit fill.
- `bridge/broker/hyperliquid.py:812-817` explicitly iterates and dispatches every fill in a broker message, so multiple fills are a supported production input shape.
- The 18 focused tests contain no split-entry or split-exit case.

Direct real-code probe through `OrderManager._ingest_fill`:

```text
split_entry true_pnl=0 persisted_pnl= -10.0 stored_entry_px= 110.0
split_exit after_first true_partial_pnl=-10 persisted_pnl= -20.0
split_exit final_true_pnl=0 persisted_pnl= 20.0
```

Concrete failure scenarios:

1. A two-unit entry filled at 100 and 110, then exited at 105, has true gross PnL 0. The code stores entry 110 and PnL -10, which can wrongly trip either gate.
2. A two-unit entry at 100, then one-unit exits at 90 and 110, has final gross PnL 0. The code first closes it at -20 and later overwrites it to +20. The first fill can wrongly trip a gate; the final value can erase a real loss or reset a streak.

Smallest safe required edit: make fill accounting cumulative. Derive entry filled quantity and entry VWAP from persisted fills; use each exit fill's actual quantity; accumulate exit gross and all costs; retain an open/partial trade until cumulative exit quantity reaches cumulative entry quantity; only then persist final exit timestamp, exit VWAP, net PnL, and `TRADE_CLOSED`. Order `filled_qty`, average price, and status must also be cumulative. Add split-entry, split-exit, mixed-price, fee, duplicate-fill, and restart tests. If this cannot be done without the wider order-lifecycle task, this interim deployment must wait for that task.

### R-02 — CRITICAL / BLOCK: production funding is always zero despite the net-PnL contract

Evidence:

- `bridge/engine/types.py:73-83` gives `FillEvent.funding` a default of `0.0`.
- `bridge/broker/hyperliquid.py:825-847` maps quantity, price, timestamp, and fee, but never maps funding into `FillEvent`.
- `hyperliquid.py:804-823` handles fill and order-update messages only; no production funding-ledger event is parsed or attributed.
- Repository-wide search found no other production writer of a nonzero funding value. The only nonzero funding values are synthetic test inputs in `tests/test_interim_risk_wiring.py:419-434`.
- The captured real fill fixture at `tests/test_hyperliquid_broker.py:1164-1200` proves fee parsing but contains no funding field and makes no funding assertion.
- The contract at `docs/20_INTERIM_TSP1007_RISK_WIRING.md:57-61` nevertheless claims net PnL includes `SUM(fills.funding)` under a Hyperliquid sign convention.

Direct parser probe, including a literal funding field:

```text
parser fee= 2.0 funding= 0.0
```

Concrete failure scenario: a position incurs a funding debit large enough to cross the daily loss threshold or turn a gross-flat/gross-win trade into a net loss. The persisted funding remains zero, daily loss is understated, and the loss streak can reset instead of incrementing.

Smallest safe required edit: wire an actual broker funding source into a persisted ledger with an explicit debit/credit sign and deterministic run/trade/day attribution, then consume it in the gate value. Add tests based on a captured real funding payload, including debit, credit, restart, and day-boundary cases. If funding is intentionally excluded from this interim control, the contract and tests must stop claiming it is included, but that scope change still requires explicit owner acceptance because the resulting gate is not net economic PnL.

### R-03 — MEDIUM: the claimed 18/18 red proof is constructor-signature proof, not semantic repair proof

With only the three production files restored to `6fa0c831`, the repaired test file does produce **18 failed in 1.19s**. Every test fails while constructing `Store(..., clock=...)`, because the old constructor does not accept `clock`; no gate assertion is reached. The build report's description of a semantic/signature mix is therefore inaccurate for the literal run.

A process-only compatibility shim that let the old Store accept and ignore `clock` produced **14 failed, 4 passed in 2.49s**. This is useful semantic red evidence, but it is not the claimed 18/18 proof.

Smallest required edit: record the literal red proof honestly and add a compatibility fixture or separate pre-repair semantic suite that can reach each repaired behavior. This evidence defect does not independently corrupt a gate, but it hides coverage quality.

### R-04 — NIT: the streak query should be indexed before materially larger history

In-memory timings on this host, using same-environment closed trades and 20 warmed measurements:

| Rows | Daily median | Streak median | Streak max |
| ---: | ---: | ---: | ---: |
| 1,000 | 0.125 ms | 0.529 ms | 0.969 ms |
| 10,000 | 1.341 ms | 6.495 ms | 7.177 ms |
| 100,000 | 12.788 ms | 76.061 ms | 87.981 ms |

`EXPLAIN QUERY PLAN` uses `idx_trades_run` for the daily lookup, while the streak path scans/index-walks all trades and builds a temporary B-tree for ordering. Present single-coin 1h volume does not make this a release blocker. Retain the existing TS-P2-006 follow-up for a suitable environment/time/order index or bounded latest-streak query.

## A. Scope integrity

Commands:

```text
git -C C:\P1IF rev-parse HEAD
git -C C:\P1IF rev-parse HEAD^
git -C C:\P1IF merge-base HEAD abda6717
git -C C:\P1IF diff --name-status 6fa0c831..066b49cc
git -C C:\P1IF diff --name-status abda6717..066b49cc
git -C C:\P1IF show --stat --oneline --summary 066b49cc
git -C C:\P1IF diff --check
```

Results:

- HEAD, parent, and merge-base were exactly `066b49cc...`, `6fa0c831...`, and `abda6717...`.
- The repair diff and the full base-to-target diff each contain exactly five paths: `bridge/store/db.py`, `bridge/engine/engine.py`, `bridge/engine/orders.py`, `tests/test_interim_risk_wiring.py`, and `docs/20_INTERIM_TSP1007_RISK_WIRING.md`.
- Target stat: **5 files changed, 491 insertions, 88 deletions** relative to `6fa0c831`.
- No config, strategy, schema/version, Pine, parity, `MTC_V2`, or protected path changed. `bridge/engine/risk.py` is byte-identical to base.
- Defaults remain `max_daily_loss_pct=0.02` and `max_consecutive_losses=3` at `bridge/engine/risk.py:14-21`.
- `git diff --check` passed and `C:\P1IF` was clean before and after all restoration/probe cycles.

## B. Pre-fix inertness

Independent `git show`/`git grep` on `abda6717` reconfirmed:

- `bridge/engine/engine.py:236-242` called `risk_engine.evaluate(...)` without `realized_today` or `consecutive_losses`.
- `bridge/engine/orders.py:151-158` hardcoded equity telemetry `realized_today=0.0`.
- `bridge/store/db.py:469` defined `upsert_risk_day`; there was no production caller. A direct Store unit-test call means “zero callers” is only accurate when qualified as production.
- `tests/test_risk.py:39-46` reached DAILY_LOSS only by directly injecting `realized_today=-25.0` into `RiskEngine.evaluate`.

The base was therefore inert through the operational engine path.

## C. Store-query attack results

### Environment scope and restart behavior

`Store._run_environment` and both queries at `bridge/store/db.py:455-510` correctly join `trades` to `runs` and scope by the current run's `mode` and `network`. Same-environment cross-run history remains restart-proof; dry-run/replay rows no longer pollute paper rows. Unknown runs raise `LookupError`.

Source configuration still defaults all modes to `data/bridge.db` (`bridge/app.py:65`), so isolation is query-level. A manually created unrelated `paper/testnet` run in that same file will deliberately share gate history. That is acceptable for restart continuity only if the DB is not reused for unrelated same-environment experiments.

### Timestamp and NULL attacks

- `_to_iso` at `db.py:12-22` parses all accepted strings and emits aware UTC ISO. Probes normalized `Z`, space-separated, offset, and naive strings to the same canonical form; invalid text raised `ValueError`.
- The sole production `update_trade_exit` caller is `orders.py:302`, passing `FillEvent.ts`; Hyperliquid creates an aware UTC datetime at `hyperliquid.py:836-844`.
- `realized_pnl_today` uses `[UTC midnight, next midnight)`, excluding future-day rows.
- Naive datetimes and injected `now` are consistently treated as UTC. DST/local-host conversion no longer enters the calculation.
- Open trades with NULL exit/PnL are ignored. Exact `pnl=0.0` contributes zero to the daily sum and correctly breaks a negative streak.

These items repair prior F-01/F-04/F-06. The consumed `trades.pnl` value is nevertheless unreliable under R-01/R-02.

## D. Engine wiring, gate order, and fail-closed behavior

Gate order remains armed state, feed readiness, open position, direction, account, DAILY_LOSS, CONSECUTIVE_LOSS, leverage, stop validity, minimum order, notional, and margin (`bridge/engine/risk.py:56-121`). Exact daily boundary behavior was reproduced with defaults:

```text
limit=2000 pnl=-2000 accepted=False rejection=DAILY_LOSS_LIMIT disarm=True
limit=2000 pnl=-1999 accepted=True rejection=None disarm=False
```

At either loss gate, `RiskResult.disarm=True` still drives `RISK_REJECT`, DISARM, and `RISK_AUTO_DISARM`.

The repaired risk-read boundary at `engine.py:240-243,326-347,488-498` is operationally fail closed: an exception blocks submission, sets in-memory DISARMED first, latches `risk_input_error`, performs best-effort persistence/event/notification, and remains visibly disarmed even if database writes fail. Direct unknown-run engine probe:

```text
state= DISARMED submitted= 0 error= LookupError: run not found for risk scoping: missing-risk-run
```

The failed bar remains non-retryable, as now documented. Human `arm()` is the only latch clear and performs reconcile/current-state checks first.

The requested regression distinction is correct. `OrderManager.reconcile` at `orders.py:150-165` catches only a missing-run `LookupError` for the non-authoritative equity telemetry row and falls back to `0.0`; other database errors still propagate. The engine risk path does not use that fallback and fails closed as above.

## E. Independently reproduced test evidence

### Bridge-root matrix (`C:\P1IF\IBKR_PAPER_BRIDGE`)

```text
python -m pytest tests/test_interim_risk_wiring.py -q
18 passed in 1.39s

python -m pytest tests/test_hyperliquid_broker.py::test_positions_and_reconcile_use_old_client_during_blocking_rebuild -q
1 passed in 0.91s

python -m pytest tests -q
150 passed, 1 warning in 14.50s
```

After all restoration/probe work, a final bridge-root rerun produced **18 passed in 1.99s** and the regression test **1 passed in 0.72s**.

### Repository-root matrix (`C:\P1IF`)

```text
python -m pytest IBKR_PAPER_BRIDGE/tests/test_interim_risk_wiring.py -q
18 passed in 1.37s

python -m pytest IBKR_PAPER_BRIDGE/tests/test_hyperliquid_broker.py::test_positions_and_reconcile_use_old_client_during_blocking_rebuild -q
1 passed in 0.87s

python -m pytest IBKR_PAPER_BRIDGE/tests -q
150 passed, 1 warning in 13.92s
```

The sole full-suite warning was the existing Starlette TestClient deprecation warning. There were zero failures.

### Repair red proof

Because the repair is committed and the worktree was clean, there was no uncommitted fix for `git stash` to remove. The bounded equivalent was:

```text
git restore --source=6fa0c831 --worktree -- \
  IBKR_PAPER_BRIDGE/bridge/store/db.py \
  IBKR_PAPER_BRIDGE/bridge/engine/engine.py \
  IBKR_PAPER_BRIDGE/bridge/engine/orders.py
python -m pytest IBKR_PAPER_BRIDGE/tests/test_interim_risk_wiring.py -q
git restore --source=HEAD --worktree -- <same three paths>
git diff --exit-code HEAD -- <same three paths>
```

Raw result: **18 failed in 1.19s**, pytest exit 1; restore diff exit 0; final tree clean. All 18 literal failures occurred at the missing `clock=` constructor seam, so see R-03.

To reach semantics, I repeated the old-production run with a process-only constructor compatibility shim. Raw result: **14 failed, 4 passed in 2.49s**. The failures reached daily trigger, restart, isolation, unknown-run, fee/funding, net-streak, failure-boundary, timestamp, and equity assertions. No source file was written by the shim.

### Additional adversarial probes

- Split entry and split exit through the actual persisted fill path: reproduced R-01.
- Hyperliquid fill parser with a literal `funding=7`: parsed funding remained `0.0`, reproducing R-02.
- Unknown-run direct `on_bar`: DISARMED, zero submits, latched LookupError.
- Missing-run pre-run reconcile: regression test passes with telemetry-only `0.0` fallback.
- Timestamp variants: canonical UTC output; invalid string rejected.
- Performance: 1K/10K/100K in-memory rows plus `EXPLAIN QUERY PLAN`; see R-04.

One first compatibility-shim attempt was invalid because the repository-root invocation lacked the bridge import path; it was restored clean and not counted. One first combined partial-fill probe produced its valid first result but then hit a Windows temporary-file cleanup error because the SQLite Store was not closed; the corrected closed-Store probe above completed and is the evidence cited.

## F. Interim gaps and documentation audit

Correctly disclosed at `docs/20_INTERIM_TSP1007_RISK_WIRING.md:75-89`:

- current account equity, not persisted day-start equity, is the percentage base;
- `risk_days`/`day_start_equity` are unwired;
- PnL is engine-derived with no broker-reconciled cross-check;
- paper and dry-run share a DB and are isolated by query;
- equity-stop, drawdown, day-start equity, full snapshot feed, and full TS-P1-007 remain behind TS-P1-005/006;
- deployment remains separately gated.

Undocumented material gaps:

- the engine-derived PnL assumes one full entry and one full exit, while production accepts multiple fills (R-01);
- funding is not populated from any production broker path despite the contract claiming it is included (R-02).

Those are findings rather than notes because they directly weaken both interim gates.

## Required repair set before another re-audit

1. Make entry/exit/order accounting correct and restart-safe for partial fills; add engine-path split-fill tests that fail on `066b49cc`.
2. Capture real Hyperliquid funding from an evidenced broker payload/ledger path with explicit signs and attribution; add captured-payload and gate tests that fail on `066b49cc`.
3. Correct the red-proof claim and provide semantic pre-repair evidence that reaches each intended repair.
4. Amend doc 20 to disclose the partial-fill lifecycle and actual funding source/limitations accurately.
5. Rerun focused, regression, and full suites from both working directories; repeat bounded red/green proof; request an independent re-audit.

Deployment remains a separate Barış-gated step after a non-BLOCK verdict. Do not combine it with repair, push, PR, or monitoring-window work.

## Skipped / constrained checks

- `C:\P2RT` was not accessed. Deployed files, DB contents, processes, scheduler, and live configuration were not inspected.
- No network/API/SDK documentation lookup was performed because the prompt prohibited network action. Funding conclusions are limited to the complete local production paths and captured fixtures under audit.
- No production database benchmark was run; performance was measured in-memory only.
- Cline was attempted for a read-only mechanical cross-check, but its hub closed with code 1006 before output. `_deepseek_driver` was not used because its required task/report files would violate the audit's no-extra-write boundary.
- No source/config/test was edited. The only writes are this requested report and the three requested canonical handoff updates.
