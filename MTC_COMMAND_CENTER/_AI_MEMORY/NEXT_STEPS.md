# NEXT_STEPS

## Confirmation Run Follow-up (2026-06-04)

### NIGHT-CONFIRM-2026-06-04 | DONE | Quiet pre-registered confirmation run + validation tail [AI: Codex GPT-5]
- Resumed Claude's interrupted Option B path and launched the quiet confirmation run with 4 workers.
- Output: `03_QUANTLENS/05_BACKTEST_RESULTS/confirm_2026-06-04/MORNING_REPORT_confirm_2026-06-04.md`.
- Result: 306 cells / ~3,672 configs / 16 PASS / 1 BH-FDR survivor / 0 DSR-robust / 0 final robust.
- A18 fixed in output: down-market alpha count/table now matches canonical `alpha_summary.json` (`down_market_alpha=6`).
- Validation tail done: CPCV, PBO, 16 evaluation artifacts, 16 Gate-2 scorecards. Scorecards: all INCOMPLETE, 0 pass.
- Morning watchdog active until 2026-06-05 07:30 local: `03_QUANTLENS/tools/overnight_runs/_heartbeat_confirm_morning_watchdog.json`.
- No Pine/MTC/parity/live-trading action is authorized by these results.

### NIGHT-CONFIRM-2026-06-05-REVIEW | DONE 2026-06-05 (Claude) | Morning review of confirmation artifacts [AI: Claude|Baris]
- Reviewed report + CPCV/PBO + 16 scorecards. A18 verified (down_market_alpha=6 == ALPHA_DONE).
- DSR rose wide→narrow (0.0→0.34-0.38 best) but none ≥0.50; Gate-2 16/16 INCOMPLETE (metric gap, not FAIL).
- **Decision:** no promotion. Forward-paper observation OPTIONAL for 2 least-weak cells: 8EMA LINK 1h, Donchian ETH 2h. No Pine/MTC/parity/live action.
- Closure done: lessons C4-C6, runbook A19 + CHANGELOG, INDEX already had 06-05 line.

### NIGHT-FOLLOWUP-HEAVY-TIER | OPEN | Compute-filling heavy-validation tier for confirmation nights [AI: Claude|Barış]
- **Problem (A19):** deterministic narrow confirmation finishes in minutes; machine sat idle-awake on watchdog the rest of the night. Tekrar = sıfır bilgi (seed=md5, mega:731).
- **Build:** a heavy-validation stage sized to wall-clock — 50k-resample bootstrap, multi-seed DSR/boot-p stability distribution (deliberately vary seed), CPCV across ALL pass cells, PBO with more combinations, ±2-step pre-registered grid + 4h/1D TFs. Wire into the confirmation runner post-pipeline with a deadline cap; if it finishes early, RELEASE the machine (no pointless keep-awake).

## SP-004 rubric sign-off (2026-06-04)

### SP-004-SIGNOFF | DONE | D1-D6 owner decisions resolved [AI: Claude | Barış]
- Barış signed D1-D6 (DECISIONS D007). Rubric `12_STRATEGY_EVALUATION_RUBRIC.md` updated: D1 Gate 1B → /100 PASS≥75 (criteria rescaled ×2), D3 parity → advisory (PARITY_WARNING, non-blocking), D2/D4/D6 accepted, D5 deferred to Phase 1.5. **Unblocks Phase 2 scoring lock.**

### SP-004-PHASE1-EVALARTIFACT | DONE | evaluation_artifact writer [AI: DeepSeek/Claude]
- Done (2026-06-04 Batch G/H): `03_QUANTLENS/tools/build_evaluation_artifact.py`. CLI `--mega --cpcv --pbo --out-dir`; pure `build_artifact()`; status-enveloped metrics (OK only when computed, else NOT_COMPUTED/N_A, never auto-zero); hard_flags/flags bare per schema; version 'v1'. Claude-audited on real 5MB MEGA: 149 artifacts, 0 schema errors (Draft2020-12+$ref), 0 fabricated numbers.
- Known limits (intentional): per-fold arrays dropped from metrics (scalars only); repaint_status=null (no repaint stage), parity_status='N_A', has_benchmark=false — fill when those stages exist.

### SP-004-PHASE2-SCORINGREADER | DONE | gate2 scoring reader [AI: DeepSeek/Claude]
- Done (2026-06-04 Batch I/J): `03_QUANTLENS/tools/score_gate2.py` (`score_gate2(artifact)->dict`, CLI `--in-dir --out-dir`). 25 criteria /100 per rubric §5.1-5.7; status-gated (non-OK metric → not scored → gate INCOMPLETE, never auto-zero); REJECT_REPAINT→FAIL; PBO≥0.5→OVERFIT_SUSPECT advisory; parity advisory; pass=(OK and ≥75). Batch J reconciled Phase-1 writer to emit schema metric vocabulary. Claude-audited real 5MB: 149 artifacts 0 schema-err, 149 scorecards all INCOMPLETE (22-43, 0 pass, 0 fabricated).

### SP-004-PHASE3-GATESCORERS | DONE | Gate1/1B/3 + unified composer [AI: Grok/Claude]
- Done (2026-06-05, dispatched to Grok grok-4 via `ds_agent.py`, Claude-audited on real data; DeepSeek was 402 Insufficient Balance).
- New files under `03_QUANTLENS/tools/`: `score_gate1.py` (intake /100, 35 criteria, `intake.*` envelopes), `score_gate1b.py` (MTC feasibility /100 PASS≥75, `feasibility.*`, D1 verdict PASS/CONDITIONAL/FAIL), `score_gate3.py` (production-readiness /100, reads `production_readiness_artifact_v1` groups per D4, 37 criteria), `score_all_gates.py` (unified composer → one `scorecard_v2`, no top-level number; `gate_summary.promotable` honest = all four OK+pass).
- All mirror `score_gate2.py`: pure `score_gateX(artifact)->dict` + CLI `--in-dir --out-dir`; status-envelope (only OK scores, non-OK → `points_awarded=None` → gate INCOMPLETE, never auto-zero); `REJECT_REPAINT`→FAIL; parity advisory; utf-8 stdout.
- Claude audit (real 16 confirm-2026-06-04 eval artifacts + synthetic): py_compile PASS ×4; full-OK→100/OK/pass; empty→INCOMPLETE; gate1 MEDIUM-repaint→98; REJECT_REPAINT→FAIL; composer all-OK→promotable. **Real 16/16 = all gates INCOMPLETE, 0 pass, 0 promotable** — correct honest status (intake/feasibility/readiness artifacts not emitted yet). Inline fix: gate1b verdict PASS-under-REJECT_REPAINT → hard-fail override.
- Carry-forward: these gates stay INCOMPLETE until writer artifacts exist (intake/feasibility for Gate1/1B; `production_readiness_artifact_v1` for Gate3; Gate2 metric-enrichment below). Scorers ready to score the moment those are emitted. Nothing committed.

### SP-004-METRIC-ENRICHMENT | DONE + COMMITTED (88a79e0) | enrich builder + engine output [AI: Claude/DeepSeek | Barış approved 2026-06-05]
- Barış approved 2026-06-05 (touches MTC strategy OUTPUT, not signal/Pine/parity logic). Done via DeepSeek dispatch + Claude audit.
- **Builder (`build_evaluation_artifact.py`, Task A):** replaced the blanket-N_A block with honest per-metric derivation from data MEGA already emits — `return_pct_compound`, `recovery_factor`, `calendar_days` (from data_start/end), `multi_window_pass` (folds_positive==n_folds), `net_after_fees_pct` (cost already in net), `avg_trade_vs_cost` — plus forward-compatible passthrough for engine-emitted fields. **Integrity call (Claude): `sharpe`/`sortino` kept N_A** because MEGA's lockbox `sharpe` is a t-stat-like per-trade scaled value, NOT the annualized Sharpe the rubric scores — mapping it would inflate the gate. `param_stability_score`, `regime.*`, `long_short_ratio`, `net_after_slippage_pct` honestly N_A. Audit: rebuilt real 16 confirm artifacts, **0 schema errors** (Draft2020-12+$ref), values hand-verified; gate2 scores moved **22–43 → 42–60** (still INCOMPLETE, 0 pass, 0 fabricated — correct).
- **Engine (`mega_walk_forward.py`, Task B):** additive OUTPUT only — added `max_consecutive_losses`, `top_trade_concentration`, `equity_curve_health` to `SliceStats`/`simulate_slice` (computed from the existing per-trade `arr`/`eq`; `asdict` auto-propagates into `lockbox_oos`). No existing field/value/trade-logic changed (verified: diff additive, formulas hand-checked mcl=1/conc=0.3333/health=0.6, import-failure is pre-existing/environmental on HEAD too). Builder passthrough will surface these on the **next** MEGA run.
- **Still N_A until further work:** sharpe/sortino (need annualized definition or time-series equity), regime.* (no regime stage), benchmark.excess_alpha/beats_ema (needs B&H-on-same-window stage), worst_window_drawdown_pct, param_stability_score. Full Gate-2 PASS also needs a **fresh sweep** under the enriched engine (Barış OPS — not run here; existing artifacts built from old MEGA JSON so the 3 new engine metrics are still N_A in them).
- **NOT COMMITTED (deliberate):** `mega_walk_forward.py` carries ~245/-50 of pre-existing uncommitted Batch A–J engine work; `build_evaluation_artifact.py` is untracked Batch G/H/J. Per the standing "leave Batch edits for Barış" rule, my enrichment rides on top uncommitted — Barış decides when to commit the combined engine/builder state.

