"""Tests for tools/wal_state_bundle.py (KVM2 P2-06 / P4-05 state tooling).

Everything runs against throwaway databases under ``tmp_path``. No real
runtime, no C:\\P2RT, no service, no network.
"""

from __future__ import annotations

import copy
import json
import shutil
import sqlite3
import threading
from contextlib import closing
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

import pytest

from bridge.store.db import Store
from tools import wal_state_bundle as wal

TS = "2026-07-26T00:00:00Z"


# ---------------------------------------------------------------------------
# fixtures
# ---------------------------------------------------------------------------


def _seed(store: Store, run_id: str = "paper-1", losses: int = 3) -> None:
    """A database with real risk history: closed losing trades in a streak,
    one open trade, one live order, and a risk_days ledger."""
    store.initialize()
    store.set_meta("app_state", "DISARMED")
    store.create_run(run_id, "paper", "testnet", {"strategy": "keltner_trail_ema8"})

    base = datetime(2026, 7, 20, 12, 0, tzinfo=UTC)
    for i in range(losses):
        trade_id = store.create_trade(
            run_id=run_id,
            coin="BTC",
            direction="LONG",
            qty=0.01,
            entry_decision_uid=f"dec-{i}",
            signal_ts=base + timedelta(hours=i),
            decision_ts=base + timedelta(hours=i),
            expected_px=60000.0,
            risk_dollars=50.0,
            risk_pct=0.005,
            leverage=1,
            sl_initial=59000.0,
            tp_initial=None,
            llm_directive_id=None,
        )
        store.update_trade_exit(
            trade_id=trade_id,
            exit_px=59500.0,
            exit_ts=base + timedelta(hours=i, minutes=30),
            exit_reason="STOP",
            pnl=-5.0 - i,
        )
        store.insert_order(
            cloid=f"cloid-{i}",
            oid=1000 + i,
            group_id=None,
            order_ref=f"ref-{i}",
            order_json={"symbol": "BTC", "trigger_px": None},
            decision_uid=f"dec-{i}",
            trade_id=trade_id,
            role="ENTRY",
            status="FILLED",
            qty=0.01,
            filled_qty=0.01,
            avg_fill_px=60000.0,
            ts_submit=base + timedelta(hours=i),
        )
        store.insert_fill(
            fill_id=f"fill-{i}",
            cloid=f"cloid-{i}",
            decision_uid=f"dec-{i}",
            fill_ts=base + timedelta(hours=i, minutes=1),
            qty=0.01,
            px=60000.0,
            fee=0.05,
            funding=0.0,
        )

    # one still-open trade plus a live order: a fresh database would lose both
    store.create_trade(
        run_id=run_id,
        coin="BTC",
        direction="LONG",
        qty=0.02,
        entry_decision_uid="dec-open",
        signal_ts=base + timedelta(days=1),
        decision_ts=base + timedelta(days=1),
        expected_px=61000.0,
        risk_dollars=50.0,
        risk_pct=0.005,
        leverage=1,
        sl_initial=60000.0,
        tp_initial=None,
        llm_directive_id=None,
    )
    store.insert_order(
        cloid="cloid-live",
        oid=2000,
        group_id=None,
        order_ref="ref-live",
        order_json={"symbol": "BTC", "trigger_px": 60000.0},
        decision_uid="dec-open",
        trade_id=None,
        role="STOP",
        status="OPEN",
        qty=0.02,
        ts_submit=base + timedelta(days=1),
    )
    store.upsert_risk_day(
        trading_date="2026-07-20",
        day_start_equity=100000.0,
        realized_pnl_engine=-18.0,
        realized_pnl_broker=-18.0,
        max_intraday_dd=-25.0,
        consecutive_losses_end=losses,
        auto_rearms_used=1,
    )


@pytest.fixture()
def source_db(tmp_path: Path) -> Path:
    db = tmp_path / "src" / "bridge.db"
    store = Store(db)
    _seed(store)
    store.close()
    return db


@pytest.fixture()
def bundle_dir(tmp_path: Path) -> Path:
    return tmp_path / "bundle"


def create(source: Path, out: Path, capsys, *extra: str) -> tuple[int, dict]:
    rc = wal.main(["create", "--source", str(source), "--out-dir", str(out),
                   "--timestamp", TS, *extra])
    captured = capsys.readouterr()
    report = json.loads(captured.out) if captured.out.strip() else {}
    return rc, report


def verify(out: Path, capsys, *extra: str) -> tuple[int, dict]:
    arguments = ["verify", "--bundle-dir", str(out), *extra]
    if "--expect-bundle-sha256" not in extra or "--expect-invariants-sha256" not in extra:
        try:
            manifest = read_manifest(out)
        except (FileNotFoundError, json.JSONDecodeError):
            manifest = None
        if manifest is not None:
            if "--expect-bundle-sha256" not in extra:
                bundle_hash = (
                    manifest.get("bundle", {}).get("db_sha256", "0" * 64)
                    if isinstance(manifest, dict)
                    else "0" * 64
                )
                arguments.extend(
                    ["--expect-bundle-sha256", bundle_hash]
                )
            if "--expect-invariants-sha256" not in extra:
                invariants_digest = (
                    manifest.get("invariants_sha256", "0" * 64)
                    if isinstance(manifest, dict)
                    else "0" * 64
                )
                arguments.extend(
                    ["--expect-invariants-sha256", invariants_digest]
                )
    rc = wal.main(arguments)
    captured = capsys.readouterr()
    report = json.loads(captured.out) if captured.out.strip() else {}
    return rc, report


def read_manifest(out: Path) -> dict:
    return json.loads((out / wal.MANIFEST_NAME).read_text(encoding="utf-8"))


def write_manifest(out: Path, manifest: dict, resign: bool = False) -> None:
    if resign:
        manifest["integrity_sha256"] = wal._integrity_hash(manifest)
    (out / wal.MANIFEST_NAME).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


# ---------------------------------------------------------------------------
# create — happy path
# ---------------------------------------------------------------------------


