#!/usr/bin/env python
"""
Generate 4H regime calendar using autorun defaults + optional YAML overrides.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
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
    if not path.exists():
        return {}
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def _load_catalog(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Catalog not found: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Invalid catalog structure: {path}")
    return payload


def _resolve_data_ref(data_ref: str, catalog: dict[str, Any]) -> Path:
    ref = str(data_ref).strip()
    if ":" not in ref:
        p = _abs(ref)
        if p.exists():
            return p
        raise FileNotFoundError(f"Dataset not found: {p}")

    symbol, tf = [x.strip() for x in ref.split(":", 1)]
    entry = catalog.get(symbol, {}).get(tf, {})
    if not isinstance(entry, dict):
        raise FileNotFoundError(f"Catalog entry not found for {ref}")
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
    raise FileNotFoundError(f"Unable to resolve data_ref {ref}")


def _build_overrides_json(override_yaml_path: Path) -> Path | None:
    if not override_yaml_path.exists():
        return None
    payload = _load_yaml(override_yaml_path)
    windows = payload.get("windows", [])
    enabled = bool(payload.get("enabled", True))
    if not enabled or not isinstance(windows, list) or not windows:
        return None

    normalized = []
    for w in windows:
        if not isinstance(w, dict):
            continue
        s = str(w.get("start", "")).strip()
        e = str(w.get("end", "")).strip()
        label = str(w.get("label", "")).strip()
        if not s or not e or not label:
            continue
        normalized.append({"start": s, "end": e, "label": label})

    if not normalized:
        return None

    tmp = tempfile.NamedTemporaryFile(prefix="regime_override_", suffix=".json", delete=False)
    tmp_path = Path(tmp.name)
    tmp.close()
    tmp_path.write_text(json.dumps(normalized, indent=2, ensure_ascii=False), encoding="utf-8")
    return tmp_path


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate regime calendar (4H) from autorun defaults.")
    ap.add_argument("--autorun", default="mtc_backtest/backtest_assets/autorun.yaml")
    ap.add_argument("--override-yaml", default="mtc_backtest/backtest_assets/regime_override.yaml")
    args = ap.parse_args()

    py = sys.executable
    autorun = _load_yaml(_abs(args.autorun))
    regime_cfg = autorun.get("regime", {})
    data_cfg = autorun.get("data", {})

    catalog_path = _abs(str(data_cfg.get("catalog", "mtc_backtest/backtest_assets/data_catalog.json")))
    catalog = _load_catalog(catalog_path)
    data_ref = str(regime_cfg.get("data_4h_ref", "BTCUSDT:4h"))
    data_path = _resolve_data_ref(data_ref, catalog)

    out_json = _abs(str(regime_cfg.get("out_json", "mtc_backtest/backtest_assets/regime_calendar_4h.json")))
    out_md = _abs(str(regime_cfg.get("out_md", "mtc_backtest/backtest_assets/regime_calendar_4h.md")))
    out_json.parent.mkdir(parents=True, exist_ok=True)

    override_json = _build_overrides_json(_abs(args.override_yaml))
    cmd = [
        py,
        "mtc_backtest/regimes/regime_cli.py",
        "--data",
        str(data_path),
        "--out-json",
        str(out_json),
        "--out-md",
        str(out_md),
    ]
    if override_json is not None:
        cmd.extend(["--overrides", str(override_json)])

    p = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    if p.stdout:
        print(p.stdout)
    if p.stderr:
        print(p.stderr)
    if p.returncode != 0:
        return p.returncode

    print(f"data_4h={data_path}")
    print(f"out_json={out_json}")
    print(f"out_md={out_md}")
    if override_json is not None:
        print(f"override_json={override_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

