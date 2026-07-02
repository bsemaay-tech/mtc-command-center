# EXECUTION ARCHITECTURE DECISION

> Status: DRAFT.
> Track: SYSTEM_TEST_ONLY / NOT STRATEGY_APPROVED / NO REAL MONEY.
> Date: 2026-07-02.
> Source: Fable architecture audit package, adapted to the live repo paths by Codex.
> Binding status: Gate V0 planning approval recorded on 2026-07-02.
> No implementation, execution, schema, testnet, broker, TradingView, or
> WunderTrading work is approved by this document.

## Purpose

This document records the intended execution architecture direction without
authorizing execution work. It exists to prevent future agents from assuming
that TradingView -> WunderTrading -> broker is the production path.

The current repo state still has no live-ready strategy. Recent broad sweeps
show `robust_final = 0` across the existing library. This decision is about
future system architecture and a fake-money system test track only.

## Decision

1. The Python engine remains the single source of truth for strategy signals,
   risk decisions, state reconciliation, and any future execution path.
2. Target eventual production architecture is Option C:
   Python engine -> self-owned minimal execution service -> exchange API.
   This is not approved for implementation as production infrastructure now.
3. Transition architecture is Option D:
   Pine/TradingView may be used as a monitor and visualization layer. Pine is
   not the production signal source. Pine/Python divergence is a bug alarm,
   not a trade instruction.
4. WunderTrading may be considered only as a later demo/paper bridge if Baris
   separately approves that extension leg. It is not the production execution
   layer under this decision.
5. MTC Command Center remains read-only tracking and decision support. It must
   not gain execution capability or wording that implies execution capability.

## What This Decision Forbids

- Real exchange API keys, real capital, mainnet orders, live orders, broker
  actions, paper-broker actions, TradingView actions, WunderTrading actions,
  or testnet actions under this draft package.
- Treating TradingView alerts as reliable without a logged fidelity test.
- Treating a Pine compile pass as parity.
- Treating any SYSTEM_TEST_ONLY artifact as strategy evidence.
- Generating `backtest_profile_result.json`, `top_results.json`, scorecard
  changes, promotion states, or live/paper readiness evidence from this track.
- Editing Pine logic, `MTC_V2`, parity files, `02_MTC_BACKTEST`,
  `07_ADAPTERS`, or `06_SCHEMAS` without explicit Baris approval.

## Repo Safety Anchors

The live safety chain for this repo is:

- `AGENTS.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/AI_RULES.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/DO_NOT_TOUCH.md`
- `MTC_COMMAND_CENTER/AI_OPERATING_RULES.md`

`MTC_COMMAND_CENTER/AI_OPERATING_RULES.md` explicitly forbids live trading and
adding live webhooks, WunderTrading, or TradersPost integrations in foundation
work. This decision does not override that rule. It only defines a draft route
for a future fake-money, localhost-first SYSTEM_TEST_ONLY track.

## Currently Authorized Scope

Baris approved Gate V0 for SYSTEM_TEST_ONLY vertical-slice planning on
2026-07-02. This authorizes planning only. No execution architecture
implementation is authorized until a separate implementation prompt is
approved.

The planned core slice in `VERTICAL_SLICE_SCOPE.md` remains:

- localhost-first
- fake money only
- no real network dependency
- no `06_SCHEMAS` file until separate `schema_allow`
- no TradingView, WunderTrading, broker, testnet, or live extension leg without
  separate approval

## Signature

- [x] Baris approved this draft decision for planning only on: 2026-07-02.
