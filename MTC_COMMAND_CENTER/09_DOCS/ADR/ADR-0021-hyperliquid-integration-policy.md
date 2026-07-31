# ADR-0021 - Hyperliquid Integration Policy

- Status: Accepted
- Ratification: Barış, 2026-07-18 — recorded in `_AI_MEMORY/DECISIONS.md` entry D016 (created 2026-07-17 as Accepted without sign-off, corrected to Proposed, then formally ratified 2026-07-18).
- Date: 2026-07-17
- Decision owners: Barış (approval owner); exchange-adapter and execution maintainers
- Related systems: Any Hyperliquid market-data, account, order, and reconciliation adapter
- Related reports: Consolidated report Sections 2, 11, 13, 19, and 21; evidence claims CLM-006, CLM-011, and CLM-015 through CLM-024
- Related ADRs: [ADR-0011](./ADR-0011-subprocess-environment-isolation.md), [ADR-0015](./ADR-0015-command-allowlist-and-network-gate.md), [ADR-0019](./ADR-0019-separate-research-validation-paper-live.md), [ADR-0023](./ADR-0023-idempotent-order-management-reconciliation.md), [ADR-0027](./ADR-0027-supply-chain-secret-security.md)
- Review trigger: Hyperliquid API/SDK major change, unsupported required feature, or addition of another exchange

## Context

Official documentation verifies the Hyperliquid Python SDK, CCXT integration, agent/API wallets, signer-scoped nonces, `cloid`, reduce-only and trigger orders, subaccount/vault behavior, builder codes, WebSocket heartbeats, and separate testnet/mainnet endpoints. Neither SDK supplies a project-complete order manager, risk engine, or reconciler.

## Problem

Using only CCXT can hide exchange-specific semantics. Using only the official SDK can couple domain logic directly to a moving API and does not provide multi-exchange normalization. The project needs one owned boundary that preserves native behavior and recovery evidence.

## Decision Drivers

- Official signing and API behavior for critical paths.
- Multi-exchange normalization where semantics are genuinely common.
- Explicit handling of account, order, fill, nonce, and recovery states.
- Least-privilege wallet isolation.
- Testnet/mainnet separation.
- Observable rate limits, reconnects, and reconciliation health.

## Considered Options

### Option A - CCXT only

Provides broad normalization but may lag or flatten native Hyperliquid behavior.

### Option B - Official SDK directly throughout domain code

Preserves native capabilities but spreads exchange coupling and makes testing/replacement harder.

### Option C - Project-owned adapter using the official SDK with selective CCXT paths

Keep native critical behavior in one adapter and use CCXT for normalized, non-critical multi-exchange operations.

## Decision

Adopt Option C.

- The official `hyperliquid-python-sdk` is the native base for signing and exchange-specific behavior.
- CCXT may be used where normalization is useful and equivalent behavior is verified.
- Native overrides are required for signing, signer-scoped atomic nonce handling, client order IDs, trigger and reduce-only orders, partial fills, subaccounts, vaults, builder fields, and other non-portable semantics.
- Use separate agent/API wallets per trading process or subaccount as official nonce guidance recommends. Query account state using the actual master/subaccount/vault address.
- Testnet and mainnet use separate endpoints, credentials, configuration, state, and evidence. Testnet success is not mainnet readiness.
- WebSocket handling includes heartbeat, reconnect/backoff, resubscription, sequence/gap detection, and stale-data state. REST is a bounded recovery/reconciliation path.
- Rate-limit and exchange error bodies remain observable; silent retry is forbidden for unknown order outcomes.
- Open orders, fills, positions, balances, and margin are reconciled after restart/reconnect and periodically.
- Builder-code support, if ever used, must be explicit, opt-in, disclosed, and accounted for; this ADR does not select a fee policy.

Neither the official SDK nor CCXT is a trading engine or source of risk policy.

## Rationale

The hybrid adapter keeps official native behavior while limiting exchange coupling and preserving future multi-exchange options. High-confidence official evidence supports the boundary even though exact pinned-version coverage remains a gap-audit task.

## Consequences

### Positive consequences

- Critical Hyperliquid semantics remain explicit and testable.
- CCXT does not become the lowest-common-denominator authority.
- Domain logic is insulated from SDK changes.

### Negative consequences

- Two client stacks can duplicate market/account operations.
- Native overrides increase maintenance and test scope.
- Feature parity must be rechecked on upgrades.

### Operational consequences

- Runtime status must expose endpoint/environment, wallet role, connection state, rate-limit state, reconcile freshness, and adapter version.

### Security consequences

- Agent private keys remain outside source control and are isolated by environment/process.
- Main-wallet and withdrawal authority are excluded from bot runtime.

### Licensing consequences

- Pin and review the official SDK and CCXT versions and transitive dependencies; retain required notices.

## Implementation Implications

Future implementation needs an exchange-neutral domain interface plus a Hyperliquid-native adapter and contract tests. No connector or dependency is changed by this ADR.

## Validation Requirements

- Source-level feature matrix for the pinned SDK and CCXT versions.
- Offline contract tests for signing inputs, nonce uniqueness, `cloid`, triggers, reduce-only, partial fills, and errors.
- Separately approved testnet tests for reconnect, REST recovery, rate limits, subaccounts/vaults, restart, and reconciliation.
- Proof that unknown outcomes do not cause blind resubmission.
- Secret scan and no-mainnet/no-withdrawal verification.

## Rollback or Reversal Conditions

Replace or narrow the adapter if the official SDK becomes unsuitable, CCXT proves complete for a non-critical path, or the venue API changes materially. Reversal requires preserved order identity/state and a migration test; direct domain-wide SDK calls remain disallowed.

## Open Questions

- OQ-006 through OQ-008: pinned feature coverage and environment differences.
- OQ-012: wallet lifecycle and rotation.
- OQ-020: builder-code fee policy.

## Evidence and References

- Consolidated report Sections 11, 13, 19, and 21.
- Evidence register CLM-006, CLM-011, and CLM-015 through CLM-024.
- [Official Hyperliquid Python SDK](https://github.com/hyperliquid-dex/hyperliquid-python-sdk).
- [Official Hyperliquid API documentation](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api).
