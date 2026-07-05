from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from mcc_readonly.param_specs_reader import build_param_specs


def _write_registry(root: Path, payload) -> None:
    reg = root / "05_REGISTRY"
    reg.mkdir(parents=True, exist_ok=True)
    (reg / "STRATEGY_PARAM_SPECS.json").write_text(json.dumps(payload), encoding="utf-8")


class TestParamSpecsReader(unittest.TestCase):
    def test_valid_registry(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _write_registry(root, {
                "generated_utc": "2026-07-01T00:00:00Z",
                "universe": {"symbols": 51, "timeframes": 7, "cells": 357},
                "execution_model": {"profit_target_R": 2.0, "rolling_folds": 3},
                "library_totals": {"strategies": 2, "sum_grid_size": 68, "total_cases_full_universe": 72828},
                "strategies": [
                    {
                        "strategy_id": "GEN_DONCHIAN_BREAKOUT",
                        "grid_size": 60,
                        "optimizable": {"channel_len": {"values": [10, 20], "count": 2, "type": "int"}},
                        "cases_full_universe": 64260,
                        "annotation_status": "documented",
                        "fixed_knobs": [{"name": "atr_period", "value": 14, "reason": "hardcoded"}],
                        "missing_knobs": [{"name": "short_side", "phase": "3-RnD"}],
                    },
                    {"strategy_id": "GEN_TRIPLE_EMA_STACK", "grid_size": 8},
                ],
            })
            out = build_param_specs(root)
            self.assertTrue(out["available"])
            self.assertEqual(out["count"], 2)
            self.assertEqual(out["universe"]["cells"], 357)
            self.assertEqual(out["execution_model"]["profit_target_R"], 2.0)
            don = out["by_id"]["GEN_DONCHIAN_BREAKOUT"]
            self.assertEqual(don["grid_size"], 60)
            self.assertEqual(don["cases_full_universe"], 64260)
            self.assertEqual(don["fixed_knobs"][0]["name"], "atr_period")
            self.assertEqual(don["missing_knobs"][0]["phase"], "3-RnD")

    def test_skips_entries_without_id(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _write_registry(root, {"strategies": [{"strategy_id": "ok", "grid_size": 1}, {"grid_size": 2}, "junk"]})
            out = build_param_specs(root)
            self.assertEqual(out["count"], 1)
            self.assertEqual(out["strategies"][0]["strategy_id"], "ok")

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as d:
            out = build_param_specs(Path(d))
            self.assertFalse(out["available"])
            self.assertEqual(out["reason"], "registry_not_found")
            self.assertEqual(out["strategies"], [])

    def test_malformed_json(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            reg = root / "05_REGISTRY"
            reg.mkdir(parents=True)
            (reg / "STRATEGY_PARAM_SPECS.json").write_text("{ not json", encoding="utf-8")
            out = build_param_specs(root)
            self.assertFalse(out["available"])
            self.assertTrue(out["reason"].startswith("json_error"))


if __name__ == "__main__":
    unittest.main()
