"""SQLite Store with schema v3 (TS-P1-002 durable identity)."""

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
# TS-P1-002 identity helpers (module-level so orders.py can reuse them)
# ---------------------------------------------------------------------------

_IDENTITY_INTENT_VERSION = "ts-p1-002-intent-v1"
_IDENTITY_REQUEST_VERSION = "ts-p1-002-request-v1"


def _float_hex(value: float) -> str:
    """Deterministic IEEE-754 hex representation; rejects NaN/Inf, normalizes -0 → +0."""
    import math
    if math.isnan(value) or math.isinf(value):
        raise ValueError(f"float value must be finite: {value!r}")
    if value == 0.0:
        value = 0.0  # normalizes -0.0 → 0.0
    return value.hex()


def _canonical_json(obj: Any) -> str:
    """Deterministic JSON: sorted keys, compact, UTF-8, no NaN."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False)


def _finite_float(value: float) -> float:
    """Reject NaN/Inf; normalizes -0 → +0."""
    import math
    if math.isnan(value) or math.isinf(value):
        raise ValueError(f"float value must be finite: {value!r}")
    if value == 0.0:
        return 0.0
    return value


def compute_intent_identity(
    strategy_id: str,
    symbol: str,
    direction: str,
    signal_ts: datetime,
) -> tuple[str, str, str]:
    """Return (intent_id, intent_preimage, intent_version).

    intent_id = "intent-v1:<sha256-hex>"

    Requires timezone-aware signal_ts with a concrete UTC offset;
    rejects naive datetimes and tzinfo objects whose utcoffset() returns None.
    """
    if signal_ts.tzinfo is None:
        raise ValueError("signal_ts must be timezone-aware")
    if signal_ts.utcoffset() is None:
        raise ValueError("signal_ts must have a concrete UTC offset")
    ts_str = signal_ts.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    obj = {
        "version": _IDENTITY_INTENT_VERSION,
        "strategy_id": strategy_id,
        "symbol": symbol.upper(),
        "direction": direction.upper(),
        "signal_ts": ts_str,
    }
    preimage = _canonical_json(obj)
    digest = hashlib.sha256(preimage.encode("utf-8")).hexdigest()
    intent_id = f"intent-v1:{digest}"
    return intent_id, preimage, _IDENTITY_INTENT_VERSION


def compute_request_identity(
    intent_id: str,
    symbol: str,
    direction: str,
    ref_price: float,
    qty: float,
    entry_type: str,
    limit_price: float | None,
    stop_loss: float,
    take_profit: float | None,
    leverage: int,
) -> tuple[str, str, str]:
    """Return (request_id, request_preimage, request_version).

    request_id = "request-v1:<sha256-hex>"

    All float params must be finite.  Non-integral leverage raises ValueError.
    """
    import math

    # Validate leverage is a true integer (not bool, not float)
    if not isinstance(leverage, int) or isinstance(leverage, bool):
        raise ValueError(f"leverage must be a true int, got {type(leverage).__name__}: {leverage!r}")
    if leverage <= 0:
        raise ValueError(f"leverage must be positive: {leverage!r}")

    # Validate all floats are finite
    for name, val in [("ref_price", ref_price), ("qty", qty), ("stop_loss", stop_loss)]:
        if math.isnan(val) or math.isinf(val):
            raise ValueError(f"{name} must be finite: {val!r}")
    if limit_price is not None:
        if math.isnan(limit_price) or math.isinf(limit_price):
            raise ValueError(f"limit_price must be finite: {limit_price!r}")
    if take_profit is not None:
        if math.isnan(take_profit) or math.isinf(take_profit):
            raise ValueError(f"take_profit must be finite: {take_profit!r}")

    obj: dict[str, Any] = {
        "version": _IDENTITY_REQUEST_VERSION,
        "intent_id": intent_id,
        "symbol": symbol.upper(),
        "direction": direction.upper(),
        "ref_price": _float_hex(ref_price),
        "qty": _float_hex(qty),
        "entry_type": entry_type,
        "limit_price": _float_hex(limit_price) if limit_price is not None else None,
        "stop_loss": _float_hex(stop_loss),
        "take_profit": _float_hex(take_profit) if take_profit is not None else None,
        "leverage": leverage,
    }
    preimage = _canonical_json(obj)
    digest = hashlib.sha256(preimage.encode("utf-8")).hexdigest()
    request_id = f"request-v1:{digest}"
    return request_id, preimage, _IDENTITY_REQUEST_VERSION


# ---------------------------------------------------------------------------
# Custom exceptions
# ---------------------------------------------------------------------------

class IdentityCollisionError(Exception):
    """Raised when identity reservation detects a collision."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


class OrderCollisionError(Exception):
    """Raised when order insertion detects a cloid collision with different identity."""

    def __init__(self, cloid: str, existing_decision_uid: str, new_decision_uid: str) -> None:
        self.cloid = cloid
        self.existing_decision_uid = existing_decision_uid
        self.new_decision_uid = new_decision_uid
        super().__init__(
            f"IDENTITY_ORDER_COLLISION: cloid={cloid} "
            f"existing_decision={existing_decision_uid} "
            f"new_decision={new_decision_uid}"
        )


class MigrationError(Exception):
    """Raised when v2→v3 migration cannot complete safely."""

    def __init__(self, message: str) -> None:
        super().__init__(f"MIGRATION_V2_FAILED: {message}")


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------

