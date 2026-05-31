import pytest
import sqlite3
import json
import pandas as pd
from pathlib import Path
from src.optimizer_v0 import pareto

def test_compute_pareto_logic():
    # Case 1: Simple domination
    # A: profit=10, dd=5  (Better profit, lower DD) -> Dominates B
    # B: profit=5,  dd=10 (Worse profit, higher DD)
    items = [
        {"net_profit": 10, "dd_pct": 5, "id": "A"},
        {"net_profit": 5,  "dd_pct": 10, "id": "B"},
    ]
    frontier = pareto.compute_pareto(items)
    assert len(frontier) == 1
    assert frontier[0]["id"] == "A"

    # Case 2: Trade-off (frontier)
    # A: profit=20, dd=20 (High risk/return)
    # B: profit=10, dd=5  (Low risk/return)
    # Neither dominates. Both should be in frontier.
    items = [
        {"net_profit": 20, "dd_pct": 20, "id": "A"},
        {"net_profit": 10, "dd_pct": 5,  "id": "B"},
    ]
    frontier = pareto.compute_pareto(items)
    assert len(frontier) == 2
    # Should be sorted by dd_pct ASC
    assert frontier[0]["id"] == "B" # (dd=5)
    assert frontier[1]["id"] == "A" # (dd=20)
    
    # Case 3: Equal DD, different profit
    # A: profit=10, dd=5
    # B: profit=8,  dd=5
    # A dominates B.
    items = [
        {"net_profit": 10, "dd_pct": 5, "id": "A"},
        {"net_profit": 8,  "dd_pct": 5, "id": "B"},
    ]
    frontier = pareto.compute_pareto(items)
    assert len(frontier) == 1
    assert frontier[0]["id"] == "A"

def test_load_trials_csv(tmp_path):
    csv = tmp_path / "test.csv"
    df = pd.DataFrame([
        {"idx": 1, "net_profit": 100, "max_dd_pct": 5, "status": "OK", "p1": 1},
        {"idx": 2, "net_profit": 50, "max_dd_pct": 2, "status": "OK", "p1": 2},
        {"idx": 3, "net_profit": 0, "max_dd_pct": 0, "status": "PRUNED", "p1": 3},
    ])
    df.to_csv(csv, index=False)
    
    # Load OK only
    trials = pareto.load_trials_from_csv(csv, include_pruned=False)
    assert len(trials) == 2
    assert trials[0]["net_profit"] == 100
    assert trials[0]["dd_pct"] == 5
    assert trials[0]["params"] == {"p1": 1}

    # Load All
    trials_all = pareto.load_trials_from_csv(csv, include_pruned=True)
    assert len(trials_all) == 3

def test_write_pareto_json(tmp_path):
    out = tmp_path / "pareto.json"
    payload = {"source": "test", "items": [{"a": 1}]}
    pareto.write_pareto_json(out, payload)
    
    assert out.exists()
    content = json.loads(out.read_text("utf-8"))
    assert content["source"] == "test"
    assert content["items"][0]["a"] == 1


def test_compute_pareto_multi_objective():
    # B dominates A on all maximize metrics and has lower DD.
    items = [
        {"id": "A", "net_profit": 100, "max_dd_pct": 12, "profit_factor": 1.2, "win_rate": 45, "total_trades": 50},
        {"id": "B", "net_profit": 110, "max_dd_pct": 10, "profit_factor": 1.3, "win_rate": 47, "total_trades": 55},
        # C is a trade-off point (higher profit but higher DD and lower WR).
        {"id": "C", "net_profit": 130, "max_dd_pct": 18, "profit_factor": 1.25, "win_rate": 44, "total_trades": 52},
    ]

    frontier = pareto.compute_pareto(
        items,
        maximize=["net_profit", "profit_factor", "win_rate", "total_trades"],
        minimize=["max_dd_pct"],
    )
    ids = [x["id"] for x in frontier]
    assert "A" not in ids
    assert "B" in ids
    assert "C" in ids


def test_compute_pareto_alias_dd_pct():
    items = [
        {"id": "A", "net_profit": 100, "dd_pct": 8},
        {"id": "B", "net_profit": 95, "max_dd_pct": 7},
    ]
    frontier = pareto.compute_pareto(items, maximize=["net_profit"], minimize=["max_dd_pct"])
    assert len(frontier) == 2
