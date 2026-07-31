# WP-S — TS-P1-009B S2 CLOSURE + MINIMUM S3 (2026-07-31)

**Work package:** WP-S of the accepted 50-Hour DISARMED Safety MVP plan.
**Budget:** 12 h (S2 repair 4 h · Audit-1 first pass 2 h · S3 implementation 4 h · S3 Gate-5 2 h).
**Status:** **S2 CLOSURE ACCEPTED.** Minimum S3 in progress.
**Lead Orchestrator / acceptance authority:** Claude `claude-opus-5`.
**Implementer:** Codex CLI `gpt-5.6-sol`, effort `xhigh`.

Authorisation: standing owner prompt `11_TRIAGE/OWNER_AUTH_50H_EXECUTION_PROMPT_2026-07-31.md`,
including the Gate-1 authorisation for a **NEW** S2 repair cycle. The historical three-round loop
is closed and spent; this cycle carries its own bound of three non-accepting rounds.
Scope frozen in `11_TRIAGE/WP0_SCOPE_BASELINE_RECORD_2026-07-31.md`.

## 1. Branch and artifact chain

| Commit | Meaning |
|---|---|
| `678e8b946e34a55eca85f88d2e6ca54514b182f7` | parent — the terminally blocked S2 artifact |
| `d3a455291e37671b057ce435a39ad5e982e024c6` | round 1 — **non-accepting** (introduced R1) |
| **`0c65a73196428ac1da758c4c80ce7282a7ab46fe`** | **round 2 — ACCEPTED** |

Branch `feature/ts-p1-009b-s2-closure`, isolated worktree `C:/WPS`, pushed to `origin`.

**Branch base is `678e8b94`, not `origin/master`** — a recorded deliberate deviation from the
authorisation's generic instruction, because WP-S continues the accepted S1 stack. It is safe:
`merge-base(678e8b94, origin/master) = 3cccc4c2`, and the Bridge tree is byte-identical between
`3cccc4c2` and the live master, so branching here equals branching from master plus the accepted
S1 stack, with zero Bridge conflict surface.

## 2. Test floor

Environment: Python 3.14.2, pytest 9.0.2, CWD `IBKR_PAPER_BRIDGE`,
`--ignore=TSP1009B.pytest_tmp_s1r1 -p no:randomly`.

| Artifact | Result |
|---|---|
| `678e8b94` (entry floor) | **2 failed, 1113 passed** |
| `d3a45529` (round 1) | 2 failed, 1117 passed (+4 tests) |
| `0c65a731` (round 2, accepted) | **2 failed, 1118 passed** (+5 tests) |

The two failures — `test_canonical_ledger_and_all_three_row_fixtures_validate` (stale KVM2 ledger
artifact hash) and `test_invariants_preserve_risk_and_history` (`assert '4' == '2'`, stale
expectation against default schema v4) — were independently confirmed by the Lead to fail
**identically on the `origin/master` Bridge tree**, so neither is caused by this branch. Both are
outside the frozen allowlist and were not touched.

Floor held at every checkpoint. No third failure, neither pre-existing failure "fixed".

## 3. The two S2 blockers — closed

Both were located on real source by the Lead before any dispatch, not restated from a report.

### B1 — sub-1e-12 `trades.exit_px` / `pnl` tampering evaded detection and permitted ACK/DISARM

At `678e8b94`, `db.py` `_assert_kill_flatten_closure_in_tx` compared the durable `trades` row to
the recomputed expectation with `math.isclose(..., rel_tol=0.0, abs_tol=1e-12)`, while the parallel
`TRADE_CLOSED` decision-payload comparison ten lines above was **exact** with a type check. Any
perturbation below 1e-12 absolute passed, and the episode proceeded to ACK/DISARM on tampered
durable evidence.

**Closed by** holding the `trades` row to the same exactness as the payload — raw storage-type
equality plus exact `!=` — and, critically, by **unifying the write path** rather than relaxing the
comparison. Write and verify previously duplicated the same arithmetic without sharing it; both now
call one `_canonical_trade_close_values` helper.

**Lead-verified residual risk, closed at source.** Exact comparison is only correct if write and
verify select identical inputs. Their source-selection conditions *look* divergent
(`orders.py:3129` uses `totals["entry_qty"] > 0 and totals["entry_vwap"] is not None`;
`db.py:6387` uses `float(totals["entry_qty"] or trade["qty"])`). Both auditors suspected this and
neither proved it. The Lead verified it directly: `db.py:7519-7522` sets `entry_qty` **and**
`entry_vwap` inside the same `if entry["qty"] > 0` block, so `entry_qty > 0` ⟺
`entry_vwap is not None` and the divergent state is structurally unconstructible. `exit_vwap` and
`costs` come from the same `trade_fill_totals` / `trade_costs` calls on both sides, computed in
`Decimal` then converted — identical inputs, identical floats. **No false-positive fail-closed
risk.**

