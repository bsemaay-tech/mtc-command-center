# Codex Task Template: Run Parity Task

## Purpose

Run an explicitly assigned parity comparison task and update MCC status/report files.

## Preconditions

- User or task queue provides case IDs.
- TradingView exports are present.
- Parity tooling path is known.
- Task scope explicitly allows reading parity inputs.

## Workflow

1. Read architecture and operating rules.
2. Confirm assigned case list.
3. Create a report manifest before running.
4. Run only approved local parity commands.
5. Continue on individual case failure.
6. Write per-case diagnostic notes.
7. Update `03_STATUS/PARITY_STATUS.json`.
8. Append task history.

## Safety

Do not edit PineTS/parity engine files or TradingView export files unless explicitly assigned.
