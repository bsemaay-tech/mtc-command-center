# REPO MAP (generated)

- **Generation date:** 2026-08-09
- **Source:** mechanical inventory (`repo_map_inventory.md`) + first-12-line doc headers from 120 README/INDEX/START_HERE/AGENTS files
- **Refresh policy:** regenerate after structural merges
- NOT authoritative: gates/decisions live in _AI_MEMORY handoff files; verify paths before acting.

---

## MTC_COMMAND_CENTER/ (~6,928 files total; two tree listings: 71 + 6,857)

The live MTC Command Center — the canonical operational repo at `C:\LAB\Tradingview_LAB_CLEAN`. Houses MTC V2 active development (Pine/Python parity-first engine), the Python backtest and optimization system, the QuantLens YouTube-strategy research pipeline, agent protocols, prompts, dashboards, adapters, parity Pinets, and triage areas.

The mandatory onboarding chain for any agent starts at repo-root `AGENTS.md`, then proceeds to `MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md`. The frozen legacy repo at `C:\LAB\tradingview-lab` is explicitly off-limits: do not read, run, or edit anything there.

The repo operates under a **two-tier model**: Codex is the lead orchestrator and independent acceptance authority; Claude Code CLI is the implementation agent. Codex delegates implementation to Claude via `Invoke-CodexForClaude.ps1` (never bare `codex`). All agents must update handoff files before stopping.

The mechanical inventory produced two MTC_COMMAND_CENTER tree listings (71 files and 6,857 files). The smaller entry covers only `00_INBOX` and `03_QUANTLENS` and may represent a separately tracked git subset or a partial scan artifact. The larger listing is treated as authoritative for file counts below.

### 00_AGENT_PROTOCOLS/ (16 files)
Protocol files governing agent behavior, repo guard rules, and operational constraints. The key document is `MTC_REPO_GUARD_PROTOCOL.md`, which gates any exchange-facing action (even testnet) and is explicitly referenced by IBKR_PAPER_BRIDGE as requiring Baris approval before running against the exchange. Other files likely define agent-specific operational boundaries, task acceptance criteria, and inter-agent communication protocols. (inferred)

### 00_CONFIG/ (7 files)
Repository-level configuration files. Likely includes machine-readable versions of the AI account routing tables, model selection configs, and environment-specific settings referenced by `_AI_MEMORY/AI_ACCOUNT_AND_MODEL_ROUTING.md`. May also contain paths, credentials templates, and feature flags used across the Command Center. (inferred)

### 00_INBOX/ (14 files)
User-facing drop folder. The `USER_INTAKE/` subdirectory accepts raw research inputs — video/course/article transcripts (`.txt`, `.md`), chart screenshots (`.png`, `.jpg`), and descriptive notes. An AI agent routes material to the correct internal location automatically; the user does not need to know the internal folder layout. Also contains a `from_user/` subdirectory.

### 01_MTC_PROJECT/ (870 files)
Active development area for **MTC V2** — Pine Script and Python backtest engine developed together, layer-by-layer, under a parity-first approach. Scope is build-stage only (no run/optimize orchestration yet). First target: Supertrend producer parity. Contains:

- `00_PYTHON/` (39 files): Python skeleton with `pyproject.toml` entry point; build-stage only.
- `01_PINE/` (2 files): Pine skeleton; single-file policy, input surface stays in main strategy file.
- `03_DOCS/` (6 files): Architecture, UI input spec, handoff, runbook — these are source of truth.
- `04_AUDIT/` (6 files): Audit reports including pending gate release audits.
- `05_PARITY/` (568 files): Parity verification suite, the largest sub-tree.
- `feature_contracts/` (29 files): Generic feature contracts as local source of truth for any MTC V2 feature change (contract → implementation → trace → parity → acceptance gate workflow).
- `parity_oracles/` (57 files): Feature traces and independent reference oracles; pure-Python expected-value calculators that cross-check Python and PineTS traces without importing production code.
- `optimization/` (27 files): Parameter library with research seeds (not Pine defaults, not production parameters).
- `handoff/` (13 files): Portable handoff packages (`MTC_V2_PORTABLE_HANDOFF/`) for workspace continuation.
- `experiments/` (7 files): PyneCore oracle POC and vectorbt signal oracle POC.
- `docs/` (64 files): Including `START_HERE_FOR_CODEX.md`, multi-oracle starter kit, optimization rules.
- `cases/`, `scripts/`, `tests/`, `tools/`: Supporting infrastructure.

