"""D-7 PREVIEW on the candidate bytes: interrupted / inconsistent runs. Arms a-f mutate the global manifest of a good run
(unchanged from 09-14); NEW arm g runs a REAL interrupted backup (copy dies on the second file) and shows: no COMPLETE.json,
no RUN_MANIFEST.jsonl, restore.py rc 3 run_not_complete (check-only and restore), adapter refusal; NEW arm h writes a
hand-made, internally consistent completion pair into that interrupted run and shows it is still refused (Gemini F-01 arm);
NEW arm i: the restore CLI refuses --latest and a missing --run (usage error rc 2) and accepts an explicit run in check-only."""
import contextlib
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

LANE = Path(r"C:/tmp/P026_DRILLS_TA_PREVIEW_20260915")
_TMP = LANE / "tmp"
_TMP.mkdir(parents=True, exist_ok=True)
os.environ["TEMP"] = str(_TMP)
os.environ["TMP"] = str(_TMP)
os.environ["PYTHONUTF8"] = "1"
sys.path.insert(0, str((LANE / "wt").resolve()))
import p030_closed_partition_backup_adapter as adapter
from p030_closed_partition_backup_adapter import backup_stable_prefix, restore_verified_prefix

backup = adapter.backup
restore = adapter.restore
BASE = LANE / "fixtures"
base_backup = BASE / "backup_root"
config_base = json.loads((BASE / "config" / "intended_config_d4.json").read_text(encoding="utf-8"))
STORE = "p030_closed_partition"
run_id = [json.loads(l).get("run_id") for l in (base_backup / "manifest.jsonl").read_text(encoding="utf-8").splitlines() if json.loads(l).get("record") == "run_start"][-1]


def _cfg(name, root):
    cfg = BASE / "config" / f"intended_config_d7_{name}.json"
    payload = dict(config_base)
    payload["backup_root"] = str(root.resolve())
    cfg.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return cfg


def _restore_attempt(name, root, rid=None):
    rid = rid or run_id
    target = BASE / f"d7_target_{name}"
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    try:
        restore_verified_prefix(_cfg(name, root), run_id=rid, store_id=STORE, target=target)
        print(f"{name}: OK")
    except Exception as exc:
        print(f"{name}: ERROR {type(exc).__name__}: {exc}")
    written = sorted(p.relative_to(target).as_posix() for p in target.rglob("*") if p.is_file())
    print(f"{name}: target_written={written}")


