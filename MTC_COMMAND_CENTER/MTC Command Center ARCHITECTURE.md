# MTC Command Center ARCHITECTURE.md

**Document role:** Canonical Architecture / Single Source of Truth  
**Product name:** MTC Command Center  
**Short name:** MCC  
**Canonical file name:** `MTC Command Center ARCHITECTURE.md`  
**Canonical local path:** `C:\LAB\tradingview-lab\MTC_COMMAND_CENTER\MTC Command Center ARCHITECTURE.md`  
**Project root:** `C:\LAB\tradingview-lab\MTC_COMMAND_CENTER`  
**Document version:** v2.3 — final implementation-readiness audit refinements
**Last updated:** 2026-05-30
**Status:** Pre-implementation architecture, foundation-ready, code implementation gated

**Changelog vs v2.0-v2.2 (cross-audit refinements):**
- §7.3: clean-environment rule for MTC_v2 subprocess invocations (no `PYTHONPATH`/`VIRTUAL_ENV` bleed)
- §9.3: paths must be canonicalized to absolute form before any `\\?\` UNC prefix is applied
- §10.5: quarantine directory for schema-invalid writes
- §10.6: stale-lock sweeper rule (`expires_at` enforcement and `.lock.stale` rename)
- §12.9 / §13.3: dashboard "Handoff Paste Block" for TradingView compile error/result paste
- §14.4: mechanical protected-path enforcement via `09_DOCS/hooks/protected_paths_hook` and commit-message token
- §15.1: explicit `.gitignore` requirement for `.locks/`, `.backups/`, `secrets.local.json`, `.env.local`, `quarantine/`
- §22: ADR-0011 (subprocess environment isolation), ADR-0012 (mechanical protected-path hook)
- §8 / §13.4: manual user input drop-folder with per-drop manifest
- §8 / §10.8: task proposal inbox/outbox for controlled writes
- §10.7 / §11.10: atomic write sequence and minimal append-only status event audit log
- §15.3: command allowlist and outbound network gate for dashboard-triggered execution
- §20.2: MVP-1 health endpoint contract
- §10.2: canonical lockfile location per resource and UTF-8 JSON lockfile rule
- §10.6: corrupt/malformed lock recovery rule
- §10.7: Windows sharing-violation retry handling, copy-not-rename backup rule, and event append inside the lock window
- §11.11: path/config contract for MVP-1 health checks
- §15.1: local config override files excluded from git
- §19/§20/§24: MVP-1 read model and path/schema validation gates

---

## 0. Executive Summary

MTC Command Center is an AI-operated local dashboard and project-memory system for the existing **MTC_v2** trading research, backtest, parity, QuantLens, and PineScript workflow.

The user is not expected to manually run every technical workflow from the dashboard. The intended operating model is:

```text
Human user = observer + decision maker + external-data provider
AI agents  = operators + analysts + report writers + implementation assistants
Dashboard  = memory + status + evidence + control center
MTC_v2     = protected core research/backtest/parity system
```

The dashboard will help the user remember and inspect what happened across AI-driven work: parity cases, backtests, QuantLens candidates, Pine drafts, reports, task history, and next recommended actions.

MTC Command Center must be built professionally and incrementally:

```text
Architecture first
Requirements first
Data contracts first
Folder structure first
Read-only MVP first
Report-first AI workflow
No direct core patching
No live trading in early phases
```

This architecture supersedes earlier draft names such as `MTC_V2_AI_COMMAND_CENTER`. The product name is **MTC Command Center** and the root folder is **`MTC_COMMAND_CENTER`**.

---

## 1. Goals and Non-Goals

### 1.1 Primary goals

1. Provide a single local dashboard to monitor MTC_v2 project state.
2. Track parity status across Python, PineTS, and TradingView export cases.
3. Track AI tasks executed by Codex, Claude Code, Gemini Antigravity, and future AI agents.
4. Maintain a reliable project memory through machine-readable status files and human-readable reports.
5. Manage QuantLens-style strategy intake from YouTube transcripts, internet research, and user-provided ideas.
6. Support Python prototype/backtest evaluation before any MTC_v2 integration.
7. Support Pine draft creation through pinescript-agents concepts and pine-mcp reference checks.
8. Preserve MTC_v2 parity-first discipline.
9. Make all important AI work auditable, reproducible, and recoverable.
10. Keep the user’s manual work limited to things AI cannot reliably perform.

### 1.2 Non-goals for early phases

The early phases must not include:

```text
- Live trading
- Direct WunderTrading or TradersPost live webhook execution
- Direct modification of MTC_V2.pine
- Direct modification of MTC_v2 Python core engine
- Automatic acceptance of AI-generated strategies
- Automatic promotion of strategies into MTC_v2
- Replacing PineTS
- Replacing TradingView export checks
- Replacing MTC_v2 Python engine
- Turning command-dash into the core engine
```

---

## 2. External Reference Repositories and Correct Roles

| Repository / Tool | Correct role in MCC | Incorrect role |
|---|---|---|
| `TradersPost/command-dash` | UI/API inspiration; dashboard shell reference; webhook/live-panel reference | MTC_v2 core backtest engine replacement |
| `TradersPost/pinescript-agents` | PineScript workflow inspiration; video/strategy/Pine assistant ideas; Pine draft generation concepts | Parity oracle or MTC_v2 engine |
| `TradersPost/pine-mcp` | Pine Script v6 documentation MCP server for AI-assisted Pine correctness | Backtest engine or parity oracle |
| `TradersPost/signal-quorum` | Future LiveOps/confluence-router sandbox idea | Early-stage live trading engine or parity component |
| PineTS | Pine/Python parity oracle | UI/dashboard engine |
| TradingView export | External reference/truth check | Fully automated dependency in early MVP |
| MTC_v2 Python engine | Main backtest engine | Secondary helper |

---

## 3. Core Architectural Decisions

### 3.1 MCC is an independent project folder

MCC must live under:

```text
C:\LAB\tradingview-lab\MTC_COMMAND_CENTER
```

It must not be placed inside the MTC_v2 core folders during the foundation phase. It may read MTC_v2 artifacts through paths defined in `00_CONFIG/paths.example.json` / future `00_CONFIG/paths.local.json`.

### 3.2 File-based status store first; database later only when needed

MVP-0 and MVP-1 use JSON and Markdown files because:

```text
- AI agents can read/write them easily.
- Human can inspect them easily.
- No database driver setup is needed for foundation work.
- The first dashboard is read-only.
```

However, the file-based store has risks. Therefore:

```text
- MVP-0/MVP-1: JSON/MD files only.
- MVP-2: single-writer rule + lockfile protocol for writes.
- Later: optional SQLite index for large report/backtest history.
```

SQLite is not required for foundation. It is reserved for report/history indexing when directory scanning becomes slow or when concurrent writes become unavoidable.

### 3.3 Read-only first

MVP-1 must only read files and display status. It must not execute backtests or write to MTC_v2.

### 3.4 Report-first and patch-plan-first

Any task that might affect protected files requires:

```text
1. Diagnosis report
2. Patch plan
3. Risk report
4. Explicit user approval
5. Implementation
6. Verification report
```

### 3.5 No live trading in MVP phases

LiveOps exists only as a future dry-run sandbox until explicitly approved.

### 3.6 Pine Builder creates standalone review files first

AI-generated Pine must be written as standalone review files, never directly into `MTC_V2.pine` during early phases.

---

## 4. User and AI Operating Model

### 4.1 User role

The user is primarily an observer, decision maker, and manual external-data provider.

The user may:

```text
- Watch dashboard tabs
- Read reports
- Assign tasks to Codex, Claude Code, Gemini Antigravity, or another AI
- Provide YouTube transcripts when AI cannot fetch them
- Export TradingView XLSX/CSV files when needed
- Observe TradingView compile results and provide error/output text to AI
- Enter private API keys or tokens manually
- Approve or reject major changes
- Decide whether a strategy candidate should continue
```

The user should not need to remember project state manually.

### 4.2 AI agent roles

| AI agent | Preferred responsibilities |
|---|---|
| Codex | Repo-level coding, test harnesses, adapters, dashboard API, backtest runner integration, controlled file updates |
| Claude Code | PineScript generation, Pine debugging, Pine Builder prompts, documentation refinement, strategy decomposition |
| Gemini Antigravity | Research review, strategy intake review, internet/video strategy classification, alternative critique |
| ChatGPT | Architecture, planning, task prompt creation, cross-agent orchestration, review, documentation |

### 4.3 AI task principle

AI agents must work from documented files, not memory:

```text
1. Read MTC Command Center ARCHITECTURE.md
2. Read START_HERE_FOR_AI.md or role-specific start file
3. Read AI_OPERATING_RULES.md
4. Read CURRENT_STATUS.md and 03_STATUS/CURRENT_STATUS.json
5. Read TASK_QUEUE.json
6. Perform only assigned scope
7. Produce report
8. Update status/history if allowed
```

---

## 5. Accepted Audit Improvements Incorporated Since v2.0

The architecture audit passes identified several practical risks. This v2.x architecture accepts the following fixes:

```text
ACCEPTED:
- UTF-8 / Windows path policy
- Path length policy
- Single-writer rule for early phases
- Lockfile protocol for later write phases
- JSON schema validation policy
- Data lineage requirement for backtest/parity records
- TradingView export manifest protocol
- Protected core paths policy
- Manual user input protocol
- Error taxonomy document
- Task timeout / stale task handling
- Backup-before-write for critical JSON files
- Separate MCC virtual environment policy
- Report manifest registry
```

The following audit suggestions are explicitly modified or deferred:

```text
MODIFIED:
- Use single-writer + lockfiles first, not full event-sourcing immediately.
- Use SQLite later for report/history indexing, not as the foundation store.
- Use UNC path prefix only as a fallback in path utilities, not everywhere.
- Use protected-path scanner / git diff check first; file watchdog can be later.
- Keep adapter documentation in 07_ADAPTERS; implementation adapters can later live under apps/api/app/adapters.

