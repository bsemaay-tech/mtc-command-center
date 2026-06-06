# S2 — ChatGPT Codex: Dashboard UI Components (A5 / A6 / A7 / D4)

## Project context

Repo: `C:\LAB\Tradingview_LAB_CLEAN`  
Dashboard: `MTC_COMMAND_CENTER/08_DASHBOARD_APP/`  
Backend API: `apps/api/mcc_readonly/` — serves JSON via Flask at `http://127.0.0.1:8765`  
Frontend: `apps/web/app.js` (≈2400 lines) + `apps/web/styles.css`  
Dashboard runs: `cd MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api && python -m mcc_readonly serve`

The dashboard shows trading strategy evaluation results. Each strategy has up to 4 gates
(Gate1=Intake, Gate1B=MTC Feasibility, Gate2=Backtest Evidence, Gate3=Production Readiness).
Gate data is in `scorecard_v2` JSON files and exposed via `/api/snapshot` under key `scorecards`.

**CRITICAL:** Read `app.js` fully before writing ANY code. You must understand existing
functions before adding new ones. Especially read: `renderUnifiedStrategyDetail()`,
`renderQuantlensVerdict()`, `buildWaveADecision()`, `renderStrategyList()`.

---

## scorecard_v2 JSON schema (what you'll read from the API)

```json
{
  "scorecard_version": "v2",
  "strategy_id": "QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL",
  "base_strategy_id": "QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL",
  "symbol": "LINKUSDT",
  "timeframe": "1h",
  "gate1": {
    "status": "OK",
    "score": 96,
    "pass": true,
    "gate_label": "Gate 1 Intake",
    "criteria_count": 35,
    "points_possible": 100
  },
  "gate1B": {
    "status": "OK",
    "score": 80,
    "pass": true,
    "gate_label": "Gate 1B MTC Feasibility"
  },
  "gate2": {
    "status": "OK",
    "score": 100,
    "pass": true,
    "gate_label": "Gate 2 Backtest Evidence",
    "metrics": {
      "sharpe": {"status": "OK", "value": 1.307},
      "sortino": {"status": "OK", "value": 2.696},
      "net_after_slippage_pct": {"status": "OK", "value": 67.1},
      "param_stability_score": {"status": "OK", "value": 0.899},
      "beats_ema_benchmark": {"status": "OK", "value": true},
      "regime_coverage_count": {"status": "OK", "value": 4},
      "worst_window_drawdown_pct": {"status": "OK", "value": 19.5},
      "cpcv_pass_ratio": {"status": "OK", "value": 1.0},
      "pbo": {"status": "OK", "value": 0.014}
    }
  },
  "gate3": {
    "status": "INCOMPLETE",
    "score": 30,
    "pass": false,
    "gate_label": "Gate 3 Production Readiness"
  },
  "gate_summary": {
    "promotable": false,
    "blocking": ["gate3_incomplete"],
    "notes": "Gate3 production-readiness evidence missing"
  }
}
```

The API snapshot exposes `scorecards.by_strategy` (keyed by `base_strategy_id`) and
`scorecards.cards` (flat list). The strategy detail page row already has
`row.scorecard_v2` attached by `scorecard_reader.py`.

---

## Task A5 — Backtest Evidence block in strategy detail page

**Where:** Inside `renderUnifiedStrategyDetail()` in app.js, AFTER the existing
scorecard gate section, BEFORE the Source Material section.

**What to add:** A collapsible `<details><summary>Backtest Evidence</summary>` section
showing up to 8 evidence cards from Gate2 metrics. Only show a card if the metric has
`status === "OK"`. Show honest "No data" if Gate2 is INCOMPLETE or metric absent.

Evidence cards (render from `row.scorecard_v2.gate2.metrics` if available):

| Card | Metric key | Display |
|---|---|---|
| Sharpe / Sortino | `sharpe`, `sortino` | Two numbers side-by-side |
| CPCV Pass Ratio | `cpcv_pass_ratio` | Percentage bar (×100) |
| PBO | `pbo` | Number (lower = better, < 0.5 = OK) |
| Slippage Net Return | `net_after_slippage_pct` | Number + sign |
| Param Stability | `param_stability_score` | Progress bar 0-1 |
| EMA Benchmark | `beats_ema_benchmark` | Badge: BEATS / FAILS |
| Regime Coverage | `regime_coverage_count` | Count out of 4 |
| Worst-Window Drawdown | `worst_window_drawdown_pct` | Number (negative = bad) |

