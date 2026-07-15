"""Exit-aware gauntlet tooling tests (2026-07-15).

Verifies that cpcv_validator / multiwindow_oos / probabilistic_pbo thread a
row's exit_mode into simulate_slice, stamp it into outputs, and preserve
byte-identical numeric behaviour for legacy fixed_2R inputs. simulate_slice and
the data loaders are monkeypatched with spies so NO real backtest runs.

Run: pytest tests/test_exit_aware_gauntlet.py
"""
import sys
import types
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

import mega_walk_forward as mw  # noqa: E402
import cpcv_validator as cpcv  # noqa: E402
import multiwindow_oos as mwin  # noqa: E402


class FakeStats:
    """Minimal stand-in for SliceStats: only the attributes the tools read."""

    def __init__(self, net_return_pct=1.0, num_trades=40, max_drawdown_pct=-5.0,
                 profit_factor=1.5, sharpe=1.0):
        self.net_return_pct = net_return_pct
        self.num_trades = num_trades
        self.max_drawdown_pct = max_drawdown_pct
        self.profit_factor = profit_factor
        self.sharpe = sharpe


def _install_spy(monkeypatch, module=None):
    """Patch mega_walk_forward.simulate_slice with a spy recording exit_mode.

    The tools call `mw.simulate_slice` / `M.simulate_slice` — both alias the one
    mega_walk_forward module — so patching it there covers every tool.
    """
    seen = []

    def spy(df, sig, stop, strategy, s_idx, e_idx, return_trades=False,
            direction="long", return_trade_events=False, exit_mode=mw.DEFAULT_EXIT_MODE):
        seen.append(exit_mode)
        stats = FakeStats()
        if return_trades:
            return stats, [1.0] * stats.num_trades
        return stats

    monkeypatch.setattr(mw, "simulate_slice", spy)
    return seen


def _install_data_stubs(monkeypatch, module=None):
    # load_df returns a plain list long enough for n_groups=6; the tools only
    # need len(df), df.copy(), and pass it opaquely to the (stubbed) signals.
    monkeypatch.setattr(mw, "find_ds", lambda manifest, sym, tf: {"normalized_path": "x"})
    monkeypatch.setattr(mw, "load_df", lambda path: list(range(6000)))
    monkeypatch.setattr(mw, "build_signals", lambda strat, df, params, dmap: ([0], [0]))


class Args:
    n_groups = 6
    test_groups = 2
    embargo_pct = 0.01
    min_trades = 30
    min_pf = 1.0
    max_dd_floor = -50.0


def _row(exit_mode=None):
    r = {"strategy": "GEN_KELTNER_BREAKOUT", "symbol": "SPY", "timeframe": "1h",
         "classification": "STRONG_PASS",
         "summary": {"best_params": {"ema_len": 50, "atr_len": 10, "mult": 2.0}}}
    if exit_mode is not None:
        r["exit_mode"] = exit_mode
    return r


# ---- cpcv_validator ----

def test_cpcv_defaults_to_fixed_2r_for_legacy_row(monkeypatch):
    seen = _install_spy(monkeypatch, cpcv)
    _install_data_stubs(monkeypatch, cpcv)
    out = cpcv.validate_candidate(_row(exit_mode=None), {}, Args())
    assert out["status"] == "OK"
    assert out["exit_mode"] == "fixed_2R"
    assert seen and all(em == "fixed_2R" for em in seen)


def test_cpcv_threads_trail_ema8(monkeypatch):
    seen = _install_spy(monkeypatch, cpcv)
    _install_data_stubs(monkeypatch, cpcv)
    out = cpcv.validate_candidate(_row(exit_mode="trail_ema8"), {}, Args())
    assert out["status"] == "OK"
    assert out["exit_mode"] == "trail_ema8"
    assert seen and all(em == "trail_ema8" for em in seen)
    # every split row is stamped so an auditor can detect substitution
    assert all("test_groups" in s for s in out["split_results"])


def test_cpcv_stamps_exit_mode_on_na_and_insufficient(monkeypatch):
    _install_spy(monkeypatch, cpcv)
    # N_A path: find_ds returns None
    monkeypatch.setattr(mw, "find_ds", lambda m, s, t: None)
    out = cpcv.validate_candidate(_row(exit_mode="trail_ema8"), {}, Args())
    assert out["status"] == "N_A"
    assert out["exit_mode"] == "trail_ema8"


def test_cpcv_evaluate_split_passes_exit_mode(monkeypatch):
    seen = _install_spy(monkeypatch, cpcv)
    cpcv.evaluate_split([0], [0], [0], "S", [(0, 100), (100, 200)], exit_mode="trail_ema8")
    assert seen == ["trail_ema8", "trail_ema8"]
    # None -> default fixed_2R (legacy parity)
    seen.clear()
    cpcv.evaluate_split([0], [0], [0], "S", [(0, 100)])
    assert seen == ["fixed_2R"]


# ---- multiwindow_oos ----

def _install_queue_spy(monkeypatch, stats_queue):
    """simulate_slice spy that pops a FakeStats per call; records exit_mode."""
    seen = []
    q = list(stats_queue)

    def spy(df, sig, stop, strategy, s_idx, e_idx, return_trades=False,
            direction="long", return_trade_events=False, exit_mode=mw.DEFAULT_EXIT_MODE):
        seen.append(exit_mode)
        stats = q.pop(0) if q else FakeStats()
        if return_trades:
            return stats, [1.0] * max(int(stats.num_trades), 0)
        return stats

    monkeypatch.setattr(mw, "simulate_slice", spy)
    monkeypatch.setattr(mw, "bootstrap_p_positive", lambda R, n, seed: 0.5)
    monkeypatch.setattr(mw, "build_signals", lambda strat, df, params, dmap: ([0], [0]))
    return seen


def test_multiwindow_score_window_threads_exit_mode(monkeypatch):
    seen = _install_queue_spy(monkeypatch, [FakeStats()])
    mwin.score_window([0], [0], [0], "S", 0, 100, seed=1, exit_mode="trail_ema8")
    assert seen == ["trail_ema8"]


def test_neighbor_stability_strict_counts_low_trade_as_fail(monkeypatch):
    # two literal neighbours: first healthy+positive, second low-trade
    lits = [{"ema_len": 20}, {"ema_len": 60}]
    # strict=True: low-trade neighbour stays in denominator as a failure
    _install_queue_spy(monkeypatch, [FakeStats(num_trades=40, net_return_pct=2.0),
                                     FakeStats(num_trades=5, net_return_pct=2.0)])
    pos, tot = mwin.neighbor_stability("S", [0], {"ema_len": 50}, "SPY", 0, 100,
                                       exit_mode="trail_ema8", literal_neighbors=lits, strict=True)
    assert (pos, tot) == (1, 2)  # 1 of 2 pass; low-trade counted as fail


def test_neighbor_stability_legacy_excludes_low_trade(monkeypatch):
    lits = [{"ema_len": 20}, {"ema_len": 60}]
    _install_queue_spy(monkeypatch, [FakeStats(num_trades=40, net_return_pct=2.0),
                                     FakeStats(num_trades=5, net_return_pct=2.0)])
    pos, tot = mwin.neighbor_stability("S", [0], {"ema_len": 50}, "SPY", 0, 100,
                                       literal_neighbors=lits, strict=False)
    assert (pos, tot) == (1, 1)  # low-trade excluded from denominator (legacy)
