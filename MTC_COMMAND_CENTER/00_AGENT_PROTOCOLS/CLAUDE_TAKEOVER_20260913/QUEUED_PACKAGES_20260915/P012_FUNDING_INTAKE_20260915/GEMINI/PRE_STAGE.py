"""Stages the Gemini packet P012_INTAKE_20260915: DETECTION review of the Lead-written P0-12 funding intake
adapter (non-accepting half) at the branch HEAD. Idempotent; refuses while agy runs."""
import pathlib, shutil, hashlib, subprocess, sys
DST = pathlib.Path("C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_20260915")
WT = "C:/tmp/P012_INTAKE_20260915"
RUN = pathlib.Path("C:/tmp/CLAUDE_P0_RUN_20260913/P012_FUNDING_INTAKE_20260915")
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
(DST / "subject/funding_intake_adapter.py").write_bytes(git("show", f"{HEAD}:IBKR_PAPER_BRIDGE/tools/funding_intake_adapter.py"))
(DST / "subject/test_funding_intake_adapter.py").write_bytes(git("show", f"{HEAD}:IBKR_PAPER_BRIDGE/tests/test_funding_intake_adapter.py"))
(DST / "subject/DIFF_STAT_fcac0ac6_HEAD.txt").write_bytes(git("diff", "--stat", "fcac0ac6", HEAD))
(DST / "subject/COMMIT_HEAD.txt").write_bytes(git("log", "-1", "--format=%H%n%an <%ae>%n%ci%n%n%B", HEAD))
shutil.copy2(RUN / "P012_FUNDING_INTAKE_DESIGN_20260915.md", DST / "subject/P012_FUNDING_INTAKE_DESIGN_20260915.md")
# the export tool the adapter targets (read-only context; lines cited in the design note) and the capture tool's derived-view builders
(DST / "sources/export_mtc_funding_fcac0ac6.py").write_bytes(git("show", "fcac0ac6:IBKR_PAPER_BRIDGE/tools/export_mtc_funding.py"))
cap = subprocess.run(["git", "-C", "C:/tmp/P1CAP_20260914", "-c", "safe.directory=*", "show", "af921d75:IBKR_PAPER_BRIDGE/tools/capture_own_account_evidence.py"], capture_output=True).stdout
(DST / "sources/capture_own_account_evidence_af921d75.py").write_bytes(cap)
# the real r1 dry-run outputs (short-form address only) and the r1 derived extraction (public data; address absent)
for n in ("binding_packet_draft.json", "retained_rows_expected.json", "intake_gap_report.json"):
    shutil.copy2(RUN / "intake_r1" / n, DST / "sources" / f"r1_{n}")
shutil.copy2(pathlib.Path("C:/tmp/CLAUDE_P0_RUN_20260913/P012_PATH1_REAL_CAPTURE_20260915/r1/DERIVED_EXTRACTION.json"), DST / "sources/r1_DERIVED_EXTRACTION.json")
for n in ("LEAD_PYTEST_focused.txt", "LEAD_RUFF.txt", "LEAD_GUARD.txt", "LEAD_RED_ARM_fabrication_fence.txt", "LEAD_INTAKE_r1_stdout.txt", "LEAD_RED_ARM_nit01_wall_clock.txt", "LEAD_RUFF_nit01.txt", "LEAD_GUARD_nit01.txt"):
    p = RUN / n
    if p.exists():
        b = p.read_bytes().decode("utf-8", "replace")
        (DST / "sources" / n).write_text("".join(ch if ord(ch) < 128 else "?" for ch in b), encoding="ascii", newline="\n")  # ASCII: the reviewer's native view refuses non-ASCII text files
dec = (CT13 / "DECISIONS.md").read_text(encoding="utf-8").split("\n")
rows = [l for l in dec if l.startswith("| OD-20260915-BUILD-ABC-1") or l.startswith("| OD-20260914-P012-ADMISSION-Q3") or l.startswith("| OD-20260914-P012-ADMISSION-Q6")]
(DST / "sources/DECISIONS_rows_P012.md").write_text("# Rows from C:/CT13/DECISIONS.md (verbatim)\n" + "\n".join(rows) + "\n", encoding="utf-8", newline="\n")
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
sums = [f"{H(p)}  {p.relative_to(DST).as_posix()}" for p in sorted(DST.rglob("*")) if p.is_file() and p.name != "PACKET_SHA256SUMS.txt"]
(DST / "PACKET_SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="ascii")
print("STAGED", DST, len(sums), "files; HEAD", head)
