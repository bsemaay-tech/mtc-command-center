# FINAL_STRATEGY_CONTRACT — Crabel Range Expansion (canonical)

| # | Field | Value |
|---|---|---|
| 1 | Candidate ID | `CRABEL_OPENING_RANGE_STRETCH_v1_CONTRACT` |
| 2 | Source file | Toby Crabel, *Day Trading with Short-Term Price Patterns and Opening Range Breakout* (1990). The Ne3X-l6W4CQ intake is NOT a primary source for Crabel and should not be cited. |
| 3 | Source URL | n/a (book reference); secondary context: Linda Raschke Ne3X-l6W4CQ |
| 4 | Strategy family | intraday_opening_range_breakout / volatility_expansion |
| 5 | Native market | Liquid futures (ES, NQ, CL, ZB, GC) and large-cap US equities; FX optional |
| 6 | Native timeframe | Intraday session (each trading day is one trade window). Stops set at session open; exit at session close. |
| 7 | Minimum data required | OHLC of regular trading hours per session + access to today's open, prior 10 days for Stretch, prior 4-7 days for NR pattern |
| 8 | Tradable universe | Defined by an asset with a clear daily session open (futures, US equities). Crypto only acceptable if "session" defined as 00:00–24:00 UTC and explicitly relabelled as "Crabel-adapted-crypto" |
| 9 | Setup context | Prior day is NR4 or NR7 (range ≤ min of last 4 or 7). Optional further filter: ID/NR4 (inside day AND NR4) |
| 10 | Entry trigger | Place buy-stop at `O_today + Stretch * mult`, sell-stop at `O_today − Stretch * mult` where `Stretch = mean(min(O−L, H−O), n=10)` and mult ∈ [0.4, 0.6, 0.8, 1.0]; first stop hit wins |
| 11 | Confirmation | None additional; trigger is the order fill |
| 12 | Filters | NR-pattern (mandatory). Optional: trend (EMA200 of daily close), volatility regime (Stretch percentile not extreme), no major scheduled news |
| 13 | Initial stop | Opposite stop level (i.e. long stop = sell-stop level) |
| 14 | Profit target | Optional: 1×Stretch from entry; or prior-day H/L; default = none |
| 15 | Time stop | Mandatory: exit at session close (Crabel's "go home flat") |
| 16 | Exit rules | First of: profit target hit, opposite stop hit, session close |
| 17 | Position sizing | Fixed risk per trade ≤ 1% of equity using `(entry − stop)` |
| 18 | Do-not-trade | No NR pattern in prior day; major scheduled news (FOMC, NFP, earnings); session shortened (half-day); first-day-of-month optional skip |
| 19 | Ambiguities | Stretch multiplier; NR4 vs NR7 vs ID/NR4; whether to allow reversal entries; profit target style |
| 20 | Mechanical confidence | 5 / 5 — Crabel's rules are extremely explicit |
| 21 | Data confidence | 2 / 5 on current bundle (no intraday equity/futures data; crypto-daily wrong) |
| 22 | MTC compatibility | 2 / 5 — session-anchored intraday strategy; MTC's bar-by-bar producer model fits awkwardly; stop-entry orders pre-placed at open need careful Pine modelling |
| 23 | Testability | 4 / 5 with proper data; 1 / 5 with current bundle |
| 24 | Was previous backtest fair? | **NO** |
| 25 | Deserves repaired test? | **YES** — but only after intraday/session data acquired; the "Crabel on crypto-daily" question is invalid by construction |
