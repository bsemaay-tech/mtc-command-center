# 26 — Full Reconciliation Contract (TS-P1-005)

Status: implemented, **opt-in**. Default schema stays v4; nothing in this
contract is active on a v4 or v5 runtime database.

TS-P1-006 extension: newly accepted captures use
`ts-p1-006-snapshot-v2`, adding canonical positions/balances/margin rows to
the existing immutable checkpoint JSON. Historical v1 checkpoints remain
valid retained reconciliation evidence but are not risk-readable and cannot
authorize v6 ARM. See `27_AUTHORITATIVE_RISK_SNAPSHOT_CONTRACT.md`.

Predecessor: TS-P1-004 partial-fill protection (`25_PARTIAL_FILL_PROTECTION_CONTRACT.md`),
commit `7f72f71c`.

Owner decisions in force: **D1=B, D2=A, D3=A, D4=A** (Gate 1, 2026-07-26).

---

## 1. Purpose

Obtain authoritative, read-only broker evidence for orders, fills, positions,
balances, margin and funding; read the durable local intent and pending-action
state; compare them deterministically; and commit exactly one atomic outcome:

1. an accepted, immutable checkpoint with source timestamps, collection bounds,
   reason codes and evidence lineage, **or**
2. a failed/incomplete attempt that leaves the previous accepted checkpoint
   untouched, sets full readiness false, and keeps the bridge DISARMED.

An incomplete or ambiguous collection is never treated as success.

Nothing here mutates exchange state. There is no cancel, adopt, re-protect,
flatten or retry in this path.

## 2. Components

A complete capture carries all seven components (`ReconcileComponentKind`):

| Component | Source | Notes |
| --- | --- | --- |
| `OPEN_ORDERS` | exchange | live order rows, keyed by cloid |
| `FILLS` | exchange | time-paginated over the capture window |
| `POSITIONS` | exchange | derived from one account read |
| `BALANCES` | exchange | equity, withdrawable — same read as positions |
| `MARGIN` | exchange | margin used, available — same read as positions |
| `FUNDING` | exchange | signed ledger keyed by the exchange event hash |
| `PENDING_ACTIONS` | local | TS-P1-003 quarantine + TS-P1-004 recovery rows |

A component is *accepted* only when its status is `COMPLETE` **and** it is
exact, complete, and carries an observation timestamp. Anything else —
`UNAVAILABLE`, `TRUNCATED`, `MALFORMED`, `CONFLICTING`, `STALE` — makes the
whole attempt non-accepting. A healthy component is never reused from an
earlier observation to patch a composite.

## 3. Attempt lifecycle

States: `COLLECTING` → one of `COMPLETE` / `INCOMPLETE` / `CONFLICTING` / `STALE`.

Ordering, strictly:

1. Check the **global full-writer guard**. An overlapping full attempt is
   *refused*, not queued.
2. Reserve the attempt durably (`reconcile_attempts`, `COLLECTING`) — before
   any broker I/O.
3. Acquire the guard, then drain queued broker callbacks through
   `OrderManager.drain_queued_events()` under the existing per-symbol writer
   locks, so the capture sees one coherent local epoch.
4. Collect read-only evidence.
5. Validate the envelope, then every component.
6. Compute the deterministic diff.
7. Persist snapshot, diff, provenance, verdict and pointer **atomically**, last.

No SQLite transaction spans broker I/O. Lock order is always
*full-writer guard → symbol locks*; it is never inverted.

`COMPLETE` + no blocking diff → accepted, and the latest-accepted pointer
advances. `COMPLETE` collection + at least one blocking diff → `CONFLICTING`,
not accepted.

## 4. Readiness (distinct from the light path)

`OrderManager.reconcile()` keeps sole ownership of the existing light
`reconcile_ready` flag. TS-P1-005 adds a **separate** gate:

- `Store.full_reconcile_ready(now, max_age_s)` is true only for a *fresh*
  accepted v6 checkpoint resolved through the single transactional pointer,
  **and only while that checkpoint's attempt is still the most recently
  resolved attempt** (`Store.latest_resolved_reconcile_attempt_id()`). Any
  later failed, conflicting, stale or restart-interrupted attempt makes
  readiness false immediately, however young the checkpoint is — freshness
  alone must never let a checkpoint outvote newer contradicting evidence.
- `BridgeEngine.full_reconcile_ready()` returns false on any non-v6 store,
  **and false while `full_reconcile_error` is non-`None`**. That latch is
  sticky: only a fresh accepted capture clears it. Neither `arm()` nor a light
  reconcile recovery may clear it.
- On a v6 store, `arm()` requires **both** gates. Light success can never
  satisfy the full gate, because only `finalize_reconcile_attempt(accepted=True)`
  writes a checkpoint.
- A checkpoint accepted in the future (clock rollback) is not fresh.

### Freshness bound (owner policy)

The full checkpoint's maximum age is **not** a new constant. It reuses the
existing accepted light formula, evaluated at call time:

```
BridgeEngine.full_reconcile_max_age_s() == max(reconcile_interval_s * 3, 30.0)
```

Changing the health cadence therefore moves both bounds together, and there is
no second, unratified freshness policy anywhere in this path.

On a v4/v5 store, predecessor ARM behavior is bit-for-bit unchanged.

### Separate failure budgets

