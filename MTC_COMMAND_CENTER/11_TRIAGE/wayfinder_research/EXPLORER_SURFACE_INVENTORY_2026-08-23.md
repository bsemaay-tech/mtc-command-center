# Explorer Surface Inventory — Research-Side Browse/Display Surfaces

**Date:** 2026-08-23 · **Wayfinder ticket:** #80 (map #78) · **Branch:** `research/explorer-surface-inventory`
**Baseline:** `master` @ `ab35ca66` · **Method:** read-only file/code inspection, no servers run, no network calls.
**Feeds:** the map #78 minimum-vs-advanced ticket for a future research explorer.

## Scope note on repo state

Two of the five items named in the ticket (`Deepreseach` / `Deepresearc 2`) exist **only** as
untracked files in the main checkout `C:\LAB\Tradingview_LAB_CLEAN` — they are not on `master`
and therefore do not exist in this worktree (`C:\WFE1`). They were inspected read-only, in place,
from the main checkout without modifying anything there, per the ticket's instruction to inventory
them.

## Summary verdict table

| # | Surface | Location | Data nature | Staleness (as of 2026-08-23) | Verdict for a future explorer |
|---|---|---|---|---|---|
| 1 | `mcc_readonly` reader/API layer | `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/*.py` | Real, live-filesystem-backed JSON/CSV read model | Reader code last touched Jun–Jul 2026 (7–12 weeks); some source data (e.g. `STRATEGY_REGISTRY.json`, QuantLens candidate registry) frozen since 2026-05-31 | **Reusable** — this is the only real data-access layer in the whole inventory. Keep the read-only aggregation pattern (per-file reader → `read_model.py` → cached snapshot → HTTP), extend rather than replace. |
| 2 | "Strategy Intelligence Command Center" web app | `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/{index.html,app.js,styles.css}` | Renders the live snapshot from #1 | `app.js` last touched 2026-07-13; `README.md`'s 10-tab list is stale against the 14-page `PAGE_FEEDS` table actually in code | **Reusable** — flagship "Strategy Detail" page and "Backtest Result Explorer" preview are the closest existing thing to a research explorer today. Vanilla JS/no framework/no build step; safe to extend in place or fork as a starting skeleton. |
| 3 | Dashboard V2 read-only prototype | `IBKR_PAPER_BRIDGE/dashboard_v2_prototype/` | 100% synthetic fixture JSON, frozen `as_of: 2026-08-18T02:40:00Z` | Newest artifact in this inventory (merged `31906ee1`, 2026-08-17/18); by construction it can never go stale because it never reads real data | **Reusable as UI/interaction reference only, dead as a data path.** Good source for the V2 visual vocabulary (worker identity tuple, Guardian veto tiers, three-layer desired/accepted/actual model, phone layout) — but it is Bridge **execution**-side (workers, orders, Guardian), not research-side, and is fixture-only with zero wiring to anything real. |
| 4 | "QuantLens report pages" | No standalone app exists (see below) — QuantLens data reaches users only through surfaces #1/#2, plus a mostly-empty Reports tab and a dead prototype set | Mixed | Reports tab content root (`04_REPORTS/quantlens/`) contains only `.gitkeep` — no live reports; `legacy_web_prototypes/` frozen 2026-06-16 | **Half reusable, half dead.** QuantLens registry/scorecard/audit data is real and live via readers #1 (reusable). The dedicated "Reports" viewer is real code but has no content today. The 10 `legacy_web_prototypes/*.html` mockups are explicitly labeled dead ("NOT loaded by the live dashboard", "throwaway"), superseded by the shipped app — reference only. |
| 5 | `apps/Deepreseach/` + `apps/Deepresearc 2/` | `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/Deepreseach*` (untracked, main checkout only) | Static AI-authored research markdown + a few screenshot PNGs, not code | Deepreseach: 2026-08-18; Deepresearc 2: 2026-08-20 | **Dead as a surface** — these are not browse/display code, they are dropped-in AI research exports (ChatGPT/Gemini/Grok/DeepSeek/Perplexity/Manus reports on dashboard/observability architecture) sitting inside the `apps/` code directory by accident. Nothing imports or serves them. Worth relocating out of `apps/` (e.g. into `11_TRIAGE/` or a research-notes folder) as housekeeping, but that's a separate, out-of-scope cleanup — not an explorer-input decision. |

