# SYSTEM_TEST_ONLY Vertical Slice Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a localhost/fake-money vertical slice that proves signal emission, validation, idempotency, simulated fills, reconciliation, and failure drills for the approved STG002 benchmark.

**Architecture:** The first implementation is replay-first: it reads existing STG002 trade artifacts and emits deterministic `mtc.signal/v1` JSON payloads into an isolated system-test run directory. The receiver owns local state, deterministic fake fills, idempotency, and rejection dispositions; the reconciler compares the three local ledgers. There is no broker, exchange, TradingView, WunderTrading, testnet, real key, CLI, server, or dashboard execution surface in V1.

**Tech Stack:** Python standard library, existing STG002 CSV artifacts, pytest-style or unittest-compatible tests under `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests`, Markdown reports.

---

## Status And Scope

Status: DRAFT / SYSTEM_TEST_ONLY / NOT STRATEGY_APPROVED / NO REAL MONEY.

Gate V0 allows planning only. This plan does not authorize implementation. A
separate Baris approval prompt is required before any file in the future
implementation allowlist is created.

Approved benchmark:

- Strategy folder:
  `MTC_COMMAND_CENTER/03_QUANTLENS/strategies/STG002_ql_alpha_link_8ema_1h/`
- Candidate id:
  `QL_ALPHA_LINK_8EMA_1H`
- Engine strategy id:
  `QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL`
- Symbol/timeframe:
  `LINKUSDT` / `1h`
- Source artifacts for first slice:
  `QL_ALPHA_LINK_8EMA_1H_signals.csv`,
  `QL_ALPHA_LINK_8EMA_1H_trades.csv`, and `producer_spec.json`

The replay-first choice is intentional. It tests the execution plumbing against
a stable known signal/trade set before any future worker connects the slice to
engine-forward generation. Connecting to `mega_walk_forward.py` or any strategy
producer remains a separate approval decision.

## Non-Negotiable Boundaries

- No `MTC_COMMAND_CENTER/06_SCHEMAS/` write. The schema remains appendix-only
  in `PAPER_RECONCILIATION_PROTOCOL.md` until Gate V1 `schema_allow`.
- No Pine, `*.pine`, `MTC_V2`, parity, `02_MTC_BACKTEST`, `07_ADAPTERS`,
  broker, exchange, testnet, TradingView, or WunderTrading changes.
- No backtest, optimization, scorecard, promotion, `top_results.json`, or
  `backtest_profile_result.json` generation.
- No secret in the repo. Test auth tokens must be synthetic strings generated
  inside tests or passed via environment variables.
- Every emitted artifact and report must include:
  `SYSTEM_TEST_ONLY / NOT STRATEGY_APPROVED / NO REAL MONEY`.

## Planned File Structure

Create only after separate implementation approval:

- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/vertical_slice/__init__.py`
  Package marker.
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/vertical_slice/constants.py`
  Banner text, approved benchmark identifiers, default artifact paths, allowed
  environment values for this track.
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/vertical_slice/contracts.py`
  In-code copy of the appendix schema fields plus validation helpers. This is
  not a repo schema file.
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/vertical_slice/stg002_replay_emitter.py`
  Reads STG002 CSV artifacts and writes EXPECTED signal payloads.
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/vertical_slice/local_receiver.py`
  Pure local receiver logic: validate, authenticate, checksum, deduplicate,
  track one local simulated position, write RECEIVED rows, and emit
  deterministic fake FILLED rows without broker semantics.
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/vertical_slice/reconciler.py`
  Three-ledger diff and report writer.
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_vertical_slice_contracts.py`
  Contract and validation tests.
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_vertical_slice_replay.py`
  STG002 replay tests on small temporary samples.
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_vertical_slice_receiver.py`
  Receiver idempotency, auth, checksum, and state tests.
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_vertical_slice_reconciler.py`
  Reconciliation and failure-drill tests.

Deferred V1.1 files, not part of the first implementation:

- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/vertical_slice/cli.py`
  Thin local CLI wrapper.
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/vertical_slice/drills.py`
  Standalone drill generators. V1 implements drills as test cases first.

Runtime outputs, after implementation approval, should go under:

`MTC_COMMAND_CENTER/03_QUANTLENS/system_test/<run_id>/`

