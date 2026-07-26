"""Tests for tools/check_runtime_baseline.py (TS-P0-001).

All fixtures are throwaway temp git repositories — the real repo and the real
runtime are never touched. The tool under test is imported in-process so
monkeypatching git output is possible without shelling tricks.
"""

from __future__ import annotations

import json
import hashlib
import subprocess
import sys
from pathlib import Path

import pytest

from tools import check_runtime_baseline as crb


# ---------------------------------------------------------------------------
# fixture helpers: temp git repos shaped like the bridge repo
# ---------------------------------------------------------------------------


def _git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(cwd), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _init_repo(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    _git(root, "init", "--quiet")
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "Test")
    _git(root, "config", "core.autocrlf", "false")


def _commit_all(root: Path, msg: str) -> str:
    _git(root, "add", "-A")
    _git(root, "commit", "--quiet", "-m", msg)
    return _git(root, "rev-parse", "HEAD")


def _write(root: Path, rel: str, content: str) -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8", newline="\n")
    return p


def make_source_repo(tmp_path: Path) -> Path:
    """Minimal repo mirroring the hashed scope layout."""
    root = tmp_path / "repo"
    _init_repo(root)
    _write(root, "IBKR_PAPER_BRIDGE/bridge/app.py", "APP = 1\n")
    _write(root, "IBKR_PAPER_BRIDGE/bridge/engine/engine.py", "ENGINE = 1\n")
    _write(root, "IBKR_PAPER_BRIDGE/bridge/store/db.py", "SCHEMA = 1\n")
    _write(root, "IBKR_PAPER_BRIDGE/config/bridge.yaml", "mode: paper\n")
    _write(
        root,
        "IBKR_PAPER_BRIDGE/config/strategies/keltner.yaml",
        "strategy: keltner\n",
    )
    _write(root, "IBKR_PAPER_BRIDGE/requirements.txt", "fastapi==0.1\n")
    _write(root, "IBKR_PAPER_BRIDGE/tools/run_bridge_p2.ps1", "# wrapper\n")
    _commit_all(root, "initial")
    return root


def clone_runtime(repo: Path, tmp_path: Path) -> Path:
    runtime = tmp_path / "runtime"
    subprocess.run(
        [
            "git",
            "clone",
            "--quiet",
            "--config",
            "core.autocrlf=false",
            str(repo),
            str(runtime),
        ],
        check=True,
        capture_output=True,
    )
    _git(runtime, "config", "user.email", "test@example.com")
    _git(runtime, "config", "user.name", "Test")
    _git(runtime, "config", "core.autocrlf", "false")
    return runtime


@pytest.fixture()
def pair(tmp_path):
    repo = make_source_repo(tmp_path)
    runtime = clone_runtime(repo, tmp_path)
    head = _git(repo, "rev-parse", "HEAD")
    return repo, runtime, head


TS = "2026-07-19T00:00:00Z"


def run_tool(repo, runtime, expected, capsys, *extra):
    argv = [
        "--repo-root",
        str(repo),
        "--runtime-root",
        str(runtime),
        "--expected-commit",
        expected,
        "--timestamp",
        TS,
        *extra,
    ]
    rc = crb.main(argv)
    captured = capsys.readouterr()
    return rc, captured.out, captured.err


def manifest_of(out: str) -> dict:
    return json.loads(out)


def _snapshot(root: Path) -> dict:
    """Full recursive content snapshot used by the no-mutation test."""
    snap = {}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            snap[p.relative_to(root).as_posix()] = hashlib.sha256(
                p.read_bytes()
            ).hexdigest()
    return snap


# ---------------------------------------------------------------------------
# required tests (card TS-P0-001)
# ---------------------------------------------------------------------------


def test_clean_match_exit_0(pair, capsys):
    repo, runtime, head = pair
    rc, out, err = run_tool(repo, runtime, head, capsys)
    m = manifest_of(out)
    assert rc == 0
    assert m["verdict"] == "MATCH"
    assert m["drift_reasons"] == []
    assert m["repo"]["commit"] == head
    assert m["runtime"]["commit"] == head
    assert m["repo"]["dirty"] is False
    assert m["runtime"]["dirty"] is False
    assert m["comparison"]["source_tree_hash_equal"] is True
    assert m["comparison"]["config_hash_equal"] is True
    # acceptance: schema version, timestamp, canonical paths, both commits present
    assert m["schema_version"] == crb.SCHEMA_VERSION
    assert m["generated_at_utc"] == TS
    assert Path(m["repo"]["root"]).resolve() == repo.resolve()
    assert Path(m["runtime"]["root"]).resolve() == runtime.resolve()


