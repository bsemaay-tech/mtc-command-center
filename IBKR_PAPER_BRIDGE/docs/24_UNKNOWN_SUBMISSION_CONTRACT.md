# TS-P1-003 Unknown-Submission Quarantine Contract

**Status:** Implemented  
**Parent:** `fbd63474c5df10fa801c989cf7596ca9a3cf7a75`  
**Schema:** v4 (adds `submission_attempts`, `submission_recovery_evidence`)

## 1. Purpose

When a bracket-submission call may have reached the exchange but the bridge
cannot prove the outcome, persist a durable `UNKNOWN_SUBMISSION` quarantine
before any later signal can resubmit that request. Recovery must survive
process restart and may resolve only from complete, request-specific broker
evidence.

This prevents duplicate exposure after:
- Timeout or connection reset after the request was sent
- Malformed post-send response
- Delayed exchange visibility
- Process crash between exchange acceptance and local finalization
- Local finalization failure after broker success

## 2. States and Transitions

```
                     ┌──────────────────┐
                     │    SUBMITTING     │  ← persisted before broker I/O
                     └───────┬──────────┘
                             │
          ┌──────────────────┼──────────────────┐
          ▼                  ▼                  ▼
┌─────────────────┐ ┌────────────────┐ ┌──────────────────┐
│VERIFIED_SUCCESS │ │DEFINITIVE_     │ │UNKNOWN_SUBMISSION│
│   (terminal)    │ │REJECTION       │ │   (quarantined)  │
└─────────────────┘ │(terminal)      │ └────────┬─────────┘
                    └────────────────┘          │
                                   ┌────────────┼────────────┐
                                   ▼            ▼            ▼
                          ┌──────────────┐ ┌──────────┐ ┌──────────────┐
                          │CONFIRMED_    │ │ INCOMPLETE│ │CONFIRMED_    │
                          │PRESENT       │ │ (resets   │ │ABSENT        │
                          │(terminal)    │ │  absence  │ │(terminal)    │
                          └──────────────┘ │  sequence)│ └──────────────┘
                                           └──────────┘
```

### Forward-only transition matrix

| From                | To                    | Condition                              |
|---------------------|-----------------------|----------------------------------------|
| SUBMITTING          | VERIFIED_SUCCESS      | All roles/cloids verified, trade finalized |
| SUBMITTING          | DEFINITIVE_REJECTION  | Complete response: all rejected, none accepted |
| SUBMITTING          | UNKNOWN_SUBMISSION    | Ambiguous — timeout, partial, crash, exception |
| UNKNOWN_SUBMISSION  | CONFIRMED_PRESENT     | Any planned cloid found authoritatively |
| UNKNOWN_SUBMISSION  | CONFIRMED_ABSENT      | 3 complete cycles spanning ≥120s, all absent |
| UNKNOWN_SUBMISSION  | UNKNOWN_SUBMISSION    | Recovery cycle is INCOMPLETE/CONFLICTING |

All transitions require exact pre-state check with row-count verification.
Self-transitions and backward transitions are rejected.
Callers cannot authorize arbitrary transitions by supplying crafted from-state lists.

## 3. Submission Attempt Lifecycle

### Before Broker I/O
1. Compute intent_id and request_id (TS-P1-002, unchanged)
2. Obtain planned cloids from broker's `get_planned_cloids()` method
3. In one `BEGIN IMMEDIATE` transaction:
   - Reserve identity (`RESERVED`)
   - Create submission attempt (`SUBMITTING`)
4. Commit before calling broker

### Broker Outcome Classification
The broker returns a typed `SubmissionResult`:
- `PRE_SEND_FAILURE`: Adapter proved no exchange write began
- `DEFINITIVE_REJECTION`: Complete response proves all planned orders rejected, none accepted/pending/resting/filled
- `OUTCOME_UNKNOWN`: Timeout, transport loss, malformed/incomplete response, partial acceptance, verification failure, or exception after send may have started
- `VERIFIED_SUCCESS`: Exact role/cloid coverage, success-compatible statuses

Never infer outcome from exception message substrings.

### After Broker I/O
- `PRE_SEND_FAILURE` → `DEFINITIVE_REJECTION` (safe, no exchange write)
- `DEFINITIVE_REJECTION` → terminal, identity blocked
- `OUTCOME_UNKNOWN` → `UNKNOWN_SUBMISSION`, `DISARMED`, block ARM/new entries
- `VERIFIED_SUCCESS` → atomic finalization (trade + orders + identity + attempt in one transaction)

If the `UNKNOWN_SUBMISSION` transition itself fails, `SUBMITTING` remains and is treated as quarantined on restart.

## 4. Recovery Evidence Contract

### Evidence sources (per planned cloid, per cycle)

