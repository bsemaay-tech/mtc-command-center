# GEN_RSI TRXUSDT 1H SOURCE_NAKED Artifact Audit - 2026-06-16

## 1. Executive verdict

Final verdict: ACCEPT

The generated `SOURCE_NAKED` research artifact for `GEN_RSI_OVERSOLD_REVERSAL | TRXUSDT | 1h` passes the requested static audit. It parses, validates against `backtest_profile_result.schema.json`, contains exactly one result row, preserves research-only/non-promotional safety flags, preserves Gate 3 as incomplete, and does not generate `top_results.json`.

## 2. Files inspected

- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/profile_result_GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h_SOURCE_NAKED_2026-06-16/backtest_profile_result.json`
- `MTC_COMMAND_CENTER/11_TRIAGE/GEN_RSI_TRXUSDT_1H_SOURCE_NAKED_ARTIFACT_GENERATION_REPORT_2026-06-16.md`
- `MTC_COMMAND_CENTER/06_SCHEMAS/backtest_profile_result.schema.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/iter_05/evaluation_artifacts/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/iter_05/scorecard_v2/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/iter_05/all_gate/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/iter_05/all_gate_g3enriched/GEN_RSI_OVERSOLD_REVERSAL__TRXUSDT__1h.eval.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/iter_05/gate2_scorecards/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/night_1m_2026-06-07/iter_05/gate3_scorecards/GEN_RSI_OVERSOLD_REVERSAL_TRXUSDT_1h.scorecard.json`

## 3. Artifact existence and counts

- Target artifact exists: PASS.
- Generation report exists: PASS.
- Recursive `backtest_profile_result.json` count under `05_BACKTEST_RESULTS`: 2.
- Recursive `top_results.json` count under `05_BACKTEST_RESULTS`: 0.

## 4. Schema validation

- JSON parse: PASS.
- `jsonschema.validate(artifact, backtest_profile_result.schema.json)`: PASS.
- `results` is present and contains exactly one row.

## 5. Row identity validation

Expected identity is present exactly:

- `strategy_id`: `GEN_RSI_OVERSOLD_REVERSAL`
- `symbol`: `TRXUSDT`
- `timeframe`: `1h`
- `profile`: `SOURCE_NAKED`
- `profile_type`: `SOURCE_NAKED`
- `source_strategy_id`: `GEN_RSI_OVERSOLD_REVERSAL|TRXUSDT|1h`

No mixed result row was found for `LINKUSDT|2h`, `TRXUSDT|2h`, `ETHUSDT|4h`, `LTCUSDT|1h`, or another symbol/timeframe.

## 6. Metrics validation

The required metrics are stored under `results[0].metrics` and match the approved source mapping:

| Metric | Expected | Actual | Result |
|---|---:|---:|---|
| `net_profit` | 70.498 | 70.498 | PASS |
| `profit_factor` | 1.381 | 1.381 | PASS |
| `max_drawdown` | 13.07 | 13.07 | PASS |
| `trade_count` | 280 | 280 | PASS |
| `sharpe` | 1.753 | 1.753 | PASS |
| `sortino` | 2.4775 | 2.4775 | PASS |
| `max_loss_streak` | 10 | 10 | PASS |
| `buy_hold_alpha` | -37.743 | -37.743 | PASS |

## 7. Null/default validation

The required missing values are explicit nulls in the artifact:

- `results[0].metrics.win_rate`: null.
- `results[0].parameter_set_id`: null.
- `results[0].metrics.buy_hold_return`: null.
- `results[0].metrics.exposure`: null.
- `results[0].metrics.avg_trade`: null.

No missing value fabrication was found:

- `avg_trade_vs_cost` was not remapped to `metrics.avg_trade`.
- `benchmark.excess_alpha_pct` remains separate from `metrics.buy_hold_return`; `metrics.buy_hold_return` stays null.

## 8. Gate/promotion validation

Gate summary is preserved:

- Gate 1: `OK`, score `96.0`.
- Gate 1B: `OK`, score `80.0`.
- Gate 2: `OK`, score `92.0`.
- Gate 3: `INCOMPLETE`, score `46.0`.
- `all_pass`: false.
- `promotable`: false.
- `blocking`: `["gate3"]`.

Safety and promotion fields are preserved:

- `promotion_status`: `RESEARCH_ONLY`.
- `paper_ready`: false.
- `live_ready`: false.
- `native_us_equities`: false.
- `mtc_light`: false.
- `risk_normalized`: false.
- `top_results_ranking`: false.
- `strategy_promotion`: false.

## 9. Provenance validation

All six approved provenance/source paths exist on disk and remain inside the approved `night_1m_2026-06-07/iter_05` bucket. The artifact's `artifacts` object points to the expected eval, scorecard_v2, all_gate, all_gate_g3enriched, gate2_scorecards, and gate3_scorecards files. The `provenance` object also points to the expected primary eval and primary scorecard and marks `same_bucket_only=true`.

## 10. `top_results.json` validation

Recursive search under `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS` found 0 `top_results.json` files. PASS.

## 11. Git/index status

Preflight results:

- `git status --short`: working tree was already dirty with existing modified/untracked files before this audit report was created.
- `git diff --cached --stat`: empty.
- `git log --oneline -8`: latest commits begin with `aa63bbc Add night artifact reader schemas`, `3900ec6 Lazy-load scorecard gate details`, and `7ce20ff Slim dashboard snapshot payload`.

Post-report index check:

- `git diff --cached --stat`: empty.
- The audit report is untracked; no files were staged.

## 12. Protected scope check

Both protected-scope checks returned no output:

- `git diff --name-only -- MTC_COMMAND_CENTER/02_MTC_BACKTEST MTC_COMMAND_CENTER/07_ADAPTERS MTC_COMMAND_CENTER/01_PINE MTC_COMMAND_CENTER/MTC_V2`
- `git diff --cached --name-only -- MTC_COMMAND_CENTER/02_MTC_BACKTEST MTC_COMMAND_CENTER/07_ADAPTERS MTC_COMMAND_CENTER/01_PINE MTC_COMMAND_CENTER/MTC_V2`

Protected scope is clean for this audit.

## 13. Dashboard/read-model visibility if checked

No dashboard server was started. Existing local checks did not produce a usable snapshot:

- `http://127.0.0.1:8765/api/snapshot?refresh=1`: timed out.
- `http://127.0.0.1:8777/api/snapshot?refresh=1`: unreachable.

Static artifact audit is sufficient for this request; dashboard/read-model visibility remains optional follow-up.

## 14. Issues found

None for the static artifact contract.

Residual context only: the repo working tree contains unrelated pre-existing modified and untracked files. The Git index remained empty throughout this audit.

## 15. Recommended next action

Accept the artifact as a valid research-only `SOURCE_NAKED` profile result. Do not promote it, do not paper-trade it, and do not treat it as live-ready because Gate 3 is still incomplete and all promotion/readiness flags are false.

## 16. Safety confirmation

- No code files were modified by this audit.
- No files were staged or committed.
- No files were deleted, reset, moved, or cleaned.
- No backtests or optimizations were run.
- No `top_results.json` was generated.
- No Pine, MTC_V2, parity, backtest engine execution logic, broker/live/paper execution logic, API write behavior, or strategy logic was touched.
- The only intended write from this audit is this report file.

Final verdict: ACCEPT
