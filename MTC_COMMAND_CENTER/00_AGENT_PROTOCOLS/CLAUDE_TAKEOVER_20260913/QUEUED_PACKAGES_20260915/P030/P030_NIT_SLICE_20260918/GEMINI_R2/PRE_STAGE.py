"""Stages the Gemini packet P030_R2_20260919: DETECTION/delta review of the P0-30 NIT-slice REPAIR ROUND 2
(d426e79f -> b4df1413: nesting fences derived per layer on the running interpreter, third adapter parse site
guarded, receipt-side race arm, docstring trim). Idempotent; refuses while agy runs."""
import pathlib, shutil, hashlib, subprocess, sys, re
DST = pathlib.Path("C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P030_R2_20260919")
WT = "C:/tmp/P030_INTEGRATION_20260913"
RUN = pathlib.Path("C:/tmp/CLAUDE_P0_RUN_20260913/P030_NIT_SLICE_20260918/REPAIR_R2_20260919")
LANE = pathlib.Path("C:/tmp/OPUS_QUEUE_20260916/P030")
HEAD = pathlib.Path(__file__).with_name("HEAD_PIN.txt").read_text(encoding="ascii").strip()
PRE = "d426e79f"
FILES = ("p030_archive_exporter.py", "check_p030_archive_exporter.py", "p030_closed_partition_backup_adapter.py", "check_p030_closed_partition_backup_adapter.py")
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
for f in FILES:
    (DST / "subject" / f"{f}_HEAD_complete.py").write_bytes(git("show", f"{HEAD}:{f}"))
(DST / "subject/DIFF_d426e79f_b4df1413.patch").write_bytes(git("diff", PRE, HEAD, "--", *FILES))
(DST / "subject/DIFF_STAT_d426e79f_b4df1413.txt").write_bytes(git("diff", "--stat", PRE, HEAD))
(DST / "subject/COMMIT_b4df1413.txt").write_bytes(git("log", "-1", "--format=%H%n%an <%ae>%n%ci%n%n%B", HEAD))
(DST / "subject/BLOB_OIDS_HEAD.txt").write_bytes(git("ls-tree", HEAD, "--", *FILES))
shutil.copy2(LANE / "LEAD_ADJUDICATION_P030_NIT_T0.md", DST / "sources/LEAD_ADJUDICATION_P030_NIT_T0.md")
shutil.copy2(LANE / "ATTEMPT4_REQUEST_CHANGES_d426e79f" / "OPUS_T0_REPORT.md", DST / "sources/OPUS_T0_REPORT_attempt4_d426e79f.md")
shutil.copy2(RUN / "LEAD_VERIFICATION_P030_NIT_R2.md", DST / "sources/LEAD_VERIFICATION_P030_NIT_R2.md")
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
