"""D-6 PREVIEW on the candidate bytes: tamper arms. (1) snapshot byte flip, (2) receipt tamper (unchanged arms);
NEW (3) COMPLETE.json field tamper, (4) RUN_MANIFEST.jsonl byte tamper, (5) forged second run_end in the global manifest,
(6) COMPLETE.json deleted, (7) hand-made pair with a re-hashed marker over a forged per-run record. Every arm must leave the target empty."""
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

LANE = Path(r"C:/tmp/P026_DRILLS_TA_PREVIEW_20260915")
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
run_id = [json.loads(l).get("run_id") for l in (base_backup / "manifest.jsonl").read_text(encoding="utf-8").splitlines() if json.loads(l).get("record") == "run_start"][-1]
STORE = "p030_closed_partition"


def prepare_copy(name):
    root = BASE / f"backup_root_d6_{name}"
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(base_backup, root)
    return root


def write_config(name, backup_root):
    cfg = BASE / "config" / f"intended_config_d6_{name}.json"
    payload = dict(config_base)
    payload["backup_root"] = str(backup_root.resolve())
    cfg.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return cfg


def empty_target(name):
    t = BASE / f"d6_restore_target_{name}"
    if t.exists():
        shutil.rmtree(t)
    t.mkdir(parents=True)
    return t


def attempt(label, root):
    target = empty_target(label)
    try:
        restore_verified_prefix(write_config(label, root), run_id=run_id, store_id=STORE, target=target)
        print(f"{label}: restore_verified_prefix=OK")
    except Exception as exc:
        print(f"{label}: restore_verified_prefix=ERROR {type(exc).__name__}: {exc}")
    written = sorted(p.relative_to(target).as_posix() for p in target.rglob("*") if p.is_file())
    print(f"{label}: target_written={written}")


# (1) snapshot byte flip in the archived snapshot
root = prepare_copy("snapshot")
snap = root / "runs" / run_id / STORE / "source.jsonl"
raw = bytearray(snap.read_bytes())
raw[10] = (raw[10] + 1) & 0xFF
snap.write_bytes(bytes(raw))
attempt("D6-snapshot", root)

# (2) receipt tamper
root = prepare_copy("receipt")
rp = root / "runs" / run_id / STORE / "_P030_STABLE_PREFIX.json"
rec = json.loads(rp.read_text(encoding="utf-8"))
rec["state"] = "tampered"
rp.write_text(json.dumps(rec, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
attempt("D6-receipt", root)

# (3) NEW marker field tamper: files 2 -> 3 (global manifest untouched, per-run manifest untouched, digest still binds)
root = prepare_copy("marker_files")
mp = root / "runs" / run_id / "COMPLETE.json"
m = json.loads(mp.read_text(encoding="utf-8"))
m["files"] = 3
mp.write_text(json.dumps(m, sort_keys=True), encoding="utf-8")
attempt("D6-marker-files", root)

# (4) NEW per-run manifest byte tamper (one byte appended) -> marker digest no longer binds
root = prepare_copy("run_manifest")
rmp = root / "runs" / run_id / "RUN_MANIFEST.jsonl"
rmp.write_bytes(rmp.read_bytes() + b"\n")
attempt("D6-run-manifest-bytes", root)

# (5) NEW forged second run_end appended to the global manifest
root = prepare_copy("forged_run_end")
gm = root / "manifest.jsonl"
records = [json.loads(l) for l in gm.read_text(encoding="utf-8").splitlines() if l.strip()]
end = next(r for r in records if r.get("record") == "run_end" and r.get("run_id") == run_id)
records.append(dict(end))
gm.write_text("\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in records) + "\n", encoding="utf-8")
attempt("D6-forged-second-run-end", root)

# (6) NEW COMPLETE.json deleted (RUN_MANIFEST.jsonl kept)
root = prepare_copy("marker_deleted")
(root / "runs" / run_id / "COMPLETE.json").unlink()
attempt("D6-marker-deleted", root)

# (7) NEW forged per-run file record with the marker re-hashed to match (candidate test arm (d))
root = prepare_copy("forged_pair")
rmp = root / "runs" / run_id / "RUN_MANIFEST.jsonl"
mp = root / "runs" / run_id / "COMPLETE.json"
lines = rmp.read_text(encoding="utf-8").splitlines()
r = json.loads(lines[-1])
r["sha256"] = "0" * 64
lines[-1] = json.dumps(r, ensure_ascii=False, sort_keys=True)
forged = ("\n".join(lines) + "\n").encode("utf-8")
rmp.write_bytes(forged)
m = json.loads(mp.read_text(encoding="utf-8"))
m["run_manifest_sha256"] = hashlib.sha256(forged).hexdigest()
mp.write_text(json.dumps(m, sort_keys=True), encoding="utf-8")
attempt("D6-forged-pair-rehashed", root)
