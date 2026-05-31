# CODEX NIGHTLY PROMPT — QuantLens 66 Intake Full Processing + Strategy Research

## Context

Repo root:

```text
C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2
```

QuantLens lab root:

```text
C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB
```

Prompt files to use:

```text
C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\_prompts\01_quantlens_candidate_intake_prompt.md
C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\_prompts\02_quantlens_python_experiment_runner_prompt.md
C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\_prompts\03_quantlens_parity_promoter_prompt.md
C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\_prompts\05_quantlens_nightly_batch_prompt.md
```

Do **not** use Pine integration tonight:

```text
C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\_prompts\04_quantlens_pine_integration_prompt.md
```

Reason: tonight is research/prototype/planning only. No Pine integration. No live trading. No production changes.

Input reports folder:

```text
C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\00_INBOX_REPORTS
```

Search recursively under this folder for all `.md` intake reports, including date subfolders such as:

```text
C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\00_INBOX_REPORTS\3 Mayıs
```

The user has completed approximately 66 QuantLens intake reports from YouTube transcripts. Your job is to process all of them overnight in a controlled, restartable, evidence-based way.

---

## Absolute Rules

1. Do not ask questions.
2. Start immediately.
3. Do not modify:

```text
01_PINE\MTC_V2.pine
```

4. Do not modify production Python runner behavior.
5. Do not do any live trading, broker integration, webhook execution, or alert execution.
6. Do not write secrets, API keys, tokens, or account information.
7. Do not overwrite existing reports without first reading them and creating a new timestamped or suffix version if needed.
8. Every step must be restartable/resumable.
9. If one candidate fails, write the error into that candidate’s folder and continue with the next candidate.
10. Do not launch a huge unbounded exhaustive grid. Use bounded, staged validation.
11. Use at least 5 assets per candidate whenever the candidate is testable on available data.
12. If a candidate is native to US equities but you only have crypto data, label the result clearly as `CRYPTO_PROXY`, not native validation.
13. Backtest success is not live-trading approval.
14. Pine/parity/live integration is not allowed tonight. At most, produce parity-preparation documents via prompt `03` for promising candidates.

---

## Main Mission

Process all 66 intake reports, triage them into QuantLens candidates, test the suitable candidates, and prepare a morning decision package with:

1. Best day-trade strategy candidates.
2. Best swing-trade strategy candidates.
3. Best long-term / position-investing candidates.
4. Rejected / blocked / wiki-only / salvage ideas.
5. Evidence-based next actions for each candidate.
6. No Pine changes.

The ideal morning output should tell the user:

- what was processed,
- what was skipped and why,
- what was tested,
- which strategies are promising,
- which strategies failed,
- what needs better data,
- what should be tested next,
- and whether anything deserves later parity/Pine preparation.

---

## Stage 0 — Initial Repo Safety Audit

Before doing anything else:

1. Run:

```powershell
git status --short
```

2. Record the current dirty state in:

```text
06_QUANTLENS_LAB\99_NIGHTLY_RUNS\YYYY-MM-DD_quantlens_full_intake_nightly\00_initial_git_status.txt
```

3. Create the nightly root folder:

```text
06_QUANTLENS_LAB\99_NIGHTLY_RUNS\YYYY-MM-DD_quantlens_full_intake_nightly\
```

4. Create a run log:

```text
06_QUANTLENS_LAB\99_NIGHTLY_RUNS\YYYY-MM-DD_quantlens_full_intake_nightly\nightly_run_log.md
```

5. In every report, explicitly state that this run did not intentionally touch MTC Pine or production runner files.

---

## Stage 1 — Discover and De-Duplicate Intake Reports

Search recursively:

```text
06_QUANTLENS_LAB\00_INBOX_REPORTS\**\*.md
```

Build an intake manifest:

```text
06_QUANTLENS_LAB\99_NIGHTLY_RUNS\YYYY-MM-DD_quantlens_full_intake_nightly\01_intake_manifest.csv
06_QUANTLENS_LAB\99_NIGHTLY_RUNS\YYYY-MM-DD_quantlens_full_intake_nightly\01_intake_manifest.json
```

For each `.md` file, extract where available:

```yaml
source_path:
file_name:
file_size:
sha256:
source_url:
normalized_youtube_url:
video_id:
video_title:
existing_candidate_id_if_any:
existing_status_if_any:
strategy_family_guess:
market_type_guess:
timeframe_guess:
is_duplicate_exact:
is_duplicate_semantic_possible:
```

