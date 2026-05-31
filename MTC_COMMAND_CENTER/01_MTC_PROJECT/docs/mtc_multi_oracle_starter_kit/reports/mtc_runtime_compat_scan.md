# MTC Runtime Compatibility Scan

- File: `/mnt/data/mtc_multi_oracle_starter_kit/examples/synthetic_case/example_mtc_strategy.pine`
- Scanned UTC: `2026-04-26T14:18:48.481699+00:00`
- Pine version: `6`
- File size: `593` bytes

## Feature counts

| Feature | Count / Value |
|---|---:|
| `pine_version` | `6` |
| `strategy_declaration` | `1` |
| `indicator_declaration` | `0` |
| `strategy_entry` | `1` |
| `strategy_exit` | `0` |
| `strategy_close` | `1` |
| `strategy_close_all` | `0` |
| `strategy_position_size` | `0` |
| `strategy_opentrades` | `0` |
| `strategy_closedtrades` | `0` |
| `request_security` | `0` |
| `request_security_lower_tf` | `0` |
| `array_namespace` | `0` |
| `matrix_namespace` | `0` |
| `map_namespace` | `0` |
| `type_declarations` | `0` |
| `method_definitions` | `0` |
| `var_keyword` | `0` |
| `varip_keyword` | `0` |
| `input_namespace` | `0` |
| `alert_calls` | `0` |
| `alertcondition_calls` | `0` |
| `timeframe_namespace` | `0` |
| `session_mentions` | `0` |
| `barstate_isconfirmed` | `2` |
| `barstate_namespace` | `2` |
| `ta_namespace` | `4` |
| `math_namespace` | `0` |
| `line_label_table_drawing` | `0` |
| `plot_calls` | `6` |
| `plotshape_calls` | `0` |
| `plotchar_calls` | `0` |
| `lookahead_mentions` | `0` |
| `gaps_mentions` | `0` |

## Top ta.* functions

| Function | Count |
|---|---:|
| `ta.ema` | 2 |
| `ta.crossover` | 1 |
| `ta.crossunder` | 1 |

## Top strategy.* functions

| Function | Count |
|---|---:|
| `strategy.entry` | 1 |
| `strategy.close` | 1 |

## request.security calls


## Input titles


## Interpretation hints

- Many `request.security` calls increase HTF alignment risk.
- `varip` usage needs special attention outside TradingView.
- `strategy.exit`, BE/trailing/partial exits must be compared at L5 execution level.
- Indicator equality at L1 does not prove trade parity at L5/L6.
