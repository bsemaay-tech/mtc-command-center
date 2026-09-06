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


# ---------------------------------------------------------------------------
# Lane R1 adversarial-review nits (OVERNIGHT_LANE_R1_ADVERSARIAL_CODE_REVIEW,
# 361b6451 subsection): widen the WAITING FOR OWNER "no ask" tokens beyond
# bare "nothing...", and line-anchor the NEXT ACTION presence check so a
# prose mention without a label doesn't satisfy it.
# ---------------------------------------------------------------------------
class TestWaitingForOwnerNoAskTokens:
    """`_is_no_owner_ask` must treat each of these as "no ask" (case-insensitive),
    matching the widened `_WAITING_NOTHING_WHOLE_VALUE_TOKENS` /
    `_WAITING_NOTHING_PREFIX_RE`."""

    def test_bare_none_token_is_no_ask(self):
        from mtc_cli.commands import audit as audit_mod

        assert audit_mod._is_no_owner_ask("none") is True
        assert audit_mod._is_no_owner_ask("None") is True
        assert audit_mod._is_no_owner_ask("NONE") is True

    def test_none_with_trailing_prose_is_not_automatically_no_ask(self):
        """Unlike 'nothing', 'none' is matched as the whole value, not a
        prefix: 'none' followed by more words is a real, countable ask."""
        from mtc_cli.commands import audit as audit_mod

        assert audit_mod._is_no_owner_ask("none for this lane") is False

    def test_parenthesized_none_is_no_ask(self):
        from mtc_cli.commands import audit as audit_mod

        assert audit_mod._is_no_owner_ask("(none)") is True
        assert audit_mod._is_no_owner_ask("(None)") is True
        assert audit_mod._is_no_owner_ask("( none )") is True

    def test_n_slash_a_token_is_no_ask(self):
        from mtc_cli.commands import audit as audit_mod

        assert audit_mod._is_no_owner_ask("n/a") is True
        assert audit_mod._is_no_owner_ask("N/A") is True

    def test_bare_hyphen_placeholder_is_no_ask(self):
        from mtc_cli.commands import audit as audit_mod

        assert audit_mod._is_no_owner_ask("-") is True

    def test_em_dash_placeholder_is_no_ask(self):
        from mtc_cli.commands import audit as audit_mod

        assert audit_mod._is_no_owner_ask("—") is True

    def test_empty_value_is_no_ask(self):
        from mtc_cli.commands import audit as audit_mod

        assert audit_mod._is_no_owner_ask("") is True
        assert audit_mod._is_no_owner_ask("   ") is True

    def test_nothing_for_this_lane_still_no_ask(self):
        """Regression: the pre-existing 'Nothing ...' behavior is unchanged."""
        from mtc_cli.commands import audit as audit_mod

        assert audit_mod._is_no_owner_ask("Nothing for this lane") is True
        assert audit_mod._is_no_owner_ask("Nothing.") is True

    def test_real_ask_is_not_no_ask(self):
        """A genuine ask must not be swallowed by the widened tokens."""
        from mtc_cli.commands import audit as audit_mod

        assert audit_mod._is_no_owner_ask("approve PAYG budget") is False
        assert audit_mod._is_no_owner_ask("none of the below — needs a decision on scope") is False

    def test_hyphen_prefixed_real_item_is_not_no_ask(self):
        """A '-' that starts a real sentence (not a bare placeholder) still counts."""
        from mtc_cli.commands import audit as audit_mod

        assert audit_mod._is_no_owner_ask("- approve the PR") is False

    def test_fixture_none_token_yields_zero_waiting_for_owner(self, tmp_path):
        """End-to-end: a 'None' WAITING FOR OWNER value audits as 0, not 1."""
        from mtc_cli.commands import audit as audit_mod

        root = _router_era_fixture(tmp_path)
        (root / GOV_HANDOFF).write_text(
            "# Governance stage handoff\n\n"
            "## [Lead] 2026-09-07 — fixture\n\n"
            "- **NEXT ACTION:** publish through protected CI.\n"
            "- **WAITING FOR OWNER:** None\n",
            encoding="utf-8",
        )
        env = audit_mod.run(repo_root=root)
        assert env.ok is True
        assert env.data["handoff_waiting_for_owner"] == 0

    def test_fixture_parenthesized_none_yields_zero_waiting_for_owner(self, tmp_path):
        """End-to-end: a '(none)' WAITING FOR OWNER value audits as 0, not 1."""
        from mtc_cli.commands import audit as audit_mod

        root = _router_era_fixture(tmp_path)
        (root / GOV_HANDOFF).write_text(
            "# Governance stage handoff\n\n"
            "## [Lead] 2026-09-07 — fixture\n\n"
            "- **NEXT ACTION:** publish through protected CI.\n"
            "- **WAITING FOR OWNER:** (none)\n",
            encoding="utf-8",
        )
        env = audit_mod.run(repo_root=root)
        assert env.ok is True
        assert env.data["handoff_waiting_for_owner"] == 0


