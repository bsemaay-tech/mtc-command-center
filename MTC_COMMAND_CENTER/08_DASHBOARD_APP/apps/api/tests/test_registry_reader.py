from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from mcc_readonly.registry_reader import _candidate_csv_row, build_strategy_registry


SOURCE_MCC_ROOT = Path(__file__).resolve().parents[4]


class RegistryReaderTests(unittest.TestCase):
    def test_reads_candidate_csv_and_promoted_specs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "MTC_COMMAND_CENTER"
            mtc = Path(tmp) / "mtc"
            lab = mtc / "06_QUANTLENS_LAB"
            registry = lab / "_registry"
            backtests = lab / "05_BACKTEST_RESULTS"
            promoted = lab / "06_PROMOTED_TO_PARITY" / "QL_ALPHA"
            (root / "00_CONFIG").mkdir(parents=True)
            registry.mkdir(parents=True)
            backtests.mkdir(parents=True)
            promoted.mkdir(parents=True)
            candidate_folder = lab / "01_TRIAGED_CANDIDATES" / "QL_ONE"
            candidate_folder.mkdir(parents=True)
            _write_paths(root, mtc)
            (registry / "quantlens_candidate_registry.csv").write_text(
                "\n".join(
                    [
                        "candidate_id,status,title,source_url,market_type,timeframe,candidate_kind,commercial_value_score,complexity_score,repaint_risk,lookahead_risk,closed_source_risk,mtc_overlap,next_action,candidate_folder,created_at,updated_at",
                        "QL_ONE,PROTOTYPED,One,,CRYPTO,1h,entry|exit,7,3,LOW,LOW,LOW,overlap,next,06_QUANTLENS_LAB/01_TRIAGED_CANDIDATES/QL_ONE,2026-05-01,2026-05-30",
                    ]
                ),
                encoding="utf-8",
            )
            (candidate_folder / "00_raw_quantlens_report.md").write_text(
                "# Candidate\n"
                "Source URL: https://youtu.be/example123\n",
                encoding="utf-8",
            )
            _write_json(backtests / "QL_ONE_results.json", {"summary": {}})
            _write_json(
                promoted / "producer_spec.json",
                {
                    "candidate_id": "QL_ALPHA",
                    "engine_strategy_id": "QL_ONE",
                    "strategy_family": "Family",
                    "symbol": "BTCUSDT",
                    "timeframe": "1h",
                    "promotion_status": ["PROMOTE_TO_PARITY_CANDIDATE"],
                    "metrics_lockbox": {"return_pct_compound": 10.0, "profit_factor": 1.2, "trades": 5},
                },
            )

            registry_payload = build_strategy_registry(root)
            self.assertEqual(len(registry_payload["candidates"]), 1)
            self.assertEqual(len(registry_payload["strategies"]), 1)
            self.assertEqual(registry_payload["candidates"][0]["evidence_level"], "backtested")
            self.assertEqual(registry_payload["candidates"][0]["source_url"], "https://youtu.be/example123")
            self.assertEqual(registry_payload["strategies"][0]["evidence_level"], "promoted_to_parity")

    def test_real_config_returns_registry_shape(self) -> None:
        registry = build_strategy_registry(SOURCE_MCC_ROOT)
        self.assertIn("candidates", registry)
        self.assertIn("strategies", registry)
        self.assertGreaterEqual(len(registry["candidates"]), 0)

    def test_csv_row_repair_mismatched_column_count_is_rejected(self) -> None:
        # A header that has grown beyond the 12-leading/4-trailing shape the
        # repair path assumes (schema drift). The repair always produces
        # exactly 17 columns, so it can never satisfy this 20-column header.
        header = [
            "candidate_id", "status", "title", "source_url", "market_type", "timeframe",
            "candidate_kind", "commercial_value_score", "complexity_score", "repaint_risk",
            "lookahead_risk", "closed_source_risk", "mtc_overlap", "next_action",
            "candidate_folder", "created_at", "updated_at", "reviewer", "review_notes", "flagged",
        ]
        # 21 raw fields: an unquoted comma inside mtc_overlap split it into two
        # pieces, so this row has more fields than the 20-column header.
        fields = [
            "QL_BAD", "PROTOTYPED", "Bad", "", "CRYPTO", "1h", "entry|exit", "5", "2",
            "LOW", "LOW", "LOW", "oops", " unquoted comma here", "next", "folder",
            "2026-05-01", "2026-05-30", "alice", "ok", "false",
        ]
        self.assertGreater(len(fields), len(header))
        self.assertIsNone(_candidate_csv_row(header, fields))

    def test_reads_candidate_csv_skips_row_whose_repair_does_not_match_header(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "MTC_COMMAND_CENTER"
            mtc = Path(tmp) / "mtc"
            lab = mtc / "06_QUANTLENS_LAB"
            registry = lab / "_registry"
            (root / "00_CONFIG").mkdir(parents=True)
            registry.mkdir(parents=True)
            _write_paths(root, mtc)
            header_line = (
                "candidate_id,status,title,source_url,market_type,timeframe,candidate_kind,"
                "commercial_value_score,complexity_score,repaint_risk,lookahead_risk,"
                "closed_source_risk,mtc_overlap,next_action,candidate_folder,created_at,"
                "updated_at,reviewer,review_notes,flagged"
            )
            good_row = (
                "QL_GOOD,PROTOTYPED,Good,,CRYPTO,1h,entry|exit,7,3,LOW,LOW,LOW,overlap,next,"
                "06_QUANTLENS_LAB/01_TRIAGED_CANDIDATES/QL_GOOD,2026-05-01,2026-05-30,"
                "bob,fine,true"
            )
            # Unquoted comma inside mtc_overlap pushes this row to 21 raw
            # fields against a 20-column header; the fixed 12+1+4 repair
            # always yields 17, which can never match 20.
            bad_row = (
                "QL_BAD,PROTOTYPED,Bad,,CRYPTO,1h,entry|exit,5,2,LOW,LOW,LOW,"
                "oops, unquoted comma here,next,folder,2026-05-01,2026-05-30,"
                "alice,ok,false"
            )
            (registry / "quantlens_candidate_registry.csv").write_text(
                "\n".join([header_line, good_row, bad_row]),
                encoding="utf-8",
            )

            registry_payload = build_strategy_registry(root)
            candidate_ids = [c["candidate_id"] for c in registry_payload["candidates"]]
            self.assertEqual(candidate_ids, ["QL_GOOD"])
            self.assertNotIn("QL_BAD", candidate_ids)
            # The malformed row's reviewer name must never leak into another
            # candidate's field (e.g. misaligned into candidate_folder).
            for candidate in registry_payload["candidates"]:
                self.assertNotIn("alice", candidate.values())

    def test_reads_candidate_csv_row_that_repairs_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "MTC_COMMAND_CENTER"
            mtc = Path(tmp) / "mtc"
            lab = mtc / "06_QUANTLENS_LAB"
            registry = lab / "_registry"
            (root / "00_CONFIG").mkdir(parents=True)
            registry.mkdir(parents=True)
            _write_paths(root, mtc)
            header_line = (
                "candidate_id,status,title,source_url,market_type,timeframe,candidate_kind,"
                "commercial_value_score,complexity_score,repaint_risk,lookahead_risk,"
                "closed_source_risk,mtc_overlap,next_action,candidate_folder,created_at,updated_at"
            )
            # Unquoted comma inside mtc_overlap makes this an 18-field row
            # against a 17-column header - the repairable case the 12+1+4
            # split exists for.
            repairable_row = (
                "QL_REPAIR,PROTOTYPED,Repair,,CRYPTO,1h,entry|exit,7,3,LOW,LOW,LOW,"
                "overlaps, with mtc,next-step,"
                "06_QUANTLENS_LAB/01_TRIAGED_CANDIDATES/QL_REPAIR,2026-05-01,2026-05-30"
            )
            (registry / "quantlens_candidate_registry.csv").write_text(
                "\n".join([header_line, repairable_row]),
                encoding="utf-8",
            )

            registry_payload = build_strategy_registry(root)
            self.assertEqual(len(registry_payload["candidates"]), 1)
            candidate = registry_payload["candidates"][0]
            self.assertEqual(candidate["candidate_id"], "QL_REPAIR")
            self.assertEqual(candidate["notes"], "next-step")


def _write_paths(root: Path, mtc: Path) -> None:
    shutil.copytree(SOURCE_MCC_ROOT / "06_SCHEMAS", root / "06_SCHEMAS")
    (root / "00_CONFIG" / "paths.example.json").write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "mcc_root": str(root),
                "mtc_v2_root": str(mtc),
                "mtc_v2_python_exe": None,
                "pinets_root": str(mtc / "05_PARITY"),
                "tradingview_exports_dir": None,
                "reports_root": str(root / "04_REPORTS"),
            }
        ),
        encoding="utf-8",
    )


def _write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
