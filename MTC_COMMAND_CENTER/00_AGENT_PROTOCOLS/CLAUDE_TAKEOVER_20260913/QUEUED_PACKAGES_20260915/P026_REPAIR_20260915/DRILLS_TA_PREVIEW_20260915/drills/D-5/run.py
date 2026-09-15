"""D-5 PREVIEW on the candidate bytes: isolated explicit-run restore through the adapter; the isolated root must carry the run's completion pair."""
import hashlib, json, os, shutil, sys
from pathlib import Path
LANE = Path(r"C:/tmp/P026_DRILLS_TA_PREVIEW_20260915")
_TMP = LANE / "tmp"; _TMP.mkdir(parents=True, exist_ok=True)
os.environ["TEMP"] = str(_TMP); os.environ["TMP"] = str(_TMP); os.environ["PYTHONUTF8"] = "1"
sys.path.insert(0, str((LANE / "wt").resolve()))
from p030_closed_partition_backup_adapter import restore_verified_prefix
BASE = LANE / "fixtures"
config = BASE / "config" / "intended_config_d4.json"
manifest = BASE / "backup_root" / "manifest.jsonl"
run_ids = [json.loads(l).get("run_id") for l in manifest.read_text(encoding="utf-8").splitlines() if json.loads(l).get("record") == "run_start"]
print(f"run_ids_in_manifest={run_ids}")
run_id = run_ids[-1]
target = BASE / "d5_restore" / "target"
if target.exists(): shutil.rmtree(target)
target.mkdir(parents=True)
receipt_path = restore_verified_prefix(config, run_id=run_id, store_id="p030_closed_partition", target=target)
print(f"run_id={run_id}")
print(f"receipt={receipt_path}")
print(f"receipt_exists={receipt_path.exists()}")
print(f"target_entries={sorted(str(p.relative_to(target)) for p in target.rglob('*'))}")
receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
print(f"receipt_identity run_id={receipt.get('run_id')} store_id={receipt.get('store_id')} restored_prefix={receipt.get('restored_prefix')}")
for f in ("high_water_bytes", "record_count", "last_observation_id", "prefix_sha256", "captured_at_utc", "dataset_content_hash"):
    print(f"receipt_field {f}={receipt.get(f)}")
restored_prefix = Path(receipt["restored_prefix"])
for path in sorted(restored_prefix.rglob("*")):
    rel = path.relative_to(restored_prefix).as_posix()
    print(f"type {rel} is_symlink={path.is_symlink()} is_junction={path.is_junction()} is_file={path.is_file()} is_dir={path.is_dir()}")
archived = BASE / "backup_root" / "runs" / run_id / "p030_closed_partition"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
print(f"restored_bytes_equal_archived receipt={sha(restored_prefix / '_P030_STABLE_PREFIX.json') == sha(archived / '_P030_STABLE_PREFIX.json')} snapshot={sha(restored_prefix / 'source.jsonl') == sha(archived / 'source.jsonl')}")
# NEW: the completion pair the isolated restore carried = the real run's pair (restore.py printed completion_marker=verified + run_manifest_sha256 above)
real_rm_sha = sha(BASE / "backup_root" / "runs" / run_id / "RUN_MANIFEST.jsonl")
print(f"real_run_manifest_sha256={real_rm_sha}")
print(f"target_has_no_completion_pair={not (target / 'COMPLETE.json').exists() and not (target / 'RUN_MANIFEST.jsonl').exists()}")
