# CODEX OVERNIGHT MASTER PROMPT — QuantLens 66 Intake Processing + Prototype Backtest

## ABSOLUTE MODE

NO QUESTIONS. START IMMEDIATELY.

You are working inside this repo:

```text
C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2
```

Primary goal for this overnight run:

1. Process all 66 finished ChatGPT intake `.md` reports.
2. Apply the repo prompt `06_QUANTLENS_LAB\_prompts\01_quantlens_candidate_intake_prompt.md` to every intake report.
3. Build/update the QuantLens registry.
4. Select `READY_FOR_PYTHON_PROTOTYPE` candidates.
5. Run bounded, restartable Python prototype/backtest work using the rules in `05_quantlens_nightly_batch_prompt.md` and `02_quantlens_python_experiment_runner_prompt.md`.
6. If any candidate becomes `BACKTEST_PROMISING` or `BACKTEST_PASSED`, prepare parity-readiness documentation using `03_quantlens_parity_promoter_prompt.md`.
7. Do **not** do Pine integration tonight.
8. Produce a morning summary with ranked:
   - day-trade strategy candidates,
   - swing-trade strategy candidates,
   - long-term / position-trading / investment-style candidates,
   - salvage-only risk/position-management modules.

---

## CRITICAL SAFETY RULES

These rules override every other instruction.

- Do **not** modify `01_PINE\MTC_V2.pine`.
- Do **not** modify production Python runner behavior.
- Do **not** start large exhaustive grids.
- Do **not** use secrets, API keys, broker accounts, live trading credentials, webhook URLs, or live-trade actions.
- Do **not** run Pine integration prompt `04_quantlens_pine_integration_prompt.md` tonight.
- Do **not** claim TradingView/Pine parity unless a real parity package and required lifecycle evidence exist.
- Do **not** stop the whole overnight run because one candidate fails.
- If a candidate fails, write the error to that candidate’s output folder, mark next action, and continue.
- Every step must be restartable/resumable.
- Avoid overwriting existing files. Read first. If conflict exists, create `_V2`, timestamp, or append safely.

---

## INPUTS

Prompt files are expected here:

```text
06_QUANTLENS_LAB\_prompts\01_quantlens_candidate_intake_prompt.md
06_QUANTLENS_LAB\_prompts\02_quantlens_python_experiment_runner_prompt.md
06_QUANTLENS_LAB\_prompts\03_quantlens_parity_promoter_prompt.md
06_QUANTLENS_LAB\_prompts\04_quantlens_pine_integration_prompt.md
06_QUANTLENS_LAB\_prompts\05_quantlens_nightly_batch_prompt.md
06_QUANTLENS_LAB\_prompts\README_PROMPTS.md
```

The 66 finished intake reports should be placed in this folder before starting:

```text
06_QUANTLENS_LAB\00_CHATGPT_INTAKE_REPORTS
```

If the folder name is different, search under:

```text
06_QUANTLENS_LAB
```

for `.md` files that look like completed intake reports.

---

## PHASE 0 — PRE-FLIGHT CHECK

Before doing any work:

1. Run `git status --short`.
2. Record repo state in:

```text
06_QUANTLENS_LAB\reports\nightly\preflight_YYYY-MM-DD_HHMM.md
```

3. Verify the prompt files exist.
4. Verify the intake report folder exists.
5. Count intake `.md` files.
6. Create or verify these folders:

```text
06_QUANTLENS_LAB\00_INBOX_REPORTS
06_QUANTLENS_LAB\01_TRIAGED_CANDIDATES
06_QUANTLENS_LAB\02_REJECTED
06_QUANTLENS_LAB\03_SALVAGE_IDEAS
06_QUANTLENS_LAB\04_PYTHON_PROTOTYPES
06_QUANTLENS_LAB\05_BACKTEST_RESULTS
06_QUANTLENS_LAB\06_PROMOTED_TO_PARITY
06_QUANTLENS_LAB\_registry
06_QUANTLENS_LAB\reports\nightly
```

7. Create a run manifest:

```text
06_QUANTLENS_LAB\reports\nightly\run_manifest_YYYY-MM-DD_HHMM.json
```

Manifest fields:

```json
{
  "run_started_at": "",
  "repo_root": "",
  "input_report_count": 0,
  "input_report_paths": [],
  "processed_reports": [],
  "failed_reports": [],
  "triaged_candidates": [],
  "backtested_candidates": [],
  "promoted_candidates": [],
  "skipped_candidates": [],
  "final_summary_path": ""
}
```

---

## PHASE 1 — APPLY PROMPT 01 TO ALL 66 INTAKE REPORTS

Read and follow:

```text
06_QUANTLENS_LAB\_prompts\01_quantlens_candidate_intake_prompt.md
```

For each intake report:

1. Read the full file.
2. Extract:
   - source URL,
   - video title,
   - current intake verdict,
   - candidate/salvage/reject rationale,
   - any strategy atoms,
   - market type,
   - timeframe,
   - risk-management notes,
   - whether it is day trade, swing trade, position trade, or investment style.
