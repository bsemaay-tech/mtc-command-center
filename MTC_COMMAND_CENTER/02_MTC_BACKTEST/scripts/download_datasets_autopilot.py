#!/usr/bin/env python
"""
Autopilot data bootstrap wrapper (parity-lock safe).

This script composes existing, proven commands:
- data_tools/download_cli.py
- data_tools/validate.py
- scripts/build_dataset_catalog.py
- scripts/data_parity_guard.py
- scripts/checksum_registry.py

It also builds compatibility parquet files under mtc_backtest/data
without changing engine semantics.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import yaml


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
REPO_ROOT = PROJECT_ROOT.parent


def _abs(path_like: str) -> Path:
    p = Path(path_like)
    return p if p.is_absolute() else (REPO_ROOT / p).resolve()


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Invalid YAML root: {path}")
    return data


def _run(cmd: list[str], *, cwd: Path) -> tuple[int, str, str]:
    p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def _load_catalog(catalog_path: Path) -> dict[str, Any]:
    if not catalog_path.exists():
        return {}
    payload = json.loads(catalog_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return {}
    return payload


def _resolve_entry_path(entry: dict[str, Any]) -> Path | None:
    abs_path = str(entry.get("abs_path", "")).strip()
    rel_path = str(entry.get("path", "")).strip()
    if abs_path:
        p = Path(abs_path)
        if p.exists():
            return p.resolve()
    if rel_path:
        p1 = (REPO_ROOT / rel_path).resolve()
        p2 = (REPO_ROOT / "110_" / rel_path).resolve()
        if p1.exists():
            return p1
        if p2.exists():
            return p2
    return None


def _ensure_timestamp_column(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "timestamp" not in out.columns:
        if isinstance(out.index, pd.DatetimeIndex):
            out = out.reset_index()
            if "timestamp" not in out.columns:
                out = out.rename(columns={str(out.columns[0]): "timestamp"})
        elif "index" in out.columns:
            out = out.rename(columns={"index": "timestamp"})
    if "timestamp" not in out.columns:
        raise ValueError("Dataset has no timestamp axis.")
    out["timestamp"] = pd.to_datetime(out["timestamp"], utc=True)
    return out


def _sync_compat_data(
    *,
    catalog: dict[str, Any],
    out_data_dir: Path,
    symbols: list[str],
) -> list[Path]:
    out_data_dir.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []

    for sym in symbols:
        sym_entry = catalog.get(sym, {})
        if not isinstance(sym_entry, dict):
            continue
        for tf, entry in sym_entry.items():
            if not isinstance(entry, dict):
                continue
            src = _resolve_entry_path(entry)
            if src is None or not src.exists():
                continue

            if src.suffix.lower() == ".parquet":
                df = pd.read_parquet(src)
            elif src.suffix.lower() == ".csv":
                df = pd.read_csv(src)
            else:
                continue

            df = _ensure_timestamp_column(df)
            start = df["timestamp"].min().date().strftime("%Y%m%d")
            end = df["timestamp"].max().date().strftime("%Y%m%d")
            out_file = out_data_dir / f"{sym}_{tf}_{start}_{end}.parquet"
            df.to_parquet(out_file, index=False)
            created.append(out_file.resolve())

            # Compatibility alias used by current default parity/backtest cases.
            if sym == "BTCUSDT" and tf == "15m":
                alias = out_data_dir / "BTCUSDT_15m_20240101_20260213.parquet"
                s = pd.Timestamp("2024-01-01T00:00:00Z")
                e = pd.Timestamp("2026-02-13T23:59:59Z")
                clipped = df[(df["timestamp"] >= s) & (df["timestamp"] <= e)].copy()
                if not clipped.empty:
                    clipped.to_parquet(alias, index=False)
                    created.append(alias.resolve())

    return created


def _catalog_has_symbol_tfs(catalog: dict[str, Any], symbol: str, tfs: list[str]) -> bool:
    sym_entry = catalog.get(symbol, {})
    if not isinstance(sym_entry, dict):
        return False
    for tf in tfs:
        entry = sym_entry.get(tf, {})
        if not isinstance(entry, dict):
            return False
        ds = _resolve_entry_path(entry)
        if ds is None or not ds.exists():
            return False
    return True


def _append_validation_extension(
    *,
    validation_report: Path,
    lines: list[str],
) -> None:
    validation_report.parent.mkdir(parents=True, exist_ok=True)
    if not validation_report.exists():
        validation_report.write_text("# Validation Report\n\n", encoding="utf-8")
    content = validation_report.read_text(encoding="utf-8")
    marker = "\n## Autopilot Extension Checks\n"
    if marker in content:
        content = content.split(marker, 1)[0].rstrip() + "\n"
    with validation_report.open("w", encoding="utf-8") as f:
        f.write(content)
        f.write("\n## Autopilot Extension Checks\n\n")
        for ln in lines:
            f.write(f"- {ln}\n")


def main() -> int:
    ap = argparse.ArgumentParser(description="Autopilot dataset build/validate wrapper.")
    ap.add_argument("--autorun", default="mtc_backtest/backtest_assets/autorun.yaml")
    ap.add_argument("--only-required", action="store_true")
    args = ap.parse_args()

    py = sys.executable
    autorun_path = _abs(args.autorun)
    autorun = _load_yaml(autorun_path)
    data_cfg = autorun.get("data", {})

    processed_root = _abs(str(data_cfg.get("processed_root", "110_/data/processed")))
    catalog_path = _abs(str(data_cfg.get("catalog", "mtc_backtest/backtest_assets/data_catalog.json")))
    validation_report = _abs(str(data_cfg.get("validation_report", "mtc_backtest/backtest_assets/validation_report.md")))
    validation_no_fail = bool(data_cfg.get("validation_no_fail", True))

    ext_lines: list[str] = []
    failed_required = False

    jobs = data_cfg.get("download_jobs", [])
    for job in jobs:
        if not isinstance(job, dict):
            continue
        required = bool(job.get("required", True))
        if args.only_required and not required:
            ext_lines.append(f"SKIP optional job: {job.get('symbol','UNKNOWN')}")
            continue
        cmd = [
            py,
            "mtc_backtest/data_tools/download_cli.py",
            "--provider",
            str(job.get("provider", "binance")),
            "--symbol",
            str(job.get("symbol", "BTCUSDT")),
            "--start",
            str(job.get("start", "2018-07-01")),
            "--timeframes",
            ",".join([str(x) for x in job.get("timeframes", ["15m"])]),
            "--out-root",
            str(processed_root),
            "--catalog",
            str(catalog_path),
        ]
        if job.get("end"):
            cmd.extend(["--end", str(job.get("end"))])
        if job.get("chunk_days") is not None:
            cmd.extend(["--chunk_days", str(int(job["chunk_days"]))])

        code, out, err = _run(cmd, cwd=REPO_ROOT)
        sym = str(job.get("symbol", "UNKNOWN"))
        if code == 0:
            ext_lines.append(f"PASS download {sym}")
        else:
            msg = (err or out or "").strip().splitlines()
            tail = msg[-1] if msg else "unknown error"
            if required:
                catalog_now = _load_catalog(catalog_path)
                tfs = [str(x) for x in job.get("timeframes", [])]
                if _catalog_has_symbol_tfs(catalog_now, sym, tfs):
                    ext_lines.append(f"PASS download {sym} (fallback existing catalog)")
                else:
                    failed_required = True
                    ext_lines.append(f"FAIL required download {sym}: {tail}")
            else:
                ext_lines.append(f"SKIP optional download {sym}: {tail}")

    # Optional CSV imports
    for job in data_cfg.get("csv_import_jobs", []):
        if not isinstance(job, dict):
            continue
        if not bool(job.get("enabled", False)):
            continue
        required = bool(job.get("required", False))
        cmd = [
            py,
            "mtc_backtest/data_tools/download_cli.py",
            "--provider",
            "csv",
            "--symbol",
            str(job.get("symbol", "CSV_SYMBOL")),
            "--csv-file",
            str(job.get("csv_file", "")),
            "--start",
            str(job.get("start", "2018-01-01")),
            "--timeframes",
            ",".join([str(x) for x in job.get("timeframes", ["1d"])]),
            "--out-root",
            str(processed_root),
            "--catalog",
            str(catalog_path),
        ]
        if job.get("end"):
            cmd.extend(["--end", str(job.get("end"))])
        code, out, err = _run(cmd, cwd=REPO_ROOT)
        sym = str(job.get("symbol", "CSV_SYMBOL"))
        if code == 0:
            ext_lines.append(f"PASS csv import {sym}")
        else:
            msg = (err or out or "").strip().splitlines()
            tail = msg[-1] if msg else "unknown error"
            if required:
                failed_required = True
                ext_lines.append(f"FAIL required csv import {sym}: {tail}")
            else:
                ext_lines.append(f"SKIP optional csv import {sym}: {tail}")

    # Validation (primary source: processed-root catalog)
    validate_cmd = [
        py,
        "mtc_backtest/data_tools/validate.py",
        "--catalog",
        str(catalog_path),
        "--out",
        str(validation_report),
    ]
    if validation_no_fail:
        validate_cmd.append("--no-fail")
    v_code, _, v_err = _run(validate_cmd, cwd=REPO_ROOT)
    ext_lines.append("PASS validate catalog" if v_code == 0 else f"FAIL validate catalog: {v_err.strip().splitlines()[-1] if v_err.strip() else 'error'}")

    # Build compatibility copies into mtc_backtest/data
    catalog = _load_catalog(catalog_path)
    symbols = [str(j.get("symbol", "")).strip() for j in jobs if isinstance(j, dict) and str(j.get("symbol", "")).strip()]
    compat_dir = (PROJECT_ROOT / "data").resolve()
    compat_files = _sync_compat_data(catalog=catalog, out_data_dir=compat_dir, symbols=symbols)
    ext_lines.append(f"PASS compat sync -> {len(compat_files)} files in {compat_dir}")

    # Build compatibility inventory for mtc_backtest/data
    compat_json = (PROJECT_ROOT / "backtest_assets" / "data_catalog_compat.json").resolve()
    compat_csv = (PROJECT_ROOT / "backtest_assets" / "data_catalog_compat.csv").resolve()
    inv_cmd = [
        py,
        "-m",
        "scripts.build_dataset_catalog",
        "--data-dir",
        str(compat_dir),
        "--out-json",
        str(compat_json),
        "--out-csv",
        str(compat_csv),
    ]
    i_code, _, i_err = _run(inv_cmd, cwd=PROJECT_ROOT)
    ext_lines.append("PASS compat catalog build" if i_code == 0 else f"FAIL compat catalog build: {i_err.strip().splitlines()[-1] if i_err.strip() else 'error'}")

    # Data parity guard + checksum registry on compatibility files (timestamp-column schema)
    checksum_registry = (PROJECT_ROOT / "backtest_assets" / "checksum_registry.json").resolve()
    guard_out_dir = (PROJECT_ROOT / "backtest_assets" / "quality").resolve()
    guard_out_dir.mkdir(parents=True, exist_ok=True)

    for ds in compat_files:
        stem = ds.stem
        parts = stem.split("_")
        sym = parts[0] if len(parts) > 0 else "UNKNOWN"
        tf = parts[1] if len(parts) > 1 else "unknown_tf"

        guard_out = guard_out_dir / f"{sym}_{tf}.json"
        g_cmd = [
            py,
            "-m",
            "scripts.data_parity_guard",
            "--dataset",
            str(ds),
            "--symbol",
            sym,
            "--exchange",
            "BINANCE",
            "--timeframe",
            str(tf),
            "--out",
            str(guard_out),
        ]
        g_code, _, g_err = _run(g_cmd, cwd=PROJECT_ROOT)
        ext_lines.append(f"{'PASS' if g_code == 0 else 'FAIL'} data_parity_guard {sym}:{tf}" + (f" ({g_err.strip().splitlines()[-1]})" if g_code != 0 and g_err.strip() else ""))

        c_cmd = [
            py,
            "-m",
            "scripts.checksum_registry",
            "--registry",
            str(checksum_registry),
            "--dataset",
            str(ds),
            "--symbol",
            sym,
            "--exchange",
            "BINANCE",
            "--timeframe",
            str(tf),
            "--update",
            "--verify",
        ]
        c_code, _, c_err = _run(c_cmd, cwd=PROJECT_ROOT)
        ext_lines.append(f"{'PASS' if c_code == 0 else 'FAIL'} checksum_registry {sym}:{tf}" + (f" ({c_err.strip().splitlines()[-1]})" if c_code != 0 and c_err.strip() else ""))

    _append_validation_extension(validation_report=validation_report, lines=ext_lines)

    print(f"autorun={autorun_path}")
    print(f"catalog={catalog_path}")
    print(f"validation_report={validation_report}")
    print(f"compat_catalog={compat_json}")
    print(f"compat_files={len(compat_files)}")
    print(f"generated_at={datetime.now(timezone.utc).isoformat()}")

    if failed_required:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