The `exit_qty` vs `entry_qty` `abs_tol=1e-12` at `db.py:6424` was deliberately **retained**: it is
an aggregate *completeness* check on independently quantized quantities, not persisted
evidence-integrity. Both auditors confirmed the distinction.

### B2 — stale recovery could commit the lifecycle close before the post-ingestion epoch rejection

At `678e8b94`, `orders.py:1662-1680` asserted epoch ownership on *either side of* the
`_ingest_fill` commit rather than inside it. If the epoch was invalidated between the pre-check and
the commit, the trade close was already durable when the post-ingestion assertion raised. A
superseded recovery process could commit a lifecycle close a newer epoch had already revoked —
exactly the failure class `31_KILL_EVIDENCE_EPOCH_CONTRACT.md` §Objective item 2 exists to prevent.

**Closed by** moving the fence one layer down into `close_trade_once_with_decision`: `BEGIN
IMMEDIATE` → `_assert_kill_epoch_in_tx` → `UPDATE trades` → `INSERT decisions` → `commit`, with any
`KillConflictError` rolling back both writes and recording the stale-write rejection. Because the
fence sits at the store boundary, it also covers the **live/query flatten route**, not just restart
recovery. The existing CAS was reused (`meta.kill_epoch_active`, `kill_requests.epoch_token`,
`_owned_kill_epoch`); no second mechanism was invented.

## 4. R1 — the round-1 regression, and how it was caught

Round 1 closed B1 and B2 but made a caller-owned epoch **unconditionally required** for every
`exit_reason == "KILL_FLATTEN"` close, while the engine supplies that epoch only from
`_active_kill_epoch` — legitimately `None` on every non-kill path, **including the ordinary
reconcile drain that runs first on every startup**.

Failure path: crash mid-flatten → restart → broker re-delivers the flatten fill with
`role="UNKNOWN"` (skipping the role-conflict quarantine, since `_order_specs` is in-memory and
empty after restart) → `get_order` resolves the durable order with `role="KILL_FLATTEN"` →
`close_trade_once_with_decision(epoch=None)` → `KILL_EPOCH_REQUIRED`.

**There is no handler anywhere on that chain** — not in `drain_queued_events`, `sync_broker_state`,
`OrderManager.reconcile`, or `BridgeEngine.start`. The Lead confirmed this directly in source. The
exception propagates through the `app.py` lifespan hook and **the bridge does not start**: no API,
therefore no `/api/kill`, therefore no route to close the lifecycle — a hard wedge requiring a code
change or manual DB surgery. The parent commit closed that same drain cleanly.

**Repaired in round 2 by containment, not by weakening the rule:**

| Case | Behaviour |
|---|---|
| `epoch is None` (ordinary drain — no kill authority) | `_ingest_fill` returns `False`; the existing `pending` mechanism keeps the event queued; startup completes; a later epoch-owning `/api/kill` recovery closes the lifecycle |
| `epoch` present but stale | unchanged from round 1 — rejected inside `BEGIN IMMEDIATE`, both writes roll back, stale-write rejection recorded, raises |
| direct store call, epoch-less `KILL_FLATTEN` | still raises `KILL_EPOCH_REQUIRED` |

No path can commit an unowned close.

The implementer also caught its own neighbour route mid-build: an initial N2 CAS formulation
referenced `kill_requests` unconditionally, which would have broken ordinary non-kill closes on v4
stores that lack that table. The final version keeps the table-free `UPDATE` for non-epoch closes
and binds `epoch_token` only on the fenced path. **First time in five rounds the implementer found
the neighbour itself.**

## 5. Lead independent verification — performed, not delegated

Per the authorisation, no implementer or auditor report was accepted without inspecting real
repository state.

**Round 1:** built a throwaway worktree at the unrepaired `678e8b94`, copied only the new test
file, and reproduced RED for the right reasons — both one-ULP tampers gave
`Failed: DID NOT RAISE KillConflictError`, and the stale-recovery case gave
`AssertionError: assert '2026-07-31T13:19:05.374000+00:00' is None`, i.e. the close **was** durably
committed under a revoked epoch. Worktree removed after.

**Round 2:** built a throwaway worktree at `d3a45529`, copied only the new test file, and
reproduced R1's RED — `KillConflictError: KILL_EPOCH_REQUIRED` raised out of `drain_queued_events`
— **with the four round-1 B1/B2 tests still passing there**, isolating R1 to exactly one defect.
Worktree removed after.

