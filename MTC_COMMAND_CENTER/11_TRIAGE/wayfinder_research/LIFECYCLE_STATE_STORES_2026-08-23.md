# Lifecycle / Promotion State Stores — Inventory (wayfinder #58)

**Scope:** read-only inventory of every place this repository records candidate/strategy
lifecycle or promotion state today, done from an isolated worktree (`C:\WFRES4`, branch
`research/lifecycle-state-stores`, based on `a3656fc0`). All file paths below are relative to
the repo root unless a full path is given. Historical documents are cited as
`git show <ref>:<path>`.

## Summary

**No, there is not a single authoritative lifecycle-state store today, and the repository's own
audit already says so.** `05_REGISTRY/PROMOTION_REGISTRY.json` — the file whose name and schema
suggest it is the canonical promotion ledger — has never been written to (`promotions: []`,
confirmed empty; see F-6 below). But that does not mean lifecycle/promotion state does not
exist: it exists, scattered, in at least five other places that were never wired to the
"official" registry: a `promotion_status` field carrying real values (44 of 63 non-empty) inside
per-strategy `producer_spec.json` files that the dashboard actually reads and displays; a
`promotable` boolean in `VARIANT_LOG_REGISTRY.json`; a `decision` verdict in
`AI_QUANTLENS_VERDICT_REGISTRY.json`; a `recommended_next_step` / `eligible_for_retriage` pair in
`TRIAGE_CANDIDATE_REGISTRY.json`; and, on the execution side, the IBKR/Hyperliquid Bridge's own
per-run SQLite store, which records nothing about strategy identity at all (no `candidate_id`,
`package_hash`, or `deployment_identity_hash` column anywhere in its schema). None of these
stores' identity keys match the `candidate_id` / `package_hash` / `deployment_identity_hash`
scheme the frozen master brief defines in §6.7. **What would need to change:** the frozen
planning set already answers this at the store-topology level — Map #37's owner decision on
ticket #41 settles the model as **hybrid** (per-worker SQLite = source of truth, a supervisor
derived registry/snapshot on top, central Postgres deferred) — but that decision is about
*where bytes live*, not about *which of today's five-plus registries is authoritative for a
given fact*, and no document found in this repo reconciles today's parallel promotion-status
fields under that model. That reconciliation is open work, not something this inventory can
resolve.

---

## 1. F-6 — the empty promotion registry

**File:** `MTC_COMMAND_CENTER/05_REGISTRY/PROMOTION_REGISTRY.json` (confirmed at
`C:\WFRES4\MTC_COMMAND_CENTER\05_REGISTRY\PROMOTION_REGISTRY.json`).

**Schema (entire file, 4 lines):**
```json
{
  "schema_version": "1.0",
  "promotions": []
}
```
One top-level array field, `promotions`, empty. No record shape is defined anywhere else in the
repo (no schema file under `06_SCHEMAS/` references it — see search below).

**The audit fact itself**, found via `git show 764da27f:MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md`,
lines 430–435:
> `## F-6 [FACT] The promotion registry has never been used`
> - `05_REGISTRY/PROMOTION_REGISTRY.json` → `promotions: []` (50 bytes).
> - `05_REGISTRY/STRATEGY_REGISTRY.json` → `candidates: []` (97 bytes).
> - Against: `STRATEGY_RESEARCH_REGISTRY.json` 63 strategies; `TRIAGE_CANDIDATE_REGISTRY.json`
>   172 candidates (159 with transcripts, 89 high-quality, 90 eligible for retriage);
>   `RESEARCH_RUN_REGISTRY.json` 6 runs.
> - **The promotion ladder has never been walked end to end.** Candidate identity has no
>   persistent home.

F-6 is listed among the findings that survived every review round unchanged (same document,
line 273 and line 3039 — "the empty promotion registry (F-6)" confirmed by the Gate-5 audit).
(Note: an unrelated finding also labeled "F-6" exists in a different, single-topic self-QA
document — `MTC_COMMAND_CENTER/11_TRIAGE/WPI_SELFQA_CLAIM_AUDIT_SEC102_2026-08-12.md:58` — about a
stop-move miscount in an unrelated security-hardening battery. That is a different document's own
F-numbering and is not about the promotion registry; it is noted here only to rule it out.)

**Why nothing writes to it — evidence, not inference:**
- Repo-wide grep for `PROMOTION_REGISTRY` (case-sensitive, all file types) returns only seven
  hits, and every one is either a migration-manifest checksum row or prose documentation, never
  code:
  - `docs/migration_manifests/mtc_command_center_sha256_manifest.csv:84`
  - `docs/migration_manifests/copy_manifest.csv:97`
  - `docs/migration_manifests/phase2c_pine_sha256_before_smoke.csv:10914`
  - `docs/migration_manifests/phase2c_pine_sha256_after_smoke.csv:10935`
  - `MTC_COMMAND_CENTER/MTC Command Center ARCHITECTURE.md:502` (directory listing only)
  - `MTC_COMMAND_CENTER/11_TRIAGE/CHATGPT_MENTOR_BUNDLE_PLAN_2026-06-22.md:194,296` ("near-empty;
    include as-is or skip")
  - `MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_.../CANDIDATE_RELEASE_SHA256SUMS:5696`
  - No `.py`, `.ts`, `.tsx`, or `.js` file anywhere in the repo references the string
    `PROMOTION_REGISTRY` (verified by re-running the search restricted to those extensions).
- The migration-manifest checksums are the clinching evidence: the file's SHA-256
  (`f992505916...e555be7b2`) is **identical** in both
  `phase2c_pine_sha256_before_smoke.csv:10914` and `phase2c_pine_sha256_after_smoke.csv:10935` —
  the file was byte-for-byte unchanged across that whole migration/smoke window, i.e. observed
  proof of "never modified," not just "no writer code found."
- The dashboard's own file-read model (`MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py`,
  `READ_MODEL_FILES` tuple, lines 61–79) does not include `PROMOTION_REGISTRY.json` among the
  files it loads at all — the dashboard does not even read it, let alone write it.
