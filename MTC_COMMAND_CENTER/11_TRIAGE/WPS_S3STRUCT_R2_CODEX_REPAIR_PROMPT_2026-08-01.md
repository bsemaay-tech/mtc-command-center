# S3-STRUCT ROUND 2 — CODEX REPAIR DISPATCH (2026-08-01)

## 0. ROLE OVERRIDE — READ FIRST

**You are the IMPLEMENTER.** Claude `claude-opus-5` is Lead and acceptance authority; you are the
counterpart flagship implementer (`gpt-5.6-sol`, effort `xhigh`). Do **not** delegate to Claude Code
CLI or any other model — a delegation attempt returns `ConnectionRefused` and wastes the round.
Implement it yourself, here, now.

**You cannot run Git.** `.git` is read-only for you. The Lead does every Git operation. Reading with
`git diff` / `git status` is fine.

Workspace: `C:/WPS` — branch `feature/ts-p1-009b-s2-closure`, HEAD `34d35286` (your round-1 work,
already committed by the Lead).

## 1. WHERE THE ROUND STANDS

Round 1 (`34d35286`) was **NOT accepted**. Verdict `REQUEST_CHANGES` from canonical auditor
`gpt-5.6-sol` xhigh, **reproduced by the Lead on real source**. Suite was clean —
`2 failed, 1262 passed`, no third failure, no weakened tests, allowlist exact.

**What round 1 got right — keep all of it.** The auditor and the Lead both judged the boundary
genuinely structural, not a fourth point fix: one registry-driven `DurableRowAccessor` /
`ValidatedDurableRow` over `DURABLE_EVENT_COLUMN_TYPES`, a matrix generated from that registry, the
class-C join added as a conjunct with the epoch fence intact, and both legacy helpers deleted rather
than left as a competing path. The accessor is type-total across bytes/memoryview, `Decimal('NaN')`,
`bool`, non-finite values, subnormals, and `±2**63`. **Do not redesign any of that.**

**This is round 1 of a maximum 3 non-accepting rounds.** Two remain.

## 2. R-1 — THE ONE REQUIRED REPAIR

**Your own S3T-B raise opened the next neighbour.** This is the exact pattern the cycle exists to
break: a repair that closes its defect and leaves the class open one call away.

Verified escape chain, every step read on real source at `34d35286`:

1. `db.py:7656` — the new binding veto raises
   `KillConflictError("KILL_LIFECYCLE_IDENTITY_MISSING", ...)`. Correct: it rolls back, records
   evidence, leaves the trade open. Nothing wrong here.
2. `orders.py:2853` — `_ingest_queued_event`'s containment allowlist now includes
   `KILL_LIFECYCLE_IDENTITY_MISSING`, so it calls `_defer_kill_lifecycle_event(...)`.
3. `orders.py:2785-2792` — with `identity=None`, that re-reads the order and calls
   `_kill_lifecycle_identity(order)`.
4. **`orders.py:2733` — the defect.** `if order is None or str(order.get("role")) != "KILL_FLATTEN":
   return None, None, ()`. A second `Store` changed `orders.role` to `'CLOSE'` between the first
   validation and the close, so this returns identity `None` with an **empty** `missing_identity`.
5. `orders.py:2790-2793` — `missing_identity` is falsy, so the quarantine branch is skipped;
   `resolved_identity is None`, so it returns `_KILL_LIFECYCLE_UNBOUND`.
6. `orders.py:2862` — `raise` re-raises the `KillConflictError`.
7. Neither `_drain_queued_events_locked` nor `drain_queued_events` catches `KillConflictError` — you
   gave them a `DurableRowFault` handler only. It unwinds through the unguarded `BridgeEngine.start()`
   and the `app.py` lifespan hook.

**Result: `BridgeEngine.start()` does not return normally.** That violates the explicit cycle
decision that **identity faults are contained** and only evidence-store outages propagate.

**Reproduction (use the existing active-epoch two-`Store` setup, no new harness needed):** after
`_kill_lifecycle_identity` validates the queued fill under an active epoch, have `Store` 2 run
`UPDATE orders SET role='CLOSE'` before `close_trade_once_with_decision` runs.

### The root cause to fix — fix this, not step 7

The reachable defect is that **`_kill_lifecycle_identity` conflates two different situations** and
returns the same `(None, None, ())` for both:

- *"This order was never a kill-lifecycle order"* — a legitimate not-applicable answer. `_ingest_fill`
  depends on this to route ordinary ENTRY/SL/TP fills, and it must keep working unchanged.
- *"This order **was** the validated `KILL_FLATTEN` binding and is not any more"* — an identity fault
  that must be quarantined with durable evidence, never silently reported as not-applicable.

On the fault path — reached only because a `KILL_LIFECYCLE_IDENTITY_MISSING` conflict already told
you the binding broke — the second situation is the only one that can be true, and it currently
produces no reason and no evidence.

