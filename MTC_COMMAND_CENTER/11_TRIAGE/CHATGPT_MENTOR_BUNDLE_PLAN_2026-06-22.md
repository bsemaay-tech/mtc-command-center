# CHATGPT_MENTOR_BUNDLE_PLAN_2026-06-22 — AUDIT FIRST

Mode: **AUDIT + PLAN ONLY**. No zip, no stage, no commit, no push, no merge, no execution, no branch creation.

---

## 1 Executive summary

**Goal:** Produce a safe, auditable file bundle so ChatGPT can mentor Barış on MTC Command Center backend, database/data model, dashboard, and Strategy Intelligence development.

**Current git state (verified):**
- Branch: `master`
- `git pull --ff-only origin master` → already up to date
- `git rev-list --count '@{u}..HEAD'` → **0** (no commits ahead)
- `git status` → **2 untracked paths only:**
  1. `MTC_COMMAND_CENTER/11_TRIAGE/CHATGPT_MENTOR_BUNDLE_PLAN_2026-06-22.md` (this file)
  2. `MTC_COMMAND_CENTER/11_TRIAGE/FUSION/` (5 fusion-review markdown files)
- **No planning branch exists.** No `feature/chatgpt-mentor-bundle-plan` or similar.
- **No dirty tracked files.** Worktree is otherwise clean relative to `origin/master`.

**Key findings:**
- **43 SQLite `.db` files** exist — all under protected scope `02_MTC_BACKTEST`. None proposed.
- **No `.env`** files in proposed areas. One `secrets.example.env` in `00_CONFIG/` (template, no real secrets).
- **Data model is mixed:** backtest/optimization engine uses SQLite (`02_MTC_BACKTEST`); dashboard/Strategy Intelligence layer is **file-based** (JSON registries in `05_REGISTRY`, JSON Schemas in `06_SCHEMAS`, result artifacts).
- **36 JSON Schema files** in `06_SCHEMAS/` (including `write_lock.schema.json`).
- **17 JSON registry files** in `05_REGISTRY/` — several large (217 KB, 130 KB, 126 KB, 53 KB). Only small/safe ones proposed as-is; large ones need sanitized samples.
- **`TRIAGE_CANDIDATE_REGISTRY.json`** (126 KB) contains external YouTube URLs → excluded from full copy.
- **`_AI_MEMORY/`** contains 36 files including large prose files (`GLOBAL_HANDOFF.md` 163 KB, `NEXT_STEPS.md` 110 KB, `SESSION_LOG.md` 88 KB). Select only essential handoff/context files.
- **`00_AGENT_PROTOCOLS/`** has 8 protocol docs (not 4 as previously claimed).
- **`09_DOCS/`** has ~40+ docs including ADRs, security model, data contracts, lineage spec — valuable mentor context.
- **`04_SHARED/`** has Pine modules and prompt templates — relevant for Strategy Intelligence context.

**Mentor strategy:** Ship **schemas + read-only API source + frontend + key docs + small representative registry files + ADRs**. Contracts come from `06_SCHEMAS`, not from bulk data. Large registries → sanitized head samples only.

**Proposed file count: 184 files** (audited by running the section 10 manifest filter without copying).

**Recommendation: AUDIT COMPLETE — AWAITING BARIS APPROVAL.**

---

## 2 Exact files proposed for bundle

Paths relative to `MTC_COMMAND_CENTER/`. The section 10 manifest filter was run in read-only mode and resolves to **184 proposed files**.

### 2.1 Handoff / product / protocol context (~18 files)

