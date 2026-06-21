# Home Canonical Strategy Universe Patch — Report — 2026-06-15

## 1. Executive summary
Overnight bounded maintenance queue. Resolved the product ambiguity from the prior Home
aggregation patch: `Total Strategies` had grown 176→212 by unioning pipeline ids with
scorecard-only ids. Now the user-facing Strategy Universe uses the **canonical** count
(pipeline rows primary; registry candidates fallback only when pipeline is empty).
Scorecard-only ids are surfaced separately as orphan evidence. Added a Python invariant
test mirroring the JS aggregation, renamed the broad "Needs Attention" metric to "Needs
Review" with an explanatory tooltip/note, and preserved the Strategy Intelligence Gate 1
version work. Read-only throughout; no execution/write/KPI changes. All validation green.

## 2. Initial git status / scope report
`git status --short` / `git diff --stat` (PHASE 0; nothing cleaned/staged/committed/reset):
- Tracked modified (this + prior phases): `apps/api/mcc_readonly/read_model.py`, `apps/api/tests/test_readonly_core.py`, `apps/web/app.js`, `apps/web/index.html`, `apps/web/styles.css`, `_AI_MEMORY/*.md`.
- Staged renames (prior phase): `apps/web/prototypes/* → 11_TRIAGE/ui_references/legacy_web_prototypes/*`.
- Untracked from prior phases: `06_SCHEMAS/*.schema.json`, `night_artifacts_reader.py`, `build_run_plan.py`, `tests/test_build_run_plan.py`, `tests/test_night_artifacts_reader.py`, several `11_TRIAGE/*REPORT*.md`.
- Unrelated untracked repo noise (left untouched per stop conditions): `../HERMES/`, `../MCC_COMMAND_CENTER/`, `Temp/`, `YT_TRANSCRIPT_COLLECTOR/`, screenshots, etc.

**Scope note:** dirty tree predates this task and spans prior accepted phases + unrelated untracked files. Nothing was cleaned/deleted/reset/moved. This patch touched only the Home aggregation + a new test + report/handoff/audit-prompt files.

## 3. Files changed (this patch)
- `08_DASHBOARD_APP/apps/web/app.js` — `metric()` gains optional `title`; "Needs Attention Strategies" → "Needs Review Strategies" + tooltip; metric note extended. (Canonical helpers `canonicalStrategyIds`/`strategyUniverse` alias/`orphanScorecardIds` + "Scorecard-only Strategy IDs" card already landed in the prior canonical patch and are unchanged here.)
- `08_DASHBOARD_APP/apps/web/index.html` — cache bump `app.js?v=7 → v=8`.
- `08_DASHBOARD_APP/apps/api/tests/test_home_metric_invariants.py` — **new** invariant test (mirrors JS aggregation).
- `11_TRIAGE/NEXT_CODEX_AUDIT_PROMPT_HOME_CANONICAL_UNIVERSE_2026-06-15.md` — **new** copy-ready audit prompt.
- `11_TRIAGE/HOME_CANONICAL_UNIVERSE_PATCH_REPORT_2026-06-15.md` — this report.
- `_AI_MEMORY/{SESSION_LOG,NEXT_STEPS,ACTIVE_FILES}.md` — updated.

## 4. Canonical strategy universe definition
`canonicalStrategyIds()`:
1. Primary: unique base ids from `candidate_pipeline.rows`.
2. Fallback: unique base ids from registry candidates/strategies **only if** pipeline rows are empty/unavailable.
3. Scorecard-only ids are **never** added.
`strategyUniverse()` aliases this; all strategy-level metrics iterate it. Because
`cardsForStrategy(id)` matches only cards whose base id equals a canonical id, orphan
cards cannot contribute to any strategy-level count.

## 5. Scorecard-only / orphan id definition
`orphanScorecardIds()` = unique base strategy ids present in `scorecards.cards` but absent
from the canonical universe. Rendered as **Scorecard-only Strategy IDs** in the Evidence /
System Volume group. Represents scorecard evidence with no matching pipeline/registry
strategy (legacy/orphan), pending promotion into the registry/pipeline.

## 6. Before / after Home metrics (live `/api/snapshot?refresh=1`)
| Metric | Aggregation patch (union) | This/canonical patch |
|---|---|---|
| Total Strategies | 212 | **176** (source: pipeline) |
| Gate 1 Passed Strategies | 45 | **10** |
| Gate 1B Passed Strategies | 45 | **10** |
| Gate 2 Passed Strategies | 39 | **5** |
| Gate 2 Failed Strategies | 6 | **5** |
| Paper Ready Strategies | 1 | **0** (the 1 was an orphan id) |
| Needs Review Strategies | 176 (as "Needs Attention") | **176** (relabelled + tooltip) |
| Scorecard-only Strategy IDs | — | **36** (Evidence group) |
| Scorecard Rows / Backtest Runs / Reports | 837 / 80 / 13 | 837 / 80 / 13 |