**Do not** simply add `except KillConflictError` to the two drains. That contains the symptom, buries
the missing evidence, and is precisely the point-fix strategy the owner stopped. Make the identity
path report the fault it actually observed.

**Requirements:**

- A binding that was validated and is no longer valid produces a **non-empty** identity fault with a
  reason distinguishing *role changed*, *group_id changed/cleared*, *trade_id changed*, and *order
  row disappeared* — so the durable evidence says which one.
- The event is quarantined and consumed exactly as other identity faults are:
  `app_state` durably `KILLED`, ARM refuses, ACK unreachable, trade left open, queue and deferred map
  consistent.
- `BridgeEngine.start()` **returns normally**.
- `_ingest_fill`'s ordinary non-kill routing through `_kill_lifecycle_identity` is unchanged.
- `KILL_STALE_EVIDENCE_RECORD_FAILED` and genuine evidence-store write failures **still propagate** —
  do not contain those for symmetry.

## 3. WHY S3T-D MISSED THIS — the second required piece

Your matrix generates over **value corruption**: every registered column × `{NULL, non-numeric TEXT,
storage class, int64 range, non-finite}`. R-1 is not a corrupt value. Every value involved is
perfectly well-formed. What broke is the **binding between validation and use** — a second `Store`
mutating an identity column mid-flight.

**Add that as a second generated dimension**, do not hand-write one test for R-1.

For each identity column that participates in the kill-lifecycle binding — at minimum
`orders.role`, `orders.group_id`, `orders.trade_id`, and the order row's existence — generate a case
that, **with an active epoch**, mutates that column via a second `Store` **after** first validation
and **before** the close, then asserts the same four invariants your existing matrix asserts:

1. `BridgeEngine.start()` returns normally;
2. durable evidence exists, naming which binding element broke;
3. fail-closed — `app_state` `KILLED`, ARM refuses, ACK unreachable, trade left open;
4. queue and deferred map end consistent.

A single hand-written R-1 regression test will be rejected. The generated mutation dimension is the
deliverable — the same reason S3T-D was required in round 1.

## 4. UNCHANGED CONSTRAINTS

**Allowlist — exhaustive:**

```
IBKR_PAPER_BRIDGE/bridge/engine/orders.py
IBKR_PAPER_BRIDGE/bridge/store/db.py
IBKR_PAPER_BRIDGE/tests/test_engine_dryrun.py
IBKR_PAPER_BRIDGE/tests/test_store.py
IBKR_PAPER_BRIDGE/docs/31_KILL_EVIDENCE_EPOCH_CONTRACT.md
```

`bridge/engine/engine.py` is **not** allowed. Report a needed scope extension; never take one.

**Forbidden:** any `*.pine`, `MTC_V2`, `parity`, `01_PINE`, `02_MTC_BACKTEST`, `07_ADAPTERS` path ·
`bridge/engine/strategies/**`, `config/strategies/**` · `bridge/api/routes.py` · `bridge/broker/**` ·
**any risk-threshold value** in `config/bridge.yaml` · any credential, wallet secret, API key, host,
IP or private path · **weakening, deleting, skipping or `xfail`-ing any existing test — grep your own
diff for `-` lines under `tests/` before reporting** · any migration or schema change · any broker,
network, TESTNET, ARM or runtime action. DISARMED only.

**Test contract** — from `C:/WPS/IBKR_PAPER_BRIDGE`:

```
python -m pytest -q --ignore=TSP1009B.pytest_tmp_s1r1 -p no:randomly
```

`--ignore` is mandatory. Never pass `--basetemp` inside `.pytest_cache`.

Floor at `34d35286`: **`2 failed, 1262 passed`**. Same two pre-existing failures — stale KVM2 ledger
hash, and `schema_version == "2"` against default v4. **Do not "fix" them.** A third failure is a
required finding. Run the full suite yourself before reporting; a report without executed suite
output will be returned.

## 5. REPORT FORMAT — end with exactly this

```
R-1 root cause fix : <what _kill_lifecycle_identity now distinguishes, and where>
R-1 fault reasons  : <the distinct reason codes for role / group_id / trade_id / missing row>
R-1 containment    : <how start() now returns normally, and where the evidence is written>
Non-kill routing   : <proof _ingest_fill's ordinary path is unchanged>
Propagation intact : <proof KILL_STALE_EVIDENCE_RECORD_FAILED still propagates>
Mutation dimension : <how many identity columns x cases = how many generated assertions>
files changed      : <exact list>
tests added        : <names>
existing tests touched : <list | none>   # any '-' line under tests/ must appear here
suite output       : <the literal final pytest line>
scope extensions   : <none | what you needed and why you did NOT take it>
open risks         : <anything the Lead should probe first>
```

Begin. Implement in `C:/WPS`. No Git. No delegation.
