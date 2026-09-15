# Lane V — dashboard path model: derived locations vs the migrated layout (decision packet)

Scope: every reader module under `08_DASHBOARD_APP/apps/api/mcc_readonly/*.py`. Read-only —
no source, test, config, or launcher file was edited; no server was started. Builds on Lane L's
legacy-fallback review and Lane R1's nit on `f4455150` (both already merged in). Canonical example
config used throughout: `00_CONFIG/paths.example.json` → `mtc_v2_root = .../01_MTC_PROJECT`,
`pinets_root = .../12_PARITY_PINETS`, `reports_root = .../04_REPORTS` (values are Windows-absolute
in the file; this checkout maps each to the equivalent repo-relative directory per the task brief
and verifies with `test -d`/`ls`/`git ls-files`).

**Headline finding beyond Lane L/R1.** `pine_builder_reader.py:47` and `liveops_reader.py:59` each
compute `mtc_v2_root / "06_QUANTLENS_LAB" / "06_PROMOTED_TO_PARITY"` as their **only** path — unlike
`registry_reader.py`/`backtest_reader.py`, they have no `default_quantlens_root()` fallback and no
existence-gated alternate. Under the canonical config this branch is not a dead fallback, it is the
live, always-evaluated path, and `01_MTC_PROJECT` has no `06_QUANTLENS_LAB` — so both panels
(Pine Builder compile-status observations; LiveOps paper-trade plans) are **structurally always
empty** on a correctly configured checkout, silently, every run.

## Table: derived location vs canonical layout

