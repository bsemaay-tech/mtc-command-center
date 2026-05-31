from datetime import datetime, timezone

from src.ui.dataset_defaults import choose_default_dataset


def test_choose_default_dataset_prefers_wider_span():
    datasets = [
        {
            "filename": "short.parquet",
            "bar_count": 1000,
            "start_date": datetime(2025, 1, 1, tzinfo=timezone.utc),
            "end_date": datetime(2025, 6, 1, tzinfo=timezone.utc),
        },
        {
            "filename": "long.parquet",
            "bar_count": 800,
            "start_date": datetime(2024, 1, 1, tzinfo=timezone.utc),
            "end_date": datetime(2026, 1, 1, tzinfo=timezone.utc),
        },
    ]
    assert choose_default_dataset(datasets) == "long.parquet"


def test_choose_default_dataset_handles_empty():
    assert choose_default_dataset([]) is None
