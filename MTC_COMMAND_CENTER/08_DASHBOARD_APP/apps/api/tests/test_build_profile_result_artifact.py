from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from mcc_readonly.night_artifacts_reader import build_night_artifacts
from mcc_readonly.schema import validate_json_schema

MCC_ROOT = Path(__file__).resolve().parents[4]
MODULE_PATH = MCC_ROOT / "03_QUANTLENS" / "tools" / "build_profile_result_artifact.py"
SCHEMA_DIR = MCC_ROOT / "06_SCHEMAS"

SPEC = importlib.util.spec_from_file_location("build_profile_result_artifact", MODULE_PATH)
assert SPEC and SPEC.loader
bpra = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bpra)

STRATEGY = "QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK"


def _mega_source(with_metrics: bool = True) -> dict:
    row = {
        "strategy": STRATEGY,
        "symbol": "XRPUSDT",
        "timeframe": "4h",
        "classification": "PASS",
        "data_start": "2020-01-06 08:00:00+00:00",
        "data_end": "2026-04-27 12:00:00+00:00",
        "dsr_p_value": 0.0069,
        "dsr_robust": False,
        "bh_fdr_survivor": False,
        "robust_final": False,
        "summary": {
            "best_params": {"pullback_atr": 0.4, "impulse_atr": 1.0, "slope_window": 5},
            "n_folds": 3,
            "folds_positive": 2,
            "avg_fold_test_return_pct": 1.2,
        },
    }
    if with_metrics:
        row["summary"]["lockbox_oos"] = {
            "num_trades": 108, "win_rate": 0.3519, "net_return_pct": 40.407,
            "max_drawdown_pct": -30.808, "profit_factor": 1.358, "sharpe": 1.1282,
        }
    return {"generated_utc": "2026-06-01T03:02:14+00:00", "config": {"cost_bps": 8.0, "num_rolling_folds": 3}, "results": [row]}


def _write_source(tmp: Path, doc: dict) -> Path:
    p = tmp / "MEGA_results_iter_test_results.json"
    p.write_text(json.dumps(doc), encoding="utf-8")
    return p


def _schema() -> dict:
    return json.loads((SCHEMA_DIR / "backtest_profile_result.schema.json").read_text(encoding="utf-8"))


