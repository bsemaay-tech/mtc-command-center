# Acceptance Criteria

## MVP-0 Foundation

- Required folder structure exists under `MTC_COMMAND_CENTER`.
- Starter docs and prompts contain meaningful content.
- Status, task, registry, and schema files are valid JSON.
- `MTC Command Center ARCHITECTURE.md` is preserved as the single canonical architecture file.
- No protected MTC_v2, PineTS, Pine, export, package, or live system changes occur.

## MVP-1 Read-only Dashboard

- Dashboard reads status and registry files.
- No write operations occur from the dashboard.
- Missing files are shown as warnings.
- User can see phase, task board, parity summary, backtest summary, and reports.

## MVP-2 AI Task Queue

- Tasks have stable IDs, owners, phases, statuses, and history entries.
- Failed or blocked tasks create reports.
- User-required input is clearly marked.

## MVP-3 Parity Status Reader

- Existing parity outputs are read without modification.
- Aggregate and per-case statuses are visible.
- Repeated failure patterns are noted.

## MVP-4 Backtest Status Reader

- Existing backtest outputs are read without modifying engine files.
- Latest run metrics and failures are visible.

## MVP-5 QuantLens Registry

- Strategy candidates have intake status and evidence notes.
- Missing transcript or source data is visible.

## MVP-6 Pine Builder Workflow

- Drafts, reviews, compile observations, and promotion gates are tracked.
- Production Pine files remain protected.

## MVP-7 Optimization Lab

- Optimization runs have parameter metadata, summaries, and report links.

## MVP-8 LiveOps Dry-run Sandbox

- LiveOps remains dry-run only.
- No live webhooks or trades are sent.
