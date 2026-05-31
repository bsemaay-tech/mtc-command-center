# CODEX NIGHTLY — QUANTLENS 66 INTAKE → TRIAGE → BOUNDED TEST → MORNING STRATEGY SHORTLIST

## ABSOLUTE MODE

You are Codex running inside this repo:

C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2

Work continuously, carefully, and restartably until the configured stopping condition is reached. Do not ask questions. Do not wait for user input. Do not stop after the first candidate. If one candidate fails, write the error into that candidate’s output folder and continue with the next candidate.

Primary objective: process all QuantLens intake `.md` reports, create/refresh candidate documentation and registry, then run bounded Python prototype/backtest only for the best and sufficiently specified candidates. By morning, produce a practical shortlist of:

1. Day-trade strategy candidates
2. Swing-trade strategy candidates
3. Long-term / position-investing candidates
4. Candidates rejected or postponed, with reasons
5. Best next actions for tomorrow

## IMPORTANT SAFETY AND SCOPE RULES

1. Do NOT modify:
   - `01_PINE/MTC_V2.pine`
   - Any production Python runner behavior
   - Any live trading / broker / webhook / API-secret file

2. Do NOT run broad exhaustive optimization as a first step.

3. Do NOT start Pine integration tonight.

4. Do NOT use `04_quantlens_pine_integration_prompt.md` tonight unless a candidate is already explicitly `READY_FOR_PINE_INTEGRATION` before this run and all required plan checks pass. Even then, do not patch Pine tonight; prepare a plan only.

5. All prototypes must be isolated:
   - New experimental code must live under `06_QUANTLENS_LAB`
   - Do not alter production behavior
   - Use adapters/wrappers where possible
   - Keep everything feature-isolated and reversible

6. Every phase must be resumable:
   - Before writing a file, check whether it exists.
   - Do not overwrite existing files blindly.
   - If a file exists, append a new section or create `_V2` / timestamped output.
   - Maintain a run log.

7. If data is missing, mark the candidate `NEEDS_MORE_INFO`; do not invent rules.

8. If a strategy needs fundamental data not available locally, do not fake it. Mark the data dependency clearly and test only the technically testable subset if meaningful.

9. Commission/slippage assumptions must be explicit in every backtest report.

10. Net profit alone is not a pass criterion. Consider:
    - trade count
    - max drawdown
    - profit factor
    - average R
    - robustness
    - parameter sensitivity
    - multi-symbol behavior
    - walk-forward / OOS behavior
    - whether edge survives reasonable costs

## PROMPTS TO USE

Use the prompt files in:

C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\_prompts\

Apply them in this order:

1. `01_quantlens_candidate_intake_prompt.md`
   - Use for every intake report.
   - It archives the report, creates Candidate ID, classifies status, creates metadata, maps to MTC modules, and updates registry.

2. `02_quantlens_python_experiment_runner_prompt.md`
   - Use only for candidates with `READY_FOR_PYTHON_PROTOTYPE`.
   - Run bounded validation only.

3. `03_quantlens_parity_promoter_prompt.md`
   - Use only for candidates that become `BACKTEST_PASSED` or `BACKTEST_PROMISING`.
   - Produce parity contract/planning outputs only.

4. `05_quantlens_nightly_batch_prompt.md`
   - Use as the controlling night-batch behavior: runtime bound, resumable outputs, per-candidate folder, final morning summary.

Do not use `04_quantlens_pine_integration_prompt.md` for actual Pine changes tonight.

## INPUT FOLDERS

Find intake reports in these likely locations. Check all that exist:

- `06_QUANTLENS_LAB\00_INBOX_REPORTS`
- `06_QUANTLENS_LAB\INTAKE_REPORTS`
- `06_QUANTLENS_LAB\intake_reports`
- `06_QUANTLENS_LAB\_intake`
- `06_QUANTLENS_LAB\_incoming`
- Any folder under `06_QUANTLENS_LAB` containing files matching:
  - `INTAKE_*.md`
  - `*intake*.md`
  - `*.md` with QuantLens metadata

If multiple copies exist, deduplicate by:
- normalized YouTube URL
- video_id
- transcript hash if present
- title similarity

## OUTPUT ROOT

Use:

`06_QUANTLENS_LAB`

Expected important outputs:

- `_registry\quantlens_candidate_registry.csv`
- `_registry\quantlens_candidate_registry.jsonl`
- `05_BACKTEST_RESULTS\nightly_summary_2026-05-04.md`
- `05_BACKTEST_RESULTS\nightly_ranked_shortlist_2026-05-04.md`
- `05_BACKTEST_RESULTS\nightly_run_log_2026-05-04.md`
- `05_BACKTEST_RESULTS\nightly_errors_2026-05-04.md`

