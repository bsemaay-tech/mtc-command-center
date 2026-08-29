"""Regression tests for producer-spec promotion-status generation."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "generate_producer_specs.py"
SPEC = importlib.util.spec_from_file_location("generate_producer_specs", MODULE_PATH)
assert SPEC and SPEC.loader
generator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(generator)


class ProducerSpecPromotionTests(unittest.TestCase):
    def test_pass_classification_returns_empty_admission_set(self) -> None:
        self.assertEqual(generator.promotion_status("PASS", True), [])

    def test_classification_and_data_presence_never_mint_promotion_tokens(self) -> None:
        promotion_like = {
            "PROMOTE_TO_SANDBOX",
            "PROMOTE_TO_FORWARD_PAPER_TRADE",
            "MTC_ENGINE_VALIDATED",
            "PROMOTE_TO_PARITY_CANDIDATE",
            "APPROVED_FOR_MTC_V2_INTEGRATION",
            "FORWARD_PAPER_CANDIDATE",
            "ROBUST_CANDIDATE",
        }
        cases = [
            ("PASS", True),
            ("STRONG_PASS", True),
            ("FORWARD_PAPER", True),
            ("PASS", False),
            ("SKIPPED_RULE", True),
            (None, False),
        ]

        for classification, is_real in cases:
            with self.subTest(classification=classification, is_real=is_real):
                status = generator.promotion_status(classification, is_real)
                self.assertEqual(status, [])
                self.assertTrue(set(status).isdisjoint(promotion_like))


if __name__ == "__main__":
    unittest.main()
