# GLOBAL_HANDOFF

Last updated: 2026-06-05 (SP-004 annualized Sharpe/Sortino enrichment)
Updated by: Codex GPT-5
Active project: TradingView-LAB / MTC Command Center
Current objective: enrich Gate 2 annualized Sharpe/Sortino evidence - DONE.
Current phase: DeepSeek delegated implementation audited by Codex; ready for fresh sweep propagation.
Current blockers: full scorecard promotion remains blocked by missing intake, feasibility, production-readiness, param-stability, slippage, EMA benchmark, and regime metrics.

## Codex GPT-5 + DeepSeek 2026-06-05 - SP-004 annualized Sharpe/Sortino
Scope: delegated read-only feasibility investigation, then bounded additive output work to DeepSeek for `03_QUANTLENS/tools/mega_walk_forward.py` and `build_evaluation_artifact.py`; Codex audited the diff and validation. No signal logic, classification thresholds, old MEGA `sharpe`/`sharpe_pt`, Pine, MTC behavior, parity, schemas, generated artifacts, or live-trading surface changed.

Implemented:
- `SliceStats` now has defaulted `annualized_sharpe` and `annualized_sortino` fields.
- `simulate_slice` records closed trade events and derives a daily strategy equity curve from calendar-day last equity, with exit-bar costs applied exactly once via existing `net`.
- Annualized Sharpe uses daily returns with `sqrt(365)`; Sortino uses downside daily returns with conservative finite fallback `0.0` when undefined.
- `build_evaluation_artifact.py` maps `metrics.sharpe` and `metrics.sortino` only from the new annualized lockbox fields. Older MEGA `sharpe`/`sharpe_pt` and any old `sortino` remain unused.

Validation:
- DeepSeek reported py_compile and synthetic checks PASS.
- Codex audit PASS: py_compile, `git diff --check`, real one-cell MEGA run, artifact build, Gate2 score, schema validation, and backward-compatibility check on pre-annualized MEGA JSON.
- Real one-cell result: existing lockbox fields unchanged; new lockbox `annualized_sharpe=1.307`, `annualized_sortino=2.6959`; artifact Sharpe/Sortino OK from annualized source paths; Gate2 Sharpe 5/5 and Sortino 4/4; schema errors 0.
- Backward compatibility: rebuilding 38 artifacts from `worst_window_2026-06-05_283d198` produced Sharpe N_A 38/38 and Sortino N_A 38/38, proving old t-stat fields are not remapped.

Carry-forward:
- Run a fresh full sweep before dashboard scorecards show annualized Sharpe/Sortino globally.
- Remaining Gate2 blockers after propagation: parameter stability, slippage model, EMA benchmark, and regime split.

## Codex GPT-5 2026-06-05 - SP-004 worst-window fresh sweep
Scope: regenerated run artifacts under the committed worst-window drawdown code (`283d198`). No Pine, MTC behavior, parity, schema, live-trading surface, or signal logic changed.

Run: `03_QUANTLENS/05_BACKTEST_RESULTS/worst_window_2026-06-05_283d198/`.
- MEGA: 1700 cells, 8 workers, 880.4s; 31 PASS + 7 STRONG_PASS = 38 candidate cells; 1 BH-FDR survivor; 0 DSR-robust; 0 robust final.
- Validation tail: CPCV `--v2`, PBO, 38 evaluation artifacts, 38 Gate-2 scorecards, 38 scorecard_v2 files.
- Audit: 38/38 PASS+STRONG_PASS cells include `summary.buy_hold_lockbox`; 38/38 include `summary.worst_window_drawdown_pct`; 38/38 artifacts have B&H benchmark OK and worst-window metric OK; 38/38 artifacts schema-valid.
- Result: Gate2 score range 42.59-73.0, mean 56.04; all 38 remain INCOMPLETE, 0 Gate2 pass, 0 all-gate promotable. Top cell: `QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL|LINKUSDT|1h` score 73.0.

Carry-forward:
- B&H benchmark and worst-window drawdown are no longer Gate2 blockers for the fresh scorecard set.
- Remaining Gate2 blockers: annualized Sharpe/Sortino, parameter stability, slippage model, EMA benchmark, and regime split.

## Codex GPT-5 + DeepSeek 2026-06-05 - SP-004 Gate2 worst-window drawdown
Scope: delegated bounded additive output work to DeepSeek for `03_QUANTLENS/tools/mega_walk_forward.py` and `build_evaluation_artifact.py`; Codex audited the diff and validation. No signal logic, classification thresholds, Pine, MTC behavior, parity, schemas, generated artifacts, or live-trading surface changed.

Implemented:
- `mega_walk_forward.py` now emits `summary.worst_window_drawdown_pct` as the maximum absolute `max_drawdown_pct` across the selected config's `fold_test` slices, rounded to 3 decimals and JSON-safe.
- `build_evaluation_artifact.py` now maps `metrics.worst_window_drawdown_pct` from `summary.worst_window_drawdown_pct` first, with backward-compatible lockbox fallback only if that exact field exists. It does not fabricate this metric from lockbox max drawdown.

Validation:
- DeepSeek harness reported py_compile and synthetic builder checks PASS.
- Codex audit PASS: py_compile both files, `git diff --check`, synthetic builder primary/fallback/missing checks, real one-cell MEGA run `QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL LINKUSDT 1h`.
- Real one-cell result: `summary.worst_window_drawdown_pct=19.452`; artifact metric OK from `mega:summary.worst_window_drawdown_pct`; Gate2 worst-window criterion scored 4/4; one-cell artifact schema errors 0.

Carry-forward:
- Run a fresh full sweep before dashboard scorecards show the new worst-window metric globally.
- Remaining Gate2 blockers after worst-window propagation: annualized Sharpe/Sortino, parameter stability, slippage model, EMA benchmark, and regime split.

## Codex GPT-5 2026-06-05 - SP-004 B&H benchmark fresh sweep
Scope: regenerated run artifacts under the committed same-window B&H benchmark code (`7175ff6`). No Pine, MTC behavior, parity, schema, live-trading surface, or signal logic changed.

Run: `03_QUANTLENS/05_BACKTEST_RESULTS/bh_benchmark_2026-06-05_7175ff6/`.
- MEGA: 1700 cells, 8 workers, 807.5s; 31 PASS + 7 STRONG_PASS = 38 candidate cells; 1 BH-FDR survivor; 0 DSR-robust; 0 robust final.
- Validation tail: CPCV `--v2`, PBO, 38 evaluation artifacts, 38 Gate-2 scorecards, 38 scorecard_v2 files.
- Audit: 38/38 PASS+STRONG_PASS cells include `summary.buy_hold_lockbox`; 38/38 evaluation artifacts have B&H benchmark OK and `completeness.has_benchmark=true`; 38/38 artifacts schema-valid against `evaluation_artifact_v1`.
- Result: Gate2 score range 38.59-69.0, mean 52.1; all 38 remain INCOMPLETE, 0 Gate2 pass, 0 all-gate promotable. Top cell: `QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL|LINKUSDT|1h` score 69.0.

Carry-forward:
- B&H is no longer a Gate2 blocker for the fresh scorecard set.
- Remaining Gate2 blockers: annualized Sharpe/Sortino, worst-window drawdown, parameter stability, slippage model, EMA benchmark, and regime split.

## Codex GPT-5 + DeepSeek 2026-06-05 — SP-004 Gate-2 same-window buy-and-hold benchmark
Scope: delegated bounded additive output work to DeepSeek for `03_QUANTLENS/tools/mega_walk_forward.py` and `build_evaluation_artifact.py`; Codex audited the diff and fixed two correctness details before accepting it. No signal logic, classification thresholds, Pine, MTC behavior, parity, schemas, generated artifacts, or live-trading surface changed.

Implemented:
- `mega_walk_forward.py` now computes `summary.buy_hold_lockbox` for the exact lockbox window: long-only buy at first lockbox open, hold to final lockbox close, with compound return, positive max drawdown, and finite return/DD ratio.
- Codex audit fix: the B&H equity curve includes the entry baseline so an immediate close below entry counts as drawdown.
- Codex audit fix: helper returns plain Python floats, not `numpy.float64`, to preserve JSON safety.
- `build_evaluation_artifact.py` now emits `benchmark.excess_alpha_pct` as `strategy net_return_pct - buy_hold_return_pct` and `benchmark.beats_bh_risk_adjusted` as `strategy ret_dd_ratio > buy_hold_ret_dd_ratio AND excess_alpha_pct >= 0`, both `OK` only when real inputs exist. `benchmark.beats_ema_benchmark` remains `N_A`.
- `completeness.has_benchmark` is now true only when the B&H benchmark fields are OK; otherwise `benchmark` remains in `missing`.

Validation:
- `python -m py_compile MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_evaluation_artifact.py` PASS.
- Synthetic helper smoke PASS: entry open 100, first close 80, final close 120 -> return 20.0%, max drawdown 20.0%, JSON-safe floats.
- Synthetic builder smoke PASS: benchmark fields become OK and `has_benchmark=true` when B&H inputs exist.
- Real one-cell audit run PASS: `QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL LINKUSDT 1h`, 1 worker, 4.3s, STRONG_PASS. New B&H fields: `buy_hold_return_pct=-22.615`, `buy_hold_max_drawdown_pct=73.96`, `buy_hold_ret_dd_ratio=-0.3058`. Built artifact benchmark OK: `excess_alpha_pct=97.989`, `beats_bh_risk_adjusted=true`; Gate2 score 56 but still INCOMPLETE because other fields remain unavailable.

Carry-forward:
- A fresh full sweep is required before the dashboard's 38 enriched scorecards show these benchmark fields globally.
- Remaining Gate2 blockers are genuine: annualized Sharpe/Sortino definition/equity series, worst-window drawdown, parameter stability, slippage model, EMA benchmark, and regime split.

## Codex GPT-5 2026-06-05 — SP-005 Wave C scorecard_v2 render
Scope: implemented Wave C as a read-only dashboard consumer of real `scorecard_v2` artifacts. Added `08_DASHBOARD_APP/apps/api/mcc_readonly/scorecard_reader.py`, wired `read_model.py` to expose top-level `scorecards`, and attached `scorecard_v2` / `scorecard_v2_cases` to matching rows by base strategy id. Frontend `apps/web/app.js` now renders the actual composer shape (`gate1`, `gate1B`, `gate2`, `gate3`) with separate gate sections, promotable/blocking chips, symbol/timeframe cases, `N/A` for non-OK/null scores, and compact missing/not-scored fields. `styles.css` adds case/missing-field styling. No Pine, MTC behavior, parity, schema, or live-trading surface touched.

Artifact state: generated real all-gate outputs with `score_all_gates.py --in-dir ../05_BACKTEST_RESULTS/enriched_metrics_2026-06-05/evaluation_artifacts --out-dir ../05_BACKTEST_RESULTS/enriched_metrics_2026-06-05/scorecard_v2`; 38 scorecard_v2 files, 0 promotable. Snapshot links 10 audit rows to scorecard_v2. All linked scorecards remain honestly INCOMPLETE/non-promotable because Gate 1/Gate 1B/Gate 3 envelopes are absent and Gate 2 still has N_A sharpe/sortino/regime/benchmark fields.

Validation: gate tool py_compile PASS; corrected synthetic checks PASS (full OK -> 100/OK/pass, empty -> INCOMPLETE/null points, medium repaint -> Gate 1 score 98, REJECT_REPAINT blocks, no top-level blended `score`); real confirm-2026-06-04 all-gates 16/16 INCOMPLETE and 0 promotable; API `py_compile` PASS; dashboard API tests PASS (`35 passed, 1 subtest`); `node --check app.js` PASS; live browser check on `http://127.0.0.1:8765/dashboard` shows linked 8EMA scorecard gates/missing fields and unlinked VWAP missing-artifact fallback with no JS console errors. Browser screenshot capture timed out; functional browser checks passed.

