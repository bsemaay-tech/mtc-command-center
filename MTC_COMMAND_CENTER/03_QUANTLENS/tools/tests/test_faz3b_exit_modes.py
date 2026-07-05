"""Faz 3b (D013) unit tests for swept exit_mode in simulate_slice.

Covers the four exit modes and the MEGA_EXIT_MODES parser. Self-parity
(fixed_2R byte-identity) is proven separately by faz3b_self_parity.py --verify;
these tests pin the NEW modes' semantics.

Run: pytest tests/test_faz3b_exit_modes.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

import mega_walk_forward as mw  # noqa: E402

NON_TRAIL_STRAT = "SOME_GENERIC_STRATEGY"  # not the native is_trail strategy


def _make_df(n, *, open_, high, low, close, ema_8=None):
    """Build a synthetic OHLC df of length n with a valid datetime `date` col."""
    data = {
        "open": np.asarray(open_, dtype=float),
        "high": np.asarray(high, dtype=float),
        "low": np.asarray(low, dtype=float),
        "close": np.asarray(close, dtype=float),
        "date": pd.date_range("2024-01-01", periods=n, freq="h"),
    }
    if ema_8 is not None:
        data["ema_8"] = np.asarray(ema_8, dtype=float)
    return pd.DataFrame(data)


def _flat(n, v):
    return np.full(n, float(v))


def _one_trade_frame(n=130):
    """Single long entry at bar 21 (sig[20]=True); stop at 99, entry open=100."""
    op = _flat(n, 100.0)
    hi = _flat(n, 100.5)
    lo = _flat(n, 99.5)
    cl = _flat(n, 100.0)
    sig = np.zeros(n, dtype=bool)
    sig[20] = True
    stop = _flat(n, 0.0)
    stop[20] = 99.0  # risk = 1.0 (entry 100 - stop 99)
    return op, hi, lo, cl, sig, stop


# --------------------------------------------------------------------------
# fixed_3R target math (and fixed_2R contrast on identical data)
# --------------------------------------------------------------------------
def test_fixed_2R_vs_3R_target_math():
    op, hi, lo, cl, sig, stop = _one_trade_frame()
    # Bar 22 spikes high to 103 (>= 3R target 103) with low above the 99 stop;
    # bar 21 is neutral (high 100.5 below both 2R=102 and 3R=103 targets).
    hi[22] = 103.0
    df = _make_df(len(op), open_=op, high=hi, low=lo, close=cl)
    sig_s, stop_s = pd.Series(sig), pd.Series(stop)

    stats2, R2 = mw.simulate_slice(df, sig_s, stop_s, NON_TRAIL_STRAT, 0, len(op),
                                   return_trades=True, exit_mode="fixed_2R")
    stats3, R3 = mw.simulate_slice(df, sig_s, stop_s, NON_TRAIL_STRAT, 0, len(op),
                                   return_trades=True, exit_mode="fixed_3R")

    assert stats2.num_trades == 1 and stats3.num_trades == 1
    assert R2[0] == pytest.approx(2.0, abs=1e-9)  # exits at entry + 2R
    assert R3[0] == pytest.approx(3.0, abs=1e-9)  # exits at entry + 3R


# --------------------------------------------------------------------------
# trail_ema8: exits at NEXT open when close < ema8
# --------------------------------------------------------------------------
def test_trail_ema8_exits_next_open_on_close_below_ema():
    op, hi, lo, cl, sig, stop = _one_trade_frame()
    n = len(op)
    ema = _flat(n, 99.0)          # close (100) stays above ema (99): no trail exit
    ema[22] = 101.0              # bar 22 close 100 < ema 101 -> trail exit
    op[23] = 100.7               # exit fills at bar 23 open
    df = _make_df(n, open_=op, high=hi, low=lo, close=cl, ema_8=ema)
    sig_s, stop_s = pd.Series(sig), pd.Series(stop)

    stats, R, events = mw.simulate_slice(
        df, sig_s, stop_s, NON_TRAIL_STRAT, 0, n,
        return_trades=True, return_trade_events=True, exit_mode="trail_ema8")

    assert stats.num_trades == 1
    assert events[0]["exit_idx"] == 22          # signal bar
    assert events[0]["exit_price"] == pytest.approx(100.7)  # next open


# --------------------------------------------------------------------------
# trail_ema8: NA-skip (never zeros) when the slice has no ema_8 column
# --------------------------------------------------------------------------
def test_trail_ema8_na_skip_without_ema_column():
    op, hi, lo, cl, sig, stop = _one_trade_frame()
    n = len(op)
    df = _make_df(n, open_=op, high=hi, low=lo, close=cl)  # NO ema_8
    sig_s, stop_s = pd.Series(sig), pd.Series(stop)

    na = mw.simulate_slice(df, sig_s, stop_s, NON_TRAIL_STRAT, 0, n,
                           exit_mode="trail_ema8")
    assert mw.slice_is_na(na)
    assert na.num_trades == -1           # NA sentinel, explicitly NOT a zero-trade result

    # same df runs fine under a non-trail mode (proves the skip is trail-specific)
    ok = mw.simulate_slice(df, sig_s, stop_s, NON_TRAIL_STRAT, 0, n,
                           exit_mode="fixed_2R")
    assert not mw.slice_is_na(ok)
    assert ok.num_trades >= 0


# --------------------------------------------------------------------------
# opposite_channel: exit level = rolling min(low, exit_len).shift(1), no look-ahead
# --------------------------------------------------------------------------
def test_opposite_channel_exit_level_and_shift1_no_lookahead():
    op, hi, lo, cl, sig, stop = _one_trade_frame()
    n = len(op)
    assert mw.EXIT_CHANNEL_LEN == 20
    # Wide stop so the channel (not the stop) drives the exit.
    stop[20] = 89.0                       # risk = 11
    lo[:] = 100.0
    lo[40] = 98.0                         # min of lows[30:50] (excludes bar 50) = 98
    lo[50] = 90.0                         # bar 50's own low; MUST be excluded by shift(1)
    cl[50] = 97.0                         # close 97 < channel 98 -> exit; 97 !< 90 (bug case)
    op[51] = 100.3                        # exit fills at bar 51 open
    df = _make_df(n, open_=op, high=hi, low=lo, close=cl)
    sig_s, stop_s = pd.Series(sig), pd.Series(stop)

    stats, R, events = mw.simulate_slice(
        df, sig_s, stop_s, NON_TRAIL_STRAT, 0, n,
        return_trades=True, return_trade_events=True, exit_mode="opposite_channel")

    assert stats.num_trades == 1
    assert events[0]["exit_idx"] == 50            # channel breach bar
    assert events[0]["exit_price"] == pytest.approx(100.3)  # next open
    # Direct level check: shift(1) excludes bar 50 (low 90); channel == 98.
    chan = pd.Series(lo).rolling(mw.EXIT_CHANNEL_LEN).min().shift(1).to_numpy()
    assert chan[50] == pytest.approx(98.0)


# --------------------------------------------------------------------------
# MEGA_EXIT_MODES parser
# --------------------------------------------------------------------------
def test_parse_exit_modes_default_and_variants():
    assert mw.parse_exit_modes(None) == ["fixed_2R"]
    assert mw.parse_exit_modes("") == ["fixed_2R"]
    assert mw.parse_exit_modes("   ") == ["fixed_2R"]
    assert mw.parse_exit_modes("fixed_2R,trail_ema8") == ["fixed_2R", "trail_ema8"]
    assert mw.parse_exit_modes(" fixed_2R , fixed_3R ") == ["fixed_2R", "fixed_3R"]
    assert mw.parse_exit_modes("fixed_2R,fixed_2R") == ["fixed_2R"]  # de-dup, order kept
    assert mw.parse_exit_modes("opposite_channel,fixed_2R") == ["opposite_channel", "fixed_2R"]


def test_parse_exit_modes_rejects_unknown():
    with pytest.raises(SystemExit):
        mw.parse_exit_modes("fixed_2R,made_up_mode")