| File | Size | Notes |
|------|------|-------|
| `_AI_MEMORY/START_HERE.md` | 2.5 KB | Entry point |
| `_AI_MEMORY/PROJECT_MEMORY.md` | 3.7 KB | Project memory |
| `_AI_MEMORY/PIPELINE_STATE.md` | 4.0 KB | Pipeline state |
| `_AI_MEMORY/DECISIONS.md` | 7.0 KB | Decision log |
| `_AI_MEMORY/ACTIVE_FILES.md` | 27.4 KB | Active file index |
| `_AI_MEMORY/NEXT_STEPS.md` | 109.7 KB | Large but current; keep |
| `_AI_MEMORY/GLOBAL_HANDOFF.md` | 162.6 KB | Large; optional — trim if bundle size matters |
| `_AI_MEMORY/AI_RULES.md` | 4.4 KB | AI operating rules |
| `_AI_MEMORY/DO_NOT_TOUCH.md` | 0.2 KB | Protected paths reminder |
| `_AI_MEMORY/REVIEW_CHECKLIST.md` | 2.0 KB | Review checklist |
| `_AI_MEMORY/STRATEGY_RESEARCH_WORKFLOW.md` | 2.8 KB | Research workflow |
| `00_AGENT_PROTOCOLS/MCC_PRODUCT_CONTEXT.md` | 3.6 KB | Product context |
| `00_AGENT_PROTOCOLS/CHATGPT_WEB_MENTOR_WORKFLOW.md` | 1.8 KB | Mentor workflow |
| `00_AGENT_PROTOCOLS/NO_PROMOTION_SAFETY_RULES.md` | 0.8 KB | Safety rules |
| `00_AGENT_PROTOCOLS/MTC_REPO_GUARD_PROTOCOL.md` | 2.0 KB | Repo guard |
| `00_AGENT_PROTOCOLS/AGENT_HANDOFF_BUNDLE_PROTOCOL.md` | 1.4 KB | Bundle protocol |
| `00_AGENT_PROTOCOLS/SCREENSHOT_AND_UI_REVIEW_PROTOCOL.md` | 1.0 KB | UI review protocol |
| `00_AGENT_PROTOCOLS/CLEAN_WORKTREE_AND_PUSH_PROTOCOL.md` | 1.4 KB | Clean/push protocol |
| `00_AGENT_PROTOCOLS/MTC_REPO_GUARD_USAGE.md` | 1.0 KB | Guard usage |

### 2.2 Triage design context (5 files)

| File | Size | Notes |
|------|------|-------|
| `11_TRIAGE/STRATEGY_INTELLIGENCE_DESIGN_CONTEXT.md` | 12.8 KB | Strategy Intelligence design |
| `11_TRIAGE/DASHBOARD_DATA_AVAILABILITY_AUDIT_2026-06-15.md` | 40.3 KB | Data availability audit |
| `11_TRIAGE/RUN_PLAN_BUILDER_AUDIT_2026-06-15.md` | 16.5 KB | Run plan builder audit |
| `11_TRIAGE/BACKTEST_ARTIFACT_READER_INTEGRATION_REPORT_2026-06-15.md` | 8.8 KB | Artifact reader integration |
| `11_TRIAGE/README.md` | 2.6 KB | Triage README |

### 2.3 Backend / read-only API (29 files)

Whole package `08_DASHBOARD_APP/apps/api/mcc_readonly/` (28 `.py` + `README.md`):

`__init__.py`, `__main__.py`, `ai_names_reader.py`, `audit_reader.py`, `backtest_reader.py`, `cli.py`, `expert_quantlens_reader.py`, `health.py`, `heartbeat_reader.py`, `json_io.py`, `liveops_reader.py`, `mtc_v2_reader.py`, `night_artifacts_reader.py`, `optimization_reader.py`, `parity_reader.py`, `paths.py`, `pine_builder_reader.py`, `pipeline_reader.py`, `presentation_reader.py`, `quantlens_reader.py`, `read_model.py`, `registry_reader.py`, `research_reader.py`, `schema.py`, `scorecard_reader.py`, `server.py`, `task_lifecycle.py`, `writer.py`, `apps/api/README.md`.

Plus `08_DASHBOARD_APP/README.md` (top-level dashboard readme).

### 2.4 Backend tests (21 files)

All of `08_DASHBOARD_APP/apps/api/tests/test_*.py`:

`test_ai_names_reader.py`, `test_audit_reader.py`, `test_backtest_reader.py`, `test_build_profile_result_artifact.py`, `test_build_run_plan.py`, `test_expert_quantlens_reader.py`, `test_heartbeat_reader.py`, `test_home_metric_invariants.py`, `test_liveops_reader.py`, `test_mtc_v2_reader.py`, `test_needs_backtest_selector.py`, `test_night_artifacts_reader.py`, `test_optimization_reader.py`, `test_parity_reader.py`, `test_pine_builder_reader.py`, `test_pipeline_reader.py`, `test_readonly_core.py`, `test_registry_reader.py`, `test_scorecard_reader.py`, `test_task_lifecycle.py`, `test_writer_gate.py`.

### 2.5 Frontend / dashboard (6 files)

