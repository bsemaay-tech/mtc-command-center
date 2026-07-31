# ADR-0024 - Data Storage Separation

- Status: Accepted
- Ratification: Barış, 2026-07-18 — recorded in `_AI_MEMORY/DECISIONS.md` entry D016. Accepts the separation DIRECTION only; no database migration until the TS-P2-006 benchmark decides keep-vs-migrate.
- Date: 2026-07-17
- Decision owners: Barış (approval owner); data, operations, and audit maintainers
- Related systems: Research lake, operational state, audit events, dashboard metrics
- Related reports: Consolidated report Sections 15 and 19; evidence claims CLM-028, CLM-029, and CLM-031
- Related ADRs: [ADR-0002](./ADR-0002-file-status-first-sqlite-later.md), [ADR-0006](./ADR-0006-single-writer-lockfile-before-database.md), [ADR-0014](./ADR-0014-minimal-status-event-ledger.md), [ADR-0017](./ADR-0017-windows-safe-lock-and-atomic-write-recovery.md), [ADR-0023](./ADR-0023-idempotent-order-management-reconciliation.md)
- Review trigger: Completion of the storage gap audit/benchmark or material workload/deployment change

## Context

Research history, operational orders, append-only audit events, and monitoring metrics have different consistency and query needs. Existing ADRs deliberately use inspectable files and single-writer safeguards before database migration. The consolidated research proposes Parquet/DuckDB for history and a transactional operational store, but does not justify PostgreSQL yet.

## Problem

One storage technology can create poor fit or unsafe writer coupling. Premature migration can discard current Windows/file reliability lessons; indefinite file use can limit transactional recovery.

## Decision Drivers

- Immutable, efficient historical analytics.
- Transactional order/fill/risk/reconcile state.
- Append-only forensic history.
- Metrics optimized for monitoring, not domain truth.
- Compatibility with current single-writer and atomic-write rules.

## Considered Options

### Option A - Keep all state in JSON/Markdown

Inspectable but weak for transactional relationships and scale.

### Option B - Put all data in PostgreSQL immediately

Strong transactions but premature, operationally heavier, and poor as the only analytical/audit format.

### Option C - Separate stores by responsibility

Parquet/DuckDB for historical research; existing transactional mechanism or PostgreSQL after gap analysis for operational state; append-only event log for audit; structured/Prometheus-compatible metrics for monitoring.

## Decision

Propose Option C. This ADR does not mandate PostgreSQL or migrate existing files. ADR-0002, ADR-0006, ADR-0014, and ADR-0017 remain valid until the gap audit and recovery benchmark justify a change.

Historical data must preserve immutable raw inputs and versioned normalized/derived layers. Operational state requires one authoritative writer and atomic transactions. Audit events are append-only and not silently rewritten. Metrics are derived observability, not order truth.

## Rationale

Separation aligns consistency, retention, and query patterns while allowing an evidence-based database choice.

## Consequences

### Positive consequences

- Better analytical performance and clearer sources of truth.
- Operational transactions are isolated from research scans.

### Negative consequences

- Multiple stores require lineage, backup, and retention coordination.
- Cross-store reports may be eventually consistent.

### Operational consequences

- Each store needs ownership, schema/version, backup, restore, and corruption procedures.

### Security consequences

- Operational and credential-adjacent data require stricter access; metrics/audit exports require redaction.

### Licensing consequences

- Exact database, driver, ORM, DuckDB, and PyArrow versions/licenses require review.

## Implementation Implications

Future work must inventory existing stores and benchmark representative Windows and target-host recovery. No schema, database, or dependency change is authorized.

## Validation Requirements

- OQ-004/016 workload and concurrency gap audit.
- Crash/restart/backup/restore tests for candidate operational stores.
- Representative DuckDB/Parquet query and schema-evolution benchmark.
- Proven lineage from raw data to derived research and metrics.
- Single-writer and atomicity guarantees preserved during any migration.

## Rollback or Reversal Conditions

Retain or return to current file/single-writer mechanisms if a database adds failure risk without required value. Any migration must be reversible with verified exports and reconciliation.

## Open Questions

- PostgreSQL versus SQLite/single-writer.
- Partitioning, retention, and schema evolution.
- Prometheus-compatible stack and cardinality limits.

## Evidence and References

- Consolidated report Section 15.
- Evidence register CLM-028, CLM-029, and CLM-031.
