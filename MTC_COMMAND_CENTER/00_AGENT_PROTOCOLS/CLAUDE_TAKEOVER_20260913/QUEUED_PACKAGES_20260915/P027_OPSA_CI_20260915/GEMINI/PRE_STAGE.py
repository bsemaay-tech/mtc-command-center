"""Stages the Gemini packet P027_OPSA_20260915: DETECTION review of the Lead-written OPS-A tests CI workflow (PR #194) at 63b7bbe0."""
import pathlib, shutil, hashlib, subprocess, sys
DST = pathlib.Path("C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_OPSA_20260915")
WT = "C:/tmp/P027_OPSA_CI_20260915"
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
(DST / "subject/opsa-tests_63b7bbe0.yml").write_bytes(git("show", f"{HEAD}:.github/workflows/opsa-tests.yml"))
(DST / "subject/DIFF_STAT_fcac0ac6_HEAD.txt").write_bytes(git("diff", "--stat", BASE, HEAD))
(DST / "subject/DIFF_fcac0ac6_HEAD.diff").write_bytes(git("diff", BASE, HEAD))
(DST / "subject/COMMIT_HEAD.txt").write_bytes(git("log", "-1", "--format=%H%n%an <%ae>%n%ci%n%n%B", HEAD))
(DST / "sources/ci_fcac0ac6.yml").write_bytes(git("show", f"{BASE}:.github/workflows/ci.yml"))
(DST / "sources/research-gates_fcac0ac6.yml").write_bytes(git("show", f"{BASE}:.github/workflows/research-gates.yml"))
(DST / "sources/test_opsa_fcac0ac6.py").write_bytes(git("show", f"{BASE}:MTC_COMMAND_CENTER/tools/opsa/test_opsa.py"))
E = RUN / "P027_OPSA_CI_20260915"
for n in ("P027_OPSA_CI_EVIDENCE_20260915.md", "RED_RUN_34983897746_failed_excerpt.txt", "opsa_tests_run_34983809921_GREEN.json", "opsa_tests_run_34983897746_RED.json", "pr194_state.json", "pr195_state_RED.json"):
    p = E / n
    if p.exists():
        b = p.read_bytes().decode("utf-8", "replace")
        (DST / "sources" / n).write_text("".join(ch if ord(ch) < 128 else "?" for ch in b), encoding="ascii", newline="\n")
pol = (CT13 / "MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_27_CI_HOME_2026-08-25/CI_POLICY.md").read_bytes().decode("utf-8", "replace")
(DST / "sources/CI_POLICY_CT13.md").write_text("".join(ch if ord(ch) < 128 else "?" for ch in pol), encoding="ascii", newline="\n")
dec = (CT13 / "DECISIONS.md").read_text(encoding="utf-8").split("\n")
rows = [l for l in dec if l.startswith("| OD-20260915-BUILD-ABC-1") or l.startswith("| OD-20260915-P027-DAYONE-ACCEPT-1") or l.startswith("| OD-20260915-P027-T1-WEDOPUS-1")]
(DST / "sources/DECISIONS_rows_P027.md").write_text("# Rows from C:/CT13/DECISIONS.md (verbatim)\n" + "\n".join("".join(ch if ord(ch) < 128 else "?" for ch in l) for l in rows) + "\n", encoding="ascii", newline="\n")
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
sums = [f"{H(p)}  {p.relative_to(DST).as_posix()}" for p in sorted(DST.rglob("*")) if p.is_file() and p.name != "PACKET_SHA256SUMS.txt"]
(DST / "PACKET_SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="ascii")
print("STAGED", DST, len(sums), "files; HEAD", head)
