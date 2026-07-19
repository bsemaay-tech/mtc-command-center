"""TS-P0-001 — read-only repository/runtime baseline manifest and drift checker.

Offline CLI. Compares an explicit source repository worktree against an explicit
runtime worktree plus an expected release commit, and emits deterministic JSON
and Markdown manifests.

Exit codes:
  0  exact clean match (commits equal + expected, both trees clean, all scope
     hashes equal)
  2  drift: commit mismatch, dirty repo/runtime, hash mismatch, or runtime
     root missing
  3  invalid evidence input: missing/non-git repo root, malformed git output,
     invalid expected commit or timestamp

Default operation performs no HTTP call, no exchange call, no Task Scheduler,
no database access, and no process control. It never writes inside either root;
output files go only to the explicit --json-out / --md-out paths.

Secret safety: files matching the denylist (SECRET_FILE_DENYLIST) are never
opened or hashed; they are recorded as excluded by name only.

Contract: IBKR_PAPER_BRIDGE/docs/RUNTIME_BASELINE_CONTRACT.md
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

SCHEMA_VERSION = "1.0.0"

# Hashed scope, relative to each root. Rationale in RUNTIME_BASELINE_CONTRACT.md.
SOURCE_SCOPE = (
    "IBKR_PAPER_BRIDGE/bridge",
    "IBKR_PAPER_BRIDGE/requirements.txt",
    "IBKR_PAPER_BRIDGE/tools/run_bridge_p2.ps1",
)
CONFIG_SCOPE = ("IBKR_PAPER_BRIDGE/config",)

EXCLUDED_DIR_NAMES = {".git", "__pycache__", ".pytest_cache"}

# Never read, never hashed — recorded by path only.
SECRET_FILE_PATTERNS = (
    re.compile(r"^\.env(\..*)?$", re.IGNORECASE),
    re.compile(r"^secrets?(\..*)?$", re.IGNORECASE),
    re.compile(r".*\.(key|pem|p12|pfx)$", re.IGNORECASE),
    re.compile(r".*\.(db|sqlite|sqlite3|log)$", re.IGNORECASE),
)

_HEX_RE = re.compile(r"^[0-9a-f]{40}$")
_EXPECTED_RE = re.compile(r"^[0-9a-f]{7,40}$")
_TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


class EvidenceError(Exception):
    """Invalid evidence input (exit 3)."""


def _run_git(root: Path, *args: str) -> str:
    """Run a read-only git command; raise EvidenceError on failure."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:  # git missing / hung
        raise EvidenceError(f"git invocation failed for {root}: {exc}") from exc
    if proc.returncode != 0:
        raise EvidenceError(
            f"git {' '.join(args)} failed for {root}: {proc.stderr.strip()[:200]}"
        )
    return proc.stdout


def _read_git_facts(root: Path, label: str) -> dict:
    head = _run_git(root, "rev-parse", "HEAD").strip()
    if not _HEX_RE.match(head):
        raise EvidenceError(f"malformed git HEAD output for {label} root: {head!r}")
    porcelain = _run_git(root, "status", "--porcelain")
    entries = sorted(line for line in porcelain.splitlines() if line.strip())
    return {
        "root": root.resolve().as_posix(),
        "commit": head,
        "dirty": bool(entries),
        "dirty_entries": entries,
    }


def _is_secret_name(name: str) -> bool:
    return any(p.match(name) for p in SECRET_FILE_PATTERNS)


def _hash_file(path: Path) -> str:
    """SHA-256 with CRLF->LF normalization for text files.

    The repo and runtime worktrees can be checked out under different git
    line-ending smudge behavior while git itself reports both clean and
    identical (observed on the real C:/TSP0 vs C:/P2RT pair). Raw-byte
    hashing would flag that noise as drift, so text content is normalized
    the same way git's clean filter does. Files that look binary (NUL in
    the first 8KB) are hashed raw.
    """
    with open(path, "rb") as fh:
        data = fh.read()
    if b"\x00" not in data[:8192]:
        data = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def _walk_scope(root: Path, scope: tuple[str, ...]) -> tuple[dict, list, list]:
    """Return (files{rel: sha256}, excluded[{path, reason}], missing[rel])."""
    files: dict[str, str] = {}
    excluded: list[dict] = []
    missing: list[str] = []
    for entry in scope:
        target = root / entry
        if not target.exists():
            missing.append(entry)
            continue
        candidates = [target] if target.is_file() else sorted(
            p for p in target.rglob("*") if p.is_file()
        )
        for p in candidates:
            rel = p.relative_to(root).as_posix()
            if any(part in EXCLUDED_DIR_NAMES for part in p.relative_to(root).parts):
                continue
            if _is_secret_name(p.name):
                excluded.append({"path": rel, "reason": "secret_denylist"})
                continue
            files[rel] = _hash_file(p)
    excluded.sort(key=lambda e: e["path"])
    return dict(sorted(files.items())), excluded, sorted(missing)


