import os
import sys
from pathlib import Path

LANE = Path(r"C:/tmp/P026_DRILLS_TA_20260914")
_TMP = LANE / "tmp"
_TMP.mkdir(parents=True, exist_ok=True)
os.environ["TEMP"] = str(_TMP)
os.environ["TMP"] = str(_TMP)
os.environ["PYTHONUTF8"] = "1"

sys.path.insert(0, str((LANE / "wt").resolve()))

from p030_closed_partition_backup_adapter import load_runnable_config

BASE = LANE / "fixtures"
CONFIG_NULL = BASE / "config" / "null_config.json"
CONFIG_BULK = BASE / "config" / "bulk_store_config.json"
CONFIG_MISMATCH = BASE / "config" / "mismatch_path_config.json"
CONFIG_INTENDED = BASE / "config" / "intended_config.json"
STABLE_PREFIX = BASE / "contract_partition" / "stable_prefix"

CASES = [
    ("a", CONFIG_NULL),
    ("b", CONFIG_BULK),
    ("c", CONFIG_MISMATCH),
    ("d", CONFIG_INTENDED),
]

for name, path in CASES:
    try:
        result = load_runnable_config(
            path, stable_prefix=STABLE_PREFIX, store_id="p030_closed_partition"
        )
    except Exception as exc:
        print(f"{name}: ERROR {type(exc).__name__}: {exc}")
        cause = exc.__cause__
        if cause is not None:
            print(f"{name}: inner {type(cause).__name__}: {cause}")
        wrapped_at = (
            "p030_closed_partition_backup_adapter.py:388"
            if str(exc) == "backup config is not runnable"
            else None
        )
        if wrapped_at:
            print(f"{name}: wrapped_at {wrapped_at}")
    else:
        store = result["stores"][0]
        print(f"{name}: OK {store['id']} {store['class']} {store['path']}")
