# Forward Paper-Trade Plan — QL_ALPHA_LINK_8EMA_1H

> **Paper-trade only. No real capital. No live orders, alerts, or webhooks.**

## Scope
- Symbol/TF: LINKUSDT 1h, LONG-only.
- Params frozen: `pullback_atr=0.5, impulse_atr=1.6, slope_window=3`, stop=3-bar low, exit=EMA8 trailing, cost 8 bps round-trip.
- Start date: **next session** (fill actual UTC date when started).

## Minimum observation requirements
- **Minimum observation period:** 12 weeks of new forward bars.
- **Minimum NEW forward trades before evaluation:** 30 (no decision before this; below it → `INSUFFICIENT_TRADES`).

## Metrics to track (forward window only)
- Trades, win rate, profit factor, expectancy (R), max drawdown.
- **Strategy return vs LINK buy&hold over the SAME forward window** + excess alpha (mandatory).
- Average bars held, % time in market.
- Slippage/cost assumption used (keep 8 bps round-trip).

## Daily / weekly review fields
- Date, # new trades, open position?, cumulative forward return, cumulative buy&hold, excess alpha, current drawdown, any data gaps.

## Stop conditions (halt the paper-trade)
- Forward max drawdown exceeds −30% (worse than backtest −16% by a wide margin).
- 30+ forward trades with NEGATIVE excess alpha vs buy&hold.
- Profit factor < 1.0 after 30 trades.

## Promotion conditions (advance toward parity/integration)
- ≥30 forward trades AND positive excess alpha vs buy&hold AND PF ≥ 1.3 AND max DD ≤ −25%.
- Then eligible to advance from `PROMOTE_TO_PARITY_CANDIDATE` work to deeper review (still NOT live).

## Demotion conditions
- Any stop condition met → `HOLD_AS_RESEARCH_NOTE`.
- Forward behavior diverges materially from backtest distribution → re-open spec review.

## Mandatory benchmark rule
Every forward evaluation MUST report strategy vs buy&hold and the excess alpha. Positive net return alone is not sufficient.