def test_create_then_verify_round_trip(source_db, bundle_dir, capsys):
    rc, report = create(source_db, bundle_dir, capsys)
    assert rc == 0, report
    assert report["verdict"] == "CAPTURED"
    assert (bundle_dir / wal.BUNDLE_DB_NAME).is_file()
    assert (bundle_dir / wal.MANIFEST_NAME).is_file()

    vrc, vreport = verify(bundle_dir, capsys)
    assert vrc == 0, vreport
    assert vreport["verdict"] == "VALID"
    assert vreport["failures"] == []


def test_manifest_records_online_backup_and_both_ends_integrity(source_db, bundle_dir, capsys):
    rc, report = create(source_db, bundle_dir, capsys)
    assert rc == 0, report
    m = read_manifest(bundle_dir)
    assert m["capture_mode"] == "sqlite_online_backup"
    assert m["source"]["integrity_check"] == "ok"
    assert m["bundle"]["integrity_check"] == "ok"
    assert m["source"]["db_sha256"] and m["bundle"]["db_sha256"]
    assert m["invariants_sha256"] == wal.invariants_hash(m["invariants"])
    assert m["integrity_sha256"] == wal._integrity_hash(m)
    snapshot = m["source"]["capture_snapshot"]
    assert snapshot["before"] == snapshot["after"]
    assert snapshot["changed_components"] == []
    assert snapshot["invariants_changed"] is False
    for component in ("db", "wal", "shm"):
        assert isinstance(snapshot["before"][component]["present"], bool)
    assert snapshot["before"]["db"]["sha256"] == m["source"]["db_sha256"]


def test_quiesced_capture_completes_wal_attach_before_drift_boundary(
    source_db, bundle_dir, capsys, monkeypatch
):
    """Emulate SQLite stacks that attach WAL only on a real schema read."""
    real_connect = wal.sqlite3.connect
    real_snapshot = wal._source_snapshot
    source_uri = f"{source_db.resolve().as_uri()}?mode=ro"
    main_db_read = {"started": False}

    def connect_with_delayed_attach(database, *args, **kwargs):
        conn = real_connect(database, *args, **kwargs)
        if str(database) == source_uri:
            def authorizer(action, table, _column, _database, _trigger):
                if action == sqlite3.SQLITE_READ and table in {
                    "sqlite_master",
                    "sqlite_schema",
                }:
                    main_db_read["started"] = True
                return sqlite3.SQLITE_OK

            conn.set_authorizer(authorizer)
        return conn

    def snapshot_with_delayed_sidecars(source):
        result = real_snapshot(source)
        if Path(source).resolve() != source_db.resolve():
            return result
        if not main_db_read["started"]:
            result["wal"] = {"present": False}
            result["shm"] = {"present": False}
        return result

    monkeypatch.setattr(
        wal,
        "sqlite3",
        SimpleNamespace(
            connect=connect_with_delayed_attach,
            Error=sqlite3.Error,
            Row=sqlite3.Row,
        ),
    )
    monkeypatch.setattr(wal, "_source_snapshot", snapshot_with_delayed_sidecars)

    rc, report = create(source_db, bundle_dir, capsys)

    assert rc == 0, report
    assert report["verdict"] == "CAPTURED"
    capture = read_manifest(bundle_dir)["source"]["capture_snapshot"]
    assert capture["arrival"]["wal"]["present"] is False
    assert capture["arrival"]["shm"]["present"] is False
    assert capture["before"]["wal"]["present"] is True
    assert capture["before"]["shm"]["present"] is True
    assert capture["before"] == capture["after"]
    assert capture["changed_components"] == []
    verify_rc, verify_report = verify(bundle_dir, capsys)
    assert verify_rc == 0, verify_report
    assert verify_report["verdict"] == "VALID"


def _change_snapshot_metadata(snapshot, component, field, amount=1):
    for key in ("metadata_before_hash", "metadata_after_hash"):
        snapshot[component][key][field] += amount


def test_shm_mode_flip_after_read_connection_initializes_fails_closed(
    tmp_path, bundle_dir, capsys, monkeypatch
):
    """Reproduce the auditor's real 0666 -> 0444 initialization-window attack."""
    source_db = tmp_path / "live-mode-flip" / "bridge.db"
    store = Store(source_db)
    _seed(store)
    source_shm = source_db.with_name(source_db.name + "-shm")
    real_snapshot = wal._source_snapshot
    calls = {"source": 0}

    def snapshot_with_mode_flip(source):
        if Path(source).resolve() == source_db.resolve():
            calls["source"] += 1
            if calls["source"] == 2:
                # _connect_readonly has completed the schema read and is about
                # to embed the SHM boundary before returning to its caller.
                # Starting mode is platform-dependent (Windows 0o666 vs a
                # POSIX umask-masked value); assert only that the flip target
                # differs so the attack actually mutates the mode.
                assert source_shm.stat().st_mode & 0o777 != 0o444
                source_shm.chmod(0o444)
        return real_snapshot(source)

    monkeypatch.setattr(wal, "_source_snapshot", snapshot_with_mode_flip)
    try:
        rc, report = create(source_db, bundle_dir, capsys)

        assert calls["source"] == 3
        assert rc == 2
        assert report["verdict"] == "INVALID"
        assert report["failures"] == ["source_changed_during_capture"]
        assert report["drift_evidence"]["changed_components"] == ["shm"]
        assert not (bundle_dir / wal.MANIFEST_NAME).exists()
        assert not (bundle_dir / wal.BUNDLE_DB_NAME).exists()
    finally:
        if source_shm.exists():
            source_shm.chmod(0o666)
        store.close()


