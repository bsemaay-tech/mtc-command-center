from pathlib import Path


def test_runbook_uses_psscriptroot_and_no_hardcoded_repo_prefix():
    runbook = Path(__file__).resolve().parents[1] / "runbook.ps1"
    text = runbook.read_text(encoding="utf-8")

    assert "$PSScriptRoot" in text
    assert "mtc_backtest\\configs\\cases\\" not in text


def test_runbook_replay_uses_resolved_case_paths():
    runbook = Path(__file__).resolve().parents[1] / "runbook.ps1"
    text = runbook.read_text(encoding="utf-8")

    assert "Resolve-CasePath" in text
    assert "--case `\"$case1`\"" in text
    assert "--case `\"$case2`\"" in text
