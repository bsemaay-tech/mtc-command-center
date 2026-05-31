# MEGA Rolling Walk-Forward + Deflated Sharpe + Bootstrap-FDR — Overnight Audit

- Generated: `2026-05-31T04:50:21.335327+00:00`
- Runtime: `66.0s` (1.1 min) with `8` worker processes
- Symbols: 17 | Timeframes: ['15m', '1h', '2h', '4h', '1D']
- Strategies: 8 (11 prototyped + 6 generic patterns)
- Param sets total across grids: **42**
- Total (strategy, symbol, tf) jobs: **680**
- Cost: `8.0 bps` round-trip | Lockbox: last 25% | Rolling folds: 3
- Classification counts: `{'INSUFFICIENT_TRADES': 343, 'PASS': 42, 'FAIL': 257, 'STRONG_PASS': 6, 'NO_DATA': 32}`
- PASS configurations: **48**
- Bootstrap-FDR family size (testable lockboxes): **305** | BH q=0.10 | threshold p≤0.00131
- BH-FDR survivors: **2** | DSR-robust (p≥0.95): **0**
- **FINAL ROBUST (PASS ∧ BH-FDR ∧ DSR): 0**

## Methodology note

Three independent gates must ALL pass for `robust_final`:
1. **Rolling walk-forward** — best param chosen on train folds; profitable on a 25% locked-box OOS slice never seen in selection; positive in ≥ half of forward folds.
2. **Bootstrap significance** — 2000-resample one-sided bootstrap that lockbox mean-R > 0, then **Benjamini-Hochberg FDR (q=0.10)** across ALL testable cells to control multiple-testing.
3. **Deflated Sharpe Ratio** — Bailey & López de Prado, per-trade Sharpe deflated by the expected max across the grid's parameter trials; p ≥ 0.95.

## FINAL ROBUST Survivors (all three gates)

| Strategy | Symbol | TF | Best Params | Lockbox Ret % | Sharpe | Boot p | DSR p | Trades | PF | Max DD % | Folds+ | Class |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| _(none survived all three gates)_ | | | | | | | | | | | | |

## Bootstrap-FDR Survivors (gate 1+2, DSR aside)

| Strategy | Sym | TF | Lockbox Ret % | Sharpe | Boot p | DSR p | Trades | PF | Folds+ | Class |
|---|---|---|---|---|---|---|---|---|---|---|
| `QL_HIGHEST_VOLUME_EDGE_PROSWING_1D` | TRXUSDT | 15m | 65.69 | 1.14 | 0.0 | 0.0006 | 1000 | 1.143 | 1/3 | PASS |
| `QL_DEEPAK_259_RISK_OVERLAY` | TRXUSDT | 4h | 42.22 | 1.33 | 0.001 | 0.5441 | 111 | 1.351 | 3/3 | STRONG_PASS |

## All PASS / STRONG_PASS (no multiplicity filter)