That directory must never be treated as `05_BACKTEST_RESULTS` and must never
feed promotion, scorecard, dashboard KPI, Strategy Research Lab, or
`RESEARCH_RUN_REGISTRY.json` paths. Implementation must verify the root is
git-ignored before any local run. If it is not ignored, stop and ask Baris for
approval to add the ignore rule.

## Data Flow

1. `stg002_replay_emitter.py` reads the existing STG002 CSV artifacts.
2. It derives EXPECTED payloads from `QL_ALPHA_LINK_8EMA_1H_trades.csv` as the
   position-aware truth. Each trade row creates one ENTRY payload and one EXIT
   payload.
3. ENTRY payloads use `bar_time_utc = entry_time - 1h` as the signal bar,
   `stop_loss = stop`, `take_profit = null`, and the trade `entry_time` as the
   intended fill time. EXIT payloads use `bar_time_utc = exit_time` and carry
   the trade `reason`.
4. It writes `expected_signals.jsonl` and `emitter_manifest.json`.
5. `local_receiver.py` accepts only `environment: "paper"` during this
   SYSTEM_TEST_ONLY phase and rejects `live` and `testnet`.
6. `local_receiver.py` converts accepted entries/exits into deterministic fake
   fills with no slippage modeling and no broker semantics.
7. `reconciler.py` compares EXPECTED, RECEIVED, and FILLED ledgers and writes a
   report with explicit orphan rows.
8. `QL_ALPHA_LINK_8EMA_1H_signals.csv` is not the source of EXPECTED entries in
   V1 because it contains signal-bar candidates, including in-position signals
   that the engine did not trade. It is used only for the entry-while-open drill
   with explained disposition `rejected(entry_while_open)`.
9. Failure drills are implemented as focused tests first. Standalone drill
   generation is V1.1+.

## Task 0: Approval And Preflight

**Files:**
- Read:
  `AGENTS.md`,
  `MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md`,
  `MTC_COMMAND_CENTER/_AI_MEMORY/AI_RULES.md`,
  `MTC_COMMAND_CENTER/_AI_MEMORY/DO_NOT_TOUCH.md`,
  `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/EXECUTION_ARCHITECTURE_DECISION.md`,
  `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/VERTICAL_SLICE_SCOPE.md`,
  `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/PAPER_RECONCILIATION_PROTOCOL.md`,
  `MTC_COMMAND_CENTER/_AI_MEMORY/LIVE_TRADING_GATE.md`
- Modify: none.

- [ ] **Step 0.1: Obtain implementation approval**

  Required approval sentence before any implementation:

  `I approve implementation of the SYSTEM_TEST_ONLY local vertical slice plan for STG002. No schemas, no broker, no TradingView, no WunderTrading, no testnet, no real money.`

- [ ] **Step 0.2: Confirm protected-path cleanliness**

  Run:

  ```powershell
  git status --short -- MTC_COMMAND_CENTER\06_SCHEMAS MTC_COMMAND_CENTER\01_PINE MTC_COMMAND_CENTER\02_MTC_BACKTEST MTC_COMMAND_CENTER\07_ADAPTERS
  ```

  Expected: no new implementation changes from this slice in those paths.

- [ ] **Step 0.3: Confirm STG002 source artifacts exist**

  Run:

  ```powershell
  Test-Path MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG002_ql_alpha_link_8ema_1h\QL_ALPHA_LINK_8EMA_1H_signals.csv
  Test-Path MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG002_ql_alpha_link_8ema_1h\QL_ALPHA_LINK_8EMA_1H_trades.csv
  Test-Path MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG002_ql_alpha_link_8ema_1h\producer_spec.json
  ```

  Expected: all three commands print `True`.

- [ ] **Step 0.4: Confirm test runner availability**

  Run:

  ```powershell
  python -m pytest --version
  ```

  Expected: pytest version prints and exit code is 0. If this fails, write the
  vertical-slice tests so they are unittest-compatible and use:

  ```powershell
  python -m unittest MTC_COMMAND_CENTER\03_QUANTLENS\tools\tests\test_vertical_slice_contracts.py
  ```

  Apply the same unittest fallback to every later focused test command.

- [ ] **Step 0.5: Confirm system-test output root is not research-scanned**

  Run:

  ```powershell
  git check-ignore -q MTC_COMMAND_CENTER\03_QUANTLENS\system_test\_probe
  if ($LASTEXITCODE -eq 0) { "ignored" } else { "not ignored"; exit 1 }
  ```

  Expected: `ignored`. If it is not ignored, stop and ask Baris for approval to
  add a `.gitignore` rule before the first local run. Do not write outputs under
  `03_QUANTLENS/research/`.

