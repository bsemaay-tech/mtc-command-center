#!/usr/bin/env python3
"""Transform bridge/store/db.py from v2 to v3 using str.replace() anchoring.

TSP-1-002: Adds durable identity table (order_identities), schema version
management, v2->v3 migration, collision-safe order insertion, and identity-
store methods.
"""

from __future__ import annotations



# ---------------------------------------------------------------------------
# Multi-line string constants used during replacement
# ---------------------------------------------------------------------------

_V3_DDL_STRING = '''_V3_DDL = """
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

'''
import sys
from pathlib import Path


_NEW_INITIALIZE = '''    def initialize(self) -> None:
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
            )'''


_HELPER_METHODS_PART1 = '''
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
            self._write_schema_version(3)'''


_HELPER_METHODS_PART2 = '''
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
            )'''


_HELPER_METHODS_PART3 = '''
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
        return str(row["intent_preimage"]) == intent_preimage'''


_NEW_INSERT_ORDER = '''    def insert_order(
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
        return "EXACT_REPLAY" if existing == normalized else "CONFLICT"'''


_INSERT_ORDER_SAFE = '''
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
        )'''


_NEW_GET_SNAPSHOT_RETURN = '''    def get_snapshot(self) -> dict[str, list[dict[str, Any]]]:
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
        }'''


# ---------------------------------------------------------------------------
# Anchor strings (exact substrings present in the CURRENT v2 db.py)
# ---------------------------------------------------------------------------

ANCHOR_CLASS_STORE = (
    '\n\nclass Store:\n'
    '    """Small SQLite access layer for the bridge runtime database."""'
)

ANCHOR_INIT_AFTER_DOCSTRING = (
    '"""Small SQLite access layer for the bridge runtime database."""\n'
    '\n    def __init__('
)


ANCHOR_INITIALIZE_START = (
    '    def initialize(self) -> None:\n'
    '        self.conn.executescript('
)
ANCHOR_INITIALIZE_END = (
    '        self.conn.commit()\n'
    '\n    def get_meta(self, key: str)'
)

ANCHOR_INSERT_ORDER_START = (
    '    def insert_order(\n'
    '        self,\n'
    '        cloid: str,\n'
    '        oid: int | None,\n'
    '        group_id: str | None,\n'
    '        order_ref: str,\n'
    '        order_json: dict[str, Any],\n'
    '        decision_uid: str,\n'
    '        trade_id: int | None,\n'
    '        role: str,\n'
    '        status: str,\n'
    '        qty: float,\n'
    '        filled_qty: float = 0.0,\n'
    '        avg_fill_px: float | None = None,\n'
    '        ts_submit: datetime | str | None = None,\n'
    '        ts_last: datetime | str | None = None,\n'
    '    ) -> None:'
)
ANCHOR_INSERT_ORDER_END = '\n\n    def update_order_status('

ANCHOR_GET_SNAPSHOT_START = (
    '    def get_snapshot(self) -> dict[str, list[dict[str, Any]]]:\n'
    '        return {'
)
ANCHOR_GET_SNAPSHOT_END = '\n\n    def get_trades(self, limit: int'


# Combine helper parts into the single string used by the replacement
_HELPER_METHODS = _HELPER_METHODS_PART1 + _HELPER_METHODS_PART2 + _HELPER_METHODS_PART3


# ---------------------------------------------------------------------------
# Transformation logic
# ---------------------------------------------------------------------------