DEFERRED / NOT EARLY-PHASE:
- LiveOps webhook hardening implementation
- Daily backup scheduler
- Full event-sourced state machine
- Dashboard embedded terminal
- Local Pine compiler
- Dashboard as git commit orchestrator
- Five-minute checkpoint requirement for every AI task
```

---

## 6. Professional SDLC Process

MCC must follow a staged software-development lifecycle.

### 6.1 SDLC stages

1. Architecture / Single Source of Truth
2. Requirements
3. Architecture Decision Records
4. Data contracts
5. Folder structure
6. MVP roadmap
7. Design docs
8. Implementation planning
9. Read-only prototype
10. Test strategy
11. Acceptance criteria
12. Controlled implementation
13. Verification
14. Handoff
15. Maintenance

### 6.2 Phase 0 — Foundation and documentation

Before app code:

```text
- Create root folder
- Place canonical architecture file
- Create README
- Create START_HERE_FOR_AI
- Create AI_OPERATING_RULES
- Create PROJECT_HANDOFF
- Create initial JSON schemas
- Create task/status/registry examples
- Create manual input protocol
- Create error taxonomy
- Create data lineage spec
- Create protected paths policy
```

### 6.3 Phase 1 — Read-only discovery and dashboard MVP

Read existing files and show status. No backtest execution. No core writes.

### 6.4 Phase 2 — AI Task Board and controlled writes

Introduce task queue, task history, write protocol, single-writer/lockfile rules, and stale task detection.

### 6.5 Phase 3 — Parity status reader

Parse existing parity artifacts into `PARITY_STATUS.json` and display them.

### 6.6 Phase 4 — Backtest Lab status reader and controlled runner

First read historical results. Later allow AI-triggered safe backtest commands with lineage.

### 6.7 Phase 5 — QuantLens Strategy Registry

Add candidate lifecycle, dedupe, scoring, reports, and status display.

### 6.8 Phase 6 — Pine Builder workflow

Generate standalone Pine review drafts using Pine v6 rules and pine-mcp reference checks.

### 6.9 Phase 7 — Optimization Lab

Show optimization/walk-forward results and worker status.

### 6.10 Phase 8 — LiveOps dry-run sandbox

Future only. No live trade until separately approved.

---

## 7. System Architecture

### 7.1 Architectural pattern

MCC uses a ports-and-adapters pattern:

```text
Dashboard Web UI
    ↓
Dashboard API
    ↓
Application Services
    ↓
Adapters
    ↓
