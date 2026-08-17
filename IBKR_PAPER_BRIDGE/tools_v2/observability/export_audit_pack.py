#!/usr/bin/env python3
"""export_audit_pack — read-only Markdown audit/export pack for a bridge-format
SQLite store. Package 5a, Local Observability Toolkit (first increment).

Gate-1 record: `MTC_COMMAND_CENTER/11_TRIAGE/GATE1_PACKAGE5A_OBSERVABILITY_TOOLKIT_2026-08-18.md`.

Contract of this tool:

- Python 3 stdlib only (sqlite3 included). No network. No bridge imports.
- The store path is ALWAYS caller-supplied and required — there is no default
  path, live or otherwise. The tool never writes to the store: it opens the
  database in SQLite read-only mode (``file:...?mode=ro``).
- The report timestamp is caller-supplied. The tool never reads the clock for
  the report header (filesystem mtimes in the optional log section are labeled
  as filesystem evidence, not report time).
- Anything missing or malformed (missing table, missing meta key, unreadable
  store, unparseable value, missing log file) is reported as an explicit
  **[REPORTED]** gap. Data is never invented, defaulted, or guessed.
- Output is ONE Markdown document, written to ``--out`` or to stdout.

This tool is evidence output only. It controls nothing, approves nothing, and
authorizes nothing.
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

TOOL_NAME = "export_audit_pack"
TOOL_VERSION = "1.0.0"

# --- bounded-output guarantees -------------------------------------------
DEFAULT_RECENT_N = 50
MIN_RECENT_N = 1
MAX_RECENT_N = 500
MAX_META_ROWS = 100
MAX_LOG_TAIL_LINES = 40
MAX_LOG_READ_BYTES = 65536
MAX_CELL_CHARS = 80
MAX_ERROR_CHARS = 160

# The v4 baseline table set as created by bridge/store/db.py
# (_create_tables_v3 + _create_submission_ledger_v4). Used ONLY to report
# absent tables as gaps — presence of other tables is informational.
EXPECTED_V4_TABLES = (
    "meta",
    "runs",
    "bars",
    "decisions",
    "orders",
    "fills",
    "trades",
    "equity",
    "risk_days",
    "directives",
    "llm_calls",
    "events",
    "signal_fingerprints",
    "order_identity",
    "submission_attempts",
    "submission_recovery_evidence",
)

# Window-state meta keys surfaced in the State section
# (docs/21_WINDOW_STATE_CONTRACT.md:19-24).
KEY_META_KEYS = (
    "app_state",
    "run_id",
    "window_started_ts",
    "window_last_alive_ts",
    "window_interrupted_ts",
    "window_reset_ts",
)

RECENT_ORDER_COLUMNS = (
    "cloid",
    "role",
    "status",
    "qty",
    "filled_qty",
    "avg_fill_px",
    "ts_submit",
    "ts_last",
    "decision_uid",
    "trade_id",
)

RECENT_EVENT_COLUMNS = ("id", "ts", "severity", "code", "detail")

KNOWN_APP_STATES = ("ARMED", "DISARMED", "KILLED")


class _Gaps:
    """Collector for explicitly REPORTED integrity gaps."""

    def __init__(self) -> None:
        self.items: list[tuple[str, str]] = []

    def add(self, area: str, detail: str) -> None:
        self.items.append((area, _clip(detail, MAX_ERROR_CHARS)))

    def __len__(self) -> int:
        return len(self.items)


def _clip(text: str, limit: int) -> str:
    text = str(text)
    if len(text) <= limit:
        return text
    return text[:limit] + "…(truncated)"


def _md_cell(value: object) -> str:
    """Render one value as a safe, bounded Markdown table cell."""
    if value is None:
        return "*(null)*"
    text = str(value)
    text = text.replace("\r", " ").replace("\n", " ").replace("|", "\\|")
    return _clip(text, MAX_CELL_CHARS)


def _connect_read_only(store_path: str) -> sqlite3.Connection:
    """Open the store strictly read-only. Never creates or mutates a file."""
    uri = Path(store_path).resolve().as_uri() + "?mode=ro"
    return sqlite3.connect(uri, uri=True)


def _safe_error(exc: BaseException) -> str:
    """A safe, bounded error string — type name + message, nothing else."""
    return _clip(f"{type(exc).__name__}: {exc}", MAX_ERROR_CHARS)


def _quote_ident(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def _section_header(lines: list[str], title: str) -> None:
    lines.append("")
    lines.append(f"## {title}")
    lines.append("")


def _render_table(lines: list[str], header: tuple[str, ...], rows: list[tuple]) -> None:
    lines.append("| " + " | ".join(header) + " |")
    lines.append("|" + "|".join("---" for _ in header) + "|")
    for row in rows:
        lines.append("| " + " | ".join(_md_cell(v) for v in row) + " |")
    lines.append("")


def _open_store(store_path: str, gaps: _Gaps) -> sqlite3.Connection | None:
    """Connect read-only and probe it; None means the store is unreadable.

    ``sqlite3.connect`` is lazy — a missing or non-SQLite file only fails at
    the first query — so the probe here is what turns that into an explicit
    REPORTED gap instead of a crash mid-report.
    """
    conn: sqlite3.Connection | None = None
    try:
        conn = _connect_read_only(store_path)
        conn.execute("SELECT 1 FROM sqlite_master LIMIT 1").fetchone()
        return conn
    except Exception as exc:  # path-to-URI failures (e.g. ValueError) must be gaps, not crashes
        gaps.add("store", f"store could not be opened read-only: {_safe_error(exc)}")
        if conn is not None:
            conn.close()
        return None


def _list_tables(conn: sqlite3.Connection, gaps: _Gaps) -> list[str]:
    """User tables present in the store (sqlite internal tables excluded)."""
    try:
        rows = conn.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type = 'table' AND name NOT LIKE 'sqlite_%' "
            "ORDER BY name"
        ).fetchall()
        return [str(r[0]) for r in rows]
    except sqlite3.Error as exc:
        gaps.add("schema", f"table listing failed: {_safe_error(exc)}")
        return []


def _count_rows(conn: sqlite3.Connection, table: str, gaps: _Gaps) -> int | None:
    try:
        row = conn.execute(f"SELECT COUNT(*) FROM {_quote_ident(table)}").fetchone()
        return int(row[0])
    except (sqlite3.Error, TypeError, ValueError) as exc:
        gaps.add("schema", f"row count failed for table '{table}': {_safe_error(exc)}")
        return None


def _read_meta(conn: sqlite3.Connection, gaps: _Gaps) -> dict[str, str | None] | None:
    """Return the meta table as a dict, or None when unreadable."""
    try:
        rows = conn.execute(
            "SELECT key, value FROM meta ORDER BY key LIMIT ?", (MAX_META_ROWS + 1,)
        ).fetchall()
    except sqlite3.Error as exc:
        gaps.add("state", f"meta table unreadable: {_safe_error(exc)}")
        return None
    meta: dict[str, str | None] = {}
    for key, value in rows:
        meta[str(key)] = None if value is None else str(value)
    if len(rows) > MAX_META_ROWS:
        gaps.add(
            "state",
            f"meta has more than {MAX_META_ROWS} rows; listing was truncated at "
            f"{MAX_META_ROWS}",
        )
    return meta


def _report_schema_version(meta: dict[str, str | None] | None, gaps: _Gaps) -> str:
    if meta is None:
        return "**[REPORTED]** — meta unreadable; schema_version not reported (never invented)"
    if "schema_version" not in meta:
        gaps.add("schema", "meta key 'schema_version' missing — not reported (never invented)")
        return "**[REPORTED]** — meta key 'schema_version' missing"
    raw = meta["schema_version"]
    if raw is None or raw.strip() == "":
        gaps.add("schema", "meta key 'schema_version' present but empty — malformed")
        return "**[REPORTED]** — 'schema_version' present but empty"
    try:
        int(raw.strip())
    except ValueError:
        gaps.add("schema", f"'schema_version' value not an integer: {raw!r} — malformed")
        return f"**[REPORTED]** — malformed value (reported as-is): `{raw}`"
    return f"`{raw.strip()}`"


def _report_app_state(meta: dict[str, str | None] | None, gaps: _Gaps) -> str:
    if meta is None:
        return "**[REPORTED]** — meta unreadable; app_state not reported (never invented)"
    if "app_state" not in meta:
        gaps.add("state", "meta key 'app_state' missing — not reported (never invented)")
        return "**[REPORTED]** — meta key 'app_state' missing"
    value = meta["app_state"]
    if value is None or value == "":
        gaps.add("state", "meta key 'app_state' present but empty — malformed")
        return "**[REPORTED]** — 'app_state' present but empty"
    suffix = ""
    if value not in KNOWN_APP_STATES:
        gaps.add("state", f"'app_state' value not in {KNOWN_APP_STATES}: {value!r}")
        suffix = " *(unrecognized value, reported as-is)*"
    return f"`{value}`{suffix}"


def _recent_rows(
    conn: sqlite3.Connection,
    table: str,
    columns: tuple[str, ...],
    order_by: str,
    limit: int,
    tables: list[str],
    gaps: _Gaps,
) -> list[tuple] | None:
    """Most-recent rows for a known table; None means the section is a gap."""
    if table not in tables:
        gaps.add("orders/events", f"table '{table}' not present — recent rows not reported")
        return None
    col_list = ", ".join(_quote_ident(c) for c in columns)
    sql = f"SELECT {col_list} FROM {_quote_ident(table)} ORDER BY {order_by} LIMIT ?"
    try:
        return conn.execute(sql, (limit,)).fetchall()
    except sqlite3.Error as exc:
        gaps.add(
            "orders/events",
            f"recent-rows query failed for table '{table}': {_safe_error(exc)}",
        )
        return None


def _render_log_section(lines: list[str], log_paths: tuple[str, ...], gaps: _Gaps) -> None:
    if not log_paths:
        lines.append("No log files were supplied to this export.")
        return
    for raw_path in log_paths:
        lines.append(f"### Log: `{raw_path}`")
        lines.append("")
        path = Path(raw_path)
        if not path.exists():
            gaps.add("logs", f"log path not found: {raw_path} — not reported (never invented)")
            lines.append("**[REPORTED]** — path not found; nothing reported for it.")
            lines.append("")
            continue
        if path.is_dir():
            gaps.add("logs", f"log path is a directory, not a file: {raw_path}")
            lines.append("**[REPORTED]** — path is a directory; nothing reported for it.")
            lines.append("")
            continue
        try:
            size = path.stat().st_size
            mtime = path.stat().st_mtime
            lines.append(
                f"- size: {size} bytes · filesystem mtime: {mtime!r} "
                "(filesystem evidence, not report time)"
            )
            with path.open("rb") as handle:
                if size > MAX_LOG_READ_BYTES:
                    handle.seek(-MAX_LOG_READ_BYTES, 2)
                blob = handle.read(MAX_LOG_READ_BYTES)
            text = blob.decode("utf-8", errors="replace")
            tail_lines = text.splitlines()[-MAX_LOG_TAIL_LINES:]
            lines.append(f"- tail (last {MAX_LOG_TAIL_LINES} lines, bounded):")
            lines.append("")
            lines.append("```text")
            for tl in tail_lines:
                lines.append(_clip(tl, MAX_CELL_CHARS * 2))
            lines.append("```")
        except OSError as exc:
            gaps.add("logs", f"log unreadable: {raw_path}: {_safe_error(exc)}")
            lines.append(f"**[REPORTED]** — unreadable: `{_safe_error(exc)}`")
        lines.append("")


def build_audit_pack(
    store_path: str,
    log_paths: tuple[str, ...] | list[str] = (),
    timestamp: str | None = None,
    recent_n: int = DEFAULT_RECENT_N,
    output_path: str | None = None,
) -> str:
    """Build the audit pack and return it as one Markdown string.

    ``recent_n`` is clamped into ``[MIN_RECENT_N, MAX_RECENT_N]``; the clamp
    is recorded as a note in the pack, never silently applied.
    """
    gaps = _Gaps()
    notes: list[str] = []

    requested_n = recent_n
    recent_n = max(MIN_RECENT_N, min(MAX_RECENT_N, recent_n))
    if requested_n != recent_n:
        notes.append(
            f"requested --recent-n={requested_n} clamped to {recent_n} "
            f"(bounds [{MIN_RECENT_N}, {MAX_RECENT_N}])"
        )

    lines: list[str] = []
    lines.append("# Bridge V2 Observability — Audit/Export Pack")
    lines.append("")
    lines.append(f"- tool: `{TOOL_NAME}` v{TOOL_VERSION} (stdlib-only, read-only)")
    lines.append(f"- store (caller-supplied path): `{store_path}`")
    if timestamp:
        lines.append(f"- report timestamp (caller-supplied): `{timestamp}`")
    else:
        lines.append("- report timestamp: **NOT SUPPLIED** (caller provided none; "
                     "this tool never invents one)")
    lines.append("- store opened in SQLite read-only mode (`mode=ro`); "
                 "no store or input file was created, modified, or deleted by this "
                 "tool (the only file written is this output pack)")
    if notes:
        for note in notes:
            lines.append(f"- note: {note}")

    conn = _open_store(store_path, gaps)

    # ---- Schema section -------------------------------------------------
    _section_header(lines, "Schema")
    if conn is None:
        lines.append("**[REPORTED]** — store unreadable; no schema evidence collected.")
    else:
        meta = _read_meta(conn, gaps)
        lines.append(f"- schema_version (from meta): {_report_schema_version(meta, gaps)}")
        lines.append("")
        tables = _list_tables(conn, gaps)
        if tables:
            rows: list[tuple] = []
            for table in tables:
                count = _count_rows(conn, table, gaps)
                rows.append((table, "**[REPORTED]**" if count is None else count))
            _render_table(lines, ("table", "row count"), rows)
        else:
            lines.append("**[REPORTED]** — no tables discovered (or listing failed); "
                         "nothing invented.")
        missing = [t for t in EXPECTED_V4_TABLES if t not in tables]
        extra = [t for t in tables if t not in EXPECTED_V4_TABLES]
        for table in missing:
            gaps.add("schema", f"expected v4 baseline table missing: '{table}'")
        if missing:
            lines.append(
                f"Expected v4 baseline tables missing (**[REPORTED]**, not invented): "
                + ", ".join(f"`{t}`" for t in missing)
            )
            lines.append("")
        if extra:
            lines.append(
                "Tables present beyond the v4 baseline set (informational, not a gap): "
                + ", ".join(f"`{t}`" for t in extra)
            )
            lines.append("")

        # ---- State section ----------------------------------------------
        _section_header(lines, "State (app_state and key meta values)")
        if meta is None:
            lines.append("**[REPORTED]** — meta unreadable; state not reported.")
        else:
            lines.append(f"- app_state: {_report_app_state(meta, gaps)}")
            lines.append("")
            state_rows: list[tuple] = []
            for key in KEY_META_KEYS:
                if key == "app_state":
                    continue
                state_rows.append((key, meta.get(key, "*(not present)*")))
            _render_table(lines, ("meta key", "value"), state_rows)
            lines.append(
                "Window keys follow docs/21_WINDOW_STATE_CONTRACT.md:19-24; "
                "`*(not present)*` means the key is absent in this store — "
                "reported as-is, never defaulted."
            )

        # ---- Recent orders / events -------------------------------------
        _section_header(
            lines, f"Recent orders (most recent {recent_n}, bounded)"
        )
        orders = _recent_rows(
            conn,
            "orders",
            RECENT_ORDER_COLUMNS,
            "ts_submit DESC, rowid DESC",
            recent_n,
            tables,
            gaps,
        )
        if orders is None:
            lines.append("**[REPORTED]** — orders not reportable (see gaps).")
        elif not orders:
            lines.append("(no rows)")
        else:
            _render_table(lines, RECENT_ORDER_COLUMNS, [tuple(r) for r in orders])

        _section_header(
            lines, f"Recent events (most recent {recent_n}, bounded)"
        )
        events = _recent_rows(
            conn,
            "events",
            RECENT_EVENT_COLUMNS,
            "ts DESC, id DESC",
            recent_n,
            tables,
            gaps,
        )
        if events is None:
            lines.append("**[REPORTED]** — events not reportable (see gaps).")
        elif not events:
            lines.append("(no rows)")
        else:
            _render_table(lines, RECENT_EVENT_COLUMNS, [tuple(r) for r in events])

        conn.close()

    # ---- Logs section ----------------------------------------------------
    _section_header(lines, "Logs (optional, caller-supplied)")
    _render_log_section(lines, tuple(log_paths), gaps)

    # ---- Gaps section ----------------------------------------------------
    _section_header(lines, "Gaps (explicitly REPORTED)")
    if gaps.items:
        lines.append(
            f"{len(gaps)} gap(s) reported below. Every one is an observation of "
            "missing/malformed evidence; no value was invented anywhere in this pack."
        )
        lines.append("")
        for area, detail in gaps.items:
            lines.append(f"- **[REPORTED]** ({area}) {detail}")
    else:
        lines.append("No gaps reported.")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(
        "*This pack is read-only evidence output from a local observability "
        "tool. It controls nothing, approves nothing, and authorizes nothing.*"
    )
    lines.append("")

    pack = "\n".join(lines)
    if output_path:
        out_file = Path(output_path)
        if not out_file.parent.exists():
            out_file.parent.mkdir(parents=True)
        out_file.write_text(pack, encoding="utf-8")
    return pack


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog=TOOL_NAME,
        description=(
            "Build a read-only Markdown audit/export pack from an explicit "
            "bridge-format SQLite store path (fixtures in tests; never a live "
            "default). Missing/malformed structures are REPORTED, never invented."
        ),
    )
    parser.add_argument(
        "--store",
        required=True,
        help="explicit path to the SQLite store to report on (no default path exists)",
    )
    parser.add_argument(
        "--log",
        action="append",
        default=None,
        metavar="PATH",
        help="optional log file to include (bounded tail); repeatable",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="optional output path for the Markdown pack (default: stdout)",
    )
    parser.add_argument(
        "--timestamp",
        default=None,
        help="caller-supplied report timestamp (this tool never reads the clock)",
    )
    parser.add_argument(
        "--recent-n",
        type=int,
        default=DEFAULT_RECENT_N,
        help=f"most recent orders/events to include "
        f"(default {DEFAULT_RECENT_N}, clamped to "
        f"[{MIN_RECENT_N}, {MAX_RECENT_N}])",
    )
    args = parser.parse_args(argv)

    pack = build_audit_pack(
        store_path=args.store,
        log_paths=tuple(args.log or ()),
        timestamp=args.timestamp,
        recent_n=args.recent_n,
        output_path=args.out,
    )
    if not args.out:
        sys.stdout.write(pack)
    else:
        sys.stderr.write(f"wrote audit pack to {args.out} ({len(pack)} chars)\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
