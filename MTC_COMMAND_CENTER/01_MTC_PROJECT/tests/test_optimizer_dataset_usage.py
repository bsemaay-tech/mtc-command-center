from __future__ import annotations

import json
from pathlib import Path

from tools.validate_optimizer_dataset_usage import validate_job


def _write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def _bundle_files(tmp_path: Path) -> tuple[Path, Path, str]:
    bundle = tmp_path / "bundle"
    regime_file = bundle / "regimes" / "per_dataset" / "d1_regimes.csv"
    normalized = bundle / "normalized" / "d1.csv"
    raw = bundle / "raw" / "d1.csv"
    regime_file.parent.mkdir(parents=True)
    normalized.parent.mkdir(parents=True)
    raw.parent.mkdir(parents=True)
    regime_file.write_text("timestamp_utc,dataset_id,regime\n", encoding="utf-8")
    normalized.write_text("timestamp_utc,open,high,low,close\n", encoding="utf-8")
    raw.write_text("time,open,high,low,close\n", encoding="utf-8")
    dataset_id = "BINANCE_FUTURES_BTCUSDT_1h_20200101_20260427"
    manifest = _write_json(
        bundle / "manifests" / "dataset_manifest.json",
        {
            "datasets": [
                {
                    "dataset_id": dataset_id,
                    "symbol": "BTCUSDT",
                    "timeframe": "1h",
                    "timeframe_normalized": "1h",
                    "source_type": "binance_public_futures_klines",
                    "raw_path": str(raw.relative_to(bundle)),
                    "normalized_path": str(normalized.relative_to(bundle)),
                    "sha256_raw": "abc",
                    "sha256_normalized": "def",
                    "ohlcv_validation_status": "PASS",
                    "regime_file": str(regime_file.relative_to(bundle)),
                }
            ]
        },
    )
    regimes = _write_json(
        bundle / "regimes" / "regime_registry.json",
        {"datasets": [{"dataset_id": dataset_id, "regime_file": str(regime_file.relative_to(bundle))}]},
    )
    return manifest, regimes, dataset_id


def _job(tmp_path: Path, manifest: Path, regimes: Path, dataset_ids: list[str], **overrides: object) -> Path:
    payload = {
        "job_id": "job",
        "feature_id": "mtc_v2",
        "profile": "smoke",
        "dataset_manifest_path": str(manifest),
        "dataset_ids": dataset_ids,
        "regime_registry_path": str(regimes),
        "required_symbols_min": 1,
        "required_timeframes": ["1h"],
        "walkforward": {"enabled": True},
        "scoring_profile": "coverage_aware",
        "preconditions": {
            "require_hash_validation": True,
            "require_walkforward": True,
            "allow_unknown_source": False,
            "min_symbols_for_robust_claim": 2,
            "min_timeframes_for_robust_claim": 1,
        },
        "output_root": "reports/optimization/test",
    }
    payload.update(overrides)
    return _write_json(tmp_path / "job.yml", payload)


def test_valid_manifest_dataset_id_passes(tmp_path: Path) -> None:
    manifest, regimes, dataset_id = _bundle_files(tmp_path)
    report = validate_job(_job(tmp_path, manifest, regimes, [dataset_id]), manifest, regimes)

    assert report["status"] == "PASS"
    assert report["dataset_count"] == 1


def test_unknown_dataset_id_fails(tmp_path: Path) -> None:
    manifest, regimes, _dataset_id = _bundle_files(tmp_path)
    report = validate_job(_job(tmp_path, manifest, regimes, ["missing"]), manifest, regimes)

    assert report["status"] == "FAIL"
    assert any("unknown_dataset_id" in item for item in report["errors"])


def test_xlsx_path_as_chart_data_fails(tmp_path: Path) -> None:
    manifest, regimes, dataset_id = _bundle_files(tmp_path)
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    payload["datasets"][0]["raw_path"] = "raw/bad.xlsx"
    manifest.write_text(json.dumps(payload), encoding="utf-8")

    report = validate_job(_job(tmp_path, manifest, regimes, [dataset_id]), manifest, regimes)

    assert report["status"] == "FAIL"
    assert any("xlsx_chart_data_forbidden" in item for item in report["errors"])


def test_insufficient_symbol_coverage_warning(tmp_path: Path) -> None:
    manifest, regimes, dataset_id = _bundle_files(tmp_path)
    report = validate_job(
        _job(tmp_path, manifest, regimes, [dataset_id], required_symbols_min=2),
        manifest,
        regimes,
    )

    assert report["status"] == "PASS_WITH_WARNINGS"
    assert "INSUFFICIENT_SYMBOL_COVERAGE" in report["warnings"]


def test_missing_regime_file_fails(tmp_path: Path) -> None:
    manifest, regimes, dataset_id = _bundle_files(tmp_path)
    (tmp_path / "bundle" / "regimes" / "per_dataset" / "d1_regimes.csv").unlink()

    report = validate_job(_job(tmp_path, manifest, regimes, [dataset_id]), manifest, regimes)

    assert report["status"] == "FAIL"
    assert any("missing_regime_file" in item for item in report["errors"])
