# R2-36 Gate2 Tooltip Audit - Codex GPT-5 - 2026-06-08

Scope: display-only audit for the Round-2 remaining item "Gate2 ghost tooltip".
No trading logic, Pine logic, MTC behavior, parity files, or score math changed.

## Result

R2-36 is closed as **NO CODE CHANGE REQUIRED**.

The suspected tooltip text is in `08_DASHBOARD_APP/apps/web/app.js`:

- `blockingGateTooltip("gate2")` says Gate 2 may block because the score is below 75, backtest metrics are missing, or walk-forward is incomplete.
- The compact missing-fields tooltip says missing criteria were not produced or not scored by the backtest run.

This is not a ghost requirement. The emitted Gate 2 vocabulary includes the walk-forward criterion:

- 360/360 discovered `scorecard_v2/*.scorecard.json` files include `metrics.wfo_pass`.
- `03_QUANTLENS/tools/score_gate2.py` defines criterion `wfo_pass` with source metric `metrics.wfo_pass`.
- `03_QUANTLENS/tools/build_evaluation_artifact.py` emits `metrics["wfo_pass"]` from `folds_positive` and `n_folds` when present, or marks it N/A when missing.

## Commands Run

```powershell
rg -n "tooltip|title=|Gate 2|Gate2|gate2|Missing / not scored|metrics not produced|required|requirement|ghost|field" MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\app.js
```

```powershell
node -e "<scan scorecard_v2 sub_scores>"
```

Output summary:

```text
scorecard_v2_files 360
360 metrics.wfo_pass
```

```powershell
rg -n "walk.?forward|wfo|rolling|oos|fold|lockbox|incomplete" MTC_COMMAND_CENTER\03_QUANTLENS\tools\score_gate2.py MTC_COMMAND_CENTER\03_QUANTLENS\tools\build_evaluation_artifact.py MTC_COMMAND_CENTER\06_SCHEMAS -g "*.py" -g "*.json"
```

## Decision

Keep the existing Gate 2 tooltip. It accurately points to a real Gate 2 criterion and its source metric. Removing it would hide useful evidence about why Gate 2 can block promotion.
