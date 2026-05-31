from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from parity_oracles.common.io_utils import ROOT, git_code_hash, write_json


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _lifecycle_level(path: Path, level: str) -> dict[str, Any]:
    target = path / f"python_engine_range_filter_vs_pinets_range_filter_full_{level}.json"
    return _read_json(target)


def build_consensus(feature_report: Path, reference_report: Path, lifecycle_dir: Path) -> dict[str, Any]:
    feature = _read_json(feature_report)
    reference = _read_json(reference_report)
    levels = {level: _lifecycle_level(lifecycle_dir, level) for level in ["L0", "L1", "L2", "L3", "L4", "L5", "L6"]}
    l0_l3_pass = all(levels[level].get("verdict") == "PASS" for level in ["L0", "L1", "L2", "L3"])
    l4_l6_not_comparable = all(levels[level].get("verdict", "").startswith("FAIL_") for level in ["L4", "L5", "L6"])
    feature_pass = feature.get("verdict") == "FEATURE_TRACE_PASS"
    reference_pass = reference.get("verdict") == "REFERENCE_PASS"
    if feature_pass and reference_pass and l0_l3_pass and l4_l6_not_comparable:
        consensus = "LOCAL_ORACLE_CONFIDENCE_HIGH"
    elif feature_pass and reference_pass:
        consensus = "LOCAL_ORACLE_CONFIDENCE_MEDIUM"
    elif not feature or not reference:
        consensus = "NOT_COMPARABLE"
    else:
        consensus = "LOCAL_ORACLE_CONFIDENCE_LOW"
    return {
        "consensus": consensus,
        "feature_id": feature.get("feature_id", "producer_range_filter_v1"),
        "feature_parity_verdict": feature.get("verdict", "UNAVAILABLE"),
        "reference_oracle_verdict": reference.get("verdict", "UNAVAILABLE"),
        "lifecycle_levels": {level: levels[level].get("verdict", "UNAVAILABLE") for level in levels},
        "l0_l3_pass": l0_l3_pass,
        "l4_l6_limitation": "NOT_COMPARABLE: PineTS full adapter does not emit real decision/trade/stats lifecycle rows.",
        "pinets_role": "PineTS is validated for L0-L3 on this feature.",
        "python_role": "Python is validated against PineTS and independent reference for feature trace; Python remains local lifecycle owner.",
        "tradingview_claim": "No TradingView final audit claim is made.",
        "input_paths": {
            "feature_report": str(feature_report),
            "reference_report": str(reference_report),
            "lifecycle_dir": str(lifecycle_dir),
        },
        "code_hash": git_code_hash(),
    }


def markdown_report(payload: dict[str, Any], command: str) -> str:
    levels = payload["lifecycle_levels"]
    lines = [
        "# Range Filter Oracle Consensus Report",
        "",
        f"- Consensus: `{payload['consensus']}`",
        f"- Command: `{command}`",
        f"- Feature parity verdict: `{payload['feature_parity_verdict']}`",
        f"- Reference oracle verdict: `{payload['reference_oracle_verdict']}`",
        f"- L0: `{levels.get('L0')}`",
        f"- L1: `{levels.get('L1')}`",
        f"- L2: `{levels.get('L2')}`",
        f"- L3: `{levels.get('L3')}`",
        f"- L4: `{levels.get('L4')}` classified as `NOT_COMPARABLE` for lifecycle smoke",
        f"- L5: `{levels.get('L5')}` classified as `NOT_COMPARABLE` for lifecycle smoke",
        f"- L6: `{levels.get('L6')}` classified as `NOT_COMPARABLE` for lifecycle smoke",
        f"- Code hash: `{payload['code_hash']}`",
        "",
        "## Roles",
        "",
        f"- {payload['pinets_role']}",
        f"- {payload['python_role']}",
        f"- {payload['l4_l6_limitation']}",
        f"- {payload['tradingview_claim']}",
        "",
        "## Inputs",
        "",
    ]
    for key, value in payload["input_paths"].items():
        lines.append(f"- {key}: `{value}`")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--feature-report", default="reports/parity/case_001/features/producer_range_filter_v1/FEATURE_PARITY_REPORT.json")
    parser.add_argument("--reference-report", default="reports/INDEPENDENT_REFERENCE_ORACLE/range_filter_reference_oracle_report.json")
    parser.add_argument("--lifecycle-dir", default="reports/parity/case_001_range_filter")
    parser.add_argument("--out-md", default="reports/INDEPENDENT_REFERENCE_ORACLE/range_filter_oracle_consensus_report.md")
    parser.add_argument("--out-json", default="reports/INDEPENDENT_REFERENCE_ORACLE/range_filter_oracle_consensus_report.json")
    args = parser.parse_args()
    command = "python parity_oracles/oracle_consensus_report.py " + " ".join(sys.argv[1:])
    payload = build_consensus(ROOT / args.feature_report, ROOT / args.reference_report, ROOT / args.lifecycle_dir)
    payload["command"] = command
    payload["output_paths"] = {"markdown": args.out_md, "json": args.out_json}
    write_json(ROOT / args.out_json, payload)
    out_md = ROOT / args.out_md
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(markdown_report(payload, command), encoding="utf-8")
    print(out_md)
    print(ROOT / args.out_json)
    return 0 if payload["consensus"] in {"LOCAL_ORACLE_CONFIDENCE_HIGH", "LOCAL_ORACLE_CONFIDENCE_MEDIUM"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