## Task 1: Package Skeleton And Constants

**Files:**
- Create:
  `MTC_COMMAND_CENTER/03_QUANTLENS/tools/vertical_slice/__init__.py`
- Create:
  `MTC_COMMAND_CENTER/03_QUANTLENS/tools/vertical_slice/constants.py`
- Test:
  `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_vertical_slice_contracts.py`

- [ ] **Step 1.1: Write tests for immutable route constants**

  The test must assert:

  - banner equals `SYSTEM_TEST_ONLY / NOT STRATEGY_APPROVED / NO REAL MONEY`
  - benchmark candidate id equals `QL_ALPHA_LINK_8EMA_1H`
  - symbol/timeframe equals `LINKUSDT` / `1h`
  - allowed runtime environment for the core slice is exactly `paper`
  - forbidden labels include `live`, `testnet`, `broker`, `TradingView`, and
    `WunderTrading`

- [ ] **Step 1.2: Run the focused test and verify it fails before constants exist**

  Run:

  ```powershell
  python -m pytest MTC_COMMAND_CENTER\03_QUANTLENS\tools\tests\test_vertical_slice_contracts.py -q
  ```

  Expected: failure caused by missing `vertical_slice` package or missing
  constants.

- [ ] **Step 1.3: Add the minimal package and constants**

  Keep this file declarative only. It must not import engine, dashboard,
  broker, network, Pine, or adapter modules. It must not embed any default auth
  token value, including `"test-token"` or other placeholders; tests generate
  synthetic tokens per run.

- [ ] **Step 1.4: Re-run the focused test**

  Run:

  ```powershell
  python -m pytest MTC_COMMAND_CENTER\03_QUANTLENS\tools\tests\test_vertical_slice_contracts.py -q
  ```

  Expected: all tests in that file pass.

## Task 2: Appendix Schema Validation In Code

**Files:**
- Create:
  `MTC_COMMAND_CENTER/03_QUANTLENS/tools/vertical_slice/contracts.py`
- Modify:
  `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_vertical_slice_contracts.py`

- [ ] **Step 2.1: Write validation tests**

  Tests must prove:

  - a complete ENTRY payload validates
  - `environment: "live"` is rejected
  - `environment: "testnet"` is rejected in the core slice
  - missing `idempotency_key` is rejected
  - malformed checksum is rejected
  - extra unrecognized fields are rejected
  - `auth_token` is required at validation time but is redacted before reports
  - timestamp inputs ending with `+0000`, `+00:00`, and `Z` canonicalize to
    `YYYY-MM-DDTHH:MM:SSZ` and produce the same `signal_id`
  - `action: ENTRY` requires `current_position_intent: FLAT_TO_LONG` or
    `FLAT_TO_SHORT`
  - `action: EXIT` requires `current_position_intent: LONG_TO_FLAT` or
    `SHORT_TO_FLAT`

- [ ] **Step 2.2: Implement validation without writing `06_SCHEMAS`**

  `contracts.py` may hold an in-code schema dictionary copied from
  `PAPER_RECONCILIATION_PROTOCOL.md` Appendix A. It must not create, modify, or
  depend on `MTC_COMMAND_CENTER/06_SCHEMAS/`.

- [ ] **Step 2.3: Re-run contract tests**

  Run:

  ```powershell
  python -m pytest MTC_COMMAND_CENTER\03_QUANTLENS\tools\tests\test_vertical_slice_contracts.py -q
  ```

  Expected: all contract tests pass.

## Task 3: STG002 Replay Emitter

**Files:**
- Create:
  `MTC_COMMAND_CENTER/03_QUANTLENS/tools/vertical_slice/stg002_replay_emitter.py`
- Test:
  `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_vertical_slice_replay.py`

