# TS-P1-007 Durable Daily-Risk Controls

Status: implemented locally, opt-in only. Operational activation and migration
remain separately prohibited.

## Owner policy

- Whole-account equity from one accepted TS-P1-006 checkpoint is authoritative.
- Trading days use UTC. The baseline is the last accepted checkpoint at or
  before 00:00 UTC; no baseline means fail closed.
- Daily-loss limit: 2% of day-start equity.
- Maximum intraday drawdown: 5% of the monotonic daily peak.
- Absolute equity floor: 500 USDC.
- Control evidence is sticky and append-only. Manual ARM cannot clear it.
- Schema v7 is additive and explicit; the application default remains v4.

## Data and ordering

An accepted v7 reconciliation transaction writes the checkpoint, its immutable
daily-risk row, every independently crossed control latch, and the latest accepted checkpoint
pointer atomically. Broker I/O occurs before that transaction. Risk evaluation
is pure and receives the portfolio snapshot and daily state bound to the same
checkpoint.

Missing, stale, future, malformed, cross-environment, policy-mismatched,
unattributed-funding, or date-mismatched evidence vetoes new risk and leaves the
engine DISARMED. Funding is retained diagnostically and is not subtracted from
whole-account equity a second time.

## Reset and rollback

Daily-loss and maximum-drawdown evidence can be superseded only after a new UTC
day has an authoritative baseline and an exact human acknowledgement is
recorded by the ARM request. UTC rollover alone does not deactivate a latch.
An equity-stop latch is account-scoped and additionally requires a fresh,
latest-resolved checkpoint above the persisted approved floor. Reset validation
is bound to the persisted policy version and occurs in the same transaction as
the reset row. Trigger/reset rows are never updated or deleted.

Rollback may stop consuming v7 and return to the predecessor path while
DISARMED. It may not delete v7 checkpoints, latches, reconcile failures,
funding evidence, or migration-failure evidence.

## Activation boundary

`Store.initialize()` still defaults to schema v4. Tests exercise v7 only on
pytest-owned temporary SQLite files. No operational database was migrated and
no runtime, broker, TESTNET, or deployment action is authorized by this
contract.
