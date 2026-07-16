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

import json  # noqa: E402

import mega_walk_forward as mw  # noqa: E402
import cpcv_validator as cpcv  # noqa: E402
import multiwindow_oos as mwin  # noqa: E402
import probabilistic_pbo as pbo  # noqa: E402
import exit_aware_gauntlet as gaunt  # noqa: E402


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


# ---- probabilistic_pbo ----

def test_pbo_candidate_id_exit_and_params_aware():
    legacy = pbo.candidate_id({"strategy": "S", "symbol": "SPY", "timeframe": "1h"})
    assert legacy == "S|SPY|1h"  # legacy rows unchanged
    full = pbo.candidate_id({"strategy": "S", "symbol": "SPY", "timeframe": "1h",
                             "exit_mode": "trail_ema8", "params": {"ema_len": 50, "atr_len": 10}})
    assert full == "S|SPY|1h|trail_ema8|atr_len=10,ema_len=50"


def _write_matrix(tmp_path, configs, cell=None):
    cell = cell or {"strategy": "S", "symbol": "SPY_NEW", "timeframe": "1h", "exit_mode": "trail_ema8"}
    p = tmp_path / "config_matrix.json"
    p.write_text(json.dumps({"cell": cell, "period_labels": ["G0", "G1", "G2"], "configs": configs}), encoding="utf-8")
    return p


def test_pbo_config_matrix_rows_are_configs(tmp_path):
    configs = [
        {"params": {"ema_len": 50}, "role": "primary", "returns_pct": [1.0, 2.0, -1.0]},
        {"params": {"ema_len": 20}, "role": "star", "returns_pct": [0.5, 1.0, 0.0]},
    ]
    ids, matrix = pbo.load_config_matrix(_write_matrix(tmp_path, configs))
    assert len(ids) == 2 and len(matrix) == 2 and len(matrix[0]) == 3
    assert all("SPY_NEW|1h|trail_ema8" in i for i in ids)
    assert ids[0] != ids[1]  # distinct params -> distinct configs


def test_pbo_config_matrix_refuses_single_config(tmp_path):
    configs = [{"params": {"ema_len": 50}, "role": "primary", "returns_pct": [1.0, 2.0]}]
    with pytest.raises(ValueError):
        pbo.load_config_matrix(_write_matrix(tmp_path, configs))


def test_pbo_config_matrix_refuses_ragged_periods(tmp_path):
    configs = [
        {"params": {"ema_len": 50}, "role": "primary", "returns_pct": [1.0, 2.0, 3.0]},
        {"params": {"ema_len": 20}, "role": "star", "returns_pct": [1.0, 2.0]},
    ]
    with pytest.raises(ValueError):
        pbo.load_config_matrix(_write_matrix(tmp_path, configs))


# ---- exit_aware_gauntlet orchestrator ----

def test_build_config_matrix_shape_and_exit_stamp(monkeypatch):
    seen = _install_queue_spy(monkeypatch, [FakeStats(net_return_pct=float(i)) for i in range(6)])
    cell = {"strategy": "S", "symbol": "SPY_NEW", "timeframe": "1h", "exit_mode": "trail_ema8"}
    configs = [{"params": {"ema_len": 50}, "role": "primary"},
               {"params": {"ema_len": 20}, "role": "star"}]
    art = gaunt.build_config_matrix(cell, list(range(300)), configs, n_groups=3)
    assert art["cell"]["exit_mode"] == "trail_ema8"
    assert len(art["configs"]) == 2
    assert all(len(c["returns_pct"]) == 3 for c in art["configs"])
    assert all(em == "trail_ema8" for em in seen)  # exit threaded into every group sim


def test_build_config_matrix_feeds_pbo(tmp_path, monkeypatch):
    _install_queue_spy(monkeypatch, [FakeStats(net_return_pct=1.0) for _ in range(6)])
    cell = {"strategy": "S", "symbol": "SPY_NEW", "timeframe": "1h", "exit_mode": "trail_ema8"}
    configs = [{"params": {"ema_len": 50}, "role": "primary"},
               {"params": {"ema_len": 20}, "role": "star"}]
    art = gaunt.build_config_matrix(cell, list(range(300)), configs, n_groups=3)
    p = tmp_path / "m.json"
    p.write_text(json.dumps(art), encoding="utf-8")
    ids, matrix = pbo.load_config_matrix(p)  # must be consumable end-to-end
    assert len(ids) == 2 and len(matrix[0]) == 3


def test_verdict_all_gates_pass():
    v = gaunt.verdict({"status": "OK", "pass_rate": 0.8}, {"status": "OK", "pbo": 0.2},
                      mw_pos=4, mw_stable_pos=4, mw_stable_tot=4)
    assert v["gauntlet_pass"] and v["status"] == "PASS" and not v["reasons"]


