# Backtest Artifact Reader Integration Report — 2026-06-15

Phase: Read-Only Backtest Artifact Contract + Profile-Separated Result Integration.
Reader + contract layer only. No backtests run, no artifacts generated, no write paths added.

## 1. Files changed
**New schemas (`06_SCHEMAS/`)**
- `run_plan.schema.json`
- `run_status.schema.json`
- `backtest_profile_result.schema.json`
- `artifact_index.schema.json`
- `top_results.schema.json`

**New reader**
- `08_DASHBOARD_APP/apps/api/mcc_readonly/night_artifacts_reader.py`

**New test**
- `08_DASHBOARD_APP/apps/api/tests/test_night_artifacts_reader.py` (7 cases)

**Edited (read-only extensions / wiring)**
- `08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py` — import + call `build_night_artifacts`, add `night_artifacts` snapshot key.
- `08_DASHBOARD_APP/apps/web/app.js` — accessors + wiring for Planner, Runs, Result Explorer, Leaderboard, Strategy Intelligence detail, Advanced Artifacts, Diagnostics, Read Model.
- `08_DASHBOARD_APP/apps/web/index.html` — cache bust `app.js?v=3` → `?v=4`.

**Handoff**
- `11_TRIAGE/BACKTEST_ARTIFACT_READER_INTEGRATION_REPORT_2026-06-15.md` (this file)
- `_AI_MEMORY/SESSION_LOG.md`, `_AI_MEMORY/NEXT_STEPS.md`, `_AI_MEMORY/ACTIVE_FILES.md`

## 2. Files intentionally NOT changed
- Pine scripts, `MTC_V2`, backtest engine core, broker/live/paper execution, strategy execution — untouched.
- `server.py` — already enforces read-only (POST/PUT/PATCH/DELETE → 405); no change needed.
- Existing readers (`backtest_reader.py`, `scorecard_reader.py`, etc.) — untouched.
- `styles.css` — no change required (reused existing components).

## 3. Artifact paths searched
Search root: `03_QUANTLENS/05_BACKTEST_RESULTS/` (resolved via `default_quantlens_root`).
Reader probes `05_BACKTEST_RESULTS/` itself + its most-recent immediate subdirectories (bounded `MAX_RUN_DIRS=150`, single shallow scan, no deep recursion). Per dir it checks for: `run_plan.json`, `run_status.json`, `artifact_index.json`, `backtest_profile_result.json`, `top_results.json`, `leaderboard_delta.json`, `benchmark_update_candidate.json`, plus companions `run_plan.md`, `approval_package.md`, `expected_artifacts.json`, `progress.json`, `heartbeat.json`, `summary.json`, `morning_report.md`.

## 4. Schemas added/updated
All 5 minimum schemas added under `06_SCHEMAS/` (repo convention). Required fields kept to identifying core; `metrics` block allows-but-not-requires net_profit / profit_factor / max_drawdown / win_rate / trade_count / buy_hold_return / buy_hold_alpha / sharpe / sortino / exposure / avg_trade / max_loss_streak. Profiles constrained to `SOURCE_NAKED | RISK_NORMALIZED | MTC_LIGHT | FULL_MTC_CANDIDATE`. Permissive `additionalProperties` so partial real files validate.

