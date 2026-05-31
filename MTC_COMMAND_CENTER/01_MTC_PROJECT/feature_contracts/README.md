# MTC V2 Generic Feature Contracts

Feature contracts are the local source of truth for any future MTC V2 feature change. The required workflow is:

1. contract
2. implementation
3. trace
4. parity
5. acceptance gate

No feature is ready until its contract-specific acceptance profile passes or the user explicitly accepts a classified mismatch.

## Contract Skeleton

```yaml
feature_id: producer_range_filter_v1
feature_name: range_filter
feature_type: signal_producer
version: 0.1.0
status: draft
owner: codex
created_at: 2026-04-26
updated_at: 2026-04-26
description: Replaces Supertrend raw signal producer with Range Filter.
implementation_targets:
  pine_files_touched: []
  python_files_touched: []
  pine_anchor_points: ["isolated PineTS adapter first"]
  python_anchor_points: ["00_PYTHON/mtc_v2/signals/range_filter.py"]
  integration_mode: isolated_adapter_only
input_parameters: []
state:
  state_variables: []
  persistent_state: []
  reset_conditions: ["case start"]
  warmup_policy: {bars: contract_defined, exclude_from_comparison: true}
trace:
  required_trace_columns: ["source_price", "direction", "raw_long", "raw_short"]
  optional_trace_columns: []
  expected_event_columns: []
  signal_columns: ["raw_long", "raw_short"]
  decision_columns: []
  execution_columns: []
parity:
  required_parity_levels: ["L0", "L1", "L2"]
  tolerance_policy: {numeric_abs_tol: 1.0e-8, numeric_rel_tol: 1.0e-6, tick_tolerance: 0}
  acceptance_profile: feature_contracts/acceptance_profiles/producer_acceptance.yml
  supported_oracles: {python: true, pinets: true, pynecore: optional, vectorbt: optional, tradingview_export: final_release_audit}
  baseline_oracle: python
  candidate_oracles: ["pinets"]
safety:
  rollback_files: []
  risk_notes: []
  known_limitations: []
  not_comparable_conditions: []
reporting:
  required_report_sections: ["Command run", "Hashes", "Oracle status", "Verdict"]
  acceptance_verdicts: ["FEATURE_TRACE_PASS", "FEATURE_TRACE_FAIL", "FEATURE_TRACE_NOT_COMPARABLE"]
  final_verdict_rule: pass required acceptance profile before integration
```
