# QuantLens data bundles — inventory

Discoverable index of OHLCV data available to the QuantLens engine (`mega_walk_forward.py`).
Any agent: read this before assuming "no data exists" for a symbol/timeframe.

## How the engine consumes data

`mega_walk_forward.py` loads ONE bundle manifest, chosen by env var:

```
$env:MEGA_BUNDLE_MANIFEST = "<path>\manifests\dataset_manifest.json"
```

Manifest contract (per dataset entry): `symbol`, `timeframe_normalized`, `exchange`,
`ohlcv_validation_status` (must be `"PASS"`), `normalized_path` (relative to the bundle root,
i.e. manifest's grandparent dir). Normalized CSV columns: `timestamp_utc,open,high,low,close`
(volume optional — the 8EMA/most strategies use OHLC only). Symbols/timeframes are further
filtered by `--symbol` / `--tf` CLI flags.

## Native bundles in this folder (`03_QUANTLENS/data/`)

| Bundle dir | Symbols | TF | Bars | Source | Validation | Notes |
|---|---|---|---|---|---|---|
| `native_us_equities_10m_us3_tradingview_2026-06-28/` | SPY, QQQ, AAPL | 10m | 20,094 each | TradingView Chart Data export (`BATS:`) | PASS | **Use this one for US-equities 10m.** RTH-only XNYS, no volume, adjustment unknown. 2024-06-03 → 2026-06-26. |
| `native_us_equities_10m_spy_tradingview_2026-06-28/` | SPY | 10m | 20,094 | same | PASS | SPY-only superset-subset of the us3 bundle; kept for provenance. Prefer us3. |

Raw consolidated source CSVs (pre-normalization) live in
`00_INBOX/USER_INTAKE/` (`SPY_10m_tradingview__*.csv`, `BATS_QQQ_10m_CONSOLIDATED_*.csv`,
`BATS_AAPL_10m_CONSOLIDATED_*.csv` + `*_CONSOLIDATION_REPORT.json`). Do not delete.

### Reuse for other strategies

Any engine strategy can run on these bundles — just point `MEGA_BUNDLE_MANIFEST` at the manifest
and pass `--strategy <id> --symbol SPY|QQQ|AAPL --tf 10m`. Already tested 2026-06-28: the 8EMA
family + 15 other distinct strategies — **none robust on this window** (see
`11_TRIAGE/US_EQUITIES_10M_MULTI_STRATEGY_SWEEP_2026-06-28.md`). Data is fine; strategies don't
transfer. New/custom strategy logic is the open path.

## Crypto data (elsewhere in repo — for reference)

| Location | Symbols | TF | Format |
|---|---|---|---|
| `02_MTC_BACKTEST/data/` (catalog: `02_MTC_BACKTEST/backtest_assets/data_catalog.json`) | BTCUSDT, ETHUSDT, BTCUSDT.P | 5m–1d | Parquet (Binance via ccxt) |
| `03_QUANTLENS/research/data_acquisition_5m_2026_05_03/normalized/binance_futures/` | 17 USDT pairs | 5m | CSV |
| `C:\LAB\_MTC_V2_REPO_CLEANUP_ARCHIVE_20260529\...\MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427\` | 17 crypto pairs | 15m–1D | CSV bundle (engine default manifest) |

> `02_MTC_BACKTEST/` is protected scope — read its catalog, do not edit it without Barış approval.

## Adding a new native bundle

1. Validate raw CSV (timestamps monotonic/unique, OHLC sanity, gaps, session policy).
2. Write `normalized/<SYMBOL>_<TF>.csv` with `timestamp_utc,open,high,low,close`.
3. Write `manifests/dataset_manifest.json` per the contract above (`ohlcv_validation_status:"PASS"` only if real).
4. Add a row to this README so other agents can find it.
