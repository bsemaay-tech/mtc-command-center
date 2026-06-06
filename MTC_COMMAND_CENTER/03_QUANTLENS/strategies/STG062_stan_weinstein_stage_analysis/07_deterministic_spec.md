# Stan Weinstein Stage Analysis

## Source
- Strategy ID: STG062
- Source candidate IDs: QL_STAN_FAILED_RALLY_200D_SHORT_AVOID_v0; QL_STAN_FOREST_GROUP_TREE_FILTER_v0; QL_STAN_GOOD_COMPANY_BAD_CHART_BLOCK_v0; QL_STAN_SPLIT_TAPE_BREADTH_FILTER_v0; QL_STAN_STAGE_1B_TO_2A_BREAKOUT_v0; QL_STAN_STAGE_2A_PULLBACK_SUPPORT_v0; QL_STAN_UNFILLED_GAP_CONTINUATION_v0
- Source transcript paths: 11_TRIAGE/strategies/stg160.md through 11_TRIAGE/strategies/stg166.md
- Source URL: https://youtu.be/O0GpSPtmCuM?si=Ra7X5w149KdMksmj

## Plain-English Summary
A top-down stage-analysis framework for selecting long exposure in Stage 2 leadership and avoiding inferior merchandise in Stage 3/4. The transcript supports several reusable modules: failed-rally/200-day avoid, group-vs-stock filtering, breadth split-tape filter, Stage 1B-to-2A breakout, Stage 2A pullback support, and unfilled-gap continuation.

## Market / Asset Assumptions
- Primary asset class: US equities.
- Requires broad-market, sector/group, and individual-stock context.
- Best value is as a regime and selection layer for long swing/position systems.

## Timeframe Assumptions
- Original timeframe: daily charts with weekly/long-term stage context.
- Recommended timeframes: 1d and 1w.

## Entry Rules
1. Prefer stocks transitioning from Stage 1B to Stage 2A or already in constructive Stage 2 behavior.
2. Require the stock and its group/sector to be constructive; do not isolate the tree from the forest.
3. Prefer breakouts or pullbacks that hold support in Stage 2A.
4. Treat unfilled upside gaps as continuation evidence only when the broader context is supportive.

## Exit Rules
- Avoid or exit names that fail on rallies into the 200-day moving average.
- Avoid good-company/bad-chart situations.
- De-risk when breadth shows a split tape or when the market becomes increasingly selective.
- Avoid Stage 3/4 inferior merchandise.

## Stop Logic
Use failure below breakout/support zones or rejection at the long-term moving average as invalidation. Exact stop distance is unknown.

## Take-Profit Logic
Unknown. The source emphasizes selection and avoidance more than profit targets.

## Trailing Logic
Unknown. A future implementation should define whether trend moving averages or stage downgrades trail exits.

## Filters
- Stage classifier.
- 200-day failed-rally avoid filter.
- Group/sector strength filter.
- Breadth split-tape filter.
- Good-company/bad-chart block.

## Regime Assumptions
Works best when broad market and leadership breadth support Stage 2 exposure. It explicitly warns against late, selective, split-tape environments.

## Indicators / Components Used
- 200-day moving average.
- Stage analysis.
- Relative/group strength.
- Breadth / new-high context.
- Gap persistence.

## Repaint / Lookahead / Data Leakage Notes
- Repaint risk: medium if stage labels are assigned retrospectively.
- Lookahead risk: medium until stage transitions are defined by completed-bar rules.
- Data leakage risk: breadth and group-state inputs must be timestamped at decision time.

## Ambiguities
- Exact Stage 1B, 2A, 3, and 4 formulas.
- Breadth thresholds for split tape.
- Group/sector strength ranking method.
- Gap persistence window.
- Stop and profit-taking rules.

## Rejection or Promotion Notes
Promoted to matured strategy folder as a deterministic-spec candidate and reusable filter framework. Not a profitability claim and not backtest-ready until objective classifiers are added.

## Implementation Readiness Rating
Medium. The conceptual modules are clear, but market breadth and stage formulas must be formalized.

## Backtest Readiness Rating
Needs review. Requires a stage classifier and breadth/group data.

## Next Steps
1. Build a completed-bar Stage 1-4 classifier.
2. Define breadth and group-strength inputs.
3. Test as a filter overlay on existing VCP/breakout systems before treating it as standalone.
