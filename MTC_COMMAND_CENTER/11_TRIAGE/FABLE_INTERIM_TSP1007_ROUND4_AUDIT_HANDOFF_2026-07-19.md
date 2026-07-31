# Fable audit handoff - interim TS-P1-007 round-4 repair

Audit date: 2026-07-19  
Builder: Codex GPT-5  
Independent auditor requested: Claude Fable  
Worktree: `C:\P1IF`  
Branch: `feature/interim-daily-loss-wiring`  
Target: `acb83b5b1dc464bad0db28f8a104015e3c1aa864`  
Parent: `b11a2e36f18287db347ce53f7379139b72aba940`  
Round-3 BLOCK report: `CODEX_INTERIM_TSP1007_REAUDIT2_2026-07-18.md`

## Requested verdict

Independently audit real code and rerun evidence. Return **PASS**, **PASS-WITH-NITS**, or
**BLOCK**. BLOCK any path that can rewrite canonical closed PnL, corrupt either risk-gate
input, duplicate terminal/partial accounting, or leave owned broker exposure unprotected or
misclassified as foreign.

Do not trust the builder claims below without reproducing them.

## Scope identity

The target is one commit over the documentation-only D017 parent and changes exactly four
files:

- `IBKR_PAPER_BRIDGE/bridge/store/db.py`
- `IBKR_PAPER_BRIDGE/bridge/engine/orders.py`
- `IBKR_PAPER_BRIDGE/tests/test_interim_risk_wiring.py`
- `IBKR_PAPER_BRIDGE/docs/20_INTERIM_TSP1007_RISK_WIRING.md`

Recorded stat: **4 files changed, 417 insertions, 33 deletions**. No engine gate, threshold,
strategy, config, schema version, Pine, parity, runtime, or deployment file is in the diff.
Funding remains excluded under owner decision D017: production interim PnL is gross minus
captured fees; full funding attribution remains deferred.

## Repair claims to attack

1. **Immutable fill IDs.** `Store.insert_fill` at `bridge/store/db.py:372` uses insert-once
   semantics and returns `INSERTED`, `EXACT_DUPLICATE`, or `CONFLICT`. A conflict preserves the
   first economic tuple and causes `FILL_ID_CONFLICT` plus DISARM. Exact redelivery cannot
   duplicate a partial decision, but can replay idempotent accounting after a prior close
   transaction failure.
2. **Immutable canonical close.** `_ingest_fill` at `bridge/engine/orders.py:264` refuses to
   rewrite a trade whose `exit_ts` is set. A distinct late SL/TP/CLOSE fill is retained as raw
   fill evidence, emits `POST_CLOSE_FILL`, and DISARMS. Canonical exit price, PnL, daily sum,
   loss streak, and the single `TRADE_CLOSED` decision remain unchanged.
3. **Overfill quarantine.** Per-order overfill emits `ORDER_OVERFILL`; cross-order aggregate
   exit quantity beyond entry quantity emits `TRADE_OVERFILL`. Neither path terminally closes
   or rewrites the trade.
4. **Owned partial-entry remainder.** `Store.has_live_entry_remainder` at `db.py:627` prevents
   terminal close while an ENTRY order in OPEN/SUBMITTED/PENDING has unfilled quantity. The
   bridge DISARMS with `ENTRY_REMAINDER_LIVE`, keeps the trade open, and a later entry fill
   remains attached across manager restart. Reconcile then reprotects or flattens exposure
   rather than emitting `FOREIGN_POSITION_IGNORED`.
5. **Atomic terminal state.** `Store.close_trade_once_with_decision` at `db.py:489` performs the
   guarded trade close and `TRADE_CLOSED` insert in one SQLite transaction. A forced abort of
   the decision insert rolls back the close; exact fill redelivery after restart completes it
   once.
6. **Semantic half-exit test.** Quantity is now 100, so old code's phantom close crosses the
   default `-2000` daily boundary. Correct code leaves the trade open with zero gate input.

## Builder evidence already obtained

From `C:\P1IF\IBKR_PAPER_BRIDGE`:

```text
python -m pytest tests/test_interim_risk_wiring.py -q
32 passed in 2.66s

python -m pytest tests/test_hyperliquid_broker.py::test_positions_and_reconcile_use_old_client_during_blocking_rebuild -q
1 passed in 1.57s

python -m pytest tests -q
164 passed, 1 warning in 21.73s
```

From `C:\P1IF`:

