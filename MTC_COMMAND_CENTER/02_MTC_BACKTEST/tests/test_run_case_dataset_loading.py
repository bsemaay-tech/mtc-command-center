"""Regression tests for dataset normalization in scripts/run_case.py."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pandas as pd
import pytest


def _load_run_case_module():
    mod_path = Path(__file__).resolve().parent.parent / "scripts" / "run_case.py"
    spec = importlib.util.spec_from_file_location("run_case_module", mod_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["run_case_module"] = module
    spec.loader.exec_module(module)
    return module


def test_load_dataset_accepts_datetimeindex_parquet(tmp_path: Path):
    pytest.importorskip("pyarrow")
    run_case = _load_run_case_module()

    idx = pd.date_range("2025-01-01", periods=4, freq="15min", tz="UTC")
    df = pd.DataFrame(
        {
            "open": [1.0, 2.0, 3.0, 4.0],
            "high": [1.1, 2.1, 3.1, 4.1],
            "low": [0.9, 1.9, 2.9, 3.9],
            "close": [1.05, 2.05, 3.05, 4.05],
            "volume": [10.0, 11.0, 12.0, 13.0],
        },
        index=idx,
    )
    # Keep index unnamed to cover "index" -> "timestamp" rename path.
    df.index.name = None

    p = tmp_path / "idx_only.parquet"
    df.to_parquet(p)

    loaded, used = run_case.load_dataset(str(p))
    assert used == p.resolve()
    assert "timestamp" in loaded.columns
    assert loaded["timestamp"].dt.tz is not None
    assert str(loaded["timestamp"].dt.tz) == "UTC"
    assert len(loaded) == len(df)


def test_load_dataset_raises_without_timestamp_axis(tmp_path: Path):
    run_case = _load_run_case_module()

    df = pd.DataFrame({"open": [1.0], "high": [1.1], "low": [0.9], "close": [1.0], "volume": [1.0]})
    p = tmp_path / "no_time.csv"
    df.to_csv(p, index=False)

    with pytest.raises(ValueError, match="no timestamp axis"):
        run_case.load_dataset(str(p))

