# Fable Audit Prompt - STG002 SYSTEM_TEST_ONLY Vertical Slice Plan

You are Claude Fable auditing a draft implementation plan for the MTC Command
Center repo.

Repo: `C:\LAB\Tradingview_LAB_CLEAN`

Audit target:

`MTC_COMMAND_CENTER\00_AGENT_PROTOCOLS\SYSTEM_TEST_VERTICAL_SLICE_IMPLEMENTATION_PLAN.md`

## Core Context

Baris approved Gate V0 planning only and selected
`STG002 / QL_ALPHA_LINK_8EMA_1H` as the benchmark for a SYSTEM_TEST_ONLY
vertical slice.

This is not strategy approval. This is not paper-trading approval. This is not
live-trading approval. This is not promotion evidence. It must remain:

`SYSTEM_TEST_ONLY / NOT STRATEGY_APPROVED / NO REAL MONEY`

The intended first slice is local and fake-money only:

1. replay STG002 signal/trade artifacts into expected signal payloads
2. validate those payloads through a local receiver
3. simulate local fills without broker semantics
4. reconcile EXPECTED / RECEIVED / FILLED ledgers
5. run induced-failure drills

No code has been approved yet.

## Required Read Order

1. `AGENTS.md`
2. `MTC_COMMAND_CENTER\_AI_MEMORY\START_HERE.md`
3. `MTC_COMMAND_CENTER\_AI_MEMORY\AI_RULES.md`
4. `MTC_COMMAND_CENTER\_AI_MEMORY\DO_NOT_TOUCH.md`
5. `MTC_COMMAND_CENTER\00_AGENT_PROTOCOLS\EXECUTION_ARCHITECTURE_DECISION.md`
6. `MTC_COMMAND_CENTER\00_AGENT_PROTOCOLS\VERTICAL_SLICE_SCOPE.md`
7. `MTC_COMMAND_CENTER\00_AGENT_PROTOCOLS\PAPER_RECONCILIATION_PROTOCOL.md`
8. `MTC_COMMAND_CENTER\_AI_MEMORY\LIVE_TRADING_GATE.md`
9. `MTC_COMMAND_CENTER\_AI_MEMORY\DECISIONS.md`
10. `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md`
11. `MTC_COMMAND_CENTER\_AI_MEMORY\NEXT_STEPS.md`
12. `MTC_COMMAND_CENTER\00_AGENT_PROTOCOLS\SYSTEM_TEST_VERTICAL_SLICE_IMPLEMENTATION_PLAN.md`

Optional spot-check source files:

- `MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG002_ql_alpha_link_8ema_1h\producer_spec.json`
- `MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG002_ql_alpha_link_8ema_1h\QL_ALPHA_LINK_8EMA_1H_signals.csv`
- `MTC_COMMAND_CENTER\03_QUANTLENS\strategies\STG002_ql_alpha_link_8ema_1h\QL_ALPHA_LINK_8EMA_1H_trades.csv`

Do not read or edit Pine source unless you find a specific plan claim that
requires verifying Pine. The plan should not depend on Pine.

## Hard Rules

- Audit only. Do not implement anything.
- Do not edit files.
- Do not run backtests, optimizations, servers, testnet, broker, TradingView,
  WunderTrading, Pine parity, or live/paper execution.
- Do not write schemas.
- Do not ask for or inspect secrets.
- Treat any planned touch to `06_SCHEMAS`, Pine, `MTC_V2`, parity,
  `02_MTC_BACKTEST`, `07_ADAPTERS`, broker/exchange/testnet, TradingView, or
  WunderTrading as a likely blocker unless it is explicitly approval-gated and
  out of the first implementation.

## Audit Questions

### A. Scope And Safety

1. Does the plan stay inside the approved Gate V0 planning route?
2. Does it clearly require separate Baris approval before implementation?
3. Does it prevent strategy-quality, paper-readiness, live-readiness, promotion,
   or profitability contamination?
4. Are all artifacts clearly marked SYSTEM_TEST_ONLY / NOT STRATEGY_APPROVED /
   NO REAL MONEY?

### B. Architecture Choice

5. Is replay-first the safest first implementation, or should the first slice
   call the Python engine directly? Give a clear recommendation.
6. If replay-first is accepted, does the plan preserve a clean later path to
   engine-forward emission without hiding that future risk?
7. Does the plan correctly keep Python as source of truth and avoid treating
   TradingView, Pine, WunderTrading, or a broker bridge as the production path?

### C. STG002 Benchmark Fit

8. Is STG002 suitable as a crash-test dummy for plumbing based on the repo
   evidence?
9. Are the plan's assumptions about STG002 CSV columns and producer metadata
   accurate?
10. Does using STG002 risk implying that it is strategy-approved? If yes, how
    should the wording be tightened?

### D. Signal Contract And Idempotency

11. Are `signal_id`, `idempotency_key`, checksum, environment, auth token, and
    current-position-intent responsibilities specific enough?
12. Does the plan reject `live` and `testnet` in the core slice?
13. Does it avoid committing secrets while still making auth behavior testable?
14. Are the planned validation tests strong enough to prevent malformed payloads
    from reaching the receiver ledger?

### E. Receiver, Fill Simulation, And Reconciliation

15. Does the local receiver design test the right behavior without becoming a
    hidden production executor?
16. Is the fake fill simulator clearly separated from broker/exchange behavior?
17. Is the three-ledger reconciliation model sufficient to catch dropped,
    duplicate, orphan, and unexplained events?
18. Are halt conditions explicit enough when `UNEXPLAINED > 0`?

### F. Failure Drills

19. Are D1 through D5 implemented at the correct stage?
20. Is it correct to defer D6 receiver-down and D7 restart-mid-state until a
    separate localhost-server or testnet approval exists?
21. Are any important failure drills missing for a fake-money local slice?

### G. File Boundaries

22. Are the planned file paths appropriate for this repo?
23. Should runtime outputs live under
    `03_QUANTLENS/research/system_test_vertical_slice/`, or is there a safer
    location?
24. Does the plan accidentally require dashboard, scorecard, registry, schema,
    protected trading, or adapter writes?

### H. Tests And Verification

25. Are the proposed tests sufficient and not overbroad?
26. Are the proposed verification commands realistic for this repo?
27. What exact additional tests would you require before allowing one local
    replay run?

### I. What To Cut

28. Is the plan too large for a first implementation?
29. Which tasks should be cut or split so the first implementation is smaller
    and safer?
30. What is the minimum acceptable V1 slice that still proves meaningful
    plumbing?

## Output Required

Write a concise but ruthless audit report with this structure:

1. **Verdict**
   Use one:
   - `SAFE TO IMPLEMENT AFTER BARIS APPROVAL`
   - `SAFE ONLY AFTER PLAN FIXES`
   - `UNSAFE - DO NOT IMPLEMENT`

2. **Top Findings**
   Findings first, ordered by severity. Use:
   `severity - file:line - issue - required fix`

3. **Recommended Plan Changes**
   Give concrete edits to the plan. Do not rewrite the whole plan unless it is
   structurally wrong.

4. **Minimum Safe First Slice**
   State the smallest implementation Fable would allow after fixes.

5. **Explicit Non-Approvals**
   Confirm this audit does not approve real money, live trading, paper broker,
   testnet, TradingView, WunderTrading, Pine edits, parity edits, schema writes,
   or strategy promotion.

If you find no blockers, still list residual risks and the first three things
Codex should verify after implementation.

