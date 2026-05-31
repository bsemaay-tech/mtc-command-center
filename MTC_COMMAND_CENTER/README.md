# MTC Command Center

Folder name: `MTC_COMMAND_CENTER`

MTC Command Center (MCC) is the command-center layer for the MTC_v2 trading research, backtest, and parity ecosystem. The product goal is to let AI workers operate the research workflow while the user watches progress, status, reports, and risks from a dashboard.

## Purpose

MCC is designed as a dashboard memory and control center. It tracks AI tasks, status files, registries, reports, parity state, backtest state, Pine draft workflow, and future dry-run LiveOps concepts without modifying the MTC_v2 core system.

## User Role

The user does not write code inside MCC during normal operation. The user provides YouTube transcripts, TradingView exports, TradingView compile observations, secrets when needed, approvals for large changes, and dashboard review.

## AI Role

AI workers read the repo, follow prompts, run approved backtest or parity tasks, write reports, update status files, create Python prototypes, draft Pine ideas, diagnose failures, update task queues, and prepare handoffs.

## First Version Mode

The first version is read-only, dry-run, and report-first. It must not send live trades, call webhooks, patch MTC_v2 core files, modify `MTC_V2.pine`, or alter PineTS/parity pipelines unless a future task explicitly authorizes that scope.

## Reference Ideas

MCC may learn from command-dash for command-center dashboard structure, pine-mcp for Pine tooling boundaries, pinescript-agents for AI-assisted Pine workflows, and SignalQuorum for future LiveOps and signal supervision ideas. These are references only; MCC remains an independent dashboard and workflow system.

## Dashboard Role

The dashboard is the user's project memory and control surface. It should show current status, task queue, parity matrix, backtest summaries, data health, worker activity, reports, and future dry-run LiveOps state from files that AI workers maintain.
