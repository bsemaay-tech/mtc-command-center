"""Independent RED probes for the exact T0 read of b4df1413 (K-01..K-03 + the N3 binding)."""

from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path

import p030_archive_exporter as exporter
import p030_closed_partition_backup_adapter as adapter
from d13_probe import CAPTURED_AT, EXPORTED_AT, collector_partition


def attempt(label: str, root: Path, mutate, *, exported_at=EXPORTED_AT) -> None:
    source_root, source = collector_partition(root)
    mutate(source)
    target = root / "out" / "p.jsonl"
    receipt = Path(str(target) + ".p030export.json")
    staging = Path(str(target) + exporter.STAGING_SUFFIX)
    try:
        exporter.export_partition(
            source, target, source_root=source_root, exported_at_utc=exported_at
        )
        outcome = "EXPORTED (no refusal)"
        code = "-"
    except exporter.ExportRefused as refused:
        outcome = f"ExportRefused: {refused}"
        code = refused.code
    except BaseException as other:  # a raw exception is the thing we are hunting
        outcome = f"RAW {type(other).__name__}: {other}"
        code = "RAW"
    print(
        f"{label:<34} code={code:<22} target_exists={target.exists()} "
        f"receipt_exists={receipt.exists()} staging_exists={staging.exists()}"
    )
    print(f"    -> {outcome}")


def rows_of(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def write_rows(path: Path, rows) -> None:
    path.write_text(
        "".join(
            json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n"
            for row in rows
        ),
        encoding="utf-8",
    )


def main() -> None:
    cases = [
        ("K-01 overflow literal 1e999", lambda s: s.write_bytes(s.read_bytes() + b'{"open":1e999}\n')),
        ("K-01 nested -1e999", lambda s: s.write_bytes(s.read_bytes() + b'{"a":{"b":[1,-1e999]}}\n')),
        ("K-01 NaN literal", lambda s: s.write_bytes(s.read_bytes() + b'{"open":NaN}\n')),
        ("K-01 Infinity literal", lambda s: s.write_bytes(s.read_bytes() + b'{"open":Infinity}\n')),
        ("duplicate JSON key", lambda s: s.write_bytes(s.read_bytes() + b'{"a":1,"a":2}\n')),
        ("K-02 contract refused (row)", lambda s: write_rows(s, [dict(r, open="not-a-decimal") for r in rows_of(s)])),
        ("K-02 contract refused (slice)", lambda s: write_rows(s, [rows_of(s)[0], rows_of(s)[0]])),
        ("no mutation (control)", lambda s: None),
    ]
    for label, mutate in cases:
        with tempfile.TemporaryDirectory() as temporary:
            attempt(label, Path(temporary), mutate)
    for stamp in ("2026-09-14T00:00:00.500Z", "2026-09-14T00:00:00.000001Z", "2026-09-14T00:00:00+00:00"):
        with tempfile.TemporaryDirectory() as temporary:
            attempt(f"K-03 timestamp {stamp}", Path(temporary), lambda s: None, exported_at=stamp)

    # N3: tamper with the published export before the capture -> the drill's binding must break
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        source_root, source = collector_partition(root)
        target = root / "export-root" / "p.jsonl"
        receipt = exporter.export_partition(
            source, target, source_root=source_root, exported_at_utc=EXPORTED_AT
        )
        rows = rows_of(target)
        rows[0]["open"] = rows[0]["open"] + "0"
        target.write_text(
            "".join(
                json.dumps(r, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
                for r in rows
            ),
            encoding="utf-8",
        )
        stable_receipt = adapter.capture_stable_prefix(
            target,
            root / "stable",
            source_root=target.parent,
            high_water_bytes=target.stat().st_size,
            captured_at_utc=CAPTURED_AT,
            dataset_content_hash=receipt.dataset_content_hash,
        )
        stable = json.loads(stable_receipt.read_text(encoding="utf-8"))
        print("\nN3 tamper-after-export:")
        print(f"    adapter accepted the tampered partition: True (record_count={stable['record_count']})")
        print(f"    prefix_sha256 == receipt.exported_sha256: {stable['prefix_sha256'] == receipt.exported_sha256}")
        print(f"    sha256(tampered bytes) = {hashlib.sha256(target.read_bytes()).hexdigest()[:16]}...")
        print(f"    receipt.exported_sha256 = {receipt.exported_sha256[:16]}...")


if __name__ == "__main__":
    main()