As of 2026-05-29, cases 110, 111, 134, 153, 154 all pass PineTS/Python parity. Three Python runner bugs were fixed (exit reason label map, L18 one-shot fire reset, deferred flip post-L21). Range Filter local feature parity is green.

### 01_PROMPTS/ (21 files)
Agent-specific prompt templates and startup checklists:

- `CLAUDE/` (5 files): Pine builder workflows, Pine review, documentation, prompt refinement. Startup: read ARCHITECTURE → START_HERE_FOR_AI → AI_OPERATING_RULES → assigned task.
- `CODEX/` (6 files): Repo automation, Python/backtest/parity execution, file-based reporting, MCC status. Startup: read ARCHITECTURE → START_HERE_FOR_AI → AI_OPERATING_RULES → TASK_QUEUE.json → confirm task ID.
- `GEMINI/` (4 files): Research, external strategy review, intake evaluation. Startup: read ARCHITECTURE → START_HERE_FOR_AI → AI_OPERATING_RULES → research task → evidence-linked notes.
- `SHARED/` (4 files): Prompts shared across agents.

Also contains a `CLAUDE_CONTINUATION_2026-05-31.md` — a token-efficient continuation prompt referencing `PROJECT_HANDOFF.md`, overnight lessons, and morning reports.

### 02_MTC_BACKTEST/ (1,473 files)
**MTC Python Backtest & Optimization System v1.0.0** (MVP Ready). A local-only Windows 11 application that ports the TradingView MASTER_TEMPLATE_CORE (MTC) Pine Script v6 strategy to Python for backtesting and parameter optimization. Entry via `run_app.bat` (double-click). Key structure:

- `app.py` and `pyproject.toml`: Main application entry points.
- `src/` (68 files): Core source including `cli/` tools (`run_backtest.py`, `mtc_engine_validate.py`, `refresh_demo.py`).
- `parity_suite_350/` (663 files): The largest sub-tree; contains the 350-case parity verification suite with scripts for bootstrap, freeze, case-set generation, UI coverage optimization, and TradingView XLSX routing.
- `configs/` (342 files): Case configurations including an autopilot index.
- `data/` (146 files): Data bundles and manifests.
- `tests/` (81 files): Test suite.
- `scripts/` (62 files): Operational scripts.
- `backtest_assets/` (26 files): Runtime reference artifacts (data catalog, validation reports, regime calendars) — generated by CLI tools, not hand-edited.
- `docs/` (17 files): Including `PARITY_FREEZE.md` (canonical execution contract).
- `tools/`, `utils/`, `data_providers/`, `data_tools/`, `regimes/`: Supporting modules.

Notable: `OPP_SIGNAL` + `allow_flip=true` + `exit_on_opposite_signal=true` is treated as same-bar reversal. Other close-style exits remain next-bar only. An alias-preservation bug in `optimizer_v0/replay_candidates.py` was fixed; corrected Supertrend walk-forward winner is ATR 48.

### 02_TASKS/ (7 files)
Task queue and inbox/outbox system. Contains `TASK_QUEUE.json` (referenced by Codex startup checklist), `.locks/`, `inbox/`, and `outbox/` subdirectories. (inferred)

### 03_QUANTLENS/ (2,845 files)
**QuantLens Lab** — the YouTube-strategy research pipeline. Archives, classifies, and evaluates strategy videos; performs duplicate video control and channel quality tracking; generates Python prototypes and backtests; promotes successful candidates into the parity-first Pine/Python integration process. Key structure:

- `00_INBOX_REPORTS/` (109 files): Incoming QuantLens reports from Gemini.
- `research/` (1,772 files): The largest sub-tree. Contains overnight intake batches (2026-05-03), audited re-runs, clean reruns, strategy batches, Stage-2 robustness testing (parameter grids, walk-forward, regime splits, fee stress, Monte Carlo, exit variants), Crabel range expansion POC, 5m data acquisition, and transcript intake audits. Intake batches evaluate candidates with aggregate profit factor, net return, max drawdown, and fee stress at 2x/3x.
- `strategies/` (480 files): Promoted strategy candidates (STG001–STG022), each sourced from the legacy tradingview-lab QuantLens promoted-to-parity folders.
- `tools/` (299 files): Including `mega_walk_forward.py` engine.
- `11_TRADER_WIKI/` (52 files): Trader knowledge archive; non-destructive dated imports from transcript audits. Wisdom is not strategy proof.
- `12_LLM_WIKI/` (28 files): Machine-readable repaired classifications and missing wisdom. No profitability claims.
- `_prompts/` (7 files): Prompt guide (`README_PROMPTS.md`) with 6 stage-gated prompts (transcript intake → candidate intake → Python experiment → parity promoter → Pine integration → nightly batch).
- `_AI_MEMORY/`, `_registry/`, `_skills/`, `_templates/`, `_user_guide/`: Supporting infrastructure.
- `data/` (9 files): Data bundle manifests consumed by `mega_walk_forward.py`.
- `03_SALVAGE_IDEAS/`, `04_PYTHON_PROTOTYPES/`, `05_BACKTEST_RESULTS/`, `06_PROMOTED_TO_PARITY/`: Pipeline stage directories.