- [ ] **Step 3.1: Write tests using temporary CSV fixtures**

  The tests must use small temp files with these exact signal columns:

  `timestamp_utc,open,high,low,close,atr14,ema8,long_entry,stop_at_signal`

  The tests must use small temp files with these exact trade columns:

  `entry_time,exit_time,entry,stop,exit,reason,ret_net_pct,R`

  Required assertions:

  - each `trades.csv` row produces exactly one ENTRY payload and one EXIT
    payload
  - ENTRY `bar_time_utc` is `entry_time - 1h`, normalized to
    `YYYY-MM-DDTHH:MM:SSZ`
  - ENTRY `stop_loss` maps from trade column `stop`
  - EXIT `bar_time_utc` maps from trade column `exit_time`
  - EXIT payload carries the trade column `reason`
  - `take_profit` is null because STG002 uses trailing exit logic
  - each payload has deterministic `signal_id`, `idempotency_key`, and
    checksum
  - every payload carries the required SYSTEM_TEST_ONLY banner in its sidecar
    manifest or report metadata
  - `emitter_manifest.json` includes `benchmark_role: SYSTEM_TEST_ONLY`,
    `promotable: false`, `strategy_approval_status: NOT_APPROVED`, and a note
    that the current library-wide robust result is `robust_final = 0`

- [ ] **Step 3.2: Implement trades-driven replay emission**

  The emitter must derive EXPECTED ENTRY/EXIT payloads from `trades.csv`. It
  may read `signals.csv` only for the suppressed-signal drill. It must not call
  `mega_walk_forward.py`, `build_signals`, backtest runners, optimizers, Pine,
  parity, broker, or network code.

- [ ] **Step 3.3: Re-run replay tests**

  Run:

  ```powershell
  python -m pytest MTC_COMMAND_CENTER\03_QUANTLENS\tools\tests\test_vertical_slice_replay.py -q
  ```

  Expected: all replay tests pass.

## Task 4: Local Receiver

**Files:**
- Create:
  `MTC_COMMAND_CENTER/03_QUANTLENS/tools/vertical_slice/local_receiver.py`
- Test:
  `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_vertical_slice_receiver.py`

- [ ] **Step 4.1: Write receiver tests**

  Tests must prove:

  - valid payload becomes one RECEIVED row with disposition `accepted`
  - duplicate `idempotency_key` becomes `duplicate_dropped`
  - wrong auth token is rejected
  - wrong checksum is rejected
  - `environment: "live"` is rejected loudly
  - EXIT while flat is rejected with reason `exit_with_no_position`
  - ENTRY while already long is rejected with reason `entry_while_open`
  - accepted ENTRY creates one fake fill, opens one local simulated position,
    and writes `simulated: true`
  - accepted EXIT closes that local simulated position and writes
    `simulated: true`
  - duplicate accepted rows do not create duplicate fills
  - rejected rows never create fills

- [ ] **Step 4.2: Implement receiver as pure local logic first**

  Use function-level receiver logic that takes payloads and a local state
  object. A persistent localhost HTTP wrapper can be added only after these
  pure tests pass and Baris approves running a local server. The first
  implementation should not start a server by default.

  The receiver owns deterministic fake-fill state in V1. Do not create a
  separate `simulated_fills.py` module in the first implementation.

- [ ] **Step 4.3: Re-run receiver tests**

  Run:

  ```powershell
  python -m pytest MTC_COMMAND_CENTER\03_QUANTLENS\tools\tests\test_vertical_slice_receiver.py -q
  ```

  Expected: all receiver tests pass.

## Task 5: V1 Scope Cut - No Separate Simulated Fill Module

**Files:**
- Create: none.
- Modify: none.

- [ ] **Step 5.1: Keep fill behavior inside Task 4**

  The first implementation must not create
  `MTC_COMMAND_CENTER/03_QUANTLENS/tools/vertical_slice/simulated_fills.py`.
  The fill-state tests listed in Task 4 are the V1 acceptance criteria.

- [ ] **Step 5.2: Reconsider only after Fable/Baris approval**

  A separate fill module is allowed only if the receiver file becomes too large
  or unclear during implementation review. It remains prohibited from importing
  `ccxt`, exchange clients, adapter modules, or broker code.

## Task 6: Reconciler

**Files:**
- Create:
  `MTC_COMMAND_CENTER/03_QUANTLENS/tools/vertical_slice/reconciler.py`
- Test:
  `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_vertical_slice_reconciler.py`

- [ ] **Step 6.1: Write reconciliation tests**

  Tests must prove:

  - matching EXPECTED, RECEIVED, and FILLED ledgers produce zero unexplained
    orphan rows
  - missing RECEIVED row is reported as EXPECTED-not-RECEIVED
  - accepted RECEIVED row without fill is reported as RECEIVED-not-FILLED
  - unknown RECEIVED row is reported as RECEIVED-not-EXPECTED
  - any unexplained count greater than zero sets status `HALT`
  - report includes the SYSTEM_TEST_ONLY banner

