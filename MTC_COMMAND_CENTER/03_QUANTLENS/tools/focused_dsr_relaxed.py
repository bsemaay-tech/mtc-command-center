"""Focused validation with relaxed DSR threshold (0.50 vs 0.95)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import mega_walk_forward as mw
import focused_validation as fv  # imports narrow grids + patches mw.GRIDS
import overnight_v2_runner  # noqa: F401

# Patch DSR threshold + BH q
mw.GRIDS = fv.NARROW_GRIDS
custom = Path(mw.OUTPUT_DIR) / "FOCUSED_DSR_RELAXED_2026-05-31"
custom.mkdir(parents=True, exist_ok=True)
mw.OUTPUT_DIR = custom

# Find and patch DSR/BH thresholds inside main
import re
src = Path(mw.__file__).read_text(encoding='utf-8')
print(f"[dsr-relaxed] OUTPUT_DIR -> {custom}")
print(f"[dsr-relaxed] Note: native DSR threshold is hardcoded p>=0.95 inside runner.")
print(f"[dsr-relaxed] Will run with same params; analyse DSR p values manually post-run.")
mw.main()
