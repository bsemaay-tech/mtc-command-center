# Codex independent adversarial audit — interim TS-P1-007 risk-gate wiring

Date: 2026-07-18  
Auditor: Codex GPT-5  
Builder: Claude Fable 5  
Audited worktree: `C:\P1IF`  
Audited commit: `6fa0c83153a79d5e43ca5c5f27ae6840163a2b57`  
Base: `abda67173964bb3dd0ce303ef07a699c691da7b9`

## Verdict: **BLOCK**

The intended engine-path wiring exists and the reported 8-test and 140-test suites reproduce from both supported working directories. The change is nevertheless not safe to deploy. Two independently reproduced defects violate the audit's BLOCK rule:

1. the new cross-run queries also cross runtime modes, while paper and dry-run default to the same SQLite file, so dry-run/replay rows can wrongly trip or reset paper gates; and
2. the persisted `trades.pnl` used by both gates excludes fees and funding even though those costs are captured, so a net losing trade can be recorded as zero or a win and both gates can fail to trigger.

A database-read failure also leaves the engine visibly `ARMED`, marks the bar processed, and emits no risk rejection or auto-disarm event. No deploy, push, runtime, scheduler, credential, exchange, testnet, paper, ARM, DISARM, or `C:\P2RT` action was performed.

## Findings

### F-01 — CRITICAL / BLOCK: dry-run and paper trades contaminate each other's gates

Evidence:

- `IBKR_PAPER_BRIDGE/bridge/app.py:64-73` uses `data/bridge.db` for both normal paper startup and `--dry-run`; only the run ID/mode label changes.
- `IBKR_PAPER_BRIDGE/bridge/store/db.py:451-481` queries every closed row in `trades` and neither joins `runs` nor filters `runs.mode` or `runs.network`.
- The schema records the mode in `runs.mode` at `bridge/store/db.py:61-68`, so the information needed for isolation exists but is unused.
- In-memory reproduction on the audited code: one `runs.mode='dry_run'` closed trade with PnL `-2000` made `realized_pnl_today(...)` return `-2000.0` and `consecutive_closed_losses()` return `1` for the shared store before a paper run.

Concrete failure scenario: an operator launches `python -m bridge.app --dry-run` from the deployed checkout. The replay writes to the same `data/bridge.db`. A replay loss can later auto-disarm paper incorrectly; a replay win or zero-PnL close can also reset a real paper consecutive-loss streak. This is not the approved restart-proofing behavior; it is environment contamination.

Smallest required edit: preserve cross-`run_id` restart behavior but scope both helpers to the current run's environment. Pass the current `run_id` (or explicit mode/network) into the helpers, join `trades` to `runs`, and include only rows with the same mode and network. Add mixed paper/dry-run/live fixtures proving losses and wins cannot cross the boundary while same-mode restarts still do. A later dedicated DB path per environment remains desirable under TS-P2-007, but query isolation is required now.

### F-02 — CRITICAL / BLOCK: fee/funding losses are omitted from the PnL source used by both gates

Evidence:

- `IBKR_PAPER_BRIDGE/bridge/engine/orders.py:264-273` persists `FillEvent.fee` and `FillEvent.funding`.
- `IBKR_PAPER_BRIDGE/bridge/engine/orders.py:284-290` computes trade PnL only as price delta × quantity × direction and passes that gross value to `update_trade_exit`.
- `IBKR_PAPER_BRIDGE/bridge/store/db.py:458-480` uses that gross `trades.pnl` for both daily PnL and loss-streak classification.
- In-memory reproduction through the actual `_ingest_fill` path: a flat close at entry price with `fee=25.0` persisted `trade.pnl=0.0`; `consecutive_closed_losses()` returned `0`. Economically the trade lost 25.

Concrete failure scenario: three gross-flat or small-gross-win trades that are net losers after entry/exit fees or funding are classified as non-losses. They break the consecutive-loss streak and understate daily loss, allowing a new order after the configured limits should have blocked it.

