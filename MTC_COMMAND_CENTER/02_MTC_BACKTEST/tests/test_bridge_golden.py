import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from src.data.io import save_dataset

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _oscillating_df(n: int = 400) -> pd.DataFrame:
    idx = pd.date_range("2025-01-01", periods=n, freq="15min", tz="UTC")
    # Drift + oscillation so Supertrend flips direction and trades occur.
    close = 100.0 + np.arange(n) * 0.05 + 5.0 * np.sin(np.arange(n) / 8.0)
    return pd.DataFrame(
        {
            "timestamp": idx,
            "open": close - 0.1,
            "high": close + 0.6,
            "low": close - 0.6,
            "close": close,
            "volume": 1000.0,
        }
    )


def _run(data_path: Path, outdir: Path) -> dict:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "src.cli.mtc_engine_validate",
            "--producer",
            "supertrend",
            "--data",
            str(data_path),
            "--warmup",
            "30",
            "--output",
            str(outdir),
        ],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
    )
    assert completed.returncode == 0, completed.stderr
    return json.loads((outdir / "results.json").read_text(encoding="utf-8"))


def test_bridge_metrics_are_deterministic(tmp_path):
    data_path = tmp_path / "osc.csv"
    save_dataset(_oscillating_df(), data_path, format="csv")

    first = _run(data_path, tmp_path / "run1")
    second = _run(data_path, tmp_path / "run2")

    m1 = first["metrics"]
    m2 = second["metrics"]

    # Same input -> identical engine output (deterministic snapshot).
    assert m1["strategy_return_pct"] == m2["strategy_return_pct"]
    assert m1["max_drawdown_pct"] == m2["max_drawdown_pct"]
    assert m1["total_trades"] == m2["total_trades"]
    assert m1["profit_factor"] == m2["profit_factor"]

    # Structural invariants the report depends on.
    assert first["profile"] == "light-risk"
    assert first["config_snapshot"]["filters_off"] is True
    assert first["config_snapshot"]["guards_off"] is True
    assert isinstance(m1["strategy_return_pct"], (int, float))
    assert "buy_hold_return_pct" in m1
    assert m1["excess_alpha_pct"] == m1["strategy_return_pct"] - m1["buy_hold_return_pct"]