class BuildProfileResultTests(unittest.TestCase):
    def test_default_without_apply_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            src = _write_source(tmp, _mega_source())
            old_root = bpra.BACKTEST_ROOT
            try:
                bpra.BACKTEST_ROOT = tmp / "05_BACKTEST_RESULTS"
                out = bpra.BACKTEST_ROOT / "profile_default_no_write"
                rc = bpra.main(["--strategy-id", STRATEGY, "--source-path", str(src),
                                "--output-dir", str(out)])
                self.assertEqual(rc, 0)
                self.assertFalse((out / "backtest_profile_result.json").exists())
            finally:
                bpra.BACKTEST_ROOT = old_root

    def test_dry_run_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            src = _write_source(tmp, _mega_source())
            old_root = bpra.BACKTEST_ROOT
            try:
                bpra.BACKTEST_ROOT = tmp / "05_BACKTEST_RESULTS"
                out = bpra.BACKTEST_ROOT / "profile_dry_run"
                rc = bpra.main(["--strategy-id", STRATEGY, "--source-path", str(src),
                                "--output-dir", str(out), "--dry-run", "--apply"])
                self.assertEqual(rc, 0)
                self.assertFalse((out / "backtest_profile_result.json").exists())
            finally:
                bpra.BACKTEST_ROOT = old_root

    def test_apply_writes_inside_backtest_results(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            src = _write_source(tmp, _mega_source())
            old_root = bpra.BACKTEST_ROOT
            try:
                bpra.BACKTEST_ROOT = tmp / "05_BACKTEST_RESULTS"
                out = bpra.BACKTEST_ROOT / "profile_apply"
                rc = bpra.main(["--strategy-id", STRATEGY, "--source-path", str(src),
                                "--output-dir", str(out), "--apply"])
                self.assertEqual(rc, 0)
                self.assertTrue((out / "backtest_profile_result.json").exists())
            finally:
                bpra.BACKTEST_ROOT = old_root

    def test_refuses_existing_output_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            src = _write_source(tmp, _mega_source())
            old_root = bpra.BACKTEST_ROOT
            try:
                bpra.BACKTEST_ROOT = tmp / "05_BACKTEST_RESULTS"
                out = bpra.BACKTEST_ROOT / "profile_existing"
                out.mkdir(parents=True)
                target = out / "backtest_profile_result.json"
                target.write_text("KEEP", encoding="utf-8")
                rc = bpra.main(["--strategy-id", STRATEGY, "--source-path", str(src),
                                "--output-dir", str(out), "--apply"])
                self.assertEqual(rc, 5)
                self.assertEqual(target.read_text(encoding="utf-8"), "KEEP")
            finally:
                bpra.BACKTEST_ROOT = old_root

    def test_force_allows_existing_output_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            src = _write_source(tmp, _mega_source())
            old_root = bpra.BACKTEST_ROOT
            try:
                bpra.BACKTEST_ROOT = tmp / "05_BACKTEST_RESULTS"
                out = bpra.BACKTEST_ROOT / "profile_existing_force"
                out.mkdir(parents=True)
                target = out / "backtest_profile_result.json"
                target.write_text("OLD", encoding="utf-8")
                rc = bpra.main(["--strategy-id", STRATEGY, "--source-path", str(src),
                                "--output-dir", str(out), "--apply", "--force"])
                self.assertEqual(rc, 0)
                self.assertNotEqual(target.read_text(encoding="utf-8"), "OLD")
            finally:
                bpra.BACKTEST_ROOT = old_root

    def test_refuses_output_dir_outside_backtest_results(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            src = _write_source(tmp, _mega_source())
            old_root = bpra.BACKTEST_ROOT
            try:
                bpra.BACKTEST_ROOT = tmp / "05_BACKTEST_RESULTS"
                out = tmp / "outside"
                rc = bpra.main(["--strategy-id", STRATEGY, "--source-path", str(src),
                                "--output-dir", str(out), "--apply"])
                self.assertEqual(rc, 5)
                self.assertFalse((out / "backtest_profile_result.json").exists())
            finally:
                bpra.BACKTEST_ROOT = old_root

    def test_refuses_insufficient_source(self) -> None:
        # rows present but no lockbox_oos -> must refuse, not emit fake/empty artifact.
        with tempfile.TemporaryDirectory() as t:
            src = _write_source(Path(t), _mega_source(with_metrics=False))
            rc = bpra.main(["--strategy-id", STRATEGY, "--source-path", str(src),
                            "--output-dir", str(Path(t) / "out")])
            self.assertEqual(rc, 4)
            self.assertFalse((Path(t) / "out" / "backtest_profile_result.json").exists())

    def test_refuses_unknown_strategy(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            src = _write_source(Path(t), _mega_source())
            rc = bpra.main(["--strategy-id", "QL_NOT_IN_SOURCE", "--source-path", str(src)])
            self.assertEqual(rc, 4)

    def test_output_is_schema_valid(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            src = _write_source(Path(t), _mega_source())
            doc, _ = bpra.build_document(src, STRATEGY, "SOURCE_NAKED", "run_x", "PASS", None, None, 10)
            self.assertEqual(validate_json_schema(doc, _schema()), [])

    def test_provenance_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            src = _write_source(Path(t), _mega_source())
            doc, _ = bpra.build_document(src, STRATEGY, "SOURCE_NAKED", "run_x", "PASS", None, None, 10)
            self.assertIn("provenance", doc)
            self.assertEqual(doc["provenance"]["source_type"], "deterministic_soak_mega_results")
            self.assertTrue(doc["conversion_timestamp"])
            row = doc["results"][0]
            self.assertEqual(row["provenance"]["source_type"], "deterministic_soak_mega_results")
            # universe mismatch must be surfaced, not hidden
            self.assertIsNotNone(row["provenance"]["universe_mismatch"])

    def test_no_fake_kpis_when_absent(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            src = _write_source(Path(t), _mega_source())
            doc, _ = bpra.build_document(src, STRATEGY, "SOURCE_NAKED", "run_x", "PASS", None, None, 10)
            m = doc["results"][0]["metrics"]
            # present in source -> copied:
            self.assertEqual(m["net_profit"], 40.407)
            self.assertEqual(m["trade_count"], 108)
            # absent in source -> explicit null, never invented:
            for absent in ("sortino", "exposure", "avg_trade", "buy_hold_return", "buy_hold_alpha", "max_loss_streak"):
                self.assertIsNone(m[absent])

    def test_non_robust_not_promoted(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            src = _write_source(Path(t), _mega_source())
            doc, _ = bpra.build_document(src, STRATEGY, "SOURCE_NAKED", "run_x", "PASS", None, None, 10)
            self.assertEqual(doc["results"][0]["promotion_status"], "RESEARCH_ONLY")

    def test_reader_discovers_and_populates_official_bucket(self) -> None:
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            src = _write_source(tmp, _mega_source())
            doc, _ = bpra.build_document(src, STRATEGY, "SOURCE_NAKED", "run_x", "PASS", None, None, 10)
            # write into a temp MCC root the reader can scan
            root = root_with_schemas(tmp)
            run_dir = root / "03_QUANTLENS" / "05_BACKTEST_RESULTS" / "pilot_test"
            run_dir.mkdir(parents=True, exist_ok=True)
            (run_dir / "backtest_profile_result.json").write_text(json.dumps(doc), encoding="utf-8")
            model = build_night_artifacts(root)
            self.assertGreater(model["summary"]["profile_result_rows"], 0)
            self.assertTrue(model["summary"]["has_profile_separated_results"])
            rows = model["profile_results"]
            self.assertTrue(all(r["profile"] in ("SOURCE_NAKED", "RISK_NORMALIZED", "MTC_LIGHT", "FULL_MTC_CANDIDATE") for r in rows))
            self.assertEqual(rows[0]["strategy_id"], STRATEGY)

    def test_reader_passes_through_badge_data(self) -> None:
        # The UI hardening badges need provenance + profile_mapping + robustness in the
        # snapshot rows. Confirm the reader forwards them (not just metrics).
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            src = _write_source(tmp, _mega_source())
            doc, _ = bpra.build_document(src, STRATEGY, "SOURCE_NAKED", "run_x", "PASS", None, None, 10)
            root = root_with_schemas(tmp)
            run_dir = root / "03_QUANTLENS" / "05_BACKTEST_RESULTS" / "pilot_test"
            run_dir.mkdir(parents=True, exist_ok=True)
            (run_dir / "backtest_profile_result.json").write_text(json.dumps(doc), encoding="utf-8")
            row = build_night_artifacts(root)["profile_results"][0]
            # research-only signal
            self.assertEqual(row["promotion_status"], "RESEARCH_ONLY")
            # non-robust signal
            self.assertIsInstance(row["robustness"], dict)
            self.assertIs(row["robustness"]["robust_final"], False)
            # universe mismatch signal (truthy string)
            self.assertTrue(row["provenance"]["universe_mismatch"])
            # profile mapping interpreted signal
            self.assertTrue(row["profile_mapping"]["is_interpretation"])


def root_with_schemas(tmp: Path) -> Path:
    root = tmp / "MTC_COMMAND_CENTER"
    (root / "00_CONFIG").mkdir(parents=True, exist_ok=True)
    shutil.copytree(MCC_ROOT / "06_SCHEMAS", root / "06_SCHEMAS")
    return root


if __name__ == "__main__":
    unittest.main()