`_run_reconcile_cycle` runs the light path in `_run_light_reconcile_cycle()`
and then calls `run_full_reconcile()` **outside** that try/handler.
`run_full_reconcile()` swallows every non-`CancelledError` exception into
`full_reconcile_error` (secret-safe: `FULL_RECONCILE_CYCLE_FAILED:<TYPE>`).

A full ledger or capture failure therefore can never:

- increment `_consecutive_reconcile_failures`,
- change `reconcile_ready` / `reconcile_error`,
- emit `RECONCILE_FAILED` / `RECONCILE_FAILED_TOLERATED`, or
- disarm through the light budget.

It only latches the full gate shut and records `FULL_RECONCILE_BLOCKED`.
`asyncio.CancelledError` is re-raised unchanged on both paths.

## 5. Temporal envelope (D2=A)

| Rule | Value | Failure |
| --- | --- | --- |
| Whole-capture deadline | 5 s, monotonic | `FULL_RECONCILE_DEADLINE_EXCEEDED` |
| Max component source skew | 5 s | `FULL_RECONCILE_SOURCE_SKEW` |
| Source timestamp in the future | > 5 s past end | `FULL_RECONCILE_SOURCE_IN_FUTURE` |
| Source older than the start | > 5 s before start | `FULL_RECONCILE_SOURCE_STALE` |
| End before start | any | `FULL_RECONCILE_CLOCK_ROLLBACK` |
| Adapter client pair swapped mid-capture | any | `FULL_RECONCILE_CLIENT_REBUILT` |

The deadline is **enforced during collection, not only checked afterwards**.
Every adapter await runs under `asyncio.timeout(remaining_budget)`, where
`remaining_budget = deadline_s − monotonic_elapsed`. A hung adapter call is
cut off, the component becomes `STALE` / `<COMPONENT>_DEADLINE_EXCEEDED`, any
remaining component is skipped without issuing I/O, and the whole attempt
resolves `STALE` / `FULL_RECONCILE_DEADLINE_EXCEEDED` in bounded wall time with
no checkpoint. The post-hoc monotonic check remains as a second, independent
guard. `asyncio.timeout` cancels the *current* task instead of wrapping the
call in a child task, so an outer `CancelledError` and a real `BaseException`
kill both propagate exactly as before.

Elapsed time is measured monotonically; the durable evidence keeps UTC bounds.
A restart never resets a deadline — it resolves the dangling attempt as
`INCOMPLETE` instead.

These values govern only the new capture. The light reconcile interval and its
consecutive-failure budget are untouched.

### Bounded REST budget (Gate-2 proof)

One capture on the Hyperliquid adapter issues **four** reads:

| Call | Components produced |
| --- | --- |
| `Info.user_state` | `POSITIONS` + `BALANCES` + `MARGIN` |
| `Info.open_orders` | `OPEN_ORDERS` |
| `Info.user_fills_by_time` | `FILLS` (1 page for an ordinary window) |
| `Info.user_funding_history` | `FUNDING` (1 page for an ordinary window) |

Deriving positions, balances and margin from a single `user_state` read is
deliberate: those three components then share one observation timestamp, so
intra-account skew is structurally zero. Paginated components are hard-capped
at `FULL_RECONCILE_MAX_PAGES` (32) each, so the worst case is
`2 + 2×32 = 66` calls, and exceeding the budget is `TRUNCATED`, never a longer
deadline. `test_bounded_rest_call_budget_is_four_reads` asserts the nominal
four-call budget offline.

## 5b. Fills/funding coverage — durable continuity, no fixed lookback

There is **no history-window constant**. An arbitrary lookback would either
re-read time already proven or, worse, silently skip time nobody observed. The
window is derived from durable state instead:

| Case | Lower bound |
| --- | --- |
| Before the first acceptance | `min(` current run's durable `runs.started_ts`, `MIN(reconcile_attempts.started_ts)` `)` |
| Every capture after an acceptance | The common `cursor_end_ms` of the pointed checkpoint's immutable `FILLS` and `FUNDING` components |

The upper bound is always the capture's own `started_ts`.

The pre-acceptance floor takes the attempt ledger into account deliberately.
Until something is accepted there is no accepted coverage evidence, and the *current*
run's start alone is not a safe floor: a run that observed for hours, never
accepted, and was then restarted under a new `run_id` would hand the new run a
lower bound after the old run's observation window and silently drop the
interval in between. `Store.earliest_reconcile_attempt_started_ts()` reads
`MIN(started_ts)` over the append-only, identity-frozen `reconcile_attempts`
table (UTC-normalized), which is durable evidence of when observation actually
began and survives both restarts and a new run id. The current attempt is
already durably reserved when the bounds are computed, so it is included and
can only ever lower the floor to its own start, never raise it. Proven by
`test_coverage_floor_survives_a_restart_before_the_first_accept`.

- Coverage is derived **only on acceptance** from the immutable `FILLS` and
  `FUNDING` component bounds written in the same `BEGIN IMMEDIATE` as the
  checkpoint and sole latest-accepted pointer. A failed attempt cannot advance
  it, so the next capture's window grows to span the failure.
- Coverage is **monotonic**. A bound that would move backwards is
  `RECONCILE_COVERAGE_REGRESSION` and rolls the whole finalize back.