Duplicate policy:

- If same `video_id`, same normalized URL, or same SHA256 already processed, do not process twice.
- If same strategy idea appears in multiple videos, do not duplicate blindly. Link the later report as supporting evidence to the existing candidate or create a `V2` only if there is a materially different rule set.
- Write duplicates to:

```text
06_QUANTLENS_LAB\99_NIGHTLY_RUNS\YYYY-MM-DD_quantlens_full_intake_nightly\02_duplicate_audit.md
```

---

## Stage 2 — Apply Candidate Intake Prompt to All New Reports

For every unique unprocessed intake report:

1. Read:

```text
06_QUANTLENS_LAB\_prompts\01_quantlens_candidate_intake_prompt.md
```

2. Apply that prompt exactly in spirit:

- archive/report,
- generate Candidate ID,
- decide STOP / REJECT / SALVAGE / READY_FOR_PYTHON_PROTOTYPE,
- create candidate folder,
- create metadata,
- update registry CSV and JSONL.

Expected folder outputs per prompt `01`:

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

Registry paths:

```text
06_QUANTLENS_LAB\_registry\quantlens_candidate_registry.csv
06_QUANTLENS_LAB\_registry\quantlens_candidate_registry.jsonl
```

Important:

- Do not write code in this stage.
- Do not run backtests in this stage.
- Only documentation, classification, mapping, and registry updates.

After Stage 2, create:

```text
06_QUANTLENS_LAB\99_NIGHTLY_RUNS\YYYY-MM-DD_quantlens_full_intake_nightly\03_stage1_candidate_triage_summary.md
06_QUANTLENS_LAB\99_NIGHTLY_RUNS\YYYY-MM-DD_quantlens_full_intake_nightly\03_candidate_triage_table.csv
```

---

## Stage 3 — Prioritize Test Queue

Read the registry and all new candidate metadata. Build a test queue.

Create:

```text
06_QUANTLENS_LAB\99_NIGHTLY_RUNS\YYYY-MM-DD_quantlens_full_intake_nightly\04_test_queue.md
06_QUANTLENS_LAB\99_NIGHTLY_RUNS\YYYY-MM-DD_quantlens_full_intake_nightly\04_test_queue.csv
```

### Priority order

Use this order unless the evidence in the candidate report clearly contradicts it.

#### Priority A — Day-trade candidates

Highest priority if:

- mechanical intraday rules exist,
- clear entry/exit exists,
- clear SL/TP or MTC-compatible risk management exists,
- can be tested on existing 5m data,
- not dependent on US microcap borrow/locate mechanics,
- not dependent on missing proprietary indicators.

Test first:

1. Crabel / daily range extension / opening range / range expansion models.
2. Intraday breakout/pullback/retest models with clear OHLC rules.
3. Liquidity/volatility transition models that can be proxied on crypto 5m.
4. Opening range or session-based models, but clearly label crypto session proxy limitations.
5. EMA/retest only as baseline, not as high-priority alpha.

#### Priority B — Swing-trade candidates

Test after day-trade candidates or in parallel if cheap:

1. Linda Raschke / 5SMA / pullback / range models.
2. Oliver Kell / cycle-aware pullback and trend models.
3. Anthony Shi / relative strength + sector/theme + cycle-aware momentum framework.
4. BigBeluga divergence / CHoCH / ATR concepts.
5. CANSLIM-style momentum/growth models, but only if testable with available data or as proxy.

#### Priority C — Long-term / position-investing candidates

Prepare and test if rules can be expressed using 1D/1W data:

1. Relative-strength portfolio rotation.
2. Trend-following / moving-average regime allocation.
3. CANSLIM or leadership model adapted to position trading.
4. Crypto large-cap momentum/position model.
5. Risk-managed cash/position switching.

#### Priority D — Salvage / filters / gates

Do not force as standalone strategies. Test as filters if cheap:

1. Daily extension anti-chase.
2. Market cycle phase filters.
3. Relative strength gates.
4. Volume/ATR volatility filters.
5. Time/session filters.
6. MTC SL/TP/trailing enhancement ideas.

#### Priority E — Block or defer

Block/defer if:

- needs US microcap borrow/locate/short-fee data,
- needs live order book or L2 tape,
- depends on influencer claims without rules,
- only gives vague advice,
- has no risk management,
- requires unavailable paid/proprietary indicators,
- is pure educational/process content with no testable rules.

Examples to treat carefully:

- TY Rajnus microcap short: likely `DATA_BLOCKED_US_MICROCAP` unless proper US microcap short/borrow/locate data is available.
- Generic EMA crossover/retest: likely baseline only unless it shows robust edge after fees.
- Influencer copy-trade/video extraction: wiki/process automation idea, not direct strategy edge.

---

## Stage 4 — Data Availability Audit

Before running prototypes, inspect available data manifests.

Look for existing data folders such as:

```text
06_QUANTLENS_LAB\research\data_acquisition_5m_2026_05_03
06_QUANTLENS_LAB\research\MTC_V2_OPTIMIZATION_DATA_BUNDLE*
```

Create:

```text
06_QUANTLENS_LAB\99_NIGHTLY_RUNS\YYYY-MM-DD_quantlens_full_intake_nightly\05_data_availability_audit.md
```

For each candidate, write:

```yaml
candidate_id:
native_market:
available_data:
proxy_data_used:
minimum_5_assets_available:
selected_assets:
selected_timeframes:
dataset_id:
source_type:
limitations:
```

Minimum crypto asset set when applicable:

```text
BTCUSDT
ETHUSDT
SOLUSDT
BNBUSDT
XRPUSDT
```

If more are available and runtime allows, include:

```text
DOGEUSDT
ADAUSDT
AVAXUSDT
LINKUSDT
NEARUSDT
OPUSDT
ARBUSDT
INJUSDT
APTUSDT
SUIUSDT
POLUSDT
```

If a strategy requires 5m data and 5m is missing, use existing downloader only if already available and safe. Keep download bounded. Do not block the full run if data acquisition fails.

---

## Stage 5 — Python Prototype / Backtest for READY Candidates

Read:

```text
06_QUANTLENS_LAB\_prompts\02_quantlens_python_experiment_runner_prompt.md
06_QUANTLENS_LAB\_prompts\05_quantlens_nightly_batch_prompt.md
```

For each `READY_FOR_PYTHON_PROTOTYPE` candidate in priority order:

1. Create isolated result folder:

```text
06_QUANTLENS_LAB\05_BACKTEST_RESULTS\<CandidateID>\
```

2. Use isolated prototype/adapter only.
3. Do not change production runner behavior.
4. Do bounded validation.
5. Use at least 5 assets if available.
6. Use the candidate’s own timeframe if specified.
7. Use 5m data for day-trade/intraday candidates where possible.
8. Use 1D/4H/1W where appropriate for swing/position candidates.
9. Include commission/slippage assumptions.
10. Run cost stress at base / 2x / 3x costs.
11. Ensure fee stress is monotonic: base >= 2x >= 3x.
12. Check lookahead/repaint risk.
13. Check trade count.
14. Check OOS/walk-forward if data length is enough.
15. Check sensitivity/robustness without exhaustive grid.
16. Record failures and continue.

Required result files:

```text
06_QUANTLENS_LAB\05_BACKTEST_RESULTS\<CandidateID>\
├─ backtest_config.yaml
├─ symbol_results.csv
├─ walk_forward_results.csv
├─ robustness_summary.md
├─ pass_fail_decision.md
├─ next_action.md
└─ errors.md  # only if needed
```

Registry status must become one of:

```text
BACKTEST_FAILED
BACKTEST_PROMISING
BACKTEST_PASSED
NEEDS_MORE_INFO
```

### Classification guardrails

Do not classify as passed only because net return is positive.

Use these categories:

```yaml
BACKTEST_PASSED:
  - survives costs
  - multi-asset robustness acceptable
  - OOS/walk-forward acceptable
  - no obvious lookahead
  - drawdown manageable
  - trade count sufficient
  - not single-outlier dependent

BACKTEST_PROMISING:
  - edge exists but weak robustness or high drawdown
  - needs better data
  - works only as filter/gate
  - good risk-adjusted subset but not enough proof

BACKTEST_FAILED:
  - PF below acceptable after costs
  - drawdown too high
  - edge disappears under fee stress
  - too few trades
  - unstable across assets/timeframes

NEEDS_MORE_INFO:
  - rules incomplete
  - data unavailable
  - native market cannot be proxied responsibly
```

---

