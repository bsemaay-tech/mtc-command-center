# ADR-0026 - LLM Trading Safety Boundary

- Status: Accepted
- Ratification: Barış, 2026-07-18 — recorded in `_AI_MEMORY/DECISIONS.md` entry D016 addendum, after explicit discussion (created 2026-07-17 as Accepted without sign-off, corrected to Proposed, then formally ratified).
- Date: 2026-07-17
- Decision owners: Barış (authority owner); AI workflow, security, risk, and execution maintainers
- Related systems: Codex/LLM workflows, research tools, dashboards, risk engine, order manager
- Related reports: Consolidated report Sections 2, 17, 20, and 26; evidence claims CLM-010, CLM-034, and CLM-036
- Related ADRs: [ADR-0010](./ADR-0010-protected-core-path-policy.md), [ADR-0015](./ADR-0015-command-allowlist-and-network-gate.md), [ADR-0022](./ADR-0022-independent-risk-engine-veto.md), [ADR-0027](./ADR-0027-supply-chain-secret-security.md), [ADR-0028](./ADR-0028-dashboard-read-only-first.md)
- Review trigger: Any new model connector, tool permission, autonomous workflow, or proposed execution control

## Context

LLMs are useful for summarization, code review, hypothesis generation, anomaly explanation, and documentation. They are nondeterministic, prompt-injectable, and can leak supplied data. CLM-010 establishes no direct order authority.

## Problem

Giving an LLM credentials or mutable execution tools could turn untrusted text, hallucination, or model compromise into financial action.

## Decision Drivers

- Deterministic authorization and reproducibility.
- Least privilege and secret isolation.
- Human ownership of promotion and risk policy.
- Prompt-injection and data-exfiltration resistance.

## Considered Options

### Option A - LLM directly trades with limits

Rejected: limits do not make nondeterministic authority auditable.

### Option B - LLM emits executable commands for automatic approval

Rejected: formatting or schema validation does not prove intent or safety.

### Option C - LLM produces advisory artifacts only

Outputs pass deterministic schema, policy, tests, evidence, and human approval before any separate implementation or execution workflow.

## Decision

Adopt Option C. LLMs may summarize, analyze, review code, generate hypotheses, draft strategy candidates, explain anomalies, and produce reports. They may not sign or submit orders, change leverage or live risk limits, access withdrawal credentials, bypass deterministic validation, or promote a strategy to live trading. Model output is untrusted input.

## Rationale

This preserves analytical value without creating an untestable execution authority.

## Consequences

### Positive consequences

- Prompt injection or hallucination cannot directly create market exposure.
- Decisions retain deterministic evidence and human accountability.

### Negative consequences

- More manual and deterministic review gates.
- Some autonomous-agent features cannot be used.

### Operational consequences

- Record model/version, redacted inputs, output hash, reviewer, and disposition for material artifacts.

### Security consequences

- Secrets and raw sensitive logs are excluded; connectors require telemetry and outbound review.

### Licensing consequences

- Model/provider terms and generated-code provenance require review before distribution or import.

## Implementation Implications

Future tooling must enforce read-only/advisory permissions and separate model output from deterministic writers. No tool permissions change here.

## Validation Requirements

- Permission tests prove no model path can reach signing/order/risk-limit mutation.
- Prompt-injection tests against reports, logs, dashboards, and messages.
- Redaction and outbound-network tests.
- Rejected/approved artifact audit trail.

## Rollback or Reversal Conditions

Only a stricter boundary may supersede this ADR. Direct model trading authority is not a permitted rollback target.

## Open Questions

- OQ-005 exact connector/tool threat model.
- OQ-014 telemetry and data-flow audit.

## Evidence and References

- Consolidated report Sections 17 and 20.
- Evidence register CLM-010, CLM-034, and CLM-036.