- Conclusion: this is not a stubbed-but-wired writer and not a writer that silently no-ops — it
  is a file with **no code reference of any kind**, anywhere in the tracked tree. The registry
  was created (by hand or by a one-off script outside the repo) and never connected to anything.

**Readers:** none found. Repo-wide search for the filename in code (`.py/.ts/.tsx/.js`) returned
zero hits.

**Append-only vs mutable:** N/A — never written, so the question does not apply. The schema
itself (`promotions: []`) implies an append-only list was intended, matching the `promotions`
field name, but this was never exercised.

**§6.7 identity match:** N/A — no record shape exists to compare (the array has never held an
entry), so it neither matches nor mismatches `candidate_id` / `package_hash` /
`deployment_identity_hash`.

---

## 2. `05_REGISTRY/*.json` inventory

Directory listing (`C:\WFRES4\MTC_COMMAND_CENTER\05_REGISTRY`), 21 files total. Grouped below by
relevance to lifecycle/promotion state; every file's top-level schema was read directly.

### 2a. Directly lifecycle/promotion-relevant

| File | Top-level schema | Records | Count |
|---|---|---|---|
| `PROMOTION_REGISTRY.json` | `schema_version`, `promotions[]` | (never used — see §1) | 0 |
| `STRATEGY_REGISTRY.json` | `schema_version`, `generated_at`, `candidates[]` | (see below — also unused) | 0 |
| `STRATEGY_RESEARCH_REGISTRY.json` | `schema_version`, `generated_at`, `generator`, `strategies[]` | taxonomy/classification per strategy (`strategy_id`, `current_status`, `maturity_level`, `strategy_category`, `tags`, …) | 63 |
| `TRIAGE_CANDIDATE_REGISTRY.json` | `schema_version`, `generated_at`, `generator`, `source_worklist`, `summary`, `candidates[]` | per-candidate triage fields: `candidate_id` (e.g. `QLR_9ZJK8175drM`), `stg_code`, `recommended_next_step`, `eligible_for_retriage`, `coverage_status_*` | 172 |
| `VARIANT_LOG_REGISTRY.json` | `schema_version`, `generated_at`, `variants[]` | per-variant record incl. **`promotable` (bool)**, `validation_status`, `phase`, `research_run_id` | 20 |
| `RESEARCH_RUN_REGISTRY.json` | `schema_version`, `generated_at`, `research_runs[]` | per-run `research_run_id`, `status`, `outcome`, `tier`, `approval` | 6 |
| `RESEARCH_BACKTEST_REGISTRY.json` | `schema_version`, `generated_at: null`, `results[]` | (empty — 76-byte stub) | 0 |
| `TAG_DICTIONARY.json` | (not fully expanded; read by `research_reader.py:45`) | tag taxonomy | — |
| `AI_QUANTLENS_VERDICT_REGISTRY.json` | `schema_version`, `generated_at`, `model`, `description`, `entries[]` | per-strategy verdict: `strategy_id`, **`decision`** ∈ {`NEEDS_CLARIFICATION` (141), `RESEARCH_ONLY` (46), `SALVAGE` (25)}, `decision_label`, `blocking`, `next_action` | 212 |

### 2b. Present but not lifecycle-relevant (schema noted for completeness)

| File | Top-level schema | Notes |
|---|---|---|
| `AI_STRATEGY_NAME_REGISTRY.json` | `schema_version`, `generated_at`, `model`, `description`, `entries[]` (212) | display-name mapping, read by `ai_names_reader.py` |
| `AI_TASKS.json` | `schema_version`, `updated`, `intro`, `tasks[]` (5) | AI task prompts, read by `ai_tasks_reader.py`; referenced directly in `apps/web/app.js:568` |
| `AI_WORKER_REGISTRY.json` | `schema_version`, `workers[]` (3) | worker roster, not candidate state |
| `CASE_REGISTRY.json` | `schema_version`, `generated_at`, `cases[]` | empty stub (97 bytes) |
| `COMPONENT_REGISTRY.json` | `schema_version`, `generated_at`, `generator`, `components[]` (78) | reusable strategy components |
| `DATA_SOURCE_REGISTRY.json` | `schema_version`, `sources[]` | empty stub (51 bytes) |
| `INDICATOR_REGISTRY.json` | `schema_version`, `generated_at`, `generator`, `indicators[]` (27) | indicator taxonomy |
| `MTC_V2_INDICATOR_INVENTORY.md` | — | markdown, not JSON |
| `STRATEGY_PARAM_SPECS.json` | `schema_version`, `generated_utc`, `generator`, `source_of_truth`, `read_only: true`, `phase_legend`, `universe`, `execution_model`, `parity_contract`, `library_totals`, `strategies[]` (28) | parameter grids; declares its own `source_of_truth: "mega_walk_forward.GRIDS (code) + STRATEGY_PARAM_SPEC_ANNOTATIONS.json (curated overlay)"` and `read_only: true`, `generator: 03_QUANTLENS/tools/build_strategy_param_specs.py` — this file is explicit about *not* being the source of truth for parameters (the code grid is); it carries no promotion/lifecycle field |
| `STRATEGY_PARAM_SPEC_ANNOTATIONS.json` | `schema_version`, `authored_by`, `authored_utc`, `purpose`, `phase_legend`, `strategies{}` (21) | curated overlay feeding the above |
| `TW_EXPORT_REGISTRY.json` | `schema_version`, `exports[]` | empty stub (51 bytes) |

