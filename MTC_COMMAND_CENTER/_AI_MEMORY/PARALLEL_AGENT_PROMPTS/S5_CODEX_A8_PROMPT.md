# S5 — ChatGPT Codex: A8 Global Acceptance Criterion (Dashboard Summary Header)

## Project context

Repo: `C:\LAB\Tradingview_LAB_CLEAN`  
Dashboard frontend: `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/app.js` (≈2400+ lines after S2)  
Dashboard CSS: `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/styles.css`  
Backend API: `http://127.0.0.1:8765` — serves `/api/snapshot`  
Dashboard runs: `cd MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api && python -m mcc_readonly serve`

This is the MTC Command Center — a trading strategy research + backtesting system.
Previous agent (S2) already added A5/A6/A7/D4 to app.js. READ app.js FULLY before touching it.

---

## Task A8 — Global Acceptance Criterion Panel

### What it does

The dashboard home/overview must answer — **without opening any file** — one question:

> *"En iyi aday ne, ne bloke, neden, sıradaki aksiyon ne?"*  
> ("What's the best candidate, what's blocked, why, what's the next action?")

This is a top-level summary banner/panel, visible without clicking into any strategy.

### Where to add it

Find the **Home tab** or the first rendered section of the dashboard (where the Pipeline
overview / snapshot summary currently appears). Add the A8 panel BEFORE or AT THE TOP
of that section.

If no obvious "Home" or "Overview" section exists, add it as a sticky banner at the top
of the main content area, visible on the Pipeline tab.

### What to render

Read from `snapshot.scorecards.cards` (flat list of scorecard_v2 objects).

**Panel: "MCC System Status"** — one compact card with 4 rows:

```
┌─────────────────────────────────────────────────────────────┐
│  MCC SYSTEM STATUS                              2026-06-06  │
├─────────────────────────────────────────────────────────────┤
│  🏆 BEST CANDIDATE   QL_FAM_MOMENTUM_CONTINUATION           │
│                      TRXUSDT · 4h · PROMOTABLE              │
│                                                             │
│  ⚠ BLOCKED (8)       Gate3 incomplete — paper-trade evid.  │
│                      missing for 8 strategies               │
│                                                             │
│  📊 PIPELINE         349 scorecards · 1 promotable          │
│                      Gate2 PASS: N · Gate3 OK: 1            │
│                                                             │
│  ➤ NEXT ACTION       Run forward-paper trade for            │
│                      TRXUSDT 4h (Gate3→paper-trade step)    │
└─────────────────────────────────────────────────────────────┘
```

**Derive these values from the API data:**

```javascript
function buildAcceptanceSummary(scorecards) {
    const cards = scorecards?.cards || [];

    // Best candidate: promotable=true first, then highest gate2 score
    const promotable = cards.filter(c => c.gate_summary?.promotable);
    const best = promotable[0] || cards.sort((a,b) =>
        (b.gate2?.score||0) - (a.gate2?.score||0))[0];

    const gate2Pass = cards.filter(c => c.gate2?.pass).length;
    const gate3OK = cards.filter(c => c.gate3?.status === 'OK').length;
    const blocked = cards.filter(c => !c.gate_summary?.promotable).length;

    // Derive next action
    let nextAction = 'No actionable candidates yet';
    if (promotable.length > 0) {
        nextAction = `Run forward-paper trade for ${best.symbol} ${best.timeframe} (Gate3→paper-trade step)`;
    } else if (gate2Pass > 0) {
        nextAction = `Complete Gate3 production-readiness evidence for ${gate2Pass} Gate2-passing strategies`;
    } else {
        nextAction = 'Run backtest batch to generate Gate2 evidence';
    }

    return { best, promotable: promotable.length, gate2Pass, gate3OK, blocked,
             total: cards.length, nextAction };
}
```

**Style:** Terminal/monospace, consistent with existing dashboard. Use existing CSS classes where possible. Add minimal new CSS to `styles.css` for `.mcc-status-panel` if needed.

**Update dynamically:** Panel should re-render when snapshot refreshes (if dashboard polls).
If snapshot is loaded once on page load, render after snapshot fetch resolves.

---

## Validation

```bash
# After app.js change:
node --check MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/app.js
# Expected: no errors

# API tests (run from repo root):
cd C:\LAB\Tradingview_LAB_CLEAN
set PYTHONPATH=MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api
python -m pytest MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests -q
# Expected: 35 passed — must not regress

# Start dashboard and verify panel renders:
cd MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api && python -m mcc_readonly serve
# Open http://127.0.0.1:8765/dashboard
# Panel should appear at top/home with correct values from snapshot
```

---

## HARD SAFETY RULES

- NEVER edit: `*.pine` files, any file in `02_MTC_BACKTEST/src/engine/`, `mega_walk_forward.py`
- NEVER edit: `apps/api/mcc_readonly/*.py` files (backend — hands off)
- NEVER fabricate scorecard scores or metrics — only render what API provides
- NEVER edit `05_REGISTRY/*.json`
- app.js is single-writer — do ONE coherent edit pass
- Only write to:
  - `08_DASHBOARD_APP/apps/web/app.js` (add `buildAcceptanceSummary` + render call)
  - `08_DASHBOARD_APP/apps/web/styles.css` (minimal new classes only if needed)
  - `08_DASHBOARD_APP/apps/web/index.html` (only if a mount point div is needed)

---

## Report output

Write your complete report to EXACTLY this path:
`C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\_AI_MEMORY\PARALLEL_AGENT_REPORTS\S5_CODEX_A8_REPORT.md`

Report must contain:
- Which function was added and at which line
- Where in the UI the panel appears (tab name / position)
- `node --check` result (pass/fail)
- API test result (N passed)
- Browser screenshot description: what the panel shows with live snapshot data
- Any data that was `null` / missing in live snapshot (honest "no data" handling)
