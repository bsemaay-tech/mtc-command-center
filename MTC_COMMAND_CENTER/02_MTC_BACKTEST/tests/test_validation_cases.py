import json
from pathlib import Path


def load_case(relpath: str) -> dict:
    root = Path(__file__).resolve().parents[1]
    return json.loads((root / relpath).read_text(encoding="utf-8"))


def test_multi_asset_templates_exist_and_are_pyramiding_1():
    eth = load_case("configs/cases/ethusdt_15m_walkforward_template.json")
    sol = load_case("configs/cases/solusdt_15m_walkforward_template.json")

    assert eth["dataset"].startswith("ETHUSDT_15m_")
    assert sol["dataset"].startswith("SOLUSDT_15m_")
    assert eth["config"]["strategy"]["pyramiding"] == 1
    assert sol["config"]["strategy"]["pyramiding"] == 1


def test_dst_boundary_cases_exist_and_are_parity_enabled():
    mar = load_case("configs/cases/dst_boundary_mar2025_btcusdt_15m.json")
    oct_ = load_case("configs/cases/dst_boundary_oct2025_btcusdt_15m.json")

    assert mar["config"]["parity"]["enabled"] is True
    assert oct_["config"]["parity"]["enabled"] is True
    assert mar["config"]["strategy"]["pyramiding"] == 1
    assert oct_["config"]["strategy"]["pyramiding"] == 1


def test_supertrend_walkforward_cases_exist_and_force_terminal_close():
    train = load_case("configs/cases/supertrend_wf_train_20260308.json")
    target1 = load_case("configs/cases/supertrend_wf_target1_20260308.json")
    target2 = load_case("configs/cases/supertrend_wf_target2_20260308.json")

    for case in (train, target1, target2):
        assert case["dataset"] == "BTCUSDT_PERP_15m_20240101_20260101_long.parquet"
        assert case["config"]["signal_mode"] == "Supertrend"
        assert case["config"]["trade"]["entry_mode"] == "Edge"
        assert case["config"]["parity"]["enabled"] is True
        assert case["config"]["parity"]["force_terminal_manual_close"] is True
        assert case["config"]["strategy"]["pyramiding"] == 1
