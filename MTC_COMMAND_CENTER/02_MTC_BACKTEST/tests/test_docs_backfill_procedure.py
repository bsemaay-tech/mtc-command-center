from pathlib import Path


def test_historical_backfill_doc_exists_and_has_required_steps():
    doc = Path(__file__).resolve().parents[1] / "docs" / "historical_backfill_etl.md"
    assert doc.exists()
    text = doc.read_text(encoding="utf-8")
    assert "data_parity_guard.py" in text
    assert "checksum_registry.py" in text
    assert "build_dataset_catalog.py" in text