| Strategy | Sym | TF | Lockbox Ret % | Sharpe | Boot p | DSR p | Trades | PF | MaxDD % | Folds+ | Class |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `QL_DEEPAK_SNAPBACK_50SMA_INTRADAY` | TRXUSDT | 2h | 101.11 | 2.41 | 0.0055 | 0.0 | 120 | 1.815 | -11.86 | 3/3 | STRONG_PASS |
| `QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M` | OPUSDT | 1h | 94.62 | 1.44 | 0.061 | 0.651 | 74 | 1.459 | -39.69 | 1/3 | PASS |
| `QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M` | ETHUSDT | 1h | 94.08 | 1.36 | 0.0715 | 0.5513 | 102 | 1.394 | -38.43 | 2/3 | PASS |
| `QL_HIGHEST_VOLUME_EDGE_PROSWING_1D` | TRXUSDT | 15m | 65.69 | 1.14 | 0.0 | 0.0006 | 1000 | 1.143 | -42.01 | 1/3 | PASS |
| `QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M` | NEARUSDT | 4h | 62.00 | 1.17 | 0.099 | 0.6154 | 51 | 1.419 | -34.09 | 1/3 | PASS |
| `QL_HIGHEST_VOLUME_EDGE_PROSWING_1D` | TRXUSDT | 2h | 61.37 | 1.25 | 0.0095 | 0.3592 | 137 | 1.35 | -25.49 | 3/3 | STRONG_PASS |
| `QL_DEEPAK_SNAPBACK_50SMA_INTRADAY` | LTCUSDT | 1h | 55.04 | 1.35 | 0.1345 | 0.0 | 80 | 1.506 | -13.51 | 1/3 | PASS |
| `QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M` | BNBUSDT | 1h | 49.66 | 1.05 | 0.1045 | 0.4182 | 107 | 1.278 | -31.73 | 2/3 | PASS |
| `QL_DEEPAK_153_FILTER_1D` | SOLUSDT | 2h | 48.06 | 1.32 | 0.0125 | 0.478 | 54 | 1.541 | -15.36 | 3/3 | STRONG_PASS |
| `QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M` | TRXUSDT | 2h | 46.96 | 1.19 | 0.0975 | 0.6103 | 55 | 1.497 | -17.00 | 3/3 | STRONG_PASS |
| `QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M` | TRXUSDT | 15m | 43.05 | 1.01 | 0.043 | 0.0788 | 397 | 1.156 | -34.66 | 3/3 | PASS |
| `QL_DEEPAK_259_RISK_OVERLAY` | TRXUSDT | 4h | 42.22 | 1.33 | 0.001 | 0.5441 | 111 | 1.351 | -15.05 | 3/3 | STRONG_PASS |
| `QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M` | TRXUSDT | 1h | 41.90 | 1.01 | 0.111 | 0.3942 | 111 | 1.285 | -27.72 | 2/3 | PASS |
| `QL_DEEPAK_SNAPBACK_50SMA_INTRADAY` | OPUSDT | 1h | 39.54 | 1.03 | 0.013 | 0.0 | 125 | 1.239 | -22.95 | 2/3 | PASS |
| `QL_DEEPAK_259_RISK_OVERLAY` | TRXUSDT | 1h | 38.42 | 0.98 | 0.0065 | 0.0463 | 528 | 1.12 | -26.80 | 3/3 | PASS |
| `QL_DEEPAK_153_FILTER_1D` | ETHUSDT | 2h | 38.19 | 1.11 | 0.021 | 0.1993 | 110 | 1.284 | -17.91 | 2/3 | PASS |
| `QL_DEEPAK_153_FILTER_1D` | XRPUSDT | 4h | 37.91 | 0.98 | 0.1915 | 0.4711 | 32 | 1.568 | -31.09 | 1/3 | PASS |
| `QL_DEEPAK_SNAPBACK_50SMA_INTRADAY` | LTCUSDT | 2h | 35.02 | 0.86 | 0.283 | 0.0009 | 42 | 1.475 | -17.88 | 1/3 | PASS |
| `QL_DEEPAK_SNAPBACK_50SMA_INTRADAY` | OPUSDT | 2h | 32.86 | 1.03 | 0.0215 | 0.0087 | 31 | 1.56 | -15.22 | 1/3 | PASS |
| `QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M` | ETHUSDT | 2h | 32.53 | 0.75 | 0.2175 | 0.4326 | 57 | 1.261 | -43.76 | 3/3 | PASS |
| `QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M` | BTCUSDT | 4h | 30.98 | 0.84 | 0.1695 | 0.5322 | 39 | 1.352 | -32.40 | 2/3 | PASS |
| `QL_HIGHEST_VOLUME_EDGE_PROSWING_1D` | ETHUSDT | 2h | 29.03 | 0.70 | 0.105 | 0.1286 | 178 | 1.144 | -44.74 | 2/3 | PASS |
| `QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M` | SOLUSDT | 2h | 28.90 | 0.70 | 0.229 | 0.4224 | 54 | 1.237 | -31.70 | 3/3 | PASS |
| `QL_DEEPAK_SNAPBACK_50SMA_INTRADAY` | NEARUSDT | 2h | 26.70 | 0.78 | 0.2945 | 0.0016 | 37 | 1.372 | -22.65 | 2/3 | PASS |
| `QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M` | LTCUSDT | 4h | 23.77 | 0.68 | 0.2235 | 0.4489 | 44 | 1.248 | -37.34 | 1/3 | PASS |
| `QL_DEEPAK_SNAPBACK_50SMA_INTRADAY` | TRXUSDT | 4h | 20.81 | 0.93 | 0.0285 | 0.0041 | 34 | 1.497 | -13.58 | 3/3 | STRONG_PASS |
| `QL_DEEPAK_SNAPBACK_50SMA_INTRADAY` | TRXUSDT | 1h | 20.36 | 0.98 | 0.3085 | 0.0 | 94 | 1.369 | -16.33 | 3/3 | PASS |
| `QL_DEEPAK_153_FILTER_1D` | ETHUSDT | 4h | 19.29 | 0.66 | 0.1875 | 0.3037 | 40 | 1.283 | -26.26 | 2/3 | PASS |
| `QL_HIGHEST_VOLUME_EDGE_PROSWING_1D` | TRXUSDT | 1h | 18.88 | 0.57 | 0.06 | 0.0156 | 390 | 1.099 | -45.20 | 3/3 | PASS |
| `QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M` | OPUSDT | 2h | 15.63 | 0.52 | 0.284 | 0.4271 | 34 | 1.22 | -42.52 | 2/3 | PASS |
| `QL_DEEPAK_153_FILTER_1D` | DOGEUSDT | 15m | 15.30 | 0.54 | 0.2395 | 0.0 | 589 | 1.056 | -45.26 | 1/3 | PASS |
| `QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M` | BTCUSDT | 15m | 14.90 | 0.96 | 0.1185 | 0.5768 | 39 | 1.523 | -10.17 | 1/3 | PASS |
| `QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M` | ARBUSDT | 1h | 13.93 | 0.52 | 0.25 | 0.2652 | 89 | 1.123 | -25.71 | 3/3 | PASS |
| `QL_DEEPAK_259_RISK_OVERLAY` | ETHUSDT | 4h | 13.29 | 0.49 | 0.148 | 0.2505 | 102 | 1.116 | -47.75 | 2/3 | PASS |
| `QL_DEEPAK_SNAPBACK_50SMA_INTRADAY` | BNBUSDT | 4h | 12.86 | 0.52 | 0.371 | 0.0001 | 51 | 1.192 | -17.44 | 3/3 | PASS |
| `QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M` | BNBUSDT | 4h | 12.60 | 0.47 | 0.303 | 0.4242 | 30 | 1.222 | -31.02 | 2/3 | PASS |
| `QL_DEEPAK_153_FILTER_1D` | BNBUSDT | 4h | 11.00 | 0.48 | 0.088 | 0.1984 | 51 | 1.167 | -28.36 | 3/3 | PASS |
| `QL_DEEPAK_153_FILTER_1D` | BNBUSDT | 2h | 8.68 | 0.42 | 0.0285 | 0.0438 | 131 | 1.095 | -22.89 | 3/3 | PASS |
| `QL_DEEPAK_SNAPBACK_50SMA_INTRADAY` | SOLUSDT | 2h | 8.51 | 0.41 | 0.228 | 0.0 | 124 | 1.096 | -31.27 | 1/3 | PASS |
| `QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M` | TRXUSDT | 4h | 6.49 | 0.35 | 0.3375 | 0.3761 | 30 | 1.166 | -34.57 | 3/3 | PASS |
| `QL_DEEPAK_153_FILTER_1D` | BTCUSDT | 4h | 6.26 | 0.38 | 0.257 | 0.1939 | 45 | 1.14 | -17.05 | 3/3 | PASS |
| `QL_DEEPAK_153_FILTER_1D` | TRXUSDT | 4h | 4.64 | 0.30 | 0.034 | 0.1386 | 56 | 1.103 | -30.85 | 3/3 | PASS |
| `QL_DEEPAK_153_FILTER_1D` | ARBUSDT | 1h | 3.85 | 0.27 | 0.268 | 0.1166 | 62 | 1.086 | -26.71 | 2/3 | PASS |
| `QL_HIGHEST_VOLUME_EDGE_PROSWING_1D` | BTCUSDT | 4h | 3.65 | 0.30 | 0.251 | 0.2069 | 66 | 1.096 | -35.67 | 2/3 | PASS |
| `QL_DEEPAK_259_RISK_OVERLAY` | BTCUSDT | 2h | 2.79 | 0.24 | 0.279 | 0.2117 | 81 | 1.061 | -18.23 | 2/3 | PASS |
| `QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M` | SOLUSDT | 4h | 2.68 | 0.31 | 0.3975 | 0.3507 | 33 | 1.123 | -36.15 | 3/3 | PASS |
| `QL_DEEPAK_259_RISK_OVERLAY` | ETHUSDT | 2h | 0.35 | 0.31 | 0.237 | 0.0694 | 239 | 1.046 | -48.05 | 3/3 | PASS |
| `QL_DEEPAK_SNAPBACK_50SMA_INTRADAY` | APTUSDT | 1h | 0.21 | 0.18 | 0.168 | 0.0 | 115 | 1.045 | -29.76 | 3/3 | PASS |

