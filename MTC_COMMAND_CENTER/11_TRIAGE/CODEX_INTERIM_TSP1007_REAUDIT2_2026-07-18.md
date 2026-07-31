# Codex independent adversarial round-3 re-audit — interim TS-P1-007

Date: 2026-07-18  
Auditor: Codex GPT-5  
Builder: Claude Fable 5  
Worktree: `C:\P1IF`  
Branch: `feature/interim-daily-loss-wiring`  
Requested code target: `3fa13f3ef0752e822c42c85812f1ef12016e3642`  
Repair parent: `066b49cc1e40457169a32a26c6624005cba740ab`  
Base: `abda67173964bb3dd0ce303ef07a699c691da7b9`

## Verdict: **BLOCK**

The normal split-entry and split-exit repairs work, the six new tests are genuinely semantic, and all reported green suites reproduce. Funding exclusion is now an explicit owner-approved interim limitation (D017), so this audit does not require a funding-ledger build.

The cumulative accounting is still not safe under late, conflicting, or mixed-role fills. A late TP fill after an SL close rewrote an exact-boundary `-2000` loss to `0`, clearing both gate inputs while leaving the original `TRADE_CLOSED` audit decision unchanged. A duplicate `fill_id` with a changed payload can similarly rewrite a loss into a profit. A partially filled entry can be marked closed while its entry order remains live; a later entry fill creates a position whose trade remains closed, and reconciliation ignores that position as foreign. Each is a state-corruption or wrong-gate scenario and therefore meets the prompt's BLOCK rule.

No deploy, push, runtime, network, scheduler, credential, exchange, testnet, paper, ARM/DISARM/KILL, threshold, config, schema, strategy, Pine, parity, or `C:\P2RT` action occurred.

## Target identity note

The clean worktree had advanced one documentation-only commit beyond the requested target:

```text
HEAD  b11a2e36f18287db347ce53f7379139b72aba940
HEAD^ 3fa13f3ef0752e822c42c85812f1ef12016e3642
```

`b11a2e36` changes only `docs/20_INTERIM_TSP1007_RISK_WIRING.md` to record D017. `git diff --exit-code 3fa13f3e..b11a2e36 -- IBKR_PAPER_BRIDGE/bridge IBKR_PAPER_BRIDGE/tests` passed. Therefore every production/test result below exercises code byte-identical to `3fa13f3e`, with the current owner-accepted contract disclosure from `b11a2e36`.

## Findings

### R3-01 — CRITICAL / BLOCK: a post-close exit fill rewrites closed PnL and clears gates

Evidence:

- `bridge/engine/orders.py:303-315` recomputes cumulative exit totals for every exit fill and records `was_closed` only as a flag.
- `orders.py:315-323` accepts `exit_qty >= entry_qty` and calls `update_trade_exit(...)` even when `was_closed` is already true.
- `orders.py:324-341` suppresses only the second `TRADE_CLOSED` decision; it does not suppress mutation of the already-closed trade.
- `bridge/store/db.py:524-558` averages all exit-role fills across SL, TP, TRAIL, and CLOSE orders. It has no overfill or post-close invariant.

Direct mixed-role reproduction through the real `_ingest_fill` path:

```text
after_SL pnl= -2000.0 daily= -2000.0 streak= 1
after_late_TP pnl= 0.0 daily= 0.0 streak= 0 closed_decisions= 1
```

Concrete failure: a 200-unit long enters at 100. Its SL fills at 90, creating the exact configured daily boundary loss and a loss streak. A late TP fill at 110 on the same trade makes cumulative exit VWAP 100; the code overwrites `trades.pnl` to zero. DAILY_LOSS and CONSECUTIVE_LOSS no longer see the loss, while the sole `TRADE_CLOSED` decision still records the original close. The persisted risk source and audit chain disagree.

Smallest safe required edit: once `exit_ts` is set, never recompute or overwrite the closed trade from a new fill. Require exit quantity to equal—not exceed—the entry basis within tolerance. A distinct post-close/overfill event must be persisted separately, raise an explicit `POST_CLOSE_FILL`/`OVERFILL` fault, and force fail-closed reconciliation/quarantine. Add SL→late-TP, TP→late-SL, late-CLOSE, and exact-boundary gate tests. Trade close and `TRADE_CLOSED` should be one atomic transaction.

