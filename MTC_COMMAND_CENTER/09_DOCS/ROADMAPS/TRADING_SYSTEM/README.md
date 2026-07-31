# Trading System Implementation Roadmap

Status: **Planning complete; implementation not started**

Created: 2026-07-17

Canonical directory: `C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\09_DOCS\ROADMAPS\TRADING_SYSTEM`

Repository baseline: branch `feature/donchian-crypto-ladder`, commit `70586cf5e023c74ac77d4cda503979c01531c36b`

Deployed-runtime baseline: isolated worktree `C:\P2RT`, detached commit `74e0990b1d0722a301d8385f7833d4903baeeb8f`

This package converts the consolidated research and ADRs into an incremental implementation plan. It does not authorize implementation, dependency installation, exchange calls, testnet/paper operations, database changes, scheduler changes, credential access, or live trading.

## Authority and boundaries

- The existing Python system remains the working product boundary while ADR-0018 and ADR-0025 remain Proposed.
- Accepted ADRs are binding constraints, not claims that code is complete.
- Proposed ADRs schedule evidence tasks; this roadmap does not silently accept them.
- `C:\P2RT` is a protected deployed-runtime worktree. It was inspected read-only and was not changed.
- The Hyperliquid bridge was not listening on port 8790 during this planning run. Therefore no active monitoring window is claimed.
- `_AI_MEMORY\LIVE_TRADING_GATE.md` is unsigned. Phase 6 is blocked and is governance-only.
- The MTC dashboard remains read-only. Existing localhost bridge mutation endpoints are current-state evidence, not the target remote-control design.

## Document map

| Document | Purpose |
| --- | --- |
| [01 Current System Baseline](./01_CURRENT_SYSTEM_BASELINE.md) | Verified, partial, documented-only, and missing capabilities |
| [02 Current System Gap Audit](./02_CURRENT_SYSTEM_GAP_AUDIT.md) | Current-to-target gaps with severity and phase |
| [03 Target Architecture](./03_TARGET_ARCHITECTURE.md) | Incremental component, control, data, and recovery design |
| [04 Implementation Roadmap](./04_IMPLEMENTATION_ROADMAP.md) | Phase outcomes and task-level implementation contract |
| [05 Implementation Backlog](./05_IMPLEMENTATION_BACKLOG.md) | Execution-ready task cards and the single first task |
| [06 Validation and Release Gates](./06_VALIDATION_AND_RELEASE_GATES.md) | Required pass/fail evidence |
| [07 Dependency and Sequence Map](./07_DEPENDENCY_AND_SEQUENCE_MAP.md) | Critical path, approvals, and parallel work |
| [08 Risk Register](./08_RISK_REGISTER.md) | Delivery and operational risks with controls |
| [09 Test Strategy](./09_TEST_STRATEGY.md) | Test tiers, environments, and evidence rules |
| [10 Phase Execution Protocol](./10_PHASE_EXECUTION_PROTOCOL.md) | Mandatory protocol for later implementation sessions |

## Governing inputs

- `09_DOCS\ADR\ADR_INDEX.md` and ADR-0001 through ADR-0029.
- `C:\LAB\Trading Bot Research\#03 Deep research\01_CONSOLIDATED_REPORT\CONSOLIDATED_TRADING_BOT_RESEARCH_2026-07-17.md`.
- `C:\LAB\Trading Bot Research\#03 Deep research\02_EVIDENCE_REGISTER\CLAIM_EVIDENCE_REGISTER.md`.
- `C:\LAB\Trading Bot Research\#03 Deep research\04_OPEN_QUESTIONS\OPEN_QUESTIONS_AND_CONFLICTS.md`.
- `03_QUANTLENS\_user_guide\07_BACKTEST_AND_OPTIMIZATION_RULES.md` and `11_TRIAGE\BACKTEST_OPTIMIZATION_RUNBOOK.md`.
- `IBKR_PAPER_BRIDGE` source, tests, architecture/status/deployment documents, plus read-only inspection of the deployed `C:\P2RT` code.

## Existing plans reused; duplicates avoided

`09_DOCS\MVP_ROADMAP.md` remains the historical MTC read-only-dashboard roadmap. `00_AGENT_PROTOCOLS\EXECUTION_ARCHITECTURE_DECISION.md`, `PAPER_RECONCILIATION_PROTOCOL.md`, and the bridge build/status documents remain subsystem evidence. They are not duplicate full-system roadmaps and are linked rather than copied.

## First implementation task

**TS-P0-001 — Add a read-only repository/runtime baseline manifest and drift checker.** It must compare source/config identity without starting, stopping, arming, querying, or modifying the bridge. See [the backlog task card](./05_IMPLEMENTATION_BACKLOG.md#ts-p0-001--add-a-read-only-repositoryruntime-baseline-manifest-and-drift-checker).

## Status vocabulary

- `Not started`: no implementation authorized or performed.
- `Blocked`: a required decision, evidence item, monitoring period, or human approval is missing.
- `Deferred`: intentionally outside the current delivery horizon.
- No roadmap task is marked complete.