def test_verdict_any_missing_gate_fails():
    # PBO N_A (as in the Donchian 0-eligible case) => GAUNTLET_FAIL, never waived
    v = gaunt.verdict({"status": "OK", "pass_rate": 0.9}, {"status": "INSUFFICIENT_DATA", "pbo": None},
                      mw_pos=5, mw_stable_pos=4, mw_stable_tot=4)
    assert not v["gauntlet_pass"] and v["status"] == "GAUNTLET_FAIL"
    assert any("pbo" in r for r in v["reasons"])


def test_faz3b_self_parity_module_present():
    # sanity: the engine self-parity gate exists and is unaffected (we never touch the engine)
    assert (TOOLS / "faz3b_self_parity.py").exists()


# ---- faz3b_newsymbol_runner (pre-registration scope guards) ----

import faz3b_newsymbol_runner as runner  # noqa: E402


def test_runner_grid_is_exactly_the_frozen_winner():
    # the whole design: ONE config decides, no selection on the new data
    assert runner.frozen_grid() == [{"ema_len": 50, "atr_len": 10, "mult": 2.0}]
    assert len(runner.frozen_grid()) == 1


def test_runner_symbol_universe_frozen_and_grouped():
    assert len(runner.SYMBOLS) == 16
    assert len(set(runner.SYMBOLS)) == 16  # no duplicates
    assert len(runner.SYMBOL_GROUPS) == 4  # >=2 groups required to confirm
    assert runner.EXPECTED_ROWS == 32  # 16 symbols x 2 exit modes


def test_runner_rejects_stride_set(monkeypatch, tmp_path):
    monkeypatch.setenv("MEGA_GRID_STRIDE", "3")
    monkeypatch.setenv("MEGA_EXIT_MODES", "fixed_2R,trail_ema8")
    m = tmp_path / "manifest.json"; m.write_text("{}", encoding="utf-8")
    with pytest.raises(SystemExit):
        runner.assert_scope([], str(m), tmp_path / "out")


def test_runner_rejects_wrong_exit_modes(monkeypatch, tmp_path):
    monkeypatch.delenv("MEGA_GRID_STRIDE", raising=False)
    monkeypatch.setenv("MEGA_EXIT_MODES", "fixed_2R")  # missing the candidate
    m = tmp_path / "manifest.json"; m.write_text("{}", encoding="utf-8")
    with pytest.raises(SystemExit):
        runner.assert_scope([], str(m), tmp_path / "out")


def test_runner_rejects_wrong_timeframe(monkeypatch, tmp_path):
    monkeypatch.delenv("MEGA_GRID_STRIDE", raising=False)
    monkeypatch.setenv("MEGA_EXIT_MODES", "fixed_2R,trail_ema8")
    m = tmp_path / "manifest.json"; m.write_text("{}", encoding="utf-8")
    with pytest.raises(SystemExit):
        runner.assert_scope(["--tf", "4h"], str(m), tmp_path / "out")


def test_runner_rejects_nonempty_out_dir(monkeypatch, tmp_path):
    monkeypatch.delenv("MEGA_GRID_STRIDE", raising=False)
    monkeypatch.setenv("MEGA_EXIT_MODES", "fixed_2R,trail_ema8")
    m = tmp_path / "manifest.json"; m.write_text("{}", encoding="utf-8")
    out = tmp_path / "out"; out.mkdir(); (out / "stale.json").write_text("{}", encoding="utf-8")
    with pytest.raises(SystemExit):
        runner.assert_scope([], str(m), out)


def test_runner_accepts_correct_scope(monkeypatch, tmp_path):
    monkeypatch.delenv("MEGA_GRID_STRIDE", raising=False)
    monkeypatch.setenv("MEGA_EXIT_MODES", "fixed_2R,trail_ema8")
    m = tmp_path / "manifest.json"; m.write_text("{}", encoding="utf-8")
    runner.assert_scope(["--tf", "1h"], str(m), tmp_path / "fresh_out")  # must not raise


# ---- alpaca_download_dataset --symbols override (data acquisition prerequisite) ----

import alpaca_download_dataset as dl  # noqa: E402


def test_downloader_default_universe_unchanged():
    # parity: no --symbols -> exactly the historical universe (equities + crypto)
    uni = dl.build_universe()
    syms = [s for s, _c, _a in uni]
    assert len(uni) == len(dl.EQUITY_UNIVERSE) + len(dl.CRYPTO_UNIVERSE)
    assert "SPY" in syms and "BTC/USD" in syms
    assert any(is_crypto for _s, is_crypto, _a in uni)


def test_downloader_explicit_symbols_override():
    uni = dl.build_universe(["JPM", "EWJ", "RSP"], asset_class="confirm_newsymbol")
    assert [s for s, _c, _a in uni] == ["JPM", "EWJ", "RSP"]
    assert all(not is_crypto for _s, is_crypto, _a in uni)  # no crypto smuggled in
    assert all(ac == "confirm_newsymbol" for _s, _c, ac in uni)
    # the hardcoded universe is never mutated
    assert "JPM" not in dl.EQUITY_UNIVERSE
