"""Opus read-2 mutant driver: apply one textual mutation to a scratch copy of tools/opsa,
run the suite, restore the pristine bytes. Read-only w.r.t. the worktree."""
from __future__ import annotations
import shutil
import subprocess
import sys
from pathlib import Path

SCRATCH = Path(r"C:/tmp/OPUS_P026_SCRATCH/read2_opsa")
PRISTINE = Path(r"C:/tmp/OPUS_P026_SCRATCH/read2_pristine")
PY = r"C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe"

MUTANTS = {
    # (a1) NIT-1 readback claim check disabled
    "a1_readback_unchecked": ("restore.py",
        'if marker.get("readback") != "all_match":',
        'if False and marker.get("readback") != "all_match":'),
    # (a2) NIT-1 run_manifest claim check disabled
    "a2_run_manifest_unchecked": ("restore.py",
        'if marker.get("run_manifest") != RUN_MANIFEST_NAME:',
        'if False and marker.get("run_manifest") != RUN_MANIFEST_NAME:'),
    # (a3) both NIT-1 checks disabled at once
    "a3_both_unchecked": ("restore.py", None, None),
    # (e) NIT-5: reinstate the removed condition, inverted, to prove it is dead
    "e_nit5_status_inverted": ("backup.py",
        'return RC_OK if not errors else RC_ERROR  # status is derived from errors alone (NIT-5)',
        'return RC_OK if not errors and status != "ok" else RC_ERROR  # NIT-5 deadness probe'),
    # control: the gate itself removed -> many tests must fail
    "ctl_gate_removed": ("restore.py",
        "        marker = verify_completion_evidence(run_dir, resolved, records)",
        "        marker = {}  # gate bypassed (control mutant)"),
}


def restore_pristine() -> None:
    for name in ("restore.py", "backup.py", "opsa_common.py", "test_opsa.py"):
        shutil.copyfile(PRISTINE / name, SCRATCH / name)


def apply(name: str) -> None:
    fname, old, new = MUTANTS[name]
    if name == "a3_both_unchecked":
        target = SCRATCH / "restore.py"
        text = target.read_text(encoding="utf-8")
        for key in ("a1_readback_unchecked", "a2_run_manifest_unchecked"):
            _, o, n = MUTANTS[key]
            assert text.count(o) == 1, (key, text.count(o))
            text = text.replace(o, n)
        target.write_text(text, encoding="utf-8")
        return
    target = SCRATCH / fname
    text = target.read_text(encoding="utf-8")
    assert text.count(old) == 1, f"anchor count {text.count(old)} for {name}"
    target.write_text(text.replace(old, new), encoding="utf-8")


def run_suite() -> tuple[int, str]:
    proc = subprocess.run([PY, "-B", "test_opsa.py", "-v"], cwd=str(SCRATCH),
                          capture_output=True, text=True, encoding="utf-8", errors="replace")
    return proc.returncode, proc.stdout + proc.stderr


def main(argv: list[str]) -> int:
    if not PRISTINE.exists():
        PRISTINE.mkdir(parents=True)
        for name in ("restore.py", "backup.py", "opsa_common.py", "test_opsa.py"):
            shutil.copyfile(SCRATCH / name, PRISTINE / name)
        print("pristine snapshot taken")
    name = argv[0]
    restore_pristine()
    if name != "baseline":
        apply(name)
    rc, out = run_suite()
    restore_pristine()
    tail = [ln for ln in out.splitlines()
            if ln.startswith(("FAIL:", "ERROR:", "Ran ", "OK", "FAILED"))]
    print(f"### mutant={name} rc={rc}")
    print("\n".join(tail))
    Path(rf"C:/tmp/OPUS_P026_SCRATCH/read2_mut_{name}.txt").write_text(out, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
