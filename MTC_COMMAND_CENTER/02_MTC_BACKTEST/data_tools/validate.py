"""
Validator — check Parquet datasets for data-quality issues.

Usage
-----
python mtc_backtest/data_tools/validate.py \\
    --catalog mtc_backtest/backtest_assets/data_catalog.json \\
    --out     mtc_backtest/backtest_assets/validation_report.md

Exit codes
----------
0 — all OK (or only warnings)
1 — one or more ERROR-level issues found (unless --no-fail used)
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import NamedTuple

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Timeframe → minutes lookup
# ---------------------------------------------------------------------------
TF_MINUTES: dict[str, int] = {
    "5m": 5,
    "15m": 15,
    "1h": 60,
    "2h": 120,
    "4h": 240,
    "1d": 1440,
}


# ---------------------------------------------------------------------------
class CheckResult(NamedTuple):
    status: str   # "OK" | "WARN" | "ERROR"
    message: str


def icon(status: str) -> str:
    return {"OK": "[OK]", "WARN": "[WARN]", "ERROR": "[ERROR]"}.get(status, "[?]")


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------

def check_monotonic(df: pd.DataFrame) -> CheckResult:
    if df.index.is_monotonic_increasing:
        return CheckResult("OK", "Index is monotonically increasing.")
    n = int((~pd.Series(df.index).diff().gt(pd.Timedelta(0))).sum())
    return CheckResult("ERROR", f"Index is NOT monotonic — {n} violation(s).")


def check_duplicates(df: pd.DataFrame) -> CheckResult:
    n = int(df.index.duplicated().sum())
    if n == 0:
        return CheckResult("OK", "No duplicate timestamps.")
    return CheckResult("ERROR", f"{n} duplicate timestamp(s) found.")


def check_utc(df: pd.DataFrame) -> CheckResult:
    if df.index.tz is None:
        return CheckResult("ERROR", "DatetimeIndex has no timezone. UTC required.")
    tz_str = str(df.index.tz)
    if tz_str not in ("UTC", "utc", "Etc/UTC"):
        return CheckResult("ERROR", f"Timezone is '{tz_str}', expected UTC.")
    return CheckResult("OK", f"Timezone confirmed UTC ({tz_str}).")


def check_gaps(df: pd.DataFrame, timeframe: str, is_24_7: bool) -> CheckResult:
    if not is_24_7:
        return CheckResult(
            "OK", "Session-based market -- gap check skipped (market-hours gaps are expected)."
        )
    tf_min = TF_MINUTES.get(timeframe)
    if tf_min is None:
        return CheckResult("WARN", f"Unknown timeframe '{timeframe}' -- gap check skipped.")
    if len(df) < 2:
        return CheckResult("OK", "Too few bars to compute gaps.")

    expected = pd.Timedelta(minutes=tf_min)
    diffs = df.index.to_series().diff().dropna()
    large = diffs[diffs > expected]

    # Use absolute time thresholds regardless of timeframe:
    #   WARN  : gap > 1 hour (unexpected even for 5m data)
    #   ERROR : gap > 24 hours (true data loss — exchange maintenance is typically < 12h)
    warn_threshold = pd.Timedelta(hours=1)
    error_threshold = pd.Timedelta(hours=24)

    critical = diffs[diffs > error_threshold]
    warn = diffs[(diffs > warn_threshold) & (diffs <= error_threshold)]

    if len(critical) > 0:
        worst = critical.max()
        return CheckResult(
            "ERROR",
            f"{len(critical)} critical gap(s) > 24h. "
            f"Largest: {worst} (expected {expected}). "
            f"Total gaps > 1h: {len(large[large > warn_threshold])}.",
        )
    if len(warn) > 0:
        worst = warn.max()
        return CheckResult(
            "WARN",
            f"{len(warn)} gap(s) between 1h-24h. "
            f"Largest: {worst} (expected {expected}). "
            f"Likely exchange maintenance (Binance can have ~10-12h downtime).",
        )
    return CheckResult("OK", f"No significant gaps (expected interval: {expected}).")


def check_ohlc_sanity(df: pd.DataFrame) -> CheckResult:
    issues: list[str] = []
    high_ok = df["high"] >= df[["open", "close"]].max(axis=1)
    n_high = int((~high_ok).sum())
    if n_high:
        issues.append(f"high < max(open,close): {n_high} row(s)")

    low_ok = df["low"] <= df[["open", "close"]].min(axis=1)
    n_low = int((~low_ok).sum())
    if n_low:
        issues.append(f"low > min(open,close): {n_low} row(s)")

    vol_ok = df["volume"] >= 0
    n_vol = int((~vol_ok).sum())
    if n_vol:
        issues.append(f"volume < 0: {n_vol} row(s)")

    if issues:
        return CheckResult("ERROR", "OHLC sanity violations: " + "; ".join(issues))
    return CheckResult("OK", "OHLC sanity: high>=max(O,C), low<=min(O,C), volume>=0.")




# ---------------------------------------------------------------------------
# Per-dataset validation
# ---------------------------------------------------------------------------

class DatasetReport(NamedTuple):
    symbol: str
    timeframe: str
    path: str
    bar_count: int
    start: str
    end: str
    monotonic: CheckResult
    duplicates: CheckResult
    utc: CheckResult
    gaps: CheckResult
    ohlc: CheckResult

    @property
    def overall_status(self) -> str:
        statuses = [self.monotonic.status, self.duplicates.status,
                    self.utc.status, self.gaps.status, self.ohlc.status]
        if "ERROR" in statuses:
            return "ERROR"
        if "WARN" in statuses:
            return "WARN"
        return "OK"


def validate_dataset(
    symbol: str,
    timeframe: str,
    entry: dict,
) -> DatasetReport:
    path = entry.get("abs_path") or entry.get("path", "")
    path_obj = Path(path)

    if not path_obj.exists():
        dummy = CheckResult("ERROR", f"File not found: {path}")
        return DatasetReport(
            symbol=symbol, timeframe=timeframe, path=path,
            bar_count=0, start="N/A", end="N/A",
            monotonic=dummy, duplicates=dummy, utc=dummy,
            gaps=dummy, ohlc=dummy,
        )

    df = pd.read_parquet(path_obj)
    bar_count = len(df)
    start_str = str(df.index[0]) if bar_count else "N/A"
    end_str = str(df.index[-1]) if bar_count else "N/A"

    is_24_7 = entry.get("is_24_7", True)

    return DatasetReport(
        symbol=symbol, timeframe=timeframe, path=path,
        bar_count=bar_count, start=start_str, end=end_str,
        monotonic=check_monotonic(df),
        duplicates=check_duplicates(df),
        utc=check_utc(df),
        gaps=check_gaps(df, timeframe, is_24_7),
        ohlc=check_ohlc_sanity(df),
    )


# ---------------------------------------------------------------------------
# Report rendering
# ---------------------------------------------------------------------------

def render_markdown(reports: list[DatasetReport], generated_at: str) -> str:
    lines: list[str] = [
        "# MTC Data Validation Report",
        f"Generated: {generated_at}",
        "",
    ]

    # Summary table
    lines += [
        "## Summary",
        "",
        "| Symbol | TF | Bars | Status |",
        "|--------|----|------|--------|",
    ]
    for r in reports:
        lines.append(f"| {r.symbol} | {r.timeframe} | {r.bar_count:,} | {icon(r.overall_status)} {r.overall_status} |")

    lines += [""]

    # Detail per dataset
    for r in reports:
        lines += [
            f"---",
            f"## {r.symbol} / {r.timeframe}",
            f"- **Path**: `{r.path}`",
            f"- **Bars**: {r.bar_count:,}",
            f"- **Range**: {r.start} → {r.end}",
            f"- **Monotonic**: {icon(r.monotonic.status)} {r.monotonic.status} — {r.monotonic.message}",
            f"- **Duplicates**: {icon(r.duplicates.status)} {r.duplicates.status} — {r.duplicates.message}",
            f"- **UTC**: {icon(r.utc.status)} {r.utc.status} — {r.utc.message}",
            f"- **Gaps**: {icon(r.gaps.status)} {r.gaps.status} — {r.gaps.message}",
            f"- **OHLC Sanity**: {icon(r.ohlc.status)} {r.ohlc.status} — {r.ohlc.message}",
            f"",
            f"**Overall Status: {icon(r.overall_status)} {r.overall_status}**",
            "",
        ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Validate Parquet datasets listed in data_catalog.json.")
    p.add_argument(
        "--catalog",
        default=str(Path(__file__).resolve().parent.parent / "backtest_assets" / "data_catalog.json"),
        help="Path to data_catalog.json",
    )
    p.add_argument(
        "--out",
        default=str(Path(__file__).resolve().parent.parent / "backtest_assets" / "validation_report.md"),
        help="Output path for validation_report.md",
    )
    p.add_argument(
        "--no-fail",
        action="store_true",
        help="Exit 0 even on ERROR-level issues (useful in CI preview mode)",
    )
    p.add_argument(
        "--fail-on-warn",
        action="store_true",
        help="Exit 1 on WARN-level issues",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    catalog_path = Path(args.catalog)
    out_path = Path(args.out)

    if not catalog_path.exists():
        print(f"[validate] ERROR: catalog not found: {catalog_path}", file=sys.stderr)
        sys.exit(1)

    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    reports: list[DatasetReport] = []

    for symbol, tfs in catalog.items():
        for timeframe, entry in tfs.items():
            print(f"[validate] Checking {symbol}/{timeframe} ...", end=" ", flush=True)
            r = validate_dataset(symbol, timeframe, entry)
            print(f"{icon(r.overall_status)} {r.overall_status}")
            reports.append(r)

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    md = render_markdown(reports, generated_at)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"\n[validate] Report written -> {out_path}")

    has_error = any(r.overall_status == "ERROR" for r in reports)
    has_warn = any(r.overall_status == "WARN" for r in reports)

    if has_error and not args.no_fail:
        print("[validate] ERROR: One or more ERROR-level issues. Exit 1.", file=sys.stderr)
        sys.exit(1)
    if has_warn and args.fail_on_warn:
        print("[validate] WARN: One or more WARN-level issues. Exit 1 (--fail-on-warn).", file=sys.stderr)
        sys.exit(1)

    print("[validate] OK Done.")


if __name__ == "__main__":
    main()