### 2c. `STRATEGY_REGISTRY.json` is a second, independently-dead stub — and the dashboard doesn't even read it

Content (full file):
```json
{"schema_version": "1.0", "generated_at": "2026-05-30T00:00:00+03:00", "candidates": []}
```
F-6 cites this file as corroborating evidence alongside `PROMOTION_REGISTRY.json` (master brief
line 433). But it is more than unused — it is **bypassed by design**. The dashboard's
`READ_MODEL_FILES` (`read_model.py:71`) does load it into
`files["strategy_registry"]["data"]`, but `build_dashboard_snapshot()` (`read_model.py:335`)
immediately **overwrites** that local variable with the return value of
`build_strategy_registry()` from a different module,
`MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/registry_reader.py:19-39`, which
builds its "strategy_registry" payload **entirely by scanning `03_QUANTLENS/` on disk** — a CSV
or JSONL candidate registry under `_registry/` (`registry_reader.py:42-49`) plus a live glob of
every `*/producer_spec.json` file (`registry_reader.py:198`) — and never opens
`05_REGISTRY/STRATEGY_REGISTRY.json` at all. The on-disk JSON is read once into a dict that is
then discarded before the HTTP response is built (`read_model.py:406`,
`"strategy_registry": strategy_registry` — the overwritten value, not `files["strategy_registry"]`).

### 2d. The real, non-empty "promotion status" store: `producer_spec.json`

**File pattern:** `MTC_COMMAND_CENTER/03_QUANTLENS/strategies/STGxxx_.../producer_spec.json` — one
file per strategy folder, 63 folders/files present (`C:\WFRES4\MTC_COMMAND_CENTER\03_QUANTLENS\strategies`).

Each file carries a `promotion_status` array field. Example,
`03_QUANTLENS/strategies/STG001_ql_alpha_ada_two_candle_sr_1h/producer_spec.json:64-67`:
```json
"promotion_status": [
  "PROMOTE_TO_FORWARD_PAPER_TRADE",
  "PROMOTE_TO_PARITY_CANDIDATE"
]
```
Surveyed all 63 files: **44 of 63 carry a non-empty `promotion_status`**, with values drawn from
`PROMOTE_TO_FORWARD_PAPER_TRADE`, `PROMOTE_TO_PARITY_CANDIDATE`, `FORWARD_PAPER_CANDIDATE`, and
`RESEARCH_GRADE`. This is real, populated lifecycle/promotion data — the opposite of F-6's
`PROMOTION_REGISTRY.json`.

**Writer:** `MTC_COMMAND_CENTER/03_QUANTLENS/tools/generate_producer_specs.py:618`
(`out_path = folder / "producer_spec.json"`) — auto-generates missing `producer_spec.json` files
for STG023+ strategies (file docstring, line 4). A second writer path exists for a related but
distinct artifact: `03_QUANTLENS/tools/build_profile_result_artifact.py:141-148` computes a
`promotion_status` value from `robust_final`/DSR/FDR flags (comment at lines 17-18: "a non-robust
PASS becomes RESEARCH_ONLY, never 'promoted'") and writes it via `target.write_text(...)` at
line 312, to an output directory resolved under the backtest root (`--output-dir`, default
resolved by `_resolve_under_backtest_root`, lines 240, 294) — **not** the same file as
`producer_spec.json`, so this is a second, separate promotion-status artifact family, not proven
to reconcile with the first.

**Readers (confirmed, with line numbers):**
- `registry_reader.py:198` globs `promoted_root.glob("*/producer_spec.json")`; `_strategy_from_spec()`
  at line 208 extracts `raw.get("promotion_status")` at **line 210** and folds it into a
  `status` string (`"|".join(...)`, line 212) that becomes part of the dashboard's
  `strategy_registry.strategies[]` payload.
- `pipeline_reader.py` reads `producer_spec.json` in multiple places: `_read_producer_spec()`
  (line 231-238), `_producer_spec_detail()` (line 242-247), `_iter_producer_specs()`
  (line 276-281, same glob pattern), and surfaces `row["producer_spec"]`,
  `row["producer_spec_summary"]`, `row["producer_spec_next_action"]`, etc. at lines 861-866 and
  928-934 — i.e. the dashboard's candidate-pipeline view is built in part from this file.

**Identity keys vs §6.7:** `producer_spec.json`'s own `candidate_id` field (e.g.
`"QL_ALPHA_ADA_TWO_CANDLE_SR_1H"`, line 2 of the STG001 example above) is a **stable,
human-readable slug**, not the `QLC-<yyyymmdd>-<8hex>` form §6.7 defines for `candidate_id`
(master brief line 1371). There is no `package_hash` or `deployment_identity_hash` field
anywhere in the file. **Match: no.**