### SP-004-METRIC-ENRICHMENT-RUN | DONE | fresh sweep under enriched engine [AI: Claude, Barış go-ahead 2026-06-05]
- Ran 2026-06-05 (Claude): full MEGA sweep under enriched engine (commit 88a79e0). 1700 cells / 14m43s / 8 workers; 38 PASS+STRONG_PASS. Validation tail: CPCV (v2 patch) + PBO. Built 38 enriched artifacts + 38 Gate-2 scorecards.
- **Result (regeneration, NOT promotion):** new engine metrics (max_consecutive_losses/top_trade_concentration/equity_curve_health) + builder-derived (recovery/calendar_days/multi_window_pass/net_after_fees/avg_trade_vs_cost) + cpcv/pbo now OK 38/38. Gate-2 scores **22–43 → 39–64 (mean 51.8, top 63.6)**. Still all INCOMPLETE / 0 pass / 0 fabricated / 0 schema errors — sharpe/sortino/regime/benchmark honestly N_A.
- Output (on disk, untracked like other run dirs): `05_BACKTEST_RESULTS/enriched_metrics_2026-06-05/` (results json, cpcv, pbo, evaluation_artifacts, scorecards, ENRICHED_RUN_SUMMARY.md). No Pine/MTC/parity/live action authorized.
- **Remaining for full Gate-2 PASS (genuine future work, not fakeable):** annualized Sharpe/Sortino (needs time-series equity, not per-trade R), a regime-split stage, and a same-window Buy&Hold benchmark stage. These are the only blockers between INCOMPLETE and a scorable PASS.
- **Finding:** all 149 cells score INCOMPLETE because MEGA/CPCV/PBO don't produce: sharpe, sortino, recovery_factor, worst_window_drawdown_pct, max_consecutive_losses, calendar_days, regime_coverage_count, top_trade_concentration, long_short_ratio, param_stability_score, multi_window_pass, net_after_fees_pct, net_after_slippage_pct, avg_trade_vs_cost, equity_curve_health, return_pct_compound, benchmark.excess_alpha_pct/beats_ema, regime.* (and CPCV only ran on a few cells → cpcv_pass_ratio mostly N_A).
- To make Gate 2 fully scorable: enrich the backtest engine (mega_walk_forward) to emit these per-cell (OOS sharpe/sortino/recovery/regime split/benchmark), and run CPCV across all PASS cells. Backtest-side work — needs design + Barış. Until then INCOMPLETE is the correct honest status.

### SP-004-GATE2-BENCHMARK | DONE + COMMITTED (7175ff6) | same-window Buy&Hold benchmark [AI: DeepSeek/Codex GPT-5]
- Done 2026-06-05 via DeepSeek dispatch + Codex audit. `mega_walk_forward.py` now emits `summary.buy_hold_lockbox` for the exact lockbox window: buy at first lockbox open, hold to final lockbox close, with return, positive max drawdown, and finite return/DD ratio.
- Codex audit fixes applied: entry baseline included in the B&H equity curve so immediate drawdown is counted; helper returns JSON-native floats.
- `build_evaluation_artifact.py` now sets `benchmark.excess_alpha_pct` and `benchmark.beats_bh_risk_adjusted` to OK when real B&H inputs exist, and marks `completeness.has_benchmark` dynamically. `beats_ema_benchmark` remains N_A until a separate EMA benchmark stage exists.
- Validation PASS: py_compile, synthetic helper smoke, synthetic builder smoke, and real one-cell audit `QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL LINKUSDT 1h`. Real artifact benchmark OK (`excess_alpha_pct=97.989`, `beats_bh_risk_adjusted=true`), Gate2 score 56 but still INCOMPLETE due remaining N_A fields.
- Fresh sweep DONE 2026-06-05: `05_BACKTEST_RESULTS/bh_benchmark_2026-06-05_7175ff6/`. MEGA 1700 cells / 38 PASS+STRONG_PASS; CPCV+PBO+38 eval artifacts+38 Gate2+38 scorecard_v2 rebuilt. Audit: 38/38 artifacts B&H benchmark OK, `has_benchmark=true`, 0 schema errors. Gate2 scores 38.59-69.0 mean 52.1; still 38/38 INCOMPLETE, 0 pass, 0 promotable.
- Remaining blockers after B&H closure: annualized Sharpe/Sortino, worst-window drawdown, param stability, slippage, EMA benchmark, and regime split.

### SP-004-GATE2-WORST-WINDOW | DONE + COMMITTED (283d198) | worst-window drawdown metric [AI: DeepSeek/Codex GPT-5]
- Done 2026-06-05 via DeepSeek dispatch + Codex audit. `mega_walk_forward.py` now emits `summary.worst_window_drawdown_pct` as max absolute fold-test drawdown for the selected config; `build_evaluation_artifact.py` maps `metrics.worst_window_drawdown_pct` from that summary field first and does not fabricate it from lockbox max drawdown.
- Validation PASS: py_compile, diff-check, synthetic builder primary/fallback/missing checks, and real one-cell audit `QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL LINKUSDT 1h` emitted `worst_window_drawdown_pct=19.452`; artifact metric OK; Gate2 worst-window criterion scored 4/4; schema errors 0.
- Fresh sweep DONE 2026-06-05: `05_BACKTEST_RESULTS/worst_window_2026-06-05_283d198/`. MEGA 1700 cells / 38 PASS+STRONG_PASS; CPCV+PBO+38 eval artifacts+38 Gate2+38 scorecard_v2 rebuilt. Audit: 38/38 artifacts B&H benchmark OK and worst-window OK, 0 schema errors. Gate2 scores 42.59-73.0 mean 56.04; still 38/38 INCOMPLETE, 0 pass, 0 promotable.
- Remaining blockers after worst-window closure: annualized Sharpe/Sortino, param stability, slippage, EMA benchmark, and regime split.

### SP-004-GATE2-ANNUALIZED-RISK | DONE + COMMITTED (15e8d47) | annualized Sharpe/Sortino [AI: DeepSeek/Codex GPT-5]
- Done 2026-06-05 via DeepSeek investigation + implementation dispatch, Codex audited. MEGA now emits `lockbox_oos.annualized_sharpe` and `lockbox_oos.annualized_sortino` from a daily strategy equity curve; old MEGA `sharpe`/`sharpe_pt` are preserved and not reused for Gate2 annualized Sharpe.
- `build_evaluation_artifact.py` maps Gate2 `metrics.sharpe` and `metrics.sortino` only from the new annualized lockbox fields. Backward rebuild of pre-annualized 38 artifacts kept Sharpe/Sortino N_A 38/38.
- Validation PASS: py_compile, diff-check, real one-cell audit, existing lockbox fields unchanged, one-cell annualized_sharpe=1.307 and annualized_sortino=2.6959, Gate2 Sharpe 5/5 and Sortino 4/4, schema errors 0.
- Fresh sweep DONE 2026-06-05: `05_BACKTEST_RESULTS/annualized_risk_2026-06-05_15e8d47/`. MEGA 1700 cells / 38 PASS+STRONG_PASS; CPCV+PBO+38 eval artifacts+38 Gate2+38 scorecard_v2 rebuilt. Audit: 38/38 artifacts Sharpe/Sortino/B&H/worst-window OK, 0 schema errors. Gate2 scores 46.25-82.0 mean 61.88; still 38/38 INCOMPLETE, 0 pass, 0 promotable because param stability/slippage/EMA/regime remain N_A.
- Remaining blockers after annualized-risk closure: param stability, slippage, EMA benchmark, and regime split.

### SP-004-GATE2-SLIPPAGE | DONE + NEEDS FRESH SWEEP | post-hoc slippage stress [AI: DeepSeek/Codex GPT-5]
- Done 2026-06-05 via DeepSeek dispatch + Codex audit. MEGA now emits `lockbox_oos.net_after_slippage_pct` using `SLIPPAGE_BPS_PER_SIDE=2.0` (4 bps round trip) subtracted from each existing per-trade net return before compounding; existing `COST_BPS` and `net_return_pct` are unchanged.
- `build_evaluation_artifact.py` maps Gate2 `metrics.net_after_slippage_pct` only from the new lockbox field. Backward rebuild of pre-slippage 38 artifacts kept slippage N_A 38/38.
- Validation PASS: py_compile, diff-check, real one-cell audit, existing lockbox fields unchanged, one-cell net_return_pct=75.374 / net_after_slippage_pct=67.119, Gate2 slippage 2/2, schema errors 0.
- Carry-forward: run a fresh full sweep before dashboard scorecards show slippage globally. Remaining blockers after propagation: param stability, EMA benchmark, and regime split.

