# Lane S report — WP-P0-18 chart-library POC

## Status

**IMPLEMENTER COMPLETE; Gate 4 self-QA passed. Awaiting Lead-owned T1 Gate 5 review and Git commit.**

- Worktree: `C:\WPP018_20260825`
- Branch: `feature/wp-p0-18-chart-poc-20260825`
- Base/current HEAD before Lead commit: `46f5bafbf82f3366c8bc7ee08f6f0eee08d46138`
- Audit tier: T1, fixed by the package contract because POC code exists
- Protected surfaces changed: none
- Other AI CLIs used: none
- Network use: only npm metadata/downloads for `lightweight-charts@5.2.1` and `echarts@6.1.0`
- Push: not performed

## Deliverables

- `poc/lightweight/`: offline Lightweight Charts page, pinned runtime, exact licence, draggable level, stepped overlays, 100k/5k test
- `poc/echarts/`: offline ECharts page with the equivalent workload and interaction
- `poc/qa_browser.mjs`: dependency-free Edge/CDP QA harness
- `CHART_LIBRARY_COMPARISON.md`: six-criterion evidence, required decision evidence, and the shared recommendation

Open either `poc/lightweight/index.html` or `poc/echarts/index.html` directly. No server or build step is required.

## Gate 4 evidence

Commands executed:

```powershell
node --check MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_18_CHART_POC_2026-08-25\poc\lightweight\app.js
node --check MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_18_CHART_POC_2026-08-25\poc\echarts\app.js
node --check MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_18_CHART_POC_2026-08-25\poc\qa_browser.mjs
node MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_18_CHART_POC_2026-08-25\poc\qa_browser.mjs
```

Result: syntax checks returned exit 0. Three final sequential browser runs (R12–R14) returned exit 0. Every run asserted `ready=true`, 100,000 points, exactly 5,000 markers, seven programmatic JSON annotations, a full-size canvas, no page error, a changed level after real mouse input, and a changed level after six simulated touch moves. Final screenshots were visually inspected: candles, entry/exit markers, SL/TP/Multi-TP, stepped trail, drag level, and the aligned equity pane were present in both.

Median final timings:

| Measure | Lightweight | ECharts |
|---|---:|---:|
| Harness attach-to-ready wait | 842.88 ms | 586.29 ms |
| Library ingest | 322.7 ms | 398.5 ms |
| Pan frame p95 | 18.4 ms | 23.6 ms |
| Drag motion p95 | 0.1 ms | 0.1 ms |
| Level-series commit on release | included in motion update | 98.9 ms |

Runtime offline scan:

```text
OFFLINE_RUNTIME_SCAN_PASS: no external request/import tokens
```

Both vendored licence files SHA-256-matched their npm package source copies. The final comparison contains runtime hashes, bundle sizes, run ranges, environment, and measurement caveats.

## Staged file list

The exact paths staged for Lead review are:

```text
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_18_CHART_POC_2026-08-25/CHART_LIBRARY_COMPARISON.md
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_18_CHART_POC_2026-08-25/LANE_REPORT.md
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_18_CHART_POC_2026-08-25/poc/qa_browser.mjs
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_18_CHART_POC_2026-08-25/poc/lightweight/index.html
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_18_CHART_POC_2026-08-25/poc/lightweight/app.js
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_18_CHART_POC_2026-08-25/poc/lightweight/THIRD_PARTY.md
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_18_CHART_POC_2026-08-25/poc/lightweight/vendor/lightweight-charts-5.2.1.min.js
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_18_CHART_POC_2026-08-25/poc/lightweight/vendor/LICENSE.lightweight-charts-5.2.1.txt
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_18_CHART_POC_2026-08-25/poc/echarts/index.html
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_18_CHART_POC_2026-08-25/poc/echarts/app.js
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_18_CHART_POC_2026-08-25/poc/echarts/THIRD_PARTY.md
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_18_CHART_POC_2026-08-25/poc/echarts/vendor/echarts-6.1.0.min.js
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_18_CHART_POC_2026-08-25/poc/echarts/vendor/LICENSE.echarts-6.1.0.txt
```

## Commit sequencing

Implementation commit SHA: **PENDING — Lead-owned after accepting T1 Gate 5.**

Required commit message:

```text
feat(wp-p0-18): chart-library POC - draggable level in both candidates (T1, lane S 2026-08-25)
```

The implementer did not self-audit Gate 5, commit, or push. The Lead must independently inspect the staged diff, rerun the published QA command verbatim, perform the required T1 flagship review, and only then commit if the verdict is PASS or PASS-WITH-NITS.

## Open issues and limits

1. Touch was simulated through Edge CDP; no physical phone was used tonight, as required by the lane.
2. Timings are local comparative evidence under headless software rendering, not production capacity guarantees.
3. ECharts can expose native draggable graphic elements. The POC retained an accessible DOM hit target and measured the required data-series commit; a library-specific graphic optimization was not explored.
4. The recommended library is not adopted by this POC. The verdict consumers retain the decision authority.
5. The #94 canvas remained a visual reference only and was not copied or made a dependency.