Overcount check (shared mirror module): **NONE** — no strategy-level count > Total 176.

## 7. Strategy-level metric definitions (canonical ids only)
- **Total Strategies** — canonical pipeline (fallback registry) base ids.
- **Gate 1 / 1B Passed** — ≥1 associated version/scorecard with that gate status pass/ok/accepted/passed/certified.
- **Gate 2 Passed** — ≥1 version Gate 2 pass/ok **or** benchmark candidate (any card `gate2.score ≥ 80`).
- **Gate 2 Failed** — Gate 2 evidence exists, no pass anywhere, ≥1 version failed (conservative).
- **Paper Ready** — row `scorecard_v2.gate_summary.promotable` or any card `gate_summary.promotable`.
- **Needs Review** — canonical strategy whose pipeline next_action/notes/canonical mentions pending/missing/fail/define/freeze (broad heuristic; see §9).

## 8. Evidence / system metric definitions (raw, labelled)
- **Scorecard Rows** — `scorecards.cards.length` (837).
- **Gate 1 Passed Rows** — cards with Gate 1 pass status (646).
- **Benchmark Candidate Rows** — cards `gate2.score ≥ 80` (344).
- **Gate 2 Failed Rows** — cards with Gate 2 fail status (143).
- **Backtest Runs** — `backtest_status.runs.length` (80).
- **Reports Indexed** — `report_manifest.reports.length` (13).
- **Scorecard-only Strategy IDs** — orphan ids (36).
- **Artifact Errors** — failed file diagnostics.

## 9. Needs Attention / Needs Review logic (PHASE 3)
Current logic is a broad keyword match over pipeline-row `next_action` + `notes` +
`canonical` JSON for `pending|missing|fail|define|freeze`. No reliable separate
action-queue/blocker model exists to replace it. Per stop-conditions ("do not fake
precision"), the count is kept conservative but the label was changed
**"Needs Attention Strategies" → "Needs Review Strategies"**, with a hover tooltip and a
sentence in the metric note clarifying it is a broad heuristic (review/rule-freeze needed),
not a strict blocker count. The label now matches the logic; it does not imply all 176 are
broken.

## 10. Strategy Intelligence preservation check (PHASE 4)
`gate1Section()` is unchanged this phase. Preserved: best Gate 1 passing version card
("Showing best Gate 1 passing version" / "No Gate 1 passing version found"), full metadata
fields with explicit missing markers, and the Advanced / All Versions table (G1/G1B/G2
PASS/FAIL/PENDING). No versions hidden; no faked metadata.

## 11. Validation results (PHASE 6)
- `node --check app.js` → **JS_OK**.
- API suite → **Ran 60 tests … OK** (+5 new `test_home_metric_invariants.py`; +prior builder/night-artifact tests).
- `/api/snapshot?refresh=1` → **200**; canonical Total=176, orphans=36, no overcount (verified via shared mirror module).
- `POST /api/snapshot` → **405** (write blocked).
- `/healthz` → **200** (read_only=true).
- **Visual QA: not performed** — no interactive browser available in this session. Relied on `node --check`, the invariant test, and live snapshot validation. Recommend a manual browser pass on Home / Strategy Intelligence / Result Explorer.

## 12. Safety confirmation
No backtests, no optimization, no `backtest_profile_result.json` / `top_results.json`, no
fake KPIs. No Pine / MTC_V2 / backtest-engine / broker / live / paper execution touched. No
POST/PUT/PATCH/DELETE behavior added (`POST`→405). No unrelated files cleaned/deleted/
reset/moved. Frontend aggregation/label + one test + docs only. Missing/orphan data shown
explicitly, never faked.

## 13. Remaining limitations
- Registry fallback path is exercised only by the unit test; live data has pipeline rows, so the fallback branch is unobserved in production.
- `Scorecard-only Strategy IDs` (36) is a count only; no drill-down list of the orphan ids yet.
- `Needs Review` remains a broad heuristic; a precise blocker/action-queue model is not available and was intentionally not faked.
- The invariant test mirrors the JS logic in Python rather than executing the JS directly; if `app.js` aggregation changes, the mirror must be updated in lockstep (documented in the test header).

## 14. Recommended next phase
- Optional orphan drill-down panel + a defined promotion path for scorecard-only ids into the registry/pipeline.
- Consider a real action-queue/blocker model so "Needs Review" can become a precise count.
- A lightweight JS test harness (e.g. jsdom) to execute `app.js` aggregation directly and retire the Python mirror.
- (Deferred, NOT tonight) real `backtest_profile_result.json` / `top_results.json` writer outside the read-only app to populate official Result Explorer buckets.