## Stage 6 — Stage 2 Robustness for Best Candidates Only

After all candidates have at least initial pass/fail result, select top candidates for additional robustness.

Selection max:

```yaml
max_day_trade_candidates_stage2: 3
max_swing_candidates_stage2: 3
max_position_candidates_stage2: 2
```

Stage 2 should include:

- expanded assets if available,
- parameter sensitivity,
- train/test split,
- walk-forward,
- fee stress,
- slippage stress,
- long-only/short-only separation if relevant,
- regime breakdown,
- return concentration check,
- drawdown clustering,
- compare against baseline.

Create:

```text
06_QUANTLENS_LAB\99_NIGHTLY_RUNS\YYYY-MM-DD_quantlens_full_intake_nightly\06_stage2_robustness_selection.md
```

and per selected candidate:

```text
06_QUANTLENS_LAB\05_BACKTEST_RESULTS\<CandidateID>\stage2_robustness_summary.md
```

---

## Stage 7 — Parity Preparation for Promising/Passed Candidates Only

Read:

```text
06_QUANTLENS_LAB\_prompts\03_quantlens_parity_promoter_prompt.md
```

For candidates with:

```text
BACKTEST_PROMISING
BACKTEST_PASSED
```

create parity preparation documents only. Do not write Pine. Do not edit production runner.

Output:

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

If parity risk is not solvable, status:

```text
PARITY_BLOCKED
```

If ready for later human review:

```text
READY_FOR_PINE_INTEGRATION
```

Important: even if a candidate becomes `READY_FOR_PINE_INTEGRATION`, do **not** apply prompt `04` tonight.

---

## Stage 8 — Final Morning Reports

Create the main nightly summary:

```text
06_QUANTLENS_LAB\05_BACKTEST_RESULTS\nightly_summary_YYYY-MM-DD.md
```

Also create a full run report:

```text
06_QUANTLENS_LAB\99_NIGHTLY_RUNS\YYYY-MM-DD_quantlens_full_intake_nightly\FINAL_NIGHTLY_MASTER_REPORT.md
```

Create separate decision reports:

```text
06_QUANTLENS_LAB\99_NIGHTLY_RUNS\YYYY-MM-DD_quantlens_full_intake_nightly\DAY_TRADE_CANDIDATES.md
06_QUANTLENS_LAB\99_NIGHTLY_RUNS\YYYY-MM-DD_quantlens_full_intake_nightly\SWING_TRADE_CANDIDATES.md
06_QUANTLENS_LAB\99_NIGHTLY_RUNS\YYYY-MM-DD_quantlens_full_intake_nightly\POSITION_INVESTING_CANDIDATES.md
06_QUANTLENS_LAB\99_NIGHTLY_RUNS\YYYY-MM-DD_quantlens_full_intake_nightly\REJECTED_BLOCKED_AND_SALVAGE.md
06_QUANTLENS_LAB\99_NIGHTLY_RUNS\YYYY-MM-DD_quantlens_full_intake_nightly\NEXT_ACTION_PLAN.md
```

Create CSV dashboards:

```text
06_QUANTLENS_LAB\99_NIGHTLY_RUNS\YYYY-MM-DD_quantlens_full_intake_nightly\MASTER_CANDIDATE_STATUS.csv
06_QUANTLENS_LAB\99_NIGHTLY_RUNS\YYYY-MM-DD_quantlens_full_intake_nightly\MASTER_BACKTEST_RESULTS.csv
06_QUANTLENS_LAB\99_NIGHTLY_RUNS\YYYY-MM-DD_quantlens_full_intake_nightly\MASTER_PRIORITY_RANKING.csv
```

### FINAL_NIGHTLY_MASTER_REPORT.md must include

```markdown
# QuantLens Full Intake Nightly Report

## 1. Executive Summary
- total intake files found
- unique intake files
- duplicates skipped
- candidates created
- rejected
- salvaged
- ready for prototype
- backtested
- failed
- promising
- passed
- parity prepared
- blocked/deferred

## 2. Safety Statement
- MTC_V2.pine touched? yes/no
- production runner touched? yes/no
- live trading touched? yes/no
- secrets touched? yes/no

## 3. Best Day-Trade Candidates
For each:
- rank
- candidate_id
- source report
- strategy idea
- assets/timeframes tested
- PF
- net return
- max DD
- trade count
- fee stress
- decision
- next action

## 4. Best Swing-Trade Candidates
Same fields.

## 5. Best Position-Investing Candidates
Same fields or explain if not fully testable.

## 6. Candidates Not Worth More Time
- candidate_id
- reason
- evidence

## 7. Candidates Needing Better Data
- candidate_id
- native data required
- why proxy is insufficient

## 8. MTC V2 Mapping
- producers
- entry gates
- guards
- exits
- SL/TP/trailing
- sizing
- portfolio/exposure controls

## 9. Parity/Pine Readiness
- ready later
- blocked
- must not integrate yet

## 10. Tomorrow’s Recommended Action
- exact next commands/prompts
- which candidates to inspect first
- which results need human review
```

