from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from .paths import canonicalize, load_path_config, resolve_configured_path
from .read_model import build_read_model


PATH_KEYS = (
    "mcc_root",
    "mtc_v2_root",
    "mtc_v2_python_exe",
    "pinets_root",
    "tradingview_exports_dir",
    "reports_root",
)


def build_health_report(mcc_root: str | Path | None = None) -> dict[str, Any]:
    root = canonicalize(mcc_root or Path(__file__).resolve().parents[4])
    model = build_read_model(root)
    path_config = load_path_config(root)
    config = path_config.config

    path_checks = _build_path_checks(config)
    lock_dirs = {
        "status_locks": _dir_access(root / "03_STATUS" / ".locks"),
        "task_locks": _dir_access(root / "02_TASKS" / ".locks"),
    }
    mtc_v2_root = resolve_configured_path(config, "mtc_v2_root")
    mtc_v2_root_reachable = bool(mtc_v2_root and mtc_v2_root.exists() and mtc_v2_root.is_dir())

    required_files_ok = bool(model["summary"]["required_files_ok"])
    schema_validation_ok = bool(model["summary"]["schema_validation_ok"])
    lock_dir_writable = all(item["exists"] and item["writable"] for item in lock_dirs.values())
    paths_resolvable = all(item["resolvable"] for item in path_checks.values())

    checks = {
        "api_ok": True,
        "read_only": True,
        "required_files_ok": required_files_ok,
        "schema_validation_ok": schema_validation_ok,
        "lock_dir_writable": lock_dir_writable,
        "paths_resolvable": paths_resolvable,
        "mtc_v2_root_reachable": mtc_v2_root_reachable,
    }

    warnings = list(path_config.warnings)
    configured_mcc_root = resolve_configured_path(config, "mcc_root")
    if configured_mcc_root and configured_mcc_root != root:
        warnings.append(f"configured mcc_root differs from runtime root: {configured_mcc_root}")

    return {
        "schema_version": "1.0",
        "service": "mcc-readonly-api",
        "mode": "read_only",
        "overall_ok": all(checks.values()),
        "checks": checks,
        "api_ok": checks["api_ok"],
        "schema_validation_ok": schema_validation_ok,
        "lock_dir_writable": lock_dir_writable,
        "paths_resolvable": paths_resolvable,
        "mtc_v2_root_reachable": mtc_v2_root_reachable,
        "mcc_root": str(root),
        "path_config_sources": path_config.sources,
        "path_checks": path_checks,
        "lock_dirs": lock_dirs,
        "read_model_summary": model["summary"],
        "warnings": warnings,
    }


def _build_path_checks(config: dict[str, Any]) -> dict[str, Any]:
    checks: dict[str, Any] = {}
    for key in PATH_KEYS:
        value = config.get(key)
        if value in (None, ""):
            checks[key] = {
                "configured": False,
                "resolvable": True,
                "exists": None,
                "path": None,
            }
            continue
        try:
            resolved = canonicalize(str(value))
            checks[key] = {
                "configured": True,
                "resolvable": True,
                "exists": resolved.exists(),
                "path": str(resolved),
            }
        except Exception as exc:
            checks[key] = {
                "configured": True,
                "resolvable": False,
                "exists": False,
                "path": str(value),
                "error": str(exc),
            }
    return checks


def _dir_access(path: Path) -> dict[str, Any]:
    return {
        "path": str(path),
        "exists": path.exists() and path.is_dir(),
        "readable": os.access(path, os.R_OK),
        "writable": os.access(path, os.W_OK),
    }

