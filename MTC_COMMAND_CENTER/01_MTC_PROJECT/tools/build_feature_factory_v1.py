from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STAMP = "feature_factory_v1_20260426"


FEATURE_TYPES = {
    "signal_producer": {
        "profile": "producer_acceptance.yml",
        "levels": ["L0", "L1", "L2", "L3"],
        "required": ["source_price", "supertrend_line", "direction", "raw_long", "raw_short", "conflict_reason"],
        "optional": ["atr", "upper_band", "lower_band", "warmup_ready", "valid_bar"],
        "anchor_pine": "02 Signal Producer section or isolated PineTS adapter",
        "anchor_python": "00_PYTHON/mtc_v2/signals/<name>.py",
    },
    "signal_transform": {
        "profile": "transform_acceptance.yml",
        "levels": ["L0", "L2", "L3"],
        "required": ["raw_long_in", "raw_short_in", "pending_side", "waiting", "confirmation_counter", "retest_level", "transformed_long", "transformed_short"],
        "optional": ["timeout_counter", "refresh_reason"],
        "anchor_pine": "L18/L18b/L21 transform block or isolated PineTS adapter",
        "anchor_python": "00_PYTHON/mtc_v2/core/confirmation.py",
    },
    "entry_filter": {
        "profile": "filter_gate_acceptance.yml",
        "levels": ["L0", "L1", "L2"],
        "required": ["filter_input_values", "allowed_long", "allowed_short", "blocked_reason_long", "blocked_reason_short"],
        "optional": ["threshold", "filter_ready"],
        "anchor_pine": "03 Entry Gates block or isolated PineTS adapter",
        "anchor_python": "00_PYTHON/mtc_v2/core/gates.py",
    },
    "exit_rule": {
        "profile": "exit_rule_acceptance.yml",
        "levels": ["L0", "L3", "L4"],
        "required": ["position_before", "exit_condition", "exit_reason", "exit_allowed", "exit_price", "close_this_bar"],
        "optional": ["exit_priority", "entry_id"],
        "anchor_pine": "06 Signal/Filter Exits or L15/L6 execution block",
        "anchor_python": "00_PYTHON/mtc_v2/core/exits.py",
    },
    "stop_loss": {
        "profile": "stop_loss_acceptance.yml",
        "levels": ["L0", "L1", "L4"],
        "required": ["initial_sl", "active_sl", "sl_update_reason", "sl_hit", "sl_exit_price", "stop_owner"],
        "optional": ["sl_distance", "tick_rounded_sl"],
        "anchor_pine": "05 Exit Skeleton stop block or isolated PineTS adapter",
        "anchor_python": "00_PYTHON/mtc_v2/core/exits.py",
    },
    "take_profit": {
        "profile": "take_profit_acceptance.yml",
        "levels": ["L0", "L1", "L4"],
        "required": ["tp1_price", "tp2_price", "tp1_hit", "tp2_hit", "partial_qty", "remaining_qty", "tp_exit_reason"],
        "optional": ["tp_mode", "tp_fill_price"],
        "anchor_pine": "05 Exit Skeleton take-profit block or isolated PineTS adapter",
        "anchor_python": "00_PYTHON/mtc_v2/core/exits.py",
    },
    "break_even": {
        "profile": "break_even_acceptance.yml",
        "levels": ["L0", "L3", "L4"],
        "required": ["be_trigger_price", "be_triggered", "be_activation_bar", "old_sl", "new_sl", "be_stop_owner"],
        "optional": ["be_buffer", "risk_r"],
        "anchor_pine": "Break-even stop owner block or isolated PineTS adapter",
        "anchor_python": "00_PYTHON/mtc_v2/core/exits.py",
    },
    "trailing_stop": {
        "profile": "trailing_stop_acceptance.yml",
        "levels": ["L0", "L3", "L4"],
        "required": ["trail_active", "trail_trigger_price", "trail_candidate", "active_trail_stop", "monotonic_merge_result", "trail_exit"],
        "optional": ["trail_distance", "trail_owner"],
        "anchor_pine": "Trailing stop owner block or isolated PineTS adapter",
        "anchor_python": "00_PYTHON/mtc_v2/core/exits.py",
    },
    "position_sizing": {
        "profile": "position_sizing_acceptance.yml",
        "levels": ["L0", "L3", "L4"],
        "required": ["equity_source", "account_equity", "risk_pct", "risk_amount", "sl_distance", "fallback_pct", "qty", "notional", "leverage", "max_leverage_cap", "blocked_reason"],
        "optional": ["qty_step", "min_notional"],
        "anchor_pine": "Position sizing block or isolated PineTS adapter",
        "anchor_python": "00_PYTHON/mtc_v2/core/position_sizer.py",
    },
    "portfolio_guard": {
        "profile": "portfolio_guard_acceptance.yml",
        "levels": ["L0", "L3", "L4"],
        "required": ["equity_curve_state", "daily_pnl", "drawdown_pct", "consecutive_losses", "guard_active", "guard_block_reason", "recovery_state"],
        "optional": ["guard_name", "recovery_counter"],
        "anchor_pine": "L16 Guards block or isolated PineTS adapter",
        "anchor_python": "00_PYTHON/mtc_v2/core/gates.py",
    },
    "visualization_only": {
        "profile": "visualization_acceptance.yml",
        "levels": ["L0", "L2", "L4"],
        "required": ["plotted_value", "marker_condition", "marker_type", "label_text", "performance_mode_gate"],
        "optional": ["plot_count", "label_count"],
        "anchor_pine": "Visualization block or isolated PineTS adapter",
        "anchor_python": "docs-only unless Python report rendering is needed",
    },
    "alert_payload": {
        "profile": "alert_payload_acceptance.yml",
        "levels": ["L0", "L3", "L4"],
        "required": ["event_id", "event_type", "side", "qty", "price", "reason", "once_per_bar_key", "payload_json", "schema_valid", "idempotency_key"],
        "optional": ["webhook_profile", "reduce_only"],
        "anchor_pine": "L25 alert/webhook block or isolated PineTS adapter",
        "anchor_python": "00_PYTHON/mtc_v2/core/alerts_<name>.py or docs-only",
    },
}


