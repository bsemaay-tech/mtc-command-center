"""Independent D-13 probe for the exact T0 read of b4df1413.

RED: the real adapter refuses the raw collector partition.
GREEN: the real adapter accepts the exported partition, and the capture is bound to the receipt.
DEPENDENCE: mutating one byte of the published export must make the same adapter refuse.
Also prints the publication order actually observed (receipt name taken before the target name).
"""

from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path

import check_market_data_collector as collector_fixtures
import market_data_collector
import p030_archive_exporter as exporter
import p030_closed_partition_backup_adapter as adapter

EXPORTED_AT = "2026-09-14T00:00:00Z"
CAPTURED_AT = "2026-09-14T00:01:00Z"


def collector_partition(root: Path) -> tuple[Path, Path]:
    source_root = root / "collector-root"
    archive = market_data_collector.MonthlyArchive(source_root)
    now = collector_fixtures.JANUARY_LAST_BAR + 10 * collector_fixtures.STEP
    base = collector_fixtures.PERSISTED_ORDER_BASE
    for offset in (0, 1):
        bar = market_data_collector.normalize_bar(
            collector_fixtures.raw_bar(base + offset * collector_fixtures.STEP),
            source_producer="WS_LIVE",
            ingest_time=now,
            env_lineage_id="fixture-lineage",
            identities=collector_fixtures.IDENTITIES,
        )
        assert archive.append_bar(bar) == "APPENDED"
    source = source_root / "bars" / "HYPERLIQUID" / "BTC" / "15m" / "2026-02.jsonl"
    return source_root, source


def capture(path: Path, out: Path, root: Path, dataset_hash: str) -> Path:
    return adapter.capture_stable_prefix(
        path,
        out,
        source_root=root,
        high_water_bytes=path.stat().st_size,
        captured_at_utc=CAPTURED_AT,
        dataset_content_hash=dataset_hash,
    )


def main() -> None:
    print("adapter module under test:", adapter.__file__)
    print("capture_stable_prefix is the real adapter function:", adapter.capture_stable_prefix.__module__)
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        source_root, source = collector_partition(root)
        target = root / "export-root" / "exported.jsonl"
        receipt = exporter.export_partition(
            source, target, source_root=source_root, exported_at_utc=EXPORTED_AT
        )

        # RED: the raw collector partition, through the real adapter
        try:
            capture(source, root / "raw-stable", source_root, receipt.dataset_content_hash)
            print("D-13 RED: ADAPTER ACCEPTED THE RAW PARTITION  <-- would be a failure")
        except ValueError as error:
            print(f"D-13 RED  raw partition refused by the adapter: {error}")

        # GREEN: the exported partition, through the same function
        stable_receipt = capture(
            target, root / "exported-stable", target.parent, receipt.dataset_content_hash
        )
        stable = json.loads(stable_receipt.read_text(encoding="utf-8"))
        published = hashlib.sha256(target.read_bytes()).hexdigest()
        print(f"D-13 GREEN exported partition accepted, record_count={stable['record_count']}")
        print(f"   receipt.exported_sha256 = {receipt.exported_sha256}")
        print(f"   capture prefix_sha256   = {stable['prefix_sha256']}")
        print(f"   sha256(published bytes) = {published}")
        print(
            "   N3 binding holds:",
            receipt.exported_sha256 == stable["prefix_sha256"] == published,
        )
        print(
            "   dataset_content_hash equal:",
            stable["dataset_content_hash"] == receipt.dataset_content_hash,
        )

        # DEPENDENCE: mutate one byte of the published export -> the same adapter must refuse
        mutated_root = root / "mutated-root"
        mutated_root.mkdir()
        mutated = mutated_root / "exported.jsonl"
        raw = target.read_bytes()
        rows = raw.split(b"\n")
        first = json.loads(rows[0])
        first["open"] = first["open"] + "0"  # still a decimal string, different bytes
        rows[0] = json.dumps(first, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
        mutated.write_bytes(b"\n".join(rows))
        try:
            capture(mutated, root / "mutated-stable", mutated_root, receipt.dataset_content_hash)
            print("D-13 DEPENDENCE: ADAPTER ACCEPTED MUTATED EXPORT  <-- would be a failure")
        except ValueError as error:
            print(f"D-13 DEPENDENCE mutated export refused: {error}")

        # a byte-level tamper that keeps the identity fields untouched
        tampered_root = root / "tampered-root"
        tampered_root.mkdir()
        tampered = tampered_root / "exported.jsonl"
        tampered.write_bytes(raw.replace(b'"track"', b'"TRACK"', 1))
        try:
            capture(tampered, root / "tampered-stable", tampered_root, receipt.dataset_content_hash)
            print("D-13 DEPENDENCE(2): ADAPTER ACCEPTED KEY-CASE TAMPER  <-- would be a failure")
        except ValueError as error:
            print(f"D-13 DEPENDENCE(2) key-case tamper refused: {error}")

    # publication order, observed
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        source_root, source = collector_partition(root)
        target = root / "order" / "p.jsonl"
        order: list[str] = []
        real_publish = exporter._publish

        def watched(staging: Path, final: Path) -> None:
            order.append(Path(final).name)
            return real_publish(staging, final)

        exporter._publish = watched
        try:
            exporter.export_partition(
                source, target, source_root=source_root, exported_at_utc=EXPORTED_AT
            )
        finally:
            exporter._publish = real_publish
        print("publication order observed:", order)


if __name__ == "__main__":
    main()