---

## 1. `mcc_readonly` dashboard readers (data layer)

Path: `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/`

This is a pure read-only Python package: one "reader" module per data domain, all composed by
`read_model.py::build_read_model()` / `build_dashboard_snapshot_cached()` into one JSON snapshot,
served by `server.py` (stdlib `http.server`, no framework) at `/api/snapshot`, `/api/read-model`,
`/api/report`, `/api/scorecard-detail`, `/healthz`. POST/PUT/PATCH/DELETE are hard-rejected
("MVP-1 API is read-only"). `paths.py` resolves `mcc_root`/`quantlens_root` via
`00_CONFIG/paths.example.json` + `paths.local.json` overlay.

| Reader | Shows | Source files | Last touched |
|---|---|---|---|
| `read_model.py` | Aggregates everything below into one snapshot + JSON-schema validates each `READ_MODEL_FILES` entry | `03_STATUS/*.json`, `02_TASKS/*.json`, `05_REGISTRY/STRATEGY_REGISTRY.json`, `00_CONFIG/*.json` | 2026-07-05 |
| `registry_reader.py` | Strategy registry (candidate list, backtest result links, promoted-to-parity status) | `03_QUANTLENS/_registry/quantlens_candidate_registry.{csv,jsonl}`, `05_BACKTEST_RESULTS/{id}_results.json`/`_summary.md`, `06_PROMOTED_TO_PARITY/` | 2026-06-06 |
| `scorecard_reader.py` | Per-strategy Gate 1/1B/2/3 scorecards, canonical display rows | scorecard artifacts under QuantLens results tree | 2026-06-08 |
| `audit_reader.py` (56 KB, largest reader) | Candidate audit trail / AI verdict authoring evidence | `00_INBOX_REPORTS`, `research/` under QuantLens root | 2026-06-06 |
| `pipeline_reader.py` (56 KB) | 6-stage candidate pipeline board (DISCOVERED → BACKTESTED → PROMOTED → …), one next-action per candidate | Joins registry + pine builder + liveops + parity + backtest readers by candidate id | not individually dated (co-changes with above) |
| `expert_quantlens_reader.py` | AI QuantLens verdict registry | `05_REGISTRY/AI_QUANTLENS_VERDICT_REGISTRY.json` | — |
| `ai_names_reader.py` | AI-assigned strategy display names | `05_REGISTRY/AI_STRATEGY_NAME_REGISTRY.json` | — |
| `ai_tasks_reader.py` | Copy-ready AI prompt template library | `05_REGISTRY/AI_TASKS.json` | — |
| `param_specs_reader.py` | Per-strategy optimizable vs. hardcoded parameter grid | `05_REGISTRY/STRATEGY_PARAM_SPECS.json` (generated by `03_QUANTLENS/tools/build_strategy_param_specs.py`) | — |
| `research_reader.py` | Strategy research classification (confidently-classified fields, `review_needed` flag) | `05_REGISTRY/` | — |
| `backtest_reader.py` | Backtest run status/results | `06_QUANTLENS_LAB/05_BACKTEST_RESULTS/`, `reports/optimization` | — |
| `night_artifacts_reader.py` | Night backtest artifact contract: run plans/status, **profile-separated results** (`SOURCE_NAKED`/`RISK_NORMALIZED`/`MTC_LIGHT`/`FULL_MTC_CANDIDATE`), top results, leaderboard delta. States each artifact `absent/invalid/incomplete/usable`. Bounded to 150 run dirs, 4 MB/file. | `05_BACKTEST_RESULTS/` per-run dirs | — |
| `validation_reader.py` | Strategy Validation Terminal: funnel, survivors, graveyard, IS/OOS scatter, cross-asset consistency — pure in-memory aggregation | Derived from `night_artifacts["profile_results"]`, no disk re-read | — |
| `optimization_reader.py` | Optimization Lab run/candidate/risk-note inspection, worker-scaling benchmark | `reports/optimization/`, `worker_scaling_benchmark/summaries/WORKER_SCALING_SUMMARY.csv` | — |
| `pine_builder_reader.py` | Pine draft status | `06_QUANTLENS_LAB/06_PROMOTED_TO_PARITY` | — |
| `parity_reader.py` | Pine/Python parity results | `_nightly/parity_results.json` | — |
| `mtc_v2_reader.py` | MTC V2 readiness (Pine source presence, architecture doc presence, parity case tracker) | `01_PINE/MTC_V2.pine`, `03_DOCS/MTC_V2_ARCHITECTURE.md`, `05_PARITY/MTC_V2_PARITY_CASES.csv` | — |
| `liveops_reader.py` | LiveOps dry-run status | `03_STATUS/LIVEOPS_STATUS.json` | — |
| `system_test_reader.py` | System Test Lab (fake-money plumbing evidence, firewalled from paper/testnet/live) | QuantLens `system_test/` | — |
| `heartbeat_reader.py` | Overnight run heartbeat | overnight run dir | — |
| `presentation_reader.py` | Action-hint text mapping + canonical scorecard builder used by other readers | `11_TRIAGE/strategies/_stg_code_map.json` | — |
| `task_lifecycle.py`, `schema.py`, `json_io.py`, `health.py`, `writer.py`, `cli.py` | Support: task-state helpers, JSON-schema validator, safe file read, `/healthz` builder, (unused-by-readers) write path, CLI entrypoint | — | — |

