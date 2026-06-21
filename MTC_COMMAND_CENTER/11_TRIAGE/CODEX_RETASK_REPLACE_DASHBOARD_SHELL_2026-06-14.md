# Codex Re-Task — Replace Dashboard Shell with Strategy Intelligence UI

Date: 2026-06-14
Author: Claude (auditor)
Status: HANDOFF TO CODEX — not yet implemented

## Why the last attempt failed (do not repeat)

The previous Codex run was given reference path
`MTC_COMMAND_CENTER/11_TRIAGE/ui_references/google_strategy_intelligence_v2_final`
— **that path does not exist on disk.** Not finding it, Codex added 3 tabs
(Strategy Detail, Backtest Result Explorer, Strategy Leaderboard) onto the
*existing old* vanilla "MTC Command Center" tab shell and reported success.

Result: `/dashboard` still serves the old shell. Tests passed (`node --check`,
39 API unittests) but the UI was never replaced. **Do not assume green tests =
integrated UI.**

## Correct reference (verified on disk)

`MTC_COMMAND_CENTER/11_TRIAGE/ui_references/strategy_intelligence_lovable/`
— React/TSX design.

Full page set in
`strategy_intelligence_lovable/mtc-strategy-intelligence (4)/src/components/`:

- `CommandCenterHome.tsx`  (the default home view)
- `StrategyPipeline.tsx`
- `StrategyRegistry.tsx`
- `StrategyOverview.tsx` / `STG112Intelligence.tsx`
- `BacktestPlanner.tsx`
- `BacktestRuns.tsx`
- `BacktestResultExplorer.tsx`
- `StrategyLeaderboard.tsx`
- `PaperTrading.tsx` (+ `PaperTradingReadiness.tsx`)
- `AIKnowledgeBase.tsx`
- `AdvancedArtifacts.tsx`
- `Diagnostics.tsx`
- `Reports.tsx`
- Shell: `App.tsx` + sidebar + `RightStickyRail.tsx`

## Serving facts (do not break)

- `/dashboard` → serves `apps/web/index.html`
  (`apps/api/mcc_readonly/server.py:21`).
- Assets at `/web/*` → served from `apps/web/`
  (`server.py:24`).
- Server = Python stdlib `http.server` (ThreadingHTTPServer), no build step,
  `Cache-Control: no-store` on every response (`server.py:90`).
- Data source = `mcc_readonly` snapshot: `/api/snapshot`, `/api/read-model`.
- API is read-only: POST/PUT/PATCH/DELETE all return 405 (`server.py:52-62`).

## Task

Replace the served UI shell so `/dashboard` opens on the **Command Center home**
with the new sidebar and reachable pages, matching the reference design.

This is NOT added-on tabs. The old `<nav class="tabs">` tab strip and the
"MTC Command Center / MVP-1" topbar shell must be gone.

## Hard scope guards

- Vanilla JS/CSS only, UNLESS you also wire a build output into the server.
  If you build the React app, state the path and prove the server serves it.
- No Pine / MTC trading-logic changes.
- No backtest-engine changes.
- No write-back / broker / paper-trading / live-trading behavior.
- API stays read-only (snapshot based).
- Do NOT implement night-backtest ingestion.
- Disabled / pilot chips stay disabled (e.g. "View Approval Package",
  "Not wired" filters).

## Acceptance criteria (must prove ALL — served evidence, not just unit tests)

1. `curl 127.0.0.1:8765/dashboard` → **no** `<title>MTC Command Center</title>`
   old shell, **no** `<nav class="tabs">`.
2. Default view = Command Center home (not the Pipeline tab).
3. New sidebar present; every reference page reachable and rendering live
   snapshot data.
4. `node --check app.js` passes AND visual confirmation (screenshot or served
   HTML grep) that the shell changed.
5. State which integration path was taken (vanilla port vs built React) and the
   exact served entry file.

## Evidence required in Codex report

- Output of `curl 127.0.0.1:8765/dashboard | head` showing new shell markers.
- The served `app.js` / asset path actually loaded by the new `index.html`.
- Screenshot or DOM dump of Command Center home as the default `/dashboard` view.
