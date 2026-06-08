from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


TOOLS_ROOT = Path(__file__).resolve().parents[4] / "03_QUANTLENS" / "tools"
MODULE_PATH = TOOLS_ROOT / "build_needs_backtest_selector.py"
SPEC = importlib.util.spec_from_file_location("build_needs_backtest_selector", MODULE_PATH)
assert SPEC and SPEC.loader
selector_module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(selector_module)


class NeedsBacktestSelectorTests(unittest.TestCase):
    def test_selects_eligible_rows_without_scorecards(self) -> None:
        rows = [
            {"id": "A", "eligible_for_backtest": True, "has_deterministic_rules": True},
            {"id": "B", "eligible_for_backtest": True, "scorecard_v2": {"strategy_id": "B"}},
            {"id": "C", "eligible_for_backtest": False},
            {
                "id": "D",
                "eligible_for_backtest": True,
                "expert_quantlens_verdict": {"decision": "SALVAGE"},
            },
        ]

        selected = selector_module.select_needs_backtest(rows)

        self.assertEqual([row["strategy_id"] for row in selected], ["A"])
        self.assertEqual(selected[0]["priority_band"], "MEDIUM")


if __name__ == "__main__":
    unittest.main()
