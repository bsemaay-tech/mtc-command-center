from pathlib import Path

from src.ui.parity_case_loader import build_backtest_state_from_case, diff_backtest_state_with_case


def test_build_backtest_state_from_case_maps_parity_fields():
    case_path = Path(__file__).resolve().parents[1] / "configs" / "cases" / "full_jul2025_jan2026_parity.json"
    state = build_backtest_state_from_case(case_path)

    assert state["bt_dataset"] == "BTCUSDT_15m_20240101_20260213.parquet"
    assert str(state["bt_range_start"]) == "2025-06-30"
    assert str(state["bt_range_end"]) == "2026-02-01"
    assert state["bt_warmup"] == 200
    assert state["bt_preroll_days"] == 365
    assert state["bt_pyramiding"] == 1
    assert state["bt_pyr_max"] == 1
    assert state["bt_sig_max_ent"] == 1
    assert state["bt_comm"] == 0.04
    assert state["bt_slip"] == 5
    assert state["bt_mintick"] == 0.1


def test_diff_backtest_state_with_case_detects_mismatch():
    case_path = Path(__file__).resolve().parents[1] / "configs" / "cases" / "full_jul2025_jan2026_parity.json"
    state = build_backtest_state_from_case(case_path)
    state["bt_comm"] = 0.05
    mismatches = diff_backtest_state_with_case(case_path, state)
    assert "bt_comm" in mismatches
