# AI Operating Rules

These rules apply to Codex, Claude, Gemini Antigravity, and any future AI worker using MCC.

## Required Workflow

- Use a report-first workflow: inspect, write findings, then update status files.
- Start read-only: prefer reading files and generating reports before any implementation.
- Do not directly patch MTC_v2 core files.
- Do not modify `MTC_V2.pine` unless a future explicit task authorizes it.
- Do not touch PineTS/parity pipelines unless explicitly assigned.
- Do not perform live trading.
- Do not add live webhooks, WunderTrading, or TradersPost integrations in foundation work.
- Do not install packages unless explicitly approved.
- Do not store secrets, API keys, tokens, passwords, or account identifiers in files.
- Every task must update status and history files when completed or blocked.
- Failed tasks must create a diagnostic report.
- AI must not invent missing results, metrics, exports, or compile outcomes.
- If source data is missing, mark the task as `WAITING_FOR_USER`.

## Status Discipline

Status files are dashboard-facing contracts. Update only the fields relevant to the assigned task and preserve valid JSON.

## Scope Discipline

Each case is atomic and independently logged. Continue on failure where safe, record the failure, and avoid cascading unrelated changes.
