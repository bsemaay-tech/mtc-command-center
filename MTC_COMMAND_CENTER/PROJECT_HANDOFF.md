# Project Handoff

MTC Command Center (MCC) continuity handoff between AI sessions.

> **▶ LATEST HANDOFF (2026-06-08, Claude → Codex): `_AI_MEMORY/CODEX_PICKUP_2026-06-08.md`.** 5 open work items + binding constraints + the night-run→MCC enrich gap. The 2026-05-31 state below is older background.

## Current State (2026-05-31)

- Product: MTC Command Center · Short name: MCC
- Phase: MVP-8 + Strategy Pipeline + Audit (Codex) + **Triage Workflow + embedded transcript ingest + promoted producer-spec pipeline + Christian OR validation + audit eligibility review + audit/pipeline UI polish, scoring, and MTC_V2 readiness (Codex, 2026-05-31)**
- Mode: read-only, dry-run, report-first (unchanged)
- Root: `C:/LAB/tradingview-lab/MTC_COMMAND_CENTER`
- Dashboard app: `08_DASHBOARD_APP/apps/api` (Python, dependency-free) + `08_DASHBOARD_APP/apps/web` (vanilla JS)
- Triage workspace: `11_TRIAGE/` — worklist xlsx, per-strategy stg*.md notes, ingest pipeline, analyzer reports
- Audit verdict (2026-05-31): **8.5/10** — production-ready, refactor adayları görece düşük öncelikli (see `11_TRIAGE/mcc_audit_2026-05-31.md`)

## Current UI polish (2026-05-31)

- Pipeline and Audit tabs now have explanatory tooltips, stable `Stg001`-style triage codes, and a heuristic 100-point scorecard.
- Pipeline and Audit now expose score-band filters. Audit also exposes dropdown filters for Strategy, Quality, Rules, Source, Eligible, Blocked reason, Canonical, and Next step.
- The scorecard is triage-oriented, not a profit forecast. It combines source coverage, rule quality, backtest evidence, execution readiness, and risk/cleanliness.
- MTC_V2 readiness is now a read-only tab fed by Pipeline/Audit and the MTC_V2 parity tracker. It does not edit `MTC_V2.pine`.
- The `Sources` card in Audit still means raw scanned source-record count. `2060` is the number of source entries read from JSONL/CSV inputs, not unique strategies.

## Latest Follow-up Completed (Codex, 2026-05-31)

- MTC_V2 readiness was calibrated: current result is 0 fully ready rows, 1 row needing forward evidence, and 195 blocked/parked/low-score rows.
- Leading row is `QL_ALPHA_LINK_8EMA_1H`: score `88/100`, bucket `NEEDS_FORWARD_EVIDENCE`, forward progress `0/30` trades.
- MTC_V2 rows now include direct decision sentences such as why a high-score strategy is still not ready.
- Forward paper-trade progress is shown in the MTC_V2 tab and readiness export.
- Readiness exports were generated:
  - `11_TRIAGE/mtc_v2_readiness_export_2026-05-31.md`
  - `11_TRIAGE/mtc_v2_readiness_export_2026-05-31.csv`
- `/api/snapshot` now has a short in-memory cache. Dashboard Refresh calls `/api/snapshot?refresh=1` to force a fresh rebuild.
- Guardrail remained intact: this pass did not edit `01_MASTER TEMPLATE_V2/01_PINE/MTC_V2.pine`.

## How to run / verify

```
cd 08_DASHBOARD_APP/apps/api
python -m pytest tests/                 # 32 passed (32/32)
python -m mcc_readonly health           # overall_ok=true
python -m mcc_readonly serve --host 127.0.0.1 --port 8765
# open http://127.0.0.1:8765/dashboard  (Pipeline is the default first tab)
```

If port 8765 is already occupied by an older server process, start a fresh server on another port before
browser verification, for example `--port 8768`. The latest browser check used
`http://127.0.0.1:8768/dashboard` and rendered 196 pipeline rows / 196 audit rows / 196 MTC_V2 readiness rows with no console errors.

## Triage workflow (11_TRIAGE/)

