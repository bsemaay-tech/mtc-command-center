# PROJECT_MEMORY

Stable repository facts. Update only when a fact actually changes.
Volatile / per-session state belongs in `GLOBAL_HANDOFF.md`,
`SESSION_LOG.md`, or `ACTIVE_FILES.md` — not here.

## Repo Identity

- Name: `Tradingview_LAB_CLEAN`
- Purpose: TradingView strategy + Pine development, backtest, parity suite,
  and MTC (Master Trading Core) workflow command center.
- Primary developer: Barış (solo).

## Top-Level Layout

- `AGENTS.md`                          — agent contract (read first).
- `CLAUDE.md`                          — Claude-specific instructions.
- `YT_TRANSCRIPT_COLLECTOR/`           — isolated local Python utility for collecting public YouTube transcripts from `urls.txt` via `youtube-transcript-api`; no browser automation, login, video/audio download, or account actions.
- `MTC_COMMAND_CENTER/`                — main workspace.
  - `_AI_MEMORY/`                      — AI memory + rules (this folder).
  - `02_MTC_BACKTEST/`                 — Python backtester + parity suite.
  - `04_SHARED/`                       — shared Pine modules + prompts.
  - `tools/`                           — repo-level helpers, incl. `repo_guard.ps1` and `resilient_dispatch.sh`.
  - other numbered subprojects.
- `IBKR_PAPER_BRIDGE/`                 — the Trading System runtime (see below).
- `docs/migration_manifests/`          — migration policy + audit reports.

## Trading System / IBKR_PAPER_BRIDGE

Despite the legacy name, this is the **Hyperliquid** paper/TESTNET execution bridge — the runtime
the Trading System roadmap hardens. Stable facts:

- Layout: `bridge/{api,broker,engine,store}/`, `config/`, `deploy/linux/`, `docs/`, `tests/`,
  `requirements.{in,lock,txt}`.
- Runtime entry `bridge/app.py`; FastAPI + uvicorn, bound to `127.0.0.1:8790` (loopback only).
- **Startup is fail-closed:** `app.py` forces `app_state` to `DISARMED` on every start unless it is
  `KILLED`. ARM is an explicit API action; there is no automatic ARM.
- Operational DB is **SQLite, WAL**, single `Store` per connection. Every mutating store method is
  one explicit `BEGIN IMMEDIATE` transaction — the connection is created with the sqlite3 default
  `isolation_level`, so a caller must never leave an implicit transaction open.
- Schema: **default target v4**; v9 is the opt-in KILL-evidence capability. Migrations are additive
  with no downgrade path, and `_migrate_v8_to_v9` preserves the predecessor row census by design.
- `deploy/linux/` holds the complete Ubuntu deployment package — installer, rollback, verify,
  logrotate, env template, and two systemd unit templates. The **steady (restart-enabled) profile is
  deliberately inert**: no script installs or enables it. Both templates are loopback-only, hardened,
  `KillSignal=SIGTERM`, `TimeoutStopSec=45`.
- Test suite lives in `IBKR_PAPER_BRIDGE/tests/` and must be run with CWD `IBKR_PAPER_BRIDGE` and
  `--ignore=TSP1009B.pytest_tmp_s1r1` — that directory is ACL-locked and plain `pytest` aborts
  collection with `PermissionError`.
- Two suite failures are **pre-existing and out of scope** on every branch: the stale KVM2 evidence
  ledger hash, and `test_invariants_preserve_risk_and_history` asserting `schema_version == "2"`
  against the current default v4.
- Contracts are documented per task under `IBKR_PAPER_BRIDGE/docs/` (`22_ORDER_STATE` …
  `31_KILL_EVIDENCE_EPOCH_CONTRACT`).

## Key Contracts

- Pine logic, MTC strategy behavior, and parity files are **protected**.
  See `DO_NOT_TOUCH.md`.
- MTC-Engine Validation is a shortlist-only intermediate funnel stage in
  `02_MTC_BACKTEST`: use `src/config/profiles/light_risk.py`,
  manual adapters under `src/modules/signals/producers/`, and
  `python -m src.cli.mtc_engine_validate`. It reuses `MTCRunner`; it is not
  a new engine, not live trading, and not `MTC_V2.pine` integration.
- QuantLens CPCV validation defaults to all PASS/STRONG_PASS candidates.
  In `03_QUANTLENS/tools/cpcv_validator.py`, `--max-candidates 0` means no
  cap; pass a positive value only for an intentional smoke/sample run.
- Path rewrite policy: active set complete, deferred set fix-on-demand.
  See `docs/migration_manifests/PATH_REWRITE_POLICY.md`.
- Legacy freeze policy: accept-and-document (no NTFS DACL).
  See `docs/migration_manifests/LEGACY_FREEZE_POLICY.md`.
- Dashboard route contract: `/dashboard` serves
  `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/index.html` as the
  Strategy Intelligence Command Center shell. The active shell is vanilla
  HTML/JS/CSS with left-sidebar navigation, default Command Center Home, and
  read-only API feeds from `/healthz`, `/api/snapshot`, and `/api/read-model`.
  It is not a React runtime and it must not imply backtest, broker, paper, or
  live execution capability.
- Dashboard visual contract: the Strategy Intelligence Command Center shell
  should follow the final `11_TRIAGE/ui_references/google_strategy_intelligence_v2_final`
  dark command-center reference: dark canvas, compact left navigation, dense
  dark cards/tables, teal/blue/amber/red status accents, workflow cards, and
  read-only missing-artifact states. Avoid returning to a light admin skeleton.

## Existing Prompt Library

`MTC_COMMAND_CENTER/04_SHARED/prompts/`
- `01_master_template_audit/`
- `02_youtube_strategy/`
- `04_performance_audit/`
- `05_ai_workflow/`   — generic GStack-style workflow gates (this layer).

## Cross-References

- Memory entry point: `START_HERE.md`.
- Workflow rules: `AI_RULES.md`.
- Active working set: `ACTIVE_FILES.md`.
- Pre-merge / pre-commit gates: `REVIEW_CHECKLIST.md`.
- Sprint loop: `SPRINT_WORKFLOW.md`.

## What Does NOT Belong Here

- In-progress task notes        → `GLOBAL_HANDOFF.md`
- "What I did today"            → `SESSION_LOG.md`
- "What to do next"             → `NEXT_STEPS.md`
- One-off decisions             → `DECISIONS.md`
- File-level forbidden zones    → `DO_NOT_TOUCH.md`