@pytest.mark.parametrize("attack", ["inode_swap", "size_change", "deletion"])
def test_shm_initialization_identity_or_presence_attack_fails_closed(
    tmp_path, bundle_dir, capsys, monkeypatch, attack
):
    source_db = tmp_path / f"live-{attack}" / "bridge.db"
    store = Store(source_db)
    _seed(store)
    real_snapshot = wal._source_snapshot
    calls = {"source": 0}

    def snapshot_with_attack(source):
        result = real_snapshot(source)
        if Path(source).resolve() != source_db.resolve():
            return result
        calls["source"] += 1
        if calls["source"] >= 2:
            if attack == "inode_swap":
                _change_snapshot_metadata(result, "shm", "inode")
            elif attack == "size_change":
                _change_snapshot_metadata(
                    result, "shm", "size_bytes", wal.SHM_REGION_BYTES
                )
            else:
                result["shm"] = {"present": False}
        return result

    monkeypatch.setattr(wal, "_source_snapshot", snapshot_with_attack)
    try:
        rc, report = create(source_db, bundle_dir, capsys)

        assert calls["source"] == 3
        assert rc == 2
        assert report["verdict"] == "INVALID"
        assert report["failures"] == ["source_changed_during_capture"]
        assert report["drift_evidence"]["changed_components"] == ["shm"]
        assert not (bundle_dir / wal.MANIFEST_NAME).exists()
        assert not (bundle_dir / wal.BUNDLE_DB_NAME).exists()
    finally:
        store.close()


def test_shm_deletion_then_creation_after_boundary_fails_closed(
    tmp_path, bundle_dir, capsys, monkeypatch
):
    source_db = tmp_path / "live-shm-recreate" / "bridge.db"
    store = Store(source_db)
    _seed(store)
    real_snapshot = wal._source_snapshot
    calls = {"source": 0}

    def snapshot_with_recreation(source):
        result = real_snapshot(source)
        if Path(source).resolve() == source_db.resolve():
            calls["source"] += 1
            if calls["source"] == 2:
                result["shm"] = {"present": False}
        return result

    monkeypatch.setattr(wal, "_source_snapshot", snapshot_with_recreation)
    try:
        rc, report = create(source_db, bundle_dir, capsys)

        assert calls["source"] == 3
        assert rc == 2
        assert report["verdict"] == "INVALID"
        assert report["failures"] == ["source_changed_during_capture"]
        assert report["drift_evidence"]["changed_components"] == ["shm"]
        assert not (bundle_dir / wal.MANIFEST_NAME).exists()
        assert not (bundle_dir / wal.BUNDLE_DB_NAME).exists()
    finally:
        store.close()


def test_empty_wal_created_with_metadata_drift_fails_closed(
    source_db, bundle_dir, capsys, monkeypatch
):
    source_wal = source_db.with_name(source_db.name + "-wal")
    real_snapshot = wal._source_snapshot
    calls = {"source": 0}

    def snapshot_with_wal_mode_drift(source):
        if Path(source).resolve() == source_db.resolve():
            calls["source"] += 1
            if calls["source"] == 2:
                assert source_wal.stat().st_size == 0
                # Starting mode is platform-dependent; assert only that the
                # flip target differs so the drift is genuinely introduced.
                assert source_wal.stat().st_mode & 0o777 != 0o444
                source_wal.chmod(0o444)
        return real_snapshot(source)

    monkeypatch.setattr(wal, "_source_snapshot", snapshot_with_wal_mode_drift)
    try:
        rc, report = create(source_db, bundle_dir, capsys)

        assert calls["source"] == 3
        assert rc == 2
        assert report["verdict"] == "INVALID"
        assert report["failures"] == ["source_changed_during_capture"]
        assert report["drift_evidence"]["changed_components"] == ["wal"]
        assert not (bundle_dir / wal.MANIFEST_NAME).exists()
        assert not (bundle_dir / wal.BUNDLE_DB_NAME).exists()
    finally:
        if source_wal.exists():
            source_wal.chmod(0o666)


def test_hot_wal_with_unusable_shm_is_rejected_before_connecting(
    tmp_path, bundle_dir, monkeypatch
):
    live_db = tmp_path / "live" / "bridge.db"
    store = Store(live_db)
    _seed(store)
    live_wal = live_db.with_name(live_db.name + "-wal")
    crashed_db = tmp_path / "crashed" / "bridge.db"
    crashed_wal = crashed_db.with_name(crashed_db.name + "-wal")
    crashed_shm = crashed_db.with_name(crashed_db.name + "-shm")
    try:
        assert live_wal.stat().st_size > 0
        crashed_db.parent.mkdir(parents=True)
        shutil.copy2(live_db, crashed_db)
        shutil.copy2(live_wal, crashed_wal)
    finally:
        store.close()
    crashed_shm.write_bytes(b"")
    source_before = {
        path.name: path.read_bytes()
        for path in (crashed_db, crashed_wal, crashed_shm)
    }
    real_connect = sqlite3.connect
    connect_calls = []

    def counting_connect(database, *args, **kwargs):
        connect_calls.append(str(database))
        return real_connect(database, *args, **kwargs)

    monkeypatch.setattr(
        wal,
        "sqlite3",
        SimpleNamespace(
            connect=counting_connect,
            Error=sqlite3.Error,
            Row=sqlite3.Row,
        ),
    )

    with pytest.raises(wal.BundleError, match="hot WAL"):
        wal.create_bundle(crashed_db, bundle_dir, timestamp=TS)

    assert connect_calls == []
    assert {
        path.name: path.read_bytes()
        for path in (crashed_db, crashed_wal, crashed_shm)
    } == source_before
    assert not (bundle_dir / wal.BUNDLE_DB_NAME).exists()
    assert not (bundle_dir / wal.MANIFEST_NAME).exists()


def test_hot_wal_with_unrelated_shm_is_rejected_before_connecting(
    tmp_path, bundle_dir, monkeypatch
):
    primary_db = tmp_path / "primary" / "bridge.db"
    other_db = tmp_path / "other" / "bridge.db"
    primary = Store(primary_db)
    other = Store(other_db)
    _seed(primary, run_id="primary")
    _seed(other, run_id="other")
    crashed_db = tmp_path / "crashed-unrelated" / "bridge.db"
    crashed_wal = crashed_db.with_name(crashed_db.name + "-wal")
    crashed_shm = crashed_db.with_name(crashed_db.name + "-shm")
    try:
        primary_wal = primary_db.with_name(primary_db.name + "-wal")
        other_shm = other_db.with_name(other_db.name + "-shm")
        crashed_db.parent.mkdir(parents=True)
        shutil.copy2(primary_db, crashed_db)
        shutil.copy2(primary_wal, crashed_wal)
        shutil.copy2(other_shm, crashed_shm)
    finally:
        primary.close()
        other.close()
    assert wal._shm_is_structurally_usable(crashed_shm) is True
    assert wal._shm_holds_usable_wal_index(crashed_shm, crashed_wal) is False

    real_connect = sqlite3.connect
    connect_calls = []

    def counting_connect(database, *args, **kwargs):
        connect_calls.append(str(database))
        return real_connect(database, *args, **kwargs)

    monkeypatch.setattr(
        wal,
        "sqlite3",
        SimpleNamespace(
            connect=counting_connect,
            Error=sqlite3.Error,
            Row=sqlite3.Row,
        ),
    )

    with pytest.raises(wal.BundleError, match="hot WAL"):
        wal.create_bundle(crashed_db, bundle_dir, timestamp=TS)

    assert connect_calls == []
    assert not (bundle_dir / wal.BUNDLE_DB_NAME).exists()
    assert not (bundle_dir / wal.MANIFEST_NAME).exists()


