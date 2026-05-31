# MTC V2 Optimization Loop + Scoring + Cross-Market Validation Plan

**Document status:** Planning document  
**Target repo folder suggestion:** `docs/optimization/` or `03_DOCS/OPTIMIZATION_LOOP_PLAN.md`  
**Intended user:** Codex / Claude / AI coding agents working inside the MTC V2 repo  
**Primary goal:** Add an AI-operated optimization and validation layer on top of the existing Feature Parity Factory without breaking Pine/Python/PineTS parity.

---

## 1. Executive Summary

### 2026-04-28 Optimization Consolidation

Current implementation status:

- Optimizer infrastructure hardening is ready.
- External optimization data bundle is ready.
- Dataset usage rules are ready and require manifest/job mode.
- Big overnight multi-asset optimization is partial, with `168337 / 6615000` split evaluations completed.
- Confirmed ranked output has `144` robust medium candidates and `0` robust strict candidates.
- Next safe action is resume/de-dup smoke, then resume the exhaustive core grid from the existing output root.
- Medium candidates are second-pass research seeds only and must not be promoted to Pine defaults.
- Optimization output does not claim TradingView release parity.

This plan defines the next development layer after the Generic Feature Parity Factory.

The system must allow an AI coding agent to:

1. Take a feature that already passed feature-level parity.
2. Integrate it as a selectable feature only after parity gates pass.
3. Run parameter variations locally without requiring TradingView export for every iteration.
4. Score each variation using risk-adjusted metrics.
5. Validate the best candidates across multiple symbols, timeframes, and market regimes.
6. Promote only robust candidates for final TradingView audit.

The desired workflow is:

```text
Feature parity PASS
→ selectable integration
→ local FAST_SUITE
→ optimization job
→ scoring/ranking
→ cross-market validation
→ out-of-sample validation
→ final candidate report
→ optional TradingView release audit
```

Important: this is not a replacement for the MTC V2 parity engine. It is an optimization layer that must sit **after** parity gates.

---

## 2. Why This Layer Exists

The external AI Backtesting Engine report introduced useful ideas:

- AI agent writes strategy variants.
- Python engine runs backtests locally.
- AI reads results and iterates.
- Hundreds or thousands of parameter variations may be tested.
- Strategies are tested across multiple markets to reduce overfitting.
- In-sample / out-of-sample validation is used.
- A scoring formula ranks candidates.
- Data may be cached locally and reused.

However, MTC V2 has a stricter requirement:

```text
Before optimizing a feature, Pine/PineTS/Python behavior must be aligned.
```

Therefore, MTC V2 must not start with “find profitable strategy”. It must start with:

```text
Prove the feature behaves the same in Python and PineTS.
Then optimize.
Then validate.
Then final TradingView audit.
```

---

## 3. Existing MTC V2 Foundation

The following foundations already exist and must be treated as the base:

### 3.1 Main local execution owner

```text
00_PYTHON/mtc_v2/*
```

The Python MTC engine remains the main local execution, backtest, optimization, and parity owner.

### 3.2 Local Pine feature oracle

```text
PineTS / pinets-cli
```

PineTS is used as a local feature/indicator/signal oracle. It is not the final trade execution authority.

### 3.3 Generic Feature Parity Factory

Existing or expected folders:

```text
feature_contracts/
parity_oracles/feature_traces/
parity_oracles/templates/
tools/scaffold_new_feature.py
parity_oracles/run_feature_parity.py
docs/CODEX_GENERIC_FEATURE_CHANGE_WORKFLOW.md
```

This system defines the mandatory workflow:

```text
contract → implementation → trace → parity → acceptance gate
```

### 3.4 First real feature POC

Range Filter already passed as an isolated `signal_producer` feature POC:

```text
feature_id: producer_range_filter_v1
verdict: FEATURE_TRACE_PASS
canonical MTC_V2.pine: not modified during POC
production Python runner: not modified during POC
TradingView export: not used
```

This proves the factory can generate and validate a new feature locally.

---

## 4. Core Principle

Optimization must never bypass parity.

Hard rule:

```text
No parameter optimization, scoring, or cross-market validation is allowed until the feature passes its contract-specific parity gate.
```

For example:

- A new producer must pass producer acceptance.
- A new stop loss must pass stop_loss acceptance.
- A new take profit must pass take_profit acceptance.
- A sizing change must pass position_sizing acceptance.
- An alert payload change must pass alert_payload acceptance.

Only then can optimization begin.

---

## 5. What We Are Building

Create a new optimization layer with these responsibilities:

```text
optimization/
├── README.md
├── schema/
│   ├── optimization_job.schema.json
│   ├── optimization_result.schema.json
│   ├── scoring_profile.schema.json
│   └── dataset_manifest.schema.json
├── jobs/
│   ├── examples/
│   └── active/
├── scoring_profiles/
│   ├── conservative.yml
│   ├── balanced.yml
│   ├── aggressive.yml
│   └── parity_first.yml
├── datasets/
│   ├── dataset_manifest.yml
│   └── regimes.yml
├── reports/
│   └── README.md
└── docs/
    ├── OPTIMIZATION_WORKFLOW.md
    ├── SCORING_RULES.md
    ├── CROSS_MARKET_VALIDATION.md
    └── CODEX_OPTIMIZATION_AGENT_RULES.md

tools/
├── run_feature_optimization.py
├── rank_optimization_results.py
├── validate_cross_market.py
├── split_in_out_sample.py
├── build_dataset_manifest.py
└── summarize_optimization_report.py
```

The exact folder names can be adjusted by Codex, but the separation must remain:

- `feature_contracts/` = feature parity rules
- `parity_oracles/` = feature and parity comparison
- `optimization/` = search, scoring, ranking, cross-market validation
- `tools/` = CLI entrypoints

---

## 6. Architecture Overview

```text
User / Codex request
        │
        ▼
Feature Contract
        │
        ▼
Feature Parity Factory
        │
        ├── Python feature trace
        ├── PineTS feature trace
        └── Acceptance profile
        │
        ▼
Feature parity PASS?
        │
        ├── No → stop, diagnose, do not optimize
        │
        └── Yes
             │
             ▼
Selectable integration
             │
             ▼
Local FAST_SUITE
             │
             ▼
Optimization Job
             │
             ├── parameter generator
             ├── Python engine runner
             ├── result normalizer
             ├── scoring profile
             └── ranking report
             │
             ▼
Cross-Market Validation
             │
             ├── symbols
             ├── timeframes
             ├── market regimes
             └── out-of-sample splits
             │
             ▼
Candidate Promotion
             │
             ├── promote to candidate
             ├── freeze parameters
             ├── generate final audit package
             └── optional TradingView export
```

---

## 7. Development Phases

## Phase 1 — Optimization Foundation

### Goal

Create the folder structure, schemas, scoring profiles, and agent rules. Do not run heavy optimization yet.

### Deliverables

```text
optimization/README.md
optimization/schema/optimization_job.schema.json
optimization/schema/optimization_result.schema.json
optimization/schema/scoring_profile.schema.json
optimization/schema/dataset_manifest.schema.json
optimization/scoring_profiles/parity_first.yml
optimization/scoring_profiles/conservative.yml
optimization/scoring_profiles/balanced.yml
optimization/scoring_profiles/aggressive.yml
optimization/docs/CODEX_OPTIMIZATION_AGENT_RULES.md
```

### Requirements

- Optimization jobs must reference a feature contract.
- Optimization jobs must record feature parity status.
- Optimization jobs must refuse to run if the feature parity gate has not passed.
- Every run must produce exact commands, hashes, and output paths.
- The first implementation must support simple grid search.
- Random search and Bayesian/Optuna search can be added later.

### Codex acceptance

Codex may return `OPTIMIZATION_FOUNDATION_READY` only if:

- Schemas exist.
- Scoring profiles exist.
- Agent rules exist.
- A sample job exists.
- No production MTC behavior is changed.

---

## Phase 2 — Dataset Manifest + Market Regime Registry

### Goal

Create a stable dataset system so optimization does not accidentally compare different data windows.

### Folder

```text
optimization/datasets/
```