def _aggregate(files: dict[str, str]) -> str:
    h = hashlib.sha256()
    for rel in sorted(files):
        h.update(f"{rel}\n{files[rel]}\n".encode("utf-8"))
    return h.hexdigest()


def _hash_side(root: Path) -> dict:
    src_files, src_excluded, src_missing = _walk_scope(root, SOURCE_SCOPE)
    cfg_files, cfg_excluded, cfg_missing = _walk_scope(root, CONFIG_SCOPE)
    all_files = dict(sorted({**src_files, **cfg_files}.items()))
    return {
        "files": all_files,
        "excluded": sorted(src_excluded + cfg_excluded, key=lambda e: e["path"]),
        "missing_scope_entries": sorted(src_missing + cfg_missing),
        "source_tree_hash": _aggregate(src_files),
        "config_hash": _aggregate(cfg_files),
    }


def _render_markdown(m: dict) -> str:
    c = m["comparison"]
    lines = [
        "# Runtime Baseline Manifest",
        "",
        f"- schema_version: `{m['schema_version']}`",
        f"- generated_at_utc: `{m['generated_at_utc']}`",
        f"- verdict: **{m['verdict']}** (exit {m['exit_code']})",
        "",
        "## Repository",
        f"- root: `{m['repo']['root']}`",
        f"- commit: `{m['repo']['commit']}`",
        f"- dirty: `{m['repo']['dirty']}`",
        "",
        "## Runtime",
        f"- root: `{m['runtime']['root']}`",
        f"- present: `{m['runtime']['present']}`",
        f"- commit: `{m['runtime']['commit']}`",
        f"- dirty: `{m['runtime']['dirty']}`",
        "",
        "## Expected release",
        f"- expected_commit: `{m['expected']['commit']}`",
        "",
        "## Comparison",
    ]
    for key in sorted(c):
        lines.append(f"- {key}: `{c[key]}`")
    lines += ["", "## Drift reasons"]
    if m["drift_reasons"]:
        lines += [f"- `{r}`" for r in m["drift_reasons"]]
    else:
        lines.append("- none")
    lines += [
        "",
        "## Hashes",
        f"- repo source_tree_hash: `{m['hashes']['repo']['source_tree_hash']}`",
        f"- repo config_hash: `{m['hashes']['repo']['config_hash']}`",
        f"- runtime source_tree_hash: `{m['hashes']['runtime']['source_tree_hash']}`",
        f"- runtime config_hash: `{m['hashes']['runtime']['config_hash']}`",
        "",
    ]
    return "\n".join(lines)


