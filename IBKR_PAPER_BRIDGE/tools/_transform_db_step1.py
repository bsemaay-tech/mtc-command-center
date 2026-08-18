#!/usr/bin/env python3
"""Transform db.py from v2 to v3 for TS-P1-002.

This script reads the original db.py, applies all required changes,
and writes the result back.  Run from C:\TSP1002\IBKR_PAPER_BRIDGE.
"""

import re
from pathlib import Path

SRC = Path("bridge/store/db.py")
ORIG = SRC.read_text(encoding="utf-8")

# ── Step 1: update module docstring and add hashlib import ──────────
ORIG = ORIG.replace(
    '"""SQLite Store with schema v2 from the architecture spec."""',
    '"""SQLite Store with schema v3 from the architecture spec.\n\n'
    'V3 (TS-P1-002) adds the durable identity table (order_identities) for\n'
    'intent/request identity, fail-closed double-submission prevention, and\n'
    'collision-safe order persistence.\n"""',
)
ORIG = ORIG.replace("import json\nimport sqlite3", "import hashlib\nimport json\nimport sqlite3")

# ── Step 2: insert identity primitives after _json() and before class Store ──
IDENTITY_PRIMITIVES = r'''

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


# ---------------------------------------------------------------------------
# Exception classes
# ---------------------------------------------------------------------------


class IdentityCollisionError(Exception):
    """Durable identity collision: same digest, different preimage."""


class IdentityMismatchError(Exception):
    """Same intent maps to a different request - material change detected."""


class ReservationBlockedError(Exception):
    """Reservation blocked: intent already exists in any state."""


class SchemaVersionError(Exception):
    """Unsupported or corrupt schema version."""


class V2MigrationError(Exception):
    """v2 -> v3 migration failed; rollback completed."""

'''

ORIG = ORIG.replace(
    "\n\nclass Store:",
    IDENTITY_PRIMITIVES + "\n\nclass Store:",
)

print("Step 1+2 done")
SRC.write_text(ORIG, encoding="utf-8")
print(f"Wrote intermediate {SRC}")