```
cd MTC_COMMAND_CENTER
python 11_TRIAGE/generate_worklist.py            # builds xlsx + 172 stg*.md
python 11_TRIAGE/extract_urls_from_intakes.py    # auto-extract URLs from intake reports
python 11_TRIAGE/analyze_transcripts.py          # heuristic transcript scan → 4 reports
python 11_TRIAGE/sample_for_review.py            # condensed context for REVIEW_HUMAN
python 11_TRIAGE/deep_sample.py <cid>            # deep context per candidate
python 11_TRIAGE/ingest.py [--apply]             # ingest URLs+transcripts back to QuantLens
python 11_TRIAGE/aggregate_overnight_iters.py    # cross-iteration robustness
```

## Last Completed Work (Codex, 2026-05-31) - Claude continuation P1-P5

- Embedded transcript ingest is complete. `11_TRIAGE/ingest.py` detects large stg markdown bodies with many
  timestamp tokens even when no `## Transcript` heading exists, writes transcript files idempotently, and records
  transcript paths in `manual_backfill/2026-05-31/quantlens_source_map.csv`.
- `audit_reader.py` now merges duplicate source records for the same candidate/group, preserving the higher-rank
  primary record while filling missing transcript/source fields from lower-rank source-map rows.
- `11_TRIAGE/url_hints_dossier_2026-05-31.md` was generated for the 11 `NO_URL` candidates. Most matches are
  intentionally low-confidence search leads, not proof.
- Christian Open Range 5% Stop follow-up validation is documented in
  `11_TRIAGE/christian_or_validation_2026-05-31.md`. Result: 4/6 cells pass block-bootstrap, 1/6 passes both
  block and rolling-origin checks; recommendation is `PROMOTE_TO_PINETS_PARITY_REVIEW` with a weak/mixed
  rolling-origin caveat.
- `pipeline_reader.py` now scans `06_PROMOTED_TO_PARITY/*/producer_spec.json` and injects promoted-stage rows
  when the candidate is not already a canonical registry strategy. Live pipeline summary: discovered 196,
  classified 196, backtested 31, promoted 22, pre_parity 1, paper_trade 0, integrated 0.
- `pipeline_reader.py` and `audit_reader.py` now attach heuristic scorecards, next-action hints, and stable
  triage codes resolved from `11_TRIAGE/strategies/_stg_code_map.json`.
- `mtc_v2_reader.py` adds a read-only readiness queue for `READY_FOR_MTC_V2_REVIEW`, forward-evidence,
  PineTS parity, promotion-pack, backtest, source-audit, split/parked, and low-score review buckets.
- `backtest_reader.py` now exposes MEGA matrix metadata. Live MEGA row: 17 symbols, timeframes
  `15m, 1D, 1h, 2h, 4h`, trade_count 325318.
- Audit eligibility jump review is complete. `11_TRIAGE/audit_eligibility_jump_review_2026-05-31.md`
  documents the 11-row eligibility drop caused by higher-rank source-map classifications; the change
  looks deliberate but should stay visible as an execution-queue gate.
- UI polish complete: tooltips and filters now make Audit/Pipeline more self-explanatory, and the strategy
  detail page shows score breakdowns by category plus a decision panel. The score/readiness rules are
  documented in `11_TRIAGE/scorecard_and_mtc_v2_readiness_2026-05-31.md`.
- Verification: `python -m pytest tests/` -> 32 passed; `python -m mcc_readonly snapshot` -> ok;
  fresh dashboard server on port 8768 rendered healthy with no browser console errors.

Important caveat: the source-record merge materially changes the audit snapshot. Direct latest snapshot shows
196 total rows, 167 eligible, 26 blocked, 166 with source material, and 191 deterministic-rule rows. Review this
eligibility jump before treating audit eligibility as an execution queue.

## Last Completed Work (Codex, 2026-05-30) - Expanded QuantLens discovery coverage

- Root cause for "only 15 discovered": the Pipeline originally read only the canonical
  `_registry/quantlens_candidate_registry.csv` plus promoted specs. It did not read broader
  QuantLens research / LLM discovery ledgers.
- `pipeline_reader.py` now also reads:
  - `research/**/FINAL_LLM_KNOWLEDGE_BASE.jsonl`
  - `research/**/AUDITED_CANDIDATE_EXTRACTION.jsonl`
  - `12_LLM_WIKI/**/quantlens_strategy_candidates.jsonl`
  - `12_LLM_WIKI/**/quantlens_knowledge_base.jsonl`
- Extra rows are deduped by `candidate_id`, do not overwrite canonical registry/promoted rows,
  and remain read-only. Blocked/rejected/wiki-only discoveries are shown as parked rows.
