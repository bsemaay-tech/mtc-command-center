#!/usr/bin/env python
"""
Detect likely TV trade-list truncation cases.

Heuristic:
- read each case json end_date
- read corresponding TV *_trades.csv in case folder
- compute gap_days = end_date_utc - last_tv_exit_utc
- flag when gap_days > threshold_days

Output:
- parity_suite_350/compare_runs/tv_trade_list_truncation_scan.csv
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class CaseRow:
    run_order: str
    case_id: str
    case_json: Path
    case_folder: Path
    tv_trades_csv: Path
    end_date_utc: pd.Timestamp
    last_tv_exit_utc: pd.Timestamp
    gap_days: float
    tv_unique_trades: int
    flagged: bool
    note: str


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--suite-root",
        default="parity_suite_350",
        help="Path to parity_suite_350 root (relative to mtc_backtest or absolute)",
    )
    p.add_argument(
        "--threshold-days",
        type=float,
        default=30.0,
        help="Flag when (end_date - last_tv_exit) exceeds this value.",
    )
    p.add_argument(
        "--out",
        default="compare_runs/tv_trade_list_truncation_scan.csv",
        help="Output CSV path relative to suite root.",
    )
    return p.parse_args()


def _to_utc(ts: str) -> pd.Timestamp:
    t = pd.to_datetime(ts, utc=True)
    if t.tzinfo is None:
        return t.tz_localize("UTC")
    return t.tz_convert("UTC")


def _read_case_json(case_json: Path) -> dict:
    return json.loads(case_json.read_text(encoding="utf-8"))


def _pick_tv_trades_csv(case_folder: Path) -> Path | None:
    files = sorted(case_folder.glob("*_trades.csv"))
    if not files:
        return None
    # Prefer newest by mtime when multiple files exist.
    return max(files, key=lambda p: p.stat().st_mtime)


def _extract_last_exit(tv_csv: Path) -> tuple[pd.Timestamp, int]:
    df = pd.read_csv(tv_csv)
    if "Type" not in df.columns or "Date and time" not in df.columns or "Trade #" not in df.columns:
        raise ValueError(f"unexpected TV columns in {tv_csv}")
    ex = df[df["Type"].astype(str).str.contains("Exit", case=False, na=False)].copy()
    if ex.empty:
        raise ValueError(f"no exit rows in {tv_csv}")
    # Existing suite convention: TV timestamps are interpreted in Europe/London,
    # then converted to UTC with -1 hour normalization used in current pipeline.
    ex["Date and time"] = pd.to_datetime(ex["Date and time"], utc=True) - pd.Timedelta(hours=1)
    last_exit = ex["Date and time"].max()
    uniq = int(df["Trade #"].nunique())
    return last_exit, uniq


def main() -> int:
    args = parse_args()
    here = Path(__file__).resolve()
    mtc_root = here.parents[2]
    suite_root = Path(args.suite_root)
    if not suite_root.is_absolute():
        suite_root = mtc_root / suite_root
    cases_dir = suite_root / "cases"
    tv_dir = suite_root / "tv_manual_inputs"

    if not cases_dir.exists():
        raise SystemExit(f"cases dir not found: {cases_dir}")
    if not tv_dir.exists():
        raise SystemExit(f"tv_manual_inputs dir not found: {tv_dir}")

    rows: list[CaseRow] = []
    case_jsons = sorted(cases_dir.glob("*.json"))
    for case_json in case_jsons:
        case_id = case_json.stem
        parts = case_id.split("_")
        run_order = ""
        if len(parts) >= 3 and parts[1] in {"core", "bnd", "pair"}:
            try:
                # case id style: parity_core_194_...
                idx = 2
                run_order = str(int(parts[idx]))
            except Exception:
                run_order = ""

        folder_match = sorted(tv_dir.glob(f"*{case_id}"))
        if not folder_match:
            continue
        case_folder = folder_match[0]
        tv_csv = _pick_tv_trades_csv(case_folder)
        if tv_csv is None:
            continue

        try:
            case_obj = _read_case_json(case_json)
            end_date_utc = _to_utc(case_obj["end_date"])
            last_tv_exit_utc, tv_unique = _extract_last_exit(tv_csv)
            gap_days = float((end_date_utc - last_tv_exit_utc).total_seconds() / 86400.0)
            flagged = gap_days > args.threshold_days
            # Heuristic only. Large gap can also come from valid no-trade regimes
            # (e.g. equity depletion / risk lockout). Treat as investigation candidate.
            note = "TV_EARLY_TRADE_END_CANDIDATE" if flagged else ""
            rows.append(
                CaseRow(
                    run_order=run_order,
                    case_id=case_id,
                    case_json=case_json,
                    case_folder=case_folder,
                    tv_trades_csv=tv_csv,
                    end_date_utc=end_date_utc,
                    last_tv_exit_utc=last_tv_exit_utc,
                    gap_days=gap_days,
                    tv_unique_trades=tv_unique,
                    flagged=flagged,
                    note=note,
                )
            )
        except Exception as e:
            rows.append(
                CaseRow(
                    run_order=run_order,
                    case_id=case_id,
                    case_json=case_json,
                    case_folder=case_folder,
                    tv_trades_csv=tv_csv,
                    end_date_utc=pd.Timestamp("1970-01-01", tz="UTC"),
                    last_tv_exit_utc=pd.Timestamp("1970-01-01", tz="UTC"),
                    gap_days=-1.0,
                    tv_unique_trades=0,
                    flagged=False,
                    note=f"ERROR: {e}",
                )
            )

    out = Path(args.out)
    if not out.is_absolute():
        out = suite_root / out
    out.parent.mkdir(parents=True, exist_ok=True)

    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "run_order",
                "case_id",
                "gap_days",
                "flagged",
                "tv_unique_trades",
                "end_date_utc",
                "last_tv_exit_utc",
                "tv_trades_csv",
                "note",
            ]
        )
        for r in sorted(rows, key=lambda x: (x.run_order, x.case_id)):
            w.writerow(
                [
                    r.run_order,
                    r.case_id,
                    f"{r.gap_days:.2f}",
                    "yes" if r.flagged else "no",
                    r.tv_unique_trades,
                    r.end_date_utc.isoformat(),
                    r.last_tv_exit_utc.isoformat(),
                    str(r.tv_trades_csv),
                    r.note,
                ]
            )

    flagged_count = sum(1 for r in rows if r.flagged)
    print(f"scanned={len(rows)} flagged={flagged_count}")
    print(f"output={out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
