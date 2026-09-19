"""Branch-kill sweep: disable each refusal in the completion gate one at a time and record
which tests (if any) go RED. A branch no test kills is an unfenced refusal."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

SCR = Path(r"C:/tmp/OPUS_P026_SCRATCH")
HEAD = Path(r"C:/tmp/P026_REPAIR_20260915/MTC_COMMAND_CENTER/tools/opsa")
WORK = SCR / "read2_sweep"
PY = r"C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe"

# (label, file, exact source line prefix to neutralise)
BRANCHES = [
    ("G1 marker absent", "opsa_common.py", "    if not marker.is_file():"),
    ("G2 per-run manifest absent", "opsa_common.py", "    if not manifest.is_file():"),
    ("G3 marker not a JSON object", "opsa_common.py", "    if not isinstance(payload, dict):"),
    ("G4 marker schema", "opsa_common.py", "    if payload.get(\"schema\") != RUN_COMPLETE_SCHEMA:"),
    ("G5 marker names another run", "opsa_common.py", "    if payload.get(\"run_id\") != run_id:"),
    ("G6 manifest digest binding", "opsa_common.py",
     "    if not isinstance(recorded, str) or recorded != actual:"),
    ("R1 exactly one run_end", "restore.py", "    if len(ends) != 1:"),
    ("R2 run_end ok / no errors", "restore.py",
     "    if end.get(\"status\") != \"ok\" or end.get(\"errors\") != []:"),
    ("R3 per-run malformed lines", "restore.py",
     "    if any(r.get(\"record\") == \"_malformed\" for r in run_records):"),
    ("R4 per-run header", "restore.py",
     "    if header.get(\"record\") != \"run_manifest_header\" or header.get(\"run_id\") != run_id:"),
    ("R5 per-run vs global file records", "restore.py", "    if per_run_files != global_files:"),
    ("R6 declared files is an int == count", "restore.py",
     "    if not isinstance(declared, int) or isinstance(declared, bool) or declared != len(per_run_files):"),
    ("R7 run_end files == declared", "restore.py", "    if end.get(\"files\") != declared:"),
    ("R8 per-record readback", "restore.py",
     "    if any(r.get(\"readback\") != \"match\" for r in run_records if r.get(\"record\") == \"file\"):"),
    ("R9 NIT-1 marker readback claim", "restore.py",
     "    if marker.get(\"readback\") != \"all_match\":"),
    ("R10 NIT-1 marker run_manifest claim", "restore.py",
     "    if marker.get(\"run_manifest\") != RUN_MANIFEST_NAME:"),
]


def build() -> None:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    for p in HEAD.iterdir():
        if p.is_file():
            shutil.copyfile(p, WORK / p.name)


def neutralise(fname: str, line_prefix: str) -> None:
    target = WORK / fname
    text = target.read_text(encoding="utf-8")
    assert text.count(line_prefix) == 1, f"anchor x{text.count(line_prefix)}: {line_prefix!r}"
    indent = line_prefix[: len(line_prefix) - len(line_prefix.lstrip())]
    killed = f"{indent}if False:  # branch killed"
    target.write_text(text.replace(line_prefix, killed), encoding="utf-8")


def run() -> tuple[int, list[str]]:
    env = {"PYTHONDONTWRITEBYTECODE": "1", "SystemRoot": r"C:\Windows",
           "TEMP": r"C:\tmp\OPUS_P026_SCRATCH\read2_tmp", "TMP": r"C:\tmp\OPUS_P026_SCRATCH\read2_tmp",
           "PATH": r"C:\Windows\system32;C:\Windows"}
    p = subprocess.run([PY, "-B", "-m", "unittest", "test_opsa"], cwd=str(WORK),
                       capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    out = p.stdout + p.stderr
    names = sorted({ln.split("(")[0].replace("FAIL: ", "").replace("ERROR: ", "").strip()
                    for ln in out.splitlines() if ln.startswith(("FAIL: ", "ERROR: "))})
    return p.returncode, names


def main(_argv):
    unfenced = []
    for label, fname, prefix in BRANCHES:
        build()
        neutralise(fname, prefix)
        rc, names = run()
        status = "KILLED by" if rc != 0 else "*** NO TEST KILLS THIS BRANCH ***"
        print(f"{label:<42} {status} {', '.join(names) if names else ''}")
        if rc == 0:
            unfenced.append(label)
    print("\nUNFENCED BRANCHES:", unfenced or "none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
