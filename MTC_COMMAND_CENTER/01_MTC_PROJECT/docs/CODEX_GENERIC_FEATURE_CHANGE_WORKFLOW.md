# Codex Generic Feature Change Workflow

Common rule: no feature is ready until its contract-specific acceptance profile passes or the mismatch is explicitly classified and accepted by the user.

## Required Flow

1. Scaffold the feature contract and isolated adapters.
2. Implement the feature in Python and Pine draft/adapter form.
3. Emit Python feature trace.
4. Emit PineTS feature trace.
5. Compare traces with the contract acceptance profile.
6. Integrate into canonical `01_PINE/MTC_V2.pine` and production Python only after feature-level parity passes.
7. Run selected local FAST_SUITE parity checks.
8. Use TradingView export only as final release audit.

## Examples

### Replace Supertrend with Range Filter

Use `feature_type: signal_producer`.

Required workflow: scaffold feature, create contract, implement isolated PineTS adapter, implement Python feature, emit traces, run L0/L1/L2/L3, integrate only after pass.

### Add ATR-based stop loss

Use `feature_type: stop_loss`.

Required workflow: contract, Python SL implementation, Pine SL implementation draft/adapter, trace `initial_sl`, `active_sl`, `sl_hit`, `exit_reason`, run stop_loss acceptance, integrate only after pass.

### Add multi-R partial TP

Use `feature_type: take_profit`.

Required workflow: trace TP prices, partial qty, remaining qty, TP fill event, then run take_profit acceptance.

### Add ADX filter

Use `feature_type: entry_filter`.

Required workflow: trace ADX value, allowed/blocked booleans, blocked_reason, then run filter_gate acceptance.

### Change risk sizing

Use `feature_type: position_sizing`.

Required workflow: trace equity source, risk amount, qty, notional, leverage, then run position_sizing acceptance.

### Change WunderTrading alert JSON

Use `feature_type: alert_payload`.

Required workflow: trace event_id, payload JSON, schema validation, idempotency key, then run alert_payload acceptance.

## Codex Must Never

- Modify canonical `01_PINE/MTC_V2.pine` before feature parity passes.
- Change production Python behavior before the isolated contract is accepted.
- Hide mismatch by increasing tolerance.
- Fake oracle output.
- Use TradingView export as the normal development loop.
- Place live orders or use API keys.

## Reports

Every feature parity result must produce `FEATURE_PARITY_REPORT.md` and `FEATURE_PARITY_REPORT.json` with exact command, data hash, config hash, code hash, output paths, first divergence, missing columns, and verdict.

## NOT_COMPARABLE Handling

Return a structured `FEATURE_TRACE_NOT_COMPARABLE`, `PYTHON_TRACE_UNAVAILABLE`, `PINETS_UNAVAILABLE`, or `TRACE_CONTRACT_INCOMPLETE` report. Continue without claiming ready.

## Independent Reference Oracle Layer

For small new or changed features, Codex should add an independent reference oracle when practical.

- The reference oracle is a pure-Python expected-value calculator.
- It must not import the production implementation it checks.
- It compares independent expected trace vs Python feature trace vs PineTS feature trace.
- It is feature-level only, not a full backtest engine.
- It does not replace Python lifecycle ownership, PineTS L0-L3 trace parity, or TradingView final audit.
- PyneCore, backtesting.py, backtrader, FinRL, and vectorbt are not part of the required local loop.

## When TradingView Export Is Needed

TradingView export is still required for final release audit after local contract-level and selected FAST_SUITE parity checks pass.