| Source             | Required for ABSENT_CANDIDATE |
|--------------------|------------------------------|
| DIRECT_LOOKUP      | Yes — `query_order_by_cloid()` |
| OPEN_ORDERS        | Yes — `open_orders()`         |
| HISTORICAL_ORDERS  | Yes — `historical_orders()`   |
| FILLS              | Yes — `user_fills()`          |
| POSITION           | No — exposure/conflict only, never proves absence |

### Per-source verdicts

- `FOUND`: Authoritative match (open, historical, filled, pending, cancelled, rejected, expired)
- `NOT_FOUND`: Authoritative absence for this source
- `QUERY_FAILED`: API call raised or returned invalid
- `INCOMPLETE`: Response truncated or missing coverage
- `STALE`: Response window does not cover attempt window
- `TRUNCATED`: Known partial data

### Completeness

- `COMPLETE`: Source covered all planned cloids within attempt window
- `INCOMPLETE`: Source could not cover all planned cloids
- `COVERAGE_MISSING`: Source not available

### Cycle verdict

- `PRESENT`: Any source found any planned cloid → `CONFIRMED_PRESENT`
- `INCOMPLETE`/`CONFLICTING`: Any source failed or incomplete → reset absence candidate sequence
- `ABSENT_CANDIDATE`: All mandatory sources COMPLETE and all cloids NOT_FOUND

## 5. Three-Cycle / 120-Second Rule

Confirmed absence requires:
1. Three consecutive `ABSENT_CANDIDATE` cycles
2. First-to-last cycle timestamps span ≥ 120 seconds
3. All planned cloids absent from all mandatory sources in each cycle
4. Trusted local acquisition timestamps

Any `INCOMPLETE`, `CONFLICTING`, or `PRESENT` observation resets the sequence.
One empty `open_orders()` call alone never proves absence.

Query failures, unavailable APIs, truncation, stale coverage, partial bracket results,
conflicting sources, or unattributable position data stay `UNKNOWN_SUBMISSION`
and reset the absence candidate sequence.

## 6. Restart Behavior

On startup:
1. Scan `submission_attempts` for `SUBMITTING`, `UNKNOWN_SUBMISSION`, `CONFIRMED_PRESENT`
2. Run one recovery cycle
3. If active quarantine persists, DISARM the engine
4. Block ARM and all new entry submissions

Zero broker placement/cancel/flatten/re-protection calls during recovery.
Recovery runs at both startup and during recurring reconciliation while recoverable attempts exist.

## 7. Quarantine Visibility

`CONFIRMED_PRESENT` and `CONFIRMED_ABSENT` are terminal states:
- `CONFIRMED_PRESENT` remains visible in status/quarantine counts and blocks ARM
- `CONFIRMED_ABSENT` preserves all evidence; ordinary replay remains blocked by identity

No automatic resubmission, cancel, flatten, re-protection, or mutation of foreign/manual state.

## 8. Persistence

Schema v4 tables (added without rebuilding `order_identity`):

### `submission_attempts`
- `attempt_id`: auto-increment PK
- `request_id`: links to `order_identity.request_id`
- `origin_run_id`, `origin_decision_uid`: lineage
- `strategy_id`, `coin`, `direction`, `qty`: request context
- `planned_roles`, `planned_cloids_json`: exact planned role→cloid map
- `recovery_payload_json`: canonical secret-safe recovery payload
- `state`: `SUBMITTING`, `VERIFIED_SUCCESS`, `DEFINITIVE_REJECTION`, `UNKNOWN_SUBMISSION`, `CONFIRMED_PRESENT`, `CONFIRMED_ABSENT`
- `reason_code`, `created_ts`, `state_ts`, `disarmed_ts`, `final_ts`

### `submission_recovery_evidence`
- Append-only, unique per `(attempt_id, cycle_id, source, planned_cloid)`
- `verdict`: `FOUND`, `NOT_FOUND`, `QUERY_FAILED`, `INCOMPLETE`, `STALE`, `TRUNCATED`
- `completeness`: `COMPLETE`, `INCOMPLETE`, `COVERAGE_MISSING`
- `safe_payload_json`: structured IDs/statuses only — no raw exchange bodies, exception messages, credentials, keys, wallet data, or secret-looking strings

### Migration: v3 → v4
- One `BEGIN IMMEDIATE` transaction
- Creates `submission_attempts` and `submission_recovery_evidence` tables and indexes
- Bumps `schema_version` to "4"
- On failure, rolls back to clean v3 with no v4 residue
- v2 databases first run v2→v3 migration, then v3→v4

## 9. Forbidden Actions

- TS-P1-004 partial-fill protect-or-flatten
- TS-P1-005 full reconciliation snapshot/diff
- Automatic resubmission, cancel, flatten, re-protection, or mutation of foreign/manual state
- Config threshold changes, API/dashboard expansion, strategy/Pine/parity/MTC changes
- Runtime/P2RT actions, broker/exchange calls, testnet, deployment, push, merge, or PR
