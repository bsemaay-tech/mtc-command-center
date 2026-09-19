"""Item 3 (D026 evidence): run the CANDIDATE test_opsa.py against PRE-FIX module sets.

Arm A - pre-fix backup.py + restore.py, candidate opsa_common.py + test_opsa.py
        (the Lead's LEAD_RED_ARMS_PREFIX_BACKUP_RESTORE arm; the candidate opsa_common is
        needed because the suite imports RUN_MANIFEST_NAME/COMPLETE_MARKER_NAME/write_once_bytes).
Arm B - pre-fix opsa_common.py as well (expect a collection-level ImportError; shows WHY arm A
        keeps the new common module).
Arm C - slice-1 opsa_common.py (6ac9cfb7) with everything else from HEAD - the reserved-store-id
        fence added in slice 2.
Arm D - slice-2 backup.py + restore.py (8d4056c5) with the HEAD suite - the Gemini F-01 fence.
Arm E - e114ed31 restore.py + backup.py with the HEAD suite - the NIT-1 fence (this slice).
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

SCR = Path(r"C:/tmp/OPUS_P026_SCRATCH")
HEAD = Path(r"C:/tmp/P026_REPAIR_20260915/MTC_COMMAND_CENTER/tools/opsa")
PY = r"C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe"
REPO = r"C:/tmp/P026_REPAIR_20260915"

ARMS = {
    "A_prefix_backup_restore": {"backup.py": "fcac0ac6", "restore.py": "fcac0ac6"},
    "B_prefix_all_three": {"backup.py": "fcac0ac6", "restore.py": "fcac0ac6",
                           "opsa_common.py": "fcac0ac6"},
    "C_slice1_common": {"opsa_common.py": "6ac9cfb7"},
    "D_slice2_backup_restore": {"backup.py": "8d4056c5", "restore.py": "8d4056c5"},
    "E_e114ed31_backup_restore": {"backup.py": "e114ed31", "restore.py": "e114ed31"},
}


def blob(rev: str, name: str) -> bytes:
    p = subprocess.run(["git", "-c", "safe.directory=*", "-C", REPO, "show",
                        f"{rev}:MTC_COMMAND_CENTER/tools/opsa/{name}"], capture_output=True)
    if p.returncode:
        raise SystemExit(f"git show {rev}:{name} failed: {p.stderr!r}")
    return p.stdout


def build(arm: str, overrides: dict) -> Path:
    work = SCR / f"red2_{arm}"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    for p in HEAD.iterdir():
        if p.is_file():
            shutil.copyfile(p, work / p.name)
    for name, rev in overrides.items():
        (work / name).write_bytes(blob(rev, name))
    return work


def main(argv):
    names = list(ARMS) if not argv else argv
    for arm in names:
        work = build(arm, ARMS[arm])
        env = {"PYTHONDONTWRITEBYTECODE": "1", "SystemRoot": r"C:\Windows",
               "TEMP": r"C:\tmp\OPUS_P026_SCRATCH\read2_tmp",
               "TMP": r"C:\tmp\OPUS_P026_SCRATCH\read2_tmp",
               "PATH": r"C:\Windows\system32;C:\Windows"}
        proc = subprocess.run([PY, "-B", "-m", "unittest", "test_opsa", "-v"], cwd=str(work),
                              capture_output=True, text=True, encoding="utf-8", errors="replace",
                              env=env)
        out = proc.stdout + proc.stderr
        (SCR / f"read2_red_{arm}.txt").write_text(out, encoding="utf-8")
        head = [ln for ln in out.splitlines()
                if ln.startswith(("FAIL:", "ERROR:", "Ran ", "OK", "FAILED"))]
        print(f"\n### ARM {arm}  overrides={ARMS[arm]}  rc={proc.returncode}")
        print("\n".join(head) or out.strip().splitlines()[-3:])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
