"""WAL-consistent bridge state bundle: capture + verify (KVM2 P2-06 / P4-05).

Why this tool exists
--------------------
The bridge runtime database runs in WAL mode (`PRAGMA journal_mode=WAL`, see
`bridge/store/db.py`). Copying the live `bridge.db` / `bridge.db-wal` /
`bridge.db-shm` trio with a file copy is **not** a consistent snapshot: the
three files are only mutually consistent under SQLite's own locking, and a
naive copy can silently produce a database that loses committed trades, or
resets daily-loss / consecutive-loss / foreign-position risk history. That is
the exact failure mode the canonical Bridge VPS Deploy Task List blocks on
(blocking finding 4) and that KVM2-P4-05 must prove did not happen.

This tool therefore **never copies the trio**. It uses the SQLite online backup
API (`sqlite3.Connection.backup`), which produces one self-contained, internally
consistent database file, then:

* runs `PRAGMA integrity_check` and `PRAGMA foreign_key_check` on both ends;
* records SHA-256 of the source main/-wal/-shm files (provenance only) and of
  the produced bundle (authoritative);
* extracts sanitized, application-level risk/history invariants that must
  survive a migration — counts, open trades, live orders, per-environment
  realized PnL, consecutive closed losses and the `risk_days` ledger;
* re-derives every invariant from the bundle during `verify` and fails closed on
  any mismatch.

Sanitization
------------
The manifest and every stdout report contain hashes, counts, aggregates, UTC
timestamps and file *base names* only. No directory path, host, IP, account
address, wallet key, environment-variable value or raw log/event text is read
into, or written out of, this tool. A sanitization guard rejects the manifest
before it is written if any string field looks like a path, an address or a
key.

Non-actions
-----------
Read-only against the source (opened with `mode=ro`). No network, no exchange
call, no service control, no scheduler access, no mutation of the source
database or its sidecars. It is offline tooling; running it against a live
runtime worktree requires the separate owner authorization that governs that
runtime.

Invocation
----------
    python IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py create \
        --source <path/to/bridge.db> --out-dir <bundle dir> \
        [--timestamp YYYY-MM-DDTHH:MM:SSZ] [--allow-live-source] [--force]

    python IBKR_PAPER_BRIDGE/tools/wal_state_bundle.py verify \
        --bundle-dir <bundle dir> \
        --expect-bundle-sha256 <hex> --expect-invariants-sha256 <hex>

Exit codes
----------
| 0 | capture succeeded / bundle verified                                    |
| 2 | a check failed: corruption, hash mismatch, invariant drift, bad schema |
| 3 | invalid input: missing/unreadable file, corrupt JSON, bad CLI usage    |

Failure mode is safe: exit 3 prints a single `wal_state_bundle: ...` line to
stderr with no traceback and no absolute path.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import stat
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = "1.0.0"
TOOL_NAME = "wal_state_bundle"
BUNDLE_DB_NAME = "bridge.db"
MANIFEST_NAME = "bundle_manifest.json"
CAPTURE_MODE = "sqlite_online_backup"

#: Sidecars that must never appear next to a finished bundle. Their presence
#: means the bundle was produced (or later touched) by something other than the
#: online-backup path this tool guarantees.
FORBIDDEN_SIDECARS = ("-wal", "-shm", "-journal")

#: Tables the bridge schema (v2) must expose for the invariants below to mean
#: anything. A missing table fails closed rather than reporting zeros.
REQUIRED_TABLES = (
    "meta",
    "runs",
    "trades",
    "orders",
    "fills",
    "decisions",
    "events",
    "equity",
    "bars",
    "risk_days",
    "signal_fingerprints",
    "directives",
    "llm_calls",
)

COUNT_TABLES = (
    "runs",
    "trades",
    "orders",
    "fills",
    "decisions",
    "events",
    "equity",
    "bars",
    "risk_days",
    "signal_fingerprints",
    "directives",
    "llm_calls",
)

LIVE_ORDER_STATUSES = ("OPEN", "SUBMITTED", "PENDING")

REQUIRED_MANIFEST_FIELDS = (
    "schema_version",
    "tool",
    "generated_at_utc",
    "capture_mode",
    "source",
    "bundle",
    "invariants",
    "invariants_sha256",
    "verdict",
    "exit_code",
    "integrity_sha256",
)

#: Float rounding for hash-stable invariants. SQLite REAL round-trips through
#: JSON exactly at this precision for the magnitudes the bridge stores.
FLOAT_NDIGITS = 12
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

# --- sanitization ----------------------------------------------------------

_SANITIZE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("path_separator", re.compile(r"[\\/]")),
    ("drive_letter", re.compile(r"^[A-Za-z]:")),
    ("ipv4_literal", re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")),
    (
        "hostname_literal",
        re.compile(
            r"(?i)\b[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?\."
            r"(?:local|internal|lan|example|invalid|test)\b"
        ),
    ),
    ("at_sign", re.compile(r"@")),
    ("hex_key_or_address", re.compile(r"0[xX][0-9a-fA-F]{20,}")),
    ("secret_name", re.compile(r"(?i)(HL_API_WALLET_KEY|HL_ACCOUNT_ADDRESS|HL_LIVE_ACK|API_KEY|BOT_TOKEN|PRIVATE_KEY)")),
)


class SanitizationError(Exception):
    """Raised when a value that would be written out looks like a secret."""


def _assert_sanitized(value: Any, where: str = "manifest") -> None:
    """Fail closed if any string in *value* looks like a private identifier."""
    if isinstance(value, str):
        for name, pattern in _SANITIZE_PATTERNS:
            if pattern.search(value):
                raise SanitizationError(f"{where}: {name}")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            _assert_sanitized(str(key), f"{where}.{key}(key)")
            _assert_sanitized(item, f"{where}.{key}")
        return
    if isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _assert_sanitized(item, f"{where}[{index}]")


# --- small helpers ---------------------------------------------------------


class BundleError(Exception):
    """Invalid input (exit 3)."""


def _canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _integrity_hash(manifest: dict[str, Any]) -> str:
    body = {k: v for k, v in manifest.items() if k != "integrity_sha256"}
    return _sha256_bytes(_canonical_json(body).encode("utf-8"))


def _num(value: Any) -> float | None:
    return None if value is None else round(float(value), FLOAT_NDIGITS)


def _connect_readonly(path: Path) -> sqlite3.Connection:
    """Open *path* strictly read-only so the source can never be mutated.

    Known limitation: SQLite cannot open a WAL database read-only when a hot
    `-wal` exists without its `-shm` (a crashed writer). That case fails closed
    here; recovering it needs a read-write connection and therefore a separate
    owner authorization — it is never done silently by this tool.
    """
    wal = path.with_name(path.name + "-wal")
    shm = path.with_name(path.name + "-shm")
    if wal.is_file() and not shm.is_file():
        raise BundleError(
            "source database has a hot WAL without -shm and cannot be opened "
            "read-only; recover it under separate authorization first"
        )
    try:
        uri = f"{path.resolve().as_uri()}?mode=ro"
    except ValueError as exc:  # pragma: no cover - defensive
        raise BundleError("cannot resolve source database path") from exc
    try:
        conn = sqlite3.connect(uri, uri=True)
        # Touch the main database before the capture bracket opens. A constant
        # SELECT may not attach the WAL, so its sidecars could otherwise be
        # materialised later by our own integrity check and misreported as
        # source-writer drift.
        conn.execute("SELECT name FROM sqlite_master LIMIT 1").fetchone()
    except sqlite3.Error as exc:
        if wal.is_file() and not shm.is_file():
            raise BundleError(
                "source database has a hot WAL without -shm and cannot be opened "
                "read-only; recover it under separate authorization first"
            ) from exc
        raise BundleError(
            f"cannot open database read-only: {exc.__class__.__name__}"
        ) from exc
    conn.row_factory = sqlite3.Row
    return conn


def _table_names(conn: sqlite3.Connection) -> set[str]:
    rows = conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
    return {str(row[0]) for row in rows}


def _integrity_check(conn: sqlite3.Connection) -> str:
    rows = conn.execute("PRAGMA integrity_check").fetchall()
    return ";".join(str(row[0]) for row in rows)


def _foreign_key_violations(conn: sqlite3.Connection) -> int:
    return len(conn.execute("PRAGMA foreign_key_check").fetchall())


# --- invariants ------------------------------------------------------------


def collect_invariants(conn: sqlite3.Connection) -> dict[str, Any]:
    """Sanitized application-level state that a migration must not lose.

    Every value here is a count, an aggregate, a UTC timestamp or an enum-like
    state string. Nothing derived from `runs.config_json`, `events.detail`,
    `decisions.payload_json` or `directives.raw_response` is read, because those
    can carry account identifiers or free text.
    """
    missing = [name for name in REQUIRED_TABLES if name not in _table_names(conn)]
    if missing:
        raise BundleError(f"schema missing tables: {','.join(sorted(missing))}")

    counts = {
        table: int(conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
        for table in COUNT_TABLES
    }

    placeholders = ",".join("?" for _ in LIVE_ORDER_STATUSES)
    live_orders = int(
        conn.execute(
            f"SELECT COUNT(*) FROM orders WHERE status IN ({placeholders})",
            LIVE_ORDER_STATUSES,
        ).fetchone()[0]
    )
    open_trades = int(
        conn.execute("SELECT COUNT(*) FROM trades WHERE exit_ts IS NULL").fetchone()[0]
    )
    closed_trades = int(
        conn.execute(
            "SELECT COUNT(*) FROM trades WHERE exit_ts IS NOT NULL AND pnl IS NOT NULL"
        ).fetchone()[0]
    )

    max_ids = {
        "decision_id": conn.execute("SELECT MAX(id) FROM decisions").fetchone()[0],
        "event_id": conn.execute("SELECT MAX(id) FROM events").fetchone()[0],
        "trade_id": conn.execute("SELECT MAX(trade_id) FROM trades").fetchone()[0],
    }
    max_ids = {k: (None if v is None else int(v)) for k, v in max_ids.items()}

    return {
        "schema_version": _meta(conn, "schema_version"),
        "app_state": _meta(conn, "app_state"),
        "counts": counts,
        "open_trades": open_trades,
        "live_orders": live_orders,
        "closed_trades": closed_trades,
        "max_ids": max_ids,
        "environments": _environment_invariants(conn),
        "risk_days": _risk_day_invariants(conn),
    }


def _meta(conn: sqlite3.Connection, key: str) -> str | None:
    row = conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
    return None if row is None else str(row[0])


def _environment_invariants(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    """Per (mode, network) risk continuity — the daily-loss and consecutive-loss
    evidence that a fresh database would silently reset."""
    environments = conn.execute(
        "SELECT DISTINCT mode, network FROM runs ORDER BY mode, network"
    ).fetchall()
    result: list[dict[str, Any]] = []
    for row in environments:
        mode, network = str(row[0]), str(row[1])
        scoped = (
            "FROM trades t JOIN runs r ON r.run_id = t.run_id "
            "WHERE r.mode = ? AND r.network = ? "
            "AND t.exit_ts IS NOT NULL AND t.pnl IS NOT NULL"
        )
        agg = conn.execute(
            f"SELECT COUNT(*), COALESCE(SUM(t.pnl), 0.0), MAX(t.exit_ts) {scoped}",
            (mode, network),
        ).fetchone()
        last_exit_ts = agg[2]
        latest_date = None if last_exit_ts is None else str(last_exit_ts)[:10]
        latest_pnl = None
        if latest_date is not None:
            latest_pnl = conn.execute(
                f"SELECT COALESCE(SUM(t.pnl), 0.0) {scoped} AND substr(t.exit_ts, 1, 10) = ?",
                (mode, network, latest_date),
            ).fetchone()[0]
        pnls = conn.execute(
            f"SELECT t.pnl {scoped} ORDER BY t.exit_ts DESC, t.trade_id DESC",
            (mode, network),
        ).fetchall()
        streak = 0
        for (pnl,) in pnls:
            if float(pnl) < 0:
                streak += 1
            else:
                break
        result.append(
            {
                "mode": mode,
                "network": network,
                "runs": int(
                    conn.execute(
                        "SELECT COUNT(*) FROM runs WHERE mode = ? AND network = ?",
                        (mode, network),
                    ).fetchone()[0]
                ),
                "closed_trades": int(agg[0]),
                "realized_pnl_total": _num(agg[1]),
                "last_exit_ts": None if last_exit_ts is None else str(last_exit_ts),
                "latest_trading_date": latest_date,
                "realized_pnl_latest_date": _num(latest_pnl),
                "consecutive_closed_losses": streak,
                "open_trades": int(
                    conn.execute(
                        "SELECT COUNT(*) FROM trades t JOIN runs r ON r.run_id = t.run_id "
                        "WHERE r.mode = ? AND r.network = ? AND t.exit_ts IS NULL",
                        (mode, network),
                    ).fetchone()[0]
                ),
            }
        )
    return result


def _risk_day_invariants(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT trading_date, day_start_equity, realized_pnl_engine, realized_pnl_broker,
               max_intraday_dd, consecutive_losses_end, auto_rearms_used
        FROM risk_days ORDER BY trading_date
        """
    ).fetchall()
    return [
        {
            "trading_date": str(row[0]),
            "day_start_equity": _num(row[1]),
            "realized_pnl_engine": _num(row[2]),
            "realized_pnl_broker": _num(row[3]),
            "max_intraday_dd": _num(row[4]),
            "consecutive_losses_end": None if row[5] is None else int(row[5]),
            "auto_rearms_used": None if row[6] is None else int(row[6]),
        }
        for row in rows
    ]