- An accepted attempt **must** carry a coverage bound
  (`RECONCILE_ACCEPT_REQUIRES_COVERAGE`): acceptance is the proof of coverage.
- Before accepting, `FullReconciler._coverage_failure` requires both the
  `FILLS` and `FUNDING` components to report cursor bounds that *contain*
  `[start_ms, end_ms]`. Evidence that narrowed its own window is
  `FULL_RECONCILE_COVERAGE_GAP` and is refused.
- With no accepted coverage **and** no durable run row, any lower bound would
  be invented: `FULL_RECONCILE_COVERAGE_UNPROVABLE`, before a single broker
  read. The attempt ledger does not substitute for that missing lineage — it
  can only *lower* an already provable floor. A pointer ahead of the capture
  end (clock rollback) fails the same way.
- If retention, the page budget or the deadline stop the endpoint short of the
  required interval, the component is `TRUNCATED`/`UNAVAILABLE`, the attempt
  fails closed, and coverage does **not** advance. The interval is retried,
  never skipped.
- On reopen the pointed checkpoint must contain one accepted `FILLS` and one
  accepted `FUNDING` component with coherent cursor bounds. Any residual legacy
  `reconcile_coverage_upper_bound_ms` value is unauthorized and aborts.

After a 48 h downtime the next capture therefore reads
`[last accepted upper bound, now]` in full — proven by
`test_coverage_is_continuous_across_a_48h_downtime_and_reopen`, where a funding
event 10 h into the gap is still captured (a fixed 24 h lookback would have
lost it).

## 6. Pagination and identity (authoritative API semantics)

Documented Info-endpoint behavior, verified 2026-07-26:

- A time-ranged Info response returns at most a fixed number of elements
  (500 in general; 2000 for `userFillsByTime`). Larger ranges are walked by
  using the **last returned timestamp** as the next `startTime`.
- That boundary is inclusive, so the boundary row replays. Authoritative
  identities are therefore deduplicated: an exact replay is idempotent, a
  conflicting redefinition of the same identity is `CONFLICTING`.
- **Strict cursor progress is required.** A full page that does not advance the
  cursor is `HL_CURSOR_STALLED` → `TRUNCATED`. It is never read as "the end".
- `userFillsByTime` retains only the 10 000 most recent fills. A window that
  reaches that cap cannot be proven complete → `HL_HISTORY_LIMIT_REACHED`.

### Fill identity

The documented record carries `coin, side, px, sz, time, hash, oid, …`. Identity
is the exchange `tid` when present, otherwise the documented `hash:oid:time`
triple. Nothing is invented; a row missing any of those fields fails closed.

### Funding identity (D3=A)

The documented `userFunding` record is:

```
{delta: {coin, fundingRate, szi, type: 'funding', usdc, nSamples}, hash, time}
```

- identity — `hash` (authoritative, **never synthesized**)
- signed amount — `delta.usdc`
- symbol — `delta.coin`
- effective timestamp — `time` (UTC; UTC is the storage day boundary)

A missing/blank hash, a `delta.type` other than `funding`, a blank coin, a
non-finite `usdc`, an invalid `time`, a malformed `delta`, or unprovable
pagination completeness makes the component `MALFORMED`/`TRUNCATED` and fails
the attempt. Installed SDK method: `Info.user_funding_history(user, startTime, endTime)`.

Attribution: an event whose symbol has owned-order lineage is `ATTRIBUTED`;
otherwise it is recorded as `UNATTRIBUTED` **and blocks readiness**. Funding is
a separate signed ledger — it is never folded into `fills.funding` and never
double-counted.

**Attribution is not part of the identity digest.** `funding_events.payload_digest`
is `FundingEventRecord.authoritative()` — `event_id`, `symbol`, `amount_usdc`,
`effective_ts`, `source`, `funding_rate`, `position_szi`, `n_samples` — every
one of them straight from the `userFunding` record and immutable for a given
`hash`. `attribution` is *locally derived*: the same untouched exchange event
is `UNATTRIBUTED` before its symbol has owned-order lineage and `ATTRIBUTED`
after. Hashing it would make the append-only identity a function of local
state, so the next capture after the lineage appeared would raise
`FUNDING_EVENT_IDENTITY_CONFLICT` against the event's own earlier row and lose
the whole evidence write (`FULL_RECONCILE_EVIDENCE_WRITE_FAILED`).
Attribution therefore lives in the canonical snapshot view
(`FundingEventRecord.canonical()`) and in the durable **first-seen**
`funding_events.attribution` column, which — like every other column of that
append-only table — is never rewritten by a later observation. Re-observing an
unchanged event is a no-op. Proven by
`test_attribution_change_is_not_a_funding_identity_conflict`.

## 7. Diff and ownership (D1=B)

Diffs are sorted canonically by `(kind, subject, reason_code, ownership)` and
hashed with the component digests, so identical evidence and identical durable
state always produce the same `canonical_hash` regardless of wire row order.

