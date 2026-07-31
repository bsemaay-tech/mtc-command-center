# ADR-0018 - Continue the Existing Python Trading System

- Status: Accepted
- Ratification: Barış, 2026-07-18 — recorded in `_AI_MEMORY/DECISIONS.md` entry D016. Route decided: continue the existing Python system (resolves TS-P0-004 jointly with ADR-0025).
- Date: 2026-07-17
- Decision owners: Barış (approval owner); MTC maintainers (architecture and evidence)
- Related systems: MTC Command Center, QuantLens, Python execution services, Hyperliquid bridge
- Related reports: Consolidated report Sections 2, 5, 19, 23, 28, and 29; evidence claims CLM-001 through CLM-009
- Related ADRs: [ADR-0001](./ADR-0001-command-dash-as-reference.md), [ADR-0004](./ADR-0004-no-live-trading-in-mvp.md), [ADR-0010](./ADR-0010-protected-core-path-policy.md), [ADR-0025](./ADR-0025-build-core-risk-reconciliation-internally.md)
- Review trigger: Completion of the current-system gap audit, or a funded proposal to replace the Python core

## Context

The repository already contains Python research, validation, dashboard, state, and execution-support capabilities with project-specific safety rules. The consolidated research found no third-party framework that matches the full Hyperliquid-first, auditable, Windows-aware workflow without major migration, licensing, or behavior compromises. Evidence claim CLM-009 accepts continuing the system only provisionally because the current capability gap is not yet mapped.

## Problem

The project needs a durable route decision before roadmap work. Wholesale adoption could accelerate selected features but would require re-platforming existing contracts. Continuing the current system preserves control but leaves the project responsible for difficult risk, reconciliation, recovery, and security work.

## Decision Drivers

- Preserve working project-specific research and audit contracts.
- Keep Python as the source of truth for strategy, risk, and state decisions.
- Retain native control of Hyperliquid-specific semantics.
- Avoid importing GPL/LGPL obligations accidentally.
- Minimize migration risk and duplicate validation systems.
- Permit best-of-breed libraries behind owned interfaces.
- Resolve OQ-001 with real code and test evidence before final acceptance.

## Considered Options

### Option A - Adopt an existing bot directly

Adopt Freqtrade or another complete bot. This provides mature workflows quickly, but imposes framework conventions, migration cost, and licensing constraints and does not eliminate project-specific safety work.

### Option B - Fork an existing bot

Fork Freqtrade, Hummingbot, Passivbot, or a smaller Hyperliquid bot. This adds upstream synchronization and security burden. Passivbot strategy logic is explicitly rejected; Hummingbot is specialized toward market making.

### Option C - Rewrite on NautilusTrader

Use NautilusTrader as the new core. It is the strongest architecture reference, but a Rust/Python rewrite would be a major migration and its Hyperliquid adapter remains a moving integration surface.

### Option D - Continue the current Python system and borrow selectively

Retain the system boundary and import SDKs, research tools, and design patterns only where contracts and licenses are clear.

## Decision

Propose Option D. Continue the existing Python trading system and do not replace it wholesale. Use Freqtrade as a general benchmark, NautilusTrader as an architecture reference, Hummingbot as a market-making reference, and selected libraries through project-owned interfaces.

This proposal does not claim that the current implementation already satisfies the target architecture. It becomes eligible for `Accepted` only after the gap audit demonstrates a credible path for the order, risk, reconciliation, data, and security gaps.

## Rationale

Selective borrowing preserves accumulated domain knowledge and limits framework lock-in. It also keeps the highest-risk behavior under explicit project governance. The initial conservative `Proposed` status reflected CLM-009's medium confidence and the unresolved OQ-001 capability map; D016 (2026-07-18) ratified the ADR as Accepted with OQ-001 still tracked as follow-up evidence.

## Consequences

### Positive consequences

- Existing artifacts, tests, and operating knowledge remain useful.
- Exchange and research libraries can evolve behind stable interfaces.
- Framework licensing does not automatically determine the product license.

### Negative consequences

- The project owns complex safety-critical engineering.
- Delivery may be slower than adopting a complete bot.
- Internal interfaces can become bespoke or under-tested.

### Operational consequences

- Roadmap work must begin with a file-and-test gap matrix.
- Framework migration remains a documented fallback, not parallel implementation.

### Security consequences

- Retaining control does not reduce the need for independent security review, secret isolation, or failure drills.

### Licensing consequences

- Patterns should be reimplemented cleanly when source licenses are incompatible.
- Exact dependency versions and notices require review before import.

## Implementation Implications

Future implementation would need owned interfaces for exchange access, order state, risk, persistence, and research validation. No interface, dependency, or code change is authorized by this ADR.

## Validation Requirements

- Map every target capability to current modules, tests, and known gaps.
- Compare migration cost and safety coverage against Freqtrade, NautilusTrader, and Hummingbot.
- Identify protected-path and parity impacts.
- Produce a dependency and license inventory.
- Demonstrate that proposed phases can close all blocker gaps without dual sources of truth.

## Rollback or Reversal Conditions

Reverse this proposal if the gap audit shows that the internal core cannot reach required safety/recovery standards at reasonable cost, if the product becomes primarily market making, or if a framework demonstrably satisfies the required contracts with lower risk. Reversal requires a superseding ADR and migration/rollback plan.

## Open Questions

- OQ-001: exact current-system capability gaps.
- OQ-013: clean-room and license boundaries.
- OQ-018: minimum event-driven validation engine.

## Evidence and References

- `C:\LAB\Trading Bot Research\#03 Deep research\01_CONSOLIDATED_REPORT\CONSOLIDATED_TRADING_BOT_RESEARCH_2026-07-17.md`, Sections 2, 5, 19, 23, and 28.
- `C:\LAB\Trading Bot Research\#03 Deep research\02_EVIDENCE_REGISTER\CLAIM_EVIDENCE_REGISTER.md`, CLM-001 through CLM-009.
- `00_AGENT_PROTOCOLS/EXECUTION_ARCHITECTURE_DECISION.md`, Python-engine source-of-truth direction.
