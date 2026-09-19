"""Stages the Gemini packet P031_M2_DESIGN_20260916: T2 documentary corroboration of the WP-P0-31 Milestone-2
DESIGN HALF (source census, mapping dry run, fixture designs) produced by the Lead under OD-20260916-P031-M2-Q1-Q6-1
(Q1 A). Idempotent; refuses while agy runs. The scratch stores are public repository data (no credential); the
three run reports are trimmed to their summaries (dispositions/seeds dropped) plus 12 sample dispositions each."""
import pathlib, shutil, hashlib, subprocess, sys, json, re
DST = pathlib.Path("C:/LAB/Tradingview_LAB_CLEAN/_gemini_packets_20260913/P031_M2_DESIGN_20260916")
DESIGN = pathlib.Path("C:/tmp/P031_M2_DESIGN_20260916")
RUN = pathlib.Path("C:/tmp/CLAUDE_P0_RUN_20260913")
CANON = pathlib.Path("C:/LAB/Tradingview_LAB_CLEAN")
CT13 = pathlib.Path("C:/CT13")
out = subprocess.run(["tasklist"], capture_output=True, text=True).stdout.lower()
if any(l.startswith("agy.exe") for l in out.splitlines()):
    print("REFUSE: agy running"); sys.exit(1)
if DST.exists() and (DST / "PACKET_SHA256SUMS.txt").exists():
    print("ALREADY STAGED (idempotent)", DST); sys.exit(0)
if DST.exists():
    shutil.rmtree(DST)
(DST / "subject").mkdir(parents=True); (DST / "sources").mkdir()
for n in ("P031_M2_SOURCE_CENSUS_20260916.md", "P031_M2_MAPPING_DRY_RUN_20260916.md", "P031_M2_FIXTURE_DESIGN_20260916.md",
          "census.json", "m2_census.py", "m2_dry_run.py", "table_4a_prime_PROPOSED.json"):
    shutil.copy2(DESIGN / n, DST / "subject" / n)
for run in ("run_as_ruled", "run_planted", "run_whatif_4a_prime"):
    rep = json.loads((DESIGN / run / "reconciliation_report.json").read_text(encoding="utf-8"))
    summary = {k: v for k, v in rep.items() if k not in ("dispositions", "seeds", "unknown_targets", "conflicts")}
    summary["full_report_sha256"] = (DESIGN / run / "reconciliation_report.json.sha256").read_text(encoding="ascii").strip()
    summary["disposition_count"] = len(rep["dispositions"]); summary["seed_count_check"] = len(rep["seeds"])
    summary["sample_dispositions_first_12"] = rep["dispositions"][:12]
    summary["sample_unknown_targets_first_6"] = rep["unknown_targets"][:6]
    summary["sample_conflicts_first_4"] = rep["conflicts"][:4]
    summary["seed_state_by_source_prefix"] = {}
    (DST / "subject" / f"{run}_SUMMARY.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
# sources: the fold (mapping tables + record types), the M2 scope packet, the ruling row, the four registry stores
# (public repo data; value distributions are what the census claims), the producer_spec value listing
fold = (CANON / "MTC_COMMAND_CENTER/11_TRIAGE/WAYFINDER_LIFECYCLE_FOLD_2026-08-23.md").read_text(encoding="utf-8").split("\n")
(DST / "sources/FOLD_section4_to_6.md").write_text("\n".join(fold[55:118]) + "\n", encoding="utf-8", newline="\n")
shutil.copy2(RUN / "P031_M2_SCOPE_PACKET_DRAFT_20260915.md", DST / "sources/P031_M2_SCOPE_PACKET_DRAFT_20260915.md")
dec = (CT13 / "DECISIONS.md").read_text(encoding="utf-8").split("\n")
rows = [l for l in dec if l.startswith("| OD-20260916-P031-M2-Q1-Q6-1") or l.startswith("| OD-20260914-P031-")]
(DST / "sources/DECISIONS_rows_P031.md").write_text("# Rows from C:/CT13/DECISIONS.md (verbatim)\n" + "\n".join(rows) + "\n", encoding="utf-8", newline="\n")
for n in ("STRATEGY_RESEARCH_REGISTRY.json", "VARIANT_LOG_REGISTRY.json", "TRIAGE_CANDIDATE_REGISTRY.json", "AI_QUANTLENS_VERDICT_REGISTRY.json"):
    shutil.copy2(DESIGN / "scratch_stores" / n, DST / "sources" / f"scratch_{n}")
lines = []
for p in sorted((DESIGN / "scratch_stores/producer_specs").rglob("producer_spec.json")):
    d = json.loads(p.read_text(encoding="utf-8"))
    lines.append(f"{p.relative_to(DESIGN / 'scratch_stores/producer_specs').as_posix()}  candidate_id={d.get('candidate_id')!r}  promotion_status={d.get('promotion_status')!r}")
(DST / "sources/producer_spec_promotion_status_listing.txt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
# the M1 ledger's vocabulary the design refers to (registrar transitions, schema CHECK)
led = subprocess.run(["git", "-C", "C:/tmp/P031_M1_20260913", "-c", "safe.directory=*", "show", "48bd70de:MTC_COMMAND_CENTER/03_QUANTLENS/tools/p031_lifecycle_ledger.py"], capture_output=True).stdout
(DST / "sources/p031_lifecycle_ledger_48bd70de_lines1-230.py").write_bytes(b"\n".join(led.split(b"\n")[:230]) + b"\n")
for p in DST.rglob("*"):
    if p.is_file() and p.suffix in (".md", ".txt", ".py", ".json"):
        txt = p.read_bytes().decode("utf-8", "replace")
        if re.search(r"[A-Za-z0-9._%+-]+@gmail\.com", txt):
            print("REFUSE: a mailbox address reached the packet", p.name); shutil.rmtree(DST); sys.exit(1)
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
sums = [f"{H(p)}  {p.relative_to(DST).as_posix()}" for p in sorted(DST.rglob("*")) if p.is_file() and p.name != "PACKET_SHA256SUMS.txt"]
(DST / "PACKET_SHA256SUMS.txt").write_text("\n".join(sums) + "\n", encoding="ascii")
print("STAGED", DST, len(sums), "files")