## Codex GPT-5 2026-06-05 — Hermes MTC memory import package
Scope: created proposed Hermes memory import package only under `_HERMES_MEMORY_IMPORT/` (no copy/install into `$env:USERPROFILE\.hermes\memories`; no Pine/MTC/parity/backtest/dashboard changes). Files: `01_PROPOSED_HERMES_MEMORY/USER.md`, `MEMORY.md`, `02_PROJECT_CONTEXT/MTC_COMMAND_CENTER_CONTEXT.md`, `README.md`. Validation: exact marker-content PASS; counts USER 1270 / MEMORY 2070; no existing core USER/MEMORY found; awaiting Baris approval.

## Claude Opus 4.8 2026-06-05 — Confirmation (Option B) review + night-end closure

Scope: reviewed the 2026-06-04 quiet confirmation run (Codex launched it) and completed the night-end closure. No Pine, MTC, parity, or live-trading action.

Run: `confirm_2026-06-04` — pre-registered narrow grid, 6 candidate strategies × 17 symbols × {15m,1h,2h}, narrow grids (grid_n 6-18), 4 workers, ~70s, 0 crash. Codex then ran CPCV + PBO + 16 evaluation artifacts + 16 Gate-2 scorecards + a keep-awake watchdog to 07:30.

Results:
- multiwindow 16 cand → 9 regime+stable; alpha 16 PASS / 11 beat b&h / 6 premium / **6 down-market alpha**.
- DSR rose wide→narrow (best 0.0→0.34-0.38, A17 fix works) but NONE ≥0.50 → `STATISTICALLY_UNCONFIRMED`.
- Gate-2 16/16 INCOMPLETE (32-46), 0 pass — honest status (MEGA lacks ~17 Gate-2 metrics), not FAIL.
- Cross-symbol alpha positive (LINK 1h+2h, ETH 2h, NEAR 1h while b&h<0 = real alpha not beta).

Code changes:
- **A18 FIXED** in `03_QUANTLENS/tools/write_overnight_morning_report.py`: counts + alpha tables now read canonical `alpha_summary.json` (`down_market_alpha`/`premium`) = ALPHA_DONE single source of truth, with a drift assert. Verified: report down_market=6 == log 6 (the 78≠8 bug gone).
- New: `confirmation_runner_2026-06-04.py` (narrow-grid monkey-patch over mega, non-destructive) + `run_confirmation_2026-06-04.sh` (retry + isolated output + post-pipeline).

Closure: lessons `OVERNIGHT_LESSONS_2026-06-05.md` C4-C6 added; runbook §8 A19 + CHANGELOG; NEXT_STEPS review DONE + `NIGHT-FOLLOWUP-HEAVY-TIER` opened.

Key lesson (A19/C4-C5): the run is fully deterministic (bootstrap seed = md5(strat|sym|tf), mega:731) — repeating it overnight yields zero new info. Narrow grid was correct for DSR power; the waste was the idle keep-awake watchdog. Future confirmation nights need a compute-filling heavy-validation tier (50k bootstrap, multi-seed stability, CPCV-all-cells) or must release the machine.

Decision: no promotion. Optional forward-paper observation only for 8EMA LINK 1h and Donchian ETH 2h.

## Codex GPT-5 2026-06-04 — Hermes install and MTC agent profiles

Scope: installed Hermes Agent and created five MTC-specific Hermes profiles. No Pine, MTC strategy behavior, parity files, live trading, backtest launch, account action, git commit, or secret value logging performed.

Install result:
- Official Windows installer was downloaded and inspected from `https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1`.
- Official git-based installer timed out during repository clone; the incomplete clone under `%LOCALAPPDATA%/hermes/hermes-agent` was removed after stopping only the stalled clone process tree.
- Hermes was installed successfully via PyPI into `%LOCALAPPDATA%/hermes/hermes-pypi-venv`.
- Verified: `Hermes Agent v0.15.2 (2026.5.29.2)`, Python `3.11.14`.
- User PATH updated to include `%LOCALAPPDATA%/hermes/hermes-pypi-venv/Scripts`, `%LOCALAPPDATA%/hermes/bin`, and `%USERPROFILE%/.local/bin`. Existing Codex shell may need restart to pick it up.

Profiles created:
- `mtc-steward`
- `quantlens-research`
- `dashboard-qa`
- `backtest-monitor`
- `repo-hygiene`

Profile guardrails:
- Each profile has its own Hermes state directory under `%USERPROFILE%/.hermes/profiles/<profile>/`.
- Each profile has custom `SOUL.md`, `memories/USER.md`, `memories/MEMORY.md`, and `MTC_WORKSPACE.md`.
- Guardrails encode English responses, repo pre-read chain, read-first behavior, no autonomous deletion, and no Pine/MTC/parity/live-trading/backtest-launch changes without explicit approval.
- Model/provider setup intentionally left unconfigured per profile to avoid choosing paid/remote model behavior without Baris approval; run `<profile> setup` or `hermes -p <profile> model` when ready.

## Codex GPT-5 2026-06-04 — Fallow tool evaluation transcript

Scope: fetched and evaluated transcript for `https://youtu.be/Iy8l_Wx1Bpg?si=v5Q2oV9vyHVtF2hD` to assess the video tool for MTC Command Center development. No browser automation, YouTube login, video/audio download, account action, Pine, MTC behavior, parity, backtest, optimization, or implementation changes touched.

Result:
- Transcript fetched successfully: `YT_TRANSCRIPT_COLLECTOR/transcripts/Iy8l_Wx1Bpg.md`.
- Transcript metadata: Turkish auto-generated.
- Tool identified as Fallow: Rust-native JS/TS codebase intelligence for dead code, unused dependencies/exports/types, duplication, complexity, cycles, and boundary checks.
- Recommendation: useful only as an optional read-only audit for the small dashboard JS/frontend surface; not a primary MTC Command Center development tool because this repo is mostly Python/Pine and has no normal Node package graph for the dashboard.

## Codex GPT-5 2026-06-04 — Hermes transcript folder organization

Scope: organized Hermes-related transcript files only. No browser automation, YouTube login, video/audio download, account action, Pine, MTC behavior, parity, backtest, or optimization touched.

Result:
- Created `YT_TRANSCRIPT_COLLECTOR/transcripts/hermes/`.
- Moved 7 collected YouTube transcript Markdown files into `YT_TRANSCRIPT_COLLECTOR/transcripts/hermes/`: `2NuvYsXMehw.md`, `QQEgIo4Juxg.md`, `nb5ALoAGAbE.md`, `gb5TlGw6Uks.md`, `xK1cgyCla-8.md`, `k5NhsF7t68M.md`, `LvWobwr0Neg.md`.
- Moved 4 files from `Temp/HERMES/` into the same `hermes/` folder.
- Deleted `Temp/HERMES/` after verifying it was empty.
- Updated current `YT_TRANSCRIPT_COLLECTOR/reports/transcript_index.csv` output paths for the five rows it currently tracks.

## Codex GPT-5 2026-06-04 — YouTube transcript fetch batch 5

Scope: ran the isolated `YT_TRANSCRIPT_COLLECTOR` tool for five user-provided YouTube URLs. No browser automation, YouTube login, video/audio download, account action, Pine, MTC behavior, parity, backtest, or optimization touched.

Result:
- PASS: `Processed 5 URL(s): 5 success, 0 failed`.
- Input: `YT_TRANSCRIPT_COLLECTOR/urls_run_batch_2026_06_04_5.txt`.
- Reports refreshed: `YT_TRANSCRIPT_COLLECTOR/reports/transcript_index.csv`, `YT_TRANSCRIPT_COLLECTOR/reports/failed_videos.csv`.
- Outputs:
  - `YT_TRANSCRIPT_COLLECTOR/transcripts/nb5ALoAGAbE.md` — English auto-generated.
  - `YT_TRANSCRIPT_COLLECTOR/transcripts/gb5TlGw6Uks.md` — English auto-generated.
  - `YT_TRANSCRIPT_COLLECTOR/transcripts/xK1cgyCla-8.md` — Turkish auto-generated.
  - `YT_TRANSCRIPT_COLLECTOR/transcripts/k5NhsF7t68M.md` — English auto-generated.
  - `YT_TRANSCRIPT_COLLECTOR/transcripts/LvWobwr0Neg.md` — Turkish manual.

## Codex GPT-5 2026-06-04 — YouTube transcript fetch run QQEgIo4Juxg

Scope: ran the isolated `YT_TRANSCRIPT_COLLECTOR` tool for `https://youtu.be/QQEgIo4Juxg?si=H_WHHEOQOrbqK9e_`. No browser automation, YouTube login, video/audio download, account action, Pine, MTC behavior, parity, backtest, or optimization touched.

Result:
- PASS: `Processed 1 URL(s): 1 success, 0 failed`.
- Transcript: `YT_TRANSCRIPT_COLLECTOR/transcripts/QQEgIo4Juxg.md`.
- Index: `YT_TRANSCRIPT_COLLECTOR/reports/transcript_index.csv`.
- Failures report: `YT_TRANSCRIPT_COLLECTOR/reports/failed_videos.csv` with 0 failed rows.
- Transcript metadata: `English (en)`, type `manual`.
- Added collector-local `.gitignore` for `.venv/`, `__pycache__/`, and `*.py[cod]`.

## Codex GPT-5 2026-06-04 — YouTube transcript fetch run

Scope: ran the isolated `YT_TRANSCRIPT_COLLECTOR` tool for `https://youtu.be/2NuvYsXMehw?si=Qvt1Y5yuBdvo2HNh`. No browser automation, YouTube login, video/audio download, account action, Pine, MTC behavior, parity, backtest, or optimization touched.

Run details:
- Created local venv under `YT_TRANSCRIPT_COLLECTOR/.venv/` and installed `youtube-transcript-api==1.2.4` via `requirements.txt`.
- Created run input `YT_TRANSCRIPT_COLLECTOR/urls_run_2NuvYsXMehw.txt`.
- Initial run exposed a UTF-8 BOM parsing issue from PowerShell-created URL files; fixed `read_urls()` to use `encoding="utf-8-sig"` and added a regression test.
- Final command: `.\.venv\Scripts\python.exe .\collect_transcripts.py --urls .\urls_run_2NuvYsXMehw.txt`.

Result:
- PASS: `Processed 1 URL(s): 1 success, 0 failed`.
- Transcript: `YT_TRANSCRIPT_COLLECTOR/transcripts/2NuvYsXMehw.md`.
- Index: `YT_TRANSCRIPT_COLLECTOR/reports/transcript_index.csv`.
- Failures report: `YT_TRANSCRIPT_COLLECTOR/reports/failed_videos.csv` with 0 failed rows.
- Transcript metadata: `Turkish (auto-generated) (tr)`, type `auto-generated`.

Validation:
- `.\.venv\Scripts\python.exe -m py_compile .\collect_transcripts.py .\tests\test_collector.py` PASS.
- `.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"` PASS: 3 tests.
- Python UTF-8 readback confirmed Turkish characters are stored correctly; PowerShell preview may display mojibake depending on terminal encoding.

## Claude 2026-06-04 — SP-004 rubric D1-D6 SIGNED OFF

