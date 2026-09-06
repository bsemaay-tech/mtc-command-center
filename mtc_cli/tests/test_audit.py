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


# ---------------------------------------------------------------------------
# Router-era layout regression (D9 / commit 552a41ec): GLOBAL_HANDOFF.md and
# NEXT_STEPS.md moved to _AI_MEMORY/history/; current state lives in stage
# HANDOFF.md files, sticky decisions in root DECISIONS.md.
# ---------------------------------------------------------------------------
ROUTER_ERA_FILES = [
    "AGENTS.md",
    "CONTEXT_MAP.md",
    "DECISIONS.md",
    "MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md",
    "MTC_COMMAND_CENTER/_AI_MEMORY/AI_RULES.md",
    "MTC_COMMAND_CENTER/_AI_MEMORY/PROJECT_MEMORY.md",
    "MTC_COMMAND_CENTER/_AI_MEMORY/ACTIVE_FILES.md",
    "MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOCK.md",
    # archives: present only under history/, never at the pre-router path
    "MTC_COMMAND_CENTER/_AI_MEMORY/history/GLOBAL_HANDOFF.md",
    "MTC_COMMAND_CENTER/_AI_MEMORY/history/NEXT_STEPS.md",
]
GOV_HANDOFF = "MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/HANDOFF.md"
GOV_HANDOFF_TEXT = (
    "# Governance stage handoff\n\n"
    "## [Lead] 2026-09-06 — fixture\n\n"
    "- **NEXT ACTION:** publish through protected CI.\n"
    "- **WAITING FOR OWNER:** Nothing.\n"
)


def _router_era_fixture(root: Path) -> Path:
    for rel in ROUTER_ERA_FILES:
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f"# {rel}\n", encoding="utf-8")
    gov = root / GOV_HANDOFF
    gov.parent.mkdir(parents=True, exist_ok=True)
    gov.write_text(GOV_HANDOFF_TEXT, encoding="utf-8")
    assert not (root / "MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md").exists()
    assert not (root / "MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md").exists()
    return root


class TestRouterEraLayout:
    def test_real_repo_does_not_require_moved_files(self):
        """Real CLI must not flag the two files that 552a41ec moved into history/."""
        result = run_cli("audit", "repo", "--json")
        envelope = json.loads(result.stdout)
        moved = [
            f["message"] for f in envelope["findings"]
            if "_AI_MEMORY/GLOBAL_HANDOFF.md" in f["message"].replace("\\", "/")
            or "_AI_MEMORY/NEXT_STEPS.md" in f["message"].replace("\\", "/")
        ]
        assert moved == [], moved
        assert envelope["data"]["memory_files_ok"] is True

    def test_fixture_mirroring_router_layout_is_ok(self, tmp_path):
        """A tree laid out like the live repo (archives under history/) audits OK."""
        from mtc_cli import contract
        from mtc_cli.commands import audit as audit_mod

        env = audit_mod.run(repo_root=_router_era_fixture(tmp_path))
        errors = [f for f in env.findings if f["severity"] == "ERROR"]
        assert errors == [], errors
        assert env.ok is True
        assert env.exit_code() == contract.EXIT_OK
        assert env.data["memory_files_ok"] is True
        assert env.data["handoff_next_actions"] == 1
        assert env.data["handoff_waiting_for_owner"] == 0

    def test_fixture_missing_required_file_still_fails(self, tmp_path):
        """Mutant: dropping a current-state file (DECISIONS.md) must yield FAIL / exit 2."""
        from mtc_cli import contract
        from mtc_cli.commands import audit as audit_mod

        root = _router_era_fixture(tmp_path)
        (root / "DECISIONS.md").unlink()
        env = audit_mod.run(repo_root=root)
        assert env.ok is False
        assert env.exit_code() == contract.EXIT_VALIDATION
        assert env.data["memory_files_ok"] is False
        assert {"severity": "ERROR", "message": "missing: DECISIONS.md"} in env.findings

    def test_fixture_missing_governance_handoff_is_not_silent(self, tmp_path):
        """The next-action check must report, not silently pass, when HANDOFF.md is absent."""
        from mtc_cli import contract
        from mtc_cli.commands import audit as audit_mod

        root = _router_era_fixture(tmp_path)
        (root / GOV_HANDOFF).unlink()
        env = audit_mod.run(repo_root=root)
        assert env.ok is False
        assert env.exit_code() == contract.EXIT_VALIDATION
        assert env.data["handoff_next_actions"] is None
        skipped = [f for f in env.findings if f["message"].startswith("handoff check skipped")]
        assert len(skipped) == 1 and skipped[0]["severity"] == "ERROR"

    def test_fixture_waiting_for_owner_counted(self, tmp_path):
        """A real WAITING FOR OWNER item (not 'Nothing') is surfaced in data."""
        from mtc_cli.commands import audit as audit_mod

        root = _router_era_fixture(tmp_path)
        (root / GOV_HANDOFF).write_text(
            GOV_HANDOFF_TEXT + "- **WAITING FOR OWNER:** approve PAYG budget.\n",
            encoding="utf-8",
        )
        env = audit_mod.run(repo_root=root)
        assert env.ok is True
        assert env.data["handoff_waiting_for_owner"] == 1
