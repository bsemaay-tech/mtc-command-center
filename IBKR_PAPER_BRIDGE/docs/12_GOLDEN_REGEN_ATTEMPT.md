# T12 Golden Regeneration Attempt - 2026-07-12

Status: **BLOCKED; provisional golden retained.**

## Data validation

- Manifest: `MTC_COMMAND_CENTER/03_QUANTLENS/data/native_multiasset_alpaca_2026-06-28/manifests/dataset_manifest.json`
- Dataset: `BTCUSD`, `1h`, `CRYPTO`, validation `PASS`
- Physical CSV: `normalized/BTCUSD_1h.csv`
- Actual disk rows: 48,077 bars (48,078 lines including header)
- Actual first bar: `2021-01-01 06:00:00+00:00`
- Actual last bar: `2026-06-28 00:00:00+00:00`

## Exact attempt

Environment:

- `MEGA_BUNDLE_MANIFEST` = primary multi-asset manifest above
- `MEGA_OUTPUT_DIR` = `IBKR_PAPER_BRIDGE/data/golden_quantlens_attempt_20260712`
- `MEGA_EXIT_MODES` = `trail_ema8`

Command:

```powershell
python MTC_COMMAND_CENTER\03_QUANTLENS\tools\mega_walk_forward.py --strategy keltner_trail_ema8 --symbol BTCUSD --tf 1h
```

Result (exit 1, before any run):

```text
Unknown strategy id(s): ['keltner_trail_ema8']
```

## Why no substitute was used

The engine registers `GEN_KELTNER_BREAKOUT`, but it is not signal-equivalent to the bridge subject:
it uses an EMA midline, EMA-200 filter, long-only crossover semantics, and a five-bar-low stop. The
bridge subject uses prior-window Keltner bands, two-sided breakout state changes, and the opposite
band as the initial stop. Running `GEN_KELTNER_BREAKOUT` and labeling it as bridge parity would
fabricate evidence.

`tests/fixtures/golden_signals.json` therefore remains marked `provisional: true`, and
`golden_run_id` remains `PROVISIONAL_SYNTHETIC_REFERENCE_2026-07-06`. A real golden requires first
registering the exact bridge signal rules as a read-only QuantLens strategy or adding an approved
source-engine export path.
