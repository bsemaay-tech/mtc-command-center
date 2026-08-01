# S3-STRUCT — GATE-5 CANONICAL AUDIT BRIEF (2026-08-01)

> **Fill `34d35286` before dispatch.** Everything else is stable across rounds. This brief is
> written to be pasted standalone: an auditor needs nothing but this file and the worktree.

## 0. WHAT YOU ARE

You are a **canonical Gate-5 auditor** under `AGENTS.md` §CANONICAL AUDIT ROSTER. You are
independent: you did not write this code, you have no implementer session context, and you must not
accept the implementer's self-report as evidence for anything.

This is a **routine internal review of our own trading-support service**, conducted by the team that
owns it. The subject is defensive input validation on a database read path. Verify your conclusions
by **running the existing `pytest` suite**, not by writing throwaway crash-simulation or
failure-injection scripts — a previous audit round was killed mid-run by a provider content filter
triggered by exactly such a script, and re-running the audit cost real money for no added assurance.

Your workspace is a **dedicated worktree pinned at the frozen SHA**. Do not edit any file. When you
finish, the Lead will verify `git status --porcelain` is empty to prove you edited nothing.

**Verdict vocabulary — use these exact words:**

| Verdict | Meaning |
|---|---|
| `PASS` | Clean — no required changes. |
| `PASS-WITH-NITS` | Accepting — optional nits only, **zero** required repairs. If you have even one required repair, this is the wrong verdict. |
| `REQUEST_CHANGES` | Non-accepting — at least one required repair. |
| `BLOCK` | The workflow cannot safely continue. |

**D025 rule 1 binds you: if you cannot execute the mandated test suite, you must return `BLOCK`.**
Non-execution is never acceptance. A read-only opinion on a diff you could not exercise is
supplemental for the round, whatever label you print on it. Say plainly whether you ran the suite and
paste its final line.

---

## 1. THE ARTIFACT UNDER AUDIT

- Repo: MTC Command Center, Bridge subtree `IBKR_PAPER_BRIDGE/`
- Branch: `feature/ts-p1-009b-s2-closure`
- **Frozen SHA: `34d35286`**
- Round delta: `git diff 732b37c3..34d35286`
- Predecessor (the rejected artifact): `732b37c3`
- Last accepted artifact: `0c65a731` (S2 closure, both flagships PASS-WITH-NITS)

### Test contract — mandatory form

From `<WORKTREE>/IBKR_PAPER_BRIDGE`:

```
python -m pytest -q --ignore=TSP1009B.pytest_tmp_s1r1 -p no:randomly
```

`--ignore` is **mandatory** — `TSP1009B.pytest_tmp_s1r1/` is ACL-locked and plain `pytest` aborts
collection with `PermissionError`. **Never** pass `--basetemp` inside `.pytest_cache` (it produced
623 errors once). The run takes roughly two minutes; let it finish.

Floor at the predecessor `732b37c3`: **`2 failed, 1140 passed`**.

The two failures — a stale KVM2 ledger hash, and `test_invariants_preserve_risk_and_history`
asserting `schema_version == "2"` against default v4 — fail identically on the `origin/master` Bridge
tree, are **pre-existing**, and are outside every allowlist. They are **not** findings. **A third
failure is a required finding.**

---

## 2. WHY THIS CYCLE EXISTS — JUDGE THE STRATEGY, NOT ONLY THE LINES

Three prior rounds each closed exactly the call sites the previous audit named, and each left the
same *defect class* open at a neighbouring site:

| Round | Scoped to close | What it left open |
|---|---|---|
| 1 | the startup-failure class | re-opened a reachable variant, dropped an event, relocated unbounded growth |
| 2 | identity *shape* validation | the store also required durable *binding*; `int()` ran before validation |
| 3 | identity parsing + durable binding + schema capability | `insert_fill` ran ahead of every guard; `_event_symbol` never got the parser |

The owner therefore stopped the point-fix strategy and authorised a **structural** cycle (D027).

> **Guard the entry point, not one line.**

**This is the central question of your audit.** A diff that adds a `try` at each of the five sites in
§3 and passes the suite is a **fourth point fix** and must be `REQUEST_CHANGES`, however clean the
code reads. Ask specifically:

- Is there **one** boundary a reviewer can point at, or a helper sprinkled at named sites?
- Is the boundary driven by a **declared column/type registry**, or by per-call-site literals?
- Does the S3T-D matrix **generate** from that registry, or does it hand-list the five known findings?
- **Find the next neighbour.** Every prior round was defeated by a site nobody had named yet. Walk
  the reachable set from a queued broker event yourself and look for a durable-row read that still
  bypasses the boundary. This is the single most valuable thing you can do in this audit.

