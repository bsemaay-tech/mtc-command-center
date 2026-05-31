# Codex Task Template: Run Backtest Task

## Purpose

Run an assigned MTC_v2 backtest task and write MCC-readable outputs.

## Preconditions

- Strategy or case input is defined.
- Required market data exists.
- Command is documented or provided by the task.
- Task explicitly permits local backtest execution.

## Workflow

1. Read task scope and safety rules.
2. Verify inputs without modifying them.
3. Prepare a report path.
4. Run the approved backtest command.
5. Capture summary metrics and failures.
6. Update `03_STATUS/BACKTEST_STATUS.json`.
7. Add a history entry.

## Safety

Do not patch the Python engine during a run task. Diagnose separately if failures appear.