### SP-004-SCHEMA-PARITY | DONE | Move parity to advisory in schema [AI: DeepSeek/Claude]
- Done (2026-06-04 Batch F): `06_SCHEMAS/evaluation_artifact_v1.schema.json` — `parity_gate` removed from `hard_flags`; new advisory `flags.parity_status` ∈ {PASS, WARN, N_A, null}. Claude-audited: json.load VALID, Draft2020-12 check_schema VALID, parity_gate gone everywhere, completeness intact.
- **Reader carry-forward (Phase 2):** the future scoring reader must read `flags.parity_status` (NOT `hard_flags.parity_gate`) and treat WARN as non-blocking. Captured for the Phase-2 build.

## Local YouTube Transcript Collector (2026-06-04)

### YT-TRANSCRIPT-001 | DONE | Local transcript collector utility [AI: Codex GPT-5]
- Added isolated Python tool under `YT_TRANSCRIPT_COLLECTOR/`.
- Reads `urls.txt`, extracts YouTube video IDs, fetches transcripts with `youtube-transcript-api`, prefers `tr` then `en` then any available transcript, writes Markdown under `transcripts/`, and writes `reports/transcript_index.csv` plus `reports/failed_videos.csv`.
- Safety boundary: no YouTube login, no password request, no video/audio download, no browser automation, and no account actions.
- Validation: py_compile PASS, 2 offline URL extraction tests PASS from tool folder and repo root, CLI help PASS.
- Run update 2026-06-04: fetched `2NuvYsXMehw` successfully; output `YT_TRANSCRIPT_COLLECTOR/transcripts/2NuvYsXMehw.md`; metadata `Turkish (auto-generated) (tr)`. Added UTF-8 BOM URL-file regression fix/test after PowerShell input exposed it.
- Organization update 2026-06-04: moved Hermes-related transcript files into `YT_TRANSCRIPT_COLLECTOR/transcripts/hermes/`; moved contents of `Temp/HERMES/` there and deleted the old empty folder.
- No open follow-up unless Baris explicitly requests Playwright/browser fallback after transcript-api failures.

## Hermes Agent Layer (2026-06-04)

### HERMES-001 | DONE | Install Hermes and create MTC profiles [AI: Codex GPT-5]
- Installed Hermes Agent `0.15.2` in `%LOCALAPPDATA%/hermes/hermes-pypi-venv` after the official git installer clone timed out.
- Created profiles: `mtc-steward`, `quantlens-research`, `dashboard-qa`, `backtest-monitor`, `repo-hygiene`.
- Wrote profile-specific `SOUL.md` plus shared `memories/USER.md`, `memories/MEMORY.md`, and `MTC_WORKSPACE.md` guardrails.
- PATH updated for new terminals; current shells may need restart.
- Model/provider setup intentionally not selected to avoid unapproved paid/remote model routing.

### HERMES-002 | OPEN | Configure model/provider per profile [AI: Baris]
- Run one of: `<profile> setup`, `hermes -p <profile> model`, or `hermes -p <profile> config set model <provider/model>`.
- Desktop path is now also available: open Hermes Desktop, click Settings, and choose a provider/model there. Do this only when remote/paid routing is approved.

### HERMES-003 | DONE | Install Hermes Desktop app [AI: Codex GPT-5]
- Installed official Hermes Desktop under `%LOCALAPPDATA%/hermes/hermes-agent/apps/desktop/release/win-unpacked/Hermes.exe`.
- Created Desktop and Start Menu shortcuts.
- Verified normal app launch after fixing the bootstrap marker.
- Screenshot: `C:\tmp\hermes_desktop_final.png`.
- Choose cost/routing policy before using Hermes for live agent sessions.

### HERMES-004 | AWAITING APPROVAL | Install proposed MTC memory package into Hermes core memory [AI: Baris]
- Package path: `_HERMES_MEMORY_IMPORT/`
- Proposed target: `%USERPROFILE%\.hermes\memories\USER.md` + `MEMORY.md`
- Current state: no existing USER.md/MEMORY.md found in Hermes core; directory exists.
- Approval required before any copy/install.

## SP-005 Wave A status update (2026-06-04)

### SP-005 | DONE WAVE A | Strategy Detail Page Redesign [AI: Codex GPT-5]
- Status: **SP-005 Wave A implemented; Wave B/C pending.**
- Files changed: `08_DASHBOARD_APP/apps/web/app.js`, `08_DASHBOARD_APP/apps/web/styles.css`, `08_DASHBOARD_APP/apps/api/mcc_readonly/pipeline_reader.py`.
- Implemented live Strategy Detail Page Wave A: terminal single-scroll layout, human title fallback, merged Verdict & Decision block, Scorecard placeholder directly below verdict, Strategy Taxonomy shell, Review Journey, expanded Trading Rules with visible "Not defined yet", honest Backtest Evidence unavailable state/checklist, Salvageable Ideas placeholder, de-emphasized Source Material, and collapsed Technical Details carrying raw IDs/legacy composite/debug data.
- Intentionally not implemented: SP-004 scoring math, `scorecard_v2`, QuantLens structured reader, backtest-case visualizations, source-claim-vs-reproduced visuals, filter migration to gate status, Pine/MTC/parity/backtest behavior changes, audit-data deletion.
- Validation: `node --check app.js` PASS; `py_compile pipeline_reader.py` PASS; dashboard API tests PASS (`35 passed` with `PYTHONPATH` set); browser check on `http://127.0.0.1:8765/dashboard` confirms all Wave A sections render, first tested title is not raw ID, Technical Details collapsed, missing fields visible, no desktop horizontal overflow after CSS containment.
- Data caveat: current snapshot has no row with real `metrics`, so metrics-present Backtest Evidence could not be visually verified. Missing-rules, legacy-score-only, and no-QuantLens states were verified from snapshot data.

### SP-005 | DONE WAVE B | QuantLens structured reader + detail-page card [AI: Claude]
- Reader DONE (2026-06-05, dispatched to Grok grok-4, Claude-audited): read-only `08_DASHBOARD_APP/apps/api/mcc_readonly/quantlens_reader.py` parses `03_SALVAGE_IDEAS/<candidate>/01_candidate_metadata.yaml` (PyYAML, guarded import). Emits per-candidate `quantlens_verdict` (decision label, commercial-value band §8.6, complexity, testability §8.7, risks — commentary/labels, NO computed score), structured `salvageable_ideas[]` from `candidate_kind` flags, derived `stop_state` (CLOSED_SOURCE_STOP from closed_source_risk HIGH / COMPLEXITY_OVERLOAD from complexity≥8 / GARBAGE), `reference_files` repo-relative links, JSON-safe `raw`. Wired `quantlens` key into `read_model.py`. Fixed 2 audit bugs (ref-files→dir; date→str coercion). Dashboard API tests 35 passed.
- UI DONE (2026-06-05, Claude): `apps/web/app.js` — `findQuantlensCandidate` (joins by candidate_id===row.id, confirmed all 3 match pipeline/audit rows), new `renderQuantlensVerdict` card (decision badge, stop-state banner, commercial/complexity/testability/instrument facts, risk chips, recommended next step), real `renderSalvageableIdeas` from `salvageable_ideas[]`, `buildWaveADecision` now surfaces the real QuantLens label. Section order Verdict→Scorecard→QuantLens Verdict→Taxonomy. `styles.css` adds `.quantlens-stop`. Verified live in the running dashboard (preview): QL strategy renders full card (Equilibrium: SALVAGE, 4/10, 4 components), non-QL strategy shows clean "Not in QuantLens" fallback, no JS error, `node --check` PASS. Not committed.
- Carry-forward: stop-state banner code path (CLOSED_SOURCE_STOP/COMPLEXITY_OVERLOAD) is wired but unverified live (no on-disk candidate currently has a stop_state; all 3 are SALVAGE/no-stop).

### SP-005 | DONE WAVE C | scorecard_v2 gate render [AI: Codex GPT-5]
- Implemented 2026-06-05 as read-only dashboard consumption of real `scorecard_v2` artifacts.
- Added `mcc_readonly/scorecard_reader.py`; `read_model.py` now exposes top-level `scorecards` and attaches `scorecard_v2` / `scorecard_v2_cases` to matching audit/pipeline rows by base strategy id.
- Generated 38 real all-gate scorecard_v2 files for `05_BACKTEST_RESULTS/enriched_metrics_2026-06-05/scorecard_v2`; snapshot currently links 10 audit rows.
- `app.js` renders Gate 1 Intake, Gate 1B MTC Feasibility, Gate 2 Backtest Evidence, and Gate 3 Production Readiness separately; no blended score; null/non-OK scores display as `N/A`; missing/not-scored fields are visible; missing artifacts have a clean fallback.
- Validation: API py_compile PASS, API tests PASS (`35 passed, 1 subtest`), `node --check app.js` PASS, browser check PASS for one linked scorecard row and one missing-artifact fallback row with no JS console errors.
- Honest state: 38/38 scorecard_v2 are still non-promotable/INCOMPLETE because intake, feasibility, production-readiness, annualized sharpe/sortino, regime, and same-window benchmark fields are not available yet. This is expected and not a UI failure.

## MTC-Engine Validation step (2026-06-04)

