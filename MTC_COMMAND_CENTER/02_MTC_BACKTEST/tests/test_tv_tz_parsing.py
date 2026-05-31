"""
Tests for DST-aware TV timestamp parsing.

Verifies that Europe/London timestamps are correctly converted to UTC
around the BST<->GMT boundary (last Sunday of October).
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import pandas as pd
import pytest


def test_bst_summer_offset():
    """BST (summer): 2025-07-15 12:00 London = 11:00 UTC."""
    from compare_tv import _parse_tv_time
    result = _parse_tv_time("2025-07-15 12:00", tv_tz="Europe/London")
    assert result.hour == 11
    assert result.minute == 0
    assert str(result.tzinfo) in ("UTC", "utc")


def test_gmt_winter_offset():
    """GMT (winter): 2026-01-13 22:15 London = 22:15 UTC."""
    from compare_tv import _parse_tv_time
    result = _parse_tv_time("2026-01-13 22:15", tv_tz="Europe/London")
    assert result.hour == 22
    assert result.minute == 15


def test_dst_boundary_october():
    """Oct 26 2025 01:30 is ambiguous (clocks fall back). Should still parse."""
    from compare_tv import _parse_tv_time
    result = _parse_tv_time("2025-10-26 01:30", tv_tz="Europe/London")
    assert result is not pd.NaT
    # During ambiguous time, we pick DST=True (summer), so UTC = 00:30
    assert result.hour == 0
    assert result.minute == 30


def test_before_dst_switch():
    """Oct 10 2025 22:30 BST = 21:30 UTC (still summer)."""
    from compare_tv import _parse_tv_time
    result = _parse_tv_time("2025-10-10 22:30", tv_tz="Europe/London")
    assert result.hour == 21
    assert result.minute == 30


def test_after_dst_switch():
    """Nov 20 2025 17:00 GMT = 17:00 UTC (winter)."""
    from compare_tv import _parse_tv_time
    result = _parse_tv_time("2025-11-20 17:00", tv_tz="Europe/London")
    assert result.hour == 17
    assert result.minute == 0


def test_invalid_timestamp():
    """Invalid timestamp returns NaT."""
    from compare_tv import _parse_tv_time
    result = _parse_tv_time("not-a-date", tv_tz="Europe/London")
    assert pd.isna(result)


def test_utc_tz_no_offset():
    """When tv_tz='UTC', no offset applied."""
    from compare_tv import _parse_tv_time
    result = _parse_tv_time("2025-07-15 12:00", tv_tz="UTC")
    assert result.hour == 12
    assert result.minute == 0
