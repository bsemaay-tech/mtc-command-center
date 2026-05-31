from __future__ import annotations

import argparse
import csv
import hashlib
import importlib
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


def _export_with_registered_module(
    oracle: str,
    feature_id: str,
    contract: dict[str, Any],
    case: dict[str, Any],
    out_path: Path,
) -> dict[str, Any]:
    module_name = f"parity_oracles.feature_traces.{oracle}.{feature_id}_trace"
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        return {"status": f"{oracle.upper()}_TRACE_UNAVAILABLE", "reason": f"no registered exporter: {module_name}"}
    try:
        return module.export_trace(contract, case, out_path)
    except Exception as exc:
        return {"status": f"{oracle.upper()}_TRACE_UNAVAILABLE", "reason": str(exc)}


def _trace_policy(contract: dict[str, Any], key: str) -> str:
    return str(contract.get("trace", {}).get(key, ""))


def _policy_mismatch(contract: dict[str, Any], python_status: dict[str, Any], pinets_status: dict[str, Any]) -> list[str]:
    mismatches: list[str] = []
    for key in ["timestamp_policy", "bar_index_policy", "trace_source_mode", "config_source", "candle_source"]:
        expected = _trace_policy(contract, key)
        left = str(python_status.get(key, ""))
        right = str(pinets_status.get(key, ""))
        if expected and (left != expected or right != expected):
            mismatches.append(f"{key}: expected={expected} python={left} pinets={right}")
        elif left != right:
            mismatches.append(f"{key}: python={left} pinets={right}")
    return mismatches


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
                bar_index=bar_index,
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
        python_status = _export_with_registered_module("python", feature_id, contract, case, python_trace)
    if "pinets" in args.oracles:
        pinets_status = _export_with_registered_module("pinets", feature_id, contract, case, pinets_trace)

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
    else:
        policy_mismatches = _policy_mismatch(contract, python_status, pinets_status)
        if policy_mismatches:
            verdict = "TRACE_POLICY_MISMATCH"
        elif missing:
            verdict = "TRACE_CONTRACT_INCOMPLETE"
        else:
            comparison = compare_traces(
                python_trace,
                pinets_trace,
                warmup_bars=int(contract.get("trace", {}).get("warmup_bars", contract.get("state", {}).get("warmup_policy", {}).get("bars", 0)) or 0),
                include_columns=set(required_trace_columns(contract)),
            )
            verdict = comparison["verdict"]

    payload = {
        "command": "python " + " ".join(sys.argv),
        "contract_path": str(contract_path),
        "case_path": str(case_path),
        "feature_id": feature_id,
        "feature_type": contract.get("feature_type"),
        "levels": args.levels,
        "oracles": args.oracles,
        "acceptance_profile": contract.get("parity", {}).get("acceptance_profile"),
        "trace_source_mode": contract.get("trace", {}).get("trace_source_mode"),
        "config_source": contract.get("trace", {}).get("config_source"),
        "timestamp_policy": contract.get("trace", {}).get("timestamp_policy"),
        "bar_index_policy": contract.get("trace", {}).get("bar_index_policy"),
        "data_hash": sha256_file(ROOT / case.get("data_file", "")),
        "config_hash": sha256_file(ROOT / "05_PARITY" / "TW_EXPORT_CASES_V2" / case_id / "case_plan.json"),
        "code_hash": git_code_hash(),
        "python_trace_status": python_status,
        "pinets_trace_status": pinets_status,
        "missing_trace_columns": missing,
        "policy_mismatches": locals().get("policy_mismatches", []),
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