### MEV-001 | DONE | MTC-Engine Validation implementation [AI: Claude]
- Implemented additive stage in `02_MTC_BACKTEST`: light-risk profile, manual producer adapter
  scaffold, bridge CLI, Supertrend standalone Pine producer adapter, docs, and tests.
- Entry command: `cd MTC_COMMAND_CENTER/02_MTC_BACKTEST && python -m src.cli.mtc_engine_validate --producer supertrend --data <ohlcv> --symbol <symbol> --timeframe <tf>`.
- Verification 2026-06-04: 4 focused tests PASS, compileall PASS, BTCUSDT 1d real-data smoke PASS.
- `MTC_V2.pine` untouched; `MTCRunner` untouched; parity is producer-level raw-signal only.

### MEV-002 | OPEN | Wire first real shortlisted QuantLens producer adapter [AI: Claude | Barış approval]
- Pick one shortlisted producer that already passed cheap naked screening.
- Implement one manual `SignalPlugin` adapter under `02_MTC_BACKTEST/src/modules/signals/producers/`.
- Add or map a standalone Pine producer adapter under `01_MTC_PROJECT/parity_oracles/feature_adapters/pinets/`.
- Run `mtc_engine_validate` with producer-specific risk overrides and record artifacts before promotion.

### MEV-003 | OPEN | Add callable producer-level parity command for bridge reports [AI: Claude]
- Current bridge supports `--parity-command`, but generic auto-discovery is intentionally not implemented.
- Next step: create a feature contract/trace command for each real producer so reports can show `PASS/FAIL`
  instead of `NOT_RUN`.

## Immediate — Sabah Görevleri (2026-06-03)

### NIGHT-2026-06-03 | DONE | 21-iter overnight sweep + morning report [Claude]
- 21 iter / 0 crash / ~3.6M param-eval. Rapor: `05_BACKTEST_RESULTS/MORNING_REPORT.md`.
- 149 robust PASS, 89 beat b&h, 8 down-market alpha — hepsi DSR p<0.50 (kanıtsız).

### NIGHT-FOLLOWUP-001 | OPEN | Down-market 8 adayı forward-paper-trade [Barış onayı]
- APT/ADA/LINK 1h hücreleri en güçlü. Live-bar OOS topla, parity öncesi izle.
- Kaynak: `05_BACKTEST_RESULTS/alpha_summary.json` (down_market_alpha).

### NIGHT-FOLLOWUP-002 | OPEN | DSR ~0 kök neden: search-space inflation [AI: Claude|DeepSeek]
- Tüm adaylar DSR'da çakılıyor. Dar pre-registered hipotez grid'i ile confirmation-only run (küçük family → yüksek DSR gücü).

### NIGHT-FOLLOWUP-003 | DONE | generate_morning_report.py legacy hardcoded OUTPUT_DIR fix [AI: Claude]
- Hâlâ `C:\LAB\tradingview-lab\...` okuyordu (A1). Rapor elle üretildi. `hardcoded_path_rewrite_TODO`'ya bağlıydı.
- Fix (2026-06-05 Claude): replaced the hardcoded legacy path with env-overridable repo-relative default mirroring `mega_walk_forward.py` — `MEGA_OUTPUT_DIR` env else `Path(__file__).parent.parent/"05_BACKTEST_RESULTS"`; added `import os`. Verified: py_compile PASS; default resolves to `03_QUANTLENS/05_BACKTEST_RESULTS` (no `tradingview-lab`); env override honored. Not committed.

### MORNING-001 | OPEN | Buy&Hold baseline güncelle [AI veya Barış]
- Aggregate tamamlandı: 16 iter, 149 robust winner (≥8/16).
- Çalıştır: `python buy_hold_baseline.py --sprint-dir sprint_runs`
- Amaç: TRXUSDT (+107%) / XRPUSDT (+124%) bull market etkisini filtrele, net alpha gör.

### MORNING-002 | OPEN | Promotion assessment güncelle [Barış onayı]
- Mevcut assessment 2026-06-01 tarihli, sadece 13 iter bazlı.
- 149 robust cell ile ADAUSDT/LINKUSDT/SOLUSDT stratejiler ELITE adayı.
- Güncelle: `sprint_runs/PROMOTION_ASSESSMENT_2026-06-01.md`
- Önerilen ELITE onaylar: `QL_DEEPAK_SNAPBACK_50SMA_INTRADAY/TRXUSDT/2h`, `QL_DEEPAK_153_FILTER_1D/SOLUSDT/2h`

### MORNING-003 | OPEN | Transcript manual review [Barış — 31 aday]
- 31 aday bekliyor: 17 LIKELY_MISCLASSIFIED + 14 REVIEW_HUMAN
- Dosya: `11_TRIAGE/reclassification_audit_2026-06-01.md`

---

## Strategy Research Lab (infra eklendi 2026-06-03)

### RESEARCH-001 | REVIEWED — BLOCKED (stale as written), do NOT mass-move [AI: Claude → Barış]
- Reviewed 2026-06-05 (Claude). The literal task is unsafe/obsolete as written:
  1. **`03_SALVAGE_IDEAS/` is now LIVE reader data** — `mcc_readonly/quantlens_reader.py` (SP-005 Wave B) parses those candidate dirs into the dashboard. Moving them WOULD BREAK the QuantLens Verdict card. Exclude from any move.
  2. **`route_user_intake.py` targets a different inbox** (`00_INBOX/USER_INTAKE`, currently EMPTY — dry-run "nothing to route"), NOT `00_INBOX_REPORTS/`.
  3. **`00_INBOX_REPORTS/` = 206 files in Turkish date-folders** (`1 Haziran`, `3 Mayıs`, `Transcrips`). Mapping each to one of 63 STG strategies needs per-file content judgment; auto-token-matching risks misfiling 206 files.
- **Recommendation:** do NOT auto-move. If consolidation is wanted: (a) leave `03_SALVAGE_IDEAS` in place; (b) review `00_INBOX_REPORTS` in small human-confirmed batches, routing only files whose target STG is unambiguous; (c) extend `route_user_intake.py` to accept `00_INBOX_REPORTS` as a source only after a dry-run confirms matches. Left for Barış to greenlight a batch.

### RESEARCH-003 | DONE | Full indicator inventory from MTC_V2.pine [AI: Claude]
- Done 2026-06-05 (Claude), read-only. Extracted the MTC_V2 indicator set from `01_MTC_PROJECT/01_PINE/MTC_V2.pine` (2079 lines) via `ta.*` primitives + plot/variable titles — WITHOUT modifying the `.pine` and without ingesting the full 128K (token-efficient). Output: `05_REGISTRY/MTC_V2_INDICATOR_INVENTORY.md`.
- Inventory: Supertrend (signal producer), MACD (+regime/cross/zero-dist/HTF variants), ADX/DMI, ATR (stops/targets/vol-floor), MA filter, MA slope, **McGinley Dynamic (new)**, **Choppiness (new)**, Donchian/Highest-Lowest, EMA/SMA/WMA/RMA, HTF trend/MACD, barssince. McGinley + Choppiness are the likely gaps vs the current 27-entry seed.
- **Did NOT hand-edit `INDICATOR_REGISTRY.json`** (AGENTS.md: it is generator-produced). The inventory is a reference to feed the generator's curated seed when desired. Full per-gate semantic map (exact lengths/sources/conditions) deferred — needs a dedicated heavy `.pine` read.

### RESEARCH-002 | OPEN | Classification review for review_needed fields [AI: Claude|Barış]
- 63 strategies have at least one `review_needed` placeholder after the 2026-06-04 re-triage refresh.
- Edit each `STGxxx/01_candidate_metadata.yaml` / `producer_spec.json`, then
  re-run `python 03_QUANTLENS/tools/build_strategy_research_registry.py`.
- Track via **Strategy Research Lab → Missing Metadata** tab.

### RESEARCH-003 | OPEN | Full indicator inventory from MTC_V2.pine [AI: Claude]
- INDICATOR_REGISTRY.json is seeded from strategy references + curated list.
- Extract the complete MTC_V2 indicator set (read-only; do NOT modify the .pine).

### RESEARCH-004 | DONE | Re-triage transcript-now-present candidates [AI: Claude — batched]
- Completed 2026-06-04 by Codex. Ledger: `11_TRIAGE/retriage_progress.json` now shows `done=87 pending=0 next_stg=STG064`; plus pilot entries `Stg082`, `Stg083`, `Stg087` = all 90 eligible candidates accounted for.
- Final dispositions log: `11_TRIAGE/retriage_dispositions_2026-06-04.md`.
- New/updated matured strategy folders from final batch:
  - `STG061_ryan_pierpont_breakout_discipline` repaired with spec + source intake for Stg154-Stg158.
  - `STG062_stan_weinstein_stage_analysis` created for Stg160-Stg166.
  - `STG063_tito_options_aware_rs_breakout` created for Stg167-Stg169 and marked `needs_manual_review`.
  - Stg170, Stg171, Stg172 marked duplicates and transcripts attached to existing STG032, STG022, STG056.
