# Order Identity Contract (TS-P1-002)

## Overview

TS-P1-002 implements durable order identity for the IBKR Paper Bridge. The
same canonical trading intent receives the same durable internal identity and
exchange cloid across process restart and run-id changes. Materially different
order requests cannot alias. Duplicate delivery/replay never creates a second
broker submission.

## Dual Identity Model

### Semantic `intent_id`

Canonical intent fields:
- version/domain: `ts-p1-002-intent-v1`
- stable strategy id: `keltner_trail_ema8`
- normalized uppercase symbol
- normalized uppercase direction
- timezone-aware signal timestamp, normalized to UTC with fixed microsecond
  precision and `Z` suffix

Format: `intent-v1:<sha256-hex>`

### Immutable `request_id`

Canonical request fields:
- version/domain: `ts-p1-002-request-v1`
- `intent_id`
- symbol and direction
- signal reference price
- quantity
- entry type
- limit price or null
- stop loss
- take profit or null
- leverage

Format: `request-v1:<sha256-hex>`

### Canonical Encoding

- Deterministic JSON: sorted keys, compact separators, UTF-8, `ensure_ascii=False`,
  `allow_nan=False`
- Floating values: normalized IEEE-754 hex representation (`float.hex()`)
- Negative zero normalized to positive zero
- NaN/Infinity rejected

### Digest vs Preimage

SHA-256 digests are computed but never trusted alone. Every equality check
compares exact preimages. Same digest with different preimage is a collision
that fails closed.

## Schema v3

### `order_identity` table

| Column | Type | Constraint |
|--------|------|------------|
| intent_id | TEXT | PRIMARY KEY, CHECK(length=74, prefix 'intent-v1:', 64 lowercase hex) |
| intent_preimage | TEXT | NOT NULL CHECK(!= '') |
| intent_version | TEXT | NOT NULL DEFAULT 'ts-p1-002-intent-v1' CHECK(= 'ts-p1-002-intent-v1') |
| request_id | TEXT | UNIQUE NOT NULL CHECK(length=75, prefix 'request-v1:', 64 lowercase hex) |
| request_preimage | TEXT | NOT NULL CHECK(!= '') |
| request_version | TEXT | NOT NULL DEFAULT 'ts-p1-002-request-v1' CHECK(= 'ts-p1-002-request-v1') |
| cloid_seed | TEXT | NOT NULL CHECK(!= '') |
| origin_run_id | TEXT | NOT NULL CHECK(!= '') |
| origin_decision_uid | TEXT | NOT NULL CHECK(!= '') |
| state | TEXT | NOT NULL CHECK (RESERVED, SUBMITTED, LEGACY_RESERVED, LEGACY_SUBMITTED) |
| reserved_ts | TEXT | NOT NULL CHECK(!= '') |
| submitted_ts | TEXT | |

Table-level CHECK: `(state IN ('RESERVED','LEGACY_RESERVED') AND submitted_ts IS NULL)
OR (state IN ('SUBMITTED','LEGACY_SUBMITTED') AND submitted_ts IS NOT NULL)`

### v2→v3 Migration

- Migration wrapper (`_migrate_v2_to_v3`) owns the single commit: BEGIN IMMEDIATE,
  calls in-transaction helper (`_migrate_v2_to_v3_in_tx`) that never commits,
  then commits once; rollback on all failures
- DDL, backfill, and schema-version update are all-or-nothing
- On error: rollback leaves schema_version=2, all legacy data unchanged, no
  order_identity table/index residue
- **Global coverage invariant**: Before the v3 version bump, every pre-existing
  legacy trade and order that represents broker/persistence evidence MUST be
  covered by exactly one reconstructable fingerprint origin (exact
  `run_id` + `decision_uid`).  Any trade or order that cannot be mapped to
  exactly one fingerprint origin — including zero matches and multiple/ambiguous
  origins — fails closed with `MigrationError` and full rollback.
- **Empty-database exception**: A v2 database with zero `signal_fingerprints`
  rows may upgrade ONLY when both `orders` and `trades` are also empty.  If
  either table contains legacy evidence, the migration raises `MigrationError`
  and rolls back.  A truly empty v2 database (no fingerprints, no trades, no
  orders) upgrades cleanly at schema_version=3 with zero identities.
- **Trade coverage**: Every trade must have its `(run_id, entry_decision_uid)`
  pair match exactly one `order_identity` row (`origin_run_id` +
  `origin_decision_uid`).  A trade without any matching fingerprint origin is
  ambiguous evidence and fails closed — it is not silently dropped from the
  identity ledger.