| File | Size | Notes |
|------|------|-------|
| `08_DASHBOARD_APP/apps/web/index.html` | — | Shell |
| `08_DASHBOARD_APP/apps/web/app.js` | 124.6 KB | Dashboard logic |
| `08_DASHBOARD_APP/apps/web/styles.css` | — | Styling |
| `08_DASHBOARD_APP/apps/web/PRODUCT.md` | — | Product contract |
| `08_DASHBOARD_APP/apps/web/DESIGN.md` | — | Design contract |
| `08_DASHBOARD_APP/apps/web/README.md` | — | Run/build notes |

### 2.6 Data contracts — JSON Schemas (36 files)

All `06_SCHEMAS/*.schema.json` (exclude `__pycache__`):

`artifact_index`, `backtest_profile_result`, `backtest_status`, `case_plan`, `component_registry`, `current_status`, `dashboard_config`, `evaluation_artifact_v1`, `indicator_registry`, `lineage`, `liveops_status`, `manual_input_request`, `optimization_status`, `parity_status`, `paths`, `pine_builder_status`, `production_readiness_artifact_v1`, `report_manifest`, `research_backtest_registry`, `research_run_registry`, `run_plan`, `run_status`, `status_envelope`, `status_event`, `strategy_registry`, `strategy_research_registry`, `tag_dictionary`, `task_history`, `task_proposal`, `task_proposal_receipt`, `task_queue`, `top_results`, `triage_candidate_registry`, `tw_export_manifest`, `variant_log_registry`, `write_lock`.

### 2.7 Registry samples — small/safe only (3 files)

| File | Size | Notes |
|------|------|-------|
| `05_REGISTRY/TAG_DICTIONARY.json` | 4.6 KB | Small, safe |
| `05_REGISTRY/INDICATOR_REGISTRY.json` | 24.9 KB | Small, safe |
| `05_REGISTRY/COMPONENT_REGISTRY.json` | 37.3 KB | Small, safe |

Large/sensitive registries handled in §8 (sanitized samples).

### 2.8 QuantLens user guide (16 files)

All `03_QUANTLENS/_user_guide/*.md`:

`00_START_HERE.md` … `14_OPTIMIZASYON_SKORLAMA_TR.md`, `QUANTLENS_ASSISTANT_PROMPT_TR_DRAFT.md`.

### 2.9 QuantLens hardened builder tools (4 files)

| File | Notes |
|------|-------|
| `03_QUANTLENS/tools/build_run_plan.py` | Run plan builder |
| `03_QUANTLENS/tools/build_profile_result_artifact.py` | Profile result builder |
| `03_QUANTLENS/tools/build_needs_backtest_selector.py` | Needs-backtest selector |
| `03_QUANTLENS/tools/build_evaluation_artifact.py` | Evaluation artifact builder |

### 2.10 QuantLens tool tests (3 files)

| File | Notes |
|------|-------|
| `03_QUANTLENS/tools/tests/test_progress_emitter.py` | Progress emitter test |
| `03_QUANTLENS/tools/tests/test_run_emitter_supervisor.py` | Run emitter supervisor test |
| `03_QUANTLENS/tools/tests/test_run_watchdog.py` | Run watchdog test |

### 2.11 Architecture / design docs (optional, ~10 files)

Selected from `09_DOCS/` for mentor context:

| File | Size | Notes |
|------|------|-------|
| `09_DOCS/DATA_CONTRACTS.md` | — | Data contract overview |
| `09_DOCS/DATA_LINEAGE_SPEC.md` | — | Lineage specification |
| `09_DOCS/SECURITY_MODEL.md` | 0.9 KB | Security model |
| `09_DOCS/MVP1_READ_MODEL.md` | — | MVP1 read model |
| `09_DOCS/MVP_ROADMAP.md` | — | MVP roadmap |
| `09_DOCS/ERROR_TAXONOMY.md` | — | Error taxonomy |
| `09_DOCS/HEALTHCHECKS.md` | — | Health check spec |
| `09_DOCS/TASK_LIFECYCLE_STATE_MACHINE.md` | 0.4 KB | Task lifecycle |
| `09_DOCS/STATUS_WRITE_PROTOCOL.md` | 0.9 KB | Status write protocol |
| `09_DOCS/TRADINGVIEW_EXPORT_PROTOCOL.md` | 0.4 KB | TV export protocol |
| `09_DOCS/ACCEPTANCE_CRITERIA.md` | — | Acceptance criteria |
| `09_DOCS/ADR/ADR-0001*` through `ADR-0017*` | ~0.3 KB each | All 17 ADRs |
| `09_DOCS/PROTECTED_PATHS_POLICY.md` | — | Protected paths policy |
| `09_DOCS/CONTROLLED_TASK_WRITER.md` | — | Controlled task writer |
| `09_DOCS/MANUAL_USER_INPUT_PROTOCOL.md` | — | Manual input protocol |
| `09_DOCS/COMMAND_ALLOWLIST.md` | — | Command allowlist |
| `09_DOCS/NAMING_CONVENTIONS.md` | — | Naming conventions |
| `09_DOCS/SDLC_PROCESS.md` | — | SDLC process |
| `09_DOCS/RECOVERY_PLAYBOOK.md` | — | Recovery playbook |
| `09_DOCS/AI_WORKFLOW.md` | — | AI workflow |
| `09_DOCS/USER_MANUAL_DRAFT.md` | 1.1 KB | User manual draft |
| `09_DOCS/DASHBOARD_TABS.md` | — | Dashboard tabs spec |

### 2.12 Config examples (3 files)

| File | Notes |
|------|-------|
| `00_CONFIG/paths.example.json` | Path config template |
| `00_CONFIG/dashboard_config.example.json` | Dashboard config template |
| `00_CONFIG/PATHS_RESOLUTION.md` | Path resolution docs |

**Proposed total: 184 files.** Read-only manifest enumeration completed; no files copied.

---

## 3 Files explicitly excluded

- **Protected scopes** (path names only for context): `02_MTC_BACKTEST/`, `07_ADAPTERS/`, `01_PINE/`, `MTC_V2/`
- **All 43 SQLite `.db` files** (all under `02_MTC_BACKTEST/`)
- **`05_REGISTRY/TRIAGE_CANDIDATE_REGISTRY.json`** (126 KB — contains external YouTube URLs)
- **Large data registries** (full copies excluded; sanitized head samples proposed in §8):
  - `AI_QUANTLENS_VERDICT_REGISTRY.json` (217 KB)
  - `STRATEGY_RESEARCH_REGISTRY.json` (130 KB)
  - `AI_STRATEGY_NAME_REGISTRY.json` (53 KB)
  - `STRATEGY_REGISTRY.json` (0.1 KB — near-empty, but excluded by default)
  - `PROMOTION_REGISTRY.json` (0.05 KB — near-empty)
  - `RESEARCH_BACKTEST_REGISTRY.json`, `RESEARCH_RUN_REGISTRY.json`, `VARIANT_LOG_REGISTRY.json`, `TW_EXPORT_REGISTRY.json`, `CASE_REGISTRY.json`, `DATA_SOURCE_REGISTRY.json`, `AI_WORKER_REGISTRY.json`
- **Bulk result/run folders:** `03_QUANTLENS/tools/night_runs/`, `overnight_runs/`, `pbo_runs/`, `single_strategy_runs/`, `smoke_runs/`, `sprint_runs/`, `cpcv_runs/`
- **`.venvs/`**, `__pycache__/`, `.pytest_cache/`, `.impeccable/`, `.ruff_cache/`
- **`top_results.json`** (not found in proposed areas; schema only)
- **Business Excel files** (`*.xlsx`), logs, cache, zip archives
- **YouTube URL/transcript history**, Hermes memory exports, broker/exchange files, private local-only archives
- **`11_TRIAGE/FUSION/`** (5 fusion-review files — not proposed)
- **`11_TRIAGE` scratch noise:** one-off `.py`, `.csv`, dated scratch markdown files not listed in §2.2
- **`_AI_MEMORY/SESSION_LOG.md`** (88 KB — operational log, not mentor context)
- **`_AI_MEMORY/SESSION_LOCK.md`** (33 bytes — lock file)
- **`_AI_MEMORY/RESULT_*.md`** files (10 files — agent result artifacts, not mentor context)
- **`_AI_MEMORY/CODEX_PICKUP_2026-06-08.md`**, `DEEPSEEK_DISPATCH.md`, `HANDOFF_PROMPT_SP004_PHASE3.md`, `IMPECCABLE_STRATEGY_DETAIL_PICKUP_2026-06-21.md`, `MCC_COMPLETION_MASTER_PLAN.md`, `MCC_READINESS_REPORT.md`, `N5_CODABILITY_AUDIT.md`, `NIGHT_BATCHES.md`, `FORWARD_PAPER_QUEUE.md`, `A3_GAP_MATRIX.md`, `SPRINT_WORKFLOW.md`, `STRATEGY_CODE_REVIEW_CHECKLIST.md`, `STRATEGY_COMPONENT_LIBRARY.md`, `SESSION_RECOVERY_2026-06-07.md`, `PARALLEL_AGENT_PROMPTS/`, `PARALLEL_AGENT_REPORTS/`
- **`00_CONFIG/secrets.example.env`** (template — excluded as a precaution)
- **`00_CONFIG/paths.local.json`** (local machine paths)
- **`04_SHARED/`** (Pine modules and prompts — excluded; relevant but not core to backend/dashboard/data-model mentoring)
- **`01_MTC_PROJECT/`** (Pine strategy project — excluded; protected scope adjacent)
- **`02_TASKS/`** (task queue — excluded; operational)
- **`00_INBOX/`**, `01_PROMPTS/`, `03_STATUS/`, `04_REPORTS/`, `10_ARCHIVE/` (excluded; not core)

