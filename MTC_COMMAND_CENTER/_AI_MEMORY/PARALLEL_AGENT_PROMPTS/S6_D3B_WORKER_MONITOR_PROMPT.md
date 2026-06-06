# S6 — Worker Monitor UI Tab (D3b)

## PREREQUISITE CHECK — do this first

Before doing anything else, verify S4's D3a work is present:

```bash
python -c "
import sys; sys.path.insert(0, 'MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api')
from mcc_readonly.heartbeat_reader import build_overnight_heartbeat
r = build_overnight_heartbeat()
print('D3a present:', True)
print('available:', r['available'])
"
```

If this fails with `ModuleNotFoundError`, stop immediately and report: "D3a not complete — heartbeat_reader.py missing."

---

## Project context

Repo: `C:\LAB\Tradingview_LAB_CLEAN`  
Dashboard frontend: `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/app.js`  
Dashboard CSS: `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/styles.css`  
Backend API snapshot key: `snapshot.overnight_heartbeat` (added by D3a)  
Dashboard runs: `cd MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api && python -m mcc_readonly serve`

**CRITICAL:** Read app.js FULLY before writing ANY code. Previous agents (S2, S5) have
already added many functions. Do not duplicate or overwrite existing functions.

---

## Task D3b — Worker Monitor UI Tab/Panel

### What to build

Add a **Worker Monitor** section to the dashboard showing the overnight batch run
heartbeat status from `snapshot.overnight_heartbeat`.

### API data shape

```json
{
  "overnight_heartbeat": {
    "available": true,
    "source_file": "_heartbeat_20260606_220000.json",
    "is_alive": true,
    "age_minutes": 3.2,
    "stage": "gate2_scoring",
    "status": "running",
    "run_id": "fam_batch_20260606",
    "timestamp": "2026-06-06T22:00:00+00:00",
    "raw": {}
  }
}
```

When `available: false`:
```json
{ "available": false, "reason": "overnight_runs dir not found" }
```

### Where to add it

Find the **Worker Monitor** or **LiveOps** tab/section in the existing dashboard.
If no such tab exists, add a small "Overnight Runner" status card to the Backtest
Lab section or the main overview area (wherever the night run data from D4 appears).

Do NOT create a new top-level tab just for this — embed as a status widget/card.

### What to render

```
┌────────────────────────────────────────────────────────────┐
│  OVERNIGHT RUNNER STATUS                                   │
├────────────────────────────────────────────────────────────┤
│  Status:   🟢 ALIVE (last heartbeat 3 min ago)             │
│  Stage:    gate2_scoring                                   │
│  Run ID:   fam_batch_20260606                              │
│  Updated:  2026-06-06 22:00 UTC                            │
└────────────────────────────────────────────────────────────┘
```

When `available: false`:
```
┌────────────────────────────────────────────────────────────┐
│  OVERNIGHT RUNNER STATUS                                   │
│  ⬜ No active run — overnight_runs/ not found              │
└────────────────────────────────────────────────────────────┘
```

When `available: true` but `is_alive: false`:
```
│  Status: 🔴 STALE (last heartbeat N min ago — run may have ended)
```

### JavaScript function to add

```javascript
function renderOvernightRunnerStatus(heartbeat) {
    if (!heartbeat || !heartbeat.available) {
        const reason = heartbeat?.reason || 'No heartbeat data';
        return `<div class="worker-monitor-card">
            <div class="wm-header">OVERNIGHT RUNNER STATUS</div>
            <div class="wm-offline">⬜ Offline — ${reason}</div>
        </div>`;
    }

    const aliveIcon = heartbeat.is_alive ? '🟢' : '🔴';
    const aliveText = heartbeat.is_alive
        ? `ALIVE (last heartbeat ${heartbeat.age_minutes?.toFixed(1) ?? '?'} min ago)`
        : `STALE (last heartbeat ${heartbeat.age_minutes?.toFixed(1) ?? '?'} min ago)`;

    return `<div class="worker-monitor-card">
        <div class="wm-header">OVERNIGHT RUNNER STATUS</div>
        <div class="wm-row"><span class="wm-label">Status:</span>
            <span class="wm-value">${aliveIcon} ${aliveText}</span></div>
        <div class="wm-row"><span class="wm-label">Stage:</span>
            <span class="wm-value">${heartbeat.stage ?? 'N/A'}</span></div>
        <div class="wm-row"><span class="wm-label">Run ID:</span>
            <span class="wm-value">${heartbeat.run_id ?? 'N/A'}</span></div>
        <div class="wm-row"><span class="wm-label">Updated:</span>
            <span class="wm-value">${heartbeat.timestamp ?? 'N/A'}</span></div>
    </div>`;
}
```

Call this in the appropriate render function and pass `snapshot.overnight_heartbeat`.

### CSS additions (styles.css)

```css
.worker-monitor-card {
    border: 1px solid var(--border, #444);
    padding: 0.75rem 1rem;
    margin: 0.5rem 0;
    font-family: monospace;
    font-size: 0.85rem;
}
.wm-header {
    font-weight: bold;
    color: var(--accent, #aaa);
    margin-bottom: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.wm-row { display: flex; gap: 1rem; line-height: 1.6; }
.wm-label { color: var(--muted, #888); min-width: 80px; }
.wm-value { color: var(--text, #ccc); }
.wm-offline { color: var(--muted, #888); font-style: italic; }
```

---

## Validation

```bash
node --check MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/app.js
# Expected: PASS

cd C:\LAB\Tradingview_LAB_CLEAN
set PYTHONPATH=MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api
python -m pytest MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests -q
# Expected: 35 passed — must not regress

# Start dashboard and verify:
cd MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api && python -m mcc_readonly serve
# Open http://127.0.0.1:8765/dashboard
# Worker Monitor card should appear showing "Offline" state (no heartbeat files yet)
```

---

## HARD SAFETY RULES

- NEVER edit: `*.pine` files, any file in `02_MTC_BACKTEST/src/engine/`, `mega_walk_forward.py`
- NEVER edit: `apps/api/mcc_readonly/*.py` files
- NEVER edit `05_REGISTRY/*.json`
- app.js is single-writer — one coherent edit pass only
- Only write to:
  - `08_DASHBOARD_APP/apps/web/app.js`
  - `08_DASHBOARD_APP/apps/web/styles.css`
  - `08_DASHBOARD_APP/apps/web/index.html` (only if mount point div needed)

---

## Report output

Write your complete report to EXACTLY this path:
`C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\_AI_MEMORY\PARALLEL_AGENT_REPORTS\S6_D3B_WORKER_MONITOR_REPORT.md`

Report must contain:
- D3a prerequisite check result (pass/fail)
- Which function added and at what line in app.js
- Where the widget renders in the UI (tab/section name)
- `node --check` result
- API test result (N passed)
- Browser verification: does the "Offline" state render correctly?
