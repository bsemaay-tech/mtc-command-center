"""
No-op migration strategy for optimizer_v0 SQLite DB.

Current schema is managed in src.optimizer_v0.store_sqlite (SCHEMA_VERSION=1).
This script validates DB accessibility and prints migration intent so future
schema upgrades have a stable entry point.
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.optimizer_v0.store_sqlite import SCHEMA_VERSION, SQLiteStore


def migrate(db_path: Path) -> None:
    SQLiteStore(db_path)  # Ensures baseline tables exist.
    with sqlite3.connect(db_path) as conn:
        run_count = conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0]
        trial_count = conn.execute("SELECT COUNT(*) FROM trials").fetchone()[0]
    print(f"DB: {db_path}")
    print(f"Schema version target: {SCHEMA_VERSION}")
    print(f"Runs: {run_count} | Trials: {trial_count}")
    print("No migration steps required for schema v1.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate/migrate optimizer_v0 SQLite DB.")
    parser.add_argument("--db", required=True, help="Path to SQLite DB file")
    args = parser.parse_args()
    migrate(Path(args.db))


if __name__ == "__main__":
    main()
