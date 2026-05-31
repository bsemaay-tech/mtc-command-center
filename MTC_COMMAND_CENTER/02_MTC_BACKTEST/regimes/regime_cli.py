"""
Regime Calendar CLI — generate the 4H regime calendar from a Parquet file.

Usage
-----
python mtc_backtest/regimes/regime_cli.py \\
    --data 110_/data/processed/binance/BTCUSDT/4h.parquet \\
    --out-json mtc_backtest/backtest_assets/regime_calendar_4h.json \\
    --out-md   mtc_backtest/backtest_assets/regime_calendar_4h.md \\
    [--overrides path/to/overrides.json] \\
    [--thresholds '{"adx_threshold": 25}']
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

_HERE = Path(__file__).resolve()
_PKG_ROOT = _HERE.parent.parent
if str(_PKG_ROOT) not in sys.path:
    sys.path.insert(0, str(_PKG_ROOT))

from regimes.labeler import (  # noqa: E402
    DEFAULT_THRESHOLDS,
    LABEL_DISPLAY,
    METHOD_VERSION,
    RegimeLabeler,
)
from regimes.manual_override import ManualOverride  # noqa: E402

DEFAULT_OUT_JSON = _PKG_ROOT / "backtest_assets" / "regime_calendar_4h.json"
DEFAULT_OUT_MD = _PKG_ROOT / "backtest_assets" / "regime_calendar_4h.md"


# ---------------------------------------------------------------------------
def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
def compute_coverage(windows: list[dict]) -> dict[str, float]:
    total = sum(w.get("bars") or 0 for w in windows)
    if total == 0:
        return {lbl: 0.0 for lbl in LABEL_DISPLAY}
    coverage = {}
    for lbl in LABEL_DISPLAY:
        c = sum(w.get("bars") or 0 for w in windows if w["label"] == lbl)
        coverage[lbl] = round(100.0 * c / total, 2)
    return coverage


def render_json(
    windows: list[dict],
    thresholds: dict,
    data_hash: str,
    fingerprint: str,
    generated_at: str,
) -> dict:
    coverage = compute_coverage(windows)
    return {
        "metadata": {
            "method": METHOD_VERSION,
            "thresholds": thresholds,
            "dataset_hash_sha256": data_hash,
            "fingerprint": fingerprint,
            "generated_at_utc": generated_at,
            "total_windows": len(windows),
            "label_coverage_pct": coverage,
        },
        "windows": windows,
    }


def render_markdown(cal_json: dict, data_path: str) -> str:
    meta = cal_json["metadata"]
    windows = cal_json["windows"]
    coverage = meta["label_coverage_pct"]
    th = meta["thresholds"]
    lines: list[str] = [
        "# 4H Regime Calendar",
        "",
        f"**Method**: `{meta['method']}`",
        f"**Generated**: {meta['generated_at_utc']}",
        f"**Source data**: `{data_path}`",
        f"**Dataset hash**: `{meta['dataset_hash_sha256'][:16]}...`",
        f"**Fingerprint**: `{meta['fingerprint'][:16]}...`",
        "",
        "## Thresholds",
        "",
        "| Parameter | Value |",
        "|-----------|-------|",
    ]
    for k, v in th.items():
        lines.append(f"| `{k}` | `{v}` |")

    lines += [
        "",
        "## Label Coverage",
        "",
        "| Label | Coverage |",
        "|-------|----------|",
    ]
    for lbl, pct in coverage.items():
        display = LABEL_DISPLAY.get(lbl, lbl)
        lines.append(f"| {display} | {pct:.1f}% |")

    lines += [
        "",
        f"**Total windows**: {meta['total_windows']}",
        "",
        "## Windows",
        "",
        "| # | Start | End | Label | Bars | Source |",
        "|---|-------|-----|-------|------|--------|",
    ]
    for i, w in enumerate(windows, 1):
        display = LABEL_DISPLAY.get(w["label"], w["label"])
        bars = w.get("bars") or "—"
        lines.append(
            f"| {i} | {w['start'][:10]} | {w['end'][:10]} | {display} | {bars} | {w.get('source','auto')} |"
        )

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate 4H regime calendar from a Parquet file.")
    p.add_argument("--data", required=True, help="Path to 4H parquet file")
    p.add_argument("--out-json", default=str(DEFAULT_OUT_JSON))
    p.add_argument("--out-md", default=str(DEFAULT_OUT_MD))
    p.add_argument("--overrides", default=None, help="Path to manual overrides JSON")
    p.add_argument(
        "--thresholds",
        default=None,
        help="JSON string of threshold overrides, e.g. '{\"adx_threshold\": 20}'",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    data_path = Path(args.data).resolve()

    if not data_path.exists():
        print(f"[regime_cli] ERROR: data file not found: {data_path}", file=sys.stderr)
        sys.exit(1)

    print(f"[regime_cli] Loading {data_path} ...")
    df = pd.read_parquet(data_path)
    print(f"[regime_cli] {len(df)} bars, {df.index[0]} -> {df.index[-1]}")

    # Parse thresholds
    th_override = {}
    if args.thresholds:
        th_override = json.loads(args.thresholds)

    labeler = RegimeLabeler(thresholds=th_override)
    effective_thresholds = labeler.thresholds

    # Compute label series
    print("[regime_cli] Computing regime labels ...")
    label_series = labeler.label(df)

    # Compress to windows
    windows = labeler.compress_to_windows(label_series)
    print(f"[regime_cli] {len(windows)} contiguous windows found.")

    # Apply manual overrides
    if args.overrides:
        print(f"[regime_cli] Applying overrides from {args.overrides} ...")
        mo = ManualOverride.load(args.overrides)
    else:
        mo = ManualOverride.empty()
    windows = mo.apply(windows)

    # Hashes & fingerprint
    data_hash = sha256_file(data_path)
    fingerprint = labeler.compute_fingerprint(data_hash)
    generated_at = _now_utc()

    # Build output
    cal_json = render_json(windows, effective_thresholds, data_hash, fingerprint, generated_at)

    # Write JSON
    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(cal_json, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[regime_cli] OK JSON written -> {out_json}")

    # Write Markdown
    out_md = Path(args.out_md)
    out_md.write_text(render_markdown(cal_json, str(data_path)), encoding="utf-8")
    print(f"[regime_cli] OK Markdown written -> {out_md}")

    # Print coverage summary
    meta = cal_json["metadata"]
    print("\n[regime_cli] Coverage:")
    for lbl, pct in meta["label_coverage_pct"].items():
        print(f"  {LABEL_DISPLAY[lbl]:<12} {pct:5.1f}%")
    print(f"\n[regime_cli] Fingerprint: {fingerprint[:32]}...")


if __name__ == "__main__":
    main()
