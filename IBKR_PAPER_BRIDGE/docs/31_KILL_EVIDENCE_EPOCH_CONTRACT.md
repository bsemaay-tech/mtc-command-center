# TS-P1-009B Kill Evidence Epoch Contract

Status: implemented for the opt-in schema-v9 KILL capability. The default schema target remains
v4. This contract does not activate v9, migrate a runtime database, start the bridge, or authorize
broker activity.

This document extends `30_TSP1009_KILL_EVIDENCE_RECOVERY.md`. That document remains authoritative
for owned-only action identity, deadlines, direct-query proof, retention, and ACK freshness.

## Objective and scope

The epoch closes two failure classes:

1. a same-net exchange position could contain foreign replacement fills while appearing equal to
   the locally derived owned net; and
2. an older recovery process could publish state or proof after a newer recovery had invalidated
   its observation.

Findings 2, 3, 4, 5, the prior NIT, S2/S3, and TS-P1-010 are outside this change.

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
`state = OPEN | CLOSED`. The two CAS anchors are:

- `kill_requests.epoch_token`; and
- `meta.kill_epoch_active`.

Both must contain the same canonical token. `meta.kill_request_active` continues to identify the
unacknowledged episode.

## Mandatory ordering

```text
LATCH -> OPEN -> CAPTURE -> PROVE -> MUTATE -> RECONCILE -> BIND -> CLOSE
```

1. **LATCH** — set in-memory KILLED and `OrderManager.kill_latched` before persistence or broker
   I/O.
2. **OPEN** — under `BEGIN IMMEDIATE`, create attempt 1 or CAS-replace the prior attempt with
   `attempt_no + 1`. A replay clears old terminal/checkpoint/proof authority but retains the same
   episode and actions.
3. **CAPTURE** — under the full-writer guard and then the symbol lock, collect typed authoritative
   positions, open orders, and fill history bound to the open epoch.
4. **PROVE** — intersect the capture with durable local lineage. Absence of contradiction is not
   positive ownership proof.
5. **MUTATE** — cancel only exact owned risk orders or send the one deterministic exact-lot
   reduce-only flatten. Assert the epoch immediately before broker mutation.
6. **RECONCILE** — after a direct safe symbol proof, run the existing full reconciliation. The
   additive KILL capture seam does not create or alter a reconciliation checkpoint.
7. **BIND** — bind the current accepted checkpoint and terminal proof only through epoch CAS.
8. **CLOSE** — CAS the same token from `OPEN` to `CLOSED`. Only a closed, proof-bound epoch can
   become ACK-eligible.

No SQLite transaction spans broker I/O.

## Invariants

| ID | Contract |
|---|---|
| EP-1 | No broker mutation occurs outside an open epoch owned by the current process. |
| EP-2 | Ownership proof and mutation use the same epoch. Epoch *n* cannot authorize epoch *n+1*. |
| EP-3 | Every durable request-state mark, action write, proof bind, and close is CAS-guarded by the active epoch. |
| EP-4 | A stale epoch write is rejected and a secret-safe `KILL_EPOCH_STALE_WRITE_REJECTED` event is appended. |
| EP-5 | OPEN failure leaves the in-memory KILL latch set, performs no broker mutation, and fabricates no completion. |
| EP-6 | Reserved for S2. S1 does not change or claim the finding-5 consistency matrix; the accepted TS-P1-004 same-identity retry law remains binding. |
| EP-7 | Historical request/action/event evidence is retained; epoch replay invalidates authority without rewriting identity or deadlines. |
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

Before any cancel or flatten, the model requires:

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

The capture lower bound covers durable run/fill lineage. Its read-only upper bound uses the later
of the injected action clock and current UTC, widened only by the accepted full-reconcile skew
tolerance. This prevents an injected action-clock rollback from suppressing capture. It does not
alter action reservation, wall deadlines, process-local monotonic deadlines, or resend authority.
If a valid capture interval still cannot be proved, mutation remains forbidden.

## CAS-protected write surface

The active open token is checked in the same transaction as each durable write:

- request terminal-state marking;
- action reservation/replay;
- action-event append and folded outcome;
- durable action-clock observation;
- terminal checkpoint/proof binding; and
- epoch close.

The check requires both `meta.kill_epoch_active` and the request row to match the caller's exact
open token. A newer OPEN changes both anchors. An older process can then neither publish a stale
safe proof nor continue state/action writes. Rejection is rolled back, recorded as stale evidence
outside the failed transaction, and raised to the caller.

This closes the second finding-6 route: guarding only `bind_kill_terminal_proof` would still allow
an older process to mark terminal state, reserve an action, or append outcome evidence after a
newer attempt began. Those writes now share the same CAS boundary as proof binding and close.

## Replay, restart, and the same-identity retry law

Opening a newer attempt invalidates prior safe proof authority; it does not mint a new episode,
action identity, cloid, reservation time, or deadline.

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

Schema v9 adds the epoch token column to the unshipped KILL request topology and uses
`meta.kill_epoch_active` as its CAS anchor. Migration remains v8 to v9 under `BEGIN IMMEDIATE` and
validates canonical topology, token/pointer agreement, and episode identity before commit.

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
