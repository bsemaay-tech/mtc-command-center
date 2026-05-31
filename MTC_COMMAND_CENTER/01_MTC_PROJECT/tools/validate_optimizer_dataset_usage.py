from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ALLOWED_SOURCE_TYPES = {
    "binance_public_futures_klines",
    "tradingview_chart_csv_binance",
    "downloaded_ccxt",
}
FORBIDDEN_SOURCE_TYPES = {"tradingview_strategy_tester_xlsx"}
REPORT_ROOT = Path("reports/optimization_dataset_usage")


def load_json_or_sidecar(path: Path) -> dict[str, Any]:
    if not path.exists():
        sidecar = path.with_suffix(".json")
        if sidecar.exists():
            path = sidecar
        else:
            raise FileNotFoundError(str(path))
    text = path.read_text(encoding="utf-8-sig").strip()
    if text.startswith("{"):
        return json.loads(text)
    sidecar = path.with_suffix(".json")
    if sidecar.exists():
        return json.loads(sidecar.read_text(encoding="utf-8-sig"))
    raise ValueError(f"Only JSON or YAML with JSON sidecar is supported by this lightweight validator: {path}")


def bundle_root_from_manifest(manifest_path: Path) -> Path:
    if manifest_path.parent.name == "manifests":
        return manifest_path.parent.parent
    return manifest_path.parent


def resolve_bundle_path(bundle_root: Path, value: str | None) -> Path | None:
    if not value:
        return None
    path = Path(value)
    return path if path.is_absolute() else bundle_root / path


def load_manifest_entries(manifest_path: Path) -> list[dict[str, Any]]:
    payload = load_json_or_sidecar(manifest_path)
    entries = payload.get("datasets", payload if isinstance(payload, list) else [])
    if not isinstance(entries, list):
        raise ValueError("Manifest must contain a datasets list")
    return [dict(item) for item in entries]


def load_regime_entries(regime_path: Path) -> dict[str, dict[str, Any]]:
    payload = load_json_or_sidecar(regime_path)
    entries = payload.get("datasets", [])
    return {str(item.get("dataset_id")): dict(item) for item in entries if item.get("dataset_id")}


def selected_dataset_ids(job: dict[str, Any]) -> list[str]:
    ids = job.get("dataset_ids", [])
    if not isinstance(ids, list):
        raise ValueError("dataset_ids must be a list")
    return [str(item) for item in ids]