def transform(text: str) -> str:
    """Apply all v2->v3 transformations using str.replace() anchoring."""

    # --- 1. Insert _V3_DDL, exception classes, then "class Store:" ---------
    old = ANCHOR_CLASS_STORE
    new = (
        "\n" + _V3_DDL_STRING + "\n\n"
        "# -------------------------------------------------------------------\n"
        "# Exception classes\n"
        "# -------------------------------------------------------------------\n"
        "\n"
        "\n"
        "class IdentityCollisionError(Exception):\n"
        '    """Durable identity collision: same digest, different preimage."""\n'
        "\n"
        "\n"
        "class IdentityMismatchError(Exception):\n"
        '    """Same intent maps to a different request - material change."""\n'
        "\n"
        "\n"
        "class ReservationBlockedError(Exception):\n"
        '    """Reservation blocked: intent already exists in any state."""\n'
        "\n"
        "\n"
        "class SchemaVersionError(Exception):\n"
        '    """Unsupported or corrupt schema version."""\n'
        "\n"
        "\n"
        "class V2MigrationError(Exception):\n"
        '    """v2 -> v3 migration failed; rollback completed."""\n'
        "\n"
        "\nclass Store:\n"
        '    """Small SQLite access layer for the bridge runtime database."""'
    )
    if text.count(old) != 1:
        raise RuntimeError(
            f"Anchor for _V3_DDL count={text.count(old)}, expected 1"
        )
    text = text.replace(old, new, 1)

    # --- 2. Add _SCHEMA_VERSION class variable ---------------------------
    old = ANCHOR_INIT_AFTER_DOCSTRING
    new = (
        '"""Small SQLite access layer for the bridge runtime database."""\n'
        '\n    _SCHEMA_VERSION = 3\n\n    def __init__('
    )
    if text.count(old) != 1:
        raise RuntimeError(
            f"Anchor for _SCHEMA_VERSION count={text.count(old)}, expected 1"
        )
    text = text.replace(old, new, 1)

    # --- 3. Replace initialize() with version-checked + helpers ----------
    s_idx = text.index(ANCHOR_INITIALIZE_START)
    e_idx = text.index(ANCHOR_INITIALIZE_END, s_idx + len(ANCHOR_INITIALIZE_START))
    replacement = _NEW_INITIALIZE + _HELPER_METHODS
    tail_start = e_idx + len("        self.conn.commit()")
    text = text[:s_idx] + replacement + text[tail_start:]

    # --- 4. Replace insert_order with collision-safe version --------------
    s_idx = text.index(ANCHOR_INSERT_ORDER_START)
    e_idx = text.index(ANCHOR_INSERT_ORDER_END, s_idx + len(ANCHOR_INSERT_ORDER_START))
    replacement = _NEW_INSERT_ORDER + _INSERT_ORDER_SAFE
    tail_start = e_idx
    text = text[:s_idx] + replacement + text[tail_start:]

    # --- 5. Update get_snapshot return dict --------------------------------
    s_idx = text.index(ANCHOR_GET_SNAPSHOT_START)
    e_idx = text.index(ANCHOR_GET_SNAPSHOT_END, s_idx + len(ANCHOR_GET_SNAPSHOT_START))
    text = text[:s_idx] + _NEW_GET_SNAPSHOT_RETURN + "\n" + text[e_idx:]

    return text


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    db_path = repo_root / "bridge" / "store" / "db.py"

    if not db_path.exists():
        print(f"ERROR: {db_path} not found", file=sys.stderr)
        sys.exit(1)

    original = db_path.read_text(encoding="utf-8")

    # ── idempotency: skip if already v3 ───────────────────────────
    v3_markers = [
        "_SCHEMA_VERSION = 3",
        "order_identities",
        "def reserve_identity(",
        "def finalize_identity(",
        'Literal["INSERTED", "EXACT_REPLAY", "CONFLICT"]',
        '"identities"',  # in get_snapshot
    ]
    missing = [m for m in v3_markers if m not in original]
    if not missing:
        print("db.py is already schema v3 — nothing to transform.")
        return

    print(f"Detected v2 (missing markers: {missing}). Applying v3 transform...")

    try:
        transformed = transform(original)
    except (ValueError, RuntimeError) as exc:
        print(f"ERROR: transformation failed: {exc}", file=sys.stderr)
        print(
            "The file may have unexpected content.",
            file=sys.stderr,
        )
        sys.exit(1)

    if len(transformed) < len(original):
        print(
            "WARNING: transformed file is smaller than original - "
            "possible data loss; aborting.",
            file=sys.stderr,
        )
        sys.exit(1)

    db_path.write_text(transformed, encoding="utf-8")
    print(
        f"OK - wrote {db_path} "
        f"({len(original)} -> {len(transformed)} chars)"
    )


if __name__ == "__main__":
    main()