- Validation after refresh: `build_strategy_research_registry.py` wrote 63 strategies / 27 indicators / 78 components; `--check` PASS; `validate_research_registries.py` PASS; `build_triage_registry.py` PASS; `node --check app.js` PASS; dashboard API tests `35 passed` with `PYTHONPATH` set; snapshot `strategy_research` includes STG061-STG063.
- Pilot batch (3 HIGH) done 2026-06-04, review-first. Dispositions: `11_TRIAGE/retriage_dispositions_2026-06-04.md`.
  - Stg083 -> CANDIDATE -> created `03_QUANTLENS/strategies/STG047_brian_lee_smallcap_gap_mr_short`.
  - Stg082 -> WIKI_ONLY (Ted Zhang momentum podcast). Stg087 -> DUPLICATE (8EMA exit; overlaps STG002/042/043).
- Finding: top HIGH candidates are interview/educational -> expect WIKI/SALVAGE/DUPLICATE for most; far fewer than 90 new strategies.
- 172 triage worklist now reconciled with on-disk transcripts: 159 have transcripts,
  **90 eligible** (87 HIGH + 3 MEDIUM) — previously rejected only for missing transcript.
- Worklist: `11_TRIAGE/retriage_worklist_2026-06-04.md`. Live registry:
  `05_REGISTRY/TRIAGE_CANDIDATE_REGISTRY.json` (regen `build_triage_registry.py`).
- Visible in **Strategy Research Lab → Triage Worklist** tab.

### RESEARCH-005 | OPEN | Manual review STG063 options-aware proxy assumptions [AI: Claude|Barış]
- `STG063_tito_options_aware_rs_breakout` is a partial deterministic spec. Decide whether to keep it as manual options-aware research or build a stock-only proxy with explicit caveats.
- Do not backtest options returns from stock-only data.

---

## Completed Sprint (2026-06-01 — overnight)
- T-01 Buy&Hold baseline: DONE (117→ şimdi 149 robust, güncelleme gerekli)
- T-02 CPCV + PBO gate: DONE
- T-03 Promotion assessment: DONE (güncelleme gerekli — MORNING-002)
- T-04 MEGA overnight loop: DONE (16 iter, tamamlandı 06:33 yerel)
- T-05 QQE smoke test: DONE (FILTER_OVERLAY — overfitting, kaydedildi)
- T-07 SP-001 MVP-0 CLI: DONE (`mtc_cli/`, 8 test PASS)
- T-08 SP-002 vectorbt enrichment: DONE (`vbt_enrichment.py`, smoke PASS)

## Active (2026-06-01 — overnight workflow consolidation aftermath)

### IM-001 | DONE | analyze_transcripts.py path-resolution fix + basename fallback
- Completed 2026-06-01 by Codex (initial). Verified + basename fallback added by DeepSeek V4 Pro 2026-06-01.
- 165/165 transcripts now resolved and analyzed. 67 had legacy `06_QUANTLENS_LAB\` prefix → basename fallback finds them in `03_QUANTLENS/00_INBOX_REPORTS/Transcrips/`.
- Audit results: 115 ALREADY_OK, 17 LIKELY_MISCLASSIFIED, 14 REVIEW_HUMAN, 19 KEEP_REJECTED, 0 SPLIT_RECOMMENDED.
- 17 + 14 = 31 candidates need Barış manual review. See `11_TRIAGE/reclassification_audit_2026-06-01.md`. [AI: Barış]

### IM-002 | DONE | OUTPUT_DIR / hardcoded path audit script
- Completed 2026-06-01 by Codex. Added `03_QUANTLENS/tools/audit_hardcoded_paths.py`; pre-commit hook calls staged audit. Full default scan currently reports 2,488 existing legacy references.
- `tools/audit_hardcoded_paths.py` yaz — repo'da `C:\LAB\tradingview-lab\` veya benzeri legacy işaretleri grep'le, listele.
- CI/precommit hook'a ekle.
- Mevcut bilinen: `mega_walk_forward.py:32-36` (DATA_BUNDLE_PATH hala legacy işaret ediyor — `MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427` yolu).

### IM-003 | DONE | mega_walk_forward resumable iter
- Completed 2026-06-01 by Codex. `mega_walk_forward.py` supports `--resume`, periodic checkpoint pickle, partial JSON, completed-job skip, and atomic final JSON replace. Verification used synthetic checkpoint helpers; full engine run not executed.
- Crash sonrası iter baştan başlıyor; %94 hesap kayıp.
- `--resume <pickle>` arg ekle. Her N iter'de pickled checkpoint.
- Atomik temp-rename ile partial JSON.

### IM-004 | DONE | Heartbeat in-iter granularity
- Completed 2026-06-01 by Codex. Mega now refreshes heartbeat during in-iteration progress events using `MEGA_HEARTBEAT_*`; loop scripts export context. Verification: Python helper PASS; bash syntax check unavailable.
- Mevcut: heartbeat sadece iter-arası. 75dk sessizlik mümkün.
- Mega'nın `[N/total] elapsed=Xs counts=...` her dakika print'ini parse et, heartbeat dakikalık güncelle.
- Monitor script anomaly threshold için bu lazım.

### IM-005 | DONE | Windows taskschd kurulum
- Completed 2026-06-01 by Codex. `MCC_Overnight_Monitor` scheduled task registered successfully; state `Ready`.
- `tools/register_overnight_monitor.ps1` admin PS ile TEK SEFER çalıştır.
- Çift kanal (taskschd + wakeup) — wakeup tek mekanizma riski yeniden yaşanmasın.

### IM-006 | DONE | CPCV (Combinatorial Purged Cross-Validation)
- Completed 2026-06-01 by Codex. Added `cpcv_validator.py` and rules CPCV Gate. Smoke report: `03_QUANTLENS/tools/cpcv_runs/smoke/CPCV_VALIDATION_REPORT.md`.
- Mevcut 4-gate'e **5. gate** olarak eklenecek.
- Rolling WF + lockbox bağımlı fold'lar yaratıyor; CPCV tüm `(N choose k)` train/test ayrımlarını test eder.
- Embargo + purge (overlap silme) lookahead riskini sıfırlar.
- Referans: López de Prado, "Advances in Financial Machine Learning" Ch.12
- Hedef: `03_QUANTLENS/tools/cpcv_validator.py` — mevcut `mega_walk_forward.py` `_worker` çıktısını alıp CPCV yeniden çalıştırır
- Rules dosyası §8'e "CPCV Gate" satırı eklenecek

### IM-007 | DONE | Probabilistic OOS / PBO
- Completed 2026-06-01 by Codex. Added `probabilistic_pbo.py` and PBO Gate. Smoke report: `03_QUANTLENS/tools/pbo_runs/smoke/PBO_REPORT.md`.
- Mevcut bootstrap_p_positive zaten Probabilistic Sharpe Ratio'nun bir formu
- **Probabilistic Backtest Overfitting (PBO)** ekle — combinatorically symmetric cross-validation
- DSR + PBO birlikte → en katı statistical layer
- Hedef: `tools/probabilistic_pbo.py`

### IM-008 | DONE | In-day single strategy hizli akis scripti
- Completed 2026-06-01 by Codex. Added `single_strategy_backtest.py`; MEGA supports `--strategy/--symbol/--tf`. Smoke output: `03_QUANTLENS/tools/single_strategy_runs/smoke_IM008/`.
- `tools/single_strategy_backtest.py <strategy_id> <symbol> <tf>`
- Tek komut → veri validation + sandbox WF + 4-gate + buy&hold + morning_report
- "1 strateji 5dk" akışı 4-gate atlanmadan otomatik
- Rules §2'deki "Standard Backtest Workflow" 10 adımını sırayla çalıştırır

### IM-009 | DONE | data_check module
- Completed 2026-06-01 by Codex. Added `data_check.py` and wired `single_strategy_backtest.py` to it. Smoke output: `03_QUANTLENS/tools/single_strategy_runs/smoke_IM009/`.
- `tools/data_check.py` — `verify_actual_range(symbol, tf)` API
- Rules §3 "Mandatory Data Validation Rules" first-class destek
- Cache disk içeriği (parquet/csv) ilk/son timestamp ve bar count
- Yanlış manifest claim'lerine karşı tek-doğru-kaynak

## Waiting On
- (none)

## Audit Backlog — LLM Code Review Findings (2026-06-02)

Aşağıdakiler ChatGPT 5.5 / DeepSeek V4 Pro audit'inden çıkan, henüz fix edilmemiş bulgular.
Her item yanında hangi modelin yapması uygun yazıyor.

### AUDIT-001 | DONE | ADX yön hatası [AI: DeepSeek — 1 satır fix]
- `overnight_v2_runner.py:594` — `QL_QTREND_V2_STRONG_ADX` strateji `adx_14 < adx_threshold` kullanıyor.
- Strateji ismi "STRONG ADX" → yüksek ADX (trend) demek; ama kod düşük ADX'de giriyor.
- **KARAR (Barış 2026-06-04, D004): strong-trend intent → `>=`.** İsim aynı kalır (zaten `strong_buy` gate ile tutarlı).
- Fix (2026-06-04 DeepSeek): `adx_14 < ...` → `adx_14 >= ...`. py_compile PASS, line 594 verified.

### AUDIT-002 | DONE | CPCV 3-tuple short strategy desteği [AI: DeepSeek]
- `cpcv_validator.py:86` — CPCV `build_signals()` her zaman 2-tuple varsayıyor.
- `QL_QTREND_V1_SHORT` 3-tuple döndürüyor → crash veya yanlış direction.
- Fix (2026-06-04 DeepSeek): canonical 3-tuple parse from mega_walk_forward.py:654-658; `evaluate_split` gets `direction` param → `simulate_slice`; validated via CPCV smoke.

### AUDIT-003 | DONE | rigorous_walk_forward.py short desteği yok [AI: DeepSeek]
- `rigorous_walk_forward.py:266` ve `rigorous_walk_forward_parallel.py:254` — `simulate_slice` `direction` parametresi yok.
- Short strategy feed edilirse sıfır trade / NaN sonuç üretir sessizce.
- Fix: `mega_walk_forward.py:simulate_slice` ile aynı short branch'i ekle (direction param + is_short logic).
- Fix (2026-06-04 DeepSeek): added `direction="long"` default + 3-tuple-safe `build_signals` parsing to both rigorous walk-forward tools; ported mega short branch with short stop above entry, target below entry, no short trailing-EMA exit, `raw=entry/exit-1`, and short R `(entry-exit)/risk`. Verified py_compile PASS, long 2-tuple regression byte-identical, synthetic short smoke PASS for both iat and numpy loops.

### AUDIT-004 | DONE | BUNDLE_MANIFEST env override yok [AI: DeepSeek]
- `mega_walk_forward.py:35-38` — `BUNDLE_MANIFEST` hardcoded arşiv path, `MEGA_OUTPUT_DIR` gibi env override yok.
- Fix (2026-06-04 DeepSeek): `MEGA_BUNDLE_MANIFEST` env var with legacy fallback; env override + fallback both verified.

### AUDIT-005 | DONE | PBO asimetrik CSCV split sorunu [AI: DeepSeek]
- `probabilistic_pbo.py:54` — default CPCV 15 sütun emit eder (tek sayı), PBO `n_splits // 2` ile 7/8 asimetrik partition oluşturur.
- Fix (2026-06-04 DeepSeek): `usable = n_splits_available - (n_splits_available % 2)` → even splits; dropped column tracked via `splits_used`/`splits_available`/`partition_note`; validated 15→14 even split, pbo=0.102564.

