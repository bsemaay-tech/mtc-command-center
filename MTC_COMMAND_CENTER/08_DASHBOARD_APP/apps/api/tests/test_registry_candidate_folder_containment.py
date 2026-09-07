from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from mcc_readonly.registry_reader import build_strategy_registry

HEADER = (
    "candidate_id,status,title,source_url,market_type,timeframe,candidate_kind,"
    "commercial_value_score,complexity_score,repaint_risk,lookahead_risk,closed_source_risk,"
    "mtc_overlap,next_action,candidate_folder,created_at,updated_at"
)


def _registry_with_folder(tmp: Path, candidate_folder: str) -> Path:
    root = tmp / "MTC_COMMAND_CENTER"
    lab = root / "03_QUANTLENS"
    registry = lab / "_registry"
    registry.mkdir(parents=True)
    (root / "00_CONFIG").mkdir(parents=True)
    (root / "00_CONFIG" / "paths.local.json").write_text(
        json.dumps({"mtc_v2_root": str(tmp / "mtc")}), encoding="utf-8"
    )
    row = (
        f"QL_X,PROTOTYPED,X,,CRYPTO,1h,entry|exit,7,3,LOW,LOW,LOW,overlap,next,"
        f"{candidate_folder},2026-05-01,2026-05-30"
    )
    (registry / "quantlens_candidate_registry.csv").write_text(
        HEADER + "\n" + row + "\n", encoding="utf-8"
    )
    return root


def _url_file(folder: Path, video_id: str) -> None:
    folder.mkdir(parents=True)
    (folder / "00_raw.md").write_text(f"Source URL: https://youtu.be/{video_id}\n", encoding="utf-8")


class CandidateFolderContainmentTests(unittest.TestCase):
    """Gate-5 finding F1 (claude-opus-5, 2026-09-07): a registry CSV `candidate_folder`
    value must never resolve outside the canonical QuantLens root."""

    def test_sibling_tree_under_mcc_root_is_not_read(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = _registry_with_folder(Path(tmp), "06_QUANTLENS_LAB/01_TRIAGED_CANDIDATES/QL_X")
            _url_file(root / "06_QUANTLENS_LAB" / "01_TRIAGED_CANDIDATES" / "QL_X", "legacy123")
            payload = build_strategy_registry(root)
            self.assertEqual(payload["candidates"][0]["source_url"], "")

    def test_parent_traversal_is_not_read(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = _registry_with_folder(Path(tmp), "../OUTSIDE/QL_X")
            _url_file(root / "OUTSIDE" / "QL_X", "outside456")
            payload = build_strategy_registry(root)
            self.assertEqual(payload["candidates"][0]["source_url"], "")

    def test_absolute_path_is_not_read(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            outside = Path(tmp) / "ELSEWHERE" / "QL_X"
            root = _registry_with_folder(Path(tmp), str(outside))
            _url_file(outside, "absolute789")
            payload = build_strategy_registry(root)
            self.assertEqual(payload["candidates"][0]["source_url"], "")

    def test_in_root_folder_is_still_read(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = _registry_with_folder(Path(tmp), "01_TRIAGED_CANDIDATES/QL_X")
            _url_file(root / "03_QUANTLENS" / "01_TRIAGED_CANDIDATES" / "QL_X", "inside789")
            payload = build_strategy_registry(root)
            self.assertIn("inside789", payload["candidates"][0]["source_url"])


if __name__ == "__main__":
    unittest.main()