class TestNextActionLabelLine:
    """`_handoff_next_action_count` is line-anchored: it counts lines carrying
    NEXT ACTION as a *label* (bolded or colon-terminated), not a bare
    substring match anywhere in the section."""

    def test_labelled_bullet_line_is_counted(self):
        from mtc_cli.commands import audit as audit_mod

        section = "- **NEXT ACTION:** open a PR for review.\n"
        assert audit_mod._handoff_next_action_count(section) == 1

    def test_bolded_label_without_colon_is_counted(self):
        from mtc_cli.commands import audit as audit_mod

        section = "**NEXT ACTION** open a PR for review.\n"
        assert audit_mod._handoff_next_action_count(section) == 1

    def test_plain_colon_label_without_bold_is_counted(self):
        from mtc_cli.commands import audit as audit_mod

        section = "NEXT ACTION: open a PR for review.\n"
        assert audit_mod._handoff_next_action_count(section) == 1

    def test_bare_prose_mention_without_label_is_not_counted(self):
        """A NEXT ACTION mention with no colon and no bold-wrap is prose, not
        a label, and must NOT satisfy the check — this is the bug the
        line-anchored regex fixes (previously a bare substring count)."""
        from mtc_cli.commands import audit as audit_mod

        section = "We are still deciding on the NEXT ACTION for this lane.\n"
        assert audit_mod._handoff_next_action_count(section) == 0

    def test_labelled_occurrence_embedded_in_a_longer_prose_line_is_counted(self):
        """A NEXT ACTION label (colon-terminated) that sits inside a longer
        prose sentence, rather than on its own bullet line, still counts —
        the label form (not the line's shape) is what makes it countable."""
        from mtc_cli.commands import audit as audit_mod

        section = (
            "Discussion continued for a while, and the NEXT ACTION: ship the fix, "
            "was agreed by everyone on the call.\n"
        )
        assert audit_mod._handoff_next_action_count(section) == 1

    def test_two_labelled_lines_count_two(self):
        from mtc_cli.commands import audit as audit_mod

        section = (
            "- **NEXT ACTION:** first item.\n"
            "- **NEXT ACTION:** second item (superseded by history; kept for the count).\n"
        )
        assert audit_mod._handoff_next_action_count(section) == 2

    def test_fixture_prose_only_mention_fails_the_audit(self, tmp_path):
        """End-to-end: an unlabelled NEXT ACTION mention must not satisfy the
        real audit's presence check (exit 2 / ERROR finding)."""
        from mtc_cli import contract
        from mtc_cli.commands import audit as audit_mod

        root = _router_era_fixture(tmp_path)
        (root / GOV_HANDOFF).write_text(
            "# Governance stage handoff\n\n"
            "## [Lead] 2026-09-07 — fixture\n\n"
            "Still deciding on the NEXT ACTION for this lane.\n"
            "- **WAITING FOR OWNER:** Nothing.\n",
            encoding="utf-8",
        )
        env = audit_mod.run(repo_root=root)
        assert env.ok is False
        assert env.exit_code() == contract.EXIT_VALIDATION
        assert env.data["handoff_next_actions"] == 0
        missing_next_action = [
            f for f in env.findings if "missing a NEXT ACTION line" in f["message"]
        ]
        assert len(missing_next_action) == 1
