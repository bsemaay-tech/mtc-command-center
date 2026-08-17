# S3-STRUCT ROUND 1 — CODEX IMPLEMENTATION DISPATCH (2026-08-01)

## 0. ROLE OVERRIDE — READ FIRST, THIS SUPERSEDES `AGENTS.md` §TWO-TIER

**You are the IMPLEMENTER for this task.** Claude `claude-opus-5` is the Lead Orchestrator and the
acceptance authority; you are the counterpart flagship implementer (`gpt-5.6-sol`, effort `xhigh`).

Do **not** delegate this work to Claude Code CLI, Cline, DeepSeek, or any other model. Do not attempt
to dispatch a counterpart. Implement it yourself, in this worktree, now. Previous rounds were lost
because a dispatch attempt returned `ConnectionRefused` and the session reported BLOCKED with zero
edits. That is a failure mode, not an outcome.

**You cannot run Git.** `.git` is read-only for you. Do not run `git add`, `git commit`, `git
checkout`, `git reset`, `git stash`, `git worktree`, or any other Git write. The Lead performs every
Git operation. Reading with `git diff` / `git status` is fine and encouraged for self-review.

Workspace: `C:/WPS` — branch `feature/ts-p1-009b-s2-closure`, HEAD `732b37c3`.

---

## 1. WHAT THIS CYCLE IS AND WHY IT EXISTS

This is **not** a fourth point-fix round. Three prior rounds each closed exactly the call sites the
previous audit named, and each one left the same *defect class* open at a neighbouring site:

| Round | Scoped to close | What it left open |
|---|---|---|
| 1 | the startup-failure class | re-opened a reachable variant, dropped an event, relocated unbounded growth |
| 2 | identity *shape* validation | the store also required durable *binding*; `int()` ran before validation |
| 3 | identity parsing + durable binding + schema capability | `insert_fill` runs ahead of every guard; `_event_symbol` never got the parser |

The owner stopped the point-fix strategy and authorised a **structural** cycle (decision D027).

> **Guard the entry point, not one line.**

A patch that adds a `try` at each of the five sites named in §2 **will be rejected**, even if the
suite is green. The deliverable is a boundary plus a matrix-generated acceptance suite that proves
the class is closed for columns nobody has probed yet.

---

## 2. THE DEFECT CLASS — ALL FIVE FINDINGS VERIFIED BY THE LEAD ON REAL SOURCE AT `732b37c3`

SQLite columns in this schema are **affinity-only**: no `CHECK`, no `NOT NULL`, no `STRICT`.
`fills.qty REAL` accepts non-numeric TEXT and NULL. `orders.trade_id INTEGER` accepts arbitrary TEXT.
The v8→v9 migration preserves predecessor rows unvalidated **by design** — `_migrate_v8_to_v9`
asserts the row census is unchanged. So schema-admitted corruption is a real, reachable input, not a
hypothetical.

### Class A — schema-admitted data reaches an unguarded conversion on the drain path

- **A1 — `bridge/store/db.py:7338-7339`** (`insert_fill`). The duplicate-classification tuple builds
  with bare `float(row["qty"])` / `float(row["px"])`. Two lines below, `fee`/`funding` use
  `float(row["fee"] or 0.0)`: the NULL case was considered for two columns and missed on the two
  that matter. **`insert_fill` runs ahead of every guard round 3 added.** Both flagship auditors
  found this independently.
- **A2 — `bridge/engine/orders.py:2670`** (`_event_symbol`). Uses raw `int(order["trade_id"])`.
  `_parse_store_trade_id` exists at `orders.py:2687` and is applied at only `2727` and `3229`.
  `_event_symbol` runs for **every** queued event, on **both** drains, before any guard.
- **A3 — `bridge/engine/orders.py:2856-2860`** (`_canonical_status`). Computes
  `float(filled_qty) if filled_qty is not None else float(order.get("filled_qty") or 0.0)`
  **outside** its own `try`, which does not open until line `2864`.

