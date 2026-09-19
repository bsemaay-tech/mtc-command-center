"""Stages the Gemini packet P030_O9FIX_20260915: DELTA review of the Lead-built O9FIX commit on the WP-P0-30
exporter candidate (daf6a43b -> HEAD_PIN) that answers the Gemini NITs K-01..K-05. Idempotent; refuses while agy runs."""
import pathlib, shutil, hashlib, subprocess, sys
DST = pathlib.Path("C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_O9FIX_20260915")
WT = "C:/tmp/P030_INTEGRATION_20260913"
LANE = pathlib.Path("C:/tmp/CLAUDE_P0_RUN_20260913/laneO9FIX_build")
BASE = "daf6a43b0c4eaafd78e84df776d30d3e41d81d7b"
HEAD = pathlib.Path(__file__).with_name("HEAD_PIN.txt").read_text(encoding="ascii").strip()
out = subprocess.run(["tasklist"], capture_output=True, text=True).stdout.lower()
if any(l.startswith("agy.exe") for l in out.splitlines()):
    print("REFUSE: agy running"); sys.exit(1)
if DST.exists() and (DST / "PACKET_SHA256SUMS.txt").exists():
    print("ALREADY STAGED (idempotent)", DST); sys.exit(0)
if DST.exists():
    shutil.rmtree(DST)
(DST / "subject").mkdir(parents=True); (DST / "sources").mkdir()
def git(*a):
    r = subprocess.run(["git", "-C", WT, "-c", "safe.directory=*"] + list(a), capture_output=True)
    if r.returncode != 0:
        print("REFUSE: git failed", a, r.stderr.decode("utf-8", "replace")[-300:]); sys.exit(1)
    return r.stdout
head = git("rev-parse", "HEAD").decode().strip()
if head != HEAD:
    print("REFUSE: worktree HEAD drifted", head); sys.exit(1)
if git("status", "--porcelain", "--untracked-files=no").decode().strip():
    print("REFUSE: worktree dirty"); sys.exit(1)
(DST / "subject/DELTA_daf6a43b_HEAD.diff").write_bytes(git("diff", BASE, HEAD, "--", "p030_archive_exporter.py", "check_p030_archive_exporter.py"))
(DST / "subject/DELTA_STAT_daf6a43b_HEAD.txt").write_bytes(git("diff", "--stat", BASE, HEAD))
(DST / "subject/p030_archive_exporter_HEAD.py").write_bytes(git("show", f"{HEAD}:p030_archive_exporter.py"))
(DST / "subject/check_p030_archive_exporter_HEAD.py").write_bytes(git("show", f"{HEAD}:check_p030_archive_exporter.py"))
(DST / "subject/COMMIT_HEAD.txt").write_bytes(git("log", "-1", "--format=%H%n%an <%ae>%n%ci%n%n%B", HEAD))
(DST / "sources/p030_closed_partition_backup_adapter_HEAD.py").write_bytes(git("show", f"{HEAD}:p030_closed_partition_backup_adapter.py"))
(DST / "sources/p030_market_data_contracts_HEAD.py").write_bytes(git("show", f"{HEAD}:p030_market_data_contracts.py"))
shutil.copy2(LANE / "GEMINI_REPORT.md", DST / "sources/GEMINI_REPORT_daf6a43b_K01_K05.md")
shutil.copy2(LANE / "TASK.md", DST / "sources/TASK_O9FIX.md")
for n in ("DISPOSITION_O9FIX.md", "LEAD_check_p030_archive_exporter.txt", "LEAD_check_market_data_collector.txt", "LEAD_check_p030_market_data_contracts.txt",
          "LEAD_RED_ARM_new_checker_old_exporter.txt", "LEAD_RUFF_O9FIX.txt", "SHA256SUMS.txt", "LEAD_GUARD_O9FIX.txt"):
    p = LANE / n
    if p.exists(): shutil.copy2(p, DST / "sources" / n)
adapter_tail = (LANE / "LEAD_check_p030_closed_partition_backup_adapter.txt").read_text(encoding="utf-8", errors="replace").split("\n")
(DST / "sources/LEAD_check_p030_closed_partition_backup_adapter_TAIL.txt").write_text("# TAIL (12 lines); full file has %d lines\n" % len(adapter_tail) + "\n".join(adapter_tail[-12:]) + "\n", encoding="utf-8", newline="\n")
dec = pathlib.Path("C:/CT13/DECISIONS.md").read_text(encoding="utf-8").split("\n")
rows = [l for l in dec if l.startswith("| OD-20260915-BUILD-ABC-1") or l.startswith("| OD-20260914-P030-EXPORTER-GO-1") or l.startswith("| OD-20260914-P030-BRIDGE-SHAPE-1")]
(DST / "sources/DECISIONS_rows_P030.md").write_text("# Rows from C:/CT13/DECISIONS.md (verbatim)\n" + "\n".join(rows) + "\n", encoding="utf-8", newline="\n")
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
sums = [f"{H(p)}  {p.relative_to(DST).as_posix()}" for p in sorted(DST.rglob("*")) if p.is_file() and p.name != "PACKET_SHA256SUMS.txt"]
(DST / "PACKET_SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="ascii")
print("STAGED", DST, len(sums), "files; HEAD", head)