| # | Reader(s) | File:line | Expression | Expected data | Exists under canonical (Y/N) | Migrated candidate (evidence) | Impact if missing |
|---|---|---|---|---|---|---|---|
| 1 | shared (`default_quantlens_root`) | `paths.py:25` | `root / "03_QUANTLENS"` | QuantLens lab root | **Y** | — (this is the migrated location itself; `03_QUANTLENS` has content: `05_BACKTEST_RESULTS`, `06_PROMOTED_TO_PARITY`, `_registry`, `strategies`, …) | none — this candidate always wins first |
| 2 | shared (`default_quantlens_root`) | `paths.py:26` | `root / "06_QUANTLENS_LAB"` | fallback QuantLens root | N | never valid in either layout (would be inside `MTC_COMMAND_CENTER` itself) | none — unreachable, candidate #1 always wins |
| 3 | shared (`default_quantlens_root`) | `paths.py:27` | `root.parent / "01_MASTER TEMPLATE_V2" / "06_QUANTLENS_LAB"` | legacy frozen-repo sibling | N (dir absent here; also outside the repo tree by construction) | N/A — cannot address the frozen `tradingview-lab` repo (see Lane R1) | none in this checkout — see Lane L for the "stray leftover on owner's machine" caveat |
| 4 | `mtc_v2_reader` | `mtc_v2_reader.py:19` | `mtc_root = resolve_configured_path(config, "mtc_v2_root")` | MTC_V2 root | **Y** (resolves to `01_MTC_PROJECT`, which exists) | already fixed — commit `79c77050` replaced the old hard-coded `root.parent / "01_MASTER TEMPLATE_V2"` that Lane L flagged; no further action needed here | n/a |
| 5 | `mtc_v2_reader` | `mtc_v2_reader.py:37` | `mtc_root / "01_PINE" / "MTC_V2.pine"` | MTC_V2 Pine source | **Y** — `01_MTC_PROJECT/01_PINE/MTC_V2.pine` exists | — | none |
| 6 | `mtc_v2_reader` | `mtc_v2_reader.py:38` | `mtc_root / "03_DOCS" / "MTC_V2_ARCHITECTURE.md"` | architecture doc | **Y** — exists | — | none |
| 7 | `mtc_v2_reader` | `mtc_v2_reader.py:251` | `mtc_root / "05_PARITY" / "MTC_V2_PARITY_CASES.csv"` | MTC_V2 parity tracker CSV | **Y** — `01_MTC_PROJECT/05_PARITY/MTC_V2_PARITY_CASES.csv` exists | — | none |
| 8 | `registry_reader` | `registry_reader.py:24-27` | `quantlens_root = mtc_v2_root / "06_QUANTLENS_LAB"` (fallback, only if #1 result is absent) | QuantLens candidates/strategies root | N (`01_MTC_PROJECT/06_QUANTLENS_LAB` absent) | dead branch here — `default_quantlens_root()` already resolves to `03_QUANTLENS` (row 1), so this fallback never fires in this checkout | would be `_empty_registry(...)` if it ever fired |
| 9 | `registry_reader` | `registry_reader.py:43-44` | `quantlens_root / "_registry" / "quantlens_candidate_registry.{csv,jsonl}"` | candidate registry | **Y** — both files exist under `03_QUANTLENS/_registry` | — | none |
| 10 | `registry_reader` | `registry_reader.py:83-86` | `quantlens_root / "01_TRIAGED_CANDIDATES"` / `"03_SALVAGE_IDEAS"` (folder-discovery fallback, only if CSV+JSONL both missing) | per-candidate folders | `01_TRIAGED_CANDIDATES` N, `03_SALVAGE_IDEAS` Y (3 entries) | dead branch — CSV from row 9 exists, so this never runs | would show `TRIAGED` rows only, never `SALVAGE_ONLY`, if it ever fired |
| 11 | `registry_reader` | `registry_reader.py:109-110` | `quantlens_root / "05_BACKTEST_RESULTS" / "{id}_{results.json,summary.md}"` | per-candidate backtest evidence | **Y** dir exists (per-file depends on candidate) | — | none structural |
| 12 | `registry_reader` | `registry_reader.py:203` | `quantlens_root / "06_PROMOTED_TO_PARITY"` | promoted strategies | **Y** — exists, has `producer_spec.json`-bearing folders | — | none |
| 13 | `backtest_reader` | `backtest_reader.py:32-34` | `quantlens_root = mtc_v2_root / "06_QUANTLENS_LAB"` (fallback, only if `default_quantlens_root()` result is absent) | same as row 8 | N | dead branch, same reasoning as row 8 | would be empty run list if it ever fired |
| 14 | `backtest_reader` | `backtest_reader.py:68,107` | `quantlens_root / "05_BACKTEST_RESULTS"` | backtest run artifacts | **Y** | — | none |
| 15 | `backtest_reader` | `backtest_reader.py:114` | `mtc_v2_root / "reports" / "optimization"` (unconditional, no fallback) | optimization `metrics.json` runs | **N** — `01_MTC_PROJECT/reports` does not exist | `01_MTC_PROJECT/optimization/**` exists (schema, jobs, parameter_library) but has a different internal shape and **no `metrics.json` anywhere in the repo** (`git ls-files \| grep -i metrics.json` → 0 hits) | `_collect_optimization_metrics` returns `[]` (guarded, fail-closed) — "optimization_metric_runs" always 0 |
| 16 | `optimization_reader` | `optimization_reader.py:27` | `optimization_root = mtc_v2_root / "reports" / "optimization"` (unconditional, no fallback) | optimization job runs/candidates/risk notes | **N** — same as row 15 | same candidate as row 15; no matching `metrics.json`/ranked-CSV convention found under `01_MTC_PROJECT/optimization/` | `build_optimization_status` returns `_empty_status(str(optimization_root))` — whole optimization panel empty, fail-closed |
| 17 | `pine_builder_reader` | `pine_builder_reader.py:17-21` | `mtc_v2_root = resolve_configured_path(...)`; then `mtc_v2_root.rglob("*.pine")` | Pine draft/core files | **Y** — `01_MTC_PROJECT` has `.pine` files under `01_PINE/` | — | none for the file listing itself |
| 18 | `pine_builder_reader` | `pine_builder_reader.py:47` | `promoted_root = mtc_v2_root / "06_QUANTLENS_LAB" / "06_PROMOTED_TO_PARITY"` (unconditional, **no fallback**) | `PINE_PARITY_PLAN.md` compile-status observations | **N** | `03_QUANTLENS/strategies/<STGxxx_id>/PINE_PARITY_PLAN.md` (3 strategies confirmed: STG001–STG003) | `_compile_observations` returns `{}` — drafts still list, but `compile_status` join is always empty (silent, not fail-closed with a visible reason) |
| 19 | `liveops_reader` | `liveops_reader.py:15-16` | `mtc_v2_root = resolve_configured_path(...)` | gate for whether to look for paper plans at all | **Y** (root itself exists) | — | none |
| 20 | `liveops_reader` | `liveops_reader.py:59` | `promoted_root = mtc_v2_root / "06_QUANTLENS_LAB" / "06_PROMOTED_TO_PARITY"` (unconditional, **no fallback**) | `FORWARD_PAPER_TRADE_PLAN.md` | **N** | `03_QUANTLENS/strategies/<STGxxx_id>/FORWARD_PAPER_TRADE_PLAN.md` (3 confirmed) | `_paper_trade_plans` returns `[]` — LiveOps "paper_trade_plans" list always empty, silently |
| 21 | `parity_reader` | `parity_reader.py:13,17-19` | `pinets_root / "_nightly" / "parity_results.json"`, `pinets_root / "parity_results.json"` | pinets nightly parity results | **Y** — both exist under `12_PARITY_PINETS` | — | none |
| 22 | `night_artifacts_reader` | `night_artifacts_reader.py:69-70` | `quantlens_root = default_quantlens_root(root)`; `results_root = quantlens_root / "05_BACKTEST_RESULTS"` | D1 night-run structured artifacts | **Y** | — | none |
| 23 | `scorecard_reader` | `scorecard_reader.py:23` | `default_quantlens_root(root) / "05_BACKTEST_RESULTS"` | scorecard_v2 JSON files | **Y** | — | none |
| 24 | `system_test_reader` | `system_test_reader.py:41-42` | `quantlens_root / "system_test"` | fake-money benchmark replay runs | N | git-ignored runtime output by design (docstring: "git-ignored runtime output") — **not a migration mismatch**, honest empty state until a run is launched | none (already the documented, intended empty state) |
| 25 | `pipeline_reader` | `pipeline_reader.py:213-214` | `default_quantlens_root(mcc_root) / "06_PROMOTED_TO_PARITY"` | promoted-strategy join source | **Y** | — | none |
| 26 | `pipeline_reader` | `pipeline_reader.py:139-141` | `quantlens_root`, `quantlens_root / "00_INBOX_REPORTS"`, `quantlens_root / "research"` | source-record scan roots | **Y** — both subdirs exist under `03_QUANTLENS` | — | none |
| 27 | `quantlens_reader` | `quantlens_reader.py:180,188` | `ql_root / "03_SALVAGE_IDEAS"`, `ql_root / "strategies"` | Quantlens Verdicts candidate folders | **Y** — both exist | — | none |
| 28 | `audit_reader` | `audit_reader.py:87,970,1068` | `quantlens_root = default_quantlens_root(root)` (+ `root` as second scan root) | transcript/source-record intake scan | **Y** | — | none |
| 29 | `research_reader`, `ai_names_reader`, `ai_tasks_reader`, `param_specs_reader`, `expert_quantlens_reader` | `research_reader.py:19`; `ai_names_reader.py:10`; `ai_tasks_reader.py:14`; `param_specs_reader.py:18`; `expert_quantlens_reader.py:10` | `mcc_root / "05_REGISTRY" / "<file>.json"` | Strategy Research Lab registries | **Y** — `05_REGISTRY/` exists at `mcc_root` (not `mtc_v2_root`-relative) with all five named files | — | none — this family is unaffected by the `mtc_v2_root`/`quantlens_root` migration question entirely |
| 30 | `presentation_reader` | `presentation_reader.py:52-53` | `mcc_root / "11_TRIAGE" / "strategies" / "_stg_code_map.json"` | STG-code lookup map | **Y** — exists | — | none |
| 31 | `server` | `server.py:118` | `root / "04_REPORTS"` (mcc_root-relative; security boundary for `_send_report`) | report-serving containment root | **Y** — `04_REPORTS/` exists at `mcc_root` | — | none |
| 32 | `health`, `parity_reader` (`PATH_KEYS` display only) | `health.py:12-17`, `parity_reader.py:11-18` | `resolve_configured_path(config, "reports_root")`, `"tradingview_exports_dir"` | diagnostic existence display only | config values point at `04_REPORTS` and `12_PARITY_PINETS/TW_EXPORT_CASES_V2`, both **Y** on disk | — | **orphaned config keys**: no reader actually derives a data path from `reports_root` or `tradingview_exports_dir` — they are read only for the health/parity path-check display, never joined into any `build_*` function's file lookups. Not a "missing location" bug, but the two keys currently do nothing beyond a health-panel checkmark. |

31 substantive rows (32 counting the header notes row) covering every reader module in
`mcc_readonly/*.py` that derives a filesystem location from `mcc_root`, `mtc_v2_root`,
`quantlens_root`, `pinets_root`, `reports_root`, or a hard-coded sub-path. `writer.py`, `schema.py`,
`task_lifecycle.py`, `validation_reader.py`, `cli.py`, `json_io.py`, `__main__.py`, `__init__.py`
were checked and derive no additional root-relative business-data path (verified by grep, not
reproduced as rows).

**Live, always-firing gaps under the canonical config**: rows 15, 16, 18, 20 (4 locations).
**Dead/unreachable fallback branches** (only misleading if someone reads the source without
tracing reachability): rows 2, 3, 8, 10 (partial — the folder-discovery fallback would be
half-correct if it ever fired, since `03_SALVAGE_IDEAS` exists but `01_TRIAGED_CANDIDATES` does
not). Everything else resolves correctly today.

## Diagnostics run (read-only, from `apps/api`, venv312, `PYTHONUTF8=1`)

`health` against this worktree shows `mtc_v2_root_reachable: false` and every configured path
`exists: false` — but this is a **sandbox/platform artifact**, not evidence about the migrated
layout: `paths.example.json` stores Windows-absolute values (`C:/LAB/...`), and `canonicalize()`
(`Path(...).resolve()`) treats `C:/LAB/...` as a *relative* path segment on Linux, so it resolves
to `.../apps/api/C:/LAB/...` under the cwd — never a real directory on this checkout regardless of
migration state. The table above instead maps each config value to its intended repo-relative
directory (per the task brief) and checks that with `test -d`/`ls`. Quoting the diagnostics anyway
since they corroborate the empty-panel behavior end-to-end:

```
backtest-status  -> summary.total_runs: 0, optimization_metric_runs: 0, discovered_runs: 0
optimization-status -> source: ".../01_MTC_PROJECT/reports/optimization", all counts 0
parity-status    -> source: "parity_results_missing" (pinets_root also unresolvable on Linux
                     under the Windows-absolute example value; rows 21 above use test -d instead)
```

## Decision packet

### Group A — rows 15, 16 (`backtest_reader.py:114`, `optimization_reader.py:27`): `mtc_v2_root/"reports"/"optimization"`

- **Option A (repoint).** Change both lines to `mtc_v2_root / "optimization"` and adopt whatever
  the real overnight/optimization runner actually writes under `01_MTC_PROJECT/optimization/**`
  (today: `schema/`, `jobs/`, `parameter_library/` — no `metrics.json` output convention yet exists
  anywhere in the repo, so this option is only a *directory* rename until a runner starts emitting
  `metrics.json`/ranked CSVs there). Tests to change: `test_backtest_reader.py` (optimization-metrics
  fixture directory), `test_optimization_reader.py` (whole fixture tree, `optimization_reader.py:27`'s
  companion `_collect_top_candidates`/`_collect_risk_notes`/`_worker_benchmark`/`_artifact_summary`
  helpers all key off `optimization_root`, so the fixture's directory literal moves but assertions
  are unchanged).
- **Option B (keep, document as legacy-only panel).** Leave the path as-is and record in
  `AGENTS.md`/`HANDOFF.md` that the Optimization panel is empty until an `optimization_root` config
  key (or a real runner writing to `01_MTC_PROJECT/optimization/reports/`) exists. Zero code risk,
  but the panel stays permanently empty on every correctly configured checkout today.
- **Option C (retire the panel).** Remove `optimization_reader`/the optimization section of
  `backtest_reader` from `read_model.py` until a real optimization-run artifact format is decided.
  Overkill — the panel is fail-closed already (empty, not wrong), so retiring loses information value
  for zero safety gain.
- **Recommendation: B now, A once the owner confirms where `metrics.json`/ranked CSVs actually land
  post-migration** — a real runner needs to exist and write somewhere first; renaming the reader
  path without a producer is cosmetic. **Risk: low** either way (fail-closed today, stays fail-closed).

### Group B — rows 18, 20 (`pine_builder_reader.py:47`, `liveops_reader.py:59`): `mtc_v2_root/"06_QUANTLENS_LAB"/"06_PROMOTED_TO_PARITY"`

- **Option A (repoint to `default_quantlens_root()`).** Both functions already import
  `resolve_configured_path`; add `from .paths import default_quantlens_root` and replace
  `mtc_v2_root / "06_QUANTLENS_LAB" / "06_PROMOTED_TO_PARITY"` with
  `default_quantlens_root(root) / "06_PROMOTED_TO_PARITY"` (matching the pattern already used by
  `pipeline_reader.py:214`, `registry_reader.py:203`) — but the actual `PINE_PARITY_PLAN.md` and
  `FORWARD_PAPER_TRADE_PLAN.md` files now live under `03_QUANTLENS/strategies/<id>/`, **not**
  `03_QUANTLENS/06_PROMOTED_TO_PARITY/<id>/` (verified: `06_PROMOTED_TO_PARITY` holds
  `PARITY_EXECUTION_CHECKLIST.md`/`PARITY_RESULTS.md`/`PROMOTION_INDEX.md`, not per-candidate plan
  files). So the correct repoint is `default_quantlens_root(root) / "strategies"`, glob
  `*/PINE_PARITY_PLAN.md` and `*/FORWARD_PAPER_TRADE_PLAN.md` respectively. Tests to change:
  `test_pine_builder_reader.py:19-20,62` (fixture moves from
  `mtc/"06_QUANTLENS_LAB"/"06_PROMOTED_TO_PARITY"` to a `strategies/<id>/` fixture tree);
  `test_liveops_reader.py:19,85` (same fixture reshape).
- **Option B (keep, document as legacy-only panels).** Record that Pine Builder's compile-status
  annotations and LiveOps's paper-trade-plan list are silently empty on every correctly configured
  checkout; no code change. Cheapest, but leaves two panels that look like "nothing to show" when
  the real data (3 strategies' worth) exists one directory segment away.
- **Option C (retire).** Not appropriate — the surrounding panels (draft list, LiveOps status) still
  carry real, correct data; only the cross-reference join is broken.
- **Recommendation: Option A.** This is a genuine, silent, always-firing bug (not a guarded
  fallback) with a confirmed migrated candidate and existing test fixtures to reshape — same shape
  of fix as the already-merged `mtc_v2_reader.py:19` repoint (commit `79c77050`). **Risk: low** —
  fail-closed either way (empty list vs. populated list), and the new path is verified present.

### Group C — rows 2, 3, 8, 10, 13 (dead `06_QUANTLENS_LAB` / `01_MASTER TEMPLATE_V2` fallback branches in `paths.py`, `registry_reader.py`, `backtest_reader.py`)

- Already analyzed in depth by Lane L (`OVERNIGHT_LANE_L_DASHBOARD_LEGACY_FALLBACKS_2026-09-07.md`)
  with an illustrative diff and the same A/B options; this lane's `test -d` checks corroborate Lane
  L's findings exactly (both `06_QUANTLENS_LAB` and `01_MASTER TEMPLATE_V2` are absent here, and
  `03_QUANTLENS` wins immediately). **Recommendation: defer to Lane L's packet** — no new
  information to add beyond confirming the folder-discovery fallback (row 10) would be
  half-correct (`03_SALVAGE_IDEAS` exists, `01_TRIAGED_CANDIDATES` does not) if it ever fired.

### Group D — row 32 (`reports_root`, `tradingview_exports_dir` configured but unused by any reader)

- **Option A (wire them in or remove them).** Either make a reader consume `reports_root` (e.g.
  `server.py:118`'s hard-coded `root / "04_REPORTS"` could instead call
  `resolve_configured_path(config, "reports_root")` for parity with `mtc_v2_root`/`pinets_root`) or
  drop the two keys from `paths.example.json`/`paths.local.example.json` and `health.py`'s
  `PATH_KEYS`/`parity_reader.py`'s `PATH_KEYS` tuple so the health panel doesn't imply they gate
  anything. Tests to change: none currently assert on `reports_root` consumption, so this is
  additive either way.
- **Option B (keep, document as reserved/future keys).** Leave as-is; note in `AGENTS.md`/`INPUTS.md`
  that `reports_root`/`tradingview_exports_dir` are health-check-only today.
- **Option C (retire).** Not applicable — these are config keys, not panels.
- **Recommendation: B.** Low priority, cosmetic; not worth touching until a reader actually needs
  a configurable reports/exports root. **Risk: none** — these keys currently do nothing either way.

## Commands executed

```
git log --oneline -1 ; git merge-base --is-ancestor 234c7188 HEAD ; git merge --ff-only 234c7188
grep -n -E "mcc_root|mtc_v2_root|quantlens_root|reports_root|pinets_root|tradingview_exports_dir" mcc_readonly/*.py
find 03_QUANTLENS -maxdepth 1 -type d ; find 01_MTC_PROJECT -maxdepth 1 -type d
find 12_PARITY_PINETS -maxdepth 2 -type d ; find 04_REPORTS -maxdepth 2
test -d 03_QUANTLENS/_registry ; test -d 03_QUANTLENS/01_TRIAGED_CANDIDATES ; test -d 03_QUANTLENS/03_SALVAGE_IDEAS
git ls-files | grep -i "parity_results\|metrics.json\|PINE_PARITY_PLAN\|FORWARD_PAPER_TRADE_PLAN"
find 03_QUANTLENS/06_PROMOTED_TO_PARITY -iname "PINETS_PARITY_RESULT.json"
python -m mcc_readonly --mcc-root <worktree>/MTC_COMMAND_CENTER health|backtest-status|optimization-status|parity-status
Read: paths.py, mtc_v2_reader.py, registry_reader.py, backtest_reader.py, optimization_reader.py,
pine_builder_reader.py, liveops_reader.py, parity_reader.py, night_artifacts_reader.py,
scorecard_reader.py, system_test_reader.py, pipeline_reader.py, quantlens_reader.py, audit_reader.py,
research_reader.py, server.py, health.py, presentation_reader.py, json_io.py, writer.py,
validation_reader.py (grep only), cli.py (grep only)
```

No source changed; no server started.

WAITING FOR OWNER: choose A/B/C per reader
