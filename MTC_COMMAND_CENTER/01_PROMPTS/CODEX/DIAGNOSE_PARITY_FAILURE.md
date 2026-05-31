# Codex Task Template: Diagnose Parity Failure

## Purpose

Investigate assigned parity failures and produce a diagnostic report.

## Inputs

- Case IDs
- Latest parity result file
- TradingView export path
- Python/PineTS output references

## Workflow

1. Read source outputs without editing them.
2. Compare failure signatures per case.
3. Group repeated failures.
4. Identify likely cause, evidence, and next action.
5. Mark missing data as `WAITING_FOR_USER`.
6. Update parity status only with evidence-backed facts.

## Output

Write a diagnostic report under `04_REPORTS/diagnostics` and update task history.