### Files

```text
optimization/datasets/dataset_manifest.yml
optimization/datasets/regimes.yml
tools/build_dataset_manifest.py
tools/verify_dataset_manifest.py
```

### Dataset manifest fields

Each dataset entry should include:

```yaml
dataset_id: BTCUSDT_15m_2024_2025
symbol: BTCUSDT.P
exchange: BINANCE
timeframe: 15m
start: 2024-01-01T00:00:00Z
end: 2025-01-01T00:00:00Z
source_type: case_plan | local_csv | tradingview_export | downloaded_ccxt
source_path: cases/...
row_count: 35040
timezone: UTC
hash: sha256_here
has_gaps: false
gap_report_path: reports/...
notes: ""
```

### Regime registry fields

```yaml
regime_id: BTCUSDT_15m_TREND_UP_2024_Q1
dataset_id: BTCUSDT_15m_2024_2025
symbol: BTCUSDT.P
timeframe: 15m
start: 2024-01-01T00:00:00Z
end: 2024-03-31T23:59:59Z
regime_type: trend_up
notes: ""
```

Suggested regime types:

```text
trend_up
trend_down
sideways_chop
high_volatility
low_volatility
post_news_spike
mixed
```

### Important data rule

All timestamps must be normalized to UTC.

### Data fetching

Optional later:

```text
tools/download_ohlcv_ccxt.py
```

Data fetching must be controlled and deterministic:

- Never overwrite existing data without a new hash.
- Always save source, exchange, symbol, timeframe, start, end.
- Never mix downloaded data with TradingView export data without labeling source.

---

## Phase 3 — Optimization Job Schema

### Goal

Define how Codex will ask the optimizer to run parameter sweeps.

### Example file

```text
optimization/jobs/examples/range_filter_balanced_grid.yml
```

### Required fields

```yaml
job_id: opt_range_filter_v1_balanced_001
feature_id: producer_range_filter_v1
feature_type: signal_producer
contract_path: feature_contracts/active/producer_range_filter_v1.yml

preconditions:
  require_feature_parity_pass: true
  required_feature_parity_report: reports/parity/case_001/features/producer_range_filter_v1/FEATURE_PARITY_REPORT.json
  required_verdicts:
    - FEATURE_TRACE_PASS
    - FEATURE_TRACE_PASS_WITH_TOLERANCE

integration_mode: selectable_feature

parameter_space:
  length:
    type: int
    values: [20, 30, 40, 50, 60]
  multiplier:
    type: float
    values: [1.5, 2.0, 2.5, 3.0]
  source:
    type: enum
    values: [close, hl2]

constraints:
  max_variants: 100
  max_runtime_minutes: 30
  min_trades: 20
  max_drawdown_pct: 35

datasets:
  in_sample:
    - BTCUSDT_15m_2024_Q1
  out_of_sample:
    - BTCUSDT_15m_2024_Q2
  cross_market:
    - ETHUSDT_15m_2024_Q1
    - SOLUSDT_15m_2024_Q1

scoring_profile: optimization/scoring_profiles/balanced.yml

outputs:
  report_dir: reports/optimization/opt_range_filter_v1_balanced_001
```

### Preconditions are mandatory

The optimization runner must stop if:

- Feature parity report is missing.
- Feature parity verdict is not accepted.
- Dataset manifest cannot be verified.
- Feature is not integrated as selectable feature if the job requires full strategy execution.

---

## Phase 4 — Optimization Runner

### Tool

```text
tools/run_feature_optimization.py
```

### Command

```powershell
python tools/run_feature_optimization.py --job optimization/jobs/active/opt_range_filter_v1_balanced_001.yml
```

### Responsibilities

1. Load job file.
2. Validate job schema.
3. Verify feature parity preconditions.
4. Verify dataset manifest.
5. Generate parameter combinations.
6. Run Python MTC engine for each combination.
7. Save normalized result for every run.
8. Score each result.
9. Rank candidates.
10. Generate markdown and JSON reports.
11. Save best candidate config.
12. Never modify `MTC_V2.pine` automatically.

### Output folder

