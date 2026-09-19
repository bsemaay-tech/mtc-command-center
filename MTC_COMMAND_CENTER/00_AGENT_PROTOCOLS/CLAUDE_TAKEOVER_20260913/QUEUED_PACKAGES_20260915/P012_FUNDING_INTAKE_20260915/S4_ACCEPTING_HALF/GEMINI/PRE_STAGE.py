"""Stages the Gemini packet P012_INTAKE_S4_20260916: DETECTION review of the Lead-written WP-P0-12 funding
intake slice 4 (the ACCEPTING half of export_mtc_funding.py under D-1..D-6 + the adapter's real-capture
packet) at the branch HEAD. Idempotent; refuses while agy runs."""
import pathlib, shutil, hashlib, subprocess, sys
DST = pathlib.Path("C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_INTAKE_S4_20260916")
WT = "C:/tmp/P012_INTAKE_20260915"
RUN = pathlib.Path("C:/tmp/CLAUDE_P0_RUN_20260913/P012_FUNDING_INTAKE_20260915")
S4 = RUN / "S4_ACCEPTING_HALF"
CT13 = pathlib.Path("C:/CT13")
HEAD = pathlib.Path(__file__).with_name("HEAD_PIN.txt").read_text(encoding="ascii").strip()
FORMAT_ONLY = "b667dbcc1a38e795a19576dab93e7723e78ad620"  # ruff-format commit, parent of the slice
PRE_SLICE = "4c802e9b"  # branch HEAD before this slice
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
if git("rev-parse", f"{HEAD}~1").decode().strip() != FORMAT_ONLY:
    print("REFUSE: the slice's parent is not the format-only commit"); sys.exit(1)
# subject: the four files at HEAD (blob bytes, LF), the semantic diff (format commit -> slice), the
# format-only diff (pre-slice -> format commit) for the mechanical check, and both commit messages
for name, path in (
    ("export_mtc_funding.py", "IBKR_PAPER_BRIDGE/tools/export_mtc_funding.py"),
    ("funding_intake_adapter.py", "IBKR_PAPER_BRIDGE/tools/funding_intake_adapter.py"),
    ("test_mtc_funding_export_real_capture.py", "IBKR_PAPER_BRIDGE/tests/test_mtc_funding_export_real_capture.py"),
    ("test_funding_intake_adapter.py", "IBKR_PAPER_BRIDGE/tests/test_funding_intake_adapter.py"),
):
    (DST / "subject" / name).write_bytes(git("show", f"{HEAD}:{path}"))
(DST / "subject/DIFF_semantic_b667dbcc_9ef072a8.patch").write_bytes(git("diff", FORMAT_ONLY, HEAD))
(DST / "subject/DIFF_STAT_semantic_b667dbcc_9ef072a8.txt").write_bytes(git("diff", "--stat", FORMAT_ONLY, HEAD))
(DST / "subject/DIFF_format_only_4c802e9b_b667dbcc.patch").write_bytes(git("diff", PRE_SLICE, FORMAT_ONLY))
(DST / "subject/COMMITS_HEAD_and_parent.txt").write_bytes(git("log", "-2", "--format=%H%n%an <%ae>%n%ci%n%n%B%n----", HEAD))
(DST / "subject/BLOB_OIDS_HEAD.txt").write_bytes(git("ls-tree", HEAD, "--", "IBKR_PAPER_BRIDGE/tools/export_mtc_funding.py", "IBKR_PAPER_BRIDGE/tools/funding_intake_adapter.py", "IBKR_PAPER_BRIDGE/tests/test_mtc_funding_export_real_capture.py", "IBKR_PAPER_BRIDGE/tests/test_funding_intake_adapter.py"))
shutil.copy2(S4 / "LEAD_VERIFICATION_P012_INTAKE_S4.md", DST / "subject/LEAD_VERIFICATION_P012_INTAKE_S4.md")
# sources: the exporter as the slice found it (format-only commit, = pre-slice semantics), the synthetic
# contract suite it must not disturb (carried fences), the 09-15 design note + owner packet, the r1 real
# packet and gap report from the real dry run (short-form address only), the r1 derived view, evidence
(DST / "sources/export_mtc_funding_b667dbcc_pre_slice.py").write_bytes(git("show", f"{FORMAT_ONLY}:IBKR_PAPER_BRIDGE/tools/export_mtc_funding.py"))
(DST / "sources/test_mtc_funding_export_carried_fences.py").write_bytes(git("show", f"{HEAD}:IBKR_PAPER_BRIDGE/tests/test_mtc_funding_export.py"))
(DST / "sources/funding_intake_adapter_4c802e9b_pre_slice.py").write_bytes(git("show", f"{PRE_SLICE}:IBKR_PAPER_BRIDGE/tools/funding_intake_adapter.py"))
shutil.copy2(RUN / "P012_FUNDING_INTAKE_DESIGN_20260915.md", DST / "sources/P012_FUNDING_INTAKE_DESIGN_20260915.md")
shutil.copy2(RUN / "P012_INTAKE_DECISIONS_OWNER_PACKET_20260915.md", DST / "sources/P012_INTAKE_DECISIONS_OWNER_PACKET_20260915.md")
for n in ("binding_packet_real_capture.json", "intake_gap_report.json", "retained_rows_expected.json"):
    shutil.copy2(RUN / "intake_r1_s4" / n, DST / "sources" / f"r1_s4_{n}")
shutil.copy2(pathlib.Path("C:/tmp/CLAUDE_P0_RUN_20260913/P012_PATH1_REAL_CAPTURE_20260915/r1/DERIVED_EXTRACTION.json"), DST / "sources/r1_DERIVED_EXTRACTION.json")
for p in sorted(S4.glob("LEAD_*.txt")) + sorted(S4.glob("BLOB_OIDS_*.txt")):
    b = p.read_bytes().decode("utf-8", "replace")
    (DST / "sources" / p.name).write_text("".join(ch if ord(ch) < 128 else "?" for ch in b), encoding="ascii", newline="\n")  # ASCII: the reviewer's native view refuses non-ASCII text files
dec = (CT13 / "DECISIONS.md").read_text(encoding="utf-8").split("\n")
rows = [l for l in dec if l.startswith("| OD-20260916-P012-INTAKE-D1-D6-R-1") or l.startswith("| OD-20260914-P012-ADMISSION-Q3") or l.startswith("| OD-20260914-P012-ADMISSION-Q6") or l.startswith("| OD-20260915-BUILD-ABC-1")]
(DST / "sources/DECISIONS_rows_P012.md").write_text("# Rows from C:/CT13/DECISIONS.md (verbatim)\n" + "\n".join(rows) + "\n", encoding="utf-8", newline="\n")
# leak check: the full mainnet address must appear nowhere in the packet
import re
for p in DST.rglob("*"):
    if p.is_file():
        txt = p.read_bytes().decode("utf-8", "replace")
        for m in re.findall(r"0x[0-9a-fA-F]{40}(?![0-9a-fA-F])", txt):
            if m.lower() != "0x" + "0" * 40:
                print("REFUSE: a full 0x address reached the packet", p.name, m[:8]); shutil.rmtree(DST); sys.exit(1)
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
sums = [f"{H(p)}  {p.relative_to(DST).as_posix()}" for p in sorted(DST.rglob("*")) if p.is_file() and p.name != "PACKET_SHA256SUMS.txt"]
(DST / "PACKET_SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="ascii")
print("STAGED", DST, len(sums), "files; HEAD", head)
