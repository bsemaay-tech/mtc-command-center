# ADR-0022 - Independent Risk Engine with Veto Authority

- Status: Accepted
- Ratification: Barış, 2026-07-18 — recorded in `_AI_MEMORY/DECISIONS.md` entry D016 (created 2026-07-17 as Accepted without sign-off, corrected to Proposed, then formally ratified 2026-07-18).
- Date: 2026-07-17
- Decision owners: Barış (risk-policy owner); MTC risk and execution maintainers
- Related systems: Strategy plugins, portfolio state, order manager, monitoring, kill controls
- Related reports: Consolidated report Sections 14 and 19; evidence claims CLM-010 and CLM-030
- Related ADRs: [ADR-0004](./ADR-0004-no-live-trading-in-mvp.md), [ADR-0019](./ADR-0019-separate-research-validation-paper-live.md), [ADR-0023](./ADR-0023-idempotent-order-management-reconciliation.md), [ADR-0026](./ADR-0026-llm-trading-safety-boundary.md)
- Review trigger: Any change to risk authority, portfolio scope, leverage, or emergency controls

## Context

Strategies express trade intent; they are not reliable authorities for portfolio, account, or operational risk. Research consensus strongly supports an internal risk engine with independent authority. Exact thresholds remain open under OQ-011.

## Problem

Strategy-owned limits can be inconsistent or bypassed. Exchange limits prevent invalid orders but do not enforce the project's loss, exposure, freshness, or concentration policies.

## Decision Drivers

- One deterministic policy boundary before order authorization.
- Portfolio-wide and venue-aware controls.
- Fail-closed behavior on stale or inconsistent state.
- Human-governed limits and auditable decisions.
- No strategy or LLM bypass.

## Considered Options

### Option A - Risk inside each strategy

Simple but inconsistent and bypassable.

### Option B - Rely on exchange margin and liquidation controls

Insufficient; exchange constraints protect the venue, not the project.

### Option C - Independent risk engine with veto authority

Centralize policy using current portfolio, account, market, and operational state.

## Decision

Adopt Option C. Strategies propose intents. The risk engine may permit, resize, reject, freeze new risk, require exposure reduction, or authorize a policy-defined close. It evaluates position sizing, maximum leverage, daily loss, maximum drawdown, symbol/side exposure, total wallet exposure, liquidation distance, data freshness, reconcile health, kill state, and equity hard stop. No strategy, dashboard, operator shortcut, or LLM may bypass it.

This ADR fixes authority and required control classes, not numeric thresholds or implementation.

## Rationale

Independent veto authority prevents local strategy logic from weakening account-wide safety and makes every decision explainable and testable.

## Consequences

### Positive consequences

- Consistent portfolio protection and a single audit point.
- Strategies remain simpler and less privileged.

### Negative consequences

- The risk engine becomes safety-critical and potentially a throughput bottleneck.
- Bad global policy can block valid trades or mishandle emergencies.

### Operational consequences

- Risk state, data age, inputs, decision, rule IDs, and reason codes must be observable.

### Security consequences

- Limit changes require authenticated, authorized, logged control; default startup is frozen/disarmed until state is valid.

### Licensing consequences

- Third-party numeric libraries may assist calculations, but copied framework risk code requires license review.

## Implementation Implications

Future work needs a deterministic risk contract, immutable policy version, portfolio snapshot, reason codes, and kill/freeze paths. No code or limits are changed here.

## Validation Requirements

- Boundary tests for every control and precedence rule.
- Stale/missing/contradictory state fails closed.
- Strategies and LLM paths cannot reach order authorization directly.
- Restart reproduces risk state from authoritative inputs.
- Kill and equity-stop drills produce complete audit evidence.

## Rollback or Reversal Conditions

The veto boundary may be superseded only by a stricter independently reviewed design. Risk authority must never revert to strategy-only or LLM-controlled logic.

## Open Questions

- OQ-011: thresholds and precedence.
- Portfolio correlation/concentration model.
- Authorized emergency-close semantics.

## Evidence and References

- Consolidated report Section 14.
- Evidence register CLM-010 and CLM-030.
