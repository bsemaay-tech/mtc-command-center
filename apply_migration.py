from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
from collections import defaultdict
from datetime import datetime
from pathlib import Path


LEGACY = Path(r"C:\LAB\tradingview-lab")
TARGET = Path(r"C:\LAB\Tradingview_LAB_CLEAN")
DRAFT = Path(r"C:\LAB\MIGRATION_PLANNING_DRAFTS\Tradingview_LAB_CLEAN_PHASE0")
MANIFEST_DIR = TARGET / "docs" / "migration_manifests"

EXCLUDED_NAMES = {
    ".git",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".cache",
    ".venv",
    "venv",
    "dist",
    "build",
    "debug",
    ".tmp",
    "temp",
    "tmp",
    ".next",
    ".nuxt",
    ".parcel-cache",
    "coverage",
}
EXCLUDED_TOP_PROJECTS = {"SECONDBRAIN", "SECONDBRAIN_TEMP", "BUDGET APP"}
ROOT_SCRIPTS = ["add_htf_cols.py", "add_l12_cases.py", "mtc_bridge.mjs", "optimize.py", "parity_compare.py"]
HARDCODED_PATTERNS = [
    r"C:\LAB\tradingview-lab",
    r"C:/LAB/tradingview-lab",
    "01_MASTER TEMPLATE_V2",
    "06_QUANTLENS_LAB",
    "MTC_COMMAND_CENTER",
    "mtc_backtest",
    "110_MTC_BACKTEST_OPTİMİZASYON_DİZİNLERİ",
]

copy_manifest: list[dict[str, str]] = []
dedupe_manifest: list[dict[str, str]] = []
excluded_manifest: list[dict[str, str]] = []


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path: Path, root: Path = LEGACY) -> str:
    return str(path.relative_to(root)).replace("/", "\\")


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def is_excluded(path: Path, root: Path = LEGACY) -> tuple[bool, str]:
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        parts = path.parts
    if parts and parts[0] in EXCLUDED_TOP_PROJECTS:
        return True, "excluded unrelated top-level project"
    if path.name.startswith("~$"):
        return True, "excluded Office temporary lock file"
    if path.suffix.lower() in {".log", ".tmp"}:
        return True, "excluded generated log/temp file"
    for part in parts:
        if part in EXCLUDED_NAMES:
            return True, f"excluded generated/cache/temp folder: {part}"
    if len(parts) >= 2 and parts[0] == "external" and parts[1] == "traderspost-command-dash":
        return True, "external traderspost dashboard is out of scope for Phase 1"
    return False, ""


def copy_file(source: Path, target: Path, classification: str, note: str = "") -> None:
    excluded, reason = is_excluded(source)
    if excluded:
        excluded_manifest.append({"source": str(source), "target": str(target), "reason": reason})
        return
    ensure_parent(target)
    shutil.copy2(source, target)
    source_hash = sha256(source)
    target_hash = sha256(target)
    if source_hash != target_hash:
        raise RuntimeError(f"SHA256 mismatch after copy: {source} -> {target}")
    copy_manifest.append(
        {
            "source": str(source),
            "target": str(target),
            "bytes": str(source.stat().st_size),
            "source_sha256": source_hash,
            "target_sha256": target_hash,
            "classification": classification,
            "note": note,
        }
    )


def copy_tree(source: Path, target: Path, classification: str, skip_predicate=None) -> None:
    for root, dirnames, filenames in os.walk(source, topdown=True):
        root_path = Path(root)
        kept = []
        for dirname in dirnames:
            child = root_path / dirname
            excluded, reason = is_excluded(child)
            if excluded:
                excluded_manifest.append({"source": str(child), "target": str(target / child.relative_to(source)), "reason": reason})
                continue
            if skip_predicate and skip_predicate(child, True):
                excluded_manifest.append({"source": str(child), "target": str(target / child.relative_to(source)), "reason": "skipped by Phase 1 scope predicate"})
                continue
            kept.append(dirname)
        dirnames[:] = kept
        for filename in filenames:
            file_path = root_path / filename
            if skip_predicate and skip_predicate(file_path, False):
                excluded_manifest.append({"source": str(file_path), "target": str(target / file_path.relative_to(source)), "reason": "skipped by Phase 1 scope predicate"})
                continue
            copy_file(file_path, target / file_path.relative_to(source), classification)