---

## 4 Backend/API map

`08_DASHBOARD_APP/apps/api/mcc_readonly/` — read-only FastAPI/CLI service over the file-based data model:

| Module | Role |
|--------|------|
| `server.py` / `cli.py` / `__main__.py` | Entrypoints (read-only API surface) |
| `read_model.py` | Snapshot / read model assembly for the dashboard |
| `pipeline_reader.py` | Pipeline state reader (data availability) |
| `backtest_reader.py`, `optimization_reader.py`, `parity_reader.py`, `night_artifacts_reader.py` | Result artifact readers |
| `registry_reader.py`, `scorecard_reader.py`, `quantlens_reader.py`, `expert_quantlens_reader.py`, `research_reader.py`, `mtc_v2_reader.py`, `ai_names_reader.py`, `pine_builder_reader.py`, `liveops_reader.py`, `audit_reader.py`, `heartbeat_reader.py`, `presentation_reader.py` | Domain readers |
| `schema.py` | JSON Schema validation |
| `paths.py` | Path resolution |
| `json_io.py` | Safe JSON IO |
| `health.py` | Health endpoint |
| `writer.py` + `task_lifecycle.py` | Gated writer (see `test_writer_gate.py`) |

Tests exercise home metrics, run-plan, artifact builders, and writer gate invariants.

---

## 5 Frontend/dashboard map

`08_DASHBOARD_APP/apps/web/` — static SPA consuming the read-only API:

| File | Role |
|------|------|
| `index.html` | Shell |
| `app.js` (124.6 KB) | Dashboard logic, views, data fetch/render |
| `styles.css` | Styling |
| `PRODUCT.md` / `DESIGN.md` | Product + design contract (Strategy-Detail UI) |
| `README.md` | Run/build notes |

---

## 6 Data model / database map

- **SQLite databases found: 43 `.db` files**, all under `02_MTC_BACKTEST/`:
  - `results/` — optimizer databases (signal, exits, filters, money management, local/robust refine stages)
  - `results/walkforward/` — walk-forward databases (supertrend variants)
  - `reports/benchmarks/` — benchmark databases
- **Data model type: mixed.**
  - **Engine layer:** SQLite (`02_MTC_BACKTEST/results/`, `reports/benchmarks/`)
  - **Dashboard / Strategy Intelligence layer:** **file-based** JSON (`05_REGISTRY/` instances, `06_SCHEMAS/` contracts, result artifacts read by `mcc_readonly`)
- **No DB files proposed.** If schema-level DB understanding is later needed, propose a **schema-only export** (no rows), pending Barış approval — not done in this audit:
  ```powershell
  # schema-only, read-only, NO data dump (run later, only if approved)
  sqlite3 "MTC_COMMAND_CENTER\02_MTC_BACKTEST\results\optimizer_smoke.db" ".schema" > <out>\SQLITE_SCHEMA_optimizer_smoke.sql
  ```

---

## 7 Sensitive-data risk check

