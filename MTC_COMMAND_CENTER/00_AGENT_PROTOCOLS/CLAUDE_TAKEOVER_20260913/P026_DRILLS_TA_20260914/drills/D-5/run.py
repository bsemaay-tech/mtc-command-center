import hashlib
import json
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
from p030_closed_partition_backup_adapter import restore_verified_prefix

BASE = LANE / "fixtures"
config = BASE / "config" / "intended_config_d4.json"
manifest = BASE / "backup_root" / "manifest.jsonl"

run_id = None
for line in manifest.read_text(encoding="utf-8").splitlines():
    rec = json.loads(line)
    if rec.get("record") == "run_start":
        run_id = rec.get("run_id")
if run_id is None:
    raise RuntimeError("no run_id")

target_root = BASE / "d5_restore"
target = target_root / "target"
if target.exists():
    shutil.rmtree(target)
target.mkdir(parents=True)

receipt_path = restore_verified_prefix(
    config, run_id=run_id, store_id="p030_closed_partition", target=target
)
print(f"run_id={run_id}")
print(f"receipt={receipt_path}")
print(f"receipt_exists={receipt_path.exists()}")
print(f"target_entries={sorted(str(p.relative_to(target)) for p in target.rglob('*'))}")

receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
identity_fields = (
    "high_water_bytes",
    "record_count",
    "last_observation_id",
    "prefix_sha256",
    "captured_at_utc",
    "dataset_content_hash",
)
print(
    f"receipt_identity run_id={receipt.get('run_id')} store_id={receipt.get('store_id')} "
    f"restored_prefix={receipt.get('restored_prefix')}"
)
for field in identity_fields:
    print(f"receipt_field {field}={receipt.get(field)}")

restored_prefix = Path(receipt["restored_prefix"])
print("type_checks:")
for path in sorted(restored_prefix.rglob("*")):
    rel = path.relative_to(restored_prefix).as_posix()
    print(
        f"type {rel} is_symlink={path.is_symlink()} is_junction={path.is_junction()} "
        f"is_file={path.is_file()} is_dir={path.is_dir()}"
    )

archived_prefix = BASE / "backup_root" / "runs" / run_id / "p030_closed_partition"


def sha256_hex(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


restored_receipt = sha256_hex(restored_prefix / "_P030_STABLE_PREFIX.json")
restored_snapshot = sha256_hex(restored_prefix / "source.jsonl")
archived_receipt = sha256_hex(archived_prefix / "_P030_STABLE_PREFIX.json")
archived_snapshot = sha256_hex(archived_prefix / "source.jsonl")
print(
    f"restored_bytes_equal_archived "
    f"receipt={restored_receipt == archived_receipt} "
    f"snapshot={restored_snapshot == archived_snapshot} "
    f"receipt_sha256={restored_receipt} snapshot_sha256={restored_snapshot}"
)