### AUDIT-006 | DONE | rolling_fold_indices min bars guard [AI: DeepSeek]
- `mega_walk_forward.py:590` — `span_end < 1000` guard. 1000 bar altı dataset (yüksek TF, kısa tarih) sessizce `[]` döner; cell test edilmeden skip.
- Fix (2026-06-04 DeepSeek): added `fold_feasibility(n_bars)` sibling helper (mirrors rolling_fold_indices guards), `warnings.warn` + `INSUFFICIENT_DATA` classification in `_worker` after MIN_BARS_REQUIRED. Verified fold_feasibility(500)→(False,...), (50000)→(True,""). Did not change fold math/step/overlap.

### AUDIT-008 | DONE | Rolling fold OOS window overlap [AI: DeepSeek/Claude]
- `mega_walk_forward.py:604` — `step = remaining//(NUM_FOLDS-1)` = 0.10·span = half of test_size → structural 50% OOS overlap; `folds_positive` inflated.
- **KARAR (Barış 2026-06-04, D006): disjoint OOS — `step = test_size`** + PASS tightened to `pos == n_folds`.
- Fix (2026-06-04 DeepSeek Batch D): line 604 `step = test_size`; line 732 PASS elif `pos >= ceil(n_folds/2)` → `pos == n_folds` (STRONG inner unchanged). Claude-audited: py_compile PASS; disjoint verified n=1500/6000/50000/100000 (always 2 folds, prev OOS ke == next ks, 0 overlap); n<1000-span → []. No lockbox/CPCV/PBO change.
- **OPEN op (Barış, not code): re-run existing sweep** — 149 robust-PASS (DSR-unconfirmed) were computed under old overlapping geometry; must re-run under disjoint folds + `pos==n_folds` before DSR-lock.

### AUDIT-007 | DONE | paths.py empty dir silent select [AI: DeepSeek/Claude]
- `paths.py:30` — `03_QUANTLENS` boş olsa da ilk `exists()` match seçiliyor.
- Fix (2026-06-04 DeepSeek Batch C): `default_quantlens_root` artık non-empty dir tercih ediyor (`any(c.iterdir())`, OSError-skip), fallback first-existing→candidates[0]. registry_reader + audit_reader inherit. Claude-audited: py_compile + 5/5 mock selection cases (a-e) PASS.

### AUDIT-009 | DONE | bars_per_day=78 crypto'ya yanlış [AI: DeepSeek/Claude]
- Fix (2026-06-04 DeepSeek Batch E): mega `EQUITY_ONLY_STRATEGIES` set (empty default) + `EQUITY_EXCHANGES={NYSE,NASDAQ,ARCA,AMEX,BATS}`; gate in `_worker` after find_ds → `SKIPPED_RULE` if strategy equity-only AND `ds.exchange` not equity. `overnight_v2_runner` registers the 4 OR strategies. Data is 100% Binance crypto → all 4 skip now; auto-run if US-equity data added. Claude-audited: py_compile PASS, end-to-end `_worker(GAP_5M,BTCUSDT,15m)`→SKIPPED_RULE(exchange=BINANCE), no over-skip (NASDAQ would run), pure-mega unaffected (empty set). bars_per_day=78 unchanged (correct for equity).
- `overnight_v2_runner.py:418,447,474,506,509` — `bars_per_day = 78` hardcoded (US equity 5m session = 6.5h).
- Etkilenen 4 OR stratejisi: QL_CONNELL_EVENT_DRIVEN_GAP_5M, QL_AVWAP_BRIAN_INTRADAY_OR_5M, QL_EPISODIC_PIVOT_CHRISTIAN_5M, QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M.
- Crypto 24/7 → session open yok. `bar_idx % 78` her 24h crypto gününün ilk 78 barını yanlışlıkla "opening range" etiketliyor.
- **KARAR (Barış 2026-06-04, D005): US-equity-session-only.** `bars_per_day=78` doğru, crypto'ya GENELLEŞTİRME. Crypto/24-7 data'da bu 4 strateji skip + `INSUFFICIENT_DATA`/`N_A` not ile (opening-range session open olmadan anlamsız). Symbol-aware/288 YOK.
- Fix: 4 OR stratejisini US-equity sembol/session'a gate et; crypto feed'de signal üretme, explicit skip-reason döndür.
- Doğrulandı: kod incelendi 2026-06-02 (Mimo v2.5 audit Run 7,11 — gerçek bulgu).

### AUDIT-010 | DONE | ingest.py transcript re-write race [AI: DeepSeek/Claude]
- `ingest.py:249-251` — `if not target.exists() or sha != state_sha:` dış koşul, ama iç `if not target.exists():` sadece yeni dosya append ediyor.
- Bug: dosya VAR + içerik DEĞİŞTİ (sha farklı) durumunda → dış koşul True, iç koşul False → **dosya hiç güncellenmiyor**, sadece `transcript_main_sha` state set ediliyor.
- Fix (2026-06-04 DeepSeek Batch C): iç guard kaldırıldı; `new_transcripts.append(...)` dış koşul altında koşulsuz çalışıyor → sha-mismatch overwrite queue ediyor. Writer (L341 `target.write_text`) koşulsuz overwrite — safe. Claude-audited: py_compile + on-disk read confirm, surroundings untouched.

## Side Projects (parked — pick up when ready)

### SP-005 | Strategy Detail Page Redesign (trading-review dashboard) [AI: Claude lead + Barış]
Status: plan v3 ready, not started. Proposed 2026-06-02, revised 2026-06-03 (v2→v3).
Trigger: Barış flagged the strategy-detail page as confusing/too technical.
**Direction LOCKED: terminal** (`proto_B2_terminal.html`; single-scroll; A/clinical/
editorial dropped). v3 structural rules: (1) ONE scoring system = Scorecard;
QuantLens = commentary that references it, no double scoring. (2) Verdict & Decision
MERGED into one top block. (3) Scorecard directly under verdict, click-to-expand
gates. (4) Backtest = TradingView-tester-style CASES (video-settings + optimized
best, each w/ settings·symbol·timeframe on one standard window). (5) Stage prototypes
built (rules-extracted/testability/backtested/promotion). Prototypes + shared
`proto_terminal.css` in `08_DASHBOARD_APP/apps/web/prototypes/`.

Problem: current page (`08_DASHBOARD_APP/apps/web/app.js:389` `renderUnifiedStrategyDetail`)
is a debug dump — raw ID as title, two dense parallel tables, one misleading
`57/100` headline, bare machine terms. Raw decision sentence from
`mtc_v2_reader.py:217` (interpolates raw ID + raw status).

Fix: single-scroll trading-review dashboard — English-only UI, human name +
translated-to-English description, sticky mini-summary, decision summary,
**QuantLens Verdict** (ruthless audit layer), **Strategy Taxonomy** chips,
review-journey stepper, expanded trading rules, 4 gate bars, honest backtest
evidence, **Salvageable Ideas** (mandatory), debug collapsed into Technical.