- **Order coverage**: Every order must map through its non-null `trade_id` to a
  trade whose `run_id` and `entry_decision_uid` match exactly one
  `signal_fingerprint` origin and whose `origin_decision_uid` equals the order's
  `decision_uid`.  Zero-match, multiple/ambiguous origin, NULL `trade_id`,
  missing trade, cross-run mismatch, and orphan evidence all fail closed.
- Backfill: joins exact `run_id`/`decision_uid` to exactly one SIGNAL and one
  RISK_PASS row; zero or duplicates fail closed
- SIGNAL and order_plan semantics must agree (symbol, direction, timestamp,
  reference price, stop_loss, take_profit); canonical finite comparisons with
  exact float encoding
- Timestamps compared as timezone-aware datetimes via fixed-microsecond UTC
  canonical representation; equivalent Z/+00:00/offset spellings accepted
- Reference price compared using exact deterministic finite float encoding
  (`float.hex()`), never epsilon tolerance
- RISK_PASS embedded signal stop_loss and take_profit compared canonically
  to order_plan.stop_loss/take_profit including exact None symmetry
- Non-integral leverage rejected; int-truncation never silently applied
- Every request float validated as finite before digesting
- LEGACY_SUBMITTED only from consistent order + trade mapping for exact
  run/decision: every order must have non-null trade_id and a trade with BOTH
  `run_id==fingerprint.run_id` and `entry_decision_uid==fingerprint.decision_uid`
- Orders with NULL trade_id fail closed as incompatible legacy mapping
- Multiple fingerprints resolving to same intent/request: compare retained
  origin_run_id, origin_decision_uid, cloid_seed, state, and submitted mapping;
  any incompatible legacy mapping rolls back the whole migration

## Reservation Protocol

1. Compute both preimages and IDs
2. `BEGIN IMMEDIATE`
3. If no identity exists: insert `RESERVED`, commit
4. If exact intent+request exist: return `BLOCKED` (no broker I/O)
5. If same intent with different request: `IdentityCollisionError`, audit event
   with exc.code
6. If digest collision: `IdentityCollisionError`, audit event
7. Database failure propagates; never submit without committed reservation

## Atomic Finalization

1. `BEGIN IMMEDIATE`
2. Verify intent_id exists, is RESERVED, request_id matches
3. Reject empty/invalid returned order sets
4. Insert trade
5. Insert all orders collision-safely
6. Transition exactly one row `RESERVED → SUBMITTED`
7. Check `UPDATE rowcount == 1`
8. Commit once
9. Any failure: rollback all new trade/order/state changes; prior reservation
   stays RESERVED

## Collision-Safe Order Persistence

- No `INSERT OR REPLACE` on orders
- New cloid: insert
- Same cloid, same immutable identity (oid, group_id, order_ref, decision_uid,
  trade_id, role, qty): update mutable fields only (status, filled_qty,
  avg_fill_px, ts_last, order_json)
- Same cloid, different identity: preserve original row, raise `OrderCollisionError`
- Public `insert_order`: rollback pending statement before raising; must not
  commit unrelated pending work

## plan.decision_uid Management

- `request_id` is the broker cloid seed
- Before broker call: `plan.decision_uid = request_id`
- After broker call (finally): `plan.decision_uid = original_decision_uid`
- Original run-scoped `decision_uid` persists in all decision/trade/order lineage

## broker_result Validation

- broker_result must be a non-empty mapping (`isinstance(dict)` and truthy)
- Every returned entry must be a valid order mapping with required keys:
  `cloid`, `role`, `status`, `qty`
- Non-dict entries are not silently skipped; they raise
- Failure after broker I/O leaves reservation RESERVED, creates no trade/order,
  logs only safe error code/type, and never retries

## Event Sanitization

- `PLACE_BRACKET_FAILED` events persist only structured IDs and exception
  type name (`error_type`), never `str(exc)` or raw messages
- Identity finalization failures persist only structured IDs; generic failures
  persist only the error code, no raw exception text
- Reservation collision events use `exc.code` from the caught
  `IdentityCollisionError`, never a hardcoded string

## compute_intent_identity Timezone Validation

- Rejects naive datetimes (`tzinfo is None`)
- Rejects tzinfo objects whose `utcoffset(signal_ts)` returns `None`
- Only normalizes genuinely timezone-aware inputs with concrete UTC offsets

## Rollback/Export

- Never drop or clear the v3 identity table
- `get_snapshot()` includes `identities` key
- No destructive downgrade command

## Lossless Data Integrity

- Non-integral leverage values are rejected, never int-truncated
- Every float ingested by `compute_request_identity` is validated as finite
  before digesting; NaN/Infinity raise `ValueError`