```text
python -m pytest IBKR_PAPER_BRIDGE/tests/test_interim_risk_wiring.py -q
32 passed in 2.72s

python -m pytest IBKR_PAPER_BRIDGE/tests/test_hyperliquid_broker.py::test_positions_and_reconcile_use_old_client_during_blocking_rebuild -q
1 passed in 1.52s

python -m pytest IBKR_PAPER_BRIDGE/tests -q
164 passed, 1 warning in 18.70s
```

The warning is the existing Starlette TestClient deprecation warning. After semantic-red
restoration, a final focused run was **32 passed in 2.16s** and the worktree was clean.

## Semantic red proof

With the committed tests unchanged, only `bridge/store/db.py` and `bridge/engine/orders.py`
were restored to `b11a2e36`, then restored to HEAD:

```powershell
$auditPaths = @(
  'IBKR_PAPER_BRIDGE/bridge/store/db.py',
  'IBKR_PAPER_BRIDGE/bridge/engine/orders.py'
)
git restore --source=b11a2e36 --worktree -- $auditPaths
python -m pytest IBKR_PAPER_BRIDGE/tests/test_interim_risk_wiring.py -q
git restore --source=HEAD --worktree -- $auditPaths
git add -- $auditPaths  # refresh Windows index stat only; blob hashes already equaled HEAD
git diff --cached --exit-code HEAD -- $auditPaths
git status --short
```

Raw result: **8 failed / 24 passed**. Failures were:

- SL close then late TP rewrote `-2000` to `0`.
- TP then late SL rewrote `+10` to `0`.
- SL then late CLOSE rewrote `-10` to `-2.5`.
- cross-order reused `fill_id` rewrote `-11` to `+10`.
- exact partial redelivery duplicated `TRADE_PARTIAL_EXIT`.
- a flat partial entry terminally closed while its entry remainder stayed live.
- cross-order exit overfill terminally closed.
- forced `TRADE_CLOSED` insert failure left the trade row closed, proving non-atomic old state.

The existing half-exit test is now semantic, but it was one of the 24 passing cases against
`b11a2e36` because that parent already contains the earlier cumulative partial-fill repair.
Its relevant red target is `066b49cc`, not this round's immediate parent. Fable should verify
that distinction rather than accepting a blanket red claim. Codex also ran that single test
against `066b49cc`: **1 failed in 0.98s** because old phantom PnL blocked the engine submission;
the two production files were then restored to exact HEAD blobs and status was clean.

## Mandatory adversarial checks for Fable

1. Confirm target/parent/branch/clean status and the exact four-file diff.
2. Re-run focused, regression, and full suites from both CWDs.
3. Reproduce the 8F/24P parent red result and exact clean restoration.
4. Attack SL-to-late-TP, TP-to-late-SL, and late-CLOSE at daily/streak boundaries.
5. Reuse a fill ID with changed price, fee, timestamp, role/order, quantity, and decision UID;
   confirm the first row and canonical PnL never change.
6. Redeliver exact entry, partial-exit, final-exit, post-close, and entry-remainder fills across
   fresh managers; confirm decisions/events are acceptably idempotent.
7. Inject failures before/inside/after terminal writes. Confirm trade close and
   `TRADE_CLOSED` never diverge and a restart can complete a previously persisted fill.
8. Attack order overfill, cross-order trade overfill, float tolerance boundaries, and mixed
   SL/TP/CLOSE races.
9. Attack live entry remainder statuses, cancellation/terminal statuses, manager restart, and
   reconcile. Owned exposure must be reprotected or flattened, never ignored as foreign.
10. Check quarantine is genuinely fail closed (`app_state=DISARMED`, high-severity event)
    without mutating already-canonical risk facts.
11. Verify doc 20 matches production behavior and D017 remains accurately scoped.

## Hard boundaries

Read-only audit plus local tests and the requested audit report. No push, PR, merge, deploy,
runtime start/restart, network, scheduler, credential, exchange, testnet, paper, ARM, threshold,
config, schema, strategy, Pine, parity, or `C:\P2RT` action. Deployment remains a separate
Baris approval gate after a non-BLOCK independent verdict.

Write the independent result to
`MTC_COMMAND_CENTER/11_TRIAGE/FABLE_INTERIM_TSP1007_ROUND4_AUDIT_2026-07-19.md`, then update
`GLOBAL_HANDOFF.md`, `NEXT_STEPS.md`, and `ACTIVE_FILES.md` using normal D/M/R discipline.