def test_capture_drift_allows_only_existing_shm_readmark_content_change():
    stable_metadata = {
        "device": 1,
        "inode": 2,
        "mode": 0o666,
        "size_bytes": wal.SHM_REGION_BYTES,
        "mtime_ns": 10,
        "ctime_ns": 10,
    }
    database = {
        "present": True,
        "sha256": "db",
        "metadata_before_hash": stable_metadata,
        "metadata_after_hash": stable_metadata,
        "changed_during_hash": False,
    }
    before = {
        "db": database,
        "wal": {"present": False},
        "shm": {
            "present": True,
            "sha256": "shm-before",
            "metadata_before_hash": stable_metadata,
            "metadata_after_hash": stable_metadata,
            "changed_during_hash": False,
        },
    }
    arrival = copy.deepcopy(before)
    after = copy.deepcopy(before)
    after["shm"]["sha256"] = "shm-after"
    for key in ("metadata_before_hash", "metadata_after_hash"):
        after["shm"][key] = dict(stable_metadata, mtime_ns=20, ctime_ns=20)

    assert wal._capture_changed_components(arrival, before, after) == []


def test_capture_drift_ignores_read_open_empty_wal_materialization():
    database_metadata = {
        "device": 1,
        "inode": 2,
        "mode": 0o666,
        "size_bytes": 4096,
        "mtime_ns": 10,
        "ctime_ns": 10,
    }
    wal_metadata = dict(database_metadata, inode=3, size_bytes=0)
    arrival = {
        "db": {
            "present": True,
            "sha256": "db",
            "metadata_before_hash": database_metadata,
            "metadata_after_hash": database_metadata,
            "changed_during_hash": False,
        },
        "wal": {"present": False},
        "shm": {"present": False},
    }
    before = {
        "db": copy.deepcopy(arrival["db"]),
        "wal": {
            "present": True,
            "sha256": wal._sha256_bytes(b""),
            "metadata_before_hash": wal_metadata,
            "metadata_after_hash": wal_metadata,
            "changed_during_hash": False,
        },
        "shm": {"present": True, "sha256": "sqlite-read-marks"},
    }
    after = copy.deepcopy(before)

    assert wal._capture_changed_components(arrival, before, after) == []


def test_capture_drift_unions_both_intervals_without_duplicates():
    arrival = {
        "db": {"sha256": "db-arrival"},
        "wal": {"sha256": "wal-arrival"},
        "shm": {"sha256": "shm-arrival"},
    }
    before = {
        "db": {"sha256": "db-before"},
        "wal": {"sha256": "wal-before"},
        "shm": {"sha256": "shm-before"},
    }
    after = {
        "db": {"sha256": "db-after"},
        "wal": {"sha256": "wal-before"},
        "shm": {"sha256": "shm-after"},
    }

    assert wal._capture_changed_components(arrival, before, after) == [
        "db",
        "wal",
        "shm",
    ]


def test_bundle_never_contains_a_wal_shm_trio(tmp_path, bundle_dir, capsys):
    """The source is captured while its WAL is hot; the bundle must still be a
    single self-contained file, and the WAL-resident rows must be present."""
    db = tmp_path / "live" / "bridge.db"
    store = Store(db)
    _seed(store)
    # deliberately NOT closed: -wal (and -shm) are live next to the database
    try:
        assert db.with_name(db.name + "-wal").exists()

        rc, _ = create(db, bundle_dir, capsys, "--allow-live-source")
        assert rc == 0

        produced = sorted(p.name for p in bundle_dir.iterdir())
        assert produced == sorted([wal.BUNDLE_DB_NAME, wal.MANIFEST_NAME])

        m = read_manifest(bundle_dir)
        assert m["source"]["wal_present"] is True
        assert m["source"]["wal_sha256"]
        # WAL-resident rows made it into the bundle
        assert m["invariants"]["counts"]["trades"] == 4
        assert m["invariants"]["closed_trades"] == 3
    finally:
        store.close()


def test_invariants_preserve_risk_and_history(source_db, bundle_dir, capsys):
    with closing(sqlite3.connect(source_db)) as source:
        source_schema_row = source.execute(
            "SELECT value FROM meta WHERE key = 'schema_version'"
        ).fetchone()
    assert source_schema_row is not None

    rc, _ = create(source_db, bundle_dir, capsys)
    assert rc == 0
    inv = read_manifest(bundle_dir)["invariants"]

    assert inv["app_state"] == "DISARMED"
    assert inv["schema_version"] == source_schema_row[0]
    assert inv["open_trades"] == 1
    assert inv["live_orders"] == 1
    assert inv["closed_trades"] == 3

    env = inv["environments"][0]
    assert (env["mode"], env["network"]) == ("paper", "testnet")
    assert env["consecutive_closed_losses"] == 3
    assert env["realized_pnl_total"] == pytest.approx(-18.0)
    assert env["latest_trading_date"] == "2026-07-20"
    assert env["realized_pnl_latest_date"] == pytest.approx(-18.0)

    day = inv["risk_days"][0]
    assert day["trading_date"] == "2026-07-20"
    assert day["consecutive_losses_end"] == 3
    assert day["auto_rearms_used"] == 1