def with_manifest(name, mutate):
    root = BASE / f"backup_root_d7_{name}"
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(base_backup, root)
    mpath = root / "manifest.jsonl"
    records = [json.loads(l) for l in mpath.read_text(encoding="utf-8").splitlines() if l.strip()]
    end_idx = next(i for i, r in enumerate(records) if r.get("run_id") == run_id and r.get("record") == "run_end")
    mutate(records, end_idx)
    mpath.write_text("\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in records) + "\n", encoding="utf-8")
    _restore_attempt(name, root)


# a) status not ok
with_manifest("status", lambda rs, i: rs[i].__setitem__("status", "partial"))


# b) errors non-empty
def _errors(rs, i):
    rs[i]["status"] = "ok"
    rs[i]["errors"] = ["manual failure"]


with_manifest("errors", _errors)


# c) files count mismatch
def _files(rs, i):
    rs[i]["files"] = len([r for r in rs if r.get("run_id") == run_id and r.get("record") == "file"]) + 1


with_manifest("files", _files)
# d) skipped record injected
with_manifest("skipped", lambda rs, i: rs.insert(i, {"record": "skipped", "run_id": run_id, "store_id": STORE, "class": "protected", "rel": "skipped.txt", "reason": "manual skip"}))
# e) extra file member
with_manifest("third", lambda rs, i: rs.insert(i, {"record": "file", "run_id": run_id, "store_id": STORE, "class": "protected", "src": "manual/src.bin", "rel": "extra.bin", "size": 11, "sha256": "00" * 32, "readback": "match", "copied_at": "2026-09-15T00:00:00Z"}))
# f) malformed JSONL line
root = BASE / "backup_root_d7_malformed"
if root.exists():
    shutil.rmtree(root)
shutil.copytree(base_backup, root)
(root / "manifest.jsonl").write_bytes((root / "manifest.jsonl").read_bytes() + b"{not-json\n")
_restore_attempt("malformed", root)

# ---- NEW g) a REAL interrupted backup on the candidate: the second file copy dies ----
iroot = BASE / "backup_root_d7_interrupted"
if iroot.exists():
    shutil.rmtree(iroot)
iroot.mkdir(parents=True)
icfg = _cfg("interrupted", iroot)
receipt = BASE / "contract_partition" / "stable_prefix" / "drill_3" / "_P030_STABLE_PREFIX.json"
real_copyfile = backup.shutil.copyfile
calls = {"n": 0}


def dying_copyfile(src, dst, *a, **kw):
    calls["n"] += 1
    if calls["n"] == 2:
        raise OSError("simulated interruption during the second file copy")
    return real_copyfile(src, dst, *a, **kw)


backup.shutil.copyfile = dying_copyfile
try:
    try:
        backup_stable_prefix(icfg, stable_receipt=receipt, store_id=STORE, source_root=BASE / "contract_partition")
        print("interrupted: backup_stable_prefix=OK (UNEXPECTED)")
    except Exception as exc:
        print(f"interrupted: backup_stable_prefix=ERROR {type(exc).__name__}: {exc}")
finally:
    backup.shutil.copyfile = real_copyfile
recs = [json.loads(l) for l in (iroot / "manifest.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
irun = [r["run_id"] for r in recs if r.get("record") == "run_start"][0]
ends = [r for r in recs if r.get("record") == "run_end" and r.get("run_id") == irun]
print(f"interrupted: run_id={irun} global_record_types={[r.get('record') for r in recs if r.get('run_id') == irun]}")
print(f"interrupted: global_run_end={json.dumps(ends[0], sort_keys=True) if ends else None}")
irun_dir = iroot / "runs" / irun
entries = sorted(str(p.relative_to(irun_dir)) for p in irun_dir.rglob("*")) if irun_dir.exists() else "ABSENT"
print(f"interrupted: run_dir_entries={entries}")
print(f"interrupted: complete_marker_exists={(irun_dir / 'COMPLETE.json').exists()} run_manifest_exists={(irun_dir / 'RUN_MANIFEST.jsonl').exists()}")
# restore.py itself (the tool, not the adapter): check-only then restore
for check_only in (True, False):
    tgt = BASE / "d7_target_interrupted_direct"
    if tgt.exists():
        shutil.rmtree(tgt)
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = restore.run_restore(icfg, run_id=irun, target=None if check_only else tgt, check_only=check_only)
    last = err.getvalue().strip().splitlines()[-1] if err.getvalue().strip() else ""
    print(f"interrupted: restore.run_restore check_only={check_only} rc={rc} stderr_last={last} target_exists={tgt.exists()}")
_restore_attempt("interrupted_adapter", iroot, rid=irun)

# ---- NEW h) hand-made completion pair on the interrupted run (Gemini F-01 arm of the repair) ----
irun_dir.mkdir(parents=True, exist_ok=True)
files = [r for r in recs if r.get("run_id") == irun and r.get("record") == "file"]
hdr = {"record": "run_manifest_header", "schema": "mtc.opsa_run_manifest/v1", "run_id": irun}
lines = [json.dumps(hdr, sort_keys=True)] + [json.dumps(r, ensure_ascii=False, sort_keys=True) for r in files]
rm_bytes = ("\n".join(lines) + "\n").encode("utf-8")
(irun_dir / "RUN_MANIFEST.jsonl").write_bytes(rm_bytes)
marker = {"schema": "mtc.opsa_run_complete/v1", "run_id": irun, "files": len(files), "run_manifest_sha256": hashlib.sha256(rm_bytes).hexdigest(), "status": "ok"}
(irun_dir / "COMPLETE.json").write_text(json.dumps(marker, sort_keys=True), encoding="utf-8")
binds = marker["run_manifest_sha256"] == hashlib.sha256((irun_dir / "RUN_MANIFEST.jsonl").read_bytes()).hexdigest()
print(f"handmade: pair_written files={len(files)} marker_binds={binds}")
tgt = BASE / "d7_target_handmade_direct"
if tgt.exists():
    shutil.rmtree(tgt)
out, err = io.StringIO(), io.StringIO()
with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
    rc = restore.run_restore(icfg, run_id=irun, target=tgt, check_only=False)
last = err.getvalue().strip().splitlines()[-1] if err.getvalue().strip() else ""
print(f"handmade: restore.run_restore rc={rc} stderr_last={last} target_exists={tgt.exists()}")
_restore_attempt("handmade_adapter", iroot, rid=irun)

# ---- NEW i) restore CLI surface: --latest gone; --run required; explicit run check-only works ----
py = sys.executable
rp = LANE / "wt" / "MTC_COMMAND_CENTER" / "tools" / "opsa" / "restore.py"
good_cfg = BASE / "config" / "intended_config_d4.json"
arms = (
    ("cli_latest", ["--config", str(good_cfg), "--latest", "--check-only"]),
    ("cli_no_run", ["--config", str(good_cfg), "--check-only"]),
    ("cli_latest_with_run", ["--config", str(good_cfg), "--run", run_id, "--latest", "--check-only"]),
    ("cli_explicit_check_only", ["--config", str(good_cfg), "--run", run_id, "--check-only"]),
)
for label, args in arms:
    p = subprocess.run([py, str(rp)] + args, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(LANE / "tmp"))
    so = (p.stdout.strip().splitlines() or [""])[-1][:200]
    se = (p.stderr.strip().splitlines() or [""])[-1][:200]
    print(f"{label}: rc={p.returncode} stdout_last={so} stderr_last={se}")
