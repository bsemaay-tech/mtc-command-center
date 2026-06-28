# Codex Audit Prompt — Strategy Validation Terminal (read-only dashboard feature)

You are auditing a completed, read-only feature branch in the MTC Command Center repo.
**Do not implement anything. Audit only. Report findings with file:line evidence.**

## Context

Branch: `feature/validation-terminal`. The feature adds a "Strategy Validation Terminal"
dashboard tab that aggregates existing backtest evidence into a validation funnel, survivor list,
graveyard, family survival, validation gauntlet, IS/OOS scatter, and parameter-sensitivity view.

Design intent (must be enforced — flag any violation):
- **Read-only.** No file writes, no backtest/optimization execution, no Pine/MTC_V2 changes,
  no new artifact files, no new JSON schemas.
- **No fabricated data.** Every metric/verdict derives from real fields already present in
  `backtest_profile_result.json` rows (surfaced via the snapshot's
  `night_artifacts.profile_results`). No demo/mock data in the production path.
- **Reuse existing vocabulary** (robustness flags, classification, promotion_status). No new
  verdict enum, no black-box composite score.
- **Honest evidence.** If zero strategies survive, the UI must show that truthfully, not pad it.

## Files to audit

1. `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/validation_reader.py` — aggregator.
2. `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/read_model.py` — wiring (search `validation_terminal`).
3. `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_validation_reader.py` — tests.
4. `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/app.js` — UI (search `renderValidationTerminal`, `vt`, `validationEvidenceSection`).
5. `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/styles.css` — `vt-*` styles.
6. `MTC_COMMAND_CENTER/11_TRIAGE/STRATEGY_VALIDATION_TERMINAL_MCC_NATIVE_PLAN_2026-06-28.md` — plan/DoD.

## Audit checklist

### A. Correctness of aggregation logic (`validation_reader.py`)
- Funnel monotonicity: does each stage strictly narrow the previous? Confirm
  `completed_runs >= positive_oos >= beats_buy_hold`. Is `robust_passed`/`survivors` counted from
  the right fields (`robust_final`, `bh_fdr_survivor`)?
- `_gate_flags`: are missing-evidence rows treated as NOT-passed (so they fall to graveyard, never
  silently survive)? Verify bool coercion can't let a truthy-string or `None` slip through.
- `_primary_failure`: gate order matches `07_BACKTEST_AND_OPTIMIZATION_RULES.md`
  (data → OOS → benchmark → robustness → DSR → FDR)? Does it surface engine `classification`
  (e.g. OVERFIT_SUSPECT, INSUFFICIENT_TRADES) when robustness fails?
- `_cross_asset_scores`: 0–4 bucketing — any off-by-one? Does it only count symbols where BOTH
  `bh_fdr_survivor` AND beats-B&H? Could the top bucket (4) be reached without real multi-TF breadth?
- `_parameter_sensitivity`: spread = max−min OOS across distinct `parameter_set_id`; single-param
  strategies excluded; `_median` correct for even/odd lengths?
- `_num`: does it correctly reject bools (so `True` is not read as 1.0)?
- Survivor ranking key: real components only (dsr_robust, cross_asset, buy_hold_alpha)? No hidden
  composite?

### B. Read-only / safety
- Confirm the module never opens files, never writes, never imports an execution path.
- Confirm `read_model.py` only adds a derived key and does not re-read disk or mutate
  `night_artifacts`.
- Confirm `_slim_http_snapshot` does not need to strip `validation_terminal` for payload size, or
  flag if the survivors/graveyard lists could grow unbounded (should they be capped?).

### C. UI integrity (`app.js`)
- XSS: every interpolated value passes through `esc()` before hitting innerHTML? Check the scatter
  `<title>`, graveyard `source_rel_path`, strategy ids, family labels.
- Empty-state handling: tab with zero rows, survivors empty, graveyard empty, scatter with missing
  axes, parameter-sensitivity with no multi-param strategies — all safe, no thrown errors?
- `validationEvidenceSection` strategy matching (`vtRowsForStrategy`): is the normalized
  substring match too loose (false-positive cross-strategy matches) or too strict? Suggest a more
  precise key if warranted.
- Does the new tab follow existing component patterns (`.panel`, `.grid-table`, `badge`, `lc-kpi`)
  without breaking the 14-tab nav or the intelligence detail layout?

### D. Tests
- Do the 10 tests actually assert the invariants above, or are any tautological?
- Missing coverage worth adding (name them): malformed `robustness` blocks, non-numeric metrics,
  duplicate strategy_ids across runs, very large row counts.

### E. Plan honesty
- Does the plan doc's "already in MCC" table match reality? Spot-check 3 claims against the repo.
- Are the Phase 2 "blocked-on-data" items genuinely absent from the snapshot, or could they have
  been wired without fabrication?

## Output format

For each finding: `severity (BLOCKER/HIGH/MED/LOW) — file:line — problem — suggested fix`.
End with a one-paragraph verdict: is this safe to merge to `master` as-is, or what must change first.
Do not modify any files.
