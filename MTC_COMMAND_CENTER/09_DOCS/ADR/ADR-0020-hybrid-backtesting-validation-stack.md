# ADR-0020 - Hybrid Backtesting and Validation Stack

- Status: Accepted
- Ratification: Barış, 2026-07-18 — recorded in `_AI_MEMORY/DECISIONS.md` entry D016. Accepts the tier DIRECTION; hftbacktest Hyperliquid coverage audit (TS-P3-004) and engine mapping remain required before integration.
- Date: 2026-07-17
- Decision owners: Barış (approval owner); QuantLens and MTC maintainers
- Related systems: QuantLens, existing fast and event-driven engines, research data lake
- Related reports: Consolidated report Sections 2, 12, 15, and 19; evidence claims CLM-004, CLM-005, CLM-025, and CLM-027
- Related ADRs: [ADR-0008](./ADR-0008-lineage-required-for-executed-results.md), [ADR-0011](./ADR-0011-subprocess-environment-isolation.md), [ADR-0019](./ADR-0019-separate-research-validation-paper-live.md), [ADR-0029](./ADR-0029-paper-to-live-promotion-gates.md)
- Review trigger: Completion of OQ-009/OQ-018, or addition of a strategy whose edge depends on order-book microstructure

## Context

Vectorized engines are efficient for broad exploration, while event-driven engines better represent order lifecycle. Queue position, maker fill, and latency require full order-book replay. The consolidated report concludes that no single backtester is sufficient for every strategy class. Full Hyperliquid collector coverage for hftbacktest remains unverified.

## Problem

Selecting one engine for every purpose either sacrifices research throughput or produces unrealistic execution claims. Multiple engines, however, can create inconsistent strategy definitions and non-reproducible comparisons.

## Decision Drivers

- Fast hypothesis and parameter triage.
- Explicit event/order semantics before operational use.
- Microstructure realism where the edge requires it.
- Walk-forward, bootstrap, Monte Carlo, benchmark, fee/funding/slippage, and parameter-stability evidence.
- Reproducible data/code/config lineage.
- Minimal duplication of strategy logic.

## Considered Options

### Option A - Vectorized or existing fast engine only

Maximizes throughput but cannot establish maker-fill, queue, or latency realism.

### Option B - Event-driven engine only

Improves lifecycle fidelity but makes broad exploration slower and still may not model queue position.

### Option C - hftbacktest for all research

Provides microstructure tools but requires high-quality L2/L3 data and adds unnecessary complexity for bar-based strategies.

### Option D - Tiered hybrid validation

Use the least expensive engine that can answer each question, with explicit escalation and common lineage.

## Decision

Propose Option D:

1. VectorBT or the existing fast engine for exploratory sweeps and parameter triage.
2. The existing event-driven engine, strengthened with NautilusTrader patterns where useful, for execution-parity validation.
3. hftbacktest for strategies sensitive to maker fills, latency, cancel/replace timing, or queue position.
4. All promotable research must also satisfy the repository's walk-forward, bootstrap, Monte Carlo, fee/funding/slippage stress, minimum-sample, multi-window, and benchmark requirements.

Engine results are not interchangeable. Each result records the engine, assumptions, data lineage, and validation tier.

The proposal does not add VectorBT or hftbacktest and does not claim collector completeness.

## Rationale

The tiered design aligns validation cost with strategy sensitivity while avoiding false precision. D016 (2026-07-18) accepted this direction; current-engine mapping and OQ-009 Hyperliquid data coverage remain evidence gates before integration.

## Consequences

### Positive consequences

- High research throughput without labeling vectorized fills as realistic.
- Explicit escalation for order-book-sensitive strategies.
- Better separation of hypothesis evidence from execution evidence.

### Negative consequences

- Multiple engines increase maintenance and parity work.
- Metrics may differ because assumptions differ.
- L2/L3 data acquisition and storage may be costly.

### Operational consequences

- A run manifest must identify engine tier and assumptions.
- Strategy logic needs a testable shared decision core or translation contract.

### Security consequences

- New packages/data collectors require dependency and outbound-network review.

### Licensing consequences

- Exact VectorBT edition, hftbacktest version, and transitive licenses must be reviewed before adoption.

## Implementation Implications

Future work would define a validation-tier contract, common metrics, reproducible manifests, and escalation rules. This ADR authorizes none of that work.

## Validation Requirements

- Gap audit of current fast/event-driven capabilities.
- Same-data comparison on representative bar and order-book strategies.
- Verified absence of lookahead and explicit fill/fee/funding assumptions.
- hftbacktest Hyperliquid field, sequence, timestamp, and gap audit.
- Deterministic rerun from frozen code/config/data.
- Documented criteria for when Tier 3 is mandatory.

## Rollback or Reversal Conditions

Use fewer engines if the gap audit proves one engine covers required tiers with equivalent evidence, or if data quality makes microstructure simulation misleading. Any simplification must preserve the evidence labels.

## Open Questions

- OQ-009: hftbacktest Hyperliquid collector completeness.
- OQ-010: required market-data sources and retention.
- OQ-018: existing engine versus Nautilus integration.

## Evidence and References

- Consolidated report Sections 12, 15, 19, and 21.
- Evidence register CLM-004, CLM-005, CLM-025, and CLM-027.
- `03_QUANTLENS/_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md` for existing promotion evidence requirements.