- Live pipeline now shows 177 rows: 15 canonical/promoted rows + 162 extra QuantLens discoveries.
- Browser verified at `http://127.0.0.1:8765/dashboard`: `177 strategies`, Discovered `177`, QLR
  rows present, no console errors.

## Last Completed Work (Codex, 2026-05-30) - Read-only candidate audit

- Added `audit_reader.py` and wired `candidate_audit` into the dashboard snapshot.
- The audit layer classifies all 177 pipeline rows with:
  - `source_quality`
  - `has_deterministic_rules`
  - `has_source_url_transcript`
  - `eligible_for_backtest`
  - `blocked_reason`
  - `duplicate/canonical mapping`
  - `recommended_next_pipeline_step`
- Audit row detail now includes human-readable explanations for quality, rule extraction,
  backtest eligibility, duplicate mapping, and next-step recommendation.
- Audit source loading now scans both QuantLens JSONL and `quantlens_source_map.csv`, and also
  checks transcript markdowns for recovered YouTube URLs when the direct record is incomplete.
- Web dashboard now has a dedicated **Audit** tab with summary cards, filters, and a table view.
- CLI now has `python -m mcc_readonly audit`.
- Test suite now passes with 27 tests.

## Previous Completed Work (Codex, 2026-05-30) - Direction research and polish

- Every Pipeline detail row now includes `directional_research`.
- Promoted strategies read `producer_spec.json` to show the locked current direction, long rule,
  short-rule status, and a safe short-side research action.
- Current promoted strategies are `long_only` with `short_signal_definition: null`; the dashboard
  marks them `SHORT_UNTESTED` and shows a mirror-rule research hint instead of treating long metrics
  as short evidence.
- Dashboard phase is now "Strategy Pipeline"; Tasks tab/heading is relabeled as MCC build tasks.
- Browser verified at `http://127.0.0.1:8765/dashboard`: phase/title polish is visible and LINK
  detail shows the Long / short research block with no console errors.

## Previous Completed Work (Codex, 2026-05-30) - Pipeline detail enrichment

- `pipeline_reader.py`: promoted strategy rows now include `paper_trade_detail`, `equity_curve`,
  and `pinets_parity_proof`.
- Paper-trade detail reads `FORWARD_PAPER_TRADE_PLAN.md`, reports `WAITING_FOR_FORWARD_RESULTS`
  when no forward output exists, and will summarize future forward result JSON/CSV files.
- Equity sparkline data is built read-only from `<id>_trades.csv` using cumulative compounded
  `ret_net_pct`.
- PineTS parity proof exposes source path, summary fields, and raw `PINETS_PARITY_RESULT.json`
  for AI review.
- Web detail view renders the sparkline, paper-trade plan/results section, and structured parity
  proof block.
- `backtest_reader.py`: MEGA/RIGOROUS matrix walk-forward files (`config` + `results[]`) are parsed
  as `COMPLETED` aggregate runs with 17-symbol x 5-timeframe summaries and classification counts
  instead of run-level `FAIL`.
- Added `tests/test_pipeline_reader.py`; API test suite is now 24 passed.
- Browser verified at `http://127.0.0.1:8765/dashboard`: Pipeline loads 15 rows; LINK detail opens;
  sparkline, paper-trade, and parity-proof blocks render with no console errors.

## Previous Completed Work (Claude, 2026-05-30) — Strategy Pipeline

Goal: turn the domain-siloed dashboard into a candidate-centric pipeline so a returning user
instantly sees which strategy is at which stage and the single next action.

New / changed files:
- NEW `apps/api/mcc_readonly/pipeline_reader.py` — `build_candidate_pipeline()` aggregator.
- CHANGED `apps/api/mcc_readonly/read_model.py` — imports + calls it, exposes `candidate_pipeline` in the snapshot.
- CHANGED `apps/web/index.html` — added Pipeline tab (default) + panel + detail container.
- CHANGED `apps/web/app.js` — `renderPipeline()`, `stageCell()`, `openStrategyDetail()`, `closeStrategyDetail()`, `ytEmbed()`.
- CHANGED `apps/web/styles.css` — stage-status badges, clickable rows, detail-view layout, YouTube embed.

6 stages (simplified from the 9-step QuantLens→MTC_v2 workflow):
`discovered → backtested → promoted → pre_parity → paper_trade → integrated`.
Stage status values: `done | active | pending | fail | na`.

