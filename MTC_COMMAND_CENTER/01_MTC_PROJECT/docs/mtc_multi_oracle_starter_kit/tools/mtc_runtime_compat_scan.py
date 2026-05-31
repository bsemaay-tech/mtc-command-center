#!/usr/bin/env python3
"""
MTC Pine Runtime Compatibility Scanner

Regex-based scanner for Pine Script v6 files. It does not claim semantic parsing.
It is designed to quickly map which runtime features an MTC file uses.

Usage:
  python tools/mtc_runtime_compat_scan.py --pine path/to/MASTER_TEMPLATE_CORE.pine --out-dir reports
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from datetime import datetime, timezone

FEATURE_PATTERNS = {
    "pine_version": r"//@version\s*=\s*(\d+)",
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
    "array_namespace": r"\barray\.",
    "matrix_namespace": r"\bmatrix\.",
    "map_namespace": r"\bmap\.",
    "type_declarations": r"(?m)^\s*type\s+[A-Za-z_][A-Za-z0-9_]*",
    "method_definitions": r"(?m)^\s*method\s+[A-Za-z_][A-Za-z0-9_]*",
    "var_keyword": r"(?<![A-Za-z0-9_])var\s+",
    "varip_keyword": r"(?<![A-Za-z0-9_])varip\s+",
    "input_namespace": r"\binput\.",
    "alert_calls": r"\balert\s*\(",
    "alertcondition_calls": r"\balertcondition\s*\(",
    "timeframe_namespace": r"\btimeframe\.",
    "session_mentions": r"\bsession\b",
    "barstate_isconfirmed": r"\bbarstate\.isconfirmed\b",
    "barstate_namespace": r"\bbarstate\.",
    "ta_namespace": r"\bta\.",
    "math_namespace": r"\bmath\.",
    "line_label_table_drawing": r"\b(line|label|table)\.",
    "plot_calls": r"\bplot\s*\(",
    "plotshape_calls": r"\bplotshape\s*\(",
    "plotchar_calls": r"\bplotchar\s*\(",
    "lookahead_mentions": r"\blookahead\b",
    "gaps_mentions": r"\bgaps\b",
}

def strip_comments(text: str) -> str:
    # Keep version comment. Remove obvious block comments and line comments for better counting.
    version_lines = "\n".join(re.findall(r"(?m)^//@version\s*=\s*\d+.*$", text))
    no_blocks = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    no_lines = re.sub(r"(?m)^\s*//(?!@version).*$", "", no_blocks)
    return version_lines + "\n" + no_lines

def extract_balanced_calls(text: str, func_name: str, limit: int = 50) -> list[str]:
    results = []
    pattern = re.compile(re.escape(func_name) + r"\s*\(")
    for m in pattern.finditer(text):
        start = m.start()
        i = m.end() - 1
        depth = 0
        end = None
        for j in range(i, min(len(text), i + 2000)):
            ch = text[j]
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    end = j + 1
                    break
        if end:
            snippet = " ".join(text[start:end].split())
            results.append(snippet[:500])
        if len(results) >= limit:
            break
    return results

def scan_pine(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8", errors="replace")
    text = strip_comments(raw)

    features = {}
    for name, pat in FEATURE_PATTERNS.items():
        if name == "pine_version":
            m = re.search(pat, raw)
            features[name] = m.group(1) if m else None
        else:
            features[name] = len(re.findall(pat, text))

    ta_funcs = Counter(re.findall(r"\bta\.([A-Za-z_][A-Za-z0-9_]*)\s*\(", text))
    strategy_funcs = Counter(re.findall(r"\bstrategy\.([A-Za-z_][A-Za-z0-9_]*)\s*\(", text))
    input_names = re.findall(r'\binput\.[A-Za-z_][A-Za-z0-9_]*\s*\([^)]*?title\s*=\s*"([^"]+)"', text)

    return {
        "scanned_at_utc": datetime.now(timezone.utc).isoformat(),
        "file": str(path),
        "bytes": path.stat().st_size,
        "features": features,
        "top_ta_functions": ta_funcs.most_common(50),
        "top_strategy_functions": strategy_funcs.most_common(50),
        "request_security_calls": extract_balanced_calls(text, "request.security", 50),
        "request_security_lower_tf_calls": extract_balanced_calls(text, "request.security_lower_tf", 50),
        "input_titles": input_names[:200],
    }

def md_report(result: dict) -> str:
    f = result["features"]
    lines = [
        "# MTC Runtime Compatibility Scan",
        "",
        f"- File: `{result['file']}`",
        f"- Scanned UTC: `{result['scanned_at_utc']}`",
        f"- Pine version: `{f.get('pine_version')}`",
        f"- File size: `{result['bytes']}` bytes",
        "",
        "## Feature counts",
        "",
        "| Feature | Count / Value |",
        "|---|---:|",
    ]
    for key, value in f.items():
        lines.append(f"| `{key}` | `{value}` |")

    lines += ["", "## Top ta.* functions", "", "| Function | Count |", "|---|---:|"]
    for name, count in result["top_ta_functions"]:
        lines.append(f"| `ta.{name}` | {count} |")

    lines += ["", "## Top strategy.* functions", "", "| Function | Count |", "|---|---:|"]
    for name, count in result["top_strategy_functions"]:
        lines.append(f"| `strategy.{name}` | {count} |")

    lines += ["", "## request.security calls", ""]
    for i, call in enumerate(result["request_security_calls"], 1):
        lines.append(f"{i}. `{call}`")

    lines += ["", "## Input titles", ""]
    for title in result["input_titles"]:
        lines.append(f"- {title}")

    lines += [
        "",
        "## Interpretation hints",
        "",
        "- Many `request.security` calls increase HTF alignment risk.",
        "- `varip` usage needs special attention outside TradingView.",
        "- `strategy.exit`, BE/trailing/partial exits must be compared at L5 execution level.",
        "- Indicator equality at L1 does not prove trade parity at L5/L6.",
    ]
    return "\n".join(lines) + "\n"

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pine", required=True, help="Path to Pine Script file")
    ap.add_argument("--out-dir", default="reports", help="Output directory")
    args = ap.parse_args()

    pine_path = Path(args.pine)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not pine_path.exists():
        raise FileNotFoundError(f"Pine file not found: {pine_path}")

    result = scan_pine(pine_path)

    json_path = out_dir / "mtc_runtime_compat_scan.json"
    md_path = out_dir / "mtc_runtime_compat_scan.md"
    json_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    md_path.write_text(md_report(result), encoding="utf-8")

    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