- [ ] **Step 6.2: Implement three-ledger diff**

  The reconciler must read only local JSONL/JSON files from a run directory and
  write a Markdown report plus machine-readable summary. It must not write to
  dashboard, scorecard, promotion, or backtest artifact directories.

- [ ] **Step 6.3: Re-run reconciliation tests**

  Run:

  ```powershell
  python -m pytest MTC_COMMAND_CENTER\03_QUANTLENS\tools\tests\test_vertical_slice_reconciler.py -q
  ```

  Expected: all reconciliation tests pass.

## Task 7: Induced-Failure Drills

**Files:**
- Create: none in V1.
- Modify:
  `MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_vertical_slice_reconciler.py`

- [ ] **Step 7.1: Write drill tests**

  Tests must cover:

  - D1 duplicate signal
  - D2 dropped signal
  - D3 exit-with-no-position
  - D4 wrong environment
  - D5 malformed payload
  - D8 out-of-order delivery: EXIT before ENTRY
  - D9 entry-while-open using suppressed in-position signal candidates from
    `signals.csv`
  - D10 semantic sanity bounds: checksum-valid but impossible payload values,
    such as negative price or long ENTRY with `stop_loss >= entry`

  D6 receiver-down and D7 restart-mid-state stay extension-leg documentation
  only until a separately approved localhost server or testnet leg exists.

- [ ] **Step 7.2: Implement drills as tests first**

  Each drill test must create isolated input rows under a temp run directory and
  assert the expected receiver/reconciler disposition. Do not create
  `drills.py` in V1 unless Baris separately approves a standalone drill
  generator. No drill may call network, broker, exchange, TradingView,
  WunderTrading, testnet, Pine, or parity code.

- [ ] **Step 7.3: Re-run drill tests**

  Run:

  ```powershell
  python -m pytest MTC_COMMAND_CENTER\03_QUANTLENS\tools\tests\test_vertical_slice_reconciler.py -q
  ```

  Expected: all reconciliation and drill tests pass.

## Task 8: V1.1 Deferred - Thin CLI Wrapper

**Files:**
- Create: none in V1.
- Test: none in V1.

- [ ] **Step 8.1: Do not implement CLI in V1**

  The first implementation uses tests and, after separate run approval, a
  single importable entry function. Do not create
  `MTC_COMMAND_CENTER/03_QUANTLENS/tools/vertical_slice/cli.py` in V1.

- [ ] **Step 8.2: Carry CLI constraints into V1.1 backlog**

  If a later CLI is approved, it must support only local commands such as
  `emit-replay`, `receive-file`, `reconcile`, and `run-drills`, and it must
  reject:

  - `--environment live`
  - `--environment testnet`
  - any output directory under `05_BACKTEST_RESULTS`
  - any output directory under `03_QUANTLENS/research/`
  - any output directory outside `03_QUANTLENS/system_test/`

- [ ] **Step 8.3: Re-run vertical-slice tests without CLI**

  Run:

  ```powershell
  python -m pytest MTC_COMMAND_CENTER\03_QUANTLENS\tools\tests\test_vertical_slice_contracts.py MTC_COMMAND_CENTER\03_QUANTLENS\tools\tests\test_vertical_slice_replay.py MTC_COMMAND_CENTER\03_QUANTLENS\tools\tests\test_vertical_slice_receiver.py MTC_COMMAND_CENTER\03_QUANTLENS\tools\tests\test_vertical_slice_reconciler.py -q
  ```

  Expected: all vertical-slice tests pass.

## Task 9: First Approved Local Run

**Files:**
- Runtime output only:
  `MTC_COMMAND_CENTER/03_QUANTLENS/system_test/<run_id>/`
- Modify: none outside the runtime output directory.

- [ ] **Step 9.1: Ask Baris before the first local run**

  Required approval sentence:

  `I approve one local SYSTEM_TEST_ONLY replay run for STG002. No broker, no TradingView, no WunderTrading, no testnet, no real money.`

- [ ] **Step 9.2: Run the local replay slice through the approved entry function**

  Use the implemented entry function only after approval. It must point to the
  STG002 CSV artifacts and an output directory under
  `03_QUANTLENS/system_test/`.

  Expected event counts for the first real STG002 replay:

  - EXPECTED payloads: 888 total
  - ENTRY payloads: 444
  - EXIT payloads: 444
  - FILLED lifecycle rows: 444 round trips
  - suppressed-signal drill rows: explained rejections only
  - `UNEXPLAINED`: 0