def test_commit_drift_exit_2(pair, capsys):
    repo, runtime, head = pair
    _write(repo, "IBKR_PAPER_BRIDGE/bridge/app.py", "APP = 2\n")
    _commit_all(repo, "drift")
    rc, out, _ = run_tool(repo, runtime, head, capsys)
    m = manifest_of(out)
    assert rc == 2
    assert m["verdict"] == "DRIFT"
    assert "repo_commit_mismatch_expected" in m["drift_reasons"]
    assert "repo_runtime_commit_mismatch" in m["drift_reasons"]
    assert "source_tree_hash_mismatch" in m["drift_reasons"]


def test_dirty_repo_exit_2(pair, capsys):
    repo, runtime, head = pair
    _write(repo, "IBKR_PAPER_BRIDGE/bridge/app.py", "APP = 999\n")  # uncommitted
    rc, out, _ = run_tool(repo, runtime, head, capsys)
    m = manifest_of(out)
    assert rc == 2
    assert m["repo"]["dirty"] is True
    assert "repo_dirty" in m["drift_reasons"]
    assert m["repo"]["dirty_entries"]  # porcelain entries surfaced


def test_dirty_runtime_exit_2(pair, capsys):
    repo, runtime, head = pair
    _write(runtime, "IBKR_PAPER_BRIDGE/config/bridge.yaml", "mode: tampered\n")
    rc, out, _ = run_tool(repo, runtime, head, capsys)
    m = manifest_of(out)
    assert rc == 2
    assert m["runtime"]["dirty"] is True
    assert "runtime_dirty" in m["drift_reasons"]
    assert "config_hash_mismatch" in m["drift_reasons"]


def test_missing_runtime_exit_2(pair, tmp_path, capsys):
    repo, _, head = pair
    missing = tmp_path / "does-not-exist"
    rc, out, _ = run_tool(repo, missing, head, capsys)
    m = manifest_of(out)
    assert rc == 2
    assert m["verdict"] == "RUNTIME_MISSING"
    assert m["runtime"]["present"] is False
    assert "runtime_missing" in m["drift_reasons"]


def test_changed_config_detected(pair, capsys):
    repo, runtime, head = pair
    _write(runtime, "IBKR_PAPER_BRIDGE/config/bridge.yaml", "mode: live\n")
    _commit_all(runtime, "runtime config change")
    rc, out, _ = run_tool(repo, runtime, head, capsys)
    m = manifest_of(out)
    assert rc == 2
    assert m["runtime"]["dirty"] is False  # committed, so not dirty
    assert m["comparison"]["config_hash_equal"] is False
    assert "config_hash_mismatch" in m["drift_reasons"]
    assert "runtime_commit_mismatch_expected" in m["drift_reasons"]


def test_invalid_git_output_exit_3(pair, capsys, monkeypatch):
    repo, runtime, head = pair

    def bad_git(root, *args):
        if args[:2] == ("rev-parse", "HEAD"):
            return "this-is-not-a-commit-sha"
        return ""

    monkeypatch.setattr(crb, "_run_git", bad_git)
    rc, out, err = run_tool(repo, runtime, head, capsys)
    assert rc == 3
    assert "Traceback" not in err
    assert "invalid" in err.lower() or "malformed" in err.lower()


def test_missing_repo_root_exit_3(pair, tmp_path, capsys):
    _, runtime, head = pair
    rc, out, err = run_tool(tmp_path / "nope", runtime, head, capsys)
    assert rc == 3
    assert "Traceback" not in err


def test_invalid_expected_commit_exit_3(pair, capsys):
    repo, runtime, _ = pair
    rc, out, err = run_tool(repo, runtime, "zzzz-not-hex", capsys)
    assert rc == 3
    assert "Traceback" not in err


def test_deterministic_file_ordering(pair, capsys):
    repo, runtime, head = pair
    # create in reverse-sorted order; committed so trees stay comparable
    _write(repo, "IBKR_PAPER_BRIDGE/bridge/zzz.py", "Z = 1\n")
    _write(repo, "IBKR_PAPER_BRIDGE/bridge/aaa.py", "A = 1\n")
    _commit_all(repo, "ordering")
    head2 = _git(repo, "rev-parse", "HEAD")
    rc, out, _ = run_tool(repo, runtime, head2, capsys)
    m = manifest_of(out)
    repo_files = list(m["hashes"]["repo"]["files"].keys())
    assert repo_files == sorted(repo_files)
    # byte-for-byte identical on rerun with same declared timestamp
    rc2, out2, _ = run_tool(repo, runtime, head2, capsys)
    assert out == out2


