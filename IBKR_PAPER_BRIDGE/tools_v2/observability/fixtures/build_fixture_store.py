#!/usr/bin/env python3
"""Build a synthetic v4-shaped SQLite fixture store for observability tooling.

Package 5a (Local Observability Toolkit, first increment). See the Gate-1
record: `MTC_COMMAND_CENTER/11_TRIAGE/GATE1_PACKAGE5A_OBSERVABILITY_TOOLKIT_2026-08-18.md`.

The CREATE statements below replicate the minimal table/column shape of the
bridge v4 baseline store (`bridge/store/db.py`: `_create_tables_v3` plus
`_create_submission_ledger_v4`) so that observability tools can be exercised
against realistic structures WITHOUT importing any bridge code and without
ever touching a live store. Values are deliberately synthetic and
self-labelling (`SYNTH`, `synth-*` ids) so a fixture can never be mistaken
for production evidence.

Trim (vs. the real v4 DDL): indexes and triggers are omitted; CHECK
constraints are kept only where they are cheap and characteristic
(`order_identity`, `submission_attempts`, `submission_recovery_evidence`).
This is a fixture shape, not a migration path — it is never a substitute for
`bridge/store/db.py`.

No bridge imports. Python 3 stdlib only. Deterministic output: the same
`--out` path always receives byte-identical content (no randomness, no
clock reads), so tests can assert exact row counts.

Usage:
    python build_fixture_store.py --out /path/to/fixture.db
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

FIXTURE_LABEL = "synthetic fixture (Package 5a observability)"

# ---------------------------------------------------------------------------
# v4-shaped DDL — mirrors bridge/store/db.py column names/types exactly;
# see module docstring for the recorded trim.
# ---------------------------------------------------------------------------

DDL_STATEMENTS = (
    """
    CREATE TABLE IF NOT EXISTS meta (
      key TEXT PRIMARY KEY,
      value TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS runs (
      run_id TEXT PRIMARY KEY,
      started_ts TEXT,
      ended_ts TEXT,
      mode TEXT CHECK(mode IN ('paper','dry_run','live')),
      network TEXT,
      config_json TEXT
    )
    """,
    """
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
    )
    """,
    """
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
    )
    """,
    """
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
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS fills (
      fill_id TEXT PRIMARY KEY,
      cloid TEXT,
      decision_uid TEXT,
      fill_ts TEXT,
      qty REAL,
      px REAL,
      fee REAL,
      funding REAL
    )
    """,
    """
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
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS equity (
      run_id TEXT,
      ts TEXT,
      equity REAL,
      cash REAL,
      unrealized REAL,
      realized_today REAL,
      PRIMARY KEY(run_id, ts)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS risk_days (
      trading_date TEXT PRIMARY KEY,
      day_start_equity REAL,
      realized_pnl_engine REAL,
      realized_pnl_broker REAL,
      max_intraday_dd REAL,
      consecutive_losses_end INTEGER,
      auto_rearms_used INTEGER
    )
    """,
    """
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
    )
    """,
    """
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
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS events (
      id INTEGER PRIMARY KEY,
      run_id TEXT,
      ts TEXT,
      severity TEXT,
      code TEXT,
      detail TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS signal_fingerprints (
      run_id TEXT,
      fingerprint TEXT,
      decision_uid TEXT,
      ts TEXT,
      PRIMARY KEY(run_id, fingerprint)
    )
    """,
    """
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
      submitted_ts TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS submission_attempts (
      attempt_id TEXT PRIMARY KEY
        CHECK(length(attempt_id) = 75 AND substr(attempt_id, 1, 11) = 'attempt-v1:' AND NOT substr(attempt_id, 12) GLOB '*[^0-9a-f]*'),
      intent_id TEXT UNIQUE NOT NULL,
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
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS submission_recovery_evidence (
      evidence_id INTEGER PRIMARY KEY,
      attempt_id TEXT NOT NULL,
      cycle_no INTEGER NOT NULL CHECK(cycle_no > 0),
      observed_ts TEXT NOT NULL CHECK(observed_ts != ''),
      verdict TEXT NOT NULL CHECK(verdict IN (
        'PRESENT','ABSENT_COMPLETE','INCOMPLETE','CONFLICTING'
      )),
      evidence_json TEXT NOT NULL CHECK(evidence_json != ''),
      UNIQUE(attempt_id, cycle_no)
    )
    """,
)

# ---------------------------------------------------------------------------
# Synthetic rows. Every value is deliberately fake; ids spell out their own
# fixture origin. Deterministic — no clock, no randomness.
# ---------------------------------------------------------------------------

RUN_ID = "synth-run-0001"

META_ROWS = (
    ("schema_version", "4"),
    ("app_state", "DISARMED"),
    ("run_id", RUN_ID),
    ("window_started_ts", "2026-08-18T00:05:00Z"),
    ("window_last_alive_ts", "2026-08-18T00:34:12Z"),
)

RUNS_ROWS = (
    (RUN_ID, "2026-08-18T00:05:00Z", None, "paper", "synthetic-fixture-net",
     '{"label": "synthetic fixture (Package 5a observability)"}'),
)

BARS_ROWS = (
    ("SYNTH", "1m", "2026-08-18T00:30:00Z", 100.0, 101.0, 99.5, 100.5, 1000.0),
    ("SYNTH", "1m", "2026-08-18T00:31:00Z", 100.5, 100.75, 100.25, 100.5, 750.0),
    ("SYNTH", "1m", "2026-08-18T00:32:00Z", 100.5, 100.6, 100.1, 100.2, 640.0),
)

DECISIONS_ROWS = (
    (1, "synth-decision-0001", RUN_ID, "2026-08-18T00:10:00Z", "SYNTH",
     "SIGNAL", 1, '{"synthetic": true, "stage": "SIGNAL"}', 1),
    (2, "synth-decision-0001", RUN_ID, "2026-08-18T00:10:01Z", "SYNTH",
     "RISK_PASS", 1, '{"synthetic": true, "stage": "RISK_PASS"}', 1),
    (3, "synth-decision-0001", RUN_ID, "2026-08-18T00:10:02Z", "SYNTH",
     "SUBMITTED", 1, '{"synthetic": true, "stage": "SUBMITTED"}', 1),
    (4, "synth-decision-0002", RUN_ID, "2026-08-18T00:20:00Z", "SYNTH",
     "REJECTED", None, '{"synthetic": true, "stage": "REJECTED"}', 1),
)

# v4-realistic raw status spellings only (OPEN / FILLED / CANCELLED_BY_ENGINE);
# partial progress lives in filled_qty, not in the raw status — see
# docs/22_ORDER_STATE_CONTRACT.md "Quantity limitation".
ORDERS_ROWS = (
    ("synth-entry-0001", 9001, "synth-group-0001", "synth-orderref-0001",
     '{"synthetic": true, "role": "ENTRY"}', "synth-decision-0001", 1,
     "ENTRY", "FILLED", 1.0, 1.0, 100.25,
     "2026-08-18T00:10:02Z", "2026-08-18T00:12:00Z"),
    ("synth-sl-0001", 9002, "synth-group-0001", "synth-orderref-0001",
     '{"synthetic": true, "role": "SL"}', "synth-decision-0001", 1,
     "SL", "CANCELLED_BY_ENGINE", 1.0, 0.0, None,
     "2026-08-18T00:10:02Z", "2026-08-18T00:25:00Z"),
    ("synth-tp-0001", 9003, "synth-group-0001", "synth-orderref-0001",
     '{"synthetic": true, "role": "TP"}', "synth-decision-0001", 1,
     "TP", "OPEN", 1.0, 0.0, None,
     "2026-08-18T00:10:02Z", "2026-08-18T00:10:02Z"),
    ("synth-entry-0002", 9004, "synth-group-0002", "synth-orderref-0002",
     '{"synthetic": true, "role": "ENTRY"}', "synth-decision-0003", 2,
     "ENTRY", "OPEN", 2.0, 1.0, 100.4,
     "2026-08-18T00:15:00Z", "2026-08-18T00:16:30Z"),
    ("synth-sl-0002", 9005, "synth-group-0002", "synth-orderref-0002",
     '{"synthetic": true, "role": "SL"}', "synth-decision-0003", 2,
     "SL", "OPEN", 2.0, 0.0, None,
     "2026-08-18T00:15:00Z", "2026-08-18T00:15:00Z"),
)

FILLS_ROWS = (
    ("synth-fill-0001", "synth-entry-0001", "synth-decision-0001",
     "2026-08-18T00:12:00Z", 1.0, 100.25, 0.10, 0.0),
    ("synth-fill-0002", "synth-entry-0002", "synth-decision-0003",
     "2026-08-18T00:16:30Z", 1.0, 100.4, 0.10, 0.0),
)

TRADES_ROWS = (
    (1, RUN_ID, "SYNTH", "LONG", 1.0, "synth-decision-0001",
     "2026-08-18T00:09:59Z", "2026-08-18T00:10:00Z", "2026-08-18T00:10:02Z",
     "2026-08-18T00:12:00Z", "2026-08-18T00:12:00Z",
     100.2, 100.25, "2026-08-18T00:12:00Z",
     101.0, "2026-08-18T00:24:00Z", "SYNTH_TAKE_PROFIT",
     0.72, 5.0, 10.0, 0.001, 3, 99.2, 101.0, None),
    (2, RUN_ID, "SYNTH", "LONG", 2.0, "synth-decision-0003",
     "2026-08-18T00:14:59Z", "2026-08-18T00:15:00Z", "2026-08-18T00:15:00Z",
     "2026-08-18T00:16:30Z", "2026-08-18T00:16:30Z",
     100.35, 100.4, "2026-08-18T00:16:30Z",
     None, None, None, None, None, 20.0, 0.002, 3, 99.6, None, None),
)

EQUITY_ROWS = (
    (RUN_ID, "2026-08-18T00:05:00Z", 10000.0, 10000.0, 0.0, 0.0),
    (RUN_ID, "2026-08-18T00:12:00Z", 10000.72, 10000.72, 0.0, 0.72),
    (RUN_ID, "2026-08-18T00:34:00Z", 10000.10, 9998.10, 2.0, 0.72),
)

RISK_DAYS_ROWS = (
    ("2026-08-18", 10000.0, 0.72, 0.72, 0.0, 0, 0),
)

DIRECTIVES_ROWS = (
    (1, "2026-08-18T00:08:00Z", "SYNTH_NEUTRAL", 0.55, 60,
     "synthetic directive rationale — fixture only",
     "synth-sources-hash-0001",
     '{"synthetic": true}', 1),
)

LLM_CALLS_ROWS = (
    (1, "2026-08-18T00:08:00Z", "regime", "synth-model",
     "synth-prompt-hash-0001", 420, "OK", 100, 50, 0.0),
)

EVENTS_ROWS = (
    (1, RUN_ID, "2026-08-18T00:05:00Z", "INFO", "SYNTH_FIXTURE_BRIDGE_STARTED",
     '{"label": "synthetic fixture (Package 5a observability)"}'),
    (2, RUN_ID, "2026-08-18T00:05:00Z", "INFO", "SYNTH_BRIDGE_DISARMED_DEFAULT",
     "fixture opens DISARMED; synthetic only"),
    (3, RUN_ID, "2026-08-18T00:05:00Z", "INFO", "WINDOW_STARTED",
     "synthetic window start"),
    (4, RUN_ID, "2026-08-18T00:10:02Z", "INFO", "ORDER_SUBMITTED",
     "synthetic entry submission, cloid synth-entry-0001"),
    (5, RUN_ID, "2026-08-18T00:12:00Z", "INFO", "FILL_INGESTED",
     "synthetic fill 1.0 @ 100.25"),
    (6, RUN_ID, "2026-08-18T00:16:30Z", "WARN", "SYNTH_PARTIAL_PROGRESS_NOTE",
     "synthetic partial progress note; raw status deliberately left OPEN"),
    (7, RUN_ID, "2026-08-18T00:25:00Z", "INFO", "ORDER_CANCELED",
     "synthetic engine cancel, cloid synth-sl-0001"),
    (8, RUN_ID, "2026-08-18T00:34:12Z", "INFO", "RECONCILE_CYCLE_OK",
     "synthetic liveness pulse"),
)

SIGNAL_FINGERPRINTS_ROWS = (
    (RUN_ID, "synth-fingerprint-0001", "synth-decision-0001",
     "2026-08-18T00:09:59Z"),
)

# 64-hex synthetic digests (clearly fake; fixed strings, not hashes of
# anything). Chunked 8x8 so the length is self-evident; asserted below so a
# future edit that breaks the v3 CHECK lengths fails loudly at build time.
_SYNTH_HEX_64 = (
    "59594e54" "48455449" "43464958" "54555245"
    "30303030" "30303030" "30303030" "30303030"
)
_SYNTH_HEX_64_B = (
    "59594e54" "48455449" "43464958" "54555245"
    "30303030" "30303030" "30303030" "30303031"
)
assert len(_SYNTH_HEX_64) == 64 and len(_SYNTH_HEX_64_B) == 64
assert len("intent-v1:") == 10 and len("request-v1:") == 11 and len("attempt-v1:") == 11

ORDER_IDENTITY_ROWS = (
    ("intent-v1:" + _SYNTH_HEX_64,
     "synthetic-intent-preimage-0001", "ts-p1-002-intent-v1",
     "request-v1:" + _SYNTH_HEX_64,
     "synthetic-request-preimage-0001", "ts-p1-002-request-v1",
     "synth-cloid-seed-0001", RUN_ID, "synth-decision-0001",
     "SUBMITTED", "2026-08-18T00:10:01Z", "2026-08-18T00:10:02Z"),
    ("intent-v1:" + _SYNTH_HEX_64_B,
     "synthetic-intent-preimage-0002", "ts-p1-002-intent-v1",
     "request-v1:" + _SYNTH_HEX_64_B,
     "synthetic-request-preimage-0002", "ts-p1-002-request-v1",
     "synth-cloid-seed-0002", RUN_ID, "synth-decision-0003",
     "RESERVED", "2026-08-18T00:14:59Z", None),
)

SUBMISSION_ATTEMPTS_ROWS = (
    ("attempt-v1:" + _SYNTH_HEX_64,
     "intent-v1:" + _SYNTH_HEX_64,
     "request-v1:" + _SYNTH_HEX_64,
     RUN_ID, "synth-decision-0001",
     "VERIFIED_SUCCESS",
     '{"synthetic": true, "recovery": "fixture"}',
     '["synth-entry-0001","synth-sl-0001","synth-tp-0001"]',
     "2026-08-18T00:10:01Z", "2026-08-18T00:10:02Z",
     "SYNTH_FIXTURE_VERIFIED", 0, None, None, "2026-08-18T00:10:02Z"),
)

SUBMISSION_RECOVERY_EVIDENCE_ROWS = (
    (1, "attempt-v1:" + _SYNTH_HEX_64, 1, "2026-08-18T00:10:02Z",
     "PRESENT", '{"synthetic": true, "cycle": 1}'),
)

TABLE_ROW_DATA = {
    "meta": META_ROWS,
    "runs": RUNS_ROWS,
    "bars": BARS_ROWS,
    "decisions": DECISIONS_ROWS,
    "orders": ORDERS_ROWS,
    "fills": FILLS_ROWS,
    "trades": TRADES_ROWS,
    "equity": EQUITY_ROWS,
    "risk_days": RISK_DAYS_ROWS,
    "directives": DIRECTIVES_ROWS,
    "llm_calls": LLM_CALLS_ROWS,
    "events": EVENTS_ROWS,
    "signal_fingerprints": SIGNAL_FINGERPRINTS_ROWS,
    "order_identity": ORDER_IDENTITY_ROWS,
    "submission_attempts": SUBMISSION_ATTEMPTS_ROWS,
    "submission_recovery_evidence": SUBMISSION_RECOVERY_EVIDENCE_ROWS,
}


def build_fixture_store(out_path: str | Path) -> dict[str, int]:
    """Create (or atomically replace) the fixture store at ``out_path``.

    Returns a ``{table_name: row_count}`` dict of what was written. The
    output is fully deterministic for a given version of this file.
    """
    out_file = Path(out_path)
    if out_file.exists():
        out_file.unlink()
    if not out_file.parent.exists():
        out_file.parent.mkdir(parents=True)

    conn = sqlite3.connect(str(out_file))
    try:
        conn.execute("BEGIN")
        for statement in DDL_STATEMENTS:
            conn.execute(statement)
        for table, rows in TABLE_ROW_DATA.items():
            if not rows:
                continue
            placeholders = ",".join("?" * len(rows[0]))
            conn.executemany(
                f'INSERT INTO "{table}" VALUES ({placeholders})', rows
            )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    return {name: len(rows) for name, rows in TABLE_ROW_DATA.items()}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build a synthetic v4-shaped SQLite fixture store for Package 5a "
            "observability tooling. Output is always synthetic; there is no "
            "live-path default and no bridge code is imported."
        )
    )
    parser.add_argument(
        "--out",
        required=True,
        help="explicit output path for the fixture .db file (replaced if present)",
    )
    args = parser.parse_args(argv)

    counts = build_fixture_store(args.out)
    total = sum(counts.values())
    print(f"fixture store written: {args.out} ({FIXTURE_LABEL})")
    for name in sorted(counts):
        print(f"  {name}: {counts[name]} rows")
    print(f"  total rows: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
