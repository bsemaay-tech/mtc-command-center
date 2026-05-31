from pathlib import Path


def test_phase8_docs_exist_with_required_keywords():
    root = Path(__file__).resolve().parents[1]
    required = [
        (root / "docs" / "staging_environment_mirror.md", ["staging", "ops_metrics.py"]),
        (root / "docs" / "uat_scenarios.md", ["Scenario 1", "runbook.ps1"]),
        (root / "docs" / "go_live_checklist.md", ["Rollback Plan", "On-Call"]),
        (root / "docs" / "release_semver_changelog.md", ["SemVer", "CHANGELOG.md"]),
        (root / "CHANGELOG.md", ["Unreleased"]),
    ]
    for path, words in required:
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        for w in words:
            assert w in text