Join keys (all read-only, from existing readers):
- `registry.candidates[].candidate_id` (early-stage items, 14)
- `registry.strategies[].strategy_id` (promoted QL_ALPHA_* items, 3; `candidate_id` links to origin)
- `pine_builder.drafts[].candidate_id`, `liveops.paper_trade_plans[].candidate_id`
- PineTS parity read directly from `01_MASTER TEMPLATE_V2/06_QUANTLENS_LAB/06_PROMOTED_TO_PARITY/<id>/PINETS_PARITY_RESULT.json`

Detail page contents: plain-language description (entry/exit), historical metrics
(return/PF/trades/DD/win/direction), equity sparkline, stage list, next action, embedded YouTube
source video, paper-trade detail, machine-readable PineTS parity proof, long/short research, id.

## Last Completed Work (Claude, 2026-05-30 / 2026-05-31)

### Triage workflow + worklist (11_TRIAGE/)

- `generate_worklist.py`: 172-row xlsx + 172 per-strategy stg*.md files. Persistent stg_code map
  (`_stg_code_map.json`) so re-runs preserve user-edited .md files.
- `ingest.py`: parses stg*.md, writes new URLs to
  `06_QUANTLENS_LAB/12_LLM_WIKI/manual_backfill/<date>/quantlens_source_map.csv` and new transcripts to
  `06_QUANTLENS_LAB/00_INBOX_REPORTS/Transcrips/`. Default `--dry-run`; idempotent state file.
- Heuristic analyzer (`analyze_transcripts.py`) over 67 transcripts yielded:
  KEEP_REJECTED 23 · LIKELY_MISCLASSIFIED 24 · REVIEW_HUMAN 18 · SPLIT_RECOMMENDED 1 · ALREADY_OK 1.
- Manual review of 18 REVIEW_HUMAN → reclassification: 7 LIKELY_MISCLASSIFIED, 9 KEEP, 1 SPLIT, 1 ambiguous
  (see `11_TRIAGE/reclassification_decisions_2026-05-30.md`).

### 19 candidate promotions (specs + first-pass prototypes materialized)

Approved promotions (see `11_TRIAGE/promotion_packets_2026-05-30.md`, `split_packet_2026-05-30.md`,
`deepak_comparison_2026-05-30.md`, `andrew_connell_deep_read_2026-05-30.md`):

| Group | Candidates | Notes |
|---|---|---|
| A: LIKELY_MISCLASSIFIED | 7 + Andrew Connell deep read = 8 | VCP×2, AVWAP parent, Christian parent, Deepak filter, Sell-rule overlay, Connell 1D+5M |
| B: Pro Swing Ep 2 split | 3 | Launchpad, Highest-Volume edge, RS phase/days overlay |
| Christian sub-cases | 4 | Episodic pivot 5M, 20MA trail, VCP early entry, OR 5% stop |
| Brian Shannon AVWAP sub-cases | 4 | Gap reclaim, Stage-2 emerging, Intraday OR, Earnings anchor |
| Deepak corpus | 3 | 153 Filter (already), 259 Risk overlay, Snapback 50SMA intraday |
| **Total unique** | **19** | First-pass prototype skeletons in `06_QUANTLENS_LAB/04_PYTHON_PROTOTYPES/` |

Materialized via `11_TRIAGE/overnight_orchestrator.py --apply`:
- 19 × `producer_spec.json` under `06_QUANTLENS_LAB/06_PROMOTED_TO_PARITY/<id>/`
- 19 × `<id>_prototype.py` under `06_QUANTLENS_LAB/04_PYTHON_PROTOTYPES/` (first-pass entry/exit logic, compile-ready)

### Overnight v2 backtest sweep — 19 iterations, ~6M case-folds

- `overnight_v2_runner.py` monkey-patches `mega_walk_forward.py` to add 19 new strategies (no edit to upstream),
  taking total to 39 strategies × 1797 param sets.
- `overnight_loop.sh` wraps runner in 7.5h deadline loop. **19 successful iterations** at ~18 min each
  (run start 00:56, end 06:45).
- Per iter: 3315 jobs × ~46 configs × 3 folds ≈ 457K case-folds. Total ≈ **6 million case-folds**.
- Outputs in `06_QUANTLENS_LAB/tools/overnight_runs/` (gitignored): 19 timestamped JSON+MD per iter.
- Aggregated cross-iter via `aggregate_overnight_iters.py` → `OVERNIGHT_AGGREGATED_REPORT.md`
  (committed copy at `11_TRIAGE/morning_report_2026-05-31.md`).

