# PREVIOUS_LLM_INTERPRETATION_AUDIT — Crabel Range Expansion

## What Codex coded (`signal_crabel`)
```
prev_range  = high.shift(1) - low.shift(1)
buy_stop    = close.shift(1) + prev_range * mult       # mult default 0.9
sell_stop   = close.shift(1) - prev_range * mult
long_entry  = high >= buy_stop
short_entry = low  <= sell_stop
```
Optional EMA200 trend filter and ATR percentile filter; default `direction_mode=both`. Run on daily crypto bars (BTC/ETH/SOL/BNB/XRP).

## Comparison to canonical Crabel

| Crabel requirement | Coded? | Notes |
|---|---|---|
| Stretch = mean_10d(min(O−L, H−O)) | NO | Replaced with prior-day range × 0.9 (very different magnitude) |
| Trigger anchored to **today's open** | NO | Anchored to **yesterday's close** |
| NR4 / NR7 / ID-NR4 setup filter | NO | Missing entirely |
| Session-based EOD exit | N/A on daily bars | Strategy run on 1D bars → no real intraday exit |
| Native instruments (futures, US equities) | NO | Crypto majors |
| Opening-gap context | NO | Missing |

## Errors

- **Wrong trigger formula:** previous range × constant is *not* Stretch. Magnitude and meaning differ; Stretch is much smaller and based on intra-day extension from open, not full bar range.
- **Wrong anchor:** Crabel anchors stops to today's OPEN, not yesterday's CLOSE. On gap days these differ materially.
- **Wrong timeframe:** Crabel is intra-day; daily bars cannot reproduce his execution path. Treating "high>=buy_stop" on a daily bar conflates "price touched" with "intraday breakout from open at any time" — but the entry/stop levels themselves are wrong because they're computed from yesterday-close not today-open.
- **Wrong market:** crypto is 24/7. The concept of "session open" needs explicit redefinition; without it the strategy is not Crabel.
- **Missing setup filter:** NR4/NR7 was the gating filter — the *whole point* is "low-vol day → expansion next day". Without it, the strategy degenerates to "buy any breakout above prior close + 0.9*range, short any breakdown".
- **Discretionary component falsely mechanized:** Crabel taught a stack of pattern qualifiers (NR4, NR7, ID/NR4, 2BH/2BL); reducing it to a single multiplier removes ~all of his pattern logic.

## Classification
**MATERIAL_MISINTERPRETATION** — the implemented logic is a generic daily mean-reverting volatility breakout, not Crabel.

## Was the previous backtest fair?
**NO.** It tested an unrelated breakout strategy and labelled it Crabel. Crypto-daily Stage-2 metrics tell us nothing about the actual Crabel edge.
