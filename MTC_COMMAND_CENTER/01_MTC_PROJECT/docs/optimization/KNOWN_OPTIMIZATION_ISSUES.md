# Known Optimization Issues

## Patched Issues Requiring Validation

- `tp_mode=None` with canonical `tp_r_multiple=null` caused failed evaluations before the post-run patch. Current big-runner code preserves canonical null for `evaluation_key` semantics and converts to numeric `tp_r_multiple=1.0` before Runner validation.
- The keep-awake heartbeat script initially had a UInt32 cast issue. Current script uses `[Convert]::ToUInt32(..., 16)` for execution-state flags.
- Resume skip initially risked overwriting `COMPLETED` registry status with `SKIPPED_ALREADY_COMPLETED`; this was fixed during the 2026-04-28 consolidation so completed identity remains resumable after repeated skips.

## Strategy And Research Weaknesses

- CHOPPY regime aggregate PnL was negative in the completed multi-asset subset.
- CONSOLIDATING regime aggregate PnL was negative in the completed multi-asset subset.
- 1D timeframe had very weak positive-test coverage compared with intraday timeframes.
- The exhaustive core grid is incomplete: 321 of 12,600 unique parameter variants were completed.
- No strict robust candidate exists yet.

## Infrastructure And Workflow Gaps

- Resume/de-dup was present during the big run, but the first run naturally reported `skipped_already_completed=0`.
- The 2026-04-28 dedicated restart smoke proved `skipped_already_completed > 0`, `duplicate_conflicts=0`, and completed keys remain completed after repeated skips.
- The data bundle must remain external to the portable handoff package.
- Heavy worker outputs and `all_evaluations` files must not be placed into the portable handoff package.
- Optimization output does not claim TradingView release parity.

## Codex UI Can Close During Long Runs

- Status: observed during the worker scaling benchmark.
- Impact: a direct Codex-terminal optimization run can abort if the Codex Windows UI closes or the session is interrupted.
- Evidence: after the UI closure, no active Python benchmark process remained and the benchmark had to be resumed after reopening Codex.
- Mitigation: launch big runs through a detached PowerShell process with heartbeat, checkpoints, `resume_registry.sqlite`, stdout/stderr logs, and status checks.

## Auto Worker Cap Was Too Conservative

- Status: observed.
- Root cause: the auto worker path resolved to `min(max(os.cpu_count() - 1, 1), 6)`.
- Impact: the previous big run used `6` workers despite the system exposing `20` logical CPUs.
- Mitigation: use explicit `--max-workers 16` for the next big resume, keep `16` as the current safe cap, and update runner defaults only after careful review.

## 20+ Worker Not Yet Approved

- Status: not tested and not recommended.
- Reason: the system exposes `20` logical CPUs and `16` is the highest tested safe worker count.
- Risk: `20+` workers may oversubscribe CPU, memory, disk I/O, or SQLite registry write paths.
- Mitigation: require a new worker scaling benchmark before exceeding `16`.

## Background Apps Can Reduce Stability

- Resource-heavy apps can reduce overnight optimization stability by consuming RAM, CPU, disk I/O, GPU/UI resources, or file-sync locks.
- Before a big resume, close or pause Chrome tabs, TradingView, AutoCAD, Excel, Teams, Outlook, OneDrive sync, and unnecessary WebView/Copilot apps.

## Additional Issues Found In Reports

- Throughput was not sufficient to complete 6,615,000 planned split evaluations in 8 hours.
- Failed evaluations count was 33,075 in the completed subset.
- Mixed data source labels exist and must remain preserved in result rows.