Smallest required edit: define and persist canonical net realized PnL, including all entry/exit fees and signed funding for the trade, then make both helpers consume that value. Add engine-path tests for fee-only loss, gross-win/net-loss, funding debit/credit, and restart persistence. Document the exact sign convention. Broker reconciliation can remain a later cross-check, but already-captured costs cannot be discarded from the interim engine-derived number.

### F-03 — HIGH: risk-query database failure is order-safe for that bar but not an acceptable operational fail-closed state

Evidence:

- `IBKR_PAPER_BRIDGE/bridge/engine/engine.py:236-244` calls both store helpers outside any error boundary.
- `IBKR_PAPER_BRIDGE/bridge/engine/engine.py:184-190` marks the timestamp processed before those reads.
- `IBKR_PAPER_BRIDGE/bridge/engine/bars.py:134-141,208-217` schedules `on_bar` as a detached task; it does not observe task exceptions.
- Forced `sqlite3.DatabaseError` reproduction: exception propagated, no order submitted, but state remained `ARMED`, processed-bar count became 1, the only decision stage was `SIGNAL`, and there was no `RISK_AUTO_DISARM` event.

Concrete failure scenario: a transient or persistent SQLite read failure silently drops a signal while the dashboard continues to report `ARMED`; the bar cannot be retried because it is already in `_processed_bar_ts`. The absence of an order is fail-closed at the individual submit boundary, but the engine state and audit trail are not fail-closed.

Smallest required edit: add a tested risk-input failure boundary that blocks submission, makes the unhealthy/disarmed state observable even if SQLite itself cannot accept another write, emits an out-of-band notification, and defines whether the bar is retryable. Do not reuse `disarm()` blindly if its persistence write can fail through the same broken connection.

### F-04 — MEDIUM: timestamp comparison is not correct for every value the Store API accepts

Evidence:

- `_to_iso` returns string inputs unchanged at `IBKR_PAPER_BRIDGE/bridge/store/db.py:12-19`.
- The daily query compares text lexicographically and has no upper bound at `db.py:451-463`.
- A valid instant written as `2026-07-17T23:30:00-02:00` (2026-07-18 01:30 UTC) was wrongly excluded from the July 18 UTC sum.
- A valid SQLite/Python-style string `2026-07-18 01:00:00` was also wrongly excluded because the space sorts before `T`.
- A future close on July 19 was wrongly included in a July 18 query because the predicate is only `exit_ts >= day_start`.
- On this host, naive `now=datetime(2026,7,18,1)` was interpreted in Eastern European Summer Time while `_to_iso` treats naive stored datetimes as UTC; a July 17 23:00 UTC loss was consequently included.

All production `update_trade_exit` calls were inspected. The sole production caller is `bridge/engine/orders.py:290`, and it passes `FillEvent.ts`; `FillEvent.ts` is typed as `datetime` at `bridge/engine/types.py:73-83`. Hyperliquid constructs an aware UTC datetime at `bridge/broker/hyperliquid.py:836-844`. The other callers are tests at `tests/test_store.py:54` and `tests/test_interim_risk_wiring.py:128`. Therefore the offset/string issue is not currently reachable through the audited production fill path, but the public Store contract explicitly accepts strings and the missing upper bound is independently real.

Smallest required edit: normalize every accepted timestamp string to an aware UTC ISO form at write time (or reject noncanonical strings), treat naive values consistently as UTC, and query the half-open UTC interval `[day_start, next_day_start)`. Add offset, `Z`, space-separated, naive, and future-row tests. Apply the same canonical ordering guarantee to the streak query.

### F-05 — MEDIUM: day-start-equity / `risk_days` omission is not explicitly documented

Evidence:

- `IBKR_PAPER_BRIDGE/bridge/engine/risk.py:73-84` compares realized PnL against the current account equity, not a persisted UTC day-start equity.
- `IBKR_PAPER_BRIDGE/bridge/store/db.py:160-168` already contains `risk_days.day_start_equity`, but the interim change does not wire it.
- `docs/20_INTERIM_TSP1007_RISK_WIRING.md` documents engine-derived PnL, missing broker reconciliation, missing equity-stop/drawdown, and the later full snapshot, but does not explicitly say that `risk_days` and day-start equity remain unwired or that the interim percentage uses current equity.

