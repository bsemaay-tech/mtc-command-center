"""Tests for the Package 5a observability audit/export pack.

Builds the synthetic v4-shaped fixture store AT TEST TIME (no .db binary is
committed), runs the export against it, and asserts:

- the schema version is read from meta and reported,
- table row counts match the fixture builder's row data,
- recent orders/events row bounds are respected (including clamping),
- missing tables / missing meta keys / malformed values / unreadable stores
  / missing log paths are all handled as explicit REPORTED gaps — never
  invented data.

No bridge code is imported anywhere in this file.
"""

from __future__ import annotations

import importlib.util
import shutil
import sqlite3
import sys
from pathlib import Path

import pytest

OBS_DIR = Path(__file__).resolve().parents[1]
if str(OBS_DIR) not in sys.path:
    sys.path.insert(0, str(OBS_DIR))

import export_audit_pack as eap  # noqa: E402


def _load_builder():
    path = OBS_DIR / "fixtures" / "build_fixture_store.py"
    spec = importlib.util.spec_from_file_location("build_fixture_store", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


BUILDER = _load_builder()

TIMESTAMP = "2026-08-18T01:02:03Z"


@pytest.fixture()
def fixture_store(tmp_path: Path) -> Path:
    out = tmp_path / "fixture.db"
    BUILDER.build_fixture_store(out)
    return out


def _section(pack: str, title: str) -> str:
    """Return the Markdown text between `## <title>` and the next `## `."""
    start_marker = f"## {title}"
    assert start_marker in pack, f"section {title!r} missing from pack"
    start = pack.index(start_marker) + len(start_marker)
    rest = pack[start:]
    end = rest.index("\n## ")
    return rest[:end]


def _data_row_count(section: str) -> int:
    """Count Markdown table data rows (header row excluded).

    Only lines starting with ``"| "`` are counted; the separator row starts
    with ``"|-"`` and so never matches.
    """
    table_lines = [ln for ln in section.splitlines() if ln.startswith("| ")]
    assert table_lines, "expected a table with at least a header row"
    return len(table_lines) - 1


def _drop_table(store: Path, table: str) -> None:
    conn = sqlite3.connect(str(store))
    try:
        conn.execute(f'DROP TABLE "{table}"')
        conn.commit()
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Happy path: healthy fixture store
# ---------------------------------------------------------------------------

class TestHealthyFixture:
    def test_pack_is_one_markdown_document(self, fixture_store: Path) -> None:
        pack = eap.build_audit_pack(str(fixture_store), timestamp=TIMESTAMP)
        assert pack.startswith("# Bridge V2 Observability — Audit/Export Pack")
        assert pack.rstrip().endswith("*")

    def test_schema_version_reported_from_meta(self, fixture_store: Path) -> None:
        pack = eap.build_audit_pack(str(fixture_store), timestamp=TIMESTAMP)
        assert "schema_version (from meta): `4`" in pack

    def test_healthy_fixture_has_no_gaps(self, fixture_store: Path) -> None:
        pack = eap.build_audit_pack(str(fixture_store), timestamp=TIMESTAMP)
        assert "No gaps reported." in pack
        assert "**[REPORTED]**" not in pack

    def test_all_v4_tables_present_with_row_counts(self, fixture_store: Path) -> None:
        pack = eap.build_audit_pack(str(fixture_store), timestamp=TIMESTAMP)
        for name, rows in BUILDER.TABLE_ROW_DATA.items():
            assert f"| {name} | {len(rows)} |" in pack, name

    def test_app_state_and_window_meta_reported(self, fixture_store: Path) -> None:
        pack = eap.build_audit_pack(str(fixture_store), timestamp=TIMESTAMP)
        assert "`DISARMED`" in pack
        for key in ("window_started_ts", "window_last_alive_ts"):
            assert key in pack
        # absent optional key reported as-is, never defaulted
        assert "*(not present)*" in pack  # window_interrupted_ts absent by design


# ---------------------------------------------------------------------------
# Bounds
# ---------------------------------------------------------------------------

class TestBounds:
    def test_default_recent_n_caps_rows(self, fixture_store: Path) -> None:
        pack = eap.build_audit_pack(str(fixture_store), timestamp=TIMESTAMP)
        orders = _section(pack, "Recent orders (most recent 50, bounded)")
        events = _section(pack, "Recent events (most recent 50, bounded)")
        assert _data_row_count(orders) == len(BUILDER.ORDERS_ROWS)  # 5 < 50
        assert _data_row_count(events) == len(BUILDER.EVENTS_ROWS)  # 8 < 50

    def test_small_recent_n_respected(self, fixture_store: Path) -> None:
        pack = eap.build_audit_pack(str(fixture_store), timestamp=TIMESTAMP, recent_n=3)
        orders = _section(pack, "Recent orders (most recent 3, bounded)")
        assert _data_row_count(orders) == 3
        # most-recent ordering: latest ts_submit first, rowid DESC breaking
        # the 00:15:00 tie (synth-sl-0002 was inserted after synth-entry-0002).
        # Section layout: [0]="" [1]="" [2]=table header [3]=separator [4:]=data.
        assert "synth-sl-0002" in orders.splitlines()[4]
        assert "synth-entry-0002" in orders.splitlines()[5]

    def test_huge_recent_n_clamped_to_max(self, fixture_store: Path) -> None:
        pack = eap.build_audit_pack(str(fixture_store), timestamp=TIMESTAMP,
                                    recent_n=10**9)
        assert f"clamped to {eap.MAX_RECENT_N}" in pack
        orders = _section(
            pack, f"Recent orders (most recent {eap.MAX_RECENT_N}, bounded)")
        assert _data_row_count(orders) == len(BUILDER.ORDERS_ROWS)

    def test_zero_recent_n_clamped_to_min(self, fixture_store: Path) -> None:
        pack = eap.build_audit_pack(str(fixture_store), timestamp=TIMESTAMP, recent_n=0)
        assert "clamped to 1" in pack
        orders = _section(pack, "Recent orders (most recent 1, bounded)")
        assert _data_row_count(orders) == 1


# ---------------------------------------------------------------------------
# Explicit REPORTED gaps — never invented data
# ---------------------------------------------------------------------------

class TestReportedGaps:
    def test_missing_table_is_reported(self, fixture_store: Path, tmp_path: Path) -> None:
        second = tmp_path / "missing_table.db"
        shutil.copyfile(fixture_store, second)
        _drop_table(second, "fills")

        pack = eap.build_audit_pack(str(second), timestamp=TIMESTAMP)
        assert "**[REPORTED]**" in pack
        assert "No gaps reported." not in pack
        assert "expected v4 baseline table missing: 'fills'" in pack
        # the dropped table's row count must NOT be invented
        assert "| fills |" not in pack

    def test_missing_orders_table_disables_recent_section(
        self, fixture_store: Path, tmp_path: Path
    ) -> None:
        second = tmp_path / "no_orders.db"
        shutil.copyfile(fixture_store, second)
        _drop_table(second, "orders")

        pack = eap.build_audit_pack(str(second), timestamp=TIMESTAMP)
        orders = _section(pack, "Recent orders (most recent 50, bounded)")
        assert "**[REPORTED]**" in orders
        assert "table 'orders' not present" in pack

    def test_missing_schema_version_key_is_reported(
        self, fixture_store: Path, tmp_path: Path
    ) -> None:
        second = tmp_path / "no_schema_version.db"
        shutil.copyfile(fixture_store, second)
        conn = sqlite3.connect(str(second))
        try:
            conn.execute("DELETE FROM meta WHERE key = 'schema_version'")
            conn.commit()
        finally:
            conn.close()

        pack = eap.build_audit_pack(str(second), timestamp=TIMESTAMP)
        assert "meta key 'schema_version' missing" in pack
        assert "schema_version (from meta): **[REPORTED]**" in pack
        # app_state is unaffected and still reported honestly
        assert "`DISARMED`" in pack

    def test_malformed_schema_version_is_reported(
        self, fixture_store: Path, tmp_path: Path
    ) -> None:
        second = tmp_path / "malformed.db"
        shutil.copyfile(fixture_store, second)
        conn = sqlite3.connect(str(second))
        try:
            conn.execute("UPDATE meta SET value = 'four' WHERE key = 'schema_version'")
            conn.commit()
        finally:
            conn.close()

        pack = eap.build_audit_pack(str(second), timestamp=TIMESTAMP)
        assert "malformed" in pack
        assert "schema_version (from meta): **[REPORTED]** — malformed value" in pack
        # raw malformed value still surfaced as-is
        assert "`four`" in pack

    def test_nonexistent_store_is_reported_not_crashed(self, tmp_path: Path) -> None:
        missing = tmp_path / "does_not_exist.db"
        pack = eap.build_audit_pack(str(missing), timestamp=TIMESTAMP)
        assert "**[REPORTED]** — store unreadable" in pack
        # read-only mode must never create the file
        assert not missing.exists()


# ---------------------------------------------------------------------------
# Timestamp, logs, CLI
# ---------------------------------------------------------------------------

class TestTimestampLogsCli:
    def test_caller_supplied_timestamp_in_header(self, fixture_store: Path) -> None:
        pack = eap.build_audit_pack(str(fixture_store), timestamp=TIMESTAMP)
        assert f"report timestamp (caller-supplied): `{TIMESTAMP}`" in pack

    def test_absent_timestamp_is_never_invented(self, fixture_store: Path) -> None:
        pack = eap.build_audit_pack(str(fixture_store))
        assert "NOT SUPPLIED" in pack

    def test_log_tail_included_and_missing_log_reported(
        self, fixture_store: Path, tmp_path: Path
    ) -> None:
        log = tmp_path / "bridge.log"
        log.write_text(
            "\n".join(f"synthetic log line {i}" for i in range(1, 11)) + "\n",
            encoding="utf-8",
        )
        missing_log = tmp_path / "nope.log"

        pack = eap.build_audit_pack(
            str(fixture_store),
            log_paths=(str(log), str(missing_log)),
            timestamp=TIMESTAMP,
        )
        assert "synthetic log line 10" in pack
        assert "log path not found" in pack
        assert "**[REPORTED]**" in pack

    def test_main_cli_writes_output_file(
        self, fixture_store: Path, tmp_path: Path
    ) -> None:
        out = tmp_path / "packs" / "audit.md"
        rc = eap.main([
            "--store", str(fixture_store),
            "--timestamp", TIMESTAMP,
            "--recent-n", "10",
            "--out", str(out),
        ])
        assert rc == 0
        assert out.exists()
        text = out.read_text(encoding="utf-8")
        assert text.startswith("# Bridge V2 Observability — Audit/Export Pack")
        assert "schema_version (from meta): `4`" in text
        assert "No gaps reported." in text

    def test_main_cli_requires_explicit_store(self, tmp_path: Path) -> None:
        with pytest.raises(SystemExit) as excinfo:
            eap.main(["--timestamp", TIMESTAMP])
        assert excinfo.value.code == 2  # argparse: missing required --store
