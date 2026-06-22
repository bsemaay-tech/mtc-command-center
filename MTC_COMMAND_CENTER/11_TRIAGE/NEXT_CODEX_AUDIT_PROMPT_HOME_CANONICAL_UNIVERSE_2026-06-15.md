# Codex Audit Prompt — Home Canonical Strategy Universe Patch (2026-06-15)

> Copy the block below into Codex to audit the completed Home canonical-universe patch.
> This is a prompt file only. Do not run Codex from here.

---

You are auditing a completed, read-only dashboard patch in the MTC Command Center repo.
Scope: `08_DASHBOARD_APP/apps/web/app.js`, `apps/web/index.html`, `apps/web/styles.css`,
and `08_DASHBOARD_APP/apps/api/tests/test_home_metric_invariants.py`. Do not modify code.
Verify and report PASS/FAIL with evidence for each item.

Context: A prior patch separated strategy-level metrics from raw scorecard-row counts but
inflated `Total Strategies` 176→212 by unioning pipeline ids with scorecard-only ids. The
follow-up patch redefines the Home Strategy Universe to the canonical pipeline/registry
universe and surfaces scorecard-only ids separately as orphan evidence.

Verify:

1. **Canonical Total** — `Total Strategies` uses the canonical universe: `canonicalStrategyIds()` draws from `candidate_pipeline.rows` (primary) and registry candidates only as a fallback when pipeline rows are empty. Confirm scorecard-only ids are NOT added.
2. **No scorecard-only inflation** — `strategyUniverse()` aliases `canonicalStrategyIds()`; no path adds scorecard-card ids to the strategy universe.
3. **Orphan ids shown separately** — `orphanScorecardIds()` = unique base ids in `scorecards.cards` absent from canonical universe; rendered on Home as "Scorecard-only Strategy IDs" in the Evidence / System Volume group.
4. **No overcount** — every strategy-level count (Gate 1 / 1B / 2 Passed, Gate 2 Failed, Paper Ready, Needs Review) is a per-id boolean over the canonical set, so none can exceed `Total Strategies`. Confirm against `/api/snapshot?refresh=1` (expected ~Total 176, orphans ~36).
5. **Row labels explicit** — Evidence group metrics carry `Rows` / `Runs` / `Indexed` / `Errors` / `Scorecard-only` labels and are visually separated from the Strategy Universe group; explanatory note present.
6. **Needs Review label matches logic** — the card is labelled "Needs Review Strategies" (not "Needs Attention"), with a tooltip/note stating it is a broad heuristic (pending/missing/fail/define/freeze in pipeline metadata), not a strict blocker count.
7. **Strategy Intelligence preserved** — `gate1Section()` still renders the best Gate 1 passing version card ("Showing best Gate 1 passing version" / "No Gate 1 passing version found") and the Advanced / All Versions table; no versions hidden, no faked metadata.
8. **API read-only** — no POST/PUT/PATCH/DELETE behavior added; `POST /api/snapshot` returns 405; `/healthz` reports read_only=true.
9. **No forbidden touches** — no changes to Pine, MTC_V2, backtest engine execution, broker/live/paper execution, or generation of `backtest_profile_result.json` / `top_results.json` / KPIs.
10. **Tests pass** — `node --check apps/web/app.js` passes; `python -m unittest discover tests` (from `08_DASHBOARD_APP/apps/api`, `PYTHONPATH=.`) passes, including `test_home_metric_invariants.py` (canonical total, orphan exclusion, no overcount, registry fallback).

Deliver a verdict: ACCEPT / ACCEPT WITH FOLLOW-UP / REJECT, with per-item evidence.