def write_text(path: Path, text: str) -> None:
    ensure_parent(path)
    path.write_text(text, encoding="utf-8", newline="\n")


def slug_full(name: str) -> str:
    value = name.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value).strip("_")
    return value or "unnamed_strategy"


def collect_stg_sources() -> list[tuple[Path, str]]:
    specs = [
        (Path(r"01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\06_PROMOTED_TO_PARITY"), r"^QL_"),
        (Path(r"01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\research\strategy_batch_2026_05_03_AUDITED\strategies"), r"^\d+_"),
        (Path(r"01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\01_TRIAGED_CANDIDATES"), r"^QL_"),
        (Path(r"01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB\strategy_sandboxes"), r"^QLR_"),
    ]
    result: list[tuple[Path, str]] = []
    for bucket_rel, pattern in specs:
        bucket = LEGACY / bucket_rel
        if not bucket.exists():
            continue
        for child in sorted([p for p in bucket.iterdir() if p.is_dir()], key=lambda p: p.name.lower()):
            if re.match(pattern, child.name):
                result.append((child, str(bucket_rel)))
    return result


def v2_reports_canonical_map(reports_root: Path) -> dict[Path, Path]:
    files = [p for p in reports_root.rglob("*") if p.is_file() and not is_excluded(p)[0]]
    groups: defaultdict[str, list[Path]] = defaultdict(list)
    for path in files:
        groups[sha256(path)].append(path)
    canonical_by_file: dict[Path, Path] = {}
    for digest, group in groups.items():
        if len(group) <= 5:
            for path in group:
                canonical_by_file[path] = path
            continue
        canonical = sorted(group, key=lambda p: (p.stat().st_mtime, priority_score(p)), reverse=True)[0]
        for path in group:
            canonical_by_file[path] = canonical
            if path != canonical:
                dedupe_manifest.append(
                    {
                        "skipped_source": str(path),
                        "canonical_source": str(canonical),
                        "sha256": digest,
                        "bytes": str(path.stat().st_size),
                        "reason": "hash group count > 5; canonical is newest by mtime under highest-priority parent path",
                    }
                )
    return canonical_by_file


def priority_score(path: Path) -> int:
    text = rel(path)
    priorities = [
        r"MTC_COMMAND_CENTER",
        r"mtc_backtest",
        r"01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB",
        r"01_MASTER TEMPLATE_V2",
        r"reports",
    ]
    for index, prefix in enumerate(priorities):
        if text.startswith(prefix):
            return 100 - index
    return 0


def copy_v2_reports_dedup() -> None:
    source = LEGACY / r"01_MASTER TEMPLATE_V2\reports"
    if not source.exists():
        return
    target_root = TARGET / r"MTC_COMMAND_CENTER\01_MTC_PROJECT\reports"
    canonical_by_file = v2_reports_canonical_map(source)
    copied_canonicals: set[Path] = set()
    for file_path, canonical in canonical_by_file.items():
        if file_path != canonical:
            continue
        if canonical in copied_canonicals:
            continue
        copied_canonicals.add(canonical)
        copy_file(canonical, target_root / canonical.relative_to(source), "ACTIVE_KEEP_DEDUPED_REPORT", "canonical duplicate-prune copy")


def portable_duplicate_hashes_against_v2() -> set[str]:
    v2 = LEGACY / "01_MASTER TEMPLATE_V2"
    portable = v2 / "MTC_V2_PORTABLE_HANDOFF"
    hashes = set()
    for path in v2.rglob("*"):
        if not path.is_file() or portable in path.parents or is_excluded(path)[0]:
            continue
        hashes.add(sha256(path))
    return hashes


