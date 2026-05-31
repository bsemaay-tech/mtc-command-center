from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from parity_oracles.common.io_utils import ROOT, git_code_hash, sha256_file, sha256_json, write_json


PATTERNS = {
    "strategy_declaration": r"\bstrategy\s*\(",
    "indicator_declaration": r"\bindicator\s*\(",
    "strategy_entry": r"\bstrategy\.entry\s*\(",
    "strategy_exit": r"\bstrategy\.exit\s*\(",
    "strategy_close": r"\bstrategy\.close\s*\(",
    "strategy_close_all": r"\bstrategy\.close_all\s*\(",
    "strategy_position_size": r"\bstrategy\.position_size\b",
    "strategy_opentrades": r"\bstrategy\.opentrades\b",
    "strategy_closedtrades": r"\bstrategy\.closedtrades\b",
    "request_security": r"\brequest\.security\s*\(",
    "request_security_lower_tf": r"\brequest\.security_lower_tf\s*\(",
    "array_usage": r"\barray\.",
    "matrix_usage": r"\bmatrix\.",
    "map_usage": r"\bmap\.",
    "type_declarations_udt": r"(?m)^\s*type\s+\w+",
    "method_definitions": r"(?m)^\s*method\s+\w+",
    "var": r"\bvar\s+",
    "varip": r"\bvarip\s+",
    "input_usage": r"\binput(?:\.\w+)?\s*\(",
    "alert_usage": r"\balert\s*\(",
    "alertcondition_usage": r"\balertcondition\s*\(",
    "timeframe_usage": r"\btimeframe\.",
    "session_time_filters": r"\bsession\b|\btime\s*\(",
    "barstate_isconfirmed": r"\bbarstate\.isconfirmed\b",
    "barstate_usage": r"\bbarstate\.",
    "ta_usage": r"\bta\.",
    "math_usage": r"\bmath\.",
    "line_label_table_drawing": r"\b(?:line|label|table)\.",
    "plot_usage": r"\bplot(?:shape|char)?\s*\(",
    "security_lookahead_gaps": r"\b(?:lookahead|gaps)\s*=",
}


def top_functions(text: str, namespace: str, limit: int = 50) -> list[dict[str, int | str]]:
    counter = Counter(re.findall(rf"\b{re.escape(namespace)}\.(\w+)\s*(?:\(|\b)", text))
    return [{"name": name, "count": count} for name, count in counter.most_common(limit)]


def extract_inputs(text: str) -> list[str]:
    names: list[str] = []
    for match in re.finditer(r"\binput(?:\.\w+)?\s*\(([^)]*)\)", text, flags=re.DOTALL):
        body = match.group(1)
        title_match = re.search(r"title\s*=\s*['\"]([^'\"]+)['\"]", body)
        if title_match:
            names.append(title_match.group(1))
            continue
        first_string = re.search(r"['\"]([^'\"]+)['\"]", body)
        if first_string:
            names.append(first_string.group(1))
    return sorted(set(names))


def extract_request_expressions(text: str) -> list[str]:
    expressions: list[str] = []
    for match in re.finditer(r"\brequest\.security(?:_lower_tf)?\s*\((.{0,240})", text):
        snippet = " ".join(match.group(0).split())
        expressions.append(snippet[:240])
    return expressions[:50]


def scan(pine: Path, command: str) -> dict[str, object]:
    text = pine.read_text(encoding="utf-8", errors="replace")
    version_match = re.search(r"//@version\s*=\s*(\d+)", text)
    counts = {name: len(re.findall(pattern, text)) for name, pattern in PATTERNS.items()}
    return {
        "pine_file": str(pine),
        "pine_version": version_match.group(1) if version_match else "unknown",
        "command": command,
        "data_hash": sha256_file(pine),
        "config_hash": sha256_json({}),
        "code_hash": git_code_hash(),
        "counts": counts,
        "top_ta_functions": top_functions(text, "ta"),
        "top_strategy_functions": top_functions(text, "strategy"),
        "top_request_security_expressions": extract_request_expressions(text),
        "input_names": extract_inputs(text),
    }


def write_markdown(report: dict[str, object], path: Path) -> None:
    counts = report["counts"]
    lines = [
        "# MTC Runtime Compatibility Scan",
        "",
        f"- Pine file: `{report['pine_file']}`",
        f"- Pine version: `{report['pine_version']}`",
        f"- Command: `{report['command']}`",
        f"- Data hash: `{report['data_hash']}`",
        f"- Config hash: `{report['config_hash']}`",
        f"- Code hash: `{report['code_hash']}`",
        "",
        "## Feature Counts",
        "",
        "| Feature | Count |",
        "|---|---:|",
    ]
    for key, value in sorted(counts.items()):
        lines.append(f"| {key} | {value} |")
    lines.extend(["", "## Top ta.* Functions", ""])
    for item in report["top_ta_functions"]:
        lines.append(f"- {item['name']}: {item['count']}")
    lines.extend(["", "## Top strategy.* Functions", ""])
    for item in report["top_strategy_functions"]:
        lines.append(f"- {item['name']}: {item['count']}")
    lines.extend(["", "## request.security Expressions", ""])
    for expression in report["top_request_security_expressions"]:
        lines.append(f"- `{expression}`")
    lines.extend(["", "## Inputs", ""])
    for name in report["input_names"]:
        lines.append(f"- {name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pine", type=Path, required=True)
    parser.add_argument("--out-md", type=Path, default=ROOT / "reports" / "mtc_runtime_compat_scan.md")
    parser.add_argument("--out-json", type=Path, default=ROOT / "reports" / "mtc_runtime_compat_scan.json")
    args = parser.parse_args()
    command = f"python tools/mtc_runtime_compat_scan.py --pine {args.pine}"
    report = scan(args.pine, command)
    write_json(args.out_json, report)
    write_markdown(report, args.out_md)
    print(args.out_md)
    print(args.out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
