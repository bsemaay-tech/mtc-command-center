"""Stages the Gemini packet P031_R1_20260916: DETECTION/delta review of the P0-31 M1 T0 repair round 1
(48bd70de -> e9e37aec: one fence test for the OD-7 revocation guard). Idempotent; refuses while agy runs."""
import pathlib, shutil, hashlib, subprocess, sys, re
DST = pathlib.Path("C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_R1_20260916")
WT = "C:/tmp/P031_M1_20260913"
RUN = pathlib.Path("C:/tmp/CLAUDE_P0_RUN_20260913/P031_FIX_20260915/REPAIR_R1_20260916")
LANE = pathlib.Path("C:/tmp/OPUS_QUEUE_20260916/P031")
HEAD = pathlib.Path(__file__).with_name("HEAD_PIN.txt").read_text(encoding="ascii").strip()
PRE = "48bd70de"
LEDGER = "MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py"
TESTS = "MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p031_lifecycle_ledger.py"
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
(DST / "subject/DIFF_48bd70de_e9e37aec.patch").write_bytes(git("diff", PRE, HEAD))
(DST / "subject/DIFF_STAT_48bd70de_e9e37aec.txt").write_bytes(git("diff", "--stat", PRE, HEAD))
(DST / "subject/COMMIT_e9e37aec.txt").write_bytes(git("log", "-1", "--format=%H%n%an <%ae>%n%ci%n%n%B", HEAD))
# the test module is 5000+ lines: the subject is the new test in context (lines 2500-2680 at HEAD) plus the
# ledger's guard region; the reviewer names the ranges it read
test_lines = git("show", f"{HEAD}:{TESTS}").decode("utf-8").split("\n")
(DST / "subject/test_p031_lifecycle_ledger_HEAD_lines_2500-2680.py").write_text("\n".join(test_lines[2499:2680]) + "\n", encoding="utf-8", newline="\n")
(DST / "subject/test_p031_lifecycle_ledger_HEAD_lines_1-420_helpers.py").write_text("\n".join(test_lines[:420]) + "\n", encoding="utf-8", newline="\n")
ledger_lines = git("show", f"{HEAD}:{LEDGER}").decode("utf-8").split("\n")
(DST / "sources/p031_lifecycle_ledger_HEAD_lines_640-880.py").write_text("\n".join(ledger_lines[639:880]) + "\n", encoding="utf-8", newline="\n")
shutil.copy2(LANE / "ATTEMPT1_REQUEST_CHANGES_48bd70de" / "OPUS_T0_REPORT.md", DST / "sources/OPUS_T0_REPORT_attempt1_48bd70de.md")
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