---

## 3. THE FIVE FINDINGS THIS CYCLE MUST CLOSE — all Lead-verified on real source at `732b37c3`

SQLite columns here are **affinity-only**: no `CHECK`, no `NOT NULL`, no `STRICT`. `fills.qty REAL`
accepts non-numeric TEXT and NULL; `orders.trade_id INTEGER` accepts arbitrary TEXT. The v8→v9
migration preserves predecessor rows unvalidated **by design** (`_migrate_v8_to_v9` asserts the row
census is unchanged). Schema-admitted corruption is a reachable input, not a hypothetical.

**Class A — schema-admitted data reaches an unguarded conversion on the drain path**

- **A1** `bridge/store/db.py:7338-7339` (`insert_fill`) — bare `float(row["qty"])` / `float(row["px"])`
  in the duplicate-classification tuple, while `fee`/`funding` two lines below use `or 0.0`.
  `insert_fill` runs ahead of every guard round 3 added.
- **A2** `bridge/engine/orders.py:2670` (`_event_symbol`) — raw `int(order["trade_id"])`;
  `_parse_store_trade_id` exists at `2687` but was applied at only `2727` and `3229`. `_event_symbol`
  runs for **every** queued event, on **both** drains, before any guard.
- **A3** `bridge/engine/orders.py:2856-2860` (`_canonical_status`) — `float(...)` computed **outside**
  its own `try`, which does not open until `2864`.

Escape route, identical in every case:

```
BridgeEngine.start() → order_manager.reconcile() → sync_broker_state()
  → drain_queued_events() → _ingest_queued_event() → _ingest_event() → _ingest_fill()
```

`_ingest_queued_event` catches only `KillConflictError`. Everything else unwinds through the
**unguarded** `BridgeEngine.start()` and the `app.py` lifespan hook: **the bridge does not start and
no durable evidence is written.**

**Class B** — `_parse_store_trade_id` is type-total but not storage-boundary safe: it accepts any
Python `int` or Unicode-decimal string without SQLite signed-64-bit bounds validation. A value above
`2**63 - 1` parses in Python and then raises `OverflowError` when `sqlite3` binds it in `get_trade`.

**Class C — the close path never re-derived its binding (the most serious).**
`close_trade_once_with_decision` fenced the **epoch** (`_assert_kill_epoch_in_tx` plus the
`kill_requests` `EXISTS` predicate) but the fenced `UPDATE` contained **no join back to `orders`**.
With active epoch A: `Store` 1 validates a `KILL_FLATTEN` order bound to episode A / trade T;
`Store` 2 clears or changes `orders.group_id`; `Store` 1 continues down the active-epoch branch and
closes T, writing `TRADE_CLOSED` with no identity quarantine. Round 3's two-`Store` test missed this
because it runs with **no active epoch** and never reaches the close path.

---

## 4. WHAT WAS REQUIRED — audit against this, not against your own preferred design

**S3T-A — validated accessor boundary.** One typed accessor layer for reading durable
`orders`/`fills`/`trades` values. Every durable-row read on any path reachable from a queued broker
event goes through it. It returns **a validated typed value or a containable fault** and never raises
an unguarded `ValueError`, `TypeError`, `OverflowError`, or `decimal.InvalidOperation` into its
caller. Per served column it must contain: `NULL`; non-numeric TEXT; unexpected storage class;
integer outside signed 64-bit; non-finite float (`NaN`, `±inf`). Faults carry a stable reason code.
It must be **one boundary driven by a declared registry**, not scattered guards.

**S3T-B — close path re-derives its binding.** Inside the existing `BEGIN IMMEDIATE`,
`close_trade_once_with_decision` re-derives that the trade is *currently* bound to the active episode
— joining `orders` on (`role='KILL_FLATTEN'`, `group_id` = active `episode_id`, `trade_id` = the
trade being closed). If the binding no longer holds: **roll back, write durable evidence, fail
closed.** The existing epoch fence — `_assert_kill_epoch_in_tx`, the `kill_requests` `EXISTS`
predicate, the stale-epoch rollback + EP-4 append + raise-to-caller — must be **intact and
unweakened**. Verify that specifically. The non-kill (`resolved_epoch is None`) branch keeps its
current behaviour.

**S3T-C — entry-point containment.** Every entry point reachable from a queued broker event uses the
boundary, explicitly including `_event_symbol` and `_canonical_status`.

