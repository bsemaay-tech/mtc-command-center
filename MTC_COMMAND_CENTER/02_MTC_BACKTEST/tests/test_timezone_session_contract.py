from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

from src.engine.mtc_runner import MTCRunner

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from compare_tv import _parse_tv_time


def test_end_of_day_boundary_on_dst_weekend_uses_utc_dates():
    tv_times = [
        "2025-10-26 23:30",
        "2025-10-26 23:45",
        "2025-10-27 00:00",
    ]
    ts_series = pd.Series([_parse_tv_time(t, tv_tz="Europe/London") for t in tv_times])

    assert MTCRunner._is_end_of_day(0, ts_series) is False
    assert MTCRunner._is_end_of_day(1, ts_series) is True
    assert MTCRunner._is_end_of_day(2, ts_series) is True


def test_end_of_week_boundary_uses_iso_week_rollover():
    ts_series = pd.Series(
        pd.to_datetime(
            [
                "2025-12-28T23:45:00Z",  # Sunday
                "2025-12-29T00:00:00Z",  # Monday (new ISO week)
                "2025-12-29T00:15:00Z",
            ],
            utc=True,
        )
    )

    assert MTCRunner._is_end_of_week(0, ts_series) is True
    assert MTCRunner._is_end_of_week(1, ts_series) is False
    assert MTCRunner._is_end_of_week(2, ts_series) is True
