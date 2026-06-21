# Dashboard UI Integration Audit — Why /dashboard Still Shows Old UI

Date: 2026-06-14
Author: Claude (auditor only — no code changed)
Question audited: Why does `http://127.0.0.1:8765/dashboard` still show the old
MTC Command Center UI instead of the new Strategy Intelligence / Command Center
design?

## 1. Executive diagnosis

**Codex patch incomplete (case J).** Codex never integrated the Strategy
Intelligence redesign. It made incremental additions to the existing old vanilla
"MTC Command Center" tab UI — added 3 tabs (Strategy Detail, Backtest Result
Explorer, Strategy Leaderboard), widened the Registry table, added a Strategy
Detail panel and a "Read Model / Data Model Contract" sub-block in Diagnostics.
The shell (sidebar `.tabs`, brand "MTC Command Center", "MVP-1" topbar, tab
routing) is unchanged.

The new design exists only as an unconnected React/TSX reference at
`11_TRIAGE/ui_references/strategy_intelligence_lovable/`. Never ported, never
served, not reachable from `/dashboard`.

Root cause of Codex error: its prompt pointed at a non-existent reference path
(`ui_references/google_strategy_intelligence_v2_final`). Real path is
`ui_references/strategy_intelligence_lovable`.

NOT cache. NOT wrong directory. NOT stale server. NOT a missing route hookup.
The served file IS the old shell.

Confidence: HIGH.

## 2. Active served files

- `/dashboard` → returns `apps/web/index.html` (`server.py:21`).
- Assets `/web/*` → `apps/web/` (`server.py:24`): `/web/styles.css`,
  `/web/app.js?v=20260531-source-parent`.
- Live `curl 127.0.0.1:8765/dashboard` → `<title>MTC Command Center</title>`,
  `class="tabs"`, `app-shell` = old shell. ("Strategy Intelligence" appears only
  as a tab title string, not a page.)
- Served JS/CSS matches edited repo files. `Cache-Control: no-store`
  (`server.py:90`) — no cache layer. On-screen UI = exactly the on-disk files.

## 3. Repo file changes verified

`git diff --stat HEAD -- apps/web/`: app.js +1121, index.html +59/-57,
styles.css +265. All 3 active (served). Changes are additive into the old shell:

- index.html: +Strategy Detail tab, +Result Explorer tab, +Leaderboard tab,
  +Registry columns, +`diagnosticsContract` div. Sidebar still
  `<nav class="tabs">`, brand still "MTC Command Center".
- app.js new strings are minor: "View Approval Package" disabled chips
  (`app.js:887,1103`) inside Strategy Detail panel; "Read Model / Data Model
  Contract" (`app.js:3224`) inside Diagnostics. No `renderCommandCenter`,
  `renderStrategyIntelligence`, or `activePage`.

## 4. Routing / rendering diagnosis

- Router unchanged: old tab system, `.tab-panel` + `data-tab`
  (`app.js:46,123`).
- Default view = `data-tab="pipeline"` marked `is-active` (`index.html:21`).
  `/dashboard` opens on old Pipeline tab.
- New Command Center home: does not exist in vanilla app.
- New sidebar: not present (still old tab strip).
- New pages (AI Knowledge Base, Backtest Planner, Paper Trading approval,
  Advanced Artifacts, Read Model page): not reachable — only the React
  reference has them.

## 5. Cache / server diagnosis

- Cache: not the cause. `Cache-Control: no-store` on every response; app.js
  cache-bust query also present.
- Restart: not needed for diagnosis — running server already serves edited files.
- Wrong directory: no. `_web_root` → `apps/web` is the edited dir.

## 6. Missing integration points

Entire port missing. Reference components in
`strategy_intelligence_lovable/mtc-strategy-intelligence (4)/src/components/`:
`CommandCenterHome`, `StrategyPipeline`, `StrategyRegistry`, `StrategyOverview`/
`STG112Intelligence`, `BacktestPlanner`, `BacktestRuns`, `BacktestResultExplorer`,
`StrategyLeaderboard`, `PaperTrading`(+`PaperTradingReadiness`),
`AIKnowledgeBase`, `AdvancedArtifacts`, `Diagnostics`, `Reports`, plus shell
(`App.tsx`, sidebar, `RightStickyRail`). None wired into app.js/index.html.

## 7. Minimal fix plan

No small/obvious fix exists. No file swap, route change, or default-tab flip
produces the new UI — it was never built into the served vanilla app. Making
`/dashboard` show Command Center = real porting work (React reference → vanilla
JS, or stand up a Vite build and point `/dashboard` at it). That is the broad
redesign explicitly scoped out of this audit.

Correct outcome: reject the assumption that Codex integrated the UI. It did not.
Decide integration approach before any code.

## 8. Safety check

No Pine/MTC/backtest-engine/broker files involved. Changes confined to
`apps/web/`. API stays `mcc_readonly` snapshot, read-only (POST/PUT/PATCH/DELETE
→ 405, `server.py:52-62`). No execution / write-back touched.

## 9. Commands run + results

- `git diff --stat HEAD -- apps/web/` → app.js +1121, index.html +59/-57,
  styles.css +265.
- `git diff index.html` → only additive tabs + Registry columns + diagnostics
  div; shell unchanged.
- Grep new-UI strings in `apps/web/` → matches only in old index.html, app.js
  (minor), prototypes/*. Full design only under
  `11_TRIAGE/ui_references/strategy_intelligence_lovable/` (React/TSX).
- Grep `server.py` → `/dashboard`→index.html, `/web/`→static, `no-store`.
- `curl 127.0.0.1:8765/dashboard` → old shell.
- `netstat :8765` → LISTENING, PID 20944.

## 10. Decision + next action

Barış decision (2026-06-14): **Re-task Codex.** Corrected, explicit brief written
to `11_TRIAGE/CODEX_RETASK_REPLACE_DASHBOARD_SHELL_2026-06-14.md`. Claude remains
auditor only; no code changes.
