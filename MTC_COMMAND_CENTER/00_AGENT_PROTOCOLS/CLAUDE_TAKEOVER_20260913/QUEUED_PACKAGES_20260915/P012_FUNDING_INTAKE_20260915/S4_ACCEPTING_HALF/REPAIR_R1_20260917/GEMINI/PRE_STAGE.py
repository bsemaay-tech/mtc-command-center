"""Stages the Gemini packet P012_INTAKE_R1_20260917: DETECTION/delta review of the WP-P0-12 intake slice-4
T0 repair round 1 (9ef072a8 -> a871e429: the D-6 completion_check position_source fix + two tests).
Idempotent; refuses while agy runs."""
import pathlib, shutil, hashlib, subprocess, sys, re
DST = pathlib.Path("C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_R1_20260917")
WT = "C:/tmp/P012_INTAKE_20260915"
RUN = pathlib.Path("C:/tmp/CLAUDE_P0_RUN_20260913/P012_FUNDING_INTAKE_20260915/S4_ACCEPTING_HALF/REPAIR_R1_20260917")
LANE = pathlib.Path("C:/tmp/OPUS_QUEUE_20260916/P012INTAKE")
HEAD = pathlib.Path(__file__).with_name("HEAD_PIN.txt").read_text(encoding="ascii").strip()
PRE = "9ef072a8"
EXP = "IBKR_PAPER_BRIDGE/tools/export_mtc_funding.py"
TESTS = "IBKR_PAPER_BRIDGE/tests/test_mtc_funding_export_real_capture.py"
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
(DST / "subject/DIFF_9ef072a8_a871e429.patch").write_bytes(git("diff", PRE, HEAD))
(DST / "subject/DIFF_STAT_9ef072a8_a871e429.txt").write_bytes(git("diff", "--stat", PRE, HEAD))
(DST / "subject/COMMIT_a871e429.txt").write_bytes(git("log", "-1", "--format=%H%n%an <%ae>%n%ci%n%n%B", HEAD))
exp = git("show", f"{HEAD}:{EXP}").decode("utf-8").split("\n")
(DST / "subject/export_mtc_funding_HEAD_lines_150-200_constants_limitations.py").write_text("\n".join(exp[149:200]) + "\n", encoding="utf-8", newline="\n")
(DST / "subject/export_mtc_funding_HEAD_lines_1140-1290_real_fills_completion.py").write_text("\n".join(exp[1139:1290]) + "\n", encoding="utf-8", newline="\n")
tests = git("show", f"{HEAD}:{TESTS}").decode("utf-8").split("\n")
(DST / "subject/test_real_capture_HEAD_lines_1-120_fixtures.py").write_text("\n".join(tests[:120]) + "\n", encoding="utf-8", newline="\n")
(DST / "subject/test_real_capture_HEAD_lines_195-275_helpers.py").write_text("\n".join(tests[194:275]) + "\n", encoding="utf-8", newline="\n")
(DST / "subject/test_real_capture_HEAD_lines_890-975_new_tests.py").write_text("\n".join(tests[889:975]) + "\n", encoding="utf-8", newline="\n")
rep = LANE / "ATTEMPT1_REQUEST_CHANGES_9ef072a8" / "OPUS_REPORT.md"
shutil.copy2(rep, DST / "sources/OPUS_REPORT_attempt1_9ef072a8.md")
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
