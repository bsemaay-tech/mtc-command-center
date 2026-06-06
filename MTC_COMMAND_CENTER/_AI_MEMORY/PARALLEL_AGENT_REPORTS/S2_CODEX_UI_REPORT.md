# S2 Codex UI Report

## Completed tasks
- A5: Completed. Strategy detail now renders a collapsible Backtest Evidence details block from `row.scorecard_v2.gate2.metrics`. Only `status === "OK"` metrics produce cards; missing/incomplete Gate2 renders honest `No data`.
- A6: Completed. Strategy detail now renders a Not Promotable blocker panel when `gate_summary.promotable === false`, and a green Scorecard Promotable panel when true.
- A7: Completed. Pipeline strategy list now has Gate status filters: Gate2 PASS only, Gate3 Incomplete, Promotable Only, Blocked by Gate3. Rows without `scorecard_v2` remain visible by default.
- D4: Completed. Backtest rows are clickable and open an in-tab Night Run Detail panel with header, metrics, Gate2 split, artifact paths, candidate table fallback, and validation checklist.

## Files changed
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/app.js`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/index.html`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/styles.css`

No Pine, parity, MTC strategy logic, backtest engine, or API reader files were edited.

## app.js functions added or modified
- Modified `bindFilters()` around line 38 to bind `#pipelineGateFilter`.
- Modified `renderUnifiedStrategyDetail()` around lines 435-473 to place Promotability and Backtest Evidence after Scorecard.
- Added `renderPromotabilityPanel()` around line 944.
- Replaced/modified `renderBacktestEvidence()` around line 991 to use `scorecard_v2.gate2.metrics`.
- Added Gate2 evidence helpers around lines 1023-1089: `renderSharpeSortinoCard`, `renderEmaBenchmarkCard`, `renderEvidenceMetricCard`, `okMetricValue`, `formatMetricValue`.
- Modified `renderBacktest()` around lines 1712-1737 to support clickable run rows and detail panel.
- Added D4 helpers around lines 1740-1846: `renderNightRunDetail`, `nightRunArtifacts`, `renderArtifactPath`, `nightRunCandidates`.
- Modified `filterPipelineRows()` around lines 2157-2171.
- Added A7 helpers around lines 2174-2188: `scorecardV2ForRow`, `passesGateFilter`.

## Validation
- `node --check MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\app.js`: PASS.
- API tests requested command could not run in this environment because both available Python runtimes lack `pytest`:
  - `C:\Python314\python.exe: No module named pytest`
  - bundled Codex Python: `No module named pytest`
- Dashboard server started successfully:
  - `http://127.0.0.1:8765/healthz` returned `overall_ok: true`.
- DeepSeek adversarial review dispatch attempted with read-only task `C:\tmp\s2_codex_ui_review_task.json`, but harness could not start because both Python runtimes lack `openai`.

## Browser verification
- Opened `http://127.0.0.1:8765/dashboard` in the in-app Browser.
- Dashboard loaded healthy; observed 151 Pipeline rows and 80 Backtest rows.
- A7: Gate status filter exists and can select `gate3_incomplete`; existing rows stayed visible because current live scorecards are Gate3 incomplete/unscored.
- A6: Strategy detail rendered the Not Promotable blocker panel with failed/incomplete gates on a live scorecard row.
- A5: Backtest Evidence rendered the honest No data state on live scorecard rows. Current `/api/snapshot` scorecards do not expose `gate2.metrics` maps, so OK metric evidence cards could not be visually verified with real live data.
- D4: Clicking Backtest run `fam_templates_2026-06-06` rendered Night Run Detail with status, date, run type, total cells, candidates, workers, runtime, Gate2 split, artifact table, candidate-table fallback, and validation checklist.
- Browser console error log: empty.

## Skipped / caveats
- No API/backend reader changes were made, per S2 hard safety rules.
- No fabricated scorecard metrics were added. Because current live scorecard payloads contain empty `gate2.metrics`, the positive evidence-card visual path remains data-dependent.