| Risk | Finding |
|------|---------|
| `.env` / secrets in proposed areas | **None found.** One `secrets.example.env` in `00_CONFIG/` is a template (excluded). |
| API keys, tokens, credentials | **None found** in any proposed file. |
| Broker/exchange/live files | **None found** in proposed set. |
| External URLs | **Only in `TRIAGE_CANDIDATE_REGISTRY.json`** (126 KB) — **excluded**. |
| Real DBs with live data | **All 43 `.db` files excluded** (protected scope `02_MTC_BACKTEST`). |
| Large generated outputs / `top_results.json` | **Excluded.** Schema-only for `top_results`. |
| PII / personal data | **None identified** in proposed files. |
| Local machine paths | `paths.local.json` excluded. `paths.py` uses configurable paths. |

**Risk verdict: LOW** with the §3 exclusions applied.

---

## 8 Recommended sanitized samples

For large/sensitive registries, instead of full files ship a small head sample with sensitive fields redacted (URLs, raw transcript text, private notes):

| Registry | Size | Sanitization needed |
|----------|------|---------------------|
| `STRATEGY_RESEARCH_REGISTRY.json` | 130 KB | First 2–3 entries, drop URL/transcript fields |
| `AI_QUANTLENS_VERDICT_REGISTRY.json` | 217 KB | 2–3 verdicts, keep metric shape, drop source links |
| `TRIAGE_CANDIDATE_REGISTRY.json` | 126 KB | 2–3 entries, **strip all URLs** |
| `AI_STRATEGY_NAME_REGISTRY.json` | 53 KB | First 5 entries, no sensitive fields expected |
| `STRATEGY_REGISTRY.json` | 0.1 KB | Near-empty; include as-is or skip |
| `PROMOTION_REGISTRY.json` | 0.05 KB | Near-empty; include as-is or skip |

**Sanitization to be done by Barış (or a follow-up approved task) — not performed here.** Schemas in §2.6 already convey the full contract without any instance data.

---

## 9 Proposed bundle path

```
C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\11_TRIAGE\_chatgpt_mentor_bundle_2026-06-22\
```

Staging folder for review; zip only after Barış approval.

---

## 10 Exact next command to create the bundle after Baris approval

Copies the §2 file set into the staging folder. **Do not run during this audit.**

