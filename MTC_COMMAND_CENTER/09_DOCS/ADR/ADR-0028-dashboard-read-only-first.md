# ADR-0028 - Dashboard Is Read-Only First

- Status: Accepted
- Ratification: Barış, 2026-07-18 — recorded in `_AI_MEMORY/DECISIONS.md` entry D016 addendum, after explicit discussion (created 2026-07-17 as Accepted without sign-off, corrected to Proposed, then formally ratified).
- Date: 2026-07-17
- Decision owners: Barış (authority owner); dashboard, monitoring, risk, and operations maintainers
- Related systems: MTC dashboard/API, monitoring, reconciliation, runtime status, emergency controls
- Related reports: Consolidated report Sections 16 and 19; evidence claims CLM-035 and CLM-040
- Related ADRs: [ADR-0001](./ADR-0001-command-dash-as-reference.md), [ADR-0003](./ADR-0003-read-only-first.md), [ADR-0015](./ADR-0015-command-allowlist-and-network-gate.md), [ADR-0022](./ADR-0022-independent-risk-engine-veto.md), [ADR-0023](./ADR-0023-idempotent-order-management-reconciliation.md)
- Review trigger: Any proposed dashboard command, order action, mutable risk control, or remote emergency control

## Context

The existing dashboard contract is read-only. Research supports observability before remote control and identifies FreqUI and commercial products as UX references only.

## Problem

A dashboard that both displays and mutates trading state expands authentication, authorization, CSRF, network, and operator-error risk before core state is trustworthy.

## Decision Drivers

- Trustworthy observability and honest missing-data states.
- Minimal remote attack surface.
- Separation of monitoring from execution authority.
- Complete audit for any future emergency action.

## Considered Options

### Option A - Full remote trading console

Rejected for the initial architecture.

### Option B - Read-only dashboard plus ordinary remote controls

Still creates a privileged command path before authorization design.

### Option C - Read-only observability; emergency controls separately gated

Display authoritative state. Defer remote actions; any later emergency control requires explicit authorization and audit.

## Decision

Adopt Option C. The dashboard initially exposes exchange connection, last market-data timestamp, WebSocket health, REST fallback state, reconcile freshness, local/exchange differences, unknown orders, risk-engine state, daily PnL, exposure, leverage, liquidation distance, runtime version/commit, mode, and kill-switch status. It does not submit orders or change risk/execution state.

Emergency controls are deferred to a separate approved design with authenticated named actions, least privilege, confirmation, idempotency, and append-only audit evidence.

## Rationale

Read-only-first preserves visibility without making a web surface part of the critical execution path.

## Consequences

### Positive consequences

- Lower attack surface and clearer operational truth.
- Dashboard failure cannot directly create orders.

### Negative consequences

- Operators need a separate local/runbook path for intervention.
- Read models may lag operational state.

### Operational consequences

- Every metric needs source, age, mode, and unavailable/stale semantics.

### Security consequences

- Write verbs remain denied; future emergency controls need separate auth/threat review.

### Licensing consequences

- UX may be inspired by products, but code/assets and licenses are not copied blindly.

## Implementation Implications

Future roadmap work may add read models and health indicators only after source contracts are mapped. No dashboard code changes here.

## Validation Requirements

- HTTP write verbs remain rejected.
- Displayed values trace to authoritative sources with freshness.
- Stale/missing state cannot appear healthy.
- No credential or secret exposure.
- Runtime mode/commit and kill status are explicit.

## Rollback or Reversal Conditions

Adding any mutation requires a superseding ADR and security review. Read-only behavior remains the fallback.

## Open Questions

- OQ-019 prioritized UX references.
- Authentication and out-of-band emergency-control design.

## Evidence and References

- Consolidated report Section 16.
- Evidence register CLM-035 and CLM-040.