Concrete failure scenario: if current equity rises from 100,000 to 110,000, a realized loss of 2,100 does not trigger a nominal 2% day-start limit; if it falls to 90,000, a loss of 1,900 triggers early. This is an intentionally deferred full-TS-P1-007 concern, but the interim contract currently overstates the precision of the daily percentage gate by omission.

Smallest required edit: explicitly document current-equity semantics and the unwired `risk_days`/day-start-equity limitation in doc 20 and the build report. Keep the full authoritative correction behind TS-P1-005/006 as approved; do not invent a new threshold in this repair round.

### F-06 — LOW: `_today_base()` can flake across UTC midnight

`IBKR_PAPER_BRIDGE/tests/test_interim_risk_wiring.py:105-108` captures a timestamp near `now`, but the production helper calls `datetime.now(UTC)` later. If the test seeds just before midnight and evaluates just after midnight, the seeded loss becomes yesterday. Trigger, restart, and equity-row tests can fail nondeterministically in that narrow window.

Smallest required edit: inject/freeze the same clock for seeding and store queries, or add a Store clock seam used by the engine-path tests. Do not stabilize it by relying on future timestamps, because F-04 requires a future upper bound.

### F-07 — NIT: full scans are acceptable now but should be indexed before materially larger history

`EXPLAIN QUERY PLAN` shows `SCAN trades` for the daily sum and `SCAN trades` plus `USE TEMP B-TREE FOR ORDER BY` for the streak. In-memory timings on this host:

| Closed rows | Daily sum | Worst-case all-loss streak |
| ---: | ---: | ---: |
| 1,000 | 0.142 ms | 1.126 ms |
| 10,000 | 1.062 ms | 7.706 ms |
| 100,000 | 9.476 ms | 88.463 ms |

The queries execute only when a signal reaches risk evaluation; for the present single-coin 1h bridge, even 100,000 closed trades is far beyond near-term realistic history. No index is required to unblock this interim repair. Track an index/query-shape benchmark under TS-P2-006 or add it if mixed-mode joins materially change latency.

## A. Scope integrity

`git -C C:\P1IF show --stat 6fa0c831` and `git diff --name-status abda6717..6fa0c831` independently confirmed exactly five paths:

- `IBKR_PAPER_BRIDGE/bridge/engine/engine.py` — +2
- `IBKR_PAPER_BRIDGE/bridge/engine/orders.py` — +1/-1
- `IBKR_PAPER_BRIDGE/bridge/store/db.py` — +32
- `IBKR_PAPER_BRIDGE/docs/20_INTERIM_TSP1007_RISK_WIRING.md` — +55
- `IBKR_PAPER_BRIDGE/tests/test_interim_risk_wiring.py` — +313

`git rev-parse 6fa0c831^` and `git merge-base 6fa0c831 abda6717` both returned `abda67173964bb3dd0ce303ef07a699c691da7b9`. `git diff --check` passed. No `RiskConfig` default, `risk.py`, strategy, `bridge.yaml`, schema version, Pine, parity, `MTC_V2`, or other protected path changed. Defaults remain `max_daily_loss_pct=0.02` and `max_consecutive_losses=3` at `bridge/engine/risk.py:14-21`.

## B. Pre-fix inertness

Independent `git show`/`git grep` evidence on `abda6717`:

- `bridge/engine/engine.py:236-242` called `risk_engine.evaluate(...)` without `realized_today` or `consecutive_losses`.
- `bridge/engine/orders.py:151-158` persisted `realized_today=0.0`.
- `bridge/store/db.py:469` defined `upsert_risk_day`; the only other repository hit was the direct Store unit call in `tests/test_store.py:56`. There was no production caller.
- `tests/test_risk.py:39-46` exercised DAILY_LOSS only by passing `realized_today=-25.0` directly to `RiskEngine.evaluate`.
- Temporarily restoring only the three production files from `abda6717` made the new suite fail **5 failed, 3 passed**, then restoring from `HEAD` returned the tree to clean.