PROFILE_RULES = {
    "producer_acceptance.yml": [
        "L0 data must pass.",
        "L1 indicator trace must pass within numeric tolerance.",
        "L2 raw_long/raw_short must exact match.",
        "L3 transformed signal must exact match if producer feeds transform layer.",
        "No ready verdict if raw signal diverges without classification.",
    ],
    "transform_acceptance.yml": [
        "Raw input signals must match before transform.",
        "Transform state must match.",
        "pending_side, waiting, confirmation, and retest state must match.",
        "transformed_long/transformed_short must exact match.",
    ],
    "filter_gate_acceptance.yml": [
        "Input indicators must match.",
        "Allowed/blocked booleans must exact match.",
        "blocked_reason must exact match.",
        "First divergence table is required.",
    ],
    "exit_rule_acceptance.yml": [
        "Position state before exit must match.",
        "Exit condition and reason must match.",
        "Exit timestamp/bar must match.",
        "Exit-first ordering must be preserved.",
    ],
    "stop_loss_acceptance.yml": [
        "initial_sl must match within tick tolerance.",
        "active_sl must match every bar.",
        "Stop owner and update sequence must match.",
        "Stop hit bar and exit reason must match.",
    ],
    "take_profit_acceptance.yml": [
        "TP level prices must match.",
        "Partial close percent, partial qty, and remaining qty must match.",
        "TP fill event and TP exit reason must match.",
    ],
    "break_even_acceptance.yml": [
        "Trigger condition and activation bar must match.",
        "old_sl/new_sl must match.",
        "No backward stop movement is allowed.",
        "Stop owner transition must match.",
    ],
    "trailing_stop_acceptance.yml": [
        "Trail activation bar, candidate, and active stop sequence must match.",
        "Monotonic merge rule must match.",
        "Exit bar and reason must match.",
    ],
    "position_sizing_acceptance.yml": [
        "Equity source and risk amount must match.",
        "SL distance used for sizing must match.",
        "qty must match within size tolerance.",
        "Notional, leverage cap, and fallback sizing must match.",
    ],
    "portfolio_guard_acceptance.yml": [
        "Guard state must match.",
        "Daily PnL, drawdown, and consecutive loss state must match.",
        "Block/recovery decision and blocked reason must exact match.",
    ],
    "visualization_acceptance.yml": [
        "Visualization must not affect trading logic.",
        "Strategy signals/trades must be unchanged.",
        "Plot, label, and table counts must remain performance-safe.",
    ],
    "alert_payload_acceptance.yml": [
        "event_id recipe and once-per-bar/idempotency key must match.",
        "side, reason, qty, and price must match.",
        "JSON schema validation must pass.",
        "Alert payload must not drift from strategy event.",
    ],
}


def backup_if_exists(path: Path) -> None:
    if path.exists():
        backup = path.with_name(f"{path.name}.bak_{STAMP}")
        if not backup.exists():
            shutil.copy2(path, backup)


def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    backup_if_exists(target)
    target.write_text(content.strip() + "\n", encoding="utf-8")


def yaml_list(values: list[str], indent: int = 0) -> str:
    prefix = " " * indent
    return "\n".join(f"{prefix}- {value}" for value in values)


def make_contract_template(feature_type: str, meta: dict[str, object]) -> str:
    required = meta["required"]
    optional = meta["optional"]
    profile = meta["profile"]
    levels = meta["levels"]
    return f"""
feature_id: example_{feature_type}_v1
feature_name: example_{feature_type}
feature_type: {feature_type}
version: 0.1.0
status: draft
owner: codex
created_at: 2026-04-26
updated_at: 2026-04-26
description: Contract template for {feature_type} features.
intended_use: Replace this with the exact user-requested feature behavior.
implementation_targets:
  pine_files_touched: []
  python_files_touched: []
  pine_anchor_points:
    - "{meta['anchor_pine']}"
  python_anchor_points:
    - "{meta['anchor_python']}"
  integration_mode: isolated_adapter_only
input_parameters:
  - name: example_parameter
    type: float
    default: 1.0
    min: 0.0
    max: null
    options: []
    pine_input_title: Example Parameter
    python_config_field: example_parameter
state:
  state_variables: []
  persistent_state: []
  reset_conditions:
    - case start
    - invalid bar when feature requires reset
  warmup_policy:
    bars: contract_defined
    exclude_from_comparison: true
trace:
  required_trace_columns:
{yaml_list(required, 4)}
  optional_trace_columns:
{yaml_list(optional, 4)}
  expected_event_columns: []
  signal_columns:
    - raw_long
    - raw_short
  decision_columns: []
  execution_columns: []
parity:
  required_parity_levels:
{yaml_list(levels, 4)}
  tolerance_policy:
    numeric_abs_tol: 1.0e-8
    numeric_rel_tol: 1.0e-6
    tick_tolerance: 0
    booleans: exact
    strings: exact
  acceptance_profile: feature_contracts/acceptance_profiles/{profile}
  supported_oracles:
    python: true
    pinets: true
    pynecore: optional
    vectorbt: optional
    tradingview_export: final_release_audit
  baseline_oracle: python
  candidate_oracles:
    - pinets
safety:
  rollback_files: []
  rollback_notes:
    - Do not integrate into canonical MTC_V2.pine until feature-level parity passes.
  risk_notes: []
  known_limitations: []
  not_comparable_conditions:
    - required trace column unavailable
    - oracle unavailable
reporting:
  example_output_report_fields:
    - command
    - data_hash
    - config_hash
    - code_hash
    - first_divergence
    - missing_trace_columns
  required_report_sections:
    - Command run
    - Contract used
    - Case used
    - Oracle status
    - Acceptance profile
    - Verdict
  acceptance_verdicts:
    - FEATURE_TRACE_PASS
    - FEATURE_TRACE_FAIL
    - FEATURE_TRACE_NOT_COMPARABLE
    - ORACLE_UNAVAILABLE
  final_verdict_rule: Do not return ready code until this profile passes or the user explicitly accepts a classified mismatch.
integration_rule: Do not integrate into canonical MTC_V2.pine until feature-level parity passes.
"""


def make_acceptance_profile(filename: str, applicable: list[str]) -> str:
    rules = PROFILE_RULES[filename]
    return f"""
profile_id: {filename.removesuffix('.yml')}
applicable_feature_types:
{yaml_list(applicable, 2)}
required_levels:
  - contract.required_parity_levels
required_oracles:
  - python
  - pinets
optional_oracles:
  - pynecore
  - vectorbt
  - tradingview_export
numeric_tolerance:
  numeric_abs_tol: 1.0e-8
  numeric_rel_tol: 1.0e-6
  tick_tolerance: configurable
boolean_match_policy: exact
event_match_policy:
  timestamp: exact
  bar_index: exact
  reason_code: exact
warmup_policy:
  default_exclude_warmup: true
  source: contract.warmup_policy
pass_conditions:
{yaml_list(rules, 2)}
fail_conditions:
  - Required oracle output is unavailable.
  - Required trace columns are missing.
  - Numeric values exceed configured tolerance.
  - Boolean, event, reason, or payload values drift.
  - First divergence is unclassified.
report_requirements:
  - exact command
  - data hash
  - config hash
  - code hash
  - output file paths
  - first divergence table
  - missing trace columns
  - final acceptance verdict
"""


SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "MTC V2 Generic Feature Contract",
    "type": "object",
    "required": ["feature_id", "feature_name", "feature_type", "version", "status", "owner", "created_at", "updated_at", "description", "implementation_targets", "input_parameters", "state", "trace", "parity", "safety", "reporting"],
    "properties": {
        "feature_id": {"type": "string", "pattern": "^[a-z0-9_]+$"},
        "feature_name": {"type": "string"},
        "feature_type": {"type": "string", "enum": list(FEATURE_TYPES.keys())},
        "version": {"type": "string"},
        "status": {"type": "string", "enum": ["draft", "parity_testing", "accepted", "rejected", "deprecated"]},
        "owner": {"type": "string"},
        "created_at": {"type": "string"},
        "updated_at": {"type": "string"},
        "description": {"type": "string"},
        "implementation_targets": {
            "type": "object",
            "properties": {
                "pine_files_touched": {"type": "array", "items": {"type": "string"}},
                "python_files_touched": {"type": "array", "items": {"type": "string"}},
                "pine_anchor_points": {"type": "array", "items": {"type": "string"}},
                "python_anchor_points": {"type": "array", "items": {"type": "string"}},
                "integration_mode": {"type": "string", "enum": ["isolated_adapter_only", "draft_only", "selectable_feature", "production_integrated"]},
            },
        },
        "input_parameters": {"type": "array", "items": {"type": "object"}},
        "state": {"type": "object"},
        "trace": {"type": "object"},
        "parity": {"type": "object"},
        "safety": {"type": "object"},
        "reporting": {"type": "object"},
    },
    "additionalProperties": True,
}


