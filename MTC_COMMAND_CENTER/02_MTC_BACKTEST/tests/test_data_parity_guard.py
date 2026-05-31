import hashlib
from pathlib import Path

import pytest
import pandas as pd

from scripts.data_parity_guard import (
    compute_timestamp_quality,
    normalize_exchange,
    normalize_symbol,
    parse_timeframe,
    validate_expected_sha256,
)


def test_normalize_symbol_perp_suffixes():
    assert normalize_symbol("BTCUSDT.P") == "BTCUSDT"
    assert normalize_symbol("ethusdt.perp") == "ETHUSDT"
    assert normalize_symbol("SOLUSDT-PERP") == "SOLUSDT"


def test_normalize_symbol_with_exchange_prefix():
    assert normalize_symbol("BINANCE:BTCUSDT.P") == "BTCUSDT"


def test_normalize_exchange_uppercase():
    assert normalize_exchange("binance") == "BINANCE"


def test_expect_sha256_check(tmp_path: Path):
    p = tmp_path / "dataset.txt"
    p.write_text("abc", encoding="utf-8")
    actual = hashlib.sha256(b"abc").hexdigest()

    from scripts.data_parity_guard import sha256_file

    assert sha256_file(p) == actual


def test_expect_sha256_mismatch_message(tmp_path: Path):
    p = tmp_path / "dataset.txt"
    p.write_text("abc", encoding="utf-8")

    with pytest.raises(ValueError, match="Checksum mismatch: expected="):
        validate_expected_sha256(p, "deadbeef")


def test_parse_timeframe_units():
    assert parse_timeframe("15m").total_seconds() == 900
    assert parse_timeframe("1h").total_seconds() == 3600
    assert parse_timeframe("1d").total_seconds() == 86400


def test_compute_timestamp_quality_detects_duplicate_and_gap():
    ts = pd.to_datetime(
        [
            "2026-01-01T00:00:00Z",
            "2026-01-01T00:15:00Z",
            "2026-01-01T00:15:00Z",  # duplicate
            "2026-01-01T01:00:00Z",  # gap from expected 15m cadence
        ],
        utc=True,
    )
    quality = compute_timestamp_quality(pd.Series(ts), parse_timeframe("15m"))
    assert quality["duplicate_timestamps"] == 1
    assert quality["gap_count"] == 1
