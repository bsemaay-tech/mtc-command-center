import json
from pathlib import Path

from scripts.compare_objective_reports import compare, load_metric_rows, summarize
from scripts.export_pareto_buckets import bucket_top_k
from scripts.generate_optimizer_charts import load_trials, write_summary_json


def test_compare_objective_reports_summary(tmp_path: Path):
    csv_a = tmp_path / "a.csv"
    csv_b = tmp_path / "b.csv"
    csv_a.write_text(
        "trial_id,net_profit,max_dd_pct,profit_factor,win_rate,total_trades\n"
        "1,10,20,1.1,40,100\n",
        encoding="utf-8",
    )
    csv_b.write_text(
        "trial_id,net_profit,max_dd_pct,profit_factor,win_rate,total_trades\n"
        "1,20,10,1.3,45,120\n",
        encoding="utf-8",
    )

    a = summarize(load_metric_rows(csv_a))
    b = summarize(load_metric_rows(csv_b))
    d = compare(a, b)
    assert d["net_profit_mean"] == 10.0
    assert d["max_dd_pct_mean"] == -10.0


def test_export_pareto_buckets_top_k():
    rows = [
        {"trial_id": 1, "net_profit": 100, "max_dd_pct": 10},
        {"trial_id": 2, "net_profit": 90, "max_dd_pct": 12},
        {"trial_id": 3, "net_profit": 80, "max_dd_pct": 20},
        {"trial_id": 4, "net_profit": 70, "max_dd_pct": 40},
    ]
    buckets = bucket_top_k(rows, top_k=1)
    assert buckets["low_risk"][0]["trial_id"] == 1
    assert buckets["mid_risk"][0]["trial_id"] == 3
    assert buckets["high_risk"][0]["trial_id"] == 4


def test_generate_optimizer_chart_summary(tmp_path: Path):
    trials = tmp_path / "trials.csv"
    trials.write_text(
        "trial_id,net_profit,max_dd_pct\n"
        "1,10,20\n"
        "2,30,15\n",
        encoding="utf-8",
    )
    rows = load_trials(trials)
    out = tmp_path / "summary.json"
    write_summary_json(rows, out)
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["count"] == 2
    assert payload["best_net_profit"] == 30.0