| Reason code | Ownership | Blocking |
| --- | --- | --- |
| `OWNED_ORDER_MISSING_ON_EXCHANGE` | OWNED | yes |
| `OWNED_ORDER_QTY_MISMATCH` | OWNED | yes |
| `OWNED_ORDER_STATUS_MISMATCH` | OWNED | yes |
| `OWNED_ORDER_SIZE_QUANTUM_UNKNOWN` | OWNED | yes |
| `ORPHAN_OWNED_CLOID` | OWNED | yes |
| `EXCHANGE_IDENTITY_CONFLICT` | UNKNOWN | yes |
| `UNKNOWN_OWNERSHIP_ORDER` | UNKNOWN | yes |
| `UNKNOWN_OWNERSHIP_POSITION` | UNKNOWN | yes |
| `POSITION_QTY_MISMATCH` | OWNED | yes |
| `POSITION_SIZE_QUANTUM_UNKNOWN` | UNKNOWN | yes |
| `ACCOUNT_ARITHMETIC_INCONSISTENT` | OWNED | yes |
| `PENDING_ACTION_DIVERGENCE` | OWNED | yes |
| `FUNDING_UNATTRIBUTED` | UNKNOWN | yes |
| `LOCAL_ORDER_STATUS_UNKNOWN` | OWNED | yes |
| **`FOREIGN_ORDER_OBSERVED`** | FOREIGN_IDENTIFIED | **no** |

### The durable local status space is closed and derived

`Store.live_local_orders()` answers "durably still live on the exchange". Its
status set is **derived**, never hand-listed:

```
LIVE_DURABLE_ORDER_STATUSES =
      {non-terminal OrderState values}
    ∪ {non-terminal RAW_ORDER_STATUS_ALIASES keys}
    ∪ {ACCEPTED, RESTING, WAITING_CHILD}        # accepted legacy live spellings
TERMINAL_DURABLE_ORDER_STATUSES =
      {TERMINAL_ORDER_STATES values} ∪ {terminal alias keys}
KNOWN_DURABLE_ORDER_STATUSES = LIVE ∪ TERMINAL
```

`ACCEPTED`, `RESTING` and `WAITING_CHILD` are spellings that
`OrderManager._normalize_success_orders()` persists verbatim; the first two are
live open-order states and the third is a child order awaiting its parent
trigger. Adding a non-terminal `OrderState` or alias now widens the live query
automatically, so a live order can no longer fall out of the comparison.

Anything outside `KNOWN_DURABLE_ORDER_STATUSES` is **not dropped**:
`Store.local_orders_with_unknown_status()` surfaces it and the reconciler emits
a blocking `LOCAL_ORDER_STATUS_UNKNOWN` diff. Such a row is neither provably
live nor provably terminal, so it must block rather than vanish.

Only an *order-level* row with a complete, non-owned identity qualifies as
observe-only foreign state. It is reason-coded, retained and never mutated.

An exchange position has no cloid of its own. Without owned-order lineage its
ownership is UNKNOWN and it blocks — a position is never "safely foreign".

Quantities are compared in **exact integer lots** using the exchange size
quantum. There is no epsilon and no cross-symbol quantum reuse; an unknown
quantum blocks the affected classification. The only tolerance anywhere in this
path is `ACCOUNT_IDENTITY_ABS_TOL = 1e-6`, applied solely to the float residue
of the money identity `available_margin == equity − margin_used`.

Higher-priority gates dominate: an active TS-P1-003 quarantine or TS-P1-004
recovery appears as `PENDING_ACTION_DIVERGENCE` and blocks. A checkpoint can
never clear a quarantine or a human re-arm latch.

## 8. Persistence — schema v6 (D4=A, opt-in)

Exactly five additive objects plus one transactional pointer:

| Object | Contents |
| --- | --- |
| `reconcile_attempts` | attempt identity, run/seq, state, UTC bounds, monotonic duration, deadline/skew envelope, completeness, freshness, canonical hash, reason |
| `reconcile_components` | one row per component: source, status, observed time, exact/complete flags, cursor/page/call metadata, normalized payload digest |
| `reconcile_diffs` | reason-coded local/exchange comparison + ownership class |
| `reconcile_checkpoints` | immutable accepted checkpoint (hash + snapshot payload) |
| `funding_events` | exchange-unique identity, symbol, signed amount, effective time, source, digest, attribution — append-only |

Pointer (the sole plain `meta` row, written in the checkpoint transaction):

| Key | Meaning |
| --- | --- |
| `reconcile_checkpoint_latest` | the latest accepted checkpoint id |
A checkpoint pointer that does not resolve, lacks a complete accepted attempt,
or lacks coherent immutable fills/funding coverage evidence fails closed on reopen.

Immutability triggers:

- `reconcile_components`, `reconcile_diffs`, `funding_events` — append-only
  (no UPDATE, no DELETE).
- `reconcile_checkpoints` — fully immutable.
- `reconcile_attempts` — resolvable exactly once: only a `COLLECTING` row may be
  updated, never back into `COLLECTING`, and identity/bounds are frozen. DELETE
  is refused.

### Migration

- `SCHEMA_VERSION_BASELINE` stays **4**. `Store.initialize()` with the default
  target never reaches v5 or v6.
- v6 is reached only through the proven chain v4 → v5 → v6. There is no skip
  migration.
- The v5→v6 step runs DDL, a pre-existing-object check, canonical topology
  validation, an evidence census and the version bump inside one
  `BEGIN IMMEDIATE`. Any failure rolls back to a valid, reopenable v5 with every
  row untouched, and leaves no v6 residue.
- Any pre-existing v6-named object, residual pointer, or census change aborts
  the whole migration.
- Reopen re-validates the exact normalized SQL of every v6 object, the PRAGMA
  topology, foreign-key integrity and the pointer.