## Per-Strategy Top 3 PASS configurations

### `QL_DEEPAK_153_FILTER_1D`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| SOLUSDT | 2h | `{"sma_fast":50,"sma_slow":200,"trigger_ema":21,"stop_lookback":10}` | 48.06 | 1.32 | 0.478 | 54 | 1.541 | 3/3 |
| ETHUSDT | 2h | `{"sma_fast":50,"sma_slow":200,"trigger_ema":8,"stop_lookback":5}` | 38.19 | 1.11 | 0.1993 | 110 | 1.284 | 2/3 |
| XRPUSDT | 4h | `{"sma_fast":50,"sma_slow":200,"trigger_ema":13,"stop_lookback":5}` | 37.91 | 0.98 | 0.4711 | 32 | 1.568 | 1/3 |

### `QL_DEEPAK_259_RISK_OVERLAY`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| TRXUSDT | 4h | `{"entry_ema":21,"risk_pct":0.01,"stop_atr":1.5,"stop_lookback":10}` | 42.22 | 1.33 | 0.5441 | 111 | 1.351 | 3/3 |
| TRXUSDT | 1h | `{"entry_ema":8,"risk_pct":0.01,"stop_atr":2.0,"stop_lookback":10}` | 38.42 | 0.98 | 0.0463 | 528 | 1.12 | 3/3 |
| ETHUSDT | 4h | `{"entry_ema":21,"risk_pct":0.01,"stop_atr":1.5,"stop_lookback":10}` | 13.29 | 0.49 | 0.2505 | 102 | 1.116 | 2/3 |

