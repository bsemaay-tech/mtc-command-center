from __future__ import annotations

import unittest

from mcc_readonly.validation_reader import build_validation_terminal


def _row(**kw):
    """Build a profile_results row with sane defaults; override per test."""
    metrics = {
        "net_profit": kw.pop("net_profit", 10.0),
        "max_drawdown": kw.pop("max_drawdown", -20.0),
        "buy_hold_return": kw.pop("buy_hold_return", 5.0),
        "buy_hold_alpha": kw.pop("buy_hold_alpha", 5.0),
        "trade_count": kw.pop("trade_count", 100),
    }
    robustness = {
        "classification": kw.pop("classification", "PASS"),
        "dsr_p_value": kw.pop("dsr_p_value", 0.01),
        "dsr_robust": kw.pop("dsr_robust", True),
        "bh_fdr_survivor": kw.pop("bh_fdr_survivor", True),
        "robust_final": kw.pop("robust_final", True),
        "avg_fold_test_return_pct": kw.pop("oos", 12.0),
    }
    return {
        "strategy_id": kw.pop("strategy_id", "QL_2026_US_10M_8EMA_PULLBACK"),
        "profile": kw.pop("profile", "SOURCE_NAKED"),
        "symbol": kw.pop("symbol", "SPY"),
        "timeframe": kw.pop("timeframe", "10m"),
        "score": kw.pop("score", 1.2),
        "metrics": metrics,
        "robustness": robustness,
        "promotion_status": kw.pop("promotion_status", "RESEARCH_ONLY"),
        "source_rel_path": kw.pop("source_rel_path", "x/backtest_profile_result.json"),
    }


def _wrap(rows):
    return {"profile_results": rows}


class ValidationReaderTests(unittest.TestCase):
    def test_empty_inputs_are_safe(self) -> None:
        for arg in (None, {}, {"profile_results": None}, {"profile_results": []}):
            out = build_validation_terminal(arg)
            self.assertEqual(out["funnel"]["total_variants"], 0)
            self.assertEqual(out["survivors"], [])
            self.assertEqual(out["graveyard"], [])
            self.assertEqual(out["source_counts"]["profile_result_rows"], 0)

    def test_non_dict_rows_ignored(self) -> None:
        out = build_validation_terminal(_wrap([None, 5, "x", _row()]))
        self.assertEqual(out["funnel"]["total_variants"], 1)

    def test_survivor_path(self) -> None:
        out = build_validation_terminal(_wrap([_row()]))
        self.assertEqual(out["funnel"]["survivors"], 1)
        self.assertEqual(len(out["survivors"]), 1)
        self.assertEqual(out["graveyard"], [])
        s = out["survivors"][0]
        self.assertTrue(s["dsr_robust"])
        self.assertIn("cross_asset_consistency_score", s)

    def test_funnel_narrows_monotonically(self) -> None:
        rows = [
            _row(symbol="A"),  # full survivor
            _row(symbol="B", bh_fdr_survivor=False),  # robust but not fdr survivor
            _row(symbol="C", oos=-3.0, bh_fdr_survivor=False, robust_final=False),  # negative OOS
            _row(symbol="D", buy_hold_alpha=-2.0, bh_fdr_survivor=False, robust_final=False),  # fails B&H
        ]
        out = build_validation_terminal(_wrap(rows))
        f = out["funnel"]
        self.assertEqual(f["total_variants"], 4)
        self.assertGreaterEqual(f["completed_runs"], f["positive_oos"])
        self.assertGreaterEqual(f["positive_oos"], f["beats_buy_hold"])
        self.assertEqual(f["survivors"], 1)

    def test_primary_failure_reasons(self) -> None:
        out = build_validation_terminal(_wrap([
            _row(symbol="C", oos=-3.0, bh_fdr_survivor=False, robust_final=False),
            _row(symbol="D", buy_hold_alpha=-2.0, bh_fdr_survivor=False, robust_final=False),
            _row(symbol="E", classification="OVERFIT_SUSPECT", robust_final=False,
                 dsr_robust=False, bh_fdr_survivor=False),
        ]))
        reasons = {g["primary_failure"] for g in out["graveyard"]}
        self.assertIn("negative_oos", reasons)
        self.assertIn("did_not_beat_buy_hold", reasons)
        self.assertIn("OVERFIT_SUSPECT", reasons)
        # gauntlet aggregates the same failures
        self.assertTrue(any(g["filter"] == "negative_oos" for g in out["gauntlet"]))

    def test_cross_asset_score_buckets(self) -> None:
        rows = [_row(strategy_id="S1", symbol=s) for s in ("A", "B", "C", "D", "E", "F")]
        out = build_validation_terminal(_wrap(rows))
        # 6 distinct survivor symbols, single timeframe -> bucket 3
        self.assertEqual(out["survivors"][0]["cross_asset_consistency_score"], 3)

    def test_cross_asset_score_multi_timeframe_top_bucket(self) -> None:
        rows = [_row(strategy_id="S1", symbol=s, timeframe=tf)
                for s, tf in (("A", "10m"), ("B", "10m"), ("C", "10m"),
                              ("D", "1h"), ("E", "1h"), ("F", "1h"))]
        out = build_validation_terminal(_wrap(rows))
        self.assertEqual(out["survivors"][0]["cross_asset_consistency_score"], 4)

    def test_family_survival_rate(self) -> None:
        rows = [
            _row(strategy_id="QL_X_RSI_OVERSOLD", symbol="A"),
            _row(strategy_id="QL_X_RSI_OVERSOLD", symbol="B", bh_fdr_survivor=False),
        ]
        out = build_validation_terminal(_wrap(rows))
        fam = out["family_survival"][0]
        self.assertEqual(fam["family"], "RSI_OVERSOLD")
        self.assertEqual(fam["tested"], 2)
        self.assertEqual(fam["survivors"], 1)
        self.assertEqual(fam["survival_rate"], 0.5)

    def test_scatter_requires_both_axes(self) -> None:
        out = build_validation_terminal(_wrap([
            _row(symbol="A"),                 # has score + oos -> point
            _row(symbol="B", score=None),     # missing IS -> no point
        ]))
        self.assertEqual(len(out["is_oos_scatter"]), 1)
        self.assertEqual(out["is_oos_scatter"][0]["symbol"], "A")


if __name__ == "__main__":
    unittest.main()