def invariants_hash(invariants: dict[str, Any]) -> str:
    return _sha256_bytes(_canonical_json(invariants).encode("utf-8"))


# --- create ----------------------------------------------------------------


def _sidecar_paths(db_path: Path) -> list[Path]:
    return [db_path.with_name(db_path.name + suffix) for suffix in FORBIDDEN_SIDECARS]


def _stable_metadata(file_stat: Any) -> dict[str, int]:
    return {
        "device": int(file_stat.st_dev),
        "inode": int(file_stat.st_ino),
        "mode": int(stat.S_IMODE(file_stat.st_mode)),
        "size_bytes": int(file_stat.st_size),
        "mtime_ns": int(file_stat.st_mtime_ns),
        "ctime_ns": int(file_stat.st_ctime_ns),
    }


def _file_snapshot(path: Path) -> dict[str, Any]:
    """Hash one source component with metadata bracketing the full read."""
    try:
        before_stat = path.lstat()
    except FileNotFoundError:
        return {"present": False}
    if not stat.S_ISREG(before_stat.st_mode):
        raise BundleError("source database snapshot contains a non-regular entry")
    before = _stable_metadata(before_stat)
    digest = _sha256_file(path)
    try:
        after_stat = path.lstat()
    except FileNotFoundError:
        return {
            "present": False,
            "changed_during_hash": True,
            "metadata_before_hash": before,
        }
    if not stat.S_ISREG(after_stat.st_mode):
        raise BundleError("source database snapshot changed to a non-regular entry")
    after = _stable_metadata(after_stat)
    return {
        "present": True,
        "sha256": digest,
        "metadata_before_hash": before,
        "metadata_after_hash": after,
        "changed_during_hash": before != after,
    }


