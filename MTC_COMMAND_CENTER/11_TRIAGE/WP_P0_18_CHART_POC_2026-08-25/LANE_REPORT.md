# Lane S report — WP-P0-18 chart-library POC

## Status

**T1 AUDIT REPAIR IMPLEMENTED; Gate 4 self-QA passed. Awaiting Lead-owned T1 re-audit and acceptance.**

- Worktree: `C:\WPP018_20260825`
- Branch: `feature/wp-p0-18-chart-poc-20260825`
- Repair base HEAD: `5c0f95df`
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

Result: syntax checks returned exit 0. The post-audit repair browser run returned exit 0 for both pages. It asserted `ready=true`, 100,000 actual generated points, exactly 5,000 markers, seven programmatic JSON annotations, a full-size canvas, an empty `#error` element, no CDP runtime exception/console error/unhandled rejection, and no non-`file:`/non-`data:` request during a harness-controlled reload. Mouse and touch were measured separately: mouse-only deltas were 4.14 (Lightweight) and 3.66 (ECharts), with eight pointer moves each; touch-only deltas were -3.48 and -2.85, with six pointer moves each.

The older R12–R14 runs remain the source of the median timing table below; they did not contain the repaired point-count, annotation-count, runtime-error, network-isolation, or mouse-only fences and are not claimed as evidence for those assertions. Their screenshots were visually inspected: candles, entry/exit markers, SL/TP/Multi-TP, stepped trail, drag level, and the aligned equity pane were present in both.

### D026 falsification evidence

Each new fence was deliberately falsified, returned non-zero, and was then restored before the final green run:

| Mutant | Real RED output |
|---|---|
| Mouse moves held at the starting Y while touch remained active | `echarts: real pointer drag did not change the level` |
| Lightweight actual point count changed from 100000 to 99999 | `lightweight: expected 100000 points, got 99999` |
| Lightweight programmatic annotation count changed from 7 to 6 | `lightweight: expected 7 programmatic annotations, got 6` |
| `console.error` plus an unhandled rejected promise injected | `lightweight: runtime error(s)` with both `__QA_D026_CONSOLE_ERROR__` and `__QA_D026_UNHANDLED_REJECTION__` |
| External image request injected | `lightweight: external network request(s): GET https://example.invalid/__QA_D026_EXTERNAL_REQUEST__` |

Final restored GREEN: `node poc/qa_browser.mjs` exit 0 for both pages, with `runtimeErrors: []` and `externalRequests: []`.

Median final timings:

| Measure | Lightweight | ECharts |
|---|---:|---:|
| Harness attach-to-ready wait | 842.88 ms | 586.29 ms |
| Library ingest | 322.7 ms | 398.5 ms |
| Pan frame p95 | 18.4 ms | 23.6 ms |
| Drag motion p95 | 0.1 ms | 0.1 ms |
| Level-series commit on release | included in motion update | 98.9 ms |

Static offline scan and live controlled-reload check:

```text
OFFLINE_RUNTIME_SCAN_PASS: no external request/import tokens
REPAIR_DIFF_OFFLINE_PASS: no added external URL in poc/**/*.html or poc/**/*.js
LIVE_NETWORK_ASSERTION_PASS: no non-file/non-data request
```

Both vendored licence files SHA-256-matched their npm package source copies. The final comparison contains runtime hashes, bundle sizes, run ranges, environment, and measurement caveats.

## Staged file list

The exact paths staged for the repair commit are:

```text
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_18_CHART_POC_2026-08-25/CHART_LIBRARY_COMPARISON.md
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_18_CHART_POC_2026-08-25/LANE_REPORT.md
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_18_CHART_POC_2026-08-25/poc/qa_browser.mjs
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_18_CHART_POC_2026-08-25/poc/lightweight/app.js
MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_18_CHART_POC_2026-08-25/poc/echarts/app.js
```

## Commit sequencing

Repair commit message:

```text
fix(wp-p0-18): make QA harness assertions discriminating + align evidence claims (T1 findings)
```

The implementer did not self-audit or issue a Gate 5 verdict and did not push. The Claude Lead must independently inspect the repair diff, rerun the published QA command verbatim, and perform the required T1 re-audit before accepting the repair.

## Audit-claim reconciliation

- Added as real harness assertions: 100,000 actual generated points; seven parsed-JSON annotations; an empty CDP runtime/console/unhandled-rejection error set; an empty non-`file:`/non-`data:` request set during a controlled reload; and independent non-zero mouse-only and touch-only movement.
- Narrowed: the R12–R14 historical sentence no longer claims those repaired assertions existed in the older harness. Offline readiness is scoped to the observed controlled reload plus the separate static URL scan, not to every possible future browser or network path.

## Open issues and limits

1. Touch was simulated through Edge CDP; no physical phone was used tonight, as required by the lane.
2. Timings are local comparative evidence under headless software rendering, not production capacity guarantees.
3. ECharts can expose native draggable graphic elements. The POC retained an accessible DOM hit target and measured the required data-series commit; a library-specific graphic optimization was not explored.
4. The recommended library is not adopted by this POC. The verdict consumers retain the decision authority.
5. The #94 canvas remained a visual reference only and was not copied or made a dependency.
