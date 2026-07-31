# ADR-0025 - Build Core Risk and Reconciliation Internally

- Status: Accepted
- Ratification: Barış, 2026-07-18 — recorded in `_AI_MEMORY/DECISIONS.md` entry D016. Route decided: build core risk/order/reconciliation internally, borrow bounded tools behind owned interfaces (resolves TS-P0-004 jointly with ADR-0018).
- Date: 2026-07-17
- Decision owners: Barış (approval owner); MTC architecture maintainers
- Related systems: Risk, portfolio, order management, reconciliation, release governance, third-party dependencies
- Related reports: Consolidated report Sections 19 and 22 through 25; evidence claims CLM-001 through CLM-011 and CLM-030
- Related ADRs: [ADR-0018](./ADR-0018-continue-existing-python-system.md), [ADR-0020](./ADR-0020-hybrid-backtesting-validation-stack.md), [ADR-0021](./ADR-0021-hyperliquid-integration-policy.md), [ADR-0022](./ADR-0022-independent-risk-engine-veto.md), [ADR-0023](./ADR-0023-idempotent-order-management-reconciliation.md)
- Review trigger: ADR-0018 acceptance/rejection, inability to close a core gap, or proposed framework fork

## Context

External frameworks provide useful SDKs, algorithms, and patterns, but the project's highest-risk policies depend on its own state, approvals, and recovery contracts. The route decision was initially Proposed pending OQ-001; Barış ratified it Accepted in D016 (2026-07-18), with the OQ-001 capability map still tracked as follow-up evidence.

## Problem

Importing a complete framework can hide or constrain core invariants; building every utility internally wastes effort and increases defects.

## Decision Drivers

- Project ownership of safety and state invariants.
- Reuse mature bounded libraries.
- Avoid framework lock-in and incompatible licenses.
- Keep strategy behavior and release gates explicit.

## Considered Options

### Option A - Build everything internally

Maximum control but duplicates mature SDK, optimization, and validation work.

### Option B - Adopt a complete framework core

Faster feature acquisition but transfers architecture, upgrade, and licensing constraints.

### Option C - Own safety-critical core and borrow bounded components

Build domain authority; import tools behind owned interfaces; study frameworks without copying behavior blindly.

## Decision

Propose Option C.

Build internally: risk engine, order manager, reconciliation, portfolio state, and release/promotion gates. Borrow or import after review: official exchange SDKs, CCXT, VectorBT where licensing permits, hftbacktest when applicable, and Optuna where pre-registered optimization is appropriate. Study only: Freqtrade, NautilusTrader, Hummingbot, Passivbot, OctoBot, and commercial UX products.

This does not authorize implementation or copying. Passivbot strategy logic and experimental AI trading cores remain rejected.

## Rationale

The split reuses mature low-level capabilities without outsourcing project-specific authority. D016 (2026-07-18) accepted this route together with ADR-0018 after the gap-audit review.

## Consequences

### Positive consequences

- Safety invariants remain inspectable and testable.
- Dependencies are replaceable behind project interfaces.

### Negative consequences

- Considerable internal engineering and review burden.
- Clean-room pattern reimplementation can be slower.

### Operational consequences

- Each borrowed component needs an owner, pin, upgrade test, and rollback plan.

### Security consequences

- Imported packages remain untrusted until reviewed; internal code still requires adversarial testing.

### Licensing consequences

- GPL/LGPL code is not copied into incompatible distributions; exact dependencies and notices are reviewed.

## Implementation Implications

The gap audit must produce explicit build/import/study mappings at module level. No package or source file changes occur here.

## Validation Requirements

- Capability and cost comparison for every core subsystem.
- Dependency/license/security review for imports.
- Contract and replacement tests at each borrowed boundary.
- Proof that external components cannot bypass project risk/order authority.

## Rollback or Reversal Conditions

Supersede if the gap audit proves a framework core is safer and cheaper, with acceptable migration and licensing. Reversal requires a separate migration ADR.

## Open Questions

- OQ-001 capability gaps.
- OQ-013 licensing boundaries.
- Delivery-capacity threshold that triggers framework reconsideration.

## Evidence and References

- Consolidated report Sections 19 and 22 through 25.
- Evidence register CLM-001 through CLM-011 and CLM-030.
