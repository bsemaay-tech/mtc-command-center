"""SQLite Store with schema v3 from the architecture spec.

V3 (TS-P1-002) adds the durable identity table (order_identities) for
intent/request identity, fail-closed double-submission prevention, and
collision-safe order persistence.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Literal


def _to_iso(value: datetime | str | None) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        # Canonicalize instead of passing through: lexicographic range queries
        # on TEXT timestamps are only correct if every stored value has the
        # same aware-UTC ISO shape. Invalid strings raise (fail closed).
        value = datetime.fromisoformat(value)
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(UTC).isoformat()


def _json(value: Any) -> str:
    def default(obj: Any) -> str:
        if isinstance(obj, datetime):
            return _to_iso(obj) or ""
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=default)

# ---------------------------------------------------------------------------
# TS-P1-002: durable identity primitives
# ---------------------------------------------------------------------------


def _float_hex(value: float) -> str:
    """Deterministic finite IEEE-754 representation string."""
    if value != value:
        raise ValueError("float NaN not allowed in identity preimage")
    if value == float("inf") or value == float("-inf"):
        raise ValueError("float Infinity not allowed in identity preimage")
    if value == 0.0 and str(value).startswith("-"):
        value = 0.0
    return value.hex()


def _normalize_ts(ts: datetime) -> str:
    """UTC timestamp with fixed microsecond precision + Z."""
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=UTC)
    utc = ts.astimezone(UTC)
    return utc.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"


def _canonical_json(obj: Any) -> str:
    """Deterministic JSON: sorted keys, compact separators, UTF-8, no NaN."""
    return _json(obj)


_INTENT_VERSION = "ts-p1-002-intent-v1"
_REQUEST_VERSION = "ts-p1-002-request-v1"


def compute_intent_id(
    strategy_id: str, symbol: str, direction: str, signal_ts: datetime
) -> tuple[str, str]:
    """Return (intent_id, exact_canonical_preimage)."""
    preimage = _canonical_json({
        "version": _INTENT_VERSION,
        "strategy_id": strategy_id,
        "symbol": symbol.upper(),
        "direction": direction.upper(),
        "signal_ts": _normalize_ts(signal_ts),
    })
    digest = hashlib.sha256(preimage.encode("utf-8")).hexdigest()
    return f"intent-v1:{digest}", preimage


def compute_request_id(
    intent_id: str, symbol: str, direction: str,
    ref_price: float, qty: float, entry_type: str,
    limit_price: float | None, stop_loss: float,
    take_profit: float | None, leverage: int,
) -> tuple[str, str]:
    """Return (request_id, exact_canonical_preimage)."""
    preimage = _canonical_json({
        "version": _REQUEST_VERSION,
        "intent_id": intent_id,
        "symbol": symbol.upper(),
        "direction": direction.upper(),
        "ref_price": _float_hex(ref_price),
        "qty": _float_hex(qty),
        "entry_type": entry_type,
        "limit_price": None if limit_price is None else _float_hex(limit_price),
        "stop_loss": _float_hex(stop_loss),
        "take_profit": None if take_profit is None else _float_hex(take_profit),
        "leverage": leverage,
    })
    digest = hashlib.sha256(preimage.encode("utf-8")).hexdigest()
    return f"request-v1:{digest}", preimage



_V3_DDL = """
            CREATE TABLE meta (
              key TEXT PRIMARY KEY,
              value TEXT
            );

            CREATE TABLE runs (
              run_id TEXT PRIMARY KEY,
              started_ts TEXT,
              ended_ts TEXT,
              mode TEXT CHECK(mode IN ('paper','dry_run','live')),
              network TEXT,
              config_json TEXT
            );

            CREATE TABLE bars (
              coin TEXT,
              tf TEXT,
              bar_end_ts TEXT,
              open REAL,
              high REAL,
              low REAL,
              close REAL,
              volume REAL,
              PRIMARY KEY(coin, tf, bar_end_ts)
            );

            CREATE TABLE decisions (
              id INTEGER PRIMARY KEY,
              decision_uid TEXT NOT NULL,
              run_id TEXT,
              ts TEXT,
              coin TEXT,
              stage TEXT,
              trade_id INTEGER,
              payload_json TEXT,
              payload_version INTEGER DEFAULT 1
            );

            CREATE TABLE orders (
              cloid TEXT PRIMARY KEY,
              oid INTEGER,
              group_id TEXT,
              order_ref TEXT,
              order_json TEXT,
              decision_uid TEXT,
              trade_id INTEGER,
              role TEXT,
              status TEXT,
              qty REAL,
              filled_qty REAL,
              avg_fill_px REAL,
              ts_submit TEXT,
              ts_last TEXT
            );

            CREATE TABLE fills (
              fill_id TEXT PRIMARY KEY,
              cloid TEXT,
              decision_uid TEXT,
              fill_ts TEXT,
              qty REAL,
              px REAL,
              fee REAL,
              funding REAL
            );

            CREATE TABLE trades (
              trade_id INTEGER PRIMARY KEY,
              run_id TEXT,
              coin TEXT,
              direction TEXT,
              qty REAL,
              entry_decision_uid TEXT,
              signal_ts TEXT,
              decision_ts TEXT,
              submit_ts TEXT,
              first_fill_ts TEXT,
              last_fill_ts TEXT,
              expected_px REAL,
              entry_px REAL,
              entry_ts TEXT,
              exit_px REAL,
              exit_ts TEXT,
              exit_reason TEXT,
              pnl REAL,
              slippage_bps_entry REAL,
              risk_dollars REAL,
              risk_pct REAL,
              leverage INTEGER,
              sl_initial REAL,
              tp_initial REAL,
              llm_directive_id INTEGER
            );

            CREATE TABLE equity (
              run_id TEXT,
              ts TEXT,
              equity REAL,
              cash REAL,
              unrealized REAL,
              realized_today REAL,
              PRIMARY KEY(run_id, ts)
            );

            CREATE TABLE risk_days (
              trading_date TEXT PRIMARY KEY,
              day_start_equity REAL,
              realized_pnl_engine REAL,
              realized_pnl_broker REAL,
              max_intraday_dd REAL,
              consecutive_losses_end INTEGER,
              auto_rearms_used INTEGER
            );

            CREATE TABLE directives (
              id INTEGER PRIMARY KEY,
              ts TEXT,
              regime TEXT,
              confidence REAL,
              ttl_minutes INTEGER,
              rationale TEXT,
              sources_hash TEXT,
              raw_response TEXT,
              valid INTEGER
            );

            CREATE TABLE llm_calls (
              id INTEGER PRIMARY KEY,
              ts TEXT,
              role TEXT,
              model TEXT,
              prompt_hash TEXT,
              latency_ms INTEGER,
              verdict TEXT,
              tokens_in INTEGER,
              tokens_out INTEGER,
              cost_est REAL
            );

            CREATE TABLE events (
              id INTEGER PRIMARY KEY,
              run_id TEXT,
              ts TEXT,
              severity TEXT,
              code TEXT,
              detail TEXT
            );

            CREATE TABLE signal_fingerprints (
              run_id TEXT,
              fingerprint TEXT,
              decision_uid TEXT,
              ts TEXT,
              PRIMARY KEY(run_id, fingerprint)
            );

            CREATE TABLE order_identities (
              intent_id TEXT PRIMARY KEY,
              intent_preimage TEXT NOT NULL,
              intent_version TEXT NOT NULL,
              request_id TEXT UNIQUE NOT NULL,
              request_preimage TEXT NOT NULL,
              request_version TEXT NOT NULL,
              cloid_seed TEXT NOT NULL,
              origin_run_id TEXT NOT NULL,
              original_decision_uid TEXT NOT NULL,
              state TEXT NOT NULL CHECK(state IN (
                'RESERVED','SUBMITTED','LEGACY_RESERVED','LEGACY_SUBMITTED'
              )),
              reserved_ts TEXT,
              submitted_ts TEXT
            );

            CREATE INDEX idx_order_identities_request_id ON order_identities(request_id);
            CREATE INDEX idx_order_identities_state ON order_identities(state);
            CREATE INDEX idx_order_identities_origin_run ON order_identities(origin_run_id);
            """



# -------------------------------------------------------------------
# Exception classes
# -------------------------------------------------------------------


class IdentityCollisionError(Exception):
    """Durable identity collision: same digest, different preimage."""


class IdentityMismatchError(Exception):
    """Same intent maps to a different request - material change."""


class ReservationBlockedError(Exception):
    """Reservation blocked: intent already exists in any state."""


class SchemaVersionError(Exception):
    """Unsupported or corrupt schema version."""


class V2MigrationError(Exception):
    """v2 -> v3 migration failed; rollback completed."""


class Store:
    """Small SQLite access layer for the bridge runtime database."""

    _SCHEMA_VERSION = 3

    def __init__(self, db_path: str | Path, clock: Callable[[], datetime] | None = None):
        self.db_path = Path(db_path)
        self._conn: sqlite3.Connection | None = None
        self._clock: Callable[[], datetime] = clock or (lambda: datetime.now(UTC))

    @property
    def conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA foreign_keys=ON")
        return self._conn

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def initialize(self) -> None:
        """Version-checked schema initialisation.

        None  -> fresh v3 creation
        2     -> migrate v2 -> v3
        3     -> idempotent reopen
        other -> SchemaVersionError
        """
        existing = self._read_schema_version()
        if existing is None:
            self._init_v3_fresh()
        elif existing == 2:
            self._migrate_v2_to_v3()
        elif existing == 3:
            self._ensure_v3_schema()
        else:
            raise SchemaVersionError(
                f"Unsupported schema version {existing!r}; "
                "expected None (fresh), 2, or 3."
            )
    # -------------------------------------------------------------------
    # Schema version helpers
    # -------------------------------------------------------------------

    def _read_schema_version(self) -> int | None:
        """Return the stored schema version or None if meta table is absent."""
        try:
            row = self.conn.execute(
                "SELECT value FROM meta WHERE key = 'schema_version'"
            ).fetchone()
        except sqlite3.OperationalError:
            return None
        if row is None:
            return None
        try:
            return int(row["value"])
        except (TypeError, ValueError):
            raise SchemaVersionError(
                f"Corrupt schema_version value: {row['value']!r}"
            )

    def _write_schema_version(self, version: int) -> None:
        self.conn.execute(
            "INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', ?)",
            (str(version),),
        )
        self.conn.commit()

    def _init_v3_fresh(self) -> None:
        """Execute the full v3 DDL on a pristine database."""
        self.conn.executescript(_V3_DDL)
        self._write_schema_version(3)

    def _ensure_v3_schema(self) -> None:
        """Idempotent reopen: ensure all tables/indices exist."""
        self.conn.executescript(_V3_DDL)
        stored = self._read_schema_version()
        if stored != 3:
            self._write_schema_version(3)
    def _migrate_v2_to_v3(self) -> None:
        """Migrate a v2 database to v3 in a single transaction.

        1. Create order_identities table and its indices.
        2. Backfill from signal_fingerprints joined with SIGNAL/RISK_PASS
           decisions: LEGACY_RESERVED for SIGNAL, LEGACY_SUBMITTED for
           RISK_PASS.
        3. Write schema_version = 3.
        """
        try:
            with self.conn:
                self.conn.executescript("""
                    CREATE TABLE IF NOT EXISTS order_identities (
                      intent_id TEXT PRIMARY KEY,
                      intent_preimage TEXT NOT NULL,
                      intent_version TEXT NOT NULL,
                      request_id TEXT UNIQUE NOT NULL,
                      request_preimage TEXT NOT NULL,
                      request_version TEXT NOT NULL,
                      cloid_seed TEXT NOT NULL,
                      origin_run_id TEXT NOT NULL,
                      original_decision_uid TEXT NOT NULL,
                      state TEXT NOT NULL CHECK(state IN (
                        'RESERVED','SUBMITTED','LEGACY_RESERVED','LEGACY_SUBMITTED'
                      )),
                      reserved_ts TEXT,
                      submitted_ts TEXT
                    );

                    CREATE INDEX IF NOT EXISTS idx_order_identities_request_id
                      ON order_identities(request_id);
                    CREATE INDEX IF NOT EXISTS idx_order_identities_state
                      ON order_identities(state);
                    CREATE INDEX IF NOT EXISTS idx_order_identities_origin_run
                      ON order_identities(origin_run_id);
                """)

                rows = self.conn.execute(
                    """
                    SELECT sf.run_id, sf.fingerprint, sf.decision_uid, sf.ts
                    FROM signal_fingerprints sf
                    ORDER BY sf.ts
                    """
                ).fetchall()

                for row in rows:
                    run_id = str(row["run_id"])
                    fingerprint = str(row["fingerprint"])
                    signal_uid = str(row["decision_uid"])
                    ts_val = str(row["ts"])

                    rp_row = self.conn.execute(
                        """
                        SELECT d.decision_uid, d.ts
                        FROM decisions d
                        WHERE d.stage = 'RISK_PASS'
                          AND d.run_id = ?
                          AND d.decision_uid LIKE ?
                        ORDER BY d.id LIMIT 1
                        """,
                        (run_id, signal_uid.replace("SIGNAL:", "RISK_PASS:")),
                    ).fetchone()

                    legacy_intent_id = f"legacy-v2:intent:{run_id}:{fingerprint}"
                    legacy_request_id = f"legacy-v2:request:{run_id}:{fingerprint}"

                    if rp_row is not None:
                        self.conn.execute(
                            """
                            INSERT OR IGNORE INTO order_identities(
                              intent_id, intent_preimage, intent_version,
                              request_id, request_preimage, request_version,
                              cloid_seed, origin_run_id, original_decision_uid,
                              state, reserved_ts, submitted_ts
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """,
                            (
                                legacy_intent_id, fingerprint, "legacy-v2",
                                legacy_request_id, fingerprint, "legacy-v2",
                                f"legacy:{fingerprint[:32]}",
                                run_id, str(rp_row["decision_uid"]),
                                "LEGACY_SUBMITTED", ts_val, str(rp_row["ts"]),
                            ),
                        )
                    else:
                        self.conn.execute(
                            """
                            INSERT OR IGNORE INTO order_identities(
                              intent_id, intent_preimage, intent_version,
                              request_id, request_preimage, request_version,
                              cloid_seed, origin_run_id, original_decision_uid,
                              state, reserved_ts, submitted_ts
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """,
                            (
                                legacy_intent_id, fingerprint, "legacy-v2",
                                legacy_request_id, fingerprint, "legacy-v2",
                                f"legacy:{fingerprint[:32]}",
                                run_id, signal_uid,
                                "LEGACY_RESERVED", ts_val, None,
                            ),
                        )

                self._write_schema_version(3)

        except Exception:
            raise V2MigrationError(
                "v2 -> v3 migration failed; the database has been rolled back "
                "to its pre-migration state."
            )
    # -------------------------------------------------------------------
    # Durable identity store methods (TS-P1-002)
    # -------------------------------------------------------------------

    def reserve_identity(
        self,
        intent_id: str,
        intent_preimage: str,
        request_id: str,
        request_preimage: str,
        cloid_seed: str,
        origin_run_id: str,
        original_decision_uid: str,
        reserved_ts: datetime | str,
    ) -> None:
        """Insert a RESERVED row. Raises on collision or preimage mismatch."""
        ts = _to_iso(reserved_ts)
        try:
            self.conn.execute(
                """
                INSERT INTO order_identities(
                  intent_id, intent_preimage, intent_version,
                  request_id, request_preimage, request_version,
                  cloid_seed, origin_run_id, original_decision_uid,
                  state, reserved_ts
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'RESERVED', ?)
                """,
                (
                    intent_id, intent_preimage, _INTENT_VERSION,
                    request_id, request_preimage, _REQUEST_VERSION,
                    cloid_seed, origin_run_id, original_decision_uid, ts,
                ),
            )
            self.conn.commit()
        except sqlite3.IntegrityError as exc:
            existing = self.get_identity(intent_id)
            if existing is None:
                existing_by_req = self.get_identity_by_request(request_id)
                if existing_by_req is not None and existing_by_req["intent_id"] != intent_id:
                    raise IdentityCollisionError(
                        f"request_id {request_id!r} already bound to "
                        f"intent {existing_by_req['intent_id']!r}"
                    ) from exc
                raise ReservationBlockedError(
                    f"Reservation blocked for intent {intent_id!r}"
                ) from exc
            if existing["intent_preimage"] != intent_preimage:
                raise IdentityCollisionError(
                    f"intent_id {intent_id!r} collision: preimage mismatch"
                )
            if existing["request_id"] != request_id:
                raise IdentityMismatchError(
                    f"intent {intent_id!r} already bound to "
                    f"request {existing['request_id']!r}, not {request_id!r}"
                )
            raise ReservationBlockedError(
                f"Reservation blocked: intent {intent_id!r} already "
                f"exists in state {existing['state']!r}"
            ) from exc

    def finalize_identity(
        self, intent_id: str, submitted_ts: datetime | str,
    ) -> None:
        """Transition an identity from RESERVED -> SUBMITTED."""
        ts = _to_iso(submitted_ts)
        cursor = self.conn.execute(
            """
            UPDATE order_identities
            SET state = 'SUBMITTED', submitted_ts = ?
            WHERE intent_id = ? AND state = 'RESERVED'
            """,
            (ts, intent_id),
        )
        self.conn.commit()
        if cursor.rowcount != 1:
            existing = self.get_identity(intent_id)
            if existing is None:
                raise LookupError(
                    f"Cannot finalize identity: {intent_id!r} not found"
                )
            raise ReservationBlockedError(
                f"Cannot finalize identity: {intent_id!r} is "
                f"{existing['state']!r}, not RESERVED"
            )

    def get_identity(self, intent_id: str) -> dict[str, Any] | None:
        row = self.conn.execute(
            "SELECT * FROM order_identities WHERE intent_id = ?",
            (intent_id,),
        ).fetchone()
        return None if row is None else dict(row)

    def get_identity_by_request(self, request_id: str) -> dict[str, Any] | None:
        row = self.conn.execute(
            "SELECT * FROM order_identities WHERE request_id = ?",
            (request_id,),
        ).fetchone()
        return None if row is None else dict(row)

    def check_identity_preimage(
        self, intent_id: str, intent_preimage: str
    ) -> bool:
        row = self.conn.execute(
            "SELECT intent_preimage FROM order_identities WHERE intent_id = ?",
            (intent_id,),
        ).fetchone()
        if row is None:
            return False
        return str(row["intent_preimage"]) == intent_preimage

    def get_meta(self, key: str) -> str | None:
        row = self.conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
        return None if row is None else str(row["value"])

    def set_meta(self, key: str, value: str) -> None:
        self.conn.execute(
            "INSERT OR REPLACE INTO meta(key, value) VALUES (?, ?)",
            (key, value),
        )
        self.conn.commit()

    def create_run(self, run_id: str, mode: str, network: str, config: dict[str, Any]) -> None:
        self.conn.execute(
            """
            INSERT INTO runs(run_id, started_ts, ended_ts, mode, network, config_json)
            VALUES (?, ?, NULL, ?, ?, ?)
            """,
            (run_id, _to_iso(datetime.now(UTC)), mode, network, _json(config)),
        )
        self.conn.commit()

    def insert_bar(
        self,
        coin: str,
        tf: str,
        bar_end_ts: datetime | str,
        open: float,
        high: float,
        low: float,
        close: float,
        volume: float,
    ) -> None:
        self.conn.execute(
            """
            INSERT OR REPLACE INTO bars(coin, tf, bar_end_ts, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (coin, tf, _to_iso(bar_end_ts), open, high, low, close, volume),
        )
        self.conn.commit()

    def insert_decision(
        self,
        run_id: str,
        decision_uid: str,
        ts: datetime | str,
        coin: str,
        stage: str,
        payload: dict[str, Any],
        trade_id: int | None = None,
        payload_version: int = 1,
    ) -> int:
        cursor = self.conn.execute(
            """
            INSERT INTO decisions(decision_uid, run_id, ts, coin, stage, trade_id, payload_json, payload_version)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (decision_uid, run_id, _to_iso(ts), coin, stage, trade_id, _json(payload), payload_version),
        )
        self.conn.commit()
        return int(cursor.lastrowid)

    def get_decision_chain(self, decision_uid: str) -> list[dict[str, Any]]:
        rows = self._rows(
            """
            SELECT * FROM decisions
            WHERE decision_uid = ?
            ORDER BY id ASC
            """,
            (decision_uid,),
        )
        for row in rows:
            row["payload"] = json.loads(row.pop("payload_json") or "{}")
        return rows

    def insert_order(
        self,
        cloid: str,
        oid: int | None,
        group_id: str | None,
        order_ref: str,
        order_json: dict[str, Any],
        decision_uid: str,
        trade_id: int | None,
        role: str,
        status: str,
        qty: float,
        filled_qty: float = 0.0,
        avg_fill_px: float | None = None,
        ts_submit: datetime | str | None = None,
        ts_last: datetime | str | None = None,
    ) -> Literal["INSERTED", "EXACT_REPLAY", "CONFLICT"]:
        """Collision-safe order insertion (TS-P1-002).

        Returns 'INSERTED', 'EXACT_REPLAY', or 'CONFLICT'.
        """
        submit_ts = _to_iso(ts_submit) or _to_iso(datetime.now(UTC))
        _last = _to_iso(ts_last) or submit_ts
        normalized = (
            cloid, oid, group_id, order_ref, _json(order_json),
            decision_uid, trade_id, role, status,
            float(qty), float(filled_qty),
            float(avg_fill_px) if avg_fill_px is not None else None,
            submit_ts, _last,
        )
        cursor = self.conn.execute(
            """
            INSERT OR IGNORE INTO orders(
              cloid, oid, group_id, order_ref, order_json, decision_uid,
              trade_id, role, status, qty, filled_qty, avg_fill_px,
              ts_submit, ts_last
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            normalized,
        )
        self.conn.commit()
        if cursor.rowcount == 1:
            return "INSERTED"

        row = self.conn.execute(
            """SELECT cloid, oid, group_id, order_ref, order_json,
                      decision_uid, trade_id, role, status, qty,
                      filled_qty, avg_fill_px, ts_submit, ts_last
               FROM orders WHERE cloid = ?""",
            (cloid,),
        ).fetchone()
        if row is None:
            return "CONFLICT"
        existing = (
            str(row["cloid"]), int(row["oid"]),
            str(row["group_id"]) if row["group_id"] is not None else None,
            str(row["order_ref"]) if row["order_ref"] is not None else None,
            str(row["order_json"]), str(row["decision_uid"]),
            int(row["trade_id"]), str(row["role"]), str(row["status"]),
            float(row["qty"]), float(row["filled_qty"]),
            float(row["avg_fill_px"]) if row["avg_fill_px"] is not None else None,
            str(row["ts_submit"]), str(row["ts_last"]),
        )
        return "EXACT_REPLAY" if existing == normalized else "CONFLICT"
    def insert_order_safe(
        self,
        cloid: str, oid: int | None, group_id: str | None,
        order_ref: str, order_json: dict[str, Any],
        decision_uid: str, trade_id: int | None, role: str,
        status: str, qty: float, filled_qty: float = 0.0,
        avg_fill_px: float | None = None,
        ts_submit: datetime | str | None = None,
        ts_last: datetime | str | None = None,
    ) -> Literal["INSERTED", "EXACT_REPLAY", "CONFLICT"]:
        """Alias for collision-safe insert_order (TS-P1-002)."""
        return self.insert_order(
            cloid=cloid, oid=oid, group_id=group_id,
            order_ref=order_ref, order_json=order_json,
            decision_uid=decision_uid, trade_id=trade_id, role=role,
            status=status, qty=qty, filled_qty=filled_qty,
            avg_fill_px=avg_fill_px, ts_submit=ts_submit, ts_last=ts_last,
        )

    def update_order_status(
        self,
        cloid: str,
        status: str,
        filled_qty: float | None = None,
        avg_fill_px: float | None = None,
        ts_last: datetime | str | None = None,
    ) -> None:
        self.conn.execute(
            """
            UPDATE orders
            SET status = ?,
                filled_qty = COALESCE(?, filled_qty),
                avg_fill_px = COALESCE(?, avg_fill_px),
                ts_last = ?
            WHERE cloid = ?
            """,
            (status, filled_qty, avg_fill_px, _to_iso(ts_last) or _to_iso(datetime.now(UTC)), cloid),
        )
        self.conn.commit()

    def insert_fill(
        self,
        fill_id: str,
        cloid: str,
        decision_uid: str,
        fill_ts: datetime | str,
        qty: float,
        px: float,
        fee: float,
        funding: float,
    ) -> Literal["INSERTED", "EXACT_DUPLICATE", "CONFLICT"]:
        """Insert an immutable fill record and classify a primary-key hit."""
        normalized = (
            fill_id,
            cloid,
            decision_uid,
            _to_iso(fill_ts),
            float(qty),
            float(px),
            float(fee),
            float(funding),
        )
        cursor = self.conn.execute(
            """
            INSERT OR IGNORE INTO fills(fill_id, cloid, decision_uid, fill_ts, qty, px, fee, funding)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            normalized,
        )
        self.conn.commit()
        if cursor.rowcount == 1:
            return "INSERTED"

        row = self.conn.execute(
            """
            SELECT fill_id, cloid, decision_uid, fill_ts, qty, px, fee, funding
            FROM fills WHERE fill_id = ?
            """,
            (fill_id,),
        ).fetchone()
        if row is None:
            return "CONFLICT"
        existing = (
            str(row["fill_id"]),
            str(row["cloid"]),
            str(row["decision_uid"]),
            str(row["fill_ts"]),
            float(row["qty"]),
            float(row["px"]),
            float(row["fee"] or 0.0),
            float(row["funding"] or 0.0),
        )
        return "EXACT_DUPLICATE" if existing == normalized else "CONFLICT"

    def create_trade(
        self,
        run_id: str,
        coin: str,
        direction: str,
        qty: float,
        entry_decision_uid: str,
        signal_ts: datetime | str,
        decision_ts: datetime | str,
        expected_px: float,
        risk_dollars: float,
        risk_pct: float,
        leverage: int,
        sl_initial: float,
        tp_initial: float | None,
        llm_directive_id: int | None,
    ) -> int:
        cursor = self.conn.execute(
            """
            INSERT INTO trades(
              run_id, coin, direction, qty, entry_decision_uid, signal_ts, decision_ts,
              expected_px, risk_dollars, risk_pct, leverage, sl_initial, tp_initial, llm_directive_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run_id,
                coin,
                direction,
                qty,
                entry_decision_uid,
                _to_iso(signal_ts),
                _to_iso(decision_ts),
                expected_px,
                risk_dollars,
                risk_pct,
                leverage,
                sl_initial,
                tp_initial,
                llm_directive_id,
            ),
        )
        self.conn.commit()
        return int(cursor.lastrowid)

    def update_trade_exit(
        self,
        trade_id: int,
        exit_px: float,
        exit_ts: datetime | str,
        exit_reason: str,
        pnl: float,
    ) -> None:
        self.conn.execute(
            """
            UPDATE trades
            SET exit_px = ?, exit_ts = ?, exit_reason = ?, pnl = ?
            WHERE trade_id = ?
            """,
            (exit_px, _to_iso(exit_ts), exit_reason, pnl, trade_id),
        )
        self.conn.commit()

    def close_trade_once_with_decision(
        self,
        trade_id: int,
        run_id: str,
        decision_uid: str,
        coin: str,
        exit_px: float,
        exit_ts: datetime | str,
        exit_reason: str,
        pnl: float,
        payload: dict[str, Any],
    ) -> bool:
        """Atomically close one open trade and append its close decision."""
        ts_iso = _to_iso(exit_ts)
        with self.conn:
            cursor = self.conn.execute(
                """
                UPDATE trades
                SET exit_px = ?, exit_ts = ?, exit_reason = ?, pnl = ?
                WHERE trade_id = ? AND exit_ts IS NULL
                """,
                (exit_px, ts_iso, exit_reason, pnl, trade_id),
            )
            if cursor.rowcount != 1:
                return False
            self.conn.execute(
                """
                INSERT INTO decisions(
                  decision_uid, run_id, ts, coin, stage, trade_id, payload_json, payload_version
                ) VALUES (?, ?, ?, ?, 'TRADE_CLOSED', ?, ?, 1)
                """,
                (decision_uid, run_id, ts_iso, coin, trade_id, _json(payload)),
            )
        return True

    def _run_environment(self, run_id: str) -> tuple[str, str]:
        row = self.conn.execute(
            "SELECT mode, network FROM runs WHERE run_id = ?", (run_id,)
        ).fetchone()
        if row is None:
            # Fail closed: risk queries must not silently fall back to an
            # unscoped view when the environment is unknown.
            raise LookupError(f"run not found for risk scoping: {run_id}")
        return str(row["mode"]), str(row["network"])

    def realized_pnl_today(self, run_id: str, now: datetime | None = None) -> float:
        """Closed-trade net PnL inside [UTC midnight, next midnight) for the
        given run's mode+network. Cross-run within that environment so a
        restart inside the trading day cannot reset the daily-loss gate, but
        other environments (e.g. dry_run replays sharing the DB file) never
        leak in."""
        mode, network = self._run_environment(run_id)
        current = now if now is not None else self._clock()
        if current.tzinfo is None:
            current = current.replace(tzinfo=UTC)
        day_start = current.astimezone(UTC).replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        row = self.conn.execute(
            """
            SELECT COALESCE(SUM(t.pnl), 0.0)
            FROM trades t JOIN runs r ON r.run_id = t.run_id
            WHERE r.mode = ? AND r.network = ?
              AND t.exit_ts IS NOT NULL AND t.pnl IS NOT NULL
              AND t.exit_ts >= ? AND t.exit_ts < ?
            """,
            (mode, network, _to_iso(day_start), _to_iso(day_end)),
        ).fetchone()
        return float(row[0]) if row and row[0] is not None else 0.0

    def consecutive_closed_losses(self, run_id: str) -> int:
        """Most-recent consecutive closed trades with negative net PnL within
        the given run's mode+network. Cross-run inside that environment so the
        streak survives restarts; not day-scoped."""
        mode, network = self._run_environment(run_id)
        rows = self.conn.execute(
            """
            SELECT t.pnl
            FROM trades t JOIN runs r ON r.run_id = t.run_id
            WHERE r.mode = ? AND r.network = ?
              AND t.exit_ts IS NOT NULL AND t.pnl IS NOT NULL
            ORDER BY t.exit_ts DESC, t.trade_id DESC
            """,
            (mode, network),
        ).fetchall()
        count = 0
        for (pnl,) in rows:
            if float(pnl) < 0:
                count += 1
            else:
                break
        return count

    def order_fill_totals(self, cloid: str) -> tuple[float, float | None]:
        """Cumulative filled quantity and VWAP for one order, derived from the
        persisted fills (fill_id is the primary key, so duplicate deliveries
        coalesce and the totals are restart-safe)."""
        row = self.conn.execute(
            "SELECT COALESCE(SUM(qty), 0.0), SUM(qty * px) FROM fills WHERE cloid = ?",
            (cloid,),
        ).fetchone()
        qty = float(row[0]) if row and row[0] is not None else 0.0
        vwap = (float(row[1]) / qty) if qty > 0 and row[1] is not None else None
        return qty, vwap

    def trade_fill_totals(self, trade_id: int) -> dict[str, Any]:
        """Cumulative entry/exit fill quantities, VWAPs and timestamps for a
        trade, joining fills to their orders' roles. Restart- and
        duplicate-safe for the same reason as order_fill_totals."""
        rows = self.conn.execute(
            """
            SELECT CASE WHEN o.role = 'ENTRY' THEN 'ENTRY' ELSE 'EXIT' END AS side,
                   COALESCE(SUM(f.qty), 0.0) AS qty,
                   SUM(f.qty * f.px) AS notional,
                   MIN(f.fill_ts) AS first_ts,
                   MAX(f.fill_ts) AS last_ts
            FROM fills f JOIN orders o ON o.cloid = f.cloid
            WHERE o.trade_id = ?
            GROUP BY side
            """,
            (trade_id,),
        ).fetchall()
        totals: dict[str, Any] = {
            "entry_qty": 0.0, "entry_vwap": None, "entry_first_ts": None,
            "exit_qty": 0.0, "exit_vwap": None, "exit_last_ts": None,
        }
        for row in rows:
            qty = float(row["qty"])
            vwap = (float(row["notional"]) / qty) if qty > 0 and row["notional"] is not None else None
            if row["side"] == "ENTRY":
                totals["entry_qty"] = qty
                totals["entry_vwap"] = vwap
                totals["entry_first_ts"] = row["first_ts"]
            else:
                totals["exit_qty"] = qty
                totals["exit_vwap"] = vwap
                totals["exit_last_ts"] = row["last_ts"]
        return totals

    def has_live_entry_remainder(self, trade_id: int) -> bool:
        """Whether an owned ENTRY order can still fill more quantity."""
        for order in self.get_orders_for_trade(trade_id):
            if order["role"] != "ENTRY" or order["status"] not in {"OPEN", "SUBMITTED", "PENDING"}:
                continue
            filled_qty, _ = self.order_fill_totals(str(order["cloid"]))
            if filled_qty < float(order["qty"]) - 1e-9:
                return True
        return False

    def trade_costs(self, decision_uid: str) -> float:
        """Total captured fill costs for one trade (entry + exit + funding).
        Positive values are debits per the Hyperliquid fee convention; rebates
        arrive negative and reduce the cost."""
        row = self.conn.execute(
            """
            SELECT COALESCE(SUM(fee), 0.0) + COALESCE(SUM(funding), 0.0)
            FROM fills WHERE decision_uid = ?
            """,
            (decision_uid,),
        ).fetchone()
        return float(row[0]) if row and row[0] is not None else 0.0

    def insert_equity(
        self,
        run_id: str,
        ts: datetime | str,
        equity: float,
        cash: float,
        unrealized: float,
        realized_today: float,
    ) -> None:
        self.conn.execute(
            """
            INSERT OR REPLACE INTO equity(run_id, ts, equity, cash, unrealized, realized_today)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (run_id, _to_iso(ts), equity, cash, unrealized, realized_today),
        )
        self.conn.commit()

    def upsert_risk_day(
        self,
        trading_date: str,
        day_start_equity: float,
        realized_pnl_engine: float,
        realized_pnl_broker: float,
        max_intraday_dd: float,
        consecutive_losses_end: int,
        auto_rearms_used: int,
    ) -> None:
        self.conn.execute(
            """
            INSERT OR REPLACE INTO risk_days(
              trading_date, day_start_equity, realized_pnl_engine, realized_pnl_broker,
              max_intraday_dd, consecutive_losses_end, auto_rearms_used
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                trading_date,
                day_start_equity,
                realized_pnl_engine,
                realized_pnl_broker,
                max_intraday_dd,
                consecutive_losses_end,
                auto_rearms_used,
            ),
        )
        self.conn.commit()

    def insert_event(
        self,
        run_id: str,
        ts: datetime | str,
        severity: str,
        code: str,
        detail: str,
    ) -> int:
        cursor = self.conn.execute(
            """
            INSERT INTO events(run_id, ts, severity, code, detail)
            VALUES (?, ?, ?, ?, ?)
            """,
            (run_id, _to_iso(ts), severity, code, detail),
        )
        self.conn.commit()
        return int(cursor.lastrowid)

    def claim_signal_fingerprint(self, run_id: str, fingerprint: str, decision_uid: str, ts: datetime | str) -> bool:
        try:
            self.conn.execute(
                """
                INSERT INTO signal_fingerprints(run_id, fingerprint, decision_uid, ts)
                VALUES (?, ?, ?, ?)
                """,
                (run_id, fingerprint, decision_uid, _to_iso(ts)),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_order(self, cloid: str) -> dict[str, Any] | None:
        row = self.conn.execute("SELECT * FROM orders WHERE cloid = ?", (cloid,)).fetchone()
        return None if row is None else dict(row)

    def get_order_by_ref(self, order_ref: str) -> dict[str, Any] | None:
        """B2 fallback 2: durable identity via our order_ref tag."""
        row = self.conn.execute("SELECT * FROM orders WHERE order_ref = ?", (order_ref,)).fetchone()
        return None if row is None else dict(row)

    def find_live_orders_by_attributes(
        self,
        symbol: str,
        role: str,
        qty: float,
        trigger_px: float | None,
    ) -> list[dict[str, Any]]:
        """B2 fallback 3: conservative attribute match (spec §6.5).

        Matches only orders still in a live status; symbol and trigger price
        come from the persisted order_json. Caller treats >1 result as
        AMBIGUOUS and must not act on it.
        """
        rows = self._rows(
            """
            SELECT * FROM orders
            WHERE role = ? AND qty = ?
              AND status IN ('OPEN', 'SUBMITTED', 'PENDING')
              AND json_extract(order_json, '$.symbol') = ?
            """,
            (role, qty, symbol),
        )
        if trigger_px is None:
            return rows
        matched: list[dict[str, Any]] = []
        for row in rows:
            try:
                stored_trigger = json.loads(row["order_json"]).get("trigger_px")
            except (TypeError, ValueError):
                stored_trigger = None
            if stored_trigger is not None and abs(float(stored_trigger) - trigger_px) < 1e-9:
                matched.append(row)
        return matched

    def get_trade(self, trade_id: int) -> dict[str, Any] | None:
        row = self.conn.execute("SELECT * FROM trades WHERE trade_id = ?", (trade_id,)).fetchone()
        return None if row is None else dict(row)

    def get_open_trade_for_coin(self, run_id: str, coin: str) -> dict[str, Any] | None:
        row = self.conn.execute(
            """
            SELECT * FROM trades
            WHERE run_id = ? AND coin = ? AND exit_ts IS NULL
            ORDER BY trade_id DESC LIMIT 1
            """,
            (run_id, coin),
        ).fetchone()
        return None if row is None else dict(row)

    def get_orders_for_trade(self, trade_id: int) -> list[dict[str, Any]]:
        return self._rows(
            "SELECT * FROM orders WHERE trade_id = ? ORDER BY ts_submit",
            (trade_id,),
        )

    def update_trade_entry(self, trade_id: int, entry_px: float, entry_ts: datetime | str) -> None:
        self.conn.execute(
            """
            UPDATE trades
            SET entry_px = ?, entry_ts = ?, first_fill_ts = COALESCE(first_fill_ts, ?), last_fill_ts = ?
            WHERE trade_id = ?
            """,
            (entry_px, _to_iso(entry_ts), _to_iso(entry_ts), _to_iso(entry_ts), trade_id),
        )
        self.conn.commit()

    def get_snapshot(self) -> dict[str, list[dict[str, Any]]]:
        return {
            "runs": self._rows("SELECT * FROM runs ORDER BY started_ts"),
            "trades": self._rows("SELECT * FROM trades ORDER BY trade_id"),
            "orders": self._rows("SELECT * FROM orders ORDER BY ts_submit"),
            "fills": self._rows("SELECT * FROM fills ORDER BY fill_ts"),
            "events": self._rows("SELECT * FROM events ORDER BY id"),
            "bars": self._rows("SELECT * FROM bars ORDER BY bar_end_ts"),
            "decisions": self._rows("SELECT * FROM decisions ORDER BY id"),
            "equity": self._rows("SELECT * FROM equity ORDER BY ts"),
            "identities": self._rows(
                "SELECT * FROM order_identities ORDER BY reserved_ts"),
        }


    def get_trades(self, limit: int = 50) -> list[dict[str, Any]]:
        return self._rows("SELECT * FROM trades ORDER BY trade_id DESC LIMIT ?", (limit,))

    def get_decisions(self, trade_id: int | None = None, limit: int = 200) -> list[dict[str, Any]]:
        if trade_id is None:
            rows = self._rows("SELECT * FROM decisions ORDER BY id DESC LIMIT ?", (limit,))
        else:
            rows = self._rows(
                "SELECT * FROM decisions WHERE trade_id = ? ORDER BY id",
                (trade_id,),
            )
        for row in rows:
            row["payload"] = json.loads(row.pop("payload_json") or "{}")
        return rows

    def get_equity(self, limit: int = 1000) -> list[dict[str, Any]]:
        return self._rows("SELECT * FROM equity ORDER BY ts DESC LIMIT ?", (limit,))

    def get_events(self, severity: str | None = None, limit: int = 500) -> list[dict[str, Any]]:
        if severity is None:
            return self._rows("SELECT * FROM events ORDER BY id DESC LIMIT ?", (limit,))
        return self._rows(
            "SELECT * FROM events WHERE severity = ? ORDER BY id DESC LIMIT ?",
            (severity, limit),
        )

    def get_bars(self, limit: int = 300) -> list[dict[str, Any]]:
        return self._rows("SELECT * FROM bars ORDER BY bar_end_ts DESC LIMIT ?", (limit,))[::-1]

    def get_run(self, run_id: str) -> dict[str, Any] | None:
        row = self.conn.execute("SELECT * FROM runs WHERE run_id = ?", (run_id,)).fetchone()
        return None if row is None else dict(row)

    def get_latest_gates(self) -> dict[str, Any]:
        row = self.conn.execute(
            """
            SELECT payload_json FROM decisions
            WHERE stage IN ('RISK_PASS', 'RISK_REJECT')
            ORDER BY id DESC LIMIT 1
            """
        ).fetchone()
        if row is None:
            return {"gate_results": []}
        payload = json.loads(row["payload_json"] or "{}")
        return {"gate_results": payload.get("gates", [])}

    def _rows(self, sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
        return [dict(row) for row in self.conn.execute(sql, params).fetchall()]
