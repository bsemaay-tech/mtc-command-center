"""Generate <lane>/opus/run_max.ps1 from <lane>/opus/run.ps1: the same exact claude-opus-5 xhigh review lane, but on
the isolated Claude MAX profile (~/.claude-max) instead of the PRO profile (~/.claude). Allowed only under
OD-20260919-MAX-LANES-TODAY-1 (2026-09-19). One lane per profile at a time, machine-wide; stamp the queue log
'[MAX] launching ...' before starting it. Usage: python make_max_launcher.py <P1CAP|P012INTAKE|P030|...>"""
import pathlib
import sys

pkg = sys.argv[1]
lane = pathlib.Path("C:/tmp/OPUS_QUEUE_20260916") / pkg / "opus"
src = (lane / "run.ps1").read_text(encoding="utf-8")
old = "$env:CLAUDE_CONFIG_DIR = (Join-Path $env:USERPROFILE '.claude')"
if src.count(old) != 1:
    sys.exit(f"{pkg}: CLAUDE_CONFIG_DIR line not found exactly once in run.ps1")
dst = src.replace(old, "$env:CLAUDE_CONFIG_DIR = (Join-Path $env:USERPROFILE '.claude-max')  # MAX profile, OD-20260919-MAX-LANES-TODAY-1")
dst = dst.replace("on the Claude PRO profile (~/.claude), NOT the Max desktop session.", "on the isolated Claude MAX profile (~/.claude-max) - owner ruling OD-20260919-MAX-LANES-TODAY-1 (2026-09-19 only).", 1)
(lane / "run_max.ps1").write_text(dst, encoding="utf-8")
print("wrote", lane / "run_max.ps1", "- same HEAD pin, same brief, MAX profile; run it only when no other MAX lane is running")