Existing MTC_v2 folders/tools/reports
```

### 7.2 Runtime model by phase

```text
MVP-0: No runtime app; documentation and folder skeleton only.
MVP-1: Read-only local API and/or static dashboard reading status JSON.
MVP-2: Controlled task/status writes with validation and lockfile protocol.
MVP-3+: Controlled adapters for parity, backtest, QuantLens, Pine Builder.
```

### 7.3 Environment isolation

MCC must use its own environment when code begins:

```text
MTC_COMMAND_CENTER\.venv-mcc
```

MCC must not install dependencies into the MTC_v2 core environment unless explicitly approved. When MCC needs to run MTC_v2 commands, it should use configured executable paths and subprocess boundaries.

### 7.4 Clean-environment rule for MTC_v2 subprocesses

When the MCC API (running inside `.venv-mcc`) spawns a subprocess into the MTC_v2 environment, the spawn must use a **cleaned environment**:

```text
- Explicitly set executable = configured MTC_v2 python path (e.g. mtc_v2_venv/Scripts/python.exe)
- Do NOT inherit PYTHONPATH, PYTHONHOME, VIRTUAL_ENV, or MCC-specific package paths
- Pass only the minimum env vars needed (PATH for the MTC_v2 venv, PYTHONUTF8=1, PYTHONIOENCODING=utf-8, and any required MTC_v2-specific vars)
- Capture stdout/stderr/exit code into the lineage block of the resulting record
```

This prevents MCC dependency versions from contaminating MTC_v2's runtime and producing false parity/backtest failures.

---

## 8. Canonical Folder Structure

The foundation folder skeleton is:

```text
MTC_COMMAND_CENTER/
  README.md
  MTC Command Center ARCHITECTURE.md
  START_HERE_FOR_AI.md
  PROJECT_HANDOFF.md
  AI_OPERATING_RULES.md
  CURRENT_STATUS.md
  CHANGELOG.md

  00_INBOX/
    from_user/
      .gitkeep
    manifest.example.json

  00_CONFIG/
    paths.example.json
    paths.local.example.json
    dashboard_config.example.json
    ai_roles.json
    status_schema_notes.md
    secrets.example.env

  01_PROMPTS/
    CODEX/
      START_HERE_FOR_CODEX.md
      BOOTSTRAP_FOLDER_STRUCTURE.md
      RUN_PARITY_TASK.md
      RUN_BACKTEST_TASK.md
      DIAGNOSE_PARITY_FAILURE.md
      UPDATE_STATUS_FILES.md
    CLAUDE/
      START_HERE_FOR_CLAUDE.md
      PINE_BUILDER_TASK.md
      PINE_DEBUG_TASK.md
      PINE_MCP_USAGE_RULES.md
      REVIEW_PINE_DRAFT.md
    GEMINI/
      START_HERE_FOR_GEMINI.md
      RESEARCH_STRATEGY_TASK.md
      INTAKE_REVIEW_TASK.md
      INTERNET_STRATEGY_SCAN_TASK.md
    SHARED/
      AI_TASK_TEMPLATE.md
      REPORT_FORMAT_TEMPLATE.md
      HANDOFF_TEMPLATE.md
      SAFETY_CHECKLIST.md

  02_TASKS/
    TASK_QUEUE.json
    TASK_HISTORY.json
    TASK_TEMPLATE.md
    NEXT_RECOMMENDED_TASKS.md
    inbox/
      .gitkeep
    outbox/
      .gitkeep
    .locks/
      .gitkeep

  03_STATUS/
    CURRENT_STATUS.json
    PARITY_STATUS.json
    BACKTEST_STATUS.json
    QUANTLENS_STATUS.json
    PINE_BUILDER_STATUS.json
    OPTIMIZATION_STATUS.json
    LIVEOPS_STATUS.json
    DATA_HEALTH_STATUS.json
    REPORT_MANIFEST.json
    status_events.jsonl
    .locks/
      .gitkeep
    .backups/
      .gitkeep
    quarantine/
      .gitkeep

  04_REPORTS/
    parity/
      .gitkeep
    backtests/
      .gitkeep
    quantlens/
      .gitkeep
    pine_builder/
      .gitkeep
    optimization/
      .gitkeep
    ai_handoffs/
      .gitkeep
    diagnostics/
      .gitkeep
    liveops/
      .gitkeep
    inventory/
      .gitkeep

  05_REGISTRY/
    STRATEGY_REGISTRY.json
    CASE_REGISTRY.json
    AI_WORKER_REGISTRY.json
    DATA_SOURCE_REGISTRY.json
    PROMOTION_REGISTRY.json
    TW_EXPORT_REGISTRY.json

  06_SCHEMAS/
    current_status.schema.json
    task_queue.schema.json
    task_history.schema.json
    parity_status.schema.json
    backtest_status.schema.json
    strategy_registry.schema.json
    report_manifest.schema.json
    paths.schema.json
    dashboard_config.schema.json
    tw_export_manifest.schema.json
    manual_input_request.schema.json
    status_event.schema.json
    write_lock.schema.json
    case_plan.schema.json
    lineage.schema.json

  07_ADAPTERS/
    README.md
    mtc_engine/
      README.md
    pinets/
      README.md
    tradingview_exports/
      README.md
    quantlens/
      README.md
    pine_builder/
      README.md
    liveops/
      README.md

  08_DASHBOARD_APP/
    README.md
    apps/
      api/
        README.md
      web/
        README.md

  09_DOCS/
    SDLC_PROCESS.md
    MVP_ROADMAP.md
    MVP1_READ_MODEL.md
    DASHBOARD_TABS.md
    DATA_CONTRACTS.md
    ACCEPTANCE_CRITERIA.md
    SECURITY_MODEL.md
    AI_WORKFLOW.md
    USER_MANUAL_DRAFT.md
    DATA_LINEAGE_SPEC.md
    ERROR_TAXONOMY.md
    MANUAL_USER_INPUT_PROTOCOL.md
    TRADINGVIEW_EXPORT_PROTOCOL.md
    PROTECTED_PATHS_POLICY.md
    STATUS_WRITE_PROTOCOL.md
    TASK_LIFECYCLE_STATE_MACHINE.md
    RECOVERY_PLAYBOOK.md
    NAMING_CONVENTIONS.md
    COMMAND_ALLOWLIST.md
    HEALTHCHECKS.md
    hooks/
      protected_paths_hook.py
    ADR/
      ADR-0001-command-dash-as-reference.md
      ADR-0002-file-status-first-sqlite-later.md
      ADR-0003-read-only-first.md
      ADR-0004-no-live-trading-in-mvp.md
      ADR-0005-pine-builder-standalone-drafts.md
      ADR-0006-single-writer-lockfile-before-database.md
      ADR-0007-utf8-and-windows-path-policy.md
      ADR-0008-lineage-required-for-executed-results.md
      ADR-0009-manual-tradingview-export-manifest.md
      ADR-0010-protected-core-path-policy.md
      ADR-0011-subprocess-environment-isolation.md
      ADR-0012-mechanical-protected-path-hook.md
      ADR-0013-manual-input-drop-folder.md
      ADR-0014-minimal-status-event-ledger.md
      ADR-0015-command-allowlist-and-network-gate.md

  10_ARCHIVE/
    .gitkeep
