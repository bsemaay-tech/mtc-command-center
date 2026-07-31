# ADR-0023 - Idempotent Order Management and State Reconciliation

- Status: Accepted
- Ratification: Barış, 2026-07-18 — recorded in `_AI_MEMORY/DECISIONS.md` entry D016 (created 2026-07-17 as Accepted without sign-off, corrected to Proposed, then formally ratified 2026-07-18).
- Date: 2026-07-17
- Decision owners: Barış (approval owner); order, persistence, and reconciliation maintainers
- Related systems: Order manager, exchange adapters, operational state, risk engine, audit log
- Related reports: Consolidated report Sections 11 and 13; evidence claims CLM-015 through CLM-023 and CLM-031
- Related ADRs: [ADR-0014](./ADR-0014-minimal-status-event-ledger.md), [ADR-0017](./ADR-0017-windows-safe-lock-and-atomic-write-recovery.md), [ADR-0021](./ADR-0021-hyperliquid-integration-policy.md), [ADR-0022](./ADR-0022-independent-risk-engine-veto.md), [ADR-0024](./ADR-0024-data-storage-separation.md)
- Review trigger: Exchange adapter, order-state model, persistence, or retry-policy change

## Context

Exchange submission can time out after acceptance, fills can be partial, cancels can remain pending, and local state can become stale across reconnect/restart. Hyperliquid supports `cloid`, but the project must own identity and recovery semantics.

## Problem

Blind retries can duplicate exposure. Treating local state as exchange truth can hide orphan orders or positions. Treating only exchange snapshots as truth loses intent and audit lineage.

## Decision Drivers

- Deterministic identity and duplicate prevention.
- Explicit unknown-state recovery.
- Exchange authority for actual orders, fills, positions, and balances.
- Persistent local intent and event history.
- Periodic and event-triggered reconciliation with health metrics.

## Considered Options

### Option A - Let each exchange adapter manage lifecycle

Fragments policy and makes cross-venue behavior inconsistent.

### Option B - Trust local database state

Preserves intent but cannot prove actual exchange exposure.

### Option C - Project-owned idempotent order manager plus reconciliation

Persist intent and identity locally; reconcile actual state against the exchange.

## Decision

Adopt Option C. Every intent receives a deterministic internal ID and stable exchange `client_order_id`/`cloid`. Submission is idempotent; duplicate intent or delivery cannot create a second order. Accepted, resting, partially filled, filled, pending-cancel, canceled, rejected, expired, and unknown outcomes are represented explicitly.

An unknown submission outcome enters recovery: query by client ID and reconcile orders/fills/positions before retry. Local intent and audit history remain authoritative for what the system attempted; exchange state is authoritative for actual orders, fills, positions, balances, and margin. Reconciliation runs periodically and after startup, reconnect, timeout, error, and operator recovery. Blind resubmission is forbidden.

## Rationale

This design combines intent lineage with external truth and prevents duplicate exposure during ambiguous failures.

## Consequences

### Positive consequences

- Safe retry semantics and restart recovery.
- Detectable orphan, missing, duplicate, and divergent state.

### Negative consequences

- More persistent states and failure transitions.
- Exchange history/rate limits can delay recovery.

### Operational consequences

- Publish reconcile freshness, duration, mismatch counts, unknown orders, pending cancels, and last successful full comparison.

### Security consequences

- Recovery tools require narrow authorization; audit records must redact secrets but preserve evidence.

### Licensing consequences

- Framework implementations may be studied, but the domain state machine remains project-owned.

## Implementation Implications

Future work must define the state machine, identity algorithm, persistence transaction, exchange queries, mismatch policy, and append-only events. Nothing is implemented here.

## Validation Requirements

- Duplicate-delivery, timeout-after-accept, partial-fill, cancel-race, reconnect, and kill/restart tests.
- Collision tests for client IDs.
- Three-way reconciliation of intent, local operational state, and exchange state.
- Unknown outcomes never cause blind retry.
- Complete reason-coded event log and health metrics.

## Rollback or Reversal Conditions

Replace the design only with an equivalent or stronger idempotency/recovery contract. Migration must preserve identities, open-order mapping, and audit history.

## Open Questions

- OQ-002: exact state transitions and terminality.
- OQ-003: ID generation and retry/reuse rules.
- Reconcile mismatch severity and automatic freeze policy.

## Evidence and References

- Consolidated report Section 13.
- Evidence register CLM-015 through CLM-023 and CLM-031.
