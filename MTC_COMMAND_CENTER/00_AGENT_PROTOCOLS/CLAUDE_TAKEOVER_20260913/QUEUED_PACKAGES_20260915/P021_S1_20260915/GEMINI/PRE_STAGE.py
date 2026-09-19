"""Stages the Gemini packet P021_S1_20260915: DETECTION review of the Lead-written WP-P0-21 S1 catalogue-only slice
at the branch HEAD. Idempotent; refuses while agy runs."""
import pathlib, shutil, hashlib, subprocess, sys
DST = pathlib.Path("C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P021_S1_20260915")
WT = "C:/tmp/P021_S1_20260915"
RUN = pathlib.Path("C:/tmp/CLAUDE_P0_RUN_20260913")
CT13 = pathlib.Path("C:/CT13")
HEAD = pathlib.Path(__file__).with_name("HEAD_PIN.txt").read_text(encoding="ascii").strip()
BASE = "fcac0ac67cf2682693ad28138b1a56e15a0846f2"
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
P = "MTC_COMMAND_CENTER/03_QUANTLENS/tools/"
(DST / "subject/DELTA_fcac0ac6_HEAD.diff").write_bytes(git("diff", BASE, HEAD))
(DST / "subject/DELTA_STAT_fcac0ac6_HEAD.txt").write_bytes(git("diff", "--stat", BASE, HEAD))
(DST / "subject/p021_readiness_rules_HEAD.py").write_bytes(git("show", f"{HEAD}:{P}p021_readiness_rules.py"))
(DST / "subject/test_p021_eligibility_HEAD.py").write_bytes(git("show", f"{HEAD}:{P}tests/test_p021_eligibility.py"))
(DST / "subject/test_strategy_type_policy_set_HEAD.py").write_bytes(git("show", f"{HEAD}:{P}tests/test_strategy_type_policy_set.py"))
(DST / "subject/COMMIT_HEAD.txt").write_bytes(git("log", "-1", "--format=%H%n%an <%ae>%n%ci%n%n%B", HEAD))
(DST / "sources/p021_readiness_rules_fcac0ac6.py").write_bytes(git("show", f"{BASE}:{P}p021_readiness_rules.py"))
(DST / "sources/strategy_type_policy_set_fcac0ac6.py").write_bytes(git("show", f"{BASE}:{P}strategy_type_policy_set.py"))
(DST / "sources/data_gap_ratio_fcac0ac6.py").write_bytes(git("show", f"{BASE}:{P}data_gap_ratio.py"))
shutil.copy2(RUN / "P021_OPTIONS_PACKET_S2_20260915.md", DST / "sources/P021_OPTIONS_PACKET_S2_20260915.md")
shutil.copy2(RUN / "P021_S1_CATALOGUE_SLICE_BRIEF_20260915.md", DST / "sources/P021_S1_CATALOGUE_SLICE_BRIEF_20260915.md")
for n in ("LEAD_VERIFICATION_P021_S1.md", "LEAD_PYTEST.txt", "LEAD_SELF_CHECK.txt", "LEAD_RED_ARM_1_new_tests_old_catalogue.txt",
          "LEAD_RED_ARM_2_old_tests_new_catalogue.txt", "LEAD_RED_ARM_3_mutant_b01_dropped.txt", "LEAD_RUFF.txt", "LEAD_GUARD.txt", "DIFF_STAT_fcac0ac6_701c5ddd.txt"):
    p = RUN / "P021_S1_20260915" / n
    if p.exists():
        b = p.read_bytes().decode("utf-8", "replace")
        (DST / "sources" / n).write_text("".join(ch if ord(ch) < 128 else "?" for ch in b), encoding="ascii", newline="\n")
dec = (CT13 / "DECISIONS.md").read_text(encoding="utf-8").split("\n")
rows = [l for l in dec if l.startswith("| OD-20260915-P021-S2-RECOMMENDED-1") or l.startswith("| OD-20260914-P021-P030-RECORD-1") or l.startswith("| OD-20260907-P021")]
(DST / "sources/DECISIONS_rows_P021.md").write_text("# Rows from C:/CT13/DECISIONS.md (verbatim)\n" + "\n".join(rows) + "\n", encoding="utf-8", newline="\n")
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
sums = [f"{H(p)}  {p.relative_to(DST).as_posix()}" for p in sorted(DST.rglob("*")) if p.is_file() and p.name != "PACKET_SHA256SUMS.txt"]
(DST / "PACKET_SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="ascii")
print("STAGED", DST, len(sums), "files; HEAD", head)