def _source_snapshot(source: Path) -> dict[str, dict[str, Any]]:
    return {
        "db": _file_snapshot(source),
        "wal": _file_snapshot(source.with_name(source.name + "-wal")),
        "shm": _file_snapshot(source.with_name(source.name + "-shm")),
    }


def _changed_snapshot_components(
    before: dict[str, dict[str, Any]],
    after: dict[str, dict[str, Any]],
) -> list[str]:
    changed: list[str] = []
    for component in ("db", "wal", "shm"):
        if (
            before[component] != after[component]
            or before[component].get("changed_during_hash", False)
            or after[component].get("changed_during_hash", False)
        ):
            changed.append(component)
    return changed


def _capture_changed_components(
    arrival: dict[str, dict[str, Any]],
    before: dict[str, dict[str, Any]],
    after: dict[str, dict[str, Any]],
) -> list[str]:
    """Return capture drift once, in deterministic component order.

    DB/WAL drift starts at arrival. SHM drift starts after the read connection
    opens because SQLite may update its own shared-memory read marks on open.
    """
    arrival_to_before = set(_changed_snapshot_components(arrival, before))
    if (
        not arrival["wal"].get("present", False)
        and before["wal"].get("present", False)
        and before["wal"].get("sha256") == _sha256_bytes(b"")
        and not before["wal"].get("changed_during_hash", False)
    ):
        # SQLite can materialise a zero-byte WAL while a read-only WAL-mode
        # database opens. It contains no source state; every other WAL
        # presence/content/metadata transition remains drift.
        arrival_to_before.discard("wal")
    before_to_after = set(_changed_snapshot_components(before, after))
    return [
        component
        for component in ("db", "wal", "shm")
        if component in before_to_after
        or (
            component in {"db", "wal"}
            and component in arrival_to_before
        )
    ]