3. Archive/copy raw report into:

```text
06_QUANTLENS_LAB\00_INBOX_REPORTS
```

4. Generate a Candidate ID using the rule from prompt 01:

```text
QL_YYYY-MM-DD_<MARKET>_<TF>_<SHORT_STRATEGY_SLUG>
```

5. If slug collision occurs, append `_V2`, `_V3`, etc.
6. Classify into one of:
   - `STOP`
   - `REJECT`
   - `SALVAGE`
   - `READY_FOR_PYTHON_PROTOTYPE`
7. Create the candidate output folder according to prompt 01:

```text
<CandidateID>\
├─ 00_raw_quantlens_report.md
├─ 01_candidate_metadata.yaml
├─ 02_codex_triage.md
├─ 03_mtc_module_mapping.md
├─ 04_experiment_plan.md
├─ 05_risks_and_unknowns.md
└─ 06_next_action.md
```

8. Update both registry files:

```text
06_QUANTLENS_LAB\_registry\quantlens_candidate_registry.csv
06_QUANTLENS_LAB\_registry\quantlens_candidate_registry.jsonl
```

Required metadata fields:

```yaml
candidate_id:
source_url:
video_title:
quantlens_decision:
codex_status:
market_type:
primary_timeframe:
strategy_type:
commercial_value_score:
complexity_score:
repaint_risk:
lookahead_risk:
overfit_risk:
closed_source_risk:
risk_management_quality:
candidate_kind:
  producer:
  entry_gate:
  guard:
  confirmation:
  exit_rule:
  sl_tp_method:
  trailing_be_method:
  money_management:
existing_mtc_overlap:
new_feature_required:
recommended_next_step:
created_at:
updated_at:
```

9. If a report is duplicate or nearly duplicate:
   - Do not create redundant candidate logic.
   - Link it to the existing candidate.
   - Write duplicate reason.
   - Continue.

10. If a report is only psychological/process/risk content:
   - Usually classify as `SALVAGE`.
   - Map it to MTC layers such as:
     - Position Sizing,
     - PortfolioState,
     - Position Manager,
     - Exit Rules,
     - Risk Guard,
     - Drawdown Throttle.

11. If a report has no executable edge:
   - Mark `REJECT` or `WIKI_ONLY/SALVAGE`, depending on usefulness.
   - Do not waste backtest time.

---

## PHASE 2 — REGISTRY AUDIT + RANKING

After all 66 reports are triaged, create:

```text
06_QUANTLENS_LAB\reports\nightly\registry_audit_YYYY-MM-DD.md
```

Include:

1. Total reports processed.
2. Counts by status:
   - READY_FOR_PYTHON_PROTOTYPE
   - SALVAGE
   - REJECT
   - STOP
   - duplicate
   - NEEDS_MORE_INFO
3. Top candidates ranked by:
   - rule clarity,
   - OHLCV testability,
   - risk-management quality,
   - data availability,
   - MTC overlap/reuse potential,
   - likely commercial value,
   - low repaint/lookahead risk,
   - low complexity.
4. Separate rankings:
   - Day-trade / intraday / 5m candidates.
   - Swing-trade / daily candidates.
   - Position-trade / weekly candidates.
   - Long-term investment-style candidates.
   - Salvage-only risk modules.

Recommended scoring:

```text
FinalPriorityScore =
  commercial_value_score * 2
+ risk_management_quality * 2
+ OHLCV_testability_score * 2
+ clarity_score * 2
+ MTC_reuse_score
- complexity_score
- overfit_risk
- repaint_risk
- lookahead_risk
```

---

## PHASE 3 — NIGHTLY PYTHON PROTOTYPE/BACKTEST LOOP

Read and follow:

```text
06_QUANTLENS_LAB\_prompts\05_quantlens_nightly_batch_prompt.md
06_QUANTLENS_LAB\_prompts\02_quantlens_python_experiment_runner_prompt.md
```

Process candidates with `codex_status: READY_FOR_PYTHON_PROTOTYPE`.

Important: do not run a huge exhaustive grid. Use bounded validation only.

Use this priority order:

1. Highest-ranked intraday/day-trade candidates with clear 5m rules.
2. Highest-ranked swing candidates with daily/weekly rules.
3. Position-trade candidates.
4. Only then lower-priority candidates.

For each selected candidate:

1. Read:
   - `01_candidate_metadata.yaml`
   - `02_codex_triage.md`
   - `03_mtc_module_mapping.md`
   - `04_experiment_plan.md`
   - `05_risks_and_unknowns.md`
2. If critical rules are missing, mark `NEEDS_MORE_INFO` and continue.
3. Use isolated prototype/adapter approach only.
4. Do not change production runner behavior.
5. Use manifest-first data selection.
6. Report:
   - dataset_id,
   - source_type,
   - symbols,
   - timeframe,
   - date range,
   - commission assumption,
   - slippage assumption.
7. Suggested symbols if available:
   - BTCUSDT
   - ETHUSDT
   - SOLUSDT
   - BNBUSDT
   - XRPUSDT
   - other existing data-bundle symbols where appropriate