### 03_STATUS/ (161 files)
Status tracking, lifecycle evidence, and validation reports. Contains timestamped snapshots from June 2026:

- `dry_run_evidence_2026-06-06/` (65 files): Evidence from dry-run executions.
- `lifecycle_fixed_2026-06-06/` (28 files): Lifecycle state snapshots after fixes.
- `mtc_engine_validation_2026-06-06/` (27 files): Engine validation run outputs.
- `producer_parity_2026-06-06/` (28 files): Producer-level parity verification results.
- `quarantine/` (1 file): Quarantined items pending review.
- `.backups/` and `.locks/`: Operational support files.

These directories serve as the evidentiary backbone for gate decisions. (inferred)

### 04_REPORTS/ (22 files)
Generated reports organized by domain and consumer:

- `ai_handoffs/` (14 files): The largest subdirectory. Contains AI agent handoff reports summarizing session state.
- `backtests/` (1 file): Backtest result summaries.
- `diagnostics/` (1 file): System diagnostic outputs.
- `inventory/` (1 file): Repository inventory snapshots (likely the source for `repo_map_inventory.md`).
- `liveops/` (1 file): Live operations reports.
- `optimization/` (1 file): Optimization run summaries.
- `parity/` (1 file): Parity verification reports.
- `pine_builder/` (1 file): Pine script builder outputs.
- `quantlens/` (1 file): QuantLens research summaries. (inferred)

### 04_SHARED/ (38 files)
Cross-cutting shared resources consumed by multiple Command Center subsystems:

- `modules/` (8 files): Reusable Python modules providing common functionality (data access, utilities, constants).
- `prompts/` (30 files): The larger subdirectory. Shared prompt templates and reusable prompt fragments used across agent contexts. (inferred)

### 05_REGISTRY/ (20 files)
Central registries providing module catalogs, strategy indexes, and configuration tracking. These serve as lookup tables enabling agents to discover available modules and their capabilities without broad repository scans. (inferred)

### 06_SCHEMAS/ (36 files)
JSON and YAML schema definitions used for data validation, configuration integrity checks, and type enforcement across the Command Center subsystems. Likely includes schemas for case configs, task definitions, parity manifests, and report formats. (inferred)

### 07_ADAPTERS/ (9 files)
Integration adapter layer that bridges the Command Center to external systems and internal subsystems. Each adapter provides a consistent interface for a specific domain:

- `liveops/` (3 files): Live trading operations adapter — the largest adapter subdirectory.
- `mtc_engine/` (1 file): MTC engine adapter for backtest/validation orchestration.
- `pine_builder/` (1 file): Pine Script builder adapter for Pine code generation workflows.
- `pinets/` (1 file): PineTS adapter for Pine-to-Python translation parity checks.
- `quantlens/` (1 file): QuantLens adapter for research pipeline integration.
- `tradingview_exports/` (1 file): TradingView export adapter for XLSX/CSV data ingestion. (inferred)

### 08_DASHBOARD_APP/ (68 files)
Web-based dashboard application providing a graphical interface for MTC operations. Entry points:

- `START_DASHBOARD.bat`: Windows launcher script.
- `apps/` (65 files): The application tree, overwhelmingly dominant. Contains `apps/api/mcc_readonly/cli.py` — a read-only API CLI for querying MTC Command Center data without modification rights.

The dashboard likely provides monitoring views, configuration interfaces, and status displays for the broader MTC system. (inferred)

### 09_DOCS/ (80 files)
Cross-cutting documentation that spans multiple subsystems:

