from pathlib import Path

import pytest

from scripts.artifact_guard import validate_csv


def test_validate_csv_missing(tmp_path):
    with pytest.raises(FileNotFoundError):
        validate_csv(tmp_path / "missing.csv")


def test_validate_csv_empty(tmp_path):
    p = tmp_path / "x.csv"
    p.write_text("", encoding="utf-8")
    with pytest.raises(ValueError):
        validate_csv(p)


def test_validate_csv_ok(tmp_path):
    p = tmp_path / "x.csv"
    p.write_text("a,b\n1,2\n", encoding="utf-8")
    validate_csv(p)


def test_validate_csv_blank_header_message(tmp_path):
    p = tmp_path / "x.csv"
    p.write_text("\n1,2\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Corrupt artifact \\(blank header\\):"):
        validate_csv(p)