def main() -> None:
    write("feature_contracts/schema/feature_contract.schema.json", json.dumps(SCHEMA, indent=2))
    write(
        "feature_contracts/README.md",
        """
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
""",
    )
    for feature_type, meta in FEATURE_TYPES.items():
        write(f"feature_contracts/templates/{feature_type}_contract.template.yml", make_contract_template(feature_type, meta))
    profile_to_types: dict[str, list[str]] = {}
    for feature_type, meta in FEATURE_TYPES.items():
        profile_to_types.setdefault(str(meta["profile"]), []).append(feature_type)
    for profile, applicable in profile_to_types.items():
        write(f"feature_contracts/acceptance_profiles/{profile}", make_acceptance_profile(profile, applicable))

    write("parity_oracles/feature_traces/trace_schema.py", TRACE_SCHEMA_PY)
    write("parity_oracles/feature_traces/trace_contract.py", TRACE_CONTRACT_PY)
    write("parity_oracles/feature_traces/trace_io.py", TRACE_IO_PY)
    write("parity_oracles/feature_traces/validate_trace_contract.py", VALIDATE_TRACE_CONTRACT_PY)
    write("parity_oracles/feature_traces/compare_feature_trace.py", COMPARE_FEATURE_TRACE_PY)
    write("parity_oracles/feature_traces/normalize_pinets_feature_trace.py", NORMALIZE_PINETS_FEATURE_TRACE_PY)
    write("parity_oracles/feature_traces/README.md", FEATURE_TRACE_README)
    write("parity_oracles/templates/pinets_feature_adapter_template.pine", PINETS_TEMPLATE)
    write("parity_oracles/templates/python_feature_trace_template.py", PYTHON_TRACE_TEMPLATE)
    write("tools/scaffold_new_feature.py", SCAFFOLDER_PY)
    write("parity_oracles/run_feature_parity.py", RUN_FEATURE_PARITY_PY)
    write("feature_contracts/active/producer_supertrend_current.yml", SUPERTREND_CONTRACT)
    write("docs/CODEX_GENERIC_FEATURE_CHANGE_WORKFLOW.md", CODEX_WORKFLOW_MD)
    write("docs/PYNECORE_MICRO_ORACLE_SETUP.md", PYNECORE_MD)
    write("docs/VECTORBT_SIGNAL_APPROXIMATION_ROLE.md", VECTORBT_MD)


TRACE_SCHEMA_PY = r'''
from __future__ import annotations

LONG_TRACE_COLUMNS = [
    "timestamp",
    "bar_index",
    "feature_id",
    "feature_type",
    "stage",
    "column_name",
    "value",
    "value_type",
    "source_oracle",
]

SUPPORTED_STAGES = {
    "data",
    "indicator",
    "signal",
    "transform",
    "gate",
    "decision",
    "execution",
    "sizing",
    "guard",
    "alert",
    "visualization",
}

VERDICTS = {
    "FEATURE_TRACE_PASS",
    "FEATURE_TRACE_PASS_WITH_TOLERANCE",
    "FEATURE_TRACE_FAIL_DATA",
    "FEATURE_TRACE_FAIL_INDICATOR",
    "FEATURE_TRACE_FAIL_SIGNAL",
    "FEATURE_TRACE_FAIL_TRANSFORM",
    "FEATURE_TRACE_FAIL_DECISION",
    "FEATURE_TRACE_FAIL_EXECUTION",
    "FEATURE_TRACE_FAIL_SIZING",
    "FEATURE_TRACE_FAIL_ALERT",
    "FEATURE_TRACE_NOT_COMPARABLE",
    "ORACLE_UNAVAILABLE",
}

DEFAULT_TOLERANCE = {
    "numeric_abs_tol": 1.0e-8,
    "numeric_rel_tol": 1.0e-6,
    "tick_tolerance": None,
}

STAGE_TO_FAIL_VERDICT = {
    "data": "FEATURE_TRACE_FAIL_DATA",
    "indicator": "FEATURE_TRACE_FAIL_INDICATOR",
    "signal": "FEATURE_TRACE_FAIL_SIGNAL",
    "transform": "FEATURE_TRACE_FAIL_TRANSFORM",
    "gate": "FEATURE_TRACE_FAIL_DECISION",
    "decision": "FEATURE_TRACE_FAIL_DECISION",
    "execution": "FEATURE_TRACE_FAIL_EXECUTION",
    "sizing": "FEATURE_TRACE_FAIL_SIZING",
    "guard": "FEATURE_TRACE_FAIL_DECISION",
    "alert": "FEATURE_TRACE_FAIL_ALERT",
    "visualization": "FEATURE_TRACE_FAIL_DECISION",
}
'''


TRACE_CONTRACT_PY = r'''
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_contract(path: str | Path) -> dict[str, Any]:
    text = Path(path).read_text(encoding="utf-8")
    if Path(path).suffix.lower() == ".json":
        return json.loads(text)
    return _load_simple_yaml(text)


def _load_simple_yaml(text: str) -> dict[str, Any]:
    try:
        import yaml  # type: ignore
    except Exception:
        yaml = None
    if yaml is not None:
        data = yaml.safe_load(text)
        return data or {}
    result: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, result)]
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if line.startswith("- "):
            value = _scalar(line[2:])
            if isinstance(parent, list):
                parent.append(value)
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            parsed: Any
            if value == "":
                parsed = {}
                parent[key] = parsed
                stack.append((indent, parsed))
            else:
                parent[key] = _scalar(value)
    return result


def _scalar(value: str) -> Any:
    if value in {"null", "None"}:
        return None
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value.startswith("[") or value.startswith("{"):
        try:
            return json.loads(value.replace("'", '"'))
        except Exception:
            return value
    try:
        if "." in value or "e" in value.lower():
            return float(value)
        return int(value)
    except ValueError:
        return value.strip('"')


def required_trace_columns(contract: dict[str, Any]) -> list[str]:
    trace = contract.get("trace", {})
    columns = trace.get("required_trace_columns", [])
    if isinstance(columns, list):
        values: list[str] = []
        for item in columns:
            if isinstance(item, dict):
                name = item.get("name") or item.get("column_name")
                if name:
                    values.append(str(name))
            else:
                values.append(str(item))
        return values
    return []
'''


TRACE_IO_PY = r'''
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from .trace_schema import LONG_TRACE_COLUMNS


def infer_value_type(value: Any) -> str:
    if value is None or value == "":
        return "null"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, (int, float)):
        return "number"
    text = str(value).strip()
    if text.lower() in {"true", "false"}:
        return "bool"
    try:
        float(text)
        return "number"
    except ValueError:
        return "string"


def write_long_trace(path: str | Path, rows: list[dict[str, Any]]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=LONG_TRACE_COLUMNS)
        writer.writeheader()
        for row in rows:
            output = {column: row.get(column, "") for column in LONG_TRACE_COLUMNS}
            if not output["value_type"]:
                output["value_type"] = infer_value_type(output["value"])
            writer.writerow(output)


def read_long_trace(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
'''