def _paths_alias(left: Path, right: Path) -> bool:
    if left == right:
        return True
    try:
        return left.exists() and right.exists() and left.samefile(right)
    except OSError:
        return False


def _resolve_capture_paths(
    source: Path, out_dir: Path
) -> tuple[Path, Path, Path, Path, list[Path]]:
    """Resolve and reject every source/output alias before any mutation."""
    try:
        resolved_source = source.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise BundleError("cannot resolve source database path") from exc
    if not resolved_source.is_file():
        raise BundleError("source database not found")
    try:
        resolved_out = out_dir.resolve(strict=False)
    except (OSError, RuntimeError) as exc:
        raise BundleError("cannot resolve output directory path") from exc

    bundle_db = resolved_out / BUNDLE_DB_NAME
    manifest_path = resolved_out / MANIFEST_NAME
    manifest_tmp = resolved_out / f".{MANIFEST_NAME}.tmp"
    source_targets = [
        resolved_source,
        resolved_source.with_name(resolved_source.name + "-wal"),
        resolved_source.with_name(resolved_source.name + "-shm"),
    ]
    output_targets = [
        bundle_db,
        manifest_path,
        manifest_tmp,
        *_sidecar_paths(bundle_db),
    ]
    for source_target in source_targets:
        for output_target in output_targets:
            if _paths_alias(source_target, output_target):
                raise BundleError("source and output bundle targets overlap or alias")
    for index, left in enumerate(output_targets):
        for right in output_targets[index + 1 :]:
            if _paths_alias(left, right):
                raise BundleError("output bundle targets overlap or alias")
    return resolved_source, resolved_out, bundle_db, manifest_path, output_targets