**Verdict:** this package is the one genuinely reusable asset for a future explorer's *backend*.
It already does exactly the job an explorer needs — discover artifacts on disk, tolerate
missing/invalid files, validate against JSON Schema, cache with a 30 s TTL — for every research
domain except raw per-trial backtest data (see Cross-cutting finding below).

---

## 2. "Strategy Intelligence Command Center" web app

Path: `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/` (`index.html`, `app.js` — 154 KB/~2600
lines, `styles.css` — 43 KB, `README.md`, `PRODUCT.md`, `DESIGN.md`)

Vanilla JS single-page app, no framework, no build step, no bundler. Served as static files by
`mcc_readonly`'s own HTTP server (`GET /dashboard`, `GET /web/*`) — same-origin, no CORS surface.
Run instructions (`README.md`): `python -m mcc_readonly serve --host 127.0.0.1 --port 8765`, open
`http://127.0.0.1:8765/dashboard`. **Not run in this investigation** (read-only instruction).

Consumes `/api/snapshot` (cached, `?refresh=1` to bypass), lazy-loads
`/api/scorecard-detail?strategy_id=` for full per-card detail (sub_scores/notes are dropped from
the default snapshot to keep it small), and `/api/report?path=` for the Reports tab.

`PRODUCT.md` states the design intent directly: *"A read-only command center for reviewing
trading-strategy research candidates as they move through a gated evaluation pipeline (Gate 1
intake → Gate 1B MTC feasibility → Gate 2 backtest evidence → Gate 3 production readiness → paper
trading). The flagship surface is Strategy Detail... It renders a snapshot read model. It never
writes, triggers runs, or executes trades."* This framing (viewing ≠ acting) matches the
explorer's own likely constraints.

Actual page list in code (`PAGE_FEEDS` in `app.js`, 14 entries — the shipped `README.md`'s
10-tab list is stale against this):

| Page | Data feed |
|---|---|
| Home / Command Center | `candidate_pipeline`, `scorecards`, `backtest_status`, `report_manifest`, `file_diagnostics` |
| Strategy Pipeline | `candidate_pipeline.rows` |
| Strategy Registry | `strategy_registry.candidates` |
| **Strategy Intelligence** (flagship, `renderIntelligence`) | `candidate_pipeline.rows[].scorecard_v2`, `expert_quantlens_verdict`, `canonical`, `strategy_registry` — 7 sub-sections incl. Gate 1/1B, AI Verdict, Backtest Plan & Evidence, **Backtest Result Explorer**, Paper Trading Readiness, Advanced Technical Details |
| Backtest Planner | `night_artifacts.run_plans`, `candidate_pipeline` |
| Backtest Runs | `night_artifacts.run_status`, `backtest_status.runs`, `overnight_heartbeat` |
| **Backtest Result Explorer** (own top-level page) | `night_artifacts.profile_results`, `scorecards.cards` |
| Strategy Leaderboard | `night_artifacts.profile_results`, `night_artifacts.leaderboard_delta`, `scorecards.cards` |
| Promotion Readiness | `candidate_pipeline.rows`, `scorecards.gate_summary` |
| System Test Lab | `system_test_status` |
| AI Knowledge Base | `strategy_registry.candidate_kind`, `strategy_research` |
| Advanced Artifacts | `night_artifacts` (run_plans, run_status, artifact_index, profile_results, top_results, leaderboard_delta, benchmark_update_candidates) |
| Diagnostics | `healthz`, `file_diagnostics`, `night_artifacts.summary` |
| Reports | `report_manifest.reports` |
| Read Model / Data Model | all snapshot top-level keys (raw JSON viewer) |

