# FINAL_STRATEGY_CONTRACT — Kell Wedge Pop

| # | Field | Value |
|---|---|---|
| 1 | Candidate ID | `KELL_WEDGE_POP_v1_CONTRACT` |
| 2 | Source file | `2026-05-03_fYxSQvuwOQc_quantlens_oliver_kell_cycle_intake.md` + Kell Wedge Pop transcript |
| 3 | Source URL | https://youtu.be/fYxSQvuwOQc |
| 4 | Strategy family | trend_pullback / cycle_resumption (NOT a generic breakout) |
| 5 | Native market | Liquid US equity high-beta growth leaders, in-play themes |
| 6 | Native timeframe | Weekly trend + Daily trade idea + 65m/30m execution |
| 7 | Minimum data required | Daily OHLCV + Volume + Weekly OHLCV; intraday optional but recommended; sector/theme tag optional |
| 8 | Tradable universe | Top US equity leaders by liquidity ($-vol > $50M/day) and recent relative-strength rank vs SPY (top decile preferred); active theme leadership |
| 9 | Setup context | (a) Pre-flush completed (close was at least 1.5 ATR below EMA20 within last 30 bars), (b) Snapback to EMA10/EMA20 zone (within ~1% tolerance), (c) Higher-low pivot confirmed vs flush low, (d) Contraction: ATR(20) percentile dropping, recent 5-bar range < median 30-bar range × 0.7, mini-base of ≥3 bars |
| 10 | Entry trigger | Close breaks above mini-base swing high AND close > EMA10 AND close > EMA20 |
| 11 | Confirmation | Volume on trigger ≥ SMA(volume,20) × 1.0 (not strictly required but tracked) |
| 12 | Filters | Weekly close > weekly EMA10; relative-strength vs SPY (60-day) positive; no scheduled earnings within 5 trading days |
| 13 | Initial stop | min(mini-base low, higher-low pivot − 0.25 ATR) |
| 14 | Profit target | None fixed; ride MA |
| 15 | Time stop | If no follow-through (close above entry) within 5 bars → exit at next close |
| 16 | Exit rules | Default: close < EMA20. After 3 consecutive holds of EMA20 with successful bounces, switch trailing MA to EMA10. Discretionary blowoff exit when close > EMA10 × 1.20 (placeholder) |
| 17 | Position sizing | Risk per trade 0.5–1.0% of equity; Kell's name-size caps are aspirational for live, not for first backtest |
| 18 | Do-not-trade | No pre-flush detected (i.e. uptrend already extended); weekly EMA10 declining; recent earnings gap unresolved; in a known broad-market downtrend (SPY < EMA200) |
| 19 | Ambiguities | Theme/leader scoring (needs external data); blowoff threshold; exact ATR-percentile thresholds; 10-vs-20 MA switch heuristic |
| 20 | Mechanical confidence | 3 / 5 — core sequence is codable but theme/leader detection is partial proxy |
| 21 | Data confidence | 2 / 5 — needs US equity data + relative-strength rank vs SPY; current crypto bundle insufficient |
| 22 | MTC compatibility | 3 / 5 — producer-shaped but multi-TF + non-repaint + theme-gate add UI/parity work |
| 23 | Testability | 3 / 5 — testable IF equity data acquired; not testable on current crypto-only bundle |
| 24 | Was previous backtest fair? | **NO** |
| 25 | Deserves repaired test? | **YES** — high priority; previous code did not test Kell's actual idea |