8. Validation must include bounded checks:
   - in-sample / out-of-sample split,
   - walk-forward or rolling validation if feasible,
   - robustness/sensitivity,
   - enough trade-count warning,
   - per-symbol result table.
9. Net profit alone is not pass criterion.
10. Save output to:

```text
06_QUANTLENS_LAB\05_BACKTEST_RESULTS\<CandidateID>\
├─ backtest_config.yaml
├─ symbol_results.csv
├─ walk_forward_results.csv
├─ robustness_summary.md
├─ pass_fail_decision.md
└─ next_action.md
```

11. Registry status must become one of:
   - `BACKTEST_FAILED`
   - `BACKTEST_PROMISING`
   - `BACKTEST_PASSED`
   - `NEEDS_MORE_INFO`

12. If runtime gets too long:
   - stop that candidate safely,
   - write partial result,
   - mark `PARTIAL_RUNTIME_LIMIT`,
   - continue to the next candidate.

---

## PHASE 4 — PARITY PREPARATION FOR PROMISING/PASSED ONLY

For candidates with status:

```text
BACKTEST_PROMISING
BACKTEST_PASSED
```

read and follow:

```text
06_QUANTLENS_LAB\_prompts\03_quantlens_parity_promoter_prompt.md
```

Create:

```text
06_QUANTLENS_LAB\06_PROMOTED_TO_PARITY\<CandidateID>\
├─ 00_backtest_summary.md
├─ 01_feature_contract.yaml
├─ 02_python_reference_logic.md
├─ 03_pine_integration_plan.md
├─ 04_parity_test_plan.md
├─ 05_expected_risks.md
└─ 06_go_no_go.md
```

Feature type must be explicitly one or more of:

```text
producer
entry_gate
guard
confirmation
exit_rule
SL/TP
trailing/BE
sizing
```

If parity risk is unresolved, mark:

```text
PARITY_BLOCKED
```

If successful, mark:

```text
READY_FOR_PINE_INTEGRATION
```

Important:

- Do not modify Pine tonight.
- Do not write integration code tonight.
- Only prepare contract, reference logic, integration plan, and parity test plan.

---

## PHASE 5 — MORNING SUMMARY

Create the main morning report:

```text
06_QUANTLENS_LAB\05_BACKTEST_RESULTS\nightly_summary_YYYY-MM-DD.md
```

Also copy/link it to:

```text
06_QUANTLENS_LAB\reports\nightly\NIGHTLY_MASTER_SUMMARY_YYYY-MM-DD.md
```

The summary must include:

## 1. Executive Summary

- How many intake reports were found.
- How many were processed.
- How many failed and why.
- How many candidates were:
  - READY_FOR_PYTHON_PROTOTYPE
  - SALVAGE
  - REJECT
  - BACKTEST_FAILED
  - BACKTEST_PROMISING
  - BACKTEST_PASSED
  - NEEDS_MORE_INFO
  - PARITY_BLOCKED
  - READY_FOR_PINE_INTEGRATION

## 2. Best Day-Trade / Intraday Candidates

For each:

```text
Candidate ID:
Status:
Source:
Core idea:
Timeframe:
Symbols tested:
Result:
Robustness:
Main risk:
Next action:
Output path:
```

## 3. Best Swing-Trade Candidates

Same format.

## 4. Best Position-Trade / Long-Term Investment Candidates

Same format.

## 5. Best Salvage Modules

Group by MTC layer:

- Signal Producer
- Entry Gates
- Confirmation
- Guards
- Position Manager
- Position Sizing
- Exit Rules
- SL/TP
- Trailing/BE
- PortfolioState
- Reporting/Analytics

## 6. Backtest Results Table

Columns:

```text
candidate_id
strategy_type
timeframe
symbols
net_profit
max_drawdown
profit_factor
win_rate
trade_count
walk_forward_result
robustness_result
status
next_action
output_path
```

If metrics are unavailable, write `N/A` and explain.

## 7. Do Not Trust Yet

List candidates that looked good but are risky because of:

- too few trades,
- high overfit risk,
- missing fundamental data,
- lookahead risk,
- repaint risk,
- insufficient market diversity,
- single-symbol dependence,
- unrealistic commission/slippage,
- suspicious sensitivity.

## 8. Tomorrow Morning Action Plan

Create a clear next-step list for Barış:

1. What to inspect first.
2. Which candidate to give to Codex/Claude next.
3. Which candidates should be rejected.
4. Which candidates need more transcript/manual rules.
5. Which ones can go to parity promoter.
6. Which ones should wait before Pine.

## 9. Files Created / Modified

List every file created or modified.

## 10. Git Status

Run and include:

```bash
git status --short
```

If any unsafe file changed, flag it loudly.

---

## FINAL BEHAVIOR

- Work continuously until the run is complete or the available time/runtime is exhausted.
- Do not ask the user questions.
- Do not stop because of one candidate.
- Prefer partial completion over blocking.
- Keep everything restartable.
- No Pine integration tonight.
- Final answer must be a concise report with paths and statuses.