- `ADR/` (32 files): Architecture Decision Records — the largest subdirectory. Captures significant architectural choices with context, consequences, and status.
- `AI_TOOLING/` (14 files): Documentation covering AI-assisted development workflows, tool configurations, and agent operating procedures.
- `ROADMAPS/` (11 files): Project roadmaps, milestone plans, and strategic planning documents.
- `hooks/` (2 files): Git hooks and automation trigger documentation.

### 10_ARCHIVE/ (1 file)
Single-file archive. Contains deprecated or superseded artifacts retained for reference but not part of active workflows. Agents should not depend on content here. (inferred)

### 11_TRIAGE/ (375 files)
Active triage and evaluation workspace:

- `FUSION/` (5 files): Fusion module experiments.
- `GATE_A_RUN_KIT_D_2026-08-08/` (7 files) and `GATE_A_RUN_KIT_E_2026-08-09/` (3 files): Recent gate evaluation run kits.
- `KVM2_PROGRAM/` (28 files): KVM2 program artifacts.
- `UI_AUDITS/` (5 files): UI audit reports.
- `lessons_archive/` (10 files): Archived lessons learned.
- `_eval_pipeline_source_TEMP/` (10 files): Temporary eval pipeline source.
- `ui_references/` (12 files) and `ui_snapshots/` (2 files): UI reference material.
- `HANDOFF_TEMPLATE/` and `strategies/`: Templates and strategy candidates under review.

Also referenced by continuation prompts: `OVERNIGHT_LESSONS_2026-05-31.md`, `morning_report_2026-05-31.md`, `focused_validation_report_2026-05-31.md`, `mcc_audit_2026-05-31.md`. The `BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md` governs IBKR_PAPER_BRIDGE deployment.

### 12_PARITY_PINETS/ (732 files)
Parity verification artifacts for the Pine/Python pipeline:

- `TW_EXPORT_CASES_V2/` (488 files): TradingView export case data — the dominant subdirectory.
- `_nightly/` (212 files): Nightly parity run outputs.
- `01_TW_CHART_DATA/`, `case_001/`, `scripts/`, `tools/`: Supporting chart data and utilities.

### _AI_MEMORY/ (52 files)
AI agent memory store — the authoritative source for agent state and operational gates:

- `PARALLEL_AGENT_PROMPTS/` (7 files): Prompts for parallel agent dispatch.
- `PARALLEL_AGENT_REPORTS/` (7 files): Reports from parallel agent runs.
- Contains `START_HERE.md` (canonical onboarding), `AI_ACCOUNT_AND_MODEL_ROUTING.md` (routes and snapshot quotas), handoff files, and the generated `REPO_MAP.md`.

### tools/ (2 files)
Two utility scripts at the Command Center root level. These may be convenience wrappers or bootstrap scripts for common Command Center operations. Agents should verify contents before assuming functionality. (inferred)

---

## IBKR_PAPER_BRIDGE/ (131 files)

**Crypto Paper Bridge (Hyperliquid)** — a standalone live/paper execution dashboard, independent from MTC Command Center. Despite the legacy directory name (`IBKR_PAPER_BRIDGE/` kept for git-history continuity), the broker is **Hyperliquid** (testnet = paper), finalized on 2026-07-06. IBKR and Signum were evaluated and not chosen. The bridge takes one formal strategy and runs it against a Hyperliquid account, with a professional web dashboard for configuration (strategy, coin, direction, risk %, leverage, SL/TP, money management) and live monitoring. The LLM layer is **veto/regime-only** — it never originates orders. Status: v1 mock-first build present on `feature/ibkr-bridge-final`. Running against the exchange (even testnet) requires Baris approval per repo guard protocol.

Key structure:

- `bridge/` (28 files): Core application (`app.py` entry point), API layer (3 files), broker integration (4 files), engine (13 files), static assets including `index.html` dashboard, and store (2 files).
- `config/` (2 files): Configuration including `strategies/` subdirectory.
- `deploy/` (13 files): Linux deployment assets under `deploy/linux/` — **preparation only**, never executed. Replaces the obsolete global-pip/root-systemd recipe that was rejected by triage findings.
- `docs/` (44 files): Documentation including `audits/` (7 files) and `screenshots/` (2 files).
- `tests/` (32 files): Test suite including `fixtures/` (3 files).
- `tools/` (8 files): Supporting tools.

**Key entry point:** `IBKR_PAPER_BRIDGE/bridge/app.py`