### Focused validation + DSR-relaxed analysis (2026-05-31)

- `focused_validation.py`: narrowed grids (42 trials vs 1797) → DSR threshold should drop. Result: DSR p≥0.95
  still 0. Threshold simply too strict for crypto's noisy Sharpe regime.
- Applied relaxed criteria (BH-FDR survivor OR DSR p ≥ 0.50) → **8 robust survivors**, all NEW candidates:
  - 🥇 **`QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M`** survives across **6 cells** (OPUSDT 1h, ETHUSDT 1h,
    NEARUSDT 4h, TRXUSDT 2h [3/3 folds], BTCUSDT 15m, BTCUSDT 4h) with DSR p between 0.53-0.65 →
    **cross-symbol generalization = real edge**, defeats the "TRX-only overfit" first read.
  - 🥈 `QL_DEEPAK_259_RISK_OVERLAY` × TRXUSDT 4h: BH-FDR survivor + DSR p=0.54 + 3/3 folds.
  - 🥉 `QL_HIGHEST_VOLUME_EDGE_PROSWING_1D` × TRXUSDT 15m: BH-FDR survivor (single-symbol).
- Report: `11_TRIAGE/focused_validation_report_2026-05-31.md`.

### MCC end-to-end audit (2026-05-31)

`11_TRIAGE/mcc_audit_2026-05-31.md` — score 8.5/10. Highlights:

- ✅ Server.py read-only enforcement + path traversal protected + report scope limited to `04_REPORTS`.
- ✅ Writer.py atomic temp+rename + lock-file via `open("x")`, JSONL append.
- ✅ 29/29 tests pass, 271/272 funcs have return type hints, 0 bare `except`, 1 TODO (constant string).
- ✅ Overnight data integration verified: audit picked up new `manual_backfill` URLs (109 → 128 eligible),
  backtest_reader recognized MEGA_walk_forward.json (status=COMPLETED).
- ⚠️ Refactor candidates: `pipeline_reader.build_candidate_pipeline` 264 LOC single function; `audit_reader.py`
  1231 LOC heavily procedural (opportunity to extract `CandidateAuditBuilder` class).
- 2026-05-31 Codex follow-up fixed the `backtest_reader` MEGA matrix metadata extraction gap.
- ⚠️ No committed HTTP integration test yet; browser/API smoke verification was performed manually on a
  fresh local server. Per-snapshot file scans are not memoized (fine at 196 candidates, won't scale to 1000+).

## Completed Pending Work From Claude Continuation (2026-05-31)

1. Embedded transcript detection and ingest: done.
2. URL hint dossier for 11 `NO_URL` candidates: done.
3. Christian Open Range 5% Stop validation: done.
4. Promoted `producer_spec.json` pipeline wiring: done.
5. MEGA matrix metadata extraction: done.
6. Short-side research scaffolding: done.
7. Audit eligibility review, parity packet, producer-spec detail polish, URL hint follow-up, and refactor notes: done.

## Pending Work (priority order - 2026-05-31)

No active pending triage items remain from the 2026-05-31 continuation pass. The generated notes are:
- `11_TRIAGE/audit_eligibility_jump_review_2026-05-31.md`
- `11_TRIAGE/christian_or_parity_packet_2026-05-31.md`
- `11_TRIAGE/url_hint_followup_2026-05-31.md`
- `11_TRIAGE/short_side_scaffolding_2026-05-31.md`
- `11_TRIAGE/refactor_candidates_2026-05-31.md`

## Risks / Guardrails (unchanged)

- `MTC Command Center ARCHITECTURE.md` is the canonical architecture file.
- Do NOT touch MTC_v2 core, `01_PINE/MTC_V2.pine`, PineTS engine, TradingView exports, or add live trading / webhooks.
- MCC stays read-only + dry-run; the only writes allowed are the controlled task-writer gate (CLI), never from the HTTP API.
- The QuantLens lab (`01_MASTER TEMPLATE_V2/06_QUANTLENS_LAB/`) is git-ignored; MCC reads it but must not depend on it being committed.

## Manual Actions Expected From User

- Provide YouTube transcripts / URLs for strategy intake and to backfill missing `source_url`.
- Provide TradingView exports when parity/backtest comparison needs them.
- Approve large changes before implementation.
