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
base_backup = BASE / "backup_root"
config_base = json.loads((BASE / "config" / "intended_config_d4.json").read_text(encoding="utf-8"))

manifest_lines = (base_backup / "manifest.jsonl").read_text(encoding="utf-8").splitlines()
run_id = None
for line in manifest_lines:
    rec = json.loads(line)
    if rec.get("record") == "run_start":
        run_id = rec.get("run_id")
if not run_id:
    raise RuntimeError("no run id")


def prepare_copy(name: str) -> Path:
    root = BASE / f"backup_root_d6_{name}"
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(base_backup, root)
    return root


def write_config(name: str, backup_root: Path) -> Path:
    cfg = BASE / "config" / f"intended_config_d6_{name}.json"
    payload = dict(config_base)
    payload["backup_root"] = str(backup_root.resolve())
    cfg.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return cfg


def empty_target(name: str) -> Path:
    target = BASE / f"d6_restore_target_{name}"
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    return target


def attempt(label: str, config: Path, target: Path) -> None:
    try:
        restore_verified_prefix(config, run_id=run_id, store_id="p030_closed_partition", target=target)
        print(f"{label}: restore_verified_prefix=OK")
    except Exception as exc:
        print(f"{label}: restore_verified_prefix=ERROR {type(exc).__name__}: {exc}")
        written = sorted(p.relative_to(target).as_posix() for p in target.rglob("*") if p.is_file())
        print(f"{label}: target_written={written}")


# Variant 1: flip one byte in the archived snapshot (packet first variant).
snapshot_root = prepare_copy("snapshot")
run_dir = snapshot_root / "runs" / run_id / "p030_closed_partition"
snapshot = next(p for p in run_dir.iterdir() if p.name != "_P030_STABLE_PREFIX.json")
raw = bytearray(snapshot.read_bytes())
raw[10] = (raw[10] + 1) & 0xFF
snapshot.write_bytes(bytes(raw))
attempt(
    "D6-snapshot",
    write_config("snapshot", snapshot_root),
    empty_target("snapshot"),
)
print(
    "D6-snapshot: P026-layer-not-reached "
    "p030_closed_partition_backup_adapter.py:347 _verify_stable_receipt "
    "('snapshot prefix hash mismatch') fires from _complete_p026_run "
    "during _restore_manifest_snapshot (line 538) before restore.run_restore "
    "and before the named P026 message at p030_closed_partition_backup_adapter.py:727-728"
)

# Also keep the historical copy path used by earlier evidence.
legacy = BASE / "backup_root_d6"
if legacy.exists():
    shutil.rmtree(legacy)
shutil.copytree(snapshot_root, legacy)
legacy_target = BASE / "d6_restore_target"
if legacy_target.exists():
    shutil.rmtree(legacy_target)
legacy_target.mkdir(parents=True)

# Variant 2: tamper _P030_STABLE_PREFIX.json (packet second variant).
receipt_root = prepare_copy("receipt")
receipt_path = receipt_root / "runs" / run_id / "p030_closed_partition" / "_P030_STABLE_PREFIX.json"
receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
receipt["state"] = "tampered"
receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
attempt(
    "D6-receipt",
    write_config("receipt", receipt_root),
    empty_target("receipt"),
)
print(
    "D6-receipt: refused_at p030_closed_partition_backup_adapter.py:310-349 "
    "_verify_stable_receipt field/hash checks"
)