VALIDATE_TRACE_CONTRACT_PY = r'''
from __future__ import annotations

import argparse
from pathlib import Path

from .trace_contract import load_contract, required_trace_columns
from .trace_io import read_long_trace
from .trace_schema import LONG_TRACE_COLUMNS, SUPPORTED_STAGES


def validate_trace(contract_path: str, trace_path: str) -> dict[str, object]:
    contract = load_contract(contract_path)
    rows = read_long_trace(trace_path)
    missing_file_columns = [column for column in LONG_TRACE_COLUMNS if rows and column not in rows[0]]
    observed = {row.get("column_name", "") for row in rows}
    required = set(required_trace_columns(contract))
    missing_trace_columns = sorted(required - observed)
    invalid_stages = sorted({row.get("stage", "") for row in rows if row.get("stage", "") not in SUPPORTED_STAGES})
    verdict = "TRACE_CONTRACT_OK"
    if missing_file_columns or missing_trace_columns or invalid_stages:
        verdict = "TRACE_CONTRACT_INCOMPLETE"
    return {
        "verdict": verdict,
        "missing_file_columns": missing_file_columns,
        "missing_trace_columns": missing_trace_columns,
        "invalid_stages": invalid_stages,
        "row_count": len(rows),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", required=True)
    parser.add_argument("--trace", required=True)
    args = parser.parse_args()
    result = validate_trace(args.contract, args.trace)
    print(result)
    return 0 if result["verdict"] == "TRACE_CONTRACT_OK" else 2


if __name__ == "__main__":
    raise SystemExit(main())
'''


COMPARE_FEATURE_TRACE_PY = r'''
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

from .trace_io import read_long_trace, write_json
from .trace_schema import DEFAULT_TOLERANCE, STAGE_TO_FAIL_VERDICT


def _key(row: dict[str, str]) -> tuple[str, str, str, str]:
    return (row.get("timestamp", ""), row.get("bar_index", ""), row.get("stage", ""), row.get("column_name", ""))


def _as_bool(value: str) -> bool | None:
    lowered = str(value).strip().lower()
    if lowered in {"true", "1", "1.0"}:
        return True
    if lowered in {"false", "0", "0.0"}:
        return False
    return None


def _compare_values(a: str, b: str, value_type: str, abs_tol: float, rel_tol: float) -> tuple[bool, bool]:
    if value_type == "number":
        try:
            af = float(a)
            bf = float(b)
        except ValueError:
            return False, False
        if math.isnan(af) and math.isnan(bf):
            return True, False
        exact = af == bf
        return math.isclose(af, bf, abs_tol=abs_tol, rel_tol=rel_tol), not exact
    if value_type == "bool":
        return _as_bool(a) == _as_bool(b), False
    return str(a) == str(b), False


def compare_traces(
    baseline_path: str | Path,
    candidate_path: str | Path,
    *,
    warmup_bars: int = 0,
    numeric_abs_tol: float = DEFAULT_TOLERANCE["numeric_abs_tol"],
    numeric_rel_tol: float = DEFAULT_TOLERANCE["numeric_rel_tol"],
) -> dict[str, Any]:
    baseline = [row for row in read_long_trace(baseline_path) if int(row.get("bar_index") or 0) >= warmup_bars]
    candidate = [row for row in read_long_trace(candidate_path) if int(row.get("bar_index") or 0) >= warmup_bars]
    candidate_by_key = {_key(row): row for row in candidate}
    matched = 0
    tolerance_matches = 0
    missing = 0
    first_divergence = None
    window: list[dict[str, Any]] = []
    for row in baseline:
        key = _key(row)
        other = candidate_by_key.get(key)
        if other is None:
            missing += 1
            if first_divergence is None:
                first_divergence = {"reason": "missing_candidate_row", **{k: row.get(k, "") for k in ["timestamp", "bar_index", "feature_id", "stage", "column_name"]}}
            continue
        ok, within_tolerance = _compare_values(row.get("value", ""), other.get("value", ""), row.get("value_type", ""), numeric_abs_tol, numeric_rel_tol)
        if ok:
            matched += 1
            if within_tolerance:
                tolerance_matches += 1
            continue
        if first_divergence is None:
            first_divergence = {
                "reason": "value_mismatch",
                "timestamp": row.get("timestamp", ""),
                "bar_index": row.get("bar_index", ""),
                "feature_id": row.get("feature_id", ""),
                "stage": row.get("stage", ""),
                "column_name": row.get("column_name", ""),
                "baseline_value": row.get("value", ""),
                "candidate_value": other.get("value", ""),
            }
            center = int(row.get("bar_index") or 0)
            for b in baseline:
                try:
                    idx = int(b.get("bar_index") or 0)
                except ValueError:
                    continue
                if center - 3 <= idx <= center + 3 and b.get("column_name") == row.get("column_name"):
                    window.append({"baseline": b, "candidate": candidate_by_key.get(_key(b), {})})
    if first_divergence:
        stage = first_divergence.get("stage", "decision")
        verdict = STAGE_TO_FAIL_VERDICT.get(str(stage), "FEATURE_TRACE_NOT_COMPARABLE")
    elif tolerance_matches:
        verdict = "FEATURE_TRACE_PASS_WITH_TOLERANCE"
    else:
        verdict = "FEATURE_TRACE_PASS"
    return {
        "verdict": verdict,
        "matched": matched,
        "missing_candidate_rows": missing,
        "baseline_rows": len(baseline),
        "candidate_rows": len(candidate),
        "first_divergence": first_divergence,
        "window": window,
    }


def markdown_report(result: dict[str, Any]) -> str:
    first = result.get("first_divergence") or {}
    return "\n".join(
        [
            "# Feature Trace Comparison",
            "",
            f"- Verdict: `{result['verdict']}`",
            f"- Matched rows: {result['matched']}",
            f"- Baseline rows: {result['baseline_rows']}",
            f"- Candidate rows: {result['candidate_rows']}",
            f"- Missing candidate rows: {result['missing_candidate_rows']}",
            "",
            "## First Divergence",
            "",
            "None" if not first else json.dumps(first, indent=2),
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", required=True)
    parser.add_argument("--warmup-bars", type=int, default=0)
    args = parser.parse_args()
    result = compare_traces(args.baseline, args.candidate, warmup_bars=args.warmup_bars)
    write_json(args.out_json, result)
    Path(args.out_md).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_md).write_text(markdown_report(result), encoding="utf-8")
    return 0 if result["verdict"].startswith("FEATURE_TRACE_PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''


NORMALIZE_PINETS_FEATURE_TRACE_PY = r'''
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .trace_io import infer_value_type, write_long_trace


PREFIX = "FEATURE__"


