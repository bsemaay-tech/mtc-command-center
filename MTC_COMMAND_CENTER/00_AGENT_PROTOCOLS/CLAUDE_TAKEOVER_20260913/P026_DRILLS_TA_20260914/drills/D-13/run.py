import os
import shutil
import sys
from pathlib import Path

LANE = Path(r"C:/tmp/P026_DRILLS_TA_20260914")
_TMP = LANE / "tmp"
_TMP.mkdir(parents=True, exist_ok=True)
os.environ["TEMP"] = str(_TMP)
os.environ["TMP"] = str(_TMP)
os.environ["PYTHONUTF8"] = "1"

sys.path.insert(0, str((LANE / "wt").resolve()))

from p030_closed_partition_backup_adapter import capture_stable_prefix

BASE = LANE / "fixtures"


def _reset(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)


source_root = BASE / "d11" / "restart"
source_jsonl = source_root / "bars" / "HYPERLIQUID" / "BTC" / "1h" / "1970-01.jsonl"
if not source_jsonl.exists():
    raise RuntimeError(f"source partition missing: {source_jsonl}")

hash_file = BASE / "contract_partition" / "stable_hash.txt"
dataset_hash = hash_file.read_text(encoding="utf-8").strip()

stable_dir = BASE / "d13_capture" / "red"
_reset(stable_dir)

try:
    capture_stable_prefix(
        source_jsonl=source_jsonl,
        stable_prefix=stable_dir,
        source_root=source_root,
        high_water_bytes=source_jsonl.stat().st_size,
        captured_at_utc="2026-09-14T06:45:00Z",
        dataset_content_hash=dataset_hash,
    )
    print("D13-RED: OK-UNEXPECTED")
except Exception as exc:
    print(f"D13-RED: ERROR {type(exc).__name__}: {exc}")
