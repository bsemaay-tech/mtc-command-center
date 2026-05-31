# FINAL_STRATEGY_CONTRACT — Slingshot

| # | Field | Value |
|---|---|---|
| 1 | Candidate ID | `SLINGSHOT_EMA_HIGH_4_PULLBACK_v1_CONTRACT` |
| 2 | Source file | `2026-05-03_c7ZSb2wNcOc_quantlens_detailed_intake.md` |
| 3 | Source URL | https://youtu.be/c7ZSb2wNcOc |
| 4 | Strategy family | trend_pullback_resumption |
| 5 | Native market | Equities (primary); crypto majors only as exploratory secondary |
| 6 | Native timeframe | 1D primary; 1h/4h/weekly optional |
| 7 | Minimum data required | OHLC daily |
| 8 | Tradable universe | Liquid uptrending equities; or crypto majors with explicit "exploratory" tag |
| 9 | Setup context | Prior strength: close > SMA50 OR close > SMA200 OR 20-day return > 10% OR within 5% of 20-day high. Plus at least one bar in last [3,5,8,13] closed below EMA(high,4). Pullback depth from rolling-N high ≤ 15% |
| 10 | Entry trigger | Fresh cross-up: today close > EMA(high,4) AND yesterday close ≤ EMA(high,4) |
| 11 | Confirmation | Optional volume ≥ SMA(volume,20) |
| 12 | Filters | Optional EMA200 / SMA200 trend gate; market regime SPY > SPY_EMA200 (equities) |
| 13 | Initial stop | min(pullback_low_N, trigger_bar_low) OR close − 2*ATR(14) |
| 14 | Profit target | None default; sweep {none, 2R, 3R, ATR_trail, close-below-EMAH4} |
| 15 | Time stop | Optional 8-bar no-progress exit |
| 16 | Exit rules | Default: close < EMA(high, 4). Variants: ATR-2 trail, fixed R, time stop |
| 17 | Position sizing | Risk-based 0.5–1% per trade |
| 18 | Do-not-trade | No prior-strength condition; pullback depth > 15%; broad-market downtrend (SPY < EMA200 for equities) |
| 19 | Ambiguities | Pullback lookback length; depth threshold; prior-strength criterion combination; exit mode |
| 20 | Mechanical confidence | 5 / 5 |
| 21 | Data confidence | 4 / 5 (current crypto bundle suffices for *exploratory*; equity bundle preferred for verdict) |
| 22 | MTC compatibility | 4 / 5 (clean stateless producer; one EMA, one pullback flag) |
| 23 | Testability | 5 / 5 |
| 24 | Was previous backtest fair? | **PARTIALLY** (faithful logic, wrong asset class for verdict) |
| 25 | Deserves repaired test? | **YES** — minor (sweep prior-strength, lookback, exit variants); equity dataset pass for primary verdict |