**S3T-D — the matrix acceptance suite.** Generated **from the S3T-A registry**, enumerating every
durable column reachable from a queued event × every corruption case, asserting for **every**
combination: (1) `BridgeEngine.start()` returns normally; (2) durable evidence exists for the fault;
(3) the system is fail-closed — `app_state` durably `KILLED`, ARM refuses, ACK unreachable, trade
left open; (4) the queue and the deferred map end consistent (no silent event drop, no unbounded
growth — round 1 relocated exactly that defect). Plus a two-`Store` test **with an active epoch**
proving the close path refuses when the binding breaks mid-flight.

**Deliberate design decision — judge it, do not report it as a discovery.**
`KILL_STALE_EVIDENCE_RECORD_FAILED` **keeps propagating** by Lead decision. It means the durable
evidence store itself cannot be written; no durable evidence can be recorded when the evidence store
is the failing component, so halting with `app_state` durably `KILLED` is the honest fail-closed
outcome. Identity and schema-capability faults are **contained**; evidence-store outages
**propagate**. If you believe that decision is wrong, argue it as a nit with reasoning — it is not a
required repair.

### Allowlist — a change outside this set is a required finding

```
IBKR_PAPER_BRIDGE/bridge/engine/orders.py
IBKR_PAPER_BRIDGE/bridge/store/db.py
IBKR_PAPER_BRIDGE/tests/test_engine_dryrun.py
IBKR_PAPER_BRIDGE/tests/test_store.py
IBKR_PAPER_BRIDGE/docs/31_KILL_EVIDENCE_EPOCH_CONTRACT.md
```

`bridge/engine/engine.py` is **not** allowed.

**Out of scope — do not require these:** TS-P1-010+ · EP-1's residual venue-side supersede window
(Hyperliquid exposes no fencing token — a documented accepted limitation) · dashboard/read-model
redesign · **any migration, foreign key, `STRICT` table, `CHECK` constraint, or schema-version
change — the fix is defensive reading, not schema repair** · changing the default schema target away
from v4 · alerting redesign · re-opening accepted S2 mechanisms.

---

## 5. MANDATORY CHECKS — answer every one explicitly

1. **Suite executed?** Paste the literal final `pytest` line. If you could not run it, return `BLOCK`.
2. **Third failure?** Anything beyond the two pre-existing failures is a required finding.
3. **Existing tests weakened?** `git diff 732b37c3..34d35286 -- IBKR_PAPER_BRIDGE/tests/` and read
   every `-` line. Any deleted, skipped, `xfail`-ed or loosened existing assertion is a **required**
   finding. **This rule was broken once already in this programme — check it, do not assume.**
4. **One boundary or scattered guards?** Name the construct. If you cannot name one, say so.
5. **Registry-driven?** Is the matrix generated from the declared registry, or hand-listed?
6. **The next neighbour.** Walk the reachable set from a queued broker event and name any durable-row
   read that still bypasses the boundary. This is what defeated all three prior rounds.
7. **Class C.** Does the fenced `UPDATE` now join `orders` on role + `group_id` + `trade_id` inside
   the same `BEGIN IMMEDIATE`? Is the epoch fence still intact? Does a broken binding roll back,
   write evidence, and leave the trade open?
8. **Boundary totality.** Can any input make the accessor itself raise? Consider `bytes`/`memoryview`
   storage class, `Decimal('NaN')`, subnormals, `bool` where `int` is expected, and a value exactly at
   `±2**63`.
9. **Allowlist respected?** `git diff --name-only 732b37c3..34d35286`.
10. **Anything that reaches a broker, network, ARM, or live path?** There must be none. This cycle is
    DISARMED-only.

---

## 6. REPORT FORMAT — end with exactly this

```
VERDICT: PASS | PASS-WITH-NITS | REQUEST_CHANGES | BLOCK

SUITE RUN     : yes | no
SUITE RESULT  : <literal final pytest line>
THIRD FAILURE : none | <which>
TESTS WEAKENED: none | <exact '-' lines>

REQUIRED FINDINGS (numbered; each with file:line, why it is reachable, and the failing scenario)
  R-1 ...

NITS (optional, non-blocking)
  N-1 ...

STRUCTURAL JUDGEMENT: <one boundary, or a fourth point fix? name the construct>
NEXT NEIGHBOUR      : <any unrouted durable read you found | none found, and how you looked>
```

Every required finding must be **reproducible from your description alone** — the Lead reproduces
each one on real source before it binds, and a finding that does not reproduce is recorded as
unreproduced rather than spending a capped repair round.
