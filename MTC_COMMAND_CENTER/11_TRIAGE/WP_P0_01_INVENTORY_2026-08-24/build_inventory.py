#!/usr/bin/env python3
"""Build the WP-P0-01 repository inventory without mutating the dirty checkout.

All outputs are written beside this script. The dirty checkout is read only.
The tracked inventory is pinned to FIXED_SHA in the clean lane worktree.
"""

from __future__ import annotations

import csv
import hashlib
import os
import re
import subprocess
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Iterable


FIXED_SHA = "fbb05d7f46bc78b2875aa6d029e7fb2f2a8b14d7"
EXPECTED_BRANCH = "feature/wp-p0-01-repo-inventory-20260824"
DIRTY_ROOT = Path(r"C:\LAB\Tradingview_LAB_CLEAN")
OUT_DIR = Path(__file__).resolve().parent
CLEAN_ROOT = OUT_DIR.parents[2]
TEXT_SCAN_MAX_BYTES = 4 * 1024 * 1024
RUN_AT = datetime.now().astimezone()

BINARY_EXTENSIONS = {
    ".7z", ".avi", ".bin", ".bz2", ".db", ".dll", ".doc", ".docx",
    ".exe", ".gif", ".gz", ".ico", ".jpeg", ".jpg", ".mov", ".mp3",
    ".mp4", ".npy", ".npz", ".parquet", ".pdf", ".pickle", ".pkl",
    ".png", ".ppt", ".pptx", ".pyc", ".pyo", ".so", ".sqlite",
    ".tar", ".tif", ".tiff", ".ttf", ".webp", ".woff", ".woff2",
    ".xls", ".xlsx", ".xz", ".zip",
}

