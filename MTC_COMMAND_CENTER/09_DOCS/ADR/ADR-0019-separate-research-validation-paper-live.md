# ADR-0019 - Separate Research, Validation, Paper, and Live Execution

- Status: Accepted
- Ratification: Barış, 2026-07-18 — recorded in `_AI_MEMORY/DECISIONS.md` entry D016 (created 2026-07-17 as Accepted without sign-off, corrected to Proposed, then formally ratified 2026-07-18).
- Date: 2026-07-17
- Decision owners: Barış (approval owner); MTC maintainers
- Related systems: QuantLens, backtest engines, system-test tools, paper/testnet bridge, any future live execution service
- Related reports: Consolidated report Sections 1, 12, 13, 20, and 28; evidence claims CLM-024 and CLM-025
- Related ADRs: [ADR-0003](./ADR-0003-read-only-first.md), [ADR-0004](./ADR-0004-no-live-trading-in-mvp.md), [ADR-0008](./ADR-0008-lineage-required-for-executed-results.md), [ADR-0011](./ADR-0011-subprocess-environment-isolation.md), [ADR-0029](./ADR-0029-paper-to-live-promotion-gates.md)
- Review trigger: Any request to share credentials, writers, databases, or mutable configuration between operational modes

## Context

The repository already distinguishes research evidence, system-test artifacts, dashboard visibility, paper/testnet operations, and live readiness. Existing ADR-0003 and ADR-0004 establish read-only-first and no-live-in-MVP boundaries. Consolidated research confirms that research shortcuts and testnet success must not be treated as execution readiness.

## Problem

A single runtime with mode flags can allow research assumptions, credentials, state, or data to cross into higher-risk environments. Shared mutable configuration and storage also make evidence provenance and incident recovery ambiguous.

## Decision Drivers

- Prevent research outputs from directly authorizing orders.
- Make environment identity unambiguous and fail closed.
- Preserve reproducibility and lineage.
- Limit credential and state blast radius.
- Require explicit promotion evidence and human approval.
- Keep strategy logic reusable only where its behavior is deterministic and compatible.

## Considered Options

### Option A - One runtime and database with a mode flag

Simple to operate, but a configuration mistake can cross environments and corrupt evidence or state.

### Option B - Shared runtime with separate credentials and tables

Improves credential isolation but leaves deployment, dependency, and writer coupling.

### Option C - Separate operational modes with explicit promotion contracts

Use separate runtime identity, configuration, credentials, state ownership, and evidence roots for research, validation/system test, paper/testnet, and any future live environment.

## Decision

Adopt Option C.

- **Environment separation:** each mode has an explicit identity and fail-closed startup guard.
- **Configuration separation:** no production-like mode silently inherits research defaults; configuration is versioned and attributable.
- **Database separation:** research artifacts, validation outputs, paper/testnet operational state, and any future live state have separate writer authority and must not share mutable operational tables.
- **Credential separation:** research and local validation have no exchange credentials; paper/testnet and any future live environment use distinct least-privilege credentials.
- **Runtime separation:** processes, working directories, ports, logs, and release identities are independently observable.
- **Promotion gates:** artifacts move by reviewed, immutable evidence references; running code or mutable state is not promoted in place.

Shared pure strategy calculations are allowed only when versioned and tested. Execution, fill, risk, and persistence shortcuts do not cross modes.

This ADR does not approve paper, testnet, or live activity. Existing approval gates remain controlling.

## Rationale

Isolation reduces accidental authority escalation and makes results auditable. It also supports explicit comparison between research assumptions and operational behavior.

## Consequences

### Positive consequences

- Smaller credential and state blast radius.
- Clear evidence lineage and incident boundaries.
- Research speed can remain high without weakening execution controls.

### Negative consequences

- More configuration, storage, and release artifacts to maintain.
- Cross-mode parity requires deliberate testing.
- Duplicate infrastructure may be necessary.

### Operational consequences

- Every process must report mode, version, commit, configuration hash, and state root.
- Promotion is a reviewed copy/reference operation, not a flag change.

### Security consequences

- Secrets cannot be reused across testnet and any future mainnet environment.
- Cross-mode network and writer permissions must be denied by default.

### Licensing consequences

- Mode isolation does not remove dependency-license obligations; each deployable environment needs an inventory.

## Implementation Implications

Future work must define mode-specific configuration schemas, storage ownership, credential provisioning, and release metadata. No such implementation is performed here.

## Validation Requirements

- Negative tests prove that wrong-environment credentials/configuration fail startup.
- Research processes cannot reach order endpoints or operational writers.
- Paper/testnet state cannot be opened by research writers.
- Artifact lineage identifies mode, code, data, configuration, and runtime.
- Promotion requires explicit gate evidence and approval.

## Rollback or Reversal Conditions

This decision may be narrowed only if equivalent isolation is mechanically proven. Combining state or credentials requires a superseding ADR, threat model, migration plan, and rollback test.

## Open Questions

- Exact physical database boundaries and backup policy.
- Configuration versioning format.
- Deployment topology for Windows and later Linux/VPS environments.

## Evidence and References

- Consolidated report Sections 1, 12, 20, 28, and 30.
- Evidence register CLM-024 and CLM-025.
- `_AI_MEMORY/LIVE_TRADING_GATE.md`, which remains unsigned and blocks live readiness.
