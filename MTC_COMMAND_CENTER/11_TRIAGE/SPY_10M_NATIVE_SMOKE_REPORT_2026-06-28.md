# SPY 10m Native Smoke — Report

**Date:** 2026-06-28
**Author:** Claude Opus 4.8
**Classification:** **SMOKE ONLY / NOT PROMOTABLE**
**Strategy:** `QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK`
**Symbol / TF:** SPY / 10m
**Data source:** TradingView CSV → normalized native bundle (first-ever native US-equities 10m run for this strategy)

---

## What ran

The smallest possible cell: **1 strategy × 1 symbol × 1 timeframe**, 75 parameter trials, 1 worker.

```powershell
$env:MEGA_BUNDLE_MANIFEST = "...\native_us_equities_10m_spy_tradingview_2026-06-28\manifests\dataset_manifest.json"
$env:MEGA_OUTPUT_DIR      = "...\native_us_equities_10m_spy_tradingview_2026-06-28\smoke_output_2026-06-28"
$env:MEGA_WORKERS         = "1"
python MTC_COMMAND_CENTER\03_QUANTLENS\tools\mega_walk_forward.py `
  --strategy QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK --symbol SPY --tf 10m
```

`MEGA_OUTPUT_DIR` was overridden so **no output landed in `05_BACKTEST_RESULTS`** — all smoke artifacts are contained inside the bundle's `smoke_output_2026-06-28/` folder. Engine code was **not** modified (output dir is a supported env override).

- Exit code: 0
- Runtime: 3.7s
- jobs = 1, results = 1, passes = 0

## Bundle used

`03_QUANTLENS/data/native_us_equities_10m_spy_tradingview_2026-06-28/`
- `normalized/BATS_SPY_10m.csv` — `timestamp_utc,open,high,low,close`, 20,094 bars, sha256 `821ea9fb874bc1a12ef532c9c5b9f62529f941d172fc7a7cb8ccbf35ab3578d3`
- `manifests/dataset_manifest.json` — `symbol=SPY`, `exchange=BATS`, `timeframe_normalized=10m`, `ohlcv_validation_status=PASS`, `volume_available=false`, `adjustment_policy=unknown_tradingview_export`, `session_policy_inferred=RTH_ONLY_XNYS...`

## Output artifacts (in `smoke_output_2026-06-28/`)

- `MEGA_walk_forward_results.json` (real result, 1 row)
- `MEGA_walk_forward_report.md`
- `MEGA_walk_forward_partial.json`
- `MEGA_walk_forward_checkpoint.pkl`

## Result (real, not fabricated)

| Metric | Value |
|---|---|
| Classification | **INSUFFICIENT_TRADES** |
| Data rows | 20,094 (2024-06-03 → 2026-06-26) |
| Best params | pullback_atr=0.3, impulse_atr=1.6, slope_window=3 |
| Lockbox OOS trades | 17 (< 30 required for PASS) |
| Lockbox win rate | 29.4% |
| Lockbox net return | **−0.773%** |
| Lockbox profit factor | 0.684 |
| Lockbox Sharpe | −0.66 |
| Buy & hold (lockbox) | +8.90% |
| EMA benchmark (lockbox) | +6.06% |
| Walk-forward test folds | 2 folds, both negative (−1.024%, −0.774%) |
| DSR p-value | 0.2628 |
| `dsr_robust` / `bh_fdr_survivor` / `robust_final` | false / false / false |

## Interpretation

- The pipeline works end-to-end on **native** SPY 10m data — data load, signal build, walk-forward folds, lockbox OOS, DSR, regime breakdown all executed on real bars. This closes the "no native data → no soak" infrastructure blocker for SPY.
- The **strategy result is weak/negative** on SPY 10m: 17 lockbox trades (below the 30-trade floor → `INSUFFICIENT_TRADES`), net negative, well below buy & hold. This is research signal only — it does **not** mean promote or reject; it means a single symbol over this window produced too few trades to judge.

## Explicitly NOT generated (per safety rails)

- ❌ `backtest_profile_result.json` — result row is `INSUFFICIENT_TRADES` (not a usable promotable row). Not created.
- ❌ `top_results.json` — requires a multi-row same-bucket result set; a one-symbol one-row smoke cannot produce one. Not created.
- ❌ No Pine / MTC_V2 / parity / engine-logic / broker edits.

## Addendum — 3-symbol smoke (SPY + QQQ + AAPL), Barış-approved 2026-06-28

QQQ + AAPL TradingView 10m exports validated PASS (identical clean structure to SPY: 20,094 bars each, 0 dups/gaps/OHLC-fails, RTH-only, no volume). New bundle: `03_QUANTLENS/data/native_us_equities_10m_us3_tradingview_2026-06-28/` (3 normalized CSVs + 1 manifest, `universe=[SPY,QQQ,AAPL]`). Smoke: `--symbol SPY --symbol QQQ --symbol AAPL --tf 10m`, 3 cells × 75 trials, output redirected, exit 0, 9.6s.

| Symbol | Classification | Lockbox trades | Win | Net % | PF | Buy&hold % | robust_final |
|---|---|---|---|---|---|---|---|
| SPY | INSUFFICIENT_TRADES | 17 | 29.4% | −0.773 | 0.684 | +8.90 | false |
| QQQ | INSUFFICIENT_TRADES | 11 | 18.2% | −1.934 | 0.171 | +16.33 | false |
| AAPL | FAIL | 53 | 37.7% | −0.032 | 1.007 | +3.91 | false |

**Still SMOKE ONLY / NOT PROMOTABLE.** Pipeline confirmed end-to-end on native US-equities 10m across 3 symbols. The 8-EMA-pullback strategy does not hold on this 2024-06→2026-06 window for any of the three (all net-negative, all below buy&hold, 0 robust). No profile/top_results artifact generated.

## Next human decision (Barış)

To move from SMOKE toward a real native evaluation:
1. Approve a **multi-symbol** 10m universe (e.g. add QQQ + AAPL — both already consolidated in `00_INBOX/USER_INTAKE/`) and export the remaining liquid names.
2. Decide whether to **configure equity-session/exchange gating** (`EQUITY_ONLY_STRATEGIES`) for this strategy before trusting native evidence — a protected-scope engine change requiring approval.
3. Decide adjustment policy (adjusted vs raw) for the TradingView exports.
4. Only after a multi-symbol bundle + frozen run plan is approved → run a real (still pre-Gate-2) soak.
