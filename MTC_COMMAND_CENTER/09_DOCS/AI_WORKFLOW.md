# AI Workflow

## Shared Startup

All AI workers read `MTC Command Center ARCHITECTURE.md`, `CURRENT_STATUS.md`, `AI_OPERATING_RULES.md`, and `02_TASKS/TASK_QUEUE.json` before work.

## Codex

Codex handles repo automation, local file inspection, Python/backtest/parity tasks when approved, JSON status updates, and diagnostic reports.

## Claude

Claude handles Pine builder tasks, Pine review, documentation refinement, and prompt improvements.

## Gemini Antigravity

Gemini handles research, internet strategy review when explicitly assigned, transcript intake, and strategy discovery notes.

## Task Lifecycle

Tasks move from `TODO` to `IN_PROGRESS`, then `DONE`, `FAILED`, `BLOCKED`, or `WAITING_FOR_USER`. Each completed, failed, or blocked task should create or reference a report and update history.

## Handoff

Each AI worker should leave enough context for the next worker to resume safely: task ID, inputs reviewed, outputs written, blockers, and next action.