def validate_job(job_path: Path, manifest_path: Path | None = None, regimes_path: Path | None = None) -> dict[str, Any]:
    job = load_json_or_sidecar(job_path)
    manifest_path = Path(manifest_path or job.get("dataset_manifest_path", ""))
    regimes_path = Path(regimes_path or job.get("regime_registry_path", ""))
    entries = load_manifest_entries(manifest_path)
    regimes = load_regime_entries(regimes_path) if regimes_path else {}
    bundle_root = bundle_root_from_manifest(manifest_path)
    by_id = {str(item.get("dataset_id")): item for item in entries}
    errors: list[str] = []
    warnings: list[str] = []
    ids = selected_dataset_ids(job)
    selected: list[dict[str, Any]] = []
    for dataset_id in ids:
        if dataset_id not in by_id:
            errors.append(f"unknown_dataset_id:{dataset_id}")
            continue
        selected.append(by_id[dataset_id])

    preconditions = dict(job.get("preconditions", {}))
    allow_unknown = bool(preconditions.get("allow_unknown_source", False))
    require_hash = preconditions.get("require_hash_validation", True) is not False
    require_walkforward = preconditions.get("require_walkforward", True) is not False
    required_timeframes = [str(item) for item in job.get("required_timeframes", [])]
    required_symbols_min = int(job.get("required_symbols_min", preconditions.get("min_symbols_for_robust_claim", 2)))
    min_timeframes = int(preconditions.get("min_timeframes_for_robust_claim", 2))

    for item in selected:
        dataset_id = str(item.get("dataset_id"))
        source_type = str(item.get("source_type", ""))
        raw_path = str(item.get("raw_path", ""))
        normalized_path = str(item.get("normalized_path", ""))
        if raw_path.lower().endswith(".xlsx") or normalized_path.lower().endswith(".xlsx"):
            errors.append(f"xlsx_chart_data_forbidden:{dataset_id}")
        if source_type in FORBIDDEN_SOURCE_TYPES:
            errors.append(f"forbidden_source_type:{dataset_id}:{source_type}")
        if source_type == "unknown_csv" and not allow_unknown:
            errors.append(f"unknown_source_blocked:{dataset_id}")
        if source_type not in ALLOWED_SOURCE_TYPES and source_type != "unknown_csv":
            warnings.append(f"unrecognized_source_type:{dataset_id}:{source_type}")
        if require_hash and (not item.get("sha256_raw") or not item.get("sha256_normalized")):
            errors.append(f"missing_sha256:{dataset_id}")
        if str(item.get("ohlcv_validation_status", "")).upper() not in {"PASS", "WARN"}:
            errors.append(f"fatal_ohlcv_status:{dataset_id}:{item.get('ohlcv_validation_status')}")
        regime = regimes.get(dataset_id)
        if not regime:
            errors.append(f"missing_regime_registry_entry:{dataset_id}")
        else:
            regime_path = resolve_bundle_path(bundle_root, str(regime.get("regime_file", "")))
            if not regime_path or not regime_path.exists():
                errors.append(f"missing_regime_file:{dataset_id}")

    timeframes = sorted({str(item.get("timeframe_normalized") or item.get("timeframe")) for item in selected})
    symbols = sorted({str(item.get("symbol")) for item in selected})
    missing_timeframes = [timeframe for timeframe in required_timeframes if timeframe not in timeframes]
    for timeframe in missing_timeframes:
        warnings.append(f"MISSING_REQUIRED_TIMEFRAME:{timeframe}")
    if len(symbols) < required_symbols_min:
        warnings.append("INSUFFICIENT_SYMBOL_COVERAGE")
    if len(timeframes) < min_timeframes:
        warnings.append("INSUFFICIENT_TIMEFRAME_COVERAGE")
    if require_walkforward and not dict(job.get("walkforward", {})).get("enabled", False):
        errors.append("walkforward_required_but_disabled")

    status = "FAIL" if errors else "PASS_WITH_WARNINGS" if warnings else "PASS"
    report = {
        "status": status,
        "job_path": str(job_path),
        "manifest_path": str(manifest_path),
        "regime_registry_path": str(regimes_path),
        "dataset_count": len(selected),
        "symbols": symbols,
        "timeframes": timeframes,
        "source_types": sorted({str(item.get("source_type")) for item in selected}),
        "errors": errors,
        "warnings": warnings,
        "missing_timeframes": missing_timeframes,
    }
    return report


def write_reports(report: dict[str, Any]) -> None:
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    (REPORT_ROOT / "DATASET_USAGE_VALIDATION_REPORT.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    lines = [
        "# Dataset Usage Validation Report",
        "",
        f"- Status: `{report['status']}`",
        f"- Job: `{report['job_path']}`",
        f"- Manifest: `{report['manifest_path']}`",
        f"- Regime registry: `{report['regime_registry_path']}`",
        f"- Dataset count: `{report['dataset_count']}`",
        f"- Symbols: `{', '.join(report['symbols'])}`",
        f"- Timeframes: `{', '.join(report['timeframes'])}`",
        f"- Source types: `{', '.join(report['source_types'])}`",
        "",
        "## Errors",
        "",
    ]
    lines.extend(f"- `{item}`" for item in report["errors"]) if report["errors"] else lines.append("- None")
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- `{item}`" for item in report["warnings"]) if report["warnings"] else lines.append("- None")
    (REPORT_ROOT / "DATASET_USAGE_VALIDATION_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job", required=True)
    parser.add_argument("--manifest")
    parser.add_argument("--regimes")
    args = parser.parse_args()
    report = validate_job(
        Path(args.job),
        Path(args.manifest) if args.manifest else None,
        Path(args.regimes) if args.regimes else None,
    )
    write_reports(report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] != "FAIL" else 2


if __name__ == "__main__":
    raise SystemExit(main())
