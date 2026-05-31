# Christian Open Range 5% Stop Validation - 2026-05-31

- Strategy: `QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M`
- Cells tested: 6
- Block bootstrap: 10000 resamples, block_size = round(sqrt(lockbox trades))
- Rolling-origin OOS: 5 expanding folds, param re-selected on train from focused grid
- Decision rule from handoff: >=4/6 cells with block_bootstrap p <= 0.10 => propose parity promotion
- Result: 4/6 block-pass, 1/6 block+rolling-pass
- Recommendation: **PROMOTE_TO_PINETS_PARITY_REVIEW**

| Symbol | TF | Params | Trades | Ret % | PF | Focused p | DSR p | Block | Block p | Roll + | Roll avg % | Verdict |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| OPUSDT | 1h | `{"or_bars":3,"stop_pct":0.05,"target_pct":0.15}` | 74 | 94.62 | 1.459 | 0.061 | 0.651 | 9 | 0.07970 | 0/5 | -23.88 | PASS |
| ETHUSDT | 1h | `{"or_bars":3,"stop_pct":0.07,"target_pct":0.25}` | 102 | 94.08 | 1.394 | 0.0715 | 0.5513 | 10 | 0.05990 | 2/5 | -6.17 | PASS |
| NEARUSDT | 4h | `{"or_bars":1,"stop_pct":0.05,"target_pct":0.15}` | 51 | 62.00 | 1.419 | 0.099 | 0.6154 | 7 | 0.12520 | 3/5 | 8.57 | WATCH |
| TRXUSDT | 2h | `{"or_bars":3,"stop_pct":0.07,"target_pct":0.25}` | 55 | 46.96 | 1.497 | 0.0975 | 0.6103 | 7 | 0.03240 | 4/5 | 25.01 | PASS |
| BTCUSDT | 15m | `{"or_bars":1,"stop_pct":0.05,"target_pct":0.15}` | 39 | 14.90 | 1.523 | 0.1185 | 0.5768 | 6 | 0.08310 | 2/5 | -6.71 | PASS |
| BTCUSDT | 4h | `{"or_bars":1,"stop_pct":0.05,"target_pct":0.15}` | 39 | 30.98 | 1.352 | 0.1695 | 0.5322 | 6 | 0.22640 | 2/5 | -4.49 | WATCH |

## Rolling-Origin Fold Detail

### OPUSDT 1h

| Fold | Train ret % | Test ret % | Test trades | Test PF | Params |
|---:|---:|---:|---:|---:|---|
| 1 | -23.72 | -19.40 | 34 | 0.740 | `{"or_bars":3,"stop_pct":0.03,"target_pct":0.1}` |
| 2 | -24.61 | -20.18 | 42 | 0.910 | `{"or_bars":3,"stop_pct":0.05,"target_pct":0.15}` |
| 3 | -33.10 | -20.06 | 46 | 0.805 | `{"or_bars":3,"stop_pct":0.03,"target_pct":0.1}` |
| 4 | -48.17 | -8.65 | 59 | 0.968 | `{"or_bars":3,"stop_pct":0.03,"target_pct":0.1}` |
| 5 | -22.48 | -51.12 | 33 | 0.483 | `{"or_bars":5,"stop_pct":0.05,"target_pct":0.15}` |

### ETHUSDT 1h

| Fold | Train ret % | Test ret % | Test trades | Test PF | Params |
|---:|---:|---:|---:|---:|---|
| 1 | 967.28 | -31.78 | 41 | 0.762 | `{"or_bars":3,"stop_pct":0.07,"target_pct":0.25}` |
| 2 | 611.84 | -13.67 | 42 | 0.965 | `{"or_bars":3,"stop_pct":0.07,"target_pct":0.25}` |
| 3 | 514.15 | 6.45 | 38 | 1.161 | `{"or_bars":3,"stop_pct":0.07,"target_pct":0.25}` |
| 4 | 541.96 | 32.22 | 39 | 1.559 | `{"or_bars":3,"stop_pct":0.07,"target_pct":0.25}` |
| 5 | 746.21 | -24.08 | 37 | 0.758 | `{"or_bars":3,"stop_pct":0.07,"target_pct":0.25}` |

