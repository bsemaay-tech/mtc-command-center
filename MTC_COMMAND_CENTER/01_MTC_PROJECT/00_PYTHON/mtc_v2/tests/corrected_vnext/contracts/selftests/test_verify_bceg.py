from __future__ import annotations

import hashlib
import json
import math
import shutil
import subprocess
import tempfile
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from mtc_v2.tests.corrected_vnext import verify_bceg
from mtc_v2.tests.corrected_vnext.verify_bceg import (
    GateRefusal,
    build_projection_results,
    compare_documents,
    compare_scoped_expected,
    decode_stop_price_f64,
    derive_section18_served_def_sets,
    execute_corrected_scenario,
    load_json_exact,
    resolve_record_references,
    validate_corrected_event_surface,
    validate_input_envelope,
    validate_legacy_unpadded,
)


FIXTURES = Path(__file__).parent
MTC_V2_ROOT = FIXTURES.parents[3]
BASELINE_ROOT = Path(r"C:\tmp\P012_BASELINE_RUN")
EMPTY_DOCUMENT_BYTES = b"{}" + bytes([10])
PATCH_BYTES = b"--- a" + bytes([10])
MEMBER_BYTES = b"x = 1" + bytes([10])
SYNTHETIC_DIFF_BYTES = (
    b"diff --git a/core/position_sizer.py b/core/position_sizer.py\n"
    b"index 0000000..1111111 100644\n"
    b"--- a/core/position_sizer.py\n"
    b"+++ b/core/position_sizer.py\n"
    b"@@ -43,7 +43,14 @@\n"
    b"-def legacy_sizing():\n"
    b"+def corrected_sizing():\n"
    b"+    return cm * qty\n"
    b"diff --git a/core/exits.py b/core/exits.py\n"
    b"index 2222222..3333333 100644\n"
    b"--- a/core/exits.py\n"
    b"+++ b/core/exits.py\n"
    b"@@ -353,5 +353,8 @@\n"
    b"-def stop_first():\n"
    b"+def policy():\n"
    b"+    pass\n"
)

SYNTHETIC_REVIEW_IDENTITIES = {
    "worktree_head_commit": "1" * 40,
    "core_tree_oid": "2" * 40,
    "expected_seal_sha": "3" * 64,
    "implementation_anchor_sha256": "4" * 64,
    "baseline_manifest_sha256": "5" * 64,
    "design_file_sha256": "6" * 64,
    "design_version": "v1.11",
    "harness_sha256": "7" * 64,
    "catalog_sha256": "8" * 64,
}


def write_synthetic_reseal_manifest(
    root: Path, history: list[dict[str, object]]
) -> None:
    manifest = root / "tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    design = root / "design.md"
    design.write_text(
        "Design v1.11\n"
        + "\n".join(
            [
                f"| `S18-{number:02d}` | core/x.py | text | {served} | note |"
                for number, served in (
                    (1, ", ".join(f"`DEF-P012-{n:02d}`" for n in range(1, 9))),
                    (2, ", ".join(f"`DEF-P012-{n:02d}`" for n in (1, 2, 4, 5, 6, 7, 8))),
                    (3, "`DEF-P012-01`, `DEF-P012-02`"),
                    (4, "`DEF-P012-03`"),
                    (5, "`DEF-P012-04`, `DEF-P012-06`"),
                    (6, "`DEF-P012-05`, `DEF-P012-07`, `DEF-P012-08`"),
                    (7, "`DEF-P012-03`, `DEF-P012-05`, `DEF-P012-07`"),
                    (8, "`DEF-P012-02`, `DEF-P012-03`, `DEF-P012-04`, `DEF-P012-06`"),
                    (9, "`DEF-P012-08`"),
                    (10, "`DEF-P012-07`"),
                    (11, "`DEF-P012-07`, `DEF-P012-08`"),
                    (12, "—"),
                )
            ]
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    manifest.write_bytes(
        verify_bceg.canonical_json_bytes(
            {
                "reseal_history": history,
                "design": {
                    "file": str(design),
                    "sha256": verify_bceg.sha256_file(design),
                },
            }
        )
    )


def synthetic_v2_hunk_receipt(
    reviewed_head: str = SYNTHETIC_REVIEW_IDENTITIES["worktree_head_commit"],
) -> dict[str, object]:
    """Valid V2 hunk receipt: one DEF hunk and one SECTION18_SHARED hunk."""

    parsed = verify_bceg.parse_hunk_diff(SYNTHETIC_DIFF_BYTES)
    assert len(parsed) == 2

    def record(hunk: verify_bceg.ParsedHunk, **extra: object) -> dict[str, object]:
        base: dict[str, object] = {
            "path": hunk.path,
            "old_start": hunk.old_start,
            "old_count": hunk.old_count,
            "new_start": hunk.new_start,
            "new_count": hunk.new_count,
            "hunk_sha256": hashlib.sha256(hunk.raw_bytes).hexdigest(),
        }
        base.update(extra)
        return base

    return {
        "schema": verify_bceg.SEMANTIC_HUNK_COVERAGE_SCHEMA,
        "base_commit": verify_bceg.HUNK_DIFF_BASE_COMMIT,
        "reviewed_head": reviewed_head,
        "diff_command": verify_bceg.canonical_hunk_diff_command(reviewed_head),
        "diff_sha256": hashlib.sha256(SYNTHETIC_DIFF_BYTES).hexdigest(),
        "total_changed_paths": 2,
        "total_changed_files": 2,
        "changed_paths": [
            {
                "path": parsed[0].path,
                "hunk_count": 1,
                "hunk_indices": [0],
                "hunk_sha256s": [hashlib.sha256(parsed[0].raw_bytes).hexdigest()],
            },
            {
                "path": parsed[1].path,
                "hunk_count": 1,
                "hunk_indices": [1],
                "hunk_sha256s": [hashlib.sha256(parsed[1].raw_bytes).hexdigest()],
            },
        ],
        "section18_coverage": [
            {
                "row": f"S18-{number:02d}",
                "served_def_ids": {
                    1: [f"DEF-P012-{n:02d}" for n in range(1, 9)],
                    2: ["DEF-P012-01", "DEF-P012-02", "DEF-P012-04", "DEF-P012-05", "DEF-P012-06", "DEF-P012-07", "DEF-P012-08"],
                    3: ["DEF-P012-01", "DEF-P012-02"], 4: ["DEF-P012-03"],
                    5: ["DEF-P012-04", "DEF-P012-06"], 6: ["DEF-P012-05", "DEF-P012-07", "DEF-P012-08"],
                    7: ["DEF-P012-03", "DEF-P012-05", "DEF-P012-07"], 8: ["DEF-P012-02", "DEF-P012-03", "DEF-P012-04", "DEF-P012-06"],
                    9: ["DEF-P012-08"], 10: ["DEF-P012-07"], 11: ["DEF-P012-07", "DEF-P012-08"], 12: [],
                }[number],
                "hunk_indices": [1] if number == 5 else [],
            }
            for number in range(1, 13)
        ],
        "hunks": [
            record(parsed[0], terminal_class="DEF", def_ids=["DEF-P012-01"]),
            record(
                parsed[1],
                terminal_class="SECTION18_SHARED",
                section18_row="S18-05",
                served_def_ids=["DEF-P012-04", "DEF-P012-06"],
            ),
        ],
    }


def write_v2_hunk_receipt(root: Path, receipt: dict[str, object]) -> Path:
    path = root / "review-evidence" / "item-2-hunks.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(verify_bceg.canonical_json_bytes(receipt))
    return path


def hunk_record(**overrides: object) -> dict[str, object]:
    """A mutable copy of the first (DEF) hunk record for mutant tests."""

    entry = deepcopy(synthetic_v2_hunk_receipt()["hunks"][0])
    entry.update(overrides)
    return entry


def refusal(check_id: str, action) -> None:
    with pytest.raises(GateRefusal) as caught:
        action()
    assert caught.value.check_id == check_id


def semantic_review_fixture(
    root: Path,
    reviewed_head: str = SYNTHETIC_REVIEW_IDENTITIES["worktree_head_commit"],
) -> dict[str, object]:
    evidence_paths: list[str] = []
    for item in range(1, 7):
        path = root / "review-evidence" / f"item-{item}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"item {item} evidence\n", encoding="utf-8", newline="\n")
        evidence_paths.append(path.relative_to(root).as_posix())
    embedded_hunk_coverage = synthetic_v2_hunk_receipt(reviewed_head=reviewed_head)
    items = {
        str(item): {
            "disposition": "ACCEPTED",
            "evidence_paths": [evidence_paths[item - 1]],
            "notes": "Reviewed against the synthetic fixture.",
        }
        for item in range(1, 7)
    }
    items["2"]["hunk_coverage"] = embedded_hunk_coverage
    identities = dict(SYNTHETIC_REVIEW_IDENTITIES)
    identities["worktree_head_commit"] = reviewed_head
    return {
        "schema": verify_bceg.SEMANTIC_COVERAGE_REVIEW_SCHEMA,
        "reviewer": {
            "identity": "synthetic independent reviewer",
            "family": "Gemini",
            "independent_of": [
                {
                    "role": "KERNEL_IMPLEMENTER",
                    "basis": "Gemini family is distinct from the Codex-family kernel implementer.",
                },
                {
                    "role": "CONTRACT_TABLES_AUTHOR",
                    "basis": "Gemini family is distinct from the Claude-family tables author.",
                },
            ],
        },
        "reviewed_identities": identities,
        "items": items,
        "unresolved_items": [],
        "owner_ratification": {
            "chain": ["#5", "#6", "#7", "#8", "#9"],
            "ratified": True,
        },
        "signed_at": "2026-09-02T12:00:00+03:00",
    }


def run_synthetic_full_gate(
    root: Path,
    baseline_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    measured_identities: dict[str, str] | None = None,
    use_real_git: bool = False,
    contract_selftests: dict[str, object] | None = None,
) -> int:
    manifest = root / "tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json"
    if not manifest.exists():
        write_synthetic_reseal_manifest(
            root,
            [
                {"actor": f"Synthetic Lead, re-seal #{seal_id}"}
                for seal_id in range(5, 10)
            ],
        )
    measured = measured_identities or SYNTHETIC_REVIEW_IDENTITIES
    monkeypatch.setattr(
        verify_bceg,
        "run_comparison_pipeline",
        lambda _root, _baseline_root: {
            "acceptance_blockers": [],
            "sealed_producer_identities": dict(SYNTHETIC_REVIEW_IDENTITIES),
        },
    )
    monkeypatch.setattr(
        verify_bceg,
        "measure_semantic_review_identities",
        lambda _root, _baseline_root, _sealed_identities: dict(measured),
    )
    monkeypatch.setattr(
        verify_bceg,
        "semantic_review_core_tree",
        lambda _root, _commit: measured["core_tree_oid"],
    )
    monkeypatch.setattr(
        verify_bceg,
        "compute_hunk_diff",
        lambda _root, _reviewed_head: SYNTHETIC_DIFF_BYTES,
    )
    if not use_real_git:
        monkeypatch.setattr(
            verify_bceg,
            "semantic_review_commit_is_ancestor",
            lambda _root, reviewed_commit, head_commit: reviewed_commit
            == head_commit,
        )
    monkeypatch.setattr(
        verify_bceg,
        "run_contract_selftest_suite",
        lambda _root: contract_selftests
        if contract_selftests is not None
        else {
            "ran": True,
            "returncode": 0,
            "passed_count": 1,
            "failed_count": 0,
            "failing_test_ids": [],
        },
        raising=True,
    )
    return verify_bceg.main(
        [
            "--mode",
            "full-gate",
            "--root",
            str(root),
            "--baseline-root",
            str(baseline_root),
        ]
    )


def assert_invalid_semantic_review(
    capsys: pytest.CaptureFixture[str], expected_detail: str | None = None
) -> None:
    receipt = json.loads(capsys.readouterr().out)
    assert receipt["claim_label"] == verify_bceg.REFUSAL_LABEL
    assert receipt["refusals"][0]["check_id"] == "SEMANTIC_COVERAGE_REVIEW_INVALID"
    if expected_detail is not None:
        assert receipt["refusals"][0]["detail"] == expected_detail


def two_commit_repository(
    root: Path, marker_relative: str = "commit-marker.txt"
) -> tuple[str, str]:
    root.mkdir(parents=True, exist_ok=True)
    commands = (
        ("init",),
        ("config", "user.email", "w280@example.invalid"),
        ("config", "user.name", "W280 selftest"),
    )
    for command in commands:
        subprocess.run(
            ["git", "-C", str(root), *command],
            check=True,
            capture_output=True,
            text=True,
        )
    marker = root / marker_relative
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text("reviewed\n", encoding="utf-8", newline="\n")
    subprocess.run(
        ["git", "-C", str(root), "add", marker_relative],
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["git", "-C", str(root), "commit", "-m", "reviewed content"],
        check=True,
        capture_output=True,
        text=True,
    )
    reviewed_commit = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
    ).strip()
    marker.write_text("reviewed\nreceipt added\n", encoding="utf-8", newline="\n")
    subprocess.run(
        ["git", "-C", str(root), "add", marker_relative],
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["git", "-C", str(root), "commit", "-m", "add receipt"],
        check=True,
        capture_output=True,
        text=True,
    )
    head_commit = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
    ).strip()
    return reviewed_commit, head_commit


