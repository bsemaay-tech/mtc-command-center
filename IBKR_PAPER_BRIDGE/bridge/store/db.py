"""SQLite Store: v4 durable identity/submission ledger, v5 partial-fill recovery."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from collections.abc import Mapping
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable, Literal

from bridge.engine.types import (
    PARTIAL_STATE_TRANSITIONS,
    PARTIAL_TERMINAL_STATES,
    ActionOutcome,
    ActionRecordStatus,
    PartialActionKind,
    PartialProtectionState,
)


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
_SUBMISSION_ATTEMPT_VERSION = "ts-p1-003-attempt-v1"
_RECOVERY_PAYLOAD_VERSION = "ts-p1-003-recovery-v1"
_ATTEMPT_TRANSITIONS: dict[str, frozenset[str]] = {
    "SUBMITTING": frozenset({
        "PRE_SEND_FAILURE",
        "DEFINITIVE_REJECTION",
        "UNKNOWN_SUBMISSION",
        "VERIFIED_SUCCESS",
    }),
    "VERIFIED_SUCCESS": frozenset({"FINALIZED"}),
    "UNKNOWN_SUBMISSION": frozenset({"CONFIRMED_PRESENT", "CONFIRMED_ABSENT"}),
}
_QUARANTINE_STATES = frozenset({
    "SUBMITTING",
    "UNKNOWN_SUBMISSION",
    "CONFIRMED_PRESENT",
})
_EVIDENCE_STATUSES = frozenset({
    "FOUND",
    "NOT_FOUND",
    "QUERY_FAILED",
    "UNAVAILABLE",
    "TRUNCATED",
    "STALE",
    "CONFLICTING",
})


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


def compute_submission_attempt_id(request_id: str) -> str:
    """Derive the stable ledger identifier without exposing plan content."""
    digest = hashlib.sha256(
        f"{_SUBMISSION_ATTEMPT_VERSION}:{request_id}".encode("utf-8")
    ).hexdigest()
    return f"attempt-v1:{digest}"


# ---------------------------------------------------------------------------
# TS-P1-004 deterministic partial-recovery identities
# ---------------------------------------------------------------------------

SCHEMA_VERSION_BASELINE = 4
"""Default target: the accepted TS-P1-003 identity/submission ledger."""

SCHEMA_VERSION_PARTIAL_FILL = 5
"""Additive TS-P1-004 partial-fill recovery ledger; opt-in, never automatic."""

SUPPORTED_TARGET_SCHEMA_VERSIONS = (
    SCHEMA_VERSION_BASELINE,
    SCHEMA_VERSION_PARTIAL_FILL,
)

_PARTIAL_RECOVERY_VERSION = "ts-p1-004-recovery-v1"
_PARTIAL_ACTION_VERSION = "ts-p1-004-action-v1"

_PARTIAL_EVIDENCE_TABLES = (
    "orders",
    "trades",
    "fills",
    "decisions",
    "events",
    "equity",
    "signal_fingerprints",
    "order_identity",
    "submission_attempts",
    "submission_recovery_evidence",
)


class PartialRecoveryConflictError(Exception):
    """Raised when a partial-recovery write would break a durable invariant."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


def compute_partial_recovery_id(
    *, trade_id: int, entry_cloid: str, generation: int
) -> str:
    """Stable per trade/entry/generation recovery identity."""
    preimage = _canonical_json({
        "version": _PARTIAL_RECOVERY_VERSION,
        "trade_id": int(trade_id),
        "entry_cloid": str(entry_cloid),
        "generation": int(generation),
    })
    return f"pfr-v1:{hashlib.sha256(preimage.encode('utf-8')).hexdigest()}"


def compute_partial_action_id(
    *,
    kind: str,
    trade_id: int,
    entry_cloid: str,
    entry_request_id: str,
    generation: int | None = None,
    flatten_seq: int | None = None,
    qty_lots: int | None = None,
    target_cloid: str | None = None,
) -> str:
    """Deterministic action identity, one domain per action kind (Gate 1 §4).

    * ``CANCEL_ENTRY`` — entry request identity + entry cloid only, so it is
      quantity- and generation-independent and a late-fill re-entry keeps the
      same pending/unknown cancel context.
    * ``INSTALL_STOP`` — trade/entry identity + generation + target lots.
    * ``FLATTEN`` — the above plus the resolved-attempt sequence.
    * ``CANCEL_PROTECTION`` — trade/entry identity + the exact cloid removed.
    """
    action_kind = PartialActionKind(str(kind))
    body: dict[str, Any] = {
        "version": _PARTIAL_ACTION_VERSION,
        "kind": action_kind.value,
        "entry_cloid": str(entry_cloid),
    }
    if action_kind is PartialActionKind.CANCEL_ENTRY:
        body["entry_request_id"] = str(entry_request_id)
    else:
        body["trade_id"] = int(trade_id)
    if action_kind in {PartialActionKind.INSTALL_STOP, PartialActionKind.FLATTEN}:
        if generation is None or qty_lots is None:
            raise ValueError("generation and qty_lots are required for this action kind")
        body["generation"] = int(generation)
        body["qty_lots"] = int(qty_lots)
    if action_kind is PartialActionKind.FLATTEN:
        if flatten_seq is None:
            raise ValueError("flatten_seq is required for FLATTEN actions")
        body["flatten_seq"] = int(flatten_seq)
    if action_kind is PartialActionKind.CANCEL_PROTECTION:
        if not target_cloid:
            raise ValueError("target_cloid is required for CANCEL_PROTECTION")
        body["target_cloid"] = str(target_cloid)
    preimage = _canonical_json(body)
    return f"pfa-v1:{hashlib.sha256(preimage.encode('utf-8')).hexdigest()}"


