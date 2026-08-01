# TS-P1-009 Kill-Switch Evidence and Recovery

Status: implemented as an opt-in schema-v9 capability. Source schema is v8. The runtime default
remains v4. This change does not activate v9, migrate a runtime database, start the bridge, or call
an exchange.

## Safety objective

A KILL request stops new risk in memory before persistence or broker I/O. On v9 it then persists
one durable episode and its active pointer before any mutation. It cancels only exact
lineage-owned risk-increasing orders and may flatten only the exact lot-normalized owned net
quantity proved by durable fills plus a fresh exact symbol snapshot.

Foreign, mixed, opposite, excess, malformed, stale, or unknown evidence never authorizes
mutation. Transport success is evidence of a response, not proof that an order is terminal.
UNKNOWN, crash, deadline, partial application, active submission quarantine, or active partial
recovery leaves the bridge KILLED.

## Ordering and concurrency

The engine performs the following sequence:

1. Set `_kill_requested` and `OrderManager.kill_latched` in memory.
2. In one SQLite transaction, set `meta.app_state=KILLED`, insert or resolve the immutable
   `kill_requests` row, and set `meta.kill_request_active`.
3. Acquire the accepted full-reconcile writer guard, then the per-symbol writer lock. If the
   caller already owns the full writer, it is reused rather than reacquired.
4. Capture and validate an exact symbol snapshot and durable local lineage.
5. Reserve each deterministic action and its five-second deadline before broker I/O.
6. Append broker and direct-query evidence transactionally; no SQLite transaction spans network
   I/O.
7. After a direct safe terminal observation, release mutation locks and run a fresh full
   reconciliation. A current accepted checkpoint is bound to the episode for ACK authority.

The same in-memory latch is checked at the final submission boundary. A database write failure
therefore cannot permit a waiting ARMED decision to submit.

## Episode and action identity

Episode identity is:

```text
kill-v1:sha256(canonical_json(
  version, run_id, symbol, generation, flatten_requested, policy_version
))
```

The active pointer makes an identical HTTP duplicate or restart resolve the same episode.
An incompatible mode, run, symbol, or policy conflicts rather than creating a second episode.

Action identity is:

```text
killa-v1:sha256(canonical_json(
  version, episode_id, kind, target, qty_lots
))
```

Cancel uses the exact owned target cloid as its action cloid. Flatten derives one Hyperliquid
cloid as `0x + blake2s-128(version + action_id)`. A partial or UNKNOWN flatten always queries that
same identity and never mints a close for the residual quantity.

## Cancellation and protection law

All proven-owned ENTRY orders are cancelled before optional flatten evaluation. A cancel is
complete only after direct order query proves the cloid terminal or absent. Foreign and unknown
orders are preserved.

When `flatten=false`, a nonzero owned position is safe only when exactly one live, opposite-side,
reduce-only, exact-lot owned stop remains. Protection is not cancelled.

When `flatten=true`, the coordinator:

1. proves exchange net lots equal durable owned net lots and a single owned trade lineage;
2. submits one exact-size reduce-only close with the deterministic flatten cloid;
3. directly queries the same cloid and verifies terminal status, exchange oid, and exact fill
   size;
4. captures an exact flat symbol snapshot; and only then
5. cancels residual owned reduce-only protection by exact cloid and directly verifies it.

If the query proves only a partial fill, the applied quantity is retained as evidence and the
episode remains KILLED with `FLATTEN_PARTIAL`. No second full-size close is allowed.

## UNKNOWN and deadline law

Cancel verification and flatten verification each receive a separate, non-resetting five-second
budget. Reservation stores UTC `reserved_ts` and `deadline_ts`; runtime waiting also uses a
process-local monotonic deadline.

- A newly reserved action may send once.
- A crash after reservation resumes with direct query only.
- UNKNOWN or no response permits direct same-identity queries only.
- A resend is allowed only on a later replay after a direct query has durably folded the action
  to `NOT_APPLIED`.
- A timeout or transport ACK proves neither applied nor not applied.
- Restart reconstructs remaining time from the original UTC deadline; it never writes a new
  deadline.

## Schema v9

Migration adds exactly three business-evidence tables and one meta pointer:

- `kill_requests`: immutable episode identity and requested mode; mutable folded terminal and ACK
  state; optional safe-checkpoint binding.
- `kill_actions`: immutable cancel/flatten identity, exact target/quantity/cloid and fixed
  reservation/deadline; mutable folded outcome.
- `kill_action_events`: append-only ordered reservation, send, broker, query, outcome, reason-code
  and digest evidence.
- `meta.kill_request_active`: the sole unresolved or unacknowledged episode pointer.

Identity columns cannot be updated, evidence events cannot be updated or deleted, and request or
action rows cannot be deleted. Reopen revalidates canonical SQL topology, integrity, foreign
keys, pointer cardinality, deterministic identities, cloid aliases, deadline bounds, event
sequence/digests, folded outcomes, and safe-checkpoint links.

The v8→v9 migration performs canonical v8 validation, evidence census, collision and pointer
preflight, then runs DDL and the schema-version update under `BEGIN IMMEDIATE`. No broker I/O
occurs. Any failure rolls back to a reopenable v8 and records only a secret-safe failure type
after rollback. A legacy KILLED v8 is retained as KILLED without inventing an episode and requires
owner-directed recovery. Target schema 10 is unsupported and never downgraded.

## Restart and acknowledgment

Reopen resolves `meta.kill_request_active`. Any active episode dominates quarantine, partial
recovery, and risk-control presentation: startup remains KILLED. Reserved and UNKNOWN actions
resume by same-identity query; restart never acknowledges, disarms, or arms them.

`POST /api/kill` remains a loopback emergency route and does not require `X-Confirm`.
`POST /api/kill/ack` requires:

- current `X-Confirm: <state_version>`;
- terminal state `SAFE_FLAT` or `SAFE_RETAINED`;
- a complete proof digest and checkpoint binding;
- the same current pointed accepted reconciliation checkpoint; and
- checkpoint freshness under the existing `max(3 × reconcile cadence, 30 seconds)` bound.

ACK atomically marks the request acknowledged, clears `meta.kill_request_active`, appends the ACK
event, and writes `meta.app_state=DISARMED`. ACK never proves cancel/flatten completion and never
transitions to ARMED. A later ARM remains a separate explicit action.

## Evidence retention and rollback

Never delete or rewrite kill requests, actions, action events, UNKNOWN outcomes, orders, fills,
reconcile evidence, partial-recovery evidence, risk checkpoints/latches, decisions, events, or
migration-failure evidence.

Predecessor code cannot safely reopen schema v9. Safe code rollback is not a schema-meta edit.
It requires:

1. KILLED or DISARMED state;
2. export and retention of all v9 kill evidence;
3. a separately verified v8 backup from before migration;
4. restoration of that verified v8 database; and
5. independent confirmation that no unresolved v9 action has been reinterpreted as absent.

Changing `meta.schema_version` from 9 to 8 is forbidden: predecessor topology checks cannot
understand the retained v9 evidence, and an unresolved action would be lost from authority.
