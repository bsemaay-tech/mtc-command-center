#!/usr/bin/env python3
"""
Placeholder normalizer.

Codex should adapt this file to the real output format of the engine/export.
Keep the standard output filenames and columns unchanged.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from common import ensure_dir, write_csv, write_json, COLUMNS

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=False, help="Engine-specific input file/folder")
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    out_dir = ensure_dir(Path(args.out_dir))
    write_csv(out_dir / "normalized_signals.csv", COLUMNS["signals"], [])
    write_csv(out_dir / "normalized_indicators.csv", COLUMNS["indicators"], [])
    write_csv(out_dir / "normalized_decisions.csv", COLUMNS["decisions"], [])
    write_csv(out_dir / "normalized_trades.csv", COLUMNS["trades"], [])
    write_json(out_dir / "normalized_stats.json", {
        "status": "STUB",
        "message": "Codex must wire this normalizer to the real engine/export output."
    })
    print(f"Wrote stub normalized files to {out_dir}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