```text
reports/optimization/<job_id>/
├── job_snapshot.yml
├── parameter_grid.csv
├── all_results.csv
├── ranked_results.csv
├── best_candidates.json
├── failed_variants.json
├── OPTIMIZATION_REPORT.md
└── logs/
```

### Per-variant result fields

```csv
variant_id,
feature_id,
params_hash,
dataset_id,
symbol,
timeframe,
start,
end,
net_profit,
net_profit_pct,
max_drawdown,
max_drawdown_pct,
gross_profit,
gross_loss,
profit_factor,
win_rate,
total_trades,
avg_trade,
median_trade,
max_consecutive_losses,
exposure_pct,
sharpe_like,
sortino_like,
expectancy,
score,
status,
failure_reason
```

---

## Phase 5 — Scoring Profiles

### Goal

Ranking must not be based on profit alone.

The scoring system must protect against:

- high drawdown
- too few trades
- overfitting
- one-market-only success
- unstable parameter islands
- excessive trade frequency
- extremely low exposure with accidental profit
- unrealistic leverage/margin assumptions

### Scoring profile files

```text
optimization/scoring_profiles/parity_first.yml
optimization/scoring_profiles/conservative.yml
optimization/scoring_profiles/balanced.yml
optimization/scoring_profiles/aggressive.yml
```

### Common scoring components

```yaml
metrics:
  profit_score:
    source: net_profit_pct
    direction: maximize

  drawdown_penalty:
    source: max_drawdown_pct
    direction: minimize

  profit_factor_score:
    source: profit_factor
    direction: maximize

  win_rate_score:
    source: win_rate
    direction: maximize

  trade_count_quality:
    source: total_trades
    min_required: 20
    max_preferred: 500

  robustness_score:
    source: cross_market_median_rank
    direction: minimize

  stability_score:
    source: parameter_neighborhood_stability
    direction: maximize
```

### Suggested balanced scoring formula

Use this as a starting point:

```text
score =
  0.30 * normalized_net_profit_pct
+ 0.20 * normalized_profit_factor
+ 0.15 * normalized_win_rate
+ 0.20 * inverse_normalized_max_drawdown_pct
+ 0.10 * trade_count_quality
+ 0.05 * robustness_score
```

### Hard reject rules

Reject candidate regardless of score if:

```text
feature_parity_not_passed
dataset_manifest_invalid
total_trades < min_trades
max_drawdown_pct > max_drawdown_cap
profit_factor <= 1.0
net_profit_pct <= 0
too_many_failed_cross_market_runs
result_contains_nan_or_inf
```

### Important MTC parity rule

For parity work:

```text
Commission = 0
Slippage = 0
```

For optimization research:

```text
Commission/slippage may be enabled in separate optimization profiles,
but never mix parity results and optimization results without labeling.
```

---

## Phase 6 — Cross-Market Validation

### Goal

Prevent the optimizer from finding parameters that only work on one symbol or one period.

### Tool

```text
tools/validate_cross_market.py
```

### Command

```powershell
python tools/validate_cross_market.py --optimization-report reports/optimization/<job_id>/best_candidates.json --suite optimization/datasets/cross_market_suite.yml
```

### Suggested validation suite

```yaml
suite_id: crypto_major_15m_core
datasets:
  - BTCUSDT_15m_2024_Q1
  - ETHUSDT_15m_2024_Q1
  - SOLUSDT_15m_2024_Q1
  - BNBUSDT_15m_2024_Q1
  - ADAUSDT_15m_2024_Q1
```

### Cross-market metrics

For each candidate:

```text
median_score
mean_score
worst_market_score
positive_market_count
negative_market_count
median_drawdown
worst_drawdown
trade_count_distribution
rank_stability
```

### Promotion rules

A candidate is robust only if:

```text
positive_market_count >= required_positive_markets
worst_drawdown <= max_allowed_worst_drawdown
median_score >= minimum_median_score
no single market contributes more than max_profit_concentration_pct
```

### Output

```text
reports/optimization/<job_id>/cross_market/
├── CROSS_MARKET_REPORT.md
├── cross_market_results.csv
├── cross_market_ranked_candidates.csv
└── rejected_candidates.json
```

