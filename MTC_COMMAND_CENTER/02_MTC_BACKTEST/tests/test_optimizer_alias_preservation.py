import pandas as pd

from src.config.defaults import MTCConfig
from src.optimizer_v0.search import ParamDef, TrialResult, random_search
from src.optimize.runner import OptimizationRunner
from src.optimizer_v0.search import _apply_params as apply_search_params


def _base_cfg() -> MTCConfig:
    return MTCConfig.model_validate(
        {
            "signal_mode": "Range Filter Hybrid (ADX+Chop+BB)",
            "stop_loss": {"use_sl": False},
            "take_profit": {"use_tp": False},
            "break_even": {"use_break_even": False},
            "multi_tp": {"use_multi_tp": False},
            "trailing": {"use_trailing": False},
            "range_filter": {"adx_trend_threshold": 25},
        }
    )


def test_optimizer_v0_apply_params_preserves_alias_backed_flags():
    cfg = _base_cfg()

    out = apply_search_params(cfg, {"range_filter.adx_trend_threshold": 35})

    assert out.stop_loss.enabled is False
    assert out.take_profit.enabled is False
    assert out.break_even.enabled is False
    assert out.multi_tp.enabled is False
    assert out.trailing.enabled is False
    assert out.range_filter.adx_trend_threshold == 35


def test_optuna_runner_apply_params_preserves_alias_backed_flags():
    cfg = _base_cfg()
    runner = OptimizationRunner(
        df=None,  # type: ignore[arg-type]
        base_config=cfg,
        param_space={},
    )

    out = runner._apply_params({"range_filter.adx_trend_threshold": 33})

    assert out.stop_loss.enabled is False
    assert out.take_profit.enabled is False
    assert out.break_even.enabled is False
    assert out.multi_tp.enabled is False
    assert out.trailing.enabled is False
    assert out.range_filter.adx_trend_threshold == 33


def test_random_search_serializes_base_config_with_aliases(monkeypatch):
    seen = {}

    def fake_run_single_trial(idx, params, base_config_dict, *args, **kwargs):
        seen["stop_loss"] = dict(base_config_dict["stop_loss"])
        seen["take_profit"] = dict(base_config_dict["take_profit"])
        return TrialResult(
            idx=idx,
            params=params,
            score=0.0,
            net_profit=0.0,
            max_dd_pct=0.0,
            total_trades=100,
            win_rate=0.0,
            profit_factor=0.0,
            runtime_s=0.0,
            status="OK",
        )

    monkeypatch.setattr("src.optimizer_v0.search.run_single_trial", fake_run_single_trial)

    random_search(
        df=pd.DataFrame({"timestamp": []}),
        base_config=_base_cfg(),
        param_defs=[ParamDef("range_filter.adx_trend_threshold", 25, 25, 1, "int")],
        n_iters=1,
        workers=1,
        min_trades=1,
        max_dd_pct=100.0,
    )

    assert seen["stop_loss"]["use_sl"] is False
    assert seen["take_profit"]["use_tp"] is False
