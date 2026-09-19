"""Builds the Gemini packet P012_RISK_PACKET_20260914_B: the CORRECTED owner packet (after lane P12FIX), the
correction disposition, the prior Gemini audit report (F-01..F-09) and every source the corrected packet cites.
Runs only when agy is idle. Idempotent: never rewrites a staged packet (the Gemini FS watcher must see no events)."""
import pathlib, shutil, hashlib, subprocess, sys, re, collections

DST = pathlib.Path("C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_RISK_PACKET_20260914_B")
SRC = pathlib.Path("C:/tmp/P012_RISK_20260914")
PRIOR = pathlib.Path("C:/tmp/P012_S16_REVIEWS_20260913/P012_RISK_PACKET_GEMINI")
TK = pathlib.Path("C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913")
PK = pathlib.Path("C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_S16_G5_ONLY/AUTHORITY/PATH_D")

out = subprocess.run(["tasklist"], capture_output=True, text=True).stdout.lower()
if any(l.startswith("agy.exe") for l in out.splitlines()):
    print("REFUSE: agy running"); sys.exit(1)
if DST.exists() and (DST / "PACKET_SHA256SUMS.txt").exists():
    print("ALREADY STAGED (idempotent; no rewrite so the FS watcher sees no events)", DST); sys.exit(0)
if DST.exists():
    shutil.rmtree(DST)
(DST / "subject").mkdir(parents=True)
(DST / "sources").mkdir()
(DST / "prior").mkdir()

# Subject: the corrected packet and the correction lane's own records.
for name in ("P012_PRODUCTION_ADMISSION_PACKET.md", "DISPOSITION_FIX1.md", "TASK.md", "TASK_FIX1.md", "SHA256SUMS.txt"):
    shutil.copy2(SRC / name, DST / "subject" / name)
# Prior audit (attempt 2, verdict REQUEST_CHANGES) so the delta can be judged against the exact finding text.
shutil.copy2(PRIOR / "REPORT_RESPONSE_UTF8.md", DST / "prior" / "GEMINI_AUDIT_1_REPORT.md")
shutil.copy2(PRIOR / "LEAD_ADJUDICATION.md", DST / "prior" / "LEAD_ADJUDICATION_AUDIT_1.md")

# Sources: every file the corrected packet cites, copied byte-for-byte (the master plan as a line-numbered excerpt).
COPIES = {
    "C:/Users/BarışSemaay/Documents/Codex/2026-09-11/11-2/outputs/P012_INDEPENDENT_READINESS/03_PRODUCTION_CLOSURE_MATRIX.md": "03_PRODUCTION_CLOSURE_MATRIX.md",
    "C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/P012_ACCEPTANCE_AMENDMENT_20260913.md": "P012_ACCEPTANCE_AMENDMENT_20260913.md",
    "C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_S16_G5_ONLY/AUTHORITY/PATH_D/PATH_D_DECISION_PACKET.md": "PATH_D_DECISION_PACKET.md",
    "C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P012_S16_G5_ONLY/AUTHORITY/PATH_D/PATH_D_DECISION_SIGNED_20260912.md": "PATH_D_DECISION_SIGNED_20260912.md",
    "C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/REVIEW_POLICY.md": "REVIEW_POLICY.md",
    "C:/CT13/IBKR_PAPER_BRIDGE/docs/06_HYPERLIQUID_SETUP.md": "06_HYPERLIQUID_SETUP.md",
    "C:/CT13/IBKR_PAPER_BRIDGE/deploy/linux/README.md": "DEPLOY_LINUX_README.md",
    "C:/CT13/IBKR_PAPER_BRIDGE/deploy/linux/COMMANDS.md": "COMMANDS.md",
    "C:/CT13/MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/CLAUDE_TAKEOVER_20260913/P012_RATIFICATION_APPLIED_20260914/LEAD_NOTE.md": "P012_RATIFICATION_LEAD_NOTE.md",
    "C:/tmp/P012_RISK_20260914/TASK.md": "(subject/TASK.md)",
}
EXCERPT_SRC = "C:/CT13/MTC_COMMAND_CENTER/11_TRIAGE/MASTER_WORK_PACKAGE_AND_PARALLEL_DELIVERY_PLAN_2026-08-22.md"
for src, name in COPIES.items():
    if name.startswith("("):
        continue
    shutil.copy2(src, DST / "sources" / name)

# Citation census from the corrected packet: which original path:line the packet cites, mapped to the copies.
packet = (SRC / "P012_PRODUCTION_ADMISSION_PACKET.md").read_text(encoding="utf-8")
cites = re.findall(r"`([A-Za-z]:/[^`]+?):(\d+)`", packet)
per_file = collections.defaultdict(set)
for p, n in cites:
    per_file[p].add(int(n))

# Master plan: 335 KB / 1106 lines -> stage only the cited lines with +-6 lines of context, each line prefixed by its
# ORIGINAL line number, so every citation into it can be opened without shipping the whole file.
plan_lines = pathlib.Path(EXCERPT_SRC).read_text(encoding="utf-8").split("\n")
wanted = set()
for n in sorted(per_file.get(EXCERPT_SRC, ())):
    wanted.update(range(max(1, n - 6), min(len(plan_lines), n + 6) + 1))
excerpt = ["# EXCERPT of " + EXCERPT_SRC,
           "# Each line below is prefixed with its ORIGINAL line number ('NNNN: '). Only the cited lines and +-6 lines of context are staged; a gap marker shows omitted ranges.",
           ""]
prev = None
for n in sorted(wanted):
    if prev is not None and n != prev + 1:
        excerpt.append(f"...... [lines {prev + 1}-{n - 1} omitted] ......")
    excerpt.append(f"{n:04d}: {plan_lines[n - 1]}")
    prev = n
(DST / "sources" / "MASTER_WORK_PACKAGE_excerpt.md").write_text("\n".join(excerpt) + "\n", encoding="utf-8")

# FILE_MAP.md: original cited path -> staged copy, with the exact cited line numbers (so the auditor opens each one).
rows = ["# FILE_MAP — cited original path -> staged copy (line numbers are the ORIGINAL file's; copies are byte-identical, the master plan is a line-numbered excerpt)", ""]
total = 0
for p in sorted(per_file, key=lambda k: -len(per_file[k])):
    ns = sorted(per_file[p]); total += len(ns)
    if p == EXCERPT_SRC:
        copy = "sources/MASTER_WORK_PACKAGE_excerpt.md (line-numbered excerpt)"
    else:
        name = COPIES.get(p)
        copy = "subject/TASK.md" if name == "(subject/TASK.md)" else (f"sources/{name}" if name else "NOT STAGED — report as NOT VERIFIED")
    rows.append(f"- `{p}` -> `{copy}`; {len(ns)} distinct cited lines: {', '.join(map(str, ns))}")
rows += ["", f"Total citations in the packet: {len(cites)} (distinct path:line pairs: {total}).",
         "Other prose paths inside copied documents are provenance text, never files to open."]
(DST / "FILE_MAP.md").write_text("\n".join(rows) + "\n", encoding="utf-8")

H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
sums = [f"{H(p)}  {p.relative_to(DST).as_posix()}" for p in sorted(DST.rglob("*")) if p.is_file() and p.name != "PACKET_SHA256SUMS.txt"]
(DST / "PACKET_SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="ascii")
print("STAGED", DST, len(sums), "files")
