import json
import os
import subprocess
from pathlib import Path

LANE = Path(r"C:/tmp/P026_DRILLS_TA_20260914")
_TMP = LANE / "tmp"
_TMP.mkdir(parents=True, exist_ok=True)
os.environ["TEMP"] = str(_TMP)
os.environ["TMP"] = str(_TMP)
os.environ["PYTHONUTF8"] = "1"

PYTHON = r"C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe"
BASE = LANE / "fixtures"
ARCHIVE = BASE / "d12" / "archive"


def _clean_root(path: Path) -> Path:
    if path.exists():
        for child in sorted(path.rglob("*"), reverse=True):
            if child.is_file():
                child.unlink()
            elif child.is_dir():
                try:
                    child.rmdir()
                except OSError:
                    pass
    path.mkdir(parents=True, exist_ok=True)
    return path


archive = _clean_root(ARCHIVE)
month_file = archive / "bars" / "HYPERLIQUID" / "BTC" / "1h" / "1970-01.jsonl"
month_file.parent.mkdir(parents=True, exist_ok=True)
month_file.write_text(
    "\n".join(
        [
            json.dumps({"bar_open_time": 3_600_000, "symbol": "BTC", "interval": "1h"}, separators=(",", ":")),
            json.dumps({"bar_open_time": 10_800_000, "symbol": "BTC", "interval": "1h"}, separators=(",", ":")),
        ]
    )
    + "\n",
    encoding="utf-8",
)

cmd = [
    PYTHON,
    str(LANE / "wt" / "market_data_collector.py"),
    "gap-report",
    "--archive",
    str(archive),
    "--symbol",
    "BTC",
    "--interval",
    "1h",
]
result = subprocess.run(cmd, text=True, capture_output=True, encoding="utf-8")
print(result.stdout.rstrip())
if result.stderr:
    print(result.stderr.rstrip())
print(f"gap-report-rc={result.returncode}")