- A `meta.schema_version` of `6` with **no** v6 objects is corrupt metadata and
  fails closed exactly like an unknown version — a meta row is not proof of a
  version.
- v3/v7/corrupt/non-canonical inputs still fail closed. No backfill:
  reconciliation evidence is only ever created by a real capture.

`bridge/app.py` is untouched; no operational database is opened at v5 or v6 by
this task. Operational activation, backup and the general storage-migration
program remain separate authorizations (TS-P2-006, D016).

### Non-regression with the interim risk path

`Store.trade_costs()` still reads **only** the `fills` table. Populating
`funding_events` cannot change the interim TS-P1-007 gross-minus-fees result,
and the ledger is not consumed by risk before TS-P1-006 / full TS-P1-007. Proven
by `test_funding_ledger_does_not_change_the_interim_risk_result`.

### v5 gating is preserved on v6

`Store.partial_protection_enabled()` is version-**≥**5, not version-equals-5.
v6 is additive on top of v5, so the TS-P1-004 recovery ledger is still present
and still authoritative there; an equality check would have silently disabled
partial-fill gating on a v6 database.

## 9. Restart and rollback

- A capture interrupted by a crash leaves its attempt `COLLECTING` on disk.
  `Store.resolve_interrupted_reconcile_attempts()` — called by
  `BridgeEngine.__post_init__` on a v6 store — resolves it to `INCOMPLETE` with
  `RESTART_INTERRUPTED`. The evidence stays visible and the accepted pointer is
  **not** touched.
- A retained pre-crash checkpoint is never "freshly reconciled". Two
  independent gates keep it shut: the resolved interrupted attempt is now the
  most recently resolved attempt (so `Store.full_reconcile_ready()` is false),
  and `BridgeEngine.full_reconcile_error` latches `RESTART_INTERRUPTED` until a
  fresh accept. Age is additionally recomputed against
  `BridgeEngine.full_reconcile_max_age_s()` (§4).
- Coverage survives the restart: the next capture resumes at the last accepted
  upper bound, so the downtime interval is read, not skipped (§5b).
- Accepted checkpoints, failed attempts, component digests, diffs and funding
  events are never deleted or rewritten.
- Code rollback may remove this path only before runtime activation. Migration
  rollback restores a verified pre-migration v5 backup under a separate
  authorization; there is no in-place downgrade. The predecessor build must
  never open a v6 operational database.
- Reason codes and digests are secret-safe: failures record an exception *type
  name* only, never a payload or credential.

## 10. Surfaces

- `bridge/engine/reconcile.py` — `FullReconciler.run_cycle()`.
- `bridge/broker/base.py` — `FullReconciliationBroker` (read-only protocol),
  `FullReconciliationUnavailable`. A missing surface is
  `FULL_RECONCILE_API_UNAVAILABLE`, i.e. a non-accepting attempt.
- `bridge/broker/hyperliquid.py` — authoritative adapters, no mutation.
- `bridge/broker/mock.py` — deterministic fixtures, per-component failure
  injection (`RAISE`, `CRASH`, any component status, `NO_TS`, `INEXACT`) and
  real awaited delays (`full_component_delays_s`) for the deadline proof.
- `bridge/store/db.py` — v6 ledger, atomic persistence, the derived durable
  status space, `local_orders_with_unknown_status()`,
  `latest_resolved_reconcile_attempt_id()`,
  `earliest_reconcile_attempt_started_ts()` and derived checkpoint coverage.
- `bridge/engine/engine.py` — separate readiness gate with the sticky
  `full_reconcile_error` latch, the cadence-derived freshness bound, the
  separate failure budget, status fields (`full_reconcile_ready`,
  `last_full_reconcile_ts`, `full_reconcile_error`,
  `full_reconcile_attempt_id`), and one capture per health cycle.
- `bridge/engine/types.py` — reconciliation vocabulary and the derived durable
  order-status sets. **No** fixed history-window constant.
- `bridge/engine/orders.py` — `drain_queued_events()` epoch drain;
  `sync_broker_state()` behavior unchanged.

## 11. Test evidence

`tests/test_reconciliation.py` (45 tests) plus additions to `test_store.py`,
`test_mock_broker.py`, `test_hyperliquid_broker.py` and `test_engine_dryrun.py`.

The three semantic predecessor-RED tests:

1. `test_red1_complete_capture_is_order_independent_and_survives_reopen`
2. `test_red2_missing_fills_component_blocks_and_retains_prior_checkpoint`
3. `test_red3_crash_after_reserve_leaves_no_partial_checkpoint`

All three fail on `7f72f71c` (no `bridge.engine.reconcile`, no v6 store API, no
broker surface) and pass only with this behavior.

### Repair-round-1 regressions (audit BLOCK closure)

