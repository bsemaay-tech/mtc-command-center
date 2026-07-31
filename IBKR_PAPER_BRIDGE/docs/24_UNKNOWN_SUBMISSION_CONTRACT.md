# Unknown Submission Contract (TS-P1-003)

This contract covers a bracket submission whose exchange outcome cannot be
proved. It changes no Pine, strategy, entry-band, trail, or parity logic.

## Durable states

Schema v4 keeps the accepted `order_identity` table unchanged and adds
`submission_attempts` plus append-only `submission_recovery_evidence`.

Allowed attempt transitions are intrinsic to the store and enforced again by a
SQLite trigger:

```text
SUBMITTING -> PRE_SEND_FAILURE
SUBMITTING -> DEFINITIVE_REJECTION
SUBMITTING -> UNKNOWN_SUBMISSION
SUBMITTING -> VERIFIED_SUCCESS -> FINALIZED
UNKNOWN_SUBMISSION -> CONFIRMED_PRESENT
UNKNOWN_SUBMISSION -> CONFIRMED_ABSENT
```

Self, backward, skipped, and terminal transitions are forbidden. Attempt
identity, request linkage, recovery payload, planned role-to-cloid map, origin,
and creation time are immutable. Recovery evidence cannot be updated or
deleted.

`SUBMITTING`, `UNKNOWN_SUBMISSION`, and `CONFIRMED_PRESENT` are quarantine
states. Any one of them forces `DISARMED`, blocks ARM, blocks every new entry
placement in `OrderManager`, and appears in the status quarantine count.

## Before broker I/O

The broker boundary supplies one pure `planned_cloids(plan)` method. The manager
uses that exact map; Hyperliquid and Mock use the same method when building
their requests. The manager does not derive broker cloids.

One `BEGIN IMMEDIATE` transaction:

1. reserves deterministic `intent_id` and `request_id` in `order_identity`;
2. writes one immutable `SUBMITTING` attempt;
3. stores the canonical recovery payload and exact planned roles/cloids.

Only safe plan fields, canonical float encodings, codes, and identifiers are
stored. Raw exceptions, exchange bodies, secrets, credentials, wallet data,
and API keys are forbidden.

## Submission classification

Adapters return typed outcomes or typed errors. Exception-message substring
parsing is forbidden.

- `PRE_SEND_FAILURE`: legal only when the adapter proves no exchange write call
  began.
- `DEFINITIVE_REJECTION`: a complete response conclusively rejects every
  planned order and accepts, rests, fills, or leaves pending none.
- `VERIFIED_SUCCESS`: exact role and cloid coverage with only
  success-compatible states.
- `OUTCOME_UNKNOWN`: any accepted/rejected mixture, partial or malformed
  result, timeout, reset, post-send crash, duplicate/extra/missing/wrong role or
  cloid, or verification failure.

Hyperliquid marks the write boundary immediately before `bulk_orders`. Every
failure after that point is conservative. Its final typed success contains
exact planned role/cloid coverage; it never returns the old permissive raw dict
to the production manager.

Normal trade, order, identity, and attempt finalization is one SQLite
transaction with exact pre-state and row-count checks. That transaction
advances the attempt through `VERIFIED_SUCCESS` to `FINALIZED`. If local
finalization fails after possible broker success, the attempt becomes
`UNKNOWN_SUBMISSION`. If that transition write also fails, the already durable
`SUBMITTING` row remains quarantined.

The old single-entry protocol recorder used only by accepted in-process
`dry_run` tests has a narrow compatibility shim. It is not available to the
Mock or Hyperliquid adapters and is not a broker/exchange runtime path.

## Immediate engine response

`UnknownSubmissionError` contains only a safe reason code, `request_id`, and
`attempt_id`. The engine immediately:

1. sets memory and persisted application state to `DISARMED`;
2. records decision stage `UNKNOWN_SUBMISSION`;
3. records only safe codes and IDs;
4. does not increment or wait for the ordinary three-rejection counter.

While quarantined, automatic cancel, flatten, re-protection, trailing,
resubmission, and foreign/manual state mutation are not introduced.

## Recovery evidence

Each adapter query reports one typed status:

`FOUND`, authoritative `NOT_FOUND`, `QUERY_FAILED`, `UNAVAILABLE`,
`TRUNCATED`, `STALE`, or `CONFLICTING`.

A complete absence cycle requires all of the following for the exact stored
request and cloid map:

- successful direct lookup for every planned cloid, each `NOT_FOUND`;
- complete open-order coverage, `NOT_FOUND`;
- complete historical-order coverage over the attempt window, `NOT_FOUND`;
- complete fill coverage over the attempt window, `NOT_FOUND`.

Empty open orders alone never proves absence. Missing APIs, failed queries,
truncation, stale data, partial brackets, forged linkage, mismatched cloid
maps, or conflicting evidence never qualify. Position data can reveal exposure
or conflict but cannot prove absence.

Any planned cloid found by direct, open-order, historical-order, or fill
evidence resolves to `CONFIRMED_PRESENT`. The engine remains quarantined and
performs no automatic mutation.

Incomplete or conflicting evidence remains unknown and resets the consecutive
absence sequence. `CONFIRMED_ABSENT` requires three consecutive complete
cycles whose trusted local observation timestamps span at least 120 seconds.
One or two cycles, or three cycles spanning less than 120 seconds, remain
unknown.

Evidence append and its counter/state effect are one transaction. Evidence is
never rewritten after a later verdict.

## Restart and reconciliation

Startup reconciliation and every recurring reconciliation run one recovery
cycle for each active `SUBMITTING` or `UNKNOWN_SUBMISSION` attempt. A restart
therefore performs no placement retry. `CONFIRMED_PRESENT` remains visible and
blocks ARM. `CONFIRMED_ABSENT` is terminal; it does not resubmit, and the
existing deterministic identity reservation continues to block ordinary
replay.

## Migration

Fresh databases initialize at schema v4. A v3-to-v4 upgrade is one
`BEGIN IMMEDIATE` transaction and does not rebuild `order_identity`; failure
rolls back to clean v3. A v2 database first commits a validated v3 migration,
then attempts v4 separately. A later v4 failure therefore leaves valid v3.
Reopening v4 is idempotent.