## RUN PHASES

### PHASE 0 — Preflight

1. Print current repo path.
2. Run `git status --short`.
3. Record dirty files.
4. Confirm `06_QUANTLENS_LAB\_prompts` exists.
5. Confirm the five prompt files exist.
6. Create a night run folder if useful:
   `06_QUANTLENS_LAB\05_BACKTEST_RESULTS\_nightly_runs\2026-05-04`
7. Create run log:
   `06_QUANTLENS_LAB\05_BACKTEST_RESULTS\nightly_run_log_2026-05-04.md`

Write:
- start time
- repo path
- prompt files found
- dirty git state
- input folders found
- output files planned

### PHASE 1 — Intake Inventory

Scan for all intake `.md` reports.

Create:

`06_QUANTLENS_LAB\05_BACKTEST_RESULTS\nightly_intake_inventory_2026-05-04.csv`

Columns:

- file_path
- file_name
- size_bytes
- detected_url
- detected_video_id
- detected_title
- detected_status
- detected_candidate_status
- has_strategy_rules
- has_risk_rules
- has_exit_rules
- has_timeframe
- likely_category
- duplicate_key
- inventory_notes

Do not yet backtest anything.

### PHASE 2 — Apply Candidate Intake Prompt to All Reports

For every intake report, apply:

`01_quantlens_candidate_intake_prompt.md`

Goal:
- archive raw report
- create Candidate ID
- decide STOP / REJECT / SALVAGE / READY_FOR_PYTHON_PROTOTYPE
- create the required candidate files
- update registry CSV and JSONL

Do not write Pine/Python strategy code during this phase.
Do not run backtests during this phase.

If a report is WIKI_ONLY or educational but useful:
- classify as SALVAGE or WIKI_ONLY-style documentation as appropriate
- do not force it into prototype unless it has codable trade rules

### PHASE 3 — Candidate Scoring and Ranking

Read all generated candidate metadata.

Create:

`06_QUANTLENS_LAB\05_BACKTEST_RESULTS\nightly_candidate_scoreboard_2026-05-04.csv`

Score each candidate from 0 to 100.

Suggested scoring:

A. Rule clarity, 0-20
- 20 = exact entry/exit/risk rules
- 10 = partial discretionary rules
- 0 = no codable rules

B. Existing MTC overlap, 0-15
- 15 = mostly reusable with MTC_V2 modules
- 8 = some new adapter needed
- 0 = large new framework needed

C. Risk management quality, 0-15
- 15 = explicit stop, sizing, exit logic
- 8 = partial stop/exit
- 0 = no risk logic

D. Backtestability tonight, 0-15
- 15 = can be tested with existing OHLCV data
- 8 = requires approximation
- 0 = requires unavailable fundamental/news data

E. Commercial/edge promise, 0-15
- 15 = strong, repeated edge logic
- 8 = plausible
- 0 = weak or generic

F. Repaint/lookahead safety, 0-10
- 10 = closed-bar deterministic
- 5 = needs careful alignment
- 0 = high lookahead risk

G. Category coverage bonus, 0-10
- day-trade, swing, long-term, risk/guard modules; add bonus to ensure diversity

Also assign:

- primary_bucket:
  - DAY_TRADE
  - SWING_TRADE
  - POSITION_INVESTING
  - RISK_GUARD
  - WIKI_ONLY
  - REJECTED
- test_priority:
  - P0_TEST_TONIGHT
  - P1_TEST_IF_TIME
  - P2_DOC_ONLY
  - P3_NEEDS_MORE_INFO
  - P4_REJECT

### PHASE 4 — Select Bounded Test Batch

Do NOT attempt to backtest all 66.

Select a practical bounded test batch:

- Top 3 day-trade candidates
- Top 5 swing-trade candidates
- Top 2 position/long-term candidates if technically testable
- Top 2 risk/guard candidates if easy to test as overlays

Maximum candidates to test tonight: 10 to 12.

If runtime is high, reduce automatically and write why.

For untested candidates, write:
- why not tested tonight
- what is needed
- whether they remain promising

### PHASE 5 — Run Isolated Python Prototype / Bounded Validation

For each selected candidate, apply:

`02_quantlens_python_experiment_runner_prompt.md`

Rules:
- use isolated prototype/adapter
- do not alter production runner behavior
- do not alter `MTC_V2.pine`
- manifest-first data selection
- explicit commission/slippage
- bounded parameter grid only
- runtime bound per candidate
- continue on error