def compute_partial_action_cloid(action_id: str) -> str:
    """Exchange cloid bound 1:1 to the action identity.

    A proven-not-applied action therefore re-sends under the *same* cloid; a
    new cloid can only appear together with a new action identity.
    """
    digest = hashlib.blake2s(
        f"{_PARTIAL_ACTION_VERSION}:{action_id}".encode("utf-8"), digest_size=16
    ).hexdigest()
    return f"0x{digest}"


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
    """Raised when a schema migration cannot complete safely."""

    def __init__(self, message: str) -> None:
        super().__init__(f"MIGRATION_FAILED: {message}")


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

    def now(self) -> datetime:
        """Trusted local observation clock used by recovery sequencing."""
        return self._clock().astimezone(UTC)

    # ------------------------------------------------------------------
    # Schema initialization with version-aware migration
    # ------------------------------------------------------------------

    def initialize(
        self, target_schema_version: int = SCHEMA_VERSION_BASELINE
    ) -> None:
        """Open/upgrade the database up to ``target_schema_version``.

        The default target stays v4: TS-P1-004 adds schema v5 as an explicit,
        additive opt-in so that no existing caller — and no existing runtime
        database — is silently upgraded by merely opening it. Reaching v5
        requires ``initialize(target_schema_version=5)``.

        A database already at v5 is reopened idempotently regardless of the
        requested target; this code understands v5 and must never downgrade.
        Unsupported or future versions still fail closed.
        """
        if isinstance(target_schema_version, bool) or not isinstance(
            target_schema_version, int
        ):
            raise RuntimeError(
                f"Unsupported target_schema_version={target_schema_version!r}"
            )
        if target_schema_version not in SUPPORTED_TARGET_SCHEMA_VERSIONS:
            raise RuntimeError(
                f"Unsupported target_schema_version={target_schema_version!r}"
            )
        # Ensure meta table exists before querying it
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT)"
        )
        existing = self.get_meta("schema_version")
        if existing == str(SCHEMA_VERSION_PARTIAL_FILL):
            # Already migrated: idempotent reopen, never an in-place downgrade.
            self._initialize_v5_idempotent()
            return
        if existing is None:
            self._initialize_v4_fresh()
        elif existing == "4":
            self._initialize_v4_idempotent()
        elif existing == "3":
            self._migrate_v3_to_v4()
        elif existing == "2":
            self._migrate_v2_to_v3()
            # Intentionally a second committed transaction. A later v4
            # failure must leave a valid, reopenable v3 database.
            self._migrate_v3_to_v4()
        else:
            # Unsupported or corrupt version → fail closed
            raise RuntimeError(
                f"Unsupported schema_version={existing!r}; cannot initialize safely"
            )
        if target_schema_version >= SCHEMA_VERSION_PARTIAL_FILL:
            self._migrate_v4_to_v5()

    def _initialize_v4_fresh(self) -> None:
        self._create_tables_v4()
        self.conn.execute(
            "INSERT OR REPLACE INTO meta(key, value) VALUES (?, ?)",
            ("schema_version", "4"),
        )
        self.conn.commit()

    def _initialize_v4_idempotent(self) -> None:
        """Re-open an existing v4 database and verify idempotent DDL."""
        self._create_tables_v4()
        self.conn.commit()

    def _create_tables_v4(self) -> None:
        self._create_tables_v3()
        self._create_submission_ledger_v4()

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

    def _create_submission_ledger_v4(self) -> None:
        """Add v4 tables without rebuilding or rewriting order_identity."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS submission_attempts (
              attempt_id TEXT PRIMARY KEY
                CHECK(length(attempt_id) = 75 AND substr(attempt_id, 1, 11) = 'attempt-v1:' AND NOT substr(attempt_id, 12) GLOB '*[^0-9a-f]*'),
              intent_id TEXT UNIQUE NOT NULL REFERENCES order_identity(intent_id),
              request_id TEXT UNIQUE NOT NULL,
              origin_run_id TEXT NOT NULL CHECK(origin_run_id != ''),
              origin_decision_uid TEXT NOT NULL CHECK(origin_decision_uid != ''),
              state TEXT NOT NULL CHECK(state IN (
                'SUBMITTING','PRE_SEND_FAILURE','DEFINITIVE_REJECTION',
                'UNKNOWN_SUBMISSION','VERIFIED_SUCCESS','FINALIZED',
                'CONFIRMED_PRESENT','CONFIRMED_ABSENT'
              )),
              recovery_payload_json TEXT NOT NULL CHECK(recovery_payload_json != ''),
              planned_cloids_json TEXT NOT NULL CHECK(planned_cloids_json != ''),
              created_ts TEXT NOT NULL CHECK(created_ts != ''),
              updated_ts TEXT NOT NULL CHECK(updated_ts != ''),
              reason_code TEXT NOT NULL CHECK(
                length(reason_code) BETWEEN 1 AND 96
                AND reason_code NOT GLOB '*[^A-Z0-9_:.-]*'
              ),
              absence_count INTEGER NOT NULL DEFAULT 0 CHECK(absence_count >= 0),
              absence_first_ts TEXT,
              absence_last_ts TEXT,
              verdict_ts TEXT
            )""")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS submission_recovery_evidence (
              evidence_id INTEGER PRIMARY KEY,
              attempt_id TEXT NOT NULL REFERENCES submission_attempts(attempt_id),
              cycle_no INTEGER NOT NULL CHECK(cycle_no > 0),
              observed_ts TEXT NOT NULL CHECK(observed_ts != ''),
              verdict TEXT NOT NULL CHECK(verdict IN (
                'PRESENT','ABSENT_COMPLETE','INCOMPLETE','CONFLICTING'
              )),
              evidence_json TEXT NOT NULL CHECK(evidence_json != ''),
              UNIQUE(attempt_id, cycle_no)
            )""")
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_submission_attempt_state "
            "ON submission_attempts(state)")
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_submission_evidence_attempt "
            "ON submission_recovery_evidence(attempt_id, cycle_no)")
        self.conn.execute("""
            CREATE TRIGGER IF NOT EXISTS trg_submission_attempt_transition
            BEFORE UPDATE OF state ON submission_attempts
            WHEN NOT (
              (OLD.state = 'SUBMITTING' AND NEW.state IN (
                'PRE_SEND_FAILURE','DEFINITIVE_REJECTION',
                'UNKNOWN_SUBMISSION','VERIFIED_SUCCESS'
              ))
              OR (OLD.state = 'VERIFIED_SUCCESS' AND NEW.state = 'FINALIZED')
              OR (OLD.state = 'UNKNOWN_SUBMISSION' AND NEW.state IN (
                'CONFIRMED_PRESENT','CONFIRMED_ABSENT'
              ))
            )
            BEGIN
              SELECT RAISE(ABORT, 'SUBMISSION_ATTEMPT_TRANSITION_DENIED');
            END""")
        self.conn.execute("""
            CREATE TRIGGER IF NOT EXISTS trg_submission_attempt_core_immutable
            BEFORE UPDATE OF attempt_id, intent_id, request_id, origin_run_id,
              origin_decision_uid, recovery_payload_json, planned_cloids_json,
              created_ts
            ON submission_attempts
            BEGIN
              SELECT RAISE(ABORT, 'SUBMISSION_ATTEMPT_CORE_IMMUTABLE');
            END""")
        self.conn.execute("""
            CREATE TRIGGER IF NOT EXISTS trg_submission_attempt_no_delete
            BEFORE DELETE ON submission_attempts
            BEGIN
              SELECT RAISE(ABORT, 'SUBMISSION_ATTEMPT_DELETE_DENIED');
            END""")
        self.conn.execute("""
            CREATE TRIGGER IF NOT EXISTS trg_submission_evidence_no_update
            BEFORE UPDATE ON submission_recovery_evidence
            BEGIN
              SELECT RAISE(ABORT, 'SUBMISSION_EVIDENCE_APPEND_ONLY');
            END""")
        self.conn.execute("""
            CREATE TRIGGER IF NOT EXISTS trg_submission_evidence_no_delete
            BEFORE DELETE ON submission_recovery_evidence
            BEGIN
              SELECT RAISE(ABORT, 'SUBMISSION_EVIDENCE_APPEND_ONLY');
            END""")

    # ------------------------------------------------------------------
    # TS-P1-004 schema v5 (additive partial-fill recovery ledger)
    # ------------------------------------------------------------------

    def _initialize_v5_idempotent(self) -> None:
        """Re-open v5 only when its complete safety topology is canonical."""
        self._validate_partial_fill_schema_v5()

    def _create_partial_fill_tables_v5(self) -> None:
        """Purely additive DDL. Callable inside an open transaction.

        Types are fitted to the real v4 schema: ``trades.trade_id`` is INTEGER
        and orders are keyed by their durable ``cloid``, so both foreign keys
        below reference real columns rather than the illustrative TEXT
        ``trade_id`` of the plan sketch.
        """
        states = ",".join(
            f"'{state.value}'" for state in sorted(PartialProtectionState, key=lambda s: s.value)
        )
        kinds = ",".join(
            f"'{kind.value}'" for kind in sorted(PartialActionKind, key=lambda k: k.value)
        )
        statuses = ",".join(
            f"'{status.value}'"
            for status in sorted(ActionRecordStatus, key=lambda s: s.value)
        )
        terminal = ",".join(
            f"'{state.value}'"
            for state in sorted(PARTIAL_TERMINAL_STATES, key=lambda s: s.value)
        )
        self.conn.execute(f"""
            CREATE TABLE IF NOT EXISTS partial_fill_recoveries (
              recovery_id TEXT PRIMARY KEY
                CHECK(length(recovery_id) = 71 AND substr(recovery_id, 1, 7) = 'pfr-v1:'
                      AND NOT substr(recovery_id, 8) GLOB '*[^0-9a-f]*'),
              run_id TEXT NOT NULL CHECK(run_id != ''),
              symbol TEXT NOT NULL CHECK(symbol != ''),
              trade_id INTEGER NOT NULL REFERENCES trades(trade_id),
              entry_cloid TEXT NOT NULL REFERENCES orders(cloid),
              entry_decision_uid TEXT NOT NULL CHECK(entry_decision_uid != ''),
              entry_request_id TEXT NOT NULL CHECK(entry_request_id != ''),
              generation INTEGER NOT NULL CHECK(generation >= 0),
              flatten_seq INTEGER NOT NULL DEFAULT 0 CHECK(flatten_seq >= 0),
              state TEXT NOT NULL CHECK(state IN ({states})),
              provenance TEXT NOT NULL,
              size_decimals INTEGER CHECK(size_decimals IS NULL OR
                                          (size_decimals >= 0 AND size_decimals <= 18)),
              ordered_lots INTEGER CHECK(ordered_lots IS NULL OR ordered_lots > 0),
              filled_lots INTEGER CHECK(filled_lots IS NULL OR filled_lots >= 0),
              position_lots INTEGER CHECK(position_lots IS NULL OR position_lots >= 0),
              first_observed_ts TEXT NOT NULL CHECK(first_observed_ts != ''),
              protect_deadline_ts TEXT NOT NULL CHECK(protect_deadline_ts != ''),
              flatten_deadline_ts TEXT,
              reason_code TEXT NOT NULL CHECK(
                length(reason_code) BETWEEN 1 AND 96
                AND reason_code NOT GLOB '*[^A-Z0-9_:.-]*'
              ),
              created_ts TEXT NOT NULL CHECK(created_ts != ''),
              updated_ts TEXT NOT NULL CHECK(updated_ts != ''),
              UNIQUE(trade_id, entry_cloid, generation)
            )""")
        # At most one non-terminal recovery per symbol: the durable expression
        # of "one writer per symbol".
        self.conn.execute(f"""
            CREATE UNIQUE INDEX IF NOT EXISTS ux_partial_recovery_active_symbol
            ON partial_fill_recoveries(symbol)
            WHERE state NOT IN ({terminal})""")
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_partial_recovery_state "
            "ON partial_fill_recoveries(state)")
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_partial_recovery_trade "
            "ON partial_fill_recoveries(trade_id, generation)")
        self.conn.execute(f"""
            CREATE TABLE IF NOT EXISTS partial_fill_actions (
              action_id TEXT PRIMARY KEY
                CHECK(length(action_id) = 71 AND substr(action_id, 1, 7) = 'pfa-v1:'
                      AND NOT substr(action_id, 8) GLOB '*[^0-9a-f]*'),
              recovery_id TEXT NOT NULL
                REFERENCES partial_fill_recoveries(recovery_id),
              trade_id INTEGER NOT NULL REFERENCES trades(trade_id),
              kind TEXT NOT NULL CHECK(kind IN ({kinds})),
              generation INTEGER CHECK(generation IS NULL OR generation >= 0),
              flatten_seq INTEGER CHECK(flatten_seq IS NULL OR flatten_seq >= 0),
              qty_lots INTEGER CHECK(qty_lots IS NULL OR qty_lots > 0),
              target_cloid TEXT NOT NULL CHECK(target_cloid != ''),
              reserved_ts TEXT NOT NULL CHECK(reserved_ts != ''),
              UNIQUE(target_cloid, kind)
            )""")
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_partial_action_recovery "
            "ON partial_fill_actions(recovery_id, kind)")
        self.conn.execute("""
            CREATE TRIGGER IF NOT EXISTS trg_partial_action_no_update
            BEFORE UPDATE ON partial_fill_actions
            BEGIN
              SELECT RAISE(ABORT, 'PARTIAL_ACTION_IMMUTABLE');
            END""")
        self.conn.execute("""
            CREATE TRIGGER IF NOT EXISTS trg_partial_action_no_delete
            BEFORE DELETE ON partial_fill_actions
            BEGIN
              SELECT RAISE(ABORT, 'PARTIAL_ACTION_IMMUTABLE');
            END""")
        self.conn.execute(f"""
            CREATE TABLE IF NOT EXISTS partial_fill_action_events (
              event_id INTEGER PRIMARY KEY AUTOINCREMENT,
              action_id TEXT NOT NULL REFERENCES partial_fill_actions(action_id),
              recovery_id TEXT NOT NULL
                REFERENCES partial_fill_recoveries(recovery_id),
              seq INTEGER NOT NULL CHECK(seq > 0),
              status TEXT NOT NULL CHECK(status IN ({statuses})),
              evidence_source TEXT NOT NULL CHECK(evidence_source != ''),
              reason_code TEXT NOT NULL CHECK(
                length(reason_code) BETWEEN 1 AND 96
                AND reason_code NOT GLOB '*[^A-Z0-9_:.-]*'
              ),
              evidence_json TEXT NOT NULL CHECK(evidence_json != ''),
              observed_ts TEXT NOT NULL CHECK(observed_ts != ''),
              UNIQUE(action_id, seq)
            )""")
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_partial_action_event_action "
            "ON partial_fill_action_events(action_id, seq)")
        self.conn.execute("""
            CREATE TRIGGER IF NOT EXISTS trg_partial_action_event_no_update
            BEFORE UPDATE ON partial_fill_action_events
            BEGIN
              SELECT RAISE(ABORT, 'PARTIAL_ACTION_EVENT_APPEND_ONLY');
            END""")
        self.conn.execute("""
            CREATE TRIGGER IF NOT EXISTS trg_partial_action_event_no_delete
            BEFORE DELETE ON partial_fill_action_events
            BEGIN
              SELECT RAISE(ABORT, 'PARTIAL_ACTION_EVENT_APPEND_ONLY');
            END""")

    def _evidence_census(self) -> dict[str, int]:
        """Row counts of every pre-existing evidence table (migration guard)."""
        census: dict[str, int] = {}
        for table in _PARTIAL_EVIDENCE_TABLES:
            row = self.conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name = ?",
                (table,),
            ).fetchone()
            if row is None:
                continue
            count = self.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
            census[table] = int(count[0]) if count else 0
        return census

    def _validate_partial_fill_schema_v5(self) -> None:
        """Compare every v5 table/index/trigger against a canonical schema.

        Exact normalized SQL covers columns, affinities, NOT NULL/default/PK/
        UNIQUE/FK/CHECK clauses, partial-index predicates, and trigger bodies.
        PRAGMA signatures independently cover the materialized topology and
        foreign-key integrity on reopen.
        """
        tables = {
            "partial_fill_recoveries",
            "partial_fill_actions",
            "partial_fill_action_events",
        }

        reference = Store(Path(":memory:"))
        reference._conn = sqlite3.connect(":memory:")
        reference._conn.row_factory = sqlite3.Row
        reference._conn.execute("PRAGMA foreign_keys=ON")
        reference._conn.execute(
            "CREATE TABLE trades (trade_id INTEGER PRIMARY KEY)"
        )
        reference._conn.execute("CREATE TABLE orders (cloid TEXT PRIMARY KEY)")
        Store._create_partial_fill_tables_v5(reference)

        def normalized_sql(value: object) -> str:
            return " ".join(str(value or "").split()).upper()

        def object_signature(conn: sqlite3.Connection) -> dict[tuple[str, str], tuple[str, str]]:
            rows = conn.execute(
                "SELECT type, name, tbl_name, sql FROM sqlite_master "
                "WHERE sql IS NOT NULL"
            ).fetchall()
            return {
                (str(row["type"]), str(row["name"])): (
                    str(row["tbl_name"]),
                    normalized_sql(row["sql"]),
                )
                for row in rows
                if str(row["tbl_name"]) in tables
            }

        def pragma_signature(
            conn: sqlite3.Connection,
        ) -> dict[str, dict[str, tuple[tuple[object, ...], ...]]]:
            signature: dict[str, dict[str, tuple[tuple[object, ...], ...]]] = {}
            for table in sorted(tables):
                columns = tuple(
                    tuple(row)
                    for row in conn.execute(
                        f"PRAGMA table_xinfo('{table}')"
                    ).fetchall()
                )
                foreign_keys = tuple(
                    sorted(
                        (tuple(row) for row in conn.execute(
                            f"PRAGMA foreign_key_list('{table}')"
                        ).fetchall()),
                        key=repr,
                    )
                )
                indexes = []
                for row in conn.execute(
                    f"PRAGMA index_list('{table}')"
                ).fetchall():
                    index_name = str(row["name"])
                    index_columns = tuple(
                        tuple(index_row)
                        for index_row in conn.execute(
                            f"PRAGMA index_xinfo('{index_name}')"
                        ).fetchall()
                    )
                    indexes.append((tuple(row)[1:], index_columns))
                signature[table] = {
                    "columns": columns,
                    "foreign_keys": foreign_keys,
                    "indexes": tuple(sorted(indexes, key=repr)),
                }
            return signature

        try:
            expected_objects = object_signature(reference._conn)
            actual_objects = object_signature(self.conn)
            if actual_objects != expected_objects:
                missing = sorted(set(expected_objects) - set(actual_objects))
                extra = sorted(set(actual_objects) - set(expected_objects))
                changed = sorted(
                    key
                    for key in set(expected_objects) & set(actual_objects)
                    if expected_objects[key] != actual_objects[key]
                )
                raise MigrationError(
                    "v5 topology mismatch "
                    f"missing={missing} extra={extra} changed={changed}"
                )
            if pragma_signature(self.conn) != pragma_signature(reference._conn):
                raise MigrationError("v5 PRAGMA topology mismatch")
            violations = self.conn.execute("PRAGMA foreign_key_check").fetchall()
            if violations:
                raise MigrationError("v5 foreign-key integrity check failed")
        finally:
            reference._conn.close()
            reference._conn = None

    def _migrate_v4_to_v5(self) -> None:
        """Additive v4→v5 upgrade in one rollback-clean transaction.

        DDL, evidence census, validation, and the ``meta.schema_version`` bump
        all live in a single ``BEGIN IMMEDIATE``. SQLite DDL is transactional,
        so any failure rolls the whole thing back: the database stays a valid,
        reopenable v4 with every pre-existing row untouched. There is no
        speculative backfill — recovery rows are only created later, by
        ``OrderManager`` startup reconciliation, once ownership is proven.
        """
        if self.get_meta("schema_version") == str(SCHEMA_VERSION_PARTIAL_FILL):
            self._initialize_v5_idempotent()
            return
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            if self.get_meta("schema_version") != str(SCHEMA_VERSION_BASELINE):
                raise MigrationError("v4-to-v5 requires schema_version=4")
            before = self._evidence_census()
            self._create_partial_fill_tables_v5()
            self._validate_partial_fill_schema_v5()
            after = self._evidence_census()
            if before != after:
                raise MigrationError(
                    "v4-to-v5 must not alter existing evidence rows"
                )
            cursor = self.conn.execute(
                "UPDATE meta SET value = ? "
                "WHERE key = 'schema_version' AND value = ?",
                (str(SCHEMA_VERSION_PARTIAL_FILL), str(SCHEMA_VERSION_BASELINE)),
            )
            if cursor.rowcount != 1:
                raise MigrationError("v4-to-v5 version update rowcount mismatch")
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

    def _migrate_v3_to_v4(self) -> None:
        """Add the v4 ledger in one rollback-clean BEGIN IMMEDIATE transaction."""
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            if self.get_meta("schema_version") != "3":
                raise MigrationError("v3-to-v4 requires schema_version=3")
            self._create_submission_ledger_v4()
            cursor = self.conn.execute(
                "UPDATE meta SET value = '4' "
                "WHERE key = 'schema_version' AND value = '3'"
            )
            if cursor.rowcount != 1:
                raise MigrationError("v3-to-v4 version update rowcount mismatch")
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

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
    # TS-P1-003 submission-attempt ledger
    # ------------------------------------------------------------------

    @staticmethod
    def _safe_reason_code(value: str) -> str:
        code = str(value).strip().upper()
        if (
            not code
            or len(code) > 96
            or any(ch not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_:-." for ch in code)
        ):
            raise ValueError("reason_code must be a short structured code")
        return code

    @staticmethod
    def _canonical_planned_cloids(planned_cloids: Mapping[str, str]) -> dict[str, str]:
        if not isinstance(planned_cloids, Mapping) or not planned_cloids:
            raise ValueError("planned_cloids must be a non-empty mapping")
        normalized: dict[str, str] = {}
        for raw_role, raw_cloid in planned_cloids.items():
            role = str(raw_role).strip().upper()
            cloid = Store._safe_cloid(raw_cloid)
            if role not in {"ENTRY", "SL", "TP"}:
                raise ValueError("planned_cloids contains an invalid role or cloid")
            if role in normalized:
                raise ValueError("planned_cloids contains a duplicate role")
            normalized[role] = cloid
        if len(set(normalized.values())) != len(normalized):
            raise ValueError("planned_cloids contains duplicate cloids")
        return dict(sorted(normalized.items()))

    @staticmethod
    def _safe_cloid(value: object) -> str:
        cloid = str(value).strip()
        if (
            not cloid
            or len(cloid) > 256
            or any(
                ch not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_:-."
                for ch in cloid
            )
        ):
            raise ValueError("cloid must be a short structured identifier")
        return cloid

    @staticmethod
    def _canonical_recovery_payload(payload: Mapping[str, Any]) -> str:
        expected = {
            "version",
            "symbol",
            "direction",
            "signal_ts",
            "ref_price_hex",
            "qty_hex",
            "entry_type",
            "limit_price_hex",
            "stop_loss_hex",
            "take_profit_hex",
            "leverage",
        }
        if not isinstance(payload, Mapping) or set(payload) != expected:
            raise ValueError("recovery payload fields do not match the canonical contract")
        if payload.get("version") != _RECOVERY_PAYLOAD_VERSION:
            raise ValueError("recovery payload version mismatch")
        if not isinstance(payload.get("leverage"), int) or isinstance(payload.get("leverage"), bool):
            raise ValueError("recovery payload leverage must be an integer")
        for key in expected - {"limit_price_hex", "take_profit_hex", "leverage"}:
            if not isinstance(payload.get(key), str) or not str(payload[key]).strip():
                raise ValueError(f"recovery payload field {key} is invalid")
        for key in {"limit_price_hex", "take_profit_hex"}:
            if payload.get(key) is not None and not isinstance(payload.get(key), str):
                raise ValueError(f"recovery payload field {key} is invalid")
        return _canonical_json(dict(payload))

    @classmethod
    def _canonical_evidence_payload(cls, payload: Mapping[str, Any]) -> str:
        expected = {
            "request_id",
            "planned_cloids",
            "direct_lookup",
            "open_orders",
            "historical_orders",
            "fills",
            "position",
        }
        if not isinstance(payload, Mapping) or set(payload) != expected:
            raise ValueError("recovery evidence fields do not match the typed contract")
        planned = cls._canonical_planned_cloids(payload["planned_cloids"])
        if not isinstance(payload["direct_lookup"], Mapping):
            raise ValueError("direct_lookup evidence must be a mapping")
        if set(map(str, payload["direct_lookup"])) != set(planned.values()):
            raise ValueError("direct_lookup evidence does not exactly cover planned cloids")

        def validate_query(query: Any) -> None:
            if not isinstance(query, Mapping) or set(query) != {
                "status", "found_cloids", "reason_code"
            }:
                raise ValueError("query evidence fields do not match the typed contract")
            if str(query["status"]) not in _EVIDENCE_STATUSES:
                raise ValueError("query evidence status is invalid")
            if not isinstance(query["found_cloids"], (list, tuple)):
                raise ValueError("query evidence found_cloids must be a sequence")
            found_cloids = [
                cls._safe_cloid(value) for value in query["found_cloids"]
            ]
            if len(set(found_cloids)) != len(found_cloids):
                raise ValueError("query evidence contains duplicate cloids")
            if set(found_cloids) - set(planned.values()):
                raise ValueError("recovery evidence contains an unplanned cloid")
            cls._safe_reason_code(str(query["reason_code"]))

        for query in payload["direct_lookup"].values():
            validate_query(query)
        for name in ("open_orders", "historical_orders", "fills", "position"):
            validate_query(payload[name])
        return _canonical_json(dict(payload))

    def reserve_submission(
        self,
        *,
        intent_id: str,
        intent_preimage: str,
        intent_version: str,
        request_id: str,
        request_preimage: str,
        request_version: str,
        cloid_seed: str,
        origin_run_id: str,
        origin_decision_uid: str,
        recovery_payload: Mapping[str, Any],
        planned_cloids: Mapping[str, str],
    ) -> tuple[Literal["RESERVED", "BLOCKED"], str]:
        """Atomically reserve identity and the immutable SUBMITTING attempt."""
        attempt_id = compute_submission_attempt_id(request_id)
        canonical_payload = self._canonical_recovery_payload(recovery_payload)
        canonical_cloids = self._canonical_planned_cloids(planned_cloids)
        payload_has_tp = recovery_payload["take_profit_hex"] is not None
        expected_roles = {"ENTRY", "SL", "TP"} if payload_has_tp else {"ENTRY", "SL"}
        if set(canonical_cloids) != expected_roles:
            raise ValueError("planned_cloids do not exactly cover the planned bracket roles")

        self.conn.execute("BEGIN IMMEDIATE")
        try:
            result = self.reserve_identity(
                intent_id=intent_id,
                intent_preimage=intent_preimage,
                intent_version=intent_version,
                request_id=request_id,
                request_preimage=request_preimage,
                request_version=request_version,
                cloid_seed=cloid_seed,
                origin_run_id=origin_run_id,
                origin_decision_uid=origin_decision_uid,
            )
            if result == "RESERVED":
                now = _to_iso(self._clock())
                self.conn.execute(
                    """INSERT INTO submission_attempts(
                         attempt_id, intent_id, request_id,
                         origin_run_id, origin_decision_uid, state,
                         recovery_payload_json, planned_cloids_json,
                         created_ts, updated_ts, reason_code
                       ) VALUES (?, ?, ?, ?, ?, 'SUBMITTING', ?, ?, ?, ?, ?)""",
                    (
                        attempt_id,
                        intent_id,
                        request_id,
                        origin_run_id,
                        origin_decision_uid,
                        canonical_payload,
                        _canonical_json(canonical_cloids),
                        now,
                        now,
                        "SUBMISSION_RESERVED",
                    ),
                )
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        return result, attempt_id

    def get_submission_attempt(self, attempt_id: str) -> dict[str, Any] | None:
        row = self.conn.execute(
            "SELECT * FROM submission_attempts WHERE attempt_id = ?", (attempt_id,)
        ).fetchone()
        if row is None:
            return None
        result = dict(row)
        result["planned_cloids"] = json.loads(result["planned_cloids_json"])
        result["recovery_payload"] = json.loads(result["recovery_payload_json"])
        return result

    def get_submission_attempt_by_request(self, request_id: str) -> dict[str, Any] | None:
        row = self.conn.execute(
            "SELECT attempt_id FROM submission_attempts WHERE request_id = ?",
            (request_id,),
        ).fetchone()
        return None if row is None else self.get_submission_attempt(str(row["attempt_id"]))

    def get_active_submission_attempts(self) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            """SELECT attempt_id FROM submission_attempts
               WHERE state IN ('SUBMITTING','UNKNOWN_SUBMISSION')
               ORDER BY created_ts, attempt_id"""
        ).fetchall()
        return [
            attempt
            for row in rows
            if (attempt := self.get_submission_attempt(str(row["attempt_id"]))) is not None
        ]

    def get_quarantined_submission_attempts(self) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            """SELECT attempt_id FROM submission_attempts
               WHERE state IN ('SUBMITTING','UNKNOWN_SUBMISSION','CONFIRMED_PRESENT')
               ORDER BY created_ts, attempt_id"""
        ).fetchall()
        return [
            attempt
            for row in rows
            if (attempt := self.get_submission_attempt(str(row["attempt_id"]))) is not None
        ]

    def submission_quarantine_count(self) -> int:
        placeholders = ",".join("?" for _ in _QUARANTINE_STATES)
        row = self.conn.execute(
            f"SELECT COUNT(*) FROM submission_attempts WHERE state IN ({placeholders})",
            tuple(sorted(_QUARANTINE_STATES)),
        ).fetchone()
        return int(row[0]) if row else 0

    def has_submission_quarantine(self) -> bool:
        return self.submission_quarantine_count() > 0

    def _transition_attempt_in_tx(
        self, attempt_id: str, target_state: str, reason_code: str
    ) -> None:
        row = self.conn.execute(
            "SELECT state FROM submission_attempts WHERE attempt_id = ?",
            (attempt_id,),
        ).fetchone()
        if row is None:
            raise IdentityCollisionError(
                "SUBMISSION_ATTEMPT_NOT_FOUND", f"attempt_id={attempt_id}"
            )
        current = str(row["state"])
        if target_state not in _ATTEMPT_TRANSITIONS.get(current, frozenset()):
            raise IdentityCollisionError(
                "SUBMISSION_TRANSITION_DENIED",
                f"attempt_id={attempt_id} current={current} target={target_state}",
            )
        now = _to_iso(self._clock())
        cursor = self.conn.execute(
            """UPDATE submission_attempts
               SET state = ?, updated_ts = ?, reason_code = ?,
                   verdict_ts = CASE
                     WHEN ? IN ('CONFIRMED_PRESENT','CONFIRMED_ABSENT') THEN ?
                     ELSE verdict_ts
                   END
               WHERE attempt_id = ? AND state = ?""",
            (
                target_state,
                now,
                self._safe_reason_code(reason_code),
                target_state,
                now,
                attempt_id,
                current,
            ),
        )
        if cursor.rowcount != 1:
            raise IdentityCollisionError(
                "SUBMISSION_TRANSITION_ROWCOUNT",
                f"attempt_id={attempt_id} rowcount={cursor.rowcount}",
            )

    def transition_submission_attempt(
        self, attempt_id: str, target_state: str, reason_code: str
    ) -> None:
        """Forward-only transition; callers never supply or authorize from_state."""
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            self._transition_attempt_in_tx(attempt_id, target_state, reason_code)
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

    def mark_submission_unknown(self, attempt_id: str, reason_code: str) -> None:
        """Persist quarantine; an already-unknown attempt remains unchanged."""
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            row = self.conn.execute(
                "SELECT state FROM submission_attempts WHERE attempt_id = ?",
                (attempt_id,),
            ).fetchone()
            if row is None:
                raise IdentityCollisionError(
                    "SUBMISSION_ATTEMPT_NOT_FOUND", f"attempt_id={attempt_id}"
                )
            if str(row["state"]) == "SUBMITTING":
                self._transition_attempt_in_tx(
                    attempt_id, "UNKNOWN_SUBMISSION", reason_code
                )
            elif str(row["state"]) != "UNKNOWN_SUBMISSION":
                raise IdentityCollisionError(
                    "SUBMISSION_TRANSITION_DENIED",
                    f"attempt_id={attempt_id} current={row['state']} target=UNKNOWN_SUBMISSION",
                )
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

    def record_recovery_cycle(
        self,
        *,
        attempt_id: str,
        request_id: str,
        planned_cloids: Mapping[str, str],
        observed_ts: datetime,
        verdict: Literal["PRESENT", "ABSENT_COMPLETE", "INCOMPLETE", "CONFLICTING"],
        evidence_payload: Mapping[str, Any],
    ) -> str:
        """Append evidence and apply its recovery state/counter change atomically."""
        observed = _to_iso(observed_ts)
        if observed is None:
            raise ValueError("observed_ts is required")
        canonical_cloids = self._canonical_planned_cloids(planned_cloids)
        canonical_evidence = self._canonical_evidence_payload(evidence_payload)
        if evidence_payload["request_id"] != request_id:
            raise ValueError("recovery evidence request_id linkage mismatch")
        if self._canonical_planned_cloids(evidence_payload["planned_cloids"]) != canonical_cloids:
            raise ValueError("recovery evidence cloid-map linkage mismatch")
        if verdict not in {"PRESENT", "ABSENT_COMPLETE", "INCOMPLETE", "CONFLICTING"}:
            raise ValueError("recovery verdict is invalid")

        self.conn.execute("BEGIN IMMEDIATE")
        try:
            row = self.conn.execute(
                """SELECT request_id, state, planned_cloids_json, absence_count,
                          absence_first_ts, absence_last_ts
                   FROM submission_attempts WHERE attempt_id = ?""",
                (attempt_id,),
            ).fetchone()
            if row is None:
                raise IdentityCollisionError(
                    "SUBMISSION_ATTEMPT_NOT_FOUND", f"attempt_id={attempt_id}"
                )
            if str(row["request_id"]) != request_id:
                raise ValueError("stored recovery request_id linkage mismatch")
            if json.loads(str(row["planned_cloids_json"])) != canonical_cloids:
                raise ValueError("stored recovery cloid-map linkage mismatch")
            state = str(row["state"])
            if state not in {"SUBMITTING", "UNKNOWN_SUBMISSION"}:
                raise IdentityCollisionError(
                    "SUBMISSION_RECOVERY_TERMINAL",
                    f"attempt_id={attempt_id} state={state}",
                )
            cycle_row = self.conn.execute(
                """SELECT COALESCE(MAX(cycle_no), 0) + 1
                   FROM submission_recovery_evidence WHERE attempt_id = ?""",
                (attempt_id,),
            ).fetchone()
            cycle_no = int(cycle_row[0]) if cycle_row else 1
            self.conn.execute(
                """INSERT INTO submission_recovery_evidence(
                     attempt_id, cycle_no, observed_ts, verdict, evidence_json
                   ) VALUES (?, ?, ?, ?, ?)""",
                (attempt_id, cycle_no, observed, verdict, canonical_evidence),
            )

            if state == "SUBMITTING":
                self._transition_attempt_in_tx(
                    attempt_id, "UNKNOWN_SUBMISSION", "RECOVERY_OBSERVED"
                )
                state = "UNKNOWN_SUBMISSION"

            if verdict == "PRESENT":
                self.conn.execute(
                    """UPDATE submission_attempts
                       SET absence_count = 0, absence_first_ts = NULL,
                           absence_last_ts = NULL
                       WHERE attempt_id = ?""",
                    (attempt_id,),
                )
                self._transition_attempt_in_tx(
                    attempt_id, "CONFIRMED_PRESENT", "RECOVERY_PRESENT"
                )
                state = "CONFIRMED_PRESENT"
            elif verdict == "ABSENT_COMPLETE":
                count = int(row["absence_count"])
                first = row["absence_first_ts"]
                last = row["absence_last_ts"]
                if last is not None and datetime.fromisoformat(observed) <= datetime.fromisoformat(str(last)):
                    count = 0
                    first = None
                count += 1
                first = str(first) if first is not None else observed
                self.conn.execute(
                    """UPDATE submission_attempts
                       SET absence_count = ?, absence_first_ts = ?,
                           absence_last_ts = ?, updated_ts = ?
                       WHERE attempt_id = ?""",
                    (count, first, observed, observed, attempt_id),
                )
                span = (
                    datetime.fromisoformat(observed)
                    - datetime.fromisoformat(first)
                ).total_seconds()
                if count >= 3 and span >= 120.0:
                    self._transition_attempt_in_tx(
                        attempt_id, "CONFIRMED_ABSENT", "RECOVERY_ABSENT"
                    )
                    state = "CONFIRMED_ABSENT"
            else:
                self.conn.execute(
                    """UPDATE submission_attempts
                       SET absence_count = 0, absence_first_ts = NULL,
                           absence_last_ts = NULL, updated_ts = ?
                       WHERE attempt_id = ?""",
                    (observed, attempt_id),
                )
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        return state

    def get_submission_evidence(self, attempt_id: str) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            """SELECT * FROM submission_recovery_evidence
               WHERE attempt_id = ? ORDER BY cycle_no""",
            (attempt_id,),
        ).fetchall()
        result: list[dict[str, Any]] = []
        for raw in rows:
            row = dict(raw)
            row["evidence"] = json.loads(row["evidence_json"])
            result.append(row)
        return result

    # ------------------------------------------------------------------
    # TS-P1-004 partial-fill recovery ledger
    #
    # Every mutating call below is a single BEGIN IMMEDIATE transaction and
    # commits *before* the caller performs any broker I/O. This module never
    # performs broker I/O itself.
    # ------------------------------------------------------------------

    def partial_protection_enabled(self) -> bool:
        """True only on a database that carries the v5 recovery ledger."""
        return self.get_meta("schema_version") == str(SCHEMA_VERSION_PARTIAL_FILL)

    def _require_partial_schema(self) -> None:
        if not self.partial_protection_enabled():
            raise PartialRecoveryConflictError(
                "PARTIAL_SCHEMA_UNAVAILABLE",
                "partial-fill recovery requires schema_version=5",
            )

    @staticmethod
    def _partial_row(raw: sqlite3.Row | None) -> dict[str, Any] | None:
        return None if raw is None else dict(raw)

    def get_partial_recovery(self, recovery_id: str) -> dict[str, Any] | None:
        return self._partial_row(
            self.conn.execute(
                "SELECT * FROM partial_fill_recoveries WHERE recovery_id = ?",
                (recovery_id,),
            ).fetchone()
        )

    def active_partial_recovery_for_symbol(self, symbol: str) -> dict[str, Any] | None:
        """The single non-terminal recovery generation for ``symbol``, if any."""
        if not self.partial_protection_enabled():
            return None
        placeholders = ",".join("?" for _ in PARTIAL_TERMINAL_STATES)
        return self._partial_row(
            self.conn.execute(
                f"""SELECT * FROM partial_fill_recoveries
                    WHERE symbol = ? AND state NOT IN ({placeholders})""",
                (symbol, *sorted(state.value for state in PARTIAL_TERMINAL_STATES)),
            ).fetchone()
        )

    def latest_partial_recovery_for_symbol(self, symbol: str) -> dict[str, Any] | None:
        if not self.partial_protection_enabled():
            return None
        return self._partial_row(
            self.conn.execute(
                """SELECT * FROM partial_fill_recoveries
                   WHERE symbol = ? ORDER BY generation DESC, created_ts DESC
                   LIMIT 1""",
                (symbol,),
            ).fetchone()
        )

    def partial_recovery_abort_active(self, symbol: str | None = None) -> bool:
        """Sticky fail-closed latch: any recovery that ended UNPROTECTED_ABORT."""
        if not self.partial_protection_enabled():
            return False
        sql = "SELECT COUNT(*) FROM partial_fill_recoveries WHERE state = ?"
        params: tuple[Any, ...] = (PartialProtectionState.UNPROTECTED_ABORT.value,)
        if symbol is not None:
            sql += " AND symbol = ?"
            params = (*params, symbol)
        row = self.conn.execute(sql, params).fetchone()
        return bool(row and int(row[0]) > 0)

    def partial_recovery_blocks_new_risk(self) -> bool:
        """True while any recovery is non-terminal or any abort is durable."""
        if not self.partial_protection_enabled():
            return False
        placeholders = ",".join("?" for _ in PARTIAL_TERMINAL_STATES)
        row = self.conn.execute(
            f"""SELECT COUNT(*) FROM partial_fill_recoveries
                WHERE state NOT IN ({placeholders}) OR state = ?""",
            (
                *sorted(state.value for state in PARTIAL_TERMINAL_STATES),
                PartialProtectionState.UNPROTECTED_ABORT.value,
            ),
        ).fetchone()
        return bool(row and int(row[0]) > 0)

    def partial_recoveries_awaiting_rearm(self) -> list[dict[str, Any]]:
        """PROTECTED_PARTIAL generations that a human has not yet re-ARMed.

        ``PROTECTED_PARTIAL`` is accepting and terminal for automatic recovery,
        but it never restores ordinary position handling on its own: the row
        stays here until an explicit re-ARM proof archives it.
        """
        if not self.partial_protection_enabled():
            return []
        return self._rows(
            """SELECT * FROM partial_fill_recoveries
               WHERE state = ? AND reason_code != 'REARM_ARCHIVED'
               ORDER BY created_ts, recovery_id""",
            (PartialProtectionState.PROTECTED_PARTIAL.value,),
        )

    def list_partial_recoveries(self) -> list[dict[str, Any]]:
        if not self.partial_protection_enabled():
            return []
        return self._rows(
            "SELECT * FROM partial_fill_recoveries ORDER BY created_ts, recovery_id"
        )

    def open_partial_recovery(
        self,
        *,
        run_id: str,
        symbol: str,
        trade_id: int,
        entry_cloid: str,
        entry_decision_uid: str,
        entry_request_id: str,
        first_observed_ts: datetime | str,
        protect_deadline_ts: datetime | str,
        generation: int = 0,
        size_decimals: int | None = None,
        ordered_lots: int | None = None,
        filled_lots: int | None = None,
        reason_code: str = "PARTIAL_ENTRY_FILL",
    ) -> dict[str, Any]:
        """Persist the first partial observation and its fixed deadline.

        Idempotent by construction: replaying the same trade/entry/generation
        returns the stored row untouched, so neither the first-observation
        timestamp nor the deadline can ever be rewritten by a retry, a
        reconnect, or a restart.
        """
        self._require_partial_schema()
        recovery_id = compute_partial_recovery_id(
            trade_id=int(trade_id), entry_cloid=str(entry_cloid), generation=int(generation)
        )
        observed = _to_iso(first_observed_ts)
        deadline = _to_iso(protect_deadline_ts)
        if not observed or not deadline:
            raise ValueError("first_observed_ts and protect_deadline_ts are required")
        safe_reason = self._safe_reason_code(reason_code)
        now = _to_iso(self._clock())
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            # First detection, canonical order progress, and the new-risk
            # latch are one durable verdict. A crash cannot leave a partial
            # entry recorded without the application being DISARMED.
            entry = self.conn.execute(
                "SELECT qty, filled_qty, status FROM orders WHERE cloid = ?",
                (str(entry_cloid),),
            ).fetchone()
            if entry is None:
                raise sqlite3.IntegrityError(
                    f"partial recovery entry order missing: {entry_cloid}"
                )
            is_partial = (
                ordered_lots is not None
                and filled_lots is not None
                and 0 < int(filled_lots) < int(ordered_lots)
            )
            if is_partial and str(entry["status"]).upper() not in {
                "FILLED",
                "CANCELED",
                "CANCELLED",
                "CANCELLED_BY_ENGINE",
                "REJECTED",
                "EXPIRED",
            }:
                self.conn.execute(
                    "UPDATE orders SET status = 'PARTIALLY_FILLED' WHERE cloid = ?",
                    (str(entry_cloid),),
                )
            self.conn.execute(
                "INSERT OR REPLACE INTO meta(key, value) VALUES ('app_state', 'DISARMED')"
            )
            existing = self.get_partial_recovery(recovery_id)
            if existing is not None:
                self.conn.commit()
                return existing
            active = self.active_partial_recovery_for_symbol(symbol)
            if active is not None and str(active["recovery_id"]) != recovery_id:
                raise PartialRecoveryConflictError(
                    "PARTIAL_RECOVERY_SYMBOL_BUSY",
                    f"symbol={symbol} active={active['recovery_id']}",
                )
            self.conn.execute(
                """INSERT INTO partial_fill_recoveries(
                     recovery_id, run_id, symbol, trade_id, entry_cloid,
                     entry_decision_uid, entry_request_id, generation, flatten_seq,
                     state, provenance, size_decimals, ordered_lots, filled_lots,
                     position_lots, first_observed_ts, protect_deadline_ts,
                     flatten_deadline_ts, reason_code, created_ts, updated_ts
                   ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?, ?, ?, ?, NULL,
                             ?, ?, NULL, ?, ?, ?)""",
                (
                    recovery_id,
                    str(run_id),
                    str(symbol),
                    int(trade_id),
                    str(entry_cloid),
                    str(entry_decision_uid),
                    str(entry_request_id),
                    int(generation),
                    PartialProtectionState.PARTIAL_DETECTED.value,
                    "UNVERIFIED",
                    None if size_decimals is None else int(size_decimals),
                    None if ordered_lots is None else int(ordered_lots),
                    None if filled_lots is None else int(filled_lots),
                    observed,
                    deadline,
                    safe_reason,
                    now,
                    now,
                ),
            )
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        row = self.get_partial_recovery(recovery_id)
        if row is None:  # pragma: no cover - defensive
            raise PartialRecoveryConflictError(
                "PARTIAL_RECOVERY_MISSING", f"recovery_id={recovery_id}"
            )
        return row

    _PARTIAL_MUTABLE_FIELDS = frozenset({
        "provenance",
        "size_decimals",
        "ordered_lots",
        "filled_lots",
        "position_lots",
        "flatten_deadline_ts",
        "reason_code",
    })

    def _transition_partial_in_tx(
        self,
        recovery_id: str,
        expected: str,
        target: str,
        reason_code: str,
        fields: Mapping[str, Any],
    ) -> None:
        row = self.conn.execute(
            "SELECT state, flatten_deadline_ts FROM partial_fill_recoveries "
            "WHERE recovery_id = ?",
            (recovery_id,),
        ).fetchone()
        if row is None:
            raise PartialRecoveryConflictError(
                "PARTIAL_RECOVERY_NOT_FOUND", f"recovery_id={recovery_id}"
            )
        current = PartialProtectionState(str(row["state"]))
        if current is not PartialProtectionState(str(expected)):
            raise PartialRecoveryConflictError(
                "PARTIAL_TRANSITION_CAS_FAILED",
                f"recovery_id={recovery_id} current={current.value} expected={expected}",
            )
        target_state = PartialProtectionState(str(target))
        if target_state not in PARTIAL_STATE_TRANSITIONS.get(current, frozenset()):
            raise PartialRecoveryConflictError(
                "PARTIAL_TRANSITION_DENIED",
                f"recovery_id={recovery_id} {current.value} -> {target_state.value}",
            )
        assignments = ["state = ?", "reason_code = ?", "updated_ts = ?"]
        params: list[Any] = [
            target_state.value,
            self._safe_reason_code(reason_code),
            _to_iso(self._clock()),
        ]
        for key, value in fields.items():
            if key not in self._PARTIAL_MUTABLE_FIELDS:
                raise PartialRecoveryConflictError(
                    "PARTIAL_FIELD_IMMUTABLE", f"field={key}"
                )
            if key == "flatten_deadline_ts":
                # Non-resetting: the 5s budget is written exactly once.
                if row["flatten_deadline_ts"] is not None:
                    continue
                value = _to_iso(value)
            assignments.append(f"{key} = ?")
            params.append(value)
        params.extend([recovery_id, current.value])
        cursor = self.conn.execute(
            f"""UPDATE partial_fill_recoveries SET {', '.join(assignments)}
                WHERE recovery_id = ? AND state = ?""",
            tuple(params),
        )
        if cursor.rowcount != 1:
            raise PartialRecoveryConflictError(
                "PARTIAL_TRANSITION_ROWCOUNT",
                f"recovery_id={recovery_id} rowcount={cursor.rowcount}",
            )

    def transition_partial_recovery(
        self,
        recovery_id: str,
        *,
        expected: str,
        target: str,
        reason_code: str,
        **fields: Any,
    ) -> dict[str, Any]:
        """Compare-and-set the recovery state; refuses illegal/raced targets."""
        self._require_partial_schema()
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            self._transition_partial_in_tx(
                recovery_id, expected, target, reason_code, fields
            )
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        row = self.get_partial_recovery(recovery_id)
        if row is None:  # pragma: no cover - defensive
            raise PartialRecoveryConflictError(
                "PARTIAL_RECOVERY_MISSING", f"recovery_id={recovery_id}"
            )
        return row

    def open_partial_generation(
        self,
        *,
        recovery_id: str,
        reason_code: str,
        position_lots: int | None = None,
        filled_lots: int | None = None,
    ) -> dict[str, Any]:
        """Late-fill re-entry: recompute quantities inside the same row.

        The generation counter advances so newly reserved INSTALL_STOP/FLATTEN
        identities are distinct, while the fixed deadline, the first-observed
        timestamp, and every unresolved CANCEL_ENTRY context are preserved.
        """
        self._require_partial_schema()
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            row = self.conn.execute(
                "SELECT state, generation FROM partial_fill_recoveries "
                "WHERE recovery_id = ?",
                (recovery_id,),
            ).fetchone()
            if row is None:
                raise PartialRecoveryConflictError(
                    "PARTIAL_RECOVERY_NOT_FOUND", f"recovery_id={recovery_id}"
                )
            current = PartialProtectionState(str(row["state"]))
            target = PartialProtectionState.PARTIAL_DETECTED
            if target not in PARTIAL_STATE_TRANSITIONS.get(current, frozenset()):
                raise PartialRecoveryConflictError(
                    "PARTIAL_TRANSITION_DENIED",
                    f"recovery_id={recovery_id} {current.value} -> {target.value}",
                )
            cursor = self.conn.execute(
                """UPDATE partial_fill_recoveries
                   SET state = ?, generation = generation + 1, reason_code = ?,
                       position_lots = COALESCE(?, position_lots),
                       filled_lots = COALESCE(?, filled_lots),
                       updated_ts = ?
                   WHERE recovery_id = ? AND state = ?""",
                (
                    target.value,
                    self._safe_reason_code(reason_code),
                    None if position_lots is None else int(position_lots),
                    None if filled_lots is None else int(filled_lots),
                    _to_iso(self._clock()),
                    recovery_id,
                    current.value,
                ),
            )
            if cursor.rowcount != 1:
                raise PartialRecoveryConflictError(
                    "PARTIAL_GENERATION_ROWCOUNT",
                    f"recovery_id={recovery_id} rowcount={cursor.rowcount}",
                )
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        row_out = self.get_partial_recovery(recovery_id)
        if row_out is None:  # pragma: no cover - defensive
            raise PartialRecoveryConflictError(
                "PARTIAL_RECOVERY_MISSING", f"recovery_id={recovery_id}"
            )
        return row_out

    def reserve_partial_action(
        self,
        *,
        recovery_id: str,
        action_id: str,
        kind: str,
        target_cloid: str,
        expected_state: str,
        next_state: str,
        reason_code: str,
        generation: int | None = None,
        flatten_seq: int | None = None,
        qty_lots: int | None = None,
        **fields: Any,
    ) -> tuple[bool, dict[str, Any]]:
        """Reserve an action *and* commit the state transition before any I/O.

        Returns ``(is_replay, action_row)``. A pre-existing reservation is a
        replay, not an error: after a crash between reserve-commit and send,
        the restarted process finds the same identity and resolves it by
        evidence instead of minting a new action.
        """
        self._require_partial_schema()
        action_kind = PartialActionKind(str(kind))
        safe_cloid = self._safe_cloid(target_cloid)
        now = _to_iso(self._clock())
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            recovery = self.conn.execute(
                "SELECT trade_id, state FROM partial_fill_recoveries "
                "WHERE recovery_id = ?",
                (recovery_id,),
            ).fetchone()
            if recovery is None:
                raise PartialRecoveryConflictError(
                    "PARTIAL_RECOVERY_NOT_FOUND", f"recovery_id={recovery_id}"
                )
            existing = self.conn.execute(
                "SELECT * FROM partial_fill_actions WHERE action_id = ?",
                (action_id,),
            ).fetchone()
            is_replay = existing is not None
            if is_replay:
                if (
                    str(existing["recovery_id"]) != recovery_id
                    or str(existing["kind"]) != action_kind.value
                    or str(existing["target_cloid"]) != safe_cloid
                    or existing["qty_lots"] != (
                        None if qty_lots is None else int(qty_lots)
                    )
                ):
                    raise PartialRecoveryConflictError(
                        "PARTIAL_ACTION_IDENTITY_CONFLICT", f"action_id={action_id}"
                    )
            else:
                self.conn.execute(
                    """INSERT INTO partial_fill_actions(
                         action_id, recovery_id, trade_id, kind, generation,
                         flatten_seq, qty_lots, target_cloid, reserved_ts
                       ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        action_id,
                        recovery_id,
                        int(recovery["trade_id"]),
                        action_kind.value,
                        None if generation is None else int(generation),
                        None if flatten_seq is None else int(flatten_seq),
                        None if qty_lots is None else int(qty_lots),
                        safe_cloid,
                        now,
                    ),
                )
                self._append_action_event_in_tx(
                    action_id=action_id,
                    recovery_id=recovery_id,
                    status=ActionRecordStatus.RESERVED.value,
                    evidence_source="LOCAL",
                    reason_code=reason_code,
                    evidence={"kind": action_kind.value, "target_cloid": safe_cloid},
                    observed_ts=now,
                )
            if str(recovery["state"]) != str(next_state):
                self._transition_partial_in_tx(
                    recovery_id, expected_state, next_state, reason_code, fields
                )
            if action_kind is PartialActionKind.CANCEL_ENTRY:
                # The cancel reservation and PENDING_CANCEL status commit
                # together before broker I/O. UNKNOWN cancel outcomes remain
                # pending; no optimistic terminal state is invented.
                self.conn.execute(
                    """UPDATE orders SET status = 'PENDING_CANCEL'
                       WHERE cloid = ? AND status NOT IN
                         ('FILLED', 'CANCELED', 'CANCELLED',
                          'CANCELLED_BY_ENGINE', 'REJECTED', 'EXPIRED')""",
                    (safe_cloid,),
                )
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        row = self.conn.execute(
            "SELECT * FROM partial_fill_actions WHERE action_id = ?", (action_id,)
        ).fetchone()
        if row is None:  # pragma: no cover - defensive
            raise PartialRecoveryConflictError(
                "PARTIAL_ACTION_MISSING", f"action_id={action_id}"
            )
        return is_replay, dict(row)

    def _append_action_event_in_tx(
        self,
        *,
        action_id: str,
        recovery_id: str,
        status: str,
        evidence_source: str,
        reason_code: str,
        evidence: Mapping[str, Any],
        observed_ts: str,
    ) -> None:
        record_status = ActionRecordStatus(str(status))
        seq_row = self.conn.execute(
            "SELECT COALESCE(MAX(seq), 0) + 1 FROM partial_fill_action_events "
            "WHERE action_id = ?",
            (action_id,),
        ).fetchone()
        self.conn.execute(
            """INSERT INTO partial_fill_action_events(
                 action_id, recovery_id, seq, status, evidence_source,
                 reason_code, evidence_json, observed_ts
               ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                action_id,
                recovery_id,
                int(seq_row[0]) if seq_row else 1,
                record_status.value,
                str(evidence_source) or "LOCAL",
                self._safe_reason_code(reason_code),
                _canonical_json(dict(evidence)),
                observed_ts,
            ),
        )

    def record_partial_action_event(
        self,
        *,
        action_id: str,
        status: str,
        reason_code: str,
        evidence_source: str = "BROKER",
        evidence: Mapping[str, Any] | None = None,
        observed_ts: datetime | str | None = None,
    ) -> None:
        """Append one immutable outcome/evidence record for a reserved action."""
        self._require_partial_schema()
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            row = self.conn.execute(
                "SELECT recovery_id FROM partial_fill_actions WHERE action_id = ?",
                (action_id,),
            ).fetchone()
            if row is None:
                raise PartialRecoveryConflictError(
                    "PARTIAL_ACTION_NOT_FOUND", f"action_id={action_id}"
                )
            self._append_action_event_in_tx(
                action_id=action_id,
                recovery_id=str(row["recovery_id"]),
                status=status,
                evidence_source=evidence_source,
                reason_code=reason_code,
                evidence=evidence or {},
                observed_ts=_to_iso(observed_ts) or _to_iso(self._clock()) or "",
            )
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

    def partial_action_events(self, action_id: str) -> list[dict[str, Any]]:
        return self._rows(
            "SELECT * FROM partial_fill_action_events WHERE action_id = ? ORDER BY seq",
            (action_id,),
        )

    def get_partial_action(self, action_id: str) -> dict[str, Any] | None:
        return self._partial_row(
            self.conn.execute(
                "SELECT * FROM partial_fill_actions WHERE action_id = ?",
                (str(action_id),),
            ).fetchone()
        )

    def resolve_partial_action(self, action_id: str) -> str | None:
        """Fold the append-only evidence into one conservative outcome.

        ``None`` means "reserved/sent, no outcome evidence yet". Conflicting
        definitive evidence resolves to ``UNKNOWN``, the most restrictive
        verdict: query-only, never re-issued. Chronology matters: a proved
        NOT_APPLIED action may be re-sent with the exact identity and later
        become APPLIED; the reverse ordering is contradictory. A definitive
        outcome is never downgraded by later UNKNOWN evidence.
        """
        statuses = [
            str(row["status"])
            for row in self.conn.execute(
                "SELECT status FROM partial_fill_action_events "
                "WHERE action_id = ? ORDER BY seq",
                (action_id,),
            ).fetchall()
        ]
        outcome: str | None = None
        saw_unknown = False
        contradictory = False
        for status in statuses:
            if status == ActionRecordStatus.UNKNOWN.value:
                saw_unknown = True
            elif status == ActionRecordStatus.NOT_APPLIED.value:
                if outcome == ActionOutcome.APPLIED.value:
                    contradictory = True
                elif outcome is None:
                    outcome = ActionOutcome.NOT_APPLIED.value
            elif status == ActionRecordStatus.APPLIED.value:
                outcome = ActionOutcome.APPLIED.value
        if contradictory:
            return ActionOutcome.UNKNOWN.value
        if outcome is not None:
            return outcome
        return ActionOutcome.UNKNOWN.value if saw_unknown else None

    def partial_actions_for_recovery(
        self, recovery_id: str, kind: str | None = None
    ) -> list[dict[str, Any]]:
        if kind is None:
            return self._rows(
                "SELECT * FROM partial_fill_actions WHERE recovery_id = ? "
                "ORDER BY reserved_ts, action_id",
                (recovery_id,),
            )
        return self._rows(
            "SELECT * FROM partial_fill_actions WHERE recovery_id = ? AND kind = ? "
            "ORDER BY reserved_ts, action_id",
            (recovery_id, PartialActionKind(str(kind)).value),
        )

    def partial_actions_for_lineage(
        self, trade_id: int, entry_cloid: str
    ) -> list[dict[str, Any]]:
        """Immutable actions from every generation of one exact entry lineage."""
        return self._rows(
            """SELECT a.* FROM partial_fill_actions a
               JOIN partial_fill_recoveries r
                 ON r.recovery_id = a.recovery_id
               WHERE r.trade_id = ? AND r.entry_cloid = ?
               ORDER BY a.reserved_ts, a.action_id""",
            (int(trade_id), str(entry_cloid)),
        )

    def applied_partial_flatten_lots(
        self, trade_id: int, entry_cloid: str
    ) -> int:
        """Durable owned exit quantity proved by resolved recovery flattens."""
        total = 0
        for action in self.partial_actions_for_lineage(trade_id, entry_cloid):
            if str(action["kind"]) != PartialActionKind.FLATTEN.value:
                continue
            if (
                self.resolve_partial_action(str(action["action_id"]))
                != ActionOutcome.APPLIED.value
            ):
                continue
            qty_lots = action["qty_lots"]
            if qty_lots is None or int(qty_lots) <= 0:
                raise PartialRecoveryConflictError(
                    "PARTIAL_FLATTEN_QUANTITY_INVALID",
                    f"action_id={action['action_id']}",
                )
            total += int(qty_lots)
        return total

    def partial_cancel_reserved_for_cloid(self, cloid: str) -> bool:
        """Whether the stable entry cancel identity has been durably reserved."""
        if not self.partial_protection_enabled():
            return False
        row = self.conn.execute(
            """SELECT 1 FROM partial_fill_actions
               WHERE kind = ? AND target_cloid = ? LIMIT 1""",
            (PartialActionKind.CANCEL_ENTRY.value, str(cloid)),
        ).fetchone()
        return row is not None

    def unresolved_partial_actions(self, recovery_id: str) -> list[dict[str, Any]]:
        """Reserved/sent actions whose outcome is not yet definitive."""
        return [
            action
            for action in self.partial_actions_for_recovery(recovery_id)
            if self.resolve_partial_action(str(action["action_id"]))
            in (None, ActionOutcome.UNKNOWN.value)
        ]

    def bump_partial_flatten_seq(self, recovery_id: str, expected_seq: int) -> int:
        """Advance the flatten attempt counter only after a definitive outcome.

        Refuses while the current sequence's FLATTEN action is unresolved or
        UNKNOWN, so an unknown flatten can never mint a second market close.
        """
        self._require_partial_schema()
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            row = self.conn.execute(
                "SELECT flatten_seq FROM partial_fill_recoveries WHERE recovery_id = ?",
                (recovery_id,),
            ).fetchone()
            if row is None:
                raise PartialRecoveryConflictError(
                    "PARTIAL_RECOVERY_NOT_FOUND", f"recovery_id={recovery_id}"
                )
            current = int(row["flatten_seq"])
            if current != int(expected_seq):
                raise PartialRecoveryConflictError(
                    "PARTIAL_FLATTEN_SEQ_CAS_FAILED",
                    f"recovery_id={recovery_id} current={current} expected={expected_seq}",
                )
            for action in self.conn.execute(
                """SELECT action_id FROM partial_fill_actions
                   WHERE recovery_id = ? AND kind = ? AND flatten_seq = ?""",
                (recovery_id, PartialActionKind.FLATTEN.value, current),
            ).fetchall():
                outcome = self.resolve_partial_action(str(action["action_id"]))
                if outcome not in (
                    ActionOutcome.APPLIED.value,
                    ActionOutcome.NOT_APPLIED.value,
                ):
                    raise PartialRecoveryConflictError(
                        "PARTIAL_FLATTEN_SEQ_UNRESOLVED",
                        f"recovery_id={recovery_id} seq={current} outcome={outcome}",
                    )
            cursor = self.conn.execute(
                """UPDATE partial_fill_recoveries
                   SET flatten_seq = flatten_seq + 1, updated_ts = ?
                   WHERE recovery_id = ? AND flatten_seq = ?""",
                (_to_iso(self._clock()), recovery_id, current),
            )
            if cursor.rowcount != 1:
                raise PartialRecoveryConflictError(
                    "PARTIAL_FLATTEN_SEQ_ROWCOUNT",
                    f"recovery_id={recovery_id} rowcount={cursor.rowcount}",
                )
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        return current + 1

    def legacy_partial_entry_candidates(self) -> list[dict[str, Any]]:
        """Query-only survey of owned entry orders with an unfilled remainder.

        Pure local evidence: no broker call, no mutation, no recovery row. The
        caller (``OrderManager`` startup recovery) is responsible for proving
        ownership against a bounded exchange snapshot before opening anything.
        """
        rows = self._rows(
            """SELECT o.cloid AS cloid, o.qty AS ordered_qty, o.status AS status,
                      o.decision_uid AS decision_uid, o.trade_id AS trade_id,
                      o.order_ref AS order_ref, o.group_id AS group_id,
                      t.coin AS coin, t.run_id AS run_id, t.direction AS direction,
                      t.exit_ts AS exit_ts,
                      COALESCE((SELECT SUM(f.qty) FROM fills f
                                WHERE f.cloid = o.cloid),
                               o.filled_qty, 0.0) AS filled_qty,
                      (SELECT MIN(f.fill_ts) FROM fills f
                       WHERE f.cloid = o.cloid) AS first_fill_ts
               FROM orders o JOIN trades t ON t.trade_id = o.trade_id
               WHERE o.role = 'ENTRY' AND t.exit_ts IS NULL
               ORDER BY o.ts_submit, o.cloid"""
        )
        candidates: list[dict[str, Any]] = []
        for row in rows:
            try:
                ordered = Decimal(str(row["ordered_qty"] or 0))
                filled = Decimal(str(row["filled_qty"] or 0))
            except Exception:
                continue
            if ordered <= 0 or filled <= 0 or filled >= ordered:
                continue
            candidates.append(row)
        return candidates

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
        attempt_id: str | None = None,
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
                attempt_id=attempt_id,
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
        attempt_id: str | None = None,
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
        if attempt_id is not None:
            attempt = self.conn.execute(
                """SELECT intent_id, request_id, state
                   FROM submission_attempts WHERE attempt_id = ?""",
                (attempt_id,),
            ).fetchone()
            if attempt is None:
                raise IdentityCollisionError(
                    "SUBMISSION_ATTEMPT_NOT_FOUND", f"attempt_id={attempt_id}"
                )
            if (
                str(attempt["intent_id"]) != intent_id
                or str(attempt["request_id"]) != request_id
                or str(attempt["state"]) != "SUBMITTING"
            ):
                raise IdentityCollisionError(
                    "SUBMISSION_FINALIZE_PRESTATE",
                    f"attempt_id={attempt_id} state={attempt['state']}",
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
        if attempt_id is not None:
            self._transition_attempt_in_tx(
                attempt_id, "VERIFIED_SUCCESS", "BROKER_VERIFIED_SUCCESS"
            )
            self._transition_attempt_in_tx(
                attempt_id, "FINALIZED", "LOCAL_FINALIZATION_COMPLETE"
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
        rows = self.conn.execute(
            "SELECT qty, px FROM fills WHERE cloid = ? ORDER BY fill_ts, fill_id",
            (cloid,),
        ).fetchall()
        qty = Decimal(0)
        notional = Decimal(0)
        for row in rows:
            row_qty = Decimal(str(row["qty"]))
            row_px = Decimal(str(row["px"]))
            qty += row_qty
            notional += row_qty * row_px
        vwap = float(notional / qty) if qty > 0 else None
        return float(qty), vwap

    def trade_fill_totals(self, trade_id: int) -> dict[str, Any]:
        rows = self.conn.execute(
            """
            SELECT CASE WHEN o.role = 'ENTRY' THEN 'ENTRY' ELSE 'EXIT' END AS side,
                   f.qty AS qty, f.px AS px, f.fill_ts AS fill_ts
            FROM fills f JOIN orders o ON o.cloid = f.cloid
            WHERE o.trade_id = ?
            ORDER BY f.fill_ts, f.fill_id
            """,
            (trade_id,),
        ).fetchall()
        totals: dict[str, Any] = {
            "entry_qty": 0.0, "entry_vwap": None, "entry_first_ts": None,
            "exit_qty": 0.0, "exit_vwap": None, "exit_last_ts": None,
        }
        aggregates = {
            "ENTRY": {"qty": Decimal(0), "notional": Decimal(0), "first": None, "last": None},
            "EXIT": {"qty": Decimal(0), "notional": Decimal(0), "first": None, "last": None},
        }
        for row in rows:
            side = str(row["side"])
            aggregate = aggregates[side]
            qty = Decimal(str(row["qty"]))
            px = Decimal(str(row["px"]))
            aggregate["qty"] += qty
            aggregate["notional"] += qty * px
            ts = str(row["fill_ts"])
            if aggregate["first"] is None:
                aggregate["first"] = ts
            aggregate["last"] = ts
        entry = aggregates["ENTRY"]
        exit_ = aggregates["EXIT"]
        if entry["qty"] > 0:
            totals["entry_qty"] = float(entry["qty"])
            totals["entry_vwap"] = float(entry["notional"] / entry["qty"])
            totals["entry_first_ts"] = entry["first"]
        if exit_["qty"] > 0:
            totals["exit_qty"] = float(exit_["qty"])
            totals["exit_vwap"] = float(exit_["notional"] / exit_["qty"])
            totals["exit_last_ts"] = exit_["last"]
        return totals

    def has_live_entry_remainder(self, trade_id: int) -> bool:
        for order in self.get_orders_for_trade(trade_id):
            if order["role"] != "ENTRY" or order["status"] not in {
                "OPEN", "SUBMITTED", "PENDING",
                "PARTIALLY_FILLED", "PENDING_CANCEL",
            }:
                continue
            filled_qty, _ = self.order_fill_totals(str(order["cloid"]))
            if Decimal(str(filled_qty)) < Decimal(str(order["qty"])):
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
              AND status IN (
                'OPEN', 'SUBMITTED', 'PENDING',
                'PARTIALLY_FILLED', 'PENDING_CANCEL'
              )
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
                "SELECT * FROM submission_attempts ORDER BY created_ts"
            ),
            "submission_recovery_evidence": self._rows(
                "SELECT * FROM submission_recovery_evidence ORDER BY attempt_id, cycle_no"
            ),
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