---

## Stage 9 — Validation and Integrity Checks

Before finalizing, run:

1. `git status --short`
2. Python compile checks for new Python files.
3. Any available unit tests for the isolated research code.
4. CSV existence checks.
5. Registry consistency check:
   - every candidate folder has metadata,
   - every metadata has registry row,
   - every tested candidate has result folder,
   - every backtest status is valid.

Write:

```text
06_QUANTLENS_LAB\99_NIGHTLY_RUNS\YYYY-MM-DD_quantlens_full_intake_nightly\VALIDATION_CHECKLIST.md
06_QUANTLENS_LAB\99_NIGHTLY_RUNS\YYYY-MM-DD_quantlens_full_intake_nightly\FINAL_GIT_STATUS.txt
```

---

## Runtime Management

This is an overnight run. Work continuously, but stay bounded.

Use this behavior:

```yaml
if_time_is_plenty:
  - process_all_unique_intake_reports
  - prototype_all_READY_FOR_PYTHON_PROTOTYPE_candidates
  - stage2_top_candidates
  - parity_prepare_promising_candidates

if_time_is_limited:
  - finish_intake_triage_for_all
  - test_top_day_trade_candidates_first
  - test_top_swing_candidates_second
  - prepare_position_investing_candidates_as_research_plan_if_not_tested
  - write exactly what remains

if_errors_happen:
  - record error
  - mark candidate as NEEDS_MORE_INFO or BACKTEST_FAILED as appropriate
  - continue
```

Do not stop the entire nightly run because of one failure.

---

## Web Research Policy

Use web research only when it adds real value:

- to clarify a named strategy,
- to verify rule definitions,
- to identify missing original source,
- to understand native market requirements,
- to check whether a claimed indicator/strategy is real.

When web research is used, save links and notes into:

```text
06_QUANTLENS_LAB\99_NIGHTLY_RUNS\YYYY-MM-DD_quantlens_full_intake_nightly\WEB_RESEARCH_NOTES.md
```

Do not let web research consume the whole night. If web is unavailable, proceed from local reports and write the limitation.

---

## Important Strategy Interpretation Rules

1. Treat a YouTube strategy as suspicious until tested.
2. Prefer simple, testable rules.
3. Do not overfit.
4. Do not trust generic “works on all markets” claims.
5. If strategy lacks risk management, it cannot pass.
6. If strategy depends on discretionary reading, convert it to:
   - process module,
   - filter/gate,
   - regime detector,
   - or salvage idea.
7. If a strategy is native to a market you do not have data for, do not fake confidence.
8. Crypto proxy can only prove structural possibility, not native equity validity.
9. If a candidate only improves another strategy as a filter, classify it as filter/gate, not producer.
10. Separate:
    - day-trade,
    - swing-trade,
    - position-investing,
    - MTC helper/filter,
    - wiki/process-only.

---

## Expected Morning Output

When finished, the final response/report should be short and point the user to the files:

```text
Completed.

Main report:
06_QUANTLENS_LAB\99_NIGHTLY_RUNS\YYYY-MM-DD_quantlens_full_intake_nightly\FINAL_NIGHTLY_MASTER_REPORT.md

Day-trade candidates:
...\DAY_TRADE_CANDIDATES.md

Swing-trade candidates:
...\SWING_TRADE_CANDIDATES.md

Position-investing candidates:
...\POSITION_INVESTING_CANDIDATES.md

Nightly summary:
06_QUANTLENS_LAB\05_BACKTEST_RESULTS\nightly_summary_YYYY-MM-DD.md

Safety:
- MTC_V2.pine changed: NO
- Production runner changed: NO
- Live trading touched: NO

Top next action:
<write exact recommendation>
```

Start now.
