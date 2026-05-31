#!/usr/bin/env python
"""
Sync tv_manual_inputs case folders with current manifest.

Behavior:
- create missing case folders from manifest run_order + case_id
- archive obsolete numeric case folders into _archive_<timestamp> (default)
"""

from __future__ import annotations

import argparse
import csv
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CASE_DIR_RE = re.compile(r"^\d{3}_.+")


def now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def parse_int(raw: Any, default: int = 0) -> int:
    try:
        return int(str(raw).strip())
    except Exception:
        return default


def as_bool(raw: Any, default: bool = True) -> bool:
    if raw is None:
        return default
    txt = str(raw).strip().lower()
    if txt in {"1", "true", "yes", "y"}:
        return True
    if txt in {"0", "false", "no", "n"}:
        return False
    return default


def load_manifest(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    rows = [r for r in rows if as_bool(r.get("enabled", "1"), True)]
    rows.sort(key=lambda r: parse_int(r.get("run_order", 0), 0))
    return rows


def case_folder_name(row: dict[str, str]) -> str:
    run_order = parse_int(row.get("run_order", 0), 0)
    case_id = (row.get("case_id") or "").strip()
    return f"{run_order:03d}_{case_id}"


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Sync tv_manual_inputs folders from manifest.")
    ap.add_argument("--suite-root", default="mtc_backtest/parity_suite_350", help="Suite root path")
    ap.add_argument("--manifest", default="manifests/cases_manifest_all.csv", help="Manifest path")
    ap.add_argument("--tv-root", default="tv_manual_inputs", help="TV root path")
    ap.add_argument("--delete-obsolete", action="store_true", help="Delete obsolete case folders instead of archiving")
    ap.add_argument("--dry-run", action="store_true", help="Analyze only, do not modify filesystem")
    return ap.parse_args()


def resolve(base: Path, raw: str) -> Path:
    p = Path(raw)
    if p.is_absolute():
        return p
    return (base / p).resolve()


def main() -> int:
    args = parse_args()
    suite_root = Path(args.suite_root).resolve()
    manifest_path = resolve(suite_root, args.manifest)
    tv_root = resolve(suite_root, args.tv_root)

    if not manifest_path.exists():
        print(f"ERROR: manifest not found: {manifest_path}")
        return 2
    tv_root.mkdir(parents=True, exist_ok=True)

    rows = load_manifest(manifest_path)
    desired = {case_folder_name(r) for r in rows}

    existing_dirs = [p for p in tv_root.iterdir() if p.is_dir() and CASE_DIR_RE.match(p.name)]
    existing = {p.name for p in existing_dirs}

    to_create = sorted(desired - existing)
    to_remove = sorted(existing - desired)

    archive_dir = tv_root / f"_archive_{now_stamp()}"
    archived = 0
    removed = 0
    created = 0

    for name in to_create:
        p = tv_root / name
        if not args.dry_run:
            p.mkdir(parents=True, exist_ok=True)
        created += 1

    for name in to_remove:
        src = tv_root / name
        if args.delete_obsolete:
            if not args.dry_run:
                shutil.rmtree(src, ignore_errors=True)
            removed += 1
        else:
            if not args.dry_run:
                archive_dir.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(archive_dir / name))
            archived += 1

    print(f"manifest_rows={len(rows)}")
    print(f"desired_case_dirs={len(desired)}")
    print(f"existing_case_dirs={len(existing)}")
    print(f"created={created}")
    print(f"archived={archived}")
    print(f"removed={removed}")
    print(f"dry_run={int(args.dry_run)}")
    print("status=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
