#!/usr/bin/env python
"""
Run post-compare diagnostics in one command:
1) TV early trade-end candidate scan
2) Mismatch split by dual-status notes
3) Policy parity view (raw vs clip-effective)
"""

from __future__ import annotations

import subprocess
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> None:
    print(">", " ".join(cmd))
    res = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    if res.returncode != 0:
        print(res.stdout)
        print(res.stderr)
        raise SystemExit(res.returncode)
    if res.stdout.strip():
        print(res.stdout.strip())


def main() -> int:
    here = Path(__file__).resolve()
    suite_root = here.parent.parent
    mtc_root = suite_root.parent

    run(
        [
            "python",
            str(suite_root / "scripts" / "detect_tv_trade_list_truncation.py"),
            "--suite-root",
            str(suite_root),
            "--threshold-days",
            "30",
        ],
        cwd=mtc_root,
    )

    run(
        [
            "python",
            str(suite_root / "scripts" / "split_mismatch_by_dual_status.py"),
            "--suite-root",
            str(suite_root),
        ],
        cwd=mtc_root,
    )

    run(
        [
            "python",
            str(suite_root / "scripts" / "build_policy_parity_view.py"),
            "--suite-root",
            str(suite_root),
        ],
        cwd=mtc_root,
    )

    print("post-compare diagnostics complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