| Repair | Test |
| --- | --- |
| R1 live status set (present/absent) | `test_live_local_orders_include_every_derived_live_status`, `test_live_local_orders_exclude_every_terminal_status` |
| R1 unknown status blocks | `test_unknown_durable_status_is_never_silently_dropped`, `test_unknown_durable_order_status_blocks_the_capture`, `test_durable_status_space_is_derived_from_the_order_state_contract` |
| R2 readiness recency | `test_a_later_failed_attempt_makes_a_young_checkpoint_not_ready`, `test_a_restart_interrupted_attempt_makes_readiness_false`, `test_a_later_failed_capture_blocks_arm_even_with_a_young_checkpoint`, `test_a_dangling_capture_resolved_on_reopen_blocks_arm` |
| R3 separate budgets | `test_full_ledger_failure_never_consumes_the_light_failure_budget` |
| R4 real 5 s bound | `test_hung_broker_call_fails_closed_within_the_wall_clock_deadline`, `test_a_delay_inside_the_budget_still_completes` |
| R5 coverage continuity | `test_first_capture_starts_at_the_durable_run_start`, `test_coverage_is_continuous_across_a_48h_downtime_and_reopen`, `test_failed_attempts_widen_the_next_window_instead_of_skipping_it`, `test_an_unprovable_interval_fails_closed_and_keeps_coverage`, `test_a_short_window_component_is_a_coverage_gap`, `test_capture_without_durable_run_lineage_fails_closed`, `test_accepted_attempt_requires_and_advances_the_coverage_pointer`, `test_coverage_pointer_without_a_checkpoint_fails_closed_on_reopen` |
| Freshness owner policy | `test_full_reconcile_freshness_bound_is_derived_from_the_cadence` |

### Repair-round-2 regressions (re-audit BLOCK closure)

| Repair | Test |
| --- | --- |
| R6 funding digest excludes derived attribution (§6) | `test_attribution_change_is_not_a_funding_identity_conflict` |
| R7 pre-acceptance coverage floor survives a restart (§5b) | `test_coverage_floor_survives_a_restart_before_the_first_accept` |

Both fail on the pre-repair build: R6 as a
`FUNDING_EVENT_IDENTITY_CONFLICT` → `FULL_RECONCILE_EVIDENCE_WRITE_FAILED` on
the second capture of an unchanged event, R7 as a window whose lower bound is
run B's own start (the run-A interval, and the funding event inside it, gone).

### Known residual limits

- Coverage completeness rests on the endpoint's own report: the adapter records
  the *requested* cursor window and proves truncation through the documented
  page limit, the 10 000-fill retention cap and strict cursor progress. A
  silent server-side drop that returns a short, non-truncated page would not be
  detectable from the response alone.
- `funding_events.attribution` is first-seen and append-only, so an event first
  observed as `UNATTRIBUTED` keeps that column value even after its symbol
  gains owned-order lineage, and `funding_total(attributed_only=True)` keeps
  excluding it. That is the deliberate trade: the ledger never rewrites a
  durable row. Nothing in this task consumes those totals — funding does not
  reach risk before TS-P1-006 / full TS-P1-007, which is where a re-attribution
  policy (a new append-only row, never an UPDATE) belongs.
- `resolve_interrupted_reconcile_attempts()` retains its observed wall-clock
  timestamp as evidence, while readiness ordering uses append-only SQLite row
  order. A rollback can therefore never make a later interrupted attempt sort
  before an earlier accepted checkpoint.


## 12. Retained funding payload — schema v10 (P0-12, opt-in)

`funding_events` (§8) stores the identity digest of an event but not the
normalized values hashed into it. `FundingEventRecord.funding_rate`,
`position_szi` and `n_samples` are therefore observed, hashed, and then lost at
the next restart, because a SHA-256 digest cannot be inverted. Schema v10 is the
smallest additive fix: one append-only table that retains the canonical JSON of
the **existing** `FundingEventRecord.authoritative()` domain beside its ledger
row.

```sql
CREATE TABLE funding_event_payloads (
  event_id       TEXT PRIMARY KEY REFERENCES funding_events(event_id),
  payload_json   TEXT NOT NULL,   -- canonical_reconcile_json(authoritative())
  payload_digest TEXT NOT NULL,   -- repeats funding_events.payload_digest
  recorded_ts    TEXT NOT NULL
)
```

### What it guarantees

- **Opt-in only.** The default target stays v4. v10 is reached exclusively via
  `initialize(target_schema_version=10)` through the proven v4→…→v9 chain. No
  existing caller or database is upgraded by being opened, and reopening a v10
  store at a lower target never downgrades it.
- **Additive.** The migration creates one empty table in one `BEGIN IMMEDIATE`
  transaction, proves every predecessor table's row count is unchanged, and
  bumps `meta.schema_version` with a `rowcount == 1` check. A failure rolls back
  to a reopenable v9 and records a secret-safe
  `funding_payload_migration_failure` marker.
- **One transaction.** A retained payload is written in the same transaction as
  the ledger row it belongs to, so it can never become visible without its
  event, or the other way round.
- **Only newly inserted events.** An exact replay of an already-recorded event
  returns early exactly as before: one event, one payload. An event recorded
  before the upgrade stays without a payload — see below.
- **The ledger stays the authority.** The read path returns retained bytes only
  if they parse, carry exactly the authoritative domain, re-serialize to the
  same canonical bytes, and re-hash to the ledger's immutable digest. Damaged or
  edited bytes are refused (`FUNDING_PAYLOAD_DIGEST_MISMATCH`,
  `FUNDING_PAYLOAD_MALFORMED`, `FUNDING_PAYLOAD_DOMAIN_MISMATCH`), never
  returned, and a damaged store also fails closed on reopen.
