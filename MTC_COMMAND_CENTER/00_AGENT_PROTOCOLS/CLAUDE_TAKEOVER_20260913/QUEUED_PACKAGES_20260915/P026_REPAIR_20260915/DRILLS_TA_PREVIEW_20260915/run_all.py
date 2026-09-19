"""Runs the four preview drills in order with the pinned 3.12.12 interpreter; captures stdout/stderr per drill."""
import subprocess
import time
from pathlib import Path

LANE = Path("C:/tmp/P026_DRILLS_TA_PREVIEW_20260915")
PY = r"C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe"
for d in ("D-4", "D-5", "D-6", "D-7"):
    t0 = time.time()
    p = subprocess.run([PY, str(LANE / "drills" / d / "run.py")], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(LANE / "tmp"))
    (LANE / "drills" / d / "stdout.txt").write_text(p.stdout, encoding="utf-8", newline="\n")
    (LANE / "drills" / d / "stderr.txt").write_text(p.stderr, encoding="utf-8", newline="\n")
    print(f"{d}: rc={p.returncode} {time.time() - t0:.1f}s stdout_lines={len(p.stdout.splitlines())} stderr_lines={len(p.stderr.splitlines())}")