Escape route, identical in every case:

```
BridgeEngine.start() → order_manager.reconcile() → sync_broker_state()
  → drain_queued_events() → _ingest_queued_event() → _ingest_event() → _ingest_fill()
```

`_ingest_queued_event` (`orders.py:2805`) catches only `KillConflictError` (`orders.py:2830`).
Everything else unwinds through the **unguarded** `BridgeEngine.start()` and the `app.py` lifespan
hook. Result: **the bridge does not start, and no durable evidence is written.** Of 14
schema-admitted corruptions probed in round 3, 11 were contained and **3 escaped**.

### Class B — the parser is type-total but not storage-boundary safe

`_parse_store_trade_id` (`orders.py:2687`) handles "not-an-integer" correctly, but accepts any Python
`int` or Unicode-decimal string **without SQLite signed-64-bit bounds validation**. A value above
`2**63 - 1` parses fine in Python and then raises **`OverflowError`** when `sqlite3` binds it inside
`get_trade`. Same escape route, same silence.

### Class C — the close path never re-derives its binding *(the most serious)*

`close_trade_once_with_decision` (`bridge/store/db.py`, fenced branch at `7469-7491`) fences the
**epoch**: `_assert_kill_epoch_in_tx(resolved_epoch)` plus
`AND EXISTS (SELECT 1 FROM kill_requests WHERE episode_id = ? AND epoch_token = ?)`.

That proves the epoch token is current. **Lead-verified by direct source read: the fenced `UPDATE`
contains no join back to `orders`.** Nothing confirms the trade being closed is still bound to the
active episode.

Scenario: with active epoch A, `Store` 1 validates a `KILL_FLATTEN` order bound to episode A / trade
T; `Store` 2 clears or changes `orders.group_id`; `Store` 1 continues down the active-epoch branch
and **closes T and writes `TRADE_CLOSED` with no identity quarantine.**

This is a **correctness** gap, not a liveness gap. Round 3's own two-`Store` test missed it because
that test runs with **no active epoch** — it exercises the deferral store's binding check and never
the close path.

---

## 3. GATE-1 SCOPE — FROZEN BY THE LEAD. DELIVER ALL FOUR ITEMS.

### S3T-A — validated accessor boundary over durable rows

Introduce **one** typed accessor layer for reading durable `orders` / `fills` / `trades` values.
Every read of a durable row **on any path reachable from a queued broker event** goes through it.

It must return **either a validated typed value or a containable fault** — it must never raise an
unguarded `ValueError`, `TypeError`, `OverflowError`, or `decimal.InvalidOperation` into its caller.

Validation must cover, for each column it serves:

| Case | Required behaviour |
|---|---|
| `NULL` | containable fault |
| non-numeric TEXT | containable fault |
| unexpected storage class (TEXT where REAL expected, `bytes`, etc.) | containable fault |
| integer outside SQLite signed 64-bit range (`< -2**63` or `> 2**63 - 1`) | containable fault **(class B)** |
| non-finite float (`NaN`, `+inf`, `-inf`) | containable fault |
| valid value | typed result |

**Design is yours**, subject to three hard properties:

1. **It is one boundary, not a helper sprinkled at the sites an audit happened to name.** A reviewer
   must be able to point at a single module-level construct and say "every drain-reachable durable
   read goes through this."
2. **It is driven by a declared column/type registry** — an explicit table of
   `(table, column) → expected type` — not by per-call-site literals. S3T-D generates its matrix from
   this same registry, which is what makes the suite cover columns nobody has probed.
3. **A fault carries a stable reason code** identifying the column and the case, so durable evidence
   is diagnostic rather than a bare "something failed".

The boundary belongs in `bridge/store/db.py` (store layer). `bridge/engine/orders.py` consumes it.
Both files are in the allowlist. No new file outside the allowlist.

