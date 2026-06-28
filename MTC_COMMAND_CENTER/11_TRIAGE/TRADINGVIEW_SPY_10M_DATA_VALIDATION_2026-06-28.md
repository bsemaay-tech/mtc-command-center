# TradingView SPY 10m — Data Validation Report

**Date:** 2026-06-28
**Author:** Claude Opus 4.8
**Target strategy (downstream):** `QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK`
**Verdict:** **PASS** — TradingView `BATS:SPY` 10m export is clean, complete RTH-only OHLC. Usable for a SMOKE-ONLY native run. Not promotable on its own.

---

## Source

Barış exported 8 TradingView "Chart Data" CSV files for `BATS:SPY` at 10m. A prior consolidation step (Codex, same day) merged them. This report validates the **consolidated** output.

- Consolidated file: `00_INBOX/USER_INTAKE/SPY_10m_tradingview__2024-06-03_to_2026-06-26.csv`
- SHA256: `c9fc113b40c4639ac445cc8efa52571e855d9e53613ee9f054ccf0582647530d` (verified — matches `BATS_SPY_10m_CONSOLIDATION_REPORT.json`)
- Consolidation provenance (`BATS_SPY_10m_CONSOLIDATION_REPORT.json`): 8 source files, 92,892 input rows → 20,094 unique rows; 72,798 duplicate rows removed; **0 conflicting timestamps**; 18,166 timestamps appeared in multiple files (overlap only, no conflict).
- Original raw exports were consumed by the consolidation step; the consolidated CSV + JSON report are the surviving artifacts. **No original data deleted by this task.**

## Schema

- Header: `time,open,high,low,close`
- `time` = Unix epoch **seconds**, UTC.
- **Volume: NOT present.** Not fabricated. (Downstream 8-EMA-pullback strategy uses only OHLC + EMA/ATR — volume not required.)

## Validation results (independent re-check by this task)

| Check | Result |
|---|---|
| Data rows | 20,094 |
| Unique timestamps | 20,094 |
| Duplicate timestamps | **0** |
| Numeric-parse failures | **0** |
| Timestamps monotonic increasing | **Yes** |
| OHLC sanity failures (`high<max(o,c)` / `low>min(o,c)` / `high<low`) | **0** |
| First bar (UTC) | 2024-06-03 13:30:00 |
| Last bar (UTC) | 2026-06-26 19:50:00 |
| Bar-start grid all multiples of 10 min | **Yes** |
| Intra-session gaps (600s < Δt ≤ 3600s = missing 10m bars within a session) | **0** |
| Weekday coverage | Mon–Fri only (no Sat/Sun) |
| Session span of bar starts (UTC) | 13:30 → 20:50 |

### Interval distribution (Δt between consecutive bars)

| Δt (s) | Count | Meaning |
|---|---|---|
| 600 | 19,576 | normal 10m step |
| 63,600 | 400 | overnight gap (19:50 close → next 13:30 open, 17h40m) |
| 236,400 | 89 | weekend gap (Fri close → Mon open) |
| 322,800 / 150,000 / 160,800 / 240,000 / 247,200 | 11 / 7 / 3 / 2 / 2 | holiday + weekend / DST-shifted variants |

All non-600 intervals are session boundaries (overnight / weekend / holiday). **Zero intra-session gaps** → no missing bars inside any trading day.

### Session policy (inferred)

- **RTH-only (Regular Trading Hours), XNYS calendar.** Bar starts span 13:30→20:50 UTC, which is exactly 09:30→15:50 ET across both DST regimes (EDT 13:30–19:50 UTC summer; EST 14:30–20:50 UTC winter). Last bar of each day starts at :50 and covers to 16:00 ET close.
- No extended-hours (ETH) bars. No 24/7 behavior.
- Consolidation report cross-check: `expected_10m_bars_xnys = 20094`, `missing_expected_bars = 0`, `extra_bars_outside_xnys = 0` — agrees exactly.

### Price adjustment

- **Unknown.** TradingView chart-data export carries no adjustment metadata. Early-2024 SPY prints ~515; mid-2026 ~733. Treated as `unknown_tradingview_export` in the manifest. Do not assume adjusted or unadjusted.

## Conclusion

Data is **PASS** for a single-symbol SMOKE-ONLY native SPY 10m run:
- 20,094 bars ≫ engine `MIN_BARS_REQUIRED = 1500`.
- Clean, monotonic, gap-free RTH grid; no OHLC violations; no duplicates.

**Limitations (why not promotable):**
1. One symbol (SPY) only — no universe.
2. No volume (acceptable for this strategy, but a hard constraint for any volume-dependent strategy).
3. Adjustment policy unknown.
4. Equity-session/exchange gating (`EQUITY_ONLY_STRATEGIES`) still not configured for the strategy.

This validation authorizes only the smallest smoke. It does **not** satisfy Gate 2 promotion.