def _utc_now() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def build_manifest(
    repo_root: Path, runtime_root: Path, expected_commit: str, timestamp: str
) -> dict:
    if not repo_root.is_dir():
        raise EvidenceError(f"repo root does not exist: {repo_root}")
    repo = _read_git_facts(repo_root, "repo")
    repo_hashes = _hash_side(repo_root)
    if repo_hashes["missing_scope_entries"]:
        raise EvidenceError(
            "repo root is missing required scope entries: "
            + ", ".join(repo_hashes["missing_scope_entries"])
        )

    runtime_present = runtime_root.is_dir()
    if runtime_present:
        runtime = _read_git_facts(runtime_root, "runtime")
        runtime["present"] = True
        runtime_hashes = _hash_side(runtime_root)
    else:
        runtime = {
            "root": runtime_root.as_posix(),
            "commit": None,
            "dirty": None,
            "dirty_entries": [],
            "present": False,
        }
        runtime_hashes = {
            "files": {},
            "excluded": [],
            "missing_scope_entries": sorted(SOURCE_SCOPE + CONFIG_SCOPE),
            "source_tree_hash": None,
            "config_hash": None,
        }

    reasons: list[str] = []
    if not runtime_present:
        reasons.append("runtime_missing")
        comparison = {
            "repo_commit_matches_expected": repo["commit"].startswith(expected_commit),
            "runtime_commit_matches_expected": False,
            "commits_equal": False,
            "source_tree_hash_equal": False,
            "config_hash_equal": False,
            "repo_clean": not repo["dirty"],
            "runtime_clean": False,
        }
        if not comparison["repo_commit_matches_expected"]:
            reasons.append("repo_commit_mismatch_expected")
        if repo["dirty"]:
            reasons.append("repo_dirty")
        verdict = "RUNTIME_MISSING"
    else:
        comparison = {
            "repo_commit_matches_expected": repo["commit"].startswith(expected_commit),
            "runtime_commit_matches_expected": runtime["commit"].startswith(
                expected_commit
            ),
            "commits_equal": repo["commit"] == runtime["commit"],
            "source_tree_hash_equal": repo_hashes["source_tree_hash"]
            == runtime_hashes["source_tree_hash"],
            "config_hash_equal": repo_hashes["config_hash"]
            == runtime_hashes["config_hash"],
            "repo_clean": not repo["dirty"],
            "runtime_clean": not runtime["dirty"],
        }
        if not comparison["repo_commit_matches_expected"]:
            reasons.append("repo_commit_mismatch_expected")
        if not comparison["runtime_commit_matches_expected"]:
            reasons.append("runtime_commit_mismatch_expected")
        if not comparison["commits_equal"]:
            reasons.append("repo_runtime_commit_mismatch")
        if not comparison["source_tree_hash_equal"]:
            reasons.append("source_tree_hash_mismatch")
        if not comparison["config_hash_equal"]:
            reasons.append("config_hash_mismatch")
        if repo["dirty"]:
            reasons.append("repo_dirty")
        if runtime["dirty"]:
            reasons.append("runtime_dirty")
        for entry in runtime_hashes["missing_scope_entries"]:
            reasons.append(f"runtime_scope_entry_missing:{entry}")
        verdict = "MATCH" if not reasons else "DRIFT"

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "tool": "check_runtime_baseline",
        "generated_at_utc": timestamp,
        "repo": repo,
        "runtime": runtime,
        "expected": {"commit": expected_commit},
        "hash_scope": {
            "source": list(SOURCE_SCOPE),
            "config": list(CONFIG_SCOPE),
            "excluded_dir_names": sorted(EXCLUDED_DIR_NAMES),
            "secret_denylist": [p.pattern for p in SECRET_FILE_PATTERNS],
        },
        "hashes": {"repo": repo_hashes, "runtime": runtime_hashes},
        "comparison": comparison,
        "drift_reasons": sorted(reasons),
        "verdict": verdict,
        "exit_code": 0 if verdict == "MATCH" else 2,
    }
    return manifest


def _to_json(manifest: dict) -> str:
    return json.dumps(manifest, indent=2, sort_keys=True) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="check_runtime_baseline",
        description="Read-only repository/runtime baseline drift checker (TS-P0-001).",
    )
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--runtime-root", required=True)
    parser.add_argument(
        "--expected-commit",
        required=True,
        help="Expected release commit (7-40 hex chars).",
    )
    parser.add_argument(
        "--timestamp",
        default=None,
        help="Declared manifest timestamp (YYYY-MM-DDTHH:MM:SSZ); default: now.",
    )
    parser.add_argument("--json-out", default=None)
    parser.add_argument("--md-out", default=None)
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:  # argparse error -> invalid evidence input
        return 3 if exc.code != 0 else 0

    expected = args.expected_commit.strip().lower()
    if not _EXPECTED_RE.match(expected):
        print(
            f"check_runtime_baseline: invalid --expected-commit: {args.expected_commit!r}",
            file=sys.stderr,
        )
        return 3
    timestamp = args.timestamp if args.timestamp is not None else _utc_now()
    if not _TS_RE.match(timestamp):
        print(
            f"check_runtime_baseline: invalid --timestamp (want YYYY-MM-DDTHH:MM:SSZ): "
            f"{timestamp!r}",
            file=sys.stderr,
        )
        return 3

    try:
        manifest = build_manifest(
            Path(args.repo_root), Path(args.runtime_root), expected, timestamp
        )
    except EvidenceError as exc:
        print(f"check_runtime_baseline: invalid evidence input: {exc}", file=sys.stderr)
        return 3

    json_text = _to_json(manifest)
    md_text = _render_markdown(manifest)
    if args.json_out:
        Path(args.json_out).write_text(json_text, encoding="utf-8", newline="\n")
    if args.md_out:
        Path(args.md_out).write_text(md_text, encoding="utf-8", newline="\n")
    sys.stdout.write(json_text)
    return manifest["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
