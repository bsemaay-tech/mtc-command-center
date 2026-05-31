import json
from pathlib import Path

from scripts.build_dataset_catalog import build_catalog, write_csv


def test_build_catalog_has_expected_keys():
    rows = build_catalog(Path("data"))
    assert isinstance(rows, list)
    if rows:
        sample = rows[0]
        assert "filename" in sample
        assert "symbol" in sample
        assert "timeframe" in sample


def test_write_csv_writes_header(tmp_path: Path):
    rows = [
        {
            "filename": "x.parquet",
            "symbol": "BTCUSDT",
            "timeframe": "15m",
            "format": "parquet",
            "size_bytes": 10,
            "bar_count": 1,
            "start_date": "2025-01-01",
            "end_date": "2025-01-01",
            "path": "data/x.parquet",
        }
    ]
    out = tmp_path / "catalog.csv"
    write_csv(out, rows)
    text = out.read_text(encoding="utf-8")
    assert "filename,symbol,timeframe" in text