**Backtest Result Explorer, in detail (`explorerPreviewSection()`, app.js:1359-1394):** for a
strategy it shows the best profile-separated result — profile bucket, symbol/timeframe, score,
net profit %, max drawdown %, run id — with an explicit "same-bucket rule: compare only within
identical profile, timeframe, market universe, and score method" warning, and a
"Open Backtest Result Explorer (strategy scope)" button. This is the single closest existing
artifact to what a future research explorer would need to become.

**Design docs (`PRODUCT.md`/`DESIGN.md`):** describe a deliberate "precise · calm · expert"
dark command-center identity (teal/slate, JetBrains Mono for data), explicitly anti-clutter,
explicitly not aimed at first-time users. `DESIGN.md`'s token system is called "committed —
preserve."

**Verdict:** **Reusable.** This is the only end-to-end, currently-shipped, real-data research
browse surface in the repo. No build tooling to fight, no framework lock-in, and the JS is
already organized as one render-function-per-page keyed off one JSON snapshot — a pattern an
explorer can extend directly (new page = new render function + new `PAGE_FEEDS` row) rather than
rebuilding.

---

## 3. Dashboard V2 read-only prototype (accepted backlog-night package 3)

Path: `IBKR_PAPER_BRIDGE/dashboard_v2_prototype/` (`index.html`, `app.css`, `app.js` — 845 lines,
`fixtures/{workers.json, intents.json, market_context.json, data.js, build_data_js.py}`, `README.md`)

**Provenance:** accepted 2026-08-17/18 night per
`MTC_COMMAND_CENTER/11_TRIAGE/GATE1_PACKAGE3_DASHBOARD_V2_PROTOTYPE_2026-08-18.md` (Gate-1 scope
record) and `BRIDGE_V2_PACKAGES_345A_T1_ACCEPTANCE_2026-08-18.md` (acceptance record: committed
`31906ee1` on `feature/bridge-v2-package3`, accepted at `303c6d9a`, **verdict ACCEPT round 2**).
Merged to `master`; present in this worktree.

**What it shows (5 views, tab-navigated):**
1. **Overview** — aggregate execution summary: worker counts, summed per-worker P&L, worker
   table (window state, feed age, entry status, block reasons), Portfolio Guardian panel (state,
   active vetoes, 3 veto tiers, fail-closed rules), shared-infrastructure panel (REST weight +
   WebSocket budget usage).
2. **Worker detail** — 7-field worker identity tuple, health/freshness, block reasons, per-worker
   ledger, account-label panel.
3. **Market context** — context-only symbol cards, explicitly labeled CONTEXT/NON-ACTIONABLE.
4. **Three layers** — desired / accepted / exchange-truth swim-lanes per intent, with 8
   deliberately-chosen divergent synthetic cases (superseded stop update, freshness reject,
   Guardian veto, partial fill, UNKNOWN_SUBMISSION frozen pending reconciliation, blocked
   duplicate delivery).
5. **Phone monitor** — 390 px-wide responsive monitoring layout.

**From which files:** `fixtures/workers.json` (three synthetic workers: one healthy, one
stale-feed/`BLOCKED:FEED_STALE`, one Guardian-paused/`REJECTED:GUARDIAN_VETO`), `intents.json`
(layer definitions + 8-intent synthetic stream), `market_context.json` (BTC/ETH/SOL context
snapshots), `data.js` (hand-mirrored loader consumed by `index.html` — README flags it must be
regenerated via `build_data_js.py` and diffed if the JSON source changes).

**How stale:** by design, never — everything is pinned to a frozen fixture timestamp
(`meta.as_of: "2026-08-18T02:40:00Z"`), and every "age" shown on the page is computed relative to
that frozen time, never wall clock, specifically so the page can never imply liveness it doesn't
have. `fixtures/workers.json`'s own `meta.data_nature` states: *"SYNTHETIC FIXTURE DATA. There is
no live bridge, no exchange connection and no worker process behind these values."*

