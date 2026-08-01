# TS-P1-009B Kill Evidence Epoch Contract

Status: implemented for the opt-in schema-v9 KILL capability, including S2 lifecycle-close
integrity/fencing and minimum-S3 lifecycle liveness. The default schema target remains v4. This
contract does not activate v9, migrate a runtime database, start the bridge, or authorize broker
activity.

This document extends `30_TSP1009_KILL_EVIDENCE_RECOVERY.md`. That document remains authoritative
for owned-only action identity, deadlines, direct-query proof, retention, and ACK freshness.

## Objective and scope

The epoch and lifecycle fence close three failure classes:

1. a same-net exchange position could contain foreign replacement fills while appearing equal to
   the locally derived owned net; and
2. an older recovery process could publish state or proof after a newer recovery had invalidated
   its observation; and
3. a KILL flatten could appear complete without one exact, epoch-owned trade lifecycle close.

Further S3 work and TS-P1-010 are outside this change.

## Epoch identity and durable anchors

One recovery attempt is identified by:

```text
epoch = (episode_id, attempt_no, process_uid, opened_ts_monotonic)
```

- `episode_id` remains the deterministic TS-P1-009 episode identity.
- `attempt_no` increments durably whenever the same pending episode is replayed.
- `process_uid` identifies the process that opened the attempt.
- `opened_ts_monotonic` is evidence about that process-local open; it never reconstructs an action
  deadline after restart.

The canonical epoch token is compact, sorted JSON containing those four fields plus
`state = OPEN | CLOSED`. `kill_attempts` appends one row per attempt and retains that attempt's
terminal state, checkpoint, and proof. The current-attempt projection and two CAS anchors are:

- `kill_requests.epoch_token`;
- `meta.kill_epoch_active`.

Both must contain the same canonical token. `meta.kill_request_active` continues to identify the
unacknowledged episode.

## Mandatory ordering

```text
LATCH -> OPEN -> CAPTURE -> PROVE -> MUTATE -> RECONCILE -> BIND -> CLOSE
```

1. **LATCH** — set in-memory KILLED and `OrderManager.kill_latched` before persistence or broker
   I/O.
2. **OPEN** — under `BEGIN IMMEDIATE`, create attempt 1 or append `attempt_no + 1` and move the
   active projection/token. A replay invalidates old authority but never rewrites the prior
   attempt's terminal/checkpoint/proof history; the same episode and actions are retained.
3. **CAPTURE** — under the full-writer guard and then the symbol lock, collect typed authoritative
   positions, open orders, and fill history bound to the open epoch.
4. **PROVE** — intersect the capture with durable local lineage. Absence of contradiction is not
   positive ownership proof.
5. **MUTATE** — cancel only exact owned risk orders or send the one deterministic exact-lot
   reduce-only flatten. The KILL-only broker contract carries the epoch and guard into the adapter;
   Hyperliquid revalidates in the same worker-thread function immediately before the SDK write.
6. **RECONCILE** — after a direct safe symbol proof, run the existing full reconciliation. The
   additive KILL capture seam does not create or alter a reconciliation checkpoint.
7. **BIND** — bind the current accepted checkpoint and terminal proof only through epoch CAS.
8. **CLOSE** — CAS the same token from `OPEN` to `CLOSED`. Only a closed, proof-bound epoch can
   become ACK-eligible.

No SQLite transaction spans broker I/O.

## Invariants

| ID | Contract |
|---|---|
| EP-1 | Repository code checks an open epoch owned by the current process at the last local broker-mutation guard. Hyperliquid exposes no venue-side fencing token, so a residual supersede check/use window remains between that guard and venue receipt; this contract reduces but cannot eliminate that race. |
| EP-2 | Ownership proof and mutation use the same epoch. Epoch *n* cannot authorize epoch *n+1*. |
| EP-3 | Every durable request-state mark, action write, proof bind, and close is CAS-guarded by the active epoch. |
| EP-4 | A stale epoch write is rejected and a secret-safe `KILL_EPOCH_STALE_WRITE_REJECTED` event is appended; an append failure is observable and fail-closed. |
| EP-5 | OPEN failure leaves the in-memory KILL latch set, performs no broker mutation, and fabricates no completion. |
| EP-6 | Every fully applied / ACK-eligible KILL flatten has exactly one close decision and one matching `trades` closure; both must exactly match the durable fill-derived lifecycle evidence. |
| EP-7 | Historical request/attempt/action/event evidence is retained; replay appends an attempt and moves only active authority without rewriting prior attempt history, action identity, or deadlines. |
| EP-8 | ACK requires the active epoch to be `CLOSED` with a fresh current accepted checkpoint and proof bound in that epoch. |

## Authoritative capture and positive ownership

`KillEvidenceCapture` contains the typed epoch, symbol, positions component, open-orders
component, and fills component. Each component must be complete, exact, and carry an observation
time. The Hyperliquid and mock adapters return the same canonical evidence shapes used by full
reconciliation.

The engine refuses mutation when capture is absent, belongs to another epoch/symbol, or is not
accepted:

