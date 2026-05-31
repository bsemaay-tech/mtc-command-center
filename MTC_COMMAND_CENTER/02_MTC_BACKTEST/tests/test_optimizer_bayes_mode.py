import pandas as pd
import pytest
from unittest.mock import MagicMock, patch

from src.optimizer_v0.search import ParamDef, TrialResult, bayes_search


def _fake_trial(
    idx,
    params,
    base_config_dict,
    warmup_bars,
    eval_start,
    eval_end,
    min_trades,
    max_dd_pct,
):
    # Deterministic synthetic objective: best near a=3, b=4.
    score = -abs(float(params["a"]) - 3.0) - abs(float(params["b"]) - 4.0)
    return TrialResult(
        idx=idx,
        params=params,
        score=score,
        net_profit=100.0 + score,
        max_dd_pct=10.0,
        total_trades=30,
        win_rate=50.0,
        profit_factor=1.2,
        runtime_s=0.01,
        status="OK",
    )


def test_bayes_search_is_seed_deterministic():
    df = pd.DataFrame({"timestamp": []})
    base_config = MagicMock()
    base_config.model_dump.return_value = {}
    defs = [
        ParamDef("a", low=1, high=5, step=1, dtype="int"),
        ParamDef("b", low=1, high=7, step=1, dtype="int"),
    ]

    with patch("src.optimizer_v0.search.run_single_trial", side_effect=_fake_trial):
        r1 = bayes_search(df, base_config, defs, n_init=3, n_iter=4, seed=123, workers=1)
        r2 = bayes_search(df, base_config, defs, n_init=3, n_iter=4, seed=123, workers=1)

    p1 = [x.params for x in r1]
    p2 = [x.params for x in r2]
    assert len(p1) == 7
    assert p1 == p2


def test_bayes_search_workers_guardrail():
    df = pd.DataFrame({"timestamp": []})
    base_config = MagicMock()
    defs = [ParamDef("a", low=1, high=3, step=1, dtype="int")]

    with pytest.raises(ValueError):
        bayes_search(df, base_config, defs, workers=2)