```powershell
cd C:\LAB\Tradingview_LAB_CLEAN

$src = "MTC_COMMAND_CENTER"
$dst = "MTC_COMMAND_CENTER\11_TRIAGE\_chatgpt_mentor_bundle_2026-06-22"

# 1. review this plan first:
#    cat "MTC_COMMAND_CENTER\11_TRIAGE\CHATGPT_MENTOR_BUNDLE_PLAN_2026-06-22.md"

# 2. on Baris approval, create staging dir:
New-Item -ItemType Directory -Force $dst | Out-Null

# 3. enumerate and copy each proposed file, preserving tree structure.
#    This command lists every file that will be copied for audit before execution:
Get-ChildItem -Path $src -Recurse -File | Where-Object {
    $rel = $_.FullName.Substring((Get-Location).Path.Length + 1)
    # Include patterns from §2 — this is the auditable manifest generator
    $rel -match '^MTC_COMMAND_CENTER\\_AI_MEMORY\\(START_HERE|PROJECT_MEMORY|PIPELINE_STATE|DECISIONS|ACTIVE_FILES|NEXT_STEPS|GLOBAL_HANDOFF|AI_RULES|DO_NOT_TOUCH|REVIEW_CHECKLIST|STRATEGY_RESEARCH_WORKFLOW)\.md$' -or
    $rel -match '^MTC_COMMAND_CENTER\\00_AGENT_PROTOCOLS\\.+\.md$' -or
    $rel -match '^MTC_COMMAND_CENTER\\11_TRIAGE\\(STRATEGY_INTELLIGENCE_DESIGN_CONTEXT|DASHBOARD_DATA_AVAILABILITY_AUDIT_2026-06-15|RUN_PLAN_BUILDER_AUDIT_2026-06-15|BACKTEST_ARTIFACT_READER_INTEGRATION_REPORT_2026-06-15|README)\.md$' -or
    $rel -match '^MTC_COMMAND_CENTER\\08_DASHBOARD_APP\\apps\\api\\mcc_readonly\\.+\.py$' -or
    $rel -match '^MTC_COMMAND_CENTER\\08_DASHBOARD_APP\\apps\\api\\tests\\test_.+\.py$' -or
    $rel -match '^MTC_COMMAND_CENTER\\08_DASHBOARD_APP\\apps\\api\\README\.md$' -or
    $rel -match '^MTC_COMMAND_CENTER\\08_DASHBOARD_APP\\README\.md$' -or
    $rel -match '^MTC_COMMAND_CENTER\\08_DASHBOARD_APP\\apps\\web\\(index\.html|app\.js|styles\.css|PRODUCT\.md|DESIGN\.md|README\.md)$' -or
    $rel -match '^MTC_COMMAND_CENTER\\06_SCHEMAS\\.+\.schema\.json$' -or
    $rel -match '^MTC_COMMAND_CENTER\\05_REGISTRY\\(TAG_DICTIONARY|INDICATOR_REGISTRY|COMPONENT_REGISTRY)\.json$' -or
    $rel -match '^MTC_COMMAND_CENTER\\03_QUANTLENS\\_user_guide\\.+\.md$' -or
    $rel -match '^MTC_COMMAND_CENTER\\03_QUANTLENS\\tools\\(build_run_plan|build_profile_result_artifact|build_needs_backtest_selector|build_evaluation_artifact)\.py$' -or
    $rel -match '^MTC_COMMAND_CENTER\\03_QUANTLENS\\tools\\tests\\(test_progress_emitter|test_run_emitter_supervisor|test_run_watchdog)\.py$' -or
    $rel -match '^MTC_COMMAND_CENTER\\09_DOCS\\(DATA_CONTRACTS|DATA_LINEAGE_SPEC|SECURITY_MODEL|MVP1_READ_MODEL|MVP_ROADMAP|ERROR_TAXONOMY|HEALTHCHECKS|TASK_LIFECYCLE_STATE_MACHINE|STATUS_WRITE_PROTOCOL|TRADINGVIEW_EXPORT_PROTOCOL|ACCEPTANCE_CRITERIA|PROTECTED_PATHS_POLICY|CONTROLLED_TASK_WRITER|MANUAL_USER_INPUT_PROTOCOL|COMMAND_ALLOWLIST|NAMING_CONVENTIONS|SDLC_PROCESS|RECOVERY_PLAYBOOK|AI_WORKFLOW|USER_MANUAL_DRAFT|DASHBOARD_TABS)\.md$' -or
    $rel -match '^MTC_COMMAND_CENTER\\09_DOCS\\ADR\\ADR-\d+-.+\.md$' -or
    $rel -match '^MTC_COMMAND_CENTER\\00_CONFIG\\(paths\.example\.json|dashboard_config\.example\.json|PATHS_RESOLUTION\.md)$'
} | ForEach-Object {
    $rel = $_.FullName.Substring((Get-Location).Path.Length + 1)
    $target = Join-Path $dst $rel
    $targetDir = Split-Path $target -Parent
    if (-not (Test-Path $targetDir)) { New-Item -ItemType Directory -Force $targetDir | Out-Null }
    Copy-Item -Path $_.FullName -Destination $target -Force
    Write-Host "COPIED: $rel"
}

# 4. verify count:
Write-Host "`nTotal files copied: $( (Get-ChildItem -Path $dst -Recurse -File).Count )"

# 5. optional zip AFTER review:
#    Compress-Archive -Path "$dst\*" -DestinationPath "$dst.zip" -Force
```

**Note:** The `Where-Object` filter above is the auditable manifest. For a dry manifest review, run the same filter and print/count paths before the `Copy-Item` block. Current audited count is 184 files.

---

## Completion report

**Audit complete.** The existing draft contained several false state claims that have been corrected:

| False claim in prior draft | Correction |
|---|---|
| "Repo clean on master" | Worktree has 2 untracked paths (this report + FUSION/) |
| "Planning branch `feature/chatgpt-mentor-bundle-plan` created" | **No such branch exists** |
| "43 real SQLite .db files" | Confirmed — all under `02_MTC_BACKTEST` |
| "35 JSON Schemas" | **36** (includes `write_lock.schema.json`) |
| "Only one registry (TRIAGE_CANDIDATE_REGISTRY.json) contains external URLs" | Confirmed |
| "16 handoff/product context files" | Expanded to ~18 with additional protocol docs |
| "4 protocol files" | **8** protocol files in `00_AGENT_PROTOCOLS/` |
| "26 backend tests" | **21** test files (actual count) |
| "Proposed total: ~138 files" | Revised to **184** with ADRs and design docs |

**Next step:** Barış reviews §2 proposed file list, approves or modifies, then runs the §10 PowerShell command to create the staging bundle.
