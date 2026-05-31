# AI Memory Draft

## Root `AGENTS.md`
~~~markdown
# AGENTS.md

Read this file first, then read `MTC_COMMAND_CENTER\_AI_MEMORY\START_HERE.md`.
Work token-efficiently: search before opening large files and use `ACTIVE_FILES.md` before broad scans.
Do not change trading logic, Pine logic, MTC strategy behavior, or TradingView parity without explicit approval.
Before stopping after an approved write session, update the relevant handoff and next-step files.
~~~

## Root `CLAUDE.md`
~~~markdown
Read `AGENTS.md` first.
Then read `MTC_COMMAND_CENTER\_AI_MEMORY\START_HERE.md`.
Use a token-efficient workflow and update handoff files before stopping.
Do not scan the full repo unless required.
~~~

## Root `GEMINI.md`
~~~markdown
Read `AGENTS.md` first.
Then read `MTC_COMMAND_CENTER\_AI_MEMORY\START_HERE.md`.
Use a token-efficient workflow and update handoff files before stopping.
Do not scan the full repo unless required.
~~~

## Root `.chatgpt-instructions.md`
~~~markdown
Read `AGENTS.md` first.
Then read `MTC_COMMAND_CENTER\_AI_MEMORY\START_HERE.md`.
Search before opening large files.
Update handoff files before stopping.
~~~

## Root `.cursorrules`
~~~markdown
Read `AGENTS.md` first.
Then read `MTC_COMMAND_CENTER\_AI_MEMORY\START_HERE.md`.
Use `ACTIVE_FILES.md` before broad scans.
Update handoff files before stopping.
~~~

## `MTC_COMMAND_CENTER\_AI_MEMORY\START_HERE.md`
~~~markdown
# START_HERE

Purpose: clean TradingView/MTC/QuantLens workspace for MTC project work, backtesting/parity, and QuantLens strategy intake.

Read order:
1. `AGENTS.md`
2. This file
3. `GLOBAL_HANDOFF.md` only if global state is needed
4. `NEXT_STEPS.md` only when continuing active work
5. Relevant project `_AI_MEMORY\HANDOFF.md`
6. `ACTIVE_FILES.md` before broad scanning

Do not change trading logic, Pine logic, MTC behavior, or parity checks without explicit approval.
Do not paste long reports into memory files.
Keep handoffs short, current, and actionable.
Archive old detail instead of growing active memory.
End approved write sessions by updating relevant handoff files.
~~~

## `GLOBAL_HANDOFF.md`
~~~markdown
# GLOBAL_HANDOFF

Last updated:
Updated by:
Active project:
Current objective:
Current phase:
Current blockers:
Where to continue:
Warnings:
~~~

## `NEXT_STEPS.md`
~~~markdown
# NEXT_STEPS

## P0
- Keep audit/planning notes concise.

## P1
- Create approved clean structure.
- Copy approved files only.
- Verify checksums for MIGRATE_AS_IS files.

## P2
- Validate clean workspace.
- Remove or archive approved leftovers.
~~~

## `DECISIONS.md`
~~~markdown
# DECISIONS

D001 | Date | Decision | Rationale | Owner
~~~

## `ACTIVE_FILES.md`
~~~markdown
# ACTIVE_FILES

List only files future AI sessions should read first. Keep this file short and current.
~~~

## `DO_NOT_TOUCH.md`
~~~markdown
# DO_NOT_TOUCH

- Do not change Pine logic without explicit approval.
- Do not change MTC strategy behavior without explicit approval.
- Do not change TradingView parity logic without explicit approval.
- Do not rewrite MIGRATE_AS_IS files without approval and checksum verification.
~~~

## `SESSION_LOG.md`
~~~markdown
# SESSION_LOG

Keep only the 50 most recent concise entries. Promote stable rules to `DECISIONS.md`.
~~~

## `SESSION_LOCK.md`
~~~markdown
# SESSION_LOCK

Status:
Locked by:
Started:
Scope:
Expected release:
~~~

## Project-Level `HANDOFF.md` Template
~~~markdown
# HANDOFF

Last updated:
Updated by:
Current phase:
Current status:

## Active objective
...

## Completed in last session
- ...

## Current blockers
- ...

## Next 3 actions
1. ...
2. ...
3. ...

## Files changed
- ...

## Files to read next
- ...

## Warnings
- ...

## Do not do
- ...
~~~

## Project-Level `NEXT_STEPS.md` Template
~~~markdown
# NEXT_STEPS

## Immediate
1. ...
2. ...
3. ...

## Waiting On
- ...

## Later
- ...
~~~

## QuantLens `STRATEGY_REGISTRY.md` Template
~~~markdown
# STRATEGY_REGISTRY

| STG ID | Short name | Source | Market | Timeframe | Verdict | Status file | Last updated |
|---|---|---|---|---|---|---|---|
~~~

## QuantLens Strategy `STATUS.md` Template
~~~markdown
# STGxxx STATUS

Source video:
Source URL:
Current verdict:
Market:
Timeframe:
Strategy type:
Transcript status:
Intake status:
Enrichment status:
Pine status:
Backtest status:
Latest result:
Next action:
Do not repeat:
Related files:
~~~
