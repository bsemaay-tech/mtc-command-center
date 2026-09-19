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
from p030_closed_partition_backup_adapter import capture_stable_prefix

BASE = LANE / "fixtures"
source_jsonl = BASE / "contract_partition" / "source.jsonl"
source_root = BASE / "contract_partition"
stable_prefix_root = BASE / "contract_partition" / "stable_prefix"
for p in stable_prefix_root.glob("*"):
    if p.is_dir():
        shutil.rmtree(p)
    else:
        p.unlink()

meta = json.loads((BASE / "contract_partition" / "descriptor.json").read_text(encoding="utf-8"))
dataset_hash = meta["dataset_content_hash"]

d3_dir = stable_prefix_root / "drill_3"
aligned_dir = stable_prefix_root / "aligned"
mid_dir = stable_prefix_root / "mid"
truncated_dir = stable_prefix_root / "truncated"

targets = [d3_dir, aligned_dir, mid_dir, truncated_dir]
for t in targets:
    if t.exists():
        if t.is_dir():
            shutil.rmtree(t)
        else:
            t.unlink()

# D-3 full-file capture
captured = capture_stable_prefix(
    source_jsonl=source_jsonl,
    stable_prefix=d3_dir,
    source_root=source_root,
    high_water_bytes=source_jsonl.stat().st_size,
    captured_at_utc="2026-09-14T05:40:00Z",
    dataset_content_hash=dataset_hash,
)
print(f"D3: receipt={captured}")
receipt = json.loads(captured.read_text(encoding="utf-8"))
print(
    "D3: state={state} high_water_bytes={high_water_bytes} record_count={record_count} "
    "last_observation_id={last_observation_id} prefix_sha256={prefix_sha256} "
    "captured_at_utc={captured_at_utc} dataset_content_hash={dataset_content_hash} "
    "source={source_path}".format(**receipt)
)
snapshot = d3_dir / receipt["snapshot_rel"]
print(f"D3: snapshot_bytes={snapshot.stat().st_size} snapshot_equals_high_water={snapshot.stat().st_size == receipt['high_water_bytes']}")

# D-3b: inside-file record-boundary offset (not the full file)
raw = source_jsonl.read_bytes()
file_size = len(raw)
newlines = [i for i, byte in enumerate(raw) if byte == 0x0A]
if len(newlines) < 2:
    raise RuntimeError("fixture source.jsonl must contain at least two records")
# First record boundary is an offset strictly inside the file.
aligned_offset = newlines[0] + 1
if aligned_offset <= 0 or aligned_offset >= file_size:
    raise RuntimeError("aligned offset is not inside the file")
print(f"D3b-aligned: file_size={file_size} high_water_bytes={aligned_offset} inside_file={aligned_offset < file_size}")
try:
    aligned_receipt_path = capture_stable_prefix(
        source_jsonl=source_jsonl,
        stable_prefix=aligned_dir,
        source_root=source_root,
        high_water_bytes=aligned_offset,
        captured_at_utc="2026-09-14T05:40:01Z",
        dataset_content_hash=dataset_hash,
    )
    aligned_receipt = json.loads(aligned_receipt_path.read_text(encoding="utf-8"))
    print(
        f"D3b: aligned-OK high_water_bytes={aligned_receipt['high_water_bytes']} "
        f"record_count={aligned_receipt['record_count']} "
        f"last_observation_id={aligned_receipt['last_observation_id']}"
    )
except Exception as exc:
    print(f"D3b: aligned-ERROR {type(exc).__name__}: {exc}")

# D-3b: mid-record offset
mid = newlines[0] // 2 if newlines[0] > 1 else max(1, file_size // 2)
if raw[mid - 1 : mid] == b"\n":
    mid = max(1, newlines[0] - 1)
print(f"D3b-mid: high_water_bytes={mid}")
try:
    capture_stable_prefix(
        source_jsonl=source_jsonl,
        stable_prefix=mid_dir,
        source_root=source_root,
        high_water_bytes=mid,
        captured_at_utc="2026-09-14T05:40:02Z",
        dataset_content_hash=dataset_hash,
    )
    print("D3b: mid-OK")
except Exception as exc:
    print(f"D3b: mid-ERROR {type(exc).__name__}: {exc}")

# D-3b: truncated short read (high water past EOF)
truncated_high_water = file_size + 64
print(f"D3b-truncated: file_size={file_size} high_water_bytes={truncated_high_water}")
try:
    capture_stable_prefix(
        source_jsonl=source_jsonl,
        stable_prefix=truncated_dir,
        source_root=source_root,
        high_water_bytes=truncated_high_water,
        captured_at_utc="2026-09-14T05:40:03Z",
        dataset_content_hash=dataset_hash,
    )
    print("D3b: truncated-OK")
except Exception as exc:
    print(f"D3b: truncated-ERROR {type(exc).__name__}: {exc}")