def normalize_pinets_json(input_path: str | Path, output_path: str | Path, feature_type: str = "signal_producer") -> dict[str, Any]:
    payload = json.loads(Path(input_path).read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = []
    records = payload if isinstance(payload, list) else payload.get("data", payload.get("plots", []))
    for bar_index, record in enumerate(records):
        if not isinstance(record, dict):
            continue
        timestamp = record.get("timestamp") or record.get("time") or bar_index
        for key, value in record.items():
            if not str(key).startswith(PREFIX):
                continue
            parts = str(key).split("__")
            if len(parts) < 4:
                continue
            _, feature_id, stage, column_name = parts[:4]
            rows.append(
                {
                    "timestamp": timestamp,
                    "bar_index": record.get("bar_index", bar_index),
                    "feature_id": feature_id,
                    "feature_type": feature_type,
                    "stage": stage,
                    "column_name": column_name,
                    "value": value,
                    "value_type": infer_value_type(value),
                    "source_oracle": "pinets",
                }
            )
    write_long_trace(output_path, rows)
    return {"rows": len(rows), "output": str(output_path)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--feature-type", default="signal_producer")
    args = parser.parse_args()
    print(normalize_pinets_json(args.input, args.output, args.feature_type))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


FEATURE_TRACE_README = r'''
# Feature Trace Standard

The canonical format is long CSV:

`timestamp,bar_index,feature_id,feature_type,stage,column_name,value,value_type,source_oracle`

Supported stages are `data`, `indicator`, `signal`, `transform`, `gate`, `decision`, `execution`, `sizing`, `guard`, `alert`, and `visualization`.

Wide traces are allowed for adapters, but must be normalized before comparison:

`timestamp,bar_index,feature_id,<feature-specific columns...>`

Default tolerance is `numeric_abs_tol=1e-8`, `numeric_rel_tol=1e-6`, with configurable tick tolerance for price-like columns. Booleans and reason codes are exact match.
'''


PINETS_TEMPLATE = r'''
//@version=6
indicator("MTC V2 Feature Adapter Template", overlay=false, max_labels_count=500)

// This adapter is for local PineTS feature trace only.
// Do not use strategy.entry/strategy.exit here.
// Plot names must be stable: FEATURE__<feature_id>__<stage>__<column_name>

feature_id = input.string("producer_example_v1", "Feature ID")

// Signal producer example
producer_source = close
producer_direction = close >= close[1] ? 1.0 : -1.0
producer_raw_long = ta.crossover(close, ta.sma(close, 10))
producer_raw_short = ta.crossunder(close, ta.sma(close, 10))
plot(producer_source, title="FEATURE__producer_supertrend_current__indicator__source_price", display=display.none)
plot(producer_direction, title="FEATURE__producer_supertrend_current__indicator__direction", display=display.none)
plot(producer_raw_long ? 1 : 0, title="FEATURE__producer_supertrend_current__signal__raw_long", display=display.none)
plot(producer_raw_short ? 1 : 0, title="FEATURE__producer_supertrend_current__signal__raw_short", display=display.none)

// Entry filter example
filter_allowed_long = close > ta.sma(close, 20)
filter_allowed_short = close < ta.sma(close, 20)
plot(filter_allowed_long ? 1 : 0, title="FEATURE__filter_adx_v2__gate__allowed_long", display=display.none)
plot(filter_allowed_short ? 1 : 0, title="FEATURE__filter_adx_v2__gate__allowed_short", display=display.none)

// Stop loss example
active_sl = close - ta.atr(14) * 2.0
plot(active_sl, title="FEATURE__sl_swing_atr_v1__execution__active_sl", display=display.none)
plot(low <= active_sl ? 1 : 0, title="FEATURE__sl_swing_atr_v1__execution__sl_hit", display=display.none)

// Take profit example
tp1_price = close + ta.atr(14) * 3.0
plot(tp1_price, title="FEATURE__tp_multi_r_v1__execution__tp1_price", display=display.none)
plot(high >= tp1_price ? 1 : 0, title="FEATURE__tp_multi_r_v1__execution__tp1_hit", display=display.none)

// Position sizing example
risk_amount = 100.0
qty = risk_amount / math.max(ta.atr(14) * 2.0, syminfo.mintick)
plot(qty, title="FEATURE__sizing_risk_pct_v2__sizing__qty", display=display.none)
plot(qty * close, title="FEATURE__sizing_risk_pct_v2__sizing__notional", display=display.none)

// Alert payload trace example. Numeric code mirrors payload schema validity.
event_id_code = producer_raw_long ? 1.0 : producer_raw_short ? -1.0 : 0.0
plot(event_id_code, title="FEATURE__alert_wunder_v2__alert__event_id", display=display.none)
plot(1, title="FEATURE__alert_wunder_v2__alert__schema_valid", display=display.none)
'''


PYTHON_TRACE_TEMPLATE = r'''
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from parity_oracles.feature_traces.trace_contract import load_contract
from parity_oracles.feature_traces.trace_io import infer_value_type, write_long_trace


def load_case(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_candles(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def emit(rows: list[dict[str, Any]], *, candle: dict[str, Any], bar_index: int, contract: dict[str, Any], stage: str, column: str, value: Any) -> None:
    rows.append(
        {
            "timestamp": candle.get("timestamp") or candle.get("time") or bar_index,
            "bar_index": bar_index,
            "feature_id": contract["feature_id"],
            "feature_type": contract["feature_type"],
            "stage": stage,
            "column_name": column,
            "value": value,
            "value_type": infer_value_type(value),
            "source_oracle": "python",
        }
    )


def build_trace(case_path: str, contract_path: str, output_path: str) -> None:
    case = load_case(case_path)
    contract = load_contract(contract_path)
    candles = load_candles(case["data_file"])
    rows: list[dict[str, Any]] = []
    for bar_index, candle in enumerate(candles):
        close = float(candle.get("close") or candle.get("Close") or 0.0)
        emit(rows, candle=candle, bar_index=bar_index, contract=contract, stage="indicator", column="example_indicator", value=close)
        emit(rows, candle=candle, bar_index=bar_index, contract=contract, stage="signal", column="raw_long", value=False)
        emit(rows, candle=candle, bar_index=bar_index, contract=contract, stage="gate", column="allowed_long", value=True)
        emit(rows, candle=candle, bar_index=bar_index, contract=contract, stage="execution", column="exit_reason", value="")
        emit(rows, candle=candle, bar_index=bar_index, contract=contract, stage="sizing", column="qty", value=0.0)
        emit(rows, candle=candle, bar_index=bar_index, contract=contract, stage="alert", column="payload_json", value="{}")
    write_long_trace(output_path, rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", required=True)
    parser.add_argument("--contract", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    build_trace(args.case, args.contract, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


SCAFFOLDER_PY = r'''
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FEATURE_TYPES = {
    "signal_producer",
    "signal_transform",
    "entry_filter",
    "exit_rule",
    "stop_loss",
    "take_profit",
    "break_even",
    "trailing_stop",
    "position_sizing",
    "portfolio_guard",
    "visualization_only",
    "alert_payload",
}
STAMP = "feature_scaffold_backup"


def backup(path: Path) -> None:
    if path.exists():
        backup_path = path.with_name(f"{path.name}.bak_{STAMP}")
        if not backup_path.exists():
            shutil.copy2(path, backup_path)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    backup(path)
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite existing scaffold file: {path}")
    path.write_text(content.strip() + "\n", encoding="utf-8")


def python_stub_target(feature_type: str, name: str) -> Path | None:
    if feature_type == "signal_producer":
        return ROOT / "00_PYTHON" / "mtc_v2" / "signals" / f"{name}.py"
    if feature_type == "entry_filter":
        folder = ROOT / "00_PYTHON" / "mtc_v2" / "core" / "filters"
        return folder / f"{name}.py" if folder.exists() else None
    if feature_type in {"exit_rule", "stop_loss", "take_profit", "break_even", "trailing_stop"}:
        return ROOT / "00_PYTHON" / "mtc_v2" / "core" / f"exits_{name}.py"
    if feature_type == "position_sizing":
        return ROOT / "00_PYTHON" / "mtc_v2" / "core" / f"position_sizer_{name}.py"
    if feature_type == "portfolio_guard":
        return ROOT / "00_PYTHON" / "mtc_v2" / "core" / f"guards_{name}.py"
    if feature_type == "alert_payload":
        return ROOT / "00_PYTHON" / "mtc_v2" / "core" / f"alerts_{name}.py"
    return None


def scaffold(feature_type: str, feature_id: str, name: str) -> list[Path]:
    if feature_type not in FEATURE_TYPES:
        raise ValueError(f"Unsupported feature type: {feature_type}")
    created: list[Path] = []
    contract = ROOT / "feature_contracts" / "drafts" / f"{feature_id}.yml"
    adapter = ROOT / "parity_oracles" / "feature_adapters" / "pinets" / f"{feature_id}.pine"
    trace = ROOT / "parity_oracles" / "feature_traces" / "python" / f"{feature_id}_trace.py"
    notes = ROOT / "docs" / "feature_notes" / f"{feature_id}.md"
    write(contract, f"feature_id: {feature_id}\nfeature_name: {name}\nfeature_type: {feature_type}\nstatus: draft\nintegration_rule: Do not integrate into canonical MTC_V2.pine until feature-level parity passes.")
    write(adapter, f"//@version=6\nindicator(\"{feature_id} feature adapter\", overlay=false)\nplot(na, title=\"FEATURE__{feature_id}__data__placeholder\", display=display.none)")
    write(trace, f"from parity_oracles.templates.python_feature_trace_template import main\n\nif __name__ == \"__main__\":\n    raise SystemExit(main())")
    write(notes, f"# {feature_id}\n\n- Feature type: `{feature_type}`\n- Integration rule: Do not integrate into canonical MTC_V2.pine until feature-level parity passes.\n")
    created.extend([contract, adapter, trace, notes])
    target = python_stub_target(feature_type, name)
    if target is None:
        notes.write_text(notes.read_text(encoding="utf-8") + "\nPython implementation target is architecture-dependent; use docs-only stub until owner boundary is confirmed.\n", encoding="utf-8")
    else:
        write(target, f"from __future__ import annotations\n\n\ndef evaluate_{name}(*args, **kwargs):\n    raise NotImplementedError(\"Implement only after contract trace columns are finalized.\")")
        created.append(target)
    test_target = ROOT / "00_PYTHON" / "mtc_v2" / "tests" / f"test_{name}.py"
    write(test_target, f"def test_{name}_contract_placeholder():\n    assert True")
    created.append(test_target)
    return created


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--feature-type", required=True, choices=sorted(FEATURE_TYPES))
    parser.add_argument("--feature-id", required=True)
    parser.add_argument("--name", required=True)
    args = parser.parse_args()
    created = scaffold(args.feature_type, args.feature_id, args.name)
    for path in created:
        print(path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


RUN_FEATURE_PARITY_PY = r'''
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from parity_oracles.feature_traces.compare_feature_trace import compare_traces
from parity_oracles.feature_traces.trace_contract import load_contract, required_trace_columns
from parity_oracles.feature_traces.trace_io import infer_value_type, write_json, write_long_trace


def sha256_file(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return "UNAVAILABLE"
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_code_hash() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return "UNAVAILABLE"


def case_id_from_path(path: Path) -> str:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return str(payload.get("case_id") or path.stem)
    except Exception:
        return path.stem


def load_case(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def supertrend_python_trace(contract: dict[str, Any], case: dict[str, Any], out_path: Path) -> dict[str, Any]:
    sys.path.insert(0, str(ROOT / "00_PYTHON"))
    from mtc_v2.core.types import Bar
    from mtc_v2.signals.supertrend import SupertrendSignal

    data_file = ROOT / case["data_file"]
    config_path = ROOT / "05_PARITY" / "TW_EXPORT_CASES_V2" / "case_001" / "case_plan.json"
    config: dict[str, Any] = {}
    if config_path.exists():
        plan = json.loads(config_path.read_text(encoding="utf-8"))
        config.update(plan.get("overrides", {}))
    signal = SupertrendSignal(config)
    rows: list[dict[str, Any]] = []
    with data_file.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for bar_index, row in enumerate(reader):
            bar = Bar(
                timestamp=row.get("timestamp") or row.get("time") or str(bar_index),
                open=float(row.get("open") or row.get("Open")),
                high=float(row.get("high") or row.get("High")),
                low=float(row.get("low") or row.get("Low")),
                close=float(row.get("close") or row.get("Close")),
                volume=float(row.get("volume") or row.get("Volume") or 0.0),
            )
            raw = signal.calculate(bar)
            snapshot = signal.indicator_snapshot().supertrend
            values = {
                "source_price": bar.close,
                "atr": snapshot.atr,
                "upper_band": snapshot.upper_band,
                "lower_band": snapshot.lower_band,
                "supertrend_line": snapshot.line,
                "direction": snapshot.direction,
                "raw_long": raw.long,
                "raw_short": raw.short,
                "conflict_reason": raw.reason,
                "warmup_ready": snapshot.warmup_ready,
                "valid_bar": snapshot.valid_bar,
            }
            for column, value in values.items():
                stage = "indicator" if column not in {"raw_long", "raw_short", "conflict_reason"} else "signal"
                rows.append(
                    {
                        "timestamp": bar.timestamp,
                        "bar_index": bar_index,
                        "feature_id": contract["feature_id"],
                        "feature_type": contract["feature_type"],
                        "stage": stage,
                        "column_name": column,
                        "value": "" if value is None else value,
                        "value_type": infer_value_type(value),
                        "source_oracle": "python",
                    }
                )
    write_long_trace(out_path, rows)
    return {"status": "OK", "output": str(out_path), "rows": len(rows)}


def pinets_existing_supertrend_trace(contract: dict[str, Any], out_path: Path) -> dict[str, Any]:
    source = ROOT / "reports" / "parity" / "case_001" / "supertrend_isolation" / "pinets_supertrend.csv"
    if not source.exists():
        return {"status": "PINETS_UNAVAILABLE", "reason": f"missing {source}"}
    rows: list[dict[str, Any]] = []
    with source.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for bar_index, row in enumerate(reader):
            timestamp = row.get("timestamp") or row.get("time") or str(bar_index)
            mapping = {
                "supertrend_line": row.get("supertrend_line", ""),
                "direction": row.get("direction", ""),
                "raw_long": row.get("long_raw", row.get("raw_long", "")),
                "raw_short": row.get("short_raw", row.get("raw_short", "")),
            }
            for column, value in mapping.items():
                rows.append(
                    {
                        "timestamp": timestamp,
                        "bar_index": row.get("bar_index") or bar_index,
                        "feature_id": contract["feature_id"],
                        "feature_type": contract["feature_type"],
                        "stage": "signal" if column.startswith("raw_") else "indicator",
                        "column_name": column,
                        "value": value,
                        "value_type": infer_value_type(value),
                        "source_oracle": "pinets",
                    }
                )
    write_long_trace(out_path, rows)
    return {"status": "OK", "output": str(out_path), "rows": len(rows), "source": str(source)}


def validate_required_columns(contract: dict[str, Any], trace_path: Path) -> list[str]:
    if not trace_path.exists():
        return required_trace_columns(contract)
    with trace_path.open("r", newline="", encoding="utf-8") as handle:
        observed = {row.get("column_name", "") for row in csv.DictReader(handle)}
    missing = []
    for column in required_trace_columns(contract):
        if column not in observed:
            missing.append(column)
    return missing


def markdown_report(payload: dict[str, Any]) -> str:
    first = payload.get("comparison", {}).get("first_divergence")
    lines = [
        "# Feature Parity Report",
        "",
        f"- Command: `{payload['command']}`",
        f"- Data hash: `{payload['data_hash']}`",
        f"- Config hash: `{payload['config_hash']}`",
        f"- Code hash: `{payload['code_hash']}`",
        f"- Contract: `{payload['contract_path']}`",
        f"- Case: `{payload['case_path']}`",
        f"- Feature: `{payload['feature_id']}`",
        f"- Acceptance profile: `{payload['acceptance_profile']}`",
        f"- Verdict: `{payload['verdict']}`",
        "",
        "## Oracle Status",
        "",
        f"- Python trace: `{payload['python_trace_status'].get('status')}`",
        f"- PineTS trace: `{payload['pinets_trace_status'].get('status')}`",
        "",
        "## Output Files",
        "",
    ]
    for item in payload["output_files"]:
        lines.append(f"- `{item}`")
    lines.extend(["", "## Missing Trace Columns", ""])
    missing = payload.get("missing_trace_columns") or []
    lines.append("None" if not missing else "\n".join(f"- `{column}`" for column in missing))
    lines.extend(["", "## First Divergence", "", "None" if not first else json.dumps(first, indent=2)])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", required=True)
    parser.add_argument("--case", required=True)
    parser.add_argument("--oracles", nargs="+", default=["python", "pinets"])
    parser.add_argument("--levels", nargs="+", default=["L0", "L1", "L2"])
    args = parser.parse_args()

    contract_path = ROOT / args.contract
    case_path = ROOT / args.case
    contract = load_contract(contract_path)
    case = load_case(case_path)
    case_id = case_id_from_path(case_path)
    feature_id = contract["feature_id"]
    out_dir = ROOT / "reports" / "parity" / case_id / "features" / feature_id
    out_dir.mkdir(parents=True, exist_ok=True)
    python_trace = out_dir / "python_feature_trace.csv"
    pinets_trace = out_dir / "pinets_feature_trace.csv"
    python_status = {"status": "SKIPPED"}
    pinets_status = {"status": "SKIPPED"}

    if "python" in args.oracles:
        if feature_id == "producer_supertrend_current":
            try:
                python_status = supertrend_python_trace(contract, case, python_trace)
            except Exception as exc:
                python_status = {"status": "PYTHON_TRACE_UNAVAILABLE", "reason": str(exc)}
        else:
            python_status = {"status": "PYTHON_TRACE_UNAVAILABLE", "reason": "no feature trace exporter registered"}
    if "pinets" in args.oracles:
        if feature_id == "producer_supertrend_current":
            pinets_status = pinets_existing_supertrend_trace(contract, pinets_trace)
        else:
            pinets_status = {"status": "PINETS_UNAVAILABLE", "reason": "no PineTS feature adapter runner registered"}

    missing = []
    if python_status.get("status") == "OK":
        missing.extend(f"python:{column}" for column in validate_required_columns(contract, python_trace))
    if pinets_status.get("status") == "OK":
        missing.extend(f"pinets:{column}" for column in validate_required_columns(contract, pinets_trace))

    comparison: dict[str, Any] = {}
    if python_status.get("status") != "OK":
        verdict = "PYTHON_TRACE_UNAVAILABLE"
    elif pinets_status.get("status") != "OK":
        verdict = "PINETS_UNAVAILABLE"
    elif missing:
        verdict = "TRACE_CONTRACT_INCOMPLETE"
    else:
        comparison = compare_traces(python_trace, pinets_trace, warmup_bars=int(contract.get("state", {}).get("warmup_policy", {}).get("bars", 0) or 0))
        verdict = comparison["verdict"]

    payload = {
        "command": " ".join(sys.argv),
        "contract_path": str(contract_path),
        "case_path": str(case_path),
        "feature_id": feature_id,
        "feature_type": contract.get("feature_type"),
        "levels": args.levels,
        "oracles": args.oracles,
        "acceptance_profile": contract.get("parity", {}).get("acceptance_profile"),
        "data_hash": sha256_file(ROOT / case.get("data_file", "")),
        "config_hash": sha256_file(ROOT / "05_PARITY" / "TW_EXPORT_CASES_V2" / case_id / "case_plan.json"),
        "code_hash": git_code_hash(),
        "python_trace_status": python_status,
        "pinets_trace_status": pinets_status,
        "missing_trace_columns": missing,
        "comparison": comparison,
        "verdict": verdict,
        "output_files": [str(python_trace), str(pinets_trace), str(out_dir / "FEATURE_PARITY_REPORT.md"), str(out_dir / "FEATURE_PARITY_REPORT.json")],
    }
    write_json(out_dir / "FEATURE_PARITY_REPORT.json", payload)
    (out_dir / "FEATURE_PARITY_REPORT.md").write_text(markdown_report(payload), encoding="utf-8")
    print(json.dumps({"verdict": verdict, "report": str(out_dir / "FEATURE_PARITY_REPORT.md")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


SUPERTREND_CONTRACT = r'''
feature_id: producer_supertrend_current
feature_name: Current Supertrend Producer
feature_type: signal_producer
version: 1.0.0
status: parity_testing
owner: codex
created_at: 2026-04-26
updated_at: 2026-04-26
description: Describes the currently active Supertrend raw buy/sell signal producer in MTC V2.
implementation_targets:
  pine_files_touched:
    - 01_PINE/MTC_V2.pine
  python_files_touched:
    - 00_PYTHON/mtc_v2/signals/supertrend.py
    - 00_PYTHON/mtc_v2/core/config.py
  pine_anchor_points:
    - "02 Signal Producer inputs: Signal Mode, ATR Len, Factor"
    - "Supertrend calculation block around st_atr/st_factor"
    - "plot titles: supertrend_line and raw signal plots when available"
  python_anchor_points:
    - "mtc_v2.signals.supertrend.SupertrendSignal"
    - "DEFAULT_CONFIG st_atr_len/st_factor/st_use_wicks/st_use_ha"
  integration_mode: production_integrated
input_parameters:
  - name: signal_mode
    type: string
    default: Supertrend
    min: null
    max: null
    options: [Supertrend]
    pine_input_title: Signal Mode
    python_config_field: signal_mode
  - name: st_atr_len
    type: int
    default: 21
    min: 1
    max: null
    options: []
    pine_input_title: ATR Len
    python_config_field: st_atr_len
  - name: st_factor
    type: float
    default: 4.0
    min: 0.1
    max: null
    options: []
    pine_input_title: Factor
    python_config_field: st_factor
  - name: st_use_wicks
    type: bool
    default: false
    min: null
    max: null
    options: []
    pine_input_title: not visible in current Pine input surface
    python_config_field: st_use_wicks
  - name: st_use_ha
    type: bool
    default: false
    min: null
    max: null
    options: []
    pine_input_title: not visible in current Pine input surface
    python_config_field: st_use_ha
state:
  state_variables:
    - atr
    - upper_band
    - lower_band
    - direction
    - previous_close
  persistent_state:
    - previous ATR
    - previous upper/lower bands
    - previous direction
  reset_conditions:
    - case start
    - st_use_ha unsupported branch in Python
  warmup_policy:
    bars: 21
    exclude_from_comparison: true
trace:
  trace_columns:
    - {name: source_price, available: true}
    - {name: atr, available: true}
    - {name: upper_band, available: true}
    - {name: lower_band, available: true}
    - {name: supertrend_line, available: true}
    - {name: direction, available: true}
    - {name: raw_long, available: true}
    - {name: raw_short, available: true}
    - {name: conflict_reason, available: true}
    - {name: internal_event_id, available: false, reason: "not exposed by current implementation"}
  required_trace_columns:
    - supertrend_line
    - direction
    - raw_long
    - raw_short
  optional_trace_columns:
    - source_price
    - atr
    - upper_band
    - lower_band
    - conflict_reason
    - warmup_ready
    - valid_bar
  expected_event_columns:
    - conflict_reason
  signal_columns:
    - raw_long
    - raw_short
  decision_columns: []
  execution_columns: []
parity:
  required_parity_levels:
    - L0
    - L1
    - L2
  tolerance_policy:
    numeric_abs_tol: 1.0e-8
    numeric_rel_tol: 1.0e-6
    tick_tolerance: 0
    booleans: exact
    strings: exact
  acceptance_profile: feature_contracts/acceptance_profiles/producer_acceptance.yml
  supported_oracles:
    python: true
    pinets: true
    pynecore: optional
    vectorbt: optional
    tradingview_export: final_release_audit
  baseline_oracle: python
  candidate_oracles:
    - pinets
safety:
  rollback_files:
    - 01_PINE/MTC_V2.pine
    - 00_PYTHON/mtc_v2/signals/supertrend.py
    - 00_PYTHON/mtc_v2/core/config.py
  risk_notes:
    - Full engine L1/L2 can diverge from isolated Supertrend because downstream config/export surface can differ.
  known_limitations:
    - st_use_ha is scaffold-only and not supported by Python producer.
    - Current Pine UI exposes only Signal Mode, ATR Len, and Factor for this producer.
  not_comparable_conditions:
    - PineTS adapter output unavailable
    - Python trace exporter unavailable
    - required trace columns missing
reporting:
  required_report_sections:
    - Command run
    - Contract used
    - Case used
    - Python trace status
    - PineTS trace status
    - Acceptance profile used
    - Pass/fail/not comparable
    - First divergence if available
    - Missing trace columns if any
  acceptance_verdicts:
    - FEATURE_TRACE_PASS
    - FEATURE_TRACE_PASS_WITH_TOLERANCE
    - FEATURE_TRACE_FAIL_INDICATOR
    - FEATURE_TRACE_FAIL_SIGNAL
    - FEATURE_TRACE_NOT_COMPARABLE
    - ORACLE_UNAVAILABLE
  final_verdict_rule: Do not replace or remove Supertrend until the candidate producer passes producer_acceptance.yml.
'''


CODEX_WORKFLOW_MD = r'''
# Codex Generic Feature Change Workflow

Common rule: no feature is ready until its contract-specific acceptance profile passes or the mismatch is explicitly classified and accepted by the user.

## Required Flow

1. Scaffold the feature contract and isolated adapters.
2. Implement the feature in Python and Pine draft/adapter form.
3. Emit Python feature trace.
4. Emit PineTS feature trace.
5. Compare traces with the contract acceptance profile.
6. Integrate into canonical `01_PINE/MTC_V2.pine` and production Python only after feature-level parity passes.
7. Run selected local FAST_SUITE parity checks.
8. Use TradingView export only as final release audit.

## Examples

### Replace Supertrend with Range Filter

Use `feature_type: signal_producer`.

Required workflow: scaffold feature, create contract, implement isolated PineTS adapter, implement Python feature, emit traces, run L0/L1/L2/L3, integrate only after pass.

### Add ATR-based stop loss

Use `feature_type: stop_loss`.

Required workflow: contract, Python SL implementation, Pine SL implementation draft/adapter, trace `initial_sl`, `active_sl`, `sl_hit`, `exit_reason`, run stop_loss acceptance, integrate only after pass.

### Add multi-R partial TP

Use `feature_type: take_profit`.

Required workflow: trace TP prices, partial qty, remaining qty, TP fill event, then run take_profit acceptance.

### Add ADX filter

Use `feature_type: entry_filter`.

Required workflow: trace ADX value, allowed/blocked booleans, blocked_reason, then run filter_gate acceptance.

### Change risk sizing

Use `feature_type: position_sizing`.

Required workflow: trace equity source, risk amount, qty, notional, leverage, then run position_sizing acceptance.

### Change WunderTrading alert JSON

Use `feature_type: alert_payload`.

Required workflow: trace event_id, payload JSON, schema validation, idempotency key, then run alert_payload acceptance.

## Codex Must Never

- Modify canonical `01_PINE/MTC_V2.pine` before feature parity passes.
- Change production Python behavior before the isolated contract is accepted.
- Hide mismatch by increasing tolerance.
- Fake oracle output.
- Use TradingView export as the normal development loop.
- Place live orders or use API keys.

## Reports

Every feature parity result must produce `FEATURE_PARITY_REPORT.md` and `FEATURE_PARITY_REPORT.json` with exact command, data hash, config hash, code hash, output paths, first divergence, missing columns, and verdict.

## NOT_COMPARABLE Handling

Return a structured `FEATURE_TRACE_NOT_COMPARABLE`, `PYTHON_TRACE_UNAVAILABLE`, `PINETS_UNAVAILABLE`, or `TRACE_CONTRACT_INCOMPLETE` report. Continue without claiming ready.

## When TradingView Export Is Needed

TradingView export is still required for final release audit after local contract-level and selected FAST_SUITE parity checks pass.
'''


PYNECORE_MD = r'''
# PyneCore Micro-Oracle Setup

PyneCore is optional for Generic Feature Factory v1.

- Use an isolated Python 3.11 or 3.12 virtual environment.
- Do not use the paid PyneComp compiler.
- Start with small manually translated feature modules only.
- Do not treat PyneCore as a full MTC replacement.
- PyneCore is not required for Generic Feature Factory v1 PASS.

Suggested future use:

- Producer micro-oracle.
- Simple stop/TP micro-oracle.
- `request.security` / MTF micro-test only after the environment works.
'''


VECTORBT_MD = r'''
# vectorbt Signal Approximation Role

vectorbt is not exact Pine/MTC execution parity.

- It is a fast signal-array sanity checker.
- It can consume normalized signals from Python and PineTS.
- It is useful for parameter sweeps and rough behavioral checks.
- It must not be used as final L5/L6 authority.
- The Python MTC engine remains the main execution oracle.
'''


if __name__ == "__main__":
    main()