def _validate_timestamp(raw: str | None) -> str:
    if raw is None:
        return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        parsed = datetime.strptime(raw, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise BundleError("--timestamp must be YYYY-MM-DDTHH:MM:SSZ") from exc
    return parsed.strftime("%Y-%m-%dT%H:%M:%SZ")


def create_bundle(
    source: Path,
    out_dir: Path,
    timestamp: str | None = None,
    allow_live_source: bool = False,
    force: bool = False,
) -> tuple[int, dict[str, Any]]:
    """Capture a WAL-consistent bundle. Returns ``(exit_code, report)``."""
    generated_at = _validate_timestamp(timestamp)
    source, out_dir, bundle_db, manifest_path, output_targets = _resolve_capture_paths(
        source, out_dir
    )
    if (bundle_db.exists() or manifest_path.exists()) and not force:
        raise BundleError("output directory already holds a bundle; pass --force to replace")
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_tmp = out_dir / f".{MANIFEST_NAME}.tmp"
    for stale in output_targets:
        if stale.exists() or stale.is_symlink():
            stale.unlink()

    def discard() -> None:
        """Fail closed: never leave a half-trusted artefact behind."""
        for path in output_targets:
            if path.exists() or path.is_symlink():
                path.unlink()

    def reject(reason: str) -> tuple[int, dict[str, Any]]:
        discard()
        return 2, {"verdict": "INVALID", "failures": [reason], "exit_code": 2}

    # Preserve arrival provenance separately. SQLite may materialise empty
    # WAL/SHM files while opening a read-only connection; those tool-created
    # sidecars are not falsely reported as files that existed on arrival.
    source_snapshot_arrival = _source_snapshot(source)
    if not source_snapshot_arrival["db"].get("present") \
       or not source_snapshot_arrival["db"].get("sha256"):
        raise BundleError("source database changed while its arrival snapshot was captured")
    source_facts = {
        "db_sha256": source_snapshot_arrival["db"].get("sha256"),
        "wal_present": source_snapshot_arrival["wal"]["present"],
        "wal_sha256": source_snapshot_arrival["wal"].get("sha256"),
        "shm_present": source_snapshot_arrival["shm"]["present"],
        "shm_sha256": source_snapshot_arrival["shm"].get("sha256"),
    }

    failures: list[str] = []
    src = _connect_readonly(source)
    try:
        # SQLite can update read marks in an existing -shm while establishing a
        # read-only connection. Bracket the actual integrity/invariant/backup
        # capture after that setup and before close so our own connection
        # lifecycle is not misreported as source-writer drift.
        source_snapshot_before = _source_snapshot(source)
        if not source_snapshot_before["db"].get("present") \
           or not source_snapshot_before["db"].get("sha256"):
            raise BundleError(
                "source database changed while its initial snapshot was captured"
            )
        source_integrity = _integrity_check(src)
        if source_integrity != "ok":
            return reject("source_integrity_check_failed")
        source_fk = _foreign_key_violations(src)
        if source_fk:
            return reject("source_foreign_key_violations")

        # Schema check happens before anything is written, so an unsuitable
        # source produces no output file at all.
        source_invariants = collect_invariants(src)

        # Online backup: one consistent snapshot, never a db/wal/shm copy.
        try:
            dst = sqlite3.connect(bundle_db)
            try:
                src.backup(dst)
                # Leave no WAL behind so the bundle is one self-contained file.
                dst.execute("PRAGMA journal_mode=DELETE")
                dst.commit()
            finally:
                dst.close()
        except (OSError, sqlite3.Error):
            discard()
            raise
        source_snapshot_after = _source_snapshot(source)
    finally:
        src.close()

    present_sidecars = [p.name for p in _sidecar_paths(bundle_db) if p.exists()]
    if present_sidecars:
        return reject("bundle_sidecar_present")

    try:
        bundle_conn = _connect_readonly(bundle_db)
        try:
            bundle_integrity = _integrity_check(bundle_conn)
            if bundle_integrity != "ok":
                return reject("bundle_integrity_check_failed")
            bundle_fk = _foreign_key_violations(bundle_conn)
            if bundle_fk:
                return reject("bundle_foreign_key_violations")
            bundle_invariants = collect_invariants(bundle_conn)
        finally:
            bundle_conn.close()
    except (OSError, sqlite3.Error, BundleError):
        discard()
        raise

    changed_components = _capture_changed_components(
        source_snapshot_arrival,
        source_snapshot_before,
        source_snapshot_after,
    )
    invariants_changed = bundle_invariants != source_invariants
    changed_during_capture = bool(changed_components or invariants_changed)
    if changed_during_capture and not allow_live_source:
        failures.append("source_changed_during_capture")

    manifest: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "tool": TOOL_NAME,
        "generated_at_utc": generated_at,
        "capture_mode": CAPTURE_MODE,
        "source": {
            "db_name": BUNDLE_DB_NAME,
            **source_facts,
            "integrity_check": source_integrity,
            "foreign_key_violations": source_fk,
            "invariants_sha256": invariants_hash(source_invariants),
            "changed_during_capture": changed_during_capture,
            "capture_snapshot": {
                "arrival": source_snapshot_arrival,
                "before": source_snapshot_before,
                "after": source_snapshot_after,
                "changed_components": changed_components,
                "invariants_changed": invariants_changed,
            },
        },
        "bundle": {
            "db_name": BUNDLE_DB_NAME,
            "db_sha256": _sha256_file(bundle_db),
            "integrity_check": bundle_integrity,
            "foreign_key_violations": bundle_fk,
            "sidecar_files": [],
        },
        "invariants": bundle_invariants,
        "invariants_sha256": invariants_hash(bundle_invariants),
        "verdict": "INVALID" if failures else "CAPTURED",
        "exit_code": 2 if failures else 0,
        "integrity_sha256": "",
    }
    try:
        _assert_sanitized(manifest)
    except SanitizationError:
        discard()
        raise
    manifest["integrity_sha256"] = _integrity_hash(manifest)

    if failures:
        drift_evidence = manifest["source"]["capture_snapshot"]
        discard()
        return 2, {
            "verdict": "INVALID",
            "failures": failures,
            "exit_code": 2,
            "drift_evidence": drift_evidence,
        }

    try:
        manifest_tmp.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        manifest_tmp.replace(manifest_path)
    except OSError:
        discard()
        raise
    return 0, {
        "verdict": "CAPTURED",
        "failures": [],
        "exit_code": 0,
        "bundle_db_sha256": manifest["bundle"]["db_sha256"],
        "invariants_sha256": manifest["invariants_sha256"],
        "integrity_sha256": manifest["integrity_sha256"],
        "generated_at_utc": generated_at,
    }


