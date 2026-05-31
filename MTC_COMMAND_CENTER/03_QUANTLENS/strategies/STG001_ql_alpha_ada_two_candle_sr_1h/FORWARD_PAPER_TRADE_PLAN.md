# Forward Paper-Trade Plan — QL_ALPHA_ADA_TWO_CANDLE_SR_1H

> **Paper-trade only. No real capital. No live orders, alerts, or webhooks.**

## Scope
- Symbol/TF: ADAUSDT 1h, LONG-only.
- Params frozen: `level_lookback=200, upper_third=0.6, break_buf_atr=0.0`, stop=2-bar low, exit=2R/stop/96-bar, cost 8 bps.
- Start date: **next session** (fill actual UTC date when started).

## Minimum observation requirements
- **Minimum observation period:** 16 weeks (signals are rare due to the 200-bar resistance lookback).
- **Minimum NEW forward trades before evaluation:** 30. This candidate's biggest weakness is low sample (53 lockbox trades), so the forward window exists primarily to grow the sample.

## Metrics to track (forward window only)
- Trades, win rate, profit factor, expectancy (R), max drawdown, average bars held.
- **Strategy vs ADA buy&hold over the same forward window + excess alpha (mandatory).**

## Daily / weekly review fields
- Date, # new trades, open position?, cumulative forward return, cumulative buy&hold, excess alpha, current drawdown, signal frequency, any data gaps.

## Stop conditions
- Forward max drawdown exceeds −25%.
- 30+ forward trades with negative excess alpha vs buy&hold.
- Win rate collapses below 35% with PF < 1.2 after 30 trades.

## Promotion conditions
- ≥30 forward trades AND positive excess alpha AND PF ≥ 1.4 AND win rate ≥ 40%.
- Meeting these materially de-risks the low-sample concern → advance parity work.

## Demotion conditions
- Any stop condition → `HOLD_AS_RESEARCH_NOTE`.
- If forward signals are too rare to reach 30 trades within 24 weeks → demote and revisit lookback.

## Mandatory benchmark rule
Report strategy vs buy&hold and excess alpha at every evaluation. Net profit alone is insufficient.
