#!/usr/bin/env python
"""
Build module-aware autopilot case files from a base case + module registry.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
REPO_ROOT = PROJECT_ROOT.parent


def _abs(path_like: str) -> Path:
    p = Path(path_like)
    return p if p.is_absolute() else (REPO_ROOT / p).resolve()


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Invalid YAML: {path}")
    return payload


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Invalid JSON: {path}")
    return payload


def _slug(s: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "_" for ch in s).strip("_")


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate module-specific autopilot cases.")
    ap.add_argument("--base-case", default="mtc_backtest/configs/cases/sep2025_parity.json")
    ap.add_argument("--registry", default="mtc_backtest/backtest_assets/module_registry.yaml")
    ap.add_argument("--out-dir", default="mtc_backtest/configs/cases/autopilot")
    args = ap.parse_args()

    base_case_path = _abs(args.base_case)
    registry_path = _abs(args.registry)
    out_dir = _abs(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    base = _load_json(base_case_path)
    reg = _load_yaml(registry_path)
    modules = reg.get("modules", [])
    if not isinstance(modules, list) or not modules:
        raise ValueError("module_registry.yaml must contain non-empty modules list")

    generated: list[Path] = []
    for m in modules:
        if not isinstance(m, dict):
            continue
        module_id = str(m.get("module_id", "")).strip()
        signal_mode_value = str(m.get("signal_mode_value", "")).strip()
        if not module_id or not signal_mode_value:
            continue

        case = json.loads(json.dumps(base))
        cfg = case.setdefault("config", {})
        cfg["signal_mode"] = signal_mode_value

        # Optional module-specific defaults overlay
        overlay = m.get("case_overrides", {})
        if isinstance(overlay, dict):
            for k, v in overlay.items():
                cfg[k] = v

        case["strategy_id"] = f"autopilot_{module_id}"
        case["module_id"] = module_id
        case["feature_flags"] = {"autopilot_module_case": True}
        case["_generated_at_utc"] = datetime.now(timezone.utc).isoformat()
        case["_generated_from"] = str(base_case_path)

        out_file = out_dir / f"{_slug(module_id)}.json"
        out_file.write_text(json.dumps(case, indent=2, ensure_ascii=False), encoding="utf-8")
        generated.append(out_file)

    index = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "base_case": str(base_case_path),
        "registry": str(registry_path),
        "cases": [str(p) for p in generated],
    }
    (out_dir / "INDEX.json").write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"generated_cases={len(generated)}")
    print(f"out_dir={out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

