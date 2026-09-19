"""Stages the Gemini packet P027_CI_20260915: T2 read-only corroboration of (1) the PR #193 workflow diff
(`.github/workflows/research-gates.yml`, fcac0ac6 -> a3325836, owner ruling OD-20260915-P027-CI-ADDITIONS-GO-1)
and (2) the WP-P0-27 acceptance packet of 2026-09-15 (night) against its evidence copies. Idempotent; refuses
while agy runs (its git reads happen only then)."""
import pathlib, shutil, hashlib, subprocess, sys
DST = pathlib.Path("C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P027_CI_20260915")
WT = "C:/tmp/P027_CI_20260915"
RUN = pathlib.Path("C:/tmp/CLAUDE_P0_RUN_20260913/P027_RECONCILIATION_20260915")
CT13 = pathlib.Path("C:/CT13")
REC = CT13 / "MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/QUEUED_PACKAGES_20260915"
BASE, HEAD = "fcac0ac67cf2682693ad28138b1a56e15a0846f2", "a33258367739400017c11a7e498030238f9b1564"
WF = ".github/workflows/research-gates.yml"
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
dirty = git("status", "--porcelain").decode().strip()
if dirty:
    print("REFUSE: worktree dirty", dirty[:200]); sys.exit(1)
# subject 1: the PR #193 workflow diff
(DST / "subject/DIFF_fcac0ac6_a3325836_research-gates.diff").write_bytes(git("diff", BASE, HEAD, "--", WF))
(DST / "subject/DIFF_STAT_fcac0ac6_a3325836.txt").write_bytes(git("diff", "--stat", BASE, HEAD))
(DST / "subject/research-gates_a3325836.yml").write_bytes(git("show", f"{HEAD}:{WF}"))
(DST / "subject/research-gates_fcac0ac6_BASE.yml").write_bytes(git("show", f"{BASE}:{WF}"))
(DST / "subject/COMMITS_55ab90b8_a3325836.txt").write_bytes(git("log", "--format=%H%n%an <%ae>%n%ci%n%n%B%n----", f"{BASE}..{HEAD}"))
# subject 2: the acceptance packet (night)
shutil.copy2(RUN / "P027_ACCEPTANCE_PACKET_20260915.md", DST / "subject/P027_ACCEPTANCE_PACKET_20260915.md")
# sources: day-one workflow + policy + plan block + rulings
(DST / "sources/ci_fcac0ac6.yml").write_bytes(git("show", f"{BASE}:.github/workflows/ci.yml"))
(DST / "sources/pine-defang-guard_fcac0ac6.yml").write_bytes(git("show", f"{BASE}:.github/workflows/pine-defang-guard.yml"))
shutil.copy2(CT13 / "MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_27_CI_HOME_2026-08-25/CI_POLICY.md", DST / "sources/P027_CI_POLICY_2026-08-25.md")
plan = (CT13 / "MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md").read_text(encoding="utf-8").split("\n")
(DST / "sources/PLAN_WP_P0_27_block_lines590-602.md").write_text("# Master plan lines 590-602 (WP-P0-27 block), verbatim\n" + "\n".join(plan[589:602]) + "\n", encoding="utf-8", newline="\n")
dec = (CT13 / "DECISIONS.md").read_text(encoding="utf-8").split("\n")
keys = ("| OD-20260915-P027-CI-ADDITIONS-GO-1", "| OD-20260826-4", "| OD-20260826-6", "| OD-20260829-1")
rows = [l for l in dec if any(l.startswith(k) for k in keys)]
(DST / "sources/DECISIONS_rows_P027.md").write_text("# Rows from C:/CT13/DECISIONS.md (verbatim)\n" + "\n".join(rows) + "\n", encoding="utf-8", newline="\n")
# sources: evidence copies the packet cites
for n in ("P027_REQUIREMENT_RECONCILIATION_20260915.md", "RED_DEMO_EVIDENCE_20260915.md", "PR192_state_RED.json", "PR192_state_GREEN.json",
          "RED_RUN_34946092493_failed_log.txt", "GH_QUERIES_20260915_NIGHT.txt"):
    shutil.copy2(RUN / n, DST / "sources" / n)
for n in ("P027_CI_ADDITIONS_EVIDENCE_20260915.md", "pr193_state_GREEN.json", "research_gates_run_34961383292_RED_checkout.json", "research_gates_run_34963602576.json"):
    shutil.copy2(RUN / "CI_PR193" / n, DST / "sources" / n)
# e-mail artifact: header block only, gmail addresses masked (provenance without copying the owner's addresses)
import re
em = (RUN / "CI_FAILURE_EMAIL_FWD_20260915_run34961383292_REDACTED.md").read_text(encoding="utf-8")
em = re.sub(r"[A-Za-z0-9._%+-]+@gmail\.com", "<gmail-address-masked>", em)
(DST / "sources/CI_FAILURE_EMAIL_ARTIFACT_MASKED.md").write_text(em, encoding="utf-8", newline="\n")
shutil.copy2(REC / "LEAD_ADJUDICATION_GEMINI_CORROBORATION.md", DST / "sources/PREDECESSOR_LEAD_ADJUDICATION_GEMINI_CORROBORATION.md")
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
sums = [f"{H(p)}  {p.relative_to(DST).as_posix()}" for p in sorted(DST.rglob("*")) if p.is_file() and p.name != "PACKET_SHA256SUMS.txt"]
(DST / "PACKET_SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="ascii")
print("STAGED", DST, len(sums), "files; HEAD", head)