## 5. Readers added/updated
Single cohesive module `night_artifacts_reader.py` (matches repo's one-file-per-domain convention; logical sub-readers are functions: `_read_artifact`, `_extract_profile_rows`, `_search_dirs`, `_load_schema`). Guarantees:
- never writes (verified by `test_reader_does_not_write_files`)
- tolerates absent artifacts → structured `missing` list
- never crashes on invalid JSON → `state: "invalid"` + issues
- validates against schemas when present (`incomplete` on schema issues, `usable` when clean)
- bounded scan + `MAX_PARSE_BYTES=4MB` guard (large files marked incomplete, path linked, not embedded)

State model exposed per artifact: **absent / invalid / incomplete / usable**.

## 6. Snapshot fields added
New top-level `night_artifacts`:
```
run_plans[], run_status[], artifact_index[], profile_results[] (flattened official rows),
profile_result_files[], top_results[], leaderboard_delta[], benchmark_update_candidates[],
companions[], missing[], warnings[], summary{expected_types, present_types, missing_types,
files_found, invalid, incomplete, usable, profile_result_rows, has_profile_separated_results}
```

## 7. Frontend pages wired
- **Backtest Planner** — renders real `run_plan.json` (run id, strategies, profiles selected, timeframes, symbols, case count, parameter space, approval state, output dir, expected artifacts) when usable; else current pending state.
- **Backtest Runs** — adds "Run Status (artifact contract)" panel from `run_status.json` (status/stage/progress/workers/updated/output dir) when present; else current.
- **Backtest Result Explorer** — official buckets populate ONLY from `night_artifacts.profile_results`; KPI/delta columns (score/net profit/PF/max DD/B&H alpha/trades/robustness/promotion) with explicit `—` when absent; filters enable when profile rows exist; legacy rows stay quarantined under "Legacy Scorecard Reference — profile missing"; same-bucket warning retained.
- **Strategy Leaderboard** — "Validated Profile Winners" panel from profile rows / `leaderboard_delta.json` when present; else current "Top Gate 2 Reference" + warning.
- **Strategy Intelligence detail** — section 5 prefers profile-separated result preview (profile/symbol/tf/score/metrics) when present; else legacy result warning.
- **Advanced Artifacts** — Contract Summary + groups (Run Planning / Status·Heartbeat / Result Evidence / Leaderboard·Benchmark / Reports) with state badge + consumed-by + path from `night_artifacts`.
- **Diagnostics** — "Artifact Contract Diagnostics" (expected/present/missing/invalid/incomplete/usable/profile rows/reader status + warnings).
- **Read Model / Data Model** — `PAGE_FEEDS` updated to name `night_artifacts.*` feeds; snapshot-keys table auto-lists `night_artifacts`.

## 8. Missing artifacts found in current repo
No profile-separated / planning artifacts exist yet. Snapshot `night_artifacts.summary`:
`expected_types=14, present_types=1, missing_types=13, usable=0, invalid=0, profile_result_rows=0, has_profile_separated_results=false`.
Only `morning_report.md` companions are present (legacy reports). `missing` = run_plan.json, run_status.json, artifact_index.json, backtest_profile_result.json, top_results.json, leaderboard_delta.json, benchmark_update_candidate.json, run_plan.md, approval_package.md, expected_artifacts.json, progress.json, heartbeat.json, summary.json.

**Project-rule files referenced**: `03_QUANTLENS/_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md`, `11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md`, `11_TRIAGE/DASHBOARD_TARGETED_PATCH_REPORT_2026-06-15.md` present. `11_TRIAGE/DASHBOARD_DATA_AVAILABILITY_AUDIT_2026-06-15.md` — not located in repo (reported, continued).

## 9. Valid fixtures/tests added
`test_night_artifacts_reader.py` — temp-dir fixtures (no committed fake result files):
1. missing-all → structured missing states, no crash
2. valid `run_plan.json` → parsed, `usable`, fields present
3. valid `backtest_profile_result.json` → only official-profile row flattened, non-official dropped
4. invalid JSON → `invalid` state + issues, no crash
5. schema-incomplete → `incomplete` state
6. reader writes nothing (dir snapshot equal before/after)
7. real-root structure smoke

## 10. Test results
- New reader suite: **7 passed**.
- Full API suite: `Ran 46 tests ... OK` (was 39; +7).
- `node --check 08_DASHBOARD_APP/apps/web/app.js` → **JS_OK**.

## 11. Snapshot timing before/after
- Before phase: cold ~12.5s, warm ~1.1s.
- After phase: cold ~12.3s (`?refresh=1`), warm ~1.1s. No material regression (bounded shallow scan + size guard).

## 12. Remaining limitations
- No profile-separated artifacts exist → official buckets correctly remain empty; real KPIs not yet shown anywhere (by design, no fakes).
- `summary.json` / `progress.json` / `heartbeat.json` contract files captured as presence/companions; Runs page reads `run_status.json` for live status fields (none present yet).
- Cold snapshot still ~12s, dominated by existing readers (scorecards 837 rows, pipeline 176), not the new reader.
- Explorer filters render enabled when profile rows exist but are not yet interactive (no client-side filtering logic) — placeholder until artifacts arrive.

## 13. Recommended next phase
- Produce a real `run_plan.json` + `backtest_profile_result.json` + `top_results.json` for one validated strategy/profile (writer lives outside this read-only app) and confirm buckets populate end-to-end.
- Implement interactive Explorer filters once profile rows are real.
- Add a snapshot warm-up prefetch at server start to remove the ~12s cold first-load.
- Optionally split structured KPIs out of large result JSON into a `metrics.json` the reader can load cheaply.

---
**Safety confirmation**: No Pine/MTC_V2/backtest-engine/broker/live/paper/strategy-execution code touched. API still read-only (`POST /api/snapshot → HTTP 405`; `/healthz` `read_only=true overall_ok=true`). No KPIs fabricated; absent metrics render as `—`/explicit missing states.
