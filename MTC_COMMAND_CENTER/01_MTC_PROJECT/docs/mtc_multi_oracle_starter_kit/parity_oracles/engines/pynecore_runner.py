#!/usr/bin/env python3
"""
Engine runner stub.

Codex should wire this file to the actual local command/environment.
This stub intentionally does not pretend to run a real engine.
"""

from __future__ import annotations

import argparse, json
from pathlib import Path
from datetime import datetime, timezone

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", required=False)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    result = {
        "engine_name": Path(__file__).stem.replace("_runner", ""),
        "status": "STUB",
        "run_started_at": datetime.now(timezone.utc).isoformat(),
        "run_finished_at": datetime.now(timezone.utc).isoformat(),
        "command": "Not wired yet",
        "output_files": [],
        "warnings": ["Codex must wire this runner to the real local engine."],
        "errors": []
    }
    (out_dir / "result_manifest.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Wrote stub result to {out_dir / 'result_manifest.json'}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