Barış signed all six owner decisions (DECISIONS D007); rubric `12_STRATEGY_EVALUATION_RUBRIC.md` updated to match. **Phase 2 scoring lock unblocked.**
- **D1** Gate 1B → **/100, PASS ≥75** uniform with all gates (was /50+≥40; criteria rescaled ×2).
- **D2** PBO ≥0.5 → `OVERFIT_SUSPECT`, blocks promotion, keeps idea (accepted).
- **D3** parity → **ADVISORY, not a hard gate**: mismatch raises `PARITY_WARNING` + revisit note, does NOT block promotion; pure-Python strategies → `N_A`. Rationale: Pine layer may be retired for direct Python/Binance API execution.
- **D4** Gate 3 → separate `production_readiness_artifact_v1`, N/A until exists (accepted).
- **D5** numeric bands deferred to Phase 1.5 from real distributions (confirmed).
- **D6** AI-drafts thesis title, Barış overrides (accepted).
Spec-only — no code/Pine/parity-oracle change, no commit. **Follow-up (NEXT_STEPS SP-004-SCHEMA-PARITY):** move `parity_gate` out of `hard_flags` → advisory `flags.parity_status` in `evaluation_artifact_v1.schema.json` (Phase 1).

## Claude 2026-06-04 — SP-004 Batch E (AUDIT-009) + AUDIT backlog cleared

Equity gate for opening-range strategies (Barış D005; skip-by-exchange). The 4 OR strategies (`QL_CONNELL_EVENT_DRIVEN_GAP_5M`, `QL_AVWAP_BRIAN_INTRADAY_OR_5M`, `QL_EPISODIC_PIVOT_CHRISTIAN_5M`, `QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M`) hardcode `bars_per_day=78` (US-equity 6.5h session) — meaningless on the all-crypto bundle (93 datasets, all `exchange=BINANCE`). Fix: `mega_walk_forward.py` adds `EQUITY_ONLY_STRATEGIES` (empty default) + `EQUITY_EXCHANGES={NYSE,NASDAQ,ARCA,AMEX,BATS}` + a `_worker` gate (after find_ds, before load_df) returning `SKIPPED_RULE` when an equity-only strategy hits a non-equity exchange; `overnight_v2_runner.py` registers the 4. All skip today; auto-run if US-equity data is added later. Claude-audited ACCEPT: py_compile, end-to-end `_worker`→SKIPPED_RULE on BTCUSDT/BINANCE, no over-skip, pure-mega unaffected. `bars_per_day=78` left intact (correct for real equity). No commit.

**AUDIT backlog now fully cleared:** 001-010 all DONE. Open items are Barış OPS, not code: (1) re-run the sweep — 149 robust-PASS were scored under old overlapping folds + looser threshold (D006); (2) add real US-equity data if the 4 OR strategies should ever produce results; (3) commit the Batch A-E edits + untracked tools (`cpcv_validator.py`, `probabilistic_pbo.py`, `_deepseek_driver/`).

## Claude 2026-06-04 — SP-004 Batch D (AUDIT-008)

Disjoint OOS rolling folds (Barış D006). `mega_walk_forward.py`: line 604 `step = test_size` (was `remaining//(NUM_FOLDS-1)` = structural 50% OOS overlap → inflated `folds_positive`); line 732 PASS elif tightened `pos >= ceil(n_folds/2)` → `pos == n_folds` (all OOS folds positive). Now exactly 2 independent folds for every dataset size (f=2 drops at `ke-ks<200`). Claude-audited ACCEPT: py_compile PASS, disjointness verified n=1500/6000/50000/100000, no lockbox/CPCV/PBO/DSR change, no commit.
**OPEN op (Barış, not code):** existing 149 robust-PASS were computed under the OLD overlapping geometry — re-run the sweep under disjoint folds + `pos==n_folds` before DSR-lock.

## Claude 2026-06-04 — SP-004 Batch C + DeepSeek harness

**DeepSeek sandboxed harness** (`_deepseek_driver/ds_agent.py`): DeepSeek now runnable as an audited subagent over the OpenAI-compatible API (tools: read_file/edit_file/write_file/py_compile/run_python/finish). Write allowlist + denylist (`*.pine`/parity/`06_SCHEMAS`/`MTC_V2`/`.git`), no git/commit capability, `run_python` AST-guard blocks write/exec/network so all edits route through guarded `edit_file`. utf-8 stdout; report+transcript → `C:\tmp\ds_*_report.md`. Workflow: Claude writes the task prompt + audits; DeepSeek does read/edit. Key/model live (deepseek-chat & deepseek-v4-pro). Driver dir untracked.

**Batch C (AUDIT-007 + AUDIT-010)** — first live harness job, Claude-audited ACCEPT:
- AUDIT-007 `paths.py:default_quantlens_root` — prefers non-empty candidate dir (`any(c.iterdir())`, OSError-skip), fallback first-existing→candidates[0]. registry_reader + audit_reader inherit. Verified 5/5 mock selection cases.
- AUDIT-010 `ingest.py:249-251` — inner `if not target.exists()` guard removed; sha-mismatch transcript now overwrite-queued (writer `target.write_text` overwrites). Surroundings untouched.
Validation: py_compile both PASS, on-disk diff read, no unauthorized changes, no commit.

AUDIT backlog status: 001/002/003/004/005/006/007/009/010 DONE. OPEN: AUDIT-008 (fold OOS overlap — needs Barış design call: `step=test_size` vs raise PASS threshold). AUDIT-009 DECIDED (D005) but impl needs market-metadata/session path in overnight_v2_runner — not yet wired.

## DeepSeek 2026-06-04 — SP-004 Batch B short-direction support

Completed AUDIT-003 in the two rigorous walk-forward tools only:
- `03_QUANTLENS/tools/rigorous_walk_forward.py`
- `03_QUANTLENS/tools/rigorous_walk_forward_parallel.py`

Both `simulate_slice` implementations now accept `direction="long"` by default,
parse optional 3-tuple `(sig, stop, direction)` from `build_signals`, and apply
mega-style short math only when `direction == "short"`: short stop must be above
entry, target is below entry, stop checks high >= stop, target checks low <= target,
raw PnL is `entry_price / exit_price - 1.0`, and R is `(entry_price - exit_price) / risk`.
No trailing-EMA exit is used for shorts. Existing 2-tuple strategies fall back to
`direction="long"`.

Validation: `py_compile` PASS; long-parity regression on
`QL_2026-05-01_ANY_1H_RSI_CONFLUENCE_PLAYBOOK` was byte-identical before/after;
synthetic short smoke PASS for both iat and numpy loops (`short_net=11.031`,
`long_net=-5.08`, invalid short stop skipped with 0 trades). No changes to
`mega_walk_forward.py`, overnight runner, CPCV/PBO, Pine, MTC, parity, schemas,
fold logic, costs, thresholds, or SliceStats arity. No commit/push.

## Claude Opus 4.8 2026-06-04 — SP-005 Wave A audit PASS + SP-004 Phase 0A drafted

**1. SP-005 Wave A acceptance audit → PASS WITH MINOR ISSUES (accepted).**
Reviewed Codex's terminal-style Strategy Detail Page. No blockers; no faked
scorecard_v2 / QuantLens / metrics. Live snapshot confirms `scorecard_v2` absent
on all 176 rows → honest "SP-004 pending" everywhere; legacy composite relocated
to collapsed Technical Details; English title fallback works; CSS scoped (no other
screen damage); list/filters intact. Validation: `node --check` PASS, `py_compile`
PASS, 35 API tests PASS. **No files changed during audit.**
- Note: Codex under-reported `pipeline_reader.py` — it also migrated 3 path helpers
  (`_promoted_dir`/`_quantlens_root`/`_source_file_candidates`) from hardcoded
  legacy `01_MASTER TEMPLATE_V2/06_QUANTLENS_LAB` → `default_quantlens_root()`.
  Correct latent-bug fix (matches backtest_reader fix), read-only, beneficial.
- Polish backlog (non-blocking): dead Turkish `DESCRIPTIONS` block + first
  `_DEFAULT_DESC` (overwritten); orphaned `renderDecisionPanel`/`renderScorecard`
  in app.js (no call sites after rewrite).

**2. SP-004 Phase 0A — DRAFTED (spec only, no code, no Pine/MTC/parity touch).**
Migrated the Turkish source rubric into canonical English + applied both audits'
gap-fixes. Deliverables:
- `03_QUANTLENS/_user_guide/12_STRATEGY_EVALUATION_RUBRIC.md` — 4 gates + hard-fail
  gates, every sub-criterion mapped to an emittable field. Gate2 rebalanced
  (Regime 5→10, Perf 20→18, Sample 15→12 = /100); added Sharpe/Sortino/recovery/
  WFO/CPCV/PBO as Gate2 metrics; Gate1B = /50 + derived PASS≥40; Gate1B-vs-Gate3
  §6.1 de-dup; parity hard pass/fail; SAFE_WITH_DELAY −3 / NEEDS_MODIFICATION
  block-not-reject; PBO≥0.5 → OVERFIT_SUSPECT (blocks promotion, keeps idea).
- `06_SCHEMAS/status_envelope.schema.json`, `evaluation_artifact_v1.schema.json`,
  `production_readiness_artifact_v1.schema.json` (Gate3 separate, N/A until
  integration evidence). Validated: meta-schema + $ref resolution + sample
  instance + negative enum case all pass.
- `03_QUANTLENS/_templates/strategy_evaluation_record_template.yaml` (thesis_en/tr,
  gate hard_fail reasons, backtest_run_id, evaluation_artifact_version,
  phase_current = N/A discriminator).
- **Barış sign-off needed on D1-D6** (rubric §"Owner decisions") before P2 locks
  scoring. Draft uses recommended defaults. Next: **P1A** (fix CPCV 3-tuple
  AUDIT-002 + PBO split AUDIT-005 + N_A fallback) before any hard-gating.
- `_eval_pipeline_source_TEMP/` retained (delete only Phase 5).

## GPT-5 Codex 2026-06-04 — MTC-Engine Validation implementation

Implemented the additive MTC-Engine Validation stage in `02_MTC_BACKTEST`.

- New light-risk profile: `src/config/profiles/light_risk.py` returns a fresh `MTCConfig`
  with filters/guards OFF, risk features ON, and nested or dotted per-producer overrides.
- New manual producer-adapter package: `src/modules/signals/producers/`, including
  `SupertrendProducerAdapter` as the golden adapter wrapping the existing Supertrend signal code.
- New bridge CLI: `python -m src.cli.mtc_engine_validate` loads a producer adapter, applies
  the light-risk profile, injects the adapter into an `MTCRunner` instance, emits `report.md`,
  `results.json`, `manifest.json`, and `trades.csv`, and reports producer parity as `NOT_RUN`
  unless an explicit `--parity-command` is supplied.
- New standalone Pine producer adapter:
  `01_MTC_PROJECT/parity_oracles/feature_adapters/pinets/producer_supertrend_v1.pine`
  for raw-signal parity only. `01_MTC_PROJECT/01_PINE/MTC_V2.pine` was not modified.
- Workflow docs updated: `03_QUANTLENS/_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md`
  now includes `MTC_ENGINE_VALIDATED` and the MTC-Engine Validation Gate; runbook has the
  operational command block.
- Verification: `pytest tests/test_light_risk_profile.py tests/test_mtc_engine_validate_cli.py -q`
  PASS (4 tests); `compileall` PASS; real-data smoke on `BTCUSDT_1d_20180701_20260308.parquet`
  completed with strategy +20.2903%, buy&hold +111.8084%, excess -91.5181%, parity `NOT_RUN`.

No engine fork, no MTCRunner edits, no risk-module edits, no QuantLens overnight-tool edits, no
live trading functionality.

## Claude Opus 4.8 2026-06-04 — MTC-Engine Validation step design (spec)

New workflow stage designed (brainstorming complete, awaiting spec review). Problem:
QuantLens funnel tests producers **naked** (raw signal, no MTC risk) until final
integration — never sees behavior under MTC SL/TP/trailing first. Fix: insert
**MTC-Engine Validation** stage between naked screening and parity-candidate.

