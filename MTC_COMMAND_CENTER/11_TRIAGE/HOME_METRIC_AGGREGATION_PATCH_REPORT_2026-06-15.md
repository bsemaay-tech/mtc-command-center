# Home / Command Center Metric Aggregation Patch — 2026-06-15

## 1. Executive summary
Home metric cards previously mixed strategy-level counts with raw scorecard-row counts
(e.g. `Total Strategies 176` vs `Gate 1 Passed 646`), which is logically impossible if both
are strategy counts. Patch splits Home into two visibly distinct groups: **Strategy
Universe** (deduplicated by base strategy id) and **Evidence / System Volume** (raw
rows/runs/artifacts, explicitly labelled). All strategy-level counts are now per-id
booleans over the strategy universe, so none can exceed `Total Strategies`. Strategy
Intelligence Gate 1/1B section now surfaces the best Gate 1 passing version plus an
Advanced / All Versions table. Read-only; no execution/write/KPIs touched.

## 2. Initial git status / scope report
`git status --short` (worktree already dirty from prior accepted phases — NOT cleaned/reset per instruction):
- Tracked modified: `read_model.py`, `tests/test_readonly_core.py`, `apps/web/app.js`, `apps/web/index.html`, `apps/web/styles.css`, `_AI_MEMORY/*.md`.
- Renames (committed-staged): `apps/web/prototypes/* → 11_TRIAGE/ui_references/legacy_web_prototypes/*`.
- Untracked from earlier phases: `06_SCHEMAS/*.schema.json`, `night_artifacts_reader.py`, `build_run_plan.py`, `tests/test_build_run_plan.py`, `tests/test_night_artifacts_reader.py`, several `11_TRIAGE/*REPORT*.md`, plus unrelated repo noise (`HERMES/`, `Temp/`, transcript collectors, screenshots).

`git diff --stat` top: `app.js` (heavy churn from prior rebuild), `index.html`, `styles.css`, `read_model.py (+3)`, `test_readonly_core.py (+2/-1)`, `_AI_MEMORY/*`.