- **Append-only.** `UPDATE`/`DELETE` on the table abort with
  `FUNDING_PAYLOAD_APPEND_ONLY`, mirroring the ledger's own triggers.
- **Nulls stay null.** An unreported optional value is retained as `None` and is
  never substituted with `0`.

### What it deliberately does not do

- **Historical events are explicitly unavailable.** The migration fabricates no
  payload for anything already recorded, and an ordinary replay does not
  backfill one. `get_funding_event_payload()` returns `None` for such an event —
  that `None` means *not retained*, never *zero* and never *reconstructed*.
  Recovering those values would require a fresh authoritative capture, which is
  outside this capability.
- **Normalized, not raw.** What is retained is the payload the Bridge already
  computed from the `userFunding` record, not the original HTTP bytes and not
  the original decimal strings. This capability therefore proves nothing about
  venue authenticity, history completeness, settlement-oracle association, or
  the sign/meaning of a funding rate. It removes one storage obstacle; it
  decides no venue fact.
- **No new identity and no new interpretation.** The exchange-provided `hash`
  remains the sole event identity, the digest domain is unchanged, and no
  risk/order/KILL behavior is touched. Funding still does not reach risk here.

### Surfaces

- `Store.funding_payload_retention_enabled()` — true only on v10.
- `Store.get_funding_event_payload(event_id)` — the verified payload, `None`
  when explicitly unavailable, `FUNDING_PAYLOAD_EVENT_UNKNOWN` when the ledger
  has no such event, and `FUNDING_PAYLOAD_SCHEMA_INACTIVE` below v10.

Test evidence: `tests/test_funding_payload_retention.py` (offline, synthetic),
plus the v10 capability/migration extension in `tests/test_store.py` and the
end-to-end restart/conflict cases in `tests/test_reconciliation.py`.

## 13. Offline synthetic funding materialization (P0-12 D1, synthetic-only)

`tools/export_mtc_funding.py` is an **offline** CLI plus one pure function that
stages a *synthetic* MTC funding candidate from an owner-supplied offline
snapshot plus a separately source-verified binding packet. It is scaffolding for
a contract that is still blocked on venue evidence, not a production path.

Approved by D1 of the P0-12 decision packet. D1 grants bounded synthetic
implementation only. It approves no source-event digest domain, no real venue
capture, no Bridge schema10 activation, no account contact and no promotion of
an economic record.

### Surfaces

    build_funding_candidate(retained_rows, approved_event_bindings, coverage,
                            schedule_id, start_inclusive, end_exclusive)
        -> CandidateResult

    export_mtc_funding.py --snapshot OFFLINE_SCHEMA10_COPY \
        --bindings VERIFIED_LOCAL_PACKET --symbol BTC --start UTC --end UTC \
        --schedule-id ID --staging NEW_NONEXISTENT_DIRECTORY

`CandidateResult` carries either candidate bytes plus their SHA-256 and a
non-admission report, or a refusal report and no record bytes.

### Snapshot boundary: read-only, quiescent, never initialized

- The snapshot is named by the operator. The tool never captures, copies or
  discovers a live database.
- A snapshot with a `-wal`, `-shm` or `-journal` companion is refused
  (`CANDIDATE_SNAPSHOT_NOT_QUIESCENT`). Its bytes are hashed before and after
  the read; any change refuses with `CANDIDATE_SNAPSHOT_DRIFTED`.
- It is opened `mode=ro&immutable=1`. `Store.__init__` and `Store.conn` are
  bypassed deliberately, because that property creates the file and issues
  `PRAGMA journal_mode=WAL` and `PRAGMA foreign_keys=ON`, which are writes.
  `_ReadOnlySnapshot` instead binds the *actual* Store retrieval methods to the
  read-only connection, so `get_funding_event_payload()` keeps its verification
  and its reason codes rather than having them re-implemented.
- `initialize()`, migration, checkpoint and backfill are never called. A v4
  snapshot refuses with the Store's own `FUNDING_PAYLOAD_SCHEMA_INACTIVE` and
  is left byte-identical and still at v4.

### Completion evidence: a coverage flag is not evidence

`coverage` is a closed witness: `evidence_kind`, `complete`,
`interval_start_inclusive`, `interval_end_exclusive`, `symbol`,
`account_scope`, `witness_identity`, `expected_event_ids` and
`unattributed_event_ids`, plus a `source_witnesses` map from each inventoried
event ID to the lower-case hex encoding of its exact canonical synthetic event
bytes. `complete: true` alone is insufficient. The explicit
whole-interval inventory, the intended account scope and the witness identity
are all required, and the retained-row, binding, inventory and source-witness
identity sets must reconcile exactly. No row is excluded using the Bridge's
local ledger clock:

| Situation | Refusal |
| --- | --- |
| binding references an event with no retained ledger row | `CANDIDATE_BINDING_UNKNOWN_EVENT` |
| any retained row is absent from the inventory | `CANDIDATE_INVENTORY_MISMATCH` |
| inventoried event carries no binding | `CANDIDATE_EVENT_UNBOUND` |
| binding settles outside `[start, end)` | `CANDIDATE_BINDING_OUT_OF_INTERVAL` |
| non-`ATTRIBUTED` event not acknowledged by the witness | `CANDIDATE_ATTRIBUTION_SCOPE_MISMATCH` |