### 2e. Writers for the other populated registries

- `TRIAGE_CANDIDATE_REGISTRY.json` — writer: `03_QUANTLENS/tools/build_triage_registry.py:40`
  (`OUT = MCC_ROOT / "05_REGISTRY" / "TRIAGE_CANDIDATE_REGISTRY.json"`); docstring line 10:
  "emits `05_REGISTRY/TRIAGE_CANDIDATE_REGISTRY.json`". Reader: `research_reader.py:49`.
- `STRATEGY_RESEARCH_REGISTRY.json`, and per its own docstring also `INDICATOR_REGISTRY.json`,
  `COMPONENT_REGISTRY.json`, `TAG_DICTIONARY.json` — writer:
  `03_QUANTLENS/tools/build_strategy_research_registry.py` (docstring lines 8-12 list all four;
  output-dict literal for `STRATEGY_RESEARCH_REGISTRY.json` at line 820). Reader:
  `research_reader.py:42-45`.
- `RESEARCH_RUN_REGISTRY.json` — reader: `research_reader.py:46`; validated (not generated) by
  `03_QUANTLENS/tools/validate_research_registries.py:45`. **Writer: not found in repo.** Searched
  `git grep`-style (Grep tool) for `RESEARCH_RUN_REGISTRY` across all `.py` files; only the
  validator and the reader reference it. No generator script exists in the tracked tree, so this
  file is either hand-maintained or was produced by a tool that was never committed.
- `RESEARCH_BACKTEST_REGISTRY.json` — reader: `research_reader.py:48`; validated by
  `validate_research_registries.py:49`. **Writer: not found in repo** (same search method as
  above); the file is a 76-byte empty stub (`results: []`, `generated_at: null`), consistent
  with never having been populated.
- `AI_QUANTLENS_VERDICT_REGISTRY.json` — read by `expert_quantlens_reader.py`. Its writer is
  documented as a **manual/AI-authoring procedure**, not a code generator:
  `03_QUANTLENS/_user_guide/13_AI_VERDICT_AUTHORING_PROCEDURE.md` (the only other repo hit for
  this filename). Entries carry a `source` field like
  `"codex_expert_quantlens_2026_06_08"`, consistent with hand/AI-session authorship rather than
  an automated pipeline.
- `VARIANT_LOG_REGISTRY.json` — read by `research_reader.py:47`. Writer not conclusively located
  in this pass (a template exists at `03_QUANTLENS/_templates/VARIANT_LOG_TEMPLATE.md`, implying
  manual/templated authorship rather than a build script); all 20 current `promotable` values are
  `false`, so even if this field were wired to `PROMOTION_REGISTRY.json` today it would add no
  entries.

---

## 3. Dashboard data files — `08_DASHBOARD_APP/`

**No dashboard-owned SQLite/DB files exist.** Searched `08_DASHBOARD_APP/` for `*.db` / `*.sqlite*`
— zero results. The dashboard (`apps/api/mcc_readonly/`) is architecturally a read-only
aggregator: every reader module (`registry_reader.py`, `research_reader.py`, `pipeline_reader.py`,
`scorecard_reader.py`, etc.) loads JSON from `MTC_COMMAND_CENTER/` subtrees (`05_REGISTRY/`,
`03_STATUS/`, `03_QUANTLENS/`) and assembles an in-memory snapshot; `build_read_model()`
(`read_model.py:94`) and `build_dashboard_snapshot()` (`read_model.py:327`) both stamp
`"mode": "read_only"` into their output (lines 142, 392), and `build_scorecard_detail()`'s
docstring states "Never reads arbitrary files or accepts paths."

**One exception — `mcc_readonly/writer.py`**, despite the package name, is a real write path, but
it writes **task-queue lifecycle**, not candidate/promotion lifecycle: `process_proposal()`
(lines 65-166) appends to `02_TASKS/TASK_QUEUE.json` (`TASK_RESOURCE`, line 15) and
`02_TASKS/TASK_HISTORY.json` (`TASK_HISTORY`, line 17), guarded by a file lock
(`_task_lock()`, lines 203-226) and JSON-schema validation (`_write_validated_json()`, line 243,
which backs up the previous file before an atomic `os.replace`, lines 249-267). This is a
genuine mutable, schema-validated, backed-up writer — but its subject is AI task state
(`VALID_TASK_STATES`, lines 19-29: `TODO`/`READY`/`IN_PROGRESS`/.../`DONE`/`ARCHIVED`), not
strategy/candidate promotion state. It is out of scope for this inventory except as a contrast:
it shows the codebase does know how to build a safe, validated, backed-up JSON writer when it
wants to — that pattern was simply never applied to `PROMOTION_REGISTRY.json`.

