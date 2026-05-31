from pathlib import Path


def test_app_has_clean_navigation_labels_and_no_stale_not_implemented_block():
    app = Path(__file__).resolve().parents[1] / "app.py"
    text = app.read_text(encoding="utf-8")

    assert '["Home", "Data Download", "Backtest", "Optimize", "Reports"]' in text
    assert "**Not Implemented in Python engine:**" not in text


def test_app_and_components_have_no_common_mojibake_sequences():
    files = [
        Path(__file__).resolve().parents[1] / "app.py",
        Path(__file__).resolve().parents[1] / "utils" / "components.py",
    ]
    bad_tokens = ["ğŸ", "âœ", "âš", "â", "â„", "â", "ï¸"]
    for fp in files:
        text = fp.read_text(encoding="utf-8")
        for token in bad_tokens:
            assert token not in text


def test_backtest_and_optimize_have_step_flow_labels():
    app = Path(__file__).resolve().parents[1] / "app.py"
    text = app.read_text(encoding="utf-8")

    assert text.count('st.caption("Step 1: Setup")') >= 2
    assert text.count('st.caption("Step 2: Run")') >= 2
    assert text.count('st.caption("Step 3: Results")') >= 2
    assert 'st.subheader("Advanced Settings")' in text