def test_manifest_leaks_no_path_or_identifier(source_db, bundle_dir, capsys):
    rc, _ = create(source_db, bundle_dir, capsys)
    assert rc == 0
    text = (bundle_dir / wal.MANIFEST_NAME).read_text(encoding="utf-8")
    assert str(source_db.parent) not in text
    assert "/" not in json.dumps(read_manifest(bundle_dir)["source"])
    for needle in ("HL_API_WALLET_KEY", "HL_ACCOUNT_ADDRESS", "0x"):
        assert needle not in text


def test_manifest_uses_a_canonical_source_name_not_the_input_name(
    source_db, bundle_dir, capsys
):
    renamed = source_db.with_name("sensitive_identifier.db")
    source_db.replace(renamed)
    rc, _ = create(renamed, bundle_dir, capsys)
    assert rc == 0
    assert read_manifest(bundle_dir)["source"]["db_name"] == wal.BUNDLE_DB_NAME
    assert "sensitive_identifier" not in (bundle_dir / wal.MANIFEST_NAME).read_text(
        encoding="utf-8"
    )


def test_sanitization_guard_rejects_path_like_values():
    with pytest.raises(wal.SanitizationError):
        wal._assert_sanitized({"db_name": "/var/lib/mtc-bridge/bridge.db"})
    with pytest.raises(wal.SanitizationError):
        wal._assert_sanitized({"account": "0x" + "a" * 40})
    with pytest.raises(wal.SanitizationError):
        wal._assert_sanitized({"host": "synthetic-host" + "." + "example"})
    wal._assert_sanitized({"db_name": "bridge.db", "count": 3, "ok": None})


def test_source_content_is_not_mutated(source_db, bundle_dir, capsys):
    """The source database content is never written to, and the recorded
    sidecar state is the state found on arrival — not one SQLite materialised
    for our own read-only connection."""
    before = source_db.read_bytes()
    rc, _ = create(source_db, bundle_dir, capsys)
    assert rc == 0
    assert source_db.read_bytes() == before

    src = read_manifest(bundle_dir)["source"]
    assert src["wal_present"] is False
    assert src["wal_sha256"] is None
    assert src["shm_present"] is False
    assert src["db_sha256"] == wal._sha256_file(source_db)


# ---------------------------------------------------------------------------
# create — failure paths
# ---------------------------------------------------------------------------


def test_create_refuses_missing_source(tmp_path, bundle_dir, capsys):
    rc = wal.main(["create", "--source", str(tmp_path / "nope.db"),
                   "--out-dir", str(bundle_dir)])
    err = capsys.readouterr().err
    assert rc == 3
    assert "Traceback" not in err
    assert str(tmp_path) not in err


def test_create_refuses_non_sqlite_source(tmp_path, bundle_dir, capsys):
    junk = tmp_path / "bridge.db"
    junk.write_bytes(b"this is definitely not a sqlite database" * 8)
    rc = wal.main(["create", "--source", str(junk), "--out-dir", str(bundle_dir)])
    err = capsys.readouterr().err
    assert rc == 3
    assert "Traceback" not in err


def test_create_refuses_to_overwrite_without_force(source_db, bundle_dir, capsys):
    assert create(source_db, bundle_dir, capsys)[0] == 0
    rc = wal.main(["create", "--source", str(source_db), "--out-dir", str(bundle_dir),
                   "--timestamp", TS])
    assert capsys.readouterr()
    assert rc == 3


def test_create_force_replaces_existing_bundle(source_db, bundle_dir, capsys):
    assert create(source_db, bundle_dir, capsys)[0] == 0
    rc, report = create(source_db, bundle_dir, capsys, "--force")
    assert rc == 0
    assert report["verdict"] == "CAPTURED"


def test_force_rejects_source_output_overlap_without_touching_source(tmp_path, capsys):
    source = tmp_path / "overlap" / wal.BUNDLE_DB_NAME
    store = Store(source)
    _seed(store)
    store.close()
    before = source.read_bytes()

    rc = wal.main(
        [
            "create",
            "--source",
            str(source),
            "--out-dir",
            str(source.parent / "."),
            "--timestamp",
            TS,
            "--force",
        ]
    )
    err = capsys.readouterr().err
    assert rc == 3
    assert "overlap or alias" in err
    assert source.is_file()
    assert source.read_bytes() == before


def test_force_rejects_existing_output_hardlink_alias_to_source(
    source_db, bundle_dir, capsys
):
    bundle_dir.mkdir(parents=True)
    alias = bundle_dir / wal.MANIFEST_NAME
    try:
        alias.hardlink_to(source_db)
    except OSError:
        pytest.skip("hard links are not available on this host")
    before = source_db.read_bytes()

    rc = wal.main(
        [
            "create",
            "--source",
            str(source_db),
            "--out-dir",
            str(bundle_dir),
            "--timestamp",
            TS,
            "--force",
        ]
    )
    assert capsys.readouterr()
    assert rc == 3
    assert source_db.read_bytes() == before
    assert alias.exists()


def test_non_summary_source_mutation_during_capture_fails_closed(
    source_db, bundle_dir, capsys, monkeypatch
):
    """Changing order_json preserves every summarized invariant but must drift."""
    real_snapshot = wal._source_snapshot
    calls = {"n": 0}

    def mutate_after_pre_snapshot(source):
        result = real_snapshot(source)
        calls["n"] += 1
        if calls["n"] == 2:
            conn = sqlite3.connect(source_db)
            conn.execute(
                "UPDATE orders SET order_json = ? WHERE cloid = ?",
                ('{"symbol":"ETH","synthetic":"changed"}', "cloid-0"),
            )
            conn.commit()
            conn.close()
        return result

    monkeypatch.setattr(wal, "_source_snapshot", mutate_after_pre_snapshot)
    rc, report = create(source_db, bundle_dir, capsys)
    assert rc == 2
    assert report["failures"] == ["source_changed_during_capture"]
    assert calls["n"] == 3
    assert not (bundle_dir / wal.MANIFEST_NAME).exists()
    assert not (bundle_dir / wal.BUNDLE_DB_NAME).exists()


