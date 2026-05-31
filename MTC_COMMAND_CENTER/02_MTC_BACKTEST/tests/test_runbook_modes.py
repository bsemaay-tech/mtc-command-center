from pathlib import Path


def test_runbook_has_mode_switch_and_artifact_layout():
    runbook = Path(__file__).resolve().parents[1] / "runbook.ps1"
    text = runbook.read_text(encoding="utf-8")

    assert '[ValidateSet("optimize", "validate", "promote")]' in text
    assert "results" in text
    assert 'trials.csv' in text
    assert 'pareto.json' in text
    assert 'manifest.json' in text


def test_runbook_has_optional_determinism_gate():
    runbook = Path(__file__).resolve().parents[1] / "runbook.ps1"
    text = runbook.read_text(encoding="utf-8")

    assert "[switch]$DeterminismGate" in text
    assert "Determinism gate" in text


def test_runbook_has_artifact_guard_steps():
    runbook = Path(__file__).resolve().parents[1] / "runbook.ps1"
    text = runbook.read_text(encoding="utf-8")

    assert "scripts/artifact_guard.py" in text
    assert "--required-csv" in text


def test_runbook_exit_code_message_uses_braced_variable():
    runbook = Path(__file__).resolve().parents[1] / "runbook.ps1"
    text = runbook.read_text(encoding="utf-8")
    assert "${LASTEXITCODE}:" in text


def test_runbook_python_path_interpolation_uses_forward_slashes():
    runbook = Path(__file__).resolve().parents[1] / "runbook.ps1"
    text = runbook.read_text(encoding="utf-8")
    assert "Path(\"$($Layout.ReplaySummary -replace '\\\\','/')\")" in text


def test_runbook_embedded_python_uses_stdin_mode():
    runbook = Path(__file__).resolve().parents[1] / "runbook.ps1"
    text = runbook.read_text(encoding="utf-8")
    assert text.count("| python -") >= 4
