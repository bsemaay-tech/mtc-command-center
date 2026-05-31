# Independent Reference Oracle Policy

## Purpose

The Independent Reference Oracle is a small feature-level expected-value calculator used to cross-check Python and PineTS feature traces.

It compares:

- independent expected trace
- Python feature trace
- PineTS feature trace

## Roles

- PineTS remains the local Pine-side `L0`-`L3` oracle.
- Python MTC engine remains the local lifecycle owner.
- Independent reference oracle checks feature-level expected values when practical.
- TradingView export remains the final release audit.

## Rules

- The reference oracle must not import the production implementation it checks.
- The reference oracle is not a full backtest engine.
- The reference oracle is not a replacement for TradingView export.
- Existing validated MTC_V2 feature families are not re-tested as new POCs.
- Reference outputs must be generated from explicit inputs and must not be faked.
- Tolerances must not be increased to hide mismatches.

## Deferred Tools

- PyneCore is deferred and not installed in this phase.
- backtesting.py is deferred and not installed in this phase.
- backtrader is deferred and not installed in this phase.
- FinRL / FinRL-X is deferred and not relevant to the MTC parity factory now.
- vectorbt is optional future approximation only and is not implemented in this phase.

## When To Use

Use a reference oracle for new or changed features when the formula/state machine is small enough to implement independently without importing production code.

Do not use this layer to claim:

- full strategy lifecycle parity
- TradingView parity
- release readiness

Those claims require the appropriate lifecycle outputs and final TradingView audit.
