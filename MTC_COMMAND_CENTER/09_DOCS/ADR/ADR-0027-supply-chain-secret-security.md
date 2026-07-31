# ADR-0027 - Supply-Chain and Secret Security

- Status: Accepted
- Ratification: Barış, 2026-07-18 — recorded in `_AI_MEMORY/DECISIONS.md` entry D016 (created 2026-07-17 as Accepted without sign-off, corrected to Proposed, then formally ratified 2026-07-18).
- Date: 2026-07-17
- Decision owners: Barış (credential owner); security, dependency, and deployment maintainers
- Related systems: Python dependencies, containers, CI, exchange wallets, model connectors, backups
- Related reports: Consolidated report Sections 17 and 18; evidence claims CLM-018, CLM-020, CLM-032, and CLM-033
- Related ADRs: [ADR-0010](./ADR-0010-protected-core-path-policy.md), [ADR-0011](./ADR-0011-subprocess-environment-isolation.md), [ADR-0015](./ADR-0015-command-allowlist-and-network-gate.md), [ADR-0021](./ADR-0021-hyperliquid-integration-policy.md), [ADR-0026](./ADR-0026-llm-trading-safety-boundary.md)
- Review trigger: Dependency, build image, credential store, outbound destination, or deployment change

## Context

Trading packages and credentials are high-value targets. Official Hyperliquid guidance supports agent-wallet isolation; research identifies malicious packages, telemetry, and transitive dependencies as material risks.

## Problem

One compromised dependency, install script, image, connector, or leaked key can bypass application controls.

## Decision Drivers

- Least privilege and revocability.
- Reproducible, reviewable dependency sets.
- Detectable secret and software provenance failures.
- Bounded outbound communications and recoverable backups.

## Considered Options

### Option A - Trust popular packages and environment variables

Insufficient provenance, transitive, and leakage controls.

### Option B - Review only direct trading dependencies

Misses build, UI, telemetry, and transitive attack paths.

### Option C - Layered secret and supply-chain controls

Apply controls across source, build, dependency, image, runtime, network, and recovery.

## Decision

Adopt Option C. No withdrawal-enabled key or main-wallet private key enters bot runtime. Use isolated agent/API wallets, secrets outside source control, rotation/revocation, protected backups, lock files, pinned versions or hashes where practical, dependency allowlists, secret scanning, SCA, SBOM generation, container scanning, and review of install/post-install scripts and binary wheels. Unreviewed binary trading packages are forbidden. Inventory telemetry and outbound destinations; deny or approve them explicitly.

## Rationale

No single scanner protects the complete path. Layering reduces both likelihood and recovery time.

## Consequences

### Positive consequences

- Smaller credential blast radius and stronger dependency provenance.
- Faster incident containment and rebuild.

### Negative consequences

- Upgrade friction, scanner noise, and operational overhead.

### Operational consequences

- Every deployable artifact needs a dependency/SBOM record and credential-rotation/backup procedure.

### Security consequences

- Secrets never appear in logs, prompts, reports, screenshots, or repositories; outbound access is reviewed.

### Licensing consequences

- SBOM/license inventory also enforces GPL/LGPL/notices and transitive obligations.

## Implementation Implications

The gap audit must inventory current controls and propose tools. This ADR installs nothing and changes no credentials.

## Validation Requirements

- Secret and dependency scans on representative artifacts.
- Rebuild from locked inputs and verify SBOM.
- Agent-wallet revoke/rotate recovery drill under separate approval.
- Restore test for protected backups.
- Outbound/telemetry allowlist verification and malicious-package tabletop exercise.

## Rollback or Reversal Conditions

Individual tools may be replaced when equivalent controls are proven. The control classes and no-withdrawal boundary remain mandatory.

## Open Questions

- OQ-012 wallet lifecycle.
- OQ-015 exact security toolchain.
- Code-signing and provenance mechanism for Windows and future Linux images.

## Evidence and References

- Consolidated report Sections 17 and 18.
- Evidence register CLM-018, CLM-020, CLM-032, and CLM-033.
