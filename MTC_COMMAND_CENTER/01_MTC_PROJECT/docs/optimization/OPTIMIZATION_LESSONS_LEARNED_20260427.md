# Optimization Lessons Learned - 2026-04-27

## Scope

This document preserves research lessons from the recent MTC V2 optimization sequence. These observations are not production parameters and do not authorize Pine default changes.

## Stage 1 - Single Dataset

- Scale: 822 variants.
- Purpose: prove that local optimizer plumbing can run parameter sweeps on one dataset.
- Improvement gained: basic ranking and result output became useful enough to guide a wider search.
- Limitation: single-dataset output cannot be called robust and cannot support production promotion.

## Stage 2 - BTC Multi-Timeframe

- Scale: 23,730 evaluations.
- Purpose: move from one dataset to multiple BTC timeframes and walk-forward scoring.
- Improvement gained: timeframe sensitivity became visible and result rows gained stronger metadata.
- Limitation: still single-symbol, so cross-market robustness remained unproven.

## Stage 3 - Multi-Asset Overnight

- Scale: 168,337 completed evaluations out of 6,615,000 planned evaluations.
- Selected assets: ADAUSDT, AVAXUSDT, BNBUSDT, BTCUSDT, DOGEUSDT, ETHUSDT, SOLUSDT, XRPUSDT.
- Selected timeframes: 15m, 1h, 2h, 4h, 1D.
- Improvement gained: cross-asset, cross-timeframe, regime-aware reporting and resume/de-dup infrastructure were exercised on real output.
- Limitation: exhaustive core grid did not finish within the time budget.

## Why Strict Robust Candidate Count Is Still Zero

- The run completed only 321 of 12,600 unique parameter variants.
- The completed subset found 144 medium robust candidates but 0 strict robust candidates.
- Strict promotion requires positive train, validation, and test behavior, enough walk-forward consistency, enough positive symbols and timeframes, and no regime collapse.
- 1D had very weak test-positive coverage compared with intraday timeframes.
- CHOPPY and CONSOLIDATING regimes had negative aggregate PnL.

## Observed Parameter Regions

- `st_factor` around 3.0 to 4.5 appears frequently in higher-ranked research/medium rows.
- `global_atr_length` around 7, 10, and 14 appears frequently, with 21 also present in some medium rows.
- `sl_atr_mult` around 2.75 to 3.5 appears frequently.
- `tp_mode=R` and `tp_mode=None` both remain research-observed surfaces.
- `risk_long` lower than `risk_short` often appeared in candidates, especially in top medium rows.

## Worker Scaling Benchmark Lesson

- The previous 6-worker overnight run used 6 workers because the auto worker path was capped, not because the hardware maximum was 6.
- The auto path resolved to `min(max(os.cpu_count() - 1, 1), 6)`.
- The benchmark machine exposes 20 logical CPUs on an Intel i7-13700H with 14 cores and about 34 GB RAM.
- Worker counts `4`, `6`, `8`, `10`, `12`, and `16` were benchmarked on the same taskset.
- `16` workers produced the best stable tested throughput at about `5.683654` eval/sec.
- The `16` worker run had `0` failed evaluations, `0` duplicate conflicts, and a passing resume/de-dup concurrency check.
- `20+` workers are not recommended until a new benchmark proves they are safe on the same hardware and workload.
- `16` workers should be the explicit default for the next big resume.

## Codex UI Closure Lesson

- The Codex Windows UI closed during the worker scaling benchmark.
- After the UI closure, no active Python benchmark process was found.
- The benchmark command had been aborted and had to be resumed after Codex was reopened.
- Future big runs must not depend on the Codex UI staying open.
- Long optimization must be launched as a detached PowerShell process.
- Heartbeat, checkpoint output, stdout/stderr logs, and `resume_registry.sqlite` are mandatory for overnight work.

## Resource Preparation Lesson

- Before a big resume, close or pause resource-heavy applications: Chrome tabs, TradingView, AutoCAD, Excel, Teams, Outlook, OneDrive sync, and unnecessary WebView/Copilot apps.
- The goal is to free RAM, CPU, and disk I/O while reducing UI crash, app hang, sync-lock, and Windows background interruption risk.

## Permanent Rules From This Run

- Treat all listed parameter regions as research observations only.
- Do not write medium candidates into Pine defaults.
- Do not change `01_PINE/MTC_V2.pine` from optimization output.
- Do not claim TradingView release parity from Python optimizer output.
- Resume the same exhaustive core grid before drawing stronger conclusions.

## Search-Space Reduction Lesson

- The big grid showed that exhaustive producer/exit/risk crossing is too expensive to remain the default for new feature/filter research.
- Future work must first isolate producer-only seed regions, then refine exits/risk, then evaluate filters/gates, then address regimes.
- The reusable parameter library is now the research seed source.
- Medium robust candidates are research seeds only and must not change Pine defaults.
- See `docs/optimization/SEARCH_SPACE_REDUCTION_AND_SMART_SAMPLING.md` and `optimization/parameter_library/README.md`.

## Per-Asset/Timeframe Granularity Lesson

- Aggregate candidate rankings preserve broad research signal, but they hide which asset/timeframe produced or failed the result.
- Exit/risk and filter/gate refinement must start from per-asset/per-timeframe seeds, otherwise weak local behavior can be masked by aggregate averages.
- A tiny Supertrend smoke proved the granular ranking/extraction path and updated the parameter library with smoke-level asset/timeframe rows.
- Smoke seeds remain research-only and cannot justify Pine default changes.
