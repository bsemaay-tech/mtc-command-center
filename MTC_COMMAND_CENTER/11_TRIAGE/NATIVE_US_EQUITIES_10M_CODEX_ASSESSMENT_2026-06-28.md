# Native US-Equities 10m Soak - Codex Assessment

Date: 2026-06-28
Scope: assessment of `11_TRIAGE/_tmp_native_us_equities_10m_audit_2026-06-28/WORKER_REPORT.md`
Target: `QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK`

## Verdict

DeepSeek's main conclusion is accepted: the native US-equities-10m soak cannot be launched from current repo state.

The blocking chain is real:

1. No approved US equities OHLCV provider is wired into the repo.
2. No native US equities 10m OHLCV data was found on disk.
3. The draft run plan has `symbols: []` and `universe.status: needs_freeze`.
4. Existing result evidence for this strategy is crypto proxy / research-only.
5. No native `backtest_profile_result.json` or `top_results.json` can be generated without fabricating evidence.

## Corrections To Worker Report

The report's B6 wording needs tightening.

It says the strategy is "not in `EQUITY_ONLY_STRATEGIES`". Live code shows `EQUITY_ONLY_STRATEGIES` is currently an empty set in `mega_walk_forward.py`, so the precise blocker is:

> Equity-only/session gating is not configured for this strategy yet.

Operational impact is the same: once a real US equities bundle exists, the strategy should be explicitly gated to equity exchanges/session semantics before native soak evidence is trusted.

The B4 timeframe blocker is also secondary rather than critical. `build_run_plan.py` already supports explicit `--timeframes 10m`, and `mega_walk_forward.py` accepts selected timeframes via CLI. The real blocker is that no manifest/data entry exists for `10m`.

## Verified Evidence

- `02_MTC_BACKTEST/backtest_assets/data_catalog.json` contains Binance crypto data only: BTCUSDT, ETHUSDT, BTCUSDT.P; no US equities, no 10m.
- `02_MTC_BACKTEST/data_providers/__init__.py` exposes only `binance`, `binance_usdm`, and `csv` providers.
- `02_MTC_BACKTEST/data_providers/binance_provider.py` maps Binance timeframes only and has no 10m mapping.
- `03_QUANTLENS/tools/mega_walk_forward.py` defaults to 17 crypto symbols and `["15m", "1h", "2h", "4h", "1D"]`.
- `03_QUANTLENS/tools/mega_walk_forward.py` has `EQUITY_ONLY_STRATEGIES: set = set()` and exchange gating only triggers when that set is populated.
- `draft_run_plan_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_2026-06-15/run_plan.json` requests `10m` but has no symbols and blocks approval with `needs_freeze`.
- `NATIVE_RESULT_SOURCE_DISCOVERY_2026-06-16.md` already concluded no native usable result source exists.
- `REPOSITORY_NATIVE_RESULT_READINESS_AUDIT_2026-06-16.md` already classified this target as non-native / research-only.

## Decision Gate

Do not implement a data provider or run a soak until Baris chooses:

1. Provider/source:
   - existing local CSV if Baris already has bars,
   - or an external provider with 10m US equities history.
2. Initial symbol universe:
   - minimum smoke: one symbol such as `SPY` or the original source symbol if known,
   - broader soak: frozen list such as `SPY, QQQ, AAPL, MSFT, NVDA, AMZN, TSLA`, subject to Baris approval.
3. Session policy:
   - regular trading hours only vs extended hours.
4. Price policy:
   - adjusted vs unadjusted OHLCV.
5. Date range:
   - enough bars to satisfy `MIN_BARS_REQUIRED=1500` after session filtering.

## Smallest Safe Next Implementation After Approval

Use a data-first smoke, not a full soak:

1. Create or import a provider-specific adapter or CSV ingestion path for one symbol.
2. Validate the 10m OHLCV file: columns, timezone, first/last timestamp, bar count, gaps, RTH/ETH policy, adjusted/unadjusted policy.
3. Build a small bundle manifest with one symbol and one `10m` timeframe.
4. Run one read-only smoke cell under the normal backtest gates.
5. Only after the smoke passes, expand to the approved frozen universe.

No native artifact should be generated before those steps produce real matching output.

## Status For NEXT_STEPS

Mark the native US-equities-10m soak as:

`BLOCKED - DATA PROVIDER / SYMBOL UNIVERSE REQUIRED`

This is not a dashboard bug and not an artifact-converter bug.
