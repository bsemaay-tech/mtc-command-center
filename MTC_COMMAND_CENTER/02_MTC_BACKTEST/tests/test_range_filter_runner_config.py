from src.config.defaults import MTCConfig
from src.engine.mtc_runner import MTCRunner


def test_runner_respects_bb_toggle_for_adx_chop_bb_signal_mode():
    cfg = MTCConfig()
    cfg.signal_mode = "Range Filter Hybrid (ADX+Chop+BB)"
    cfg.range_filter.use_bb_filter = False

    runner = MTCRunner(cfg)

    assert runner.signal_plugin.use_bb_filter is False