`UNATTRIBUTED` is not treated as unauthentic: its status is retained verbatim
and it is admitted only under an explicit acknowledgement in the witness.
Every supplied retained row must be inventoried and bound; there is no silent
out-of-scope bucket. An empty interval can succeed only when all four supplied
identity sets are exactly empty.

### Binding contract

Each binding carries exactly the eight current MTC input fields, keyed by the
existing `event_id`: `event_timestamp`, `funding_event_id`, `raw_rate`,
`positive_rate_payer`, `oracle_price`, `oracle_price_source`, `provenance`,
`source_event_digest`. Keys and types are closed; identities and provenance must
be non-empty; referenced byte digests must be lower-case SHA-256;
`oracle_price` must be positive; `positive_rate_payer` must be the approved
`LONG` convention; timestamps must be aware.

For this synthetic-only schema, each `coverage.source_witnesses` value must be
the exact canonical UTF-8 JSON bytes for the binding's six explicit event
fields (the eight-field binding excluding `provenance` and
`source_event_digest`). The exporter decodes those bytes, requires their closed
field set and exact values to describe that binding, and recomputes both
`provenance.source_sha256` and `source_event_digest` over the bytes. Missing,
tampered, swapped, non-canonical or detached witnesses refuse. This auxiliary
map does not define a production source-byte domain.

The retained payload is re-proved *independently* by the pure function against
the same checks and codes as `Store._decode_funding_payload`
(`FUNDING_PAYLOAD_DOMAIN_MISMATCH`, `FUNDING_PAYLOAD_DIGEST_MISMATCH`,
`FUNDING_PAYLOAD_IDENTITY_MISMATCH`), so a caller cannot launder a tampered
payload past the exporter by pre-approving it. An unavailable payload stays
unavailable (`CANDIDATE_PAYLOAD_UNAVAILABLE`) and is never zeroed,
reconstructed or omitted.

### Precision and evidence separation

- Timestamps are parsed exactly, with arbitrary subsecond digits preserved and
  `+00:00` respelled `Z` without moving the instant. Ordering is by whole
  seconds and an exact decimal fraction, then by UTF-8 event-id bytes, so `.1`
  and `.10` are one instant and never order lexicographically.
- Binding numerics must be exact decimal literals. A binary `float` is refused
  (`CANDIDATE_PRECISION_UNREPRESENTABLE`) rather than re-rounded: this tool has
  no authority to choose a billing or rounding rule.
- `payload_digest` stays the normalized Bridge integrity digest. It is never
  renamed to `source_event_digest`, and a binding that reuses it refuses with
  `CANDIDATE_DIGEST_DOMAIN_CONFLATION`. `SYNTHETIC_SOURCE_EVENT_DIGEST_V1` is a
  synthetic schema only; it is not a production digest domain.
- A retained payload's `effective_ts` and `funding_rate` are Bridge
  observations carried as labelled evidence beside, never merged into, the
  explicit synthetic binding. `binding_notes` records whether the two agree; it
  never equates them. The exporter generates no lifecycle, position, sequence,
  cashflow or cumulative field; MTC computes its own 18-field result.

### Staged output

Three deterministic artifacts under a new, non-existing external directory:
`funding_candidate_synthetic.json` (UTF-8, sorted keys, compact separators, no
NaN/Infinity, final LF), its detached `.sha256` sidecar (lower-case hex plus
LF), and `materialization_report.json`. No clock value reaches any artifact, so
identical input bytes produce identical output bytes. The target must be
outside the Bridge repository, must not overlap the snapshot or binding packet,
and must have no symlink/reparse-point ancestry. Any existing target, including
an empty directory, is refused (`CANDIDATE_STAGING_NOT_EMPTY`). Artifacts are
written into a private sibling scratch directory and the whole directory is
published atomically without clobbering a raced target. A refusal publishes the
report only, never a candidate or sidecar. A write, close or publication failure
publishes nothing; cleanup failures report the exact residual unpublished
scratch path and entries instead of claiming they were removed.

### Non-admission is physical

A successful candidate is labelled `SYNTHETIC_ONLY` and its root carries no
`schedule_id`, no `events` and no `settlement_currency`. Current MTC record
selection therefore cannot consume it: `EconomicRecords.funding_schedule_id`
raises and `ExecutionEconomics._resolve_funding` refuses with its own
`REFUSED_MISSING_FUNDING_EVENT`. This is a structural shape, not a fake signed
receipt and not a promotion gate.

Production mode is unavailable and stays
`UNAVAILABLE_PENDING_SOURCE_EVENT_DIGEST_DOMAIN`. The only accepted
completion-evidence kind is `SYNTHETIC_FIXTURE`. There is no mode switch,
boolean approval flag, permissive callback or magic literal that unlocks
production; the missing binding-packet schema and `source_event_digest` byte
domain must be approved and implemented before any production path exists.

### What it deliberately does not do

Every caller fact in a synthetic run is a fixture. A successful candidate
proves nothing about real-world interval completeness, a real account, a real
payment, authoritative settlement time or rate, or venue authenticity. It is
not an accepted economic record, and no oracle is associated from nearby
context or reverse-calculated from a payment amount.

Test evidence: `tests/test_mtc_funding_export.py` (offline, synthetic), which
asserts exact candidate bytes and order, actual snapshot/sidecar state after
each run, the caller-visible command line, and the current production loader's
inability to admit the candidate.
