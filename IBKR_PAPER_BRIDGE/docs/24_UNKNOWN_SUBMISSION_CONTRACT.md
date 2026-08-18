# 24 — Unknown-Submission Quarantine Contract

**Task:** TS-P1-003  
**Date:** 2026-07-26  
**Status:** Implemented

## 1. States

| State               | Meaning                                                       |
|----------------------|---------------------------------------------------------------|
| `SUBMITTING`         | Durable attempt persisted before broker I/O; not replayable   |
| `UNKNOWN_SUBMISSION` | Broker outcome ambiguous; quarantined                          |
| `CONFIRMED_PRESENT`  | Evidence proves orders reached exchange; permanent quarantine  |
| `CONFIRMED_ABSENT`   | 3+ complete cycles spanning ≥120s confirm absence; terminal    |
| `FINALIZED`          | Normal VERIFIED_SUCCESS; attempt resolved                      |
| `REJECTED`           | PRE_SEND_FAILURE or DEFINITIVE_REJECTION; terminal             |

## 2. Transitions

```
SUBMITTING ──PRE_SEND_FAILURE──► REJECTED
SUBMITTING ──DEFINITIVE_REJECTION──► REJECTED
SUBMITTING ──OUTCOME_UNKNOWN──► UNKNOWN_SUBMISSION
SUBMITTING ──VERIFIED_SUCCESS──► FINALIZED

UNKNOWN_SUBMISSION ──recovery: PRESENT──► CONFIRMED_PRESENT
UNKNOWN_SUBMISSION ──recovery: ABSENT (3 cycles, ≥120s)──► CONFIRMED_ABSENT
UNKNOWN_SUBMISSION ──recovery: INCOMPLETE/CONFLICTING──► UNKNOWN_SUBMISSION (reset absence streak)
```

All transitions are:
- **Transactional** (exact pre-state + row-count checks)
- **Forward-only** (reject stale/backward/repeated transitions)
- **Append-only evidence** (recovery cycles never overwritten)

## 3. Evidence Completeness

Absence confirmation requires three complete, request-specific cycles:
- Direct cloid lookup (`query_order_by_cloid`)
- Open orders snapshot
- Historical orders covering the attempt window
- Fill history covering the attempt window

Each cycle must have **all** sources complete. An empty `open_orders` response alone never proves absence.

### Evidence Verdicts

| Verdict            | Trigger                                                        |
|--------------------|----------------------------------------------------------------|
| `PRESENT`          | Any planned cloid found in any source                          |
| `ABSENT_CANDIDATE` | All sources complete, zero planned cloids found               |
| `INCOMPLETE`       | Any required source failed, truncated, stale, or incomplete    |
| `CONFLICTING`      | Sources disagree, partial bracket, unattributable evidence     |

### 3-Cycle / 120-Second Rule

- 1 or 2 qualifying `ABSENT_CANDIDATE` cycles → stays `UNKNOWN_SUBMISSION`
- 3 cycles where the first-to-last timestamp span < 120 seconds → stays `UNKNOWN_SUBMISSION`
- 3 cycles spanning ≥120 seconds → `CONFIRMED_ABSENT`

## 4. Restart Behavior

1. `start()` scans `submission_attempts` for `SUBMITTING` or `UNKNOWN_SUBMISSION`
2. Any active quarantine **immediately DISARMS** the engine
3. Recovery is **read-only**: no placement, cancel, flatten, or re-protection
4. Evidence is collected and persisted; state transitions follow the same rules as online recovery
5. `SUBMITTING` rows from a prior crash are treated as ambiguous (same as `UNKNOWN_SUBMISSION`)

## 5. No-Resubmit Rule

- TS-P1-003 performs **no automatic resubmission** even after `CONFIRMED_ABSENT`
- Ordinary replay remains blocked
- A future separately authorized recovery action may create a new attempt without regressing this attempt's state

## 6. Forbidden Mutations

The following are **never** performed by TS-P1-003:
- Automatic cancel of exchange orders
- Automatic flatten of positions
- Automatic re-protection
- Any mutation of foreign/manual exchange state
- Automatic resubmission
- Config threshold changes
- API/dashboard expansion

## 7. Structured Broker Outcomes

| Outcome                | When                                               |
|------------------------|----------------------------------------------------|
| `PRE_SEND_FAILURE`     | Adapter proves no exchange write started            |
| `DEFINITIVE_REJECTION` | Complete response proves all orders rejected        |
| `VERIFIED_SUCCESS`     | Exact planned-role/cloid coverage confirmed         |
| `OUTCOME_UNKNOWN`      | Timeout, transport loss, partial, verification fail |

## 8. Secret Safety

- No raw exception messages, exchange bodies, credentials, wallet keys, or secret-looking strings are persisted in the evidence ledger
- Recovery evidence contains only safe reason codes, structured verdicts, and IDs
- `submission_recovery_evidence` records are append-only and immutable
