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
| intent_id | TEXT | PRIMARY KEY |
| intent_preimage | TEXT | NOT NULL |
| intent_version | TEXT | NOT NULL DEFAULT 'ts-p1-002-intent-v1' |
| request_id | TEXT | UNIQUE NOT NULL |
| request_preimage | TEXT | NOT NULL |
| request_version | TEXT | NOT NULL DEFAULT 'ts-p1-002-request-v1' |
| cloid_seed | TEXT | NOT NULL |
| origin_run_id | TEXT | NOT NULL |
| origin_decision_uid | TEXT | NOT NULL |
| state | TEXT | NOT NULL CHECK (RESERVED, SUBMITTED, LEGACY_RESERVED, LEGACY_SUBMITTED) |
| reserved_ts | TEXT | NOT NULL |
| submitted_ts | TEXT | |

### v2→v3 Migration

- Runs inside a single `BEGIN IMMEDIATE` transaction
- DDL, backfill, and schema-version update are all-or-nothing
- On error: rollback leaves schema_version=2, all legacy data unchanged, no
  order_identity table/index residue
- Backfill: joins exact `run_id`/`decision_uid` to exactly one SIGNAL and one
  RISK_PASS row; zero or duplicates fail closed
- SIGNAL and order_plan semantics must agree (symbol, direction)
- LEGACY_SUBMITTED only from consistent order + trade mapping for exact
  run/decision; orphan, cross-run, duplicate, or incompatible legacy mappings
  fail closed
- Multiple rows resolving to same intent/request: all preimages must be exactly
  equal; otherwise fail

## Reservation Protocol

1. Compute both preimages and IDs
2. `BEGIN IMMEDIATE`
3. If no identity exists: insert `RESERVED`, commit
4. If exact intent+request exist: return `BLOCKED` (no broker I/O)
5. If same intent with different request: `IdentityCollisionError`, audit event
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
- Same cloid, same immutable identity: update mutable fields only (status,
  filled_qty, avg_fill_px, ts_last, order_json)
- Same cloid, different identity (oid, group_id, order_ref, decision_uid,
  trade_id, role, qty): preserve original row, raise `OrderCollisionError`
- Public `insert_order`: rollback pending statement before raising; must not
  commit unrelated pending work

## plan.decision_uid Management

- `request_id` is the broker cloid seed
- Before broker call: `plan.decision_uid = request_id`
- After broker call (finally): `plan.decision_uid = original_decision_uid`
- Original run-scoped `decision_uid` persists in all decision/trade/order lineage

## Rollback/Export

- Never drop or clear the v3 identity table
- `get_snapshot()` includes `identities` key
- No destructive downgrade command
