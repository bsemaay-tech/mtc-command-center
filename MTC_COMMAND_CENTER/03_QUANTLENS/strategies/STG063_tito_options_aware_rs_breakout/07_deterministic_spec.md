# Tito Options-Aware RS Momentum Breakout

## Source
- Strategy ID: STG063
- Source candidate IDs: QL_TITO_OPTIONS_AWARE_RISK_OVERLAY_v0; QL_TITO_PROFIT_WITHDRAWAL_CAPITAL_AT_RISK_v0; QL_TITO_RS_MOMENTUM_BREAKOUT_CROSSBACK_v0
- Source transcript paths: 11_TRIAGE/strategies/stg167.md through 11_TRIAGE/strategies/stg169.md
- Source URL: https://youtu.be/NGyE4YIgGpU?si=gj_6ZcIyjUFAEGhk

## Plain-English Summary
A long-only US-equity momentum breakout framework that uses options selectively, respects market context, sizes down after mental/equity damage, and withdraws profits to keep capital at risk controlled. The source is high quality but only partially deterministic because several key thresholds are not specified.

## Market / Asset Assumptions
- Primary asset class: US equities.
- Strategy may use options, so stock-only backtests are incomplete proxies.
- Best suited to high relative-strength names in supportive markets.

## Timeframe Assumptions
- Original timeframe: daily swing trading.
- Recommended timeframe: 1d.

## Entry Rules
1. Identify a relative-strength momentum setup or breakout/crossback condition.
2. Require the broader market to support aggressive sizing.
3. If using options, account for IV expansion and leverage risk before entry.
4. Exact pivot, crossback, RS threshold, and option selection rules are unknown.

## Exit Rules
- Take profits after outsized option gains or favorable gap/IV expansion.
- Reduce capital at risk after large account gains.
- Size down after large losses or mental-equity damage before returning to normal risk.

## Stop Logic
Risk is constrained through sizing and option exposure. A precise price stop is not defined in the available transcript evidence.

## Take-Profit Logic
Profit withdrawal and capital-at-risk reduction are supported. Exact schedule or thresholds are unknown.

## Trailing Logic
Unknown.

## Filters
- Market environment gate.
- Options-aware risk overlay.
- Mental-equity/account-equity risk reset.

## Regime Assumptions
Works best in supportive growth/momentum markets. The source explicitly warns against full sizing when QQQ/SPY or short-term market context is weak.

## Indicators / Components Used
- Relative strength.
- Breakout/crossback structure.
- Short-term moving average context.
- Options IV/leverage overlay.

## Repaint / Lookahead / Data Leakage Notes
- Repaint risk: low for completed-bar price checks.
- Lookahead risk: high if later IV expansion is used as proof of entry quality.
- Data leakage risk: options-chain state and market context must be timestamped at entry time.

## Ambiguities
- Exact RS threshold.
- Exact breakout/crossback trigger.
- Options selection, delta, expiry, and IV rules.
- Stop-loss and profit-taking thresholds.
- Profit withdrawal schedule.

## Rejection or Promotion Notes
Marked needs_manual_review because the source includes important strategy/risk material but not enough deterministic options rules for direct QuantLens promotion.

## Implementation Readiness Rating
Low to medium. Stock-side breakout logic is reusable, but options implementation requires additional rules/data.

## Backtest Readiness Rating
Needs review. A stock-only proxy may test the entry idea, but cannot validate options returns.

## Next Steps
1. Decide whether to model this as stock-only breakout plus risk overlay, or keep it as options-aware manual-review research.
2. Extract exact option selection rules if additional source material exists.
3. Only backtest after defining stock and options proxy assumptions separately.
