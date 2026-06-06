# Ryan Pierpont Breakout Discipline

## Source
- Strategy ID: STG061
- Source candidate IDs: QL_RYAN_LATE_ENTRY_CHASE_FILTER_001; QL_RYAN_MARKET_AWARENESS_GATE_001; QL_RYAN_PULLBACK_DANGER_ZONE_001; QL_RYAN_SELL_INTO_STRENGTH_RUNNER_EXIT_001; QL_RYAN_TIGHT_BREAKOUT_001
- Source transcript paths: 11_TRIAGE/strategies/stg154.md through 11_TRIAGE/strategies/stg158.md
- Source URL: https://youtu.be/KQRuUWSZvLE?si=50fVh__JlzLkqeb0

## Plain-English Summary
A long-only US-equity swing breakout framework. The core idea is to enter tight, low-volatility breakouts only when the market context supports breakout risk, reject late/chased entries, manage the first pullback after entry as a danger zone, and sell partial size into strength while preserving a runner.

## Market / Asset Assumptions
- Primary asset class: US equities.
- Best suited to liquid growth/momentum stocks with institutional participation.
- Avoid applying the same sizing in weak or mixed market conditions.

## Timeframe Assumptions
- Original timeframe: daily swing trading.
- Recommended timeframe: 1d.
- Intraday execution details are unknown.

## Entry Rules
1. Define a clean pivot from a tight consolidation or constructive base.
2. Enter only when price breaks the pivot with constructive price/volume behavior.
3. Reject the entry if price is already materially extended from the pivot or from the leader move. The exact extension threshold is unknown.
4. Require a supportive market environment before A-plus sizing. Exact market inputs are unknown.

## Exit Rules
- Sell some exposure into strength after a successful breakout.
- Keep a runner only if the trend and market context remain constructive.
- Exit or reduce when the post-breakout pullback enters the danger zone and fails to recover. Exact failure threshold is unknown.

## Stop Logic
Use the pivot/base low or danger-zone failure as invalidation. The transcript does not provide a fully numeric stop rule.

## Take-Profit Logic
Partial profit taking into strength is supported. Exact target and fraction are unknown.

## Trailing Logic
Runner management is supported, but no precise moving-average or percent trailing rule is provided.

## Filters
- Late-entry chase filter.
- Market-awareness gate.
- Pullback danger-zone guard.

## Regime Assumptions
Works best in bull, trending, breakout-friendly markets. Should de-risk in choppy or weak markets.

## Indicators / Components Used
- Price base / pivot.
- Moving averages, implied by trend and market context.
- Volume / institutional participation.
- Reusable breakout risk guards.

## Repaint / Lookahead / Data Leakage Notes
- Repaint risk: low if using confirmed bars; medium if discretionary pivots are moved after the fact.
- Lookahead risk: low if pivot, market context, and extension are computed at entry time only.
- Data leakage risk: do not label entries with future leader strength or later market repair.

## Ambiguities
- Numeric overextension threshold.
- Market-awareness inputs.
- Pullback danger-zone boundary and failure rule.
- Partial exit fraction and runner trail.

## Rejection or Promotion Notes
Promoted to matured strategy folder as a deterministic-spec candidate, not as a tested or profitable strategy. It is not backtest-ready until the unknown thresholds are formalized.

## Implementation Readiness Rating
Medium. Components are clear, but several rules need numeric definitions.

## Backtest Readiness Rating
Needs review. Formalize thresholds before running QuantLens validation.

## Next Steps
1. Convert the late-entry filter and market gate into reusable guard modules.
2. Define numeric extension and danger-zone rules.
3. Test as an overlay on existing breakout producers, not as a standalone edge claim.
