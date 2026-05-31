#!/usr/bin/env python
"""
Dependency analysis for parity_suite_350 final manifest.

This analyzer compares each enabled case against baseline and flags only
case-specific changes that are inactive due to dependency gating.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class CaseAnalysis:
    case_id: str
    total_diff_paths: int
    inactive_diff_paths: list[str]

    @property
    def is_fully_inert(self) -> bool:
        return self.total_diff_paths > 0 and len(self.inactive_diff_paths) == self.total_diff_paths

    @property
    def has_issue(self) -> bool:
        return self.total_diff_paths == 0 or len(self.inactive_diff_paths) > 0


def load_optimizer_module(suite_root: Path):
    scripts_dir = suite_root / "scripts"
    sys.path.insert(0, str(scripts_dir))
    import optimize_ui_coverage_case_set as opt  # type: ignore

    return opt


def parse_bool(raw: Any, default: bool = False) -> bool:
    if raw is None:
        return default
    text = str(raw).strip().lower()
    if text in {"1", "true", "yes", "y"}:
        return True
    if text in {"0", "false", "no", "n"}:
        return False
    return default


def pick_baseline_case_id(rows: list[dict[str, str]], requested: str) -> str:
    if requested:
        for row in rows:
            if row.get("case_id", "") == requested:
                return requested
    ordered = sorted(rows, key=lambda r: int(str(r.get("run_order", "0") or "0")))
    if not ordered:
        raise RuntimeError("No rows in manifest.")
    return str(ordered[0].get("case_id", ""))


def diff_paths(
    opt: Any,
    baseline_cfg: dict[str, Any],
    case_cfg: dict[str, Any],
) -> tuple[list[str], list[str]]:
    bflat = opt.flatten_leaves(baseline_cfg)
    cflat = opt.flatten_leaves(case_cfg)
    keys = sorted(set(bflat.keys()) | set(cflat.keys()))
    changed: list[str] = []
    inactive: list[str] = []
    for path in keys:
        if path in getattr(opt, "EXCLUDED_EXACT_PATHS", set()):
            continue
        excluded_prefixes = tuple(getattr(opt, "EXCLUDED_PATH_PREFIXES", tuple()))
        if any(path.startswith(prefix) for prefix in excluded_prefixes):
            continue
        bval = opt.normalize_value(bflat.get(path, None))
        cval = opt.normalize_value(cflat.get(path, None))
        if bval == cval:
            continue
        changed.append(path)
        if not opt.is_path_active(case_cfg, path):
            inactive.append(path)
    return changed, inactive


def analyze_suite(suite_root: Path, baseline_case_id: str) -> tuple[str, list[CaseAnalysis]]:
    opt = load_optimizer_module(suite_root)
    manifest_path = suite_root / "manifests" / "cases_manifest_all.csv"
    rows = opt.load_csv(manifest_path)
    enabled_rows = [r for r in rows if parse_bool(r.get("enabled", "1"), True)]
    baseline_case_id = pick_baseline_case_id(enabled_rows, baseline_case_id)

    cfg_by_case: dict[str, dict[str, Any]] = {}
    for row in enabled_rows:
        case_id = str(row.get("case_id", "")).strip()
        if not case_id:
            continue
        case_json = suite_root / str(row.get("case_json", "")).strip()
        obj = opt.load_json(case_json)
        cfg = obj.get("config", {})
        cfg_by_case[case_id] = cfg if isinstance(cfg, dict) else {}

    if baseline_case_id not in cfg_by_case:
        raise RuntimeError(f"Baseline case_id not found in enabled set: {baseline_case_id}")
    baseline_cfg = cfg_by_case[baseline_case_id]

    results: list[CaseAnalysis] = []
    for row in enabled_rows:
        case_id = str(row.get("case_id", "")).strip()
        if not case_id or case_id == baseline_case_id:
            continue
        changed, inactive = diff_paths(opt, baseline_cfg, cfg_by_case.get(case_id, {}))
        results.append(CaseAnalysis(case_id=case_id, total_diff_paths=len(changed), inactive_diff_paths=inactive))

    return baseline_case_id, results


def write_outputs(suite_root: Path, baseline_case_id: str, results: list[CaseAnalysis]) -> None:
    report_path = suite_root / "dependency_analysis_report.md"
    csv_path = suite_root / "INERT_ANALYSIS_FULL.csv"
    json_path = suite_root / "INERT_ANALYSIS_FULL.json"

    issues = [r for r in results if r.has_issue]
    fully_inert = [r for r in results if r.is_fully_inert]
    partial = [r for r in results if (r.total_diff_paths > 0 and len(r.inactive_diff_paths) > 0 and not r.is_fully_inert)]
    zero_diff = [r for r in results if r.total_diff_paths == 0]

    lines = [
        "# Dependency Analysis Report",
        "",
        f"- baseline_case_id: `{baseline_case_id}`",
        f"- analyzed_cases: {len(results)}",
        f"- cases_with_issues: {len(issues)}",
        f"- fully_inert_cases: {len(fully_inert)}",
        f"- partially_inert_cases: {len(partial)}",
        f"- no_diff_cases: {len(zero_diff)}",
        "",
    ]
    if fully_inert:
        lines.append("## Fully Inert Cases")
        lines.append("")
        for r in fully_inert:
            lines.append(f"- `{r.case_id}` ({len(r.inactive_diff_paths)}/{r.total_diff_paths} inactive paths)")
        lines.append("")
    if partial:
        lines.append("## Partially Inert Cases")
        lines.append("")
        for r in partial:
            lines.append(f"### `{r.case_id}`")
            lines.append(f"- inactive: {len(r.inactive_diff_paths)}/{r.total_diff_paths}")
            for p in r.inactive_diff_paths:
                lines.append(f"  - `{p}`")
            lines.append("")
    if zero_diff:
        lines.append("## No-Diff Cases")
        lines.append("")
        for r in zero_diff:
            lines.append(f"- `{r.case_id}`")
        lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")

    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["case_id", "total_diff_paths", "inactive_diff_paths_count", "inactive_diff_paths", "status"],
        )
        writer.writeheader()
        for r in results:
            if r.total_diff_paths == 0:
                status = "NO_DIFF"
            elif r.is_fully_inert:
                status = "FULLY_INERT"
            elif r.inactive_diff_paths:
                status = "PARTIALLY_INERT"
            else:
                status = "OK"
            writer.writerow(
                {
                    "case_id": r.case_id,
                    "total_diff_paths": r.total_diff_paths,
                    "inactive_diff_paths_count": len(r.inactive_diff_paths),
                    "inactive_diff_paths": ";".join(r.inactive_diff_paths),
                    "status": status,
                }
            )

    payload = {
        "baseline_case_id": baseline_case_id,
        "analyzed_cases": len(results),
        "cases_with_issues": len(issues),
        "fully_inert_cases": [r.case_id for r in fully_inert],
        "partially_inert_cases": [r.case_id for r in partial],
        "no_diff_cases": [r.case_id for r in zero_diff],
    }
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"baseline_case_id={baseline_case_id}")
    print(f"analyzed_cases={len(results)}")
    print(f"cases_with_issues={len(issues)}")
    print(f"fully_inert_cases={len(fully_inert)}")
    print(f"partially_inert_cases={len(partial)}")
    print(f"no_diff_cases={len(zero_diff)}")
    print(f"report={report_path}")
    print(f"csv={csv_path}")
    print(f"json={json_path}")
    print("status=ok")


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Analyze dependency-gated inert diffs in final case set.")
    ap.add_argument("--suite-root", default="mtc_backtest/parity_suite_350", help="Suite root path")
    ap.add_argument("--baseline-case-id", default="", help="Optional baseline case_id")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    suite_root = Path(args.suite_root).resolve()
    if not suite_root.exists():
        print(f"ERROR: suite-root not found: {suite_root}")
        return 2
    baseline_case_id, results = analyze_suite(suite_root, args.baseline_case_id)
    write_outputs(suite_root, baseline_case_id, results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
