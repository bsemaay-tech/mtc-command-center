# Codex Continuation Brief — MTC Command Center (2026-05-30)

You are continuing development of **MTC Command Center (MCC)**, a local, read-only
dashboard + memory system over the existing MTC_v2 / QuantLens trading-research workflow.
A previous Claude session added a **Strategy Pipeline** view on top of the MVP-8 baseline.
This brief tells you everything needed to continue cold.

## 0. Hard guardrails (do not break)

- **Read-only + dry-run only.** No live trading, no webhooks, no broker calls.
- **Do NOT modify** MTC_v2 core, `01_MASTER TEMPLATE_V2/01_PINE/MTC_V2.pine`, the PineTS engine,
  or TradingView exports. MCC only READS those via paths.
- HTTP API stays read-only (mutations return 405). The only allowed write path is the existing
  controlled task-writer CLI gate.
- Dependency-free Python (stdlib only) for the API; vanilla JS for the web app. Keep it that way.
- The QuantLens lab `01_MASTER TEMPLATE_V2/06_QUANTLENS_LAB/` is **git-ignored**; MCC reads it but
  must tolerate it being absent/partial. MCC itself IS tracked in git.

## 1. Repo / run

- MCC root: `C:\LAB\tradingview-lab\MTC_COMMAND_CENTER`
- App: `08_DASHBOARD_APP/apps/api` (Python pkg `mcc_readonly`) + `08_DASHBOARD_APP/apps/web` (JS).
- Run from `apps/api`:
  - `python -m pytest tests/`  → must stay **22 passed** (add tests, don't break these).
  - `python -m mcc_readonly health` → `overall_ok=true`.
  - `python -m mcc_readonly serve --host 127.0.0.1 --port 8765` → `http://127.0.0.1:8765/dashboard`.
- After Python changes you MUST restart the server to see them; web files are static (just refresh).

## 2. What Claude added (Strategy Pipeline) — understand before extending

The dashboard was domain-siloed (Tasks/Parity/Backtest/Registry/...). Claude added a
**candidate-centric pipeline**: every strategy is one row across 6 stages, with a per-row next
action and a clickable detail page.

Files:
- NEW `apps/api/mcc_readonly/pipeline_reader.py` → `build_candidate_pipeline(mcc_root, registry,
  pine_builder, liveops, parity, backtest)`. Pure read-only join. Returns
  `{schema_version, mode, stages[6], summary{stage_done_counts}, rows[]}`.
  Each row: `{id, name, symbol, timeframe, origin_candidate, stages{<key>:{status,metric}},
  current_stage_key, next_stage_key, next_action, notes, source_url, description{family,what,entry,exit},
  metrics{...}, pinets_parity}`.
- `read_model.py` → `build_dashboard_snapshot` now calls it and exposes `candidate_pipeline`.
- Web `index.html` → Pipeline tab (default first) + panel (`#pipelineSummary`, `#pipelineTableWrap`,
  `#pipelineRows`, `#pipelineDetail`, `#pipelineIntro`).
- Web `app.js` → `renderPipeline()`, `stageCell()`, `stageCls()`, `stageIcon()`, `ytEmbed()`,
  `openStrategyDetail(id)`, `closeStrategyDetail()`. Rows are clickable (delegated listener on `#pipelineRows`).
- Web `styles.css` → `.badge.stage-active/.stage-pending/.stage-na`, `.muted-sub`, `tr.row-click`,
  `.detail-grid`, `.kv`, `.stage-list`, `.yt-embed`, `.back-btn`, etc.

6 stages: `discovered → backtested → promoted → pre_parity → paper_trade → integrated`.
Status values: `done | active | pending | fail | na`. Stage derivation + plain-language Turkish
descriptions live entirely in `pipeline_reader.py` (`DESCRIPTIONS` list matched by token in id/name).

Join keys: `registry.candidates[].candidate_id` (14 early items), `registry.strategies[].strategy_id`
(3 promoted QL_ALPHA_* with metrics; `.candidate_id` links to origin), `pine_builder.drafts[].candidate_id`,
`liveops.paper_trade_plans[].candidate_id`, and `06_PROMOTED_TO_PARITY/<id>/PINETS_PARITY_RESULT.json`.

Current live snapshot: 15 rows; done counts discovered 15 / backtested 12 / promoted 3 / pre_parity 1.
LINK 8EMA is furthest (PineTS parity PASS). ADA + LTC promoted, PineTS parity is their next step.

## 3. Next tasks (priority order)

**T1 — Detail page enrichment** (the user explicitly asked for these):
   a) **Paper-trade results area**: read `06_PROMOTED_TO_PARITY/<id>/FORWARD_PAPER_TRADE_PLAN.md`
      (and any future forward results file) and show plan status + (when present) live forward
      metrics. Add the data in `pipeline_reader` row (`paper_trade_detail`) and render in `openStrategyDetail`.
   b) **Small equity sparkline**: for promoted strategies, read the trades CSV
      (`06_PROMOTED_TO_PARITY/<id>/<id>_trades.csv` — column `ret_net_pct`) or the results JSON,
      compute a cumulative equity series, and draw a tiny inline SVG sparkline in the detail page
      (no charting library — build SVG path string in JS). Keep it lightweight.
   c) **Machine-readable parity-proof block**: surface the full `PINETS_PARITY_RESULT.json`
      (signal_agreement_pct, bars_compared, ema/atr diffs, verdict) as a structured block in the
      detail page — primarily for an AI reviewer to verify, plus a link to the file path.

**T2 — Backfill YouTube source_url**: many candidates have `source_url = UNKNOWN_URL` (e.g. ADA,
   LTC origins). When the user provides URLs, add them to the QuantLens registry CSV
   (`06_QUANTLENS_LAB/_registry/quantlens_candidate_registry.csv`) — that flows into the pipeline
   automatically via the registry reader. Until then the detail page shows "Video linki kayıtlı değil".

**T3 — Fix backtest reader FAIL**: `backtest_reader.py` marks `MEGA_walk_forward_results` and
   `RIGOROUS_walk_forward_results` as FAIL because those JSONs have a different shape
   (a top-level object with `results[]` of 17-symbol × 5-timeframe records, not the legacy per-run
   schema). Teach the reader to recognize this shape (status COMPLETED, summarize symbols/timeframes)
   instead of FAIL. Do not fabricate metrics; just parse what exists.

**T4 — Add `tests/test_pipeline_reader.py`**: it is the only reader without a unit test. Test the
   stage derivation (done/pending/na), the salvage branch, next_action, and the PineTS-PASS path
   using small fixtures. Keep total tests green.

**T5 — Optional polish**: rename the dashboard header from "MVP-8 LiveOps Dry-run Sandbox" to
   "Strategy Pipeline" by updating `03_STATUS/CURRENT_STATUS.json` `phase`. Also relabel the "Tasks"
   tab intent (those are MCC's own build tasks, which confuses users) — e.g. heading "MCC Build Tasks".

## 4. Working agreement

- Keep changes read-only and dependency-free. Run `pytest` after every change.
- Update `CHANGELOG.md`, `CURRENT_STATUS.md`, `PROJECT_HANDOFF.md` when you finish a task.
- Commit in small, described steps (the repo convention is direct commits on `main` with
  `feat(mcc): ...` / `fix(mcc): ...` messages). MCC files are tracked; QuantLens lab is not.
- If a source file (transcript / TradingView export / URL) is missing, surface it as
  `WAITING_FOR_USER` rather than inventing data.