```

### 8.1 Folder structure rules

1. `03_STATUS` is machine-readable JSON only.
2. `04_REPORTS` is human-readable report output, mainly Markdown.
3. `05_REGISTRY` stores canonical registries.
4. `06_SCHEMAS` stores validation schemas.
5. `07_ADAPTERS` is documentation/planning for adapters during foundation; later implementation adapters may live under `08_DASHBOARD_APP/apps/api/app/adapters`.
6. `09_DOCS` stores runbooks, ADRs, policies, protocols, and design documents.
7. Generated candidate/report folder names must use short IDs, not full video titles.
8. `00_INBOX/from_user` is the only default manual drop location for user-provided transcripts, TradingView exports, compile logs, and other externally gathered files.
9. `02_TASKS/inbox` and `02_TASKS/outbox` are proposal/result queues for controlled write phases; they do not replace `TASK_QUEUE.json`.
10. `03_STATUS/status_events.jsonl` is an append-only audit trail for accepted/rejected status writes, not a full event-sourced replacement for status JSON snapshots.

---

## 9. Windows, UTF-8, and Path Policy

MCC is expected to run on a Windows machine. Turkish characters in paths and Windows path length limits must be treated as first-class risks.

### 9.1 Encoding rules

All Python file operations must use explicit UTF-8:

```python
open(path, "r", encoding="utf-8")
open(path, "w", encoding="utf-8", newline="\n")
```

All Node/TypeScript file operations must use explicit UTF-8 when reading or writing text.

### 9.2 Environment recommendations

`secrets.example.env` / environment docs must include:

```text
PYTHONUTF8=1
PYTHONIOENCODING=utf-8
```

### 9.3 Path length rules

1. Root path is intentionally short: `C:\LAB\tradingview-lab\MTC_COMMAND_CENTER`.
2. Generated IDs must be short: e.g., `QLR-2026-0001`, not full video names.
3. A future path utility must warn when paths exceed 200 characters.
4. UNC `\\?\` path prefix is a fallback only, not the default everywhere.
5. **Canonicalize before prefixing.** Paths containing `..` or other relative segments must be resolved to absolute canonical form (e.g. Python `Path.resolve(strict=False)`, Node `path.resolve()`) *before* the `\\?\` UNC prefix is applied. Windows API calls do not accept relative segments inside a UNC-prefixed path and will raise `FileNotFoundError`.
6. The centralized path utility must automatically apply the Windows long-path prefix after canonicalization when a Windows absolute path is `>= 240` characters. This gives a safety buffer below the legacy `MAX_PATH` limit while preserving normal short-path behavior.

### 9.4 Validation requirement

Before implementation, create a small environment validation task that proves Python and Node can read/write UTF-8 JSON containing paths with Turkish characters.

---

## 10. Status Write Protocol

### 10.1 Early phase rule: single writer

Until a locking service exists, only one AI agent may write status/task/registry files at a time.

```text
Single-writer rule:
- One assigned AI may write.
- Other AIs may read or create separate audit reports.
- User must not run two write tasks simultaneously.
```

### 10.2 Lockfile protocol for MVP-2

When controlled writes begin, a lockfile must be used:

```text
02_TASKS/.locks/TASK_QUEUE.lock
03_STATUS/.locks/<status_or_registry_file>.lock
```

Canonical lock location rule:

```text
- Locks for files under 02_TASKS live under 02_TASKS/.locks/
- Locks for files under 03_STATUS live under 03_STATUS/.locks/
- Locks for files under 05_REGISTRY live under 03_STATUS/.locks/ during the file-store phase, using the registry filename in the lock resource field
- Do not create a second generic status_write.lock in another directory for the same resource
```

A lock record must include:

```json
{
  "resource": "TASK_QUEUE.json",
  "owner_ai": "Codex",
  "task_id": "MCC-AI-001",
  "acquired_at": "2026-05-29T18:00:00+03:00",
  "expires_at": "2026-05-29T18:10:00+03:00"
}
```

Lockfiles must be valid UTF-8 JSON and must validate against `06_SCHEMAS/write_lock.schema.json`. A zero-byte, malformed, or truncated lockfile is treated as a corrupt stale lock by the sweeper, never as a valid active lock.

### 10.3 Backup-before-write

Before overwriting critical JSON files, the writer must create a timestamped backup under:

```text
03_STATUS/.backups/
```

At minimum this applies to:

```text
CURRENT_STATUS.json
PARITY_STATUS.json
BACKTEST_STATUS.json
TASK_QUEUE.json
TASK_HISTORY.json
STRATEGY_REGISTRY.json
CASE_REGISTRY.json
```

Keep a rolling window of the last 15 backups per logical target unless the user explicitly changes the retention policy.

### 10.4 Schema validation

All status and registry writes must validate against `06_SCHEMAS` before being considered accepted.

Foundation phase: schemas exist as contracts.
MVP-1: validation script.
MVP-2+: API write gate or service-level validation.

Reference enforcement stack (recommended): `pydantic v2` models generated from JSON Schema in the API write path; `jsonschema` for standalone CLI validators used by AI agents before they propose a change.

### 10.5 Quarantine on validation failure

A write that fails schema validation must not silently overwrite the live status file. Instead:

```text
- The proposed payload is written to 03_STATUS/quarantine/<file>.<ts>.invalid.json
- A validation report is written under 04_REPORTS/diagnostics/
- The live status file is left untouched
- TASK_HISTORY records the rejection with reason
- The originating task is marked WAITING_FOR_AI_REVIEW (not FAILED) so the agent can self-heal
```

### 10.6 Stale-lock sweeper

Lockfiles defined in §10.2 carry an `expires_at` timestamp. To prevent a crashed writer from blocking the queue forever, every write attempt and every API startup must run the **lock sweeper**:

```text
- Read all *.lock files under 02_TASKS/.locks/ and 03_STATUS/.locks/
- If the lockfile cannot be parsed as UTF-8 JSON or fails write_lock.schema.json:
    - Rename to <name>.lock.corrupt.<ts>
    - Append an entry to TASK_HISTORY.json:
        { event: "CORRUPT_LOCK_RECOVERED", resource, swept_at, reason }
    - Grant the lock to the new requester
- If `expires_at` < current local time:
    - Rename to <name>.lock.stale.<ts>
    - Append an entry to TASK_HISTORY.json:
        { event: "STALE_LOCK_SWEPT", resource, prior_owner_ai, prior_task_id, swept_at }
    - Grant the lock to the new requester
- If `expires_at` is in the future: deny the new requester with HTTP 409 (or equivalent) and a hint with the holder's task_id
```

Stale-lock sweeps must never delete the swept file — renames preserve a forensic trail.

All lock sweep rename/write operations must handle Windows sharing violations (`PermissionError` / `WinError 32`) with bounded retry/backoff. Default: 3 attempts with short backoff. If the file remains locked, fail gracefully with `ERR-TASK-LOCKED`; do not crash the API or partially update task history.

### 10.7 Atomic write sequence

Critical JSON files must never be edited in place. Every accepted status/task/registry write follows this sequence:

```text
1. Acquire the resource lock.
2. Build the candidate payload in memory.
3. Validate the candidate against the matching schema.
4. Backup the current live file by copying it to `.backups/`.
5. Write the candidate to a same-directory temporary file.
6. Flush and close the temporary file.
7. Re-read and validate the temporary file.
8. Atomically replace the live file with the temporary file.
9. Append a status event to 03_STATUS/status_events.jsonl.
10. Release the lock.
```

The temporary file must live on the same volume and in the same directory as the target file so the final replace operation can be atomic on Windows. Failed writes must leave the live file untouched and must produce a diagnostics report.

The backup step must be a copy operation (`copy2` or equivalent), not a rename of the live file. The live file must never be moved out of place as part of backup; the atomic replace is always `replace(temp, live)` after validation.

All write, rename, replace, and backup operations must use bounded retry/backoff for Windows sharing violations. If the resource remains locked by another process, leave the live file untouched, record `ERR-TASK-LOCKED`, and return a recoverable failure.

The `status_events.jsonl` append occurs before lock release, inside the same resource lock window. It must be a single UTF-8 write of one compact JSON object plus `\n`. MVP-2 does not need a separate event-log lock as long as all accepted/rejected writes flow through the same writer boundary.

### 10.8 Writer boundary and proposal queues

The writer boundary changes by phase:

```text
MVP-0:
  Assigned AI may create documentation/scaffold files under single-writer discipline.

MVP-1:
  Dashboard/API is read-only. Status files are consumed, not mutated by the app.

MVP-2+:
  The API/service write gate is the canonical writer for 03_STATUS and 05_REGISTRY.
  AI agents submit proposed changes through 02_TASKS/inbox.
  Accepted write receipts and rejected proposals are recorded through 02_TASKS/outbox.