### R3-02 — CRITICAL / BLOCK: `fill_id` conflicts are mutable, and partial-fill redelivery duplicates decisions

Evidence:

- `bridge/store/db.py:372-390` uses `INSERT OR REPLACE` for the `fills` primary key. A repeated identifier replaces the economic facts instead of preserving the first immutable record.
- `bridge/engine/orders.py:265-266` deduplicates only through the manager's in-memory set; a restart starts with an empty set.
- `_ingest_fill` does not learn whether `insert_fill` inserted, matched, or replaced a row, so processing always continues after restart.
- `orders.py:342-352` appends `TRADE_PARTIAL_EXIT` on every reprocessing of the same partial fill.

Direct reproductions:

```text
mutdup_before pnl=-11.0 daily=-11.0 streak=1
mutdup_after  pnl=+10.0 daily=+10.0 streak=0

partial_decisions_before_restart=1
partial_decisions_after_redelivery=2 exit_ts=None
```

The changed-payload reproduction used the same `fill_id` after a fresh manager but changed exit price from 90 to 110 and fee from 1 to 0. The Store replaced the row and rewrote the trade from a loss to a profit. Exact partial-fill redelivery leaves PnL unchanged but duplicates the audit decision.

Smallest safe required edit: make fills immutable with insert-once semantics and return a result such as `INSERTED`, `EXACT_DUPLICATE`, or `CONFLICT`. Stop processing exact duplicates. A conflicting payload for an existing `fill_id` must never replace it; emit a high-severity integrity event and fail closed. Key partial-exit decisions to a fill/event identity or insert them only when the fill was newly inserted. Add restart tests for exact duplicates, changed duplicates, partial duplicates, and cross-order identifier conflicts.

### R3-03 — CRITICAL / BLOCK: a flat partial entry can close while the remaining entry order stays live

Evidence:

- `orders.py:308-315` uses the currently filled entry quantity as the close basis without checking whether the entry order is terminal or has remaining quantity.
- `orders.py:294-299` continues updating entry VWAP if a later entry fill arrives, even when the trade already has `exit_ts`.
- `orders.py:110-119` treats a broker position with no open trade row as `FOREIGN_POSITION_IGNORED`; it neither reprotects nor flattens it.

Direct reproduction:

```text
partial_entry_flat: trade closed at pnl=-10; entry_order=SUBMITTED filled_qty=1/2
late_entry_after_close: entry_px changed to 105; trade still closed; entry_order=FILLED 2/2
reconcile: open_trade=None reprotect_attempts=0 flattened=[] event=FOREIGN_POSITION_IGNORED
```

Concrete failure: one unit of a planned two-unit entry fills, then its one-unit position exits. The trade is marked closed even though the remaining entry order is live. If the second entry unit later fills, the broker has exposure but the database has no open trade; reconciliation explicitly ignores the resulting position as foreign. This breaks the claimed partial-fill safety and can leave an unprotected position.

Smallest safe required edit: a flat partial entry cannot become terminal while any owned entry remainder is live. Cancel/confirm the remaining entry before close, or place the lifecycle in a persistent quarantined/closing state until reconciliation proves no remaining entry can fill. Reject/fail closed on any entry fill for an already-closed trade. Add partial-entry→exit→late-entry tests across manager restart and a reconciliation assertion that the position is protected or flattened, never ignored.

### R3-04 — MEDIUM: the half-exit engine-path test is not a semantic red test

`tests/test_interim_risk_wiring.py:710-722` opens quantity 2 at 100 and partially exits at 50. Old `066b49cc` computes a phantom full-quantity loss of only `2 × (50-100) = -100`, far inside the default `-2000` daily limit. The test therefore passes old and new code. Its comment that the old value “would exceed the daily limit” is false.

The recorded **5 failed / 19 passed** red result is honest, and the direct split-exit assertions still prove the basic accounting repair. The pass is benign for that narrow direct proof, but this particular engine-path test does not prove gate neutrality.

