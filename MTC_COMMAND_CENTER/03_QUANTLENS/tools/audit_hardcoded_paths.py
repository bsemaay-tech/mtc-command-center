#!/usr/bin/env python
"""Audit code-like files for legacy clean-repo path regressions."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SELF = Path(__file__).resolve()

DEFAULT_EXTS = {
    ".py",
    ".ps1",
    ".sh",
    ".bat",
    ".cmd",
    ".json",
    ".toml",
    ".yaml",
    ".yml",
    ".js",
    ".ts",
}
DOC_EXTS = {".md", ".txt", ".csv"}
SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    "05_BACKTEST_RESULTS",
    "overnight_runs",
    "sprint_runs",
    "single_strategy_runs",
    "cpcv_runs",
    "pbo_runs",
    "reports",
}
PATTERNS = {
    "legacy_repo_root": re.compile(r"C:[\\/]+LAB[\\/]+tradingview-lab", re.IGNORECASE),
    "legacy_data_bundle": re.compile(r"MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427", re.IGNORECASE),
}


@dataclass
class Finding:
    path: str
    line: int
    pattern: str
    text: str


def staged_paths() -> list[Path]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git diff --cached failed")
    return [REPO_ROOT / line.strip() for line in result.stdout.splitlines() if line.strip()]


def iter_files(root: Path, include_docs: bool, staged_only: bool) -> list[Path]:
    if staged_only:
        candidates = staged_paths()
    else:
        candidates = [p for p in root.rglob("*") if p.is_file()]

    exts = DEFAULT_EXTS | (DOC_EXTS if include_docs else set())
    files: list[Path] = []
    for path in candidates:
        resolved = path.resolve()
        if resolved == SELF:
            continue
        rel_parts = set(resolved.relative_to(root).parts) if resolved.is_relative_to(root) else set()
        if rel_parts & SKIP_DIRS:
            continue
        if path.suffix.lower() in exts:
            files.append(path)
    return files


def scan_file(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return [Finding(str(path.relative_to(REPO_ROOT)), 0, "read_error", str(exc))]

    for line_no, line in enumerate(text.splitlines(), start=1):
        for name, pattern in PATTERNS.items():
            if pattern.search(line):
                findings.append(
                    Finding(
                        str(path.relative_to(REPO_ROOT)).replace("\\", "/"),
                        line_no,
                        name,
                        line.strip()[:220],
                    )
                )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    parser.add_argument("--staged", action="store_true", help="scan only staged files")
    parser.add_argument("--include-docs", action="store_true", help="include md/txt/csv files")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of text")
    parser.add_argument("--max-findings", type=int, default=200, help="text output cap; 0 prints all")
    args = parser.parse_args()

    root = args.root.resolve()
    findings: list[Finding] = []
    for path in iter_files(root, args.include_docs, args.staged):
        findings.extend(scan_file(path))

    if args.json:
        print(json.dumps([asdict(f) for f in findings], indent=2, sort_keys=True))
    elif findings:
        print(f"Hardcoded legacy path findings: {len(findings)}")
        shown = findings if args.max_findings == 0 else findings[: args.max_findings]
        for finding in shown:
            print(f"{finding.path}:{finding.line}: {finding.pattern}: {finding.text}")
        if len(shown) < len(findings):
            print(f"... {len(findings) - len(shown)} more finding(s) omitted; rerun with --json or --max-findings 0 for full output")
    else:
        print("Hardcoded legacy path audit PASS")

    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
