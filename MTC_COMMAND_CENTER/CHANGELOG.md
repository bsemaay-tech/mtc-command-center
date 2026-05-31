# Changelog

## Unreleased

### Added - 2026-05-31 (Codex) - Claude continuation P1-P5

- `11_TRIAGE/ingest.py` now detects large embedded transcript bodies without an explicit `## Transcript`
  heading, writes transcript markdowns idempotently, and backfills source-map transcript paths for existing URLs.
- `audit_reader.py` now merges source-map records for the same candidate/group so recovered transcript paths
  fill incomplete source records without discarding higher-quality primary source metadata.
- Added `11_TRIAGE/url_hints_dossier_2026-05-31.md` with local title/transcript match leads for 11 `NO_URL`
  candidates.
- Added `11_TRIAGE/block_bootstrap_christian_or.py` and generated
  `11_TRIAGE/christian_or_validation_2026-05-31.md`: Christian Open Range 5% Stop has 4/6 block-bootstrap
  passes and 1/6 block+rolling pass; recommendation is `PROMOTE_TO_PINETS_PARITY_REVIEW` with rolling-origin caveats.
- `pipeline_reader.py` now scans promoted `producer_spec.json` packets and injects promoted-stage rows when no
  canonical registry strategy exists.
- `backtest_reader.py` now exposes MEGA matrix `symbols_tested`, `timeframes_tested`, and aggregate
  `trade_count`; live MEGA snapshot shows 17 symbols, 5 timeframes, and 325318 trades.
- Dashboard/API verification on a fresh server rendered 196 pipeline rows and 196 audit rows with healthy status
  and no browser console errors. Test suite: `30 passed`.

### Added - 2026-05-31 (Claude) - Continuity handoff

- `PROJECT_HANDOFF.md` updated for the triage workflow + overnight v2 sweep + DSR-relaxed validation
  + MCC end-to-end audit. Pending Work re-prioritized with 6 explicit items.
- `11_TRIAGE/OVERNIGHT_LESSONS_2026-05-31.md` documents the 12 critical lessons from the session
  (estimation errors, background process management, sandbox + multiprocessing gotchas, DSR
  threshold reality, cross-symbol generalization > single-cell strength, etc.).
- `01_PROMPTS/CLAUDE_CONTINUATION_2026-05-31.md` is the token-efficient continuation prompt for
  the next session — pointers > prose, with first-commands, priority-ordered pending work,
  critical gotchas, and full paths cheatsheet.

### Added - 2026-05-30/31 (Claude) - Triage + overnight backtest + DSR analysis

- `11_TRIAGE/` workspace: worklist xlsx generator, per-strategy `stg*.md` notes (172 candidates),
  ingest pipeline (URL+transcript backflow), heuristic analyzer, sample/deep-sample tools.
- 19 candidate promotions from manual reclassification of 18 REVIEW_HUMAN rows + Andrew Connell
  deep read. Specs + first-pass prototypes materialized under QuantLens lab.
- Overnight v2 backtest sweep: 19 iterations × ~457K case-folds = **~6M case-folds** total via
  `overnight_v2_runner.py` (monkey-patches `mega_walk_forward.py`) wrapped in
  `overnight_loop.sh` (7.5h deadline).
- DSR-relaxed analysis (DSR p ≥ 0.50 OR BH-FDR survivor) yields 8 robust survivors. Strongest
  finding: `QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M` survives in **6 cells** across OP/ETH/NEAR/TRX/BTC.
- MCC end-to-end audit scored 8.5/10. Refactor candidates documented; no acute bugs.

### Added - 2026-05-30 (Codex) - Read-only candidate audit

- Added a new `candidate_audit` read-model layer over all 177 pipeline rows.
- The audit classifies each row with source quality, deterministic-rule presence, source/transcript coverage,
  backtest eligibility, blocked reason, duplicate/canonical mapping, and recommended next pipeline step.
- Audit detail rows include human-readable explanations for the above fields.
- Audit source loading scans both QuantLens JSONL ledgers and `quantlens_source_map.csv`, and checks transcript
  markdowns for recovered YouTube URLs when the direct record is incomplete.
- The dashboard now includes a dedicated **Audit** tab with summary cards, filters, and a row table.
- Added `python -m mcc_readonly audit` and expanded test coverage.

