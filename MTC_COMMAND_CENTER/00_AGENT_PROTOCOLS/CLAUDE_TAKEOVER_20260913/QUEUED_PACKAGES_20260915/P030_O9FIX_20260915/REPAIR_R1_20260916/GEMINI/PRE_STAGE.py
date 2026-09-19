"""Stages the Gemini packet P030_R1_20260916: DETECTION/delta review of the P0-30 exporter T0 repair round 1
(153edee9 -> 53b43c21 format-only -> 0be0a8aa) against the lane-3 exact-Opus REQUIRED findings. Idempotent;
refuses while agy runs."""
import pathlib, shutil, hashlib, subprocess, sys, re
DST = pathlib.Path("C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R1_20260916")
WT = "C:/tmp/P030_INTEGRATION_20260913"
RUN = pathlib.Path("C:/tmp/CLAUDE_P0_RUN_20260913/laneO9FIX_build/REPAIR_R1_20260916")
LANE = pathlib.Path("C:/tmp/OPUS_QUEUE_20260916/P030")
HEAD = pathlib.Path(__file__).with_name("HEAD_PIN.txt").read_text(encoding="ascii").strip()
FORMAT_ONLY = "53b43c21"
PRE = "153edee9"
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
if not git("rev-parse", f"{HEAD}~1").decode().strip().startswith(FORMAT_ONLY):
    print("REFUSE: parent is not the format-only commit"); sys.exit(1)
(DST / "subject/p030_archive_exporter.py").write_bytes(git("show", f"{HEAD}:p030_archive_exporter.py"))
(DST / "subject/check_p030_archive_exporter.py").write_bytes(git("show", f"{HEAD}:check_p030_archive_exporter.py"))
(DST / "subject/DIFF_semantic_53b43c21_0be0a8aa.patch").write_bytes(git("diff", FORMAT_ONLY, HEAD))
(DST / "subject/DIFF_format_only_153edee9_53b43c21.patch").write_bytes(git("diff", PRE, FORMAT_ONLY))
(DST / "subject/COMMITS.txt").write_bytes(git("log", "-3", "--format=%H%n%an <%ae>%n%ci%n%n%B%n----", HEAD))
(DST / "subject/BLOB_OIDS_HEAD.txt").write_bytes(git("ls-tree", HEAD, "--", "p030_archive_exporter.py", "check_p030_archive_exporter.py"))
shutil.copy2(RUN / "LEAD_VERIFICATION_P030_R1.md", DST / "subject/LEAD_VERIFICATION_P030_R1.md")
# the first exact-Opus report = the findings this repair answers
shutil.copy2(LANE / "ATTEMPT1_REQUEST_CHANGES_153edee9" / "OPUS_T0_REPORT.md", DST / "sources/OPUS_T0_REPORT_attempt1_153edee9.md")
(DST / "sources/p030_archive_exporter_153edee9_pre_repair.py").write_bytes(git("show", f"{PRE}:p030_archive_exporter.py"))
(DST / "sources/p030_closed_partition_backup_adapter_HEAD.py").write_bytes(git("show", f"{HEAD}:p030_closed_partition_backup_adapter.py"))
(DST / "sources/opsa_common_HEAD.py").write_bytes(git("show", f"{HEAD}:MTC_COMMAND_CENTER/tools/opsa/opsa_common.py"))
for p in sorted(RUN.glob("LEAD_*.txt")):
    b = p.read_bytes().decode("utf-8", "replace")
    (DST / "sources" / p.name).write_text("".join(ch if ord(ch) < 128 else "?" for ch in b), encoding="ascii", newline="\n")
for p in DST.rglob("*"):
    if p.is_file():
        txt = p.read_bytes().decode("utf-8", "replace")
        if re.search(r"[A-Za-z0-9._%+-]+@gmail\.com", txt):
            print("REFUSE: mailbox address in packet", p.name); shutil.rmtree(DST); sys.exit(1)
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
sums = [f"{H(p)}  {p.relative_to(DST).as_posix()}" for p in sorted(DST.rglob("*")) if p.is_file() and p.name != "PACKET_SHA256SUMS.txt"]
(DST / "PACKET_SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="ascii")
print("STAGED", DST, len(sums), "files; HEAD", head)
