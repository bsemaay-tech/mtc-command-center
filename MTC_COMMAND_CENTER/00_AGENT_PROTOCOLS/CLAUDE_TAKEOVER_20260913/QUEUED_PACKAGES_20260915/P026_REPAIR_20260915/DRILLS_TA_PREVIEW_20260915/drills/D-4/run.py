"""D-4 PREVIEW on the candidate bytes: backup of the stable prefix through the adapter; manifests + completion pair."""
import hashlib, json, os, sys
from pathlib import Path
LANE = Path(r"C:/tmp/P026_DRILLS_TA_PREVIEW_20260915")
_TMP = LANE / "tmp"; _TMP.mkdir(parents=True, exist_ok=True)
os.environ["TEMP"] = str(_TMP); os.environ["TMP"] = str(_TMP); os.environ["PYTHONUTF8"] = "1"
sys.path.insert(0, str((LANE / "wt").resolve()))
from p030_closed_partition_backup_adapter import backup_stable_prefix
BASE = LANE / "fixtures"
config = BASE / "config" / "intended_config_d4.json"
receipt = BASE / "contract_partition" / "stable_prefix" / "drill_3" / "_P030_STABLE_PREFIX.json"
source_root = BASE / "contract_partition"
backup_root = BASE / "backup_root"
snapshot = receipt.parent / "source.jsonl"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
before_receipt, before_snapshot = sha(receipt), sha(snapshot)
print(f"byte_compare_before receipt_sha256={before_receipt} snapshot_sha256={before_snapshot}")
run_id = backup_stable_prefix(config, stable_receipt=receipt, store_id="p030_closed_partition", source_root=source_root)
print(f"run_id={run_id}")
print(f"byte_compare_after receipt_equal={sha(receipt) == before_receipt} snapshot_equal={sha(snapshot) == before_snapshot}")
run_dir = backup_root / "runs" / run_id
archived = run_dir / "p030_closed_partition"
print(f"byte_compare_archived receipt_equal={sha(archived / '_P030_STABLE_PREFIX.json') == before_receipt} snapshot_equal={sha(archived / 'source.jsonl') == before_snapshot}")
manifest_path = backup_root / "manifest.jsonl"
print(f"manifest_exists={manifest_path.exists()}")
records = [json.loads(l) for l in manifest_path.read_text(encoding="utf-8").splitlines() if l.strip()]
run_records = [r for r in records if r.get("run_id") == run_id]
print(f"manifest_record_types={[r.get('record') for r in run_records]}")
for r in run_records:
    if r.get("record") == "file":
        print(f"manifest_file rel={r.get('rel')} readback={r.get('readback')} size={r.get('size')} sha256={r.get('sha256')}")
end = [r for r in run_records if r.get("record") == "run_end"][-1]
print(f"manifest_run_end status={end.get('status')} errors={end.get('errors')} files={end.get('files')} bytes={end.get('bytes')}")
print(f"member_set={sorted(r.get('rel') for r in run_records if r.get('record') == 'file')}")
# --- NEW on the candidate: the completion pair inside runs/<run_id>/ ---
marker_path = run_dir / "COMPLETE.json"; rm_path = run_dir / "RUN_MANIFEST.jsonl"
print(f"run_dir_entries={sorted(p.name for p in run_dir.iterdir())}")
print(f"complete_marker_exists={marker_path.exists()} run_manifest_exists={rm_path.exists()}")
marker = json.loads(marker_path.read_text(encoding="utf-8"))
print(f"complete_marker_keys={sorted(marker)}")
print(f"complete_marker schema={marker.get('schema')} run_id_match={marker.get('run_id') == run_id} files={marker.get('files')} bytes={marker.get('bytes')} status={marker.get('status')} completed_at={marker.get('completed_at')}")
rm_sha = sha(rm_path)
print(f"run_manifest_sha256_binds={marker.get('run_manifest_sha256') == rm_sha} run_manifest_sha256={rm_sha}")
rm_records = [json.loads(l) for l in rm_path.read_text(encoding="utf-8").splitlines() if l.strip()]
print(f"run_manifest_record_types={[r.get('record') for r in rm_records]}")
hdr = rm_records[0]
print(f"run_manifest_header schema={hdr.get('schema')} run_id_match={hdr.get('run_id') == run_id}")
key = lambda r: (r.get("store_id"), r.get("rel"), r.get("sha256"), r.get("size"))
per_run = sorted(key(r) for r in rm_records if r.get("record") == "file")
glob = sorted(key(r) for r in run_records if r.get("record") == "file")
print(f"per_run_file_records_equal_global={per_run == glob} count={len(per_run)}")
# ordering evidence: marker written before the global run_end (Gemini F-03 of the repair): compare timestamps
print(f"marker_completed_at={marker.get('completed_at')} global_run_end_finished_at={end.get('finished_at')}")