### `QL_DEEPAK_SNAPBACK_50SMA_INTRADAY`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| TRXUSDT | 2h | `{"sma_len":50,"dist_atr":1.0,"stop_lookback":5,"target_atr":1.0}` | 101.11 | 2.41 | 0.0 | 120 | 1.815 | 3/3 |
| LTCUSDT | 1h | `{"sma_len":50,"dist_atr":3.0,"stop_lookback":15,"target_atr":2.0}` | 55.04 | 1.35 | 0.0 | 80 | 1.506 | 1/3 |
| OPUSDT | 1h | `{"sma_len":50,"dist_atr":2.0,"stop_lookback":10,"target_atr":1.0}` | 39.54 | 1.03 | 0.0 | 125 | 1.239 | 2/3 |

### `QL_HIGHEST_VOLUME_EDGE_PROSWING_1D`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| TRXUSDT | 15m | `{"vol_lookback":60,"trend_ema":50,"stop_lookback":10}` | 65.69 | 1.14 | 0.0006 | 1000 | 1.143 | 1/3 |
| TRXUSDT | 2h | `{"vol_lookback":60,"trend_ema":50,"stop_lookback":10}` | 61.37 | 1.25 | 0.3592 | 137 | 1.35 | 3/3 |
| ETHUSDT | 2h | `{"vol_lookback":60,"trend_ema":50,"stop_lookback":5}` | 29.03 | 0.70 | 0.1286 | 178 | 1.144 | 2/3 |

### `QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M`

| Sym | TF | Params | Lockbox Ret % | Sharpe | DSR p | Trades | PF | Folds+ |
|---|---|---|---|---|---|---|---|---|
| OPUSDT | 1h | `{"or_bars":3,"stop_pct":0.05,"target_pct":0.15}` | 94.62 | 1.44 | 0.651 | 74 | 1.459 | 1/3 |
| ETHUSDT | 1h | `{"or_bars":3,"stop_pct":0.07,"target_pct":0.25}` | 94.08 | 1.36 | 0.5513 | 102 | 1.394 | 2/3 |
| NEARUSDT | 4h | `{"or_bars":1,"stop_pct":0.05,"target_pct":0.15}` | 62.00 | 1.17 | 0.6154 | 51 | 1.419 | 1/3 |

