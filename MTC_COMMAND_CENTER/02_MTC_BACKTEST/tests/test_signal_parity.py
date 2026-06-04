import pandas as pd
import pytest

from src.workflow.signal_parity import (
    RAW_LONG_TITLE,
    RAW_SHORT_TITLE,
    compare_signals,
    load_pine_signals_csv,
)


def test_compare_signals_exact_match_passes():
    py_long = [False, True, False, True]
    py_short = [True, False, False, False]
    res = compare_signals(py_long, py_short, py_long, py_short)

    assert res["status"] == "PASS"
    assert res["long_match_rate"] == 1.0
    assert res["short_match_rate"] == 1.0
    assert res["long_mismatch_bars"] == []
    assert res["short_mismatch_bars"] == []


def test_compare_signals_reports_mismatch_and_fails():
    py_long = [False, True, False, True]
    pine_long = [False, False, False, True]  # bar 1 differs
    py_short = [True, False, False, False]
    res = compare_signals(py_long, py_short, pine_long, py_short)

    assert res["status"] == "FAIL"
    assert res["long_mismatch_bars"] == [1]
    assert res["long_match_rate"] == 0.75


def test_compare_signals_tolerance_allows_partial_match():
    py_long = [True, True, True, True]
    pine_long = [True, True, True, False]  # 75% match
    py_short = [False, False, False, False]
    res = compare_signals(py_long, py_short, pine_long, py_short, min_match_rate=0.7)

    assert res["status"] == "PASS"
    assert res["long_match_rate"] == 0.75


def test_compare_signals_empty_raises():
    with pytest.raises(ValueError):
        compare_signals([], [], [], [])


def test_load_pine_signals_csv_by_title(tmp_path):
    path = tmp_path / "pine.csv"
    pd.DataFrame(
        {
            RAW_LONG_TITLE: [0.0, 1.0, 0.0],
            RAW_SHORT_TITLE: [1.0, 0.0, 0.0],
        }
    ).to_csv(path, index=False)

    long_s, short_s = load_pine_signals_csv(path)

    assert long_s.tolist() == [False, True, False]
    assert short_s.tolist() == [True, False, False]