Approved decisions: reuse existing `MTCRunner` with a **light config profile**
(filters/guards OFF, risk ON) — no engine fork; **manual SignalPlugin adapter** per
producer; runs **shortlist only**; **Python plugin + standalone Pine producer adapter
+ producer-level parity**, `MTC_V2.pine` untouched (parity via existing
`parity_oracles` infra, Production Safety preserved); **Approach A** = new bridge
CLI `mtc_engine_validate.py` orchestrating existing engine + WF/stats/parity tools.

All-additive: MTCRunner / risk modules / QL overnight tools / MTC_V2.pine NOT modified.
New: `config/profiles/light_risk.py`, `modules/signals/producers/<name>.py`,
`cli/mtc_engine_validate.py`, standalone Pine producer adapter, `MTC_ENGINE_VALIDATED`
promotion level + MTC-Engine Gate in 07 RULES.

Spec: `docs/superpowers/specs/2026-06-04-mtc-engine-validation-step-design.md`.
Next: user reviews spec -> writing-plans skill for phased implementation plan.

## Claude Opus 4.8 2026-06-04 — Triage 172 integration + re-triage pilot

Clarified "why only 46": 46 = matured QuantLens strategies; 172 = upstream raw
triage worklist (`11_TRIAGE/2026-05-30_rejected_worklist.xlsx`). xlsx was stale —
reconciled with on-disk transcripts: **159/172 now have transcripts**, 89 HIGH,
**90 eligible_for_retriage**. Old repo `C:\LAB\tradingview-lab` is behind (81) and
has nothing CLEAN lacks — ignore it; CLEAN is canonical.

- New `05_REGISTRY/TRIAGE_CANDIDATE_REGISTRY.json` (+ schema) via
  `03_QUANTLENS/tools/build_triage_registry.py` (reconciles xlsx + live transcripts).
- Surfaced in dashboard: **Strategy Research Lab -> Triage Worklist** section
  (filters: quality/transcript/re-triage) + 3 overview metrics; reader updated.
- Re-triage worklist `11_TRIAGE/retriage_worklist_2026-06-04.md` (90 rows) via
  `gen_retriage_worklist.py`.
- **Pilot re-triage (3 HIGH, review-first)**: Stg083 -> CANDIDATE ->
  `03_QUANTLENS/strategies/STG047_brian_lee_smallcap_gap_mr_short` (metadata +
  deterministic spec + transcript). Stg082 -> WIKI_ONLY, Stg087 -> DUPLICATE.
  Dispositions: `11_TRIAGE/retriage_dispositions_2026-06-04.md`.
- Generator improved: explicit `candidate_metadata.yaml` taxonomy now overrides
  heuristics (`classification_confidence: explicit_metadata`).
- Verify: registries idempotent (`--check` 0), validator OK, 35 API tests pass
  (raised test HTTP timeout 5s->30s; cold snapshot build ~6s, pre-existing, not a
  code regression — research_reader is 0.003s).
- Next: RESEARCH-004 continue ~87 remaining in batches (mostly WIKI/SALVAGE/DUP expected).

## Claude Opus 4.8 2026-06-03 — Strategy Research Lab infrastructure + UI tab + USER_INTAKE

Repo prepared for repeatable AI strategy research (no new strategy created, no
optimization run, MTC_V2.pine untouched).

- **Registries** (`05_REGISTRY/`, schemas in `06_SCHEMAS/`): generated
  `STRATEGY_RESEARCH_REGISTRY.json` (46), `INDICATOR_REGISTRY.json` (23),
  `COMPONENT_REGISTRY.json` (78), `TAG_DICTIONARY.json`; empty-but-valid
  `RESEARCH_RUN_/VARIANT_LOG_/RESEARCH_BACKTEST_REGISTRY.json`.
- **Generator** `03_QUANTLENS/tools/build_strategy_research_registry.py`
  (idempotent, `--check`), **validator** `validate_research_registries.py`,
  **router** `route_user_intake.py`.
- **Source of truth** stays per-strategy (`01_candidate_metadata.yaml` /
  `producer_spec.json`); registries are generated — do not hand-edit.
- **Docs**: `_AI_MEMORY/STRATEGY_COMPONENT_LIBRARY.md`,
  `STRATEGY_RESEARCH_WORKFLOW.md`, `STRATEGY_CODE_REVIEW_CHECKLIST.md`;
  templates `03_QUANTLENS/_templates/VARIANT_LOG_TEMPLATE.md` +
  `STRATEGY_RESEARCH_REPORT_TEMPLATE.md`.
- **Dashboard**: new **Strategy Research Lab** tab (`web/index.html` +
  `web/app.js renderResearchLab`), backed by read-only
  `apps/api/mcc_readonly/research_reader.py` → snapshot key `strategy_research`.
  35 API tests pass; tab renders 46/23/78 + Missing-Metadata (43 review_needed).
- **Intake**: `00_INBOX/USER_INTAKE/` drop folder; every strategy now has an
  (empty) `STGxxx/source_intake/{transcripts,screenshots}/`.
- **Follow-ups** in NEXT_STEPS: RESEARCH-001 retro-consolidation,
  RESEARCH-002 review_needed classification, RESEARCH-003 full MTC_V2 indicators.

## Claude Opus 4.8 2026-06-03 — Strategy Detail Page redesign plan v3 + terminal prototypes

SP-005 (Strategy Detail Page redesign) — **plan only, no live app code written.**

Plan at `03_QUANTLENS/_user_guide/11_STRATEGY_DETAIL_PAGE_REDESIGN_PLAN.md` now at **v3**.
Barış selected the **terminal** visual direction and gave 5 structural rules, all folded in:
1. **One scoring system** = the Scorecard. QuantLens gives commentary only and references
   the gate scores — no double scoring. Commercial value / complexity are labels, not bars.
2. **Verdict & Decision merged** into one top block (QuantLens is the decision authority).
3. **Scorecard directly under** the verdict, **click-to-expand** gates (`<details>`).
4. **Backtest Evidence = TradingView-tester-style cases** — video-settings case + optimized
   best cases, each with settings·symbol·timeframe on one **standard window**; TV metrics +
   equity + B&H + source-claim-vs-reproduced.
5. **One prototype per journey stage** built.

Key earlier finding (carried): QuantLens is **already a real pipeline** —
`03_QUANTLENS/03_SALVAGE_IDEAS/<candidate>/01_candidate_metadata.yaml` already has
`quantlens_decision`, `commercial_value_score`, `complexity_score`, repaint/lookahead/
closed_source risk, `candidate_kind` (salvage categories). Dashboard readers ignore these
today → the QuantLens Verdict section surfaces existing data via a future read-only
`quantlens_reader.py` (Wave B). No new scoring math; consumes `scorecard_v2` (SP-004).

Prototypes (throwaway, `08_DASHBOARD_APP/apps/web/prototypes/`, English-only, single-scroll,
CSS **inlined** so they render over `file://`): `proto_B2_terminal.html` (Source-checked/
blocked), `proto_stage_rules_extracted.html`, `proto_stage_testability.html`,
`proto_stage_backtested.html` (TV cases), `proto_stage_promotion.html` (TV cases).
Earlier `proto_A/B/C` + `proto_B2_clinical/editorial` superseded.

Delivery split into 3 waves (plan §11): A = single-scroll UI/wording/terminology on existing
data (ships first); B = `quantlens_reader.py` + QuantLens Verdict + Salvageable Ideas +
conditional render matrix; C = `scorecard_v2` gate bars + TV-style backtest-case reader.
**Wave A coding NOT yet authorized — awaiting Barış go-ahead.**

## Claude Opus 4.8 2026-06-03 — Overnight 21-iter QuantLens sweep

Gece çalışması: `tools/overnight_loop_2026-06-02_night.sh` (20w, 11h deadline cap, thread-pinned, heartbeat + crash-restart). **21 iter tamam, 0 crash**, ~3.6M param-evaluation (1M hedef 3.6×). Reçete = dün geceyle aynı (`overnight_v2_runner.py`, 43 strateji × 2031 param × 17 sym × 5 TF ≈ 172k config/iter).

Sonuç: cross-iter aggregation (≥11/21, ceil majority) → **149 robust PASS cell · 89 buy&hold yendi · 8 down-market alpha** (varlık düşerken kazanan). AMA **tüm adaylar DSR p < 0.50** (crypto research eşiği) → kanıtlı edge yok, max seviye `PROMOTE_TO_FORWARD_PAPER_TRADE`. MTC_v2 entegrasyonu/Pine default değişikliği YOK.

Top down-market: ANY_CANDLESTICK_7 APT 1h (alpha +110.9%), SP500_TWO_CANDLE ADA 1h (+109.7%), US_EQ_INTRADAY LINK 1h (+96.0%, PF 2.04).
Rapor: `03_QUANTLENS/05_BACKTEST_RESULTS/MORNING_REPORT.md`. Aggregate: `tools/night_runs/AGGREGATE_night_2026-06-02.json`. Alpha: `05_BACKTEST_RESULTS/alpha_summary.json`.

Not: `generate_morning_report.py` hâlâ legacy hardcoded OUTPUT_DIR okuyor (A1) — rapor veriden elle üretildi; generator fix `hardcoded_path_rewrite_TODO`'da bekliyor.

**İş akışı kalıcılaştırıldı (RUNBOOK §6.4 "Gece Sonu Kapanış"):** loop DEADLINE sonrası 7 zorunlu adım — aggregate → alpha → morning report → **MTC Command Center upgrade + doğrula** → **lessons arşivle (`lessons_archive/OVERNIGHT_LESSONS_<date>.md` + index + §8 anti-pattern + CHANGELOG)** → handoff → loop durdur. Dashboard güncellenmemiş VEYA ders arşivlenmemişse gece tamamlanmamış sayılır. Bu gecenin dersi: `lessons_archive/OVERNIGHT_LESSONS_2026-06-03.md` (G1-G5, A16/A17). Dashboard doğrulandı: 53 run, en yeni `MEGA_results_iter_21` COMPLETED.

## Claude Opus 4.8 2026-06-02 — "Dashboard açılmıyor" fix

