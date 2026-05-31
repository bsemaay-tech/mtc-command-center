import pandas as pd

from src.config.defaults import MTCConfig
from src.engine.mtc_runner import MTCRunner
from src.engine.mtc_state import Direction


def _df_one_bar() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "timestamp": pd.to_datetime(["2026-01-01T00:00:00Z"], utc=True),
            "open": [101.0],
            "high": [103.0],
            "low": [100.0],
            "close": [102.0],
            "volume": [100],
        }
    )


def test_trailing_exit_uses_close_price_not_trailing_stop_for_long():
    cfg = MTCConfig()
    cfg.strategy.slippage_ticks = 0
    runner = MTCRunner(cfg)
    df = _df_one_bar()

    runner.state.reset()
    runner.state.bar_index = 0
    runner.state.current_time = pd.Timestamp("2026-01-01T00:00:00Z")
    pos = runner.state.open_position(Direction.LONG, entry_price=100.0, quantity=1.0, sl_price=99.0)
    pos.trailing_active = True
    pos.trailing_stop = 101.5
    pos.highest_price = 103.0
    pos.lowest_price = 100.0

    reason = runner._process_exits(
        bar={"open": 101.0, "high": 103.0, "low": 100.0, "close": 102.0, "volume": 100},
        df=df,
        bar_idx=0,
        long_signal=False,
        short_signal=False,
        long_raw=False,
        short_raw=False,
    )

    assert reason == "TRAIL"
    trade = runner.state.trades[-1]
    assert trade.exit_price == 102.0
