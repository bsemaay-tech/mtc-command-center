# VERTICAL SLICE SCOPE

> Status: DRAFT.
> Track: SYSTEM_TEST_ONLY / NOT STRATEGY_APPROVED / NO REAL MONEY.
> Binding status: Gate V0 planning approval recorded on 2026-07-02.
> No code, execution, schema, testnet, broker, TradingView, or WunderTrading
> work is approved by this document.

Every artifact from this track must carry this banner:

**SYSTEM_TEST_ONLY / NOT STRATEGY_APPROVED / NO REAL MONEY**

The benchmark strategy is a crash-test dummy. Its PnL is meaningless by
construction and must never appear in a promotable bucket, scorecard, dashboard
KPI, or promotion discussion.

## Purpose

This track exists to test execution-system plumbing with fake money and local
artifacts while strategy research stays primary.

It is intended to close these architecture risks:

- paper substrate undefined
- live gate undefined
- alert/execution-chain behavior untested
- signal idempotency and reconciliation unproven

It does not prove strategy quality, live readiness, paper readiness, Pine
parity, broker readiness, or profitability.

## Budget

- Research : vertical slice = 75 : 25, measured weekly across sessions and
  spend.
- Implementation should be cheap-model/mechanical where possible: Cline first,
  then `_deepseek_driver`, with Codex used for bounded judgment and audit.
- If the slice starts requiring Fable-grade sessions to move, it is overscoped.
- Mandatory review at day 30: Baris decides continue, pause, or kill. No
  auto-renewal.

## Core Slice

The core slice remains local and fake-money only.

1. Signal emitter:
   daily Python forward-run of the benchmark strategy using existing behavior,
   without modifying the engine, and emitting draft `mtc.signal/v1` JSON
   artifacts to a research directory. No network.
2. Local receiver:
   localhost only. Validates token, schema, environment, checksum, and
   idempotency key. Writes an execution-intent log. No broker.
3. Reconciliation reporter:
   daily diff of expected signals, received signals, and simulated fills.
   Produces a standard report artifact with the SYSTEM_TEST_ONLY banner.
4. Induced-failure drills:
   deliberate duplicates, dropped messages, malformed payloads, wrong
   environment, and exit-with-no-position. Results are documented per
   `PAPER_RECONCILIATION_PROTOCOL.md`.

## Extension Legs

Each extension leg requires its own explicit Baris approval line. None are
approved by this draft package.

- [ ] Leg 1 - TradingView alerts:
      existing review-Pine only, read-only inspection, alerts to local receiver.
      No new Pine. No Pine edits.
      Approved on: ____________
- [ ] Leg 2 - WunderTrading demo:
      demo/paper only. No real exchange keys. No real broker.
      Approved on: ____________
- [ ] Leg 3 - Binance Spot Testnet:
      testnet only. No mainnet. Order placement, exchange-resident stop,
      kill-and-restart reconcile test.
      Approved on: ____________

## Benchmark Strategy

The benchmark must be selected only as a systems test source. Robustness is not
required and must not be implied.

Candidate constraints:

- already in the engine's known strategy set
- no new strategy code
- no new Pine
- deterministic and boring
- no `PRE_REG_NEEDED` ambiguity
- signal frequency high enough for plumbing tests
- registered or labeled as SYSTEM_TEST_ONLY / promotable false before any
  artifact is emitted

Read-only benchmark audit completed on 2026-07-02. STG002 was selected because
it has more completed lifecycle events than STG001, stronger existing parity
evidence, and enough signal/trade cadence for plumbing tests. This selection is
only a SYSTEM_TEST_ONLY benchmark decision. It is not a strategy approval.

Baris picks benchmark: STG002 / `QL_ALPHA_LINK_8EMA_1H`.

Benchmark status:

- SYSTEM_TEST_ONLY.
- NOT STRATEGY_APPROVED.
- NO REAL MONEY.
- No TradingView, WunderTrading, broker, exchange, or testnet use.
- No new Pine.
- No new strategy logic.
- No scorecard, promotion, or profitability claim may be derived from this
  slice.

## File Allowlist

This is the intended implementation allowlist for a later implementation
approval. It is not active under Gate V0 planning approval.

- New files under `MTC_COMMAND_CENTER/03_QUANTLENS/tools/vertical_slice/`
  for emitter, receiver, reconciler, and tests.
- No file in `MTC_COMMAND_CENTER/06_SCHEMAS/` until separate Gate V1
  `schema_allow` approval.
- `MTC_COMMAND_CENTER/05_REGISTRY/VARIANT_LOG_REGISTRY.json` only for a
  benchmark registration entry, if Baris approves that registry write.
- Read-only dashboard reader additions only after separate scope approval.
- `_AI_MEMORY` handoff files only as required by normal Gate 7 write-back after
  an approved write session.

## Explicitly Out Of Scope

- Real exchange API keys.
- Mainnet.
- Real capital.
- Broker actions.
- Paper-broker actions.
- TradingView actions.
- WunderTrading actions.
- Binance testnet actions before Leg 3 approval.
- Futures or leverage.
- Edits to `01_PINE`, any `*.pine`, `MTC_V2`, parity files,
  `02_MTC_BACKTEST`, or `07_ADAPTERS`.
- Any `06_SCHEMAS` write before separate `schema_allow`.
- Production executor.
- Order-management system.
- Multi-strategy routing.
- Execution UI.
- Generating `backtest_profile_result.json`, `top_results.json`, scorecard
  changes, or promotion states from slice output.

## Stop Conditions

Halt the vertical slice immediately. Research continues regardless.

1. Budget breach:
   slice exceeds its capped share in any week.
2. Protected-path creep:
   any task requires touching Pine, parity, `02_MTC_BACKTEST`, adapters, or
   schemas beyond a pre-approved allowlist.
3. Real-key or mainnet suggestion:
   any plan, prompt, or sub-agent output suggests real keys, mainnet, broker,
   paper broker, or live actions.
4. Promotion contamination:
   any slice artifact appears in a promotable bucket, scorecard, dashboard KPI,
   or strategy-quality discussion.
5. Research displacement:
   a research candidate approaches the robustness gates. The slice pauses.
6. Blocked extension leg:
   TradingView, WunderTrading, or testnet leg hits an access or reliability
   wall. Record the finding and stop the leg. No workaround building.
7. Day-30 review:
   Baris continue/pause/kill decision required to proceed.

## Approval Gates

- Gate V0:
  Approved by Baris on 2026-07-02 for planning only. Core slice planning may
  begin. Implementation still requires a separate approval prompt.
- Gate V1:
  `schema_allow` approval for `mtc.signal/v1` in
  `MTC_COMMAND_CENTER/06_SCHEMAS/`. Until then, schema content stays only as an
  appendix in `PAPER_RECONCILIATION_PROTOCOL.md`.
- Gate V2:
  Leg 1 TradingView alerts.
- Gate V3:
  Leg 2 WunderTrading demo.
- Gate V4:
  Leg 3 Binance Spot Testnet.
- Gate V5:
  Day-30 review sign-off for another window.

Anything not covered by a gate above is not authorized.

## Signature

- [x] Baris approved this draft scope for planning only on: 2026-07-02.