**Hard boundaries (from the Gate-1 record, verified in the README):** new directory only, zero
modification to any existing file (explicitly including the frozen V1 Bridge execution dashboard
at `IBKR_PAPER_BRIDGE/bridge/static/`, which it used only as visual-language reference); zero
network calls of any kind (no fetch/XHR/WebSocket/EventSource, no CDN, no web fonts); zero
ARM/order/kill/config controls, not even disabled mock buttons; no server, no build step, no new
dependency. `README.md`: *"This prototype activates nothing, wires nothing, and authorizes
nothing. It is Tier T1 display work."*

**Verdict:** **Reusable as a UI/interaction-vocabulary reference; dead as a data path.** It is
also the wrong domain for a *research* explorer specifically — it renders the Bridge's proposed
V2 **execution** surface (multi-worker live trading state, Guardian vetoes, order-layer
reconciliation), not research/backtest data. Its real value for map #78 is the demonstrated
three-layer state-labeling pattern (every panel names which truth layer it shows) and the
phone-responsive layout — both transferable interaction patterns, zero transferable code/data
wiring.

---

## 4. "QuantLens report pages"

There is **no standalone QuantLens web app or report-page surface** distinct from what's already
covered above. QuantLens data reaches a human through exactly two paths:

**a) Live, through the web app's readers.** `registry_reader.py`, `scorecard_reader.py`,
`audit_reader.py`, `expert_quantlens_reader.py`, `pipeline_reader.py`, `validation_reader.py` all
pull from the QuantLens tree (`06_QUANTLENS_LAB` / `03_QUANTLENS` per `default_quantlens_root()`
candidate-path resolution in `paths.py`) and render through the Strategy Registry / Strategy
Intelligence / Backtest Result Explorer / Strategy Leaderboard / Promotion Readiness / Validation
Terminal pages already itemized in §2. This is real and current (subject to the same reader-code
staleness noted in §1).

**b) The dashboard's "Reports" tab**, backed by `report_manifest.reports` and served through
`GET /api/report?path=` (path is validated to stay inside `04_REPORTS/`). Today
`MTC_COMMAND_CENTER/04_REPORTS/quantlens/` contains only a `.gitkeep` — **the manifest has
nothing to show**; the plumbing is real but the content pipeline that would populate it isn't
producing output into this location right now.

**c) `11_TRIAGE/ui_references/legacy_web_prototypes/`** (10 static HTML files + 1 CSS,
14–25 KB each, last touched 2026-06-16) — throwaway hand-filled mockups for the Strategy Detail
page redesign (SP-005), explicitly companion to
`03_QUANTLENS/_user_guide/11_STRATEGY_DETAIL_PAGE_REDESIGN_PLAN.md`. The directory's own
`README.md` documents three design rounds (v1 A/B/C → v2 B2 clinical/terminal/editorial → v3
terminal stage set) with an explicit **decision log**: v1 "B (single-scroll)" selected, v2
"terminal" aesthetic selected, ending with a 5-file "v3 terminal stage set" as the actual Wave-A
sign-off target. Every file's own HTML comment states *"Not loaded by the app."* — these directly
predate and were superseded by the shipped `apps/web/app.js` "Strategy Intelligence" page (dark
teal/mono terminal identity in `PRODUCT.md`/`DESIGN.md` matches the "terminal" direction chosen
here).

**Verdict:** the *data* half is reusable (already covered in §1/§2, no separate action needed);
the *dedicated-report-viewer* half is real but currently empty (plumbing without content); the
*legacy prototype* half is dead code kept intentionally as design-decision history — useful to
skim for why the current visual identity looks the way it does, not to build on.

---

## 5. Stray `apps/Deepreseach*` directories

Both directories sit inside `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/` — the same parent as the
real `api/` and `web/` app directories — but neither is tracked in git (both show as `??` in
`git status` on the main checkout) and neither exists on `master`/in this worktree.

**`apps/Deepreseach/`** (2026-08-18): `Chatgbt.md` (397 lines, Turkish-language deep-research
report critiquing a dashboard architecture proposal — reconciliation cadence, alert taxonomy,
incident-response UX, journal schema, security baseline), `Gemini.md` (0 bytes, empty),
`MAnus Dashboard & Observability for a Bar-Close Retail Trading Bot.md` (315 lines, English,
comparative feature inventory across Freqtrade/FreqUI, Jesse, OctoBot, Hummingbot, NautilusTrader,
Gekko, with a recommended "incident cockpit + trade journal" design), `deepseek_markdown_...md`
(444 lines), `grok.md` (243 lines), `preplexity.md` (234 lines) — six independent AI research
outputs on the same dashboard/observability design question, plus `Protatip resimler/Cloude 1/`
(4 PNG screenshots, apparently reference mockup images).

