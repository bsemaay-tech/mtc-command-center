# 23 — Order Identity Contract (TS-P1-002)

- **Status:** Implemented
- **ADR:** ADR-0023 Idempotent Order Management and Reconciliation
- **Task:** TS-P1-002 Durable Identity
- **Version:** v1.0.0

## 1. Purpose

Every canonical trading intent has the same durable internal identity and the
same exchange `cloid` across process restart and run-id change. Materially
different order requests cannot alias. Duplicate delivery or replay never
creates a second broker submission.

## 2. Dual-Identity Model

### 2.1 Semantic `intent_id`

Canonical intent fields (version `ts-p1-002-intent-v1`):

| Field        | Source                          |
|-------------|---------------------------------|
| version     | `"ts-p1-002-intent-v1"`        |
| strategy_id | `KeltnerTrailEma8.id`          |
| symbol      | `plan.signal.symbol.upper()`   |
| direction   | `plan.signal.direction.upper()`|
| signal_ts   | UTC-normalized with microsecond precision, `Z` suffix |

Excluded: reason, ref_price, qty, stops, tp, leverage, risk, run_id,
process id, wall-clock time, LLM output.

### 2.2 Immutable `request_id`

Canonical request fields (version `ts-p1-002-request-v1`):

| Field        | Source                      |
|-------------|-----------------------------|
| version     | `"ts-p1-002-request-v1"`   |
| intent_id   | Computed `intent_id`        |
| symbol      | `plan.signal.symbol.upper()`|
| direction   | `plan.signal.direction.upper()`|
| ref_price   | `plan.signal.ref_price`     |
| qty         | `plan.qty`                  |
| entry_type  | `plan.entry_type`           |
| limit_price | `plan.limit_price` or null  |
| stop_loss   | `plan.stop_loss`            |
| take_profit | `plan.take_profit` or null  |
| leverage    | `plan.leverage`             |

Excluded: risk_dollars, risk_pct.

### 2.3 Relationship

- `request_id` is the broker `cloid` seed; before broker I/O, the engine sets
  `plan.decision_uid = request_id`. The broker adapter derives stable cloids as
  `request_id:role`.
- `decision_uid` (run-scoped) is persisted separately in all decision/trade/
  order lineage and is never overwritten.
- One `intent_id` → exactly one `request_id` (enforced). A different request
  for the same intent is a collision.

## 3. Canonical Encoding

- Deterministic JSON: sorted keys, compact separators (`:`, `,`), UTF-8,
  `ensure_ascii=False`, `allow_nan=False`.
- Every float → `float.hex()` string (IEEE-754 normalized). Negative zero
  normalized to positive zero. NaN/Infinity rejected.
- SHA-256 digest with domain prefix: `intent-v1:<hex>` and
  `request-v1:<hex>`.
- Preimage match is required; digest match alone is insufficient. Same digest
  with different preimage → collision → fail closed + audit event.

## 4. Reservation and Submission Protocol

### 4.1 Pre-Broker Reservation

1. Compute `intent_preimage`, `intent_id`, `request_preimage`, `request_id`.
2. `BEGIN IMMEDIATE` transaction.
3. Look up by `intent_id`:
   - If row exists with same `request_id` AND preimages match → return/block
     (no broker I/O). Already `RESERVED` or `SUBMITTED`.
   - If row exists with same `intent_id` but different `request_id` →
     fail-closed collision error + audit event.
   - If `request_id` maps to different `intent_id` → fail-closed collision
     error + audit event.
4. Insert new row: state `RESERVED`, `reserved_ts` = now, all preimages and
   metadata.
5. Commit. Reservation is now durable.
6. Set `plan.decision_uid = request_id`.

### 4.2 Post-Broker Finalization (Atomic)

After broker returns successfully, in ONE SQLite transaction:

1. Insert trade row.
2. Insert each returned order row collision-safely.
3. Transition this reservation: `RESERVED` → `SUBMITTED`, set `submitted_ts`.

If ANY step fails → roll back the entire finalization. The already-committed
reservation remains `RESERVED`. Broker submission is treated as ambiguous.
No retry. Log fail-closed event after rollback when possible.

After successful finalization: run `sync_broker_state()`.

## 5. Collision-Safe Order Persistence

- `INSERT OR REPLACE` is removed.
- New cloid → `INSERT`.
- Same cloid with same immutable identity fields → no-op or update mutable
  status fields only.
- Same cloid with different identity → fail closed, preserve original row,
  leave reservation `RESERVED`, audit event.

## 6. Database Schema v3

### 6.1 Migration

- Fresh database → initializes at v3.
- v2 → backfills identity table and writes v3 in one transaction.
- v3 reopen → idempotent (no-op).
- Unsupported/corrupt version → fail closed.

### 6.2 v2 Backfill

For every `signal_fingerprints` row:
1. Join to SIGNAL decision payload → derive semantic intent.
2. Join to RISK_PASS decision payload → reconstruct request preimage.
3. Classify: orders with matching decision_uid → `LEGACY_SUBMITTED`;
   no orders → `LEGACY_RESERVED`.
4. Preserve legacy decision UID / cloid mapping.
5. Missing/malformed/conflicting data → rollback entire migration, raise error.

### 6.3 Rollback/Export

- Never drop or clear the v3 identity table.
- `get_snapshot()` includes `"identities"` key.
- Export preserves identity evidence alongside orders/trades/decisions/events.
- No destructive downgrade command.

## 7. Error Codes

| Code                        | Meaning                                |
|----------------------------|----------------------------------------|
| `IDENTITY_COLLISION_INTENT`| Same intent, different request         |
| `IDENTITY_COLLISION_REQUEST`| Same request_id, different intent     |
| `IDENTITY_DIGEST_COLLISION`| Same digest, different preimage        |
| `IDENTITY_ORDER_COLLISION` | Cloid reuse with different identity    |
| `IDENTITY_FINALIZE_FAILED` | Post-broker finalization rolled back   |
| `MIGRATION_V2_FAILED`      | v2→v3 backfill rolled back             |

## 8. TS-P1-003 Out of Scope

- UNKNOWN-submission recovery/retry is TS-P1-003.
- No retry-policy widening.
- No destructive downgrade.

## 9. Rollback Contract

Rollback retains the v3 identity table with all evidence. Older code (v2) is
disabled/disarmed when v3 schema is detected — it must refuse to operate
rather than silently ignore identity data.
