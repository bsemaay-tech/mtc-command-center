# Forward Paper-Trade Plan — QL_ALPHA_LTC_RSI_OVERSOLD_1H

> **Paper-trade only. No real capital. No live orders, alerts, or webhooks.**

## Scope
- Symbol/TF: LTCUSDT 1h, LONG-only, no trend filter.
- Params frozen: `rsi_len=5, oversold=35, recovery=45`, stop=5-bar low, exit=2R/stop/96-bar, cost 8 bps.
- Start date: **next session** (fill actual UTC date when started).

## Minimum observation requirements
- **Minimum observation period:** 8 weeks (signals are frequent — 329 trades historically).
- **Minimum NEW forward trades before evaluation:** 40 (achievable quickly; the weakness is edge quality, not sample size).

## Metrics to track (forward window only)
- Trades, win rate, **profit factor (watch closely — backtest PF only 1.23)**, expectancy (R), max drawdown.
- **Strategy vs LTC buy&hold + excess alpha (mandatory).**
- Cost sensitivity: re-evaluate at 8 and 12 bps to confirm the thin edge survives.

## Daily / weekly review fields
- Date, # new trades, open position?, cumulative forward return, cumulative buy&hold, excess alpha, current drawdown, rolling PF (last 30 trades), data gaps.

## Stop conditions
- Rolling PF (last 30 trades) < 1.05.
- Forward max drawdown exceeds −30%.
- 40+ forward trades with negative excess alpha vs buy&hold.
- Sustained LTC downtrend where the no-filter mean reversion bleeds (monitor for catching falling knives).

## Promotion conditions (to consider parity later)
- ≥40 forward trades AND positive excess alpha AND PF ≥ 1.3 AND ≥2/3 of forward sub-windows positive.
- Only then revisit `PROMOTE_TO_PARITY_CANDIDATE` (currently deferred).

## Demotion conditions
- Any stop condition → `HOLD_AS_RESEARCH_NOTE`.
- If the thin edge does not survive 12 bps cost → demote.

## Mandatory benchmark rule
Report strategy vs buy&hold and excess alpha at every evaluation. Given the thin PF, also report cost-sensitivity.
