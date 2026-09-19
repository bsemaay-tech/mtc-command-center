"""Stages the Gemini packet P021_R1_20260917: DETECTION/delta review of the WP-P0-21 S1 T0 repair round 1
(7fecf204 -> eada65ed: verbatim M-C definition, B-06 split into two tolerances, self-check honesty, provenance pins).
Idempotent; refuses while agy runs."""
import pathlib, shutil, hashlib, subprocess, sys, re
DST = pathlib.Path("C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P021_R1_20260917")
WT = "C:/tmp/P021_S1_20260915"
RUN = pathlib.Path("C:/tmp/CLAUDE_P0_RUN_20260913/P021_S1_20260915/REPAIR_R1_20260917")
LANE = pathlib.Path("C:/tmp/OPUS_QUEUE_20260916/P021S1")
PACKET = pathlib.Path("C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/QUEUED_PACKAGES_20260915/P021_OPTIONS_PACKET_S2_20260915.md")
HEAD = pathlib.Path(__file__).with_name("HEAD_PIN.txt").read_text(encoding="ascii").strip()
PRE = "7fecf204"
MOD = "MTC_COMMAND_CENTER/03_QUANTLENS/tools/p021_readiness_rules.py"
T1 = "MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_p021_eligibility.py"
T2 = "MTC_COMMAND_CENTER/03_QUANTLENS/tools/tests/test_strategy_type_policy_set.py"
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
(DST / "subject/DIFF_7fecf204_eada65ed.patch").write_bytes(git("diff", PRE, HEAD))
(DST / "subject/DIFF_STAT_7fecf204_eada65ed.txt").write_bytes(git("diff", "--stat", PRE, HEAD))
(DST / "subject/COMMIT_eada65ed.txt").write_bytes(git("log", "-1", "--format=%H%n%an <%ae>%n%ci%n%n%B", HEAD))
mod = git("show", f"{HEAD}:{MOD}").decode("utf-8").split("\n")
(DST / "subject/p021_readiness_rules_HEAD_lines_1-120_dataclasses_policy_set.py").write_text("\n".join(mod[:120]) + "\n", encoding="utf-8", newline="\n")
(DST / "subject/p021_readiness_rules_HEAD_lines_170-300_numbers_definition_rules.py").write_text("\n".join(mod[169:300]) + "\n", encoding="utf-8", newline="\n")
(DST / "subject/p021_readiness_rules_HEAD_lines_300-470_validate_record_selfcheck.py").write_text("\n".join(mod[299:470]) + "\n", encoding="utf-8", newline="\n")
t1 = git("show", f"{HEAD}:{T1}").decode("utf-8").split("\n")
(DST / "subject/test_p021_eligibility_HEAD_lines_1-160_fence.py").write_text("\n".join(t1[:160]) + "\n", encoding="utf-8", newline="\n")
t2 = git("show", f"{HEAD}:{T2}").decode("utf-8").split("\n")
(DST / "subject/test_strategy_type_policy_set_HEAD_complete.py").write_text("\n".join(t2) + "\n", encoding="utf-8", newline="\n")
pk = PACKET.read_text(encoding="utf-8").split("\n")
(DST / "sources/P021_OPTIONS_PACKET_S2_20260915_section4_lines_26-40.md").write_text("\n".join(pk[25:40]) + "\n", encoding="utf-8", newline="\n")
shutil.copy2(LANE / "ATTEMPT1_REQUEST_CHANGES_7fecf204" / "OPUS_T0_REPORT.md", DST / "sources/OPUS_T0_REPORT_attempt1_7fecf204.md")
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