**Scope note:** dirty tree predates this task and spans prior accepted phases + unrelated untracked files. Per instruction nothing was cleaned/deleted/reset. This patch touches only the intended dashboard files (see #3).

## 3. Files changed (this patch)
- `08_DASHBOARD_APP/apps/web/app.js` — strategy-level aggregation helpers; Home rewritten into two metric groups + note; `gate1Section()` adds best Gate 1 passing version + All Versions table.
- `08_DASHBOARD_APP/apps/web/styles.css` — `.metric-group`, `.metric-group-head`, `.metric-note`; `.metric-grid` → responsive `auto-fit`.
- `08_DASHBOARD_APP/apps/web/index.html` — cache bump `app.js?v=5 → v=6`.
- `11_TRIAGE/HOME_METRIC_AGGREGATION_PATCH_REPORT_2026-06-15.md` — this report.

## 4. Aggregation logic before / after (verified on live snapshot)
| Metric (as shown on Home) | Before | After |
|---|---|---|
| Total Strategies | 176 (pipeline rows) | **212** (unique base ids across pipeline rows + scorecard cards) |
| Gate 1 "Passed" | **646** (scorecard ROWS, mislabelled as strategy count) | Strategy: **45** ; Rows: **646** (now in Evidence group) |
| Benchmark | **344** (rows) | Rows: **344** (Evidence group) |
| Gate 2 Failed | **143** (rows) | Strategy: **6** ; Rows: **143** (Evidence group) |
| Gate 2 Passed Strategies | — | **39** |
| Gate 1B Passed Strategies | — | **45** |
| Paper Ready Strategies | (row-based) | **1** |
| Needs Attention Strategies | (≤5, sliced bug) | **176** (deduped, full) |

Invariant check (script over `/api/snapshot?refresh=1`): **no strategy-level count > Total (212)** — confirmed `NONE`.

Note: `Total Strategies` rose 176→212 because the universe now unions strategy ids that appear in scorecard cards but not in pipeline rows. This is intentional — every id evaluated for a gate must be in the denominator, guaranteeing the no-overcount rule.

## 5. Strategy-level metric definitions (deduplicated by base id)
- **Total Strategies** — unique base strategy ids from pipeline rows ∪ scorecard cards.
- **Gate 1 Passed Strategies** — ≥1 associated version/scorecard with Gate 1 status pass/ok/accepted/passed/certified.
- **Gate 1B Passed Strategies** — ≥1 version with Gate 1B pass/ok.
- **Gate 2 Passed Strategies** — ≥1 version Gate 2 pass/ok **or** benchmark-candidate (any card `gate2.score ≥ 80`).
- **Gate 2 Failed Strategies** — Gate 2 evidence exists, no pass anywhere, and ≥1 version failed (conservative; excludes pending/absent).
- **Paper Ready Strategies** — row `scorecard_v2.gate_summary.promotable` or any card `gate_summary.promotable`.
- **Needs Attention Strategies** — pipeline row whose next_action/notes/canonical contains pending/missing/fail/define/freeze.

## 6. Evidence / system row metric definitions (raw, explicitly labelled)
- **Scorecard Rows** — `scorecards.cards.length` (837).
- **Gate 1 Passed Rows** — cards with Gate 1 pass status (646).
- **Benchmark Candidate Rows** — cards with `gate2.score ≥ 80` (344).
- **Gate 2 Failed Rows** — cards with Gate 2 fail status (143).
- **Backtest Runs** — `backtest_status.runs.length` (80).
- **Artifact Errors** — failed file diagnostics.
- **Reports Indexed** — `report_manifest.reports.length` (13).
All carry `Rows`/`Runs`/`Indexed`/`Errors` labels and may exceed strategy count by design.

## 7. Strategy Intelligence version display changes
`gate1Section()` now adds:
- **Primary Gate 1 Version** — `bestGate1PassingVersion(id)` (highest Gate 1 score among passing cards). Badge **"Showing best Gate 1 passing version"** when found, else **"No Gate 1 passing version found"** + clear missing state. Shows strategy_id, row/run/result id, symbol/universe, timeframe, profile, Gate 1 score/status, source artifact path — each with explicit missing markers where absent (no fabrication).
- **Advanced / All Versions** — table of every scorecard row for the strategy with Gate 1 / 1B / 2 PASS/FAIL/PENDING badges, score, asset/TF, profile, run. Other versions are never hidden.

## 8. Validation results
- `node --check app.js` → **JS_OK**.
- API suite → **Ran 55 tests … OK** (no API code changed; suite re-confirmed green).
- `/api/snapshot?refresh=1` → **200**; aggregation invariant verified (no overcount).
- `POST /api/snapshot` → **405** (write API still blocked).
- `/healthz` → read_only=true, overall_ok=true (unchanged from prior phase).

## 9. Safety confirmation
No backtests run. No `backtest_profile_result.json` / KPIs generated. No Pine / MTC_V2 /
backtest-engine / broker / live / paper execution touched. No write API added. No shell
redesign. Frontend aggregation + one CSS/cache change only. Missing data shown as explicit
empty states, never faked.

## 10. Remaining limitations
- `Total Strategies` (212) > pipeline-row count (176) because scorecard cards reference 36 strategy ids absent from the pipeline rows feed; surfaced rather than hidden. If the canonical universe must equal pipeline rows only, the union can be narrowed — flagged for product decision.
- Gate 1B / Gate 2 pass at strategy level depends on `gate_summary.statuses` keys (`gate1`, `gate1B`, `gate2`) being populated; strategies with absent statuses simply don't count (conservative).
- Best Gate 1 version metadata (profile, source_path, result id) shows missing markers where the scorecard row lacks those fields — data-availability gap, not UI.
- `Needs Attention` (176) is broad (keyword-based on pipeline rows); could be tightened to action-queue severity in a later pass.

## 11. Recommended next phase
- Confirm canonical strategy universe definition (pipeline-only vs union) with product, then lock `strategyUniverse()` accordingly.
- Add a small Python/JS unit harness for `strategyMetrics()` invariants (total ≥ each sub-count) so regressions are caught in CI rather than by manual snapshot script.
- Tighten `Needs Attention` to the action-queue/blocker model used elsewhere.
