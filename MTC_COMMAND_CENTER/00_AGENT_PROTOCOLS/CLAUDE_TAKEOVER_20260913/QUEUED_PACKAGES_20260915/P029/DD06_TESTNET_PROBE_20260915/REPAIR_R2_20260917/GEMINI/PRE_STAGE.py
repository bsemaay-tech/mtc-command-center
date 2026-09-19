"""Stages the Gemini packet DD06_R2_20260917: DETECTION/delta review of the DD-06 probe T0 repair round 1
(a46b2a9d -> 2128352b: directional amount-aware attribution, errored fund arms measured and stopped, whose-funds-moved
attribution, abort propagation). Idempotent; refuses while agy runs."""
import pathlib, shutil, hashlib, subprocess, sys, re
DST = pathlib.Path("C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_R2_20260917")
WT = "C:/tmp/P029_DD06_20260915"
RUN = pathlib.Path("C:/tmp/CLAUDE_P0_RUN_20260913/DD06_TESTNET_PROBE_20260915/REPAIR_R2_20260917")
INC = pathlib.Path("C:/tmp/CLAUDE_P0_RUN_20260913/INCIDENT_20260917_LANE7_DD06")
LANE = pathlib.Path("C:/tmp/OPUS_QUEUE_20260916/DD06")
HEAD = pathlib.Path(__file__).with_name("HEAD_PIN.txt").read_text(encoding="ascii").strip()
PRE = "a46b2a9d"
TOOL = "IBKR_PAPER_BRIDGE/tools/dd06_agent_withdraw_probe.py"
TESTS = "IBKR_PAPER_BRIDGE/tests/test_dd06_agent_withdraw_probe.py"
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
(DST / "subject/DIFF_a46b2a9d_2128352b.patch").write_bytes(git("diff", PRE, HEAD))
(DST / "subject/DIFF_STAT_a46b2a9d_2128352b.txt").write_bytes(git("diff", "--stat", PRE, HEAD))
(DST / "subject/COMMIT_2128352b.txt").write_bytes(git("log", "-1", "--format=%H%n%an <%ae>%n%ci%n%n%B", HEAD))
(DST / "subject/dd06_agent_withdraw_probe_HEAD_complete.py").write_bytes(git("show", f"{HEAD}:{TOOL}"))
(DST / "subject/test_dd06_agent_withdraw_probe_HEAD_complete.py").write_bytes(git("show", f"{HEAD}:{TESTS}"))
shutil.copy2(LANE / "ATTEMPT2_REQUEST_CHANGES_a46b2a9d" / "OPUS_T0_REPORT.md", DST / "sources/OPUS_T0_REPORT_attempt2_a46b2a9d.md")
shutil.copy2(INC / "INCIDENT_20260917_LANE7_DD06_UNINTENDED_TESTNET_RUN.md", DST / "sources/INCIDENT_20260917_LANE7_DD06_UNINTENDED_TESTNET_RUN.md")
for p in sorted(RUN.glob("LEAD_*.txt")):
    b = p.read_bytes().decode("utf-8", "replace")
    (DST / "sources" / p.name).write_text("".join(ch if ord(ch) < 128 else "?" for ch in b), encoding="ascii", newline="\n")
for p in DST.rglob("*"):
    if p.is_file():
        txt = p.read_bytes().decode("utf-8", "replace")
        if re.search(r"[A-Za-z0-9._%+-]+@gmail\.com", txt):
            print("REFUSE: mailbox address in packet", p.name); shutil.rmtree(DST); sys.exit(1)
        if re.search(r"(?i)HL_API_WALLET_KEY\s*[=:]\s*0x[0-9a-f]{64}", txt):
            print("REFUSE: key-shaped material in packet", p.name); shutil.rmtree(DST); sys.exit(1)
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
sums = [f"{H(p)}  {p.relative_to(DST).as_posix()}" for p in sorted(DST.rglob("*")) if p.is_file() and p.name != "PACKET_SHA256SUMS.txt"]
(DST / "PACKET_SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="ascii")
print("STAGED", DST, len(sums), "files; HEAD", head)