**Reader-only confirmation for the lifecycle-relevant registries:** `read_model.py`'s
`READ_MODEL_FILES` (lines 61-79) loads `strategy_registry` from `05_REGISTRY/STRATEGY_REGISTRY.json`
(dead — see §2c) but does not list `PROMOTION_REGISTRY.json`, `TRIAGE_CANDIDATE_REGISTRY.json`,
`VARIANT_LOG_REGISTRY.json`, or `AI_QUANTLENS_VERDICT_REGISTRY.json` — those are loaded by the
separate reader modules described in §2, not by the generic file-model loader.

---

## 4. Bridge store — `IBKR_PAPER_BRIDGE/`

**Implementation:** `IBKR_PAPER_BRIDGE/bridge/store/db.py` (10,124 lines), class `Store` at line
728. `IBKR_PAPER_BRIDGE/bridge/store/__init__.py` is a one-line docstring module
(`"""Persistence layer for the SQLite Store."""`) with no additional exports found.

**Schema versions present** (`db.py:268-308`):
```
SCHEMA_VERSION_BASELINE          = 4
SCHEMA_VERSION_PARTIAL_FILL      = 5
SCHEMA_VERSION_FULL_RECONCILE    = 6
SCHEMA_VERSION_DURABLE_RISK      = 7
SCHEMA_VERSION_EXPOSURE_CONTROLS = 8
SCHEMA_VERSION_KILL_EVIDENCE     = 9
```
`SUPPORTED_TARGET_SCHEMA_VERSIONS` includes all six (line 302-308). The operational baseline
stays at 4; versions 5-9 each require an explicit `initialize(target_schema_version=N)` call
(comment, lines 276-282) — i.e. this is a live, actively-migrated schema, not a frozen one.

**Tables** (every `CREATE TABLE` in the file, by line number): `meta` (916), `runs` (921),
`bars` (930), `decisions` (942), `orders` (954), `fills` (971), `trades` (982), `equity` (1010),
`risk_days` (1020), `directives` (1030), `llm_calls` (1042), `events` (1055),
`signal_fingerprints` (1064), `order_identity` (1072), `submission_attempts` (1118),
`submission_recovery_evidence` (1144), `partial_fill_recoveries` (1236),
`partial_fill_actions` (1279), `partial_fill_action_events` (1310),
`reconcile_attempts` (1555), `reconcile_components` (1605), `reconcile_diffs` (1640),
`reconcile_checkpoints` (1671), `funding_events` (1702), `risk_day_checkpoints` (2020),
`risk_control_latches` (2052), `kill_requests` (2277), `kill_attempts` (2302),
`kill_actions` (2321), `kill_action_events` (2341) — 29 tables total (excluding a handful of
in-test-fixture tables at lines 1377-1379, 2106-2112, 2424-2427 used only by the module's own
migration self-tests).

**Identity model:** `runs` is keyed by `run_id`; `decisions`/`orders`/`fills` key off
`decision_uid`/`cloid`/`trade_id`; nothing else. **Repo-wide search of `db.py` for
`candidate_id`, `package_hash`, or `deployment_identity_hash` returns zero matches.** The Bridge
store has no column, table, or field anywhere that names a strategy/candidate identity in the
§6.7 sense — its identity space is entirely execution-level (run/decision/order/trade), not
strategy-lineage-level. **Match to §6.7: no.**

**Writer:** `IBKR_PAPER_BRIDGE/bridge/app.py:26` (`from bridge.store.db import Store`);
instantiated at line 107 (`store = Store(store_path or root / "data" / "bridge.db")`),
initialized at line 108 (`store.initialize()`), and given its first state write at lines 109-110
(`store.set_meta("app_state", "DISARMED")` unless already `"KILLED"`).

**Reader:** `IBKR_PAPER_BRIDGE/bridge/api/routes.py:13` (same import); used throughout the file
via `store.get_bars()`, `store.get_trades()`, `store.get_decisions()`, `store.get_equity()`,
`store.get_events()`, `store.get_run()`, `store.get_latest_gates()` (lines 22-211) — this is the
Bridge's own HTTP/API layer surfacing its SQLite state, not the MCC dashboard.

**Append-only vs mutable:** mixed by table, evidenced directly in the DDL: `orders` and `trades`
have mutable status/price columns updated as fills arrive (`orders.status`, `orders.filled_qty`,
`orders.avg_fill_px`; `trades.exit_px`, `trades.exit_ts`, `trades.pnl` — all populated after row
creation); `fills`, `events`, `submission_attempts`, `kill_action_events`,
`partial_fill_action_events` read as append/event-log tables by naming and column shape
(`*_events` tables all carry a timestamp + fixed payload with no corresponding UPDATE path found
in this pass). A full statement-by-statement audit of every `UPDATE`/`INSERT` in the 10k-line
file was out of scope for this inventory; the table list and identity-column absence above are
the load-bearing, directly-observed facts.

---

## 5. Frozen planning-set assumptions (`764da27f:.../MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md`)

Read via `git -C C:\WFRES4 show 764da27f:MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md`
(3,237 lines).

### §6.7 — Candidate identity and evidence binding (lines 1364-1435)

