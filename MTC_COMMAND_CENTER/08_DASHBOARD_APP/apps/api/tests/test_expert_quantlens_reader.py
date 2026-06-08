from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from mcc_readonly.expert_quantlens_reader import (
    attach_expert_quantlens_to_rows,
    attach_expert_quantlens_to_scorecards,
    build_expert_quantlens,
)


class ExpertQuantlensReaderTests(unittest.TestCase):
    def test_reads_and_attaches_expert_verdicts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry_dir = root / "05_REGISTRY"
            registry_dir.mkdir(parents=True)
            (registry_dir / "AI_QUANTLENS_VERDICT_REGISTRY.json").write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "entries": [
                            {
                                "strategy_id": "QL_TEST_STRATEGY",
                                "decision": "RESEARCH_ONLY",
                                "decision_label": "Research only",
                                "reason": "Scorecard evidence is incomplete.",
                                "score_reference": "Gate2 incomplete.",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            verdicts = build_expert_quantlens(root)
            rows = attach_expert_quantlens_to_rows([{"id": "QL_TEST_STRATEGY"}], verdicts)
            scorecards = attach_expert_quantlens_to_scorecards(
                {
                    "cards": [{"base_strategy_id": "QL_TEST_STRATEGY"}],
                    "by_strategy": {
                        "QL_TEST_STRATEGY": {
                            "display_card": {"base_strategy_id": "QL_TEST_STRATEGY"},
                            "cards": [{"base_strategy_id": "QL_TEST_STRATEGY"}],
                        }
                    },
                },
                verdicts,
            )

            self.assertEqual(verdicts["count"], 1)
            self.assertEqual(rows[0]["expert_quantlens_verdict"]["decision"], "RESEARCH_ONLY")
            self.assertEqual(scorecards["cards"][0]["expert_quantlens_verdict"]["decision_label"], "Research only")
            self.assertEqual(
                scorecards["by_strategy"]["QL_TEST_STRATEGY"]["display_card"]["expert_quantlens_verdict"]["reason"],
                "Scorecard evidence is incomplete.",
            )


if __name__ == "__main__":
    unittest.main()