### NEARUSDT 4h

| Fold | Train ret % | Test ret % | Test trades | Test PF | Params |
|---:|---:|---:|---:|---:|---|
| 1 | 157.74 | 39.19 | 19 | 1.758 | `{"or_bars":1,"stop_pct":0.05,"target_pct":0.15}` |
| 2 | 258.73 | -18.41 | 18 | 0.753 | `{"or_bars":1,"stop_pct":0.05,"target_pct":0.15}` |
| 3 | 177.84 | 20.07 | 14 | 1.589 | `{"or_bars":1,"stop_pct":0.05,"target_pct":0.15}` |
| 4 | 233.61 | -19.31 | 21 | 0.781 | `{"or_bars":1,"stop_pct":0.05,"target_pct":0.15}` |
| 5 | 169.19 | 21.29 | 16 | 1.519 | `{"or_bars":1,"stop_pct":0.05,"target_pct":0.15}` |

### TRXUSDT 2h

| Fold | Train ret % | Test ret % | Test trades | Test PF | Params |
|---:|---:|---:|---:|---:|---|
| 1 | 662.20 | 60.41 | 20 | 2.050 | `{"or_bars":3,"stop_pct":0.07,"target_pct":0.25}` |
| 2 | 898.94 | -25.79 | 20 | 0.574 | `{"or_bars":3,"stop_pct":0.07,"target_pct":0.25}` |
| 3 | 641.27 | 22.43 | 21 | 1.586 | `{"or_bars":3,"stop_pct":0.07,"target_pct":0.25}` |
| 4 | 819.75 | 48.66 | 19 | 2.786 | `{"or_bars":3,"stop_pct":0.07,"target_pct":0.25}` |
| 5 | 1164.44 | 19.35 | 18 | 2.006 | `{"or_bars":3,"stop_pct":0.07,"target_pct":0.25}` |

### BTCUSDT 15m

| Fold | Train ret % | Test ret % | Test trades | Test PF | Params |
|---:|---:|---:|---:|---:|---|
| 1 | 0.02 | -6.91 | 14 | 0.683 | `{"or_bars":1,"stop_pct":0.05,"target_pct":0.15}` |
| 2 | -8.59 | -11.60 | 14 | 0.329 | `{"or_bars":1,"stop_pct":0.05,"target_pct":0.15}` |
| 3 | -18.54 | 5.97 | 15 | 2.255 | `{"or_bars":5,"stop_pct":0.05,"target_pct":0.15}` |
| 4 | -11.11 | -21.50 | 17 | 0.199 | `{"or_bars":1,"stop_pct":0.05,"target_pct":0.15}` |
| 5 | -22.67 | 0.48 | 12 | 1.070 | `{"or_bars":5,"stop_pct":0.05,"target_pct":0.15}` |

### BTCUSDT 4h

| Fold | Train ret % | Test ret % | Test trades | Test PF | Params |
|---:|---:|---:|---:|---:|---|
| 1 | 96.83 | -6.01 | 14 | 0.982 | `{"or_bars":3,"stop_pct":0.07,"target_pct":0.25}` |
| 2 | 84.99 | -32.68 | 13 | 0.453 | `{"or_bars":3,"stop_pct":0.07,"target_pct":0.25}` |
| 3 | 59.85 | -14.44 | 14 | 0.682 | `{"or_bars":1,"stop_pct":0.05,"target_pct":0.15}` |
| 4 | 23.50 | 20.33 | 9 | 2.312 | `{"or_bars":1,"stop_pct":0.05,"target_pct":0.15}` |
| 5 | 48.61 | 10.33 | 15 | 1.302 | `{"or_bars":1,"stop_pct":0.05,"target_pct":0.15}` |
