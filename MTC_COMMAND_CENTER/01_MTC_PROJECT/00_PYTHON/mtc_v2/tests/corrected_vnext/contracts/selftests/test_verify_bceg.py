from __future__ import annotations

import hashlib
import json
import math
import shutil
import subprocess
from copy import deepcopy
from pathlib import Path

import pytest

from mtc_v2.tests.corrected_vnext import verify_bceg
from mtc_v2.tests.corrected_vnext.verify_bceg import (
    GateRefusal,
    build_projection_results,
    compare_documents,
    compare_scoped_expected,
    decode_stop_price_f64,
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


def refusal(check_id: str, action) -> None:
    with pytest.raises(GateRefusal) as caught:
        action()
    assert caught.value.check_id == check_id


def semantic_review_fixture(root: Path) -> dict[str, object]:
    evidence_paths: list[str] = []
    for item in range(1, 7):
        path = root / "review-evidence" / f"item-{item}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"item {item} evidence\n", encoding="utf-8", newline="\n")
        evidence_paths.append(path.relative_to(root).as_posix())
    return {
        "schema": "P012_SEMANTIC_COVERAGE_REVIEW_V1",
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
        "reviewed_identities": dict(SYNTHETIC_REVIEW_IDENTITIES),
        "items": {
            str(item): {
                "disposition": "ACCEPTED",
                "evidence_paths": [evidence_paths[item - 1]],
                "notes": "Reviewed against the synthetic fixture.",
            }
            for item in range(1, 7)
        },
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
) -> int:
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
    if not use_real_git:
        monkeypatch.setattr(
            verify_bceg,
            "semantic_review_commit_is_ancestor",
            lambda _root, reviewed_commit, head_commit: reviewed_commit
            == head_commit,
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


def two_commit_repository(root: Path) -> tuple[str, str]:
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
    marker = root / "commit-marker.txt"
    marker.write_text("reviewed\n", encoding="utf-8", newline="\n")
    subprocess.run(
        ["git", "-C", str(root), "add", "commit-marker.txt"],
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
        ["git", "-C", str(root), "add", "commit-marker.txt"],
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
    receipt = semantic_review_fixture(root)
    reviewed_commit, head_commit = two_commit_repository(root)
    measured = dict(SYNTHETIC_REVIEW_IDENTITIES)
    measured["worktree_head_commit"] = head_commit
    receipt["reviewed_identities"]["worktree_head_commit"] = reviewed_commit
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
    contracts = MTC_V2_ROOT / "tests/corrected_vnext/contracts"
    manifest = load_json_exact(contracts / "CONTRACT_TABLES_MANIFEST.json")
    anchor = load_json_exact(contracts / "implementation_anchor.json")

    refusal(
        "EXPECTED_PATH_CHANGED_AFTER_BASE",
        lambda: verify_bceg.validate_expected_source_provenance(
            MTC_V2_ROOT, manifest, anchor
        ),
    )


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
    row = {
        "scenario_id": scenario_id,
        "role": "RED",
        "input": {"path": input_path.relative_to(root).as_posix()},
        "expected_artifacts": {
            "2.0.0": {"path": golden_path.relative_to(root).as_posix()}
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


def test_probe_driver_refuses_unclosed_base_before_variant_comparison(
    tmp_path: Path,
) -> None:
    catalog = load_json_exact(
        MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json"
    )
    probe = next(
        row for row in catalog if row.get("probe_id") == "PROBE-P012-08-A"
    )
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
    assert identity_receipt["measured_failed_check"] == "CLOSED_SET_VIOLATION"
    assert (
        identity_receipt["comparator_first_differing_node"]
        == "/RESULT_SURFACE/cumulative_funding"
    )
    assert identity_receipt["expected_node_changed"] is False

    modified = MTC_V2_ROOT / probe["modified_copy_path"]
    modified_manifest = load_json_exact(
        MTC_V2_ROOT
        / "tests/corrected_vnext/probes/PROBE-P012-08-A/modified_tree_manifest.json"
    )
    modified_receipt = verify_bceg.drive_probe_variant_process(
        MTC_V2_ROOT,
        tmp_path / "unused-baseline",
        probe,
        modified,
        modified_manifest,
    )

    assert modified_receipt["status"] == "NOT_DETECTED"
    assert modified_receipt["measured_failed_check"] == "CLOSED_SET_VIOLATION"
    assert (
        modified_receipt["comparator_first_differing_node"]
        == "/RESULT_SURFACE/cumulative_funding"
    )
    assert modified_receipt["expected_node_changed"] is False


def test_probe_cannot_claim_target_membership_when_base_is_refused(
    tmp_path: Path,
) -> None:
    catalog = load_json_exact(
        MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json"
    )
    probe = next(
        row for row in catalog if row.get("probe_id") == "PROBE-P012-08-A"
    )
    expected_node = "/EVENT_SURFACE/funding_events/0/funding_cash_delta"
    comparator_first_node = "/EVENT_SURFACE/cash_events/0/signed_delta"
    assert probe["expected_first_changed_node"] == expected_node
    assert probe["comparator_first_differing_node"] == comparator_first_node
    assert expected_node != comparator_first_node

    modified = MTC_V2_ROOT / probe["modified_copy_path"]
    modified_manifest = load_json_exact(
        MTC_V2_ROOT
        / "tests/corrected_vnext/probes/PROBE-P012-08-A/modified_tree_manifest.json"
    )
    receipt = verify_bceg.drive_probe_variant_process(
        MTC_V2_ROOT,
        tmp_path / "unused-baseline",
        probe,
        modified,
        modified_manifest,
    )

    assert receipt["status"] == "NOT_DETECTED"
    assert receipt["measured_failed_check"] == "CLOSED_SET_VIOLATION"
    assert receipt["expected_first_changed_node"] == expected_node
    assert (
        receipt["comparator_first_differing_node"]
        == "/RESULT_SURFACE/cumulative_funding"
    )
    assert receipt["expected_node_changed"] is False


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
            row["scenario_id"],
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
            row["scenario_id"],
            {
                "EVENT_SURFACE": observed["EVENT_SURFACE"],
                "RESULT_SURFACE": observed["RESULT_SURFACE"],
            },
        )
    assert caught.value.check_id == "CLOSED_SET_VIOLATION"
    assert caught.value.pointer == "/RESULT_SURFACE/warnings"


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
        ("RULE2-06-EQUAL-PRICE-RED", ["SEMANTICS_VALIDATED", "PROTECTIVE_STOP_EVALUATED", "COLLISION_RESOLVED"]),
        ("RULE2-06-GREEN", ["SEMANTICS_VALIDATED", "PROTECTIVE_STOP_EVALUATED", "COLLISION_RESOLVED"]),
        ("RULE2-07-RED", ["SEMANTICS_VALIDATED", "SIZING_COMPUTED", "MIN_NOTIONAL_ADMITTED"]),
        ("RULE2-07-GREEN", ["SEMANTICS_VALIDATED"]),
        ("RULE2-08-RED", ["SEMANTICS_VALIDATED"]),
        ("RULE2-08-GREEN", ["SEMANTICS_VALIDATED"]),
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
        "RULE2-06-EQUAL-PRICE-RED",
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
        ("RULE2-06-EQUAL-PRICE-RED", {"first": 999.91, "last": 1009.8155}),
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
        "RULE2-06-EQUAL-PRICE-RED",
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
        "RULE2-06-EQUAL-PRICE-RED",
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
    if scenario_id == "RULE2-02-GREEN":
        expected.add("admitted")
    if row["owning_def_ids"][0] == "DEF-P012-07":
        expected.add("guards")
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
    assert result["run_manifest"]["cost_schedule_id"] == "NOT_CONSUMED"
    assert event["cash_events"] == []
    assert event["funding_events"] == []
    assert "cumulative_funding" not in result


def test_rule2_02_red_projection_matches_design_and_all_pairs_diverge() -> None:
    scenario_id = "RULE2-02-RED"
    expected_selectors = [
        "/RESULT_SURFACE/refusals/0/code",
        "/EVENT_SURFACE/fill_events",
        "/RESULT_SURFACE/final_position",
    ]
    catalog = load_json_exact(MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json")
    row = next(member for member in catalog if member["scenario_id"] == scenario_id)
    input_document = load_json_exact(MTC_V2_ROOT / row["input"]["path"])
    legacy = load_json_exact(
        Path(r"C:\tmp\P012_BASELINE_RUN")
        / "out"
        / scenario_id
        / "result_surface.json"
    )
    corrected = load_json_exact(
        MTC_V2_ROOT / row["expected_artifacts"]["2.0.0"]["path"]
    )

    projections = build_projection_results(
        scenario_id,
        input_document,
        legacy,
        corrected,
    )

    assert [member["selector"] for member in projections] == expected_selectors
    assert [member["equal"] for member in projections] == [False] * len(
        expected_selectors
    )


def test_all_red_projection_pairs_resolve_on_sealed_goldens_and_diverge() -> None:
    baseline_root = Path(r"C:\tmp\P012_BASELINE_RUN")
    catalog = load_json_exact(MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json")

    for row in catalog:
        if row["role"] != "RED":
            continue
        scenario_id = row["scenario_id"]
        projections = build_projection_results(
            scenario_id,
            load_json_exact(MTC_V2_ROOT / row["input"]["path"]),
            load_json_exact(
                baseline_root / "out" / scenario_id / "result_surface.json"
            ),
            load_json_exact(
                MTC_V2_ROOT / row["expected_artifacts"]["2.0.0"]["path"]
            ),
        )

        assert all(member["corrected"]["tag"] != "ABSENT" for member in projections)
        assert all(not member["equal"] for member in projections)


def test_all_cataloged_corrected_scenarios_are_executable() -> None:
    catalog = load_json_exact(MTC_V2_ROOT / "tests/corrected_vnext/contracts/scenario_catalog.json")

    observed = [
        execute_corrected_scenario(MTC_V2_ROOT, row)
        for row in catalog
        if row["role"] in {"RED", "GREEN"}
    ]

    assert [member["scenario_id"] for member in observed] == [
        row["scenario_id"] for row in catalog if row["role"] in {"RED", "GREEN"}
    ]
    assert all(member["semantics_version"] == "2.0.0" for member in observed)
