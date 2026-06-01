"""Tests for mtc_cli audit repo command."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def run_cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "mtc_cli", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=30,
    )


class TestAuditRepo:
    def test_exit_code_ok_on_healthy_repo(self):
        """Audit should exit 0 on a repo with all memory files present."""
        result = run_cli("audit", "repo", "--json")
        envelope = json.loads(result.stdout)
        # Memory files must all exist for exit 0
        if envelope["data"]["memory_files_ok"]:
            assert result.returncode == 0
        else:
            # Some memory files missing — exit 2 is correct
            assert result.returncode in (0, 2)

    def test_json_envelope_shape(self):
        """--json flag must produce a valid envelope with required keys."""
        result = run_cli("audit", "repo", "--json")
        assert result.returncode in (0, 1, 2)
        envelope = json.loads(result.stdout)
        assert "ok" in envelope
        assert "command" in envelope
        assert "data" in envelope
        assert envelope["command"] == "audit repo"

    def test_envelope_ok_field_bool(self):
        result = run_cli("audit", "repo", "--json")
        envelope = json.loads(result.stdout)
        assert isinstance(envelope["ok"], bool)

    def test_data_has_memory_files_ok(self):
        result = run_cli("audit", "repo", "--json")
        envelope = json.loads(result.stdout)
        assert "memory_files_ok" in envelope["data"]

    def test_data_has_git_staged_count(self):
        result = run_cli("audit", "repo", "--json")
        envelope = json.loads(result.stdout)
        assert "git_staged_count" in envelope["data"]

    def test_human_output_no_json_flag(self):
        """Without --json, output should be human-readable (not JSON)."""
        result = run_cli("audit", "repo")
        assert result.returncode in (0, 1, 2)
        # Should NOT be valid JSON
        try:
            json.loads(result.stdout)
            human = False
        except json.JSONDecodeError:
            human = True
        assert human, "Expected human output, got JSON"

    def test_byte_stable_on_unchanged_repo(self):
        """Running twice with same repo state must produce identical JSON."""
        r1 = run_cli("audit", "repo", "--json")
        r2 = run_cli("audit", "repo", "--json")
        e1 = json.loads(r1.stdout)
        e2 = json.loads(r2.stdout)
        # Fields that may vary: heartbeat_age_minutes (time-dependent) — exclude
        e1["data"].pop("heartbeat_age_minutes", None)
        e2["data"].pop("heartbeat_age_minutes", None)
        assert e1 == e2, f"Outputs differ:\n{e1}\nvs\n{e2}"

    def test_missing_fixture_exit_2(self, tmp_path, monkeypatch):
        """If a required memory file is missing, exit code must be 2."""
        # We test via contract logic directly (not subprocess with monkeypatch)
        import sys
        sys.path.insert(0, str(REPO_ROOT))
        from mtc_cli.commands import audit as audit_mod
        from mtc_cli import contract

        # Temporarily point to a non-existent path
        original = audit_mod.REQUIRED_MEMORY_FILES
        audit_mod.REQUIRED_MEMORY_FILES = [tmp_path / "nonexistent_file.md"]
        try:
            envelope = audit_mod.run()
            assert not envelope.ok
            assert envelope.exit_code() == contract.EXIT_VALIDATION
        finally:
            audit_mod.REQUIRED_MEMORY_FILES = original
