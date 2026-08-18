#!/usr/bin/env python3
"""Check db.py v3 feature completeness."""
from pathlib import Path

text = Path(r"C:\TSP1002\IBKR_PAPER_BRIDGE\bridge\store\db.py").read_text(encoding="utf-8")
lines = text.split("\n")
print(f"Total lines: {len(lines)}")

checks = [
    "import hashlib",
    "def _float_hex",
    "def _normalize_ts",
    "def _canonical_json",
    "_INTENT_VERSION",
    "_REQUEST_VERSION",
    "def compute_intent_id",
    "def compute_request_id",
    "class IdentityCollisionError",
    "class IdentityMismatchError",
    "class ReservationBlockedError",
    "class SchemaVersionError",
    "class V2MigrationError",
    "_V3_DDL",
    "order_identities",
    "_SCHEMA_VERSION",
    "def reserve_identity",
    "def finalize_identity",
    "def get_identity",
    "def get_identity_by_request",
    "def check_identity_preimage",
    "def insert_order_safe",
    '"identities"',
]

for c in checks:
    found = c in text
    print(f"  {'OK' if found else 'MISSING'}: {c}")

# Check reserve_identity signature
idx = text.find("def reserve_identity")
if idx >= 0:
    nl = text.find("\n", idx + 120)
    next_def = text.find("\n    def ", idx + 20)
    end = min(nl, next_def) if next_def > 0 else nl
    end = max(end, idx + 300)
    print("\nreserve_identity (first 300 chars):")
    print(text[idx:idx+300])