def test_concurrent_writer_during_capture_fails_closed(
    source_db, bundle_dir, capsys, monkeypatch
):
    """Commit a non-summary change after the capture boundary has opened."""
    real_connect = wal._connect_readonly
    wrapped = {"done": False}
    writer_started = threading.Event()
    writer_finished = threading.Event()
    writer_errors = []

    class ConcurrentWriterBackupProxy:
        def __init__(self, conn):
            self.conn = conn

        def execute(self, *args, **kwargs):
            return self.conn.execute(*args, **kwargs)

        def backup(self, target):
            def write_during_capture():
                writer_started.set()
                try:
                    writer = sqlite3.connect(source_db)
                    try:
                        writer.execute(
                            "UPDATE orders SET order_json = ? WHERE cloid = ?",
                            ('{"symbol":"ETH","concurrent":"changed"}', "cloid-0"),
                        )
                        writer.commit()
                    finally:
                        writer.close()
                except Exception as exc:  # pragma: no cover - surfaced below
                    writer_errors.append(exc)
                finally:
                    writer_finished.set()

            thread = threading.Thread(target=write_during_capture, daemon=True)
            thread.start()
            assert writer_started.wait(timeout=5)
            assert writer_finished.wait(timeout=10)
            thread.join(timeout=5)
            assert not thread.is_alive()
            assert writer_errors == []
            return self.conn.backup(target)

        def close(self):
            self.conn.close()

    def connect_with_concurrent_writer(path, **kwargs):
        connected = real_connect(path, **kwargs)
        if isinstance(connected, tuple):
            conn, snapshot = connected
        else:
            conn, snapshot = connected, None
        if Path(path).resolve() == source_db.resolve() and not wrapped["done"]:
            wrapped["done"] = True
            conn = ConcurrentWriterBackupProxy(conn)
        return (conn, snapshot) if snapshot is not None else conn

    monkeypatch.setattr(wal, "_connect_readonly", connect_with_concurrent_writer)
    rc, report = create(source_db, bundle_dir, capsys)

    assert wrapped["done"] is True
    assert writer_started.is_set()
    assert writer_finished.is_set()
    assert rc == 2
    assert report["failures"] == ["source_changed_during_capture"]
    assert report["drift_evidence"]["changed_components"]
    assert not (bundle_dir / wal.MANIFEST_NAME).exists()
    assert not (bundle_dir / wal.BUNDLE_DB_NAME).exists()


@pytest.mark.parametrize(
    ("component", "mutate"),
    [
        pytest.param(
            "db",
            lambda snapshot: _change_snapshot_metadata(snapshot, "db", "inode"),
            id="inode_replacement",
        ),
        pytest.param(
            "db",
            lambda snapshot: _change_snapshot_metadata(snapshot, "db", "mode"),
            id="permission_mode_change",
        ),
        pytest.param(
            "shm",
            lambda snapshot: snapshot["shm"].__setitem__("sha256", "f" * 64),
            id="sidecar_mutation",
        ),
    ],
)
def test_capture_metadata_and_sidecar_drift_fails_closed(
    source_db, bundle_dir, capsys, monkeypatch, component, mutate
):
    """Inject one stable post-boundary filesystem snapshot change per class."""
    real_snapshot = wal._source_snapshot
    calls = {"source": 0}

    def snapshot_with_injected_drift(source):
        result = real_snapshot(source)
        if Path(source).resolve() == source_db.resolve():
            calls["source"] += 1
            if calls["source"] == 3:
                mutate(result)
        return result

    monkeypatch.setattr(wal, "_source_snapshot", snapshot_with_injected_drift)
    rc, report = create(source_db, bundle_dir, capsys)

    assert calls["source"] == 3
    assert rc == 2
    assert report["failures"] == ["source_changed_during_capture"]
    assert component in report["drift_evidence"]["changed_components"]
    assert not (bundle_dir / wal.MANIFEST_NAME).exists()
    assert not (bundle_dir / wal.BUNDLE_DB_NAME).exists()


def test_arrival_to_before_non_summary_mutation_fails_closed(
    source_db, bundle_dir, capsys, monkeypatch
):
    """A commit inside the first read-connect gap must not escape drift checks."""
    real_connect = wal._connect_readonly
    mutated = {"done": False}

    def connect_after_arrival_mutation(path, **kwargs):
        if Path(path).resolve() == source_db.resolve() and not mutated["done"]:
            mutated["done"] = True
            writer = sqlite3.connect(source_db)
            try:
                writer.execute(
                    "UPDATE orders SET order_json = ? WHERE cloid = ?",
                    ('{"symbol":"ETH","arrival_gap":"changed"}', "cloid-0"),
                )
                writer.commit()
            finally:
                writer.close()
        return real_connect(path, **kwargs)

    monkeypatch.setattr(wal, "_connect_readonly", connect_after_arrival_mutation)
    rc, report = create(source_db, bundle_dir, capsys)

    assert mutated["done"] is True
    assert rc == 2
    assert report["failures"] == ["source_changed_during_capture"]
    changed = report["drift_evidence"]["changed_components"]
    assert any(component in changed for component in ("db", "wal"))
    assert len(changed) == len(set(changed))
    assert not (bundle_dir / wal.MANIFEST_NAME).exists()
    assert not (bundle_dir / wal.BUNDLE_DB_NAME).exists()


def test_allow_live_source_records_arrival_to_before_drift(
    source_db, bundle_dir, capsys, monkeypatch
):
    real_connect = wal._connect_readonly
    mutated = {"done": False}

    def connect_after_arrival_mutation(path, **kwargs):
        if Path(path).resolve() == source_db.resolve() and not mutated["done"]:
            mutated["done"] = True
            writer = sqlite3.connect(source_db)
            try:
                writer.execute(
                    "UPDATE orders SET order_json = ? WHERE cloid = ?",
                    ('{"symbol":"ETH","arrival_gap":"allowed"}', "cloid-0"),
                )
                writer.commit()
            finally:
                writer.close()
        return real_connect(path, **kwargs)

    monkeypatch.setattr(wal, "_connect_readonly", connect_after_arrival_mutation)
    rc, report = create(
        source_db, bundle_dir, capsys, "--allow-live-source"
    )

    assert mutated["done"] is True
    assert rc == 0, report
    manifest = read_manifest(bundle_dir)
    assert manifest["source"]["changed_during_capture"] is True
    changed = manifest["source"]["capture_snapshot"]["changed_components"]
    assert any(component in changed for component in ("db", "wal"))
    assert len(changed) == len(set(changed))
    vrc, vreport = verify(bundle_dir, capsys)
    assert vrc == 0, vreport