Three-level identity split (repaired 2026-08-22 per the doc's own §0.3 item 4, "because the same
shipped strategy had several hashes and live evidence could not accumulate against one of
them," lines 1368-1370):

```
candidate_id        = QLC-<yyyymmdd>-<8 hex of source-provenance hash>   # family lineage, STABLE
package_hash        = SHA256( spec_json )                                # DEPLOYABLE STRATEGY SEMANTICS ONLY  (line 1373)
evaluation_run_hash = SHA256( package_hash + dataset/costs/sim/eval cfg )  # HOW IT WAS EVALUATED  (line 1381)
deployment_identity_hash = SHA256( package_hash + allocator/policy/guardian/runtime/adapter/costs )  # THE ECONOMIC/DEPLOYMENT IDENTITY (line 1390-1391)
run_id              = <deployment_identity_hash>.<environment>.<seq>     # one execution in one environment (line 1407)
```

Rules (lines 1414-1433):
- `package_hash` freezes strategy semantics and is a lineage component; **it does not by itself
  start or own a forward evidence clock** (line 1414).
- The forward clock starts only when the full `deployment_identity_hash` is minted and admitted
  for an environment (line 1415, cross-referencing §6.3/§11.5).
- Any change inside `package_hash` (parameters, modules, kernel version, instrument metadata)
  mints a new package **and therefore** a new `deployment_identity_hash` (line 1427). Any change
  to a component outside `package_hash` (allocator, Guardian threshold, `snapshot_deadline_ms`,
  broker adapter, fee schedule) mints a new `deployment_identity_hash` while leaving
  `package_hash` unchanged (line 1428).
- **Six evidence classes bind to the composite identity** (line 1431): `TrialRecord` rows
  (§11.2), deterministic replay artifacts (§11.3), eligibility verdicts (§6.5), environment
  admission decisions (§11.5), promotion decision artifacts (§11.5), and rollback records (§16
  M9). "An artifact of any of these classes without a `deployment_identity_hash` is unusable as
  evidence."
- **What is stamped where** (line 1433): the promotion decision artifact carries `package_hash`,
  `evaluation_run_hash`, and `deployment_identity_hash`; `OrderIntent`, every fill record, and
  every dashboard log line carry `package_hash` and `deployment_identity_hash`.
- `candidate_id` exists purely for family-level navigation and multiple-testing accounting,
  separate from `family_id` which handles leakage control (line 1432).

**Cross-check against what actually exists in the repo today:** none of the identity strings
observed in §2 and §4 above (`QLR_9ZJK8175drM`, `QL_ALPHA_ADA_TWO_CANDLE_SR_1H`, `Stg001`,
`NEW_VOL_BREAKOUT_CONFIRMED`, Bridge's `run_id`/`decision_uid`/`cloid`) match the
`QLC-<yyyymmdd>-<8hex>` form, and no file inspected in this pass contains a `package_hash` or
`deployment_identity_hash` field at all. The §6.7 scheme is a frozen planning-document design,
not yet implemented anywhere in the current codebase.

### §11.2 — Scalable artifact model / `TrialRecord` (heading at line 1898; contract defined at §11.1, line 1885)

`TrialRecord` is the artifact meant to close the gap the brief names explicitly at line 419:
> "What does not exist anywhere is a **unified, queryable, per-trial record carrying parameters,
> gate outcomes, rejection reasons and links to trade artifacts** — which is exactly the gap
> `TrialRecord` (§11.1) fills."

Design points found:
- One row per trial, Parquet format, DuckDB-queryable, including `rejection_reasons`,
  `search_regime`, `family_size`, `simulator_class`, and `deployment_identity_hash` (A-7,
  line 2700).
- Must be defined **before** any optimizer choice is made (line 1885 heading; C-3 correction,
  line 80: "`TrialRecord` contract defined before any optimizer choice... adaptive search changes
  the DSR/BH-FDR trial family").
- Scope-limited until "A-7b" passes: rows from the unmigrated canonical engine are stamped
  `SIGNAL_SCREEN_ONLY` and are explicitly **not acceptance evidence** for any gate (line 2700).
- Contracts-package skeleton item (line 2858): `TrialRecord` ships alongside `SizingRequest`,
  `BoundSizingIntent`, `OrderIntent`, `ExitIntent`, `StrategyPackage`, `AccountSnapshot`, and the
  §6.7 identity/hash formulae, versioned from the first commit, as **schema-only, no consumers
  wired** (T1 phase).
- A **Writer Inventory** is called out as a required Phase 0 task (line 421, O-15 at line 3115):
  catalogue every existing writer's unit of persistence, fields present/missing, format, and
  whether it should emit `TrialRecord` directly or be retired — "Designing the schema without
  this risks duplicating producers that already work." This inventory (this document) is
  effectively a partial answer to that same question, extended to lifecycle/promotion state
  rather than trial-level data.

**Cross-check:** `TrialRecord` does not exist in the repo today (no file, table, or schema found
under `06_SCHEMAS/`, `08_DASHBOARD_APP/`, or `IBKR_PAPER_BRIDGE/` matching that name) — it is a
planned artifact, not a built one.

### §11.5 — Admission decisions (lines 2035-2052; table context 2046-2048)

- **Environment Admission Authority** (WP-V2A-10) issues `SHADOW_ELIGIBLE` and `TESTNET_ELIGIBLE`
  admission decisions "from accepted eligibility evidence"; explicitly forbidden from admitting
  anything to mainnet/`LIMITED_LIVE` or producing eligibility evidence itself (line 2035).
- State table (lines 2046-2048): `SHADOW_ELIGIBLE` requires an accepted `SHADOW_ELIGIBLE`
  eligibility verdict set (§6.5, **WP-P0-21**) plus a frozen `package_hash` and
  `deployment_identity_hash`, issued by the Environment Admission Authority (V2A), and grants
  `FORWARD_SHADOW` only. `PROMOTED` requires the full statistical battery, forward evidence on
  the same `deployment_identity_hash`, the leakage record (§6.6, WP-P0-22), and the signed live
  gate — issued **only** by the Promotion Authority (V3), granting mainnet/`LIMITED_LIVE`.
- Rule (line 2052): "**Every admission decision is immutable and identity-bound.** It names
  `package_hash`, `deployment_identity_hash`, the eligibility verdict set it consumed, the
  issuer, the timestamp, and the exact environment set it admits to. **It is appended, never
  edited.**"

**Who writes/reads an admission decision, per the brief:** the Environment Admission Authority
(WP-V2A-10, a planned component) writes `SHADOW_ELIGIBLE`/`TESTNET_ELIGIBLE` decisions; the
Promotion Authority (V3, also planned) writes `PROMOTED`. Nothing in the current repo implements
either authority or an admission-decision store — this is entirely planning-document design.

### WP-P0-21 / WP-V2A-10 mentions found in the 764da27f brief

- **WP-P0-21** appears bound to eligibility verdicts: "An accepted `SHADOW_ELIGIBLE` eligibility
  verdict set (§6.5, **WP-P0-21**)" (line 2046).
- **WP-V2A-10** is the Environment Admission Authority package: "the **Environment Admission
  Authority** (**WP-V2A-10**, T0), which issues the `SHADOW_ELIGIBLE` decision the loader
  requires before a shadow package may load" (line 2611); also named directly at the table row,
  line 2035 (`**Environment Admission Authority** (WP-V2A-10)`).

---

## 6. Map #37 hybrid constraint (`feature/wayfinder-fold-20260823:.../WAYFINDER_DECISION_FOLD_2026-08-23.md`)

Read via `git -C C:\WFRES4 show feature/wayfinder-fold-20260823:MTC_COMMAND_CENTER/11_TRIAGE/WAYFINDER_DECISION_FOLD_2026-08-23.md`
(61 lines total).

**Exact settled text** (ticket #41 row, line 18):
> "[Re-home the state-store decision — old Package 1 §A.2 (#41)] **Store model DECIDED: hybrid**
> — per-worker SQLite stores are the source of truth; the supervisor owns only a derived
> registry + aggregate snapshot (never independent truth; explicit freshness/reconciliation
> policy); central Postgres stays a later separately-gated escalation. No new package: spec
> detail lands in WP-V2A-02 / WP-V2B-03 / WP-V2B-04; brief §17.2's ghost "§A.2" dependency
> re-points to this resolution."

Also referenced in the amendment index (line 45): "WP-V2A-02 (hybrid store: per-worker SQLite
source of truth)".

**What exactly is "hybrid" here, precisely as worded:**
1. **Per-worker SQLite** databases are the **source of truth** for whatever that worker owns.
2. A **supervisor** layer sits on top and owns only a **derived registry + aggregate snapshot** —
   explicitly never an independent source of truth, and required to carry an **explicit
   freshness/reconciliation policy**.
3. A **central Postgres** is deferred to a later, separately-gated escalation — not part of the
   near-term design.

**How this bears on what was found in §4 (Bridge store):** the Bridge's `IBKR_PAPER_BRIDGE/bridge/store/db.py`
SQLite implementation is consistent with side 1 of this hybrid model — it is exactly the shape of
a "per-worker SQLite store" the decision describes as the intended source of truth. **This
finding does not contradict the hybrid decision; it is prior art for it**, and its
`schema_version` history (4→9) shows the pattern already migrating in place. What the hybrid
decision does **not** resolve, and what this repo does not yet have, is side 2: no "supervisor
derived registry + aggregate snapshot" with an "explicit freshness/reconciliation policy" exists
today. The MCC dashboard (§3) is read-only and aggregates from `05_REGISTRY/`/`03_QUANTLENS/`
JSON files, not from the Bridge's SQLite store — it is not the supervisor the decision describes,
and none of the five-plus registries in §2 carry a freshness/reconciliation policy against each
other or against the Bridge store. The decision names where the *future* V2 architecture's
reconciliation should live (WP-V2A-02 / WP-V2B-03 / WP-V2B-04, none found in the repo as
implemented code); it does not itself perform any reconciliation of the stores inventoried in
this document.

---

## 7. Duplicate-recording risk

Every pair below is two stores that can each independently hold a value for the **same
real-world fact**, with **no reconciliation code found** connecting them (searched: cross-file
references by filename/field name between each pair; none found beyond what is cited).

1. **A strategy's promotion status** — `producer_spec.json`'s `promotion_status` field (§2d, 44
   of 63 files populated with values like `PROMOTE_TO_FORWARD_PAPER_TRADE`) vs.
   `05_REGISTRY/PROMOTION_REGISTRY.json`'s `promotions[]` array (§1, permanently empty). The
   dashboard reads and displays the `producer_spec.json` value (`registry_reader.py:210`,
   `pipeline_reader.py:861-866`) as if it were the authoritative promotion signal, while the file
   whose name says it owns exactly this fact has never received a single write. Nothing checks
   that a `PROMOTE_TO_FORWARD_PAPER_TRADE` in a `producer_spec.json` ever produced a
   corresponding row in `PROMOTION_REGISTRY.json`, because no code path connects the two files at
   all.

2. **The same fact, a second writer path** — `03_QUANTLENS/tools/build_profile_result_artifact.py:141-148`
   independently computes its own `promotion_status` (from `robust_final`/DSR/BH-FDR flags) and
   writes it to a separate output artifact under the backtest root
   (`_resolve_under_backtest_root`, lines 240/294), distinct from `producer_spec.json`. This is a
   **third** place the same conceptual fact can be written, with its own derivation logic (a
   non-robust PASS becomes `RESEARCH_ONLY`, comment lines 17-18) that need not agree with
   whatever value a human or another tool later writes into the corresponding
   `producer_spec.json`. No code was found that cross-validates the two.

3. **A candidate's "promotable" status, a fourth place** — `VARIANT_LOG_REGISTRY.json`'s
   `promotable` boolean field (§2, `variants[]`, currently 20/20 `false`). This is a structurally
   independent yes/no promotion signal, read by `research_reader.py:47` into the same
   `strategy_research` dashboard payload that also carries `producer_spec.json`-derived status via
   a different reader. Because every current value is `false`, no live conflict exists yet — but
   the schema is there, unconnected to `PROMOTION_REGISTRY.json`, and a future edit (someone
   flipping one `promotable` to `true`) would create a fourth disagreement surface with zero
   reconciliation code to catch it.

4. **A candidate's next-step / eligibility signal vs. a strategy's early-triage verdict** —
   `TRIAGE_CANDIDATE_REGISTRY.json`'s `recommended_next_step` / `eligible_for_retriage` fields
   (§2, 172 candidates, e.g. "Source audit / park") vs. `AI_QUANTLENS_VERDICT_REGISTRY.json`'s
   `decision` field (§2, 212 entries: `NEEDS_CLARIFICATION`/`RESEARCH_ONLY`/`SALVAGE`). Both
   registries express an opinion about whether a candidate should advance, keyed by different id
   schemes (`candidate_id` like `QLR_9ZJK8175drM` in one, `strategy_id` like
   `CAND_20260503_TED_ZHANG_MAGIC_ELIXIR_MOMENTUM_HAN1kymVbTc` in the other — different ID
   *namespaces*, not just different formats), written by different processes (one by
   `build_triage_registry.py`, the other by a documented manual/AI-authoring procedure in
   `03_QUANTLENS/_user_guide/13_AI_VERDICT_AUTHORING_PROCEDURE.md`), read into the same dashboard
   snapshot (`research_reader.py:46-58` reads both) with no code found that maps one candidate's
   entries across both registries or flags disagreement.

5. **`STRATEGY_REGISTRY.json` vs. the live-scanned "strategy_registry"** — a narrower but real
   instance of the same class of risk: the on-disk `05_REGISTRY/STRATEGY_REGISTRY.json` (empty)
   is loaded by `read_model.py:71` into `files["strategy_registry"]`, but silently discarded and
   replaced by `registry_reader.build_strategy_registry()`'s live filesystem scan
   (`read_model.py:335`, §2c above) before the value ever reaches the API response. Anyone editing
   `STRATEGY_REGISTRY.json` by hand, believing it feeds the dashboard, would see no effect — the
   two "sources" for the same key (`strategy_registry`) exist in the same request path with one
   silently overriding the other, and nothing in the code comments this override's rationale
   beyond the shadowing assignment itself.

**Root cause, common to all five:** none of these stores implement the "explicit
freshness/reconciliation policy" the Map #37 hybrid decision requires of a supervisor layer
(§6). The registries in `05_REGISTRY/` and the per-strategy files in `03_QUANTLENS/` were each
built by independent one-off or semi-automated tools (§2e) at different times, for different
immediate purposes (triage worklist, AI verdict authoring, parameter-grid export, producer-spec
generation), without a shared identity scheme (§6.7's `candidate_id`/`package_hash`/
`deployment_identity_hash` is not implemented by any of them) and without any tool that treats
one of them as canonical and the others as derived. F-6's own conclusion — "candidate identity
has no persistent home" — is the accurate summary: it is not that lifecycle state is nowhere
recorded, it is that it is recorded in multiple places that do not know about each other.

---

## Search methodology notes (for anything reported "not found")

- "Writer not found in repo" claims (`RESEARCH_RUN_REGISTRY.json`, `RESEARCH_BACKTEST_REGISTRY.json`,
  `VARIANT_LOG_REGISTRY.json`) were reached by grepping the exact filename string across all
  `.py` files in `C:\WFRES4` and confirming only validator/reader hits, no generator script.
- `PROMOTION_REGISTRY` code-reference absence was checked three ways: an unrestricted repo-wide
  grep, a grep restricted to `*.py`, and a grep restricted to `*.{ts,tsx,js}` — all three
  returned either the manifest/doc hits listed in §1 or nothing.
- `candidate_id` / `package_hash` / `deployment_identity_hash` absence in
  `IBKR_PAPER_BRIDGE/bridge/store/db.py` was checked with a direct grep for all three literal
  strings against the full 10,124-line file — zero matches.
- No `.db`/`.sqlite*` file exists under `08_DASHBOARD_APP/` — checked with a recursive filename
  search.
