from pathlib import Path


def test_contract_contains_non_production_guardrails():
    text = Path("candidate_contract.yml").read_text(encoding="utf-8")
    assert "NOT_PRODUCTION" in text
    assert "must_not_be_invented" in text
    assert "No claim that this is profitable" in text


def test_required_files_exist():
    for name in [
        "candidate_contract.yml",
        "candidate_rules.md",
        "python_signal_model.py",
        "mtc_compatible_risk_adapter.py",
        "standalone_pine_visual_review.pine",
    ]:
        assert Path(name).exists(), name
