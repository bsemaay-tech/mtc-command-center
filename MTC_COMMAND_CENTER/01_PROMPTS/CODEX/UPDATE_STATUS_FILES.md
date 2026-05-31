# Codex Task Template: Update Status Files

## Purpose

Update MCC status JSON after an assigned task completes, fails, or waits for user input.

## Required Checks

- Preserve valid JSON.
- Update only relevant fields.
- Do not invent metrics or timestamps.
- Link detailed findings to report paths.
- Keep dashboard-facing summaries concise.

## Files

- `03_STATUS/CURRENT_STATUS.json`
- `03_STATUS/PARITY_STATUS.json`
- `03_STATUS/BACKTEST_STATUS.json`
- `02_TASKS/TASK_HISTORY.json`

## Safety

If the source report is missing, do not fabricate status. Mark the task as blocked and request the missing artifact.