def test_create_fails_closed_when_source_changes_during_capture(
    source_db, bundle_dir, capsys, monkeypatch
):
    """A moving source means an unquiesced writer — a cutover stop condition."""
    real = wal.collect_invariants
    calls = {"n": 0}

    def drifting(conn):
        calls["n"] += 1
        result = real(conn)
        if calls["n"] == 1:  # the source read, taken after the backup
            result = dict(result)
            result["open_trades"] = result["open_trades"] + 1
        return result

    monkeypatch.setattr(wal, "collect_invariants", drifting)
    rc, report = create(source_db, bundle_dir, capsys)
    assert rc == 2
    assert report["failures"] == ["source_changed_during_capture"]
    # fail closed: no half-trusted artefact left behind
    assert not (bundle_dir / wal.MANIFEST_NAME).exists()
    assert not (bundle_dir / wal.BUNDLE_DB_NAME).exists()


def test_allow_live_source_downgrades_drift_to_a_recorded_flag(
    source_db, bundle_dir, capsys, monkeypatch
):
    real = wal.collect_invariants
    calls = {"n": 0}

    def drifting(conn):
        calls["n"] += 1
        result = real(conn)
        if calls["n"] == 1:
            result = dict(result)
            result["open_trades"] = result["open_trades"] + 1
        return result

    monkeypatch.setattr(wal, "collect_invariants", drifting)
    rc, _ = create(source_db, bundle_dir, capsys, "--allow-live-source")
    assert rc == 0
    assert read_manifest(bundle_dir)["source"]["changed_during_capture"] is True


def test_create_rejects_bad_timestamp(source_db, bundle_dir, capsys):
    rc = wal.main(["create", "--source", str(source_db), "--out-dir", str(bundle_dir),
                   "--timestamp", "yesterday"])
    assert capsys.readouterr()
    assert rc == 3


def test_create_rejects_a_database_without_the_bridge_schema(tmp_path, bundle_dir, capsys):
    empty = tmp_path / "bridge.db"
    conn = sqlite3.connect(empty)
    conn.execute("CREATE TABLE unrelated (x INTEGER)")
    conn.commit()
    conn.close()
    rc = wal.main(["create", "--source", str(empty), "--out-dir", str(bundle_dir),
                   "--timestamp", TS])
    err = capsys.readouterr().err
    assert rc == 3
    assert "schema missing tables" in err


def test_create_discards_partial_database_when_backup_raises(
    source_db, bundle_dir, capsys, monkeypatch
):
    real_connect = wal._connect_readonly
    calls = {"count": 0}

    class FailingBackupProxy:
        def __init__(self, conn):
            self.conn = conn

        def execute(self, *args, **kwargs):
            return self.conn.execute(*args, **kwargs)

        def backup(self, target):
            target.execute("CREATE TABLE partial(x INTEGER)")
            target.commit()
            raise sqlite3.OperationalError("synthetic backup failure")

        def close(self):
            self.conn.close()

    def connect_once_failing(path, **kwargs):
        calls["count"] += 1
        connected = real_connect(path, **kwargs)
        if isinstance(connected, tuple):
            conn, snapshot = connected
        else:
            conn, snapshot = connected, None
        if calls["count"] == 1:
            conn = FailingBackupProxy(conn)
        return (conn, snapshot) if snapshot is not None else conn

    monkeypatch.setattr(wal, "_connect_readonly", connect_once_failing)
    rc, _ = create(source_db, bundle_dir, capsys)
    assert rc == 3
    assert not (bundle_dir / wal.BUNDLE_DB_NAME).exists()
    assert not (bundle_dir / wal.MANIFEST_NAME).exists()


# ---------------------------------------------------------------------------
# verify — failure paths
# ---------------------------------------------------------------------------


def test_verify_missing_manifest_exit_3(bundle_dir, capsys):
    bundle_dir.mkdir(parents=True)
    rc, _ = verify(bundle_dir, capsys)
    assert rc == 3


def test_verify_corrupt_manifest_json_exit_3(source_db, bundle_dir, capsys):
    assert create(source_db, bundle_dir, capsys)[0] == 0
    (bundle_dir / wal.MANIFEST_NAME).write_text("{not json", encoding="utf-8")
    rc, _ = verify(bundle_dir, capsys)
    err = capsys.readouterr().err
    assert rc == 3
    assert "Traceback" not in err


def test_verify_detects_missing_field(source_db, bundle_dir, capsys):
    assert create(source_db, bundle_dir, capsys)[0] == 0
    m = read_manifest(bundle_dir)
    del m["invariants_sha256"]
    write_manifest(bundle_dir, m)
    rc, report = verify(bundle_dir, capsys)
    assert rc == 2
    assert "missing_field:invariants_sha256" in report["failures"]


def test_verify_rejects_unsupported_schema_version(source_db, bundle_dir, capsys):
    assert create(source_db, bundle_dir, capsys)[0] == 0
    m = read_manifest(bundle_dir)
    m["schema_version"] = "0.9.0"
    write_manifest(bundle_dir, m, resign=True)
    rc, report = verify(bundle_dir, capsys)
    assert rc == 2
    assert "unsupported_schema_version" in report["failures"]


def test_verify_rejects_manifest_controlled_path_before_file_access(
    source_db, bundle_dir, capsys
):
    assert create(source_db, bundle_dir, capsys)[0] == 0
    m = read_manifest(bundle_dir)
    m["bundle"]["db_name"] = "." * 2 + chr(47) + "outside.db"
    write_manifest(bundle_dir, m, resign=True)
    rc, report = verify(bundle_dir, capsys)
    assert rc == 2
    assert "unsanitized_manifest" in report["failures"]


