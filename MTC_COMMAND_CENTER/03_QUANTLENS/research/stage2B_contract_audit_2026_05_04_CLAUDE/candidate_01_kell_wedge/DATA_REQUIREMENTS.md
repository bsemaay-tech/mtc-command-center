# DATA_REQUIREMENTS — Kell Wedge Pop

## Status
- **NEEDS_US_EQUITY_DAILY** (core)
- **NEEDS_RS_DATA** (relative-strength rank vs SPY/QQQ + sector benchmark)
- **NEEDS_FUNDAMENTAL_DATA** (earnings calendar at minimum)
- **NEEDS_MANUAL_LABELS** (theme/in-play sector tags) — *optional but improves fidelity*
- **CURRENT_CRYPTO_DATA_NOT_FAIR** (BTC/ETH/SOL backtest cannot validate or invalidate this strategy)

## Minimum viable dataset
- US equities daily OHLCV+volume, 10–15 year history, top 1000 by avg $-vol.
- SPY daily OHLCV (relative-strength + macro gate).
- Earnings calendar (Zacks / earningswhispers / vendor) for blackout.

## Nice-to-have
- Sector ETF OHLCV (XLK, XLE, XLV, …) for sector RS.
- 30m or 65m bars for execution-TF golden-case spot-checks.
- Theme tag table (e.g. AI 2023+, weight-loss 2023, crypto-equity 2024) for manual leader filter.

## Why crypto proxy fails
1. Kell's edge concentrates in *single-name leadership inside an in-play theme*. Crypto majors are tightly correlated to BTC; "leader" status is degenerate.
2. No earnings catalyst in crypto → kills the post-earnings pullback subset of wedge pops.
3. No US session structure → 65m TF and overnight gap dynamics absent.
4. Position sizing logic (theme leader 30% cap) has no analogue in crypto majors universe.

## Decision rule
Do NOT assign a "FAIL/WEAK" verdict to Kell based on the crypto Stage-2 numbers. Only acceptable verdicts on current data: `PREVIOUS_BACKTEST_NOT_FAIR` and `CONTRACT_NEEDS_NATIVE_DATA`.
