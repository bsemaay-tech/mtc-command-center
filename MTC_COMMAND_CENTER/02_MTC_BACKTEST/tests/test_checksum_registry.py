from __future__ import annotations

from pathlib import Path

import pytest

from scripts.checksum_registry import (
    load_registry,
    save_registry,
    upsert_dataset_entry,
    verify_dataset_entry,
)


def test_upsert_and_save_registry(tmp_path: Path):
    dataset = tmp_path / "sample.csv"
    dataset.write_text("a,b\n1,2\n", encoding="utf-8")
    registry_path = tmp_path / "registry.json"

    registry = load_registry(registry_path)
    entry = upsert_dataset_entry(
        registry,
        dataset,
        symbol="BTCUSDT",
        exchange="BINANCE",
        timeframe="15m",
    )
    save_registry(registry_path, registry)

    reloaded = load_registry(registry_path)
    key = str(dataset.resolve())
    assert key in reloaded["items"]
    assert reloaded["items"][key]["sha256"] == entry["sha256"]
    assert reloaded["items"][key]["symbol"] == "BTCUSDT"


def test_verify_detects_checksum_mismatch(tmp_path: Path):
    dataset = tmp_path / "sample.csv"
    dataset.write_text("a,b\n1,2\n", encoding="utf-8")
    registry = load_registry(tmp_path / "registry.json")
    upsert_dataset_entry(registry, dataset)

    assert verify_dataset_entry(registry, dataset) is True

    dataset.write_text("a,b\n9,9\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Checksum mismatch"):
        verify_dataset_entry(registry, dataset)
