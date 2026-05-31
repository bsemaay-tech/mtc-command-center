---
name: quantlens-python-experiment-runner
description: Use when moving a READY_FOR_PYTHON_PROTOTYPE QuantLens candidate through isolated prototype planning and bounded validation for MTC_V2.
---

# QuantLens Python Experiment Runner

## Purpose

Move a `READY_FOR_PYTHON_PROTOTYPE` candidate into isolated Python prototype and bounded validation without changing production strategy behavior.

## When to use

Use after candidate intake when registry status is `READY_FOR_PYTHON_PROTOTYPE`.

## Inputs

- Candidate ID or registry selection.
- Candidate metadata and experiment plan.
- Available data bundle manifest and symbol/timeframe availability.

## Outputs

- Results under `06_QUANTLENS_LAB/05_BACKTEST_RESULTS/<CandidateID>`.
- Backtest config, symbol results, walk-forward results, robustness summary, pass/fail decision, and next action.
- Registry status update.

## Safety rules

- Never modify `01_PINE/MTC_V2.pine`.
- Never modify production runner behavior.
- Keep prototypes isolated.
- Use bounded validation before any broad search.
- Record data source, dataset_id, timeframe, symbols, commission, and slippage assumptions.

## Backtest method assumptions

Prototype first, then bounded multi-symbol validation. Net profit alone is not enough. Low trade count is unreliable.

## Walk-forward expectations

Train, validation, and OOS/test behavior must be reported separately. Weak OOS or unstable splits block promotion.

## Pass/fail criteria

Require enough trades, acceptable drawdown, reasonable PF, multi-symbol coverage, OOS behavior, and parameter sensitivity checks.

## Registry status updates

Use `BACKTEST_FAILED`, `BACKTEST_PROMISING`, `BACKTEST_PASSED`, or `NEEDS_MORE_INFO`.