```

Direct AI writes to `03_STATUS` or `05_REGISTRY` after MVP-2 require explicit task scope and must still follow the lock, backup, validation, atomic write, and event-log rules.

---

## 11. Data Contracts

### 11.1 Common metadata block

Every generated machine-readable record should include:

```json
{
  "schema_version": "1.0",
  "generated_at": "2026-05-29T18:00:00+03:00",
  "generated_by": "Codex",
  "agent_id": "codex-local",
  "model": "gpt-5-codex",
  "session_id": null,
  "task_id": null,
  "source": "manual_or_adapter_name"
}
```

`agent_id`, `model`, `session_id`, and `task_id` should be populated when a record is produced by an AI worker. This preserves the "who did what" trail without forcing the user to inspect raw chat logs.

### 11.2 Lineage block

Any executed backtest, parity comparison, optimization, or generated output derived from code/data/config must include lineage:

```json
{
  "lineage": {
    "execution_id": "BT-2026-0001",
    "git_commit": null,
    "git_dirty": null,
    "config_hash_sha256": null,
    "data_hash_sha256": null,
    "code_hash_sha256": null,
    "engine_version": null,
    "python_version": null,
    "platform": "Windows",
    "command": null,
    "started_at": null,
    "finished_at": null
  }
}
```

A result without lineage may be displayed as exploratory, but not accepted as verified.

If `git_dirty` is `true`, the record must identify the dirty files in its linked report and may not be marked `verified` unless the task explicitly permits dirty-tree exploratory work.

### 11.3 `CURRENT_STATUS.json`

```json
{
  "schema_version": "1.0",
  "product": "MTC Command Center",
  "short_name": "MCC",
  "root": "C:/LAB/tradingview-lab/MTC_COMMAND_CENTER",
  "phase": "MVP-0 Foundation",
  "mode": "read_only",
  "dry_run": true,
  "live_trading_enabled": false,
  "last_updated": null,
  "summary": "Foundation folder structure initialized.",
  "critical_warnings": [],
  "next_recommended_action": null,
  "active_writer": null
}
```

### 11.4 `TASK_QUEUE.json`

```json
{
  "schema_version": "1.0",
  "tasks": [
    {
      "id": "MCC-BOOT-001",
      "title": "Validate folder structure",
      "status": "TODO",
      "assigned_ai": "Codex",
      "phase": "MVP-0 Foundation",
      "dependencies": [],
      "requires_user_input": false,
      "timeout_seconds": 1800,
      "retry_count": 0,
      "max_retries": 1,
      "allowed_actions": [],
      "forbidden_actions": [],
      "expected_outputs": [],
      "report_path": null,
      "created_at": null,
      "updated_at": null
    }
  ]
}
```

### 11.5 Task statuses

Allowed task statuses:

```text
TODO
READY
IN_PROGRESS
WAITING_FOR_USER
WAITING_FOR_AI_REVIEW
STALE
FAILED
DONE
ARCHIVED
```

### 11.6 `PARITY_STATUS.json`

```json
{
  "schema_version": "1.0",
  "generated_at": null,
  "source": "not_connected_yet",
  "summary": {
    "total_cases": 0,
    "runnable_cases": 0,
    "python_pass": 0,
    "pinets_pass": 0,
    "tradingview_pass": 0,
    "overall_pass": 0,
    "failed": 0,
    "needs_user_export": 0
  },
  "cases": []
}
```

### 11.7 `BACKTEST_STATUS.json`

```json
{
  "schema_version": "1.0",
  "generated_at": null,
  "source": "not_connected_yet",
  "summary": {
    "total_runs": 0,
    "last_run_id": null,
    "last_successful_run": null,
    "failed_runs": 0
  },
  "runs": []
}
```

### 11.8 TradingView export manifest

Every manual TradingView export must have a manifest:

```json
{
  "schema_version": "1.0",
  "export_id": "TW-CASE-001-20260529-001",
  "case_id": "case_001",
  "symbol": "BTCUSDT.P",
  "timeframe": "1h",
  "date_range": {
    "start": null,
    "end": null
  },
  "tradingview_chart_settings": {},
  "strategy_settings_hash_sha256": null,
  "export_file_path": null,
  "export_file_hash_sha256": null,
  "exported_by_user": true,
  "notes": null
}
```

### 11.9 Report manifest

`03_STATUS/REPORT_MANIFEST.json` indexes reports:

```json
{
  "schema_version": "1.0",
  "generated_at": null,
  "reports": [
    {
      "report_id": "RPT-2026-0001",
      "category": "parity",
      "title": "Example parity report",
      "path": "04_REPORTS/parity/example.md",
      "created_at": null,
      "created_by": null,
      "related_task_id": null,
      "related_case_id": null,
      "summary": null
    }
  ]
}
```

### 11.10 Status event audit log

`03_STATUS/status_events.jsonl` records one JSON object per accepted or rejected status write. It is a lightweight audit log, not the primary state store.

Each event should include:

```json
{
  "schema_version": "1.0",
  "event_id": "EVT-2026-000001",
  "event_type": "STATUS_WRITE_ACCEPTED",
  "created_at": "2026-05-29T18:00:00+03:00",
  "task_id": "MCC-BOOT-001",
  "agent_id": "codex-local",
  "model": "gpt-5-codex",
  "session_id": null,
  "target_file": "03_STATUS/CURRENT_STATUS.json",
  "action": "replace",
  "hash_before_sha256": null,
  "hash_after_sha256": null,
  "result": "accepted",
  "error_code": null,
  "report_path": null
}
```

The JSON status files remain the dashboard-facing snapshots. The event log exists for forensic recovery, task history, and future migration to SQLite if volume grows.

### 11.11 Path and dashboard configuration contracts

MVP-1 health checks and adapters must use a documented path/config contract, not ad hoc key names. `00_CONFIG/paths.example.json` and optional local override files must validate against `06_SCHEMAS/paths.schema.json`.

Minimum path keys:

```json
{
  "schema_version": "1.0",
  "mcc_root": "C:/LAB/tradingview-lab/MTC_COMMAND_CENTER",
  "mtc_v2_root": "C:/LAB/tradingview-lab",
  "mtc_v2_python_exe": null,
  "pinets_root": null,
  "tradingview_exports_dir": null,
  "reports_root": "C:/LAB/tradingview-lab/reports"
}
```

Rules:

```text
- `paths.example.json` contains safe example/default values only.
- `paths.local.json` may override local absolute paths and must be gitignored.
- MVP-1 `/healthz` fields must map directly to this contract:
    paths_resolvable => all configured required paths parse and canonicalize
    mtc_v2_root_reachable => mtc_v2_root exists and is readable