- unavailable, truncated, or stale capture is `UNKNOWN` and query-only;
- malformed or conflicting capture is `AMBIGUOUS` and permits no mutation.

Every mutation phase calls the idempotent capture seam again and passes a mandatory (never
optional) accepted capture into the model. Before the initial owned-risk cancellation phase, the
flatten decision, and the post-flatten residual-protection cancellation phase, the model requires:

- exact agreement between the captured position and the direct symbol snapshot;
- exact agreement between captured and direct open-order identity, side, size, and reduce-only
  status;
- exact equality of captured `(fill identity, oid)` pairs and lot totals with durable owned fill
  lineage;
- zero duplicate or malformed identities;
- exact observed net lots equal to durable owned net lots; and
- exactly one contributing owned trade when the owned net is nonzero.

Therefore an external sell that closes the owned long followed by an external buy that recreates
the same signed net is not ownership. The extra captured fill identities cannot equal the durable
owned set, so the episode becomes `OWNERSHIP_AMBIGUOUS` before an owned pending order, protection
order, or position is mutated.

The capture lower bound covers durable run/fill lineage. Its read-only upper bound is the
clock-independent year-9999 millisecond ceiling, so the venue cannot server-filter a legitimate
exchange-stamped fill merely because the local clock is behind. This does not alter action
reservation, wall deadlines, process-local monotonic deadlines, or resend authority. If a valid
capture interval still cannot be proved, mutation remains forbidden. The mock mirrors the venue's
server-side window filtering so tests cannot rely on rows the real adapter would not return.

## CAS-protected write surface

The active open token is checked in the same transaction as each durable write:

- request terminal-state marking;
- action reservation/replay;
- action-event append and folded outcome;
- durable action-clock observation;
- the atomic trade-lifecycle close and `TRADE_CLOSED` decision append;
- terminal checkpoint/proof binding; and
- epoch close.

The check requires `meta.kill_epoch_active`, the request projection, and the appended attempt row
to match the caller's exact open token. Store-local possession must also match the epoch returned
by that Store's own `open_kill_epoch`; reading the current token never grants ownership. All
epoch-fenced write helpers require the `epoch` keyword. A newer OPEN changes active authority, so
an older process can neither adopt the token, publish a stale safe proof, close it, nor continue
state/action writes. Rejection is rolled back, recorded outside the failed transaction, and raised.
Failure to record that rejection is itself raised as `KILL_STALE_EVIDENCE_RECORD_FAILED`.

This closes the second finding-6 route: guarding only `bind_kill_terminal_proof` would still allow
an older process to mark terminal state, reserve an action, or append outcome evidence after a
newer attempt began. Those writes now share the same CAS boundary as proof binding and close.

## Kill-flatten lifecycle exactness and drain deferral

An applied KILL flatten is ACK-eligible only when the durable close decision payload **and** the
matching `trades` row exactly equal the lifecycle recomputed from immutable fills. Numeric payload
types, keys, timestamps, exit price, reason, gross PnL, costs, net PnL, entry basis, exit VWAP, and
quantity are exact comparisons; a representable numeric change is a conflict rather than an
accepted approximation.

The `exit_qty` versus `entry_qty` comparison deliberately retains an absolute `1e-12` tolerance.
That comparison establishes aggregate *completeness* before closure evidence is derived; it does
not validate persisted decision or trade-row integrity. Once derived, the persisted decision
payload and `trades` closure must match exactly as described above.

The lifecycle close runs under `BEGIN IMMEDIATE`. In that same transaction it validates the
caller-owned open epoch and binds the exact `epoch_token` again in the fenced `UPDATE trades`
predicate before appending the close decision. A stale non-`None` epoch rolls the transaction
back, records `KILL_EPOCH_STALE_WRITE_REJECTED`, and raises `KILL_EPOCH_STALE_WRITE`; no lifecycle
close or decision can commit.

A new manager starts with no retained kill epoch. A running manager deliberately retains its last
epoch as historical callback context, but retention is not authority: the store rejects a stale
retained epoch with `KILL_EPOCH_STALE_WRITE`. When a startup or periodic reconcile drain encounters
a complete durable KILL flatten with no epoch, or catches that exact store conflict for a stale
epoch, it leaves the event queued rather than unwinding startup. A later `/api/kill` recovery opens
and owns an epoch and may retry the same durable event. The store still rejects every direct
KILL-flatten lifecycle-close request that omits an epoch with `KILL_EPOCH_REQUIRED`; drain
containment does not weaken the write rule.

The first deferral appends `KILL_EPOCH_LIFECYCLE_DEFERRED`. Its detail contains only SHA-256
digests of episode/fill identity, the numeric trade ID, and a bounded reason code. The store checks
that binding against the durable request/order/fill join and performs the lookup-plus-append under
`BEGIN IMMEDIATE`. Repeated drains across Store instances therefore retain one row for the same
episode/trade/fill/reason. Failure to append the evidence is raised and remains fail-closed.

