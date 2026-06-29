# Strategy Validation Terminal — MCC-Native Implementation Plan

Date: 2026-06-28
Owner: Barış
Status: APPROVED to start Phase 0/1 (read-only, single new dashboard tab)
Source: `Temp/MTC_STRATEGY_VALIDATION_TERMINAL_PLAN` (ChatGPT/AI-Pathways video plan)
Audited by: 4 independent passes (Claude/Opus, ChatGPT, DeepSeek, Antigravity) — all converged.

> **This supersedes the raw ChatGPT `STRATEGY_VALIDATION_TERMINAL_IMPLEMENTATION_PROMPT.md`.**
> Do not run that prompt directly. It was written blind to the repo and would duplicate ~60%
> of MCC plus introduce a parallel schema/module. This plan is repo-native and read-only.

---

## 1. Audit verdict (consensus of 4 passes)

The video's *methodology* is sound and already adopted by MCC — and MCC is stricter
(DSR + BH-FDR + CPCV + PBO + parity, vs the video's `Sharpe > 0.5`). The only real gaps are
**visualization / aggregation surfaces** over data the engine already produces.

### Already in MCC (do NOT rebuild)

| ChatGPT proposal | Already shipped | Evidence |
|---|---|---|
| Validation gates / funnel logic | 15 backtest gates + SP-004 scorecard (G1→G1B→G2→G3) | `03_QUANTLENS/_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md` |
| IS/OOS + walk-forward | rolling WF, multi-window, CPCV | `tools/mega_walk_forward.py`, `multiwindow_oos.py` |
| Buy&Hold mandatory + alpha | Benchmark Gate | rules §4, §8 |
| Bootstrap + overfit | bootstrap, DSR, BH-FDR, PBO | `finalize_bootstrap_bh.py` |
| Survivor flag | `robustness.bh_fdr_survivor` (bool) per result row | `backtest_profile_result.json` |
| Graveyard/survivor statuses | REJECTED / SALVAGE_ONLY / BACKTEST_FAILED vs BACKTEST_PASSED / APPROVED_FOR_MTC | `status_legend.md` |
| Strategy families | family taxonomy | `pipeline_reader.py`, `TAG_DICTIONARY.json` |
| "Building" layer-stack | profile ladder SOURCE_NAKED → RISK_NORMALIZED → MTC_LIGHT → FULL_MTC_CANDIDATE | `night_artifacts_reader.py:33` |
| Strategy Detail (LLM separated from evidence) | `intelligence` tab: Overview→Gate1→**AI Verdict**→**Backtest Evidence**→Explorer→Paper→Advanced | `apps/web/app.js` |
| Run history / result explorer / leaderboard | `backtest-runs`, `result-explorer`, `leaderboard` tabs | dashboard shell (14 tabs) |

### Real gaps (what this plan builds)

1. **Validation funnel viz** — gates exist, no "X entered → Y passed gate N" picture.
2. **Survivor aggregation** — `bh_fdr_survivor` scattered across result rows, no consolidated view.
3. **Graveyard view** — rejects have status data but no searchable why-killed surface.
4. **IS-vs-OOS scatter** — numbers exist, no plot.
5. **Killed-by-filter / gauntlet** — which gate kills most, not surfaced.
6. **Family survival rate** — comparative, not just per-strategy.
7. **Cross-asset consistency score (0–4)** — not formalized.
8. **Regime split viz** — scored in Gate 2, not shown. (Phase 2.)

### Hard rejects (all 4 passes agree)

- New parallel `validation/` module + new schemas → **reuse** `backtest_profile_result` + `scorecard_v2` + `night_artifacts`.
- Demo/fake data in production dashboard.
- HMM / portfolio / correlation lab as Phase 1 → defer.
- Any "survivor score" composite not derived from real fields → would become another misleading number.
- 5 new tabs → 14 already exist = clutter. **One** new tab with internal sub-views (Barış decision 2026-06-28).

---

## 2. Architecture (repo-native, read-only)

Data already lands in the snapshot. The Validation Terminal is a **derived view**, not a new pipeline.

```
backtest_profile_result.json (per run dir)
  results[].{strategy_id, profile, symbol, timeframe, parameter_set_id,
            score, metrics.{net_profit, max_drawdown, buy_hold_return, buy_hold_alpha,
                            trade_count, sharpe, profit_factor, win_rate},
            robustness.{classification, dsr_p_value, dsr_robust, bh_fdr_survivor,
                        robust_final, n_folds, folds_positive, avg_fold_test_return_pct},
            promotion_status, provenance.universe_mismatch}
        │
        ▼  already discovered by night_artifacts_reader → snapshot["night_artifacts"]["profile_result_files"]
        │
   [NEW] validation_reader.build_validation_terminal(night_artifacts, scorecards, candidate_pipeline)
        │   pure in-memory aggregation, no disk re-read, no new files
        ▼
   snapshot["validation_terminal"] = { funnel, survivors[], graveyard[], family_survival[],
                                       gauntlet[], is_oos_scatter[], generated_at, source_counts }
        │
        ▼
   apps/web: ONE new tab "Validation Terminal" (sub-views: Funnel · Survivors · Graveyard)
            + intelligence tab section 8 (funnel status + robustness notes)
```

### Wiring point
`apps/api/mcc_readonly/read_model.py:377` (right after `night_artifacts = build_night_artifacts(...)`):
```python
validation_terminal = build_validation_terminal(
    night_artifacts=night_artifacts,
    scorecards=scorecards,
    candidate_pipeline=candidate_pipeline,
)
# add to snapshot dict: "validation_terminal": validation_terminal,
```

---

## 3. Phase 0 — Field mapping (DONE in this plan)

Every plan concept maps to an existing field. No new field invented except the two scores below,
both derived from real data only.

| Plan concept | Source field | Notes |
|---|---|---|
| funnel: total variants | count of all `results[]` rows | |
| funnel: completed runs | rows with non-null `metrics` | |
| funnel: positive OOS | `robustness.avg_fold_test_return_pct > 0` | |
| funnel: beats B&H | `metrics.buy_hold_alpha > 0` (or net_profit > buy_hold_return) | |
| funnel: passed filters | `robustness.robust_final == true` | |
| funnel: survivors | `robustness.bh_fdr_survivor == true` | |
| survivor verdict | `robustness.classification` + `promotion_status` | reuse MCC vocab, no new enum |
| graveyard reason | first failing gate: completed→OOS→benchmark→robustness→DSR→FDR | derived from robustness flags (matches `_GATE_ORDER`) |
| family | `pipeline_reader` family map / strategy_id prefix | |
| IS score (scatter X) | `score` if score_method is IS, else folds in-sample | confirm per artifact; fallback: train fold mean |
| OOS score (scatter Y) | `robustness.avg_fold_test_return_pct` | |
| layer / building stage | `profile` (SOURCE_NAKED…FULL_MTC_CANDIDATE) | |

**Two derived scores (real fields only):**
- `cross_asset_consistency_score` (0–4) = **survivor breadth**, bucketed by count of distinct
  `symbol` where (`bh_fdr_survivor` AND beats buy&hold) for the same `strategy_id`.
  `0`=1 symbol, `1`=2–3, `2`=4–5, `3`=6+, `4`=6+ and multi-TF. **Measures symbol/timeframe breadth
  only** — it does not prove asset-class diversity or multi-window robustness (no such field on the
  row), so the label is "symbols", not "cross-class". Asset-class/window breadth is Phase 2 work.
- survivor ranking: **no new composite.** Sort by (`bh_fdr_survivor` desc, `dsr_robust` desc,
  `buy_hold_alpha` desc). Display the real components, not a black-box number.

---

## 4. Phase 1 — Build (read-only, ~3–4 days)

| Task | File | Effort |
|---|---|---|
| 1. Aggregator reader | `apps/api/mcc_readonly/validation_reader.py` (new) | 1–1.5 d |
| 2. Wire into snapshot | `apps/api/mcc_readonly/read_model.py` (edit ~line 377/400) | 0.25 d |
| 3. Tests | `apps/api/tests/test_validation_reader.py` (new) | 0.5 d |
| 4. New tab + sub-views | `apps/web/app.js` (1 nav entry + Funnel/Survivors/Graveyard render) | 1 d |
| 5. IS/OOS scatter | `apps/web` (lightweight inline SVG/canvas, no new dep) | 0.5 d |
| 6. intelligence §8 | `apps/web/app.js` (funnel status + robustness notes block) | 0.25 d |
| 7. README/handoff | `11_TRIAGE` + `_AI_MEMORY` update | 0.25 d |

**Definition of done (Phase 1):**
- New "Validation Terminal" tab renders Funnel + Survivors + Graveyard from real snapshot data.
- Zero new schemas, zero new artifact files, zero engine/Pine/MTC_V2 changes.
- Survivor vs graveyard cleanly split; every graveyard row shows a real failure reason.
- Cross-asset score + survivor ranking use only existing fields.
- `pytest apps/api/tests/test_validation_reader.py` green; existing readonly tests still green.
- Empty-state safe (no runs → friendly empty panels, never a crash).

---

## 5. Phase 2 — Status (2026-06-29)

| Item | Status | Notes |
|---|---|---|
| Parameter-sensitivity panel | **DONE** | `_parameter_sensitivity()` in validation_reader; OOS spread per strategy across parameter sets; fragile flag (spread ≥ 20%). Rendered in funnel view. Real data only. |
| Regime performance split | **BLOCKED-ON-DATA** | Per-regime returns live in `multiwindow_summary.json`, not in the in-snapshot `backtest_profile_result` rows. Wiring that artifact in is a separate reader task — NOT faked. |
| Cross-sectional / portfolio / correlation | **DEFERRED** | Needs a portfolio-level artifact that does not exist yet. Would require fabrication today → rejected. |
| HMM regime gate | **OUT OF SCOPE** | Production rule: never an immediate production dependency. |

Phase 2 honored the no-fake-data rule: only the data-backed piece (parameter sensitivity) shipped.
The rest is documented as blocked-on-data rather than mocked.

## 6a. Files delivered (2026-06-28 → 06-29)

- `08_DASHBOARD_APP/apps/api/mcc_readonly/validation_reader.py` (new aggregator)
- `08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py` (wiring)
- `08_DASHBOARD_APP/apps/api/tests/test_validation_reader.py` (10 tests)
- `08_DASHBOARD_APP/apps/web/app.js` (Validation Terminal tab + Funnel/Survivors/Graveyard
  + IS/OOS scatter + Parameter Sensitivity + intelligence §8 evidence block)
- `08_DASHBOARD_APP/apps/web/styles.css` (vt-* component styles)
- `08_DASHBOARD_APP/run_dashboard_server.ps1` (preview/dev launcher referenced by launch.json)

Verified: 99 api tests pass; live snapshot serves `validation_terminal`; browser renders all six
panels with zero console errors; survivors honest-empty on current pilot data.

---

## 6. Guardrails

- Branch `feature/validation-terminal`; never edit on master.
- Read-only: no backtests, no artifact generation, no `top_results.json` writes, no broker/live.
- Protected scopes untouched: `02_MTC_BACKTEST`, `07_ADAPTERS`, `01_PINE`, `MTC_V2`.
- Stage exact files only; run `repo_guard.ps1` at preflight/commit/merge.
- UI labels English.
