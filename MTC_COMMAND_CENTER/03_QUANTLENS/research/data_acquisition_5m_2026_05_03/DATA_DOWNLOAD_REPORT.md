# DATA DOWNLOAD REPORT

- Mode: `all`.
- Timeframe: `5m`.
- Start: `2024-01-01T00:00:00+00:00`.
- End last closed bar: `2026-05-03T17:20:00+00:00`.
- Symbols downloaded: `17`.
- Total bars: `4105966`.
- Production bundle manifest modified: `false`.
- Timezone: UTC storage; New York session conversion is handled in rerun script.

## Data Quality
- See `DATA_QUALITY_REPORT.csv`.
- Missing candle count is calculated against continuous 5-minute UTC grid between requested start and last closed bar.

## Final Quality Status
- PASS symbols: `16`.
- WARN_MISSING_CANDLES symbols: `1`.
- Warning reason: POLUSDT begins after 2024-01-01 on Binance futures, so continuous-grid missing candles exist before first available bar.