---

## Phase 7 — In-Sample / Out-of-Sample Validation

### Goal

Prevent overfitting to a training period.

### Split types

```text
fixed_date_split
rolling_walk_forward
anchored_walk_forward
regime_based_split
```

### Basic fixed split

```yaml
in_sample:
  start: 2024-01-01T00:00:00Z
  end: 2024-06-30T23:59:59Z

out_of_sample:
  start: 2024-07-01T00:00:00Z
  end: 2024-12-31T23:59:59Z
```

### Walk-forward output

```text
reports/optimization/<job_id>/walk_forward/
├── WALK_FORWARD_REPORT.md
├── windows.csv
├── per_window_results.csv
└── promoted_candidates.json
```

### Acceptance rule

A candidate cannot be promoted if it performs only in-sample and collapses out-of-sample.

Suggested rule:

```text
out_of_sample_score >= 60% of in_sample_score
out_of_sample_net_profit_pct > 0
out_of_sample_max_drawdown_pct <= max_oos_drawdown_cap
out_of_sample_total_trades >= min_oos_trades
```

---

## Phase 8 — Candidate Promotion

### Goal

Separate “good optimization result” from “candidate worth integrating or auditing”.

### Promotion levels

```text
LEVEL_0_FEATURE_TRACE_PASS
LEVEL_1_SELECTABLE_INTEGRATION_PASS
LEVEL_2_LOCAL_FAST_SUITE_PASS
LEVEL_3_OPTIMIZATION_PASS
LEVEL_4_CROSS_MARKET_PASS
LEVEL_5_OUT_OF_SAMPLE_PASS
LEVEL_6_RELEASE_AUDIT_READY
LEVEL_7_TRADINGVIEW_AUDITED
```

### Candidate file

```text
optimization/candidates/<candidate_id>.yml
```

Example:

```yaml
candidate_id: candidate_range_filter_v1_balanced_001
feature_id: producer_range_filter_v1
source_job: opt_range_filter_v1_balanced_001
params:
  length: 40
  multiplier: 2.0
  source: hl2

promotion_level: LEVEL_5_OUT_OF_SAMPLE_PASS

evidence:
  feature_parity_report: reports/parity/case_001/features/producer_range_filter_v1/FEATURE_PARITY_REPORT.json
  fast_suite_report: reports/parity/...
  optimization_report: reports/optimization/...
  cross_market_report: reports/optimization/.../cross_market/CROSS_MARKET_REPORT.md
  walk_forward_report: reports/optimization/.../walk_forward/WALK_FORWARD_REPORT.md

risk_notes:
  - Not yet TradingView audited.
  - Do not use live.
```

### Final TradingView audit

TradingView export is still required for final release audit.

It is not required for every iteration.

---

## Phase 9 — Codex Agent Rules

Create:

```text
optimization/docs/CODEX_OPTIMIZATION_AGENT_RULES.md
```

Content must include:

### Codex must do

- Verify feature parity before optimization.
- Verify dataset manifest before running.
- Save every job snapshot.
- Save every parameter combination.
- Save every result.
- Rank using scoring profile.
- Report failed variants.
- Report rejected candidates.
- Never hide bad results.
- Keep optimization results separate from parity results.
- Use exact hashes.

### Codex must not do

- Do not modify `01_PINE/MTC_V2.pine` during optimization.
- Do not modify production Python behavior during optimization.
- Do not use TradingView export as normal loop.
- Do not use live exchange APIs.
- Do not optimize directly on final audit data.
- Do not use profit-only scoring.
- Do not delete failed variants unless user explicitly asks.
- Do not claim “ready” without promotion evidence.
- Do not enable commission/slippage in parity reports.
- Do not mix parity and optimization settings silently.

---

## Phase 10 — Reporting Standards

Every optimization job must produce:

```text
OPTIMIZATION_REPORT.md
```

Required sections:

