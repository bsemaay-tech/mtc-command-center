"""
SQLite persistence for optimizer_v0.
Stores run metadata and trial results in a local SQLite database.
"""
from __future__ import annotations

import json
import re
import sqlite3
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from .search import TrialResult, _make_param_key

# Current schema version
SCHEMA_VERSION = 1

INIT_SQL = """
CREATE TABLE IF NOT EXISTS runs (
    run_id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    case_path TEXT,
    mode TEXT,
    seed INTEGER,
    iters INTEGER,
    workers INTEGER,
    min_trades INTEGER,
    max_dd_pct REAL,
    space_file TEXT,
    out_csv TEXT,
    code_hash TEXT,
    schema_version INTEGER
);

CREATE TABLE IF NOT EXISTS trials (
    run_id TEXT,
    idx INTEGER,
    params_key TEXT,
    params_json TEXT,
    metrics_json TEXT,
    score REAL,
    status TEXT,
    prune_reason TEXT,
    runtime_s REAL,
    PRIMARY KEY (run_id, idx),
    UNIQUE (run_id, params_key)
);
"""

class SQLiteStore:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute("PRAGMA busy_timeout=5000;")
        return conn

    def _init_db(self) -> None:
        """Initialize DB schema if needed."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.executescript(INIT_SQL)

    def create_run(
        self,
        case_path: str,
        mode: str,
        seed: int,
        iters: int,
        workers: int,
        min_trades: int,
        max_dd_pct: float,
        space_file: Optional[str] = None,
        out_csv: Optional[str] = None,
        code_hash: Optional[str] = None,
        run_name: Optional[str] = None,
    ) -> str:
        """Create a new run record and return its ID."""
        run_id = str(uuid.uuid4())
        if run_name:
            # Keep run_id URL/CLI friendly and deterministic for a given name input.
            slug = re.sub(r"[^a-z0-9]+", "-", run_name.strip().lower()).strip("-")
            if slug:
                run_id = f"{slug}-{run_id}"
        created_at = datetime.now(timezone.utc).isoformat()
        
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO runs (
                    run_id, created_at, case_path, mode, seed, iters, workers, 
                    min_trades, max_dd_pct, space_file, out_csv, code_hash, schema_version
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run_id, created_at, case_path, mode, seed, iters, workers,
                    min_trades, max_dd_pct, space_file, out_csv, code_hash,
                    SCHEMA_VERSION
                )
            )
        return run_id

    def get_run(self, run_id: str) -> Dict[str, Any]:
        """Fetch run metadata."""
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute("SELECT * FROM runs WHERE run_id = ?", (run_id,)).fetchone()
            if not row:
                raise ValueError(f"Run ID not found: {run_id}")
            return dict(row)

    def list_runs(self, limit: int = 20) -> List[Dict[str, Any]]:
        """List most recent runs."""
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM runs ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
            return [dict(r) for r in rows]

    def upsert_trial(
        self,
        run_id: str,
        result: TrialResult,
    ) -> None:
        """Insert or update a trial result."""
        params_key = _make_param_key(result.params)
        params_json = json.dumps(result.params, sort_keys=True)
        
        # Serialize specific metrics for queryability
        metrics = {
            "net_profit": result.net_profit,
            "max_dd_pct": result.max_dd_pct,
            "total_trades": result.total_trades,
            "win_rate": result.win_rate,
            "profit_factor": result.profit_factor,
            "score": result.score if result.score > float("-inf") else None,
            "status": result.status,
            "prune_reason": result.prune_reason,
            "idx": result.idx,
            "thresholds": {
                "min_trades": result.min_trades_threshold,
                "max_dd_pct": result.max_dd_threshold_pct
            }
        }
        metrics_json = json.dumps(metrics)

        # Handle infinite score for storage
        score_val = result.score if result.score > float("-inf") else None

        with self._connect() as conn:
            try:
                conn.execute(
                    """
                    INSERT INTO trials (
                        run_id, idx, params_key, params_json, metrics_json, 
                        score, status, prune_reason, runtime_s
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(run_id, idx) DO UPDATE SET
                        params_key=excluded.params_key,
                        params_json=excluded.params_json,
                        metrics_json=excluded.metrics_json,
                        score=excluded.score,
                        status=excluded.status,
                        prune_reason=excluded.prune_reason,
                        runtime_s=excluded.runtime_s
                    """,
                    (
                        run_id, result.idx, params_key, params_json, metrics_json,
                        score_val, result.status, result.prune_reason, result.runtime_s
                    )
                )
            except sqlite3.IntegrityError as exc:
                # Deterministic policy for duplicate params in the same run:
                # keep the first inserted params_key row and ignore later duplicates.
                if "UNIQUE constraint failed: trials.run_id, trials.params_key" in str(exc):
                    return
                raise

    def fetch_seen_params(self, run_id: str) -> Set[str]:
        """Return set of params_key that have been attempted for this run."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT params_key FROM trials WHERE run_id = ?", (run_id,)
            ).fetchall()
            return {r[0] for r in rows}

    def fetch_completed_count(self, run_id: str) -> int:
        """Return count of completed trials."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT COUNT(*) FROM trials WHERE run_id = ?", (run_id,)
            ).fetchone()
            return row[0] if row else 0

    def fetch_trials(self, run_id: str) -> List[sqlite3.Row]:
        """Fetch all trials for a run as Raw rows."""
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            return conn.execute(
                "SELECT * FROM trials WHERE run_id = ?", (run_id,)
            ).fetchall()