Existing helpers stay or are absorbed — your choice — but `_parse_store_trade_id` and `_store_float`
must not survive as a second, competing validation path that some future call site reaches instead.
If you keep them, make them thin delegations to the boundary.

### S3T-B — close path re-derives its binding

`close_trade_once_with_decision` must, **inside its existing `BEGIN IMMEDIATE`**, re-derive that the
trade it is about to close is *currently* bound to the active episode — joining `orders` on
(`role = 'KILL_FLATTEN'`, `group_id` = active `episode_id`, `trade_id` = the trade being closed) —
not merely that the epoch token is current.

If the binding no longer holds: **roll back, write durable evidence, fail closed. Do not commit.**

**Do not weaken the existing epoch fence.** `_assert_kill_epoch_in_tx`, the `kill_requests` `EXISTS`
predicate, and the stale-epoch rollback + EP-4 append + raise-to-caller all stay exactly as they are.
You are adding a conjunct, not replacing one.

The `resolved_epoch is None` branch (`db.py:7459-7467`) is the non-kill close path and keeps its
current behaviour — do not add a kill-binding requirement to ordinary closes.

### S3T-C — entry-point containment

Every entry point reachable from a queued broker event reads durable values through the S3T-A
boundary. **Explicitly including `_event_symbol` and `_canonical_status`**, which currently run
*before* any guard on both drains, and `insert_fill`'s duplicate-classification read.

Do not stop at the three named sites. Walk the reachable set from
`drain_queued_events` / `_drain_queued_events_locked` → `_ingest_queued_event` → `_ingest_event` →
`_ingest_fill` and route every durable-row read you find. State in your report which reads you found
and routed, and any you deliberately left (with the reason).

### S3T-D — the acceptance test that makes this structural

**This is the deliverable that distinguishes this cycle from a fourth point-fix round.**

A property-style test that enumerates, **from the S3T-A column registry** — not from a hand-listed
set of the five findings above — the cross-product of every durable column reachable from a queued
event × every corruption case in the S3T-A table, and asserts for **every** combination:

1. `BridgeEngine.start()` **returns normally**;
2. durable evidence exists for the fault, with its reason code;
3. the system is fail-closed — `app_state` durably `KILLED`, ARM refuses, ACK unreachable, the trade
   is left open;
4. the queue and the deferred map end in a consistent state (no silent event drop, no unbounded
   growth — round 1 relocated exactly that defect).

Plus, for class C, a **two-`Store` test with an ACTIVE EPOCH** proving the close path refuses when
the binding is broken mid-flight — the case round 3's test structurally could not reach because it
ran with no active epoch. Assert the rollback, the durable evidence, and that the trade is still
open.

A test that covers only the five known findings **does not close the class and will not be
accepted.** If the generated matrix reveals a column that faults in a way you did not anticipate,
that is the suite working — fix the boundary, do not narrow the matrix.

### Lead decision carried forward — state this, do not change it

`KILL_STALE_EVIDENCE_RECORD_FAILED` **keeps propagating.** It means the durable evidence store itself
cannot be written; no durable evidence can be recorded when the evidence store is the failing
component, so halting with `app_state` durably `KILLED` is the honest fail-closed outcome. Identity
and schema-capability faults are **contained**; evidence-store outages **propagate**. Do not
"contain" this one for symmetry.

### Explicitly OUT of scope

TS-P1-010 and beyond · EP-1's residual venue-side supersede window (Hyperliquid exposes no fencing
token — a documented accepted limitation) · any operations-dashboard or read-model redesign · **any
migration, foreign key, `STRICT` table, `CHECK` constraint, or schema-version change — the fix is
defensive reading, not schema repair** · changing the default schema target away from v4 · any
alerting redesign · re-opening accepted S2 mechanisms.

---

## 4. ALLOWLIST AND HARD CONSTRAINTS

