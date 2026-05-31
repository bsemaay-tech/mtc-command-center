import pytest

from src.optimizer_v0.__main__ import _parse_objectives


def test_parse_objectives_splits_minimize_and_maximize():
    maximize, minimize = _parse_objectives("net_profit,max_dd_pct,profit_factor,total_trades")
    assert maximize == ["net_profit", "profit_factor", "total_trades"]
    assert minimize == ["max_dd_pct"]


def test_parse_objectives_requires_known_metrics():
    with pytest.raises(ValueError):
        _parse_objectives("net_profit,foo_metric,max_dd_pct")
