# ADR-0029 - Paper-to-Live Promotion Gates

- Status: Accepted
- Ratification: Barış, 2026-07-18 — recorded in `_AI_MEMORY/DECISIONS.md` entry D016 addendum. Accepts the gate FRAMEWORK only: this ratification signs nothing operational — `_AI_MEMORY/LIVE_TRADING_GATE.md` remains unsigned, live/mainnet remains blocked, and every individual gate still requires its own evidence and signature.
- Date: 2026-07-17
- Decision owners: Barış (sole approval authority); research, risk, execution, security, and operations maintainers
- Related systems: QuantLens, paper/testnet bridge, risk, reconciliation, monitoring, release governance
- Related reports: Consolidated report Sections 12, 14, 17, 28, and 30; evidence claims CLM-024, CLM-025, CLM-030, and CLM-031
- Related ADRs: [ADR-0004](./ADR-0004-no-live-trading-in-mvp.md), [ADR-0008](./ADR-0008-lineage-required-for-executed-results.md), [ADR-0019](./ADR-0019-separate-research-validation-paper-live.md), [ADR-0020](./ADR-0020-hybrid-backtesting-validation-stack.md), [ADR-0023](./ADR-0023-idempotent-order-management-reconciliation.md), [ADR-0027](./ADR-0027-supply-chain-secret-security.md)
- Review trigger: Completion/sign-off of `_AI_MEMORY/LIVE_TRADING_GATE.md` or any request to consider real capital

## Context

Research or paper results do not establish live readiness. The repository's live-trading gate is draft and unsigned; live trading remains blocked. This ADR defines a proposed governance shape without recommending or approving live trading.

## Problem

Informal promotion can mistake backtest scores, model consensus, short paper runs, or testnet connectivity for evidence that a strategy and execution system are safe.

## Decision Drivers

- Strategy robustness and adequate sample size.
- Failure/restart/reconnect/reconciliation evidence.
- Complete audit, security, monitoring, and rollback readiness.
- Explicit human approval per strategy and capital level.

## Considered Options

### Option A - Promote after backtest thresholds

Rejected; ignores operations and forward evidence.

### Option B - Promote after a short successful paper/testnet run

Rejected; small samples and untested failures remain.

### Option C - Evidence-gated progression with explicit stop conditions

Require research, OOS, robustness, paper/testnet, operational, security, and human gates. Any limited-real-capital phase is separately approved and reversible.

## Decision

Propose Option C. Mandatory gates include research acceptance; out-of-sample and walk-forward validation; bootstrap and Monte Carlo; fee, slippage, and funding stress; minimum sample size; pre-registered paper duration; restart recovery; reconnect testing; reconciliation tests; complete audit logs; incident-free monitoring; security/credential review; and documented rollback criteria.

Only after every signed gate could a separately approved small-capital limited phase be considered. It must use a dedicated account, hard capital/exposure limits, independent kill paths, and no automatic capital increase. This sentence is governance, not a recommendation or authorization. Current live status remains blocked.

## Rationale

Promotion is a chain of independent evidence, not a score or AI judgment. D016 (2026-07-18) accepted the framework; the live gate remains unsigned and policy thresholds remain evidence-gated.

## Consequences

### Positive consequences

- Prevents weak research or connectivity evidence from becoming financial authority.
- Makes rollback and incident readiness first-class.

### Negative consequences

- Long evidence cycle; many strategies will never qualify.
- Windows reset after material changes increase time and cost.

### Operational consequences

- Each gate needs dated immutable artifacts, owner, expiry rules, and stop conditions.

### Security consequences

- Least-privilege keys, rotation, kill/revoke drills, and incident runbooks are mandatory.

### Licensing consequences

- Deployable dependency/license inventory must be complete before any higher-risk phase.

## Implementation Implications

The roadmap may define evidence-producing tasks but must not mark this ADR accepted or authorize a live phase. No run or configuration change occurs here.

## Validation Requirements

- Frozen code/config/data lineage and deterministic rerun.
- Required statistical and benchmark gates with no waived blockers.
- Pre-registered paper/testnet duration and sample; zero unexplained reconciliation breaks.
- Duplicate, timeout, reconnect, restart, kill, stale-data, and exchange-halt drills.
- Complete monitoring/audit evidence and signed rollback runbook.
- Explicit written Barış approval for each future phase.

## Rollback or Reversal Conditions

Any incident, unexplained mismatch, stale evidence, code/config change, security finding, or gate failure returns the system to the prior lower-risk/disarmed mode and resets affected evidence. Removing gates requires a superseding approved ADR.

## Open Questions

- Exact duration, sample, thresholds, and expiry rules.
- Definition of incident-free and material change.
- `_AI_MEMORY/LIVE_TRADING_GATE.md` remains unsigned.

## Evidence and References

- Consolidated report Sections 12, 14, 17, 28, and 30.
- Evidence register CLM-024, CLM-025, CLM-030, and CLM-031.
- `_AI_MEMORY/LIVE_TRADING_GATE.md` (draft; not approval).