### Fixed - 2026-05-30 (Codex) - Expanded QuantLens discovery coverage

- Pipeline no longer stops at the canonical registry CSV. It now also reads broader QuantLens
  discovery ledgers from `research/**/FINAL_LLM_KNOWLEDGE_BASE.jsonl`,
  `research/**/AUDITED_CANDIDATE_EXTRACTION.jsonl`, and `12_LLM_WIKI/**/quantlens_*.jsonl`.
- The live pipeline now shows 177 rows: 15 canonical/promoted rows plus 162 extra discovered
  QuantLens candidates/modules, deduped by `candidate_id`.
- Blocked/rejected/wiki-only discoveries are included as parked rows instead of being silently hidden.

### Added - 2026-05-30 (Codex) - Direction research and dashboard polish

- Pipeline details now include `directional_research` for every row. Promoted strategies read
  `producer_spec.json` to show the locked current direction, long rule, short-rule status, and a
  separate short-side research action without implying that long-only metrics apply to shorts.
- Web detail view renders a Long / short research block for all strategies.
- Dashboard header phase is now `Strategy Pipeline`; the Tasks tab/heading is relabeled as MCC
  build tasks to avoid confusing MCC work items with trading tasks.

### Added - 2026-05-30 (Codex) - Pipeline detail enrichment

- `pipeline_reader`: enriched promoted strategy rows with `paper_trade_detail`, `equity_curve`,
  and `pinets_parity_proof`. The reader now surfaces paper-trade plan metadata, waits cleanly for
  future forward-result files, builds a lightweight equity curve from `*_trades.csv`, and exposes
  the machine-readable PineTS parity result plus source path.
- Web Pipeline detail view: replaced the placeholder with an inline SVG equity sparkline,
  a paper-trade plan/results section, and a structured PineTS parity-proof block.
- Added `tests/test_pipeline_reader.py` for promoted PASS, paper-plan, equity, next-action, and
  salvage-only paths.

### Fixed - 2026-05-30 (Codex) - Backtest matrix shape

- `backtest_reader`: recognized MEGA/RIGOROUS matrix walk-forward JSONs (`config` + `results[]`)
  as completed aggregate runs instead of treating per-row classifications as run-level failure.
  It now reports evaluations, strategy/symbol/timeframe counts, classification counts, and parsed
  survivor flags without inventing metrics.
- Updated backtest reader tests for the matrix JSON shape.

### Added — 2026-05-30 (Claude) — Strategy Pipeline view

- `08_DASHBOARD_APP/apps/api/mcc_readonly/pipeline_reader.py`: new read-only aggregator
  `build_candidate_pipeline()` that joins registry + pine-builder + liveops + parity + backtest
  by candidate/strategy id into a candidate-centric **6-stage pipeline** (Discovered, Backtested,
  Promoted, Pre-Parity, Paper-Trade, Integrated). Each row carries per-stage status+metric,
  a single "next action", plain-language Turkish descriptions, the source YouTube URL, historical
  metrics, and the PineTS parity result (if present).
- Wired `candidate_pipeline` into `read_model.build_dashboard_snapshot`.
- Web: new **Pipeline** tab (now the default first tab) with a board (`renderPipeline`) and a
  clickable per-strategy **detail view** (`openStrategyDetail`) showing description, metrics,
  stage list, next action, and an embedded YouTube source video. Added stage-status CSS.

### Notes

- Still fully read-only; no execution, no writes, no MTC_v2 core changes.
- `python -m pytest tests/` -> 25 passed (no regressions).

## MVP-0 (foundation, earlier)

- Created foundation folder structure for MTC Command Center.
- Added starter documentation, prompt templates, task queue, status files, registries, schemas, adapter notes, and dashboard planning notes.
- Added read-only and dry-run safety language for MVP-0.

## MVP-1 .. MVP-8 (Codex)

- Read-only API core, health diagnostics, read-model adapters, dashboard shell, report viewer,
  task lifecycle diagnostics, controlled task writer gate, and domain readers
  (parity, backtest, QuantLens registry, Pine builder, optimization, LiveOps dry-run).
- No live trading; AI-generated Pine kept as standalone review files; MTC_v2 core untouched.