def test_byte_stable_json_and_md_outputs(pair, tmp_path, capsys):
    repo, runtime, head = pair
    out_a = tmp_path / "a"
    out_b = tmp_path / "b"
    for d in (out_a, out_b):
        d.mkdir()
        rc, _, _ = run_tool(
            repo,
            runtime,
            head,
            capsys,
            "--json-out",
            str(d / "m.json"),
            "--md-out",
            str(d / "m.md"),
        )
        assert rc == 0
    assert (out_a / "m.json").read_bytes() == (out_b / "m.json").read_bytes()
    assert (out_a / "m.md").read_bytes() == (out_b / "m.md").read_bytes()


def test_secret_safe_output(pair, capsys, monkeypatch):
    """All five denylist names must be excluded and never passed to _hash_file."""
    repo, runtime, head = pair
    secret = "0xDEADBEEFCAFE_SECRET_VALUE"
    secret_files = [
        ("IBKR_PAPER_BRIDGE/config/.env", f"HL_API_WALLET_KEY={secret}\n"),
        ("IBKR_PAPER_BRIDGE/config/secrets.key", secret + "\n"),
        ("IBKR_PAPER_BRIDGE/config/prod.env", f"DB_PASS={secret}\n"),
        ("IBKR_PAPER_BRIDGE/config/my.secrets", secret + "\n"),
        ("IBKR_PAPER_BRIDGE/config/key.txt", secret + "\n"),
    ]
    for path, content in secret_files:
        _write(repo, path, content)

    hashed_paths = []
    real_hash = crb._hash_file

    def spy_hash(path):
        hashed_paths.append(Path(path).name)
        return real_hash(path)

    monkeypatch.setattr(crb, "_hash_file", spy_hash)
    rc, out, err = run_tool(repo, runtime, head, capsys)
    m = manifest_of(out)
    text = out + err
    assert secret not in text
    # All five basenames must be excluded — never passed to _hash_file
    denied_names = {".env", "secrets.key", "prod.env", "my.secrets", "key.txt"}
    for name in denied_names:
        assert name not in hashed_paths, f"{name} was hashed"
    assert not any(k.endswith(".env") for k in m["hashes"]["repo"]["files"])
    assert not any(k.endswith("secrets.key") for k in m["hashes"]["repo"]["files"])
    assert not any(k.endswith("prod.env") for k in m["hashes"]["repo"]["files"])
    assert not any(k.endswith("my.secrets") for k in m["hashes"]["repo"]["files"])
    assert not any(k.endswith("key.txt") for k in m["hashes"]["repo"]["files"])
    excluded_paths = [e["path"] for e in m["hashes"]["repo"]["excluded"]]
    for name in denied_names:
        assert any(p.endswith(name) for p in excluded_paths), f"{name} not in excluded"
    # planted secrets make the repo dirty (untracked) -> must exit 2, never 0
    assert rc == 2


def test_line_ending_only_difference_not_hash_drift(pair, capsys):
    """CRLF vs LF checkout noise must not flag source-tree hash drift.

    Observed on the real pair: git reports both worktrees clean/identical
    while raw bytes differ only in line endings. The hash comparison must
    agree with git, not with raw bytes.
    """
    repo, runtime, head = pair
    target = runtime / "IBKR_PAPER_BRIDGE/bridge/app.py"
    target.write_bytes(b"APP = 1\r\n")  # same content, CRLF endings
    rc, out, _ = run_tool(repo, runtime, head, capsys)
    m = manifest_of(out)
    assert m["comparison"]["source_tree_hash_equal"] is True
    assert "source_tree_hash_mismatch" not in m["drift_reasons"]


def test_no_mutation(pair, tmp_path, capsys):
    repo, runtime, head = pair
    before_repo = _snapshot(repo)
    before_runtime = _snapshot(runtime)
    status_repo = _git(repo, "status", "--porcelain")
    status_runtime = _git(runtime, "status", "--porcelain")
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    rc, _, _ = run_tool(
        repo,
        runtime,
        head,
        capsys,
        "--json-out",
        str(out_dir / "m.json"),
        "--md-out",
        str(out_dir / "m.md"),
    )
    assert rc == 0
    assert _snapshot(repo) == before_repo
    assert _snapshot(runtime) == before_runtime
    assert _git(repo, "status", "--porcelain") == status_repo
    assert _git(runtime, "status", "--porcelain") == status_runtime
