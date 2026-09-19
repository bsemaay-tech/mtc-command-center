import hashlib
import json
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
from p030_closed_partition_backup_adapter import backup_stable_prefix

BASE = LANE / "fixtures"
config = BASE / "config" / "intended_config_d4.json"
receipt = BASE / "contract_partition" / "stable_prefix" / "drill_3" / "_P030_STABLE_PREFIX.json"
source_root = BASE / "contract_partition"
backup_root = BASE / "backup_root"
snapshot = receipt.parent / "source.jsonl"


def sha256_hex(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


before_receipt = sha256_hex(receipt)
before_snapshot = sha256_hex(snapshot)
print(f"byte_compare_before receipt_sha256={before_receipt} snapshot_sha256={before_snapshot}")

run_id = backup_stable_prefix(
    config, stable_receipt=receipt, store_id="p030_closed_partition", source_root=source_root
)
print(f"run_id={run_id}")

after_receipt = sha256_hex(receipt)
after_snapshot = sha256_hex(snapshot)
print(
    f"byte_compare_after receipt_equal={after_receipt == before_receipt} "
    f"snapshot_equal={after_snapshot == before_snapshot}"
)

archived_prefix = backup_root / "runs" / run_id / "p030_closed_partition"
archived_receipt = sha256_hex(archived_prefix / "_P030_STABLE_PREFIX.json")
archived_snapshot = sha256_hex(archived_prefix / "source.jsonl")
print(
    f"byte_compare_archived receipt_equal={archived_receipt == before_receipt} "
    f"snapshot_equal={archived_snapshot == before_snapshot}"
)

manifest_path = backup_root / "manifest.jsonl"
print(f"manifest={manifest_path}")
print(f"manifest_exists={manifest_path.exists()}")

records = [json.loads(line) for line in manifest_path.read_text(encoding="utf-8").splitlines() if line.strip()]
run_records = [rec for rec in records if rec.get("run_id") == run_id]
types = [rec.get("record") for rec in run_records]
print(f"manifest_record_types={types}")
file_recs = [rec for rec in run_records if rec.get("record") == "file"]
for rec in file_recs:
    print(f"manifest_file rel={rec.get('rel')} readback={rec.get('readback')} size={rec.get('size')} sha256={rec.get('sha256')}")
ends = [rec for rec in run_records if rec.get("record") == "run_end"]
if ends:
    end = ends[-1]
    print(f"manifest_run_end status={end.get('status')} errors={end.get('errors')} files={end.get('files')} bytes={end.get('bytes')}")
member_set = {rec.get("rel") for rec in file_recs}
print(f"member_set={sorted(member_set)}")