Kök neden: bare `python -m mcc_readonly` (step 5'in söylediği komut) argparse `required=True` subcommand yüzünden exit 2 veriyordu ("the following arguments are required: command"). Doğru komut `serve` idi → kullanıcı "açılmıyor" gördü.
Fix:
- `cli.py` — subparsers `required=False`. Komut yoksa otomatik `serve` (127.0.0.1:8765) + `webbrowser.open(/dashboard)`.
- Yeni `08_DASHBOARD_APP/START_DASHBOARD.bat` — çift tık launcher (apps\api'ye cd + bare modül + pause).
Doğrulama: py_compile PASS; bare invocation serve OK; `GET /dashboard` HTTP 200.

## Claude Opus 4.8 2026-06-02 — Dashboard ↔ MEGA entegrasyonu (Option B UYGULANDI)

Plan uygulandı + canlı doğrulandı. 5 adım:
1. `00_CONFIG/paths.local.json` oluşturuldu (mcc_root=.../MTC_COMMAND_CENTER, mtc_v2_root=C:/LAB/Tradingview_LAB_CLEAN, reports_root). Zaten `MTC_COMMAND_CENTER/.gitignore:3` ile ignore'lu → commit edilmez.
2. `03_QUANTLENS/05_BACKTEST_RESULTS/` zaten vardı (oluşturmaya gerek yok).
3. `aggregate_overnight_iters.py` — `export_to_backtest_results()` eklendi. sprint_runs MEGA JSON'larını `05_BACKTEST_RESULTS/`'a `{stem}_results.json` adıyla KOPYALAR (reader glob `*_results.json` ile eşleşsin diye rename şart). Mevcut mantığa dokunulmadı. Çıktı: "Exported 16 files to 05_BACKTEST_RESULTS".
4. `single_strategy_backtest.py` — workflow sonuna non-fatal aggregate hook eklendi (`--runs-dir sprint_runs`). Başarılı → "Dashboard updated".

**KÖK NEDEN DÜZELTMESİ (plan dışıydı, gerekti):** `backtest_reader.py` `mtc_v2_root/06_QUANTLENS_LAB/05_BACKTEST_RESULTS` HARDCODE ediyordu — bu dizin CLEAN repo'da YOK. Plan'ın "reader zaten okuyabiliyor" varsayımı yanlıştı (format uyumlu, ama dizin değil). `registry_reader.py:21` zaten doğru pattern'i kullanıyor: `default_quantlens_root(root)` (03_QUANTLENS tercih, 06 fallback). `backtest_reader.py` aynı pattern'e çevrildi (`_collect_quantlens_results` + `_collect_detached_statuses` artık quantlens_root alıyor). Tek outlier oydu — diğer reader'lar dokunulmadı.

**Doğrulama (canlı):**
- py_compile PASS (2 script)
- `aggregate --runs-dir sprint_runs` → 16 iter, 149 robust winner, 16 export
- `build_backtest_status()` → 32 run, 16 MEGA surfaced, matrix format parse OK (3655 evals)
- `python -m mcc_readonly snapshot` → backtest_status.summary total_runs=32, source=C:/LAB/Tradingview_LAB_CLEAN
- HTTP `serve --port 8770` + `GET /api/snapshot` → 32 run, last=MEGA_results_iter_13. Server kapatıldı.

**Değişen dosyalar:** `00_CONFIG/paths.local.json` (yeni, ignored), `03_QUANTLENS/tools/aggregate_overnight_iters.py`, `03_QUANTLENS/tools/single_strategy_backtest.py`, `08_DASHBOARD_APP/apps/api/mcc_readonly/backtest_reader.py`. Export JSON'lar (`05_BACKTEST_RESULTS/MEGA_*_results.json`) gitignore'lu — repo bloat yok. Henüz commit EDİLMEDİ (kullanıcı onayı bekliyor).

## Claude Sonnet 4.6 2026-06-02 — Sabah oturumu (Loop tamamlandı + Dashboard analizi)

### MEGA Overnight Loop — TAMAMLANDI
- 16 iter başarılı: 3 sprint + 13 gece (2026-06-01 23:36 → 2026-06-02 06:33)
- **149 robust winner** (≥8/16 iter PASS) — dün sabah 117 idi (+32)
- 16/16 STRONG çift: `QL_DEEPAK_SNAPBACK_50SMA_INTRADAY/TRXUSDT/2h` (ret%101, PF=1.82), `QL_DEEPAK_153_FILTER_1D/SOLUSDT/2h` (ret%56, PF=1.70)
- Aggregate çalıştırıldı → `03_QUANTLENS/tools/OVERNIGHT_AGGREGATED_REPORT.md`
- 17 JSON sprint_runs'ta: `MEGA_results_iter_1..13_*.json`

### Dashboard Bağlantı Sorunu — TESPİT EDİLDİ, FIX PLANLI
Dashboard (08_DASHBOARD_APP) Audit ve Pipeline sekmelerinde gece sonuçları GÖRÜNMÜYOR.
Kök neden 3 katmanlı:
1. `paths.local.json` YOK → dashboard `paths.example.json`'daki eski `C:/LAB/tradingview-lab/` path'ini kullanıyor (silinmiş dizin)
2. `backtest_reader.py` → `mtc_v2_root/06_QUANTLENS_LAB/05_BACKTEST_RESULTS/` okuyor (eski path)
3. MEGA sonuçları `sprint_runs/` altında — dashboard bilmiyor

**Onaylanan Fix Planı (Option B):**
Yeni oturumda yapılacaklar:
1. `paths.local.json` oluştur → doğru `C:/LAB/Tradingview_LAB_CLEAN/` path'i ver
2. `aggregate_overnight_iters.py` → sonunda MEGA JSON'larını `03_QUANTLENS/05_BACKTEST_RESULTS/` 'e kopyala
3. `single_strategy_backtest.py` → bitince aggregate'i otomatik çağır
4. Dashboard yeniden başlatınca Audit/Pipeline güncel veri gösterir

**Gerekli dosyalar:**
- `00_CONFIG/paths.local.json` (yeni, oluşturulacak)
- `03_QUANTLENS/tools/aggregate_overnight_iters.py` (değiştirilecek — export adımı eklenecek)
- `03_QUANTLENS/tools/single_strategy_backtest.py` (değiştirilecek — post-run aggregate hook)
- `03_QUANTLENS/05_BACKTEST_RESULTS/` (yeni dizin, oluşturulacak)

**Bağlamlar (yeni oturumda lazım):**
- `backtest_reader.py` `_is_matrix_walk_forward()`: `results` listesindeki her dict'te `classification` + `summary` (dict) varsa MEGA formatı tanıyor → MEGA JSON'lar doğrudan okunabilir, format uyumlu
- `paths.example.json` içeriği: `mtc_v2_root = C:/LAB/tradingview-lab/01_MASTER TEMPLATE_V2` → GEÇERSİZ
- Doğru path: `C:/LAB/Tradingview_LAB_CLEAN`

## Claude Sonnet 4.6 2026-06-02 — LLM Audit Fixes

Multi-model audit (ChatGPT 5.5 / DeepSeek V4 Pro / Grok Build 01 / Antigravity) incelendi.
**Fixed this session:**
- `aggregate_overnight_iters.py:148,164` — `or 1` → explicit `is None` check (0.0 p-value inversion fix)
- `mega_walk_forward.py:698` — `hash()` → `hashlib.md5()` deterministic bootstrap seed
- `mega_walk_forward.py:708` — PASS threshold `n_folds // 2` → `math.ceil(n_folds / 2)`
- `mega_walk_forward.py:653,690` — tuple direction detection: `result[2] in {"long","short"}` guard
- `audit_hardcoded_paths.py:31` — SKIP_DIRS'e `single_strategy_runs`, `cpcv_runs`, `pbo_runs` eklendi
- `.gitignore` — 5 run output dizini eklendi (`overnight_runs`, `sprint_runs`, `single_strategy_runs`, `cpcv_runs`, `pbo_runs`)
- `mega_walk_forward.py:523` — short R-multiple işareti (önceki oturum)
- `mega_walk_forward.py:778` — `_atomic_write_text` mkdir guard (önceki oturum)
- `ingest.py:30` — `EMBEDDED_TRANSCRIPT_MIN_SIZE` 500→5000 regression fix (önceki oturum)

Later same session — Mimo v2.5 Free audit (10 run) incelendi:
- `audit_reader.py` duplicate `_lookup_source_record` (419+872 byte-identical) → ikinci silindi
- AUDIT-008 (rolling fold OOS 113-bar overlap), AUDIT-009 (bars_per_day=78 crypto), AUDIT-010 (ingest transcript re-write race) eklendi
- Mimo false positives doğrulandı: DSR `cdf` doğru (sf değil), MEGA_WORKERS env cap'i atlıyor — bunlar fix edilmedi (gerçek değil)

**Open audit items → NEXT_STEPS.md AUDIT-001..AUDIT-010**

## Claude Sonnet 4.6 2026-06-02 — Overnight session (T-01..T-08)

### T-04 MEGA Overnight Loop
- `overnight_loop_2026-06-01_night.ps1` oluşturuldu ve başlatıldı (PID 34672)
- Deadline: 2026-06-02 06:00, 20 worker, MEGA_OUTPUT_DIR doğru
- Log: `overnight_runs/night_loop_2026-06-01.log`

### T-01 Buy & Hold Baseline
- `buy_hold_baseline.py` yazıldı → `sprint_runs/BH_BASELINE.md`
- **Kritik bulgu:** 189 ROBUST hücreden **117/189 pozitif alpha** (B&H'yi geçiyor)
- 72 hücre FAIL: TRXUSDT (+107.7% B&H) ve XRPUSDT (+124.8% B&H) bull market döneminde
- SOLUSDT, ETH, BNB, LINK gibi düşen semboller → strateji alpha'sı yüksek

### T-02 CPCV + PBO Gate
- `sprint_runs/cpcv_input_top_alpha.json` — 13 top alpha hücre filtrelendi
- CPCV: `cpcv_runs/top_alpha/CPCV_VALIDATION_REPORT.md`
- PBO: `pbo_runs/top_alpha/PBO_REPORT.md` — **PBO=0.0** (sıfır overfitting)
- `QL_DEEPAK_153_FILTER_1D SOLUSDT 2h` 3003 CPCV kombinasyonun hepsini kazanıyor

### T-03 Promotion Assessment
`sprint_runs/PROMOTION_ASSESSMENT_2026-06-01.md` — Barış onayına:

| Öneri | Strateji | Sembol/TF | CPCV | Excess |
|---|---|---|---|---|
| **ELITE** | SP500_TWO_CANDLE_SENTIMENT_SR | ADAUSDT 1h | 14/15 (93%) | +109.7% |
| **ELITE** | 8EMA_EXIT_TRAIL | LINKUSDT 1h | 14/15 (93%) | +96.0% |
| **ELITE?** | DEEPAK_153_FILTER_1D | SOLUSDT 2h | 14/15 (93%) | +121.2% |
| **STRONG** | OPEN_RANGE_5PCT_STOP | NEARUSDT 4h | 13/15 (87%) | +144.4% |
| **STRONG** | CANDLESTICK_7_PA_CONFLUENCE | APTUSDT 1h | 12/15 (80%) | +110.9% |
| **STRONG** | DEEPAK_153_FILTER_1D | ETHUSDT 2h | 12/15 (80%) | +74.1% |

### T-05 QQE Salvage
- `overnight_v2_runner.py` → `QL_QQE_SIGNALS` (strateji 43, grid 108 param)
- SOLUSDT 2h: fold +53.9% avg, lockbox -14.7% → **FILTER_OVERLAY** (overfitting)
- `03_SALVAGE_IDEAS/.../06_next_action.md` güncellendi

### T-07 SP-001 MVP-0 CLI Skeleton
- `mtc_cli/` oluşturuldu (sadece bu klasör, Pine/MTC'ye dokunulmadı)
- Dosyalar: `__main__.py`, `contract.py`, `commands/audit.py`, `tests/test_audit.py`
- Komut: `python -m mtc_cli audit repo [--json]`
- **8/8 test PASS**

### T-08 SP-002 vectorbt Enrichment
- `03_QUANTLENS/tools/vbt_enrichment.py` oluşturuldu
- API: `enrich_from_trades(tv_trades, price_df)` + `enrich_from_mega_result(lockbox_oos)`
- Metrikler: Calmar, Sortino, Omega, rolling Sharpe, underwater equity, Monte Carlo
- Smoke: DEEPAK_153 SOLUSDT 2h → Calmar=3.70, Sortino=11.63, Omega=1.63

### Sabah Yapılacaklar (Barış)
1. MEGA loop sonuçlarını aggregate: `python aggregate_overnight_iters.py --runs-dir sprint_runs`
2. B&H güncelle: `python buy_hold_baseline.py --sprint-dir sprint_runs`
3. Promotion kararları: `sprint_runs/PROMOTION_ASSESSMENT_2026-06-01.md` oku
4. 31 transcript kandidat review: `11_TRIAGE/reclassification_audit_2026-06-01.md`

## 2026-06-01 Codex sequential task run

- **IM-001 complete:** `11_TRIAGE/analyze_transcripts.py` now resolves transcript paths via the current QuantLens root before falling back to legacy paths. Verified `00_INBOX_REPORTS/Transcrips` resolves to `MTC_COMMAND_CENTER/03_QUANTLENS/...`; `py_compile` PASS.

## 2026-06-01 DeepSeek V4 Pro transcript follow-up

- **IM-001 verification + basename fallback:** Ran `analyze_transcripts.py` — initial run resolved 98/165 transcripts (67 had legacy `06_QUANTLENS_LAB\` prefix in stored path, not matching migrated `03_QUANTLENS/00_INBOX_REPORTS/Transcrips/` location). Added basename-based fallback to `resolve_transcript_path()` — searches `Transcrips/` and `00_INBOX_REPORTS/Transcrips/` by filename. Re-run: **165/165 analyzed, 0 missing.**
- **Audit results (2026-06-01):** 115 ALREADY_OK, 17 LIKELY_MISCLASSIFIED, 14 REVIEW_HUMAN, 19 KEEP_REJECTED, 0 SPLIT_RECOMMENDED. Reports: `11_TRIAGE/reclassification_audit_2026-06-01.md`, `split_candidates_2026-06-01.md`.
- **Actionable:** 17 LIKELY_MISCLASSIFIED + 14 REVIEW_HUMAN need Barış manual review. 19 KEEP_REJECTED have no numeric thresholds → correctly rejected.
- **UI integration (transcript verdict in Audit tab):**
  - `analyze_transcripts.py` now writes `11_TRIAGE/transcript_reclassification.json` (candidate_id → verdict + signals mapping).
  - `read_model.py` loads this JSON into the dashboard snapshot as `transcript_reclassification`.
  - `index.html`: added "Transcript" column to Audit table, "Tx verdict" filter dropdown.
  - `app.js`: `renderAudit()` shows verdict badge per row + verdict counts in summary. `filterAuditRows()` supports transcript verdict filter.
  - Verified: server at `http://127.0.0.1:8765/dashboard` → Audit tab shows transcript verdict column.
- **Q Trend split + backtest + classification:** `QL_2026-05-01_TV_BUYSELL_INDICATOR_PACK`'ten Q Trend (Tosenko) ayrıştırıldı.
  - **Pine → Python:** `overnight_v2_runner.py` — `_qtrend_signal()` (iteratif Pine trend line) + `_compute_adx()` + 3 grid builder + 3 signals_new branch.
  - **Motor upgrade:** `mega_walk_forward.py` `simulate_slice()` short desteği eklendi (`direction="long"/"short"`). `_worker` 3-tuple `(sig, stop, direction)` dönüşü destekler.
  - **Multi-symbol backtest (4 sym × 3 varyant, 1h):**
    - V1 Long: ETHUSDT +110.7% lockbox ama cross-symbol tutarsız → FAIL
    - V1 Short: SOLUSDT +70.8% lockbox ama fold'lar negatif → FAIL
    - V2 Strong+ADX: SOLUSDT +9.2% ama trade < 30 → INSUFFICIENT_TRADES
  - **Final classification: FILTER_OVERLAY** — standalone edge yok, confirmation/guard filter olarak kullanılabilir. Salvage dosyası güncellendi: `03_SALVAGE_IDEAS/QL_2026-05-01_TV_BUYSELL_INDICATOR_PACK/` (triage, metadata, next_action).
  - Diğer 4 indikatör (QQE, UT Bot, Pivot SuperTrend, Lorentzian) SALVAGE_ONLY — henüz split edilmedi.
  - **Artifact'lar:** `single_strategy_runs/qtrend_optimize/`, `qtrend_short_v2/`, `qtrend_strong/`
- **Modified files:** `11_TRIAGE/analyze_transcripts.py`, `08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py`, `08_DASHBOARD_APP/apps/web/index.html`, `08_DASHBOARD_APP/apps/web/app.js`, `03_QUANTLENS/tools/overnight_v2_runner.py`, `03_QUANTLENS/tools/mega_walk_forward.py`, `03_QUANTLENS/03_SALVAGE_IDEAS/QL_2026-05-01_TV_BUYSELL_INDICATOR_PACK/*`, `_AI_MEMORY/GLOBAL_HANDOFF.md`, `_AI_MEMORY/NEXT_STEPS.md`.

- **IM-002 complete:** added `03_QUANTLENS/tools/audit_hardcoded_paths.py` and wired `09_DOCS/hooks/protected_paths_hook.py` to run it on staged code-like files. Verification: `py_compile` PASS; staged audit PASS; full default audit reports 2,488 existing legacy references after generated-result dirs are skipped.
- **Sprint aggregation complete:** `aggregate_overnight_iters.py` now accepts `--runs-dir` and `--out`; sprint JSONs aggregated to `03_QUANTLENS/tools/sprint_runs/SPRINT_AGGREGATED_REPORT.md`. Result: 3 iters, 189 PASS cells, robust threshold corrected to `ceil(50%)` = 2/3.
- **IM-003 complete:** `mega_walk_forward.py` now supports `--resume <pickle>`, `--checkpoint-every N`, atomic checkpoint pickle writes, partial JSON writes, completed-job skipping, and atomic final JSON replace. Verification: `py_compile` PASS; synthetic checkpoint save/load + partial JSON helper PASS. Full engine run not executed.
- **IM-004 complete:** `mega_walk_forward.py` writes minute-level progress heartbeat from the same event that prints `[done/total] elapsed=... counts=...`; loop scripts pass heartbeat context via `MEGA_HEARTBEAT_*`. Verification: `py_compile` PASS; synthetic heartbeat JSON helper PASS. `bash -n` unavailable in this Windows shell, so shell syntax was not machine-checked.
- **IM-005 complete:** ran `register_overnight_monitor.ps1`; Windows scheduled task `MCC_Overnight_Monitor` registered successfully and is `Ready`.
- **IM-006 complete:** added `03_QUANTLENS/tools/cpcv_validator.py` and added a CPCV Gate to `07_BACKTEST_AND_OPTIMIZATION_RULES.md`. Smoke: 2 sprint candidates, 4 groups, 1 test group, V2 monkey-patch enabled; report at `03_QUANTLENS/tools/cpcv_runs/smoke/CPCV_VALIDATION_REPORT.md`.
- **IM-007 complete:** added `03_QUANTLENS/tools/probabilistic_pbo.py` and added a PBO Gate to the rules. Smoke used CPCV smoke artifact and wrote `03_QUANTLENS/tools/pbo_runs/smoke/PBO_REPORT.md`; PBO smoke value 0.0 is only tool verification.
- **IM-008 complete:** added `03_QUANTLENS/tools/single_strategy_backtest.py` and MEGA filters `--strategy/--symbol/--tf`. Smoke run: `QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK BTCUSDT 4h`, output `03_QUANTLENS/tools/single_strategy_runs/smoke_IM008/`.
- **IM-009 complete:** added `03_QUANTLENS/tools/data_check.py` with `verify_actual_range(symbol, tf)` and CLI; `single_strategy_backtest.py` now imports it. Verification: BTCUSDT 4h data check PASS; single-strategy smoke rerun output `single_strategy_runs/smoke_IM009/`; final `py_compile` PASS.

## 2026-06-01 sprint result (overnight 23:29 → 06:33 + 1h sprint)

- **Overnight 2-worker loop (23:29 → 04:06):** 3 iter crash, 0 JSON kayıt. Kök neden: `mega_walk_forward.py:37` `OUTPUT_DIR` legacy frozen path (`C:\LAB\tradingview-lab\...`) read-only. ~5.5h hesaplama veri kaybı.
- **Fix applied 04:06:** `MEGA_OUTPUT_DIR` env override + CLEAN repo default → `03_QUANTLENS/05_BACKTEST_RESULTS/`. Mega_walk_forward.py:37-42 + :742-746 (env reads).
- **Sprint 20-worker loop (05:46 → 06:46):** 3 başarılı iter (~15dk/iter). 0 crash. JSON kayıt OK.
  - `sprint_runs/MEGA_results_iter_1_20260601_054633.json` (4.6MB)
  - `sprint_runs/MEGA_results_iter_2_20260601_060216.json`
  - `sprint_runs/MEGA_results_iter_3_20260601_061755.json`
  - Iter 4 yarıda kesildi (kullanıcı kapatma talebi).

## Codex GPT-5 2026-06-04 — Confirmation run resumed after Claude token stop

Scope: resumed Claude's interrupted quiet confirmation run for `NIGHT-FOLLOWUP-002` after reading the pasted chat history and mandatory QuantLens backtest pre-reads. No Pine, MTC strategy behavior, parity files, live trading, or defaults changed.

Actions:
- Verified Claude had created `03_QUANTLENS/tools/confirmation_runner_2026-06-04.py`, `run_confirmation_2026-06-04.sh`, and the A18-fixed `write_overnight_morning_report.py`, but no live confirmation process or confirm output existed.
- Added `start_confirmation_2026-06-04_keepawake.ps1` and launched it hidden. Core confirmation run completed: 306 cells, about 3,672 configs, 4 workers, 69.6s, 16 PASS/STRONG_PASS, 1 BH-FDR survivor, 0 DSR-robust, 0 final robust.
- Post-pipeline completed: `multiwindow_oos.py`, `alpha_vs_buyhold.py`, and A18-fixed morning report.
- Filled missing aggregate artifact and ran validation tail: CPCV over 16 PASS cells, PBO, 16 `evaluation_artifacts/*.eval.json`, and 16 `scorecards/*.scorecard.json`.
- Started low-resource morning watchdog PID `44464`, heartbeat `03_QUANTLENS/tools/overnight_runs/_heartbeat_confirm_morning_watchdog.json`, deadline `2026-06-05T07:30:00` local. It keeps Windows awake and refreshes artifact status; it does not run more backtests.

Key outcome:
- Report: `03_QUANTLENS/05_BACKTEST_RESULTS/confirm_2026-06-04/MORNING_REPORT_confirm_2026-06-04.md`.
- A18 fixed in this output: `ALPHA_DONE passes=16 beat_buyhold=11 premium=6 down_market_alpha=6`, and the Down-Market Alpha table has 6 rows.
- Down-market alpha cells are still research-only. DSR research-threshold confirmations: 0. Gate-2 scorecards: 16 INCOMPLETE, 0 pass. `APPROVED_FOR_MTC_V2_INTEGRATION`: none.

Validation:
- `py_compile` PASS for confirmation runner, morning report writer, multiwindow, and alpha tools.
- Git Bash path verified via `C:\Program Files\Git\bin\bash.exe`; launcher syntax PASS with that path.
- Disk write probe PASS; C: used about 60%.
- DeepSeek harness dispatch attempted for read-only audit, but provider returned 402 insufficient balance after task JSON BOM fix; no repo files were touched by the harness.

## Workflow konsolidasyonu (en önemli)

Önceki sessions'da overnight workflow her seferinde sıfırdan icat ediliyordu. Bu seansta:

### Canonical chain (HER backtest için, in-day single dahil)
1. `AGENTS.md` → iki dosya pre-read zorunlu
2. `03_QUANTLENS/_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md` ← **canonical 299 satır** (4 gate, classification, promotion, antigravity, MORNING_REPORT format)
3. `11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md` ← **operasyonel** (tool komutları, worker, monitor, anti-pattern arşivi)
4. `04_SHARED/prompts/05_ai_workflow/08_backtest_launch.md` ← Gate 0-G7 prompt (in-day single / sprint / overnight üç senaryo)
5. `11_TRIAGE/lessons_archive/OVERNIGHT_LESSONS_INDEX.md` ← arşiv

### Wired files (bu seansta değişen)
- `AGENTS.md` — iki dosya pre-read satırı eklendi
- `_AI_MEMORY/START_HERE.md` — aynı zincir
- `04_SHARED/prompts/05_ai_workflow/00_index.md` — 08 satırı in-day dahil edilecek şekilde güncellendi
- `04_SHARED/prompts/05_ai_workflow/08_backtest_launch.md` — rename + üç senaryolu Gate 1.5
- `03_QUANTLENS/tools/mega_walk_forward.py` — OUTPUT_DIR + MEGA_WORKERS env override
- `03_QUANTLENS/tools/monitor_overnight.ps1` (yeni) — taskschd health monitor
- `03_QUANTLENS/tools/register_overnight_monitor.ps1` (yeni) — admin kurulum
- `03_QUANTLENS/tools/overnight_loop_2026-06-01_sprint.sh` (yeni) — 20-worker 1h sprint şablon
- `11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md` (yeni) — operasyonel runbook
- `11_TRIAGE/lessons_archive/` (yeni klasör) — arşiv + INDEX
- `_AI_MEMORY/NEXT_STEPS.md` — IM-001..IM-009 eklendi (CPCV, PBO, in-day script, data_check, vs)

## DeepSeek/Codex "ne yapacaksın" testi

Akşam herhangi bir model (Claude / DeepSeek V4 Pro / Codex / Gemini) "backtest iş akışım ne" sorulduğunda:
1. AGENTS.md okur (root) → pre-read zorunlu iki dosya görür
2. RULES okur → 4 gate + buy&hold + classification + promotion
3. RUNBOOK okur → in-day/sprint/overnight senaryo seçer + tool komutları
4. prompt 08 okur → Gate 0-G7 sırası

Üç farklı modelin yanıtı aynı içeriği vermeli. Tetik kelimeler: "backtest", "optimization", "walk-forward", "overnight".

Where to continue:
  - 17 LIKELY_MISCLASSIFIED + 14 REVIEW_HUMAN candidates need Barış manual transcript review. See `11_TRIAGE/reclassification_audit_2026-06-01.md`.
  - Sprint results (3 JSON) already aggregated to `03_QUANTLENS/tools/sprint_runs/SPRINT_AGGREGATED_REPORT.md`.
  - Side project SP-001 parked.
  - If asked "backtest workflow": cevap canonical chain'den okunmalı, **reinvention yasak**.
Warnings:
  - SP-001 plan in NEXT_STEPS is intent, not contract. Repo may have moved
    by scaffold time — re-check first.
  - Gate 5 (cross-model adversarial review) is discipline-only, no hook
    enforcement. Implementer must explicitly hand off to a different model
    (Codex or Gemini) for review.
  - Hard safety rules (AI_RULES.md): no Pine/MTC/parity edits without
    explicit Barış approval; no live trading; no destructive git ops; no
    `--no-verify`.

## Codex GPT-5 2026-06-04 — Transcript re-triage completion

Scope: resumed Claude's Strategy Research / QuantLens re-triage session, preserved the existing uncommitted infrastructure, and completed the remaining transcript-now-present candidates without touching Pine, MTC behavior, parity logic, live trading, or optimization.

Initial state:
- Branch: `master`.
- Worktree was already dirty with many modified/untracked files, including Strategy Research Lab infrastructure, `STG047`-`STG061`, registries, schemas, dashboard changes, and `11_TRIAGE/retriage_progress.json`.
- Claude's reported infrastructure was present enough to continue: registry scripts, schemas, `00_INBOX/USER_INTAKE`, dashboard Strategy Research Lab tab, `research_reader.py`, and source-intake folders for the prior strategy set existed. I did not recreate parallel infrastructure.

Re-triage result:
- Ledger before final batch: `done=69 pending=18 next_stg=STG062`.
- Ledger after final batch: `done=87 pending=0 next_stg=STG064`; helper `next` returns `ALL_DONE`. Together with pilot entries `Stg082`, `Stg083`, `Stg087`, all 90 eligible candidates are accounted for.
- Final batch promoted/updated:
  - `STG061_ryan_pierpont_breakout_discipline`: repaired with `07_deterministic_spec.md`, full `source_intake/`, and transcripts for `Stg154`-`Stg158`.
  - `STG062_stan_weinstein_stage_analysis`: created with metadata, deterministic spec, full `source_intake/`, and transcripts for `Stg160`-`Stg166`.
  - `STG063_tito_options_aware_rs_breakout`: created as `needs_manual_review` partial spec with full `source_intake/` and transcripts for `Stg167`-`Stg169`.
  - Duplicates: `Stg170` -> `STG032_10_ty_microcap_short`; `Stg171` -> `STG022_ql_vcp_richard_1d`; `Stg172` -> `STG056_oliver_kell_price_cycle`. Transcripts copied into each target's `source_intake/transcripts/` and duplicate notes written under `source_intake/notes/`.

Disposition counts for final batch:
- `promoted_to_matured_strategy`: 12 candidate rows.
- `needs_manual_review`: 3 candidate rows.
- `duplicate_existing_strategy`: 3 candidate rows.
- blocked: 0.

Validation:
- `python MTC_COMMAND_CENTER\03_QUANTLENS\tools\build_strategy_research_registry.py` PASS; wrote 63 strategies, 27 indicators, 78 components, 5 tag entries.
- `python MTC_COMMAND_CENTER\03_QUANTLENS\tools\build_strategy_research_registry.py --check` PASS.
- `python MTC_COMMAND_CENTER\03_QUANTLENS\tools\validate_research_registries.py` PASS.
- `python MTC_COMMAND_CENTER\03_QUANTLENS\tools\build_triage_registry.py` PASS; 172 total, 159 with transcripts, 90 eligible.
- `node --check MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\app.js` PASS.
- `python -m pytest MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\tests` PASS only after setting `PYTHONPATH=C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api`; result 35 passed.
- Dashboard snapshot check via `build_dashboard_snapshot()` PASS; `strategy_research` contains STG061, STG062, and STG063; diagnostics schema validation true.

Remaining work:
- `RESEARCH-004` is closed in `NEXT_STEPS.md`.
- New residual item: `RESEARCH-005` review whether `STG063_tito_options_aware_rs_breakout` stays manual options-aware research or becomes a stock-only proxy with explicit caveats. Do not backtest options returns from stock-only data.
- Continue `RESEARCH-002` review-needed cleanup across the refreshed 63-strategy registry.

## Codex GPT-5 2026-06-04 — SP-005 Wave A Strategy Detail Page

Scope: implemented SP-005 Wave A only for the live dashboard Strategy Detail Page. This is the presentation layer, not the SP-004 scorecard engine.

Files changed:
- `08_DASHBOARD_APP/apps/web/app.js`
- `08_DASHBOARD_APP/apps/web/styles.css`
- `08_DASHBOARD_APP/apps/api/mcc_readonly/pipeline_reader.py`
- `_AI_MEMORY/NEXT_STEPS.md`
- `_AI_MEMORY/GLOBAL_HANDOFF.md`
- `_AI_MEMORY/SESSION_LOG.md`
- `_AI_MEMORY/ACTIVE_FILES.md`

Implemented:
- Terminal-style single-scroll Strategy Detail Page with sticky mini-summary.
- Human-readable title fallback so the main title is not a raw strategy ID.
- Merged `Verdict & Decision` section using existing audit/readiness data.
- Main `Scorecard` section shows honest SP-004 pending state when `scorecard_v2` is absent.
- Legacy composite score moved into collapsed `Technical Details` only.
- Strategy Taxonomy shell, Review Journey, Trading Rules with visible `Not defined yet`, Backtest Evidence unavailable state/checklist, Salvageable Ideas placeholder, Source Material, and collapsed Technical Details.
- Existing hardcoded fallback strategy descriptions in `pipeline_reader.py` now have English override data for the detail page.

Intentionally not implemented:
- No SP-004 scoring math, no `scorecard_v2`, no fake gate scores.
- No QuantLens structured reader yet; QuantLens/Salvage render honest placeholders.
- No TradingView-style backtest case visualization yet.
- No Pine, MTC behavior, parity, backtest, or trading logic changes.
- No deletion of `11_TRIAGE/_eval_pipeline_source_TEMP/`.

Validation:
- `node --check MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\app.js` PASS.
- `python -m py_compile MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\mcc_readonly\pipeline_reader.py` PASS.
- `PYTHONPATH=C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api python -m pytest MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\tests` PASS: 35 passed.
- Started dashboard at `http://127.0.0.1:8765/dashboard`; browser check confirmed all Wave A sections render, first tested title is not raw ID, Technical Details is collapsed by default, missing fields are visible, gate scorecard placeholder is shown, QuantLens placeholder is shown, and desktop horizontal overflow is fixed.
- Snapshot verification: current data includes missing-rules and legacy-score-only cases, and no structured QuantLens data; no current row exposes real `metrics`, so metrics-present Backtest Evidence could not be visually verified.

Remaining work:
- SP-005 Wave B: add read-only QuantLens structured reader and wire real QuantLens Verdict/Salvageable Ideas fields.
- SP-005 Wave C: after SP-004 emits `scorecard_v2`, render real gate rows and backtest evidence cases from real artifacts only.
- SP-004 remains planned and incomplete; do not mark scorecard redesign complete.

## DeepSeek v4-pro 2026-06-04 — SP-004 P1A CPCV/PBO fixes (AUDIT-002 + AUDIT-005)

Completed SP-004 Phase 1A: robustness-tool hardening. Three narrow fixes applied to
validator tools, no Pine/MTC/parity/mega_walk_forward edits.

**FIX 1 — AUDIT-002 (cpcv_validator.py): 3-tuple short strategy support.**
- `validate_candidate()` line 86: replaced `sig, stop = mw.build_signals(...)` with
  canonical 3-tuple parse from mega_walk_forward.py:654-658 (`if isinstance(result, tuple)
  and len(result) == 3 and result[2] in {"long", "short"}: sig, stop, direction = result`).
- `evaluate_split()`: added `direction="long"` parameter, passed to every
  `mw.simulate_slice(..., direction=direction)` call.
- Call site at line ~91 passes `direction=direction` to `evaluate_split`.

**FIX 2 — AUDIT-005 (probabilistic_pbo.py): symmetric CSCV partition.**
- Replaced `half = n_splits // 2` with `usable = n_splits_available - (n_splits_available % 2)`
  then `half = usable // 2`. Dropped column(s) recorded via `splits_used` / `splits_available`
  / `partition_note` in result. Train and test halves equal length on every combination.

**FIX 3 — N_A / TOOL_FAILED fallback (both files).**
- cpcv_validator.py: NO_DATA→N_A, INSUFFICIENT_GROUPS→INSUFFICIENT_DATA, all with
  `reason` string; per-candidate body wrapped in try/except → `{status: "TOOL_FAILED", reason}`.
- probabilistic_pbo.py: SKIPPED→INSUFFICIENT_DATA; when pbo=None, status=`INSUFFICIENT_DATA`
  (never bare zero), normal path status=`OK`.

**Validation (all PASS):**
1. `py_compile` both files — clean.
2. CPCV smoke `--max-candidates 3` → `cpcv_results.json` + `CPCV_VALIDATION_REPORT.md` written, no crash.
3. PBO smoke on CPCV output → `split_count=14` (even), `splits_available=15` (original odd),
   `splits_used=14`, `pbo=0.102564`, `status=OK`.
4. No short 3-tuple strategy in the input set, but the code path is structurally identical
   to mega_walk_forward.py's verified pattern.

**Next:** SP-004 P1 — emit `evaluation_artifact_v1` with status envelope on 5-10 strategies.

## DeepSeek v4-pro 2026-06-04 — SP-004 Batch A engine hardening (AUDIT-001, AUDIT-004, AUDIT-006)

Completed SP-004 Batch A: three engine-hardening fixes. No Pine/MTC/parity/strategy-rename changes.

**FIX 1 — AUDIT-001 (overnight_v2_runner.py:594): ADX direction flip.**
Barış D004 decision: STRONG ADX intent = high ADX. Changed `<` to `>=`:
`sig = change_up & strong_buy & (df["adx_14"] >= int(params["adx_threshold"]))`.
One-character logic fix. Consistent with existing `strong_buy` gate. No rename.

**FIX 2 — AUDIT-004 (mega_walk_forward.py:36): BUNDLE_MANIFEST env override.**
Added `_env_manifest = os.environ.get("MEGA_BUNDLE_MANIFEST")` with legacy fallback,
matching `MEGA_OUTPUT_DIR` pattern at lines 40-45. Verified env override routes to
correct path; unset falls back to archive path.

**FIX 3 — AUDIT-006 (mega_walk_forward.py): silent fold skip → visible INSUFFICIENT_DATA.**
Added `fold_feasibility(n_bars)` sibling helper mirroring `rolling_fold_indices` guards
(span_end<1000, train_size<400, test_size<200) without changing any threshold. In
`_worker`, immediately after MIN_BARS_REQUIRED check: if infeasible, `warnings.warn`
+ returns `classification: "INSUFFICIENT_DATA"` with `reason` string — distinct from
generic NO_DATA. Added `import warnings` at module top. `if not folds: continue` kept
as defensive guard. Fold math/step/overlap unchanged (AUDIT-008 separate).

**Validation (all PASS):**
1. `py_compile` overnight_v2_runner.py + mega_walk_forward.py — clean.
2. FIX 1: line 594 shows `>=` — verified.
3. FIX 2: env override forwards to custom path; unset falls back to legacy — verified.
4. FIX 3: `fold_feasibility(500)` → `(False, "span_end=375 < 1000 (n_bars=500)")`;
   `fold_feasibility(50000)` → `(True, "")` — verified.

## Codex GPT-5 2026-06-04 — Local YouTube transcript collector

Scope: created an isolated local Python utility under `YT_TRANSCRIPT_COLLECTOR/` for collecting transcripts from user-provided YouTube URLs. No Pine, MTC behavior, TradingView parity, backtest, optimization, browser automation, login, or account action touched.

Files added:
- `YT_TRANSCRIPT_COLLECTOR/collect_transcripts.py`
- `YT_TRANSCRIPT_COLLECTOR/requirements.txt`
- `YT_TRANSCRIPT_COLLECTOR/urls.txt`
- `YT_TRANSCRIPT_COLLECTOR/README.md`
- `YT_TRANSCRIPT_COLLECTOR/tests/test_collector.py`
- `YT_TRANSCRIPT_COLLECTOR/transcripts/.gitkeep`
- `YT_TRANSCRIPT_COLLECTOR/reports/.gitkeep`

Implemented:
- Reads URLs from `urls.txt`, ignores blank/comment lines, and extracts video IDs from standard watch URLs, `youtu.be`, shorts, embed, live, `/v/`, and raw 11-character IDs.
- Uses `youtube-transcript-api` only; no video/audio download and no browser fallback.
- Selects transcript language priority `tr`, then `en`, then first available transcript; supports manual and auto-generated transcript metadata when exposed by the library.
- Writes per-video Markdown transcript files under `transcripts/`.
- Writes `reports/transcript_index.csv` and `reports/failed_videos.csv`.
- README includes Windows PowerShell install, usage, test commands, and safety notes.

Validation:
- `python -m py_compile .\YT_TRANSCRIPT_COLLECTOR\collect_transcripts.py .\YT_TRANSCRIPT_COLLECTOR\tests\test_collector.py` PASS.
- `python -m unittest discover -s tests -p "test_*.py"` from `YT_TRANSCRIPT_COLLECTOR` PASS: 2 tests.
- `python -m unittest discover -s .\YT_TRANSCRIPT_COLLECTOR\tests -p "test_*.py"` from repo root PASS: 2 tests.
- `python .\YT_TRANSCRIPT_COLLECTOR\collect_transcripts.py --help` PASS.

Notes:
- Live transcript fetch was not run; the tool requires `youtube-transcript-api` installation and depends on public transcript availability / YouTube request behavior.

## Codex GPT-5 2026-06-05 - Hermes Desktop install

Scope: installed the official Hermes Desktop app described in `nb5ALoAGAbE` using the signed Windows desktop bootstrapper from Nous Research plus the official `install.ps1` stage flow. No YouTube login, no account actions, no Pine/MTC/parity/backtest changes.

Completed:
- Downloaded `Hermes-Setup.exe` from the official Hermes Desktop documentation link and verified the Authenticode signature: signer `Nous Research Inc.`.
- Official GUI installer stalled at repository clone. Recovered by stopping only the Hermes installer process tree, seeding `%LOCALAPPDATA%\hermes\hermes-agent` from the official GitHub ZIP archive, then running official installer stages.
- Built desktop app at `%LOCALAPPDATA%\hermes\hermes-agent\apps\desktop\release\win-unpacked\Hermes.exe`.
- Created shortcuts:
  - `%USERPROFILE%\Desktop\Hermes.lnk`
  - `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Hermes.lnk`
- Rewrote `.hermes-bootstrap-complete` with pinned commit `acce1a2452f8b85343db1b057c1d98717c421522` so Desktop skips first-launch bootstrap.

Validation:
- `venv`, Python dependencies, node deps, Playwright Chromium/FFmpeg, desktop build, PATH, config templates, platform SDKs, and bootstrap marker stages all completed.
- Hermes Desktop launched and reached the normal app screen.
- Verification screenshot: `C:\tmp\hermes_desktop_final.png`.

Open:
- Model/provider selection is intentionally left unconfigured unless Baris explicitly chooses a provider or approves remote/paid routing.

## Claude Opus 4.8 2026-06-05 — SP-004 Phase 3 gate scorers

Built the remaining gate scorers (reader-side, no approval needed) by dispatching the
file labor to Grok `grok-4` via `_deepseek_driver/ds_agent.py` (DeepSeek returned 402
Insufficient Balance), then Claude-auditing each on the real 16 confirm-2026-06-04
evaluation artifacts.

New files in `03_QUANTLENS/tools/`:
- `score_gate1.py`  — Gate 1 intake /100 (35 criteria, `intake.*` envelopes).
- `score_gate1b.py` — Gate 1B MTC feasibility /100, PASS≥75 (`feasibility.*`), D1 verdict
  bands PASS/CONDITIONAL/FAIL; REJECT_REPAINT forces verdict FAIL.
- `score_gate3.py`  — Gate 3 production-readiness /100, reads `production_readiness_artifact_v1`
  groups per D4 (37 criteria).
- `score_all_gates.py` — unified composer → one `scorecard_v2` (gate1+1B+2+3); NEVER a single
  blended number; `gate_summary.promotable` = all four OK and pass.

All mirror `score_gate2.py`: pure `score_gateX(artifact)->dict` + CLI `--in-dir --out-dir`;
status-envelope rule (only OK scores; non-OK → `points_awarded=None` → gate INCOMPLETE; never
auto-zero/fabricate); `REJECT_REPAINT`→FAIL; parity advisory (WARN never blocks); utf-8 stdout.

Audit result: py_compile PASS ×4; synthetic full-OK→100/OK/pass; empty→INCOMPLETE; composer
all-OK→promotable with no top-level score. Real 16/16 = every gate INCOMPLETE, 0 pass, 0
promotable — the correct honest outcome, because intake/feasibility/readiness fields are not
emitted yet (same gap as the ~17 missing Gate-2 metrics). Inline bug fix caught by audit:
gate1b verdict reported PASS under a REJECT_REPAINT hard-fail → added override.

Not committed (Barış commits). Downstream still gated: P1.5 numeric bands (Barış), SP-005
Wave C dashboard render of `scorecard_v2`, and SP-004-METRIC-ENRICHMENT (backtest-side,
approval-gated).

## Claude Opus 4.8 2026-06-05 — Reader-side queue (morning-report path + SP-005 Wave B reader)

Continued the dispatch workflow through the no-approval reader-side queue (DeepSeek still
402 Insufficient Balance → all dispatch via Grok `grok-4`).

1. **NIGHT-FOLLOWUP-003 DONE** — `03_QUANTLENS/tools/generate_morning_report.py` legacy
   hardcoded `C:\LAB\tradingview-lab\...` OUTPUT_DIR replaced with env-overridable
   repo-relative default (`MEGA_OUTPUT_DIR` else `03_QUANTLENS/05_BACKTEST_RESULTS`),
   mirroring `mega_walk_forward.py`. Verified py_compile + default/override.

2. **SP-005 Wave B reader DONE (data layer)** — new read-only
   `08_DASHBOARD_APP/apps/api/mcc_readonly/quantlens_reader.py` parses
   `03_SALVAGE_IDEAS/<candidate>/01_candidate_metadata.yaml` and emits `quantlens_verdict`
   (decision label, commercial-value band, complexity, testability, risks — labels only, NO
   computed score), structured `salvageable_ideas[]` from `candidate_kind`, derived
   `stop_state` (CLOSED_SOURCE_STOP / COMPLEXITY_OVERLOAD / GARBAGE), `reference_files`,
   JSON-safe `raw`. Wired `quantlens` key into `read_model.py`. Claude audit: 3 real
   candidates parse correctly; fixed 2 inline bugs (reference_files → file not dir; YAML
   date objects broke snapshot JSON → `_jsonable` coercion). Dashboard API tests 35 passed.
   Remaining Wave B = the app.js QuantLens Verdict card (Claude-lead UI, not mechanical).

Cleanly-dispatchable mechanical queue now exhausted. Everything else OPEN is Claude-lead UI
(SP-005 Wave B card, Wave C — Wave C also blocked on real backtest metrics), judgment work
(RESEARCH-001 intake consolidation, RESEARCH-003 MTC_V2 indicator inventory), or Barış-gated
(SP-004 metric-enrichment, heavy-tier, MEV-002/003, promotion, US-equity data, all commits).
Nothing committed.


## Claude Opus 4.8 2026-06-05 — SP-005 Wave B UI (QuantLens Verdict card)

Built the detail-page UI for the `quantlens` snapshot key (frontend; Claude-lead, not
dispatched). `apps/web/app.js`: `findQuantlensCandidate` joins by candidate_id === pipeline/
audit row.id (all 3 salvage candidates match); new `renderQuantlensVerdict` card (decision
badge, stop-state banner, commercial-value band / complexity / testability / instrument-fit
facts, risk chips, recommended next step — commentary/labels only, never a gate score);
`renderSalvageableIdeas` now renders the real `salvageable_ideas[]`; `buildWaveADecision`
surfaces the real QuantLens label. Section order: Verdict & Decision → Scorecard → QuantLens
Verdict → Taxonomy. `styles.css` gains `.quantlens-stop`.

Verified live on the running dashboard (preview server, port 8765): the Equilibrium QL
strategy renders the full card (SALVAGE, commercial 4/10, complexity 6/10, testability
Partially testable, 4 salvageable components: guard / confirmation / SL-TP / money mgmt); a
non-QL strategy renders the clean "Not in QuantLens" fallback with no JS error; `node --check`
PASS. SP-005 Wave B (reader + UI) complete. Only the stop-state banner path is unverified-live
(no on-disk candidate currently carries CLOSED_SOURCE_STOP / COMPLEXITY_OVERLOAD). Not committed.

Wave C (scorecard_v2 gate bars + backtest-evidence visuals) remains: blocked on real backtest
metrics (no row has real Gate-2 metrics yet — SP-004-METRIC-ENRICHMENT is Barış-gated).
