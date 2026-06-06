# Variant Log — `<variant_id>`

> One file per tested variant. Also append a compact row to
> `05_REGISTRY/VARIANT_LOG_REGISTRY.json` (`variants[]`) so the variant appears
> in the **Strategy Research Lab → Variant Log** tab. Be honest: log rejected
> variants too.

| Field | Value |
|---|---|
| variant_id | `<run_id>-V001` |
| research_run_id | `<run_id>` |
| date | `YYYY-MM-DD` |
| researcher_or_ai | e.g. Claude Opus 4.8 |
| architecture_family | regime_switching_strategy \| signal_scoring_ensemble \| specialist_strategy_portfolio \| breakout_pullback_hybrid |
| hypothesis | one sentence |
| components_used | component_ids from COMPONENT_REGISTRY.json |
| indicators_used | indicator_ids from INDICATOR_REGISTRY.json |
| parameters | key params + values |
| assets_tested | e.g. BTCUSDT, ETHUSDT |
| timeframe | e.g. 1h |
| date_range | start..end |
| long_only_or_long_short | long_only \| long_short |
| commission | e.g. 8 bps round trip |
| slippage | e.g. 1 tick / model |
| starting_capital | e.g. 10000 |
| number_of_trades | |
| net_profit | absolute + % |
| max_drawdown | % |
| profit_factor | |
| win_rate | % |
| exposure | % time in market |
| worst_asset | symbol + metric |
| best_asset | symbol + metric |
| robustness_notes | multi-window, OOS, parameter sensitivity |
| code_safety_status | PASS \| FAIL \| NOT_REVIEWED (see STRATEGY_CODE_REVIEW_CHECKLIST.md) |
| decision | recommended \| needs_more_research \| rejected |
| rejection_reason_if_any | required when decision = rejected |
| next_iteration_idea | |
| report_link_or_path | path to the run report or summary |

## Registry row (paste into VARIANT_LOG_REGISTRY.json → variants[])

```json
{
  "variant_id": "<run_id>-V001",
  "research_run_id": "<run_id>",
  "date": "YYYY-MM-DD",
  "architecture_family": "",
  "components_used": [],
  "indicators_used": [],
  "assets_tested": [],
  "timeframe": "",
  "net_profit": null,
  "max_drawdown": null,
  "profit_factor": null,
  "win_rate": null,
  "code_safety_status": "NOT_REVIEWED",
  "decision": "needs_more_research",
  "rejection_reason_if_any": "",
  "report_link_or_path": ""
}
```
