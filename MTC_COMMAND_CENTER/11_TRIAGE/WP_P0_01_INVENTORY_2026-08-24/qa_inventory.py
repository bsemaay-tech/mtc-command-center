#!/usr/bin/env python3
"""Gate-4 self-QA for the WP-P0-01 inventory package."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

import build_inventory as build


OUT = Path(__file__).resolve().parent
EXPECTED_OUTPUTS = {
    "README.md",
    "LANE_REPORT.md",
    "build_inventory.py",
    "enumeration_selftest.md",
    "evidence_branches.md",
    "parity_dirs_resolution.md",
    "qa_inventory.py",
    "tier_a_classification.csv",
    "tier_b_rules.md",
    "tracked_inventory.csv",
    "untracked_inventory.csv",
}
VALID_CLASSIFICATIONS = {"CANONICAL", "LEGACY", "DUPLICATE", "EVIDENCE", "UNKNOWN"}


def read_csv(name: str) -> list[dict[str, str]]:
    with (OUT / name).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def check(condition: bool, label: str, detail: str = "") -> None:
    if not condition:
        raise AssertionError(f"FAIL {label}: {detail}")
    suffix = f" — {detail}" if detail else ""
    print(f"PASS {label}{suffix}")


def actual_ref_names() -> list[str]:
    proc = build.run_git(
        build.DIRTY_ROOT,
        ["for-each-ref", "--sort=refname", "--format=%(refname)", "refs/heads", "refs/remotes"],
    )
    return proc.stdout.decode("utf-8", errors="replace").splitlines()


def main() -> None:
    build.validate_roots()
    present = {path.name for path in OUT.iterdir() if path.is_file()}
    check(EXPECTED_OUTPUTS <= present, "deliverables present", f"{len(EXPECTED_OUTPUTS)} required files")

    tracked_model = build.tracked_files()
    tracked_paths = [row.path for row in tracked_model]
    tracked_set = set(tracked_paths)
    tracked_rows = read_csv("tracked_inventory.csv")
    check(len(tracked_rows) == len(tracked_model), "tracked row count", str(len(tracked_rows)))
    check(len({row["path"] for row in tracked_rows}) == len(tracked_rows), "tracked paths unique")
    check({row["path"] for row in tracked_rows} == tracked_set, "tracked paths reconcile to fixed SHA")
    check(
        all(row["last_commit_iso"] and row["size_bytes"].isdigit() for row in tracked_rows),
        "tracked size/date fields complete",
    )
    check(
        all(row["referenced_by_count"].isdigit() and int(row["referenced_by_count"]) >= 0 for row in tracked_rows),
        "referenced-by counts non-negative",
    )

    fresh_untracked, human_status, nul_status = build.parse_status_untracked(build.DIRTY_ROOT)
    del human_status, nul_status
    untracked_rows = read_csv("untracked_inventory.csv")
    untracked_paths = [row["path"] for row in untracked_rows]
    check(len(untracked_rows) == len(fresh_untracked), "untracked row count", str(len(untracked_rows)))
    check(len(set(untracked_paths)) == len(untracked_paths), "untracked paths unique")
    check(set(untracked_paths) == set(fresh_untracked), "fresh untracked path reconciliation")
    check(
        all(row["classification"] in VALID_CLASSIFICATIONS for row in untracked_rows),
        "untracked classifications explicit and valid",
    )
    check(
        all(row["likely_owner"] and row["likely_purpose"] and row["evidence_relevance"] for row in untracked_rows),
        "untracked owner/purpose/evidence fields complete",
    )
    check(
        all(row["mtime_iso"] and row["age_days_at_inventory"] and row["size_bytes"] for row in untracked_rows),
        "untracked filesystem metadata complete",
    )
    duplicate_untracked = [row for row in untracked_rows if row["classification"] == "DUPLICATE"]
    check(
        all(row["canonical_twin"] in tracked_set for row in duplicate_untracked),
        "untracked duplicates name tracked twins",
        f"{len(duplicate_untracked)} duplicate row(s)",
    )
    check(
        all(
            row["path"] == row["canonical_twin"] or int(row["size_bytes"]) > 0
            for row in duplicate_untracked
        ),
        "no empty cross-path false duplicates",
    )

    tier_a = read_csv("tier_a_classification.csv")
    tier_a_keys = {(row["source"], row["path"]) for row in tier_a}
    expected_tier_a = {
        ("TRACKED_FIXED_SHA", path) for path in tracked_paths if build.tier_b_rule_for(path) is None
    } | {
        ("UNTRACKED_DIRTY_CHECKOUT", path)
        for path in fresh_untracked
        if build.tier_b_rule_for(path) is None
    }
    check(len(tier_a_keys) == len(tier_a), "Tier-A keys unique")
    check(tier_a_keys == expected_tier_a, "zero unclassified Tier-A paths", str(len(tier_a)))
    check(
        all(row["classification"] in VALID_CLASSIFICATIONS and row["classification"] for row in tier_a),
        "Tier-A classifications explicit",
    )
    check(
        all(row["classification"] != "UNKNOWN" for row in tier_a if row["source"] == "TRACKED_FIXED_SHA"),
        "tracked Tier-A has four-way classification",
    )
    duplicates = [row for row in tier_a if row["classification"] == "DUPLICATE"]
    check(
        all(row["canonical_twin"] in tracked_set for row in duplicates),
        "every Tier-A duplicate names canonical twin",
        f"{len(duplicates)} duplicate row(s)",
    )

    all_paths = tracked_paths + fresh_untracked
    tier_b_paths: set[str] = set()
    tier_b_text = (OUT / "tier_b_rules.md").read_text(encoding="utf-8")
    for rule in build.TIER_B_RULES:
        matched = sorted({path for path in all_paths if rule.regex.search(path)}, key=str.casefold)
        tier_b_paths.update(matched)
        count_match = re.search(rf"## {rule.rule_id}.*?- Matched count: \*\*(\d+)\*\*", tier_b_text, re.S)
        check(count_match is not None and int(count_match.group(1)) == len(matched), f"{rule.rule_id} count", str(len(matched)))
        samples = build.deterministic_samples(matched)
        check(len(samples) >= 20 if len(matched) >= 20 else len(samples) == len(matched), f"{rule.rule_id} sample size", str(len(samples)))
        check(all(not build.is_evidence_path(path) for path in matched), f"{rule.rule_id} swallowed no evidence path")
        check(all(path not in {p for _, p in tier_a_keys} for path in matched), f"{rule.rule_id} disjoint from Tier A")
    check(len(tier_b_paths) + len(tier_a) == len(tracked_paths) + len(fresh_untracked), "Tier-A/Tier-B universe reconciliation")

    parity_text = (OUT / "parity_dirs_resolution.md").read_text(encoding="utf-8")
    dirty_05 = build.recursive_files(build.DIRTY_ROOT / "MTC_COMMAND_CENTER" / "05_PARITY")
    dirty_12 = build.recursive_files(build.DIRTY_ROOT / "MTC_COMMAND_CENTER" / "12_PARITY_PINETS")
    union = set(dirty_05) | set(dirty_12)
    verdict_rows = [
        line
        for line in parity_text.splitlines()
        if line.startswith("| ")
        and ("only-in-05_PARITY" in line or "only-in-12_PARITY_PINETS" in line or "| identical |" in line or "| differs |" in line)
    ]
    check(len(verdict_rows) == len(union), "parity per-file row count", str(len(verdict_rows)))
    check(
        all(f"MTC_COMMAND_CENTER/05_PARITY/{path}" in parity_text for path in dirty_05),
        "full 05_PARITY path list present",
    )
    check(
        all(f"MTC_COMMAND_CENTER/12_PARITY_PINETS/{path}" in parity_text for path in dirty_12),
        "full 12_PARITY_PINETS path list present",
    )
    check(
        sum("only-in-05_PARITY" in row for row in verdict_rows) == len(set(dirty_05) - set(dirty_12)),
        "parity only-in-05 verdicts reconcile",
    )
    check(
        sum("only-in-12_PARITY_PINETS" in row for row in verdict_rows) == len(set(dirty_12) - set(dirty_05)),
        "parity only-in-12 verdicts reconcile",
    )

    branch_text = (OUT / "evidence_branches.md").read_text(encoding="utf-8")
    refs = actual_ref_names()
    branch_rows = [line for line in branch_text.splitlines() if line.startswith("| refs/")]
    check(len(branch_rows) == len(refs), "branch row count", str(len(refs)))
    check(all(f"| {ref} |" in branch_text for ref in refs), "every local/remote ref classified")
    check(all("| UNKNOWN |" not in row for row in branch_rows), "no unresolved branch classification")

    selftest = (OUT / "enumeration_selftest.md").read_text(encoding="utf-8")
    check("- Result: **PASS**" in selftest and "- Found: **YES**" in selftest, "enumeration self-test recorded PASS")
    sentinel_match = re.search(r"- Randomized sentinel: `([^`]+)`", selftest)
    check(sentinel_match is not None, "self-test sentinel recorded")
    check(not (build.CLEAN_ROOT / sentinel_match.group(1)).exists(), "self-test sentinel deleted")

    status = build.run_git(build.CLEAN_ROOT, ["status", "--porcelain=v1", "-z", "--untracked-files=all"]).stdout
    scoped_paths: list[str] = []
    for record in status.split(b"\0"):
        if not record:
            continue
        if len(record) < 4:
            raise AssertionError(f"unexpected clean-worktree status record: {record!r}")
        scoped_paths.append(build.decode_path(record[3:]))
    allowed_prefix = "MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_01_INVENTORY_2026-08-24/"
    check(
        all(path.startswith(allowed_prefix) for path in scoped_paths),
        "worktree clean or changes confined to output whitelist",
        str(len(scoped_paths)),
    )

    print("GATE DECISION: proceed to Lead-owned Gate 5 (T2)")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"GATE DECISION: loop back to Gate 3 — {exc}", file=sys.stderr)
        raise