**Both rounds:** re-ran the full suite personally; traced `role = str(order["role"])` at
`orders.py:3009` (the durable *order* role, not the FillEvent role) to confirm the recovery path
reaches the fence via `kill_close_alias`; verified `_assert_kill_epoch_in_tx` is a real CAS
(process-local ownership **plus** in-transaction `meta.kill_epoch_active` token compare); checked
all three `_ingest_fill` call sites; and secret-scanned the docs diff (clean).

## 6. Audit 1 (Gate-5) — checkpoint 1

Both auditors ran in **fresh independent sessions**, never resumed from the implementer.

| Round | Artifact | Codex `gpt-5.6-sol` xhigh | Claude `claude-opus-5` xhigh | Net |
|---|---|---|---|---|
| 1 | `d3a45529` | BLOCK — 0 code defects, environmental | REQUEST_CHANGES — 1 required (R1) | **non-accepting** |
| 2 | `0c65a731` | **PASS-WITH-NITS — 0 required** | **PASS-WITH-NITS — 0 required** | **ACCEPTED** |

Two of the three permitted non-accepting rounds remain unused.

**Round-1 Codex BLOCK was a dispatch defect, not a code defect.** `codex exec --ephemeral -s
read-only` provides no writable temporary directory, so pytest died with
`FileNotFoundError: No usable temporary directory found` before collection. It could not reproduce
the mandated suite and correctly refused to accept on unverified test evidence. Its source audit
found zero required defects. Fixed for round 2 by giving the auditor a dedicated worktree at the
frozen SHA with `-s workspace-write`; **`git status --porcelain -uno` was verified empty afterwards
and HEAD unchanged**, proving it edited nothing, so the audit's independence holds.

**Round 2, both auditors independently re-ran the suite** and both reported `2 failed, 1118
passed`. Key proofs established:

- `close_trade_once_with_decision` has **exactly one** production caller, so the `return False`
  deferral in front of it is a complete fence, not a partial one.
- Both kill-path `_ingest_fill` callers (`orders.py:1285`, `:1666`) are preceded by
  `_assert_kill_epoch_active()` with **no `await` in between**, so the new `return False` is
  unreachable there — no kill episode silently degrades to UNKNOWN.
- The deferral is **fail-safe, not silent**: `app_state` stays durably `KILLED`, `arm()` raises on
  `previous == "KILLED"`, ACK cannot pass without the closure, and `status().kill_episode` surfaces
  the unresolved episode.
- The new `EXISTS (SELECT 1 FROM kill_requests …)` predicate is **dead** —
  `_assert_kill_epoch_in_tx` asserted the identical condition one statement earlier in the same
  transaction and `kill_requests.episode_id` is PRIMARY KEY — so it cannot reclassify a real stale
  write as a benign `TRADE_CLOSE_RACE` and no EP-4 evidence is lost.
- Retaining `_active_kill_epoch` cannot authorise a bad close: `_owned_kill_epoch` clears in
  `close_kill_epoch`, `_assert_kill_epoch_in_tx` additionally requires `ack_state == 'PENDING'`, and
  both `SAFE_FLAT` routes run the lifecycle validation, so a late fill hits the `POST_CLOSE_FILL`
  quarantine rather than the close branch.
- No tautological tests: both epoch tests construct a distinct `competitor = Store(db_path)` over
  shared storage and assert `competitor is not store`.

**The two-auditor roster earned its cost again.** On round 1, Codex found zero required defects
while Claude found R1 and reproduced it on both trees. That matches all three historical rounds:
each auditor catches what the other misses. One accepting verdict is never treated as clearance.

## 7. Nits carried forward — deliberately not applied to `0c65a731`

Editing the accepted commit would void its acceptance and force a re-freeze plus re-audit under
§20/§22, consuming WP-R hours for no safety gain. All nits are therefore folded into the **minimum
S3 dispatch**, which produces a new artifact that receives its own Gate-5 regardless.

1. `db.py:7364` — bare `assert not self.conn.in_transaction`, stripped under `python -O`, and the
   only such guard among ~30 `BEGIN IMMEDIATE` sites.
2. `db.py:7382-7387` — the dead `EXISTS` predicate: keep with a justifying comment or drop.
3. **Sharpest.** A *stale* non-`None` epoch would still raise `KillConflictError` out of
   `drain_queued_events` — the same handler-less chain that made R1 a wedge. Unreachable today, one
   refactor away. Containment belongs at the drain as a class.
4. `_queued_events` is unbounded and absent from `status()`; the deferral path deliberately does not
   populate `_synced_fills`, so broker redelivery accumulates.