def test_semantic_coverage_review_empty_file_is_invalid(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    review = root / "tests/corrected_vnext/contracts/semantic_coverage_review.json"
    review.parent.mkdir(parents=True)
    review.write_bytes(b"")

    assert run_synthetic_full_gate(root, tmp_path / "baseline", monkeypatch) == 2
    assert_invalid_semantic_review(capsys)


def test_semantic_coverage_review_missing_item_is_invalid(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    receipt = semantic_review_fixture(root)
    del receipt["items"]["4"]
    review = root / "tests/corrected_vnext/contracts/semantic_coverage_review.json"
    review.parent.mkdir(parents=True)
    review.write_bytes(verify_bceg.canonical_json_bytes(receipt))

    assert run_synthetic_full_gate(root, tmp_path / "baseline", monkeypatch) == 2
    assert_invalid_semantic_review(capsys)


def test_semantic_coverage_review_refused_item_is_invalid(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    receipt = semantic_review_fixture(root)
    receipt["items"]["2"]["disposition"] = "REFUSED"
    review = root / "tests/corrected_vnext/contracts/semantic_coverage_review.json"
    review.parent.mkdir(parents=True)
    review.write_bytes(verify_bceg.canonical_json_bytes(receipt))

    assert run_synthetic_full_gate(root, tmp_path / "baseline", monkeypatch) == 2
    assert_invalid_semantic_review(capsys)


def test_semantic_coverage_review_stale_head_is_invalid(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    receipt = semantic_review_fixture(root)
    receipt["reviewed_identities"]["worktree_head_commit"] = "0" * 40
    review = root / "tests/corrected_vnext/contracts/semantic_coverage_review.json"
    review.parent.mkdir(parents=True)
    review.write_bytes(verify_bceg.canonical_json_bytes(receipt))

    assert run_synthetic_full_gate(root, tmp_path / "baseline", monkeypatch) == 2
    assert_invalid_semantic_review(capsys)


def test_w280_reviewed_ancestor_with_matching_content_clears_blocker(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    reviewed_commit, head_commit = two_commit_repository(root)
    receipt = semantic_review_fixture(root, reviewed_head=reviewed_commit)
    measured = dict(SYNTHETIC_REVIEW_IDENTITIES)
    measured["worktree_head_commit"] = head_commit
    review = root / "tests/corrected_vnext/contracts/semantic_coverage_review.json"
    review.parent.mkdir(parents=True, exist_ok=True)
    review.write_bytes(verify_bceg.canonical_json_bytes(receipt))

    assert run_synthetic_full_gate(
        root, tmp_path / "baseline", monkeypatch, measured, use_real_git=True
    ) == 0
    gate_receipt = json.loads(capsys.readouterr().out)
    assert gate_receipt["claim_label"] == verify_bceg.ACCEPTING_LABEL


def test_w280_reviewed_commit_that_is_not_an_ancestor_is_invalid(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    receipt = semantic_review_fixture(root)
    _reviewed_commit, head_commit = two_commit_repository(root)
    measured = dict(SYNTHETIC_REVIEW_IDENTITIES)
    measured["worktree_head_commit"] = head_commit
    receipt["reviewed_identities"]["worktree_head_commit"] = "0" * 40
    review = root / "tests/corrected_vnext/contracts/semantic_coverage_review.json"
    review.parent.mkdir(parents=True, exist_ok=True)
    review.write_bytes(verify_bceg.canonical_json_bytes(receipt))

    assert run_synthetic_full_gate(
        root, tmp_path / "baseline", monkeypatch, measured, use_real_git=True
    ) == 2
    assert_invalid_semantic_review(
        capsys,
        "reviewed_identities.worktree_head_commit: not an ancestor of measured HEAD",
    )


def test_w280_matching_head_with_changed_core_tree_is_invalid(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    receipt = semantic_review_fixture(root)
    receipt["reviewed_identities"]["core_tree_oid"] = "9" * 40
    review = root / "tests/corrected_vnext/contracts/semantic_coverage_review.json"
    review.parent.mkdir(parents=True)
    review.write_bytes(verify_bceg.canonical_json_bytes(receipt))

    assert run_synthetic_full_gate(root, tmp_path / "baseline", monkeypatch) == 2
    assert_invalid_semantic_review(
        capsys,
        "reviewed_identities.core_tree_oid: does not match measured identity",
    )


def test_w280_harness_sha_mismatch_is_invalid(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    receipt = semantic_review_fixture(root)
    receipt["reviewed_identities"]["harness_sha256"] = "9" * 64
    review = root / "tests/corrected_vnext/contracts/semantic_coverage_review.json"
    review.parent.mkdir(parents=True)
    review.write_bytes(verify_bceg.canonical_json_bytes(receipt))

    assert run_synthetic_full_gate(root, tmp_path / "baseline", monkeypatch) == 2
    assert_invalid_semantic_review(
        capsys,
        "reviewed_identities.harness_sha256: does not match measured identity",
    )


def test_semantic_coverage_review_fully_valid_synthetic_receipt_clears_blocker(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    receipt = semantic_review_fixture(root)
    review = root / "tests/corrected_vnext/contracts/semantic_coverage_review.json"
    review.parent.mkdir(parents=True)
    review.write_bytes(verify_bceg.canonical_json_bytes(receipt))

    assert run_synthetic_full_gate(root, tmp_path / "baseline", monkeypatch) == 0
    gate_receipt = json.loads(capsys.readouterr().out)
    assert gate_receipt["claim_label"] == verify_bceg.ACCEPTING_LABEL
    assert gate_receipt["contract_selftest_suite"] == {
        "ran": True,
        "returncode": 0,
        "passed_count": 1,
        "failed_count": 0,
        "failing_test_ids": [],
    }


def run_v2_receipt_gate(
    root: Path,
    baseline_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    document: dict[str, object],
) -> int:
    """Write a V2 hunk receipt as item-2 evidence and run the synthetic full gate."""

    receipt = semantic_review_fixture(root)
    receipt["items"]["2"]["hunk_coverage"] = document
    review = root / "tests/corrected_vnext/contracts/semantic_coverage_review.json"
    review.parent.mkdir(parents=True, exist_ok=True)
    review.write_bytes(verify_bceg.canonical_json_bytes(receipt))
    return run_synthetic_full_gate(root, baseline_root, monkeypatch)


def test_v2_item2_missing_hunk_receipt_is_invalid(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    receipt = semantic_review_fixture(root)
    receipt["items"]["2"].pop("hunk_coverage")
    review = root / "tests/corrected_vnext/contracts/semantic_coverage_review.json"
    review.parent.mkdir(parents=True)
    review.write_bytes(verify_bceg.canonical_json_bytes(receipt))

    assert run_synthetic_full_gate(root, tmp_path / "baseline", monkeypatch) == 2
    assert_invalid_semantic_review(capsys, "items.2.hunk_coverage: missing")


def test_v2_item2_v1_ledger_is_superseded(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    receipt = semantic_review_fixture(root)
    v1 = {
        "schema": verify_bceg.SEMANTIC_HUNK_COVERAGE_SCHEMA_V1,
        "diff_command": "git diff --unified=0",
        "hunks": [],
    }
    review = root / "tests/corrected_vnext/contracts/semantic_coverage_review.json"
    review.parent.mkdir(parents=True)
    receipt["items"]["2"]["hunk_coverage"] = v1
    review.write_bytes(verify_bceg.canonical_json_bytes(receipt))

    assert run_synthetic_full_gate(root, tmp_path / "baseline", monkeypatch) == 2
    assert_invalid_semantic_review(capsys, "items.2.base_commit: missing")


def test_v2_item2_valid_receipt_clears_blocker(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    assert run_v2_receipt_gate(
        root, tmp_path / "baseline", monkeypatch, synthetic_v2_hunk_receipt()
    ) == 0
    gate_receipt = json.loads(capsys.readouterr().out)
    assert gate_receipt["claim_label"] == verify_bceg.ACCEPTING_LABEL


def test_v2_item2_external_evidence_never_substitutes_embedded_receipt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    receipt = semantic_review_fixture(root)
    receipt["items"]["2"].pop("hunk_coverage")
    external = write_v2_hunk_receipt(root, synthetic_v2_hunk_receipt())
    receipt["items"]["2"]["evidence_paths"] = [
        external.relative_to(root).as_posix()
    ]
    review = root / "tests/corrected_vnext/contracts/semantic_coverage_review.json"
    review.parent.mkdir(parents=True, exist_ok=True)
    review.write_bytes(verify_bceg.canonical_json_bytes(receipt))

    assert run_synthetic_full_gate(root, tmp_path / "baseline", monkeypatch) == 2
    assert_invalid_semantic_review(capsys, "items.2.hunk_coverage: missing")


def test_v2_item2_s18_02_extra_def_refuses(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    document = synthetic_v2_hunk_receipt()
    document["section18_coverage"][1]["served_def_ids"].append("DEF-P012-03")
    document["section18_coverage"][1]["served_def_ids"].sort()

    assert run_v2_receipt_gate(root, tmp_path / "baseline", monkeypatch, document) == 2
    assert_invalid_semantic_review(
        capsys, "items.2.section18_coverage.1.served_def_ids: does not match manifest-pinned design"
    )


def test_v2_item2_design_manifest_drift_refuses(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    receipt = semantic_review_fixture(root)
    write_synthetic_reseal_manifest(
        root, [{"actor": f"Synthetic Lead, re-seal #{n}"} for n in range(5, 10)]
    )
    (root / "design.md").write_text("Design v1.11\ndrift\n", encoding="utf-8", newline="\n")
    review = root / "tests/corrected_vnext/contracts/semantic_coverage_review.json"
    review.parent.mkdir(parents=True, exist_ok=True)
    review.write_bytes(verify_bceg.canonical_json_bytes(receipt))

    assert run_synthetic_full_gate(root, tmp_path / "baseline", monkeypatch) == 2
    assert_invalid_semantic_review(capsys, "section18: manifest-pinned design bytes drifted")


def test_v2_item2_wrong_base_commit_is_invalid(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    document = synthetic_v2_hunk_receipt()
    document["base_commit"] = "0" * 40

    assert run_v2_receipt_gate(root, tmp_path / "baseline", monkeypatch, document) == 2
    assert_invalid_semantic_review(
        capsys,
        f"items.2.base_commit: expected fixed base {verify_bceg.HUNK_DIFF_BASE_COMMIT}",
    )


def test_v2_item2_reviewed_head_mismatch_is_invalid(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    document = synthetic_v2_hunk_receipt()
    document["reviewed_head"] = "f" * 40

    assert run_v2_receipt_gate(root, tmp_path / "baseline", monkeypatch, document) == 2
    assert_invalid_semantic_review(
        capsys,
        "items.2.reviewed_head: does not match reviewed_identities.worktree_head_commit",
    )


def test_v2_item2_wrong_diff_command_is_invalid(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    document = synthetic_v2_hunk_receipt()
    document["diff_command"] = "git diff --unified=3"

    assert run_v2_receipt_gate(root, tmp_path / "baseline", monkeypatch, document) == 2
    assert_invalid_semantic_review(
        capsys, "items.2.diff_command: expected canonical command"
    )


def test_v2_item2_wrong_diff_sha256_is_invalid(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    document = synthetic_v2_hunk_receipt()
    document["diff_sha256"] = "0" * 64

    assert run_v2_receipt_gate(root, tmp_path / "baseline", monkeypatch, document) == 2
    assert_invalid_semantic_review(
        capsys, "items.2.diff_sha256: does not match recomputed diff"
    )


def test_v2_item2_extra_hunk_record_is_invalid(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    document = synthetic_v2_hunk_receipt()
    document["hunks"] = document["hunks"] + [deepcopy(document["hunks"][0])]

    assert run_v2_receipt_gate(root, tmp_path / "baseline", monkeypatch, document) == 2
    assert_invalid_semantic_review(capsys, "items.2.hunks: expected 2 hunk records, got 3")


def test_v2_item2_missing_hunk_record_is_invalid(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    document = synthetic_v2_hunk_receipt()
    document["hunks"] = document["hunks"][:1]

    assert run_v2_receipt_gate(root, tmp_path / "baseline", monkeypatch, document) == 2
    assert_invalid_semantic_review(capsys, "items.2.hunks: expected 2 hunk records, got 1")


def test_v2_item2_reordered_hunks_is_invalid(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    document = synthetic_v2_hunk_receipt()
    document["hunks"] = list(reversed(document["hunks"]))

    assert run_v2_receipt_gate(root, tmp_path / "baseline", monkeypatch, document) == 2
    assert_invalid_semantic_review(
        capsys, "items.2.hunks.0.path: does not match recomputed path"
    )


def test_v2_item2_wrong_path_is_invalid(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    document = synthetic_v2_hunk_receipt()
    document["hunks"][0]["path"] = "core/other.py"

    assert run_v2_receipt_gate(root, tmp_path / "baseline", monkeypatch, document) == 2
    assert_invalid_semantic_review(
        capsys, "items.2.hunks.0.path: does not match recomputed path"
    )


def test_v2_item2_wrong_hunk_range_is_invalid(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    document = synthetic_v2_hunk_receipt()
    document["hunks"][0]["old_start"] = 999

    assert run_v2_receipt_gate(root, tmp_path / "baseline", monkeypatch, document) == 2
    assert_invalid_semantic_review(
        capsys, "items.2.hunks.0.old_start: does not match recomputed hunk range"
    )


def test_v2_item2_wrong_hunk_sha256_is_invalid(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    document = synthetic_v2_hunk_receipt()
    document["hunks"][0]["hunk_sha256"] = "0" * 64

    assert run_v2_receipt_gate(root, tmp_path / "baseline", monkeypatch, document) == 2
    assert_invalid_semantic_review(
        capsys,
        "items.2.hunks.0.hunk_sha256: does not match recomputed raw hunk bytes",
    )


@pytest.mark.parametrize(
    ("def_ids", "detail"),
    [
        ([], "expected non-empty DEF id list"),
        (["DEF-P012-02", "DEF-P012-01"], "DEF ids must be sorted and unique"),
        (["DEF-P012-01", "DEF-P012-01"], "DEF ids must be sorted and unique"),
        (["DEF-P012-09"], "DEF ids must be DEF-P012-01 through DEF-P012-08"),
        (["DEF-P012-00"], "DEF ids must be DEF-P012-01 through DEF-P012-08"),
        (["DEF p012 01"], "DEF ids must be DEF-P012-01 through DEF-P012-08"),
    ],
)
def test_v2_item2_def_ids_rejection_matrix(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    def_ids: list[str],
    detail: str,
) -> None:
    root = tmp_path / "root"
    document = synthetic_v2_hunk_receipt()
    document["hunks"][0]["def_ids"] = def_ids

    assert run_v2_receipt_gate(root, tmp_path / "baseline", monkeypatch, document) == 2
    assert_invalid_semantic_review(capsys, f"items.2.hunks.0.def_ids: {detail}")


def test_v2_item2_shared_unknown_row_is_invalid(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    document = synthetic_v2_hunk_receipt()
    document["hunks"][1]["section18_row"] = "S18-99"

    assert run_v2_receipt_gate(root, tmp_path / "baseline", monkeypatch, document) == 2
    assert_invalid_semantic_review(
        capsys, "items.2.hunks.1.section18_row: unknown section-18 census row"
    )


@pytest.mark.parametrize(
    ("served_def_ids", "detail"),
    [
        (["DEF-P012-04"], "served DEF set does not match the ratified section-18 census row"),
        (["DEF-P012-04", "DEF-P012-05", "DEF-P012-06"], "served DEF set does not match the ratified section-18 census row"),
        (["DEF-P012-06", "DEF-P012-04"], "DEF ids must be sorted and unique"),
        (["DEF-P012-04", "DEF-P012-04"], "DEF ids must be sorted and unique"),
        (["DEF-P012-09"], "DEF ids must be DEF-P012-01 through DEF-P012-08"),
    ],
)
def test_v2_item2_shared_served_def_set_rejection_matrix(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    served_def_ids: list[str],
    detail: str,
) -> None:
    root = tmp_path / "root"
    document = synthetic_v2_hunk_receipt()
    document["hunks"][1]["served_def_ids"] = served_def_ids

    assert run_v2_receipt_gate(root, tmp_path / "baseline", monkeypatch, document) == 2
    assert_invalid_semantic_review(
        capsys, f"items.2.hunks.1.served_def_ids: {detail}"
    )


def test_v2_item2_undocumented_empty_reason_is_invalid(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    document = synthetic_v2_hunk_receipt()
    document["hunks"][0]["terminal_class"] = "UNDOCUMENTED"
    document["hunks"][0].pop("def_ids")
    document["hunks"][0]["reason"] = "   "

    assert run_v2_receipt_gate(root, tmp_path / "baseline", monkeypatch, document) == 2
    assert_invalid_semantic_review(
        capsys, "items.2.hunks.0.reason: nonempty reason required"
    )


def test_v2_item2_undocumented_hunk_always_refuses_item_2(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    document = synthetic_v2_hunk_receipt()
    document["hunks"][0]["terminal_class"] = "UNDOCUMENTED"
    document["hunks"][0].pop("def_ids")
    document["hunks"][0]["reason"] = "no DEF authority names this hunk"

    assert run_v2_receipt_gate(root, tmp_path / "baseline", monkeypatch, document) == 2
    assert_invalid_semantic_review(
        capsys, "items.2: UNDOCUMENTED hunk refuses item 2 for core/**"
    )


def test_v2_item2_unknown_terminal_class_is_invalid(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    document = synthetic_v2_hunk_receipt()
    document["hunks"][0]["terminal_class"] = "MAYBE"

    assert run_v2_receipt_gate(root, tmp_path / "baseline", monkeypatch, document) == 2
    assert_invalid_semantic_review(
        capsys, "items.2.hunks.0.terminal_class: outside closed domain"
    )


def test_v2_item2_mixed_class_payload_is_invalid(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    document = synthetic_v2_hunk_receipt()
    document["hunks"][0]["section18_row"] = "S18-05"

    assert run_v2_receipt_gate(root, tmp_path / "baseline", monkeypatch, document) == 2
    assert_invalid_semantic_review(
        capsys, "items.2.hunks.0.section18_row: unknown member"
    )


def test_v2_parse_hunk_diff_uses_exact_raw_bytes() -> None:
    parsed = verify_bceg.parse_hunk_diff(SYNTHETIC_DIFF_BYTES)

    assert [hunk.path for hunk in parsed] == [
        "core/position_sizer.py",
        "core/exits.py",
    ]
    assert (parsed[0].old_start, parsed[0].old_count) == (43, 7)
    assert (parsed[0].new_start, parsed[0].new_count) == (43, 14)
    assert (parsed[1].old_start, parsed[1].old_count) == (353, 5)
    assert (parsed[1].new_start, parsed[1].new_count) == (353, 8)
    assert parsed[0].raw_bytes.startswith(b"@@ -43,7 +43,14 @@")
    assert len(parsed) == 2


def test_v2_parse_refuses_binary_diff() -> None:
    with pytest.raises(GateRefusal) as caught:
        verify_bceg.parse_hunk_diff(
            b"diff --git a/core/foo.png b/core/foo.png\n"
            b"index 0000000..1111111 100644\n"
            b"Binary files a/core/foo.png and b/core/foo.png differ\n"
        )
    assert caught.value.check_id == "SEMANTIC_COVERAGE_REVIEW_INVALID"
    assert caught.value.detail == "items.2: binary diff refused"


def test_v2_parse_refuses_submodule_diff() -> None:
    with pytest.raises(GateRefusal) as caught:
        verify_bceg.parse_hunk_diff(
            b"diff --git a/core/sub b/core/sub\n"
            b"index 1111111..2222222 160000\n"
            b"--- a/core/sub\n"
            b"+++ b/core/sub\n"
            b"Subproject commit 1111111111111111111111111111111111111111\n"
        )
    assert caught.value.check_id == "SEMANTIC_COVERAGE_REVIEW_INVALID"
    assert caught.value.detail == "items.2: submodule diff refused"


def test_v2_parse_refuses_rename_diff() -> None:
    with pytest.raises(GateRefusal) as caught:
        verify_bceg.parse_hunk_diff(
            b"diff --git a/core/foo.py b/core/bar.py\n"
            b"similarity index 100%\n"
            b"rename from core/foo.py\n"
            b"rename to core/bar.py\n"
        )
    assert caught.value.check_id == "SEMANTIC_COVERAGE_REVIEW_INVALID"
    assert caught.value.detail == "items.2: rename/copy diff refused"


def test_v2_parse_refuses_no_text_hunks() -> None:
    with pytest.raises(GateRefusal) as caught:
        verify_bceg.parse_hunk_diff(
            b"diff --git a/core/foo.py b/core/foo.py\n"
            b"old mode 100644\n"
            b"new mode 100755\n"
        )
    assert caught.value.check_id == "SEMANTIC_COVERAGE_REVIEW_INVALID"
    assert caught.value.detail == "items.2: diff file has no text hunks"


def test_v2_parse_refuses_unparsed_metadata() -> None:
    with pytest.raises(GateRefusal) as caught:
        verify_bceg.parse_hunk_diff(
            b"diff --git a/core/foo.py b/core/foo.py\n"
            b"totally unknown line\n"
        )
    assert caught.value.check_id == "SEMANTIC_COVERAGE_REVIEW_INVALID"
    assert caught.value.detail == "items.2: unparsed diff metadata refused"


def test_v2_parse_empty_diff_yields_no_hunks() -> None:
    assert verify_bceg.parse_hunk_diff(b"") == []


def core_hunk_repository(tmp_path: Path) -> tuple[Path, str, str]:
    root = tmp_path / "repo"
    root.mkdir(parents=True)
    for command in (
        ("init",),
        ("config", "user.email", "v2@example.invalid"),
        ("config", "user.name", "V2 selftest"),
        ("config", "core.autocrlf", "false"),
    ):
        subprocess.run(
            ["git", "-C", str(root), *command],
            check=True,
            capture_output=True,
            text=True,
        )
    core = root / "core"
    core.mkdir()
    (core / "position_sizer.py").write_text(
        "\n".join(f"value_{index} = {index}" for index in range(1, 21)) + "\n",
        encoding="utf-8", newline="\n"
    )
    (core / "exits.py").write_text("exit_value = 1\n", encoding="utf-8", newline="\n")
    subprocess.run(["git", "-C", str(root), "add", "core"], check=True, capture_output=True, text=True)
    subprocess.run(["git", "-C", str(root), "commit", "-m", "base"], check=True, capture_output=True, text=True)
    base = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    (core / "position_sizer.py").write_text(
        "\n".join(
            f"value_{index} = {index + 100 if index in (2, 18) else index}"
            for index in range(1, 21)
        ) + "\n",
        encoding="utf-8", newline="\n"
    )
    (core / "exits.py").write_text("exit_value = 2\n", encoding="utf-8", newline="\n")
    subprocess.run(["git", "-C", str(root), "add", "core"], check=True, capture_output=True, text=True)
    subprocess.run(["git", "-C", str(root), "commit", "-m", "reviewed"], check=True, capture_output=True, text=True)
    head = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    return root, base, head


def _real_v2_receipt(
    root: Path, base: str, head: str, diff_bytes: bytes
) -> dict[str, object]:
    parsed = verify_bceg.parse_hunk_diff(diff_bytes)
    path_order: list[str] = []
    path_hunks: dict[str, list[int]] = {}
    for index, hunk in enumerate(parsed):
        path_hunks.setdefault(hunk.path, []).append(index)
        if hunk.path not in path_order:
            path_order.append(hunk.path)

    served_def_ids = {
        1: [f"DEF-P012-{number:02d}" for number in range(1, 9)],
        2: [
            "DEF-P012-01",
            "DEF-P012-02",
            "DEF-P012-04",
            "DEF-P012-05",
            "DEF-P012-06",
            "DEF-P012-07",
            "DEF-P012-08",
        ],
        3: ["DEF-P012-01", "DEF-P012-02"],
        4: ["DEF-P012-03"],
        5: ["DEF-P012-04", "DEF-P012-06"],
        6: ["DEF-P012-05", "DEF-P012-07", "DEF-P012-08"],
        7: ["DEF-P012-03", "DEF-P012-05", "DEF-P012-07"],
        8: [
            "DEF-P012-02",
            "DEF-P012-03",
            "DEF-P012-04",
            "DEF-P012-06",
        ],
        9: ["DEF-P012-08"],
        10: ["DEF-P012-07"],
        11: ["DEF-P012-07", "DEF-P012-08"],
        12: [],
    }
    records = [
        {
            "path": hunk.path,
            "old_start": hunk.old_start,
            "old_count": hunk.old_count,
            "new_start": hunk.new_start,
            "new_count": hunk.new_count,
            "hunk_sha256": hashlib.sha256(hunk.raw_bytes).hexdigest(),
            "terminal_class": "SECTION18_SHARED",
            "section18_row": "S18-05",
            "served_def_ids": served_def_ids[5],
        }
        for hunk in parsed
    ]
    return {
        "schema": verify_bceg.SEMANTIC_HUNK_COVERAGE_SCHEMA,
        "base_commit": base,
        "reviewed_head": head,
        "diff_command": verify_bceg.canonical_hunk_diff_command(head),
        "diff_sha256": hashlib.sha256(diff_bytes).hexdigest(),
        "total_changed_paths": len(path_order),
        "total_changed_files": len(path_order),
        "changed_paths": [
            {
                "path": path,
                "hunk_count": len(indices),
                "hunk_indices": indices,
                "hunk_sha256s": [
                    hashlib.sha256(parsed[index].raw_bytes).hexdigest()
                    for index in indices
                ],
            }
            for path, indices in ((path, path_hunks[path]) for path in path_order)
        ],
        "section18_coverage": [
            {
                "row": f"S18-{number:02d}",
                "served_def_ids": served_def_ids[number],
                "hunk_indices": [index for index in range(len(parsed)) if number == 5],
            }
            for number in range(1, 13)
        ],
        "hunks": records,
    }


def test_v2_real_git_receipt_accepts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root, base, head = core_hunk_repository(tmp_path)
    monkeypatch.setattr(verify_bceg, "HUNK_DIFF_BASE_COMMIT", base)
    diff_bytes = verify_bceg.compute_hunk_diff(root, head)
    assert b"diff --git a/core/position_sizer.py" in diff_bytes

    receipt = _real_v2_receipt(root, base, head, diff_bytes)
    evidence = root / "review-evidence" / "item-2-hunks.json"
    evidence.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_bytes(verify_bceg.canonical_json_bytes(receipt))
    write_synthetic_reseal_manifest(
        root, [{"actor": f"Synthetic Lead, re-seal #{n}"} for n in range(5, 10)]
    )
    manifest = load_json_exact(root / "tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json")

    verify_bceg._validate_item2_hunk_coverage(
        root, receipt, head, verify_bceg.derive_section18_served_def_sets(root, manifest)
    )


@pytest.mark.parametrize("mutation", [
    "missing_path", "duplicate_path", "reordered_path", "missing_row", "duplicate_row",
    "reordered_row", "duplicate_owner", "missing_assignment", "out_of_range_index",
])
def test_v2_real_git_receipt_census_mutations_refuse(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, mutation: str
) -> None:
    root, base, head = core_hunk_repository(tmp_path)
    monkeypatch.setattr(verify_bceg, "HUNK_DIFF_BASE_COMMIT", base)
    diff_bytes = verify_bceg.compute_hunk_diff(root, head)
    receipt = _real_v2_receipt(root, base, head, diff_bytes)
    if mutation == "missing_path":
        receipt["changed_paths"].pop()
    elif mutation == "duplicate_path":
        receipt["changed_paths"].append(deepcopy(receipt["changed_paths"][0]))
    elif mutation == "reordered_path":
        receipt["changed_paths"] = list(reversed(receipt["changed_paths"]))
    elif mutation == "missing_row":
        receipt["section18_coverage"].pop()
    elif mutation == "duplicate_row":
        receipt["section18_coverage"].append(deepcopy(receipt["section18_coverage"][0]))
    elif mutation == "reordered_row":
        receipt["section18_coverage"][4], receipt["section18_coverage"][5] = (
            receipt["section18_coverage"][5], receipt["section18_coverage"][4]
        )
    elif mutation == "duplicate_owner":
        receipt["section18_coverage"][4]["hunk_indices"] = [0, 0]
    elif mutation == "missing_assignment":
        receipt["section18_coverage"][4]["hunk_indices"] = []
    elif mutation == "out_of_range_index":
        receipt["section18_coverage"][4]["hunk_indices"] = [999]
    write_synthetic_reseal_manifest(
        root, [{"actor": "Synthetic Lead, re-seal #5"}]
    )
    manifest = load_json_exact(root / "tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json")
    with pytest.raises(GateRefusal):
        verify_bceg._validate_item2_hunk_coverage(
            root, receipt, head, derive_section18_served_def_sets(root, manifest)
        )


@pytest.mark.parametrize(
    "served",
    [
        "`DEF-P012-01`, `DEF-P012-01`",
        "`DEF-P012-01`, `DEF-P012-09`",
        "`DEF-P012-010`",
        "`DEF-P012-02`, `DEF-P012-01`",
    ],
)
def test_v2_section18_served_cell_closed_grammar_refuses(
    tmp_path: Path, served: str
) -> None:
    root = tmp_path / "root"
    write_synthetic_reseal_manifest(root, [{"actor": "Synthetic Lead, re-seal #5"}])
    design = root / "design.md"
    text = design.read_text(encoding="utf-8")
    design.write_text(text.replace("`DEF-P012-01`, `DEF-P012-02`", served), encoding="utf-8", newline="\n")
    manifest_path = root / "tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json"
    manifest = load_json_exact(manifest_path)
    manifest["design"]["sha256"] = verify_bceg.sha256_file(design)
    manifest_path.write_bytes(verify_bceg.canonical_json_bytes(manifest))
    with pytest.raises(GateRefusal):
        derive_section18_served_def_sets(root, manifest)


def test_v2_section18_served_cell_accepts_exact_ordered_tokens(tmp_path: Path) -> None:
    root = tmp_path / "root"
    write_synthetic_reseal_manifest(root, [{"actor": "Synthetic Lead, re-seal #5"}])
    manifest = load_json_exact(root / "tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json")
    sets = derive_section18_served_def_sets(root, manifest)
    assert sets["S18-02"] == frozenset(
        {"DEF-P012-01", "DEF-P012-02", "DEF-P012-04", "DEF-P012-05", "DEF-P012-06", "DEF-P012-07", "DEF-P012-08"}
    )


def test_v2_schema_accepts_complete_receipt_and_rejects_nested_mutants() -> None:
    schema = json.loads(
        (MTC_V2_ROOT / "tests/corrected_vnext/contracts/semantic_coverage_review.schema.json").read_text()
    )
    validator = Draft202012Validator(schema)
    receipt = semantic_review_fixture(Path(tempfile.mkdtemp(prefix="schema-receipt-")))
    receipt["owner_ratification"]["chain"] = [
        "#5", "#6", "#7", "#8", "#9", "#10", "#11", "#12", "#12b", "#13",
        "#14", "#14b", "#15", "#16", "#17", "#18", "#19", "#20", "#21", "#22", "#23",
    ]
    assert list(validator.iter_errors(receipt)) == []
    mutants = [
        ("changed_paths", [True]),
        ("section18_coverage", None),
        ("hunks", [1]),
        ("hunks", [{**receipt["items"]["2"]["hunk_coverage"]["hunks"][0], "terminal_class": "DEF", "section18_row": "S18-05"}]),
    ]
    for member, value in mutants:
        candidate = deepcopy(receipt)
        if member == "hunks":
            candidate["items"]["2"]["hunk_coverage"][member] = value
        else:
            candidate["items"]["2"]["hunk_coverage"][member] = value
        assert list(validator.iter_errors(candidate)), member


def test_v2_real_git_receipt_wrong_digest_refuses(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root, base, head = core_hunk_repository(tmp_path)
    monkeypatch.setattr(verify_bceg, "HUNK_DIFF_BASE_COMMIT", base)
    diff_bytes = verify_bceg.compute_hunk_diff(root, head)
    receipt = _real_v2_receipt(root, base, head, diff_bytes)
    receipt["diff_sha256"] = "0" * 64
    evidence = root / "review-evidence" / "item-2-hunks.json"
    evidence.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_bytes(verify_bceg.canonical_json_bytes(receipt))
    write_synthetic_reseal_manifest(
        root, [{"actor": f"Synthetic Lead, re-seal #{n}"} for n in range(5, 10)]
    )
    write_synthetic_reseal_manifest(
        root, [{"actor": "Synthetic Lead, re-seal #5"}]
    )
    manifest = load_json_exact(root / "tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json")

    with pytest.raises(GateRefusal) as caught:
        verify_bceg._validate_item2_hunk_coverage(
            root, receipt, head, verify_bceg.derive_section18_served_def_sets(root, manifest)
        )
    assert caught.value.detail == "items.2.diff_sha256: does not match recomputed diff"


def drifted_core_repository(tmp_path: Path) -> tuple[Path, str, str, str]:
    root = tmp_path / "repo"
    root.mkdir(parents=True)
    for command in (
        ("init",),
        ("config", "user.email", "v2@example.invalid"),
        ("config", "user.name", "V2 selftest"),
        ("config", "core.autocrlf", "false"),
    ):
        subprocess.run(
            ["git", "-C", str(root), *command],
            check=True,
            capture_output=True,
            text=True,
        )
    core = root / "core"
    core.mkdir()
    marker = root / "receipt.txt"
    marker.write_text("base\n", encoding="utf-8", newline="\n")
    (core / "a.py").write_text("1\n", encoding="utf-8", newline="\n")
    subprocess.run(["git", "-C", str(root), "add", "."], check=True, capture_output=True, text=True)
    subprocess.run(["git", "-C", str(root), "commit", "-m", "base"], check=True, capture_output=True, text=True)
    base = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    (core / "a.py").write_text("2\n", encoding="utf-8", newline="\n")
    subprocess.run(["git", "-C", str(root), "add", "core"], check=True, capture_output=True, text=True)
    subprocess.run(["git", "-C", str(root), "commit", "-m", "reviewed"], check=True, capture_output=True, text=True)
    reviewed = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    (core / "a.py").write_text("3\n", encoding="utf-8", newline="\n")
    marker.write_text("base\nreceipt\n", encoding="utf-8", newline="\n")
    subprocess.run(["git", "-C", str(root), "add", "."], check=True, capture_output=True, text=True)
    subprocess.run(["git", "-C", str(root), "commit", "-m", "receipt"], check=True, capture_output=True, text=True)
    head = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    return root, base, reviewed, head


def test_v2_reviewed_head_core_drift_refuses(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root, base, reviewed, head = drifted_core_repository(tmp_path)
    monkeypatch.setattr(verify_bceg, "HUNK_DIFF_BASE_COMMIT", base)
    monkeypatch.setattr(
        verify_bceg, "compute_hunk_diff", lambda _root, _head: SYNTHETIC_DIFF_BYTES
    )
    receipt = semantic_review_fixture(root, reviewed_head=reviewed)
    write_synthetic_reseal_manifest(
        root, [{"actor": f"Synthetic Lead, re-seal #{n}"} for n in range(5, 10)]
    )
    review = root / "tests/corrected_vnext/contracts/semantic_coverage_review.json"
    review.parent.mkdir(parents=True, exist_ok=True)
    review.write_bytes(verify_bceg.canonical_json_bytes(receipt))
    measured = dict(SYNTHETIC_REVIEW_IDENTITIES)
    measured["worktree_head_commit"] = head
    measured["core_tree_oid"] = verify_bceg.semantic_review_core_tree(root, head)

    with pytest.raises(GateRefusal) as caught:
        verify_bceg.validate_semantic_coverage_review(review, root, measured)
    assert caught.value.check_id == "SEMANTIC_COVERAGE_REVIEW_INVALID"
    assert caught.value.detail == (
        "reviewed_identities.core_tree_oid: "
        "reviewed-head core tree does not match current core tree"
    )


def test_v2_reviewed_head_core_identity_matches_clears(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root, base, reviewed, head = drifted_core_repository(tmp_path)
    monkeypatch.setattr(verify_bceg, "HUNK_DIFF_BASE_COMMIT", base)
    monkeypatch.setattr(
        verify_bceg, "compute_hunk_diff", lambda _root, _head: SYNTHETIC_DIFF_BYTES
    )
    receipt = semantic_review_fixture(root, reviewed_head=head)
    write_synthetic_reseal_manifest(
        root, [{"actor": f"Synthetic Lead, re-seal #{n}"} for n in range(5, 10)]
    )
    measured = dict(SYNTHETIC_REVIEW_IDENTITIES)
    measured["worktree_head_commit"] = head
    measured["core_tree_oid"] = verify_bceg.semantic_review_core_tree(root, head)
    receipt["reviewed_identities"]["core_tree_oid"] = measured["core_tree_oid"]
    review = root / "tests/corrected_vnext/contracts/semantic_coverage_review.json"
    review.parent.mkdir(parents=True, exist_ok=True)
    review.write_bytes(verify_bceg.canonical_json_bytes(receipt))

    verify_bceg.validate_semantic_coverage_review(review, root, measured)


def test_w352_old_chain_is_refused_when_manifest_is_past_nine(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    receipt = semantic_review_fixture(root)
    write_synthetic_reseal_manifest(
        root,
        [
            {"actor": f"Synthetic Lead, re-seal #{seal_id}"}
            for seal_id in range(5, 11)
        ],
    )
    review = root / "tests/corrected_vnext/contracts/semantic_coverage_review.json"
    review.write_bytes(verify_bceg.canonical_json_bytes(receipt))

    assert run_synthetic_full_gate(root, tmp_path / "baseline", monkeypatch) == 2
    assert_invalid_semantic_review(
        capsys,
        "owner_ratification.chain: expected seal ids #5, #6, #7, #8, #9, #10",
    )


def test_w352_manifest_derived_chain_clears_ratification_check(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    receipt = semantic_review_fixture(root)
    derived_chain = [f"#{seal_id}" for seal_id in range(5, 11)]
    write_synthetic_reseal_manifest(
        root,
        [
            {"actor": f"Synthetic Lead, re-seal {seal_id}"}
            for seal_id in derived_chain
        ],
    )
    receipt["owner_ratification"]["chain"] = derived_chain
    review = root / "tests/corrected_vnext/contracts/semantic_coverage_review.json"
    review.write_bytes(verify_bceg.canonical_json_bytes(receipt))

    assert run_synthetic_full_gate(root, tmp_path / "baseline", monkeypatch) == 0
    gate_receipt = json.loads(capsys.readouterr().out)
    assert gate_receipt["claim_label"] == verify_bceg.ACCEPTING_LABEL


def test_w352_reseal_absent_from_manifest_is_refused(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    receipt = semantic_review_fixture(root)
    derived_chain = [f"#{seal_id}" for seal_id in range(5, 11)]
    write_synthetic_reseal_manifest(
        root,
        [
            {"actor": f"Synthetic Lead, re-seal {seal_id}"}
            for seal_id in derived_chain
        ],
    )
    receipt["owner_ratification"]["chain"] = [*derived_chain, "#999"]
    review = root / "tests/corrected_vnext/contracts/semantic_coverage_review.json"
    review.write_bytes(verify_bceg.canonical_json_bytes(receipt))

    assert run_synthetic_full_gate(root, tmp_path / "baseline", monkeypatch) == 2
    assert_invalid_semantic_review(
        capsys,
        "owner_ratification.chain: expected seal ids #5, #6, #7, #8, #9, #10",
    )


def test_w352_derivation_handles_legacy_corrective_and_base_history_rows() -> None:
    manifest = {
        "reseal_history": [
            {"actor": "Synthetic legacy Lead"},
            {"actor": "Synthetic legacy Lead"},
            {"actor": "Synthetic Lead, re-seal #4"},
            {"actor": "Synthetic Lead, re-seal #5"},
            {"actor": "Synthetic Lead, re-seal #5b (metadata only)"},
            {
                "actor": (
                    "Synthetic Lead, base re-anchor (decision 1); "
                    "seal value unchanged"
                )
            },
            {"actor": "Synthetic Lead, re-seal #6"},
        ]
    }

    assert verify_bceg.derive_semantic_coverage_review_chain(manifest) == [
        "#5",
        "#5b",
        "#6",
    ]


def test_full_gate_refuses_a_red_contract_selftest_suite(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    root = tmp_path / "root"
    receipt = semantic_review_fixture(root)
    review = root / "tests/corrected_vnext/contracts/semantic_coverage_review.json"
    review.parent.mkdir(parents=True)
    review.write_bytes(verify_bceg.canonical_json_bytes(receipt))
    failing_test_id = (
        "mtc_v2/tests/corrected_vnext/contracts/selftests/test_verify_bceg.py::"
        "test_probe_driver_refuses_unclosed_base_before_variant_comparison"
    )

    assert run_synthetic_full_gate(
        root,
        tmp_path / "baseline",
        monkeypatch,
        contract_selftests={
            "ran": True,
            "returncode": 1,
            "passed_count": 1,
            "failed_count": 1,
            "failing_test_ids": [failing_test_id],
        },
    ) == 2
    gate_receipt = json.loads(capsys.readouterr().out)
    assert gate_receipt["claim_label"] == verify_bceg.REFUSAL_LABEL
    assert gate_receipt["refusals"] == [
        {
            "check_id": "CONTRACT_SELFTEST_RED",
            "detail": "1 contract self-test failed",
            "failing_test_ids": [failing_test_id],
        }
    ]
    assert gate_receipt["contract_selftest_suite"] == {
        "ran": True,
        "returncode": 1,
        "passed_count": 1,
        "failed_count": 1,
        "failing_test_ids": [failing_test_id],
    }


def test_contract_selftest_suite_reports_only_failing_test_ids(tmp_path: Path) -> None:
    root = tmp_path / "mtc_v2"
    suite = root / "tests/corrected_vnext/contracts/selftests"
    suite.mkdir(parents=True)
    (suite / "test_synthetic_contract.py").write_text(
        "def test_failing_contract():\n"
        "    assert False\n\n"
        "def test_passing_contract():\n"
        "    assert True\n",
        encoding="utf-8",
        newline="\n",
    )

    result = verify_bceg.run_contract_selftest_suite(root)

    assert result["returncode"] != 0
    assert result["ran"] is True
    assert result["passed_count"] == 1
    assert result["failed_count"] == 1
    assert result["failing_test_ids"] == [
        "mtc_v2/tests/corrected_vnext/contracts/selftests/"
        "test_synthetic_contract.py::test_failing_contract"
    ]


def test_contract_selftest_suite_reports_empty_failure_ids_when_all_pass(
    tmp_path: Path,
) -> None:
    root = tmp_path / "mtc_v2"
    suite = root / "tests/corrected_vnext/contracts/selftests"
    suite.mkdir(parents=True)
    (suite / "test_synthetic_contract.py").write_text(
        "def test_passing_contract():\n"
        "    assert True\n",
        encoding="utf-8",
        newline="\n",
    )

    result = verify_bceg.run_contract_selftest_suite(root)

    assert result == {
        "ran": True,
        "returncode": 0,
        "passed_count": 1,
        "failed_count": 0,
        "failing_test_ids": [],
    }


def test_contract_selftest_suite_records_timeout(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def raise_timeout(command: list[str], **kwargs: object) -> None:
        raise subprocess.TimeoutExpired(command, timeout=kwargs["timeout"])

    monkeypatch.setattr(verify_bceg.subprocess, "run", raise_timeout)

    assert verify_bceg.run_contract_selftest_suite(tmp_path) == {
        "ran": True,
        "returncode": 124,
        "passed_count": None,
        "failed_count": None,
        "failing_test_ids": [],
        "detail": "contract self-test suite timed out after 600 seconds",
    }


def test_contract_selftest_suite_records_oserror(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def raise_oserror(_command: list[str], **_kwargs: object) -> None:
        raise OSError("synthetic launch failure")

    monkeypatch.setattr(verify_bceg.subprocess, "run", raise_oserror)

    assert verify_bceg.run_contract_selftest_suite(tmp_path) == {
        "ran": False,
        "returncode": 126,
        "passed_count": None,
        "failed_count": None,
        "failing_test_ids": [],
        "detail": "contract self-test suite could not start: synthetic launch failure",
    }


def sealed_producer_fixture(
    tmp_path: Path,
) -> tuple[Path, Path, str, Path]:
    root = tmp_path / "root"
    contracts = root / "tests" / "corrected_vnext" / "contracts"
    baseline_root = tmp_path / "baseline"
    contract_paths = [contracts / "scenario_catalog.json"] + [
        contracts / f"member-{index:02d}.json" for index in range(1, 19)
    ]
    manifest_members: list[dict[str, object]] = []
    for index, path in enumerate(contract_paths):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(verify_bceg.canonical_json_bytes({"member": index}))
        manifest_members.append(
            {
                "path": path.relative_to(contracts).as_posix(),
                "sha256": verify_bceg.sha256_file(path),
                "bytes": path.stat().st_size,
            }
        )
    seal_lines = [
        f"{member['path']}:{member['sha256']}" for member in manifest_members
    ]
    seal = hashlib.sha256(
        "\n".join(sorted(seal_lines)).encode("utf-8")
    ).hexdigest()
    design_path = root / "design.md"
    design_path.write_bytes(b"Design pin\nSecond line\n")
    (contracts / "CONTRACT_TABLES_MANIFEST.json").write_bytes(
        verify_bceg.canonical_json_bytes(
            {
                "schema": "P012_CONTRACT_TABLES_MANIFEST_V1",
                "files": manifest_members,
                "design": {
                    "file": str(design_path),
                    "sha256": verify_bceg.sha256_file(design_path),
                    "total_lines": 2,
                },
                "seal": {"EXPECTED_SEAL_SHA": seal},
            }
        )
    )
    anchor_path = contracts / "implementation_anchor.json"
    anchor_path.write_bytes(
        verify_bceg.canonical_json_bytes({"EXPECTED_SEAL_SHA": seal})
    )
    (contracts / "implementation_anchor.json.sha256").write_text(
        f"{verify_bceg.sha256_file(anchor_path)}  implementation_anchor.json\n",
        encoding="ascii",
        newline="\n",
    )

    driver_path = baseline_root / "driver.py"
    driver_path.parent.mkdir(parents=True, exist_ok=True)
    driver_path.write_bytes(b"synthetic driver\n")
    baseline_members: list[dict[str, str]] = []
    for index in range(36):
        relative = f"scenario/member-{index:02d}.json"
        path = baseline_root / "out" / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(verify_bceg.canonical_json_bytes({"member": index}))
        baseline_members.append(
            {"path": relative, "sha256": verify_bceg.sha256_file(path)}
        )
    (baseline_root / "BASELINE_BYTES_MANIFEST.json").write_bytes(
        verify_bceg.canonical_json_bytes(
            {
                "schema": "P012_BASELINE_BYTES_MANIFEST_V1",
                "EXPECTED_SEAL_SHA_consumed": seal,
                "catalog": {
                    "sha256": verify_bceg.sha256_file(
                        contracts / "scenario_catalog.json"
                    )
                },
                "driver": {
                    "path": str(driver_path),
                    "sha256": verify_bceg.sha256_file(driver_path),
                },
                "files": baseline_members,
                "run_summary": {
                    "scenarios": 17,
                    "red": 9,
                    "green": 8,
                    "completed": 17,
                    "blocked": 0,
                    "output_files": 36,
                },
            }
        )
    )
    return root, baseline_root, seal, contract_paths[1]


def legacy_event_order_pin_fixture(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[Path, Path, dict[str, str], str, Path, Path]:
    root = tmp_path / "root"
    baseline_root = tmp_path / "baseline"
    contracts = root / "tests" / "corrected_vnext" / "contracts"
    contracts.mkdir(parents=True)
    mapping = {
        "RULE2-01-RED/event_surface/0/events": "LEGACY_EVENT_ORDINAL_V1"
    }
    digest = hashlib.sha256(verify_bceg.canonical_json_bytes(mapping)).hexdigest()
    manifest_path = contracts / "CONTRACT_TABLES_MANIFEST.json"
    anchor_path = contracts / "implementation_anchor.json"
    manifest_path.write_bytes(
        verify_bceg.canonical_json_bytes(
            {
                "legacy_event_order_map_pin": {
                    "legacy_event_order_map": mapping,
                    "legacy_event_order_map_sha256": digest,
                }
            }
        )
    )
    anchor_path.write_bytes(
        verify_bceg.canonical_json_bytes(
            {"legacy_event_order_map_sha256": digest}
        )
    )
    corpus = verify_bceg.Corpus(
        root=root,
        baseline_root=baseline_root,
        catalog=[],
        blockers=(),
        identities={},
    )
    monkeypatch.setattr(
        verify_bceg, "validate_catalog", lambda _root, _baseline_root: corpus
    )
    monkeypatch.setattr(
        verify_bceg,
        "compute_legacy_event_order_map",
        lambda _corpus: (mapping, digest),
    )
    monkeypatch.setattr(
        verify_bceg,
        "validate_expected_source_provenance",
        lambda *_args: {"status": "MATCH"},
    )
    return root, baseline_root, mapping, digest, manifest_path, anchor_path


def test_sealed_producer_validation_accepts_manifest_recorded_current_seal(
    tmp_path: Path,
) -> None:
    root, baseline_root, current_seal, _member_path = sealed_producer_fixture(
        tmp_path
    )

    assert current_seal != (
        "02b47a8e5c4a1a9ab9a671f5a14a3dc89f13fb80584dfd8648784d69515a0858"
    )
    identities = verify_bceg.validate_sealed_producers(root, baseline_root)
    assert identities["expected_seal_sha256"] == current_seal


def test_sealed_producer_validation_refuses_one_byte_changed_design_copy(
    tmp_path: Path,
) -> None:
    root, baseline_root, _current_seal, _member_path = sealed_producer_fixture(
        tmp_path
    )
    (root / "design.md").write_bytes(b"Design qin\nSecond line\n")

    refusal(
        "DESIGN_PIN_MISMATCH",
        lambda: verify_bceg.validate_sealed_producers(root, baseline_root),
    )


def test_design_pin_refuses_relative_path_even_when_cwd_can_reach_same_bytes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root, baseline_root, _seal, _member_path = sealed_producer_fixture(tmp_path)
    manifest_path = root / "tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json"
    manifest = load_json_exact(manifest_path)
    manifest["design"]["file"] = "design.md"
    manifest_path.write_bytes(verify_bceg.canonical_json_bytes(manifest))
    monkeypatch.chdir(root)
    refusal(
        "DESIGN_PIN_MISMATCH",
        lambda: verify_bceg.validate_sealed_producers(root, baseline_root),
    )


def test_design_pin_refuses_symlink_to_identical_bytes(
    tmp_path: Path,
) -> None:
    root, baseline_root, _seal, _member_path = sealed_producer_fixture(tmp_path)
    design = root / "design.md"
    target = root / "design-copy.md"
    try:
        target.symlink_to(design)
    except OSError:
        pytest.skip("symlink creation unavailable")
    manifest_path = root / "tests/corrected_vnext/contracts/CONTRACT_TABLES_MANIFEST.json"
    manifest = load_json_exact(manifest_path)
    manifest["design"]["file"] = str(target)
    manifest_path.write_bytes(verify_bceg.canonical_json_bytes(manifest))
    refusal(
        "DESIGN_PIN_MISMATCH",
        lambda: verify_bceg.validate_sealed_producers(root, baseline_root),
    )


def test_sealed_producer_validation_refuses_modified_copy_with_stale_recorded_seal(
    tmp_path: Path,
) -> None:
    root, baseline_root, _current_seal, member_path = sealed_producer_fixture(
        tmp_path
    )
    contracts = root / "tests" / "corrected_vnext" / "contracts"
    manifest_path = contracts / "CONTRACT_TABLES_MANIFEST.json"
    member_path.write_bytes(
        verify_bceg.canonical_json_bytes({"member": "modified-copy"})
    )
    manifest = verify_bceg.load_json_exact(manifest_path)
    member = next(
        item
        for item in manifest["files"]
        if item["path"] == member_path.relative_to(contracts).as_posix()
    )
    member["sha256"] = verify_bceg.sha256_file(member_path)
    member["bytes"] = member_path.stat().st_size
    manifest_path.write_bytes(verify_bceg.canonical_json_bytes(manifest))

    refusal(
        "EXPECTED_SEAL_MISMATCH",
        lambda: verify_bceg.validate_sealed_producers(root, baseline_root),
    )


def test_expected_source_provenance_refuses_copy_observed_method() -> None:
    contracts = MTC_V2_ROOT / "tests/corrected_vnext/contracts"
    manifest = load_json_exact(contracts / "CONTRACT_TABLES_MANIFEST.json")
    anchor = load_json_exact(contracts / "implementation_anchor.json")
    manifest["expected_value_provenance"]["method"] = "COPY_OBSERVED"

    refusal(
        "EXPECTED_PROVENANCE_METHOD_INVALID",
        lambda: verify_bceg.validate_expected_source_provenance(
            MTC_V2_ROOT, manifest, anchor
        ),
    )


def test_expected_source_provenance_refuses_non_ancestor_base() -> None:
    contracts = MTC_V2_ROOT / "tests/corrected_vnext/contracts"
    manifest = load_json_exact(contracts / "CONTRACT_TABLES_MANIFEST.json")
    anchor = load_json_exact(contracts / "implementation_anchor.json")
    nonexistent_commit = "f" * 40
    manifest["seal"]["IMPLEMENTATION_BASE_SHA"] = nonexistent_commit
    anchor["IMPLEMENTATION_BASE_SHA"] = nonexistent_commit

    refusal(
        "IMPLEMENTATION_BASE_ANCESTRY_MISMATCH",
        lambda: verify_bceg.validate_expected_source_provenance(
            MTC_V2_ROOT, manifest, anchor
        ),
    )


def test_expected_source_provenance_refuses_expected_path_changed_after_base() -> None:
    with tempfile.TemporaryDirectory(prefix="w385-provenance-", dir=r"C:\tmp") as temporary:
        root = Path(temporary) / "mtc_v2"
        expected_relative = "tests/corrected_vnext/contracts/expected.json"
        implementation_base, _head = two_commit_repository(root, expected_relative)
        manifest = {
            "expected_value_provenance": {
                "method": "INDEPENDENT_DERIVATION",
                "not_method": "COPY_OBSERVED",
            },
            "seal": {"IMPLEMENTATION_BASE_SHA": implementation_base},
            "files": [{"path": "expected.json"}],
        }
        anchor = {"IMPLEMENTATION_BASE_SHA": implementation_base}

        with pytest.raises(GateRefusal) as caught:
            verify_bceg.validate_expected_source_provenance(root, manifest, anchor)
        assert caught.value.check_id == "EXPECTED_PATH_CHANGED_AFTER_BASE"
        assert caught.value.pointer == expected_relative


W305_EXCEPTIONS_RELATIVE = (
    "tests/corrected_vnext/contracts/expected_provenance_exceptions.json"
)
W305_DECISION_134_PATH = (
    "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/"
    "golden/corrected_vnext/RULE2-01-GREEN.json"
)
W342C_MOVED_MANIFEST_PATHS = (
    "expected_provenance_exceptions.json",
    "implementation_anchor.json",
)
W342C_MOVED_GIT_PATHS = tuple(
    "MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/"
    f"tests/corrected_vnext/contracts/{relative}"
    for relative in W342C_MOVED_MANIFEST_PATHS
)


def w342c_provenance_manifest(*moved_paths: str) -> dict[str, object]:
    """Move expected members in-memory to paths changed after the re-anchored base."""

    contracts = MTC_V2_ROOT / "tests/corrected_vnext/contracts"
    manifest = load_json_exact(contracts / "CONTRACT_TABLES_MANIFEST.json")
    record = w305_exception_record()
    assert manifest["seal"]["IMPLEMENTATION_BASE_SHA"] == record[
        "implementation_base_sha"
    ]
    candidates = [
        member
        for member in manifest["files"]
        if member["path"] != "golden/corrected_vnext/RULE2-01-GREEN.json"
    ]
    assert len(candidates) >= len(moved_paths)
    for member, moved_path in zip(
        candidates[: len(moved_paths)], moved_paths, strict=True
    ):
        member["path"] = moved_path
    return manifest


def w305_exception_record() -> dict[str, object]:
    return load_json_exact(MTC_V2_ROOT / W305_EXCEPTIONS_RELATIVE)


def w305_provenance(
    record: dict[str, object] | None,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    moved_paths: tuple[str, ...] = (W342C_MOVED_MANIFEST_PATHS[0],),
):
    """Run the predicate against an isolated record and synthetic changed paths."""

    manifest = w342c_provenance_manifest(*moved_paths)
    contracts = MTC_V2_ROOT / "tests/corrected_vnext/contracts"
    anchor = load_json_exact(contracts / "implementation_anchor.json")
    record_path = tmp_path / "expected_provenance_exceptions.json"
    original_loader = verify_bceg.load_expected_provenance_exceptions
    original_check_output = verify_bceg.subprocess.check_output
    changed_paths = [
        W305_DECISION_134_PATH,
        *W342C_MOVED_GIT_PATHS[: len(moved_paths)],
    ]

    with monkeypatch.context() as synthetic:
        if record is None:
            synthetic.setattr(
                verify_bceg,
                "load_expected_provenance_exceptions",
                lambda _path, _base: {},
            )
        else:
            record_path.write_bytes(verify_bceg.canonical_json_bytes(record))
            synthetic.setattr(
                verify_bceg,
                "load_expected_provenance_exceptions",
                lambda _path, base: original_loader(record_path, base),
            )

        def synthetic_check_output(command, **kwargs):
            if "diff" in command and "--name-only" in command:
                return b"".join(path.encode("utf-8") + b"\0" for path in changed_paths)
            return original_check_output(command, **kwargs)

        synthetic.setattr(verify_bceg.subprocess, "check_output", synthetic_check_output)
        try:
            return verify_bceg.validate_expected_source_provenance(
                MTC_V2_ROOT,
                manifest,
                anchor,
            )
        except GateRefusal as exc:
            return exc


def test_w305_item3_recorded_exception_lifts_only_the_decision_134_path(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Owner decision 134 names RULE2-01-GREEN; the other changed paths stay refused."""

    # Decision 147; design v1.17 L14 / section-15.4 amendment: use synthetic post-63cfe2dd changes.
    without = w305_provenance(None, tmp_path, monkeypatch)
    assert isinstance(without, GateRefusal)
    assert without.check_id == "EXPECTED_PATH_CHANGED_AFTER_BASE"
    assert without.pointer == W305_DECISION_134_PATH

    with_record = w305_provenance(w305_exception_record(), tmp_path, monkeypatch)
    assert isinstance(with_record, GateRefusal)
    assert with_record.check_id == "EXPECTED_PATH_CHANGED_AFTER_BASE"
    assert with_record.pointer == W342C_MOVED_GIT_PATHS[0]


def test_w305_item3_wrong_current_oid_does_not_lift_the_refusal(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    record = w305_exception_record()
    wrong_current_oid = subprocess.check_output(
        ["git", "-C", str(MTC_V2_ROOT), "rev-parse", f"HEAD:{W342C_MOVED_GIT_PATHS[0]}"],
        text=True,
    ).strip()
    assert wrong_current_oid != record["exceptions"][0]["current_blob_oid"]
    record["exceptions"][0]["current_blob_oid"] = wrong_current_oid

    # Decision 147; design v1.17 L14 / section-15.4 amendment: wrong current identity cannot lift a synthetic change.
    outcome = w305_provenance(record, tmp_path, monkeypatch)

    assert isinstance(outcome, GateRefusal)
    assert outcome.check_id == "EXPECTED_PATH_CHANGED_AFTER_BASE"
    assert outcome.pointer == W305_DECISION_134_PATH


def test_w305_item3_wrong_base_state_does_not_lift_the_refusal(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    record = w305_exception_record()
    assert record["exceptions"][0]["base_state"] == "PRESENT_AT_BASE"
    record["exceptions"][0]["base_state"] = "ABSENT_AT_BASE"
    record["exceptions"][0]["base_blob_oid"] = None

    # Decision 147; design v1.17 L14 / section-15.4 amendment: wrong base state cannot lift a synthetic change.
    outcome = w305_provenance(record, tmp_path, monkeypatch)

    assert isinstance(outcome, GateRefusal)
    assert outcome.check_id == "EXPECTED_PATH_CHANGED_AFTER_BASE"
    assert outcome.pointer == W305_DECISION_134_PATH


def test_w305_item3_record_bound_to_another_base_is_invalid(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    record = w305_exception_record()
    record["implementation_base_sha"] = "a" * 40

    outcome = w305_provenance(record, tmp_path, monkeypatch)

    assert isinstance(outcome, GateRefusal)
    assert outcome.check_id == "EXPECTED_PROVENANCE_EXCEPTION_INVALID"


def test_w305_item3_unknown_member_in_the_record_is_invalid(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    record = w305_exception_record()
    record["exceptions"][0]["extra_member"] = 1

    outcome = w305_provenance(record, tmp_path, monkeypatch)

    assert isinstance(outcome, GateRefusal)
    assert outcome.check_id == "EXPECTED_PROVENANCE_EXCEPTION_INVALID"


def test_w305_item3_committed_record_states_it_is_not_evidence() -> None:
    record = w305_exception_record()

    # Decision 147; design v1.17 L14 / section-15.4 amendment: pin the re-anchored declaration values.
    assert record["declaration_kind"] == "OWNER_DECISION_DECLARATION_NOT_EVIDENCE"
    assert "not evidence" in record["statement"]
    assert record["implementation_base_sha"] == (
        # Decision 147 re-anchor forward, 2026-09-04: the base moved from the seal-16 copies commit
        # 63cfe2dd to the seal-20 copies commit bdacf8e4 after the owner-directed citation restyle
        # (decision 154) moved every expected path. This assertion's job is to pin whatever the
        # CURRENT re-anchored declaration says, and it was updated the same way when lane W350
        # re-anchored to 63cfe2dd. The owner's decision-134 authorization is untouched.
        "b0fa4fb1739f8d10fc7927aa1e7a879410fa06c7"
    )
    assert record["exceptions"][0]["owner_decision"] == 134
    assert record["exceptions"][0]["lane_ids"] == [
        "W156",
        "W167",
        "W172",
        "W316D",
        "W350",
    ]
    assert record["exceptions"][0]["base_state"] == "PRESENT_AT_BASE"
    # Decision 147 re-anchor forward, 2026-09-04. RULE2-01-GREEN's blob was 0ad42daf at the seal-16
    # copies base 63cfe2dd; at the seal-20 copies base bdacf8e4 it is d57b6151, and it is IDENTICAL
    # at HEAD - which is the property this record exists to assert. Measured with
    # `git rev-parse <base>:<path>` and `git rev-parse HEAD:<path>`, both d57b6151.
    assert record["exceptions"][0]["base_blob_oid"] == (
        "d57b6151c3d91516a780c76097d76870fd3ee8ee"
    )
    assert record["exceptions"][0]["current_blob_oid"] == (
        "d57b6151c3d91516a780c76097d76870fd3ee8ee"
    )


def test_w305_item8_provenance_refusal_reports_every_unlifted_path(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Decision 147; design v1.17 L14 / section-15.4 amendment: report every synthetic post-base path.
    outcome = w305_provenance(
        w305_exception_record(),
        tmp_path,
        monkeypatch,
        moved_paths=W342C_MOVED_MANIFEST_PATHS,
    )
    assert isinstance(outcome, GateRefusal)

    assert outcome.check_id == "EXPECTED_PATH_CHANGED_AFTER_BASE"
    assert outcome.pointers == list(W342C_MOVED_GIT_PATHS)
    assert outcome.as_dict()["pointers"] == outcome.pointers
    assert outcome.as_dict()["count"] == len(W342C_MOVED_GIT_PATHS)


def test_legacy_event_order_pin_missing_is_distinct_and_match_clears_blocker(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root, baseline_root, _mapping, digest, manifest_path, anchor_path = (
        legacy_event_order_pin_fixture(tmp_path, monkeypatch)
    )
    manifest = load_json_exact(manifest_path)
    del manifest["legacy_event_order_map_pin"]
    manifest_path.write_bytes(verify_bceg.canonical_json_bytes(manifest))

    missing = verify_bceg.run_comparison_pipeline(root, baseline_root)

    assert missing["legacy_event_order_map_pin"] == {"status": "MISSING"}
    assert missing["acceptance_blockers"] == [
        {
            "check_id": "LEGACY_EVENT_ORDER_MAP_PIN_MISSING",
            "detail": "no seal-pinned map/digest exists in the supplied bundle",
        }
    ]

    manifest["legacy_event_order_map_pin"] = {
        "legacy_event_order_map": _mapping,
        "legacy_event_order_map_sha256": digest,
    }
    manifest_path.write_bytes(verify_bceg.canonical_json_bytes(manifest))
    matched = verify_bceg.run_comparison_pipeline(root, baseline_root)
    assert matched["legacy_event_order_map_pin"] == {
        "status": "MATCH",
        "legacy_event_order_map_sha256": digest,
    }
    assert matched["acceptance_blockers"] == []

    anchor_path.write_bytes(
        verify_bceg.canonical_json_bytes(
            {"legacy_event_order_map_sha256": "f" * 64}
        )
    )
    anchor_mismatch = verify_bceg.run_comparison_pipeline(root, baseline_root)
    assert anchor_mismatch["acceptance_blockers"] == [
        {
            "check_id": "LEGACY_EVENT_ORDER_MAP_PIN_MISMATCH",
            "manifest_digest": digest,
            "anchor_digest": "f" * 64,
        }
    ]


def test_legacy_event_order_pin_digest_modified_copy_is_mismatch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root, baseline_root, _mapping, digest, manifest_path, _anchor_path = (
        legacy_event_order_pin_fixture(tmp_path, monkeypatch)
    )
    manifest = load_json_exact(manifest_path)
    modified_digest = ("1" if digest[0] != "1" else "0") + digest[1:]
    manifest["legacy_event_order_map_pin"][
        "legacy_event_order_map_sha256"
    ] = modified_digest
    manifest_path.write_bytes(verify_bceg.canonical_json_bytes(manifest))

    receipt = verify_bceg.run_comparison_pipeline(root, baseline_root)

    assert receipt["legacy_event_order_map_pin"]["status"] == "MISMATCH"
    assert receipt["acceptance_blockers"] == [
        {
            "check_id": "LEGACY_EVENT_ORDER_MAP_PIN_MISMATCH",
            "pinned_digest": modified_digest,
            "computed_digest": digest,
        }
    ]


def test_legacy_event_order_pin_map_modified_copy_names_first_key(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root, baseline_root, mapping, digest, manifest_path, _anchor_path = (
        legacy_event_order_pin_fixture(tmp_path, monkeypatch)
    )
    first_key = next(iter(mapping))
    manifest = load_json_exact(manifest_path)
    manifest["legacy_event_order_map_pin"]["legacy_event_order_map"][
        first_key
    ] = "LEGACY_SEQUENCE_FIELD_V1"
    manifest_path.write_bytes(verify_bceg.canonical_json_bytes(manifest))

    receipt = verify_bceg.run_comparison_pipeline(root, baseline_root)

    assert receipt["legacy_event_order_map_pin"]["status"] == "MISMATCH"
    assert receipt["acceptance_blockers"] == [
        {
            "check_id": "LEGACY_EVENT_ORDER_MAP_PIN_MISMATCH",
            "pinned_digest": digest,
            "computed_digest": digest,
            "first_differing_key": first_key,
        }
    ]


def test_identical_pair_compares_equal_on_every_node() -> None:
    left = load_json_exact(FIXTURES / "node_equal_left.json")
    right = load_json_exact(FIXTURES / "node_equal_right.json")
    assert compare_documents(left, right) is None


def test_one_node_difference_is_predetected_exactly() -> None:
    left = load_json_exact(FIXTURES / "node_equal_left.json")
    right = load_json_exact(FIXTURES / "node_one_diff.json")
    difference = compare_documents(left, right)
    assert difference is not None
    assert difference[0] == "/a/1"


def test_corrected_expectation_compares_only_the_two_design_surfaces() -> None:
    expected = {
        "EVENT_SURFACE": {"events": []},
        "RESULT_SURFACE": {"value": 1},
        "provenance": {"author": "tables"},
        "blocked_cells": ["authoring-only"],
    }
    observed = {
        "EVENT_SURFACE": {"events": []},
        "RESULT_SURFACE": {"value": 1},
        "provenance": {"author": "kernel"},
    }

    assert compare_scoped_expected(expected, observed) is None

    observed["RESULT_SURFACE"]["value"] = 2
    difference = compare_scoped_expected(expected, observed)
    assert difference is not None
    assert difference[0] == "/RESULT_SURFACE/value"


def test_w305_item1_extra_observed_member_at_a_nested_level_is_detected() -> None:
    """GM83B-F02: the comparator visited only expected keys, so a nested extra escaped."""

    golden = load_json_exact(
        MTC_V2_ROOT / "golden/corrected_vnext/RULE2-01-GREEN.json"
    )
    observed = deepcopy(golden)
    observed["EVENT_SURFACE"]["decision_events"][0]["undeclared_member"] = 1

    differences = verify_bceg.compare_scoped_expected_nodes(golden, observed)

    assert [difference[0] for difference in differences] == [
        "/EVENT_SURFACE/decision_events/0/undeclared_member"
    ]
    assert differences[0][1] == verify_bceg.canonical_node(1)
    assert differences[0][2] is None


def test_w305_item1_union_walk_keeps_the_section_15_3_byte_order() -> None:
    expected = {
        "EVENT_SURFACE": {"b": 1, "d": 2},
        "RESULT_SURFACE": {},
    }
    observed = {
        "EVENT_SURFACE": {"a": 0, "b": 1, "c": 0, "d": 3},
        "RESULT_SURFACE": {},
    }

    differences = verify_bceg.compare_scoped_expected_nodes(expected, observed)

    assert [difference[0] for difference in differences] == [
        "/EVENT_SURFACE/a",
        "/EVENT_SURFACE/c",
        "/EVENT_SURFACE/d",
    ]


def _conservation_root(tmp_path: Path) -> tuple[Path, list[dict[str, object]]]:
    """A minimal root carrying one observed pair and one KERNEL probe case."""

    root = tmp_path / "root"
    observed = root / "tests/corrected_vnext/observed"
    case = root / "tests/corrected_vnext/probes/PROBE-X"
    (observed / "1.0.0").mkdir(parents=True)
    (observed / "2.0.0").mkdir(parents=True)
    (case / "kernel").mkdir(parents=True)
    (observed / "1.0.0/S.json").write_bytes(EMPTY_DOCUMENT_BYTES)
    (observed / "2.0.0/S.json").write_bytes(EMPTY_DOCUMENT_BYTES)
    (case / "modification.patch").write_bytes(PATCH_BYTES)
    member = case / "kernel/economics.py"
    member.write_bytes(MEMBER_BYTES)
    tree_manifest = {
        "digest_method": "SHA256_CANONICAL_TREE_MANIFEST_V1",
        "files": [
            {
                "path": "economics.py",
                "sha256": hashlib.sha256(member.read_bytes()).hexdigest(),
            }
        ],
    }
    (case / "modified_tree_manifest.json").write_bytes(
        verify_bceg.canonical_json_bytes(tree_manifest)
    )
    (case / "modification_manifest.json").write_bytes(
        verify_bceg.canonical_json_bytes(
            {
                "modified_tree_manifest_path": (
                    "tests/corrected_vnext/probes/PROBE-X/modified_tree_manifest.json"
                ),
                "modifications": [
                    {
                        "operation": "KERNEL_FILE_PATCH",
                        "patch_path": (
                            "tests/corrected_vnext/probes/PROBE-X/modification.patch"
                        ),
                    }
                ],
            }
        )
    )
    catalog: list[dict[str, object]] = [
        {
            "scenario_id": "S",
            "role": "GREEN",
            "observed_artifact_paths": {
                "1.0.0": "tests/corrected_vnext/observed/1.0.0/S.json",
                "2.0.0": "tests/corrected_vnext/observed/2.0.0/S.json",
            },
        },
        {
            "scenario_id": "PROBE-X",
            "role": "PROBE",
            "probe_id": "PROBE-X",
            "modified_copy_path": "tests/corrected_vnext/probes/PROBE-X/kernel/",
            "modification_manifest_path": (
                "tests/corrected_vnext/probes/PROBE-X/modification_manifest.json"
            ),
        },
    ]
    return root, catalog


def test_w305_item2_conserved_roots_are_accepted(tmp_path: Path) -> None:
    root, catalog = _conservation_root(tmp_path)

    assert verify_bceg.validate_root_conservation(root, catalog) == {
        "observed_root_files": 2,
        "probe_root_files": 4,
    }


def test_w305_item2_orphan_under_observed_root_is_refused(tmp_path: Path) -> None:
    root, catalog = _conservation_root(tmp_path)
    (root / "tests/corrected_vnext/observed/leak.json").write_bytes(
        EMPTY_DOCUMENT_BYTES
    )

    with pytest.raises(GateRefusal) as caught:
        verify_bceg.validate_root_conservation(root, catalog)
    assert caught.value.check_id == "CATALOG_UNREFERENCED_FILE"
    assert caught.value.pointer == "tests/corrected_vnext/observed/leak.json"


def test_w305_item2_orphan_under_probe_root_is_refused(tmp_path: Path) -> None:
    root, catalog = _conservation_root(tmp_path)
    (root / "tests/corrected_vnext/probes/unreferenced_probe.json").write_bytes(
        EMPTY_DOCUMENT_BYTES
    )

    with pytest.raises(GateRefusal) as caught:
        verify_bceg.validate_root_conservation(root, catalog)
    assert caught.value.check_id == "CATALOG_UNREFERENCED_FILE"
    assert (
        caught.value.pointer
        == "tests/corrected_vnext/probes/unreferenced_probe.json"
    )


def test_w305_item2_twice_referenced_observed_file_is_refused(tmp_path: Path) -> None:
    root, catalog = _conservation_root(tmp_path)
    catalog[0]["observed_artifact_paths"]["2.0.0"] = (
        "tests/corrected_vnext/observed/1.0.0/S.json"
    )

    with pytest.raises(GateRefusal) as caught:
        verify_bceg.validate_root_conservation(root, catalog)
    assert caught.value.check_id == "CATALOG_DOUBLE_REFERENCE"
    assert caught.value.pointer == "tests/corrected_vnext/observed/1.0.0/S.json"


def test_w305_item2_patch_file_named_as_a_variant_member_is_refused(
    tmp_path: Path,
) -> None:
    root, catalog = _conservation_root(tmp_path)
    case = root / "tests/corrected_vnext/probes/PROBE-X"
    manifest = load_json_exact(case / "modification_manifest.json")
    manifest["modifications"][0]["patch_path"] = (
        "tests/corrected_vnext/probes/PROBE-X/kernel/economics.py"
    )
    (case / "modification_manifest.json").write_bytes(
        verify_bceg.canonical_json_bytes(manifest)
    )

    with pytest.raises(GateRefusal) as caught:
        verify_bceg.validate_root_conservation(root, catalog)
    assert caught.value.check_id == "CATALOG_DOUBLE_REFERENCE"


def test_w305_item2_real_catalog_conserves_both_roots() -> None:
    catalog = load_json_exact(
        MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json"
    )

    counts = verify_bceg.validate_root_conservation(MTC_V2_ROOT, catalog)

    assert counts["observed_root_files"] == 34
    assert counts["probe_root_files"] == 1103


def test_comparison_pipeline_measures_executed_output_once_per_row(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    scenario_id = "RULE2-05-RED"
    root = tmp_path / "root"
    baseline_root = tmp_path / "baseline"
    input_path = root / "inputs" / f"{scenario_id}.json"
    golden_path = root / "golden" / f"{scenario_id}.json"
    baseline_path = baseline_root / "out" / scenario_id / "result_surface.json"
    for path in (input_path, golden_path, baseline_path):
        path.parent.mkdir(parents=True, exist_ok=True)
    contracts = root / "tests" / "corrected_vnext" / "contracts"
    contracts.mkdir(parents=True)
    (contracts / "CONTRACT_TABLES_MANIFEST.json").write_bytes(
        verify_bceg.canonical_json_bytes(
            {
                "legacy_event_order_map_pin": {
                    "legacy_event_order_map": {},
                    "legacy_event_order_map_sha256": "0" * 64,
                }
            }
        )
    )
    (contracts / "implementation_anchor.json").write_bytes(
        verify_bceg.canonical_json_bytes(
            {"legacy_event_order_map_sha256": "0" * 64}
        )
    )

    golden = {
        "EVENT_SURFACE": {
            "fill_events": [
                {
                    "reference_price": 100,
                    "slippage_impact": 1,
                    "final_fill_price": 101,
                    "slippage_application_count": 1,
                }
            ]
        },
        "RESULT_SURFACE": {"final_position": {"quantity": 1}},
    }
    input_path.write_bytes(verify_bceg.canonical_json_bytes({}))
    golden_path.write_bytes(verify_bceg.canonical_json_bytes(golden))
    baseline_path.write_bytes(
        verify_bceg.canonical_json_bytes(
            {"events": [{"price": 100}], "position": {}}
        )
    )
    observed_root = root / "tests" / "corrected_vnext" / "observed"
    legacy_observed_path = observed_root / "1.0.0" / f"{scenario_id}.json"
    corrected_observed_path = observed_root / "2.0.0" / f"{scenario_id}.json"
    legacy_observed_path.parent.mkdir(parents=True, exist_ok=True)
    corrected_observed_path.parent.mkdir(parents=True, exist_ok=True)
    legacy_observed_document = {
        "EVENT_SURFACE": [],
        "RESULT_SURFACE": load_json_exact(baseline_path),
    }
    corrected_observed_document = deepcopy(golden)
    corrected_observed_document["RESULT_SURFACE"]["final_position"]["quantity"] = 2
    legacy_observed_path.write_bytes(
        verify_bceg.canonical_json_bytes(legacy_observed_document)
    )
    corrected_observed_path.write_bytes(
        verify_bceg.canonical_json_bytes(corrected_observed_document)
    )
    row = {
        "scenario_id": scenario_id,
        "role": "RED",
        "input": {"path": input_path.relative_to(root).as_posix()},
        "expected_artifacts": {
            "2.0.0": {"path": golden_path.relative_to(root).as_posix()}
        },
        "observed_artifact_paths": {
            "1.0.0": legacy_observed_path.relative_to(root).as_posix(),
            "2.0.0": corrected_observed_path.relative_to(root).as_posix(),
        },
    }
    corpus = verify_bceg.Corpus(
        root=root,
        baseline_root=baseline_root,
        catalog=[row],
        blockers=(),
        identities={},
    )
    monkeypatch.setattr(
        verify_bceg, "validate_catalog", lambda _root, _baseline_root: corpus
    )
    monkeypatch.setattr(
        verify_bceg,
        "compute_legacy_event_order_map",
        lambda _corpus: ({}, "0" * 64),
    )
    monkeypatch.setattr(
        verify_bceg,
        "_load_legacy_executor",
        lambda _root, _baseline_root: (object(), {}),
    )
    monkeypatch.setattr(
        verify_bceg,
        "_legacy_observed_document",
        lambda *_args, **_kwargs: {
            "EVENT_SURFACE": [],
            "RESULT_SURFACE": load_json_exact(baseline_path),
        },
    )
    monkeypatch.setattr(
        verify_bceg,
        "_compare_legacy_reproduction",
        lambda *_args, **_kwargs: (
            {
                "producer_id": "KERNEL_1",
                "status": "MATCH",
                "surfaces": [
                    {"surface_id": "EVENT_SURFACE", "status": "MATCH"},
                    {"surface_id": "RESULT_SURFACE", "status": "MATCH"},
                ],
            },
            None,
        ),
    )
    executed: list[str] = []

    def execute_modified_copy(
        _root: Path, candidate: dict[str, object]
    ) -> dict[str, object]:
        executed.append(str(candidate["scenario_id"]))
        observed = deepcopy(golden)
        observed["RESULT_SURFACE"]["final_position"]["quantity"] = 2
        return observed

    monkeypatch.setattr(
        verify_bceg, "execute_corrected_scenario", execute_modified_copy
    )

    receipt = verify_bceg.run_comparison_pipeline(root, baseline_root)

    assert executed == [scenario_id]
    assert receipt["scenarios"][0]["corrected_expectation"] == "STOP_MISMATCH"
    assert (
        receipt["scenarios"][0]["first_corrected_mismatch"]
        == "/RESULT_SURFACE/final_position/quantity"
    )
    assert any(
        blocker.get("check_id") == "CORRECTED_EXPECTATION_MISMATCH"
        and blocker.get("scenario_id") == scenario_id
        and blocker.get("pointer") == "/RESULT_SURFACE/final_position/quantity"
        for blocker in receipt["acceptance_blockers"]
    )
    assert receipt["observed_artifact_pins"]["count"] == 2
    assert receipt["observed_artifact_pins"]["stale_count"] == 0
    assert all(
        pin["committed_sha256"] == pin["live_run_sha256"]
        for pin in receipt["observed_artifact_pins"]["pins"]
    )


def _observed_pin_root(tmp_path: Path) -> tuple[Path, dict[str, object], dict, dict]:
    root = tmp_path / "root"
    observed = root / "tests/corrected_vnext/observed"
    (observed / "1.0.0").mkdir(parents=True)
    (observed / "2.0.0").mkdir(parents=True)
    legacy_document = {"EVENT_SURFACE": [], "RESULT_SURFACE": {"account": {}}}
    corrected_document = {"EVENT_SURFACE": {}, "RESULT_SURFACE": {"quantity": 1}}
    (observed / "1.0.0/S.json").write_bytes(
        verify_bceg.canonical_json_bytes(legacy_document)
    )
    (observed / "2.0.0/S.json").write_bytes(
        verify_bceg.canonical_json_bytes(corrected_document)
    )
    row = {
        "scenario_id": "S",
        "observed_artifact_paths": {
            "1.0.0": "tests/corrected_vnext/observed/1.0.0/S.json",
            "2.0.0": "tests/corrected_vnext/observed/2.0.0/S.json",
        },
    }
    return root, row, legacy_document, corrected_document


def test_w305_item4_fresh_observed_copies_pin_and_do_not_refuse(
    tmp_path: Path,
) -> None:
    root, row, legacy_document, corrected_document = _observed_pin_root(tmp_path)
    blockers: list[dict[str, object]] = []

    pins = verify_bceg.pin_observed_artifacts(
        root, row, legacy_document, corrected_document, blockers
    )

    assert blockers == []
    assert [pin["semantics_version"] for pin in pins] == ["1.0.0", "2.0.0"]
    assert [pin["producer_id"] for pin in pins] == ["KERNEL_1", "KERNEL_2"]
    assert all(
        pin["committed_sha256"] == pin["live_run_sha256"] for pin in pins
    )


def test_w305_item4_stale_committed_observed_artifact_is_refused(
    tmp_path: Path,
) -> None:
    """W279B-F03: the committed OBSERVED_ROOT copies were never measured."""

    root, row, legacy_document, corrected_document = _observed_pin_root(tmp_path)
    stale = deepcopy(corrected_document)
    stale["RESULT_SURFACE"]["quantity"] = 2
    (root / "tests/corrected_vnext/observed/2.0.0/S.json").write_bytes(
        verify_bceg.canonical_json_bytes(stale)
    )
    blockers: list[dict[str, object]] = []

    pins = verify_bceg.pin_observed_artifacts(
        root, row, legacy_document, corrected_document, blockers
    )

    assert [blocker["check_id"] for blocker in blockers] == [
        "OBSERVED_ARTIFACT_STALE"
    ]
    assert blockers[0]["pointer"] == "tests/corrected_vnext/observed/2.0.0/S.json"
    assert pins[1]["committed_sha256"] != pins[1]["live_run_sha256"]
    assert pins[1]["live_run_sha256"] == hashlib.sha256(
        verify_bceg.canonical_json_bytes(corrected_document)
    ).hexdigest()


def test_w305_item4_missing_committed_observed_artifact_is_refused(
    tmp_path: Path,
) -> None:
    root, row, legacy_document, corrected_document = _observed_pin_root(tmp_path)
    (root / "tests/corrected_vnext/observed/1.0.0/S.json").unlink()
    blockers: list[dict[str, object]] = []

    pins = verify_bceg.pin_observed_artifacts(
        root, row, legacy_document, corrected_document, blockers
    )

    assert [blocker["check_id"] for blocker in blockers] == [
        "OBSERVED_ARTIFACT_STALE"
    ]
    assert pins[0]["committed_sha256"] is None


def test_legacy_reproduction_refuses_one_ulp_actual(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = verify_bceg._legacy_observed_document

    def one_ulp_actual(*args, **kwargs):
        observed = original(*args, **kwargs)
        if observed["scenario_id"] == "RULE2-01-RED":
            equity = float.fromhex(observed["RESULT_SURFACE"]["account"]["equity"])
            observed["RESULT_SURFACE"]["account"]["equity"] = math.nextafter(
                equity, math.inf
            ).hex()
        return observed

    monkeypatch.setattr(verify_bceg, "_legacy_observed_document", one_ulp_actual)
    monkeypatch.setattr(
        verify_bceg,
        "run_probe_suite",
        lambda _corpus: {"probes": [], "probe_blockers": []},
    )

    receipt = verify_bceg.run_comparison_pipeline(MTC_V2_ROOT, BASELINE_ROOT)

    assert receipt["acceptance_blockers"][0] == {
        "check_id": "LEGACY_REPRODUCTION_MISMATCH",
        "scenario_id": "RULE2-01-RED",
        "pointer": "/RESULT_SURFACE/account/equity",
    }


def test_receipt_accounts_for_every_blocked_expected_node(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        verify_bceg,
        "run_probe_suite",
        lambda _corpus: {"probes": [], "probe_blockers": []},
    )

    receipt = verify_bceg.run_comparison_pipeline(MTC_V2_ROOT, BASELINE_ROOT)

    accounting = receipt["blocked_node_skips"]
    assert accounting["count"] == len(accounting["nodes"])
    assert accounting["count"] > 0
    assert {
        "scenario_id": "RULE2-01-RED",
        "pointer": "/RESULT_SURFACE/metrics",
        "expected_marker": "BLOCKED-DESIGN-UNENUMERATED",
    } in accounting["nodes"]
    assert all(
        set(node) == {"scenario_id", "pointer", "expected_marker"}
        for node in accounting["nodes"]
    )
    assert receipt["comparison_claim_scope"] == "ALL_NON_BLOCKED_EXPECTED_NODES"
    assert (
        verify_bceg.ACCEPTING_LABEL
        == "BOUNDED_NON_BLOCKED_CORRECTION_EVIDENCE_ACCEPTED"
    )


def _w356_probe_and_base_rows(
    probe_id: str,
) -> tuple[dict[str, object], dict[str, object]]:
    catalog = load_json_exact(
        MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json"
    )
    probe = next(row for row in catalog if row.get("probe_id") == probe_id)
    base = next(
        row
        for row in catalog
        if row.get("scenario_id") == probe["base_scenario_id"]
        and row.get("role") in {"RED", "GREEN"}
    )
    return probe, base


def test_w356_agreeing_probe_manifest_and_catalog_are_accepted() -> None:
    probe, base = _w356_probe_and_base_rows("PROBE-P012-01-A")

    artifact = verify_bceg._validate_probe_artifact(MTC_V2_ROOT, probe, base)

    assert artifact["pinned"] is True


def test_w356_probe_manifest_catalog_disagreement_is_refused() -> None:
    probe, base = _w356_probe_and_base_rows("PROBE-P012-01-A")
    disagreeing_probe = deepcopy(probe)
    disagreeing_probe["expected_first_changed_node"] = "/synthetic/disagreement"

    with pytest.raises(GateRefusal) as caught:
        verify_bceg._validate_probe_artifact(
            MTC_V2_ROOT, disagreeing_probe, base
        )

    assert (
        caught.value.check_id
        == "PROBE_MODIFICATION_MANIFEST_CATALOG_MISMATCH"
    )


def test_w356_all_real_probe_manifests_agree_with_catalog() -> None:
    catalog = load_json_exact(
        MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json"
    )
    probes = sorted(
        (row for row in catalog if row.get("role") == "PROBE"),
        key=lambda row: row["probe_id"],
    )
    assert len(probes) == 10

    for probe in probes:
        manifest_path = MTC_V2_ROOT / probe["modification_manifest_path"]
        manifest = load_json_exact(manifest_path)
        assert probe["modification_manifest_digest"] == hashlib.sha256(
            manifest_path.read_bytes()
        ).hexdigest()
        assert (
            manifest["expected_first_changed_node"]
            == probe["expected_first_changed_node"]
        )
        base = next(
            row
            for row in catalog
            if row.get("scenario_id") == probe["base_scenario_id"]
            and row.get("role") in {"RED", "GREEN"}
        )
        artifact = verify_bceg._validate_probe_artifact(
            MTC_V2_ROOT, probe, base
        )

        assert artifact["pinned"] is True


def test_probe_driver_refuses_unclosed_base_before_variant_comparison(
    tmp_path: Path,
) -> None:
    catalog = load_json_exact(
        MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json"
    )
    probe = next(
        row for row in catalog if row.get("probe_id") == "PROBE-P012-02-A"
    )
    base_row = next(
        row
        for row in catalog
        if row.get("scenario_id") == probe["base_scenario_id"]
        and row.get("role") in {"RED", "GREEN"}
    )
    expected = load_json_exact(
        MTC_V2_ROOT / base_row["expected_artifacts"]["2.0.0"]["path"]
    )
    refused_row = next(
        row
        for row in catalog
        if row.get("scenario_id") == "RULE2-02-RED" and row.get("role") == "RED"
    )
    refused_admission = load_json_exact(
        MTC_V2_ROOT / refused_row["expected_artifacts"]["2.0.0"]["path"]
    )
    assert "admitted" not in refused_admission["RESULT_SURFACE"]

    # Design v1.17 sections 23.4/23.5 (:1425, :1537-1539): admitted exists only
    # when the DEF-P012-02 minimum-notional predicate terminates in admission.
    verify_bceg.validate_corrected_closed_sets(
        base_row,
        {
            "EVENT_SURFACE": refused_admission["EVENT_SURFACE"],
            "RESULT_SURFACE": refused_admission["RESULT_SURFACE"],
        },
    )
    differences = verify_bceg.compare_scoped_expected_nodes(
        expected, refused_admission
    )
    assert "/RESULT_SURFACE/admitted" in {
        pointer for pointer, _observed, _expected in differences
    }

    unmodified = tmp_path / "kernel"
    shutil.copytree(
        MTC_V2_ROOT / "core",
        unmodified,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    unmodified_manifest, _ = verify_bceg.canonical_tree_manifest(unmodified)

    identity_receipt = verify_bceg.drive_probe_variant_process(
        MTC_V2_ROOT,
        tmp_path / "unused-baseline",
        probe,
        unmodified,
        unmodified_manifest,
    )

    assert identity_receipt["status"] == "NOT_DETECTED"
    assert identity_receipt["measured_failed_check"] is None
    assert identity_receipt["comparator_first_differing_node"] is None
    assert identity_receipt["expected_node_changed"] is False

    modified = MTC_V2_ROOT / probe["modified_copy_path"]
    modified_manifest = load_json_exact(
        MTC_V2_ROOT
        / "tests/corrected_vnext/probes/PROBE-P012-02-A/modified_tree_manifest.json"
    )
    modified_receipt = verify_bceg.drive_probe_variant_process(
        MTC_V2_ROOT,
        tmp_path / "unused-baseline",
        probe,
        modified,
        modified_manifest,
    )

    # Owner decision 143; design v1.17 :273-303 re-targets this probe to the
    # corrected-expectation comparator and keeps admitted in the changed set.
    assert modified_receipt["status"] == "DETECTED"
    assert modified_receipt["measured_failed_check"] == "CORRECTED_EXPECTATION"
    assert (
        modified_receipt["comparator_first_differing_node"]
        == "/EVENT_SURFACE/cash_events"
    )
    assert modified_receipt["expected_node_changed"] is True


def test_probe_cannot_claim_target_membership_when_base_is_refused(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    catalog = load_json_exact(
        MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json"
    )
    probe = next(
        row for row in catalog if row.get("probe_id") == "PROBE-P012-08-A"
    )
    expected_node = "/EVENT_SURFACE/funding_events/0/funding_cash_delta"
    # Owner decision 144; design P012_FRESH_DESIGN_V1.md:558-560 binds index-ascending comparator order; re-aligned to the W341B catalog value (W342B).
    comparator_first_node = "/EVENT_SURFACE/cash_events/0/signed_delta"
    assert probe["expected_first_changed_node"] == expected_node
    assert probe["comparator_first_differing_node"] == comparator_first_node
    assert expected_node != comparator_first_node

    modified = MTC_V2_ROOT / probe["modified_copy_path"]
    modified_manifest = load_json_exact(
        MTC_V2_ROOT
        / "tests/corrected_vnext/probes/PROBE-P012-08-A/modified_tree_manifest.json"
    )
    child = {
        "mode": "probe-child",
        "probe_id": probe["probe_id"],
        "claim_label": "PROBE_BASE_SCENARIO_REFUSED",
        "failed_check": probe["expected_failed_check"],
        "changed_nodes": [comparator_first_node],
        "comparator_first_differing_node": comparator_first_node,
    }
    completed = subprocess.CompletedProcess(
        args=[], returncode=2, stdout=json.dumps(child), stderr=""
    )
    # Decision 147; design v1.17 L14 / section-15.4 amendment: a synthetic base refusal omits the target node.
    with monkeypatch.context() as synthetic:
        synthetic.setattr(verify_bceg.subprocess, "run", lambda *args, **kwargs: completed)
        receipt = verify_bceg.drive_probe_variant_process(
            MTC_V2_ROOT,
            tmp_path / "unused-baseline",
            probe,
            modified,
            modified_manifest,
        )

    assert receipt["status"] == "NOT_DETECTED"
    assert receipt["measured_failed_check"] == "CORRECTED_EXPECTATION"
    assert receipt["expected_first_changed_node"] == expected_node
    assert receipt["comparator_first_differing_node"] == comparator_first_node
    assert receipt["expected_node_changed"] is False
    assert receipt["measured_matches_expected"] is False


@pytest.mark.parametrize(
    ("fixture", "check_id"),
    [("duplicate_key.json", "JSON_DUPLICATE_KEY"), ("nonfinite.json", "JSON_NON_FINITE")],
)
def test_strict_json_refusals(fixture: str, check_id: str) -> None:
    refusal(check_id, lambda: load_json_exact(FIXTURES / fixture))


def test_version_shaped_surface_refusals() -> None:
    padded = load_json_exact(FIXTURES / "padded_legacy.json")
    refusal("LEGACY_SCHEMA_PADDED", lambda: validate_legacy_unpadded(padded))
    sequenced = load_json_exact(FIXTURES / "wrong_sequence.json")
    refusal("CORRECTED_SEQUENCE_INVALID", lambda: validate_corrected_event_surface(sequenced))


@pytest.mark.parametrize(
    ("fixture", "check_id"),
    [
        ("input_unknown_top.json", "INPUT_UNKNOWN_TOP_LEVEL_MEMBER"),
        ("input_missing_corrected_only.json", "INPUT_MISSING_TOP_LEVEL_MEMBER"),
        ("input_corrected_in_legacy.json", "INPUT_CORRECTED_ONLY_IN_LEGACY_ARM"),
        ("input_f64_wrong_case.json", "INPUT_F64BITS_INVALID"),
        ("input_f64_short.json", "INPUT_F64BITS_INVALID"),
        ("input_f64_nonquiet.json", "INPUT_F64BITS_INVALID"),
        ("input_f64_infinity.json", "INPUT_F64BITS_INVALID"),
        ("input_f64_outside.json", "INPUT_F64BITS_OUTSIDE_SELECTOR"),
    ],
)
def test_section_22_input_refusals(fixture: str, check_id: str) -> None:
    document = load_json_exact(FIXTURES / fixture)
    refusal(check_id, lambda: validate_input_envelope(document))


def test_input_digest_mismatch_refusal() -> None:
    path = FIXTURES / "input_valid.json"
    document = load_json_exact(path)
    wrong_digest = "0" * 64
    assert hashlib.sha256(path.read_bytes()).hexdigest() != wrong_digest
    refusal(
        "INPUT_DIGEST_MISMATCH",
        lambda: validate_input_envelope(document, path=path, expected_digest=wrong_digest),
    )


def test_valid_section_22_input() -> None:
    path = FIXTURES / "input_valid.json"
    document = load_json_exact(path)
    validate_input_envelope(
        document,
        path=path,
        expected_digest=hashlib.sha256(path.read_bytes()).hexdigest(),
    )


def test_section_22_nan_decoder_preserves_the_exact_quiet_nan_bits() -> None:
    document = load_json_exact(FIXTURES / "input_valid.json")

    value = decode_stop_price_f64(document, scenario_id="RULE2-01-GREEN")

    assert value is not None
    assert value != value


def test_record_reference_digest_mismatch_refuses_before_execution() -> None:
    document = load_json_exact(FIXTURES / "input_record_digest_mismatch.json")

    refusal(
        "RECORD_DIGEST_MISMATCH",
        lambda: resolve_record_references(
            MTC_V2_ROOT, document["corrected_only"]["records"]
        ),
    )


def test_corrected_scenario_executes_real_seam_and_emits_six_containers() -> None:
    catalog = load_json_exact(MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json")
    row = next(member for member in catalog if member["scenario_id"] == "RULE2-01-RED")

    observed = execute_corrected_scenario(MTC_V2_ROOT, row)

    assert observed["producer_id"] == "KERNEL_2"
    assert observed["semantics_version"] == "2.0.0"
    assert list(observed["EVENT_SURFACE"]) == [
        "decision_events",
        "fill_events",
        "cash_events",
        "fee_events",
        "funding_events",
        "exit_events",
    ]
    assert observed["RESULT_SURFACE"]["run_manifest"]["kernel_semantics_version"] == "2.0.0"


def test_corrected_closed_set_refuses_observed_only_member(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    catalog = load_json_exact(
        MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json"
    )
    row = next(member for member in catalog if member["scenario_id"] == "RULE2-01-RED")
    original = verify_bceg.corrected_surfaces

    def with_observed_only_member(**kwargs):
        surfaces = original(**kwargs)
        surfaces["EVENT_SURFACE"]["fill_events"][0]["observed_only"] = True
        return surfaces

    monkeypatch.setattr(
        verify_bceg, "corrected_surfaces", with_observed_only_member
    )

    observed = execute_corrected_scenario(MTC_V2_ROOT, row)
    with pytest.raises(GateRefusal) as caught:
        verify_bceg.validate_corrected_closed_sets(
            row,
            {
                "EVENT_SURFACE": observed["EVENT_SURFACE"],
                "RESULT_SURFACE": observed["RESULT_SURFACE"],
            },
        )
    assert caught.value.check_id == "CLOSED_SET_VIOLATION"
    assert caught.value.pointer == "/EVENT_SURFACE/fill_events/0/observed_only"


def test_corrected_closed_set_refuses_missing_member(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    catalog = load_json_exact(
        MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json"
    )
    row = next(member for member in catalog if member["scenario_id"] == "RULE2-03-GREEN")
    original = verify_bceg.corrected_surfaces

    def without_required_member(**kwargs):
        surfaces = original(**kwargs)
        del surfaces["RESULT_SURFACE"]["warnings"]
        return surfaces

    monkeypatch.setattr(verify_bceg, "corrected_surfaces", without_required_member)

    observed = execute_corrected_scenario(MTC_V2_ROOT, row)
    with pytest.raises(GateRefusal) as caught:
        verify_bceg.validate_corrected_closed_sets(
            row,
            {
                "EVENT_SURFACE": observed["EVENT_SURFACE"],
                "RESULT_SURFACE": observed["RESULT_SURFACE"],
            },
        )
    assert caught.value.check_id == "CLOSED_SET_VIOLATION"
    assert caught.value.pointer == "/RESULT_SURFACE/warnings"


def test_w305_item7_closed_sets_ignore_scenario_identity() -> None:
    catalog = load_json_exact(
        MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json"
    )
    row = next(member for member in catalog if member["scenario_id"] == "RULE2-02-GREEN")
    observed = execute_corrected_scenario(MTC_V2_ROOT, row)
    renamed_row = deepcopy(row)
    renamed_row["scenario_id"] = "RENAMED-SAME-DECLARATION"

    verify_bceg.validate_corrected_closed_sets(
        renamed_row,
        {
            "EVENT_SURFACE": observed["EVENT_SURFACE"],
            "RESULT_SURFACE": observed["RESULT_SURFACE"],
        },
    )


@pytest.mark.parametrize(
    "scenario_id", ["RULE2-01-RED", "RULE2-03-RED", "RULE2-07-RED"]
)
def test_observed_projection_passes_no_authoring_or_membership_overrides(
    scenario_id: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    catalog = load_json_exact(
        MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json"
    )
    row = next(member for member in catalog if member["scenario_id"] == scenario_id)
    original = verify_bceg.corrected_surfaces
    calls: list[set[str]] = []

    def capture_projection(**kwargs):
        calls.append(set(kwargs))
        return original(**kwargs)

    monkeypatch.setattr(verify_bceg, "corrected_surfaces", capture_projection)
    monkeypatch.setattr(
        verify_bceg, "validate_corrected_closed_sets", lambda *_args: None
    )

    execute_corrected_scenario(MTC_V2_ROOT, row)

    assert len(calls) == 1
    assert "declared_def_ids" in calls[0]
    assert ("computed_guard_snapshot" in calls[0]) is (scenario_id == "RULE2-07-RED")
    assert calls[0].isdisjoint(
        {
            "refusals",
            "guards",
            "include_order_notional",
            "admitted",
            "include_cumulative_funding",
        }
    )


@pytest.mark.parametrize("scenario_id", ["RULE2-04-RED", "RULE2-06-GREEN"])
def test_w304_row4_serializes_the_protective_stop_reason(
    scenario_id: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    catalog = load_json_exact(
        MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json"
    )
    row = next(member for member in catalog if member["scenario_id"] == scenario_id)
    monkeypatch.setattr(
        verify_bceg, "validate_corrected_closed_sets", lambda *_args: None
    )

    observed = execute_corrected_scenario(MTC_V2_ROOT, row)

    assert observed["EVENT_SURFACE"]["exit_events"][0]["reason"] == "PROTECTIVE_STOP"


def test_w304_row5_serializes_the_bound_time_stop_reason() -> None:
    catalog = load_json_exact(
        MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json"
    )
    row = next(member for member in catalog if member["scenario_id"] == "RULE2-07-RED")

    observed = execute_corrected_scenario(MTC_V2_ROOT, row)

    assert observed["EVENT_SURFACE"]["exit_events"][0]["exit_id"] == "TIME_STOP"
    assert observed["EVENT_SURFACE"]["exit_events"][0]["reason"] == "time_stop"


@pytest.mark.parametrize(
    "scenario_id",
    ["RULE2-06-RED", "RULE2-06-GREEN"],
)
def test_w304_row6_manifest_passes_the_runners_actual_collision_policy(
    scenario_id: str,
) -> None:
    catalog = load_json_exact(
        MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json"
    )
    row = next(member for member in catalog if member["scenario_id"] == scenario_id)

    result = execute_corrected_scenario(MTC_V2_ROOT, row)["RESULT_SURFACE"]

    assert result["run_manifest"]["same_bar_collision_policy_id"] == "TARGET_FIRST"


def test_observed_path_has_no_legacy_state_seed_or_literal_surface_builder() -> None:
    assert not hasattr(verify_bceg, "_prepare_rule2_08_observation")
    assert not hasattr(verify_bceg, "_refusal_surfaces")
    assert not hasattr(verify_bceg, "_normalize_exit_surface")


@pytest.mark.parametrize(
    ("scenario_id", "expected_decisions"),
    [
        ("RULE2-01-RED", ["SEMANTICS_VALIDATED", "SIZING_COMPUTED", "MIN_NOTIONAL_ADMITTED"]),
        ("RULE2-01-GREEN", ["SEMANTICS_VALIDATED", "SIZING_COMPUTED", "MIN_NOTIONAL_ADMITTED"]),
        ("RULE2-02-RED", ["SEMANTICS_VALIDATED", "SIZING_COMPUTED", "REFUSED_MIN_NOTIONAL"]),
        ("RULE2-02-GREEN", ["SEMANTICS_VALIDATED", "SIZING_COMPUTED", "MIN_NOTIONAL_ADMITTED"]),
        ("RULE2-03-RED", ["SEMANTICS_VALIDATED", "REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION"]),
        ("RULE2-03-GREEN", ["SEMANTICS_VALIDATED", "INSTRUMENT_RECORD_VALIDATED"]),
        ("RULE2-04-RED", ["SEMANTICS_VALIDATED", "PROTECTIVE_STOP_EVALUATED"]),
        ("RULE2-04-GREEN", ["SEMANTICS_VALIDATED", "PROTECTIVE_STOP_EVALUATED"]),
        ("RULE2-05-RED", ["SEMANTICS_VALIDATED", "SIZING_COMPUTED", "MIN_NOTIONAL_ADMITTED"]),
        ("RULE2-05-GREEN", ["SEMANTICS_VALIDATED", "SIZING_COMPUTED", "MIN_NOTIONAL_ADMITTED"]),
        ("RULE2-06-RED", ["SEMANTICS_VALIDATED", "PROTECTIVE_STOP_EVALUATED", "COLLISION_RESOLVED"]),
        ("RULE2-06-GREEN", ["SEMANTICS_VALIDATED", "PROTECTIVE_STOP_EVALUATED", "COLLISION_RESOLVED"]),
        ("RULE2-07-RED", ["SEMANTICS_VALIDATED", "SIZING_COMPUTED", "MIN_NOTIONAL_ADMITTED"]),
        ("RULE2-07-GREEN", ["SEMANTICS_VALIDATED"]),
        # Owner decisions 136/137/144; design P012_FRESH_DESIGN_V1.md:1278 binds this RED reason.
        ("RULE2-08-RED", ["SEMANTICS_VALIDATED", "FUNDING_ELIGIBILITY"]),
        # Owner decisions 136/137/144; design P012_FRESH_DESIGN_V1.md:1278 binds this GREEN reason.
        ("RULE2-08-GREEN", ["SEMANTICS_VALIDATED", "FUNDING_ELIGIBILITY"]),
    ],
)
def test_raw_kernel_decision_trail_contains_each_evaluated_closed_reason(
    scenario_id: str, expected_decisions: list[str]
) -> None:
    catalog = load_json_exact(MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json")
    row = next(member for member in catalog if member["scenario_id"] == scenario_id)

    decisions = execute_corrected_scenario(MTC_V2_ROOT, row)["EVENT_SURFACE"]["decision_events"]

    assert [member["decision"] for member in decisions] == expected_decisions
    assert [member["sequence"] for member in decisions] == list(range(len(decisions)))
    assert all(member["kernel_semantics_version"] == "2.0.0" for member in decisions)
    assert all("details" not in member for member in decisions)
    assert all("lifecycle_id" not in member for member in decisions)
    assert all("refusal_code" not in member for member in decisions)
    assert "event_timestamp" not in decisions[0]


@pytest.mark.parametrize(
    "scenario_id",
    [
        "RULE2-01-RED",
        "RULE2-01-GREEN",
        "RULE2-02-RED",
        "RULE2-02-GREEN",
        "RULE2-03-RED",
        "RULE2-03-GREEN",
        "RULE2-04-RED",
        "RULE2-04-GREEN",
        "RULE2-05-RED",
        "RULE2-05-GREEN",
        "RULE2-06-RED",
        "RULE2-06-GREEN",
        "RULE2-07-RED",
        "RULE2-07-GREEN",
        "RULE2-08-RED",
        "RULE2-08-GREEN",
    ],
)
def test_section_23_every_emitted_event_carries_kernel_identity(
    scenario_id: str,
) -> None:
    catalog = load_json_exact(MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json")
    row = next(member for member in catalog if member["scenario_id"] == scenario_id)

    event_surface = execute_corrected_scenario(MTC_V2_ROOT, row)["EVENT_SURFACE"]

    assert all(
        member["kernel_semantics_version"] == "2.0.0"
        for events in event_surface.values()
        for member in events
    )


@pytest.mark.parametrize(
    ("scenario_id", "expected_equity_curve"),
    [
        ("RULE2-04-RED", {"first": 999.955, "last": 989.9145}),
        ("RULE2-04-GREEN", {"first": 999.955, "last": 999.955}),
        ("RULE2-06-RED", {"first": 999.91, "last": 1014.81325}),
        ("RULE2-06-GREEN", {"first": 999.91, "last": 979.829}),
    ],
)
def test_section_23_equity_endpoints_are_window_scoped_realized_equity(
    scenario_id: str, expected_equity_curve: dict[str, float]
) -> None:
    catalog = load_json_exact(MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json")
    row = next(member for member in catalog if member["scenario_id"] == scenario_id)

    equity_curve = execute_corrected_scenario(MTC_V2_ROOT, row)["RESULT_SURFACE"][
        "equity_curve"
    ]

    assert equity_curve == pytest.approx(expected_equity_curve)


@pytest.mark.parametrize(
    "scenario_id",
    [
        "RULE2-04-RED",
        "RULE2-04-GREEN",
        "RULE2-06-RED",
        "RULE2-06-GREEN",
    ],
)
def test_section_23_fill_and_exit_conditionals_are_closed(
    scenario_id: str,
) -> None:
    catalog = load_json_exact(MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json")
    row = next(member for member in catalog if member["scenario_id"] == scenario_id)
    events = execute_corrected_scenario(MTC_V2_ROOT, row)["EVENT_SURFACE"]
    common_fill = {
        "sequence",
        "kernel_semantics_version",
        "fill_id",
        "event_class",
        "side",
        "reference_price",
        "slippage_model_id",
        "slippage_bps",
        "slippage_impact",
        "slippage_application_count",
        "price_tick_alignment",
        "final_fill_price",
        "quantity",
        "liquidity_role",
    }
    common_exit = {
        "sequence",
        "kernel_semantics_version",
        "exit_id",
        "reason",
        "fill_id",
        "quantity",
        "final_fill_price",
        "gross_realized_pnl",
    }
    fill_by_id = {member["fill_id"]: member for member in events["fill_events"]}

    for fill in events["fill_events"]:
        expected = set(common_fill)
        if fill["event_class"].endswith("EXIT"):
            expected.add("exit_id")
        if fill["event_class"] == "PROTECTIVE_STOP_EXIT":
            expected.add("fill_trigger")
        if fill["event_class"] == "TARGET_EXIT":
            expected.update({"target_fraction", "reference_quantity"})
        assert set(fill) == expected
    for exit_event in events["exit_events"]:
        expected = set(common_exit)
        if fill_by_id[exit_event["fill_id"]]["event_class"] == "PROTECTIVE_STOP_EXIT":
            expected.add("fill_trigger")
        assert set(exit_event) == expected


@pytest.mark.parametrize(
    "scenario_id",
    [
        "RULE2-01-RED",
        "RULE2-01-GREEN",
        "RULE2-02-RED",
        "RULE2-02-GREEN",
        "RULE2-03-RED",
        "RULE2-03-GREEN",
        "RULE2-04-RED",
        "RULE2-04-GREEN",
        "RULE2-05-RED",
        "RULE2-05-GREEN",
        "RULE2-06-RED",
        "RULE2-06-GREEN",
        "RULE2-07-RED",
        "RULE2-07-GREEN",
        "RULE2-08-RED",
        "RULE2-08-GREEN",
    ],
)
def test_raw_kernel_result_membership_follows_declared_contract(
    scenario_id: str,
) -> None:
    catalog = load_json_exact(MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json")
    row = next(member for member in catalog if member["scenario_id"] == scenario_id)
    result = execute_corrected_scenario(MTC_V2_ROOT, row)["RESULT_SURFACE"]
    expected = {
        "final_position",
        "trades",
        "equity_curve",
        "metrics",
        "warnings",
        "refusals",
        "run_manifest",
    }
    if row["owning_def_ids"][0] in {"DEF-P012-01", "DEF-P012-02", "DEF-P012-05"}:
        expected.add("order_notional")
    if "DEF-P012-02" in row["owning_def_ids"] and row["role"] == "GREEN":
        expected.add("admitted")
    if row["owning_def_ids"][0] == "DEF-P012-07":
        expected.add("guards")
    if "DEF-P012-08" in row["owning_def_ids"]:
        expected.add("cumulative_funding")
    assert set(result) == expected
    assert result["metrics"] is None


@pytest.mark.parametrize(
    ("scenario_id", "expected_refusal"),
    [
        (
            "RULE2-02-RED",
            {
                "code": "REFUSED_MIN_NOTIONAL",
                "order_notional": 100,
                "required_min_notional": 101,
            },
        ),
        (
            "RULE2-03-RED",
            {
                "code": "REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION",
                "field": "price_tick",
                "record_value": 0.5,
                "runtime_value": 0.25,
                "stage": "PRE_EVALUATION",
            },
        ),
    ],
)
def test_section_23_refusals_are_closed_tagged_objects(
    scenario_id: str, expected_refusal: dict[str, object]
) -> None:
    catalog = load_json_exact(MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json")
    row = next(member for member in catalog if member["scenario_id"] == scenario_id)

    refusals = execute_corrected_scenario(MTC_V2_ROOT, row)["RESULT_SURFACE"]["refusals"]

    assert refusals == [expected_refusal]


@pytest.mark.parametrize(
    ("scenario_id", "expected"),
    [
        (
            "RULE2-07-RED",
            {
                "guard_pnl_basis": "GROSS-MINUS-FEES",
                "last_closed_guard_pnl": -0.2,
                "consecutive_loss_count": 1,
                "consec_loss_ok": False,
                "guard_blocked_raw": True,
            },
        ),
        (
            "RULE2-07-GREEN",
            {
                "guard_pnl_basis": "GROSS-MINUS-FEES",
                "consecutive_loss_count": 0,
                "consec_loss_ok": True,
                "guard_blocked_raw": False,
            },
        ),
    ],
)
def test_w304_row3_serializes_the_computed_guard_snapshot(
    scenario_id: str, expected: dict[str, object]
) -> None:
    catalog = load_json_exact(MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json")
    row = next(member for member in catalog if member["scenario_id"] == scenario_id)

    result = execute_corrected_scenario(MTC_V2_ROOT, row)["RESULT_SURFACE"]

    assert result["guards"] == expected


def test_rule2_05_red_sizes_from_final_fill_and_preserves_zero_economics() -> None:
    catalog = load_json_exact(MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json")
    row = next(member for member in catalog if member["scenario_id"] == "RULE2-05-RED")

    observed = execute_corrected_scenario(MTC_V2_ROOT, row)

    assert [
        (member["final_fill_price"], member["quantity"])
        for member in observed["EVENT_SURFACE"]["fill_events"]
    ] == [(101, 0)]
    assert [
        (member["kind"], member["signed_delta"])
        for member in observed["EVENT_SURFACE"]["cash_events"]
    ] == [("FEE", 0)]
    assert type(observed["EVENT_SURFACE"]["cash_events"][0]["signed_delta"]) is int
    assert observed["EVENT_SURFACE"]["fee_events"][0]["fee_cash_delta"] == 0
    assert observed["RESULT_SURFACE"]["final_position"] == {
        "side": "LONG",
        "quantity": 0,
        "entry_fill_price": 101,
    }
    assert observed["RESULT_SURFACE"]["order_notional"] == 0


@pytest.mark.parametrize(
    ("scenario_id", "expected_notional"),
    [
        ("RULE2-01-RED", 1000),
        ("RULE2-01-GREEN", 100),
        ("RULE2-02-RED", 100),
        ("RULE2-05-RED", 0),
        ("RULE2-05-GREEN", 100),
    ],
)
def test_w304_row1_serializes_kernel_computed_order_notional(
    scenario_id: str, expected_notional: int
) -> None:
    catalog = load_json_exact(MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json")
    row = next(member for member in catalog if member["scenario_id"] == scenario_id)

    result = execute_corrected_scenario(MTC_V2_ROOT, row)["RESULT_SURFACE"]

    assert result["order_notional"] == expected_notional


def test_w304_row2_serializes_the_kernel_admission_outcome() -> None:
    catalog = load_json_exact(MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json")
    rows = {
        member["scenario_id"]: member
        for member in catalog
        if member.get("scenario_id") in {"RULE2-02-RED", "RULE2-02-GREEN"}
    }

    red = execute_corrected_scenario(MTC_V2_ROOT, rows["RULE2-02-RED"])["RESULT_SURFACE"]
    green = execute_corrected_scenario(MTC_V2_ROOT, rows["RULE2-02-GREEN"])["RESULT_SURFACE"]

    assert "admitted" not in red
    assert green["admitted"] is True


def test_rule2_06_green_uses_the_closed_stop_touch_token() -> None:
    catalog = load_json_exact(MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json")
    row = next(member for member in catalog if member["scenario_id"] == "RULE2-06-GREEN")

    observed = execute_corrected_scenario(MTC_V2_ROOT, row)

    assert observed["EVENT_SURFACE"]["fill_events"][0]["fill_trigger"] == "STOP_TOUCH"
    assert observed["EVENT_SURFACE"]["exit_events"][0]["fill_trigger"] == "STOP_TOUCH"


@pytest.mark.parametrize("scenario_id", ["RULE2-08-RED", "RULE2-08-GREEN"])
def test_rule2_08_raw_kernel_is_not_seeded_from_legacy_state(
    scenario_id: str,
) -> None:
    catalog = load_json_exact(MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json")
    row = next(member for member in catalog if member["scenario_id"] == scenario_id)

    observed = execute_corrected_scenario(MTC_V2_ROOT, row)

    result = observed["RESULT_SURFACE"]
    event = observed["EVENT_SURFACE"]
    assert result["refusals"] == []
    # Owner decision 144; design P012_FRESH_DESIGN_V1.md:490 binds RED->RED and GREEN->GREEN cost records.
    assert result["run_manifest"]["cost_schedule_id"] == {
        "RULE2-08-RED": "SYNTH-COST-RULE2-07-RED-V1",
        "RULE2-08-GREEN": "SYNTH-COST-RULE2-07-GREEN-V1",
    }[scenario_id]
    # Owner decision 144; design P012_FRESH_DESIGN_V1.md:488,492,494 binds the in-window funding projection.
    assert [member["signed_delta"] for member in event["cash_events"]] == {
        "RULE2-08-RED": [-0.1],
        "RULE2-08-GREEN": [],
    }[scenario_id]
    assert [member["funding_cash_delta"] for member in event["funding_events"]] == {
        "RULE2-08-RED": [-0.1],
        "RULE2-08-GREEN": [],
    }[scenario_id]
    assert result["cumulative_funding"] == {
        "RULE2-08-RED": -0.1,
        "RULE2-08-GREEN": 0,
    }[scenario_id]


@pytest.fixture
def sealed_projection_row():
    def build(role: str, corrected_kind: str) -> dict[str, object]:
        field = (
            "rule2_divergent_projection"
            if role == "RED"
            else "rule2_green_projection"
        )
        relation = "DIFFERS" if role == "RED" else "EQUAL"
        return {
            "scenario_id": f"W318-{role}",
            "role": role,
            field: [
                {
                    "selector": "/RESULT_SURFACE/value",
                    "legacy": {
                        "tag": "PRESENT",
                        "node_kind": "I",
                        "value": 1,
                        "source": "DESIGN_DERIVED",
                        "design_lines": "543",
                    },
                    "corrected": {
                        "selector": ["RESULT_SURFACE", "value"],
                        "node_kind": corrected_kind,
                        "source": "CONTRACT_TABLES",
                        "design_lines": "543",
                    },
                    "expected_relation": relation,
                    "derivation": f"W318-{role}-FIXTURE",
                }
            ],
        }

    return build


@pytest.mark.parametrize(
    ("corrected_kind", "corrected_value", "expected_pass"),
    [("F", 1.0, True), ("I", 1, False)],
    ids=("unequal-kinds-pass", "equal-states-fail"),
)
def test_rule2_divergent_projection_discriminates_sealed_states(
    sealed_projection_row,
    corrected_kind: str,
    corrected_value: float | int,
    expected_pass: bool,
) -> None:
    row = sealed_projection_row("RED", corrected_kind)

    projections = build_projection_results(
        "W318-RED",
        row,
        {"must_not_be_read": "BASELINE_BYTES"},
        {"RESULT_SURFACE": {"value": corrected_value}},
    )

    assert all(not projection["equal"] for projection in projections) is expected_pass
    assert projections[0]["legacy_side_source"] == "DESIGN_DERIVED"


@pytest.mark.parametrize(
    ("corrected_kind", "corrected_value", "expected_pass"),
    [("I", 1, True), ("F", 1.0, False)],
    ids=("equal-states-pass", "unequal-kinds-fail"),
)
def test_rule2_green_projection_discriminates_sealed_states(
    sealed_projection_row,
    corrected_kind: str,
    corrected_value: float | int,
    expected_pass: bool,
) -> None:
    row = sealed_projection_row("GREEN", corrected_kind)

    projections = build_projection_results(
        "W318-GREEN",
        row,
        {"must_not_be_read": "BASELINE_BYTES"},
        {"RESULT_SURFACE": {"value": corrected_value}},
    )

    assert all(projection["equal"] for projection in projections) is expected_pass
    assert projections[0]["legacy_side_source"] == "DESIGN_DERIVED"


def test_all_projection_rows_refuse_without_sealed_selector_declarations() -> None:
    catalog = load_json_exact(MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json")

    for row in catalog:
        if row["role"] not in {"RED", "GREEN"}:
            continue
        field = (
            "rule2_divergent_projection"
            if row["role"] == "RED"
            else "rule2_green_projection"
        )
        if field in row:
            continue
        scenario_id = row["scenario_id"]
        with pytest.raises(GateRefusal) as caught:
            build_projection_results(
                scenario_id,
                row,
                {"must_not_be_read": "BASELINE_BYTES"},
                {"must_not_be_read": "CONTRACT_TABLES"},
            )

        assert caught.value.check_id == "EXPECTATION_UNSEALED"
        assert caught.value.pointer == f"/{field}"


def test_rederived_value_projection_refuses_a_sibling_citation_copy() -> None:
    catalog = load_json_exact(
        MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json"
    )
    row = next(member for member in catalog if member["scenario_id"] == "RULE2-01-RED")
    golden = load_json_exact(MTC_V2_ROOT / "golden/corrected_vnext/RULE2-01-RED.json")
    modified = deepcopy(row)
    declarations = modified["rule2_divergent_projection"]
    declarations[2]["legacy"]["design_lines"] = declarations[0]["legacy"]["design_lines"]

    with pytest.raises(GateRefusal) as caught:
        build_projection_results(
            "RULE2-01-RED",
            modified,
            {"must_not_be_read": "BASELINE_BYTES"},
            golden,
        )

    assert caught.value.check_id == "PROJECTION_CITATION_DUPLICATE"
    assert caught.value.pointer == "/rule2_divergent_projection/2/legacy/design_lines"
    build_projection_results(
        "RULE2-01-RED",
        row,
        {"must_not_be_read": "BASELINE_BYTES"},
        golden,
    )


def test_w305_item6_refuses_missing_sealed_equal_price_target_book() -> None:
    scenario_id = "RULE2-06-EQUAL-PRICE-RED"
    catalog = load_json_exact(
        MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json"
    )
    row = next(member for member in catalog if member["scenario_id"] == scenario_id)

    observed = execute_corrected_scenario(MTC_V2_ROOT, row)

    # Owner decisions 139/142; design P012_FRESH_DESIGN_V1.md:402 binds the sealed equal-price target order.
    assert observed["RESULT_SURFACE"]["refusals"] == []
    assert [member["exit_id"] for member in observed["EVENT_SURFACE"]["exit_events"]] == [
        "TARGET-FAR",
        "TARGET-NEAR",
    ]


def test_w305_item6_config_transports_only_declared_economic_inputs() -> None:
    catalog = load_json_exact(
        MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json"
    )
    row = next(member for member in catalog if member["scenario_id"] == "RULE2-01-RED")
    document = load_json_exact(MTC_V2_ROOT / row["input"]["path"])

    config = verify_bceg.corrected_contract_config(document)

    assert "same_bar_collision_policy_id" not in config
    assert "slippage_model_id" not in config


def test_all_declared_corrected_scenarios_execute_or_refuse_missing_input() -> None:
    catalog = load_json_exact(MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json")

    observed = []
    refused = []
    for row in catalog:
        if row["role"] not in {"RED", "GREEN"}:
            continue
        try:
            observed.append(execute_corrected_scenario(MTC_V2_ROOT, row))
        except GateRefusal as exc:
            refused.append((row["scenario_id"], exc.check_id, exc.pointer))

    # Owner decisions 139/142/144; design P012_FRESH_DESIGN_V1.md:402,488-494 binds all declared rows runnable.
    assert [member["scenario_id"] for member in observed] == [
        row["scenario_id"]
        for row in catalog
        if row["role"] in {"RED", "GREEN"}
    ]
    assert all(member["semantics_version"] == "2.0.0" for member in observed)
    assert refused == []