**Allowed paths — exhaustive. Touch nothing else.**

```
IBKR_PAPER_BRIDGE/bridge/engine/orders.py
IBKR_PAPER_BRIDGE/bridge/store/db.py
IBKR_PAPER_BRIDGE/tests/test_engine_dryrun.py
IBKR_PAPER_BRIDGE/tests/test_store.py
IBKR_PAPER_BRIDGE/docs/31_KILL_EVIDENCE_EPOCH_CONTRACT.md
```

`bridge/engine/engine.py` is **not** allowed — no item needs it. If you become convinced the scope
must extend, **report that as a blocker; do not take it.**

**Forbidden everywhere:**

- any `*.pine`, `MTC_V2`, `parity`, `01_PINE`, `02_MTC_BACKTEST`, `07_ADAPTERS` path
- `bridge/engine/strategies/**`, `config/strategies/**`
- `bridge/api/routes.py` · `bridge/broker/**`
- **any risk-threshold value** in `config/bridge.yaml` (position size, leverage, daily-loss,
  drawdown, equity floor, exposure, liquidation) — owner-defined, never invented or changed
- any credential, wallet secret, API key, host, IP, or private path
- **weakening, deleting, skipping or `xfail`-ing any existing test.** Grep your own diff for `-`
  lines under `tests/` before you report. **This rule was broken once already in this programme.**
- any migration or schema change
- starting the bridge against a real broker; any broker, network, TESTNET, ARM, or runtime action

**Safety:** DISARMED only. No ARM, no order, no broker, no network, no TESTNET, no VPS.

---

## 5. TEST CONTRACT

From `C:/WPS/IBKR_PAPER_BRIDGE`:

```
python -m pytest -q --ignore=TSP1009B.pytest_tmp_s1r1 -p no:randomly
```

`--ignore` is **mandatory** — `TSP1009B.pytest_tmp_s1r1/` is ACL-locked and plain `pytest` aborts
collection with `PermissionError`. **Never** pass `--basetemp` inside `.pytest_cache` (it produced
623 errors once).

Floor at `732b37c3`: **`2 failed, 1140 passed`**.

The two failures — a stale KVM2 ledger hash, and `test_invariants_preserve_risk_and_history`
asserting `schema_version == "2"` against default v4 — fail identically on the `origin/master` Bridge
tree, are pre-existing, and are outside every allowlist. **Do not "fix" them.** A third failure is a
required finding against you.

Target: `2 failed, 1140+N passed`, same two failures, no third.

**Run the full suite yourself before reporting.** A report without executed suite output is not
acceptance evidence and will be returned.

---

## 6. DEFINITION OF DONE

1. All three defect classes closed **structurally**, not point-wise.
2. The S3T-D matrix suite passes, and the escape set from a queued broker event is demonstrably
   **empty** for schema-admitted data on a healthy database.
3. Suite at `2 failed, 1140+N passed` — same two pre-existing failures, no third.
4. Your diff touches only allowlisted paths and deletes/weakens no existing test.

---

## 7. REPORT FORMAT — end your run with exactly this

```
S3T-A boundary      : <module-level construct + where the column registry lives>
S3T-A registry      : <the (table, column) -> type entries you declared>
S3T-B close fence   : <the added conjunct, and proof the epoch fence is untouched>
S3T-C routed reads  : <every drain-reachable durable read you found and routed>
S3T-C left unrouted : <any, with reason | none>
S3T-D matrix        : <how many columns x how many cases = how many generated assertions>
S3T-D class-C test  : <the active-epoch two-Store test, and what it asserts>
files changed       : <exact list>
tests added         : <names>
existing tests touched : <list | none>   # any '-' line under tests/ must appear here
suite output        : <the literal final pytest line>
scope extensions    : <none | what you needed and why you did NOT take it>
open risks          : <anything the Lead should probe first>
```

Begin. Implement in `C:/WPS`. No Git. No delegation.
