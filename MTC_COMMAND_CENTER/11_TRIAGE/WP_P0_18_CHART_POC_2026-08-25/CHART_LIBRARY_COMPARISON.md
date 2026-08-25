# WP-P0-18 chart-library comparison

## Outcome first

**Recommended shared verdict: select TradingView Lightweight Charts 5.2.1 for both the research and execution chart surfaces.** It passed every POC criterion, had the smaller vendored payload, needed the smaller drag adapter, and had the better measured pan frame and no deferred ECharts-style series commit. ECharts 6.1.0 also passed; it reached the harness-ready state faster in this run and remains a credible fallback if later requirements value its broader visualization system more than footprint and price-chart specialization.

This is a recommendation, not adoption authority. If the owner selects it, reuse is limited to the library and build-time components. Research and execution must not share a process, port, session, credential, data authority, or truth store. The gated TradingView Charting Library was not tried because both permissive candidates passed.

## Scope and method

Both pages are offline, seeded-fake-data POCs with the same workload:

- 100,000 one-minute candles;
- exactly 5,000 generated entry/exit markers;
- six JSON-described overlays: EMA, SL, TP1, TP2, TP3, and stepped trailing history;
- one draggable horizontal level, for seven programmatic annotations total;
- a linked equity pane;
- mouse drag, keyboard adjustment, and simulated touch drag.

The committed `poc/qa_browser.mjs` harness opened each page in a fresh Edge profile, sequentially, at 1440×900 with the same headless software-rendering flags. On a harness-controlled reload it asserted 100,000 actual generated points, seven parsed-JSON annotations, exact marker count, full-size canvas output, independently measured mouse and simulated-touch drags, no DOM/runtime/console/unhandled-rejection error, and no non-`file:`/non-`data:` request, then captured a screenshot. Final timing numbers are medians of the three earlier clean runs (R12–R14); ranges are shown where useful. Those earlier runs predate the repaired assertions and are used only for the timing measurements.

Environment: Windows 11 Pro build 26200; Edge 151.0.4129.101; Node 24.13.0; Intel Core i7-13700H (14 cores / 20 logical processors); 31.7 GiB RAM. Measured 2026-08-25, Europe/Chisinau.

## Measured comparison

| Measure | Lightweight Charts 5.2.1 | ECharts 6.1.0 | Interpretation |
|---|---:|---:|---|
| Data generation | 51.6 ms (51.2–52.9) | 28.6 ms (26.5–37.3) | POC code, not library work; included for reproducibility |
| Library ingest / `setOption` | 322.7 ms (306.2–365.4) | 398.5 ms (372.7–443.8) | Same 100k/5k/seven-annotation workload |
| Library paint callback after ingest | 343.7 ms | 37.6 ms | Callback semantics differ; do not compare this row alone |
| Harness attach-to-ready wait | 842.88 ms (742.39–849.74) | 586.29 ms (572.49–629.74) | Fresh profile each run, but excludes browser launch/target discovery; ECharts won this measured wait |
| 30-step pan frame p50 | 16.9 ms | 19.5 ms | RequestAnimationFrame-to-frame measurement |
| 30-step pan frame p95 | 18.4 ms (18.4–19.4) | 23.6 ms (21.1–25.1) | Both stayed below the POC's 33.3 ms usability line; Lightweight was smoother |
| Drag motion dispatch p95 | 0.1 ms | 0.1 ms | Both custom DOM hit targets move immediately |
| Level-series commit on release | included in the 0.1 ms price-line update | 98.9 ms (89.8–107.5) | ECharts defers its two-point series commit until release to keep motion smooth |
| Vendored runtime, raw / gzip | 197,922 / 62,244 bytes | 1,121,883 / 369,255 bytes | ECharts is 5.7× raw and 5.9× gzip |
| POC app / drag-adapter lines | 266 / 34 | 285 / 46 | Counted between the `DRAG-COST` markers |

The numbers are comparative POC evidence, not production capacity promises. Headless software rendering and seeded data differ from a physical phone and production hardware.