**`apps/Deepresearc 2/`** (2026-08-20, note the folder-name typo differs from the first): only
`Chatgbt.md` and `Gemini.md` — content is *different* from the first folder's same-named files
(this one's `Chatgbt.md` opens "MRC Bridge — Open-Source Technical Foundation Investigation," a
different research question about build-vs-buy technical foundations, not the dashboard UX
question in folder 1).

**Verdict:** **Dead as a browse/display surface** — these are not code, not served, not imported,
not referenced by any reader or the web app. They are AI research deliverables that were saved
directly into a source-code `apps/` directory instead of a docs/triage location, and the
duplicate/near-duplicate naming across the two folders (`Chatgbt.md`, `Gemini.md` present in both
with different content) suggests this happened at least twice without cleanup. There is real
research content in here (the MAnus/DeepSeek comparative-systems report in particular has
citations to Freqtrade/NautilusTrader/Google-SRE-style operational patterns that could inform
future explorer design), so the recommendation is **relocate and rename, don't delete outright**
— but that's a housekeeping action outside this ticket's read-only scope.

---

## Adjacent surface noted but out of scope: Bridge V1 execution dashboard

`IBKR_PAPER_BRIDGE/bridge/static/` (`index.html`, `app.js` 22 KB, `app.css` 12 KB,
`help_map.json` 113 KB) is the live Bridge's **execution**-side dashboard (ARM/DISARM/KILL,
orders, positions) — referenced by the Dashboard V2 prototype's README as "visual-language
reference only," never modified by it. This is execution-side, not research-side, so it's outside
this ticket's named scope; flagged here only because the V2 prototype (§3) explicitly names it as
its design ancestor.

---

## Cross-cutting finding relevant to "minimum vs. advanced" explorer scoping

The most consequential fact for map #78's next ticket is not any single surface's staleness — it
is a **data-granularity ceiling shared by every research surface above**: `night_artifacts_reader.py`'s
own contract docstring states artifacts are discovered per run directory and states each as
`absent/invalid/incomplete/usable`; `backtest_profile_result.json` carries **summary-level**
profile results (score, net profit, max drawdown, run id) — there is no raw per-trial/per-run
artifact contract anywhere in this reader set. The Backtest Result Explorer preview in §2 and the
Advanced Artifacts / Strategy Leaderboard pages all read from this same summary-level
`profile_results` collection. Concretely: **an explorer that wants to browse individual trials
(not just the best-summary row per strategy/profile bucket) has nothing to read today** — the
data simply is not written at that granularity. Any "advanced" explorer scope that assumes
trial-level drill-down needs a new writer/artifact contract first, not just a new UI; a "minimum"
scope that stays at the current summary level can be built by extending §1/§2 directly with no new
data plumbing.

## Staleness reference (last git-log touch, informal, for orientation only)

| Path | Last touched |
|---|---|
| `apps/api/mcc_readonly/registry_reader.py` | 2026-06-06 |
| `apps/api/mcc_readonly/audit_reader.py` | 2026-06-06 |
| `apps/api/mcc_readonly/scorecard_reader.py` | 2026-06-08 |
| `apps/api/mcc_readonly/read_model.py` | 2026-07-05 |
| `03_STATUS/CURRENT_STATUS.json` | 2026-07-05 |
| `apps/web/app.js` | 2026-07-13 |
| `05_REGISTRY/STRATEGY_REGISTRY.json` | 2026-05-31 |
| `03_QUANTLENS/_registry/quantlens_candidate_registry.csv` | 2026-05-31 |
| `11_TRIAGE/ui_references/legacy_web_prototypes/proto_A_tabbed.html` | 2026-06-16 |
| `IBKR_PAPER_BRIDGE/dashboard_v2_prototype/index.html` | 2026-08-17 |
| `apps/Deepreseach/*` (main checkout, untracked) | 2026-08-18 |
| `apps/Deepresearc 2/*` (main checkout, untracked) | 2026-08-20 |