def copy_portable_handoff_dedup() -> None:
    source = LEGACY / r"01_MASTER TEMPLATE_V2\MTC_V2_PORTABLE_HANDOFF"
    if not source.exists():
        return
    target_root = TARGET / r"MTC_COMMAND_CENTER\01_MTC_PROJECT\handoff\MTC_V2_PORTABLE_HANDOFF"
    v2_hashes = portable_duplicate_hashes_against_v2()
    for path in source.rglob("*"):
        if not path.is_file() or is_excluded(path)[0]:
            continue
        digest = sha256(path)
        if digest in v2_hashes:
            dedupe_manifest.append(
                {
                    "skipped_source": str(path),
                    "canonical_source": str(LEGACY / "01_MASTER TEMPLATE_V2"),
                    "sha256": digest,
                    "bytes": str(path.stat().st_size),
                    "reason": "MTC_V2_PORTABLE_HANDOFF byte-identical duplicate against V2; V2 canonical kept",
                }
            )
            continue
        copy_file(path, target_root / path.relative_to(source), "MIGRATE_REWRITE_SHORT_UNIQUE_HANDOFF", "unique portable handoff file")


def hardcoded_path_todo() -> str:
    sections = ["# Hardcoded Path Rewrite TODO", "", "No paths were rewritten in Phase 1. Barış must approve rewrite policy after copy verification.", ""]
    mapping = {
        r"C:\LAB\tradingview-lab": r"C:\LAB\Tradingview_LAB_CLEAN",
        r"C:/LAB/tradingview-lab": r"C:/LAB/Tradingview_LAB_CLEAN",
        "01_MASTER TEMPLATE_V2": r"MTC_COMMAND_CENTER\01_MTC_PROJECT",
        "06_QUANTLENS_LAB": r"MTC_COMMAND_CENTER\03_QUANTLENS",
        "MTC_COMMAND_CENTER": "MTC_COMMAND_CENTER",
        "mtc_backtest": r"MTC_COMMAND_CENTER\02_MTC_BACKTEST",
        "110_MTC_BACKTEST_OPTİMİZASYON_DİZİNLERİ": r"MTC_COMMAND_CENTER\02_MTC_BACKTEST\data\optimization",
    }
    for script in ROOT_SCRIPTS:
        source = LEGACY / script
        sections.append(f"## {script}")
        if not source.exists():
            sections.append("- Missing in legacy source.")
            continue
        hits = []
        text = source.read_text(encoding="utf-8", errors="replace")
        for line_no, line in enumerate(text.splitlines(), start=1):
            matched = [pattern for pattern in HARDCODED_PATTERNS if pattern in line]
            if matched:
                for pattern in matched:
                    hits.append((line_no, pattern, line.strip(), mapping[pattern]))
        if not hits:
            sections.append("- No hardcoded path hits.")
            continue
        sections.append("| Line | Matched path | Current text | Proposed clean mapping |")
        sections.append("|---|---|---|---|")
        for line_no, pattern, line, proposed in hits:
            line = line.replace("|", "/")
            sections.append(f"| {line_no} | `{pattern}` | `{line}` | `{proposed}` |")
        sections.append("")
    return "\n".join(sections)