class Store:
    """Small SQLite access layer for the bridge runtime database."""

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

    # ------------------------------------------------------------------
    # Schema initialization with version-aware migration
    # ------------------------------------------------------------------

    def initialize(self) -> None:
        # Ensure meta table exists before querying it
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT)"
        )
        existing = self.get_meta("schema_version")
        if existing is None:
            self._initialize_v3_fresh()
            self._migrate_v3_to_v4()
            return
        if existing == "4":
            self._initialize_v4_idempotent()
            return
        if existing == "3":
            self._migrate_v3_to_v4()
            return
        if existing == "2":
            self._migrate_v2_to_v3()
            self._migrate_v3_to_v4()
            return
        # Unsupported or corrupt version → fail closed
        raise RuntimeError(
            f"Unsupported schema_version={existing!r}; cannot initialize safely"
        )

    def _initialize_v3_fresh(self) -> None:
        self._create_tables_v3()
        self.conn.execute(
            "INSERT OR REPLACE INTO meta(key, value) VALUES (?, ?)",
            ("schema_version", "3"),
        )
        self.conn.commit()

    def _initialize_v3_idempotent(self) -> None:
        """Re-open an existing v3 database — ensure tables exist (idempotent)."""
        self._create_tables_v3()

    def _initialize_v4_idempotent(self) -> None:
        """Re-open an existing v4 database — ensure tables exist (idempotent)."""
        self._create_tables_v3()
        self._create_tables_v4()

    def _create_tables_v3(self) -> None:
        """Create all v3 tables and indexes (idempotent via IF NOT EXISTS).

        Does NOT use executescript so it can be called inside a transaction.
        Each statement is executed individually.
        """
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS meta (
              key TEXT PRIMARY KEY,
              value TEXT
            )""")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS runs (
              run_id TEXT PRIMARY KEY,
              started_ts TEXT,
              ended_ts TEXT,
              mode TEXT CHECK(mode IN ('paper','dry_run','live')),
              network TEXT,
              config_json TEXT
            )""")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS bars (
              coin TEXT,
              tf TEXT,
              bar_end_ts TEXT,
              open REAL,
              high REAL,
              low REAL,
              close REAL,
              volume REAL,
              PRIMARY KEY(coin, tf, bar_end_ts)
            )""")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS decisions (
              id INTEGER PRIMARY KEY,
              decision_uid TEXT NOT NULL,
              run_id TEXT,
              ts TEXT,
              coin TEXT,
              stage TEXT,
              trade_id INTEGER,
              payload_json TEXT,
              payload_version INTEGER DEFAULT 1
            )""")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
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
            )""")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS fills (
              fill_id TEXT PRIMARY KEY,
              cloid TEXT,
              decision_uid TEXT,
              fill_ts TEXT,
              qty REAL,
              px REAL,
              fee REAL,
              funding REAL
            )""")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS trades (
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
            )""")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS equity (
              run_id TEXT,
              ts TEXT,
              equity REAL,
              cash REAL,
              unrealized REAL,
              realized_today REAL,
              PRIMARY KEY(run_id, ts)
            )""")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS risk_days (
              trading_date TEXT PRIMARY KEY,
              day_start_equity REAL,
              realized_pnl_engine REAL,
              realized_pnl_broker REAL,
              max_intraday_dd REAL,
              consecutive_losses_end INTEGER,
              auto_rearms_used INTEGER
            )""")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS directives (
              id INTEGER PRIMARY KEY,
              ts TEXT,
              regime TEXT,
              confidence REAL,
              ttl_minutes INTEGER,
              rationale TEXT,
              sources_hash TEXT,
              raw_response TEXT,
              valid INTEGER
            )""")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS llm_calls (
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
            )""")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS events (
              id INTEGER PRIMARY KEY,
              run_id TEXT,
              ts TEXT,
              severity TEXT,
              code TEXT,
              detail TEXT
            )""")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS signal_fingerprints (
              run_id TEXT,
              fingerprint TEXT,
              decision_uid TEXT,
              ts TEXT,
              PRIMARY KEY(run_id, fingerprint)
            )""")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS order_identity (
              intent_id TEXT PRIMARY KEY
                CHECK(length(intent_id) = 74 AND substr(intent_id, 1, 10) = 'intent-v1:' AND NOT substr(intent_id, 11) GLOB '*[^0-9a-f]*'),
              intent_preimage TEXT NOT NULL CHECK(intent_preimage != ''),
              intent_version TEXT NOT NULL DEFAULT 'ts-p1-002-intent-v1'
                CHECK(intent_version = 'ts-p1-002-intent-v1'),
              request_id TEXT UNIQUE NOT NULL
                CHECK(length(request_id) = 75 AND substr(request_id, 1, 11) = 'request-v1:' AND NOT substr(request_id, 12) GLOB '*[^0-9a-f]*'),
              request_preimage TEXT NOT NULL CHECK(request_preimage != ''),
              request_version TEXT NOT NULL DEFAULT 'ts-p1-002-request-v1'
                CHECK(request_version = 'ts-p1-002-request-v1'),
              cloid_seed TEXT NOT NULL CHECK(cloid_seed != ''),
              origin_run_id TEXT NOT NULL CHECK(origin_run_id != ''),
              origin_decision_uid TEXT NOT NULL CHECK(origin_decision_uid != ''),
              state TEXT NOT NULL CHECK(state IN (
                'RESERVED','SUBMITTED','LEGACY_RESERVED','LEGACY_SUBMITTED'
              )),
              reserved_ts TEXT NOT NULL CHECK(reserved_ts != ''),
              submitted_ts TEXT,
              CHECK(
                (state IN ('RESERVED','LEGACY_RESERVED') AND submitted_ts IS NULL)
                OR (state IN ('SUBMITTED','LEGACY_SUBMITTED') AND submitted_ts IS NOT NULL)
              )
            )""")
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_decisions_uid ON decisions(decision_uid)")
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_decisions_run ON decisions(run_id, ts)")
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_orders_oid ON orders(oid)")
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_orders_trade ON orders(trade_id)")
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_fills_cloid ON fills(cloid)")
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_trades_run ON trades(run_id)")
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_events_run_sev ON events(run_id, severity, ts)")
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_identity_request ON order_identity(request_id)")
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_identity_state ON order_identity(state)")

    # ------------------------------------------------------------------
    # v2 → v3 migration with realistic backfill
    # ------------------------------------------------------------------

    def _migrate_v2_to_v3(self) -> None:
        """Transactional backfill of v2 signal_fingerprints into order_identity.

        The entire migration — DDL creation, backfill, and version bump — runs
        inside a single BEGIN IMMEDIATE transaction. The wrapper owns the commit.
        On any error the rollback leaves schema_version=2, all legacy data unchanged,
        and no order_identity table/index residue.
        """
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            self._migrate_v2_to_v3_in_tx()
        except Exception:
            self.conn.rollback()
            raise
        self.conn.commit()

    def _migrate_v2_to_v3_in_tx(self) -> None:
        """All migration work inside the already-open transaction.

        This helper NEVER commits. The wrapper owns the single commit.
        """
        # 1. Create v3 DDL (idempotent, inside the transaction)
        self._create_tables_v3()

        # 2. Read all signal_fingerprints
        fp_rows = self.conn.execute(
            "SELECT run_id, fingerprint, decision_uid, ts FROM signal_fingerprints ORDER BY ts"
        ).fetchall()

        if not fp_rows:
            # TS-P1-002 repair-round-4: zero fingerprints may upgrade ONLY
            # when both legacy orders and legacy trades are empty. Any
            # pre-existing evidence without a reconstructable fingerprint
            # origin is ambiguous and must fail closed.
            trade_count_row = self.conn.execute(
                "SELECT COUNT(*) FROM trades"
            ).fetchone()
            order_count_row = self.conn.execute(
                "SELECT COUNT(*) FROM orders"
            ).fetchone()
            trade_count = int(trade_count_row[0]) if trade_count_row else 0
            order_count = int(order_count_row[0]) if order_count_row else 0
            if trade_count > 0 or order_count > 0:
                raise MigrationError(
                    f"Zero signal_fingerprints but legacy evidence exists: "
                    f"trades={trade_count} orders={order_count}; "
                    f"cannot reconstruct identity origins"
                )
            # Truly empty v2 database with zero legacy evidence — safe to upgrade
            self.conn.execute(
                "INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '3')"
            )
            return

        strategy_id = "keltner_trail_ema8"

        for fp_row in fp_rows:
            run_id = str(fp_row["run_id"])
            decision_uid = str(fp_row["decision_uid"])
            fp_ts = str(fp_row["ts"]) if fp_row["ts"] else None

            # --- 1. Find exactly one SIGNAL for this run_id + decision_uid ---
            sig_rows = self.conn.execute(
                """SELECT payload_json FROM decisions
                   WHERE run_id = ? AND decision_uid = ? AND stage = 'SIGNAL'
                   ORDER BY id ASC""",
                (run_id, decision_uid),
            ).fetchall()
            if len(sig_rows) == 0:
                raise MigrationError(
                    f"No SIGNAL decision found for run_id={run_id} "
                    f"decision_uid={decision_uid}; cannot backfill identity"
                )
            if len(sig_rows) > 1:
                raise MigrationError(
                    f"Multiple SIGNAL decisions for run_id={run_id} "
                    f"decision_uid={decision_uid}; ambiguous backfill"
                )
            sig_row = sig_rows[0]
            try:
                sig_payload = json.loads(sig_row["payload_json"] or "{}")
            except (TypeError, ValueError) as exc:
                raise MigrationError(
                    f"Malformed SIGNAL payload for decision_uid={decision_uid}: {exc}"
                ) from exc

            # Extract required fields
            symbol = sig_payload.get("symbol")
            direction = sig_payload.get("direction")
            signal_ts_str = sig_payload.get("ts")
            ref_price = sig_payload.get("ref_price")
            if not symbol or not direction or signal_ts_str is None or ref_price is None:
                raise MigrationError(
                    f"Incomplete SIGNAL payload for decision_uid={decision_uid}: "
                    f"symbol={symbol!r} direction={direction!r} ts={signal_ts_str!r} ref_price={ref_price!r}"
                )
            try:
                signal_ts = datetime.fromisoformat(str(signal_ts_str))
            except (ValueError, TypeError) as exc:
                raise MigrationError(
                    f"Unparseable signal_ts in SIGNAL for {decision_uid}: {exc}"
                ) from exc

            # Compute intent identity
            intent_id, intent_preimage, intent_version = compute_intent_identity(
                strategy_id=strategy_id,
                symbol=str(symbol),
                direction=str(direction),
                signal_ts=signal_ts,
            )

            # --- 2. Find exactly one RISK_PASS for this run_id + decision_uid ---
            risk_rows = self.conn.execute(
                """SELECT payload_json FROM decisions
                   WHERE run_id = ? AND decision_uid = ? AND stage = 'RISK_PASS'
                   ORDER BY id ASC""",
                (run_id, decision_uid),
            ).fetchall()
            if len(risk_rows) == 0:
                raise MigrationError(
                    f"No RISK_PASS decision found for run_id={run_id} "
                    f"decision_uid={decision_uid}; cannot reconstruct request identity"
                )
            if len(risk_rows) > 1:
                raise MigrationError(
                    f"Multiple RISK_PASS decisions for run_id={run_id} "
                    f"decision_uid={decision_uid}; ambiguous backfill"
                )
            risk_row = risk_rows[0]
            try:
                risk_payload = json.loads(risk_row["payload_json"] or "{}")
            except (TypeError, ValueError) as exc:
                raise MigrationError(
                    f"Malformed RISK_PASS payload for {decision_uid}: {exc}"
                ) from exc

            order_plan = risk_payload.get("order_plan")
            if not isinstance(order_plan, dict):
                raise MigrationError(
                    f"Missing or invalid order_plan in RISK_PASS for {decision_uid}"
                )

            plan_signal = order_plan.get("signal")
            if not isinstance(plan_signal, dict):
                raise MigrationError(
                    f"Missing signal in order_plan for {decision_uid}"
                )

            # Validate SIGNAL and order_plan semantics agree (Repair 2-7 + Repair 3:
            # symbol, direction, timestamp, reference price, stop loss,
            # take profit — all with canonical comparisons)
            plan_symbol = plan_signal.get("symbol", symbol)
            plan_direction = plan_signal.get("direction", direction)
            if str(plan_symbol).upper() != str(symbol).upper():
                raise MigrationError(
                    f"SIGNAL/order_plan symbol mismatch for {decision_uid}: "
                    f"SIGNAL={symbol!r} order_plan={plan_symbol!r}"
                )
            if str(plan_direction).upper() != str(direction).upper():
                raise MigrationError(
                    f"SIGNAL/order_plan direction mismatch for {decision_uid}: "
                    f"SIGNAL={direction!r} order_plan={plan_direction!r}"
                )

            # Validate timestamp agreement — parse both as timezone-aware
            # datetimes and compare fixed-microsecond UTC canonical representations
            plan_ts_str = plan_signal.get("ts")
            if plan_ts_str is None:
                raise MigrationError(
                    f"Missing ts in order_plan.signal for {decision_uid}"
                )
            try:
                plan_signal_ts = datetime.fromisoformat(str(plan_ts_str))
            except (ValueError, TypeError) as exc:
                raise MigrationError(
                    f"Unparseable ts in order_plan.signal for {decision_uid}: {exc}"
                ) from exc
            if plan_signal_ts.tzinfo is None or plan_signal_ts.utcoffset() is None:
                raise MigrationError(
                    f"order_plan.signal ts must be timezone-aware for {decision_uid}"
                )
            # Compare canonical UTC representations (equivalent Z/+00:00 spellings accepted)
            _signal_ts_utc = signal_ts.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            _plan_ts_utc = plan_signal_ts.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            if _signal_ts_utc != _plan_ts_utc:
                raise MigrationError(
                    f"SIGNAL/order_plan timestamp mismatch for {decision_uid}: "
                    f"SIGNAL={_signal_ts_utc!r} order_plan={_plan_ts_utc!r}"
                )

            plan_ref_price = plan_signal.get("ref_price", ref_price)
            plan_qty = order_plan.get("qty")
            plan_entry_type = order_plan.get("entry_type", "MKT")
            plan_limit_price = order_plan.get("limit_price")
            plan_stop_loss = order_plan.get("stop_loss")
            plan_take_profit = order_plan.get("take_profit")
            plan_leverage = order_plan.get("leverage", 1)

            if plan_qty is None or plan_stop_loss is None:
                raise MigrationError(
                    f"Incomplete order_plan for {decision_uid}: "
                    f"qty={plan_qty!r} stop_loss={plan_stop_loss!r}"
                )

            # Validate reference price with exact deterministic finite float encoding
            try:
                _ref_price_float = _finite_float(float(ref_price))
                _plan_ref_price_float = _finite_float(float(plan_ref_price))
            except (ValueError, TypeError) as exc:
                raise MigrationError(
                    f"Non-finite ref_price for {decision_uid}: {exc}"
                ) from exc
            if _float_hex(_ref_price_float) != _float_hex(_plan_ref_price_float):
                raise MigrationError(
                    f"SIGNAL/order_plan ref_price mismatch for {decision_uid}: "
                    f"SIGNAL={_ref_price_float!r} order_plan={_plan_ref_price_float!r}"
                )

            # Validate stop_loss agreement
            try:
                _plan_stop_loss_f = _finite_float(float(plan_stop_loss))
            except (ValueError, TypeError) as exc:
                raise MigrationError(
                    f"Non-finite stop_loss in order_plan for {decision_uid}: {exc}"
                ) from exc

            # Validate take_profit agreement
            _plan_take_profit_f: float | None = None
            if plan_take_profit is not None:
                try:
                    _plan_take_profit_f = _finite_float(float(plan_take_profit))
                except (ValueError, TypeError) as exc:
                    raise MigrationError(
                        f"Non-finite take_profit in order_plan for {decision_uid}: {exc}"
                    ) from exc

            # --- Repair 3: Compare RISK_PASS signal stop_loss/take_profit to
            # order_plan top-level stop_loss/take_profit with exact None symmetry ---
            sig_stop_loss = plan_signal.get("stop_loss")
            if sig_stop_loss is None:
                raise MigrationError(
                    f"Missing stop_loss in order_plan.signal for {decision_uid}"
                )
            # plan_stop_loss already validated as non-None above
            try:
                _sig_sl_f = _finite_float(float(sig_stop_loss))
            except (ValueError, TypeError) as exc:
                raise MigrationError(
                    f"Non-finite signal stop_loss for {decision_uid}: {exc}"
                ) from exc
            if _float_hex(_sig_sl_f) != _float_hex(_plan_stop_loss_f):
                raise MigrationError(
                    f"Signal/order_plan stop_loss mismatch for {decision_uid}: "
                    f"signal={_sig_sl_f!r} order_plan={_plan_stop_loss_f!r}"
                )

            # Validate take_profit agreement — exact None symmetry
            sig_take_profit = plan_signal.get("take_profit")
            if sig_take_profit is None and plan_take_profit is not None:
                raise MigrationError(
                    f"Signal/order_plan take_profit None mismatch for {decision_uid}: "
                    f"signal=None order_plan={plan_take_profit!r}"
                )
            if sig_take_profit is not None and plan_take_profit is None:
                raise MigrationError(
                    f"Signal/order_plan take_profit None mismatch for {decision_uid}: "
                    f"signal={sig_take_profit!r} order_plan=None"
                )
            if sig_take_profit is not None and plan_take_profit is not None:
                try:
                    _sig_tp_f = _finite_float(float(sig_take_profit))
                except (ValueError, TypeError) as exc:
                    raise MigrationError(
                        f"Non-finite signal take_profit for {decision_uid}: {exc}"
                    ) from exc
                if _float_hex(_sig_tp_f) != _float_hex(_plan_take_profit_f):
                    raise MigrationError(
                        f"Signal/order_plan take_profit mismatch for {decision_uid}: "
                        f"signal={_sig_tp_f!r} order_plan={_plan_take_profit_f!r}"
                    )

            # Validate leverage is integral — reject non-integral rather than int-truncating
            if isinstance(plan_leverage, bool) or not isinstance(plan_leverage, (int, float)):
                raise MigrationError(
                    f"Non-numeric leverage for {decision_uid}: {plan_leverage!r}"
                )
            if isinstance(plan_leverage, float) and plan_leverage != int(plan_leverage):
                raise MigrationError(
                    f"Non-integral leverage for {decision_uid}: {plan_leverage!r}"
                )
            _leverage = int(plan_leverage)
            if _leverage <= 0:
                raise MigrationError(
                    f"Non-positive leverage for {decision_uid}: {_leverage!r}"
                )

            # Validate all request floats are finite before computing request identity
            for fname, fval in [("plan_qty", plan_qty), ("plan_stop_loss", plan_stop_loss)]:
                try:
                    _finite_float(float(fval))
                except (ValueError, TypeError) as exc:
                    raise MigrationError(
                        f"Non-finite {fname} for {decision_uid}: {exc}"
                    ) from exc
            if plan_limit_price is not None:
                try:
                    _finite_float(float(plan_limit_price))
                except (ValueError, TypeError) as exc:
                    raise MigrationError(
                        f"Non-finite plan_limit_price for {decision_uid}: {exc}"
                    ) from exc
            if plan_take_profit is not None:
                try:
                    _finite_float(float(plan_take_profit))
                except (ValueError, TypeError) as exc:
                    raise MigrationError(
                        f"Non-finite plan_take_profit for {decision_uid}: {exc}"
                    ) from exc

            request_id, request_preimage, request_version = compute_request_identity(
                intent_id=intent_id,
                symbol=str(plan_symbol),
                direction=str(plan_direction),
                ref_price=_plan_ref_price_float,
                qty=float(plan_qty),
                entry_type=str(plan_entry_type),
                limit_price=float(plan_limit_price) if plan_limit_price is not None else None,
                stop_loss=_plan_stop_loss_f,
                take_profit=_plan_take_profit_f,
                leverage=_leverage,
            )

            # --- 3. Check for existing identity row ---
            existing = self.conn.execute(
                "SELECT request_id, intent_preimage, request_preimage, "
                "origin_run_id, origin_decision_uid, cloid_seed, state, submitted_ts "
                "FROM order_identity WHERE intent_id = ?",
                (intent_id,),
            ).fetchone()
            if existing is not None:
                # Same intent — all preimages must match exactly
                if existing["request_id"] != request_id:
                    raise MigrationError(
                        f"Intent collision during migration: intent_id={intent_id} "
                        f"has existing request_id={existing['request_id']} but "
                        f"new request_id={request_id} (decision_uid={decision_uid})"
                    )
                if existing["intent_preimage"] != intent_preimage:
                    raise MigrationError(
                        f"Intent preimage collision during migration: intent_id={intent_id} "
                        f"has different preimage (decision_uid={decision_uid})"
                    )
                if existing["request_preimage"] != request_preimage:
                    raise MigrationError(
                        f"Request preimage collision during migration: request_id={request_id} "
                        f"(decision_uid={decision_uid})"
                    )
                # Repair 2-3: Compare retained origin_run_id, origin_decision_uid,
                # cloid_seed, state, and submitted mapping. Any incompatible
                # legacy mapping must roll back the whole migration.
                # We need to determine what state this new row would get
                # to compare against existing.
                order_rows_check = self.conn.execute(
                    """SELECT o.cloid, o.trade_id, o.decision_uid
                       FROM orders o
                       WHERE o.decision_uid = ?
                       ORDER BY o.ts_submit""",
                    (decision_uid,),
                ).fetchall()
                if order_rows_check:
                    for o_row in order_rows_check:
                        if o_row["trade_id"] is None:
                            raise MigrationError(
                                f"Order {o_row['cloid']} has NULL trade_id for "
                                f"decision_uid={decision_uid}; incompatible legacy mapping"
                            )
                    new_state = "LEGACY_SUBMITTED"
                    new_submitted_ts = fp_ts
                else:
                    new_state = "LEGACY_RESERVED"
                    new_submitted_ts = None

                if existing["state"] != new_state:
                    raise MigrationError(
                        f"Duplicate intent_id={intent_id} has incompatible state: "
                        f"existing={existing['state']} new={new_state} "
                        f"(decision_uid={decision_uid})"
                    )
                if existing["origin_run_id"] != run_id:
                    raise MigrationError(
                        f"Duplicate intent_id={intent_id} has incompatible origin_run_id: "
                        f"existing={existing['origin_run_id']} new={run_id} "
                        f"(decision_uid={decision_uid})"
                    )
                if existing["origin_decision_uid"] != decision_uid:
                    raise MigrationError(
                        f"Duplicate intent_id={intent_id} has incompatible origin_decision_uid: "
                        f"existing={existing['origin_decision_uid']} new={decision_uid} "
                        f"(decision_uid={decision_uid})"
                    )
                if existing["cloid_seed"] != decision_uid:
                    raise MigrationError(
                        f"Duplicate intent_id={intent_id} has incompatible cloid_seed: "
                        f"existing={existing['cloid_seed']} new={decision_uid} "
                        f"(decision_uid={decision_uid})"
                    )
                # Exact match — skip (already migrated)
                continue

            # Check request_id uniqueness
            existing_req = self.conn.execute(
                "SELECT intent_id FROM order_identity WHERE request_id = ?",
                (request_id,),
            ).fetchone()
            if existing_req is not None:
                raise MigrationError(
                    f"Request collision during migration: request_id={request_id} "
                    f"already maps to intent_id={existing_req['intent_id']} but "
                    f"new intent_id={intent_id} (decision_uid={decision_uid})"
                )

            # --- 4. Determine state from consistent order+trade mapping ---
            # Repair 2-1 & 2-2: Every submitted order must have non-null trade_id
            # and a trade with BOTH run_id==fingerprint.run_id and
            # entry_decision_uid==fingerprint.decision_uid.
            order_rows = self.conn.execute(
                """SELECT o.cloid, o.trade_id, o.decision_uid
                   FROM orders o
                   WHERE o.decision_uid = ?
                   ORDER BY o.ts_submit""",
                (decision_uid,),
            ).fetchall()

            if order_rows:
                # Repair 2-2: every order that contributes to submitted state
                # MUST have non-null trade_id
                for o_row in order_rows:
                    if o_row["trade_id"] is None:
                        raise MigrationError(
                            f"Order {o_row['cloid']} has NULL trade_id for "
                            f"decision_uid={decision_uid}; incompatible legacy mapping"
                        )
                    trade = self.conn.execute(
                        "SELECT run_id, entry_decision_uid FROM trades WHERE trade_id = ?",
                        (o_row["trade_id"],),
                    ).fetchone()
                    if trade is None:
                        raise MigrationError(
                            f"Order {o_row['cloid']} references non-existent trade "
                            f"trade_id={o_row['trade_id']} for decision_uid={decision_uid}"
                        )
                    # Repair 2-1: Verify trade's run_id AND entry_decision_uid
                    # both match the fingerprint
                    if str(trade["run_id"]) != run_id:
                        raise MigrationError(
                            f"Order {o_row['cloid']} trade_id={o_row['trade_id']} "
                            f"has run_id={trade['run_id']!r} but fingerprint "
                            f"run_id={run_id}; cross-run trade mapping"
                        )
                    if str(trade["entry_decision_uid"]) != decision_uid:
                        raise MigrationError(
                            f"Order {o_row['cloid']} trade_id={o_row['trade_id']} "
                            f"has entry_decision_uid={trade['entry_decision_uid']!r} "
                            f"but decision_uid={decision_uid}; cross-run/orphan mapping"
                        )
                state = "LEGACY_SUBMITTED"
                submitted_ts = fp_ts
            else:
                state = "LEGACY_RESERVED"
                submitted_ts = None

            # --- 5. Insert identity row ---
            self.conn.execute(
                """INSERT INTO order_identity(
                     intent_id, intent_preimage, intent_version,
                     request_id, request_preimage, request_version,
                     cloid_seed, origin_run_id, origin_decision_uid,
                     state, reserved_ts, submitted_ts
                   ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    intent_id,
                    intent_preimage,
                    intent_version,
                    request_id,
                    request_preimage,
                    request_version,
                    decision_uid,  # legacy: use original decision_uid as cloid_seed
                    run_id,
                    decision_uid,
                    state,
                    fp_ts,
                    submitted_ts,
                ),
            )

        # --- TS-P1-002 repair-round-4: global coverage validation ---
        # Every legacy trade and order must be covered by exactly one
        # fingerprint origin before the v3 version bump.  Ambiguous or
        # orphan evidence fails closed.
        self._validate_global_coverage()

        # All rows migrated and coverage validated → bump version
        self.conn.execute(
            "INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '3')"
        )

    # ------------------------------------------------------------------
    # v3 → v4 migration (submission_attempts + recovery_evidence)
    # ------------------------------------------------------------------

    def _migrate_v3_to_v4(self) -> None:
        """Transactional creation of v4 tables without rebuilding order_identity.

        One BEGIN IMMEDIATE transaction: creates both new tables and indexes,
        then bumps schema_version to 4. On failure, rollback leaves valid v3
        with no v4 residue.
        """
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            self._create_tables_v4()
            self.conn.execute(
                "INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '4')"
            )
        except Exception:
            self.conn.rollback()
            raise
        self.conn.commit()

    def _create_tables_v4(self) -> None:
        """Create v4-only tables and indexes (idempotent via IF NOT EXISTS).

        Does NOT recreate any v3 table. Must be called inside a transaction
        or standalone — each statement auto-commits if not in a tx.
        """
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS submission_attempts (
              attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
              intent_id TEXT NOT NULL
                CHECK(length(intent_id) = 74 AND substr(intent_id, 1, 10) = 'intent-v1:'),
              request_id TEXT NOT NULL
                CHECK(length(request_id) = 75 AND substr(request_id, 1, 11) = 'request-v1:'),
              run_id TEXT NOT NULL CHECK(run_id != ''),
              decision_uid TEXT NOT NULL CHECK(decision_uid != ''),
              state TEXT NOT NULL CHECK(state IN (
                'SUBMITTING','VERIFIED_SUCCESS','DEFINITIVE_REJECTION','UNKNOWN_SUBMISSION'
              )),
              outcome TEXT CHECK(outcome IN (
                'PRE_SEND_FAILURE','DEFINITIVE_REJECTION','OUTCOME_UNKNOWN','VERIFIED_SUCCESS'
              )),
              planned_cloids_json TEXT NOT NULL CHECK(planned_cloids_json != ''),
              created_ts TEXT NOT NULL CHECK(created_ts != ''),
              resolved_ts TEXT,
              CHECK(
                (state = 'SUBMITTING' AND resolved_ts IS NULL)
                OR (state != 'SUBMITTING' AND resolved_ts IS NOT NULL)
              )
            )""")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS submission_recovery_evidence (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              attempt_id INTEGER NOT NULL REFERENCES submission_attempts(attempt_id),
              cycle_number INTEGER NOT NULL CHECK(cycle_number >= 1),
              source TEXT NOT NULL CHECK(source IN (
                'open_orders','historical_orders','user_fills','positions','direct_cloid'
              )),
              cloid TEXT NOT NULL,
              found INTEGER NOT NULL CHECK(found IN (0, 1)),
              detail TEXT NOT NULL DEFAULT '',
              ts TEXT NOT NULL CHECK(ts != '')
            )""")
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_submission_attempts_intent "
            "ON submission_attempts(intent_id)")
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_submission_attempts_state "
            "ON submission_attempts(state)")
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_recovery_evidence_attempt "
            "ON submission_recovery_evidence(attempt_id, cycle_number)")

    def _validate_global_coverage(self) -> None:
        """Validate every legacy trade/order is covered by exactly one identity origin.

        Must be called inside the migration transaction after backfill.
        Raises MigrationError on any ambiguity, orphan evidence, or
        cross-wired mapping.
        """
        # --- Validate every trade has exactly one matching identity origin ---
        trade_rows = self.conn.execute(
            "SELECT trade_id, run_id, entry_decision_uid FROM trades"
        ).fetchall()

        for trade_row in trade_rows:
            trade_id = int(trade_row["trade_id"])
            trade_run_id = str(trade_row["run_id"])
            trade_ed_uid = str(trade_row["entry_decision_uid"])

            identity_count = self.conn.execute(
                "SELECT COUNT(*) FROM order_identity "
                "WHERE origin_run_id = ? AND origin_decision_uid = ?",
                (trade_run_id, trade_ed_uid),
            ).fetchone()

            if identity_count[0] == 0:
                raise MigrationError(
                    f"Trade trade_id={trade_id} run_id={trade_run_id} "
                    f"entry_decision_uid={trade_ed_uid} has no matching "
                    f"fingerprint origin; ambiguous evidence"
                )
            if identity_count[0] > 1:
                raise MigrationError(
                    f"Trade trade_id={trade_id} run_id={trade_run_id} "
                    f"entry_decision_uid={trade_ed_uid} has multiple "
                    f"({identity_count[0]}) matching fingerprint origins; "
                    f"ambiguous evidence"
                )

        # --- Validate every order is covered through its trade ---
        order_rows = self.conn.execute(
            "SELECT cloid, decision_uid, trade_id FROM orders"
        ).fetchall()

        for order_row in order_rows:
            cloid = str(order_row["cloid"])
            order_decision_uid = str(order_row["decision_uid"])
            order_trade_id = order_row["trade_id"]

            if order_trade_id is None:
                raise MigrationError(
                    f"Order {cloid} has NULL trade_id; "
                    f"incompatible legacy mapping"
                )

            trade = self.conn.execute(
                "SELECT run_id, entry_decision_uid FROM trades WHERE trade_id = ?",
                (order_trade_id,),
            ).fetchone()

            if trade is None:
                raise MigrationError(
                    f"Order {cloid} references non-existent trade "
                    f"trade_id={order_trade_id}"
                )

            trade_run_id = str(trade["run_id"])
            trade_ed_uid = str(trade["entry_decision_uid"])

            identity_count = self.conn.execute(
                "SELECT COUNT(*) FROM order_identity "
                "WHERE origin_run_id = ? AND origin_decision_uid = ?",
                (trade_run_id, trade_ed_uid),
            ).fetchone()

            if identity_count[0] == 0:
                raise MigrationError(
                    f"Order {cloid} trade_id={order_trade_id} "
                    f"run_id={trade_run_id} entry_decision_uid={trade_ed_uid} "
                    f"has no matching fingerprint origin"
                )
            if identity_count[0] > 1:
                raise MigrationError(
                    f"Order {cloid} trade_id={order_trade_id} "
                    f"run_id={trade_run_id} entry_decision_uid={trade_ed_uid} "
                    f"has multiple ({identity_count[0]}) matching fingerprint origins; "
                    f"ambiguous evidence"
                )

            # Verify the order's decision_uid matches the identity origin
            ident = self.conn.execute(
                "SELECT origin_decision_uid FROM order_identity "
                "WHERE origin_run_id = ? AND origin_decision_uid = ?",
                (trade_run_id, trade_ed_uid),
            ).fetchone()

            if ident is not None and str(ident["origin_decision_uid"]) != order_decision_uid:
                raise MigrationError(
                    f"Order {cloid} decision_uid={order_decision_uid} does not match "
                    f"identity origin_decision_uid={ident['origin_decision_uid']} "
                    f"for trade_id={order_trade_id}"
                )

    # ------------------------------------------------------------------
    # Identity reservation
    # ------------------------------------------------------------------

    def reserve_identity(
        self,
        intent_id: str,
        intent_preimage: str,
        intent_version: str,
        request_id: str,
        request_preimage: str,
        request_version: str,
        cloid_seed: str,
        origin_run_id: str,
        origin_decision_uid: str,
    ) -> Literal["RESERVED", "BLOCKED"]:
        """Reserve an identity row before broker I/O.

        Returns 'RESERVED' if a new reservation was created.
        Returns 'BLOCKED' if the exact identity already exists (idempotent replay).

        Raises IdentityCollisionError on mismatch.
        Must be called inside an explicit transaction (BEGIN IMMEDIATE).
        """
        now = _to_iso(self._clock())

        # Check existing by intent_id
        existing = self.conn.execute(
            "SELECT intent_id, intent_preimage, request_id, request_preimage, state FROM order_identity WHERE intent_id = ?",
            (intent_id,),
        ).fetchone()

        if existing is not None:
            # Same intent — verify request matches
            if existing["request_id"] != request_id:
                raise IdentityCollisionError(
                    "IDENTITY_COLLISION_INTENT",
                    f"intent_id={intent_id} maps to request_id={existing['request_id']} "
                    f"but new request_id={request_id}",
                )
            # Verify preimages match exactly
            if existing["intent_preimage"] != intent_preimage:
                raise IdentityCollisionError(
                    "IDENTITY_DIGEST_COLLISION",
                    f"intent_id={intent_id} digest collision: same hash, different preimage",
                )
            if existing["request_preimage"] != request_preimage:
                raise IdentityCollisionError(
                    "IDENTITY_DIGEST_COLLISION",
                    f"request_id={request_id} digest collision: same hash, different preimage",
                )
            # Exact match — block duplicate
            return "BLOCKED"

        # Check request_id uniqueness against different intents
        existing_req = self.conn.execute(
            "SELECT intent_id FROM order_identity WHERE request_id = ?",
            (request_id,),
        ).fetchone()
        if existing_req is not None:
            raise IdentityCollisionError(
                "IDENTITY_COLLISION_REQUEST",
                f"request_id={request_id} already maps to intent_id={existing_req['intent_id']} "
                f"but new intent_id={intent_id}",
            )

        # Insert reservation
        self.conn.execute(
            """INSERT INTO order_identity(
                 intent_id, intent_preimage, intent_version,
                 request_id, request_preimage, request_version,
                 cloid_seed, origin_run_id, origin_decision_uid,
                 state, reserved_ts, submitted_ts
               ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'RESERVED', ?, NULL)""",
            (
                intent_id,
                intent_preimage,
                intent_version,
                request_id,
                request_preimage,
                request_version,
                cloid_seed,
                origin_run_id,
                origin_decision_uid,
                now,
            ),
        )
        return "RESERVED"

    def get_identity_by_intent(self, intent_id: str) -> dict[str, Any] | None:
        row = self.conn.execute(
            "SELECT * FROM order_identity WHERE intent_id = ?", (intent_id,)
        ).fetchone()
        return None if row is None else dict(row)

    def get_identity_by_request(self, request_id: str) -> dict[str, Any] | None:
        row = self.conn.execute(
            "SELECT * FROM order_identity WHERE request_id = ?", (request_id,)
        ).fetchone()
        return None if row is None else dict(row)

    # ------------------------------------------------------------------
    # Atomic post-broker finalization
    # ------------------------------------------------------------------

    def finalize_submission(
        self,
        intent_id: str,
        request_id: str,
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
        orders_data: list[dict[str, Any]],
    ) -> int:
        """Atomically finalize: insert trade, all orders, transition RESERVED→SUBMITTED.

        All steps execute in one explicit serialized SQLite transaction.
        If any step fails, the entire transaction rolls back. The already-committed
        reservation remains RESERVED.

        Returns the new trade_id.
        """
        if not orders_data:
            raise IdentityCollisionError(
                "IDENTITY_FINALIZE_FAILED",
                f"intent_id={intent_id}: empty orders_data, cannot finalize",
            )

        self.conn.execute("BEGIN IMMEDIATE")
        try:
            trade_id = self._finalize_submission_in_tx(
                intent_id=intent_id,
                request_id=request_id,
                run_id=run_id,
                coin=coin,
                direction=direction,
                qty=qty,
                entry_decision_uid=entry_decision_uid,
                signal_ts=signal_ts,
                decision_ts=decision_ts,
                expected_px=expected_px,
                risk_dollars=risk_dollars,
                risk_pct=risk_pct,
                leverage=leverage,
                sl_initial=sl_initial,
                tp_initial=tp_initial,
                llm_directive_id=llm_directive_id,
                orders_data=orders_data,
            )
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

        return trade_id

    def _finalize_submission_in_tx(
        self,
        intent_id: str,
        request_id: str,
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
        orders_data: list[dict[str, Any]],
    ) -> int:
        """Core finalization logic inside an already-open transaction."""

        # 1. Verify identity exists and is RESERVED with matching request_id
        ident = self.conn.execute(
            "SELECT state, request_id FROM order_identity WHERE intent_id = ?",
            (intent_id,),
        ).fetchone()
        if ident is None:
            raise IdentityCollisionError(
                "IDENTITY_FINALIZE_FAILED",
                f"intent_id={intent_id} not found at finalization",
            )
        if ident["state"] != "RESERVED":
            raise IdentityCollisionError(
                "IDENTITY_FINALIZE_FAILED",
                f"intent_id={intent_id} state={ident['state']} (expected RESERVED)",
            )
        if ident["request_id"] != request_id:
            raise IdentityCollisionError(
                "IDENTITY_FINALIZE_FAILED",
                f"intent_id={intent_id} request_id mismatch: "
                f"stored={ident['request_id']} submitted={request_id}",
            )

        # 2. Insert trade
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
        trade_id = int(cursor.lastrowid)

        # 3. Insert each order collision-safely
        for od in orders_data:
            self._insert_order_in_tx(
                cloid=str(od["cloid"]),
                oid=od.get("oid"),
                group_id=od.get("group_id"),
                order_ref=str(od["order_ref"]),
                order_json=od["order_json"] if isinstance(od["order_json"], str)
                            else _json(od["order_json"]),
                decision_uid=str(od["decision_uid"]),
                trade_id=trade_id,
                role=str(od["role"]),
                status=str(od["status"]),
                qty=float(od["qty"]),
                filled_qty=float(od.get("filled_qty", 0.0)),
                avg_fill_px=od.get("avg_fill_px"),
            )

        # 4. Transition exactly one row from RESERVED → SUBMITTED
        now = _to_iso(self._clock())
        cursor = self.conn.execute(
            """UPDATE order_identity
               SET state = 'SUBMITTED', submitted_ts = ?
               WHERE intent_id = ? AND state = 'RESERVED'""",
            (now, intent_id),
        )
        if cursor.rowcount != 1:
            raise IdentityCollisionError(
                "IDENTITY_FINALIZE_FAILED",
                f"intent_id={intent_id} update rowcount={cursor.rowcount} (expected 1)",
            )

        return trade_id

    def _insert_order_in_tx(
        self,
        cloid: str,
        oid: int | None,
        group_id: str | None,
        order_ref: str,
        order_json: str,
        decision_uid: str,
        trade_id: int,
        role: str,
        status: str,
        qty: float,
        filled_qty: float = 0.0,
        avg_fill_px: float | None = None,
        ts_submit: datetime | str | None = None,
        ts_last: datetime | str | None = None,
    ) -> None:
        """Insert an order inside an already-open transaction (no commit).

        Collision-safe: on PK conflict, compares all immutable identity fields
        (oid, group_id, order_ref, decision_uid, trade_id, role, qty).
        Raises OrderCollisionError on mismatch.
        """
        submit_ts = _to_iso(ts_submit) or _to_iso(self._clock())
        last_ts = _to_iso(ts_last) or submit_ts

        try:
            self.conn.execute(
                """
                INSERT INTO orders(
                  cloid, oid, group_id, order_ref, order_json, decision_uid, trade_id,
                  role, status, qty, filled_qty, avg_fill_px, ts_submit, ts_last
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    cloid, oid, group_id, order_ref, order_json,
                    decision_uid, trade_id, role, status, qty,
                    filled_qty, avg_fill_px, submit_ts, last_ts,
                ),
            )
        except sqlite3.IntegrityError:
            # Cloid already exists — check for collision
            existing = self.conn.execute(
                "SELECT * FROM orders WHERE cloid = ?", (cloid,)
            ).fetchone()
            if existing is None:
                raise  # should not happen

            # Compare all immutable identity fields
            if (str(existing["decision_uid"]) != decision_uid
                    or existing["trade_id"] != trade_id
                    or str(existing["role"]) != role
                    or float(existing["qty"]) != qty
                    or str(existing["order_ref"]) != order_ref
                    or existing["oid"] != oid
                    or str(existing["group_id"] or "") != str(group_id or "")):
                raise OrderCollisionError(
                    cloid=cloid,
                    existing_decision_uid=str(existing["decision_uid"]),
                    new_decision_uid=decision_uid,
                )

            # Idempotent replay — update mutable fields only
            self.conn.execute(
                """UPDATE orders
                   SET status = ?, filled_qty = ?, avg_fill_px = ?,
                       ts_last = ?, order_json = ?
                   WHERE cloid = ?""",
                (status, filled_qty, avg_fill_px, last_ts, order_json, cloid),
            )

    # ------------------------------------------------------------------
    # Collision-safe insert_order (public API — commits independently)
    # ------------------------------------------------------------------

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
    ) -> None:
        """Insert an order collision-safely (commits independently).

        Replaces the former INSERT OR REPLACE behavior.
        On collision, preserves the original row and raises OrderCollisionError.
        """
        submit_ts = _to_iso(ts_submit) or _to_iso(datetime.now(UTC))
        last_ts = _to_iso(ts_last) or submit_ts
        order_json_str = _json(order_json)

        try:
            self.conn.execute(
                """
                INSERT INTO orders(
                  cloid, oid, group_id, order_ref, order_json, decision_uid, trade_id,
                  role, status, qty, filled_qty, avg_fill_px, ts_submit, ts_last
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    cloid, oid, group_id, order_ref, order_json_str,
                    decision_uid, trade_id, role, status, qty,
                    filled_qty, avg_fill_px, submit_ts, last_ts,
                ),
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            # Cloid collision — check all immutable identity fields
            existing = self.conn.execute(
                "SELECT * FROM orders WHERE cloid = ?", (cloid,)
            ).fetchone()
            if existing is None:
                self.conn.commit()
                raise

            # Compare ALL immutable identity/mapping fields
            if (str(existing["decision_uid"]) != decision_uid
                    or existing["trade_id"] != trade_id
                    or str(existing["role"]) != role
                    or float(existing["qty"]) != qty
                    or str(existing["order_ref"]) != order_ref
                    or existing["oid"] != oid
                    or str(existing["group_id"] or "") != str(group_id or "")):
                # Rollback any pending work before raising
                try:
                    self.conn.rollback()
                except Exception:
                    pass
                raise OrderCollisionError(
                    cloid=cloid,
                    existing_decision_uid=str(existing["decision_uid"]),
                    new_decision_uid=decision_uid,
                )

            # Idempotent replay — update mutable fields only
            self.conn.execute(
                """UPDATE orders
                   SET status = ?, filled_qty = ?, avg_fill_px = ?,
                       ts_last = ?, order_json = ?
                   WHERE cloid = ?""",
                (status, filled_qty, avg_fill_px, last_ts, order_json_str, cloid),
            )
            self.conn.commit()

    # ------------------------------------------------------------------
    # Existing methods (unchanged signatures)
    # ------------------------------------------------------------------

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
            raise LookupError(f"run not found for risk scoping: {run_id}")
        return str(row["mode"]), str(row["network"])

    def realized_pnl_today(self, run_id: str, now: datetime | None = None) -> float:
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
        row = self.conn.execute(
            "SELECT COALESCE(SUM(qty), 0.0), SUM(qty * px) FROM fills WHERE cloid = ?",
            (cloid,),
        ).fetchone()
        qty = float(row[0]) if row and row[0] is not None else 0.0
        vwap = (float(row[1]) / qty) if qty > 0 and row[1] is not None else None
        return qty, vwap

    def trade_fill_totals(self, trade_id: int) -> dict[str, Any]:
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
        for order in self.get_orders_for_trade(trade_id):
            if order["role"] != "ENTRY" or order["status"] not in {"OPEN", "SUBMITTED", "PENDING"}:
                continue
            filled_qty, _ = self.order_fill_totals(str(order["cloid"]))
            if filled_qty < float(order["qty"]) - 1e-9:
                return True
        return False

    def trade_costs(self, decision_uid: str) -> float:
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
            "identities": self._rows("SELECT * FROM order_identity ORDER BY reserved_ts"),
            "submission_attempts": self._rows(
                "SELECT * FROM submission_attempts ORDER BY attempt_id"
            ) if self.get_meta("schema_version") == "4" else [],
            "submission_recovery_evidence": self._rows(
                "SELECT * FROM submission_recovery_evidence ORDER BY id"
            ) if self.get_meta("schema_version") == "4" else [],
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

    # ------------------------------------------------------------------
    # TS-P1-003 submission attempt lifecycle
    # ------------------------------------------------------------------

    def create_submission_attempt(
        self,
        intent_id: str,
        request_id: str,
        run_id: str,
        decision_uid: str,
        planned_cloids: list[str],
    ) -> int:
        """Create a SUBMITTING attempt with planned cloids BEFORE broker I/O.

        Must be called inside an explicit transaction. Returns the new attempt_id.
        """
        now = _to_iso(self._clock())
        planned_json = _json({"cloids": planned_cloids})
        cursor = self.conn.execute(
            """INSERT INTO submission_attempts(
                 intent_id, request_id, run_id, decision_uid,
                 state, outcome, planned_cloids_json, created_ts
               ) VALUES (?, ?, ?, ?, 'SUBMITTING', NULL, ?, ?)""",
            (intent_id, request_id, run_id, decision_uid, planned_json, now),
        )
        return int(cursor.lastrowid)

    def resolve_submission_attempt(
        self,
        attempt_id: int,
        state: str,
        outcome: str,
    ) -> bool:
        """Resolve an attempt from SUBMITTING to a terminal state.

        Must be called inside an explicit transaction. Returns True if exactly
        one row was updated.
        """
        now = _to_iso(self._clock())
        cursor = self.conn.execute(
            """UPDATE submission_attempts
               SET state = ?, outcome = ?, resolved_ts = ?
               WHERE attempt_id = ? AND state = 'SUBMITTING'""",
            (state, outcome, now, attempt_id),
        )
        return cursor.rowcount == 1

    def get_active_unknown_count(self) -> int:
        """Return count of unresolved UNKNOWN_SUBMISSION attempts."""
        row = self.conn.execute(
            "SELECT COUNT(*) FROM submission_attempts WHERE state = 'UNKNOWN_SUBMISSION'"
        ).fetchone()
        return int(row[0]) if row else 0

    def get_active_submitting_count(self) -> int:
        """Return count of currently SUBMITTING attempts."""
        row = self.conn.execute(
            "SELECT COUNT(*) FROM submission_attempts WHERE state = 'SUBMITTING'"
        ).fetchone()
        return int(row[0]) if row else 0

    def get_submission_attempt(self, attempt_id: int) -> dict[str, Any] | None:
        row = self.conn.execute(
            "SELECT * FROM submission_attempts WHERE attempt_id = ?", (attempt_id,)
        ).fetchone()
        return None if row is None else dict(row)

    def get_active_unknown_attempts(self) -> list[dict[str, Any]]:
        """Return all unresolved UNKNOWN_SUBMISSION attempts."""
        return self._rows(
            "SELECT * FROM submission_attempts WHERE state = 'UNKNOWN_SUBMISSION' "
            "ORDER BY created_ts"
        )

    def get_submission_attempts_for_intent(
        self, intent_id: str
    ) -> list[dict[str, Any]]:
        return self._rows(
            "SELECT * FROM submission_attempts WHERE intent_id = ? ORDER BY attempt_id",
            (intent_id,),
        )

    # ------------------------------------------------------------------
    # TS-P1-003 recovery evidence (append-only, secret-safe)
    # ------------------------------------------------------------------

    def insert_recovery_evidence(
        self,
        attempt_id: int,
        cycle_number: int,
        source: str,
        cloid: str,
        found: bool,
        detail: str,
    ) -> int:
        """Append one sanitized evidence row. Never persists raw exchange text.

        The `detail` field must already be sanitized by the caller.
        Returns the new row id.
        """
        now = _to_iso(self._clock())
        cursor = self.conn.execute(
            """INSERT INTO submission_recovery_evidence(
                 attempt_id, cycle_number, source, cloid, found, detail, ts
               ) VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (attempt_id, cycle_number, source, cloid, int(found), detail, now),
        )
        self.conn.commit()
        return int(cursor.lastrowid)

    def get_recovery_evidence(
        self, attempt_id: int
    ) -> list[dict[str, Any]]:
        return self._rows(
            "SELECT * FROM submission_recovery_evidence WHERE attempt_id = ? "
            "ORDER BY cycle_number, id",
            (attempt_id,),
        )

    def get_last_recovery_cycle(
        self, attempt_id: int
    ) -> int:
        """Return the highest cycle_number for an attempt, or 0 if none."""
        row = self.conn.execute(
            "SELECT COALESCE(MAX(cycle_number), 0) FROM submission_recovery_evidence "
            "WHERE attempt_id = ?",
            (attempt_id,),
        ).fetchone()
        return int(row[0]) if row else 0

    def _rows(self, sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
        return [dict(row) for row in self.conn.execute(sql, params).fetchall()]