5. `docs/…:81` — EP-6 says "Every applied KILL flatten"; should be *fully applied / ACK-eligible*,
   since a partial flatten is durably `APPLIED` but deliberately leaves the trade open.
6. `docs/…:166` — says every periodic drain has epoch `None`, but the manager retains its last
   epoch; a stale retained epoch is **rejected**, not deferred.
7. A test assertion (`conn.in_transaction is False` after `KILL_EPOCH_REQUIRED`) is trivially true
   and asserts nothing.

## 8. Minimum S3 — Lead Gate-1 scope definition

The plan §16 names the second half of WP-S as **"minimum S3 (initial liveness/lifecycle proof)"**.
**No further S3 specification exists anywhere in the repository** — searched `11_TRIAGE`,
`_AI_MEMORY`, and `IBKR_PAPER_BRIDGE/docs`. Gate 1 is Lead-owned, so the Lead froze the scope
rather than blocking on an absent spec. Recorded here as an unattended decision.

Rationale: S1 established epoch **identity and ownership**; S2 established evidence **integrity and
epoch-fenced closure**; minimum S3 establishes that the episode **lifecycle actually progresses,
and that a non-progressing one is durably visible and blocking rather than silently pending** —
which is precisely what "liveness/lifecycle proof" means here, and precisely where the accepted
nits cluster.

| Item | Requirement |
|---|---|
| **S3-1** | Durable, **idempotent**, secret-safe deferral evidence, following the EP-4 `KILL_EPOCH_STALE_WRITE_REJECTED` precedent. The S2 deferral is currently silent. |
| **S3-2** | Explicit liveness in the existing status payload — open lifecycle awaiting epoch-owned recovery, plus deferred-queue depth. **Minimum fields only**; TS-P5-001 read-model redesign stays deferred. |
| **S3-3** | Containment as a class: `drain_queued_events` catches `KillConflictError`, defers, and records — so the R1 wedge class cannot return via a stale-epoch route. **Must not weaken B2**: the store fence stays authoritative, stale epochs still roll back, still record EP-4, still raise to the store's caller. No blanket `except Exception`. |
| **S3-4** | Queue-growth disposition: de-duplicate deferred events by `fill_id`, **or** bound the queue — and if bounded, **overflow must fail closed and latch a durable fault. Never drop an event.** |
| **S3-5** | Fold nits 1–7 above. |

**Explicitly out of scope:** TS-P1-010 and beyond; EP-1's residual venue-side supersede window
(Hyperliquid exposes no fencing token — a documented, accepted limitation, not an S3 task); any
operations-dashboard or read-model redesign; any migration; any schema-default change; any alerting
redesign.

Allowlist as for S2, plus `bridge/engine/engine.py` **only** for the S3-2 status payload.

## 9. Hour accounting — WP-S so far

| Activity | Budgeted | Actual |
|---|---:|---:|
| S2 blocker repair (rounds 1 + 2, implementer) | 4 h | 4.0 h |
| Audit-1 first pass (S2 accepting verdict) | 2 h | 2.0 h |
| S3 implementation | 4 h | in progress |
| S3 Gate-5 | 2 h | pending |
| **WP-S subtotal** | **12 h** | **6.0 h consumed** |

Round-1 re-audits at this checkpoint draw on WP-R per §20; the Audit-1 first pass is funded from
WP-S per §16. No audit activity was funded twice. **No contingency hours were consumed** — R1 was
repaired inside the round-1 → round-2 loop of the authorised cycle, not as a post-acceptance repair.

Approximate AI spend attributable to WP-S so far: ~$35 (two `xhigh` implementer dispatches, four
`xhigh` audit sessions, Lead verification).

## 10. Known leftovers

`C:/WPSAUD` — the temporary Codex audit worktree. Deregistered from Git (`git worktree list` no
longer shows it, no `.git` file remains) but the directory could not be fully deleted:
`IBKR_PAPER_BRIDGE/.pytest_cache` is ACL-locked, the same Windows ACL pattern as
`TSP1009B.pytest_tmp_s1r1`. Harmless disk residue, no Git effect. Left in place rather than
escalating privileges.

## 11. Safety statement

No implementation outside the frozen allowlist. No risk threshold invented or changed. No
credential, wallet secret, API key, or private infrastructure identifier read, written, or sent to
any model — the docs diff was independently secret-scanned clean. Default schema target remains v4;
no migration executed. No Pine, parity, MTC strategy, or protected-scope file touched. No bridge
start, broker call, network, staging, Ubuntu execution, VPS, deployment, TESTNET, ARM, or
live-capital action occurred.
