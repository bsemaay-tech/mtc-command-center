"""SQLite Store with schema v2 from the architecture spec."""

from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def _to_iso(value: datetime | str | None) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(UTC).isoformat()


def _json(value: Any) -> str:
    def default(obj: Any) -> str:
        if isinstance(obj, datetime):
            return _to_iso(obj) or ""
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=default)


class Store:
    """Small SQLite access layer for the bridge runtime database."""

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self._conn: sqlite3.Connection | None = None

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
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS meta (
              key TEXT PRIMARY KEY,
              value TEXT
            );

            CREATE TABLE IF NOT EXISTS runs (
              run_id TEXT PRIMARY KEY,
              started_ts TEXT,
              ended_ts TEXT,
              mode TEXT CHECK(mode IN ('paper','dry_run','live')),
              network TEXT,
              config_json TEXT
            );

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
            );

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
            );

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
            );

            CREATE TABLE IF NOT EXISTS fills (
              fill_id TEXT PRIMARY KEY,
              cloid TEXT,
              decision_uid TEXT,
              fill_ts TEXT,
              qty REAL,
              px REAL,
              fee REAL,
              funding REAL
            );

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
            );

            CREATE TABLE IF NOT EXISTS equity (
              run_id TEXT,
              ts TEXT,
              equity REAL,
              cash REAL,
              unrealized REAL,
              realized_today REAL,
              PRIMARY KEY(run_id, ts)
            );

            CREATE TABLE IF NOT EXISTS risk_days (
              trading_date TEXT PRIMARY KEY,
              day_start_equity REAL,
              realized_pnl_engine REAL,
              realized_pnl_broker REAL,
              max_intraday_dd REAL,
              consecutive_losses_end INTEGER,
              auto_rearms_used INTEGER
            );

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
            );

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
            );

            CREATE TABLE IF NOT EXISTS events (
              id INTEGER PRIMARY KEY,
              run_id TEXT,
              ts TEXT,
              severity TEXT,
              code TEXT,
              detail TEXT
            );

            CREATE TABLE IF NOT EXISTS signal_fingerprints (
              run_id TEXT,
              fingerprint TEXT,
              decision_uid TEXT,
              ts TEXT,
              PRIMARY KEY(run_id, fingerprint)
            );

            CREATE INDEX IF NOT EXISTS idx_decisions_uid ON decisions(decision_uid);
            CREATE INDEX IF NOT EXISTS idx_decisions_run ON decisions(run_id, ts);
            CREATE INDEX IF NOT EXISTS idx_orders_oid ON orders(oid);
            CREATE INDEX IF NOT EXISTS idx_orders_trade ON orders(trade_id);
            CREATE INDEX IF NOT EXISTS idx_fills_cloid ON fills(cloid);
            CREATE INDEX IF NOT EXISTS idx_trades_run ON trades(run_id);
            CREATE INDEX IF NOT EXISTS idx_events_run_sev ON events(run_id, severity, ts);
            """
        )
        self.conn.execute(
            "INSERT OR REPLACE INTO meta(key, value) VALUES (?, ?)",
            ("schema_version", "2"),
        )
        self.conn.commit()

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
    ) -> None:
        submit_ts = _to_iso(ts_submit) or _to_iso(datetime.now(UTC))
        self.conn.execute(
            """
            INSERT OR REPLACE INTO orders(
              cloid, oid, group_id, order_ref, order_json, decision_uid, trade_id,
              role, status, qty, filled_qty, avg_fill_px, ts_submit, ts_last
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                cloid,
                oid,
                group_id,
                order_ref,
                _json(order_json),
                decision_uid,
                trade_id,
                role,
                status,
                qty,
                filled_qty,
                avg_fill_px,
                submit_ts,
                _to_iso(ts_last) or submit_ts,
            ),
        )
        self.conn.commit()

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
    ) -> None:
        self.conn.execute(
            """
            INSERT OR REPLACE INTO fills(fill_id, cloid, decision_uid, fill_ts, qty, px, fee, funding)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (fill_id, cloid, decision_uid, _to_iso(fill_ts), qty, px, fee, funding),
        )
        self.conn.commit()

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
