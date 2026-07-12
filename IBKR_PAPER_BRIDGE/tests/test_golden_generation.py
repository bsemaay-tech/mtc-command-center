from __future__ import annotations

import json
from pathlib import Path

from bridge.engine.strategies.keltner_trail_ema8 import KeltnerTrailEma8
from tools.generate_golden import generate_golden_from_csv


def test_golden_file_is_provisional_and_matches_reference():
    fixture = Path(__file__).parent / "fixtures" / "BTC_1h.csv"
    golden_path = Path(__file__).parent / "fixtures" / "golden_signals.json"

    generated = generate_golden_from_csv(fixture)
    saved = json.loads(golden_path.read_text(encoding="utf-8"))

    assert saved["provisional"] is True
    assert saved["source"] == "synthetic_fixture_reference_keltner"
    assert saved["signals"] == generated["signals"]
    assert KeltnerTrailEma8().warmup_bars == 20
