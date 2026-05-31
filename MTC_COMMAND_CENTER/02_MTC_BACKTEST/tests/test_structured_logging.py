from __future__ import annotations

import json
from pathlib import Path

from src.common.logging import get_correlation_id, set_correlation_id, setup_logging


def test_setup_logging_structured_writes_json_lines(tmp_path: Path):
    logger = setup_logging(
        level="INFO",
        log_dir=str(tmp_path),
        log_file="structured.log",
        structured=True,
        correlation_id="cid-test-1",
    )
    logger.info("hello-structured")

    log_path = tmp_path / "structured.log"
    lines = [line for line in log_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    payloads = [json.loads(line) for line in lines]
    assert any(p["message"] == "hello-structured" for p in payloads)
    assert all("correlation_id" in p for p in payloads)
    assert any(p["correlation_id"] == "cid-test-1" for p in payloads)


def test_correlation_id_setter_getter_roundtrip():
    set_correlation_id("cid-roundtrip")
    assert get_correlation_id() == "cid-roundtrip"
