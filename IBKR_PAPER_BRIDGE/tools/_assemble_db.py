#!/usr/bin/env python3
"""Generate db.py for TS-P1-002 from content blocks."""

import os
from pathlib import Path

ROOT = Path(r"C:\TSP1002\IBKR_PAPER_BRIDGE")
OUT = ROOT / "bridge" / "store" / "db.py"

# Read all content blocks
blocks_dir = ROOT / "tools" / "_p1_002_blocks"
blocks = sorted(blocks_dir.glob("db_*.txt"))

content = ""
for b in blocks:
    content += b.read_text(encoding="utf-8")

OUT.write_text(content, encoding="utf-8")
print(f"Wrote {OUT} ({len(content)} chars) from {len(blocks)} blocks")
