# User Manual Draft

MTC Command Center is intended to let the user supervise the MTC_v2 research workflow without writing code.

## What The User Watches

- Current project phase
- AI task queue
- Parity status
- Backtest status
- Strategy intake state
- Pine draft and review state
- Reports and diagnostics
- Data health warnings

## How To Give AI Work

Create or assign a task with a clear task ID, scope, inputs, expected output, and safety boundaries. The AI should read the task queue, perform only the assigned task, write a report, and update status/history files.

## When The User Provides Inputs

- Provide YouTube transcripts for strategy intake.
- Provide TradingView exports for parity and comparison tasks.
- Observe TradingView compile results and report the exact message.
- Enter API keys or tokens only through approved future secret handling.
- Approve large changes before implementation.

## What The User Should Not Need To Do

The user should not need to write MCC code, manually edit generated status files, or inspect raw engine logs unless a diagnostic report requests a specific manual check.