KEY FINDING (2026-06-03): QuantLens is **already a real pipeline** —
`03_QUANTLENS/03_SALVAGE_IDEAS/<candidate>/` has 7 artifacts each;
`01_candidate_metadata.yaml` already carries `quantlens_decision`,
`commercial_value_score`, `complexity_score`, `repaint_risk`, `lookahead_risk`,
`closed_source_risk`, `candidate_kind` (salvage categories), `market_type`,
`recommended_next_step`. Dashboard readers **ignore these today**. QuantLens
Verdict section surfaces existing data via a new read-only `quantlens_reader.py`.

**Full plan:** `03_QUANTLENS/_user_guide/11_STRATEGY_DETAIL_PAGE_REDESIGN_PLAN.md` (v3)
**Prototypes (DONE, approved 2026-06-03):** `08_DASHBOARD_APP/apps/web/prototypes/` —
terminal set: `proto_B2_terminal.html` (blocked), `proto_stage_rules_extracted.html`,
`proto_stage_testability.html`, `proto_stage_backtested.html`, `proto_stage_promotion.html`.
English-only, single-scroll, CSS inlined.
**Depends on:** SP-004 (scoring) for Wave C gate bars.
**NEXT: awaiting Barış go-ahead to start Wave A coding (not yet authorized).**

Three waves:
- Wave A — single-scroll UI/wording/layout on EXISTING data: `ui_labels` map,
  decision-object refactor (ID-free), header + sticky summary + decision summary,
  taxonomy shell, review-journey stepper, trading-rules card ("Not defined yet"),
  Technical `<details>`, source slim-down, responsive CSS. [Claude/Any]
- Wave B — QuantLens structured data: new `quantlens_reader.py` (parses salvage
  YAML/markdown), QuantLens Verdict card, Salvageable Ideas section, conditional
  render matrix (garbage/closed-source/complexity stops), repaint/lookahead/
  marketing/unverified-claim warnings, commercial-value + testability +
  evidence-level + documented-vs-proven derivations. Schema add for
  CLOSED_SOURCE_STOP/COMPLEXITY_OVERLOAD + structured `salvageable_ideas[]`. [Claude]
- Wave C — `scorecard_v2` (SP-004 P2) gate bars + N/A + backtest-evidence visuals
  (equity, metrics, B&H, source-claim-vs-result) + filter migration. [Claude]

Files: `apps/web/{app.js,index.html,styles.css}`, `mtc_v2_reader.py` (decision
object), new `mcc_readonly/ui_labels.py`, new `mcc_readonly/quantlens_reader.py`,
`audit_reader.py` (join verdict to row). No scoring math here (consumes
`scorecard_v2`). Constraint: presentation + read-only QuantLens reader — no live
trading, no Pine/parity/pipeline change, audit data moved not deleted.

