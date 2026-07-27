# 27 — Authoritative Risk-Input Snapshot Contract (TS-P1-006)

Status: implemented as an **opt-in v6 capability**. Default schema remains v4.
This contract adds no risk thresholds and activates no runtime.

## Authority

On a v6 store, new-entry risk consumes exactly one
`AuthoritativeRiskSnapshot` loaded from the sole
`reconcile_checkpoint_latest` pointer. The risk path must not substitute
`Broker.account()`, `Broker.positions()`, a mapping, a cached object, or a
checkpoint from another read epoch. Strategies and LLMs cannot bypass this
boundary.

The v4/v5 predecessor path remains compatible because those schemas do not
carry full-reconcile checkpoints. Deployment and schema activation are separate
owner-gated work.

## Payload versions

- `ts-p1-005-snapshot-v1` is retained immutable historical evidence. It stores
  component metadata/digests but not canonical portfolio rows, so it can never
  authorize v6 ARM or risk.
- `ts-p1-006-snapshot-v2` adds canonical `POSITIONS`, `BALANCES`, and `MARGIN`
  rows plus their component digests. All seven TS-P1-005 components must still
  be complete and exact.
- A fresh real v2 reconcile is the only upgrade path. No v1 backfill or rewrite
  is possible or permitted.

The payload marker is part of the canonical hash domain. Row order is
canonicalized before digesting; a semantic row change, duplicate position,
noncanonical order, row-count mismatch, or digest mismatch fails closed.

## Atomic load

`Store.load_authoritative_risk_snapshot(now, max_age_s)` is SQLite-only. A
bounded read transaction pins one committed epoch and validates:

1. v6 is active and no caller transaction is already open;
2. the sole pointer resolves to a complete accepted checkpoint;
3. its attempt is the most recently resolved attempt;
4. all seven components are complete, exact, and timestamped;
5. the payload is v2 and its component/diff/hash chain is coherent;
6. canonical portfolio rows recompute to their persisted component digests;
7. position symbols are unique and quantities finite;
8. equity, withdrawable, used margin, and available margin are finite,
   nonnegative, and satisfy the TS-P1-005 account identity;
9. coverage bounds are provable;
10. acceptance is not in the future and age is within the existing
    `max(reconcile_interval_s * 3, 30s)` bound.

No SQLite transaction spans broker I/O or an `await`.

## Immutable risk view

`AuthoritativeRiskSnapshot` and its position rows are tuple-backed frozen
records with no instance dictionary or writable slots. They contain checkpoint,
attempt, run and hash identity; acceptance/load/component observation times;
coverage bounds; canonical positions; and account/margin values.

Risk derives its existing `AccountSnapshot` and open-position gate input from
this one object. Existing thresholds, sizing arithmetic, gate order after the
new provenance gate, realized-PnL/consecutive-loss inputs, and funding
non-consumption remain unchanged.

## Failure behavior

Missing, v1, unsupported, malformed, stale, future, superseded, incomplete,
tampered, ambiguous, or unreadable evidence is a reason-coded veto. The engine
sets in-memory `DISARMED` first, latches `risk_input_error` and
`risk_snapshot_error`, then performs best-effort persistence/notification.
There is no point-read fallback, retry, automatic re-arm, or submission.

v6 ARM also loads and validates the snapshot. A metadata-valid v1 checkpoint
therefore cannot arm and wait until the first signal to discover that risk
inputs are unavailable.

## Persistence, restart, migration, and rollback

No table, column, index, trigger, pointer, schema version, or migration is
added. v2 uses the existing immutable `reconcile_checkpoints.snapshot_json`.
Default initialization remains v4; v6 remains opt-in.

Restart retains every v1/v2 checkpoint and failed attempt. A later failed or
interrupted attempt supersedes a young accepted checkpoint for risk. Rollback
may remove the v2 consumer/producer code but must never delete or rewrite
checkpoint, diff, component, funding, decision, or failure evidence.

## Required proof

Tests cover v2 determinism and deep immutability; legacy reopen/refusal;
stale/future/superseded/malformed/duplicate/non-finite/negative/tampered
evidence; concurrent read epochs; crash/restart; nonzero positions; in-memory
DISARM on read failure; no v6 point-account call; unchanged v4 and interim PnL
behavior; and unchanged funding non-consumption.
# TS-P1-007 extension

On an explicitly opened schema-v7 store, the authoritative portfolio snapshot
is loaded together with its immutable daily-risk state and active latches in one
bounded SQLite read epoch, bound to the same checkpoint, attempt, run, equity
and policy version. A pointer move, UTC-date
change, missing baseline, policy mismatch, malformed row, or active durable
latch fails closed. Schema v4 remains the application default; v6 behavior is
unchanged when v7 is inactive.