## Owner's six failable criteria

| Criterion | Lightweight Charts | ECharts | Result |
|---|---|---|---|
| ~70k-candle smooth pan/zoom | 100k loaded; pan p95 18.4 ms | 100k loaded; pan p95 23.6 ms | **PASS / PASS.** Both exceeded the scale; Lightweight had the better frame result |
| ≥6 overlays plus hundreds of markers | Six overlays + draggable level + exactly 5,000 markers; markers visible | Same; final marker coordinate verified inside the plot and markers visible | **PASS / PASS** |
| Synced second pane and linked crosshair | Native multi-pane chart shares time scale/crosshair; screenshot verified | Two grids with linked x-axis pointer and shared data zoom; screenshot verified | **PASS / PASS** |
| Programmatic annotation from artifact JSON | Seven annotations built from parsed JSON; harness count asserted; no manual drawing | Same | **PASS / PASS** |
| Self-hostable offline licence fit | Vendored Apache-2.0 package; exact licence copied; attribution logo enabled; the repair added no external HTML/JS URL and the harness-controlled reload emitted no non-file/data request | Vendored Apache-2.0 package; exact licence copied; the repair added no external HTML/JS URL and the harness-controlled reload emitted no non-file/data request | **PASS / PASS** |
| Plain research-dashboard web stack | One HTML + one plain JS file + vendored IIFE; no build step | One HTML + one plain JS file + vendored UMD bundle; no build step | **PASS / PASS** |

## Required decision evidence

### Markers, protection overlays, and trailing history

Both candidates render the 5,000-marker series, SL, three TP legs, EMA, and a stepped trailing series. The visible-window screenshots show the marker and overlay shapes without hand-authored canvas drawing. Neither POC claims production semantics; all values are seeded fake data.

### Draggable level and integration cost

Lightweight Charts has no native draggable price line. The POC combines its price-line API with `priceToCoordinate` / `coordinateToPrice` and a 34-line accessible DOM pointer adapter. Every move updates the native price line at 0.1 ms p95.

ECharts exposes draggable graphic elements at API level, but a production level still needs price-coordinate conversion, persistence/request timing, zoom/resize synchronization, and an accessible hit target. This POC used a comparable accessible DOM adapter and a dedicated two-point ECharts series. Motion was 0.1 ms p95; the series commits once on release and cost 98.9 ms median. The adapter was 46 lines. A later ECharts-specific graphic optimization could change that commit cost, but was not needed to establish a working drag.

### Touch behaviour

Both pages use Pointer Events with `touch-action: none` on the drag target. The QA harness sent six CDP touch moves: Lightweight changed the level by -3.48 price units and ECharts by -2.85, with six pointer moves observed in each. This is an API-level simulation only. No claim is made about real-phone ergonomics, gesture conflicts, or fat-finger precision.

### Maintenance and licence

Both exact npm packages report Apache-2.0 and contain a full Apache licence. The vendored licence hashes exactly match the downloaded packages. npm reported Lightweight Charts 5.2.1 published 2026-08-12 and ECharts 6.1.0 published 2026-05-19, so neither candidate showed an abandonment signal at the measurement date.

- Lightweight runtime SHA-256: `e21cc5caa0226ef30bd8549c50b9ef926615f2a4ee6b4e486353477a55f598cf`
- ECharts runtime SHA-256: `b66b25aeb4df84e33199dc21694014d336d222cbd9deb0e5a7c14bd6aa0d0fd0`

## Verdict rationale

Lightweight Charts is the better default for this specific price-chart job: smaller payload, fewer adapter lines, better pan-frame result, direct price-series coordinate APIs, and no measurable release-time series commit. ECharts' faster harness-ready result and broad chart vocabulary are real strengths, but they do not outweigh the integration and footprint advantage for the shared research/execution chart component measured here.

The recommendation should be revisited only if a later accepted package introduces a requirement the selected library cannot meet. It must not trigger a second independent contest between the research and execution domains.