```text
A. Executive summary
B. Job metadata
C. Feature contract
D. Preconditions checked
E. Dataset manifest summary
F. Parameter search space
G. Scoring profile
H. Number of variants
I. Failed variants
J. Top 20 candidates
K. Rejected candidates
L. Best candidate details
M. In-sample performance
N. Out-of-sample performance if applicable
O. Cross-market validation if applicable
P. Robustness notes
Q. Risk notes
R. Promotion recommendation
S. Exact commands run
T. Output files
U. Final verdict
```

Allowed verdicts:

```text
OPTIMIZATION_PASS_CANDIDATES_FOUND
OPTIMIZATION_PASS_NO_ROBUST_CANDIDATE
OPTIMIZATION_BLOCKED_FEATURE_PARITY
OPTIMIZATION_BLOCKED_DATASET
OPTIMIZATION_FAILED_RUNNER_ERROR
OPTIMIZATION_NOT_COMPARABLE
```

---

## Phase 11 — Minimal First Implementation

Do not implement everything at once.

### First optimization POC target

Use Range Filter because:

- It is a real new feature.
- It passed isolated feature parity.
- It is a signal producer.
- It is currently not integrated into canonical MTC_V2.pine yet.

### Minimum order

```text
1. Complete selectable draft integration for Range Filter.
2. Run selected FAST_SUITE locally.
3. Create optimization foundation folder/schema.
4. Create one simple grid job for Range Filter.
5. Run grid on one dataset.
6. Rank results.
7. Run top 5 candidates on 2-3 cross-market datasets.
8. Produce candidate report.
```

### Do not start with

```text
100+ datasets
Bayesian optimization
PyneCore
vectorbt
TradingView automation
live trading
```

---

## Phase 12 — Integration With Existing Feature Factory

The optimizer must consume feature contracts.

Example:

```text
feature_contracts/active/producer_range_filter_v1.yml
```

The job must verify:

```text
FEATURE_TRACE_PASS
or
FEATURE_TRACE_PASS_WITH_TOLERANCE
```

before any optimization run.

### Required link

Every optimization result must reference:

```text
feature_contract_path
feature_parity_report_path
feature_parity_verdict
case_id
data_hash
config_hash
code_hash
```

---

## Phase 13 — Suggested First Codex Prompt For This Plan

Use this prompt after Range Filter selectable draft integration passes.

```text
RAPOR BAŞLADI
Model Numarası: CODEX-MTC-V2-OPTIMIZATION-FOUNDATION-V1

You are working inside:
C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2

CONTEXT
Generic Feature Parity Factory exists.
Range Filter isolated feature POC has passed.
Do not modify canonical MTC_V2.pine unless already handled by a separate selectable integration task.
Do not use TradingView export.
Do not use live trading or API keys.

MAIN GOAL
Create the optimization loop foundation for parity-safe feature optimization.

This is a foundation task, not a heavy optimization run.

REQUIREMENTS
1. Create optimization/ folder structure.
2. Create optimization schemas.
3. Create dataset manifest format.
4. Create scoring profiles:
   - parity_first
   - conservative
   - balanced
   - aggressive
5. Create Codex optimization agent rules.
6. Create tools/run_feature_optimization.py skeleton.
7. Create tools/rank_optimization_results.py skeleton.
8. Create tools/validate_cross_market.py skeleton.
9. Create sample job:
   optimization/jobs/examples/range_filter_balanced_grid.yml
10. Do not run heavy sweeps.
11. Do not modify production behavior.
12. Add final report:
   reports/OPTIMIZATION_FOUNDATION_V1_REPORT.md

FINAL VERDICT
OPTIMIZATION_FOUNDATION_READY
OPTIMIZATION_FOUNDATION_PARTIAL
OPTIMIZATION_FOUNDATION_FAILED

RAPOR BİTTİ
```

---

## Phase 14 — Suggested Second Codex Prompt

Use this after foundation exists.

