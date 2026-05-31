from pathlib import Path


def test_runner_updates_equity_once_per_bar_with_clear_flat_branch():
    runner_file = Path(__file__).resolve().parents[1] / "src" / "engine" / "mtc_runner.py"
    text = runner_file.read_text(encoding="utf-8")

    assert "if self.state.in_position:" in text
    assert "self.state.update_equity(self.state.balance + unrealized)" in text
    assert "else:\n                self.state.update_equity(self.state.balance)" in text

    # Regression guard: do not overwrite unrealized equity immediately.
    bad_pattern = (
        "self.state.update_equity(self.state.balance + unrealized)\n"
        "                self.state.update_equity(self.state.balance)"
    )
    assert bad_pattern not in text
