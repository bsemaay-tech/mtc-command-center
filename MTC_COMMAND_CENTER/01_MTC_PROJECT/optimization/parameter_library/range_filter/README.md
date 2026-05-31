# Range Filter Parameter Library

Research seeds only; not Pine defaults; not production parameters.

## Status: POC Active (2026-05-29)

Range Filter local feature parity is PASS as of 2026-05-29:
- `FEATURE_TRACE_PASS` (Python ↔ PineTS)
- `REFERENCE_PASS` — independent reference oracle, 61,327 rows, 0 mismatches
- No TradingView release parity claim; local parity only

## Producer Parameter

The Range Filter producer exposes a single tunable parameter:

| Parameter | Description | Type |
|---|---|---|
| `rf_range` | Band half-width (price units). Must be > 0. | float |

## Seed Regions

`range_filter_seed_regions.yml` — POC initial search bounds.

- 4 regions: BTCUSDT/ETHUSDT × 15m/1h
- Bounds derived from price-relative heuristics (0.3%–1.5% of current asset price)
- `accepted_for_next_stage: false` — no walkforward evidence yet
- `evidence_count: 0` — smoke run has not been executed yet

## Smoke Job

`optimization/jobs/smoke/range_filter_producer_only_seed_smoke.yml`

- Proves the Range Filter producer-only optimization pipeline produces valid
  per-asset/timeframe seed output
- Uses the same `RangeFilterSignal` code path that passed local feature parity
- Does NOT bypass feature parity
- Does NOT claim TradingView release parity

## How To Run The Smoke

```powershell
$env:PYTHONPATH='.;00_PYTHON'
python tools/run_mtc_overnight_optimization.py `
  --job optimization/jobs/smoke/range_filter_producer_only_seed_smoke.yml `
  --out reports/optimization/range_filter_seed_smoke
```

After smoke completes, update `range_filter_seed_regions.yml`:
- Set `evidence_count` to actual evaluation count per region
- Set `accepted_for_next_stage: true` for regions where walkforward consistency ≥ 0.60

## What Not To Do

- Do not reuse Supertrend seed values for Range Filter
- Do not promote regions to `accepted_for_next_stage: true` without walkforward evidence
- Do not claim TradingView release parity from these seeds
- Do not modify Pine defaults based on POC smoke evidence alone