- Windows paths must round-trip through UTF-8 JSON without mutation.
```

`00_CONFIG/dashboard_config.example.json` must validate against `06_SCHEMAS/dashboard_config.schema.json`. MVP-1 only needs read-only UI configuration: title, enabled tabs, refresh interval, and report rendering options. It must not contain secrets or executable command strings.

---

## 12. Dashboard Modules

### 12.1 Home / Project Overview

Displays:

```text
- System phase
- Last AI activity
- Open tasks
- Tasks waiting for user
- Parity pass rate
- Last backtest
- Last QuantLens candidate
- Last Pine draft
- Critical warnings
- Next recommended action
```

The next recommended action must be prominent.

### 12.2 AI Task Board

Tracks all AI tasks and clearly highlights:

```text
- WAITING_FOR_USER
- FAILED
- STALE
- IN_PROGRESS
- Tasks with missing reports
- Tasks with stale locks
```

### 12.3 Parity Matrix

Columns:

```text
case_id
symbol
timeframe
config_id
python_status
pinets_status
tradingview_status
overall_status
first_divergence_bar
lineage_status
last_run_at
report_path
```

### 12.4 Case Explorer

Displays case settings, traces, mismatch summaries, first divergence information, and report links.

### 12.5 Backtest Lab

Displays backtest results and later enables controlled AI-run workflows. All accepted runs require lineage.

### 12.6 Optimization Lab

Displays walk-forward and robustness results. Must emphasize OOS performance, parameter stability, and overfit risk.

### 12.7 QuantLens Intake

Pipeline:

```text
INBOX
DEDUPE_CHECKED
INTAKE_DONE
TRIAGED
PYTHON_PROTOTYPE_READY
BACKTESTED
REJECTED
SALVAGE
PROMOTED_TO_PARITY
APPROVED_FOR_MTC
ARCHIVED
```

### 12.8 Strategy Registry

Tracks all candidates and their source, logic, status, scores, backtest results, Pine draft status, parity status, and final decision.

### 12.9 Pine Builder

Creates standalone Pine review drafts.

Mandatory outputs:

```text
standalone_pine_strategy_REVIEW.pine
standalone_pine_indicator_REVIEW.pine
PINE_COMPILE_CHECKLIST.md
PINE_TO_MTC_INTEGRATION_PLAN.md
PARITY_PLAN.md
```

Pine Builder must use pine-mcp when Pine v6 syntax, function signatures, or migration details are uncertain.

The Pine Builder tab must expose a **Handoff Paste Block**: a plain text area where the user pastes the TradingView compile output (errors or success banner). On submit, the dashboard writes the raw paste to `04_REPORTS/pine_builder/<draft_id>/tv_compile_<ts>.txt`, updates `PINE_BUILDER_STATUS.json` with the compile status, and unblocks any task in `WAITING_FOR_USER` that requested compile feedback. This is the canonical way the observer-user closes the AI ↔ TradingView loop without becoming a manual operator.

### 12.10 Reports Center

Browse all Markdown reports via `REPORT_MANIFEST.json`.

### 12.11 Data Health

Checks missing bars, duplicates, timezone mismatch, DST risk, symbol mapping, CSV freshness, TradingView export freshness, PineTS data freshness, and warmup/history length.

### 12.12 Worker Monitor

Future module for long-running jobs. It should begin as read-only from task/status files.

### 12.13 AI Handoff Center

Shows per-agent start instructions and latest handoff summaries.

### 12.14 LiveOps Sandbox

Future dry-run module only. It may use SignalQuorum concepts but must not send live trades unless separately approved.

### 12.15 Settings / Paths

Displays configured paths, environment status, path length warnings, schema validation status, and protected path warnings.

---

## 13. Manual User Input Protocol

The user provides inputs AI cannot reliably obtain.

### 13.1 Manual input types

```text
YOUTUBE_TRANSCRIPT
TRADINGVIEW_EXPORT
TRADINGVIEW_COMPILE_RESULT
API_TOKEN_ENTRY
USER_APPROVAL
```

### 13.2 Manual input request record

When AI needs user input, it must create or update a task as `WAITING_FOR_USER` and specify:

```json
{
  "input_type": "TRADINGVIEW_EXPORT",
  "exact_request": "Export strategy trades for case_001 on BTCUSDT.P 1h",
  "expected_file_type": "xlsx_or_csv",
  "save_location": "...",
  "deadline": null,
  "why_needed": "TradingView export parity comparison"
}
```

### 13.3 TradingView compile feedback

The user may paste compile errors or report compile success. The Pine Builder must record this in `PINE_BUILDER_STATUS.json` and link any compile report.

### 13.4 Manual input drop-folder

When the user provides external artifacts, the default location is:

```text
00_INBOX/from_user/<input_id>/
```

Each drop should contain or be paired with a manifest:

```json
{
  "schema_version": "1.0",
  "input_id": "USR-IN-2026-0001",
  "task_id": "MCC-TW-001",
  "input_type": "TRADINGVIEW_EXPORT",
  "provided_at": "2026-05-29T18:00:00+03:00",
  "provided_by_user": true,
  "expected_files": ["trades.csv"],
  "actual_files": [],
  "sha256": {},
  "notes": null
}
```

AI agents should not scan arbitrary Downloads/Desktop locations looking for user files. They should request an exact drop-folder path, hash the received files, treat originals as immutable evidence, and create normalized manifests or derived reports elsewhere.

---

## 14. Protected Paths Policy

### 14.1 Protected files and folders

Protected targets include:

```text
MTC_V2.pine
MTC_v2 Python core engine files
Parity oracle core files
Canonical feature contracts
Existing parity case definitions
Existing TradingView export archives
Canonical MTC Command Center architecture file
```

### 14.2 Modification gate

Any protected file change requires:

```text
1. Task explicitly allows protected modification
2. Diagnosis report exists
3. Patch plan exists
4. Risk report exists
5. User approval is recorded
6. Backup or git diff is captured
7. Verification report is produced
```

### 14.3 Early safeguard

Before full watchdog automation, AI must run/report a protected-path check when tasks could affect files outside `MTC_COMMAND_CENTER`.

### 14.4 Mechanical pre-commit hook

Policy alone is insufficient; an AI with shell access can write to any path. To turn the protected-paths policy into a mechanical guard:

```text
- A pre-commit hook lives at 09_DOCS/hooks/protected_paths_hook (Python or PowerShell)
- The hook reads a canonical list from 09_DOCS/PROTECTED_PATHS_POLICY.md (or a sibling .protected_paths file)
- On every commit, the hook scans staged paths
- If any staged path matches the protected list, the commit is rejected UNLESS
  the commit message contains the literal token:
      APPROVED-PATCH-PLAN: <task_id>
  AND the referenced task_id exists in TASK_HISTORY.json with status = APPROVED