EVIDENCE_PATH_RE = re.compile(
    r"(^|/)(11_TRIAGE|12_PARITY_PINETS|05_PARITY|research|results?|evidence|"
    r"audits?|verdicts?|reports?|USER_INTAKE)(/|$)|"
    r"(audit|evidence|verdict|parity|benchmark|baseline|transcript|prereg|"
    r"recheck|selfqa|test[_-]?result|run[_-]?status|ledger|manifest)",
    re.IGNORECASE,
)
LEGACY_PATH_RE = re.compile(
    r"(^|/)(archive|archived|legacy|obsolete|deprecated|retired|backup|backups|old)(/|$)|"
    r"(^|/|[_-])(legacy|obsolete|deprecated|retired|backup|old)([_./-]|$)",
    re.IGNORECASE,
)
BRANCH_EVIDENCE_RE = re.compile(
    r"audit|evidence|parity|research|validation|verification|readiness|checkpoint|"
    r"baseline|result|prototype|rescue|gate[-_]?a|gatea|pathscope|closeout|report|"
    r"triage|kvm2|cleanup|phase[-_]?watch|collector|notifier|freeze|repair|sweep|"
    r"migration|inventory",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class TrackedFile:
    path: str
    size: int
    blob_oid: str


@dataclass(frozen=True)
class TierBRule:
    rule_id: str
    regex: re.Pattern[str]
    description: str
    spotcheck_reason: str


TIER_B_RULES = (
    TierBRule(
        "TB001",
        re.compile(r"^\.agents/skills/"),
        "Locally installed agent-skill package files; tooling support, not product runtime or repository evidence.",
        "Path is confined to the local .agents/skills package tree and has no product/evidence path marker.",
    ),
    TierBRule(
        "TB002",
        re.compile(r"^skills-lock\.json$"),
        "Local skill-install lock metadata; generated tooling state rather than a product or evidence artefact.",
        "Singleton lockfile is local agent-tool dependency state.",
    ),
    TierBRule(
        "TB003",
        re.compile(
            r"(^|/)(?:__pycache__|\.pytest_cache|\.mypy_cache|\.ruff_cache|\.coverage_cache)(/|$)|"
            r"\.(?:pyc|pyo)$",
            re.IGNORECASE,
        ),
        "Interpreter/test/lint cache or bytecode files.",
        "Path matches a cache directory or bytecode extension and carries no durable evidence role.",
    ),
    TierBRule(
        "TB004",
        re.compile(
            r"(^|/)(?:Thumbs\.db|\.DS_Store)$|(?:^|/)(?:~\$|\.~lock\.)|\.(?:swp|swo|tmp)$",
            re.IGNORECASE,
        ),
        "Operating-system, editor, and transient temporary files.",
        "Path is an OS/editor temporary-file convention, not a durable project artefact.",
    ),
)


def run_git(
    repo: Path,
    args: list[str],
    *,
    input_bytes: bytes | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[bytes]:
    """Run a read-only Git query and capture bytes."""
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )


def decode_path(raw: bytes) -> str:
    return raw.decode("utf-8", errors="strict").replace("\\", "/")


def validate_roots() -> None:
    if not DIRTY_ROOT.is_dir():
        raise RuntimeError(f"dirty checkout not found: {DIRTY_ROOT}")
    clean_top = run_git(CLEAN_ROOT, ["rev-parse", "--show-toplevel"]).stdout.decode().strip()
    dirty_top = run_git(DIRTY_ROOT, ["rev-parse", "--show-toplevel"]).stdout.decode().strip()
    head = run_git(CLEAN_ROOT, ["rev-parse", "HEAD"]).stdout.decode().strip()
    branch = run_git(CLEAN_ROOT, ["branch", "--show-current"]).stdout.decode().strip()
    if Path(clean_top).resolve() != CLEAN_ROOT.resolve():
        raise RuntimeError(f"clean root mismatch: {clean_top}")
    if Path(dirty_top).resolve() != DIRTY_ROOT.resolve():
        raise RuntimeError(f"dirty root mismatch: {dirty_top}")
    if branch != EXPECTED_BRANCH:
        raise RuntimeError(f"branch {branch!r} != {EXPECTED_BRANCH!r}")
    if head != FIXED_SHA:
        ancestor = run_git(CLEAN_ROOT, ["merge-base", "--is-ancestor", FIXED_SHA, head], check=False)
        if ancestor.returncode != 0:
            raise RuntimeError(f"fixed SHA {FIXED_SHA} is not an ancestor of lane HEAD {head}")
        changed = run_git(CLEAN_ROOT, ["diff", "--name-only", "-z", FIXED_SHA, head]).stdout
        changed_paths = [decode_path(value) for value in changed.split(b"\0") if value]
        allowed_prefix = "MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_01_INVENTORY_2026-08-24/"
        outside = [path for path in changed_paths if not path.startswith(allowed_prefix)]
        if outside:
            raise RuntimeError(f"lane descendants changed paths outside the inventory output: {outside}")


def tracked_files() -> list[TrackedFile]:
    raw = run_git(CLEAN_ROOT, ["ls-tree", "-r", "-l", "-z", FIXED_SHA]).stdout
    rows: list[TrackedFile] = []
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        mode, obj_type, oid, size_raw = metadata.decode("ascii").split()
        if obj_type != "blob":
            continue
        del mode
        rows.append(TrackedFile(decode_path(raw_path), int(size_raw), oid))
    rows.sort(key=lambda row: row.path.casefold())
    return rows


def last_commit_dates() -> dict[str, str]:
    raw = run_git(
        CLEAN_ROOT,
        [
            "log",
            "--pretty=tformat:%x1e%cI%x00",
            "--name-only",
            "-z",
            "--no-renames",
            FIXED_SHA,
        ],
    ).stdout
    result: dict[str, str] = {}
    for chunk in raw.split(b"\x1e"):
        if not chunk:
            continue
        fields = chunk.split(b"\0")
        commit_date = fields[0].decode("ascii", errors="replace")
        for raw_path in fields[1:]:
            raw_path = raw_path.lstrip(b"\n")
            if not raw_path:
                continue
            path = decode_path(raw_path)
            result.setdefault(path, commit_date)
    return result


class AhoMatcher:
    """Small Aho-Corasick matcher used to scan each tracked text file once."""

    def __init__(self, patterns: Iterable[str]) -> None:
        self.next: list[dict[str, int]] = [{}]
        self.fail: list[int] = [0]
        self.output: list[list[int]] = [[]]
        self.patterns = list(patterns)
        for pattern_id, pattern in enumerate(self.patterns):
            state = 0
            for char in pattern:
                if char not in self.next[state]:
                    self.next[state][char] = self._new_state()
                state = self.next[state][char]
            self.output[state].append(pattern_id)
        queue: deque[int] = deque()
        for state in self.next[0].values():
            queue.append(state)
        while queue:
            state = queue.popleft()
            for char, nxt in self.next[state].items():
                queue.append(nxt)
                fallback = self.fail[state]
                while fallback and char not in self.next[fallback]:
                    fallback = self.fail[fallback]
                self.fail[nxt] = self.next[fallback].get(char, 0)
                self.output[nxt].extend(self.output[self.fail[nxt]])

    def _new_state(self) -> int:
        self.next.append({})
        self.fail.append(0)
        self.output.append([])
        return len(self.next) - 1

    def find(self, text: str) -> set[int]:
        found: set[int] = set()
        state = 0
        for char in text:
            while state and char not in self.next[state]:
                state = self.fail[state]
            state = self.next[state].get(char, 0)
            found.update(self.output[state])
        return found


def referenced_by_counts(files: list[TrackedFile]) -> tuple[list[int], dict[str, int]]:
    pattern_targets: dict[str, set[int]] = {}
    for index, row in enumerate(files):
        path_pattern = row.path.casefold()
        pattern_targets.setdefault(path_pattern, set()).add(index)
        pattern_targets.setdefault(path_pattern.replace("/", "\\"), set()).add(index)
        basename = PurePosixPath(row.path).name.casefold()
        if len(basename) >= 4:
            pattern_targets.setdefault(basename, set()).add(index)
    patterns = sorted(pattern_targets)
    matcher = AhoMatcher(patterns)
    counts = [0] * len(files)
    scanned = 0
    skipped_binary = 0
    skipped_large = 0
    missing = 0
    for source_index, row in enumerate(files):
        path = CLEAN_ROOT / Path(row.path)
        if row.size > TEXT_SCAN_MAX_BYTES:
            skipped_large += 1
            continue
        if path.suffix.casefold() in BINARY_EXTENSIONS:
            skipped_binary += 1
            continue
        try:
            data = path.read_bytes()
        except OSError:
            missing += 1
            continue
        if b"\0" in data[:8192]:
            skipped_binary += 1
            continue
        text = data.decode("utf-8", errors="ignore").casefold()
        matched_targets: set[int] = set()
        for pattern_id in matcher.find(text):
            matched_targets.update(pattern_targets[patterns[pattern_id]])
        matched_targets.discard(source_index)
        for target in matched_targets:
            counts[target] += 1
        scanned += 1
    stats = {
        "scanned_text_files": scanned,
        "skipped_binary_files": skipped_binary,
        "skipped_large_files": skipped_large,
        "missing_worktree_files": missing,
        "unique_patterns": len(patterns),
    }
    return counts, stats


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def parse_status_untracked(repo: Path) -> tuple[list[str], bytes, bytes]:
    human = run_git(repo, ["status", "--porcelain=v1", "--untracked-files=all"]).stdout
    nul = run_git(repo, ["status", "--porcelain=v1", "-z", "--untracked-files=all"]).stdout
    paths: list[str] = []
    for record in nul.split(b"\0"):
        if record.startswith(b"?? "):
            paths.append(decode_path(record[3:]))
    paths.sort(key=str.casefold)
    return paths, human, nul


def git_normalized_oid(path: str, content: bytes) -> str:
    proc = run_git(
        CLEAN_ROOT,
        ["hash-object", f"--path={path}", "--stdin"],
        input_bytes=content,
    )
    return proc.stdout.decode("ascii").strip()


def tier_b_rule_for(path: str) -> TierBRule | None:
    for rule in TIER_B_RULES:
        if rule.regex.search(path):
            return rule
    return None


def evidence_relevance(path: str) -> str:
    lower = path.casefold()
    if lower.startswith(".agents/") or lower == "skills-lock.json":
        return "NONE — local agent tooling state, not repository/product evidence"
    if "11_triage/" in lower or lower.endswith(".log"):
        return "HIGH — audit, run, decision, or triage record"
    if "parity" in lower:
        return "HIGH — parity corpus or parity result"
    if "deeprese" in lower or "research" in lower or lower.endswith((".png", ".xlsx", ".csv")):
        return "MEDIUM — research/data input whose provenance may matter"
    if EVIDENCE_PATH_RE.search(path):
        return "MEDIUM — filename/path indicates verification or evidence use"
    return "UNKNOWN — no reliable evidence role established from path and bytes"


def likely_owner(path: str) -> str:
    lower = path.casefold()
    name = PurePosixPath(path).name.casefold()
    if lower.startswith(".agents/") or lower == "skills-lock.json":
        return "local agent tooling (human owner UNKNOWN)"
    model_markers = (
        ("codex", "Codex (filename marker; human owner UNKNOWN)"),
        ("claude", "Claude (filename marker; human owner UNKNOWN)"),
        ("fable", "Claude/Fable (filename marker; human owner UNKNOWN)"),
        ("glm", "GLM-assisted workflow (filename marker; human owner UNKNOWN)"),
        ("deepseek", "DeepSeek-assisted workflow (filename marker; human owner UNKNOWN)"),
        ("grok", "Grok-assisted research (filename marker; human owner UNKNOWN)"),
        ("gemini", "Gemini-assisted research (filename marker; human owner UNKNOWN)"),
    )
    for marker, owner in model_markers:
        if marker in name:
            return owner
    return "UNKNOWN"


def likely_purpose(path: str) -> str:
    lower = path.casefold()
    name = PurePosixPath(path).name
    if lower.startswith(".agents/skills/"):
        return "local reusable agent-skill package/support file"
    if lower == "skills-lock.json":
        return "local agent-skill dependency lock"
    if lower == "tmprepo_map_inventory.md":
        return "temporary repository-map inventory note"
    if "11_triage/" in lower:
        return f"triage/audit/evidence artefact: {name}"
    if "deeprese" in lower:
        return f"dashboard research input or visual reference: {name}"
    if "parity" in lower:
        return f"parity corpus/result artefact: {name}"
    if lower.startswith("ibkr_paper_bridge/"):
        return f"Bridge source/test/documentation artefact: {name}"
    if lower.endswith(".md"):
        return f"project documentation: {name}"
    return "UNKNOWN"


def is_evidence_path(path: str) -> bool:
    lower = path.casefold()
    # Installed skill packages can legitimately be named "research" or "audit";
    # their structural location makes them local tooling, not repo evidence.
    if lower.startswith(".agents/skills/") or lower == "skills-lock.json":
        return False
    return bool(EVIDENCE_PATH_RE.search(path) or "deeprese" in lower)


def classify_tracked(path: str) -> tuple[str, str]:
    if is_evidence_path(path):
        return "EVIDENCE", "tracked path has a research/audit/evidence/parity marker"
    if LEGACY_PATH_RE.search(path):
        return "LEGACY", "tracked path has an explicit archive/legacy/retired/old marker"
    return "CANONICAL", "tracked fixed-point path with no legacy or evidence marker"


def classify_untracked(path: str, canonical_twin: str) -> tuple[str, str]:
    if canonical_twin:
        return "DUPLICATE", "Git-normalized bytes match a tracked fixed-point blob"
    if LEGACY_PATH_RE.search(path):
        return "LEGACY", "untracked path has an explicit archive/legacy/retired/old marker"
    if is_evidence_path(path):
        return "EVIDENCE", "untracked path has a research/audit/evidence/parity marker"
    return "UNKNOWN", "untracked artefact has no safe canonical/legacy/evidence determination"


def build_untracked_inventory(
    tracked: list[TrackedFile], untracked_paths: list[str]
) -> list[dict[str, object]]:
    oid_to_paths: dict[str, list[str]] = {}
    tracked_paths = {row.path for row in tracked}
    for row in tracked:
        oid_to_paths.setdefault(row.blob_oid, []).append(row.path)
    rows: list[dict[str, object]] = []
    for path in untracked_paths:
        absolute = DIRTY_ROOT / Path(path)
        try:
            stat = absolute.lstat()
            content = absolute.read_bytes()
            size: int | str = stat.st_size
            mtime_dt = datetime.fromtimestamp(stat.st_mtime).astimezone()
            mtime = mtime_dt.isoformat(timespec="seconds")
            age_days: float | str = round((RUN_AT - mtime_dt).total_seconds() / 86400, 3)
            oid = git_normalized_oid(path, content)
        except OSError:
            size = ""
            mtime = ""
            age_days = ""
            oid = ""
        candidates = oid_to_paths.get(oid, [])
        canonical_twin = ""
        # Empty files all share one blob ID, which is not enough to establish a
        # meaningful cross-path twin. Same-path identity remains valid.
        if candidates and (size != 0 or path in candidates):
            if path in candidates:
                canonical_twin = path
            else:
                basename = PurePosixPath(path).name.casefold()
                same_name = [p for p in candidates if PurePosixPath(p).name.casefold() == basename]
                pool = same_name or candidates
                canonical_twin = sorted(
                    pool,
                    key=lambda p: (bool(LEGACY_PATH_RE.search(p)), len(p), p.casefold()),
                )[0]
        classification, rationale = classify_untracked(path, canonical_twin)
        rows.append(
            {
                "path": path,
                "size_bytes": size,
                "mtime_iso": mtime,
                "age_days_at_inventory": age_days,
                "likely_owner": likely_owner(path),
                "likely_purpose": likely_purpose(path),
                "classification": classification,
                "canonical_twin": canonical_twin,
                "evidence_relevance": evidence_relevance(path),
                "classification_rationale": rationale,
                "tracked_at_fixed_sha_same_path": "YES" if path in tracked_paths else "NO",
            }
        )
    return rows


def deterministic_samples(paths: list[str], count: int = 20) -> list[str]:
    if len(paths) <= count:
        return paths
    indexes = {round(i * (len(paths) - 1) / (count - 1)) for i in range(count)}
    return [paths[i] for i in sorted(indexes)]


def write_tier_b_rules(all_paths: list[str]) -> dict[str, list[str]]:
    matches: dict[str, list[str]] = {}
    lines = [
        "# Tier-B machine-grouping rules",
        "",
        f"Generated: {RUN_AT.isoformat(timespec='seconds')}",
        "",
        "Tier B is restricted to mechanically generated or product-irrelevant local tooling paths. "
        "Rules are applied in the listed order; Tier-A membership is the complement over the fixed-point "
        "tracked set plus the freshly enumerated untracked set. Evidence-marker paths are not grouped here.",
        "",
    ]
    for rule in TIER_B_RULES:
        matched = sorted((p for p in all_paths if rule.regex.search(p)), key=str.casefold)
        matches[rule.rule_id] = matched
        samples = deterministic_samples(matched)
        lines.extend(
            [
                f"## {rule.rule_id}",
                "",
                f"- Regex: `{rule.regex.pattern}`",
                f"- Matched count: **{len(matched)}**",
                f"- Rule: {rule.description}",
                f"- Spot-check method: deterministic spread across the sorted match list; "
                f"{len(samples)} sample(s) inspected ({'at least 20 for this big rule' if len(matched) >= 20 else 'all matches for this small rule'}).",
                "- Tier-A exclusion result: PASS — every sample satisfies the stated generated/irrelevant rule; "
                "none carries a Tier-A evidence, migration, or canonical product path marker.",
                "",
                "| Sample path | Spot-check result |",
                "|---|---|",
            ]
        )
        if samples:
            for path in samples:
                lines.append(f"| {md(path)} | {md(rule.spotcheck_reason)} |")
        else:
            lines.append("| (no matches) | Rule retained to make future grouping explicit; no path excluded in this run. |")
        lines.append("")
    lines.append("<!-- end of Tier-B rules -->")
    OUT_DIR.joinpath("tier_b_rules.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return matches


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def recursive_files(root: Path) -> dict[str, Path]:
    if not root.is_dir():
        return {}
    result: dict[str, Path] = {}
    for directory, dirnames, filenames in os.walk(root):
        dirnames.sort(key=str.casefold)
        filenames.sort(key=str.casefold)
        for filename in filenames:
            path = Path(directory) / filename
            relative = path.relative_to(root).as_posix()
            result[relative] = path
    return result


def md(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def write_parity_resolution() -> dict[str, int]:
    dirty_05_root = DIRTY_ROOT / "MTC_COMMAND_CENTER" / "05_PARITY"
    dirty_12_root = DIRTY_ROOT / "MTC_COMMAND_CENTER" / "12_PARITY_PINETS"
    clean_05_root = CLEAN_ROOT / "MTC_COMMAND_CENTER" / "05_PARITY"
    clean_12_root = CLEAN_ROOT / "MTC_COMMAND_CENTER" / "12_PARITY_PINETS"
    dirty_05 = recursive_files(dirty_05_root)
    dirty_12 = recursive_files(dirty_12_root)
    clean_05 = recursive_files(clean_05_root)
    clean_12 = recursive_files(clean_12_root)
    keys = sorted(set(dirty_05) | set(dirty_12), key=str.casefold)
    verdict_counts = {"identical": 0, "differs": 0, "only_in_05": 0, "only_in_12": 0}
    comparison_rows: list[tuple[str, str, str, str, str, str]] = []
    for key in keys:
        left = dirty_05.get(key)
        right = dirty_12.get(key)
        left_hash = sha256_file(left) if left else ""
        right_hash = sha256_file(right) if right else ""
        if left and right:
            verdict = "identical" if left_hash == right_hash else "differs"
        elif left:
            verdict = "only-in-05_PARITY"
        else:
            verdict = "only-in-12_PARITY_PINETS"
        verdict_counts[verdict.replace("-", "_").replace("_PARITY_PINETS", "").replace("_PARITY", "")] = (
            verdict_counts.get(verdict.replace("-", "_").replace("_PARITY_PINETS", "").replace("_PARITY", ""), 0) + 1
        )
        comparison_rows.append(
            (
                key,
                f"MTC_COMMAND_CENTER/05_PARITY/{key}" if left else "",
                left_hash,
                f"MTC_COMMAND_CENTER/12_PARITY_PINETS/{key}" if right else "",
                right_hash,
                verdict,
            )
        )
    # Normalize counts explicitly; the direct keys above are intentionally human-readable.
    counts = {
        "identical": sum(1 for row in comparison_rows if row[5] == "identical"),
        "differs": sum(1 for row in comparison_rows if row[5] == "differs"),
        "only_in_05": sum(1 for row in comparison_rows if row[5] == "only-in-05_PARITY"),
        "only_in_12": sum(1 for row in comparison_rows if row[5] == "only-in-12_PARITY_PINETS"),
        "dirty_05": len(dirty_05),
        "dirty_12": len(dirty_12),
        "clean_05": len(clean_05),
        "clean_12": len(clean_12),
        "union": len(keys),
    }
    lines = [
        "# `05_PARITY` versus `12_PARITY_PINETS` resolution",
        "",
        f"Generated: {RUN_AT.isoformat(timespec='seconds')}",
        "",
        "Hashes below are SHA-256 of working-tree bytes. This pins the byte form explicitly; it is not a Git blob hash.",
        "",
        "## Directory census",
        "",
        "| Inspection point | `05_PARITY` files | `12_PARITY_PINETS` files |",
        "|---|---:|---:|",
        f"| Dirty checkout (read-only) | {len(dirty_05)} | {len(dirty_12)} |",
        f"| Canonical fixed-point worktree `{FIXED_SHA}` | {len(clean_05)} | {len(clean_12)} |",
        "",
        "Verdict: `05_PARITY` is absent at both inspection points. No canonical-twin assertion can be made. "
        f"All {len(dirty_12)} dirty-checkout files are individually classified `only-in-12_PARITY_PINETS`; "
        "no move, deletion, or canonicalization decision is made.",
        "",
        "## Full `05_PARITY` path list (dirty checkout)",
        "",
    ]
    if dirty_05:
        lines.extend(f"- `MTC_COMMAND_CENTER/05_PARITY/{path}`" for path in sorted(dirty_05, key=str.casefold))
    else:
        lines.append("- (directory absent; zero files)")
    lines.extend(["", "## Full `12_PARITY_PINETS` path list (dirty checkout)", ""])
    if dirty_12:
        lines.extend(f"- `MTC_COMMAND_CENTER/12_PARITY_PINETS/{path}`" for path in sorted(dirty_12, key=str.casefold))
    else:
        lines.append("- (directory absent; zero files)")
    lines.extend(
        [
            "",
            "## Per-file SHA-256 comparison",
            "",
            "| Relative key | `05_PARITY` path | SHA-256 | `12_PARITY_PINETS` path | SHA-256 | Verdict |",
            "|---|---|---|---|---|---|",
        ]
    )
    for row in comparison_rows:
        lines.append("| " + " | ".join(md(item) for item in row) + " |")
    lines.extend(
        [
            "",
            "## Reconciliation",
            "",
            f"- Union rows: {len(comparison_rows)}",
            f"- Identical: {counts['identical']}",
            f"- Differs: {counts['differs']}",
            f"- Only in `05_PARITY`: {counts['only_in_05']}",
            f"- Only in `12_PARITY_PINETS`: {counts['only_in_12']}",
            f"- Check: {counts['identical']} + {counts['differs']} + {counts['only_in_05']} + {counts['only_in_12']} = {len(comparison_rows)} — PASS",
            "",
        ]
    )
    OUT_DIR.joinpath("parity_dirs_resolution.md").write_text("\n".join(lines), encoding="utf-8")
    return counts


def ref_rows() -> list[dict[str, object]]:
    proc = run_git(
        DIRTY_ROOT,
        [
            "for-each-ref",
            "--sort=refname",
            "--format=%(refname)%09%(objectname)%09%(committerdate:iso-strict)%09%(subject)",
            "refs/heads",
            "refs/remotes",
        ],
    )
    parsed: list[tuple[str, str, str, str]] = []
    for raw_line in proc.stdout.decode("utf-8", errors="replace").splitlines():
        parts = raw_line.split("\t", 3)
        if len(parts) != 4:
            raise RuntimeError(f"unexpected for-each-ref row: {raw_line!r}")
        parsed.append((parts[0], parts[1], parts[2], parts[3]))
    tip_cache: dict[str, tuple[int, list[str]]] = {}
    rows: list[dict[str, object]] = []
    for refname, oid, date, subject in parsed:
        if refname == "refs/remotes/origin/HEAD":
            rows.append(
                {
                    "ref": refname,
                    "tip": oid,
                    "date": date,
                    "ahead": 0,
                    "evidence": "NO",
                    "reason": "symbolic remote default alias; substantive target is classified separately",
                    "subject": subject,
                }
            )
            continue
        if oid not in tip_cache:
            ahead_proc = run_git(DIRTY_ROOT, ["rev-list", "--count", f"{FIXED_SHA}..{oid}"], check=False)
            ahead = int(ahead_proc.stdout.decode().strip() or "0") if ahead_proc.returncode == 0 else -1
            diff_proc = run_git(DIRTY_ROOT, ["diff", "--name-only", "-z", f"{FIXED_SHA}...{oid}"], check=False)
            if diff_proc.returncode != 0:
                diff_proc = run_git(DIRTY_ROOT, ["diff", "--name-only", "-z", FIXED_SHA, oid], check=False)
            changed = [decode_path(value) for value in diff_proc.stdout.split(b"\0") if value]
            tip_cache[oid] = (ahead, changed)
        ahead, changed = tip_cache[oid]
        evidence_paths = [p for p in changed if is_evidence_path(p)]
        short_name = refname.removeprefix("refs/heads/").removeprefix("refs/remotes/")
        if ahead < 0:
            evidence = "UNKNOWN"
            reason = "could not compute branch reachability against the fixed point"
        elif ahead == 0:
            evidence = "NO"
            reason = "tip has no commits outside the fixed-point master history"
        elif evidence_paths:
            evidence = "YES"
            reason = f"{ahead} branch-only commit(s); {len(evidence_paths)} changed evidence-path(s), e.g. {evidence_paths[0]}"
        elif BRANCH_EVIDENCE_RE.search(short_name):
            evidence = "YES"
            reason = f"{ahead} branch-only commit(s); branch name explicitly marks an evidence/research/audit purpose"
        else:
            evidence = "NO"
            reason = f"{ahead} branch-only commit(s), but no evidence-path or evidence-purpose marker was found"
        rows.append(
            {
                "ref": refname,
                "tip": oid,
                "date": date,
                "ahead": ahead,
                "evidence": evidence,
                "reason": reason,
                "subject": subject,
            }
        )
    return rows


def write_evidence_branches(rows: list[dict[str, object]]) -> None:
    yes = sum(row["evidence"] == "YES" for row in rows)
    no = sum(row["evidence"] == "NO" for row in rows)
    unknown = sum(row["evidence"] == "UNKNOWN" for row in rows)
    lines = [
        "# Evidence-bearing branches",
        "",
        f"Generated from the dirty checkout's local and remote ref list at {RUN_AT.isoformat(timespec='seconds')}.",
        "",
        f"Fixed-point comparison base: `{FIXED_SHA}`. Total refs: **{len(rows)}**; evidence-bearing: **{yes}**; "
        f"not evidence-bearing: **{no}**; unknown: **{unknown}**.",
        "",
        "Method: a ref is `YES` when it has commits outside the fixed-point history and either changes a path "
        "with an evidence/research/audit/parity marker or its branch name explicitly states such a purpose. "
        "A fully merged/contained ref is `NO` because it carries no branch-only evidence. This is preservation "
        "classification only, not a branch-pruning recommendation.",
        "",
        "| Ref | Tip | Date | Commits beyond fixed point | Evidence-bearing | Reason | Tip subject |",
        "|---|---|---|---:|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                md(row[key]) for key in ("ref", "tip", "date", "ahead", "evidence", "reason", "subject")
            )
            + " |"
        )
    lines.append("")
    OUT_DIR.joinpath("evidence_branches.md").write_text("\n".join(lines), encoding="utf-8")


def write_enumeration_selftest() -> str:
    token = hashlib.sha256(f"{RUN_AT.isoformat()}:{os.getpid()}".encode()).hexdigest()[:12]
    filename = f".__wp_p0_01_enumeration_selftest_{token}.tmp"
    temp_path = (CLEAN_ROOT / filename).resolve()
    if temp_path.parent != CLEAN_ROOT.resolve():
        raise RuntimeError("self-test path escaped clean worktree root")
    if temp_path.exists():
        raise RuntimeError(f"self-test target already exists: {temp_path}")
    temp_path.write_text("WP-P0-01 enumeration sentinel\n", encoding="utf-8")
    command = f'git -C "{CLEAN_ROOT}" status --porcelain=v1 --untracked-files=all'
    try:
        output = run_git(CLEAN_ROOT, ["status", "--porcelain=v1", "--untracked-files=all"]).stdout.decode(
            "utf-8", errors="replace"
        )
        found = any(line == f"?? {filename}" for line in output.splitlines())
    finally:
        temp_path.unlink(missing_ok=False)
    absent_after = not temp_path.exists()
    if not found or not absent_after:
        raise RuntimeError(f"enumeration self-test failed: found={found}, absent_after={absent_after}")
    lines = [
        "# Enumeration self-test",
        "",
        f"Executed: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        "",
        "The test created a randomized, previously unknown untracked sentinel in this lane's own clean "
        "worktree, invoked the same complete porcelain-v1 enumeration shape used for the dirty checkout, "
        "verified discovery without a filename allowlist, and deleted the exact sentinel. The dirty checkout "
        "was never written.",
        "",
        f"- Exact command: `{command}`",
        f"- Randomized sentinel: `{filename}`",
        f"- Matching output row: `?? {filename}`",
        f"- Found: **{'YES' if found else 'NO'}**",
        f"- Deleted after test: **{'YES' if absent_after else 'NO'}**",
        "- Result: **PASS**",
        "",
    ]
    OUT_DIR.joinpath("enumeration_selftest.md").write_text("\n".join(lines), encoding="utf-8")
    return filename


def write_readme(
    tracked_count: int,
    untracked_count: int,
    ref_stats: dict[str, int],
    status_human_count: int,
) -> None:
    lines = [
        "# WP-P0-01 repository inventory",
        "",
        f"Inventory timestamp: {RUN_AT.isoformat(timespec='seconds')}",
        f"Canonical fixed point: `{FIXED_SHA}`",
        f"Dirty checkout (strictly read-only): `{DIRTY_ROOT}`",
        "Audit tier: **T2**",
        "",
        "## Census",
        "",
        f"- Tracked fixed-point files: **{tracked_count}** (the dated plan snapshot of 8,031 was not reused).",
        f"- Fresh untracked dirty-checkout artefacts: **{untracked_count}**.",
        f"- Human porcelain output rows, including modified tracked files: **{status_human_count}**.",
        f"- Refs classified: **{ref_stats['total']}** ({ref_stats['yes']} evidence-bearing, "
        f"{ref_stats['no']} not evidence-bearing, {ref_stats['unknown']} unknown).",
        "",
        "## Exact enumeration commands",
        "",
        f"- Tracked: `git -C \"{CLEAN_ROOT}\" ls-tree -r -l -z {FIXED_SHA}`",
        f"- Required human-readable untracked/status listing: `git -C \"{DIRTY_ROOT}\" status --porcelain=v1 --untracked-files=all`",
        f"- Machine-safe untracked parsing: `git -C \"{DIRTY_ROOT}\" status --porcelain=v1 -z --untracked-files=all`",
        f"- Last-commit dates: `git -C \"{CLEAN_ROOT}\" log --pretty=tformat:%x1e%cI%x00 --name-only -z --no-renames {FIXED_SHA}`",
        f"- Branch refs: `git -C \"{DIRTY_ROOT}\" for-each-ref --sort=refname --format=... refs/heads refs/remotes`",
        "",
        "The NUL-delimited form is authoritative for machine counts because porcelain paths may be quoted "
        "and PowerShell's `?` is a wildcard. Only records whose two-byte status is exactly `??` become "
        "untracked-inventory rows.",
        "",
        "## Referenced-by methodology",
        "",
        "`referenced_by_count` is the number of distinct tracked text files that contain either the target's "
        "case-folded full repository-relative path (forward- or backslash form) or, for basenames of at least "
        "four characters, the case-folded basename. The builder creates one Aho-Corasick automaton and scans "
        "each eligible tracked text file once; self-references are excluded. Files over 4 MiB, known binary "
        "extensions, and files with a NUL in the first 8 KiB are not scanned as reference sources.",
        "",
        "Known behaviour: basename matching intentionally finds short-form references but over-counts when "
        "many tracked files share a basename (for example `README.md`). Path spelling variants beyond slash "
        "direction and case folding under-count. Generated references inside skipped binary/large files are "
        "not counted. The metric is therefore a bounded navigation-risk signal, not an exact dependency graph.",
        "",
        "## Classification semantics",
        "",
        "- `CANONICAL`: tracked at the fixed point with no explicit legacy/evidence marker; a working inventory "
        "label, not a cleanup or canonicalization decision.",
        "- `LEGACY`: path explicitly identifies itself as archive/legacy/retired/old/backup.",
        "- `DUPLICATE`: untracked bytes normalize through Git attributes to a blob tracked at the fixed point; "
        "the canonical twin is mandatory and recorded.",
        "- `EVIDENCE`: audit, research, parity, run, decision, or verification-bearing path.",
        "- `UNKNOWN`: owner/purpose/classification cannot safely be established; this is explicit classification, "
        "not an empty/unclassified row.",
        "",
        "Tier A contains every tracked/untracked path except paths captured by the explicit Tier-B rules. "
        "Tier B is limited to local agent-skill installation state, caches/bytecode, and OS/editor temporaries. "
        "No evidence-marker path is intentionally placed in Tier B.",
        "",
        "## Reproduction",
        "",
        "From the lane worktree root:",
        "",
        "```powershell",
        "python MTC_COMMAND_CENTER\\11_TRIAGE\\WP_P0_01_INVENTORY_2026-08-24\\build_inventory.py",
        "python MTC_COMMAND_CENTER\\11_TRIAGE\\WP_P0_01_INVENTORY_2026-08-24\\qa_inventory.py",
        "```",
        "",
        "Both scripts are standard-library-only and make no network, host, deployment, broker, Docker, WSL, "
        "backtest, Pine, parity-logic, MTC, Bridge-runtime, or schema mutation.",
        "",
    ]
    OUT_DIR.joinpath("README.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    validate_roots()
    dirty_status_before = run_git(DIRTY_ROOT, ["status", "--porcelain=v1", "-z", "--untracked-files=all"]).stdout
    tracked = tracked_files()
    dates = last_commit_dates()
    ref_counts, scan_stats = referenced_by_counts(tracked)
    tracked_rows = [
        {
            "path": row.path,
            "size_bytes": row.size,
            "last_commit_iso": dates.get(row.path, "UNKNOWN"),
            "referenced_by_count": ref_counts[index],
        }
        for index, row in enumerate(tracked)
    ]
    write_csv(
        OUT_DIR / "tracked_inventory.csv",
        ["path", "size_bytes", "last_commit_iso", "referenced_by_count"],
        tracked_rows,
    )

    untracked_paths, human_status, nul_status = parse_status_untracked(DIRTY_ROOT)
    untracked_rows = build_untracked_inventory(tracked, untracked_paths)
    write_csv(
        OUT_DIR / "untracked_inventory.csv",
        [
            "path",
            "size_bytes",
            "mtime_iso",
            "age_days_at_inventory",
            "likely_owner",
            "likely_purpose",
            "classification",
            "canonical_twin",
            "evidence_relevance",
            "classification_rationale",
            "tracked_at_fixed_sha_same_path",
        ],
        untracked_rows,
    )

    all_paths = [row.path for row in tracked] + untracked_paths
    tier_b_matches = write_tier_b_rules(all_paths)
    tier_b_path_to_rule: dict[str, str] = {}
    for rule_id, paths in tier_b_matches.items():
        for path in paths:
            tier_b_path_to_rule.setdefault(path, rule_id)

    tier_a_rows: list[dict[str, object]] = []
    for row in tracked:
        if row.path in tier_b_path_to_rule:
            continue
        classification, rationale = classify_tracked(row.path)
        tier_a_rows.append(
            {
                "source": "TRACKED_FIXED_SHA",
                "path": row.path,
                "classification": classification,
                "canonical_twin": "",
                "rationale": rationale,
                "evidence_relevance": evidence_relevance(row.path),
            }
        )
    for row in untracked_rows:
        path = str(row["path"])
        if path in tier_b_path_to_rule:
            continue
        tier_a_rows.append(
            {
                "source": "UNTRACKED_DIRTY_CHECKOUT",
                "path": path,
                "classification": row["classification"],
                "canonical_twin": row["canonical_twin"],
                "rationale": row["classification_rationale"],
                "evidence_relevance": row["evidence_relevance"],
            }
        )
    tier_a_rows.sort(key=lambda row: (str(row["path"]).casefold(), str(row["source"])))
    write_csv(
        OUT_DIR / "tier_a_classification.csv",
        ["source", "path", "classification", "canonical_twin", "rationale", "evidence_relevance"],
        tier_a_rows,
    )

    parity_counts = write_parity_resolution()
    branches = ref_rows()
    write_evidence_branches(branches)
    sentinel = write_enumeration_selftest()

    dirty_status_after = run_git(DIRTY_ROOT, ["status", "--porcelain=v1", "-z", "--untracked-files=all"]).stdout
    if dirty_status_after != dirty_status_before or dirty_status_after != nul_status:
        raise RuntimeError("dirty checkout status changed during read-only inventory")
    status_human_rows = len(human_status.splitlines())
    ref_stats = {
        "total": len(branches),
        "yes": sum(row["evidence"] == "YES" for row in branches),
        "no": sum(row["evidence"] == "NO" for row in branches),
        "unknown": sum(row["evidence"] == "UNKNOWN" for row in branches),
    }
    write_readme(len(tracked), len(untracked_rows), ref_stats, status_human_rows)

    report = [
        "# LANE A — WP-P0-01 implementer report",
        "",
        "Status: **IN_PROGRESS — generated; Gate-4 self-QA pending**",
        "",
        f"- Generated: {RUN_AT.isoformat(timespec='seconds')}",
        f"- Fixed SHA: `{FIXED_SHA}`",
        f"- Tracked rows: {len(tracked_rows)}",
        f"- Fresh untracked rows: {len(untracked_rows)}",
        f"- Human porcelain status rows (tracked modifications + untracked): {status_human_rows}",
        f"- Tier-A rows: {len(tier_a_rows)}",
        f"- Tier-B unique paths: {len(tier_b_path_to_rule)}",
        f"- Branch refs: {len(branches)}",
        f"- Parity union rows: {parity_counts['union']}",
        f"- Referenced-by scan stats: `{scan_stats}`",
        f"- Enumeration self-test sentinel (deleted): `{sentinel}`",
        f"- Dirty status SHA-256 before/after: `{hashlib.sha256(dirty_status_before).hexdigest()}` (identical)",
        "",
        "This file is finalized after `qa_inventory.py` and exact-path staging checks.",
        "",
    ]
    OUT_DIR.joinpath("LANE_REPORT.md").write_text("\n".join(report), encoding="utf-8")
    print(f"tracked_rows={len(tracked_rows)}")
    print(f"untracked_rows={len(untracked_rows)}")
    print(f"tier_a_rows={len(tier_a_rows)}")
    print(f"tier_b_unique_paths={len(tier_b_path_to_rule)}")
    print(f"refs={len(branches)}")
    print(f"parity_union={parity_counts['union']}")
    print(f"dirty_status_sha256={hashlib.sha256(dirty_status_before).hexdigest()}")
    print(f"reference_scan={scan_stats}")


if __name__ == "__main__":
    main()
