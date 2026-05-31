from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def load_trials(path: Path) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(
                {
                    "trial_id": float(row.get("trial_id", "0")),
                    "net_profit": float(row.get("net_profit", "0")),
                    "max_dd_pct": float(row.get("max_dd_pct", "0")),
                }
            )
    return rows


def write_scatter_html(rows: list[dict[str, float]], out_html: Path) -> None:
    try:
        import plotly.express as px
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("plotly is required to generate chart output") from exc

    fig = px.scatter(rows, x="max_dd_pct", y="net_profit", hover_data=["trial_id"], title="Profit vs Max Drawdown")
    out_html.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(out_html), include_plotlyjs="cdn")


def write_summary_json(rows: list[dict[str, float]], out_json: Path) -> None:
    payload = {
        "count": len(rows),
        "best_net_profit": max((r["net_profit"] for r in rows), default=0.0),
        "best_profit_trial_id": max(rows, key=lambda r: r["net_profit"], default={"trial_id": 0.0})["trial_id"],
        "min_drawdown_pct": min((r["max_dd_pct"] for r in rows), default=0.0),
    }
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate optimizer visual report artifacts.")
    parser.add_argument("--trials", required=True)
    parser.add_argument("--out-html", required=True)
    parser.add_argument("--out-summary", required=True)
    args = parser.parse_args()

    rows = load_trials(Path(args.trials))
    write_scatter_html(rows, Path(args.out_html))
    write_summary_json(rows, Path(args.out_summary))
    print("Charts generated: PASS")


if __name__ == "__main__":
    main()