Style: terminal/monospace aesthetic consistent with existing dashboard CSS.

---

## Task A6 — "Why Not Promotable" panel

**Where:** Inside `renderUnifiedStrategyDetail()`, right AFTER the verdict/scorecard section.
Only render if `row.scorecard_v2.gate_summary.promotable === false`.

**What to add:** A panel titled `⛔ Not Promotable — Blockers` showing:
1. Each item in `gate_summary.blocking` as a styled chip/badge
2. For each gate that is FAIL or INCOMPLETE: gate name + score + status
3. "Missing evidence" items from `gate_summary.notes` if present

Use red/orange chip colors for blockers, grey for INCOMPLETE vs red for FAIL.
If `promotable === true`, show a green `✓ Scorecard Promotable` badge instead.

---

## Task A7 — Gate-status filters in strategy list

**Where:** In the existing filter controls area of `renderStrategyList()` (or wherever
the current filters are rendered — read app.js to find the exact location).

**Add these filter buttons/dropdowns:**
- `Gate2: PASS only` — hides strategies where gate2.pass !== true
- `Gate3: Incomplete` — shows only strategies where gate3.status === "INCOMPLETE"
- `Promotable: Only` — shows only gate_summary.promotable === true
- `Blocked by Gate3` — shows strategies where blocking includes "gate3_incomplete"

Connect filters to existing filter state. Keep existing filters working.
If no scorecard data available for a row, treat as "unscored" — show by default.

---

## Task D4 — Night Run Detail page

**Where:** Add a new page/modal triggered from clicking a run in the Backtest Lab or
a new "Night Runs" tab. Read how the existing tabs are structured in app.js/index.html
before adding a new one.

**What to show per night run** (data from `snapshot.backtest_status.runs[]`):

Each run object from the API has: `run_id`, `status`, `cell_count`, `candidate_count`,
`source`, `run_type`, `worker_count` (may vary). Build a detail view showing:

1. **Header card**: Run ID, status badge, date, run type
2. **Summary metrics**: Total cells tested, candidates found, workers used
3. **Gate 2 split**: pass_count / fail_count / incomplete_count (from `results_summary` if available)
4. **Artifact links** (render as clickable file paths if available):
   - Morning report: look for `*MORNING_REPORT*.md` in run dir
   - CPCV report: `cpcv15/CPCV_VALIDATION_REPORT.md`
   - PBO report: `pbo/PBO_REPORT.md`
   - Alpha summary: `alpha_summary.json`
5. **Candidate table**: strategy_id | symbol | timeframe | gate2_status | gate2_score
6. **Validation checklist**: CPCV done? PBO done? Gate2 scored? All-gate artifacts? (derive from presence of files in run data)

Note: Artifact file paths in the API may not all be present — show "N/A" for missing ones.

---

## Validation (run after each task, not just at the end)

```bash
# After any app.js change:
node --check MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/app.js

# API tests (run from repo root):
cd C:\LAB\Tradingview_LAB_CLEAN
set PYTHONPATH=MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api
python -m pytest MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests -q
# Expected: 35 passed, 1 subtest
```

Also start the dashboard and visually verify each component renders:
`cd MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api && python -m mcc_readonly serve`
Then open `http://127.0.0.1:8765/dashboard` and click through to a strategy detail.

---

## HARD SAFETY RULES

- NEVER edit: `*.pine` files, any file in `02_MTC_BACKTEST/src/engine/`, `mega_walk_forward.py`
- NEVER edit: `apps/api/mcc_readonly/*.py` files (that's S3's domain — no reader changes here)
- NEVER fabricate scorecard scores or metrics — only render what the API provides
- app.js is single-writer — do NOT split into multiple simultaneous edits
- Do tasks sequentially (A5 → A6 → A7 → D4), validate after each

---

## Report output

Write your complete report to EXACTLY this path:
`C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\_AI_MEMORY\PARALLEL_AGENT_REPORTS\S2_CODEX_UI_REPORT.md`

Report must contain:
- Which tasks completed (A5 / A6 / A7 / D4)
- Which app.js functions were added or modified (with line numbers if possible)
- `node --check` result (pass/fail)
- API test result (N passed)
- Browser verification: did each component render?
- Any tasks skipped and why
