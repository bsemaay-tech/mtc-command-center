"""
Task 1 — HTF Trend Filter unit tests.
TDD: run BEFORE implementing evaluate_htf_trend_filter.
"""
from __future__ import annotations

import pytest

from mtc_v2.core.gates import evaluate_htf_trend_filter
from mtc_v2.core.types import GateResult, HtfSnapshot


# ---------------------------------------------------------------------------
# HTF Trend Filter — core gate logic
# ---------------------------------------------------------------------------

def test_htf_trend_filter_long_ok_when_price_above_htf_ma() -> None:
    """Price above HTF MA (used directly as MA value) → long OK, short blocked."""
    snap = HtfSnapshot(close=95.0)
    result = evaluate_htf_trend_filter(
        close=100.0,
        htf_snap=snap,
        ma_type="EMA",
        ma_len=1,
        buffer_pct=0.0,
    )
    assert result.long_ok is True
    assert result.short_ok is False


def test_htf_trend_filter_short_ok_when_price_below_htf_ma() -> None:
    """Price below HTF MA → long blocked, short OK."""
    snap = HtfSnapshot(close=105.0)
    result = evaluate_htf_trend_filter(
        close=100.0,
        htf_snap=snap,
        ma_type="EMA",
        ma_len=1,
        buffer_pct=0.0,
    )
    assert result.long_ok is False
    assert result.short_ok is True


def test_htf_trend_filter_both_ok_when_not_ready() -> None:
    """Warmup / HTF not ready → pass-through (both OK)."""
    snap = HtfSnapshot()  # not ready
    result = evaluate_htf_trend_filter(
        close=100.0,
        htf_snap=snap,
        ma_type="EMA",
        ma_len=10,
        buffer_pct=0.0,
    )
    assert result.long_ok is True
    assert result.short_ok is True


def test_htf_trend_filter_buffer_allows_price_near_ma() -> None:
    """Buffer pct creates a zone around MA where both sides are OK."""
    snap = HtfSnapshot(close=100.0)
    # buffer_pct=1.0 → long OK when close > 100*(1-0.01)=99
    #                  short OK when close < 100*(1+0.01)=101
    result = evaluate_htf_trend_filter(
        close=100.0,
        htf_snap=snap,
        ma_type="EMA",
        ma_len=1,
        buffer_pct=1.0,
    )
    # close=100, long threshold=99 → 100 > 99 ✓
    # close=100, short threshold=101 → 100 < 101 ✓
    assert result.long_ok is True
    assert result.short_ok is True


def test_htf_trend_filter_gate_name_and_category() -> None:
    from mtc_v2.core.gates import GATE_HTF_TREND
    snap = HtfSnapshot(close=100.0)
    result = evaluate_htf_trend_filter(
        close=99.0, htf_snap=snap, ma_type="EMA", ma_len=1, buffer_pct=0.0
    )
    assert result.gate_name == GATE_HTF_TREND
    assert result.category == "filter"


# ---------------------------------------------------------------------------
# HTF Trend — warmup parity: runner must mirror Pine l12_filters_ready
# ---------------------------------------------------------------------------

def test_runner_blocks_entry_while_htf_tracker_warming_up() -> None:
    """Runner must block entries until HTF tracker warms up.

    Mirrors Pine: ``l12_filters_ready = ... and (not use_htf_trend_filter
    or not na(htf_trend_line_state))``  — ALL entries are blocked until the
    HTF MA has accumulated enough unique HTF closes to return non-na.

    This regression test catches the bug where Python allowed entries during
    the HTF warmup window while Pine blocked them.
    """
    import datetime as dt
    from mtc_v2.core.runner import Runner
    from mtc_v2.core.types import Bar

    # Pass raw (unresolved) config — Runner calls resolve_config internally
    runner = Runner({
        "use_htf_trend_filter": True,
        "htf_trend_ma_type": "SMA",
        "htf_trend_ma_len": 1000,  # extremely long — will never warm up in 50 bars
        "htf_trend_timeframe": "240",
        "st_atr_len": 2,           # tiny ST warmup so it finishes before bar 50
    })

    start = dt.datetime(2024, 1, 1, tzinfo=dt.timezone.utc)
    price = 50000.0
    bars = [
        Bar(
            timestamp=start + dt.timedelta(hours=i),
            open=price, high=price + 100.0, low=price - 100.0,
            close=price, volume=1_000.0, bar_index=i,
        )
        for i in range(50)
    ]
    # 50 unique htf_closes → 50/1000 dedup fires → tracker NOT ready
    htf_data = {
        bar.timestamp: {
            "open": price, "high": price + 100.0, "low": price - 100.0,
            "close": price + float(i), "volume": 1e9,
        }
        for i, bar in enumerate(bars)
    }
    runner.run(bars, htf_data=htf_data)

    # Sanity: tracker genuinely not ready
    assert not runner._htf_trend_tracker.ready, "HTF tracker should still be warming up"
    # Key assertion: after static warmup + ST warmup have both cleared (bar_index=49
    # is far past warmup_bars=2), entries must STILL be blocked because the HTF
    # tracker is not ready.
    assert runner.state.block_new_entries_this_bar is True, (
        "warmup_blocks_entry must remain True while HTF tracker is warming up"
    )
