"""Tests for tools/release_evidence.py (TS-P0-002).

Reuses the temp-git-repo fixtures from test_runtime_baseline. The real repo
and runtime are never touched.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools import release_evidence as rev
from test_runtime_baseline import (
    TS,
    _commit_all,
    _git,
    _write,
    clone_runtime,
    make_source_repo,
)


@pytest.fixture()
def pair(tmp_path):
    repo = make_source_repo(tmp_path)
    # a second commit so a distinct rollback target exists
    _write(repo, "IBKR_PAPER_BRIDGE/bridge/app.py", "APP = 2\n")
    release = _commit_all(repo, "release")
    rollback = _git(repo, "rev-parse", "HEAD~1")
    runtime = clone_runtime(repo, tmp_path)
    return repo, runtime, release, rollback


def create_manifest(pair, tmp_path, capsys, out_name="release_manifest.json"):
    repo, runtime, release, rollback = pair
    out = tmp_path / out_name
    rc = rev.main(
        [
            "create",
            "--repo-root",
            str(repo),
            "--runtime-root",
            str(runtime),
            "--release-commit",
            release,
            "--rollback-commit",
            rollback,
            "--timestamp",
            TS,
            "--out",
            str(out),
        ]
    )
    capsys.readouterr()
    return rc, out


def validate(pair, out, capsys, *extra):
    repo, runtime, _, _ = pair
    rc = rev.main(
        [
            "validate",
            "--manifest",
            str(out),
            "--repo-root",
            str(repo),
            "--runtime-root",
            str(runtime),
            *extra,
        ]
    )
    captured = capsys.readouterr()
    return rc, captured.out, captured.err


# ---------------------------------------------------------------------------
# create
# ---------------------------------------------------------------------------


def test_create_writes_complete_manifest(pair, tmp_path, capsys):
    rc, out = create_manifest(pair, tmp_path, capsys)
    assert rc == 0
    m = json.loads(out.read_text(encoding="utf-8"))
    for field in rev.REQUIRED_FIELDS:
        assert field in m, f"missing {field}"
    assert m["schema_version"] == rev.SCHEMA_VERSION
    assert m["release_commit"] == pair[2]
    assert m["rollback_commit"] == pair[3]
    for key in (
        "source_tree_hash",
        "config_hash",
        "lock_hash",
        "schema_hash",
        "runtime_source_tree_hash",
        "runtime_config_hash",
    ):
        assert m["hashes"][key], f"empty hash {key}"
    assert m["integrity_sha256"]


def test_create_rejects_release_commit_not_head(pair, tmp_path, capsys):
    repo, runtime, release, rollback = pair
    rc = rev.main(
        [
            "create",
            "--repo-root",
            str(repo),
            "--runtime-root",
            str(runtime),
            "--release-commit",
            rollback,  # not HEAD
            "--rollback-commit",
            rollback,
            "--timestamp",
            TS,
            "--out",
            str(tmp_path / "m.json"),
        ]
    )
    capsys.readouterr()
    assert rc == 3


def test_create_deterministic_bytes(pair, tmp_path, capsys):
    rc_a, out_a = create_manifest(pair, tmp_path, capsys, "a.json")
    rc_b, out_b = create_manifest(pair, tmp_path, capsys, "b.json")
    assert rc_a == rc_b == 0
    assert out_a.read_bytes() == out_b.read_bytes()


# ---------------------------------------------------------------------------
# validate — happy path
# ---------------------------------------------------------------------------


def test_validate_clean_manifest_exit_0(pair, tmp_path, capsys):
    rc, out = create_manifest(pair, tmp_path, capsys)
    assert rc == 0
    vrc, vout, _ = validate(pair, out, capsys)
    report = json.loads(vout)
    assert vrc == 0, report
    assert report["verdict"] == "VALID"
    assert report["failures"] == []


# ---------------------------------------------------------------------------
# validate — required negative tests (card: tamper, missing field, old version)
# ---------------------------------------------------------------------------


def test_validate_detects_tamper(pair, tmp_path, capsys):
    rc, out = create_manifest(pair, tmp_path, capsys)
    m = json.loads(out.read_text(encoding="utf-8"))
    m["hashes"]["config_hash"] = "0" * 64  # tampered value, integrity not recomputed
    out.write_text(json.dumps(m, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    vrc, vout, _ = validate(pair, out, capsys)
    report = json.loads(vout)
    assert vrc == 2
    assert report["verdict"] == "INVALID"
    assert "integrity_hash_mismatch" in report["failures"]


def test_validate_detects_missing_field(pair, tmp_path, capsys):
    rc, out = create_manifest(pair, tmp_path, capsys)
    m = json.loads(out.read_text(encoding="utf-8"))
    del m["rollback_commit"]
    out.write_text(json.dumps(m, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    vrc, vout, _ = validate(pair, out, capsys)
    report = json.loads(vout)
    assert vrc == 2
    assert "missing_field:rollback_commit" in report["failures"]


def test_validate_rejects_old_schema_version(pair, tmp_path, capsys):
    rc, out = create_manifest(pair, tmp_path, capsys)
    m = json.loads(out.read_text(encoding="utf-8"))
    m["schema_version"] = "0.9.0"
    out.write_text(json.dumps(m, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    vrc, vout, _ = validate(pair, out, capsys)
    report = json.loads(vout)
    assert vrc == 2
    assert "unsupported_schema_version:0.9.0" in report["failures"]


def test_validate_unknown_rollback_commit(pair, tmp_path, capsys):
    repo, runtime, release, rollback = pair
    rc, out = create_manifest(pair, tmp_path, capsys)
    m = json.loads(out.read_text(encoding="utf-8"))
    fake = "ab" * 20
    m["rollback_commit"] = fake
    m["integrity_sha256"] = rev._integrity_hash(m)  # re-sign so only this check fails
    out.write_text(json.dumps(m, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    vrc, vout, _ = validate(pair, out, capsys)
    report = json.loads(vout)
    assert vrc == 2
    assert f"rollback_commit_unknown:{fake}" in report["failures"]


def test_validate_detects_current_state_drift(pair, tmp_path, capsys):
    """Manifest is internally valid but repo has moved on -> drift failure."""
    repo, runtime, release, rollback = pair
    rc, out = create_manifest(pair, tmp_path, capsys)
    _write(repo, "IBKR_PAPER_BRIDGE/bridge/app.py", "APP = 3\n")
    _commit_all(repo, "post-release change")
    vrc, vout, _ = validate(pair, out, capsys)
    report = json.loads(vout)
    assert vrc == 2
    assert "repo_head_not_release_commit" in report["failures"]


def test_validate_corrupt_json_exit_3(pair, tmp_path, capsys):
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    vrc, _, err = validate(pair, bad, capsys)
    assert vrc == 3
    assert "Traceback" not in err


def test_validate_missing_manifest_exit_3(pair, tmp_path, capsys):
    vrc, _, err = validate(pair, tmp_path / "absent.json", capsys)
    assert vrc == 3
    assert "Traceback" not in err