# --- verify ----------------------------------------------------------------


def _typed(manifest: dict[str, Any], failures: list[str]) -> bool:
    ok = True
    for field in REQUIRED_MANIFEST_FIELDS:
        if field not in manifest:
            failures.append(f"missing_field:{field}")
            ok = False
    if not ok:
        return False
    for field, expected in (
        ("schema_version", str),
        ("tool", str),
        ("generated_at_utc", str),
        ("capture_mode", str),
        ("source", dict),
        ("bundle", dict),
        ("invariants", dict),
        ("invariants_sha256", str),
        ("verdict", str),
        ("exit_code", int),
        ("integrity_sha256", str),
    ):
        if not isinstance(manifest[field], expected):
            failures.append(f"invalid_type:{field}")
            ok = False
    return ok


def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and SHA256_RE.fullmatch(value) is not None


def _validate_snapshot_state(
    state: Any, label: str, failures: list[str]
) -> bool:
    if not isinstance(state, dict):
        failures.append(f"invalid_type:{label}")
        return False
    if not isinstance(state.get("present"), bool):
        failures.append(f"invalid_type:{label}.present")
        return False
    if not state["present"]:
        return True
    if not _is_sha256(state.get("sha256")):
        failures.append(f"invalid_sha256:{label}.sha256")
    if not isinstance(state.get("changed_during_hash"), bool):
        failures.append(f"invalid_type:{label}.changed_during_hash")
    metadata_fields = (
        "device",
        "inode",
        "mode",
        "size_bytes",
        "mtime_ns",
        "ctime_ns",
    )
    for phase in ("metadata_before_hash", "metadata_after_hash"):
        metadata = state.get(phase)
        if not isinstance(metadata, dict):
            failures.append(f"invalid_type:{label}.{phase}")
            continue
        for field in metadata_fields:
            if type(metadata.get(field)) is not int:
                failures.append(f"invalid_type:{label}.{phase}.{field}")
    return not failures


