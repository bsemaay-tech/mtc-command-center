from pathlib import Path


def test_reports_page_has_run_history_compare_and_artifact_viewer():
    text = Path("mtc_backtest/app.py").read_text(encoding="utf-8")
    assert "Optimizer Run History" in text
    assert "Compare Runs" in text
    assert "Artifact Viewer" in text
    assert "from src.ui.run_history import" in text


def test_backtest_ui_no_longer_marks_filter_block_and_eod_eow_unimplemented():
    text = Path("mtc_backtest/app.py").read_text(encoding="utf-8")
    assert "Not Implemented: Filter block exit engine logic" not in text
    assert "EOD/EOW time stop: Not Implemented in Python" not in text