```text
RAPOR BAŞLADI
Model Numarası: CODEX-MTC-V2-RANGE-FILTER-OPTIMIZATION-POC

You are working inside:
C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2

CONTEXT
Optimization foundation exists.
Range Filter selectable draft integration has passed selected local checks.
Feature parity report exists and passed.

MAIN GOAL
Run a small controlled Range Filter optimization POC.

RULES
1. Use only one dataset first.
2. Use max 20-50 variants.
3. Use balanced scoring profile.
4. Do not use TradingView export.
5. Do not modify MTC_V2.pine.
6. Do not modify production Python behavior.
7. Save every result.
8. Report failed variants.
9. Promote no candidate beyond LEVEL_3_OPTIMIZATION_PASS.

OUTPUT
reports/optimization/opt_range_filter_v1_poc/OPTIMIZATION_REPORT.md

FINAL VERDICT
OPTIMIZATION_PASS_CANDIDATES_FOUND
OPTIMIZATION_PASS_NO_ROBUST_CANDIDATE
OPTIMIZATION_BLOCKED_FEATURE_PARITY
OPTIMIZATION_FAILED_RUNNER_ERROR

RAPOR BİTTİ
```

---

## Phase 15 — Suggested Third Codex Prompt

Use this after optimization POC produces top candidates.

```text
RAPOR BAŞLADI
Model Numarası: CODEX-MTC-V2-RANGE-FILTER-CROSS-MARKET-VALIDATION

You are working inside:
C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2

CONTEXT
Range Filter optimization POC produced top candidates.
Do not use TradingView export.
Do not modify code.

MAIN GOAL
Run cross-market validation on the top 5 Range Filter candidates.

RULES
1. Use dataset_manifest.yml.
2. Validate each dataset hash.
3. Use BTC, ETH, SOL if available.
4. Report per-market score.
5. Reject candidates that only work on one market.
6. Do not promote beyond LEVEL_4_CROSS_MARKET_PASS.

OUTPUT
reports/optimization/<job_id>/cross_market/CROSS_MARKET_REPORT.md

FINAL VERDICT
CROSS_MARKET_CANDIDATES_FOUND
CROSS_MARKET_ALL_REJECTED
CROSS_MARKET_BLOCKED_DATASET

RAPOR BİTTİ
```

---

## 16. Safety And Risk Rules

This system is for research and parity-safe development only.

It must not:

- place live trades
- use real exchange API keys
- claim profitability
- claim TradingView parity without audit
- hide failures
- optimize directly on release audit data
- overwrite canonical Pine without explicit integration task
- treat PineTS as final strategy execution authority

---

## 17. Final Recommended Implementation Order

The safest order is:

```text
1. Finish Range Filter selectable draft integration.
2. Run local selected FAST_SUITE.
3. Add optimization foundation.
4. Add dataset manifest.
5. Run tiny Range Filter optimization POC.
6. Add cross-market validation.
7. Add out-of-sample validation.
8. Promote best candidate to release audit candidate.
9. Run TradingView export only for final audit.
```

---

## 18. Definition Of Done

This plan is complete when:

```text
optimization/ folder exists
schemas exist
scoring profiles exist
dataset manifest exists
run_feature_optimization.py exists
rank_optimization_results.py exists
validate_cross_market.py exists
Range Filter sample optimization job exists
Codex optimization agent rules exist
small optimization POC runs
cross-market validation report is produced
candidate promotion file is produced
no production code is changed during optimization
```

---

## 19. Short Non-Technical Summary

The current Feature Factory checks whether Codex wrote the same logic in Pine and Python.

This new Optimization Loop comes after that.

It will let Codex try many parameter combinations, score them, test them on multiple markets, and select robust candidates.

But it must always follow this order:

```text
First correctness.
Then optimization.
Then robustness.
Then final TradingView audit.
```

---

## 20. Infrastructure Hardening Addendum

- Optimizer result rows must use `evaluation_key` and the official metrics shape from `mtc_v2.core.results` or `tools.runner_metrics_adapter`.
- Resume/de-dup registry is mandatory for overnight runs; completed evaluations must be skipped on restart.
- Result merges must de-duplicate by `evaluation_key`; hash conflicts must be reported.
- Coverage-aware scoring must require walk-forward consistency, validation/test positive ratios, and cross-timeframe/cross-symbol coverage where available.
- Single-symbol results must be marked as insufficient symbol coverage and must not be promoted as production robust candidates.
