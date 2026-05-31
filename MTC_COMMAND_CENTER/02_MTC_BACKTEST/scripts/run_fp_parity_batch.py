#!/usr/bin/env python
"""
Run FP parity template cases in deterministic order.

This script only runs cases whose `tv_csv` file exists.
Missing CSV cases are reported as `missing_tv_csv`.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
TPL_DIR = PROJECT_ROOT / "configs" / "cases" / "fp_parity_templates"


@dataclass
class CaseItem:
    name: str
    rel_case_path: str
    tv_csv: str


def discover_templates() -> List[CaseItem]:
    items: List[CaseItem] = []
    for p in sorted(TPL_DIR.glob("fp*_template.json")):
        with open(p, encoding="utf-8-sig") as f:
            data = json.load(f)
        tv_csv = str(data.get("tv_csv", "")).strip()
        rel_case = str(p.relative_to(PROJECT_ROOT)).replace("\\", "/")
        items.append(CaseItem(name=p.name, rel_case_path=rel_case, tv_csv=tv_csv))
    return items


def run_batch() -> int:
    sys.path.insert(0, str(SCRIPT_DIR))
    import parity_regression

    summary = []
    failures = 0
    missing = 0
    for item in discover_templates():
        tv_path = PROJECT_ROOT / item.tv_csv
        if not tv_path.exists():
            summary.append({"case": item.name, "status": "missing_tv_csv", "tv_csv": item.tv_csv})
            missing += 1
            continue
        code = int(parity_regression.run(item.rel_case_path))
        status = "pass" if code == 0 else "fail"
        summary.append({"case": item.name, "status": status, "tv_csv": item.tv_csv})
        if code != 0:
            failures += 1

    out = PROJECT_ROOT / "reports" / "fp_parity_batch_summary.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"items": summary, "failures": failures, "missing": missing}, f, indent=2)

    print(f"Summary written: {out}")
    print(f"Cases: {len(summary)} | fail={failures} | missing_tv_csv={missing}")

    if failures > 0:
        return 1
    if missing > 0:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(run_batch())
