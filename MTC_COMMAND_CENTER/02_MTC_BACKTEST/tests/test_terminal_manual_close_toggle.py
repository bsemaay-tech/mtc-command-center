import pandas as pd

from src.config.defaults import MTCConfig
from src.engine.mtc_runner import MTCRunner


def _df() -> pd.DataFrame:
    ts = pd.date_range("2026-01-01 00:00:00+00:00", periods=4, freq="15min", tz="UTC")
    return pd.DataFrame(
        {
            "timestamp": ts,
            "open": [100.0, 100.5, 101.0, 101.5],
            "high": [101.0, 101.5, 102.0, 102.5],
            "low": [99.5, 100.0, 100.5, 101.0],
            "close": [100.5, 101.0, 101.5, 102.0],
            "volume": [1.0, 1.0, 1.0, 1.0],
        }
    )


def _runner(force_terminal_manual_close: bool) -> MTCRunner:
    cfg = MTCConfig()
    cfg.parity.enabled = True
    cfg.parity.force_terminal_manual_close = force_terminal_manual_close
    cfg.strategy.close_open_at_end = False
    cfg.stop_loss.enabled = False
    cfg.take_profit.enabled = False
    cfg.break_even.enabled = False
    cfg.multi_tp.enabled = False
    cfg.trailing.enabled = False

    runner = MTCRunner(cfg)
    n = len(_df())
    long_sig = pd.Series([False, True, False, False], index=range(n), dtype=bool)
    short_sig = pd.Series([False, False, False, False], index=range(n), dtype=bool)
    allow_long = pd.Series([True] * n, index=range(n), dtype=bool)
    allow_short = pd.Series([True] * n, index=range(n), dtype=bool)

    runner.signal_plugin.generate = lambda df: (
        pd.Series(long_sig.values, index=df.index),
        pd.Series(short_sig.values, index=df.index),
    )
    runner.signal_plugin.get_debug_series = lambda df: {}
    runner.filter_chain.apply_with_details = lambda df: (
        pd.Series(allow_long.values, index=df.index),
        pd.Series(allow_short.values, index=df.index),
        {},
    )
    return runner


def test_parity_mode_can_disable_terminal_manual_close():
    df = _df()
    eval_end = pd.Timestamp(df["timestamp"].iloc[-1]).to_pydatetime()

    forced_runner = _runner(True)
    forced = forced_runner.run(df, warmup_bars=0, eval_end=eval_end)
    assert len(forced["trades"]) == 1
    assert forced["trades"][0].exit_reason.value == "MANUAL"

    not_forced_runner = _runner(False)
    not_forced = not_forced_runner.run(df, warmup_bars=0, eval_end=eval_end)
    assert len(not_forced["trades"]) == 0
    assert not_forced_runner.state.in_position is True