Smallest required edit: choose a valid quantity/equity combination that makes the old phantom close cross the daily boundary while the repaired partial exit remains open—for example, quantity 100 at the same prices. Then require the semantic red run to fail this test on `066b49cc`.

### R3-05 — NIT: risk-query scaling remains acceptable for this interim bridge

The risk aggregation queries were unchanged from `066b49cc`. Current in-memory medians on this host:

| Closed rows | Daily sum | Worst-case streak |
| ---: | ---: | ---: |
| 1,000 | 0.130 ms | 0.544 ms |
| 10,000 | 1.248 ms | 5.992 ms |
| 100,000 | 12.868 ms | 74.112 ms |

The new fill-total helpers use existing `idx_fills_cloid` and `idx_orders_trade`. No index change is required for this release; retain TS-P2-006 for larger-history benchmarking.

## A. Scope integrity

Commands included:

```text
git -C C:\P1IF status --short
git -C C:\P1IF branch --show-current
git -C C:\P1IF rev-parse HEAD
git -C C:\P1IF rev-parse HEAD^
git -C C:\P1IF merge-base HEAD abda6717
git -C C:\P1IF diff --name-status 066b49cc..3fa13f3e
git -C C:\P1IF diff --check 066b49cc..3fa13f3e
git -C C:\P1IF diff --exit-code 3fa13f3e..b11a2e36 -- IBKR_PAPER_BRIDGE/bridge IBKR_PAPER_BRIDGE/tests
```

Results:

- Worktree clean; branch correct.
- `3fa13f3e` is directly on `066b49cc`; merge-base remains `abda6717`.
- Repair diff is exactly four files: `bridge/engine/orders.py`, `bridge/store/db.py`, `tests/test_interim_risk_wiring.py`, and `docs/20_INTERIM_TSP1007_RISK_WIRING.md`.
- Stat: **4 files changed, 290 insertions, 22 deletions**.
- `b11a2e36` adds only the D017 contract disclosure.
- No `RiskConfig`, threshold, engine gate, strategy, config, schema version, Pine, parity, `MTC_V2`, or protected path changed. Defaults remain 0.02 daily loss and 3 consecutive losses.
- Diff checks passed; the target worktree was clean again after the red-proof restoration.

## B. Base inertness

The base evidence remains unchanged and was re-derived with `git show`/`git grep`:

- `abda6717` engine evaluation omitted `realized_today` and `consecutive_losses`.
- reconcile hardcoded equity telemetry `realized_today=0.0`.
- `upsert_risk_day` had no production caller.
- DAILY_LOSS unit coverage injected the value directly into `RiskEngine.evaluate`.

The original operational gates were inert; this round does not alter that conclusion.

## C. Store and fill-accounting attacks

Prior Store repairs remain correct for canonical timestamps, `[UTC midnight,next midnight)`, NULL/open trades, zero-PnL streak reset, mode/network isolation, same-environment restart persistence, and unknown-run failure. Direct timestamp probes normalized `Z`, space-separated, offset, and naive inputs to canonical UTC.

The basic R-01 repair also works:

- split entries at 100/110 produce entry VWAP 105;
- split exits at 90/110 produce exit VWAP 100 and true gross PnL zero;
- partial exit has NULL `exit_ts`/`pnl` and no gate contribution;
- exact final-fill redelivery after restart does not duplicate `TRADE_CLOSED`;
- normal partial SL status stays `OPEN`, cumulative `filled_qty=1`, and `_within_pending_grace(...)` remains true.

The unresolved post-close, immutable-ID, partial-decision, and partial-entry edges are R3-01 through R3-03.

## D. Engine and fail-closed wiring

Gate order and the repaired risk-input latch are unchanged. Boundary reproduction:

```text
limit=2000 pnl=-2000 accepted=False rejection=DAILY_LOSS_LIMIT disarm=True
limit=2000 pnl=-1999 accepted=True rejection=None disarm=False
```

Unknown-run direct `on_bar` reproduction remained fail closed:

```text
DISARMED 0 LookupError: run not found for risk scoping: missing-risk-run
```

The missing-run reconcile regression still uses telemetry-only fallback, while the engine risk path fails closed. Those earlier repairs pass. R3-01 can nevertheless erase the persisted loss before a later signal reaches these otherwise-correct gates.

