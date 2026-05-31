# Andrew Connell deep read — `QLR_kao-hhaQnig`

After targeted grep + reading the core event-driven section (lines 700-900), the strategy is **more codifiable than the initial sampler suggested.** Reclassified from "REVIEW further" → **LIKELY_MISCLASSIFIED + PROMOTE.**

## Strategy: Event-Driven Catalyst Trading

### Trigger
- News/earnings catalyst that **contradicts prevailing market narrative**
- Example given (Western Alliance, March 2023 regional bank panic): WAL reports deposit INFLOWS while every other regional bank is collapsing
- **5-minute response requirement** — "if you can see a headline and respond to it in less than five minutes with a trade idea, you're hitting your stride"

### Context filter
- Stock in stage 4 (extended decline) with recent waterfall
- Recent panic low + volume drying up
- Levels visible on chart to trade against

### Entry
- **Pre-market order** triggered on the headline
- Order fires **at the open**
- Specific entry zones (any of these qualifies):
  1. Above prior day's high
  2. Breakout from **monthly Volume Profile value area** (uses "Markets and Profile" Dalton-style indicator)
  3. Near declining 50 SMA after the waterfall base forms

### Stop loss
- **Hard stop always in place**
- Specific level: **bottom of recent green candle** (a few days back)
- Tight enough to give 1-2R potential
- **Same-day invalidation**: "if the trade doesn't work that day, I'm out"
- Logic: catalyst trades give **immediate feedback**; lack of immediate move = thesis wrong

### Profit targets (3-part scale-out)
- **Target 1**: Top of monthly value area (where 70% of last month's volume traded) — first 1/3 out
- **Target 2**: Next pivot resistance — second 1/3 out
- **Trail remaining**: under last swing low

### Position sizing
- **A+ catalyst with conviction**: 20-25% of account in one name
- **Broad-based ETF only (SPY)**: up to 100%
- **Less liquid / small-cap**: progressively smaller
- **Psychological ceiling at 25%**: above that, Andrew himself starts to exit too early due to size anxiety

### Codifiability assessment

| Component | Codifiable? | Notes |
|---|---|---|
| Catalyst detection | **Hard for backtest** | Needs news API + sentiment scoring; can substitute "earnings beat > N%" or "gap > 5% on volume > X" |
| Entry above prior day high | **Easy** | Standard price-action rule |
| Monthly value area breakout | **Medium** | Needs Volume Profile calc; standard TradingView indicator |
| 50 SMA proximity check | **Easy** | Simple MA distance |
| Hard stop at recent green candle low | **Easy** | Pivot detection |
| Same-day invalidation | **Easy** | Time-based exit on session close if -X% |
| Top-of-value-area target | **Medium** | Needs Volume Profile |
| Position sizing tiers | **Easy** | Symbol-class lookup table |

**Verdict**: **PROMOTE** as `QL_CONNELL_EVENT_DRIVEN_GAP_1D` with a "catalyst proxy" of "gap > 5% on top-decile volume". Production version would need news API; backtest version uses gap+volume proxy.

Also worth: `QL_CONNELL_EVENT_DRIVEN_GAP_5M` intraday variant for the pre-market-order-fires-on-open mechanics.

Updated A-tally: **8 promotions** (Andrew added to the 7 originals).