Suggested validation structure:

For crypto / MTC-compatible symbols:
- BTCUSDT
- ETHUSDT
- SOLUSDT
- BNBUSDT
- XRPUSDT
- plus any available data bundle symbols

For day-trade candidates:
- use 5m/15m/30m if available
- enough trade count required
- penalize overly rare setups

For swing candidates:
- use 1h/4h/daily if available
- avoid lookahead from weekly/monthly conditions

For long-term / position candidates:
- if fundamental data is unavailable, test technical proxy only
- mark as partial validation, not full validation

Each candidate output path:

`06_QUANTLENS_LAB\05_BACKTEST_RESULTS\<CandidateID>\`

Must include:

- `backtest_config.yaml`
- `symbol_results.csv`
- `walk_forward_results.csv`
- `robustness_summary.md`
- `pass_fail_decision.md`
- `next_action.md`
- `runtime_log.md`
- `errors.md` if errors occur

### PHASE 6 — Promote Only If Worthy

For candidates with:

- `BACKTEST_PASSED`
- `BACKTEST_PROMISING`

Apply:

`03_quantlens_parity_promoter_prompt.md`

Do not code Pine integration.
Do not patch MTC.
Only create planning/contract docs under:

`06_QUANTLENS_LAB\06_PROMOTED_TO_PARITY\<CandidateID>\`

Required outputs:

- `00_backtest_summary.md`
- `01_feature_contract.yaml`
- `02_python_reference_logic.md`
- `03_pine_integration_plan.md`
- `04_parity_test_plan.md`
- `05_expected_risks.md`
- `06_go_no_go.md`

### PHASE 7 — Morning Summary

Create:

`06_QUANTLENS_LAB\05_BACKTEST_RESULTS\nightly_summary_2026-05-04.md`

This must be written in Turkish.

Required sections:

1. Kısa Özet
2. İşlenen Intake Sayısı
3. Oluşturulan Candidate Sayısı
4. STOP / REJECT / SALVAGE / READY_FOR_PYTHON_PROTOTYPE Dağılımı
5. Test Edilen Candidate Sayısı
6. Backtest Sonuç Dağılımı
   - BACKTEST_FAILED
   - BACKTEST_PROMISING
   - BACKTEST_PASSED
   - NEEDS_MORE_INFO
7. En İyi Day-Trade Adayları
   - Candidate ID
   - Strategy idea
   - Timeframe
   - Why promising
   - Main metrics
   - Main risks
   - Next action
8. En İyi Swing-Trade Adayları
   - Candidate ID
   - Strategy idea
   - Timeframe
   - Why promising
   - Main metrics
   - Main risks
   - Next action
9. Uzun Vadeli / Position Investing Adayları
   - Candidate ID
   - Strategy idea
   - What can be tested
   - What needs fundamental/manual data
   - Next action
10. Risk Guard / MTC_V2 Modül Fırsatları
11. Reddedilen veya Ertelenenler
12. Hatalar ve Devam Edilebilirlik
13. Yarın İçin Net İş Planı
14. Dokunulmayan Dosyalar
   - explicitly state `01_PINE/MTC_V2.pine` was not modified
   - explicitly state production runner behavior was not modified

Also create:

`06_QUANTLENS_LAB\05_BACKTEST_RESULTS\nightly_ranked_shortlist_2026-05-04.md`

with a compact ranked table:

- Rank
- Bucket
- Candidate ID
- Video/source
- Strategy core
- Status
- Score
- Test result
- Next action

## STOPPING CONDITION

Stop only after:

1. All 66 intake reports are inventoried.
2. Candidate intake phase is completed for all non-duplicate reports.
3. Scoreboard is produced.
4. Bounded tests are attempted for the selected P0/P1 candidates.
5. Promising/passed candidates are promoted to parity planning docs.
6. Morning summary and ranked shortlist are written.

If runtime or compute limits are reached:
- stop gracefully
- write exact completed/remaining counts
- write resumable command/instructions
- do not leave partial outputs unexplained

## FINAL RESPONSE FORMAT

When done, final response must be in Turkish and include:

- processed intake count
- candidate count
- tested count
- top day-trade candidate IDs
- top swing-trade candidate IDs
- top long-term candidate IDs
- paths of summary files
- confirmation that `01_PINE/MTC_V2.pine` was not modified
- confirmation that production runner behavior was not modified
- next recommended step for tomorrow

Do not claim live-trading readiness. These are research candidates only.
