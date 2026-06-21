# Dashboard Targeted Patch Report — 2026-06-15

Targeted cleanup patch applied to the served vanilla SPA dashboard after the Strategy
Intelligence UI integration. No redesign. Dark shell + route structure preserved.
Read-only throughout; no execution / write-back / trading affordances added.

## 1. Files changed
- `08_DASHBOARD_APP/apps/web/app.js` — fixes #1, #2, #3, #4, #6, #7.
- `08_DASHBOARD_APP/apps/web/styles.css` — `.constraint-notice` styles (fix #4).
- `08_DASHBOARD_APP/apps/web/index.html` — cache bust `app.js?v=2` → `?v=3`.
- `08_DASHBOARD_APP/apps/web/prototypes/` → moved to
  `11_TRIAGE/ui_references/legacy_web_prototypes/` via `git mv` (fix #5).
- `_AI_MEMORY/SESSION_LOG.md` — handoff + test command doc (fix #8).

## 2. Files intentionally NOT changed
- Pine scripts, MTC_V2, backtest engine, broker/live/paper execution, strategy execution — untouched.
- Read-only API (`server.py`, readers, schema) — untouched; no POST/PUT/PATCH/DELETE added.
- `apps/api/tests/*` — not modified (no application-logic "test fixes"; suite already green).
- React/Vite reference under `11_TRIAGE/ui_references/google_strategy_intelligence_v2_final` — reference only, not imported.

## 3. Exact fixes applied
1. **Execution wording removed** (`app.js`):
   - `Execution Source` → `Evidence Source` ("Local status observed — read-only").
   - `Backtest Execution Prep` → `Backtest Evidence Review`.
   - Rail `Execution Mode / Read-only` → `Review State / Read-only`; `Backtest Execution / Manual trigger` → `Backtest Evidence / Manual review required`; `AI Planning Local` → `Review only`; `Morning Summary Artifact` → `Artifact review only`.
   - Planner banner reworded: "Artifact review only — no run-trigger or write-back affordances exist here." (dropped "control local workers / trigger runs").
2. **Leaderboard category claims fixed** (Option B): cards renamed `Top Gate 2 Reference #1..#4`; header `Top Gate 2 References`; warning banner "Category/profile-separated leaderboard artifacts are not present. These cards are legacy Gate 2 references, not validated category winners." Net Profit / Drawdown `N/A` → `Profile artifact missing`; empty card → `No validated candidate`.
3. **Result Explorer legacy quarantine**: official buckets (SOURCE_NAKED / RISK_NORMALIZED / MTC_LIGHT / FULL_MTC_CANDIDATE) are now all empty with `No profile-separated result artifact yet.` Non-profile rows moved to a dedicated `Legacy Scorecard Reference — profile missing` section. Added **Active Comparison State** (Score method / Profile / Timeframe / Symbol-universe / Run ID / Artifact status) and **read-only disabled Filters** with label "Filter controls pending profile-separated artifact reader." Same-bucket warning retained.
4. **Research Constraint Notice**: prominent full-width red banner on Strategy Intelligence detail, placed below hero/workflow and above Gate Status Summary (separate from right rail). Lists detected blockers (missing entry/exit/source, Gate 2 not validated, direction undefined, blocking gates). Only shown when blockers exist.
5. **Prototypes moved** out of served `/web/` root to `11_TRIAGE/ui_references/legacy_web_prototypes/` (git mv, not deleted). Web root now holds only `index.html`, `app.js`, `styles.css`, `README.md`.
6. **"Method not extracted" spam reduced**: removed from compact pipeline cards (replaced with `Instrument`); in Registry detail + Strategy Intelligence taxonomy it is now a muted/italic empty-state "Method extraction reader not implemented" (not a strong data value).
7. **Pipeline KPI strip** (Option B) added above cards: Total / Gate 1 OK / Gate 1B OK / Gate 2 Failed / Rule Freeze Needed / Paper Locked. Card grid + filters + search retained.

## 4. Screenshot / visual QA summary (live, app.js?v=3)
- **Home** — metric strip, action queue, gate system, benchmark board: intact, dark theme preserved.
- **Strategy Pipeline** — KPI strip live (Total 176 · G1 10 · G1B 10 · G2 fail 5 · Rule freeze 176 · Paper locked 176); cards show `Instrument` (e.g. TRXUSDT), no "Method not extracted" spam.
- **Strategy Intelligence detail** — Research Constraint Notice renders as prominent red banner with blocker list, correctly positioned below workflow bar.
- **Backtest Result Explorer** — Active Comparison State + disabled Filters + "Profile-separated artifacts not present" banner; official buckets empty ("No profile-separated result artifact yet"); `Legacy Scorecard Reference — profile missing` (837 rows) quarantined below.
- **Strategy Leaderboard** — "NOT VALIDATED CATEGORY WINNERS" warning; cards `Top Gate 2 Reference #1..#4`; Net Prof / Drawdown = "Profile artifact missing".
- **Strategy Registry / Backtest Planner / Paper Trading / Diagnostics / Read Model** — unchanged structurally (wording-only / no change); verified clean via source greps and prior-session visual QA. Planner banner reworded; rail wording reworded.

## 5. Safety wording search results
`grep -niE 'Execution Source|Backtest Execution|Manual trigger|Manual local worker|Launch|Deploy|\bExecute\b|Run Now|Start Backtest|Broker Socket|Safe to trade|Connect broker|Live trading' app.js index.html`
→ **NONE** (all clear).

## 6. Old shell / demo data search results
- `class="tabs" | data-tab= | tab-panel` → **NONE**.
- `STG-084 | STG-112 | 68.76 | 89.2 | BTCUSDT | ETHUSDT` → **NONE** (no hardcoded demo data; all values come from snapshot).

## 7. Snapshot response timing (127.0.0.1:8765)
- `/api/snapshot` (cold cache build): **~12.57 s**, HTTP 200.
- `/api/snapshot?refresh=1`: **~11.75 s**, HTTP 200.
- `/api/snapshot` (warm cache): **~1.10 s**, HTTP 200.
- `/healthz`: `mode=read_only`, `overall_ok=true`, `checks.read_only=true`.

## 8. Test results
- `node --check apps/web/app.js` → **PASS** (JS_OK).
- API suite: `Ran 39 tests in 52.7s` → **OK**.
  - Linux/macOS: `cd MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api && PYTHONPATH=. python -m unittest discover tests`
  - Windows PowerShell: `cd MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api; $env:PYTHONPATH="."; python -m unittest discover tests`

## 9. Remaining limitations
- Raw KPIs (net profit, profit factor, drawdown, win rate, equity/trade charts) remain absent from the read model → shown as explicit missing states, never faked.
- No `backtest_profile_result.json` / profile-separated artifact exists → all four official profile buckets stay empty by design; only legacy Gate 2 references are available.
- Explorer filters are non-functional placeholders pending a profile-separated artifact reader.
- Pipeline "Rule Freeze Needed" and "Paper Locked" both = 176 because no candidate is promotable and exit/direction metadata is broadly unextracted (accurate, not a bug).
- Cold snapshot build is ~12 s; warm cache ~1 s. Consider a warm-on-start prefetch if first paint latency matters.

## 10. Recommended next patch (if any)
- Implement a profile-separated artifact reader (`backtest_profile_result.json`) so official buckets and real KPIs populate; then activate the Explorer filters.
- Add a snapshot warm-up call at server start to remove the ~12 s cold first-load.
- Optional: Pipeline list/table toggle (Option A) in addition to the KPI strip for very large sets.