The builder's phrase “zero callers” is accurate for production but not literally repository-wide because `tests/test_store.py` calls the helper directly.

## C. Store-query attack summary

| Attack | Result |
| --- | --- |
| Canonical aware UTC datetimes from actual fill path | Lexicographic ordering is correct because `_to_iso` emits fixed UTC ISO strings. |
| String inputs accepted unchanged | Incorrect for offset dates and alternate separators; reproduced. |
| Naive persisted datetime | `_to_iso` treats it as UTC. |
| Naive injected `now` | `astimezone(UTC)` treats it as host-local; inconsistent and reproduced. |
| UTC day range | Lower bound only; future rows are included. |
| Open trade (`exit_ts`/`pnl` NULL) | Correctly ignored. |
| `pnl=0.0` | Included in daily sum and correctly breaks the negative streak. |
| Same-mode restart | Works and is covered by the new tests. |
| Cross-mode shared DB | Incorrect; dry-run/paper pollution reproduced (F-01). |
| Fees/funding | Incorrectly omitted from the consumed PnL (F-02). |
| Performance | NIT at current scale; see F-07. |

## D. Engine wiring and disarm path

Gate order in `bridge/engine/risk.py:56-121` is: armed state, feed readiness, no open position, direction, account, daily loss, consecutive loss, leverage, stop validity, minimum order, notional, margin. The new values are supplied before evaluation at `bridge/engine/engine.py:236-244`.

At either configured boundary, `_reject(..., disarm=True)` still creates `RiskResult.disarm=True` (`risk.py:83-89,149-157`). `engine.py:245-257` writes `RISK_REJECT`, calls `disarm()`, and writes `RISK_AUTO_DISARM`. The focused boundary test reproduced this path.

A failure in either new Store read propagates before `RiskEngine.evaluate`; no submit occurs. That is order-safe for the affected bar, but engine state remains `ARMED`, the bar is already marked processed, and no rejection/disarm event exists. This is not an acceptable complete fail-closed operational contract; see F-03.

## E. Independently reproduced test evidence

### Post-fix focused and full suites

From `C:\P1IF\IBKR_PAPER_BRIDGE`:

```text
python -m pytest tests/test_interim_risk_wiring.py -q
8 passed in 1.20s

python -m pytest tests -q
140 passed, 1 warning in 20.78s
```

From `C:\P1IF`:

```text
python -m pytest IBKR_PAPER_BRIDGE/tests/test_interim_risk_wiring.py -q
8 passed in 0.82s

python -m pytest IBKR_PAPER_BRIDGE/tests -q
140 passed, 1 warning in 20.25s
```

The sole warning in each full run was `StarletteDeprecationWarning` from FastAPI/Starlette TestClient import. After the pre-fix restoration cycle, the focused suite was rerun from the bridge root: **8 passed in 0.71s**.

### Pre-fix proof

The literal stash workflow was not applicable because `6fa0c831` is committed and the worktree was clean: there were no uncommitted production changes for `git stash` to remove. I used this bounded equivalent from `C:\P1IF`:

```text
git restore --source=abda6717 --worktree -- \
  IBKR_PAPER_BRIDGE/bridge/store/db.py \
  IBKR_PAPER_BRIDGE/bridge/engine/engine.py \
  IBKR_PAPER_BRIDGE/bridge/engine/orders.py
python -m pytest IBKR_PAPER_BRIDGE/tests/test_interim_risk_wiring.py -q
git restore --source=HEAD --worktree -- <same three paths>
git diff --exit-code HEAD -- <same three paths>
```

Raw result: **5 failed, 3 passed in 1.01s**, pytest exit 1; final restore diff exit 0; `git status` clean. Failed tests were daily-loss trigger, consecutive-loss trigger, restart persistence, reconcile equity row, and Store helpers.

