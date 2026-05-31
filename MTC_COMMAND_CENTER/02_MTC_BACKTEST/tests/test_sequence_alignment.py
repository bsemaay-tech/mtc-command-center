from __future__ import annotations

import pandas as pd

from src.parity.sequence_alignment import greedy_prefix_alignment


def _frame(rows: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    df["entry_time"] = pd.to_datetime(df["entry_time"], utc=True)
    df["exit_time"] = pd.to_datetime(df["exit_time"], utc=True)
    return df


def test_greedy_prefix_alignment_detects_single_extra_python_trade() -> None:
    tv = _frame(
        [
            {"side": "SHORT", "entry_time": "2025-01-01T00:00:00Z", "exit_time": "2025-01-01T00:15:00Z", "reason": "SL"},
            {"side": "SHORT", "entry_time": "2025-01-01T00:15:00Z", "exit_time": "2025-01-01T00:30:00Z", "reason": "SL"},
            {"side": "LONG", "entry_time": "2025-01-01T00:30:00Z", "exit_time": "2025-01-01T00:45:00Z", "reason": "TP"},
        ]
    )
    py = _frame(
        [
            {"side": "SHORT", "entry_time": "2025-01-01T00:00:00Z", "exit_time": "2025-01-01T00:15:00Z", "reason": "SL"},
            {"side": "SHORT", "entry_time": "2025-01-01T00:05:00Z", "exit_time": "2025-01-01T00:10:00Z", "reason": "SL"},
            {"side": "SHORT", "entry_time": "2025-01-01T00:15:00Z", "exit_time": "2025-01-01T00:30:00Z", "reason": "SL"},
            {"side": "LONG", "entry_time": "2025-01-01T00:30:00Z", "exit_time": "2025-01-01T00:45:00Z", "reason": "TP"},
        ]
    )

    got = greedy_prefix_alignment(tv, py, tolerance_min=15)

    assert got["matched_prefix_len"] == 3
    assert got["events"][1]["mode"] == "skip_py_1"
    assert got["break_tv_seq"] is None
    assert got["break_py_seq"] is None
