from __future__ import annotations

import json
import re
from pathlib import Path

from bridge.engine.strategies.keltner_trail_ema8 import KeltnerTrailEma8

FIXTURES = Path(__file__).parent / "fixtures"
YAML_PATH = Path(__file__).parents[1] / "config" / "strategies" / "keltner_trail_ema8.yaml"


def test_golden_is_real_and_synced_with_strategy_yaml():
    golden = json.loads((FIXTURES / "golden_signals.json").read_text(encoding="utf-8"))

    # Real QuantLens golden, never the provisional synthetic reference.
    assert golden["provisional"] is False
    assert golden["source"] == "quantlens_mega_walk_forward_registry"
    assert golden["strategy_id"] == "keltner_trail_ema8"
    assert golden["bar_alignment"] == "UTC_1h_24x7_close_confirmed_mkt_next"
    assert golden["dataset"]["symbol"] == "BTCUSD"
    assert golden["dataset"]["timeframe"] == "1h"
    assert golden["signal_count"] == len(golden["signals"]) > 0

    # golden_run_id in the strategy YAML must match the golden file exactly.
    yaml_text = YAML_PATH.read_text(encoding="utf-8")
    match = re.search(r'^golden_run_id: "([^"]+)"$', yaml_text, flags=re.MULTILINE)
    assert match is not None
    assert match.group(1) == golden["golden_run_id"]
    assert "PROVISIONAL" not in golden["golden_run_id"]

    # Golden params must pin the exact bridge strategy parameters.
    strategy = KeltnerTrailEma8()
    assert golden["params"] == {
        "kc_length": strategy.kc_length,
        "kc_mult": strategy.kc_mult,
        "atr_length": strategy.atr_length,
        "trail_ema": strategy.trail_ema,
    }
    assert strategy.warmup_bars == 20

    # Every signal row is well-formed runtime output (Z timestamps, both sides).
    directions = set()
    for sig in golden["signals"]:
        assert sig["ts"].endswith("Z")
        assert sig["direction"] in {"LONG", "SHORT"}
        assert sig["reason"] in {"close above keltner", "close below keltner"}
        assert sig["ref_price"] > 0
        directions.add(sig["direction"])
    assert directions == {"LONG", "SHORT"}


def test_golden_fixture_bars_cover_all_signals():
    golden = json.loads((FIXTURES / "golden_signals.json").read_text(encoding="utf-8"))
    header, first, *_, last = (
        (FIXTURES / "BTC_1h_real.csv").read_text(encoding="utf-8").splitlines()
    )
    assert header == "ts,open,high,low,close,volume"
    first_ts = first.split(",")[0].replace("+00:00", "Z")
    last_ts = last.split(",")[0].replace("+00:00", "Z")
    assert first_ts == golden["dataset"]["start"].replace("+00:00", "Z")
    assert last_ts == golden["dataset"]["end"].replace("+00:00", "Z")
    assert first_ts <= golden["signals"][0]["ts"] <= golden["signals"][-1]["ts"] <= last_ts