def test_verify_rejects_resigned_noncaptured_manifest(source_db, bundle_dir, capsys):
    assert create(source_db, bundle_dir, capsys)[0] == 0
    m = read_manifest(bundle_dir)
    m["verdict"] = "INVALID"
    m["exit_code"] = 2
    write_manifest(bundle_dir, m, resign=True)
    rc, report = verify(bundle_dir, capsys)
    assert rc == 2
    assert "manifest_not_captured" in report["failures"]
    assert "manifest_exit_code_not_zero" in report["failures"]


def test_verify_rejects_missing_nested_contract_field(source_db, bundle_dir, capsys):
    assert create(source_db, bundle_dir, capsys)[0] == 0
    m = read_manifest(bundle_dir)
    del m["bundle"]["sidecar_files"]
    write_manifest(bundle_dir, m, resign=True)
    rc, report = verify(bundle_dir, capsys)
    assert rc == 2
    assert "missing_field:bundle.sidecar_files" in report["failures"]


def test_verify_detects_manifest_tamper(source_db, bundle_dir, capsys):
    assert create(source_db, bundle_dir, capsys)[0] == 0
    m = read_manifest(bundle_dir)
    m["invariants"]["open_trades"] = 0  # not re-signed
    write_manifest(bundle_dir, m)
    rc, report = verify(bundle_dir, capsys)
    assert rc == 2
    assert "integrity_hash_mismatch" in report["failures"]


def test_verify_detects_bundle_hash_mismatch(source_db, bundle_dir, capsys):
    assert create(source_db, bundle_dir, capsys)[0] == 0
    db = bundle_dir / wal.BUNDLE_DB_NAME
    with db.open("ab") as handle:
        handle.write(b"\x00" * 16)
    rc, report = verify(bundle_dir, capsys)
    assert rc == 2
    assert "bundle_db_hash_mismatch" in report["failures"]


def test_verify_detects_invariant_drift_even_when_resigned(source_db, bundle_dir, capsys):
    """Someone edits the bundle database and re-signs the manifest: the
    re-derived invariants still expose the change."""
    assert create(source_db, bundle_dir, capsys)[0] == 0
    db = bundle_dir / wal.BUNDLE_DB_NAME
    conn = sqlite3.connect(db)
    conn.execute("DELETE FROM risk_days")
    conn.commit()
    conn.close()
    for sidecar in ("-wal", "-shm"):
        stale = db.with_name(db.name + sidecar)
        if stale.exists():
            stale.unlink()

    m = read_manifest(bundle_dir)
    m["bundle"]["db_sha256"] = wal._sha256_file(db)  # hide the byte change
    write_manifest(bundle_dir, m, resign=True)

    rc, report = verify(bundle_dir, capsys)
    assert rc == 2
    assert "invariants_drift" in report["failures"]
    assert "invariants_hash_mismatch" in report["failures"]


def test_verify_detects_missing_bundle_db(source_db, bundle_dir, capsys):
    assert create(source_db, bundle_dir, capsys)[0] == 0
    (bundle_dir / wal.BUNDLE_DB_NAME).unlink()
    rc, report = verify(bundle_dir, capsys)
    assert rc == 2
    assert "bundle_db_missing" in report["failures"]


def test_verify_rejects_a_sidecar_next_to_the_bundle(source_db, bundle_dir, capsys):
    assert create(source_db, bundle_dir, capsys)[0] == 0
    (bundle_dir / (wal.BUNDLE_DB_NAME + "-wal")).write_bytes(b"stray")
    rc, report = verify(bundle_dir, capsys)
    assert rc == 2
    assert "bundle_sidecar_present" in report["failures"]


def test_verify_expected_hashes_must_match(source_db, bundle_dir, capsys):
    assert create(source_db, bundle_dir, capsys)[0] == 0
    m = read_manifest(bundle_dir)

    rc, report = verify(bundle_dir, capsys,
                        "--expect-bundle-sha256", m["bundle"]["db_sha256"],
                        "--expect-invariants-sha256", m["invariants_sha256"])
    assert rc == 0, report

    rc, report = verify(bundle_dir, capsys, "--expect-bundle-sha256", "0" * 64)
    assert rc == 2
    assert "bundle_db_hash_not_expected" in report["failures"]

    rc, report = verify(bundle_dir, capsys, "--expect-invariants-sha256", "0" * 64)
    assert rc == 2
    assert "invariants_hash_not_expected" in report["failures"]


def test_verify_requires_both_externally_recorded_expected_hashes(
    source_db, bundle_dir, capsys
):
    assert create(source_db, bundle_dir, capsys)[0] == 0
    manifest = read_manifest(bundle_dir)

    rc = wal.main(["verify", "--bundle-dir", str(bundle_dir)])
    assert rc == 3
    assert "expect_bundle_sha256 is required" in capsys.readouterr().err

    rc = wal.main(
        [
            "verify",
            "--bundle-dir",
            str(bundle_dir),
            "--expect-bundle-sha256",
            manifest["bundle"]["db_sha256"],
        ]
    )
    assert rc == 3
    assert "expect_invariants_sha256 is required" in capsys.readouterr().err


def test_verify_rejects_malformed_expected_hash(source_db, bundle_dir, capsys):
    assert create(source_db, bundle_dir, capsys)[0] == 0
    rc, _ = verify(bundle_dir, capsys, "--expect-bundle-sha256", "not-a-hash")
    assert rc == 3
    assert "Traceback" not in capsys.readouterr().err


def test_verify_fails_closed_on_a_corrupt_bundle_database(source_db, bundle_dir, capsys):
    assert create(source_db, bundle_dir, capsys)[0] == 0
    db = bundle_dir / wal.BUNDLE_DB_NAME
    raw = bytearray(db.read_bytes())
    assert len(raw) > 16
    # Destroy the SQLite signature deterministically.
    raw[:16] = b"not-a-sqlite-db!"
    db.write_bytes(bytes(raw))

    m = read_manifest(bundle_dir)
    m["bundle"]["db_sha256"] = wal._sha256_file(db)
    write_manifest(bundle_dir, m, resign=True)

    rc, report = verify(bundle_dir, capsys)
    assert rc in (2, 3)
    if rc == 2:
        assert report["verdict"] == "INVALID"
        assert report["failures"]
