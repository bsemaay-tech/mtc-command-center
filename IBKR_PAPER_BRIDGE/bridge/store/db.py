"""SQLite Store: v4 durable identity/submission ledger, v5 partial-fill recovery."""

from __future__ import annotations

import hashlib
import json
import math
import sqlite3
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable, Literal

from bridge.engine.types import (
    ACCOUNT_IDENTITY_ABS_TOL,
    KNOWN_DURABLE_ORDER_STATUSES,
    LIVE_DURABLE_ORDER_STATUSES,
    PARTIAL_STATE_TRANSITIONS,
    PARTIAL_TERMINAL_STATES,
    RISK_SNAPSHOT_ACCOUNT_INCONSISTENT,
    RISK_SNAPSHOT_ACCOUNT_MALFORMED,
    RISK_SNAPSHOT_ACCOUNT_NEGATIVE,
    RISK_SNAPSHOT_ATTEMPT_NOT_ACCEPTED,
    RISK_SNAPSHOT_COMPONENTS,
    RISK_SNAPSHOT_COMPONENTS_INCOMPLETE,
    RISK_SNAPSHOT_COVERAGE_UNPROVABLE,
    RISK_SNAPSHOT_FUTURE_CLOCK,
    RISK_SNAPSHOT_HASH_MISMATCH,
    RISK_SNAPSHOT_LEGACY_PAYLOAD,
    RISK_SNAPSHOT_NO_CHECKPOINT,
    RISK_SNAPSHOT_PAYLOAD_MALFORMED,
    RISK_SNAPSHOT_PAYLOAD_VERSION_UNSUPPORTED,
    RISK_SNAPSHOT_POINTER_DANGLING,
    RISK_SNAPSHOT_POINTER_MOVED,
    RISK_SNAPSHOT_POSITION_DUPLICATE,
    RISK_SNAPSHOT_POSITION_MALFORMED,
    RISK_SNAPSHOT_READ_FAILED,
    RISK_SNAPSHOT_ROW_DIGEST_MISMATCH,
    RISK_SNAPSHOT_ROWS_MISSING,
    RISK_SNAPSHOT_SCHEMA_INACTIVE,
    RISK_SNAPSHOT_STALE,
    RISK_SNAPSHOT_SUPERSEDED,
    RISK_SNAPSHOT_TRANSACTION_ACTIVE,
    SNAPSHOT_PAYLOAD_VERSION_V1,
    SNAPSHOT_PAYLOAD_VERSION_V2,
    SNAPSHOT_PAYLOAD_VERSION_V3,
    ActionOutcome,
    ActionRecordStatus,
    AuthoritativeRiskSnapshot,
    ComponentEvidence,
    DailyRiskState,
    DurableRiskPolicy,
    FundingAttribution,
    FundingEventRecord,
    KillActionKind,
    KillEvidenceEpoch,
    KillTerminalState,
    KILL_VERIFY_DEADLINE_S,
    PartialActionKind,
    PartialProtectionState,
    REQUIRED_RECONCILE_COMPONENTS,
    ReconcileAttemptState,
    ReconcileComponentKind,
    ReconcileComponentStatus,
    ReconcileDiffKind,
    ReconcileDiffRecord,
    ReconcileOwnership,
    RiskPositionRow,
    RiskControlLatch,
    RiskSnapshotUnavailable,
    RISK_CONTROL_DAILY_LOSS,
    RISK_CONTROL_EQUITY_STOP,
    RISK_CONTROL_MAX_DRAWDOWN,
    RISK_DAY_BASELINE_MISSING,
    RISK_DAY_CHECKPOINT_MISMATCH,
    RISK_DAY_DATE_MISMATCH,
    RISK_DAY_POLICY_MISMATCH,
    RISK_DAY_SCHEMA_INACTIVE,
    RISK_DAY_STATE_MALFORMED,
    RISK_DAY_UNEXPLAINED_CASHFLOW,
    RISK_LATCH_ACCOUNT_SCOPE,
    risk_control_reset_token,
    canonical_reconcile_json,
    reconcile_digest,
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

SCHEMA_VERSION_FULL_RECONCILE = 6
"""Additive TS-P1-005 reconciliation ledger; opt-in, never automatic.

The operational baseline stays :data:`SCHEMA_VERSION_BASELINE`. Reaching v6
requires an explicit ``initialize(target_schema_version=6)`` and goes through
the proven v4→v5→v6 chain; no caller is upgraded by merely opening a database.
"""

SCHEMA_VERSION_DURABLE_RISK = 7
"""Additive TS-P1-007 daily-risk evidence and sticky control latches."""

SCHEMA_VERSION_EXPOSURE_CONTROLS = 8
"""Additive TS-P1-008 exposure / leverage / liquidation capability.

Strictly a capability/version bump over v7: the daily-risk tables and every
existing object remain byte-for-byte / topology compatible, and no new
business-evidence table is added (the richer v3 rows live in the existing
immutable ``reconcile_checkpoints.snapshot_json``). Reaching v8 requires an
explicit ``initialize(target_schema_version=8)`` through the proven
v4->v5->v6->v7 chain; the migration only revalidates the v7 topology, integrity
and foreign keys and bumps the meta row. A fresh real v3 capture is then
mandatory for v8 risk authority; v1/v2 checkpoints stay retained and
reopenable but can never authorize v8 risk.
"""

SCHEMA_VERSION_KILL_EVIDENCE = 9
"""Additive TS-P1-009 durable kill episode/action/evidence ledger."""

SUPPORTED_TARGET_SCHEMA_VERSIONS = (
    SCHEMA_VERSION_BASELINE,
    SCHEMA_VERSION_PARTIAL_FILL,
    SCHEMA_VERSION_FULL_RECONCILE,
    SCHEMA_VERSION_DURABLE_RISK,
    SCHEMA_VERSION_EXPOSURE_CONTROLS,
    SCHEMA_VERSION_KILL_EVIDENCE,
)

RECONCILE_CHECKPOINT_POINTER_KEY = "reconcile_checkpoint_latest"
"""The single transactional pointer at the latest accepted checkpoint."""

RISK_CONTROLS_MIGRATION_FAILURE_KEY = "risk_controls_migration_failure"
EXPOSURE_CONTROLS_MIGRATION_FAILURE_KEY = "exposure_controls_migration_failure"
KILL_EVIDENCE_MIGRATION_FAILURE_KEY = "kill_evidence_migration_failure"
KILL_REQUEST_ACTIVE_KEY = "kill_request_active"
KILL_EPOCH_ACTIVE_KEY = "kill_epoch_active"

_PARTIAL_RECOVERY_VERSION = "ts-p1-004-recovery-v1"
_PARTIAL_ACTION_VERSION = "ts-p1-004-action-v1"
_RECONCILE_ATTEMPT_VERSION = "ts-p1-005-attempt-v1"
_RECONCILE_CHECKPOINT_VERSION = "ts-p1-005-checkpoint-v1"
_KILL_EPISODE_VERSION = "ts-p1-009-episode-v1"
_KILL_ACTION_VERSION = "ts-p1-009-action-v1"

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


_FULL_RECONCILE_EVIDENCE_TABLES = _PARTIAL_EVIDENCE_TABLES + (
    "partial_fill_recoveries",
    "partial_fill_actions",
    "partial_fill_action_events",
)


class PartialRecoveryConflictError(Exception):
    """Raised when a partial-recovery write would break a durable invariant."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


class ReconcileConflictError(Exception):
    """Raised when a reconciliation write would break a durable invariant."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


class RiskControlConflictError(Exception):
    """A durable risk latch/reset invariant would be violated."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


def compute_reconcile_attempt_id(*, run_id: str, seq: int, started_ts: datetime) -> str:
    """Stable per run/sequence/start attempt identity."""
    preimage = _canonical_json({
        "version": _RECONCILE_ATTEMPT_VERSION,
        "run_id": str(run_id),
        "seq": int(seq),
        "started_ts": _to_iso(started_ts),
    })
    return f"recon-v1:{hashlib.sha256(preimage.encode('utf-8')).hexdigest()}"


def compute_reconcile_checkpoint_id(*, attempt_id: str, canonical_hash: str) -> str:
    """Checkpoint identity bound 1:1 to its accepted attempt and evidence."""
    preimage = _canonical_json({
        "version": _RECONCILE_CHECKPOINT_VERSION,
        "attempt_id": str(attempt_id),
        "canonical_hash": str(canonical_hash),
    })
    return f"ckpt-v1:{hashlib.sha256(preimage.encode('utf-8')).hexdigest()}"


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


def compute_kill_episode_id(
    *,
    run_id: str,
    symbol: str,
    generation: int,
    flatten_requested: bool,
    policy_version: str,
) -> str:
    if isinstance(generation, bool) or int(generation) <= 0:
        raise ValueError("generation must be a positive integer")
    preimage = _canonical_json({
        "version": _KILL_EPISODE_VERSION,
        "run_id": str(run_id),
        "symbol": str(symbol).upper(),
        "generation": int(generation),
        "flatten_requested": bool(flatten_requested),
        "policy_version": str(policy_version),
    })
    return f"kill-v1:{hashlib.sha256(preimage.encode('utf-8')).hexdigest()}"


def compute_kill_action_id(
    *,
    episode_id: str,
    kind: str,
    target: str,
    qty_lots: int | None = None,
) -> str:
    action_kind = KillActionKind(str(kind))
    safe_target = str(target).strip()
    if not safe_target:
        raise ValueError("kill action target must not be blank")
    if action_kind is KillActionKind.FLATTEN:
        if isinstance(qty_lots, bool) or not isinstance(qty_lots, int) or qty_lots <= 0:
            raise ValueError("flatten qty_lots must be a positive integer")
    elif qty_lots is not None:
        raise ValueError("cancel qty_lots must be null")
    preimage = _canonical_json({
        "version": _KILL_ACTION_VERSION,
        "episode_id": str(episode_id),
        "kind": action_kind.value,
        "target": safe_target,
        "qty_lots": qty_lots,
    })
    return f"killa-v1:{hashlib.sha256(preimage.encode('utf-8')).hexdigest()}"


def compute_kill_action_cloid(action_id: str) -> str:
    digest = hashlib.blake2s(
        f"{_KILL_ACTION_VERSION}:{action_id}".encode("utf-8"), digest_size=16
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


class KillConflictError(Exception):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.reason_code = code
        super().__init__(f"{code}: {message}")


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

        The default target stays v4: TS-P1-004 adds schema v5 and TS-P1-005
        adds schema v6 as explicit, additive opt-ins so that no existing caller
        — and no existing runtime database — is silently upgraded by merely
        opening it. Reaching v5/v6 requires an explicit
        ``initialize(target_schema_version=5|6)``.

        A database already at v5 or v6 is reopened idempotently regardless of
        the requested target; this code understands both and must never
        downgrade. Unsupported or future versions still fail closed.
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
        if existing == str(SCHEMA_VERSION_KILL_EVIDENCE):
            if not self._has_any_kill_evidence_object():
                raise RuntimeError(
                    f"Unsupported schema_version={existing!r}; "
                    "cannot initialize safely"
                )
            self._initialize_v5_idempotent()
            self._initialize_v6_idempotent()
            self._initialize_v7_idempotent()
            self._initialize_v8_idempotent()
            self._initialize_v9_idempotent()
            return
        if existing == str(SCHEMA_VERSION_EXPOSURE_CONTROLS):
            if not self._has_any_durable_risk_object():
                # v8 inherits the v7 objects; a meta row alone is not proof.
                raise RuntimeError(
                    f"Unsupported schema_version={existing!r}; "
                    "cannot initialize safely"
                )
            # Idempotent reopen, never an in-place downgrade.
            self._initialize_v5_idempotent()
            self._initialize_v6_idempotent()
            self._initialize_v7_idempotent()
            self._initialize_v8_idempotent()
            if target_schema_version >= SCHEMA_VERSION_KILL_EVIDENCE:
                self._migrate_v8_to_v9()
            return
        if existing == str(SCHEMA_VERSION_DURABLE_RISK):
            if not self._has_any_durable_risk_object():
                raise RuntimeError(
                    f"Unsupported schema_version={existing!r}; "
                    "cannot initialize safely"
                )
            self._initialize_v5_idempotent()
            self._initialize_v6_idempotent()
            self._initialize_v7_idempotent()
            if target_schema_version >= SCHEMA_VERSION_EXPOSURE_CONTROLS:
                self._migrate_v7_to_v8()
            if target_schema_version >= SCHEMA_VERSION_KILL_EVIDENCE:
                self._migrate_v8_to_v9()
            return
        if existing == str(SCHEMA_VERSION_FULL_RECONCILE):
            if not self._has_any_full_reconcile_object():
                # The meta row alone is not proof of a version. A database that
                # claims v6 while carrying none of the v6 objects is corrupt
                # metadata — treat it exactly like an unknown version.
                raise RuntimeError(
                    f"Unsupported schema_version={existing!r}; "
                    "cannot initialize safely"
                )
            # Already migrated: idempotent reopen, never an in-place downgrade.
            self._initialize_v5_idempotent()
            self._initialize_v6_idempotent()
            if target_schema_version >= SCHEMA_VERSION_DURABLE_RISK:
                self._migrate_v6_to_v7()
            if target_schema_version >= SCHEMA_VERSION_EXPOSURE_CONTROLS:
                self._migrate_v7_to_v8()
            if target_schema_version >= SCHEMA_VERSION_KILL_EVIDENCE:
                self._migrate_v8_to_v9()
            return
        if existing == str(SCHEMA_VERSION_PARTIAL_FILL):
            self._initialize_v5_idempotent()
            if target_schema_version >= SCHEMA_VERSION_FULL_RECONCILE:
                self._migrate_v5_to_v6()
            if target_schema_version >= SCHEMA_VERSION_DURABLE_RISK:
                self._migrate_v6_to_v7()
            if target_schema_version >= SCHEMA_VERSION_EXPOSURE_CONTROLS:
                self._migrate_v7_to_v8()
            if target_schema_version >= SCHEMA_VERSION_KILL_EVIDENCE:
                self._migrate_v8_to_v9()
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
        if target_schema_version >= SCHEMA_VERSION_FULL_RECONCILE:
            # Proven chained v4→v5→v6; there is no skip migration.
            self._migrate_v5_to_v6()
        if target_schema_version >= SCHEMA_VERSION_DURABLE_RISK:
            self._migrate_v6_to_v7()
        if target_schema_version >= SCHEMA_VERSION_EXPOSURE_CONTROLS:
            self._migrate_v7_to_v8()
        if target_schema_version >= SCHEMA_VERSION_KILL_EVIDENCE:
            self._migrate_v8_to_v9()

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

    def _evidence_census(
        self, tables: tuple[str, ...] = _PARTIAL_EVIDENCE_TABLES
    ) -> dict[str, int]:
        """Row counts of every pre-existing evidence table (migration guard)."""
        census: dict[str, int] = {}
        for table in tables:
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

    # ------------------------------------------------------------------
    # TS-P1-005 v6 reconciliation ledger (opt-in)
    # ------------------------------------------------------------------

    _FULL_RECONCILE_OBJECTS = (
        "reconcile_attempts",
        "reconcile_components",
        "reconcile_diffs",
        "reconcile_checkpoints",
        "funding_events",
    )

    def _has_any_full_reconcile_object(self) -> bool:
        placeholders = ",".join("?" for _ in self._FULL_RECONCILE_OBJECTS)
        row = self.conn.execute(
            f"SELECT COUNT(*) FROM sqlite_master WHERE name IN ({placeholders})",
            self._FULL_RECONCILE_OBJECTS,
        ).fetchone()
        return bool(row and int(row[0]) > 0)

    def _initialize_v6_idempotent(self) -> None:
        """Re-open v6 only when its complete safety topology is canonical."""
        self._validate_full_reconcile_schema_v6()

    def _create_full_reconcile_tables_v6(self) -> None:
        """Purely additive DDL for exactly the five approved D4=A objects.

        Callable inside an open transaction. The latest-accepted pointer is a
        single ``meta`` row written in the same transaction as the checkpoint,
        so a checkpoint can never become visible without its pointer or the
        other way round.
        """
        attempt_states = ",".join(
            f"'{state.value}'"
            for state in sorted(ReconcileAttemptState, key=lambda s: s.value)
        )
        component_kinds = ",".join(
            f"'{kind.value}'"
            for kind in sorted(ReconcileComponentKind, key=lambda k: k.value)
        )
        component_statuses = ",".join(
            f"'{status.value}'"
            for status in sorted(ReconcileComponentStatus, key=lambda s: s.value)
        )
        diff_kinds = ",".join(
            f"'{kind.value}'"
            for kind in sorted(ReconcileDiffKind, key=lambda k: k.value)
        )
        ownerships = ",".join(
            f"'{value.value}'"
            for value in sorted(ReconcileOwnership, key=lambda o: o.value)
        )
        attributions = ",".join(
            f"'{value.value}'"
            for value in sorted(FundingAttribution, key=lambda a: a.value)
        )
        self.conn.execute(f"""
            CREATE TABLE IF NOT EXISTS reconcile_attempts (
              attempt_id TEXT PRIMARY KEY
                CHECK(length(attempt_id) = 73 AND substr(attempt_id, 1, 9) = 'recon-v1:'
                      AND NOT substr(attempt_id, 10) GLOB '*[^0-9a-f]*'),
              run_id TEXT NOT NULL CHECK(run_id != ''),
              seq INTEGER NOT NULL CHECK(seq > 0),
              state TEXT NOT NULL CHECK(state IN ({attempt_states})),
              started_ts TEXT NOT NULL CHECK(started_ts != ''),
              ended_ts TEXT,
              duration_ms INTEGER CHECK(duration_ms IS NULL OR duration_ms >= 0),
              deadline_s REAL NOT NULL CHECK(deadline_s > 0),
              max_skew_s REAL NOT NULL CHECK(max_skew_s >= 0),
              complete INTEGER NOT NULL DEFAULT 0 CHECK(complete IN (0, 1)),
              fresh INTEGER NOT NULL DEFAULT 0 CHECK(fresh IN (0, 1)),
              canonical_hash TEXT CHECK(canonical_hash IS NULL OR
                (length(canonical_hash) = 64 AND NOT canonical_hash GLOB '*[^0-9a-f]*')),
              reason_code TEXT NOT NULL CHECK(
                length(reason_code) BETWEEN 1 AND 96
                AND reason_code NOT GLOB '*[^A-Z0-9_:.-]*'
              ),
              UNIQUE(run_id, seq),
              CHECK((state = 'COLLECTING' AND ended_ts IS NULL)
                    OR (state != 'COLLECTING' AND ended_ts IS NOT NULL))
            )""")
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_reconcile_attempt_state "
            "ON reconcile_attempts(state, started_ts)")
        # An attempt is reserved before broker I/O and resolved exactly once.
        # Identity, bounds and a terminal verdict are immutable thereafter.
        self.conn.execute("""
            CREATE TRIGGER IF NOT EXISTS trg_reconcile_attempt_resolve_once
            BEFORE UPDATE ON reconcile_attempts
            BEGIN
              SELECT RAISE(ABORT, 'RECONCILE_ATTEMPT_IMMUTABLE')
              WHERE OLD.state != 'COLLECTING'
                 OR NEW.state = 'COLLECTING'
                 OR NEW.attempt_id != OLD.attempt_id
                 OR NEW.run_id != OLD.run_id
                 OR NEW.seq != OLD.seq
                 OR NEW.started_ts != OLD.started_ts
                 OR NEW.deadline_s != OLD.deadline_s
                 OR NEW.max_skew_s != OLD.max_skew_s;
            END""")
        self.conn.execute("""
            CREATE TRIGGER IF NOT EXISTS trg_reconcile_attempt_no_delete
            BEFORE DELETE ON reconcile_attempts
            BEGIN
              SELECT RAISE(ABORT, 'RECONCILE_ATTEMPT_IMMUTABLE');
            END""")
        self.conn.execute(f"""
            CREATE TABLE IF NOT EXISTS reconcile_components (
              component_row_id INTEGER PRIMARY KEY AUTOINCREMENT,
              attempt_id TEXT NOT NULL REFERENCES reconcile_attempts(attempt_id),
              component TEXT NOT NULL CHECK(component IN ({component_kinds})),
              source TEXT NOT NULL CHECK(source != ''),
              status TEXT NOT NULL CHECK(status IN ({component_statuses})),
              observed_ts TEXT,
              exact INTEGER NOT NULL CHECK(exact IN (0, 1)),
              complete INTEGER NOT NULL CHECK(complete IN (0, 1)),
              row_count INTEGER NOT NULL CHECK(row_count >= 0),
              cursor_start_ms INTEGER,
              cursor_end_ms INTEGER,
              page_count INTEGER NOT NULL DEFAULT 0 CHECK(page_count >= 0),
              call_count INTEGER NOT NULL DEFAULT 0 CHECK(call_count >= 0),
              payload_digest TEXT NOT NULL
                CHECK(length(payload_digest) = 64 AND NOT payload_digest GLOB '*[^0-9a-f]*'),
              reason_code TEXT NOT NULL CHECK(
                length(reason_code) BETWEEN 1 AND 96
                AND reason_code NOT GLOB '*[^A-Z0-9_:.-]*'
              ),
              UNIQUE(attempt_id, component)
            )""")
        self.conn.execute("""
            CREATE TRIGGER IF NOT EXISTS trg_reconcile_component_no_update
            BEFORE UPDATE ON reconcile_components
            BEGIN
              SELECT RAISE(ABORT, 'RECONCILE_COMPONENT_APPEND_ONLY');
            END""")
        self.conn.execute("""
            CREATE TRIGGER IF NOT EXISTS trg_reconcile_component_no_delete
            BEFORE DELETE ON reconcile_components
            BEGIN
              SELECT RAISE(ABORT, 'RECONCILE_COMPONENT_APPEND_ONLY');
            END""")
        self.conn.execute(f"""
            CREATE TABLE IF NOT EXISTS reconcile_diffs (
              diff_row_id INTEGER PRIMARY KEY AUTOINCREMENT,
              attempt_id TEXT NOT NULL REFERENCES reconcile_attempts(attempt_id),
              seq INTEGER NOT NULL CHECK(seq > 0),
              kind TEXT NOT NULL CHECK(kind IN ({diff_kinds})),
              subject TEXT NOT NULL CHECK(subject != ''),
              reason_code TEXT NOT NULL CHECK(
                length(reason_code) BETWEEN 1 AND 96
                AND reason_code NOT GLOB '*[^A-Z0-9_:.-]*'
              ),
              ownership TEXT NOT NULL CHECK(ownership IN ({ownerships})),
              blocking INTEGER NOT NULL CHECK(blocking IN (0, 1)),
              payload_json TEXT NOT NULL CHECK(payload_json != ''),
              UNIQUE(attempt_id, seq)
            )""")
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_reconcile_diff_attempt "
            "ON reconcile_diffs(attempt_id, seq)")
        self.conn.execute("""
            CREATE TRIGGER IF NOT EXISTS trg_reconcile_diff_no_update
            BEFORE UPDATE ON reconcile_diffs
            BEGIN
              SELECT RAISE(ABORT, 'RECONCILE_DIFF_APPEND_ONLY');
            END""")
        self.conn.execute("""
            CREATE TRIGGER IF NOT EXISTS trg_reconcile_diff_no_delete
            BEFORE DELETE ON reconcile_diffs
            BEGIN
              SELECT RAISE(ABORT, 'RECONCILE_DIFF_APPEND_ONLY');
            END""")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS reconcile_checkpoints (
              checkpoint_id TEXT PRIMARY KEY
                CHECK(length(checkpoint_id) = 72 AND substr(checkpoint_id, 1, 8) = 'ckpt-v1:'
                      AND NOT substr(checkpoint_id, 9) GLOB '*[^0-9a-f]*'),
              attempt_id TEXT UNIQUE NOT NULL REFERENCES reconcile_attempts(attempt_id),
              run_id TEXT NOT NULL CHECK(run_id != ''),
              accepted_ts TEXT NOT NULL CHECK(accepted_ts != ''),
              canonical_hash TEXT NOT NULL
                CHECK(length(canonical_hash) = 64 AND NOT canonical_hash GLOB '*[^0-9a-f]*'),
              snapshot_json TEXT NOT NULL CHECK(snapshot_json != ''),
              reason_code TEXT NOT NULL CHECK(
                length(reason_code) BETWEEN 1 AND 96
                AND reason_code NOT GLOB '*[^A-Z0-9_:.-]*'
              )
            )""")
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_reconcile_checkpoint_accepted "
            "ON reconcile_checkpoints(accepted_ts)")
        self.conn.execute("""
            CREATE TRIGGER IF NOT EXISTS trg_reconcile_checkpoint_no_update
            BEFORE UPDATE ON reconcile_checkpoints
            BEGIN
              SELECT RAISE(ABORT, 'RECONCILE_CHECKPOINT_IMMUTABLE');
            END""")
        self.conn.execute("""
            CREATE TRIGGER IF NOT EXISTS trg_reconcile_checkpoint_no_delete
            BEFORE DELETE ON reconcile_checkpoints
            BEGIN
              SELECT RAISE(ABORT, 'RECONCILE_CHECKPOINT_IMMUTABLE');
            END""")
        self.conn.execute(f"""
            CREATE TABLE IF NOT EXISTS funding_events (
              event_id TEXT PRIMARY KEY CHECK(event_id != ''),
              symbol TEXT NOT NULL CHECK(symbol != ''),
              amount_usdc REAL NOT NULL,
              effective_ts TEXT NOT NULL CHECK(effective_ts != ''),
              source TEXT NOT NULL CHECK(source != ''),
              attribution TEXT NOT NULL CHECK(attribution IN ({attributions})),
              payload_digest TEXT NOT NULL
                CHECK(length(payload_digest) = 64 AND NOT payload_digest GLOB '*[^0-9a-f]*'),
              first_seen_attempt_id TEXT NOT NULL
                REFERENCES reconcile_attempts(attempt_id),
              recorded_ts TEXT NOT NULL CHECK(recorded_ts != '')
            )""")
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_funding_event_symbol_time "
            "ON funding_events(symbol, effective_ts)")
        self.conn.execute("""
            CREATE TRIGGER IF NOT EXISTS trg_funding_event_no_update
            BEFORE UPDATE ON funding_events
            BEGIN
              SELECT RAISE(ABORT, 'FUNDING_EVENT_APPEND_ONLY');
            END""")
        self.conn.execute("""
            CREATE TRIGGER IF NOT EXISTS trg_funding_event_no_delete
            BEFORE DELETE ON funding_events
            BEGIN
              SELECT RAISE(ABORT, 'FUNDING_EVENT_APPEND_ONLY');
            END""")

    def _validate_full_reconcile_schema_v6(self) -> None:
        """Compare every v6 object against a canonical in-memory reference.

        Same technique as the accepted v5 validator: exact normalized SQL plus
        independent PRAGMA topology and foreign-key integrity, so a hand-edited
        or partially created v6 database fails closed on reopen.
        """
        tables = {
            "reconcile_attempts",
            "reconcile_components",
            "reconcile_diffs",
            "reconcile_checkpoints",
            "funding_events",
        }

        reference = Store(Path(":memory:"))
        reference._conn = sqlite3.connect(":memory:")
        reference._conn.row_factory = sqlite3.Row
        reference._conn.execute("PRAGMA foreign_keys=ON")
        Store._create_full_reconcile_tables_v6(reference)

        def normalized_sql(value: object) -> str:
            return " ".join(str(value or "").split()).upper()

        def object_signature(
            conn: sqlite3.Connection,
        ) -> dict[tuple[str, str], tuple[str, str]]:
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
                    for row in conn.execute(f"PRAGMA table_xinfo('{table}')").fetchall()
                )
                foreign_keys = tuple(
                    sorted(
                        (
                            tuple(row)
                            for row in conn.execute(
                                f"PRAGMA foreign_key_list('{table}')"
                            ).fetchall()
                        ),
                        key=repr,
                    )
                )
                indexes = []
                for row in conn.execute(f"PRAGMA index_list('{table}')").fetchall():
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
                    "v6 topology mismatch "
                    f"missing={missing} extra={extra} changed={changed}"
                )
            if pragma_signature(self.conn) != pragma_signature(reference._conn):
                raise MigrationError("v6 PRAGMA topology mismatch")
            if self.conn.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                raise MigrationError("v6 database integrity check failed")
            if self.conn.execute("PRAGMA foreign_key_check").fetchall():
                raise MigrationError("v6 foreign-key integrity check failed")
            self._validate_reconcile_pointer_v6()
        finally:
            reference._conn.close()
            reference._conn = None

    def _validate_reconcile_pointer_v6(self) -> None:
        """The sole v6 pointer and its immutable checkpoint must be coherent."""
        pointer = self.get_meta(RECONCILE_CHECKPOINT_POINTER_KEY)
        if self.get_meta("reconcile_coverage_upper_bound_ms") is not None:
            raise MigrationError("v6 contains unauthorized coverage pointer")
        count = int(
            self.conn.execute(
                "SELECT COUNT(*) FROM reconcile_checkpoints"
            ).fetchone()[0]
        )
        if pointer is None:
            if count:
                raise MigrationError("v6 accepted checkpoints without a pointer")
            return
        row = self.conn.execute(
            "SELECT checkpoint_id, attempt_id, canonical_hash, snapshot_json "
            "FROM reconcile_checkpoints WHERE checkpoint_id = ?",
            (pointer,),
        ).fetchone()
        if row is None:
            raise MigrationError("v6 checkpoint pointer does not resolve")
        attempt = self.conn.execute(
            "SELECT canonical_hash, state, complete, fresh, reason_code "
            "FROM reconcile_attempts WHERE attempt_id = ?",
            (row["attempt_id"],),
        ).fetchone()
        if (
            attempt is None
            or str(attempt["canonical_hash"]) != str(row["canonical_hash"])
            or str(attempt["state"]) != ReconcileAttemptState.COMPLETE.value
            or int(attempt["complete"]) != 1
            or int(attempt["fresh"]) != 1
            or str(attempt["reason_code"]) != "ACCEPTED"
        ):
            raise MigrationError("v6 checkpoint attempt evidence is inconsistent")
        try:
            snapshot = json.loads(str(row["snapshot_json"]))
        except (TypeError, ValueError, json.JSONDecodeError):
            raise MigrationError("v6 checkpoint snapshot is malformed") from None
        components = self.get_reconcile_components(str(row["attempt_id"]))
        if (
            len(components) != len(REQUIRED_RECONCILE_COMPONENTS)
            or {item["component"] for item in components}
            != {kind.value for kind in REQUIRED_RECONCILE_COMPONENTS}
            or any(
                item["status"] != ReconcileComponentStatus.COMPLETE.value
                or int(item["exact"]) != 1
                or int(item["complete"]) != 1
                or item["observed_ts"] is None
                for item in components
            )
        ):
            raise MigrationError("v6 checkpoint component evidence is incomplete")
        diffs = [
            json.loads(str(item["payload_json"]))
            for item in self.get_reconcile_diffs(str(row["attempt_id"]))
        ]
        component_digests = {
            str(item["component"]): str(item["payload_digest"])
            for item in components
        }
        hash_payload = {
            "version": snapshot.get("version"),
            "components": component_digests,
            "diffs": diffs,
        }
        if snapshot.get("version") == SNAPSHOT_PAYLOAD_VERSION_V3:
            hash_payload["exposure_policy_version"] = snapshot.get(
                "exposure_policy_version"
            )
        recomputed = reconcile_digest(hash_payload)
        if (
            recomputed != str(row["canonical_hash"])
            or {
                str(key): (
                    value.get("digest") if isinstance(value, Mapping) else None
                )
                for key, value in snapshot.get("components", {}).items()
            }
            != component_digests
            or snapshot.get("diffs") != diffs
        ):
            raise MigrationError("v6 checkpoint hash or snapshot evidence mismatch")
        snapshot_components = snapshot.get("components", {})
        for item in components:
            snap = snapshot_components.get(str(item["component"]))
            if (
                not isinstance(snap, Mapping)
                or snap.get("cursor_start_ms") != item["cursor_start_ms"]
                or snap.get("cursor_end_ms") != item["cursor_end_ms"]
            ):
                raise MigrationError("v6 checkpoint cursor evidence mismatch")
        funding_ids = snapshot.get("funding_event_ids")
        if not isinstance(funding_ids, list) or any(
            not isinstance(event_id, str) or not event_id for event_id in funding_ids
        ):
            raise MigrationError("v6 checkpoint funding evidence is malformed")
        funding_digests = snapshot.get("funding_event_digests")
        if (
            not isinstance(funding_digests, Mapping)
            or set(funding_digests) != set(funding_ids)
        ):
            raise MigrationError("v6 checkpoint funding digests are malformed")
        found_funding = (
            {
                str(item["event_id"]): str(item["payload_digest"])
                for item in self.conn.execute(
                    "SELECT event_id, payload_digest FROM funding_events WHERE event_id IN "
                    f"({','.join('?' for _ in funding_ids)})",
                    tuple(funding_ids),
                ).fetchall()
            }
            if funding_ids
            else {}
        )
        if found_funding != dict(funding_digests):
            raise MigrationError("v6 checkpoint funding ledger evidence is inconsistent")
        try:
            self._coverage_upper_bound_ms_locked()
        except ReconcileConflictError as exc:
            raise MigrationError(str(exc)) from exc

    def _migrate_v5_to_v6(self) -> None:
        """Additive v5→v6 upgrade in one rollback-clean transaction.

        DDL, evidence census, topology validation and the version bump share a
        single ``BEGIN IMMEDIATE``; any failure rolls back to a valid, reopenable
        v5 database with every pre-existing row untouched. There is no backfill:
        reconciliation evidence is only ever created by a real capture.
        """
        if self.get_meta("schema_version") == str(SCHEMA_VERSION_FULL_RECONCILE):
            self._initialize_v6_idempotent()
            return
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            if self.get_meta("schema_version") != str(SCHEMA_VERSION_PARTIAL_FILL):
                raise MigrationError("v5-to-v6 requires schema_version=5")
            before = self._evidence_census(_FULL_RECONCILE_EVIDENCE_TABLES)
            for table in (
                "reconcile_attempts",
                "reconcile_components",
                "reconcile_diffs",
                "reconcile_checkpoints",
                "funding_events",
            ):
                if self.conn.execute(
                    "SELECT name FROM sqlite_master WHERE name = ?", (table,)
                ).fetchone() is not None:
                    raise MigrationError(
                        f"v5-to-v6 aborted: pre-existing object {table!r}"
                    )
            if self.get_meta(RECONCILE_CHECKPOINT_POINTER_KEY) is not None:
                raise MigrationError("v5-to-v6 aborted: residual checkpoint pointer")
            if self.get_meta("reconcile_coverage_upper_bound_ms") is not None:
                raise MigrationError("v5-to-v6 aborted: residual coverage pointer")
            self._create_full_reconcile_tables_v6()
            self._validate_full_reconcile_schema_v6()
            after = self._evidence_census(_FULL_RECONCILE_EVIDENCE_TABLES)
            if before != after:
                raise MigrationError(
                    "v5-to-v6 must not alter existing evidence rows"
                )
            cursor = self.conn.execute(
                "UPDATE meta SET value = ? "
                "WHERE key = 'schema_version' AND value = ?",
                (
                    str(SCHEMA_VERSION_FULL_RECONCILE),
                    str(SCHEMA_VERSION_PARTIAL_FILL),
                ),
            )
            if cursor.rowcount != 1:
                raise MigrationError("v5-to-v6 version update rowcount mismatch")
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

    def _has_any_durable_risk_object(self) -> bool:
        row = self.conn.execute(
            "SELECT 1 FROM sqlite_master WHERE name IN "
            "('risk_day_checkpoints','risk_control_latches') LIMIT 1"
        ).fetchone()
        return row is not None

    def _create_durable_risk_tables_v7(self) -> None:
        self.conn.execute("""
            CREATE TABLE risk_day_checkpoints (
              risk_day_row_id INTEGER PRIMARY KEY,
              checkpoint_id TEXT NOT NULL UNIQUE
                REFERENCES reconcile_checkpoints(checkpoint_id),
              attempt_id TEXT NOT NULL UNIQUE
                REFERENCES reconcile_attempts(attempt_id),
              run_id TEXT NOT NULL REFERENCES runs(run_id),
              mode TEXT NOT NULL,
              network TEXT NOT NULL,
              trading_date TEXT NOT NULL,
              policy_version TEXT NOT NULL,
              baseline_source TEXT NOT NULL,
              baseline_checkpoint_id TEXT,
              baseline_ts TEXT,
              baseline_equity REAL,
              peak_equity REAL,
              equity REAL NOT NULL,
              daily_pnl REAL,
              daily_loss_pct REAL,
              drawdown_pct REAL,
              realized_pnl_local REAL NOT NULL,
              funding_attributed_usdc REAL NOT NULL,
              authoritative INTEGER NOT NULL CHECK(authoritative IN (0,1)),
              reason_code TEXT NOT NULL,
              accepted_ts TEXT NOT NULL,
              recorded_ts TEXT NOT NULL
            )""")
        self.conn.execute("""
            CREATE INDEX risk_day_environment_idx
            ON risk_day_checkpoints(mode, network, trading_date, accepted_ts)
        """)
        self.conn.execute("""
            CREATE TABLE risk_control_latches (
              latch_row_id INTEGER PRIMARY KEY,
              record_kind TEXT NOT NULL CHECK(record_kind IN ('LATCH','RESET')),
              control TEXT NOT NULL CHECK(control IN
                ('DAILY_LOSS','MAX_DRAWDOWN','EQUITY_STOP')),
              scope_key TEXT NOT NULL,
              mode TEXT NOT NULL,
              network TEXT NOT NULL,
              run_id TEXT NOT NULL REFERENCES runs(run_id),
              trading_date TEXT NOT NULL,
              checkpoint_id TEXT NOT NULL
                REFERENCES reconcile_checkpoints(checkpoint_id),
              supersedes_row_id INTEGER REFERENCES risk_control_latches(latch_row_id),
              generation INTEGER NOT NULL CHECK(generation > 0),
              observed_value REAL NOT NULL,
              threshold_value REAL NOT NULL,
              baseline_equity REAL NOT NULL,
              peak_equity REAL NOT NULL,
              equity REAL NOT NULL,
              policy_version TEXT NOT NULL,
              actor TEXT,
              reason_code TEXT NOT NULL,
              latched_ts TEXT NOT NULL,
              recorded_ts TEXT NOT NULL
            )""")
        self.conn.execute("""
            CREATE UNIQUE INDEX risk_control_active_generation
            ON risk_control_latches(control, mode, network, scope_key, generation,
                                    record_kind)
        """)
        self.conn.execute("""
            CREATE UNIQUE INDEX risk_control_one_reset
            ON risk_control_latches(supersedes_row_id)
            WHERE record_kind = 'RESET'
        """)
        for table in ("risk_day_checkpoints", "risk_control_latches"):
            self.conn.execute(
                f"""CREATE TRIGGER {table}_immutable_update
                    BEFORE UPDATE ON {table}
                    BEGIN SELECT RAISE(ABORT, 'append-only evidence'); END"""
            )
            self.conn.execute(
                f"""CREATE TRIGGER {table}_immutable_delete
                    BEFORE DELETE ON {table}
                    BEGIN SELECT RAISE(ABORT, 'append-only evidence'); END"""
            )

    def _validate_durable_risk_schema_v7(self) -> None:
        tables = {"risk_day_checkpoints", "risk_control_latches"}
        reference = Store(Path(":memory:"))
        reference._conn = sqlite3.connect(":memory:")
        reference._conn.row_factory = sqlite3.Row
        reference._conn.execute("PRAGMA foreign_keys=ON")
        reference._conn.execute(
            "CREATE TABLE runs (run_id TEXT PRIMARY KEY)"
        )
        reference._conn.execute(
            "CREATE TABLE reconcile_attempts (attempt_id TEXT PRIMARY KEY)"
        )
        reference._conn.execute(
            "CREATE TABLE reconcile_checkpoints (checkpoint_id TEXT PRIMARY KEY)"
        )
        Store._create_durable_risk_tables_v7(reference)

        def signature(conn: sqlite3.Connection) -> dict[tuple[str, str], tuple[str, str]]:
            rows = conn.execute(
                "SELECT type,name,tbl_name,sql FROM sqlite_master "
                "WHERE sql IS NOT NULL"
            ).fetchall()
            return {
                (str(row["type"]), str(row["name"])): (
                    str(row["tbl_name"]),
                    " ".join(str(row["sql"]).split()).upper(),
                )
                for row in rows
                if str(row["tbl_name"]) in tables
            }

        expected = signature(reference.conn)
        actual = signature(self.conn)
        reference.close()
        if actual != expected:
            raise MigrationError("v7 durable-risk topology is incomplete")
        if self.conn.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise MigrationError("v7 integrity_check failed")
        if self.conn.execute("PRAGMA foreign_key_check").fetchall():
            raise MigrationError("v7 foreign_key_check failed")

    def _initialize_v7_idempotent(self) -> None:
        self._validate_durable_risk_schema_v7()

    def _migrate_v6_to_v7(self) -> None:
        if self.get_meta("schema_version") == str(SCHEMA_VERSION_DURABLE_RISK):
            self._initialize_v7_idempotent()
            return
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            if self.get_meta("schema_version") != str(SCHEMA_VERSION_FULL_RECONCILE):
                raise MigrationError("v6-to-v7 requires schema_version=6")
            for name in ("risk_day_checkpoints", "risk_control_latches"):
                if self.conn.execute(
                    "SELECT 1 FROM sqlite_master WHERE name = ?", (name,)
                ).fetchone():
                    raise MigrationError(
                        f"v6-to-v7 aborted: pre-existing object {name!r}"
                    )
            before = self._evidence_census(_FULL_RECONCILE_EVIDENCE_TABLES)
            self._create_durable_risk_tables_v7()
            self._validate_durable_risk_schema_v7()
            if self._evidence_census(_FULL_RECONCILE_EVIDENCE_TABLES) != before:
                raise MigrationError("v6-to-v7 altered predecessor evidence")
            cursor = self.conn.execute(
                "UPDATE meta SET value = ? WHERE key='schema_version' AND value=?",
                (
                    str(SCHEMA_VERSION_DURABLE_RISK),
                    str(SCHEMA_VERSION_FULL_RECONCILE),
                ),
            )
            if cursor.rowcount != 1:
                raise MigrationError("v6-to-v7 version update rowcount mismatch")
            self.conn.commit()
        except Exception as exc:
            self.conn.rollback()
            try:
                self.conn.execute(
                    "INSERT OR REPLACE INTO meta(key,value) VALUES (?,?)",
                    (
                        RISK_CONTROLS_MIGRATION_FAILURE_KEY,
                        f"RISK_CONTROLS_MIGRATION_FAILED:{type(exc).__name__}",
                    ),
                )
                self.conn.commit()
            except Exception:
                self.conn.rollback()
            raise

    def _initialize_v8_idempotent(self) -> None:
        """Reopen a v8 database: v8 inherits the v7 topology, so revalidate it.

        v8 adds no tables; the only thing that distinguishes a v8 database from
        a v7 one is the ``schema_version`` meta row plus the v3 snapshot payload
        produced/consumed only on a v8 store. Reopening therefore re-proves the
        inherited v7 topology, integrity and foreign keys, and rejects any meta
        row that does not actually claim v8.
        """
        self._validate_durable_risk_schema_v7()
        if self.get_meta("schema_version") not in {
            str(SCHEMA_VERSION_EXPOSURE_CONTROLS),
            str(SCHEMA_VERSION_KILL_EVIDENCE),
        }:
            raise MigrationError(
                "v8 topology requires schema_version=8 or additive successor"
            )

    def _migrate_v7_to_v8(self) -> None:
        """Capability-only v7 -> v8 bump in one rollback-clean transaction.

        No DDL: the v7 daily-risk tables and every predecessor object are
        already topology-compatible with v8. The migration revalidates the v7
        topology, integrity and foreign keys, proves the predecessor evidence
        census is unchanged, and bumps the meta row. A fresh real v3 capture is
        still mandatory afterwards for v8 risk authority. Any failure rolls back
        to a reopenable v7 and records a secret-safe migration failure.
        """
        if self.get_meta("schema_version") == str(SCHEMA_VERSION_EXPOSURE_CONTROLS):
            self._initialize_v8_idempotent()
            return
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            if self.get_meta("schema_version") != str(SCHEMA_VERSION_DURABLE_RISK):
                raise MigrationError("v7-to-v8 requires schema_version=7")
            self._validate_durable_risk_schema_v7()
            if self.conn.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                raise MigrationError("v8 integrity_check failed")
            if self.conn.execute("PRAGMA foreign_key_check").fetchall():
                raise MigrationError("v8 foreign_key_check failed")
            before = self._evidence_census(_FULL_RECONCILE_EVIDENCE_TABLES)
            # No tables to create; the census must be byte-for-byte unchanged.
            if self._evidence_census(_FULL_RECONCILE_EVIDENCE_TABLES) != before:
                raise MigrationError("v7-to-v8 altered predecessor evidence")
            cursor = self.conn.execute(
                "UPDATE meta SET value = ? WHERE key='schema_version' AND value=?",
                (
                    str(SCHEMA_VERSION_EXPOSURE_CONTROLS),
                    str(SCHEMA_VERSION_DURABLE_RISK),
                ),
            )
            if cursor.rowcount != 1:
                raise MigrationError("v7-to-v8 version update rowcount mismatch")
            self.conn.commit()
        except Exception as exc:
            self.conn.rollback()
            try:
                self.conn.execute(
                    "INSERT OR REPLACE INTO meta(key,value) VALUES (?,?)",
                    (
                        EXPOSURE_CONTROLS_MIGRATION_FAILURE_KEY,
                        f"EXPOSURE_CONTROLS_MIGRATION_FAILED:{type(exc).__name__}",
                    ),
                )
                self.conn.commit()
            except Exception:
                self.conn.rollback()
            raise

    # ------------------------------------------------------------------
    # TS-P1-009 v9 durable kill evidence
    # ------------------------------------------------------------------

    _KILL_EVIDENCE_OBJECTS = (
        "kill_requests",
        "kill_actions",
        "kill_action_events",
    )

    def _has_any_kill_evidence_object(self) -> bool:
        placeholders = ",".join("?" for _ in self._KILL_EVIDENCE_OBJECTS)
        return self.conn.execute(
            f"SELECT 1 FROM sqlite_master WHERE name IN ({placeholders}) LIMIT 1",
            self._KILL_EVIDENCE_OBJECTS,
        ).fetchone() is not None

    def _create_kill_evidence_tables_v9(self) -> None:
        self.conn.execute("""
            CREATE TABLE kill_requests (
              episode_id TEXT PRIMARY KEY,
              generation INTEGER NOT NULL CHECK(generation > 0),
              run_id TEXT NOT NULL REFERENCES runs(run_id),
              symbol TEXT NOT NULL CHECK(length(trim(symbol)) > 0),
              flatten_requested INTEGER NOT NULL
                CHECK(flatten_requested IN (0,1)),
              requested_ts TEXT NOT NULL,
              policy_version TEXT NOT NULL CHECK(length(trim(policy_version)) > 0),
              epoch_token TEXT NOT NULL,
              terminal_state TEXT NOT NULL CHECK(terminal_state IN
                ('IN_PROGRESS','UNRESOLVED','UNKNOWN','AMBIGUOUS',
                 'PROOF_PENDING','SAFE_RETAINED','SAFE_FLAT')),
              terminal_reason TEXT NOT NULL,
              terminal_ts TEXT,
              safe_checkpoint_id TEXT
                REFERENCES reconcile_checkpoints(checkpoint_id),
              safe_checkpoint_ts TEXT,
              proof_digest TEXT,
              ack_state TEXT NOT NULL CHECK(ack_state IN
                ('PENDING','ACKNOWLEDGED')),
              ack_ts TEXT,
              UNIQUE(run_id, symbol, generation)
            )""")
        self.conn.execute("""
            CREATE TABLE kill_actions (
              action_id TEXT PRIMARY KEY,
              episode_id TEXT NOT NULL
                REFERENCES kill_requests(episode_id),
              kind TEXT NOT NULL CHECK(kind IN ('CANCEL','FLATTEN')),
              target TEXT NOT NULL CHECK(length(trim(target)) > 0),
              qty_lots INTEGER,
              cloid TEXT NOT NULL CHECK(length(trim(cloid)) > 0),
              exit_side TEXT CHECK(exit_side IN ('BUY','SELL')),
              reserved_ts TEXT NOT NULL,
              deadline_ts TEXT NOT NULL,
              current_outcome TEXT NOT NULL CHECK(current_outcome IN
                ('RESERVED','UNKNOWN','NOT_APPLIED','APPLIED')),
              UNIQUE(episode_id, kind, target),
              CHECK(
                (kind='CANCEL' AND qty_lots IS NULL)
                OR (kind='FLATTEN' AND qty_lots > 0)
              )
            )""")
        self.conn.execute("""
            CREATE TABLE kill_action_events (
              event_row_id INTEGER PRIMARY KEY,
              action_id TEXT NOT NULL REFERENCES kill_actions(action_id),
              seq INTEGER NOT NULL CHECK(seq > 0),
              status TEXT NOT NULL CHECK(status IN
                ('RESERVED','SENT','APPLIED','NOT_APPLIED','UNKNOWN','EVIDENCE')),
              evidence_source TEXT NOT NULL,
              reason_code TEXT NOT NULL,
              evidence_json TEXT NOT NULL,
              evidence_digest TEXT NOT NULL,
              observed_ts TEXT NOT NULL,
              UNIQUE(action_id, seq)
            )""")
        self.conn.execute("""
            CREATE INDEX kill_request_state_idx
            ON kill_requests(ack_state, terminal_state, requested_ts)""")
        self.conn.execute("""
            CREATE INDEX kill_action_episode_idx
            ON kill_actions(episode_id, kind, reserved_ts, action_id)""")
        self.conn.execute("""
            CREATE TRIGGER kill_requests_identity_immutable
            BEFORE UPDATE ON kill_requests
            WHEN OLD.episode_id IS NOT NEW.episode_id
              OR OLD.generation IS NOT NEW.generation
              OR OLD.run_id IS NOT NEW.run_id
              OR OLD.symbol IS NOT NEW.symbol
              OR OLD.flatten_requested IS NOT NEW.flatten_requested
              OR OLD.requested_ts IS NOT NEW.requested_ts
              OR OLD.policy_version IS NOT NEW.policy_version
            BEGIN SELECT RAISE(ABORT, 'immutable kill request identity'); END""")
        self.conn.execute("""
            CREATE TRIGGER kill_requests_immutable_delete
            BEFORE DELETE ON kill_requests
            BEGIN SELECT RAISE(ABORT, 'append-only kill evidence'); END""")
        self.conn.execute("""
            CREATE TRIGGER kill_actions_identity_immutable
            BEFORE UPDATE ON kill_actions
            WHEN OLD.action_id IS NOT NEW.action_id
              OR OLD.episode_id IS NOT NEW.episode_id
              OR OLD.kind IS NOT NEW.kind
              OR OLD.target IS NOT NEW.target
              OR OLD.qty_lots IS NOT NEW.qty_lots
              OR OLD.cloid IS NOT NEW.cloid
              OR OLD.exit_side IS NOT NEW.exit_side
              OR OLD.reserved_ts IS NOT NEW.reserved_ts
              OR OLD.deadline_ts IS NOT NEW.deadline_ts
            BEGIN SELECT RAISE(ABORT, 'immutable kill action identity'); END""")
        self.conn.execute("""
            CREATE TRIGGER kill_actions_immutable_delete
            BEFORE DELETE ON kill_actions
            BEGIN SELECT RAISE(ABORT, 'append-only kill evidence'); END""")
        for suffix in ("update", "delete"):
            self.conn.execute(f"""
                CREATE TRIGGER kill_action_events_immutable_{suffix}
                BEFORE {suffix.upper()} ON kill_action_events
                BEGIN SELECT RAISE(ABORT, 'append-only kill evidence'); END""")

    def _validate_kill_evidence_schema_v9(self) -> None:
        reference = Store(Path(":memory:"))
        reference._conn = sqlite3.connect(":memory:")
        reference._conn.row_factory = sqlite3.Row
        reference._conn.execute("PRAGMA foreign_keys=ON")
        reference._conn.execute(
            "CREATE TABLE runs (run_id TEXT PRIMARY KEY)"
        )
        reference._conn.execute(
            "CREATE TABLE reconcile_checkpoints (checkpoint_id TEXT PRIMARY KEY)"
        )
        Store._create_kill_evidence_tables_v9(reference)

        tables = set(self._KILL_EVIDENCE_OBJECTS)

        def signature(conn: sqlite3.Connection) -> dict[tuple[str, str], tuple[str, str]]:
            rows = conn.execute(
                "SELECT type,name,tbl_name,sql FROM sqlite_master "
                "WHERE sql IS NOT NULL"
            ).fetchall()
            return {
                (str(row["type"]), str(row["name"])): (
                    str(row["tbl_name"]),
                    " ".join(str(row["sql"]).split()).upper(),
                )
                for row in rows
                if str(row["tbl_name"]) in tables
            }

        expected = signature(reference.conn)
        actual = signature(self.conn)
        reference.close()
        if actual != expected:
            raise MigrationError("v9 kill-evidence topology is incomplete")
        if self.conn.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise MigrationError("v9 integrity_check failed")
        if self.conn.execute("PRAGMA foreign_key_check").fetchall():
            raise MigrationError("v9 foreign_key_check failed")
        duplicates = self.conn.execute(
            "SELECT lower(cloid) FROM kill_actions "
            "GROUP BY lower(cloid) HAVING COUNT(*) > 1"
        ).fetchall()
        if duplicates:
            raise MigrationError("v9 duplicate action cloid alias")
        self._validate_kill_pointer_v9()
        self._validate_kill_rows_v9()

    def _validate_kill_rows_v9(self) -> None:
        """Re-prove immutable identities, event folding and safe-proof links."""
        for request in self._rows(
            "SELECT * FROM kill_requests ORDER BY requested_ts,episode_id"
        ):
            expected = compute_kill_episode_id(
                run_id=str(request["run_id"]),
                symbol=str(request["symbol"]),
                generation=int(request["generation"]),
                flatten_requested=bool(request["flatten_requested"]),
                policy_version=str(request["policy_version"]),
            )
            if str(request["episode_id"]) != expected:
                raise MigrationError("v9 kill episode identity mismatch")
            try:
                datetime.fromisoformat(str(request["requested_ts"]))
            except (TypeError, ValueError):
                raise MigrationError("v9 kill request timestamp malformed") from None
            try:
                request_epoch, request_epoch_state = (
                    self._parse_kill_epoch_token(request["epoch_token"])
                )
            except KillConflictError as exc:
                raise MigrationError("v9 kill epoch token malformed") from exc
            if request_epoch.episode_id != str(request["episode_id"]):
                raise MigrationError("v9 kill epoch episode mismatch")
            safe = str(request["terminal_state"]) in {"SAFE_FLAT", "SAFE_RETAINED"}
            proof_fields = (
                request["safe_checkpoint_id"],
                request["safe_checkpoint_ts"],
                request["proof_digest"],
            )
            if safe and request["terminal_ts"] is None:
                raise MigrationError("v9 safe kill terminal timestamp missing")
            if not safe and any(value is not None for value in proof_fields):
                raise MigrationError("v9 unsafe kill request carries safe proof")
            if any(value is not None for value in proof_fields):
                if not safe or any(value is None for value in proof_fields):
                    raise MigrationError("v9 kill safe proof is incomplete")
                digest = str(request["proof_digest"])
                if len(digest) != 64 or any(
                    char not in "0123456789abcdef" for char in digest.lower()
                ):
                    raise MigrationError("v9 kill proof digest malformed")
                checkpoint = self.conn.execute(
                    "SELECT accepted_ts FROM reconcile_checkpoints "
                    "WHERE checkpoint_id=?",
                    (str(request["safe_checkpoint_id"]),),
                ).fetchone()
                if (
                    checkpoint is None
                    or str(checkpoint["accepted_ts"])
                    != str(request["safe_checkpoint_ts"])
                ):
                    raise MigrationError("v9 kill checkpoint proof mismatch")
            acknowledged = str(request["ack_state"]) == "ACKNOWLEDGED"
            if acknowledged and (
                not safe
                or request["ack_ts"] is None
                or any(value is None for value in proof_fields)
                or request_epoch_state != "CLOSED"
            ):
                raise MigrationError("v9 acknowledged kill proof is incomplete")
            if not acknowledged and request["ack_ts"] is not None:
                raise MigrationError("v9 pending kill carries ack timestamp")

        for action in self._rows(
            "SELECT * FROM kill_actions ORDER BY episode_id,kind,target"
        ):
            expected_id = compute_kill_action_id(
                episode_id=str(action["episode_id"]),
                kind=str(action["kind"]),
                target=str(action["target"]),
                qty_lots=action["qty_lots"],
            )
            expected_cloid = (
                str(action["target"])
                if str(action["kind"]) == KillActionKind.CANCEL.value
                else compute_kill_action_cloid(expected_id)
            )
            if (
                str(action["action_id"]) != expected_id
                or str(action["cloid"]) != expected_cloid
            ):
                raise MigrationError("v9 kill action identity mismatch")
            if str(action["kind"]) == KillActionKind.FLATTEN.value and str(
                action["exit_side"] or ""
            ) not in {"BUY", "SELL"}:
                raise MigrationError("v9 kill flatten exit side missing")
            if str(action["kind"]) == KillActionKind.CANCEL.value and action[
                "exit_side"
            ] is not None:
                raise MigrationError("v9 cancel carries exit side")
            try:
                reserved = datetime.fromisoformat(str(action["reserved_ts"]))
                deadline = datetime.fromisoformat(str(action["deadline_ts"]))
                if reserved.tzinfo is None:
                    reserved = reserved.replace(tzinfo=UTC)
                if deadline.tzinfo is None:
                    deadline = deadline.replace(tzinfo=UTC)
                budget = (deadline - reserved).total_seconds()
            except (TypeError, ValueError):
                raise MigrationError("v9 kill action deadline malformed") from None
            if not (0 < budget <= KILL_VERIFY_DEADLINE_S + 0.001):
                raise MigrationError("v9 kill action deadline out of bounds")
            events = self._rows(
                "SELECT * FROM kill_action_events WHERE action_id=? ORDER BY seq",
                (str(action["action_id"]),),
            )
            if [int(event["seq"]) for event in events] != list(
                range(1, len(events) + 1)
            ):
                raise MigrationError("v9 kill action event sequence malformed")
            for event in events:
                payload = str(event["evidence_json"])
                try:
                    parsed = json.loads(payload)
                except (TypeError, ValueError, json.JSONDecodeError):
                    raise MigrationError("v9 kill evidence JSON malformed") from None
                if (
                    not isinstance(parsed, Mapping)
                    or _canonical_json(dict(parsed)) != payload
                    or hashlib.sha256(payload.encode("utf-8")).hexdigest()
                    != str(event["evidence_digest"])
                ):
                    raise MigrationError("v9 kill evidence digest mismatch")
            if not events or str(events[0]["status"]) != "RESERVED":
                raise MigrationError("v9 kill action reservation evidence missing")
            if (
                self._fold_kill_action_outcome_locked(str(action["action_id"]))
                != str(action["current_outcome"])
            ):
                raise MigrationError("v9 kill action folded outcome mismatch")

    def _validate_kill_pointer_v9(self) -> None:
        pointer = self.get_meta(KILL_REQUEST_ACTIVE_KEY)
        epoch_pointer = self.get_meta(KILL_EPOCH_ACTIVE_KEY)
        rows = self.conn.execute(
            "SELECT episode_id,epoch_token FROM kill_requests "
            "WHERE ack_state='PENDING' "
            "ORDER BY requested_ts, episode_id"
        ).fetchall()
        if pointer is None:
            if rows or epoch_pointer is not None:
                raise MigrationError("v9 active kill pointer missing")
            return
        if (
            len(rows) != 1
            or str(rows[0]["episode_id"]) != pointer
            or epoch_pointer is None
            or str(rows[0]["epoch_token"]) != epoch_pointer
        ):
            raise MigrationError("v9 active kill pointer dangling or ambiguous")
        try:
            epoch, _state = self._parse_kill_epoch_token(epoch_pointer)
        except KillConflictError as exc:
            raise MigrationError("v9 active kill epoch malformed") from exc
        if epoch.episode_id != pointer:
            raise MigrationError("v9 active kill epoch mismatch")

    def _initialize_v9_idempotent(self) -> None:
        self._validate_kill_evidence_schema_v9()
        if self.get_meta("schema_version") != str(SCHEMA_VERSION_KILL_EVIDENCE):
            raise MigrationError("v9 reopen requires schema_version=9")

    def _all_table_census(self) -> dict[str, int]:
        result: dict[str, int] = {}
        rows = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name NOT LIKE 'sqlite_%' ORDER BY name"
        ).fetchall()
        for row in rows:
            name = str(row["name"])
            if name in self._KILL_EVIDENCE_OBJECTS:
                continue
            result[name] = int(
                self.conn.execute(f'SELECT COUNT(*) FROM "{name}"').fetchone()[0]
            )
        return result

    def _migrate_v8_to_v9(self) -> None:
        if self.get_meta("schema_version") == str(SCHEMA_VERSION_KILL_EVIDENCE):
            self._initialize_v9_idempotent()
            return
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            if self.get_meta("schema_version") != str(
                SCHEMA_VERSION_EXPOSURE_CONTROLS
            ):
                raise MigrationError("v8-to-v9 requires schema_version=8")
            self._initialize_v8_idempotent()
            if self._has_any_kill_evidence_object():
                raise MigrationError(
                    "v8-to-v9 aborted: pre-existing object in kill evidence topology"
                )
            if self.get_meta(KILL_REQUEST_ACTIVE_KEY) is not None:
                raise MigrationError(
                    "v8-to-v9 aborted: residual active kill pointer"
                )
            if self.get_meta(KILL_EPOCH_ACTIVE_KEY) is not None:
                raise MigrationError(
                    "v8-to-v9 aborted: residual active kill epoch"
                )
            before = self._all_table_census()
            self._create_kill_evidence_tables_v9()
            self._validate_kill_evidence_schema_v9()
            after = self._all_table_census()
            if before != after:
                raise MigrationError("v8-to-v9 altered predecessor evidence")
            cursor = self.conn.execute(
                "UPDATE meta SET value=? WHERE key='schema_version' AND value=?",
                (
                    str(SCHEMA_VERSION_KILL_EVIDENCE),
                    str(SCHEMA_VERSION_EXPOSURE_CONTROLS),
                ),
            )
            if cursor.rowcount != 1:
                raise MigrationError("v8-to-v9 version update rowcount mismatch")
            self.conn.commit()
        except Exception as exc:
            self.conn.rollback()
            try:
                self.conn.execute(
                    "INSERT OR IGNORE INTO meta(key,value) VALUES (?,?)",
                    (
                        KILL_EVIDENCE_MIGRATION_FAILURE_KEY,
                        f"KILL_EVIDENCE_MIGRATION_FAILED:{type(exc).__name__}",
                    ),
                )
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
        """True on any database that carries the v5 recovery ledger.

        v6 is strictly additive on top of v5, so the TS-P1-004 ledger is still
        present and still authoritative there. Comparing for equality with v5
        alone would silently disable partial-recovery gating on a v6 database —
        a fail-open the reconciliation task must not introduce.
        """
        version = self.get_meta("schema_version")
        if version is None:
            return False
        try:
            return int(version) >= SCHEMA_VERSION_PARTIAL_FILL
        except ValueError:
            return False

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
    # TS-P1-009 durable kill episode/action/evidence API
    # ------------------------------------------------------------------

    def kill_evidence_enabled(self) -> bool:
        return self.get_meta("schema_version") == str(SCHEMA_VERSION_KILL_EVIDENCE)

    def _require_kill_schema(self) -> None:
        if not self.kill_evidence_enabled():
            raise KillConflictError("KILL_SCHEMA_INACTIVE", "schema v9 is not active")

    def _insert_event_in_tx(
        self, run_id: str, ts: str, severity: str, code: str, detail: str
    ) -> None:
        self.conn.execute(
            """INSERT INTO events(run_id, ts, severity, code, detail)
               VALUES (?, ?, ?, ?, ?)""",
            (str(run_id), ts, str(severity), str(code), str(detail)),
        )

    @staticmethod
    def _kill_epoch_token(epoch: KillEvidenceEpoch, state: str) -> str:
        if state not in {"OPEN", "CLOSED"}:
            raise KillConflictError("KILL_EPOCH_STATE_INVALID", str(state))
        return _canonical_json({**epoch.as_payload(), "state": state})

    @staticmethod
    def _parse_kill_epoch_token(value: object) -> tuple[KillEvidenceEpoch, str]:
        try:
            payload = json.loads(str(value))
            if not isinstance(payload, Mapping):
                raise ValueError
            state = str(payload["state"])
            epoch = KillEvidenceEpoch(
                episode_id=str(payload["episode_id"]),
                attempt_no=int(payload["attempt_no"]),
                process_uid=str(payload["process_uid"]),
                opened_ts_monotonic=float(payload["opened_ts_monotonic"]),
            )
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            raise KillConflictError(
                "KILL_EPOCH_MALFORMED", "epoch token is not canonical"
            ) from exc
        if state not in {"OPEN", "CLOSED"}:
            raise KillConflictError(
                "KILL_EPOCH_MALFORMED", "epoch state is invalid"
            )
        if Store._kill_epoch_token(epoch, state) != str(value):
            raise KillConflictError(
                "KILL_EPOCH_MALFORMED", "epoch token is not canonical"
            )
        return epoch, state

    def _active_kill_epoch(self, *, require_open: bool = True) -> KillEvidenceEpoch:
        token = self.get_meta(KILL_EPOCH_ACTIVE_KEY)
        if token is None:
            raise KillConflictError(
                "KILL_EPOCH_INACTIVE", "no durable kill epoch is active"
            )
        epoch, state = self._parse_kill_epoch_token(token)
        if require_open and state != "OPEN":
            raise KillConflictError(
                "KILL_EPOCH_CLOSED", "the active epoch is already closed"
            )
        return epoch

    def _coerce_kill_epoch(
        self,
        epoch: KillEvidenceEpoch | None,
        *,
        episode_id: str | None = None,
        require_open: bool = True,
    ) -> KillEvidenceEpoch:
        resolved = (
            self._active_kill_epoch(require_open=require_open)
            if epoch is None
            else epoch
        )
        if episode_id is not None and resolved.episode_id != str(episode_id):
            raise KillConflictError(
                "KILL_EPOCH_STALE_WRITE", "episode does not match epoch"
            )
        return resolved

    def _assert_kill_epoch_in_tx(
        self, epoch: KillEvidenceEpoch, *, require_open: bool = True
    ) -> str:
        row = self.conn.execute(
            "SELECT value FROM meta WHERE key=?", (KILL_EPOCH_ACTIVE_KEY,)
        ).fetchone()
        if row is None:
            raise KillConflictError(
                "KILL_EPOCH_STALE_WRITE", "active epoch is missing"
            )
        expected = self._kill_epoch_token(
            epoch, "OPEN" if require_open else "CLOSED"
        )
        if str(row["value"]) != expected:
            raise KillConflictError(
                "KILL_EPOCH_STALE_WRITE", "epoch compare-and-set rejected"
            )
        request = self.conn.execute(
            "SELECT epoch_token,ack_state FROM kill_requests WHERE episode_id=?",
            (epoch.episode_id,),
        ).fetchone()
        if (
            request is None
            or str(request["epoch_token"]) != expected
            or str(request["ack_state"]) != "PENDING"
        ):
            raise KillConflictError(
                "KILL_EPOCH_STALE_WRITE", "request epoch changed"
            )
        return expected

    def assert_kill_epoch_active(self, epoch: KillEvidenceEpoch) -> None:
        self._require_kill_schema()
        self._assert_kill_epoch_in_tx(epoch)

    def _record_stale_epoch_rejection(
        self, epoch: KillEvidenceEpoch, operation: str
    ) -> None:
        try:
            request = self.conn.execute(
                "SELECT run_id FROM kill_requests WHERE episode_id=?",
                (epoch.episode_id,),
            ).fetchone()
            if request is None:
                return
            now = _to_iso(self._clock()) or ""
            self.conn.execute("BEGIN IMMEDIATE")
            self._insert_event_in_tx(
                str(request["run_id"]),
                now,
                "WARN",
                "KILL_EPOCH_STALE_WRITE_REJECTED",
                (
                    f"episode={epoch.episode_id};attempt={epoch.attempt_no};"
                    f"process={epoch.process_uid};operation={operation}"
                ),
            )
            self.conn.commit()
        except Exception:
            self.conn.rollback()

    def open_kill_epoch(
        self,
        *,
        run_id: str,
        symbol: str,
        flatten_requested: bool,
        policy_version: str,
        process_uid: str,
        opened_ts_monotonic: float,
    ) -> tuple[dict[str, Any], KillEvidenceEpoch]:
        self._require_kill_schema()
        safe_run = str(run_id).strip()
        safe_symbol = str(symbol).strip().upper()
        safe_policy = str(policy_version).strip()
        safe_process = str(process_uid).strip()
        if not safe_run or not safe_symbol or not safe_policy or not safe_process:
            raise KillConflictError(
                "KILL_REQUEST_MALFORMED",
                "run, symbol, policy and process are required",
            )
        try:
            opened_mono = float(opened_ts_monotonic)
            if not math.isfinite(opened_mono):
                raise ValueError
        except (TypeError, ValueError, OverflowError) as exc:
            raise KillConflictError(
                "KILL_EPOCH_MALFORMED", "monotonic open time is invalid"
            ) from exc
        now = _to_iso(self._clock()) or ""
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            pointer_row = self.conn.execute(
                "SELECT value FROM meta WHERE key=?", (KILL_REQUEST_ACTIVE_KEY,)
            ).fetchone()
            pointer = None if pointer_row is None else str(pointer_row["value"])
            if pointer is not None:
                row = self.conn.execute(
                    "SELECT * FROM kill_requests WHERE episode_id=?", (pointer,)
                ).fetchone()
                if row is None:
                    raise KillConflictError(
                        "KILL_POINTER_DANGLING", "active episode does not resolve"
                    )
                existing = dict(row)
                if (
                    str(existing["run_id"]) != safe_run
                    or str(existing["symbol"]) != safe_symbol
                    or bool(existing["flatten_requested"]) != bool(flatten_requested)
                    or str(existing["policy_version"]) != safe_policy
                    or str(existing["ack_state"]) != "PENDING"
                ):
                    raise KillConflictError(
                        "KILL_REQUEST_CONFLICT",
                        "an incompatible episode is already active",
                    )
                prior_token = str(existing["epoch_token"])
                prior_epoch, _prior_state = self._parse_kill_epoch_token(
                    prior_token
                )
                epoch = KillEvidenceEpoch(
                    episode_id=pointer,
                    attempt_no=prior_epoch.attempt_no + 1,
                    process_uid=safe_process,
                    opened_ts_monotonic=opened_mono,
                )
                token = self._kill_epoch_token(epoch, "OPEN")
                cursor = self.conn.execute(
                    """UPDATE kill_requests
                       SET terminal_state='IN_PROGRESS',
                           terminal_reason='KILL_RECOVERY_REPLAYED',
                           terminal_ts=NULL,
                           safe_checkpoint_id=NULL,
                           safe_checkpoint_ts=NULL,
                           proof_digest=NULL,
                           epoch_token=?
                       WHERE episode_id=? AND ack_state='PENDING'
                         AND epoch_token=?""",
                    (token, pointer, prior_token),
                )
                if cursor.rowcount != 1:
                    raise KillConflictError(
                        "KILL_REQUEST_NOT_ACTIVE",
                        "replay could not invalidate prior proof",
                    )
                epoch_cursor = self.conn.execute(
                    """INSERT INTO meta(key,value) VALUES (?,?)
                       ON CONFLICT(key) DO UPDATE SET value=excluded.value
                       WHERE meta.value=?""",
                    (KILL_EPOCH_ACTIVE_KEY, token, prior_token),
                )
                if epoch_cursor.rowcount != 1:
                    raise KillConflictError(
                        "KILL_EPOCH_OPEN_CONFLICT",
                        "active epoch compare-and-set failed",
                    )
                self.conn.execute(
                    "INSERT INTO meta(key,value) VALUES ('app_state','KILLED') "
                    "ON CONFLICT(key) DO UPDATE SET value=excluded.value"
                )
                self._insert_event_in_tx(
                    safe_run,
                    now,
                    "WARN",
                    "KILL_EPISODE_REPLAYED",
                    f"episode={pointer};prior_state={existing['terminal_state']}",
                )
                self.conn.commit()
                replayed = self.conn.execute(
                    "SELECT * FROM kill_requests WHERE episode_id=?", (pointer,)
                ).fetchone()
                return dict(replayed), epoch
            request_count = int(
                self.conn.execute("SELECT COUNT(*) FROM kill_requests").fetchone()[0]
            )
            app_row = self.conn.execute(
                "SELECT value FROM meta WHERE key='app_state'"
            ).fetchone()
            if (
                request_count == 0
                and app_row is not None
                and str(app_row["value"]) == "KILLED"
            ):
                raise KillConflictError(
                    "LEGACY_KILLED_EVIDENCE_MISSING",
                    "owner-directed recovery is required",
                )
            generation = int(
                self.conn.execute(
                    "SELECT COALESCE(MAX(generation),0)+1 FROM kill_requests "
                    "WHERE run_id=? AND symbol=?",
                    (safe_run, safe_symbol),
                ).fetchone()[0]
            )
            episode_id = compute_kill_episode_id(
                run_id=safe_run,
                symbol=safe_symbol,
                generation=generation,
                flatten_requested=bool(flatten_requested),
                policy_version=safe_policy,
            )
            epoch = KillEvidenceEpoch(
                episode_id=episode_id,
                attempt_no=1,
                process_uid=safe_process,
                opened_ts_monotonic=opened_mono,
            )
            token = self._kill_epoch_token(epoch, "OPEN")
            self.conn.execute(
                """INSERT INTO kill_requests(
                     episode_id,generation,run_id,symbol,flatten_requested,
                     requested_ts,policy_version,epoch_token,
                     terminal_state,terminal_reason,
                     terminal_ts,safe_checkpoint_id,safe_checkpoint_ts,
                     proof_digest,ack_state,ack_ts)
                   VALUES (?,?,?,?,?,?,?,?,'IN_PROGRESS','KILL_LATCHED',
                           NULL,NULL,NULL,NULL,'PENDING',NULL)""",
                (
                    episode_id,
                    generation,
                    safe_run,
                    safe_symbol,
                    int(bool(flatten_requested)),
                    now,
                    safe_policy,
                    token,
                ),
            )
            self.conn.execute(
                "INSERT INTO meta(key,value) VALUES (?,?)",
                (KILL_REQUEST_ACTIVE_KEY, episode_id),
            )
            self.conn.execute(
                "INSERT INTO meta(key,value) VALUES (?,?)",
                (KILL_EPOCH_ACTIVE_KEY, token),
            )
            self.conn.execute(
                "INSERT INTO meta(key,value) VALUES ('app_state','KILLED') "
                "ON CONFLICT(key) DO UPDATE SET value=excluded.value"
            )
            self._insert_event_in_tx(
                safe_run,
                now,
                "WARN",
                "KILL_EPISODE_LATCHED",
                f"episode={episode_id};flatten={int(bool(flatten_requested))}",
            )
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        row = self.conn.execute(
            "SELECT * FROM kill_requests WHERE episode_id=?", (episode_id,)
        ).fetchone()
        return dict(row), epoch

    def begin_kill_episode(
        self,
        *,
        run_id: str,
        symbol: str,
        flatten_requested: bool,
        policy_version: str,
    ) -> dict[str, Any]:
        """Compatibility wrapper; new runtime callers retain the returned epoch."""
        request, _epoch = self.open_kill_epoch(
            run_id=run_id,
            symbol=symbol,
            flatten_requested=flatten_requested,
            policy_version=policy_version,
            process_uid=f"legacy-{id(self):x}",
            opened_ts_monotonic=0.0,
        )
        return request

    def active_kill_request(self) -> dict[str, Any] | None:
        self._require_kill_schema()
        pointer = self.get_meta(KILL_REQUEST_ACTIVE_KEY)
        if pointer is None:
            return None
        row = self.conn.execute(
            "SELECT * FROM kill_requests WHERE episode_id=?", (pointer,)
        ).fetchone()
        if row is None:
            raise KillConflictError(
                "KILL_POINTER_DANGLING", "active episode does not resolve"
            )
        return dict(row)

    def get_kill_request(self, episode_id: str) -> dict[str, Any] | None:
        self._require_kill_schema()
        row = self.conn.execute(
            "SELECT * FROM kill_requests WHERE episode_id=?", (str(episode_id),)
        ).fetchone()
        return None if row is None else dict(row)

    def mark_kill_request_state(
        self,
        episode_id: str | None = None,
        state: str = "",
        reason_code: str = "",
        *,
        epoch: KillEvidenceEpoch | None = None,
    ) -> dict[str, Any]:
        self._require_kill_schema()
        resolved_epoch = self._coerce_kill_epoch(
            epoch, episode_id=episode_id
        )
        stable_episode_id = resolved_epoch.episode_id
        terminal_state = KillTerminalState(str(state))
        safe_reason = self._safe_reason_code(reason_code)
        terminal_ts = (
            _to_iso(self._clock())
            if terminal_state in {
                KillTerminalState.SAFE_FLAT,
                KillTerminalState.SAFE_RETAINED,
            }
            else None
        )
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            token = self._assert_kill_epoch_in_tx(resolved_epoch)
            cursor = self.conn.execute(
                """UPDATE kill_requests
                   SET terminal_state=?, terminal_reason=?, terminal_ts=?,
                       safe_checkpoint_id=NULL, safe_checkpoint_ts=NULL,
                       proof_digest=NULL
                   WHERE episode_id=? AND ack_state='PENDING'
                     AND epoch_token=?""",
                (
                    terminal_state.value,
                    safe_reason,
                    terminal_ts,
                    stable_episode_id,
                    token,
                ),
            )
            if cursor.rowcount != 1:
                raise KillConflictError(
                    "KILL_REQUEST_NOT_ACTIVE", "state update rejected"
                )
            self.conn.commit()
        except Exception as exc:
            self.conn.rollback()
            if (
                isinstance(exc, KillConflictError)
                and exc.reason_code == "KILL_EPOCH_STALE_WRITE"
            ):
                self._record_stale_epoch_rejection(
                    resolved_epoch, "MARK_STATE"
                )
            raise
        return self.get_kill_request(stable_episode_id) or {}

    def reserve_kill_action(
        self,
        *,
        epoch: KillEvidenceEpoch | None = None,
        episode_id: str,
        kind: str,
        target: str,
        qty_lots: int | None,
        cloid: str,
        deadline_ts: datetime | str,
        action_id: str | None = None,
        reserved_ts: datetime | str | None = None,
        exit_side: str | None = None,
    ) -> tuple[bool, dict[str, Any]]:
        self._require_kill_schema()
        resolved_epoch = self._coerce_kill_epoch(
            epoch, episode_id=episode_id
        )
        action_kind = KillActionKind(str(kind))
        safe_target = str(target).strip()
        safe_cloid = str(cloid).strip()
        safe_exit_side = None if exit_side is None else str(exit_side).upper()
        if not safe_target or not safe_cloid:
            raise KillConflictError(
                "KILL_ACTION_MALFORMED", "target and cloid are required"
            )
        if action_kind is KillActionKind.FLATTEN and safe_exit_side not in {"BUY", "SELL"}:
            raise KillConflictError("KILL_FLATTEN_EXIT_SIDE_INVALID", "exit side required")
        if action_kind is KillActionKind.CANCEL and safe_exit_side is not None:
            raise KillConflictError("KILL_CANCEL_EXIT_SIDE_INVALID", "exit side forbidden")
        expected_id = compute_kill_action_id(
            episode_id=str(episode_id),
            kind=action_kind.value,
            target=safe_target,
            qty_lots=qty_lots,
        )
        expected_cloid = (
            safe_target
            if action_kind is KillActionKind.CANCEL
            else compute_kill_action_cloid(expected_id)
        )
        if safe_cloid != expected_cloid:
            raise KillConflictError(
                "KILL_ACTION_CLOID_CONFLICT",
                f"kind={action_kind.value}",
            )
        stable_id = expected_id if action_id is None else str(action_id)
        reserved = _to_iso(reserved_ts) or _to_iso(self._clock()) or ""
        deadline = _to_iso(deadline_ts)
        if deadline is None:
            raise KillConflictError(
                "KILL_ACTION_DEADLINE_INVALID", "deadline is required"
            )
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            self._assert_kill_epoch_in_tx(resolved_epoch)
            existing = self.conn.execute(
                "SELECT * FROM kill_actions WHERE action_id=?", (stable_id,)
            ).fetchone()
            if existing is not None:
                row = dict(existing)
                if (
                    stable_id != expected_id
                    or str(row["episode_id"]) != str(episode_id)
                    or str(row["kind"]) != action_kind.value
                    or str(row["target"]) != safe_target
                    or row["qty_lots"] != qty_lots
                    or str(row["cloid"]) != safe_cloid
                    or row["exit_side"] != safe_exit_side
                ):
                    raise KillConflictError(
                        "KILL_ACTION_IDENTITY_CONFLICT",
                        f"action_id={stable_id}",
                    )
                self.conn.commit()
                return True, row
            if stable_id != expected_id:
                raise KillConflictError(
                    "KILL_ACTION_IDENTITY_CONFLICT",
                    f"action_id={stable_id}",
                )
            alias = self.conn.execute(
                "SELECT action_id FROM kill_actions WHERE lower(cloid)=lower(?)",
                (safe_cloid,),
            ).fetchone()
            if alias is not None:
                raise KillConflictError(
                    "KILL_ACTION_CLOID_ALIAS_CONFLICT",
                    f"cloid={safe_cloid}",
                )
            self.conn.execute(
                """INSERT INTO kill_actions(
                     action_id,episode_id,kind,target,qty_lots,cloid,
                     exit_side,reserved_ts,deadline_ts,current_outcome)
                   VALUES (?,?,?,?,?,?,?,?,?,'RESERVED')""",
                (
                    stable_id,
                    str(episode_id),
                    action_kind.value,
                    safe_target,
                    qty_lots,
                    safe_cloid,
                    safe_exit_side,
                    reserved,
                    deadline,
                ),
            )
            self._append_kill_action_event_in_tx(
                epoch=resolved_epoch,
                action_id=stable_id,
                status="RESERVED",
                evidence_source="LOCAL",
                reason_code=f"{action_kind.value}_RESERVED",
                evidence={"target": safe_target, "qty_lots": qty_lots, "exit_side": safe_exit_side},
                observed_ts=reserved,
            )
            self.conn.commit()
        except Exception as exc:
            self.conn.rollback()
            if (
                isinstance(exc, KillConflictError)
                and exc.reason_code == "KILL_EPOCH_STALE_WRITE"
            ):
                self._record_stale_epoch_rejection(
                    resolved_epoch, "RESERVE_ACTION"
                )
            raise
        return False, self.get_kill_action(stable_id) or {}

    def _append_kill_action_event_in_tx(
        self,
        *,
        epoch: KillEvidenceEpoch | None = None,
        action_id: str,
        status: str,
        evidence_source: str,
        reason_code: str,
        evidence: Mapping[str, Any],
        observed_ts: str,
    ) -> None:
        if status not in {
            "RESERVED", "SENT", "APPLIED", "NOT_APPLIED", "UNKNOWN", "EVIDENCE"
        }:
            raise KillConflictError("KILL_EVENT_STATUS_INVALID", status)
        payload_data = dict(evidence)
        if epoch is not None:
            payload_data["epoch"] = epoch.as_payload()
        payload = _canonical_json(payload_data)
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        seq = int(
            self.conn.execute(
                "SELECT COALESCE(MAX(seq),0)+1 FROM kill_action_events "
                "WHERE action_id=?",
                (str(action_id),),
            ).fetchone()[0]
        )
        self.conn.execute(
            """INSERT INTO kill_action_events(
                 action_id,seq,status,evidence_source,reason_code,
                 evidence_json,evidence_digest,observed_ts)
               VALUES (?,?,?,?,?,?,?,?)""",
            (
                str(action_id),
                seq,
                status,
                str(evidence_source) or "LOCAL",
                self._safe_reason_code(reason_code),
                payload,
                digest,
                observed_ts,
            ),
        )

    def _fold_kill_action_outcome_locked(self, action_id: str) -> str:
        statuses = [
            str(row["status"])
            for row in self.conn.execute(
                "SELECT status FROM kill_action_events WHERE action_id=? "
                "ORDER BY seq",
                (str(action_id),),
            ).fetchall()
        ]
        outcome = "RESERVED"
        for status in statuses:
            if status == "UNKNOWN" and outcome not in {"APPLIED", "NOT_APPLIED"}:
                outcome = "UNKNOWN"
            elif status == "NOT_APPLIED":
                outcome = "NOT_APPLIED" if outcome != "APPLIED" else "UNKNOWN"
            elif status == "APPLIED":
                outcome = "APPLIED"
        return outcome

    def record_kill_action_event(
        self,
        *,
        epoch: KillEvidenceEpoch | None = None,
        action_id: str,
        status: str,
        reason_code: str,
        evidence_source: str = "BROKER",
        evidence: Mapping[str, Any] | None = None,
        observed_ts: datetime | str | None = None,
        local_order_terminal_status: str | None = None,
        flatten_order: Mapping[str, Any] | None = None,
        flatten_fills: Sequence[Mapping[str, Any]] | None = None,
    ) -> dict[str, Any]:
        self._require_kill_schema()
        resolved_epoch = self._coerce_kill_epoch(epoch)
        now = _to_iso(observed_ts) or _to_iso(self._clock()) or ""
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            self._assert_kill_epoch_in_tx(resolved_epoch)
            action = self.conn.execute(
                "SELECT * FROM kill_actions WHERE action_id=?", (str(action_id),)
            ).fetchone()
            if action is None:
                raise KillConflictError(
                    "KILL_ACTION_NOT_FOUND", f"action_id={action_id}"
                )
            if (flatten_order is None) != (flatten_fills is None):
                raise KillConflictError(
                    "KILL_FLATTEN_PROOF_INVALID",
                    "terminal order and fill evidence must be recorded together",
                )
            if flatten_order is not None and (
                str(action["kind"]) != KillActionKind.FLATTEN.value
                or str(status) != "APPLIED"
                or not flatten_fills
            ):
                raise KillConflictError(
                    "KILL_FLATTEN_PROOF_INVALID",
                    "a flatten order requires an APPLIED flatten event",
                )
            self._append_kill_action_event_in_tx(
                epoch=resolved_epoch,
                action_id=str(action_id),
                status=str(status),
                evidence_source=evidence_source,
                reason_code=reason_code,
                evidence=evidence or {},
                observed_ts=now,
            )
            folded = self._fold_kill_action_outcome_locked(str(action_id))
            self.conn.execute(
                "UPDATE kill_actions SET current_outcome=? WHERE action_id=?",
                (folded, str(action_id)),
            )
            if local_order_terminal_status is not None:
                cursor = self.conn.execute(
                    """UPDATE orders SET status=?, ts_last=?
                       WHERE cloid=?""",
                    (
                        str(local_order_terminal_status),
                        now,
                        str(action["target"]),
                    ),
                )
                if cursor.rowcount != 1:
                    raise KillConflictError(
                        "KILL_LOCAL_ORDER_MISSING",
                        f"cloid={action['target']}",
                    )
            if flatten_order is not None:
                row = dict(flatten_order)
                cloid = str(action["cloid"])
                try:
                    oid = int(row["oid"])
                    trade_id = int(row["trade_id"])
                    qty = float(row["qty"])
                    filled_qty = float(row["filled_qty"])
                except (KeyError, TypeError, ValueError, OverflowError) as exc:
                    raise KillConflictError(
                        "KILL_FLATTEN_ORDER_MALFORMED",
                        "terminal fill fields are invalid",
                    ) from exc
                decision_uid = str(row.get("decision_uid") or "").strip()
                symbol = str(row.get("symbol") or "").strip()
                if (
                    isinstance(row.get("oid"), bool)
                    or not decision_uid
                    or symbol != str(action["target"])
                    or not math.isfinite(qty)
                    or not math.isfinite(filled_qty)
                    or qty <= 0
                    or filled_qty <= 0
                    or filled_qty > qty
                ):
                    raise KillConflictError(
                        "KILL_FLATTEN_ORDER_MALFORMED",
                        "terminal fill fields are invalid",
                    )
                existing = self.conn.execute(
                    "SELECT * FROM orders WHERE cloid=?", (cloid,)
                ).fetchone()
                normalized = (
                    oid,
                    str(action["episode_id"]),
                    str(action_id),
                    _canonical_json({
                        "symbol": symbol,
                        "role": "KILL_FLATTEN",
                        "reduce_only": True,
                        "side": str(action["exit_side"]),
                    }),
                    decision_uid,
                    trade_id,
                    "KILL_FLATTEN",
                    "FILLED",
                    qty,
                    filled_qty,
                    now,
                    now,
                )
                if existing is None:
                    self.conn.execute(
                        """INSERT INTO orders(
                             cloid,oid,group_id,order_ref,order_json,
                             decision_uid,trade_id,role,status,qty,filled_qty,
                             avg_fill_px,ts_submit,ts_last)
                           VALUES (?,?,?,?,?,?,?,?,?,?,?,NULL,?,?)""",
                        (cloid, *normalized),
                    )
                elif (
                    str(existing["role"]) != "KILL_FLATTEN"
                    or int(existing["trade_id"]) != trade_id
                    or float(existing["qty"]) != qty
                    or float(existing["filled_qty"]) != filled_qty
                    or int(existing["oid"]) != oid
                    or str(existing["group_id"]) != str(action["episode_id"])
                    or str(existing["order_ref"]) != str(action_id)
                    or str(existing["decision_uid"]) != decision_uid
                ):
                    raise KillConflictError(
                        "KILL_FLATTEN_ORDER_CONFLICT", f"cloid={cloid}"
                    )
                total_qty = Decimal("0")
                seen_fill_ids: set[str] = set()
                for raw_fill in flatten_fills or ():
                    fill = dict(raw_fill)
                    fill_id = str(fill.get("fill_id") or "").strip()
                    fill_ts = _to_iso(fill.get("fill_ts"))
                    try:
                        fill_qty = float(fill["qty"])
                        fill_px = float(fill["px"])
                        fill_fee = float(fill.get("fee", 0.0))
                        fill_funding = float(fill.get("funding", 0.0))
                    except (
                        KeyError,
                        TypeError,
                        ValueError,
                        OverflowError,
                    ) as exc:
                        raise KillConflictError(
                            "KILL_FLATTEN_FILL_MALFORMED",
                            "terminal fill fields are invalid",
                        ) from exc
                    if (
                        not fill_id
                        or fill_id in seen_fill_ids
                        or fill_ts is None
                        or not math.isfinite(fill_qty)
                        or not math.isfinite(fill_px)
                        or not math.isfinite(fill_fee)
                        or not math.isfinite(fill_funding)
                        or fill_qty <= 0
                        or fill_px <= 0
                    ):
                        raise KillConflictError(
                            "KILL_FLATTEN_FILL_MALFORMED",
                            "terminal fill fields are invalid",
                        )
                    seen_fill_ids.add(fill_id)
                    total_qty += Decimal(str(fill_qty))
                    normalized_fill = (
                        fill_id,
                        cloid,
                        decision_uid,
                        fill_ts,
                        fill_qty,
                        fill_px,
                        fill_fee,
                        fill_funding,
                    )
                    cursor = self.conn.execute(
                        """INSERT OR IGNORE INTO fills(
                             fill_id,cloid,decision_uid,fill_ts,qty,px,fee,funding)
                           VALUES (?,?,?,?,?,?,?,?)""",
                        normalized_fill,
                    )
                    if cursor.rowcount != 1:
                        prior = self.conn.execute(
                            """SELECT fill_id,cloid,decision_uid,fill_ts,
                                      qty,px,fee,funding
                               FROM fills WHERE fill_id=?""",
                            (fill_id,),
                        ).fetchone()
                        prior_normalized = (
                            str(prior["fill_id"]),
                            str(prior["cloid"]),
                            str(prior["decision_uid"]),
                            str(prior["fill_ts"]),
                            float(prior["qty"]),
                            float(prior["px"]),
                            float(prior["fee"] or 0.0),
                            float(prior["funding"] or 0.0),
                        ) if prior is not None else None
                        if prior_normalized != normalized_fill:
                            raise KillConflictError(
                                "KILL_FLATTEN_FILL_CONFLICT",
                                f"fill_id={fill_id}",
                            )
                if total_qty != Decimal(str(filled_qty)):
                    raise KillConflictError(
                        "KILL_FLATTEN_FILL_TOTAL_CONFLICT",
                        f"cloid={cloid}",
                    )
            self.conn.commit()
        except Exception as exc:
            self.conn.rollback()
            if (
                isinstance(exc, KillConflictError)
                and exc.reason_code == "KILL_EPOCH_STALE_WRITE"
            ):
                self._record_stale_epoch_rejection(
                    resolved_epoch, "RECORD_ACTION_EVENT"
                )
            raise
        return self.get_kill_action(action_id) or {}

    def get_kill_action(self, action_id: str) -> dict[str, Any] | None:
        self._require_kill_schema()
        row = self.conn.execute(
            "SELECT * FROM kill_actions WHERE action_id=?", (str(action_id),)
        ).fetchone()
        return None if row is None else dict(row)

    def kill_actions_for_episode(
        self, episode_id: str, kind: str | None = None
    ) -> list[dict[str, Any]]:
        self._require_kill_schema()
        if kind is None:
            return self._rows(
                "SELECT * FROM kill_actions WHERE episode_id=? "
                "ORDER BY reserved_ts,action_id",
                (str(episode_id),),
            )
        return self._rows(
            "SELECT * FROM kill_actions WHERE episode_id=? AND kind=? "
            "ORDER BY reserved_ts,action_id",
            (str(episode_id), KillActionKind(str(kind)).value),
        )

    def kill_action_events(self, action_id: str) -> list[dict[str, Any]]:
        self._require_kill_schema()
        return self._rows(
            "SELECT * FROM kill_action_events WHERE action_id=? ORDER BY seq",
            (str(action_id),),
        )

    def observe_kill_action_clock(
        self,
        *,
        epoch: KillEvidenceEpoch | None = None,
        action_id: str,
        observed_ts: datetime | str,
    ) -> bool:
        """Append the latest safe wall observation; reject clock rollback."""
        self._require_kill_schema()
        resolved_epoch = self._coerce_kill_epoch(epoch)
        now = _to_iso(observed_ts)
        if now is None:
            return False
        try:
            current = datetime.fromisoformat(now)
            if current.tzinfo is None:
                current = current.replace(tzinfo=UTC)
            current = current.astimezone(UTC)
        except (TypeError, ValueError):
            return False
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            self._assert_kill_epoch_in_tx(resolved_epoch)
            action = self.conn.execute(
                "SELECT action_id FROM kill_actions WHERE action_id=?",
                (str(action_id),),
            ).fetchone()
            if action is None:
                raise KillConflictError(
                    "KILL_ACTION_NOT_FOUND", f"action_id={action_id}"
                )
            observations = self.conn.execute(
                """SELECT observed_ts FROM kill_action_events
                   WHERE action_id=?""",
                (str(action_id),),
            ).fetchall()
            if not observations:
                raise KillConflictError(
                    "KILL_ACTION_OBSERVATION_MISSING",
                    f"action_id={action_id}",
                )
            prior_values: list[datetime] = []
            for observation in observations:
                prior = datetime.fromisoformat(str(observation["observed_ts"]))
                if prior.tzinfo is None:
                    prior = prior.replace(tzinfo=UTC)
                prior_values.append(prior.astimezone(UTC))
            if current < max(prior_values):
                self.conn.commit()
                return False
            self._append_kill_action_event_in_tx(
                epoch=resolved_epoch,
                action_id=str(action_id),
                status="EVIDENCE",
                evidence_source="LOCAL",
                reason_code="KILL_ACTION_CLOCK_OBSERVED",
                evidence={"observed_ts": now},
                observed_ts=now,
            )
            self.conn.commit()
            return True
        except Exception as exc:
            self.conn.rollback()
            if (
                isinstance(exc, KillConflictError)
                and exc.reason_code == "KILL_EPOCH_STALE_WRITE"
            ):
                self._record_stale_epoch_rejection(
                    resolved_epoch, "OBSERVE_ACTION_CLOCK"
                )
            raise

    def kill_owned_position_rows(self, symbol: str) -> list[dict[str, Any]]:
        self._require_kill_schema()
        rows = self._rows(
            """SELECT o.*, json_extract(o.order_json,'$.symbol') AS symbol,
                      t.direction AS trade_direction,
                      t.run_id AS trade_run_id,
                      t.coin AS trade_coin,
                      t.entry_decision_uid AS trade_entry_decision_uid,
                      COALESCE(SUM(f.qty),0) AS durable_fill_qty,
                      COUNT(f.fill_id) AS durable_fill_count,
                      GROUP_CONCAT(DISTINCT f.fill_id) AS durable_fill_ids,
                      GROUP_CONCAT(DISTINCT f.decision_uid) AS durable_fill_decision_uids,
                      COALESCE(SUM(CASE
                        WHEN f.decision_uid IS NULL
                          OR length(trim(f.decision_uid))=0
                          OR f.decision_uid != o.decision_uid THEN 1
                        ELSE 0 END),0) AS durable_fill_identity_conflicts
               FROM orders o LEFT JOIN trades t ON t.trade_id=o.trade_id
               LEFT JOIN fills f ON f.cloid=o.cloid
               WHERE (o.filled_qty > 0 OR f.fill_id IS NOT NULL)
                 AND json_extract(o.order_json,'$.symbol')=?
               GROUP BY o.cloid
               ORDER BY o.cloid""",
            (str(symbol),),
        )
        for row in rows:
            row["kill_direct_fill_proven"] = False
            row["kill_action_qty_lots"] = None
            row["kill_action_exit_side"] = None
            if str(row.get("role") or "") != "KILL_FLATTEN":
                continue
            proofs = self._rows(
                """SELECT a.qty_lots,a.exit_side,e.evidence_json
                   FROM kill_actions a
                   JOIN kill_action_events e ON e.action_id=a.action_id
                   WHERE a.action_id=? AND a.episode_id=? AND a.cloid=?
                     AND a.kind='FLATTEN' AND a.current_outcome='APPLIED'
                     AND e.status='APPLIED'
                     AND e.reason_code IN
                       ('FLATTEN_TERMINAL_QUERY','FLATTEN_PARTIAL')
                   ORDER BY e.seq DESC""",
                (
                    str(row.get("order_ref") or ""),
                    str(row.get("group_id") or ""),
                    str(row.get("cloid") or ""),
                ),
            )
            for proof in proofs:
                try:
                    payload = json.loads(str(proof["evidence_json"]))
                    query = payload["query"]
                    exact = (
                        isinstance(query, Mapping)
                        and query.get("known") is True
                        and query.get("terminal") is True
                        and int(query["oid"]) == int(row["oid"])
                        and str(query["cloid"]) == str(row["cloid"])
                        and str(query["symbol"]) == str(symbol)
                        and float(query["filled_size"]) == float(row["filled_qty"])
                    )
                except (KeyError, TypeError, ValueError, OverflowError):
                    exact = False
                if exact:
                    row["kill_direct_fill_proven"] = True
                    row["kill_action_qty_lots"] = int(proof["qty_lots"])
                    row["kill_action_exit_side"] = str(proof["exit_side"])
                    break
        return rows

    def kill_capture_start_ms(self, run_id: str, symbol: str) -> int | None:
        """Earliest durable run/fill bound needed for positive ownership proof."""
        candidates: list[datetime] = []
        started = self.run_started_ts(str(run_id))
        if started is not None:
            candidates.append(started)
        row = self.conn.execute(
            """SELECT MIN(f.fill_ts) AS first_fill
               FROM fills f
               JOIN orders o ON o.cloid=f.cloid
               JOIN trades t ON t.trade_id=o.trade_id
               WHERE t.run_id=? AND t.coin=?
                 AND json_extract(o.order_json,'$.symbol')=?""",
            (str(run_id), str(symbol), str(symbol)),
        ).fetchone()
        if row is not None and row["first_fill"] is not None:
            try:
                first = datetime.fromisoformat(str(row["first_fill"]))
                if first.tzinfo is None:
                    first = first.replace(tzinfo=UTC)
                candidates.append(first.astimezone(UTC))
            except (TypeError, ValueError):
                return None
        if not candidates:
            return None
        return int(min(candidates).astimezone(UTC).timestamp() * 1000)

    def bind_kill_terminal_proof(
        self,
        *,
        epoch: KillEvidenceEpoch | None = None,
        episode_id: str | None = None,
        terminal_state: str,
        reason_code: str,
        checkpoint_id: str,
        proof: Mapping[str, Any],
    ) -> dict[str, Any]:
        self._require_kill_schema()
        resolved_epoch = self._coerce_kill_epoch(
            epoch, episode_id=episode_id
        )
        stable_episode_id = resolved_epoch.episode_id
        state = KillTerminalState(str(terminal_state))
        if state not in {
            KillTerminalState.SAFE_FLAT,
            KillTerminalState.SAFE_RETAINED,
        }:
            raise KillConflictError(
                "KILL_SAFE_STATE_INVALID", state.value
            )
        now = _to_iso(self._clock()) or ""
        proof_json = _canonical_json(dict(proof))
        digest = hashlib.sha256(proof_json.encode("utf-8")).hexdigest()
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            token = self._assert_kill_epoch_in_tx(resolved_epoch)
            checkpoint = self.conn.execute(
                "SELECT accepted_ts FROM reconcile_checkpoints "
                "WHERE checkpoint_id=?",
                (str(checkpoint_id),),
            ).fetchone()
            if (
                checkpoint is None
                or self.get_meta(RECONCILE_CHECKPOINT_POINTER_KEY)
                != str(checkpoint_id)
            ):
                raise KillConflictError(
                    "KILL_CHECKPOINT_NOT_CURRENT",
                    "safe proof is not pointed",
                )
            if self.get_meta(KILL_REQUEST_ACTIVE_KEY) != stable_episode_id:
                raise KillConflictError(
                    "KILL_REQUEST_NOT_ACTIVE", "proof episode is not active"
                )
            cursor = self.conn.execute(
                """UPDATE kill_requests
                   SET terminal_state=?,terminal_reason=?,terminal_ts=?,
                       safe_checkpoint_id=?,safe_checkpoint_ts=?,proof_digest=?
                   WHERE episode_id=? AND ack_state='PENDING'
                     AND epoch_token=?""",
                (
                    state.value,
                    self._safe_reason_code(reason_code),
                    now,
                    str(checkpoint_id),
                    str(checkpoint["accepted_ts"]),
                    digest,
                    stable_episode_id,
                    token,
                ),
            )
            if cursor.rowcount != 1:
                raise KillConflictError(
                    "KILL_REQUEST_NOT_ACTIVE", "proof update rejected"
                )
            self.conn.commit()
        except Exception as exc:
            self.conn.rollback()
            if (
                isinstance(exc, KillConflictError)
                and exc.reason_code == "KILL_EPOCH_STALE_WRITE"
            ):
                self._record_stale_epoch_rejection(
                    resolved_epoch, "BIND_PROOF"
                )
            raise
        return self.get_kill_request(stable_episode_id) or {}

    def close_kill_epoch(
        self, *, epoch: KillEvidenceEpoch
    ) -> dict[str, Any]:
        """CAS-close a proof-bound epoch; only then can ACK consume it."""
        self._require_kill_schema()
        now = _to_iso(self._clock()) or ""
        open_token = self._kill_epoch_token(epoch, "OPEN")
        closed_token = self._kill_epoch_token(epoch, "CLOSED")
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            self._assert_kill_epoch_in_tx(epoch)
            request = self.conn.execute(
                "SELECT * FROM kill_requests WHERE episode_id=?",
                (epoch.episode_id,),
            ).fetchone()
            if (
                request is None
                or str(request["terminal_state"])
                not in {"SAFE_FLAT", "SAFE_RETAINED"}
                or request["safe_checkpoint_id"] is None
                or request["safe_checkpoint_ts"] is None
                or request["proof_digest"] is None
            ):
                raise KillConflictError(
                    "KILL_EPOCH_PROOF_MISSING",
                    "terminal proof must be bound before close",
                )
            request_cursor = self.conn.execute(
                """UPDATE kill_requests SET epoch_token=?
                   WHERE episode_id=? AND ack_state='PENDING'
                     AND epoch_token=?""",
                (closed_token, epoch.episode_id, open_token),
            )
            epoch_cursor = self.conn.execute(
                "UPDATE meta SET value=? WHERE key=? AND value=?",
                (closed_token, KILL_EPOCH_ACTIVE_KEY, open_token),
            )
            if request_cursor.rowcount != 1 or epoch_cursor.rowcount != 1:
                raise KillConflictError(
                    "KILL_EPOCH_STALE_WRITE",
                    "epoch close compare-and-set rejected",
                )
            self._insert_event_in_tx(
                str(request["run_id"]),
                now,
                "WARN",
                "KILL_EPOCH_CLOSED",
                (
                    f"episode={epoch.episode_id};attempt={epoch.attempt_no};"
                    f"process={epoch.process_uid}"
                ),
            )
            self.conn.commit()
        except Exception as exc:
            self.conn.rollback()
            if (
                isinstance(exc, KillConflictError)
                and exc.reason_code == "KILL_EPOCH_STALE_WRITE"
            ):
                self._record_stale_epoch_rejection(epoch, "CLOSE_EPOCH")
            raise
        return self.get_kill_request(epoch.episode_id) or {}

    def acknowledge_kill_evidence(
        self, *, now: datetime, max_age_s: float
    ) -> dict[str, Any]:
        self._require_kill_schema()
        ack_ts = _to_iso(now) or ""
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            pointer = self.get_meta(KILL_REQUEST_ACTIVE_KEY)
            if pointer is None:
                raise KillConflictError(
                    "KILL_EVIDENCE_MISSING", "no active kill episode"
                )
            request_row = self.conn.execute(
                "SELECT * FROM kill_requests WHERE episode_id=?", (pointer,)
            ).fetchone()
            if request_row is None:
                raise KillConflictError(
                    "KILL_POINTER_DANGLING", "active episode does not resolve"
                )
            request = dict(request_row)
            epoch_token = str(request.get("epoch_token") or "")
            _epoch, epoch_state = self._parse_kill_epoch_token(epoch_token)
            if (
                epoch_state != "CLOSED"
                or self.get_meta(KILL_EPOCH_ACTIVE_KEY) != epoch_token
            ):
                raise KillConflictError(
                    "KILL_EPOCH_NOT_CLOSED",
                    "ACK requires the active closed proof epoch",
                )
            safe_state = str(request["terminal_state"])
            if safe_state not in {"SAFE_FLAT", "SAFE_RETAINED"}:
                raise KillConflictError(
                    "KILL_NOT_SAFE", str(request["terminal_reason"])
                )
            checkpoint_id = request["safe_checkpoint_id"]
            checkpoint_ts = request["safe_checkpoint_ts"]
            proof_digest = str(request["proof_digest"] or "")
            checkpoint = (
                self.conn.execute(
                    """SELECT accepted_ts FROM reconcile_checkpoints
                       WHERE checkpoint_id=?""",
                    (str(checkpoint_id),),
                ).fetchone()
                if checkpoint_id is not None
                else None
            )
            if (
                self.get_meta("app_state") != "KILLED"
                or checkpoint_id is None
                or checkpoint is None
                or checkpoint_ts is None
                or str(checkpoint_ts) != str(checkpoint["accepted_ts"])
                or len(proof_digest) != 64
                or any(
                    char not in "0123456789abcdef"
                    for char in proof_digest.lower()
                )
                or not self.full_reconcile_ready(now=now, max_age_s=max_age_s)
            ):
                raise KillConflictError(
                    "KILL_SAFE_PROOF_STALE",
                    "fresh current reconcile is required",
                )
            if self.get_meta(RECONCILE_CHECKPOINT_POINTER_KEY) != str(
                checkpoint_id
            ):
                raise KillConflictError(
                    "KILL_SAFE_PROOF_MOVED", "checkpoint pointer changed"
                )
            if self.get_meta(KILL_REQUEST_ACTIVE_KEY) != str(
                request["episode_id"]
            ):
                raise KillConflictError(
                    "KILL_REQUEST_NOT_ACTIVE", "active pointer changed"
                )
            cursor = self.conn.execute(
                """UPDATE kill_requests SET ack_state='ACKNOWLEDGED',ack_ts=?
                   WHERE episode_id=? AND ack_state='PENDING'
                     AND terminal_state=?
                     AND safe_checkpoint_id=?
                     AND safe_checkpoint_ts=?
                     AND proof_digest=?""",
                (
                    ack_ts,
                    str(request["episode_id"]),
                    safe_state,
                    str(checkpoint_id),
                    str(checkpoint_ts),
                    proof_digest,
                ),
            )
            if cursor.rowcount != 1:
                raise KillConflictError(
                    "KILL_ACK_CONFLICT",
                    "safe state or proof changed during acknowledgement",
                )
            cleared = self.conn.execute(
                "DELETE FROM meta WHERE key=? AND value=?",
                (KILL_REQUEST_ACTIVE_KEY, str(request["episode_id"])),
            )
            if cleared.rowcount != 1:
                raise KillConflictError(
                    "KILL_ACK_CONFLICT", "active pointer changed"
                )
            epoch_cleared = self.conn.execute(
                "DELETE FROM meta WHERE key=? AND value=?",
                (KILL_EPOCH_ACTIVE_KEY, epoch_token),
            )
            if epoch_cleared.rowcount != 1:
                raise KillConflictError(
                    "KILL_ACK_CONFLICT", "epoch pointer changed"
                )
            self.conn.execute(
                "INSERT INTO meta(key,value) VALUES ('app_state','DISARMED') "
                "ON CONFLICT(key) DO UPDATE SET value=excluded.value"
            )
            self._insert_event_in_tx(
                str(request["run_id"]),
                ack_ts,
                "WARN",
                "KILL_ACKNOWLEDGED",
                f"episode={request['episode_id']};checkpoint={checkpoint_id}",
            )
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        return self.get_kill_request(str(request["episode_id"])) or {}

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

    def list_fills_for_order(self, cloid: str) -> list[dict[str, Any]]:
        """Return immutable local fill evidence for one durable order."""
        return self._rows(
            """
            SELECT fill_id, cloid, decision_uid, fill_ts, qty, px, fee, funding
            FROM fills WHERE cloid = ? ORDER BY fill_ts, fill_id
            """,
            (cloid,),
        )

    def list_all_fills(self) -> list[dict[str, Any]]:
        """Return the complete immutable local fill ledger."""
        return self._rows(
            """
            SELECT fill_id, cloid, decision_uid, fill_ts, qty, px, fee, funding
            FROM fills ORDER BY fill_ts, fill_id
            """
        )

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

    # ------------------------------------------------------------------
    # TS-P1-005 reconciliation ledger access
    # ------------------------------------------------------------------

    # Derived, never hand-listed: every non-terminal `OrderState`, every
    # non-terminal raw alias spelling, plus the accepted legacy live spellings
    # (`ACCEPTED`, `RESTING`, `WAITING_CHILD`). A new non-terminal state or
    # alias therefore cannot silently fall out of this query. See
    # `bridge/engine/types.py` for the derivation.
    _LIVE_LOCAL_ORDER_STATUSES = tuple(sorted(LIVE_DURABLE_ORDER_STATUSES))
    _KNOWN_LOCAL_ORDER_STATUSES = tuple(sorted(KNOWN_DURABLE_ORDER_STATUSES))

    def _decorate_order_rows(self, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        for row in rows:
            try:
                row["symbol"] = str(json.loads(row["order_json"]).get("symbol") or "")
            except (TypeError, ValueError):
                row["symbol"] = ""
        return rows

    def live_local_orders(self) -> list[dict[str, Any]]:
        """Durable local intent rows that should still exist on the exchange."""
        placeholders = ",".join("?" for _ in self._LIVE_LOCAL_ORDER_STATUSES)
        return self._decorate_order_rows(
            self._rows(
                f"SELECT * FROM orders WHERE status IN ({placeholders}) ORDER BY cloid",
                self._LIVE_LOCAL_ORDER_STATUSES,
            )
        )

    def local_orders_with_unknown_status(self) -> list[dict[str, Any]]:
        """Durable order rows whose status is outside the closed status space.

        Such a row is neither provably live nor provably terminal, so it must
        never be dropped from reconciliation: the caller turns it into a
        blocking unknown-state diff.
        """
        placeholders = ",".join("?" for _ in self._KNOWN_LOCAL_ORDER_STATUSES)
        return self._decorate_order_rows(
            self._rows(
                f"SELECT * FROM orders WHERE status NOT IN ({placeholders}) "
                "ORDER BY cloid",
                self._KNOWN_LOCAL_ORDER_STATUSES,
            )
        )

    def pending_reconcile_actions(self) -> list[dict[str, Any]]:
        """Local pending/ambiguous actions that dominate reconciliation.

        TS-P1-003 quarantine and TS-P1-004 recovery rows are *local* authority:
        a reconciliation snapshot observes them, it never resolves them.
        """
        actions: list[dict[str, Any]] = []
        for row in self._rows(
            "SELECT attempt_id, state, reason_code FROM submission_attempts "
            f"WHERE state IN ({','.join('?' for _ in sorted(_QUARANTINE_STATES))}) "
            "ORDER BY attempt_id",
            tuple(sorted(_QUARANTINE_STATES)),
        ):
            actions.append({
                "kind": "SUBMISSION_QUARANTINE",
                "id": str(row["attempt_id"]),
                "state": str(row["state"]),
                "symbol": "",
            })
        if self.partial_protection_enabled():
            terminal = sorted(state.value for state in PARTIAL_TERMINAL_STATES)
            placeholders = ",".join("?" for _ in terminal)
            for row in self._rows(
                f"""SELECT recovery_id, symbol, state FROM partial_fill_recoveries
                    WHERE state NOT IN ({placeholders}) OR state = ?
                    ORDER BY recovery_id""",
                (*terminal, PartialProtectionState.UNPROTECTED_ABORT.value),
            ):
                actions.append({
                    "kind": "PARTIAL_RECOVERY",
                    "id": str(row["recovery_id"]),
                    "state": str(row["state"]),
                    "symbol": str(row["symbol"]),
                })
        return actions

    def full_reconcile_enabled(self) -> bool:
        """True when the v6 ledger or an additive successor is active."""
        return self.get_meta("schema_version") in {
            str(SCHEMA_VERSION_FULL_RECONCILE),
            str(SCHEMA_VERSION_DURABLE_RISK),
            str(SCHEMA_VERSION_EXPOSURE_CONTROLS),
            str(SCHEMA_VERSION_KILL_EVIDENCE),
        }

    def durable_risk_controls_enabled(self) -> bool:
        return self.get_meta("schema_version") in {
            str(SCHEMA_VERSION_DURABLE_RISK),
            str(SCHEMA_VERSION_EXPOSURE_CONTROLS),
            str(SCHEMA_VERSION_KILL_EVIDENCE),
        }

    def exposure_controls_enabled(self) -> bool:
        """True on opt-in schema v8 and its additive v9 successor."""
        return self.get_meta("schema_version") in {
            str(SCHEMA_VERSION_EXPOSURE_CONTROLS),
            str(SCHEMA_VERSION_KILL_EVIDENCE),
        }

    def _require_full_reconcile(self) -> None:
        if not self.full_reconcile_enabled():
            raise ReconcileConflictError(
                "FULL_RECONCILE_SCHEMA_INACTIVE",
                "reconciliation ledger requires schema v6",
            )

    def reserve_reconcile_attempt(
        self,
        *,
        run_id: str,
        started_ts: datetime,
        deadline_s: float,
        max_skew_s: float,
    ) -> str:
        """Durably reserve one attempt *before* any broker I/O begins."""
        self._require_full_reconcile()
        if not run_id:
            raise ReconcileConflictError("RECONCILE_RUN_ID_MISSING", "run_id required")
        if not (deadline_s > 0) or max_skew_s < 0:
            raise ReconcileConflictError(
                "RECONCILE_ENVELOPE_INVALID", "deadline/skew envelope invalid"
            )
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            row = self.conn.execute(
                "SELECT COALESCE(MAX(seq), 0) FROM reconcile_attempts WHERE run_id = ?",
                (run_id,),
            ).fetchone()
            seq = int(row[0]) + 1
            attempt_id = compute_reconcile_attempt_id(
                run_id=run_id, seq=seq, started_ts=started_ts
            )
            self.conn.execute(
                """
                INSERT INTO reconcile_attempts(
                  attempt_id, run_id, seq, state, started_ts, ended_ts, duration_ms,
                  deadline_s, max_skew_s, complete, fresh, canonical_hash, reason_code
                ) VALUES (?, ?, ?, 'COLLECTING', ?, NULL, NULL, ?, ?, 0, 0, NULL, ?)
                """,
                (
                    attempt_id,
                    run_id,
                    seq,
                    _to_iso(started_ts),
                    float(deadline_s),
                    float(max_skew_s),
                    "COLLECTING",
                ),
            )
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        return attempt_id

    def finalize_reconcile_attempt(
        self,
        *,
        attempt_id: str,
        state: ReconcileAttemptState,
        ended_ts: datetime,
        duration_ms: int,
        canonical_hash: str | None,
        reason_code: str,
        components: Sequence[ComponentEvidence] = (),
        diffs: Sequence[ReconcileDiffRecord] = (),
        funding_events: Sequence[FundingEventRecord] = (),
        accepted: bool,
        fresh: bool,
        snapshot_payload: Mapping[str, Any] | None = None,
        coverage_upper_bound_ms: int | None = None,
        risk_policy: DurableRiskPolicy | None = None,
    ) -> str | None:
        """Commit one attempt's whole outcome atomically.

        Snapshot rows, component provenance, the diff, the attempt verdict, the
        immutable checkpoint and the sole latest-accepted pointer share one
        ``BEGIN IMMEDIATE``. Coverage is derived from the accepted FILLS and
        FUNDING component bounds, never from a second mutable pointer.

        Returns the new checkpoint id when the attempt was accepted.
        """
        self._require_full_reconcile()
        if accepted and self.exposure_controls_enabled():
            # TS-P1-008: a v8 store still runs the v7 daily-risk ledger, so the
            # durable policy is required, but acceptance now requires a v3
            # payload that carries the per-position valuation, leverage and
            # directional liquidation evidence the exposure gates consume.
            if not isinstance(risk_policy, DurableRiskPolicy):
                raise ReconcileConflictError(
                    "RISK_POLICY_REQUIRED",
                    "schema v8 acceptance requires an approved durable policy",
                )
            if (snapshot_payload or {}).get("version") != SNAPSHOT_PAYLOAD_VERSION_V3:
                raise ReconcileConflictError(
                    "EXPOSURE_REQUIRES_V3_PAYLOAD",
                    "schema v8 exposure risk requires checkpoint-bound v3 rows",
                )
            if not isinstance(
                (snapshot_payload or {}).get("exposure_policy_version"), str
            ) or not (snapshot_payload or {}).get("exposure_policy_version"):
                raise ReconcileConflictError(
                    "EXPOSURE_POLICY_REQUIRED",
                    "schema v8 acceptance requires a checkpoint-bound exposure policy",
                )
        elif accepted and self.durable_risk_controls_enabled():
            if not isinstance(risk_policy, DurableRiskPolicy):
                raise ReconcileConflictError(
                    "RISK_POLICY_REQUIRED",
                    "schema v7 acceptance requires an approved durable policy",
                )
            if (snapshot_payload or {}).get("version") != SNAPSHOT_PAYLOAD_VERSION_V2:
                raise ReconcileConflictError(
                    "RISK_DAY_REQUIRES_V2_PAYLOAD",
                    "schema v7 daily risk requires checkpoint-bound v2 rows",
                )
        if accepted and state is not ReconcileAttemptState.COMPLETE:
            raise ReconcileConflictError(
                "RECONCILE_ACCEPT_REQUIRES_COMPLETE",
                f"cannot accept attempt in state {state.value}",
            )
        if accepted and not canonical_hash:
            raise ReconcileConflictError(
                "RECONCILE_ACCEPT_REQUIRES_HASH", "accepted attempt needs a hash"
            )
        if accepted and (
            coverage_upper_bound_ms is None
            or isinstance(coverage_upper_bound_ms, bool)
            or not isinstance(coverage_upper_bound_ms, int)
        ):
            # Acceptance *is* the proof that the interval was covered; without a
            # provable upper bound there is nothing to advance and the next
            # capture would have no continuous lower bound.
            raise ReconcileConflictError(
                "RECONCILE_ACCEPT_REQUIRES_COVERAGE",
                "accepted attempt needs a fills/funding coverage upper bound",
            )
        if accepted and not fresh:
            raise ReconcileConflictError(
                "RECONCILE_ACCEPT_REQUIRES_FRESH", "accepted attempt must be fresh"
            )
        if accepted and reason_code != "ACCEPTED":
            raise ReconcileConflictError(
                "RECONCILE_ACCEPT_REASON_INVALID", "accepted reason must be ACCEPTED"
            )
        if accepted and any(diff.blocking for diff in diffs):
            raise ReconcileConflictError(
                "RECONCILE_ACCEPT_BLOCKING_DIFF",
                "accepted attempt cannot contain a blocking diff",
            )
        if accepted:
            kinds = [component.kind for component in components]
            if (
                len(kinds) != len(REQUIRED_RECONCILE_COMPONENTS)
                or set(kinds) != set(REQUIRED_RECONCILE_COMPONENTS)
                or any(not component.accepted for component in components)
            ):
                raise ReconcileConflictError(
                    "RECONCILE_ACCEPT_COMPONENTS_INVALID",
                    "accepted attempt requires each complete component exactly once",
                )
            for kind in (
                ReconcileComponentKind.FILLS,
                ReconcileComponentKind.FUNDING,
            ):
                component = next(item for item in components if item.kind is kind)
                if (
                    component.cursor_start_ms is None
                    or component.cursor_end_ms != coverage_upper_bound_ms
                ):
                    raise ReconcileConflictError(
                        "RECONCILE_ACCEPT_COVERAGE_INVALID",
                        "fills/funding bounds must prove the accepted upper bound",
                    )
            coverage_components = [
                next(item for item in components if item.kind is kind)
                for kind in (
                    ReconcileComponentKind.FILLS,
                    ReconcileComponentKind.FUNDING,
                )
            ]
            if (
                len({item.cursor_start_ms for item in coverage_components}) != 1
                or any(
                    int(item.cursor_start_ms) > int(item.cursor_end_ms)
                    for item in coverage_components
                )
            ):
                raise ReconcileConflictError(
                    "RECONCILE_ACCEPT_COVERAGE_INVALID",
                    "fills/funding coverage bounds must be coherent",
                )
            payload = dict(snapshot_payload or {})
            payload_components = payload.get("components")
            payload_diffs = payload.get("diffs")
            if not isinstance(payload_components, Mapping) or not isinstance(
                payload_diffs, list
            ):
                raise ReconcileConflictError(
                    "RECONCILE_ACCEPT_SNAPSHOT_INVALID",
                    "accepted snapshot must contain components and diffs",
                )
            expected_component_digests = {
                component.kind.value: component.digest for component in components
            }
            funding_component = next(
                item
                for item in components
                if item.kind is ReconcileComponentKind.FUNDING
            )
            component_funding_ids = sorted(
                str(item.get("event_id"))
                for item in funding_component.canonical_rows()
                if isinstance(item.get("event_id"), str)
                and str(item.get("event_id")).strip()
            )
            supplied_funding_ids = sorted(event.event_id for event in funding_events)
            if len(set(component_funding_ids)) != len(component_funding_ids):
                raise ReconcileConflictError(
                    "RECONCILE_ACCEPT_FUNDING_LEDGER_MISMATCH",
                    "funding component contains duplicate event identities",
                )
            try:
                component_funding_digests = {
                    str(item["event_id"]): FundingEventRecord(
                        event_id=str(item["event_id"]),
                        symbol=str(item["symbol"]),
                        amount_usdc=float(item["amount_usdc"]),
                        effective_ts=datetime.fromtimestamp(
                            int(item["effective_ts_ms"]) / 1000, tz=UTC
                        ),
                        source=str(item.get("source") or "HL_USER_FUNDING"),
                        funding_rate=(
                            None
                            if item.get("funding_rate") is None
                            else float(item["funding_rate"])
                        ),
                        position_szi=(
                            None
                            if item.get("position_szi") is None
                            else float(item["position_szi"])
                        ),
                        n_samples=(
                            None
                            if item.get("n_samples") is None
                            else int(item["n_samples"])
                        ),
                    ).digest
                    for item in funding_component.canonical_rows()
                }
            except (KeyError, TypeError, ValueError, OverflowError):
                raise ReconcileConflictError(
                    "RECONCILE_ACCEPT_FUNDING_LEDGER_MISMATCH",
                    "funding component contains malformed authoritative evidence",
                ) from None
            supplied_funding_digests = {
                event.event_id: event.digest for event in funding_events
            }
            if (
                len(component_funding_ids) != len(funding_component.rows)
                or component_funding_ids != supplied_funding_ids
                or payload.get("funding_event_ids") != supplied_funding_ids
                or component_funding_digests != supplied_funding_digests
                or payload.get("funding_event_digests") != supplied_funding_digests
            ):
                raise ReconcileConflictError(
                    "RECONCILE_ACCEPT_FUNDING_LEDGER_MISMATCH",
                    "funding component, snapshot, and durable ledger must correspond",
                )
            actual_component_digests = {
                str(kind): (
                    value.get("digest") if isinstance(value, Mapping) else None
                )
                for kind, value in payload_components.items()
            }
            expected_diffs = [diff.canonical() for diff in diffs]
            hash_payload = {
                "version": payload.get("version"),
                "components": expected_component_digests,
                "diffs": expected_diffs,
            }
            if payload.get("version") == SNAPSHOT_PAYLOAD_VERSION_V3:
                hash_payload["exposure_policy_version"] = payload.get(
                    "exposure_policy_version"
                )
            recomputed_hash = reconcile_digest(hash_payload)
            if (
                actual_component_digests != expected_component_digests
                or payload_diffs != expected_diffs
                or recomputed_hash != canonical_hash
            ):
                raise ReconcileConflictError(
                    "RECONCILE_ACCEPT_HASH_MISMATCH",
                    "snapshot/component/diff evidence does not match canonical hash",
                )
            payload_version = payload.get("version")
            if payload_version == SNAPSHOT_PAYLOAD_VERSION_V2:
                # TS-P1-006: a v2 payload claims to carry the authoritative
                # risk-bearing rows, so it is checked against the very
                # ComponentEvidence being persisted in this same transaction.
                # A v1 (or any predecessor/test) marker keeps the accepted
                # TS-P1-005 validation unchanged and is simply never
                # risk-readable — see load_authoritative_risk_snapshot().
                self._validate_v2_risk_rows(payload, components)
            elif payload_version == SNAPSHOT_PAYLOAD_VERSION_V3:
                # TS-P1-008: same write-side guarantee for the richer v3 rows —
                # the persisted risk rows must be exactly the rows the capture
                # observed, so a payload can never claim valuation/liquidation
                # evidence the ComponentEvidence does not carry.
                self._validate_v3_risk_rows(payload, components)
        checkpoint_id: str | None = None
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            row = self.conn.execute(
                "SELECT state, run_id, started_ts, deadline_s, max_skew_s "
                "FROM reconcile_attempts WHERE attempt_id = ?",
                (attempt_id,),
            ).fetchone()
            if row is None:
                raise ReconcileConflictError(
                    "RECONCILE_ATTEMPT_UNKNOWN", f"unknown attempt {attempt_id}"
                )
            if str(row["state"]) != ReconcileAttemptState.COLLECTING.value:
                raise ReconcileConflictError(
                    "RECONCILE_ATTEMPT_ALREADY_RESOLVED",
                    f"attempt {attempt_id} is {row['state']}",
                )
            run_id = str(row["run_id"])
            started = datetime.fromisoformat(str(row["started_ts"]))
            if started.tzinfo is None:
                started = started.replace(tzinfo=UTC)
            started = started.astimezone(UTC)
            resolved_end = ended_ts.astimezone(UTC)
            if accepted and (
                resolved_end < started
                or duration_ms < 0
                or duration_ms > int(float(row["deadline_s"]) * 1000)
                or int(coverage_upper_bound_ms) != int(started.timestamp() * 1000)
            ):
                raise ReconcileConflictError(
                    "RECONCILE_ACCEPT_ENVELOPE_INVALID",
                    "accepted attempt exceeds its durable temporal envelope",
                )
            if accepted:
                previous_coverage = self._coverage_upper_bound_ms_locked()
                coverage_start = int(coverage_components[0].cursor_start_ms)
                if (
                    previous_coverage is not None
                    and coverage_start > previous_coverage
                ):
                    raise ReconcileConflictError(
                        "RECONCILE_ACCEPT_COVERAGE_GAP",
                        "accepted coverage must overlap prior durable coverage",
                    )
                observed = sorted(
                    component.observed_ts.astimezone(UTC) for component in components
                )
                max_skew = float(row["max_skew_s"])
                if (
                    (observed[-1] - observed[0]).total_seconds() > max_skew
                    or (started - observed[0]).total_seconds() > max_skew
                    or (observed[-1] - resolved_end).total_seconds() > max_skew
                ):
                    raise ReconcileConflictError(
                        "RECONCILE_ACCEPT_COMPONENT_STALE",
                        "component timestamps violate the durable skew envelope",
                    )
            for component in components:
                self.conn.execute(
                    """
                    INSERT INTO reconcile_components(
                      attempt_id, component, source, status, observed_ts, exact,
                      complete, row_count, cursor_start_ms, cursor_end_ms,
                      page_count, call_count, payload_digest, reason_code
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        attempt_id,
                        component.kind.value,
                        component.source,
                        component.status.value,
                        _to_iso(component.observed_ts),
                        1 if component.exact else 0,
                        1 if component.complete else 0,
                        len(component.rows),
                        component.cursor_start_ms,
                        component.cursor_end_ms,
                        int(component.page_count),
                        int(component.call_count),
                        component.digest,
                        component.reason_code,
                    ),
                )
            for index, diff in enumerate(diffs, start=1):
                self.conn.execute(
                    """
                    INSERT INTO reconcile_diffs(
                      attempt_id, seq, kind, subject, reason_code, ownership,
                      blocking, payload_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        attempt_id,
                        index,
                        diff.kind.value,
                        diff.subject,
                        diff.reason_code,
                        diff.ownership.value,
                        1 if diff.blocking else 0,
                        _canonical_json(diff.canonical()),
                    ),
                )
            for event in funding_events:
                self._append_funding_event_locked(
                    event=event, attempt_id=attempt_id, recorded_ts=ended_ts
                )
            cursor = self.conn.execute(
                """
                UPDATE reconcile_attempts
                SET state = ?, ended_ts = ?, duration_ms = ?, complete = ?,
                    fresh = ?, canonical_hash = ?, reason_code = ?
                WHERE attempt_id = ? AND state = 'COLLECTING'
                """,
                (
                    state.value,
                    _to_iso(ended_ts),
                    int(duration_ms),
                    1 if state is ReconcileAttemptState.COMPLETE else 0,
                    1 if fresh else 0,
                    canonical_hash,
                    reason_code,
                    attempt_id,
                ),
            )
            if cursor.rowcount != 1:
                raise ReconcileConflictError(
                    "RECONCILE_ATTEMPT_RESOLVE_RACE",
                    f"attempt {attempt_id} resolve rowcount mismatch",
            )
            if accepted:
                previous_coverage = self._coverage_upper_bound_ms_locked()
                checkpoint_id = compute_reconcile_checkpoint_id(
                    attempt_id=attempt_id, canonical_hash=str(canonical_hash)
                )
                self.conn.execute(
                    """
                    INSERT INTO reconcile_checkpoints(
                      checkpoint_id, attempt_id, run_id, accepted_ts,
                      canonical_hash, snapshot_json, reason_code
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        checkpoint_id,
                        attempt_id,
                        run_id,
                        _to_iso(ended_ts),
                        str(canonical_hash),
                        _canonical_json(dict(snapshot_payload or {})),
                        reason_code,
                    ),
                )
                self.conn.execute(
                    "INSERT OR REPLACE INTO meta(key, value) VALUES (?, ?)",
                    (RECONCILE_CHECKPOINT_POINTER_KEY, checkpoint_id),
                )
                if self.durable_risk_controls_enabled():
                    self._append_risk_day_state_locked(
                        checkpoint_id=checkpoint_id,
                        attempt_id=attempt_id,
                        run_id=run_id,
                        accepted_ts=resolved_end,
                        snapshot_payload=dict(snapshot_payload or {}),
                        policy=risk_policy,
                    )
                if (
                    previous_coverage is not None
                    and int(coverage_upper_bound_ms) < previous_coverage
                ):
                    # Coverage is monotonic: a bound that moves backwards would
                    # re-open an interval the ledger already claims as proven.
                    raise ReconcileConflictError(
                        "RECONCILE_COVERAGE_REGRESSION",
                        "coverage upper bound must never move backwards",
                    )
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        return checkpoint_id

    def _append_risk_day_state_locked(
        self,
        *,
        checkpoint_id: str,
        attempt_id: str,
        run_id: str,
        accepted_ts: datetime,
        snapshot_payload: Mapping[str, Any],
        policy: DurableRiskPolicy,
    ) -> None:
        environment = self.conn.execute(
            "SELECT mode, network FROM runs WHERE run_id=?", (run_id,)
        ).fetchone()
        if environment is None:
            raise ReconcileConflictError("RISK_ENVIRONMENT_MISSING", "run missing")
        mode, network = str(environment["mode"]), str(environment["network"])
        accepted_ts = accepted_ts.astimezone(UTC)
        trading_date = accepted_ts.date().isoformat()
        day_start = datetime.combine(accepted_ts.date(), datetime.min.time(), tzinfo=UTC)

        previous = self.conn.execute(
            """SELECT accepted_ts FROM risk_day_checkpoints
               WHERE mode=? AND network=?
               ORDER BY accepted_ts DESC LIMIT 1""",
            (mode, network),
        ).fetchone()
        if previous is not None:
            previous_ts = datetime.fromisoformat(str(previous["accepted_ts"]))
            if previous_ts.tzinfo is None:
                previous_ts = previous_ts.replace(tzinfo=UTC)
            if accepted_ts < previous_ts.astimezone(UTC):
                raise ReconcileConflictError(
                    "RISK_DAY_CLOCK_ROLLBACK",
                    "accepted checkpoint time moved backwards",
                )

        try:
            balances = snapshot_payload["risk_rows"]["BALANCES"]
            if not isinstance(balances, list) or len(balances) != 1:
                raise ValueError
            equity = float(balances[0]["equity"])
            if not math.isfinite(equity) or equity < 0.0:
                raise ValueError
        except (KeyError, TypeError, ValueError):
            raise ReconcileConflictError(
                "RISK_DAY_STATE_MALFORMED", "authoritative equity is malformed"
            ) from None

        baseline = self.conn.execute(
            """SELECT checkpoint_id, accepted_ts, equity
               FROM risk_day_checkpoints
               WHERE mode=? AND network=? AND accepted_ts <= ?
               ORDER BY accepted_ts DESC, risk_day_row_id DESC LIMIT 1""",
            (mode, network, _to_iso(day_start)),
        ).fetchone()
        if accepted_ts == day_start:
            baseline_checkpoint_id = checkpoint_id
            baseline_ts = accepted_ts
            baseline_equity = equity
        elif baseline is None:
            baseline_checkpoint_id = None
            baseline_ts = None
            baseline_equity = None
        else:
            baseline_checkpoint_id = str(baseline["checkpoint_id"])
            baseline_ts = datetime.fromisoformat(str(baseline["accepted_ts"]))
            baseline_equity = float(baseline["equity"])

        prior_peak = self.conn.execute(
            """SELECT MAX(peak_equity) AS peak
               FROM risk_day_checkpoints
               WHERE mode=? AND network=? AND trading_date=?""",
            (mode, network, trading_date),
        ).fetchone()["peak"]
        peak_equity = max(
            equity,
            baseline_equity if baseline_equity is not None else equity,
            float(prior_peak) if prior_peak is not None else equity,
        )
        funding = self.conn.execute(
            """SELECT
                 COALESCE(SUM(CASE WHEN attribution='ATTRIBUTED'
                                   THEN amount_usdc ELSE 0 END),0) AS attributed,
                 COALESCE(SUM(CASE WHEN attribution='UNATTRIBUTED'
                                   THEN 1 ELSE 0 END),0) AS unexplained
               FROM funding_events
               WHERE effective_ts >= ? AND effective_ts <= ?""",
            (_to_iso(day_start), _to_iso(accepted_ts)),
        ).fetchone()
        attributed = float(funding["attributed"])
        unexplained = int(funding["unexplained"]) > 0
        authoritative = baseline_equity is not None and not unexplained
        reason = (
            "AUTHORITATIVE"
            if authoritative
            else (
                RISK_DAY_UNEXPLAINED_CASHFLOW
                if unexplained
                else RISK_DAY_BASELINE_MISSING
            )
        )
        baseline_source = (
            "CHECKPOINT_AT_OR_BEFORE_UTC_MIDNIGHT"
            if baseline_equity is not None
            else "MISSING"
        )
        daily_pnl_value = (
            None if baseline_equity is None else equity - float(baseline_equity)
        )
        daily_loss_pct_value = (
            None
            if baseline_equity is None
            else max(0.0, -float(daily_pnl_value) / float(baseline_equity))
        )
        drawdown_pct_value = max(0.0, (peak_equity - equity) / peak_equity)
        self.conn.execute(
            """INSERT INTO risk_day_checkpoints(
                 checkpoint_id, attempt_id, run_id, mode, network, trading_date,
                 policy_version, baseline_source, baseline_checkpoint_id, baseline_ts,
                 baseline_equity, peak_equity, equity, daily_pnl,
                 daily_loss_pct, drawdown_pct, realized_pnl_local,
                 funding_attributed_usdc, authoritative, reason_code,
                 accepted_ts, recorded_ts
               ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                checkpoint_id,
                attempt_id,
                run_id,
                mode,
                network,
                trading_date,
                policy.version,
                baseline_source,
                baseline_checkpoint_id,
                _to_iso(baseline_ts),
                baseline_equity,
                peak_equity,
                equity,
                daily_pnl_value,
                daily_loss_pct_value,
                drawdown_pct_value,
                float(self.realized_pnl_today(run_id)),
                attributed,
                1 if authoritative else 0,
                reason,
                _to_iso(accepted_ts),
                _to_iso(self.now()),
            ),
        )
        if not authoritative:
            return
        daily_pnl = equity - float(baseline_equity)
        controls = (
            (
                RISK_CONTROL_EQUITY_STOP,
                RISK_LATCH_ACCOUNT_SCOPE,
                equity,
                policy.equity_floor_usdc,
                equity <= policy.equity_floor_usdc,
            ),
            (
                RISK_CONTROL_DAILY_LOSS,
                trading_date,
                daily_pnl,
                -(float(baseline_equity) * policy.max_daily_loss_pct),
                daily_pnl <= -(float(baseline_equity) * policy.max_daily_loss_pct),
            ),
            (
                RISK_CONTROL_MAX_DRAWDOWN,
                trading_date,
                peak_equity - equity,
                peak_equity * policy.max_intraday_drawdown_pct,
                peak_equity - equity >= peak_equity * policy.max_intraday_drawdown_pct,
            ),
        )
        for control, scope_key, observed, threshold, breached in controls:
            if not breached:
                continue
            active = self._active_latch_row_locked(
                mode=mode,
                network=network,
                control=control,
                scope_key=scope_key,
            )
            if active is not None:
                continue
            generation = int(
                self.conn.execute(
                    """SELECT COALESCE(MAX(generation),0)+1 FROM risk_control_latches
                       WHERE mode=? AND network=? AND control=? AND scope_key=?""",
                    (mode, network, control, scope_key),
                ).fetchone()[0]
            )
            self.conn.execute(
                """INSERT INTO risk_control_latches(
                     record_kind,control,scope_key,mode,network,run_id,trading_date,
                     checkpoint_id,supersedes_row_id,generation,observed_value,
                     threshold_value,baseline_equity,peak_equity,equity,
                     policy_version,actor,reason_code,latched_ts,recorded_ts
                   ) VALUES ('LATCH',?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    control,
                    scope_key,
                    mode,
                    network,
                    run_id,
                    trading_date,
                    checkpoint_id,
                    None,
                    generation,
                    float(observed),
                    float(threshold),
                    float(baseline_equity),
                    peak_equity,
                    equity,
                    policy.version,
                    None,
                    f"{control}_LIMIT",
                    _to_iso(accepted_ts),
                    _to_iso(self.now()),
                ),
            )

    def _active_latch_row_locked(
        self, *, mode: str, network: str, control: str, scope_key: str
    ) -> sqlite3.Row | None:
        return self.conn.execute(
            """SELECT l.* FROM risk_control_latches l
               WHERE l.record_kind='LATCH' AND l.mode=? AND l.network=?
                 AND l.control=? AND l.scope_key=?
                 AND NOT EXISTS (
                   SELECT 1 FROM risk_control_latches r
                   WHERE r.record_kind='RESET'
                     AND r.supersedes_row_id=l.latch_row_id)
               ORDER BY l.generation DESC LIMIT 1""",
            (mode, network, control, scope_key),
        ).fetchone()

    @staticmethod
    def _validate_v2_risk_rows(
        payload: Mapping[str, Any], components: Sequence[ComponentEvidence]
    ) -> None:
        """A v2 payload must carry exactly the rows it is being accepted with.

        Called only from the accepted branch, after the component set has
        already been proven complete, so every risk-bearing kind is present.
        The rows are compared against the *live* ComponentEvidence objects being
        written in this same transaction — a payload can never claim rows the
        capture did not actually observe.
        """
        by_kind = {component.kind: component for component in components}
        expected_rows = {
            kind.value: by_kind[kind].canonical_rows()
            for kind in RISK_SNAPSHOT_COMPONENTS
        }
        expected_digests = {
            kind.value: by_kind[kind].digest for kind in RISK_SNAPSHOT_COMPONENTS
        }
        rows = payload.get("risk_rows")
        digests = payload.get("risk_row_digests")
        if not isinstance(rows, Mapping) or not isinstance(digests, Mapping):
            raise ReconcileConflictError(
                "RECONCILE_ACCEPT_RISK_ROWS_INVALID",
                "a v2 snapshot must carry canonical risk rows and their digests",
            )
        if dict(rows) != expected_rows or dict(digests) != expected_digests:
            raise ReconcileConflictError(
                "RECONCILE_ACCEPT_RISK_ROWS_INVALID",
                "v2 risk rows do not match the accepted component evidence",
            )

    @staticmethod
    def _validate_v3_risk_rows(
        payload: Mapping[str, Any], components: Sequence[ComponentEvidence]
    ) -> None:
        """A v3 payload must carry exactly the rows it is being accepted with.

        Same write-side contract as :meth:`_validate_v2_risk_rows`, applied to
        the richer TS-P1-008 POSITIONS rows (which add ``position_value``,
        ``liquidation_px`` and ``leverage``). The deep equality over the
        canonical rows is schema-agnostic: a v3 payload can never claim
        valuation, liquidation or leverage evidence the live ComponentEvidence
        did not actually observe in the same transaction.
        """
        by_kind = {component.kind: component for component in components}
        expected_rows = {
            kind.value: by_kind[kind].canonical_rows()
            for kind in RISK_SNAPSHOT_COMPONENTS
        }
        expected_digests = {
            kind.value: by_kind[kind].digest for kind in RISK_SNAPSHOT_COMPONENTS
        }
        rows = payload.get("risk_rows")
        digests = payload.get("risk_row_digests")
        if not isinstance(rows, Mapping) or not isinstance(digests, Mapping):
            raise ReconcileConflictError(
                "EXPOSURE_ACCEPT_RISK_ROWS_INVALID",
                "a v3 snapshot must carry canonical risk rows and their digests",
            )
        if dict(rows) != expected_rows or dict(digests) != expected_digests:
            raise ReconcileConflictError(
                "EXPOSURE_ACCEPT_RISK_ROWS_INVALID",
                "v3 risk rows do not match the accepted component evidence",
            )

    def _append_funding_event_locked(
        self,
        *,
        event: FundingEventRecord,
        attempt_id: str,
        recorded_ts: datetime,
    ) -> None:
        """Append-only funding write; exact replay is idempotent, drift blocks."""
        existing = self.conn.execute(
            "SELECT payload_digest FROM funding_events WHERE event_id = ?",
            (event.event_id,),
        ).fetchone()
        digest = event.digest
        if existing is not None:
            if str(existing["payload_digest"]) != digest:
                raise ReconcileConflictError(
                    "FUNDING_EVENT_IDENTITY_CONFLICT",
                    f"conflicting payload for funding event {event.event_id}",
                )
            return
        self.conn.execute(
            """
            INSERT INTO funding_events(
              event_id, symbol, amount_usdc, effective_ts, source, attribution,
              payload_digest, first_seen_attempt_id, recorded_ts
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event.event_id,
                event.symbol,
                _finite_float(float(event.amount_usdc)),
                _to_iso(event.effective_ts),
                event.source,
                event.attribution.value,
                digest,
                attempt_id,
                _to_iso(recorded_ts),
            ),
        )

    def resolve_interrupted_reconcile_attempts(
        self, *, observed_ts: datetime, reason_code: str = "RESTART_INTERRUPTED"
    ) -> int:
        """Mark attempts that never resolved (crash/kill) as INCOMPLETE.

        The evidence stays visible and the accepted pointer is not touched: a
        pre-crash checkpoint is retained but can never be presented as freshly
        reconciled.
        """
        self._require_full_reconcile()
        cursor = self.conn.execute(
            """
            UPDATE reconcile_attempts
            SET state = ?, ended_ts = ?, duration_ms = 0, complete = 0, fresh = 0,
                reason_code = ?
            WHERE state = 'COLLECTING'
            """,
            (
                ReconcileAttemptState.INCOMPLETE.value,
                _to_iso(observed_ts),
                reason_code,
            ),
        )
        self.conn.commit()
        return int(cursor.rowcount)

    def get_reconcile_attempt(self, attempt_id: str) -> dict[str, Any] | None:
        row = self.conn.execute(
            "SELECT * FROM reconcile_attempts WHERE attempt_id = ?", (attempt_id,)
        ).fetchone()
        return None if row is None else dict(row)

    def list_reconcile_attempts(self, run_id: str | None = None) -> list[dict[str, Any]]:
        if run_id is None:
            return self._rows(
                "SELECT * FROM reconcile_attempts ORDER BY run_id, seq"
            )
        return self._rows(
            "SELECT * FROM reconcile_attempts WHERE run_id = ? ORDER BY seq",
            (run_id,),
        )

    def get_reconcile_components(self, attempt_id: str) -> list[dict[str, Any]]:
        return self._rows(
            "SELECT * FROM reconcile_components WHERE attempt_id = ? "
            "ORDER BY component",
            (attempt_id,),
        )

    def get_reconcile_diffs(self, attempt_id: str) -> list[dict[str, Any]]:
        return self._rows(
            "SELECT * FROM reconcile_diffs WHERE attempt_id = ? ORDER BY seq",
            (attempt_id,),
        )

    def latest_accepted_reconcile_checkpoint(self) -> dict[str, Any] | None:
        """Resolve the single transactional pointer; never a scan-and-guess."""
        if not self.full_reconcile_enabled():
            return None
        pointer = self.get_meta(RECONCILE_CHECKPOINT_POINTER_KEY)
        if pointer is None:
            return None
        row = self.conn.execute(
            "SELECT * FROM reconcile_checkpoints WHERE checkpoint_id = ?",
            (pointer,),
        ).fetchone()
        if row is None:
            raise ReconcileConflictError(
                "RECONCILE_POINTER_DANGLING",
                "latest-accepted pointer does not resolve",
            )
        return dict(row)

    def _coverage_upper_bound_ms_locked(self) -> int | None:
        """Derive coverage from the sole pointed checkpoint's immutable evidence."""
        pointer = self.get_meta(RECONCILE_CHECKPOINT_POINTER_KEY)
        if pointer is None:
            return None
        rows = self.conn.execute(
            """
            SELECT c.component, c.cursor_start_ms, c.cursor_end_ms
            FROM reconcile_checkpoints AS p
            JOIN reconcile_components AS c ON c.attempt_id = p.attempt_id
            WHERE p.checkpoint_id = ? AND c.component IN ('FILLS', 'FUNDING')
            ORDER BY c.component
            """,
            (pointer,),
        ).fetchall()
        if (
            len(rows) != 2
            or {str(row["component"]) for row in rows} != {"FILLS", "FUNDING"}
            or any(
                row["cursor_start_ms"] is None or row["cursor_end_ms"] is None
                for row in rows
            )
            or len({int(row["cursor_start_ms"]) for row in rows}) != 1
            or len({int(row["cursor_end_ms"]) for row in rows}) != 1
        ):
            raise ReconcileConflictError(
                "RECONCILE_COVERAGE_EVIDENCE_CORRUPT",
                "accepted fills/funding coverage evidence is incomplete",
            )
        return int(rows[0]["cursor_end_ms"])

    def reconcile_coverage_upper_bound_ms(self) -> int | None:
        """Upper bound of the fills/funding interval already proven covered."""
        if not self.full_reconcile_enabled():
            return None
        return self._coverage_upper_bound_ms_locked()

    def run_started_ts(self, run_id: str) -> datetime | None:
        """Durable start of a run, used as the very first coverage lower bound."""
        row = self.conn.execute(
            "SELECT started_ts FROM runs WHERE run_id = ?", (run_id,)
        ).fetchone()
        if row is None or row["started_ts"] is None:
            return None
        try:
            value = datetime.fromisoformat(str(row["started_ts"]))
        except ValueError:
            return None
        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)
        return value.astimezone(UTC)

    def earliest_reconcile_attempt_started_ts(self) -> datetime | None:
        """Earliest attempt start in the whole append-only attempt ledger.

        ``reconcile_attempts`` is append-only and its identity and bounds are
        frozen, so this is a durable floor for "when observation of this
        account actually began" that survives restarts and a new ``run_id``.
        It is the only such evidence while nothing has ever been accepted.

        ``started_ts`` is always stored as a fixed-width UTC ISO string
        (``_to_iso``), so SQL ``MIN`` over the text column is chronological.
        """
        if not self.full_reconcile_enabled():
            return None
        row = self.conn.execute(
            "SELECT MIN(started_ts) FROM reconcile_attempts"
        ).fetchone()
        if row is None or row[0] is None:
            return None
        try:
            value = datetime.fromisoformat(str(row[0]))
        except ValueError:
            return None
        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)
        return value.astimezone(UTC)

    def count_accepted_reconcile_checkpoints(self) -> int:
        if not self.full_reconcile_enabled():
            return 0
        return int(
            self.conn.execute(
                "SELECT COUNT(*) FROM reconcile_checkpoints"
            ).fetchone()[0]
        )

    def latest_resolved_reconcile_attempt_id(self) -> str | None:
        """The most recently *resolved* attempt, whatever its verdict.

        Durable insertion order is authoritative; wall-clock timestamps are
        evidence, never ordering keys. ``COLLECTING`` rows are excluded: an in-flight
        capture has not resolved anything yet, and a capture that never
        resolves is turned into an ``INCOMPLETE`` row on reopen — at which
        point it does count here.
        """
        row = self.conn.execute(
            "SELECT attempt_id FROM reconcile_attempts WHERE state != 'COLLECTING' "
            "ORDER BY rowid DESC LIMIT 1"
        ).fetchone()
        return None if row is None else str(row["attempt_id"])

    def full_reconcile_ready(self, *, now: datetime, max_age_s: float) -> bool:
        """Derived readiness: a *fresh, still-current* accepted v6 checkpoint.

        Deliberately independent of the light ``OrderManager.reconcile()``
        path: no light success can reach this value. A clock rollback (an
        accepted timestamp in the future) is treated as non-ready.

        Freshness alone is not enough: the pointer's attempt must also be the
        most recently resolved attempt. Any later failed, conflicting, stale or
        restart-interrupted attempt therefore makes readiness false until a new
        capture is accepted, so a still-young checkpoint can never outvote newer
        contradicting evidence.
        """
        checkpoint = self.latest_accepted_reconcile_checkpoint()
        if checkpoint is None:
            return False
        latest_resolved = self.latest_resolved_reconcile_attempt_id()
        if latest_resolved != str(checkpoint["attempt_id"]):
            return False
        attempt = self.conn.execute(
            "SELECT state, complete, fresh, canonical_hash, reason_code "
            "FROM reconcile_attempts WHERE attempt_id = ?",
            (checkpoint["attempt_id"],),
        ).fetchone()
        if (
            attempt is None
            or str(attempt["state"]) != ReconcileAttemptState.COMPLETE.value
            or int(attempt["complete"]) != 1
            or int(attempt["fresh"]) != 1
            or str(attempt["reason_code"]) != "ACCEPTED"
            or str(attempt["canonical_hash"]) != str(checkpoint["canonical_hash"])
        ):
            return False
        components = self.get_reconcile_components(str(checkpoint["attempt_id"]))
        if (
            len(components) != len(REQUIRED_RECONCILE_COMPONENTS)
            or {row["component"] for row in components}
            != {kind.value for kind in REQUIRED_RECONCILE_COMPONENTS}
            or any(
                row["status"] != ReconcileComponentStatus.COMPLETE.value
                or int(row["exact"]) != 1
                or int(row["complete"]) != 1
                or row["observed_ts"] is None
                for row in components
            )
        ):
            return False
        try:
            snapshot = json.loads(str(checkpoint["snapshot_json"]))
            diffs = [
                json.loads(str(item["payload_json"]))
                for item in self.get_reconcile_diffs(str(checkpoint["attempt_id"]))
            ]
            component_digests = {
                str(item["component"]): str(item["payload_digest"])
                for item in components
            }
            hash_payload = {
                "version": snapshot.get("version"),
                "components": component_digests,
                "diffs": diffs,
            }
            if snapshot.get("version") == SNAPSHOT_PAYLOAD_VERSION_V3:
                hash_payload["exposure_policy_version"] = snapshot.get(
                    "exposure_policy_version"
                )
            if (
                reconcile_digest(hash_payload)
                != str(checkpoint["canonical_hash"])
                or snapshot.get("diffs") != diffs
            ):
                return False
            snapshot_components = snapshot.get("components", {})
            if any(
                not isinstance(snapshot_components.get(str(item["component"])), Mapping)
                or snapshot_components[str(item["component"])].get("cursor_start_ms")
                != item["cursor_start_ms"]
                or snapshot_components[str(item["component"])].get("cursor_end_ms")
                != item["cursor_end_ms"]
                for item in components
            ):
                return False
            funding_ids = snapshot.get("funding_event_ids")
            if not isinstance(funding_ids, list) or any(
                not isinstance(event_id, str) or not event_id
                for event_id in funding_ids
            ):
                return False
            funding_digests = snapshot.get("funding_event_digests")
            if (
                not isinstance(funding_digests, Mapping)
                or set(funding_digests) != set(funding_ids)
            ):
                return False
            found_funding = (
                {
                    str(item["event_id"]): str(item["payload_digest"])
                    for item in self.conn.execute(
                        "SELECT event_id, payload_digest FROM funding_events WHERE event_id IN "
                        f"({','.join('?' for _ in funding_ids)})",
                        tuple(funding_ids),
                    ).fetchall()
                }
                if funding_ids
                else {}
            )
            if found_funding != dict(funding_digests):
                return False
            if self._coverage_upper_bound_ms_locked() is None:
                return False
        except (KeyError, TypeError, ValueError, json.JSONDecodeError, ReconcileConflictError):
            return False
        accepted_ts = datetime.fromisoformat(str(checkpoint["accepted_ts"]))
        if accepted_ts.tzinfo is None:
            accepted_ts = accepted_ts.replace(tzinfo=UTC)
        age = (now.astimezone(UTC) - accepted_ts.astimezone(UTC)).total_seconds()
        if age < 0:
            return False
        return age <= float(max_age_s)

    # ------------------------------------------------------------------
    # TS-P1-006 — the authoritative risk-input snapshot loader
    #
    # One bounded, SQLite-only read. No broker I/O, no await, no write, and no
    # transaction that outlives the call. Every exit that is not a fully proven
    # snapshot raises RiskSnapshotUnavailable with a stable reason code; there
    # is deliberately no "return None" path a caller could mistake for "no
    # exposure" and no cached value to fall back to.
    # ------------------------------------------------------------------

    @staticmethod
    def _risk_number(value: object) -> float | None:
        """Strict numeric read: no bools, no strings, no NaN/Inf.

        String coercion is refused on purpose — accepting ``"0"`` would let a
        malformed payload present itself as a valid zero balance or a flat
        position instead of failing closed.
        """
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return None
        number = float(value)
        return number if math.isfinite(number) else None

    def _risk_component_rows_locked(self, attempt_id: str) -> list[dict[str, Any]]:
        """Component provenance for one attempt, inside the caller's read epoch."""
        return [
            dict(row)
            for row in self.conn.execute(
                "SELECT component, status, observed_ts, exact, complete, row_count, "
                "cursor_start_ms, cursor_end_ms, payload_digest "
                "FROM reconcile_components WHERE attempt_id = ? ORDER BY component",
                (attempt_id,),
            ).fetchall()
        ]

    def load_authoritative_risk_snapshot(
        self, *, now: datetime, max_age_s: float
    ) -> AuthoritativeRiskSnapshot:
        """Resolve the sole latest-accepted checkpoint as one coherent view.

        Raises :class:`RiskSnapshotUnavailable` — never returns a partial,
        stale, superseded, legacy or unverifiable snapshot.
        """
        if not self.full_reconcile_enabled():
            raise RiskSnapshotUnavailable(RISK_SNAPSHOT_SCHEMA_INACTIVE)
        try:
            conn = self.conn
        except sqlite3.Error as exc:
            raise RiskSnapshotUnavailable(self._risk_read_reason(exc)) from None
        if conn.in_transaction:
            # An open transaction here would mean the caller is already mid-write;
            # joining it could read uncommitted state and could hold SQLite across
            # the caller's own awaits. Refuse instead.
            raise RiskSnapshotUnavailable(RISK_SNAPSHOT_TRANSACTION_ACTIVE)
        try:
            # A deferred read transaction pins one epoch at the first SELECT, so
            # the pointer, checkpoint, attempt, components, diffs and payload are
            # all read from the same committed state even if another connection
            # accepts a new capture meanwhile.
            conn.execute("BEGIN")
        except sqlite3.Error as exc:
            raise RiskSnapshotUnavailable(self._risk_read_reason(exc)) from None
        try:
            return self._load_risk_snapshot_locked(now=now, max_age_s=max_age_s)
        except RiskSnapshotUnavailable:
            raise
        except Exception as exc:  # noqa: BLE001 - any read failure vetoes
            raise RiskSnapshotUnavailable(self._risk_read_reason(exc)) from None
        finally:
            try:
                # Read-only by construction: end the epoch without writing.
                conn.rollback()
            except sqlite3.Error:
                pass

    @staticmethod
    def _risk_read_reason(exc: BaseException) -> str:
        """Secret-safe reason code for a failed read: type name only."""
        name = "".join(
            ch if ch.isalnum() or ch == "_" else "_"
            for ch in type(exc).__name__.upper()
        )
        return f"{RISK_SNAPSHOT_READ_FAILED}:{name}"[:96]

    def _load_risk_snapshot_locked(
        self, *, now: datetime, max_age_s: float
    ) -> AuthoritativeRiskSnapshot:
        pointer = self.get_meta(RECONCILE_CHECKPOINT_POINTER_KEY)
        if pointer is None:
            raise RiskSnapshotUnavailable(RISK_SNAPSHOT_NO_CHECKPOINT)
        checkpoint = self.conn.execute(
            "SELECT checkpoint_id, attempt_id, run_id, accepted_ts, canonical_hash, "
            "snapshot_json FROM reconcile_checkpoints WHERE checkpoint_id = ?",
            (pointer,),
        ).fetchone()
        if checkpoint is None:
            raise RiskSnapshotUnavailable(RISK_SNAPSHOT_POINTER_DANGLING)
        attempt_id = str(checkpoint["attempt_id"])
        canonical_hash = str(checkpoint["canonical_hash"])

        attempt = self.conn.execute(
            "SELECT state, complete, fresh, canonical_hash, reason_code "
            "FROM reconcile_attempts WHERE attempt_id = ?",
            (attempt_id,),
        ).fetchone()
        if (
            attempt is None
            or str(attempt["state"]) != ReconcileAttemptState.COMPLETE.value
            or int(attempt["complete"]) != 1
            or int(attempt["fresh"]) != 1
            or str(attempt["reason_code"]) != "ACCEPTED"
            or str(attempt["canonical_hash"]) != canonical_hash
        ):
            raise RiskSnapshotUnavailable(RISK_SNAPSHOT_ATTEMPT_NOT_ACCEPTED)

        # A young checkpoint may never outvote newer contradicting evidence: a
        # later failed, conflicting, stale or restart-interrupted attempt is the
        # latest word on the account.
        if self.latest_resolved_reconcile_attempt_id() != attempt_id:
            raise RiskSnapshotUnavailable(RISK_SNAPSHOT_SUPERSEDED)

        provenance = self._risk_component_rows_locked(attempt_id)
        by_component = {str(row["component"]): row for row in provenance}
        if (
            len(provenance) != len(REQUIRED_RECONCILE_COMPONENTS)
            or set(by_component) != {kind.value for kind in REQUIRED_RECONCILE_COMPONENTS}
            or any(
                str(row["status"]) != ReconcileComponentStatus.COMPLETE.value
                or int(row["exact"]) != 1
                or int(row["complete"]) != 1
                or row["observed_ts"] is None
                for row in provenance
            )
        ):
            raise RiskSnapshotUnavailable(RISK_SNAPSHOT_COMPONENTS_INCOMPLETE)
        try:
            observed = sorted(
                self._risk_utc(str(row["observed_ts"])) for row in provenance
            )
        except ValueError:
            raise RiskSnapshotUnavailable(RISK_SNAPSHOT_COMPONENTS_INCOMPLETE) from None

        payload = self._risk_payload(checkpoint["snapshot_json"])
        version = payload.get("version")
        if self.exposure_controls_enabled():
            # TS-P1-008: v8 risk authority requires a fresh v3 capture. Legacy
            # v1/v2 checkpoints remain retained and reopenable as historical
            # evidence, but they carry no per-position valuation, leverage or
            # liquidation evidence, so they can never authorize v8 risk. No
            # backfill is possible — a fresh real v3 capture is mandatory.
            if version != SNAPSHOT_PAYLOAD_VERSION_V3:
                raise RiskSnapshotUnavailable(RISK_SNAPSHOT_LEGACY_PAYLOAD)
        else:
            if version == SNAPSHOT_PAYLOAD_VERSION_V1:
                # Structurally valid predecessor evidence: retained, reopenable,
                # and never risk-readable. It stores digests and counts, not
                # rows, so no backfill is even possible — a fresh v2 capture is
                # required.
                raise RiskSnapshotUnavailable(RISK_SNAPSHOT_LEGACY_PAYLOAD)
            if version != SNAPSHOT_PAYLOAD_VERSION_V2:
                raise RiskSnapshotUnavailable(
                    RISK_SNAPSHOT_PAYLOAD_VERSION_UNSUPPORTED
                )

        component_digests = {
            component: str(row["payload_digest"])
            for component, row in by_component.items()
        }
        diffs = [
            self._risk_payload(row["payload_json"])
            for row in self.conn.execute(
                "SELECT payload_json FROM reconcile_diffs WHERE attempt_id = ? "
                "ORDER BY seq",
                (attempt_id,),
            ).fetchall()
        ]
        payload_components = payload.get("components")
        if not isinstance(payload_components, Mapping):
            raise RiskSnapshotUnavailable(RISK_SNAPSHOT_PAYLOAD_MALFORMED)
        stated_digests = {
            str(component): (value.get("digest") if isinstance(value, Mapping) else None)
            for component, value in payload_components.items()
        }
        if (
            stated_digests != component_digests
            or payload.get("diffs") != diffs
            or reconcile_digest(
                {
                    "version": version,
                    "components": component_digests,
                    "diffs": diffs,
                    **(
                        {"exposure_policy_version": payload.get("exposure_policy_version")}
                        if version == SNAPSHOT_PAYLOAD_VERSION_V3
                        else {}
                    ),
                }
            )
            != canonical_hash
        ):
            raise RiskSnapshotUnavailable(RISK_SNAPSHOT_HASH_MISMATCH)

        rows_by_kind = self._risk_rows(payload, by_component)
        positions = self._risk_positions(
            rows_by_kind[ReconcileComponentKind.POSITIONS.value],
            v3=(version == SNAPSHOT_PAYLOAD_VERSION_V3),
        )
        equity, withdrawable, margin_used, available = self._risk_account(
            rows_by_kind[ReconcileComponentKind.BALANCES.value],
            rows_by_kind[ReconcileComponentKind.MARGIN.value],
        )

        try:
            coverage_end = self._coverage_upper_bound_ms_locked()
        except ReconcileConflictError:
            raise RiskSnapshotUnavailable(RISK_SNAPSHOT_COVERAGE_UNPROVABLE) from None
        coverage_start = by_component[ReconcileComponentKind.FILLS.value][
            "cursor_start_ms"
        ]
        if coverage_end is None or coverage_start is None:
            raise RiskSnapshotUnavailable(RISK_SNAPSHOT_COVERAGE_UNPROVABLE)

        try:
            accepted_ts = self._risk_utc(str(checkpoint["accepted_ts"]))
        except ValueError:
            raise RiskSnapshotUnavailable(RISK_SNAPSHOT_PAYLOAD_MALFORMED) from None
        loaded_ts = now.astimezone(UTC) if now.tzinfo else now.replace(tzinfo=UTC)
        max_age = self._risk_number(max_age_s)
        if max_age is None or max_age < 0:
            raise RiskSnapshotUnavailable(RISK_SNAPSHOT_STALE)
        age = (loaded_ts - accepted_ts).total_seconds()
        if age < 0:
            # A checkpoint accepted in the future is a clock domain failure, not
            # a very fresh checkpoint.
            raise RiskSnapshotUnavailable(RISK_SNAPSHOT_FUTURE_CLOCK)
        if age > max_age:
            raise RiskSnapshotUnavailable(RISK_SNAPSHOT_STALE)

        # Last statement of the epoch: the pointer this view was built from must
        # still be the pointer. Anything else means the read straddled a commit.
        if self.get_meta(RECONCILE_CHECKPOINT_POINTER_KEY) != pointer:
            raise RiskSnapshotUnavailable(RISK_SNAPSHOT_POINTER_MOVED)

        return AuthoritativeRiskSnapshot(
            payload_version=str(version),
            checkpoint_id=str(checkpoint["checkpoint_id"]),
            attempt_id=attempt_id,
            run_id=str(checkpoint["run_id"]),
            canonical_hash=canonical_hash,
            accepted_ts=accepted_ts,
            loaded_ts=loaded_ts,
            observed_from_ts=observed[0],
            observed_to_ts=observed[-1],
            coverage_start_ms=int(coverage_start),
            coverage_end_ms=int(coverage_end),
            positions=positions,
            equity=equity,
            withdrawable=withdrawable,
            margin_used=margin_used,
            available_margin=available,
            exposure_policy_version=(
                str(payload.get("exposure_policy_version"))
                if version == SNAPSHOT_PAYLOAD_VERSION_V3
                and isinstance(payload.get("exposure_policy_version"), str)
                else None
            ),
        )

    @staticmethod
    def _risk_utc(value: str) -> datetime:
        parsed = datetime.fromisoformat(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=UTC)
        return parsed.astimezone(UTC)

    @staticmethod
    def _risk_payload(raw: object) -> Any:
        try:
            return json.loads(str(raw))
        except (TypeError, ValueError, json.JSONDecodeError):
            raise RiskSnapshotUnavailable(RISK_SNAPSHOT_PAYLOAD_MALFORMED) from None

    @staticmethod
    def _risk_rows(
        payload: Mapping[str, Any], by_component: Mapping[str, Mapping[str, Any]]
    ) -> dict[str, list[dict[str, Any]]]:
        """Recompute every risk row's digest from the row content itself.

        Row count and stored metadata are never taken as proof: the digest is
        recomputed exactly as ``ComponentEvidence.digest`` does, so evidence
        edited in place while preserving ``row_count`` and every metadata field
        still fails. That digest is in turn bound into ``canonical_hash``, which
        was already verified against the immutable checkpoint above.
        """
        required = {kind.value for kind in RISK_SNAPSHOT_COMPONENTS}
        rows = payload.get("risk_rows")
        digests = payload.get("risk_row_digests")
        if (
            not isinstance(rows, Mapping)
            or not isinstance(digests, Mapping)
            or set(rows) != required
            or set(digests) != required
        ):
            raise RiskSnapshotUnavailable(RISK_SNAPSHOT_ROWS_MISSING)
        resolved: dict[str, list[dict[str, Any]]] = {}
        for kind in RISK_SNAPSHOT_COMPONENTS:
            key = kind.value
            value = rows[key]
            if not isinstance(value, list) or any(
                not isinstance(row, Mapping) for row in value
            ):
                raise RiskSnapshotUnavailable(RISK_SNAPSHOT_ROWS_MISSING)
            normalized = [dict(row) for row in value]
            canonical = sorted(normalized, key=canonical_reconcile_json)
            provenance = by_component[key]
            recomputed = reconcile_digest({
                "kind": key,
                "rows": canonical,
                "cursor_start_ms": provenance["cursor_start_ms"],
                "cursor_end_ms": provenance["cursor_end_ms"],
            })
            if (
                normalized != canonical
                or recomputed != str(provenance["payload_digest"])
                or recomputed != str(digests[key])
                or len(normalized) != int(provenance["row_count"])
            ):
                raise RiskSnapshotUnavailable(RISK_SNAPSHOT_ROW_DIGEST_MISMATCH)
            resolved[key] = canonical
        return resolved

    @classmethod
    def _risk_positions(
        cls,
        rows: Sequence[Mapping[str, Any]],
        *,
        v3: bool = False,
    ) -> tuple[RiskPositionRow, ...]:
        positions: list[RiskPositionRow] = []
        seen: set[str] = set()
        # v3 extends the v2 {symbol, size} row with position_value (nonnegative
        # gross mark notional), liquidation_px (directional, optional only for a
        # zero-size row) and leverage. The loader validates structure only; the
        # semantic fail-closed checks (wrong side, nonfinite, incoherent mark)
        # live in the risk gate that consumes this view.
        expected = (
            {"symbol", "size", "position_value", "liquidation_px", "leverage"}
            if v3
            else {"symbol", "size"}
        )
        for row in rows:
            if set(row) != expected:
                raise RiskSnapshotUnavailable(RISK_SNAPSHOT_POSITION_MALFORMED)
            symbol_raw = row["symbol"]
            symbol = (
                symbol_raw.strip().upper()
                if isinstance(symbol_raw, str)
                else symbol_raw
            )
            size = cls._risk_number(row["size"])
            if not isinstance(symbol, str) or not symbol.strip() or size is None:
                raise RiskSnapshotUnavailable(RISK_SNAPSHOT_POSITION_MALFORMED)
            if symbol in seen:
                raise RiskSnapshotUnavailable(RISK_SNAPSHOT_POSITION_DUPLICATE)
            seen.add(symbol)
            if v3:
                position_value = cls._risk_number(row["position_value"])
                leverage = cls._risk_number(row["leverage"])
                liquidation_raw = row["liquidation_px"]
                liquidation_px = (
                    None
                    if liquidation_raw is None
                    else cls._risk_number(liquidation_raw)
                )
                # Non-finite valuation/leverage, or a present-but-unparseable
                # liquidation price, is malformed evidence, never coerced.
                if position_value is None or leverage is None:
                    raise RiskSnapshotUnavailable(
                        RISK_SNAPSHOT_POSITION_MALFORMED
                    )
                if liquidation_raw is not None and liquidation_px is None:
                    raise RiskSnapshotUnavailable(
                        RISK_SNAPSHOT_POSITION_MALFORMED
                    )
                positions.append(
                    RiskPositionRow(
                        symbol,
                        size,
                        position_value=position_value,
                        liquidation_px=liquidation_px,
                        leverage=leverage,
                    )
                )
            else:
                positions.append(RiskPositionRow(symbol, size))
        return tuple(positions)

    @classmethod
    def _risk_account(
        cls,
        balances: Sequence[Mapping[str, Any]],
        margin: Sequence[Mapping[str, Any]],
    ) -> tuple[float, float, float, float]:
        if (
            len(balances) != 1
            or len(margin) != 1
            or set(balances[0]) != {"equity", "withdrawable"}
            or set(margin[0]) != {"margin_used", "available_margin"}
        ):
            raise RiskSnapshotUnavailable(RISK_SNAPSHOT_ACCOUNT_MALFORMED)
        equity = cls._risk_number(balances[0]["equity"])
        withdrawable = cls._risk_number(balances[0]["withdrawable"])
        margin_used = cls._risk_number(margin[0]["margin_used"])
        available = cls._risk_number(margin[0]["available_margin"])
        if None in (equity, withdrawable, margin_used, available):
            raise RiskSnapshotUnavailable(RISK_SNAPSHOT_ACCOUNT_MALFORMED)
        if min(equity, withdrawable, margin_used, available) < 0:
            raise RiskSnapshotUnavailable(RISK_SNAPSHOT_ACCOUNT_NEGATIVE)
        if (
            withdrawable > equity
            or margin_used > equity
            or not math.isclose(
                available,
                equity - margin_used,
                rel_tol=0.0,
                abs_tol=ACCOUNT_IDENTITY_ABS_TOL,
            )
        ):
            # The same TS-P1-005 arithmetic identity, re-proven at read time
            # rather than recomputed from a later point read.
            raise RiskSnapshotUnavailable(RISK_SNAPSHOT_ACCOUNT_INCONSISTENT)
        return equity, withdrawable, margin_used, available

    def list_funding_events(
        self, *, symbol: str | None = None
    ) -> list[dict[str, Any]]:
        if not self.full_reconcile_enabled():
            return []
        if symbol is None:
            return self._rows(
                "SELECT * FROM funding_events ORDER BY effective_ts, event_id"
            )
        return self._rows(
            "SELECT * FROM funding_events WHERE symbol = ? "
            "ORDER BY effective_ts, event_id",
            (symbol,),
        )

    def get_funding_event(self, event_id: str) -> dict[str, Any] | None:
        row = self.conn.execute(
            "SELECT * FROM funding_events WHERE event_id = ?", (str(event_id),)
        ).fetchone()
        return None if row is None else dict(row)

    def funding_total(
        self,
        *,
        symbol: str | None = None,
        start_ts: datetime | None = None,
        end_ts: datetime | None = None,
        attributed_only: bool = True,
    ) -> float:
        """Signed funding total. Never consumed by risk before TS-P1-006."""
        total = 0.0
        for row in self.list_funding_events(symbol=symbol):
            if attributed_only and str(row["attribution"]) != (
                FundingAttribution.ATTRIBUTED.value
            ):
                continue
            effective = datetime.fromisoformat(str(row["effective_ts"]))
            if effective.tzinfo is None:
                effective = effective.replace(tzinfo=UTC)
            if start_ts is not None and effective < start_ts.astimezone(UTC):
                continue
            if end_ts is not None and effective > end_ts.astimezone(UTC):
                continue
            total += float(row["amount_usdc"])
        return total

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

    def get_order_by_oid(self, oid: int) -> dict[str, Any] | None:
        """Resolve one durable broker identity; zero or multiple matches are ambiguous."""
        rows = self.conn.execute(
            "SELECT * FROM orders WHERE oid = ? ORDER BY cloid", (int(oid),)
        ).fetchall()
        return dict(rows[0]) if len(rows) == 1 else None

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

    def list_risk_day_checkpoints(self) -> list[dict[str, Any]]:
        if not self.durable_risk_controls_enabled():
            return []
        return self._rows(
            "SELECT * FROM risk_day_checkpoints ORDER BY risk_day_row_id"
        )

    def list_risk_control_latches(self) -> list[dict[str, Any]]:
        if not self.durable_risk_controls_enabled():
            return []
        return self._rows(
            "SELECT * FROM risk_control_latches ORDER BY latch_row_id"
        )

    def active_risk_control_latches(
        self, *, run_id: str, now: datetime
    ) -> tuple[RiskControlLatch, ...]:
        if not self.durable_risk_controls_enabled():
            return ()
        environment = self.conn.execute(
            "SELECT mode,network FROM runs WHERE run_id=?", (run_id,)
        ).fetchone()
        if environment is None:
            return ()
        rows = self._active_risk_control_latch_rows_locked(
            mode=str(environment["mode"]),
            network=str(environment["network"]),
        )
        return self._risk_control_latches_from_rows(rows)

    def _active_risk_control_latch_rows_locked(
        self, *, mode: str, network: str
    ) -> Sequence[sqlite3.Row]:
        return self.conn.execute(
            """SELECT l.* FROM risk_control_latches l
               WHERE l.record_kind='LATCH' AND l.mode=? AND l.network=?
                 AND NOT EXISTS (
                   SELECT 1 FROM risk_control_latches r
                   WHERE r.record_kind='RESET'
                     AND r.supersedes_row_id=l.latch_row_id)
               ORDER BY CASE l.control
                 WHEN 'EQUITY_STOP' THEN 1
                 WHEN 'DAILY_LOSS' THEN 2 ELSE 3 END, l.latch_row_id""",
            (mode, network),
        ).fetchall()

    @staticmethod
    def _risk_control_latches_from_rows(
        rows: Sequence[sqlite3.Row],
    ) -> tuple[RiskControlLatch, ...]:
        return tuple(
            RiskControlLatch(
                latch_row_id=int(row["latch_row_id"]),
                control=str(row["control"]),
                scope_key=str(row["scope_key"]),
                trading_date=str(row["trading_date"]),
                checkpoint_id=str(row["checkpoint_id"]),
                generation=int(row["generation"]),
                observed_value=float(row["observed_value"]),
                threshold_value=float(row["threshold_value"]),
                equity=float(row["equity"]),
                reason_code=str(row["reason_code"]),
                policy_version=str(row["policy_version"]),
                latched_ts=datetime.fromisoformat(str(row["latched_ts"])),
            )
            for row in rows
        )

    def load_durable_risk_view(
        self, *, now: datetime, max_age_s: float, policy_version: str
    ) -> tuple[AuthoritativeRiskSnapshot, DailyRiskState]:
        if not self.durable_risk_controls_enabled():
            raise RiskSnapshotUnavailable(RISK_DAY_SCHEMA_INACTIVE)
        if self.conn.in_transaction:
            raise RiskSnapshotUnavailable(RISK_SNAPSHOT_TRANSACTION_ACTIVE)
        self.conn.execute("BEGIN")
        try:
            snapshot = self._load_risk_snapshot_locked(now=now, max_age_s=max_age_s)
            row = self.conn.execute(
            """SELECT d.*, r.mode, r.network
               FROM risk_day_checkpoints d
               JOIN runs r ON r.run_id=d.run_id
               WHERE d.checkpoint_id=?""",
            (snapshot.checkpoint_id,),
            ).fetchone()
            if row is None:
                raise RiskSnapshotUnavailable(RISK_DAY_CHECKPOINT_MISMATCH)
            if str(row["trading_date"]) != now.astimezone(UTC).date().isoformat():
                raise RiskSnapshotUnavailable(RISK_DAY_DATE_MISMATCH)
            if int(row["authoritative"]) != 1:
                raise RiskSnapshotUnavailable(str(row["reason_code"]))
            if str(row["policy_version"]) != str(policy_version):
                raise RiskSnapshotUnavailable(RISK_DAY_POLICY_MISMATCH)
            if float(row["equity"]) != snapshot.equity:
                raise RiskSnapshotUnavailable(RISK_DAY_CHECKPOINT_MISMATCH)
            baseline_ts = datetime.fromisoformat(str(row["baseline_ts"]))
            accepted_ts = datetime.fromisoformat(str(row["accepted_ts"]))
            latch_rows = self._active_risk_control_latch_rows_locked(
                mode=str(row["mode"]), network=str(row["network"])
            )
            latches = self._risk_control_latches_from_rows(latch_rows)
            if self.get_meta(RECONCILE_CHECKPOINT_POINTER_KEY) != snapshot.checkpoint_id:
                raise RiskSnapshotUnavailable(RISK_SNAPSHOT_POINTER_MOVED)
            daily = DailyRiskState(
            mode=str(row["mode"]),
            network=str(row["network"]),
            trading_date=str(row["trading_date"]),
            checkpoint_id=str(row["checkpoint_id"]),
            attempt_id=str(row["attempt_id"]),
            run_id=str(row["run_id"]),
            accepted_ts=accepted_ts,
            loaded_ts=now.astimezone(UTC),
            baseline_checkpoint_id=str(row["baseline_checkpoint_id"]),
            baseline_ts=baseline_ts,
            baseline_equity=float(row["baseline_equity"]),
            peak_equity=float(row["peak_equity"]),
            equity=float(row["equity"]),
            realized_pnl_local=float(row["realized_pnl_local"]),
            funding_attributed_usdc=float(row["funding_attributed_usdc"]),
            policy_version=str(row["policy_version"]),
            active_latches=latches,
            )
            return snapshot, daily
        except RiskSnapshotUnavailable:
            raise
        except Exception as exc:
            raise RiskSnapshotUnavailable(self._risk_read_reason(exc)) from None
        finally:
            self.conn.rollback()

    def record_risk_control_reset(
        self,
        *,
        latch_row_id: int,
        actor: str,
        acknowledgement: str,
        policy: DurableRiskPolicy,
        now: datetime,
        max_age_s: float,
    ) -> int:
        if not actor.strip():
            raise RiskControlConflictError(
                "RISK_RESET_ACTOR_REQUIRED", "human actor is required"
            )
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            latch = self.conn.execute(
            "SELECT * FROM risk_control_latches "
            "WHERE latch_row_id=? AND record_kind='LATCH'",
            (int(latch_row_id),),
            ).fetchone()
            if latch is None:
                raise RiskControlConflictError(
                "RISK_RESET_LATCH_UNKNOWN", "latch does not exist"
                )
            if str(latch["policy_version"]) != policy.version:
                raise RiskControlConflictError(
                    "RISK_RESET_POLICY_MISMATCH", "approved policy must match latch"
                )
            if self.conn.execute(
            "SELECT 1 FROM risk_control_latches "
            "WHERE record_kind='RESET' AND supersedes_row_id=?",
            (int(latch_row_id),),
            ).fetchone():
                raise RiskControlConflictError(
                "RISK_RESET_ALREADY_RECORDED", "latch already reset"
                )
            expected = risk_control_reset_token(
            str(latch["control"]), str(latch["scope_key"])
            )
            if acknowledgement != expected:
                raise RiskControlConflictError(
                "RISK_RESET_ACKNOWLEDGEMENT_INVALID",
                "exact human acknowledgement is required",
                )
            pointer = self.get_meta(RECONCILE_CHECKPOINT_POINTER_KEY)
            latest = self.conn.execute(
            """SELECT * FROM risk_day_checkpoints
               WHERE checkpoint_id=? AND mode=? AND network=?""",
            (pointer, str(latch["mode"]), str(latch["network"])),
            ).fetchone()
            if latest is None or int(latest["authoritative"]) != 1:
                raise RiskControlConflictError(
                "RISK_RESET_REQUIRES_SAFE_CHECKPOINT",
                "fresh authoritative checkpoint is required",
                )
            accepted_ts = self._risk_utc(str(latest["accepted_ts"]))
            observed_now = now.astimezone(UTC)
            age = (observed_now - accepted_ts).total_seconds()
            if (
                not math.isfinite(float(max_age_s))
                or float(max_age_s) < 0
                or age < 0
                or age > float(max_age_s)
                or str(latest["policy_version"]) != policy.version
                or self.latest_resolved_reconcile_attempt_id() != str(latest["attempt_id"])
            ):
                raise RiskControlConflictError(
                    "RISK_RESET_REQUIRES_SAFE_CHECKPOINT",
                    "fresh latest-resolved checkpoint is required",
                )
            if str(latch["control"]) in {
            RISK_CONTROL_DAILY_LOSS,
            RISK_CONTROL_MAX_DRAWDOWN,
            } and str(latest["trading_date"]) <= str(latch["trading_date"]):
                raise RiskControlConflictError(
                "RISK_RESET_REQUIRES_NEW_DAY", "new UTC-day baseline is required"
                )
            if (
            str(latch["control"]) == RISK_CONTROL_EQUITY_STOP
                and float(latest["equity"]) <= float(latch["threshold_value"])
            ):
                raise RiskControlConflictError(
                "RISK_RESET_REQUIRES_SAFE_CHECKPOINT",
                "equity remains below the approved floor",
                )
            cursor = self.conn.execute(
                """INSERT INTO risk_control_latches(
                     record_kind,control,scope_key,mode,network,run_id,trading_date,
                     checkpoint_id,supersedes_row_id,generation,observed_value,
                     threshold_value,baseline_equity,peak_equity,equity,
                     policy_version,actor,reason_code,latched_ts,recorded_ts
                   ) VALUES ('RESET',?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    str(latch["control"]),
                    str(latch["scope_key"]),
                    str(latch["mode"]),
                    str(latch["network"]),
                    str(latest["run_id"]),
                    str(latest["trading_date"]),
                    str(latest["checkpoint_id"]),
                    int(latch_row_id),
                    int(latch["generation"]),
                    float(latest["equity"]),
                    float(latch["threshold_value"]),
                    float(latest["baseline_equity"]),
                    float(latest["peak_equity"]),
                    float(latest["equity"]),
                    policy.version,
                    actor.strip(),
                    "HUMAN_RESET",
                    _to_iso(now),
                    _to_iso(self.now()),
                ),
            )
            self.conn.commit()
            return int(cursor.lastrowid)
        except sqlite3.IntegrityError as exc:
            self.conn.rollback()
            raise RiskControlConflictError(
                "RISK_RESET_ALREADY_RECORDED", "latch already reset"
            ) from exc
        except Exception:
            self.conn.rollback()
            raise

    def _rows(self, sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
        return [dict(row) for row in self.conn.execute(sql, params).fetchall()]
