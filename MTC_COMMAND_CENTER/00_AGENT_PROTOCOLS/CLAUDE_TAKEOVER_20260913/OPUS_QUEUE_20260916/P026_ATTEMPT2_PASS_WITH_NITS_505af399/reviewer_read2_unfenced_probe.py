"""For each branch the sweep found unfenced: build the state it guards, then show
(1) HEAD refuses it  -> the branch is LIVE and the state is REACHABLE, and
(2) with that single branch killed, the same state is ACCEPTED -> it is the SOLE guard."""
from __future__ import annotations

import hashlib
import io
import json
import contextlib
import importlib
import shutil
import sys
from pathlib import Path

SCR = Path(r"C:/tmp/OPUS_P026_SCRATCH")
HEAD = Path(r"C:/tmp/P026_REPAIR_20260915/MTC_COMMAND_CENTER/tools/opsa")
WORK = SCR / "read2_unfenced"

KILLS = {
    "G2 per-run manifest absent": ("opsa_common.py", "    if not manifest.is_file():"),
    "G3 marker not a JSON object": ("opsa_common.py", "    if not isinstance(payload, dict):"),
    "G4 marker schema": ("opsa_common.py", '    if payload.get("schema") != RUN_COMPLETE_SCHEMA:'),
    "R3 per-run malformed lines": ("restore.py",
                                   '    if any(r.get("record") == "_malformed" for r in run_records):'),
    "R4 per-run header": ("restore.py",
                          '    if header.get("record") != "run_manifest_header" or header.get("run_id") != run_id:'),
    "R7 run_end files == declared": ("restore.py", '    if end.get("files") != declared:'),
    "R8 per-record readback": ("restore.py",
                               '    if any(r.get("readback") != "match" for r in run_records if r.get("record") == "file"):'),
}


def build(kill: str | None) -> Path:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    for p in HEAD.iterdir():
        if p.is_file():
            shutil.copyfile(p, WORK / p.name)
    if kill:
        fname, prefix = KILLS[kill]
        t = WORK / fname
        text = t.read_text(encoding="utf-8")
        assert text.count(prefix) == 1
        indent = prefix[: len(prefix) - len(prefix.lstrip())]
        t.write_text(text.replace(prefix, f"{indent}if False:  # killed"), encoding="utf-8")
    return WORK


def load():
    for n in ("backup", "restore", "opsa_common"):
        sys.modules.pop(n, None)
    sys.path = [p for p in sys.path if p != str(WORK)]
    sys.path.insert(0, str(WORK))
    return importlib.import_module("backup"), importlib.import_module("restore")


def quiet(fn, *a, **kw):
    o, e = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(o), contextlib.redirect_stderr(e):
        rc = fn(*a, **kw)
    return rc, o.getvalue(), e.getvalue()


def scenario(root: Path, mutate) -> tuple[int, str]:
    """Fresh backup, then apply `mutate(run_dir)`, then restore --check-only."""
    backup, restore = load()
    if root.exists():
        shutil.rmtree(root)
    store = root / "store"
    store.mkdir(parents=True)
    (store / "a.jsonl").write_bytes(b'{"x":1}\n')
    (store / "b.bin").write_bytes(bytes(range(64)))
    broot = root / "backups"
    cfg = root / "cfg.json"
    cfg.write_text(json.dumps({"schema": "mtc.opsa_backup_config/v1",
                               "backup_root": str(broot),
                               "stores": [{"id": "s1", "path": str(store),
                                           "class": "protected"}]}), encoding="utf-8")
    assert quiet(backup.run_backup, cfg)[0] == 0
    rid = [json.loads(l)["run_id"] for l in (broot / "manifest.jsonl").read_text(
        encoding="utf-8").splitlines() if json.loads(l).get("record") == "run_start"][0]
    mutate(broot / "runs" / rid)
    rc, _o, e = quiet(restore.run_restore, cfg, run_id=rid, target=None, check_only=True)
    last = e.strip().splitlines()[-1] if e.strip() else ""
    try:
        detail = json.loads(last).get("detail", last)
    except Exception:  # noqa: BLE001
        detail = last
    return rc, detail[:130]


def rebind(rd: Path, data: bytes, **marker_over) -> None:
    (rd / "RUN_MANIFEST.jsonl").write_bytes(data)
    m = json.loads((rd / "COMPLETE.json").read_text(encoding="utf-8"))
    m["run_manifest_sha256"] = hashlib.sha256(data).hexdigest()
    m.update(marker_over)
    (rd / "COMPLETE.json").write_text(json.dumps(m, sort_keys=True), encoding="utf-8")


def m_g2(rd: Path):
    (rd / "RUN_MANIFEST.jsonl").rename(rd / "RUN_MANIFEST.jsonl.moved")


def m_g3(rd: Path):
    (rd / "COMPLETE.json").write_text("[1, 2, 3]", encoding="utf-8")


def m_g4(rd: Path):
    m = json.loads((rd / "COMPLETE.json").read_text(encoding="utf-8"))
    m["schema"] = "mtc.opsa_run_complete/v99"
    (rd / "COMPLETE.json").write_text(json.dumps(m, sort_keys=True), encoding="utf-8")


def m_r3(rd: Path):
    data = (rd / "RUN_MANIFEST.jsonl").read_bytes() + b"{ this is not json\n"
    rebind(rd, data)


def m_r4(rd: Path):
    lines = (rd / "RUN_MANIFEST.jsonl").read_text(encoding="utf-8").splitlines()
    data = ("\n".join(lines[1:]) + "\n").encode("utf-8")   # header dropped
    rebind(rd, data)


def m_r7(rd: Path):
    m = json.loads((rd / "COMPLETE.json").read_text(encoding="utf-8"))
    m["files"] = 99          # declared != per-run count AND != run_end files
    (rd / "COMPLETE.json").write_text(json.dumps(m, sort_keys=True), encoding="utf-8")


def m_r8(rd: Path):
    recs = [json.loads(l) for l in (rd / "RUN_MANIFEST.jsonl").read_text(
        encoding="utf-8").splitlines() if l.strip()]
    for r in recs:
        if r.get("record") == "file":
            r["readback"] = "MISMATCH"
    data = ("\n".join(json.dumps(r, sort_keys=True) for r in recs) + "\n").encode("utf-8")
    rebind(rd, data)


CASES = [("G2 per-run manifest absent", m_g2), ("G3 marker not a JSON object", m_g3),
         ("G4 marker schema", m_g4), ("R3 per-run malformed lines", m_r3),
         ("R4 per-run header", m_r4), ("R7 run_end files == declared", m_r7),
         ("R8 per-record readback", m_r8)]


def main(_argv):
    for label, mut in CASES:
        build(None)
        try:
            rc_head, d_head = scenario(SCR / "read2_unf_work", mut)
            head = f"rc={rc_head} {d_head!r}"
        except Exception as exc:  # noqa: BLE001
            head = f"UNCAUGHT {type(exc).__name__}: {str(exc)[:80]}"
        build(label)
        try:
            rc_k, d_k = scenario(SCR / "read2_unf_work", mut)
            killed = f"rc={rc_k} {d_k!r}"
        except Exception as exc:  # noqa: BLE001
            killed = f"UNCAUGHT {type(exc).__name__}: {str(exc)[:80]}"
        print(f"{label}\n    HEAD   : {head}\n    KILLED : {killed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