def _validate_manifest_contract(
    manifest: dict[str, Any], failures: list[str]
) -> bool:
    """Validate every field before any manifest-controlled path is used."""
    if not _typed(manifest, failures):
        return False
    try:
        _assert_sanitized(manifest)
    except SanitizationError:
        failures.append("unsanitized_manifest")
        return False

    if manifest["schema_version"] != SCHEMA_VERSION:
        failures.append("unsupported_schema_version")
    if manifest["tool"] != TOOL_NAME:
        failures.append("unexpected_tool")
    if manifest["capture_mode"] != CAPTURE_MODE:
        failures.append("unexpected_capture_mode")
    if manifest["verdict"] != "CAPTURED":
        failures.append("manifest_not_captured")
    if manifest["exit_code"] != 0:
        failures.append("manifest_exit_code_not_zero")
    try:
        _validate_timestamp(manifest["generated_at_utc"])
    except BundleError:
        failures.append("invalid_generated_at_utc")

    for field in ("invariants_sha256", "integrity_sha256"):
        if not _is_sha256(manifest[field]):
            failures.append(f"invalid_sha256:{field}")

    source = manifest["source"]
    bundle = manifest["bundle"]
    source_contract = {
        "db_name": str,
        "db_sha256": str,
        "wal_present": bool,
        "wal_sha256": (str, type(None)),
        "shm_present": bool,
        "shm_sha256": (str, type(None)),
        "integrity_check": str,
        "foreign_key_violations": int,
        "invariants_sha256": str,
        "changed_during_capture": bool,
        "capture_snapshot": dict,
    }
    bundle_contract = {
        "db_name": str,
        "db_sha256": str,
        "integrity_check": str,
        "foreign_key_violations": int,
        "sidecar_files": list,
    }
    for section_name, section, contract in (
        ("source", source, source_contract),
        ("bundle", bundle, bundle_contract),
    ):
        for field, expected in contract.items():
            if field not in section:
                failures.append(f"missing_field:{section_name}.{field}")
            elif not isinstance(section[field], expected):
                failures.append(f"invalid_type:{section_name}.{field}")

    if failures:
        return False
    snapshot = source["capture_snapshot"]
    for field, expected in (
        ("arrival", dict),
        ("before", dict),
        ("after", dict),
        ("changed_components", list),
        ("invariants_changed", bool),
    ):
        if field not in snapshot:
            failures.append(f"missing_field:source.capture_snapshot.{field}")
        elif not isinstance(snapshot[field], expected):
            failures.append(f"invalid_type:source.capture_snapshot.{field}")
    if failures:
        return False
    for phase in ("arrival", "before", "after"):
        for component in ("db", "wal", "shm"):
            if component not in snapshot[phase]:
                failures.append(
                    f"missing_field:source.capture_snapshot.{phase}.{component}"
                )
                continue
            _validate_snapshot_state(
                snapshot[phase][component],
                f"source.capture_snapshot.{phase}.{component}",
                failures,
            )
    if failures:
        return False
    changed_components = snapshot["changed_components"]
    if (
        any(component not in {"db", "wal", "shm"} for component in changed_components)
        or len(changed_components) != len(set(changed_components))
    ):
        failures.append("invalid_changed_components")
    elif changed_components != _capture_changed_components(
        snapshot["arrival"], snapshot["before"], snapshot["after"]
    ):
        failures.append("changed_components_mismatch")
    if source["changed_during_capture"] != bool(
        changed_components or snapshot["invariants_changed"]
    ):
        failures.append("changed_during_capture_mismatch")
    arrival = snapshot["arrival"]
    if source["db_sha256"] != arrival["db"].get("sha256"):
        failures.append("source_db_hash_snapshot_mismatch")
    for component in ("wal", "shm"):
        if source[f"{component}_present"] != arrival[component]["present"]:
            failures.append(f"source_{component}_presence_snapshot_mismatch")
        if source[f"{component}_sha256"] != arrival[component].get("sha256"):
            failures.append(f"source_{component}_hash_snapshot_mismatch")
    if failures:
        return False
    if source["db_name"] != BUNDLE_DB_NAME or bundle["db_name"] != BUNDLE_DB_NAME:
        failures.append("unexpected_database_name")
    for section_name, section, fields in (
        ("source", source, ("db_sha256", "invariants_sha256")),
        ("bundle", bundle, ("db_sha256",)),
    ):
        for field in fields:
            if not _is_sha256(section[field]):
                failures.append(f"invalid_sha256:{section_name}.{field}")
    for present_field, hash_field in (
        ("wal_present", "wal_sha256"),
        ("shm_present", "shm_sha256"),
    ):
        present = source[present_field]
        digest = source[hash_field]
        if present != (digest is not None) or (digest is not None and not _is_sha256(digest)):
            failures.append(f"invalid_sidecar_hash_contract:{hash_field}")
    if source["integrity_check"] != "ok" or source["foreign_key_violations"] != 0:
        failures.append("source_checks_not_clean")
    if bundle["integrity_check"] != "ok" or bundle["foreign_key_violations"] != 0:
        failures.append("bundle_checks_not_clean")
    if bundle["sidecar_files"] != []:
        failures.append("manifest_records_bundle_sidecars")
    return not failures