One earlier attempt was invalid because it was launched from `C:\P1IF\IBKR_PAPER_BRIDGE` with repo-root-prefixed pathspecs. Git returned `pathspec ... did not match`; the fixed code therefore reported 8 passed. No file changed. This invalid attempt is not counted as pre-fix evidence.

### Boundary math

Exact command:

```text
python -c "from bridge.engine.risk import RiskConfig; e=100000.0; c=RiskConfig(); limit=e*c.max_daily_loss_pct; print(f'equity={e:.1f} max_daily_loss_pct={c.max_daily_loss_pct:.2f} limit={limit:.1f} boundary={-limit:.1f}')"
```

Raw output: `equity=100000.0 max_daily_loss_pct=0.02 limit=2000.0 boundary=-2000.0`. `bridge/engine/risk.py:83` uses `realized_today <= -(equity * max_daily_loss_pct)`, so exactly `-2000` triggers and `-1999` does not. The focused engine-path tests reproduced both sides.

### Midnight assessment

`_today_base()` uses one captured `now`, so it has no internal double-read race. The race is between its seed timestamp and the later production query's independent clock read. Severity: LOW test flake only; it does not alter production gate math. See F-06.

## F. Interim gaps and documentation audit

Documented in `docs/20_INTERIM_TSP1007_RISK_WIRING.md`:

- engine-derived trade PnL is the interim source;
- no broker-reconciled PnL cross-check;
- no equity stop or drawdown;
- the full snapshot feed/full TS-P1-007 remains behind TS-P1-005/006 and supersedes the interim wiring;
- deploy requires a separate gate.

Not explicitly documented:

- `risk_days` and day-start equity are unwired; current equity is the percentage base (F-05);
- engine-derived PnL excludes captured fees/funding (F-02);
- the default DB path is shared across paper and dry-run while the helpers cross all modes (F-01);
- risk-input database failure leaves the engine `ARMED` without a risk failure event (F-03).

The first item is an approved full-TS-P1-007 deferral that needs honest documentation. The other three materially weaken or misstate the interim gates and require code/tests before re-audit.

## Required repair set before re-audit

1. Isolate daily/streak aggregation by current run environment while preserving same-mode restart history; add mixed-mode engine-path tests.
2. Make persisted realized PnL net of all captured fees/funding with explicit signs; add net-loss gate and streak tests.
3. Add an observable, tested fail-closed boundary for failures in either risk-input query.
4. Canonicalize accepted timestamps and use a bounded UTC-day interval; add adversarial timestamp tests.
5. Amend doc 20 to disclose current-equity/day-start semantics, mode isolation, cost inclusion, and DB-failure behavior accurately.
6. Stabilize UTC-midnight tests with a shared/injected clock.

After repairs, rerun the focused and full suites from both CWDs, repeat pre-fix/red-green proof for each new adversarial test, and request a new independent audit. Deployment remains a separate Barış-gated step after a non-BLOCK audit; it must not be combined with or inferred from this report.

## Skipped / constrained checks

- No `C:\P2RT` access, per the hard boundary. Deployed-mode conclusions use the audited source's default path/mode wiring plus the provided, repo-recorded fact that base `abda6717`'s bridge tree is byte-identical to deployed `74e0990b`; runtime DB contents/config were not inspected.
- No literal `git stash`/`git stash pop`, because the committed clean branch has no fix diff for stash to remove. The bounded three-file restore proof above is equivalent and left the tree clean.
- No deploy, push, scheduler, credential, exchange, testnet, paper, ARM/DISARM/KILL, threshold, config, schema, Pine, parity, strategy, or runtime action.
- Cline was attempted only for a read-only mechanical cross-check but its hub closed with code 1006 before output. `_deepseek_driver` was not used because its required task/report files under `C:\tmp` would violate this audit's no-extra-file-write boundary.
- No index was added or benchmarked on a copy of the production DB; performance was bounded in-memory only.

