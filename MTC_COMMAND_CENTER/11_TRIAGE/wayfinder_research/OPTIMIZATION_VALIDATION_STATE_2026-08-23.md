# Optimization and Validation Machinery — Code vs Plan (wayfinder #71)

**Map:** #67. **Ticket:** #71. **Scope:** read-only. **Worktree:** `C:/WFK4`, branch `research/optimization-validation-state`, base `origin/master@3d6a621c`.
**Method:** every claim below was verified by reading the cited source file/lines directly in this worktree (not taken from the brief's prose) unless marked "per brief" for cross-reference only.

---

## 1. Headline: the exact discard point

**File:** `MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py`
**Function:** `_worker_impl()` (starts line 1255) — this is the per-(strategy × symbol × timeframe) cell worker for the canonical research engine (`AGENTS.md:254-259` names `mega_walk_forward.py` the canonical single-run command; `_worker`/`_worker_impl` is what each multiprocessing job runs).

**The full per-trial record exists in memory, once per grid point:**
```
tools/mega_walk_forward.py:1289   configs = []
tools/mega_walk_forward.py:1292   for p in grid:                       # grid = select_grid(GRIDS[strategy], stride)
tools/mega_walk_forward.py:1310     for (ts, te, ks, ke) in folds:
tools/mega_walk_forward.py:1311        ft.append(asdict(simulate_slice(..., ts, te, ...)))   # train fold
tools/mega_walk_forward.py:1312        fk.append(asdict(simulate_slice(..., ks, ke, ...)))   # test fold
tools/mega_walk_forward.py:1313-1314  lb = asdict(simulate_slice(..., lockbox_start, n, ...))  # lockbox
tools/mega_walk_forward.py:1322   configs.append({"params": p, "fold_train": ft, "fold_test": fk,
                                                    "lockbox": lb, "mean_train_ret": ...,
                                                    "mean_train_sharpe_pt": ...})
```
`configs` at this point is exactly what a `TrialRecord` row wants for **every** grid point: parameters, all fold metrics, lockbox metrics.

**The discard:**
```
tools/mega_walk_forward.py:1339   best = max(configs, key=lambda c: c["mean_train_ret"])
```
One winner is picked. `configs` (a local Python list, one entry per trial in the grid) is never serialized — no `to_parquet`, `to_csv`, or file `.write(` call exists anywhere in this file (verified by grep: zero hits for any of the three). It simply falls out of scope when `_worker_impl` returns its row at:
```
tools/mega_walk_forward.py:1472-1499   return {
    "strategy": ..., "symbol": ..., "timeframe": ...,
    "trial_count": n_trials, "trial_sr_std": ..., "trial_sr_max": ...,   # 3 aggregate scalars
    "summary": { "best_params": best["params"], ... },                   # only the WINNER's params
    "classification": cls,
}
```
That return value is what `main()` accumulates into `results` and writes as-is:
```
tools/mega_walk_forward.py:1728-1729   out_json = OUTPUT_DIR / "MEGA_walk_forward_results.json"
                                        _atomic_write_text(out_json, json.dumps({...}))
```
So the writer that the audit calls "blocked" is literally this: the persisted JSON row is a projection of `configs` (keep `best`'s params + 3 pool-level scalars), and `configs` itself — the only place all-trial data ever existed — is discarded at the `return` in `_worker_impl`. Verified on a real artifact per the brief (F-4): `05_BACKTEST_RESULTS/MEGA_results_iter_10_20260602_042506_results.json` holds 3,655 cells, a representative cell reports `"trial_count": 64` and exactly one `best_params` — 63 trials' worth of parameters and fold/lockbox metrics per that cell are gone.

**Trade-level detail is discarded one layer deeper still.** `simulate_slice(..., return_trade_events=True)` is called exactly once per cell, on the winning config's lockbox slice only (line 1355), producing `lb_trade_events`. That list feeds `compute_regime_analysis()` (line 1443) which reduces it to a small `regime_analysis` summary dict — the raw trade list (entry/exit/R/MAE/MFE per trade) is never written anywhere. The other 63 configs' trade events (from all `fold_train`/`fold_test`/lockbox simulate_slice calls at lines 1311-1314) are never even collected with `return_trade_events=True` — they're discarded at the point of the `simulate_slice` call itself, before `configs.append`.

**Net effect:** for a 64-trial cell, the persisted artifact carries the winner's parameters plus three scalars. `TrialRecord` (brief §11.2) would instead persist a Parquet row **per trial** (not per cell) with identity/hash columns, full fold metrics, lockbox metrics, DSR/CPCV/PBO/BH-FDR statistics, and `rejection_reasons` — everything currently alive only inside the `configs` list for the lifetime of one `_worker_impl` call.

---

## 2. What optimizer/search code actually runs today

**Three implementations exist in this repo; only one is live for the canonical, promotion-deciding path.**

| Implementation | File | Mechanism | Status |
|---|---|---|---|
| **Canonical grid** | `03_QUANTLENS/tools/mega_walk_forward.py` — `GRIDS` dict (line 348+, per-strategy hand-written nested-loop grids, e.g. `grid_dual_rsi()` line 194) + `select_grid()` (line 131) | Exhaustive nested-loop enumeration; `select_grid` optionally strides/caps it (`MEGA_GRID_STRIDE` env var, D015) but never adapts to results — no feedback loop, no sampler | **This is what runs.** `AGENTS.md:254-259` names this the canonical single-run command; `03_QUANTLENS/tools` is the most recently active research tree (last commit 2026-07-13 per brief F-12) |
| Hand-written grid/random | `02_MTC_BACKTEST/src/optimizer_v0/search.py` (830 lines, calls `MTCRunner`) + `store_sqlite.py` (real per-trial SQLite store: `trials` table — `run_id, idx, params_key, params_json, metrics_json, score, status, prune_reason, runtime_s`, confirmed at `store_sqlite.py:38-50`) | Custom grid/random driver with an actual per-trial persistence layer, thinner than `TrialRecord` (no fold/lockbox/DSR/CPCV columns, no `deployment_identity_hash`) | Exists, has real trial persistence (ironically closer to `TrialRecord` in *shape*, if not fields, than the canonical engine's discard-everything pattern) but sits in `02_MTC_BACKTEST`, which is **dormant** (last commit 2026-06-06 per brief F-12). The brief explicitly says do not harvest it — "superseded by the `TrialRecord` contract" (brief, harvest-then-freeze section) |
| Optuna TPE/Random | `02_MTC_BACKTEST/src/optimize/runner.py` | Genuine adaptive search: `import optuna` (line 12), `TPESampler`/`RandomSampler` (line 13, seeded), `optuna.create_study()` (line 210), `self.study.optimize()` (line 225), trial pruning (`optuna.TrialPruned`, lines 98/128) | Real, working code — not vaporware — but also inside the dormant `02_MTC_BACKTEST` tree. `optuna>=3.5.0` is a real declared dependency (`02_MTC_BACKTEST/requirements.txt`), confirming the brief's F-11 claim it is "already a dependency," but it is not exercised by the canonical research path today |

**Verdict:** the optimizer that actually decides what gets promoted is the exhaustive/strided grid in `mega_walk_forward.py`. Optuna is real and installed but unused on the live path. The brief's §11.1 correction (C-3) — define `TrialRecord` before picking an optimizer, then measure grid vs. Optuna on frozen strategies/datasets before switching — is not yet acted on; no comparison run exists in this repo.

---

## 3. Validation battery: code vs. prose, verified line-by-line

| Control | In code? | Where | Integrated into the canonical writer, or separate/manual? |
|---|---|---|---|
| **Walk-forward folds** | **Real, integrated** | `rolling_fold_indices()`; consumed at `mega_walk_forward.py:1310-1312` (`fold_train`/`fold_test` built per grid point, per fold) | Runs inline, every trial, every cell |
| **Lockbox (held-out tail)** | **Real, integrated** | `LOCKBOX_FRACTION` slicing at `mega_walk_forward.py:1313-1314` (grid-search pass) and `:1354-1355` (winner re-run capturing per-trade R series for bootstrap) | Runs inline, every trial, every cell |
| **DSR (Bailey & López de Prado deflated Sharpe p-value)** | **Real, integrated** | Function `deflated_sharpe_pvalue()` defined at `mega_walk_forward.py:1507-1524` (Euler-Mascheroni expected-max-SR approximation, closed form, not a stub); applied in a post-process pass over already-collected cell rows at `:1678-1695`, writing `r["dsr_p_value"]` / `r["dsr_robust"]` onto each persisted row | Runs inline in the same script, after the grid loop, before the final JSON write — genuinely wired in, not prose |
| **BH-FDR (Benjamini-Hochberg)** | **Real, integrated (twice, divergently)** | Primary path: inline in `mega_walk_forward.py:1697-1716` — computes `bh_fdr_survivor` per row from `boot_p_value`, target FDR `Q=0.10`, standard BH step-up procedure; feeds `robust_final` at `:1719-1725`. **A second, standalone implementation also exists** at `tools/finalize_bootstrap_bh.py:52` (`bh_survivors(pvals_idx, m, q=0.10)`) but has **zero callers anywhere in the repo** (grep for the filename across all `.ps1`/`.py`/`.cmd` returns nothing beyond the file itself) — it is documented in the user guide/runbooks as a manual step but not exercised by any automation found | The version that actually runs is the inline one in `mega_walk_forward.py`; the standalone tool is dead/manual-only code |
| **CPCV (combinatorial purged cross-validation)** | **Real, but separate stage, and currently broken for non-default exit modes** | `tools/cpcv_validator.py` — real purge/embargo logic (`purged_train_bars()` line 26, `evaluate_split()` line 45). Not imported by `mega_walk_forward.py`; runs as a **separate post-hoc stage** over `mega_walk_forward.py`'s output JSON, wired into overnight orchestration scripts (`overnight_full_2026-07-02.ps1:79`, `overnight_turtle_heavy_2026-07-01.ps1:79`, `single_strategy_backtest.py:59`) — i.e. it is real, callable, and actually invoked in practice, just not inline in the writer | **Live bug, unfixed since 2026-07-13:** `00_AGENT_PROTOCOLS/FAZ3B_STAGE2_CONFIRM_PREREG_2026-07-13.md:13-16` records that `cpcv_validator.py` and `multiwindow_oos.py` "never pass `exit_mode` into `simulate_slice`... so they would silently score the wrong exit." **Re-verified today on current master (`3d6a621c`): `grep -n "exit_mode" cpcv_validator.py` returns zero matches** — the bug is still present five-plus weeks later. Any candidate not using the default `fixed_2R` exit is silently CPCV-validated under the wrong exit logic |
| **PBO (Probability of Backtest Overfitting)** | **Real, but separate stage, dependent on CPCV's (buggy) output** | `tools/probabilistic_pbo.py` — real logit-based estimator, `estimate_pbo()` at line 46, consuming a CPCV split-return matrix built by `load_cpcv_matrix()` (line 20). Also not imported by `mega_walk_forward.py`; chained after `cpcv_validator.py` in the same orchestration scripts (e.g. `overnight_full_2026-07-02.ps1:80`, `single_strategy_backtest.py:60`) | Inherits the CPCV exit_mode bug transitively (it only ever sees CPCV's output). Writes a separate `pbo_results`/markdown report — not merged back into any per-trial or per-cell record |

**Column-existence check against `TrialRecord` §11.2's "Statistics" group (`dsr_p_value`, `dsr_robust`, `bh_fdr_survivor`, `cpcv_pass_ratio`, `pbo`):** today, `dsr_p_value`/`dsr_robust`/`bh_fdr_survivor` genuinely populate on the per-cell JSON row written by `mega_walk_forward.py`. `cpcv_pass_ratio` and `pbo` do **not** exist as columns anywhere unified — CPCV and PBO results live only in their own separate `cpcv_results.json` / PBO markdown/JSON files, keyed loosely by `candidate_id()` (strategy|symbol|timeframe string, `probabilistic_pbo.py:16`), never joined back to the cell or trial that produced them.

---

## 4. What `TrialRecord` (brief §11.2) would capture that today's runs throw away

Cross-referencing `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:1935-1958` (§11.2 Tier 1 schema) against what `mega_walk_forward.py` actually persists today:

1. **One row per trial, not per cell.** Today: one JSON object per (strategy×symbol×timeframe) cell, `trial_count` trials collapsed into it. §11.2: one Parquet row per trial — for a 64-trial cell, 64 rows instead of 1.
2. **Every trial's parameters**, not just the winner's. Today: `summary.best_params` only (§1 above).
3. **Per-trial fold metrics** (`fold_test_returns[]`, `fold_test_sharpes[]`, `fold_test_trades[]`) for every trial. Today: `fold_train`/`fold_test` exist in `configs` for every trial but never leave the winner's slot in the return dict — only the winner's fold arrays (`summary.fold_test_returns_pct` etc., lines 1483-1488) survive.
4. **Per-trial lockbox metrics** for every trial. Today: only the winner's lockbox dict (`summary.lockbox_oos`).
5. **`rejection_reasons[]`** per trial — the "why was it rejected" column. Today: nothing records why any of the 63 non-winning configs failed to win; only the single cell-level `classification` (PASS/FAIL/etc.) exists, and that describes the winner, not each trial.
6. **`cpcv_pass_ratio` and `pbo` joined to the trial that produced them.** Today: these live in separate files keyed by a loose strategy|symbol|timeframe string, not joined to any `trial_id` or `param_hash` — and for CPCV, computed under the wrong exit_mode when the candidate isn't `fixed_2R` (§3 above).
7. **Identity columns** (`package_hash`, `deployment_identity_hash`, `evaluation_run_hash`, `family_id`, `trial_id`, `param_hash`) — none of these hashes exist anywhere in `mega_walk_forward.py`'s output today; there is no concept of a stable per-trial or per-candidate identity in the current schema, only the ad hoc `candidate_id()` string used by `probabilistic_pbo.py`.
8. **Search lineage** (`search_regime`, `preregistered_space_hash`, `trial_index_in_family`, `family_size`) — `search_regime` would today always be `grid` (§2), but none of these fields are recorded per trial; `param_set_total` (line 1748) is the closest existing analogue and it's a per-cell aggregate, not per-trial.
9. **Trade/equity link (Tier 2 artifacts: `trades.parquet`, `equity.parquet`, `intents.jsonl`, `levels.parquet`)** — today, per-trade detail (`trade_events`) is computed once for the winner's lockbox slice and reduced to a small `regime_analysis` summary; the raw trade list is never written to disk for any trial, winner or otherwise (§1 above, confirmed by grep: no `to_parquet`/`to_csv`/`.write(` call in the file).

---

## 5. Sources consulted (primary, all read directly in this worktree)

- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py` (1857 lines) — `_worker_impl` (1255-1499), `simulate_slice` (648), `deflated_sharpe_pvalue` (1507), BH-FDR block (1697-1725), `GRIDS`/`select_grid` (131, 348), final JSON write (1728-1729)
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/cpcv_validator.py` — `purged_train_bars`, `evaluate_split`; grep-verified absence of `exit_mode`
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/probabilistic_pbo.py` — `load_cpcv_matrix`, `estimate_pbo`
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/finalize_bootstrap_bh.py` — `bh_survivors`; grep-verified zero callers repo-wide
- `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/optimize/runner.py` — Optuna TPE/Random wiring
- `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/optimizer_v0/store_sqlite.py` — `trials` table schema
- `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/FAZ3B_STAGE2_CONFIRM_PREREG_2026-07-13.md:13-16` — original CPCV exit_mode defect record
- `AGENTS.md:250-259` — canonical run command / engine designation
- Orchestration scripts confirming CPCV/PBO wiring: `overnight_full_2026-07-02.ps1`, `overnight_turtle_heavy_2026-07-01.ps1`, `overnight_archetypes_resilient_2026-07-03.ps1`, `overnight_resilient_2026-07-02_2100.ps1`, `single_strategy_backtest.py`
- `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md` — F-3, F-4, F-11, F-12, §11.1, §11.2 (cited for the plan side and cross-checked, not taken on faith — every code claim in this brief that this research touched was independently re-derived from source above)

No code was executed. No files outside `MTC_COMMAND_CENTER/11_TRIAGE/wayfinder_research/OPTIMIZATION_VALIDATION_STATE_2026-08-23.md` were modified in this worktree.