**Notable relationships:** Runs independently from MTC Command Center. Broker decision rationale is in `docs/07_BROKER_DECISION.md`. Deployment governance is in `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md`. The bridge's `README.md` explicitly delegates exchange-action authority to `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/MTC_REPO_GUARD_PROTOCOL.md`.

---

## docs/ (75 files)

Repository-level documentation at the repo root. Dominated by `migration_manifests/` (63 files), which likely contain manifests tracking file migrations, renames, and structural reorganizations across the repository's history. Also contains `superpowers/specs/` (1 file), possibly a specification for agent "superpowers" or extended capabilities. No README or index file was present in the inventory doc headers for this directory, so the exact purpose of each subdirectory is inferred from directory names. (inferred)

---

## _deepseek_driver/ (11 files)

DeepSeek driver module. Contains a `tests/` subdirectory (5 test files, nearly half the file count). Likely an AI agent driver or integration shim for DeepSeek-based operations — possibly analogous to the Codex/Claude invocation helpers but for the DeepSeek model. No README or doc file was present in the inventory doc headers, so purpose and usage are inferred from the directory name and structure. (inferred)

---

## mtc_cli/ (7 files)

MTC command-line interface. Contains `commands/` (2 files) for CLI command implementations and `tests/` (2 files) for command-level testing. Provides terminal-based entry points for MTC operations, likely covering backtest invocation, status queries, and task management. No README or doc file was present in the inventory doc headers, so exact command coverage is inferred from structure. (inferred)

---

## Root files

- `.claude/` (1 file): Claude-specific skill definitions. Contains `skills/mtc-repo-guard/` — a skill definition that likely enforces the repo guard protocol for Claude agents. This is separate from the protocol document in `00_AGENT_PROTOCOLS/`. (inferred)
- `AGENTS.md`: Repository identity file — the first file any agent must read. Declares this repo (`C:\LAB\Tradingview_LAB_CLEAN`) as the live MTC Command Center, warns that `C:\LAB\tradingview-lab` is the frozen legacy repo (do not read/run/edit), and establishes the two-tier operating model: Codex is lead orchestrator and independent acceptance authority; Claude Code CLI is the implementation agent. Mandates reading `_AI_MEMORY/START_HERE.md` next and using token-efficient search before broad scans. Prohibits changing trading logic, Pine logic, MTC strategy behavior, or TradingView parity without explicit approval.
- `CLAUDE.md`: Claude-specific entry instructions. Delegates to `AGENTS.md` → `START_HERE.md`. Mandates using `Invoke-CodexForClaude.ps1` (with `-Account secondary`) — never bare `codex` and never the desktop `C:\Users\BarışSemaay\.codex` home. Routes and snapshot quotas are defined in `_AI_MEMORY/AI_ACCOUNT_AND_MODEL_ROUTING.md`. Requires updating handoff files before stopping and prohibits full repo scans unless required.

---

## Entry points

The following 11 paths were identified as executable or config entry points by the mechanical inventory scan. They are listed in the order discovered.

| Path | Description |
|------|-------------|
| `IBKR_PAPER_BRIDGE/bridge/app.py` | Crypto Paper Bridge main application — Hyperliquid testnet live/paper execution dashboard with web UI |
| `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/pyproject.toml` | MTC V2 Python project build configuration and dependency declaration (build-stage only) |
| `MTC_COMMAND_CENTER/02_MTC_BACKTEST/app.py` | MTC Python Backtest & Optimization System main application (v1.0.0, local Windows 11) |
| `MTC_COMMAND_CENTER/02_MTC_BACKTEST/pyproject.toml` | MTC Backtest Python project configuration and dependency management |
| `MTC_COMMAND_CENTER/02_MTC_BACKTEST/run_app.bat` | Windows double-click launcher for the MTC Backtest application (primary user entry) |
| `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/cli/__init__.py` | MTC Backtest CLI package initializer — makes CLI commands importable |
| `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/cli/mtc_engine_validate.py` | MTC Engine validation CLI — validates engine outputs against expected parity results |
| `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/cli/refresh_demo.py` | Demo data refresh CLI — regenerates demo/reference data artifacts for the backtest system |
| `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/cli/run_backtest.py` | Backtest runner CLI — executes backtest configurations from the command line |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/START_DASHBOARD.bat` | Dashboard web application launcher (Windows batch file) |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/cli.py` | MCC read-only API CLI — provides read-only query access to MTC Command Center data |