- [ ] **Step 9.3: Verify the run artifacts**

  Confirm the run directory contains:

  - `emitter_manifest.json`
  - `expected_signals.jsonl`
  - `received_signals.jsonl`
  - `simulated_fills.jsonl`
  - `reconciliation_summary.json`
  - `reconciliation_report.md`
  - drill result files or test evidence for D1 through D5 and D8 through D10

  Confirm every report contains:

  `SYSTEM_TEST_ONLY / NOT STRATEGY_APPROVED / NO REAL MONEY`

  Confirm no file was created under:

  - `MTC_COMMAND_CENTER/03_QUANTLENS/research/`
  - `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/`

## Task 10: Final Safety Verification And Handoff

**Files:**
- Modify after successful implementation:
  `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md`
- Modify after successful implementation:
  `MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md`
- Modify after successful implementation:
  `MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOG.md`
- Modify after successful implementation:
  `MTC_COMMAND_CENTER/_AI_MEMORY/ACTIVE_FILES.md`

- [ ] **Step 10.1: Run protected path status check**

  Run:

  ```powershell
  git status --short -- MTC_COMMAND_CENTER\06_SCHEMAS MTC_COMMAND_CENTER\01_PINE MTC_COMMAND_CENTER\02_MTC_BACKTEST MTC_COMMAND_CENTER\07_ADAPTERS
  ```

  Expected: no slice implementation changes in those paths.

- [ ] **Step 10.2: Run static and focused test verification**

  Run:

  ```powershell
  python -m py_compile MTC_COMMAND_CENTER\03_QUANTLENS\tools\vertical_slice\constants.py MTC_COMMAND_CENTER\03_QUANTLENS\tools\vertical_slice\contracts.py MTC_COMMAND_CENTER\03_QUANTLENS\tools\vertical_slice\stg002_replay_emitter.py MTC_COMMAND_CENTER\03_QUANTLENS\tools\vertical_slice\local_receiver.py MTC_COMMAND_CENTER\03_QUANTLENS\tools\vertical_slice\reconciler.py
  python -m pytest MTC_COMMAND_CENTER\03_QUANTLENS\tools\tests\test_vertical_slice_contracts.py MTC_COMMAND_CENTER\03_QUANTLENS\tools\tests\test_vertical_slice_replay.py MTC_COMMAND_CENTER\03_QUANTLENS\tools\tests\test_vertical_slice_receiver.py MTC_COMMAND_CENTER\03_QUANTLENS\tools\tests\test_vertical_slice_reconciler.py -q
  ```

  Expected: compile succeeds and all focused tests pass.

  If pytest is unavailable per Task 0.4, run the unittest-compatible focused
  test command documented by the implementer instead.

- [ ] **Step 10.3: Update AI-memory routing**

  Update the four `_AI_MEMORY` routing files with:

  - exact files changed
  - exact verification commands and results
  - whether any local replay run was performed
  - explicit statement that no real money, broker, testnet, TradingView, or
    WunderTrading path was touched

- [ ] **Step 10.4: Stop before extension legs**

  Do not proceed to TradingView alerts, WunderTrading demo, Binance testnet,
  dashboard execution UI, schema promotion, or engine-forward signal generation
  without a separate Baris approval gate.

## Self-Review Checklist

- The plan implements only the local core slice.
- STG002 is used only as a crash-test dummy.
- The replay-first approach avoids strategy logic and engine mutation.
- No planned file is under `06_SCHEMAS`, Pine, `MTC_V2`, parity,
  `02_MTC_BACKTEST`, or `07_ADAPTERS`.
- No planned output feeds scorecards, promotion, `05_BACKTEST_RESULTS`,
  `top_results.json`, or `backtest_profile_result.json`.
- No planned output is written under `03_QUANTLENS/research/` or registered in
  `RESEARCH_RUN_REGISTRY.json`.
- Failure drills D1 through D5 and D8 through D10 are included; D6 and D7
  remain blocked until a separately approved server/testnet leg exists.
- V1 intentionally excludes CLI, standalone drill generator, and separate fill
  simulator modules.
- Implementation remains blocked until Baris gives a separate implementation
  approval.