def create_ai_memory_files() -> None:
    write_text(
        TARGET / "AGENTS.md",
        "# AGENTS.md\n\nRead this file first, then read `MTC_COMMAND_CENTER\\_AI_MEMORY\\START_HERE.md`.\nUse token-efficient search before broad scans.\nDo not change trading logic, Pine logic, MTC strategy behavior, or TradingView parity without explicit approval.\nUpdate relevant handoff files before stopping after approved write sessions.\n",
    )
    stub = "Read `AGENTS.md` first.\nThen read `MTC_COMMAND_CENTER\\_AI_MEMORY\\START_HERE.md`.\nUse token-efficient workflow.\nUpdate handoff files before stopping.\nDo not scan the full repo unless required.\n"
    for name in ["CLAUDE.md", "GEMINI.md", ".chatgpt-instructions.md", ".cursorrules"]:
        write_text(TARGET / name, stub)
    write_text(TARGET / "README.md", "# TradingView LAB Clean\n\nClean Phase 1 workspace for TradingView, MTC, backtest/parity, and QuantLens work.\n")
    if (LEGACY / ".gitignore").exists():
        copy_file(LEGACY / ".gitignore", TARGET / ".gitignore", "ACTIVE_KEEP_CONFIG")
    if (LEGACY / ".gitattributes").exists():
        copy_file(LEGACY / ".gitattributes", TARGET / ".gitattributes", "ACTIVE_KEEP_CONFIG")

    memory = TARGET / r"MTC_COMMAND_CENTER\_AI_MEMORY"
    write_text(memory / "START_HERE.md", "# START_HERE\n\nRead order: `AGENTS.md`, this file, `GLOBAL_HANDOFF.md` if needed, `NEXT_STEPS.md`, then project handoff files.\n\nDo not change trading logic, Pine logic, MTC behavior, or parity checks without explicit approval.\n")
    write_text(memory / "GLOBAL_HANDOFF.md", "# GLOBAL_HANDOFF\n\nLast updated:\nUpdated by:\nActive project:\nCurrent objective:\nCurrent phase:\nCurrent blockers:\nWhere to continue:\nWarnings:\n")
    write_text(memory / "NEXT_STEPS.md", "# NEXT_STEPS\n\n## Immediate\n- Review Phase 1 verification output.\n- Decide hardcoded path rewrite policy.\n\n## Waiting On\n- Barış approval for post-copy path rewrites.\n")
    write_text(memory / "DECISIONS.md", "# DECISIONS\n\nD001 | Phase 1 | `MTC_COMMAND_CENTER` legacy source is canonical for clean command center copy.\n")
    write_text(memory / "ACTIVE_FILES.md", "# ACTIVE_FILES\n\n- `MTC_COMMAND_CENTER\\_AI_MEMORY\\START_HERE.md`\n- `MTC_COMMAND_CENTER\\02_MTC_BACKTEST\\hardcoded_path_rewrite_TODO.md`\n")
    write_text(memory / "DO_NOT_TOUCH.md", "# DO_NOT_TOUCH\n\n- Do not modify Pine logic without approval.\n- Do not modify MTC strategy behavior without approval.\n- Do not rewrite hardcoded paths until Barış approves rewrite policy.\n")
    write_text(memory / "SESSION_LOG.md", "# SESSION_LOG\n\n- Phase 1 migration copy executed from approved Phase 0 plan.\n")
    write_text(memory / "SESSION_LOCK.md", "# SESSION_LOCK\n\nStatus: unlocked\n")


def write_doc_reports() -> None:
    docs = TARGET / "docs"
    mapping = {
        "00_PHASE0_SUMMARY.md": "PHASE0_SUMMARY.md",
        "01_INVENTORY_REPORT.md": "INVENTORY_REPORT.md",
        "02_DEPENDENCY_AND_PATH_AUDIT.md": "DEPENDENCY_AND_PATH_AUDIT.md",
        "03_MIGRATION_PLAN.md": "MIGRATION_PLAN.md",
        "04_MIGRATION_MAP.md": "MIGRATION_MAP.md",
        "05_DEPRECATED_AND_EXCLUDED.md": "DEPRECATED_FILES.md",
        "06_ACTIVE_FILES.md": "ACTIVE_FILES.md",
        "07_DECISIONS_AND_DECISION_REQUESTS.md": "DECISIONS.md",
        "08_AI_MEMORY_DRAFT.md": "AI_MEMORY_DRAFT.md",
        "09_APPROVAL_REQUEST.md": "DECISION_REQUESTS.md",
    }
    for source_name, target_name in mapping.items():
        source = DRAFT / source_name
        if source.exists():
            copy_file(source, docs / target_name, "PHASE0_REPORT")
    if (DRAFT / "05_DEPRECATED_AND_EXCLUDED.md").exists():
        copy_file(DRAFT / "05_DEPRECATED_AND_EXCLUDED.md", docs / "EXCLUDED_PROJECTS.md", "PHASE0_REPORT")


