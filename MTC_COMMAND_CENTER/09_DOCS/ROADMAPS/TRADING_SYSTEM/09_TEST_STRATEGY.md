# 09 — Test Strategy

The test pyramid is environment-aware: deterministic local tests first, recorded fixtures next, testnet only under explicit approval, and real-capital observations only if Gate E is separately satisfied. Passing a lower tier never proves a higher tier.

## Test levels

| Level | Purpose | Default evidence source | External side effects |
| --- | --- | --- | --- |
| L0 static | Imports, types, formatting, route/dependency/security inventory | Source tree | None |
| L1 unit/property | Pure state transitions, identities, risk boundaries, codecs | Generated values and fixtures | None |
| L2 component/contract | Adapter/store/API/strategy interfaces | Mocks and temporary stores | None |
| L3 recorded replay | Exchange messages, fills, L2/trades, failures | Redacted immutable recordings | None |
| L4 local integration | Bridge components, restart, DB copies, read model | MockBroker/temp paths/local process if approved | Local only |
| L5 testnet/paper | Real SDK/API semantics and monitored operations | Hyperliquid testnet/approved paper run | Explicit approval; bounded attempts |
| L6 limited real observation | Real execution evidence | Dedicated restricted account | Gate E and separate Barış authorization only |

## Required coverage

| Test family | What must be proven | Primary tier | Higher-tier evidence |
| --- | --- | --- | --- |
| Unit tests | Pure calculations, parsing, state guards and error taxonomy | L1 | None |
| Property-based tests | Identity uniqueness/stability, transition legality, exposure invariants, serialization round trips | L1 | None |
| Contract tests | Strategy, market-data, broker, store, read-model and event interfaces | L2 | L3 for exchange payload variants |
| Exchange-adapter tests | Native/CCXT path, trigger/reduce-only, errors, rate/nonce/time behavior | L2/L3 | L5 for exact testnet semantics |
| Replay tests | Same event stream creates same decisions/state/checkpoint | L3/L4 | L5 only for observational comparison |
| Reconciliation tests | Orders/fills/positions/balance/margin/pending diffs; foreign-state policy | L2/L4 | L5 with raw, redacted exchange evidence |
| Restart tests | Crash at every order/reconcile/database state resumes DISARMED without duplicate/naked state | L4 | L5 bounded drill |
| Reconnect tests | WS death, resubscribe, gap classification, `DATA_RESTORED`, REST fallback and stale block | L2/L3/L4 | L5 bounded natural/injected observation |
| Partial-fill tests | All fill permutations match protection or safe flattening | L1/L2/L3 | L5 only after local matrix passes |
| Duplicate-order tests | Same intent/retry/restart produces one exchange request identity | L1/L2/L4 | L5 bounded duplicate delivery drill |
| Unknown-submission tests | Timeout/connection loss enters quarantine; no retry before absence proof | L2/L3/L4 | L5 only with strict one-attempt runbook |
| Stale-data tests | Sequence/time gap blocks new risk and emits honest health | L1/L2/L3 | L5 observation |
| Rate-limit tests | Backoff/budget/error classes do not create duplicate/unknown action | L2/L3 | L5 only if safe and approved |
| Database corruption tests | Truncation, malformed schema/WAL, partial migration and restore fail safely | L4 temp copies | Never corrupt active DB |
| Migration tests | Upgrade, idempotent rerun, compatibility, rollback/export | L2/L4 | Paper DB copy only after approval |
| Kill-switch tests | Kill is idempotent; cancels owned orders; optional flatten/restart evidence | L2/L4 | L5 drill; L6 only under signed plan |
| Risk-veto tests | Stale/incomplete inputs and every boundary block deterministically | L1/L2 | L5 observation of status only where possible |
| Paper/live parity tests | Signals, intended orders, costs/fills and divergence are attributable | L3/L5 | L6 comparison only if authorized |
| Backtest reproducibility | Frozen code/config/data/engine/cost/search reproduces artifacts | L4 research environment | No exchange needed |
| Performance tests | Reconcile deadline, event lag, order-authority latency, DB writer/load, read-model payload | L4 | L5 observation for rate/latency qualification |
| Security tests | Secret redaction, wrong-env startup, permissions, outbound destinations, dependency/SBOM/route scans | L0–L4 | Credential rotation/revoke drill separately approved |
| Dependency scanning | Lock/hash, SCA, licenses, SBOM and known-bad fixture | L0/L4 build | Container scan only when image exists |
| Testnet tests | Native SDK behavior, triggers, fills, reconnect and reconcile | L5 | Pre-registered, bounded, explicit approval |
| Limited-live evidence | Exact release, limits, kill/rollback/on-call and post-trade review | L6 | Never inferred from testnet |

## Strategy and validation tests

- Golden/fixture tests must use independently fixed expected values, not the same formula under test.
- Same-data comparisons must state bar-close timing, timezone, fees, slippage, funding, order types, partial-fill behavior and rounding.
- Fast/vectorized output is labeled research approximation.
- Event-driven validation is required before operational promotion.
- hftbacktest is required only for maker/latency/queue/cancel-replace-sensitive strategies and only after collector coverage passes.
- Canonical QuantLens gates remain mandatory: rolling walk-forward/locked OOS, buy-and-hold/excess alpha, bootstrap/BH-FDR, DSR, CPCV/PBO when applicable, multi-window/parameter stability, sample size and reproducibility.

## Order/reconciliation invariant matrix

| Invariant | Minimum tests |
| --- | --- |
| One intent, one durable request identity | property collision set; retry; process restart; DB reopen |
| Unknown never blindly retried | timeout before response; connection reset after send; delayed fill; delayed open-order appearance |
| Partial quantity always bounded | 0%, 1%, multiple partials, full fill, cancel remainder, protection reject, process crash |
| Foreign state is not auto-mutated | foreign order, position, vault/subaccount ambiguity |
| Reconcile freshness is real | stale timestamp, failed cycle, partial API response, current-run filter, recovery checkpoint |
| Kill/disarm is race-safe | kill during LLM await, account read, submission, partial fill, reconcile and restart |

## Persistence test rules

- Use temporary databases or verified copies only.
- Preserve the original DB/WAL/SHM bytes before any recovery experiment.
- Assert schema version, migration ledger, transaction boundaries and restart behavior.
- A successful open is not a restore proof; reconcile the restored checkpoint against fixtures/exchange truth at the appropriate tier.

## External-run protocol

Before L5/L6: capture release manifest; verify flat/owned state with raw response evidence; define one attempt/retry policy; define stop conditions; confirm credential/network; name observer; log timestamps/run ID; stop on unexpected response; reconcile cleanup; preserve raw redacted evidence. No external test is automatically retried.

## Test-result reporting

Report exact command, working directory, commit, environment, selected tests, counts, duration, warnings, skipped tests and failures. “Tests pass” without this identity is not gate evidence. This roadmap planning run executed no application test suite.

