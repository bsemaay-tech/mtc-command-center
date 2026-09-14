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

manifest = (base_backup / "manifest.jsonl").read_text(encoding="utf-8").splitlines()
run_id = None
for raw in manifest:
    rec = json.loads(raw)
    if rec.get("record") == "run_start":
        run_id = rec.get("run_id")
if not run_id:
    raise RuntimeError("no run id")


def with_manifest(mutator_name: str, mutate) -> None:
    root = BASE / f"backup_root_d7_{mutator_name}"
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(base_backup, root)
    mpath = root / "manifest.jsonl"
    records = [json.loads(line) for line in mpath.read_text(encoding="utf-8").splitlines()]
    run_records = [
        i
        for i, r in enumerate(records)
        if r.get("run_id") == run_id and r.get("record") in {"run_start", "file", "dir", "run_end", "skipped"}
    ]
    target_end = None
    for idx in run_records:
        if records[idx].get("record") == "run_end":
            target_end = idx
            break
    if target_end is None:
        raise RuntimeError("run_end missing")
    mutate(records, target_end)
    mpath.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in records) + "\n",
        encoding="utf-8",
    )
    _restore_attempt(mutator_name, root)


def _restore_attempt(mutator_name: str, root: Path) -> None:
    cfg = BASE / f"config/intended_config_d7_{mutator_name}.json"
    cfg_payload = dict(config_base)
    cfg_payload["backup_root"] = str(root.resolve())
    cfg.write_text(json.dumps(cfg_payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")

    target = BASE / f"d7_target_{mutator_name}"
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    try:
        restore_verified_prefix(cfg, run_id=run_id, store_id="p030_closed_partition", target=target)
        print(f"{mutator_name}: OK")
    except Exception as exc:
        print(f"{mutator_name}: ERROR {type(exc).__name__}: {exc}")


# a) status not ok
with_manifest("status", lambda records, run_end_idx: records[run_end_idx].__setitem__("status", "partial"))


# b) errors non-empty
def set_error_non_empty(records, run_end_idx):
    records[run_end_idx]["status"] = "ok"
    records[run_end_idx]["errors"] = ["manual failure"]


with_manifest("errors", set_error_non_empty)


# c) files mismatch
def files_mismatch(records, run_end_idx):
    run_records = [r for r in records if r.get("run_id") == run_id and r.get("record") == "file"]
    records[run_end_idx]["status"] = "ok"
    records[run_end_idx]["errors"] = []
    records[run_end_idx]["files"] = len(run_records) + 1


with_manifest("files", files_mismatch)


# d) skipped record injected
def add_skipped(records, run_end_idx):
    insert = {
        "record": "skipped",
        "run_id": run_id,
        "store_id": "p030_closed_partition",
        "class": "protected",
        "rel": "skipped.txt",
        "reason": "manual skip",
    }
    records.insert(run_end_idx, insert)


with_manifest("skipped", add_skipped)


# e) extra file member
def add_third_file(records, run_end_idx):
    records.insert(
        run_end_idx,
        {
            "record": "file",
            "run_id": run_id,
            "store_id": "p030_closed_partition",
            "class": "protected",
            "src": "manual/src.bin",
            "rel": "extra.bin",
            "size": 11,
            "sha256": "00" * 32,
            "readback": "match",
            "copied_at": "2026-09-14T00:00:00Z",
        },
    )


with_manifest("third", add_third_file)


# f) malformed JSONL line — refuses at _decode_strict_jsonl (adapter :99-120)
malformed_root = BASE / "backup_root_d7_malformed"
if malformed_root.exists():
    shutil.rmtree(malformed_root)
shutil.copytree(base_backup, malformed_root)
mpath = malformed_root / "manifest.jsonl"
mpath.write_bytes(mpath.read_bytes() + b"{not-json\n")
_restore_attempt("malformed", malformed_root)
