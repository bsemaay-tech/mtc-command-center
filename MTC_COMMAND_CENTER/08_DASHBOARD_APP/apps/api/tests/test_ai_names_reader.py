from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from mcc_readonly.ai_names_reader import (
    attach_ai_strategy_names_to_rows,
    attach_ai_strategy_names_to_scorecards,
    build_ai_strategy_names,
)


class AiNamesReaderTests(unittest.TestCase):
    def test_reads_and_attaches_strategy_display_names(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry_dir = root / "05_REGISTRY"
            registry_dir.mkdir(parents=True)
            (registry_dir / "AI_STRATEGY_NAME_REGISTRY.json").write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "entries": [
                            {
                                "strategy_id": "QL_TEST_STRATEGY",
                                "strategy_display_name": "Test Pullback Strategy",
                                "source": "unit_test",
                                "rationale": "Test fixture.",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            names = build_ai_strategy_names(root)
            rows = attach_ai_strategy_names_to_rows([{"id": "QL_TEST_STRATEGY"}], names)
            scorecards = attach_ai_strategy_names_to_scorecards(
                {
                    "cards": [{"base_strategy_id": "QL_TEST_STRATEGY"}],
                    "by_strategy": {
                        "QL_TEST_STRATEGY": {
                            "display_card": {"base_strategy_id": "QL_TEST_STRATEGY"},
                            "cards": [{"base_strategy_id": "QL_TEST_STRATEGY"}],
                        }
                    },
                },
                names,
            )

            self.assertEqual(names["count"], 1)
            self.assertEqual(rows[0]["strategy_display_name"], "Test Pullback Strategy")
            self.assertEqual(scorecards["cards"][0]["strategy_display_name"], "Test Pullback Strategy")
            self.assertEqual(
                scorecards["by_strategy"]["QL_TEST_STRATEGY"]["display_card"]["strategy_display_name"],
                "Test Pullback Strategy",
            )


if __name__ == "__main__":
    unittest.main()
