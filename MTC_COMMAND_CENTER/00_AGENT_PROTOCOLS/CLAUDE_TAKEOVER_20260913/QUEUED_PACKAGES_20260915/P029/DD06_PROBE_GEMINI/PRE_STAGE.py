"""Stages the Gemini packet DD06_PROBE_20260915: DETECTION review of the Lead-written WP-P0-29 DD-06 testnet
falsification probe (script + fixture tests + step packet) at the branch HEAD. Idempotent; refuses while agy runs."""
import pathlib, shutil, hashlib, subprocess, sys
DST = pathlib.Path("C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/DD06_PROBE_20260915")
WT = "C:/tmp/P029_DD06_20260915"
RUN = pathlib.Path("C:/tmp/CLAUDE_P0_RUN_20260913/DD06_TESTNET_PROBE_20260915")
CT13 = pathlib.Path("C:/CT13")
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
T = "IBKR_PAPER_BRIDGE/tools/dd06_agent_withdraw_probe.py"; X = "IBKR_PAPER_BRIDGE/tests/test_dd06_agent_withdraw_probe.py"
(DST / "subject/dd06_agent_withdraw_probe.py").write_bytes(git("show", f"{HEAD}:{T}"))
(DST / "subject/test_dd06_agent_withdraw_probe.py").write_bytes(git("show", f"{HEAD}:{X}"))
(DST / "subject/DIFF_STAT_fcac0ac6_HEAD.txt").write_bytes(git("diff", "--stat", "fcac0ac6", HEAD))
(DST / "subject/COMMIT_HEAD.txt").write_bytes(git("log", "-1", "--format=%H%n%an <%ae>%n%ci%n%n%B", HEAD))
shutil.copy2(RUN / "DD06_TESTNET_PROBE_STEP_PACKET_20260915.md", DST / "subject/DD06_TESTNET_PROBE_STEP_PACKET_20260915.md")
# sources: the Bridge pieces the probe relies on (read-only context), the smoke precedent, the ruling
(DST / "sources/bridge_settings_fcac0ac6.py").write_bytes(git("show", "fcac0ac6:IBKR_PAPER_BRIDGE/bridge/settings.py"))
(DST / "sources/smoke_p0_fcac0ac6.py").write_bytes(git("show", "fcac0ac6:IBKR_PAPER_BRIDGE/tools/smoke_p0.py"))
shutil.copy2(CT13 / "MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/BRIDGE_TESTNET_SMOKE_P0_20260914/LEAD_NOTE.md", DST / "sources/SMOKE_P0_LEAD_NOTE_20260914.md")
dec = (CT13 / "DECISIONS.md").read_text(encoding="utf-8").split("\n")
rows = [l for l in dec if l.startswith("| OD-20260915-P029-DD06-TESTNET-PROBE-PREP-1") or l.startswith("| OD-20260914-BRIDGE-SMOKE-GO-1") or l.startswith("| OD-20260915-P029-DD01-READ-1")]
(DST / "sources/DECISIONS_rows_DD06.md").write_text("# Rows from C:/CT13/DECISIONS.md (verbatim)\n" + "\n".join(rows) + "\n", encoding="utf-8", newline="\n")
for n in ("LEAD_PYTEST_focused_slice2.txt", "LEAD_PYTEST_full_bridge_slice2.txt", "LEAD_RUFF_slice2.txt", "LEAD_RED_ARM_m1.txt", "LEAD_RED_ARM_m2.txt", "LEAD_RED_ARM_m3.txt", "SDK_0_24_0_SIGNATURES.txt", "LEAD_GUARD_slice2.txt", "RECOVERED_RESPONSE_attempt1_VOIDED.md", "RECOVERED_RESPONSE_attempt2_VOIDED.md", "LEAD_PYTEST_focused_slice3.txt", "LEAD_PYTEST_full_bridge_slice3.txt", "LEAD_RUFF_slice3.txt", "LEAD_GUARD_slice3.txt", "LEAD_RED_ARM_slice3_old_probe_new_tests.txt", "kvm2_dd06_probe_run.sh", "kvm2_dd06_probe_run_OUTPUT.redacted.txt"):
    p = RUN / n
    if not p.exists(): p = pathlib.Path(__file__).with_name(n)
    if p.exists():
        b = p.read_bytes().decode("utf-8", "replace")
        (DST / "sources" / n).write_text("".join(ch if ord(ch) < 128 else "?" for ch in b), encoding="ascii", newline="\n")
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
sums = [f"{H(p)}  {p.relative_to(DST).as_posix()}" for p in sorted(DST.rglob("*")) if p.is_file() and p.name != "PACKET_SHA256SUMS.txt"]
(DST / "PACKET_SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="ascii")
print("STAGED", DST, len(sums), "files; HEAD", head)