## E. Independently reproduced test evidence

### Clean current code, bridge root (`C:\P1IF\IBKR_PAPER_BRIDGE`)

```text
python -m pytest tests/test_interim_risk_wiring.py -q
24 passed in 2.40s

python -m pytest tests/test_hyperliquid_broker.py::test_positions_and_reconcile_use_old_client_during_blocking_rebuild -q
1 passed in 1.31s

python -m pytest tests -q
156 passed, 1 warning in 43.48s
```

### Clean current code, repository root (`C:\P1IF`)

```text
python -m pytest IBKR_PAPER_BRIDGE/tests/test_interim_risk_wiring.py -q
24 passed in 2.40s

python -m pytest IBKR_PAPER_BRIDGE/tests/test_hyperliquid_broker.py::test_positions_and_reconcile_use_old_client_during_blocking_rebuild -q
1 passed in 1.34s

python -m pytest IBKR_PAPER_BRIDGE/tests -q
156 passed, 1 warning in 43.38s
```

The sole warning was the existing Starlette TestClient deprecation warning. After the red-proof restoration and adversarial probes, final bridge-root reruns produced **24 passed in 2.55s** and regression **1 passed in 0.61s**.

### Semantic red proof against `066b49cc`

Exact bounded workflow:

```text
$auditPaths = @(
  'IBKR_PAPER_BRIDGE/bridge/store/db.py',
  'IBKR_PAPER_BRIDGE/bridge/engine/orders.py'
)
git restore --source=066b49cc --worktree -- $auditPaths
python -m pytest IBKR_PAPER_BRIDGE/tests/test_interim_risk_wiring.py -q
git restore --source=HEAD --worktree -- $auditPaths
git diff --exit-code HEAD -- $auditPaths
git status --short
```

Raw result: **5 failed, 19 passed in 1.58s**, pytest exit 1. The five failures were split-entry VWAP, no-premature split exit, split-exit fees, final-fill restart idempotence, and partial-entry restart. Restore exits and final diff were zero; final status was clean.

The sixth new half-exit engine test passed old and new code for the arithmetic reason in R3-04, not because the old code handled partial exits correctly.

## F. Interim gaps and funding decision

The current contract accurately discloses:

- production gate PnL is gross minus captured fees; no production funding source exists;
- D017 explicitly accepts funding exclusion for this interim gate and defers real funding attribution to TS-P1-005/full TS-P1-007;
- the decision must be revisited before paper evidence cites the daily-loss gate or if funding becomes material;
- current equity—not day-start equity—is the percentage base;
- `risk_days`, broker reconciliation, equity stop, drawdown, and the full immutable snapshot remain deferred;
- paper/dry-run share a DB but query isolation is by mode/network;
- deployment remains separately gated.

Under the round-3 instruction and D017, missing funding is a disclosed, owner-accepted interim limitation rather than a new code finding. It does not cure the independently reproduced state-corruption defects above.

## Required repair set before another audit

1. Make closed trades immutable against later fills; detect and fail closed on post-close fills and exit overfill/mixed-role races.
2. Make `fill_id` records immutable and processing result-aware; exact duplicates must be no-ops, conflicts must quarantine, and partial decisions must be idempotent.
3. Prevent a partial entry from becoming terminal while an owned entry remainder can still fill; cancel/confirm or quarantine it, and test late-entry reconciliation across restart.
4. Make trade close plus `TRADE_CLOSED` atomic, including crash/restart proof.
5. Repair the half-exit engine-path test so it crosses the old daily-loss boundary semantically.
6. Rerun focused, regression, full, semantic red, mixed SL/TP, conflicting-duplicate, and late-entry reconciliation evidence; then request another independent audit.

Deployment remains a separate Barış-gated step after a non-BLOCK verdict.

## Skipped / constrained checks

- `C:\P2RT` was not accessed.
- No network, exchange, SDK-documentation, scheduler, credential, database-runtime, or paper/testnet action was performed.
- No production database was benchmarked; performance tests were in-memory.
- Cline completed the required read-only mechanical invocation with exit 0 but returned no review text; no claim relies on it.
- No production/test/config file was edited. The only writes are this requested audit report and the requested D/M/R handoff updates.