- Installation is documented in 09_DOCS/PROTECTED_PATHS_POLICY.md
- The hook is enabled per-clone via `git config core.hooksPath 09_DOCS/hooks` or the equivalent pre-commit framework configuration
```

This converts protected-paths from a documentation rule into a verifiable gate at the git boundary.

---

## 15. Security Model

### 15.1 Secret handling

Never commit real secrets.

Allowed secret locations:

```text
secrets.local.json  (gitignored)
.env.local          (gitignored)
OS credential store
manual user entry
```

Template files may exist, but must contain fake/example values only.

The repository `.gitignore` must explicitly exclude:

```text
00_INBOX/from_user/*
!00_INBOX/from_user/.gitkeep
00_CONFIG/paths.local.json
00_CONFIG/*.local.json
secrets.local.json
.env.local
*.env.local
02_TASKS/.locks/*.lock
02_TASKS/.locks/*.lock.stale.*
03_STATUS/.locks/*.lock
03_STATUS/.locks/*.lock.stale.*
03_STATUS/.backups/
03_STATUS/quarantine/
.venv-mcc/
```

Logs and reports must redact `Authorization`, `Set-Cookie`, `api_key`, `token`, `secret`, and `password` field values before being written to disk.

### 15.2 Live trading controls

Early phases must not contain live trade sending code.

Required future controls before live trading:

```text
- dry_run/live switch
- explicit user approval
- webhook signing
- shared secret validation
- HMAC signature validation
- timestamp expiry
- replay protection
- max order guard
- symbol allowlist
- quantity/risk cap
- audit log
```

### 15.3 Command execution controls

Future AI-triggered commands must use a safe allowlist. Arbitrary shell execution from the dashboard must not be added in early phases.

`09_DOCS/COMMAND_ALLOWLIST.md` must define allowed command families by phase. The default policy is:

```text
MVP-0/MVP-1:
  Allowed: read-only filesystem inspection, schema validation, health checks.
  Forbidden: backtests, package installs, live webhooks, broker/exchange calls.

MVP-2:
  Allowed: controlled status/task write helpers through the write gate.
  Forbidden: direct arbitrary shell execution from dashboard UI.

MVP-4+:
  Allowed: explicitly configured MTC_v2 backtest commands only, with clean subprocess env and lineage capture.
```

Dashboard-triggered commands must be declared as named operations, not free-form shell strings. Any outbound network access from dashboard/API tasks requires explicit task permission and must be reported.

---

## 16. Error Taxonomy

`09_DOCS/ERROR_TAXONOMY.md` must define standardized error codes.

Initial categories:

```text
ERR-PATH-UTF8
ERR-PATH-LENGTH
ERR-JSON-SCHEMA
ERR-TASK-STALE
ERR-TASK-LOCKED
ERR-PROTECTED-PATH
ERR-DATA-MISSING
ERR-DATA-HASH
ERR-PARITY-DIVERGENCE
ERR-PARITY-MISSING-TW_EXPORT
ERR-BACKTEST-FAILED
ERR-PINE-COMPILE
ERR-PINE-REPAINT-RISK
ERR-QUANTLENS-DUPLICATE
ERR-LIVEOPS-DISABLED
```

---

## 17. AI Task Lifecycle

### 17.1 Lifecycle steps

```text
1. Read architecture and operating rules
2. Read task queue
3. Confirm task scope
4. Verify forbidden actions
5. Acquire writer role or lock if writing
6. Backup critical JSON files if writing
7. Perform allowed work
8. Validate JSON outputs
9. Produce report
10. Update task history
11. Update project handoff
12. Release lock if used
13. End with completion summary
```

### 17.2 Definition of Ready

A task is ready only if it has:

```text
- id
- title
- scope
- allowed actions
- forbidden actions
- expected outputs
- owner AI
- required user input flag
- verification steps
- timeout_seconds
```

### 17.3 Definition of Done

A task is done only if:

```text
- Expected outputs exist
- Report exists
- Status/history updated when allowed
- Verification completed or marked incomplete honestly
- No forbidden actions were performed
- Any protected-path exposure is reported
```

### 17.4 Stale task policy

If a task remains `IN_PROGRESS` past `timeout_seconds`, it becomes `STALE` until reviewed. Another AI must not overwrite it without explicit recovery action.

---

## 18. Main Workflows

### 18.1 Parity diagnosis workflow

```text
Failed case identified
    ↓
AI reads case details and lineage
    ↓
AI compares Python/PineTS/TW outputs
    ↓
AI identifies first divergence if possible
    ↓
AI writes diagnosis report
    ↓
AI proposes patch plan if needed
    ↓
User approves before protected modifications
```

### 18.2 Backtest workflow

```text
User asks AI to run backtest
    ↓
AI verifies data health
    ↓
AI records command/config/data lineage
    ↓
AI runs MTC_v2 Python engine via approved method
    ↓
AI saves JSON output and markdown report
    ↓
AI updates BACKTEST_STATUS.json
    ↓
Dashboard displays result
```

### 18.3 TradingView export workflow

```text
AI requests exact export
    ↓
Task becomes WAITING_FOR_USER
    ↓
User exports CSV/XLSX from TradingView
    ↓
User places file in requested location
    ↓
AI creates manifest and file hash
    ↓
AI runs comparison
```

### 18.4 QuantLens strategy workflow

```text
Transcript / URL / idea provided
    ↓
Candidate record created
    ↓
Dedupe check
    ↓
Intake report
    ↓
Triage and scoring
    ↓
Python prototype if eligible
    ↓
Backtest with lineage
    ↓
Reject / salvage / promote decision
```

### 18.5 Pine Builder workflow

```text
Approved candidate or Python prototype
    ↓
AI reads Pine Builder prompt
    ↓
AI uses pine-mcp for Pine v6 reference checks when needed
    ↓
AI creates standalone Pine review draft
    ↓
User compiles in TradingView when needed
    ↓
AI records compile status and errors
    ↓
AI prepares parity plan
    ↓
Only after approval can integration planning begin
```

---

## 19. Testing and QA Strategy

### 19.1 Foundation tests

```text
- Folder structure validation
- Required file existence validation
- UTF-8 read/write validation
- Path length warning validation
- JSON schema validation for example files
- paths.example.json validation against paths.schema.json
```

### 19.2 Dashboard tests

```text
- Unit tests for status parsing
- API route tests
- UI rendering tests for empty and populated statuses
- Report manifest/link tests
```

### 19.3 Adapter tests

```text
- MTC path detection tests
- Parity report parser tests
- Backtest result parser tests
- Strategy registry parser tests
- TradingView export manifest parser tests
```

### 19.4 Workflow tests

```text
- AI task lifecycle test
- Status update test
- Task history update test
- Stale task transition test
- Backup-before-write test
- Corrupt lock recovery test
- Windows sharing violation retry/failure test
- status_events.jsonl single-line append test
- Protected-path scanner test
```

### 19.5 MTC_v2 domain tests

```text
- Parity status aggregation test
- First divergence extraction test
- Case settings extraction test
- Backtest summary extraction test
- Lineage completeness test
```

---

## 20. Acceptance Criteria

### 20.1 MVP-0 Foundation acceptance

Accepted when:

```text
- Root folder exists
- Canonical architecture file exists
- Required folders exist
- Required starter docs exist
- Example status JSON files validate
- No files outside MTC_COMMAND_CENTER were modified
- UTF-8/path policy is documented
- Protected paths policy is documented
- No packages installed unless explicitly approved
- No app started
```

### 20.2 MVP-1 Read-only dashboard acceptance

Accepted when:

```text
- API or static reader can load status JSON files
- `/healthz` or equivalent health check reports api_ok, schema_validation_ok, lock_dir_writable, paths_resolvable, and mtc_v2_root_reachable
- MVP1_READ_MODEL.md lists every file read by MVP-1 and each file has a schema or an explicit empty-stub contract
- paths.example.json validates against paths.schema.json
- Web UI displays Home, Task Board, Parity Matrix, Reports Center
- Empty-state rendering works
- Invalid JSON is handled gracefully
- No MTC_v2 core files are modified
- No backtest is executed by the dashboard
- No live webhook exists
```

### 20.3 MVP-2 AI Task Board acceptance

Accepted when:

```text
- TASK_QUEUE.json validates against schema
- TASK_HISTORY.json updates after AI task completion
- WAITING_FOR_USER tasks are clearly visible
- STALE tasks can be detected
- Single-writer or lockfile protocol is documented and tested
- Proposed writes can flow through 02_TASKS/inbox and produce accepted/rejected receipts in 02_TASKS/outbox
- status_events.jsonl records accepted/rejected write events
```

### 20.4 MVP-3 Parity integration acceptance

Accepted when:

```text
- Existing parity reports are parsed
- Cases appear in Parity Matrix
- Case detail page links to settings and reports
- First divergence and mismatch status are visible when available
- Lineage completeness is visible
```

### 20.5 MVP-4 Backtest Lab acceptance

Accepted when:

```text
- AI can run a known safe backtest command only after explicit task scope
- Data health gate has passed, or any warning is explicitly acknowledged in the run report
- Output is saved to JSON and Markdown
- Lineage block is present
- Dashboard displays the run result
- Failed runs are recorded honestly
```

### 20.6 MVP-5 QuantLens acceptance

Accepted when:

```text
- Candidate registry exists
- AI can add candidate from transcript
- Dedupe status is recorded
- Intake report is linked
- Candidate status appears in dashboard
```

### 20.7 MVP-6 Pine Builder acceptance

Accepted when:

```text
- AI can create standalone Pine review draft
- Pine compile checklist is generated
- pine-mcp usage rule is documented
- Dashboard shows Pine draft status
- MTC_V2.pine remains untouched
```

---

## 21. Documentation Standards

Every major feature requires:

```text
- Design note
- Data contract
- Prompt/task file
- Test/verification checklist
- Report output template
- Acceptance criteria
```

Every AI task report must include:

```text
- Task ID
- Model / AI agent
- Files inspected
- Files changed
- Commands run
- Results
- Verification
- Risks
- Next recommended step
```

---

## 22. Architecture Decision Records

Initial ADRs:

```text
ADR-0001 — command-dash as reference, not base engine
ADR-0002 — file status first, SQLite later for indexing
ADR-0003 — read-only first
ADR-0004 — no live trading in MVP
ADR-0005 — Pine Builder produces standalone review files first
ADR-0006 — single-writer/lockfile before database
ADR-0007 — UTF-8 and Windows path policy
ADR-0008 — lineage required for executed results
ADR-0009 — manual TradingView export manifest requirement
ADR-0010 — protected core path policy
ADR-0011 — subprocess environment isolation when invoking MTC_v2
ADR-0012 — mechanical protected-path enforcement via pre-commit hook
ADR-0013 — manual input drop-folder and immutable user-provided evidence
ADR-0014 — minimal status event ledger for audit and recovery
ADR-0015 — command allowlist and outbound network gate
ADR-0016 — MVP-1 read model and path/config contract
ADR-0017 — Windows-safe lock and atomic write recovery
```

---

## 23. Risk Register

| Risk | Impact | Mitigation |
|---|---|---|
| Concurrent AI writes corrupt JSON | High | Single-writer first, lockfile protocol later, backup-before-write |
| Unicode path errors on Windows | High | Explicit UTF-8 file IO, env policy, validation test |
| Windows path length failures | Medium | Short root, short IDs, path-length checks |
| Backtest result not reproducible | High | Lineage block with git/config/data hashes |
| AI modifies core files accidentally | High | Protected-path policy, patch-plan requirement, scanner/checks |
| Dashboard status becomes stale | Medium | Task lifecycle requires status updates |
| Strategy candidates are overfit | High | OOS, walk-forward, robustness checks |
| Pine draft compiles but parity fails | High | PineTS/TW/Python parity gates |
| User loses track of work | High | Task board, reports center, handoff center |
| Live webhook sends unwanted trade | Critical | No live webhook in MVP, dry-run only |
| Secrets are leaked to repo | Critical | `.env.local`, `secrets.local.json`, template-only examples |
| Local PC dependency affects live signals | High | LiveOps postponed; future replay/cloud design |
| User-provided artifacts are misplaced or mutated | High | Manual input drop-folder, per-drop manifest, SHA-256 hashes, immutable originals |
| Dashboard command execution escapes intended scope | Critical | Named command allowlist, no free-form shell UI, explicit outbound network permission |

---

## 24. Initial Task Backlog

Recommended first tasks:

```text
MCC-BOOT-001
Create root folder skeleton and documentation files.

MCC-BOOT-002
Validate folder structure and canonical file names.

MCC-DOC-001
Create UTF-8 / Windows path policy and validation checklist.

MCC-DOC-002
Create DATA_LINEAGE_SPEC.md.

MCC-DOC-003
Create ERROR_TAXONOMY.md.

MCC-DOC-004
Create MANUAL_USER_INPUT_PROTOCOL.md.

MCC-DOC-005
Create TRADINGVIEW_EXPORT_PROTOCOL.md.

MCC-DOC-006
Create STATUS_WRITE_PROTOCOL.md, COMMAND_ALLOWLIST.md, and HEALTHCHECKS.md.

MCC-DOC-007
Create MVP1_READ_MODEL.md and PATHS_RESOLUTION.md.

MCC-SCHEMA-001
Create JSON schemas and example status files.

MCC-SCHEMA-002
Create current_status, task_history, status_event, write_lock, lineage, case_plan, manual_input_request, paths, dashboard_config, and tw_export_manifest schemas.

MCC-SAFE-001
Create protected paths policy and verification checklist.

MCC-SAFE-002
Create `.gitignore`, protected-path hook stub, and command allowlist validation checklist.

MCC-MVP1-001
Design read-only status file generator.
```

---

## 25. What AI Must Not Do Without Approval

```text
- Modify MTC_V2.pine
- Modify MTC_v2 core Python engine
- Delete or move existing reports
- Delete or move parity cases
- Change canonical case definitions
- Send real webhooks
- Add real secrets to files
- Install large dependencies into the main MTC_v2 environment
- Merge generated Pine into production files
- Mark a strategy approved without parity gates
- Run two write tasks simultaneously without lock protocol
```

---

## 26. What AI May Do in Early Phases

```text
- Create MCC root folder
- Create Markdown documentation
- Create JSON schemas
- Create example status JSON files
- Read existing files
- Produce inventory reports
- Produce design reports
- Produce patch plans
- Create read-only adapters
- Create dashboard UI skeleton
- Create API endpoints that read local JSON files
- Create validation scripts after approval
```

---

## 27. Recommended First Codex Assignment After Approval

This is not to be executed automatically. It is stored for future use.

```text
You are implementing the first architecture-approved scaffold for MTC Command Center.

Read:
1. MTC Command Center ARCHITECTURE.md
2. AI_OPERATING_RULES.md if it exists
3. PROJECT_HANDOFF.md if it exists

Goal:
Create the initial folder skeleton, documentation files, JSON schema placeholders, and example status files only.

Forbidden:
- Do not modify MTC_V2.pine.
- Do not modify MTC_v2 Python core engine.
- Do not run live webhooks.
- Do not run backtests yet.
- Do not move or delete existing files.
- Do not install packages.

Expected output:
- Folder skeleton under C:\LAB\tradingview-lab\MTC_COMMAND_CENTER
- README.md
- PROJECT_HANDOFF.md
- AI_OPERATING_RULES.md
- START_HERE_FOR_AI.md
- Role-specific start files
- Example JSON files under 03_STATUS
- TASK_QUEUE.json and TASK_HISTORY.json
- Setup report under 04_REPORTS/ai_handoffs/

Verification:
- List created files.
- Confirm no protected files were modified.
- Confirm no files outside MTC_COMMAND_CENTER were modified.
- Confirm documentation/scaffold only.
```

---

## 28. Final Architectural Principle

MTC Command Center must enforce disciplined engineering rather than replace it.

```text
The dashboard should not be the trading engine.
The dashboard should not be the parity oracle.
The dashboard should not be the source of trading truth.
The dashboard should be the memory, evidence, status, and control surface around MTC_v2.
```

AI agents must not improvise freely. They must follow documented prompts, task queues, schemas, status files, handoff files, and acceptance gates.

The user should not need to remember everything. The system should remember.
