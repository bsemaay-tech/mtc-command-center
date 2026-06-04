import subprocess
import sys
from pathlib import Path

import pandas as pd

from src.data.io import save_dataset


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_mtc_engine_validate_help_works():
    completed = subprocess.run(
        [sys.executable, "-m", "src.cli.mtc_engine_validate", "--help"],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
    )

    assert completed.returncode == 0
    assert "MTC-Engine Validation" in completed.stdout or "MTCRunner" in completed.stdout


def test_mtc_engine_validate_small_dataset_run(tmp_path):
    rows = []
    ts = pd.date_range("2025-01-01", periods=120, freq="15min", tz="UTC")
    for i, t in enumerate(ts):
        close = 100.0 + (i * 0.1)
        rows.append(
            {
                "timestamp": t,
                "open": close - 0.1,
                "high": close + 0.5,
                "low": close - 0.5,
                "close": close,
                "volume": 1000.0,
            }
        )
    data_path = tmp_path / "sample.csv"
    save_dataset(pd.DataFrame(rows), data_path, format="csv")

    outdir = tmp_path / "out"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "src.cli.mtc_engine_validate",
            "--producer",
            "supertrend",
            "--data",
            str(data_path),
            "--symbol",
            "TEST",
            "--timeframe",
            "15m",
            "--warmup",
            "20",
            "--output",
            str(outdir),
        ],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (outdir / "report.md").exists()
    assert (outdir / "results.json").exists()
    assert (outdir / "trades.csv").exists()
