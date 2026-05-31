from __future__ import annotations

from datetime import datetime, timezone

from src.config.schema import TradeRecord
from src.parity.exporter import ParityExporter


def test_parity_exporter_records_extended_metadata() -> None:
    exporter = ParityExporter()
    effective_history_start = datetime(2025, 1, 1, tzinfo=timezone.utc)
    timestamp = datetime(2025, 1, 2, tzinfo=timezone.utc)

    exporter.record_bar(
        bar_index=10,
        timestamp_close_utc=timestamp,
        exit_reason="TP1",
        entry_reason="LONG_SIGNAL",
        exit_id="tp1",
        lifecycle_id="long_10",
        event_seq_in_bar=2,
        execution_profile_id="base_close_intrabar_protective_v1",
        working_exit_book_version=3,
        effective_history_start_utc=effective_history_start,
        warmup_bars=250,
        warmup_seeded=True,
        warmup_seed_provenance="st_atr_len=21|ma_length=200",
        close=100.0,
    )

    row = exporter.get_dataframe().iloc[0].to_dict()

    assert row["exit_id"] == "tp1"
    assert row["lifecycle_id"] == "long_10"
    assert row["event_seq_in_bar"] == 2
    assert row["execution_profile_id"] == "base_close_intrabar_protective_v1"
    assert row["working_exit_book_version"] == 3
    assert row["warmup_bars"] == 250
    assert row["warmup_seeded"] is True
    assert row["warmup_seed_provenance"] == "st_atr_len=21|ma_length=200"
    assert row["effective_history_start_utc"].startswith("2025-01-01T00:00:00")


def test_trade_record_accepts_optional_parity_metadata() -> None:
    trade = TradeRecord(
        trade_id=1,
        direction="long",
        entry_bar=10,
        entry_time=datetime(2025, 1, 2, tzinfo=timezone.utc),
        entry_price=100.0,
        exit_bar=11,
        exit_time=datetime(2025, 1, 2, 0, 15, tzinfo=timezone.utc),
        exit_price=101.0,
        quantity=1.25,
        pnl=1.25,
        pnl_pct=1.25,
        exit_reason="TP1",
        exit_id="tp1",
        lifecycle_id="long_10",
        event_seq_in_bar=1,
        execution_profile_id="base_close_intrabar_protective_v1",
        working_exit_book_version=2,
    )

    assert trade.exit_id == "tp1"
    assert trade.lifecycle_id == "long_10"
    assert trade.event_seq_in_bar == 1
    assert trade.execution_profile_id == "base_close_intrabar_protective_v1"
    assert trade.working_exit_book_version == 2