def verify_bundle(
    bundle_dir: Path,
    expect_bundle_sha256: str | None = None,
    expect_invariants_sha256: str | None = None,
) -> tuple[int, dict[str, Any]]:
    for label, digest in (
        ("expect_bundle_sha256", expect_bundle_sha256),
        ("expect_invariants_sha256", expect_invariants_sha256),
    ):
        if digest is None:
            raise BundleError(f"{label} is required")
        if SHA256_RE.fullmatch(digest.lower()) is None:
            raise BundleError(f"{label} must be exactly 64 hex characters")

    manifest_path = bundle_dir / MANIFEST_NAME
    if not manifest_path.is_file():
        raise BundleError(f"manifest not found: {MANIFEST_NAME}")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise BundleError(f"manifest is not valid JSON: {exc.__class__.__name__}") from exc
    if not isinstance(manifest, dict):
        raise BundleError("manifest root is not an object")

    failures: list[str] = []
    if not _validate_manifest_contract(manifest, failures):
        return 2, {"verdict": "INVALID", "failures": failures, "exit_code": 2}

    if _integrity_hash(manifest) != manifest["integrity_sha256"]:
        failures.append("integrity_hash_mismatch")

    bundle_db = bundle_dir / BUNDLE_DB_NAME
    present_sidecars = [p.name for p in _sidecar_paths(bundle_db) if p.exists()]
    if present_sidecars:
        failures.append("bundle_sidecar_present")

    if not bundle_db.is_file():
        failures.append("bundle_db_missing")
        return 2, {"verdict": "INVALID", "failures": failures, "exit_code": 2}

    actual_db_sha = _sha256_file(bundle_db)
    if actual_db_sha != manifest["bundle"].get("db_sha256"):
        failures.append("bundle_db_hash_mismatch")
    if expect_bundle_sha256 and expect_bundle_sha256.lower() != actual_db_sha:
        failures.append("bundle_db_hash_not_expected")

    try:
        conn = _connect_readonly(bundle_db)
        try:
            if _integrity_check(conn) != "ok":
                failures.append("bundle_integrity_check_failed")
                return 2, {"verdict": "INVALID", "failures": failures, "exit_code": 2}
            if _foreign_key_violations(conn):
                failures.append("bundle_foreign_key_violations")
            try:
                recomputed = collect_invariants(conn)
            except BundleError:
                failures.append("invariants_unavailable")
                return 2, {"verdict": "INVALID", "failures": failures, "exit_code": 2}
        finally:
            conn.close()
    except (OSError, sqlite3.Error, BundleError):
        failures.append("bundle_database_unreadable")
        return 2, {"verdict": "INVALID", "failures": failures, "exit_code": 2}

    if recomputed != manifest["invariants"]:
        failures.append("invariants_drift")
    recomputed_hash = invariants_hash(recomputed)
    if recomputed_hash != manifest["invariants_sha256"]:
        failures.append("invariants_hash_mismatch")
    if expect_invariants_sha256 and expect_invariants_sha256.lower() != recomputed_hash:
        failures.append("invariants_hash_not_expected")

    exit_code = 2 if failures else 0
    return exit_code, {
        "verdict": "INVALID" if failures else "VALID",
        "failures": failures,
        "exit_code": exit_code,
        "bundle_db_sha256": actual_db_sha,
        "invariants_sha256": recomputed_hash,
    }


# --- CLI -------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=TOOL_NAME,
        description="Capture and verify a WAL-consistent bridge state bundle.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create", help="capture a WAL-consistent bundle")
    create.add_argument("--source", required=True, help="path to the live bridge.db")
    create.add_argument("--out-dir", required=True, help="empty directory to write the bundle into")
    create.add_argument("--timestamp", default=None, help="YYYY-MM-DDTHH:MM:SSZ")
    create.add_argument(
        "--allow-live-source",
        action="store_true",
        help=(
            "record source drift during capture as a warning instead of failing. "
            "Never use this for a cutover capture: the writer must already be quiesced."
        ),
    )
    create.add_argument("--force", action="store_true", help="replace an existing bundle")

    verify = sub.add_parser("verify", help="re-derive and check an existing bundle")
    verify.add_argument("--bundle-dir", required=True)
    verify.add_argument("--expect-bundle-sha256", default=None)
    verify.add_argument("--expect-invariants-sha256", default=None)
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        if args.command == "create":
            code, report = create_bundle(
                source=Path(args.source),
                out_dir=Path(args.out_dir),
                timestamp=args.timestamp,
                allow_live_source=args.allow_live_source,
                force=args.force,
            )
        else:
            code, report = verify_bundle(
                bundle_dir=Path(args.bundle_dir),
                expect_bundle_sha256=args.expect_bundle_sha256,
                expect_invariants_sha256=args.expect_invariants_sha256,
            )
    except SanitizationError as exc:
        print(f"{TOOL_NAME}: refusing to emit unsanitized field ({exc})", file=sys.stderr)
        return 3
    except BundleError as exc:
        print(f"{TOOL_NAME}: {exc}", file=sys.stderr)
        return 3
    except (OSError, sqlite3.Error) as exc:
        print(f"{TOOL_NAME}: {exc.__class__.__name__}", file=sys.stderr)
        return 3
    try:
        _assert_sanitized(report, "report")
    except SanitizationError:
        print(f"{TOOL_NAME}: refusing to emit unsanitized report", file=sys.stderr)
        return 3
    print(json.dumps(report, indent=2, sort_keys=True))
    return code


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