def write_project_memory_templates() -> None:
    for rel_dir in [
        r"MTC_COMMAND_CENTER\01_MTC_PROJECT\_AI_MEMORY",
        r"MTC_COMMAND_CENTER\02_MTC_BACKTEST\_AI_MEMORY",
        r"MTC_COMMAND_CENTER\03_QUANTLENS\_AI_MEMORY",
    ]:
        folder = TARGET / rel_dir
        write_text(folder / "HANDOFF.md", "# HANDOFF\n\nLast updated:\nUpdated by:\nCurrent phase:\nCurrent status:\n\n## Active objective\n\n## Completed in last session\n\n## Current blockers\n\n## Next 3 actions\n1. \n2. \n3. \n\n## Files changed\n\n## Files to read next\n\n## Warnings\n\n## Do not do\n")
        write_text(folder / "NEXT_STEPS.md", "# NEXT_STEPS\n\n## Immediate\n1. Review Phase 1 verification.\n2. Approve or revise path rewrite policy.\n3. Continue only after Barış approval.\n")
        write_text(folder / "DECISIONS.md", "# DECISIONS\n\n")
        write_text(folder / "ACTIVE_FILES.md", "# ACTIVE_FILES\n\n")
    write_text(TARGET / r"MTC_COMMAND_CENTER\03_QUANTLENS\_AI_MEMORY\STRATEGY_REGISTRY.md", "# STRATEGY_REGISTRY\n\n| STG ID | Short name | Source | Bucket | Status file |\n|---|---|---|---|---|\n")


def write_status_template(path: Path, stg_id: str, source: Path) -> None:
    write_text(
        path,
        f"""# {stg_id} STATUS

Source video:
Source URL:
Current verdict:
Market:
Timeframe:
Strategy type:
Transcript status:
Intake status:
Enrichment status:
Pine status:
Backtest status:
Latest result:
Next action:
Do not repeat:
Related files:
- Source: `{source}`
""",
    )


def create_verify_script() -> None:
    script = r'''$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$target = "C:\LAB\Tradingview_LAB_CLEAN"
$legacy = "C:\LAB\tradingview-lab"
$manifestDir = Join-Path $target "docs\migration_manifests"
$result = [ordered]@{}
$result.target_tree_created = Test-Path -LiteralPath $target
$beforePath = Join-Path $manifestDir "legacy_git_status_before.txt"
$afterPath = Join-Path $manifestDir "legacy_git_status_after_verify.txt"
$before = if (Test-Path -LiteralPath $beforePath) { Get-Content -LiteralPath $beforePath -Raw -Encoding UTF8 } else { "" }
$after = git -C $legacy status --short | Out-String
Set-Content -LiteralPath $afterPath -Value $after -Encoding UTF8
$result.legacy_untouched_check = ($before.Trim() -eq $after.Trim())
$excludedNames = @("SECONDBRAIN","SECONDBRAIN_TEMP","BUDGET APP","node_modules","__pycache__",".git","debug",".pytest_cache",".venv","venv","dist","build",".tmp","temp","tmp")
$found = @()
foreach ($name in $excludedNames) {
  $found += Get-ChildItem -LiteralPath $target -Force -Recurse -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -eq $name } | Select-Object -ExpandProperty FullName
}
$dash = Join-Path $target "external\traderspost-command-dash"
if (Test-Path -LiteralPath $dash) { $found += $dash }
$result.excluded_folder_absent_check = ($found.Count -eq 0)
$result.excluded_folder_hits = @($found)
$copyManifest = Import-Csv -LiteralPath (Join-Path $manifestDir "copy_manifest.csv")
$mismatch = @()
foreach ($row in $copyManifest) {
  if (Test-Path -LiteralPath $row.target) {
    $hash = (Get-FileHash -LiteralPath $row.target -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($hash -ne $row.target_sha256.ToLowerInvariant()) { $mismatch += $row.target }
  } else {
    $mismatch += $row.target
  }
}
$result.copy_manifest_sha256_check = ($mismatch.Count -eq 0)
$result.copy_manifest_mismatches = @($mismatch)
$pineRows = @()
Get-ChildItem -LiteralPath $target -Recurse -File -Force -ErrorAction SilentlyContinue | Where-Object { $_.Extension -in @(".pine",".pinescript") -or $_.Name -like "*.pine.txt" } | ForEach-Object {
  $pineRows += [pscustomobject]@{ Path=$_.FullName; Bytes=$_.Length; SHA256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash }
}
$pineManifest = Join-Path $manifestDir "pine_sha256_manifest.csv"
$pineRows | Export-Csv -LiteralPath $pineManifest -NoTypeInformation -Encoding UTF8
$result.pine_file_count = $pineRows.Count
$dedupeManifest = Join-Path $manifestDir "deduplication_manifest.csv"
$dedupeRows = if (Test-Path -LiteralPath $dedupeManifest) { Import-Csv -LiteralPath $dedupeManifest } else { @() }
$result.deduplication_skipped_count = @($dedupeRows).Count
$result.mtc_command_center_manifest_exists = Test-Path -LiteralPath (Join-Path $manifestDir "mtc_command_center_sha256_manifest.csv")
$result.status = if ($result.target_tree_created -and $result.legacy_untouched_check -and $result.excluded_folder_absent_check -and $result.copy_manifest_sha256_check) { "PASS" } else { "FAIL" }
$json = $result | ConvertTo-Json -Depth 6
Set-Content -LiteralPath (Join-Path $manifestDir "verify_migration_result.json") -Value $json -Encoding UTF8
$json
if ($result.status -ne "PASS") { exit 1 }
'''
    write_text(TARGET / "verify_migration.ps1", script)