Both the global reconcile drain and the same-symbol locked drain use an exhaustive containment
allowlist: only `KILL_EPOCH_REQUIRED` and `KILL_EPOCH_STALE_WRITE` from a durably bound
KILL-flatten fill may be deferred. Every other `KillConflictError`, including evidence-append and
unexpected schema-store failures, propagates fail-closed. Other exception classes and a listed
conflict that cannot be identified as a KILL lifecycle also propagate. Direct store callers still
receive the conflict after the rejected lifecycle transaction rolls back and EP-4 evidence is
appended. Once a drain has deferred an unchanged fill under the same absent or stale epoch context,
later cycles retain it without repeating the rejected store call; a newly opened epoch or a durable
trade closure changes that context and permits the retry.

A schema-admitted `KILL_FLATTEN` order is quarantined as
`KILL_LIFECYCLE_IDENTITY_MISSING` when its group, integer trade identity, durable trade row, or
durably bound `kill_requests.episode_id` is missing. The same containment applies when the healthy
store is on an inactive pre-v9 kill schema: that is an admitted capability mismatch, not an
evidence-store outage. The fill is consumed, its queue and deferred-cache entries are cleared, the
durable application state remains `KILLED`, and startup returns normally with the fault visible in
status and events. A second-Store invalidation between validation and the `BEGIN IMMEDIATE` binding
check is classified and quarantined the same way. Evidence-store write failures, including
`KILL_STALE_EVIDENCE_RECORD_FAILED` and a failed quarantine/deferral append, still propagate.

The status payload exposes `kill_episode.lifecycle_state = AWAITING_EPOCH_RECOVERY` while the
active episode still needs recovery, `AWAITING_ACK` once it is safe and ACK-eligible, and
`deferred_event_queue_depth` for the current in-memory queue. This is a minimal liveness surface,
not the deferred TS-P5-001 operations read-model redesign.

Queue growth uses option (a): an exact redelivery with the same `fill_id` and identical canonical
fill fields replaces its queued copy. A different payload reusing the same `fill_id` is not
coalesced, so the existing immutable-fill conflict/quarantine path remains observable and no
distinct broker evidence is silently dropped. Distinct fill identities remain unbounded; bounding
them with a durable overflow latch is outside this minimum option-(a) disposition.

## Replay, restart, and the same-identity retry law

Opening a newer attempt appends an immutable `kill_attempts` row and moves the request/meta active
projection. Prior terminal state and proof remain readable and become trigger-protected from
updates. Replay does not mint a new episode, action identity, cloid, reservation time, or deadline.

- Existing `UNKNOWN` or `RESERVED` action: query the same identity only.
- Existing direct-query `NOT_APPLIED`: at most one later same-identity resend while the original
  process-local monotonic budget remains.
- Restarted process: no monotonic continuity is reconstructed, so it is query-only.
- Wall-clock rollback before an action's prior observation: remaining write budget is zero.
- Partial or unknown flatten: never mint a residual/full-size replacement close.

All replay queries and any permitted resend run under the newly opened epoch. Evidence from the
prior attempt cannot itself authorize the mutation; only the immutable action identity plus the
durably folded direct-query result can do so.

## Proof close and ACK

`BIND` requires the epoch still open, the episode still active, and the checkpoint still the
current accepted pointer. `CLOSE` requires a safe terminal state, checkpoint identity and
timestamp, and proof digest; it atomically CAS-updates both epoch anchors from the exact open token
to its closed form.

ACK rejects an open, stale, mismatched, unproved, or expired epoch. A successful ACK consumes the
active closed proof, marks the request acknowledged, clears the episode and epoch pointers, and
transitions only to DISARMED. It never arms.

## Migration and predecessor behavior

Schema v9 defines four unshipped KILL tables, including append-only `kill_attempts`, and uses
`meta.kill_epoch_active` as its CAS anchor. Migration remains v8 to v9 under `BEGIN IMMEDIATE` and
validates canonical topology, active attempt/projection/token agreement, retained attempt proofs,
and episode identity before commit.

Any DDL, topology, token, pointer, or meta failure rolls back to a reopenable v8. The
secret-safe migration-failure marker records only the exception type after rollback. Ordinary
v4-v8 initialize/reopen does not create epoch state or activate v9. A legacy KILLED predecessor
remains KILLED without an invented episode.

## Failure classification

| Failure | Durable/runtime result | Broker authority |
|---|---|---|
| OPEN or epoch CAS failure | KILLED; exception/reason retained | none |
| Capture unavailable/truncated/stale | `UNKNOWN` | query-only |
| Capture malformed/conflicting | `AMBIGUOUS` | none |
| Positive ownership mismatch | `OWNERSHIP_AMBIGUOUS` | none |
| Direct action evidence contradictory/unknown | action `UNKNOWN` | same-identity query only |
| Stale state/action/proof/close write | rejected plus stale event | none from stale epoch |
| Safe proof without current checkpoint | proof not bound; epoch remains open | none |
| ACK before valid close/freshness | `KILL_NOT_SAFE` or epoch conflict | none |
