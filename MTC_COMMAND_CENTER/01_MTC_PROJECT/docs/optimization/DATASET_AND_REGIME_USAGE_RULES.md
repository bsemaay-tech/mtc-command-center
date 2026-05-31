# Dataset And Regime Usage Rules

## 2026-04-28 Optimization Consolidation

- The approved optimization bundle is external: `C:\LAB\tradingview-lab\MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427`.
- Bundle reports confirm 93 datasets, 17 assets, 4,477,626 rows, and timeframes `15m`, `1h`, `2h`, `4h`, `1D`.
- Optimizer continuation must use bundle manifests and regime registry files, not direct CSV scans.
- Preserve `dataset_id`, `source_type`, and `evaluation_key` in every result row.
- Do not put the data bundle into the portable handoff zip.
- Optimization output does not claim TradingView release parity.

## 1. Source Of Truth

- Optimizers must use the optimization bundle manifest: `dataset_manifest.yml` or its JSON equivalent.
- Optimizers must reference datasets by `dataset_id`, not by hardcoded CSV paths.
- Every run result must record `dataset_id`, `source_type`, `sha256_raw` or `sha256_normalized`, symbol, timeframe, and date range.
- Direct scans of `ARŞİV` are allowed only when creating or updating a manifest.

## 2. Data Source Labels

- `binance_public_futures_klines`: Binance USD-M Futures public kline chart data; acceptable for broad optimization research.
- `tradingview_chart_csv_binance`: TradingView chart CSV for Binance symbols; acceptable only when source-labeled separately.
- `tradingview_strategy_tester_xlsx`: Strategy Tester workbook/audit artifact; forbidden as chart data.
- `downloaded_ccxt`: Exchange data downloaded through a CCXT-style provider; requires explicit source and hash metadata.
- `unknown_csv`: CSV with unclear source; blocked for optimization unless explicitly approved with `allow_unknown_source=true`.

## 3. Hard Prohibitions

- Do not treat XLSX Strategy Tester workbooks as chart data.
- Do not mix TradingView chart CSV and Binance public data without preserving `source_type`.
- Do not use `unknown_csv` for optimization unless explicitly approved.
- Do not call a single-symbol optimization robust.
- Do not claim release parity from optimization bundle data.

## 4. Regime Usage

- Optimizers must use `regime_registry.yml` or `regime_registry.json` when regime files are available.
- Every robust-candidate report must include performance by `TRENDING`, `RANGING`, `CONSOLIDATING`, and `CHOPPY`.
- Regime classification is a diagnostic helper, not market truth.
- Regime features must use only historical rolling windows ending at or before the current bar; no future leakage is allowed.

## 5. Walk-Forward Requirement

- Optimization must use train/validation/test splits.
- Result rows must include split-level metrics.
- A candidate must not be promoted if only OOS/test is positive while train or validation is weak.

## 6. Cross-Market Requirement

- A candidate is not robust unless tested across multiple symbols.
- If only one symbol is available, reports must mark `INSUFFICIENT_SYMBOL_COVERAGE`.
- Single-symbol output may be research-ranked but cannot be production-robust.

## 7. Cross-Timeframe Requirement

- Candidates should be tested across `15m`, `1h`, `2h`, and `4h` where available.
- `1D` can be separate if the strategy profile is not designed for daily bars.
- Missing timeframes must be reported explicitly.

## 8. Data Quality Requirement

- Verify SHA256 before running optimization.
- Reject datasets with fatal OHLCV errors.
- Warn on gaps and duplicate timestamps.
- Preserve quality report paths in final optimization reports.

## 9. Portable Handoff Rule

- Large optimization data bundles live outside `MTC_V2_PORTABLE_HANDOFF`.
- The portable handoff package should contain rules, schemas, examples, and code, not the full data archive.