def main() -> None:
    if not LEGACY.exists():
        raise RuntimeError(f"Legacy repo missing: {LEGACY}")
    if TARGET.exists():
        raise RuntimeError(f"Target already exists; refusing to overwrite: {TARGET}")
    TARGET.mkdir(parents=True)
    MANIFEST_DIR.mkdir(parents=True)
    before = subprocess.check_output(["git", "-C", str(LEGACY), "status", "--short"], text=True, encoding="utf-8", errors="replace")
    write_text(MANIFEST_DIR / "legacy_git_status_before.txt", before)

    create_ai_memory_files()
    write_doc_reports()
    write_project_memory_templates()

    copy_tree(LEGACY / "MTC_COMMAND_CENTER", TARGET / "MTC_COMMAND_CENTER", "ACTIVE_KEEP_CANONICAL_MTC_COMMAND_CENTER")
    copy_tree(LEGACY / "mtc_backtest", TARGET / r"MTC_COMMAND_CENTER\02_MTC_BACKTEST", "ACTIVE_KEEP_BACKTEST")

    v2_source = LEGACY / "01_MASTER TEMPLATE_V2"
    def skip_v2(path: Path, is_dir: bool) -> bool:
        try:
            relative = rel(path, v2_source)
        except ValueError:
            return False
        first = relative.split("\\", 1)[0]
        return first in {"06_QUANTLENS_LAB", "MTC_V2_PORTABLE_HANDOFF", "reports", "Michael Automates"}

    copy_tree(v2_source, TARGET / r"MTC_COMMAND_CENTER\01_MTC_PROJECT", "ACTIVE_KEEP_MTC_PROJECT", skip_v2)
    copy_v2_reports_dedup()
    copy_portable_handoff_dedup()

    ql_source = LEGACY / r"01_MASTER TEMPLATE_V2\06_QUANTLENS_LAB"
    stg_source_set = {source for source, _bucket in collect_stg_sources()}
    def skip_ql(path: Path, is_dir: bool) -> bool:
        if is_dir and path in stg_source_set:
            return True
        return False
    copy_tree(ql_source, TARGET / r"MTC_COMMAND_CENTER\03_QUANTLENS", "ACTIVE_KEEP_QUANTLENS_PIPELINE", skip_ql)

    registry_rows = ["# STRATEGY_REGISTRY", "", "| STG ID | Short name | Source | Bucket | Status file |", "|---|---|---|---|---|"]
    for index, (source, bucket) in enumerate(collect_stg_sources(), start=1):
        stg_id = f"STG{index:03d}_{slug_full(source.name)}"
        target_dir = TARGET / "MTC_COMMAND_CENTER" / "03_QUANTLENS" / "strategies" / stg_id
        copy_tree(source, target_dir, "ACTIVE_KEEP_QUANTLENS_STRATEGY")
        write_status_template(target_dir / "STATUS.md", stg_id, source)
        if not (target_dir / "README.md").exists():
            write_text(target_dir / "README.md", f"# {stg_id}\n\nSource folder: `{source}`\n")
        registry_rows.append(f"| {stg_id} | {slug_full(source.name)} | `{source}` | `{bucket}` | `strategies\\{stg_id}\\STATUS.md` |")
    write_text(TARGET / r"MTC_COMMAND_CENTER\03_QUANTLENS\_AI_MEMORY\STRATEGY_REGISTRY.md", "\n".join(registry_rows) + "\n")

    for source_rel, target_rel, classification in [
        ("20_MODULES_REUSABLE", r"MTC_COMMAND_CENTER\04_SHARED\modules", "ACTIVE_KEEP_SHARED_MODULES"),
        ("30_PROMPTS", r"MTC_COMMAND_CENTER\04_SHARED\prompts", "ACTIVE_KEEP_SHARED_PROMPTS"),
        (r"tools\parity", r"MTC_COMMAND_CENTER\02_MTC_BACKTEST\tools\parity", "ACTIVE_KEEP_PARITY_TOOLS"),
        ("scripts", r"MTC_COMMAND_CENTER\02_MTC_BACKTEST\scripts", "ACTIVE_KEEP_SCRIPTS"),
        ("reports", r"MTC_COMMAND_CENTER\02_MTC_BACKTEST\reports", "ACTIVE_KEEP_REPORTS"),
    ]:
        source = LEGACY / source_rel
        if source.exists():
            copy_tree(source, TARGET / target_rel, classification)

    for script in ROOT_SCRIPTS:
        source = LEGACY / script
        if source.exists():
            copy_file(source, TARGET / "MTC_COMMAND_CENTER" / "02_MTC_BACKTEST" / script, "ACTIVE_KEEP_ROOT_BACKTEST_SCRIPT", "paths not rewritten")
    write_text(TARGET / r"MTC_COMMAND_CENTER\02_MTC_BACKTEST\hardcoded_path_rewrite_TODO.md", hardcoded_path_todo())

    create_verify_script()
    copy_file(DRAFT / "phase1_apply_migration.py", TARGET / "apply_migration.py", "MIGRATION_TOOL")

    with (MANIFEST_DIR / "copy_manifest.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target", "bytes", "source_sha256", "target_sha256", "classification", "note"])
        writer.writeheader()
        writer.writerows(copy_manifest)
    with (MANIFEST_DIR / "deduplication_manifest.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["skipped_source", "canonical_source", "sha256", "bytes", "reason"])
        writer.writeheader()
        writer.writerows(dedupe_manifest)
    with (MANIFEST_DIR / "excluded_manifest.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target", "reason"])
        writer.writeheader()
        writer.writerows(excluded_manifest)

    mtc_rows = [
        row for row in copy_manifest
        if row["source"].startswith(str(LEGACY / "MTC_COMMAND_CENTER")) and row["classification"] == "ACTIVE_KEEP_CANONICAL_MTC_COMMAND_CENTER"
    ]
    with (MANIFEST_DIR / "mtc_command_center_sha256_manifest.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target", "bytes", "source_sha256", "target_sha256", "classification", "note"])
        writer.writeheader()
        writer.writerows(mtc_rows)

    summary = {
        "created": datetime.now().isoformat(timespec="seconds"),
        "target": str(TARGET),
        "copied_files": len(copy_manifest),
        "dedupe_skipped_files": len(dedupe_manifest),
        "excluded_items": len(excluded_manifest),
        "mtc_command_center_files_verified": len(mtc_rows),
        "root_scripts_copied": [script for script in ROOT_SCRIPTS if (TARGET / "MTC_COMMAND_CENTER" / "02_MTC_BACKTEST" / script).exists()],
        "stg_count": len(collect_stg_sources()),
    }
    write_text(MANIFEST_DIR / "phase1_apply_summary.json", json.dumps(summary, indent=2, ensure_ascii=False))
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