Barış decisions (2026-06-03, all = plan's recommended): QuantLens above Taxonomy;
AI-generated names (editable); provisional commercial-value bands; **ship Wave A
first**; closed-source → still show independent sub-ideas; derive stop-states (no
YAML schema change now). No open questions. Awaiting go-ahead to start Wave A
(not yet authorized).

### SP-004 | Strategy Scorecard Redesign (gate-based, edge-weighted) [AI: Claude lead + DeepSeek + Barış]
Status: **P0A+D1-D6 signed; P1A/P1/P2 DONE; Phase 3 gate scorers (Gate1/1B/3 + unified composer) DONE 2026-06-05. Next: P1.5 bands (Barış) + dashboard render (Wave C) + metric-enrichment (Barış-gated).**
Proposed 2026-06-02.
Trigger: when ready to fix the strategy-detail score Barış flagged as
"yetersiz ve hatalı".

**P0A delivered (spec only, no code, no Pine/MTC/parity change):**
- Canonical rubric `03_QUANTLENS/_user_guide/12_STRATEGY_EVALUATION_RUBRIC.md`
  (English; Gate2 rebalanced Regime 5→10 / Perf 20→18 / Sample 15→12; added
  Sharpe/Sortino/recovery/WFO/CPCV/PBO as Gate2 metrics; Gate1B /50+derived PASS;
  Gate1B-vs-Gate3 de-dup; parity hard gate; SAFE_WITH_DELAY −3 / NEEDS_MODIFICATION
  block; PBO≥0.5→OVERFIT_SUSPECT; field map per sub-criterion).
- Schemas `06_SCHEMAS/{status_envelope, evaluation_artifact_v1,
  production_readiness_artifact_v1}.schema.json` (validated: meta-schema + $ref +
  sample instance + negative case all pass).
- Template `03_QUANTLENS/_templates/strategy_evaluation_record_template.yaml`.
- **Barış must approve D1-D6** (rubric §"Owner decisions") before P2 scoring locks:
  D1 Gate1B mode, D2 PBO policy, D3 parity gate, D4 Gate3 separate artifact,
  D5 bands (set in P1.5), D6 thesis-title author. Draft uses recommended defaults.

Problem: current `build_scorecard()` (`08_DASHBOARD_APP/apps/api/mcc_readonly/presentation_reader.py:65`)
is one flat 100-blend that measures **pipeline progress, not edge** — 25/35
backtest points are pure stage maturity, return/PF are risk-blind, no drawdown /
Sharpe / benchmark / OOS / PBO / repaint hard-fail.

Fix: replace single composite with 4 separate gates + hard-fail flags
(Gate1 intake /100, Gate1B feasibility /50, repaint pass/fail, Gate2 backtest
/100 risk-adjusted, Gate3 production /100). Never recollapse to one number.
~Half the Gate2 inputs (WFO/CPCV/PBO/B&H) already computed by overnight tooling.

**Full plan:** `03_QUANTLENS/_user_guide/10_STRATEGY_SCORECARD_REDESIGN_PLAN.md`
**Source rubric (DELETE when done):** `11_TRIAGE/_eval_pipeline_source_TEMP/`

Phases (~8–10 days, order revised after 2 LLM audits — see plan §9):
- P0A rubric mapping + 2 JSON schemas (eval + production_readiness) + template
  fields (thesis_en, hard-fail reasons, run_id, phase_current) [Claude → Barış] — **DONE 2026-06-04, awaiting sign-off**
- P1A fix CPCV 3-tuple (AUDIT-002) + PBO split (AUDIT-005) + N_A fallback
  BEFORE hard-gating [DeepSeek] — **DONE 2026-06-04**
- P1 emit `evaluation_artifact_v1` w/ status envelope on 5–10 strategies [Claude/DeepSeek]
- P1.5 finalize numeric bands FROM real distributions, not guessed [Claude → Barış]
- P2 gate scoring engine → `scorecard_v2` (parallel to legacy) + golden tests [Claude, cross-model review]
- P3 dashboard: thesis title + gate bars + migrate filters to gate-status [Claude/Any]
- P4 backfill w/ completeness check + ranking validation [DeepSeek + Barış]
- P5 cleanup: legacy flag removal + **delete TEMP** (only now) [Claude]

Open for Barış (plan §8): numeric bands (set in P1.5), trade-count minimums,
PBO≥0.5→OVERFIT_SUSPECT?, AI-vs-human thesis title, Gate1B /50-vs-PASS,
Gate3 separate production artifact.
Constraint: read-only on trading/Pine/parity — only adds output writer + scoring + UI.

### SP-003 | Python Live Trading Engine (Pine Script bypass) [AI: Claude]
Status: planned, not started. Proposed 2026-06-01.

**Sistem Özeti:**
Mevcut MTC pipeline (backtest → optimizasyon → sinyal) çıktısını doğrudan
Binance'e bağlayan, TradingView/Pine Script bağımlılığını kaldıran tam otonom
canlı trade altyapısı.

**Mimari:**
```
mega_walk_forward.py        → optimal parametre çıktısı
      ↓
signal_generator.py         → BUY/SELL/HOLD sinyali (mevcut strateji mantığı)
      ↓
binance_executor.py         → ccxt ile Binance API order
      ↓
VPS (Hetzner/DigitalOcean)  → 7/24 çalışır, bilgisayardan bağımsız
```

**Neden Pine Script'e gerek kalmaz:**
- Pine Script sadece görsel + alert üretir; trade execution yok
- ccxt kütüphanesi 100+ exchange destekler, Binance tam uyumlu
- Python: backtest + sinyal + execution tek yerde → debug kolaylığı
- ML entegrasyonu, CPCV, PBO gibi mevcut katmanlar doğrudan bağlanabilir

**Teknik Bileşenler:**
- `ccxt` → Binance Spot / USD-M Futures / COIN-M Futures API
- Binance Testnet → gerçek para olmadan tam test (`set_sandbox_mode(True)`)
- `systemd` service veya `nohup` → VPS'te arka plan çalışma
- Position sizing → risk per trade sabit ($, % veya ATR bazlı)
- Stop-loss / take-profit → `create_order` ile OCO order

**VPS Gereksinimi:**
- Minimum: 1 CPU, 1GB RAM → Hetzner CX11 (~4€/ay)
- Lokasyon: Frankfurt veya Tokyo (Binance sunuculara düşük latency)
- Scalping varsa lokasyon kritik; swing/daily için fark yok

**Scope:**
- Yeni klasör: `MTC_COMMAND_CENTER/05_LIVE_ENGINE/` (önerilir)
- `binance_executor.py` — order yönetimi, rate limit handling
- `signal_bridge.py` — mevcut backtest çıktısını live sinyale dönüştürür
- `risk_manager.py` — position sizing, max drawdown kill switch
- `monitor_live.py` — açık pozisyon takip, heartbeat log

**Kritik Riskler:**
- Backtest → live performans farkı (slippage, funding rate, latency)
- API key güvenliği → .env, IP whitelist zorunlu
- Kill switch eksikliği → runaway loss riski
- Pine Script'te olan görsel analiz burada yok → TV charts korunabilir

**TradingView korunabilir mi:**
- Evet. TV sadece görsel analiz + chart için tutulabilir
- Sinyal ve execution Python'a taşınır
- Hibrit mimari mümkün: TV chart → alert → Python webhook → ccxt order

**Pickup trigger:**
- Backtest pipeline stabil ve tutarlı OOS sonuç ürettiğinde
- En az 3 ay paper trading (testnet) başarısı sonrası canlıya geçiş

**Out of scope (bu SP altında yapılmaz):**
- Pine Script veya MTC_V2.pine değişikliği
- Mevcut backtest/WF/CPCV pipeline değişikliği
- High-frequency / scalping (swing/daily ile başla)
- Multi-exchange (sadece Binance ile başla)

### SP-002 | vectorbt analytics layer (post-processing enrichment) [AI: Claude|DeepSeek]
Status: planned, not started. Proposed 2026-06-01.
Goal: wire vectorbt as post-processing layer on top of TradingView trade data.
`data_get_trades` MCP → `vbt.Portfolio.from_orders()` → richer metrics (Calmar,
Sortino, Omega, rolling Sharpe, underwater equity curve, Monte Carlo) not
natively available in TV. Does NOT replace Pine strategies or MCP tooling.
Optionally: validate/replace `cpcv_validator.py` with vectorbt's built-in CPCV.

Scope: new helper `03_QUANTLENS/tools/vbt_enrichment.py` only.
No Pine / MTC / parity edits. No replacement of `mega_walk_forward.py`.
Pre-req: `pip install vectorbt` (or `vectorbt-pro` if available).

Acceptance:
- Takes a list of TV trade dicts (from `data_get_trades`) + price series
- Returns enriched stats dict + optional HTML report
- Integrates as optional post-step in `single_strategy_backtest.py`

Pickup trigger: whenever a sprint or single-strategy result needs deeper
analytics than the current 4-gate pipeline provides.

### SP-001 | Internal CLI layer + dashboard buttons (`mtc_cli/`) [AI: Claude]
Status: planned, not started. Approved 2026-05-31 by Barış.
Goal: agent-native CLI surface + 1:1 dashboard buttons so any AI model (and
Barış) can drive recurring workflows without memorizing commands or scanning
the repo. Cuts next-session context cost. Wraps existing scripts + MCP — no
replacement of `MTC_V2.pine`, parity logic, or TradingView MCP tools.

Decision reference: `DECISIONS.md` D002 (adopt internal CLI; reject CLI-Anything).

Hard constraint: at scaffold time, re-read all `_AI_MEMORY/` anchors,
`AGENTS.md`, `AI_RULES.md`, `DO_NOT_TOUCH.md`, run `git status` +
`git log --oneline -20`, diff intent vs reality, surface drift to Barış,
**no write until approval**. Treat plan below as intent, not contract.

Must obey 7-gate workflow (AI_RULES.md). Start at Gate 1.

#### MVP-0 — CLI skeleton + read-only audit (~1 evening)
- Whitelist (declare in G1): new folder `mtc_cli/` only.
- Deliverables: `mtc_cli/__main__.py`, `mtc_cli/contract.py` (envelope,
  exit codes, error categories), `mtc_cli/commands/audit.py`,
  `mtc_cli/tests/`.
- Command: `python -m mtc_cli audit repo [--json]` — read-only snapshot.
- Acceptance: valid JSON envelope, exit 0 on clean repo, exit 2 on missing
  memory file fixture, byte-stable on unchanged repo.
- Touches Pine / MTC / parity: **no**. Skip explicit Barış approval gate.
- Gates: G1 → G2 → G3 → G4 → G5 (reviewer must be Codex or Gemini, not
  Claude) → G6 (subprocess + file IO surface = required) → G7.

#### MVP-0.5 — One dashboard button (~1 evening)
- Whitelist: `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/` only.
- Deliverable: minimal page with "Audit Repo" button calling the CLI via
  existing API. Tooltip = one-line explanation.
- Acceptance: click → JSON envelope rendered to screen, no business logic
  in dashboard (thin wrapper only).
- Reuses existing `08_DASHBOARD_APP/apps/api` pattern. No new app.

#### MVP-1 — Memory + handoff writes (~2–3 evenings)
- Whitelist: `mtc_cli/` + dashboard button extensions only.
- Deliverables: `mtc memory append`, `mtc handoff write`,
  `mtc handoff lock/unlock`. `.bak` rotation, mtime guard, append-only
  defaults, `--dry-run` default for first week.
- CLI becomes sole programmatic writer for `GLOBAL_HANDOFF.md`,
  `SESSION_LOG.md`, `NEXT_STEPS.md`, `DECISIONS.md` — automates Gate 7.
- Hand-edits still allowed (Barış) but a pre-commit hook warns.
- Acceptance: idempotent (run twice unchanged repo = byte-identical),
  hostile-input tests pass, generated handoff < 2KB.
- Gates: full G1 → G7. G6 mandatory.

#### MVP-2+ (later, not committed)
- `mtc pine check` (wrap MCP `pine_smart_compile` — read-only).
- `mtc report build` (deterministic report from backtest artifact dir).
- `mtc route classify` (cheap-model intake classifier with JSON-schema gate).
- CLI-Anything evaluation: deferred indefinitely. Revisit Q3 2026 only if
  trigger condition (need to drive an unscriptable external GUI) appears.

#### Out of scope (do NOT do under SP-001)
- Any edit to `MTC_V2.pine`, parity files, or MTC strategy behavior.
- Live trading anything.
- New root-level handoff files.
- New prompt folder at root — templates (if any) go in
  `04_SHARED/prompts/05_ai_workflow/`.
- Replacing `mcp__tradingview__*` tools. CLI wraps, never replaces.
- Auto-execution of `next_action` suggestions in CLI output.
- New runtimes (node, rust, go). Python + PowerShell only.

#### Open risks to carry into G1
- `PROJECT_MEMORY.md` (stable) vs `ACTIVE_FILES.md` (volatile) boundary —
  CLI's audit must respect, not blur.
- Gate 5 cross-model review not hook-enforced — must invoke Codex/Gemini
  manually for MVP-0.
- Parity smoke command not pinned — N/A for MVP-0/0.5/1, but record gap
  forward to first parity-touching sprint.

## Recently Closed (2026-05-31, Phase 6 follow-ups)
- I: source-parent cleanup completed for the Command Center audit. `QLR_*` parent rows that share a YouTube URL with extracted child candidates, or contain multi-case split evidence, are now `SOURCE_PARENT`, hidden from normal strategy/MTC_V2 queues, and protected by tests. Remaining visible rejected rows have transcripts and are rejected for source/classification reasons, not missing transcript.
- G: transcript/source-map repair for `11_TRIAGE/2026-05-30_rejected_worklist.xlsx` completed in the clean repo. The 99 HAS_URL_NO_TRANSCRIPT worklist candidates now resolve with transcript links in the refreshed audit; NO_URL_NO_TRANSCRIPT remains unresolved by user report.
- H: repeated-URL audit completed for the same workbook. See `MTC_COMMAND_CENTER/11_TRIAGE/duplicate_url_strategy_audit_2026-05-31.md`; no clear accidental duplicate group found.
- A: audit artifacts committed (`2a38d19`).
- B: legacy freeze policy ratified — accept + document, no NTFS DACL (`dcdf913`).
- C: xlsx-missing warning suppressed in CSV-only mode + AUTO_002 smoke PASS (`d35e620`).
- D: Phase 4 manifest full SHA256 + Phase 5 divergence notes (`c3e78f4`).
- E: `update_tracker.py` documented as deferred one-shot (`1b7caff`).
- F: Phase 1 verification reviewed — PASS; path rewrite policy ratified
  (active set complete, deferred set fix-on-demand). See
  `docs/migration_manifests/PATH_REWRITE_POLICY.md`.

## Reference Documents
- Migration audit: `docs/migration_manifests/phase6_audit_report.md`
- Legacy freeze policy: `docs/migration_manifests/LEGACY_FREEZE_POLICY.md`
- Path rewrite policy: `docs/migration_manifests/PATH_REWRITE_POLICY.md`
- Per-script TODO: `MTC_COMMAND_CENTER/02_MTC_BACKTEST/hardcoded_path_rewrite_TODO.md`
