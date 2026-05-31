from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class PathConfig:
    mcc_root: Path
    config: dict[str, Any]
    sources: list[str]
    warnings: list[str]


def default_mcc_root() -> Path:
    return Path(__file__).resolve().parents[4]


def canonicalize(path: str | Path) -> Path:
    return Path(path).expanduser().resolve(strict=False)


def windows_api_path(path: str | Path, threshold: int = 240) -> str:
    canonical = str(canonicalize(path))
    if os.name != "nt" or len(canonical) < threshold or canonical.startswith("\\\\?\\"):
        return canonical
    if canonical.startswith("\\\\"):
        return "\\\\?\\UNC\\" + canonical.lstrip("\\")
    return "\\\\?\\" + canonical


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_path_config(mcc_root: str | Path | None = None) -> PathConfig:
    root = canonicalize(mcc_root or default_mcc_root())
    config_dir = root / "00_CONFIG"
    example_path = config_dir / "paths.example.json"
    local_path = config_dir / "paths.local.json"
    sources: list[str] = []
    warnings: list[str] = []
    config: dict[str, Any] = {}

    if example_path.exists():
        config.update(_read_json(example_path))
        sources.append(str(example_path.relative_to(root)))
    else:
        warnings.append("00_CONFIG/paths.example.json is missing")

    if local_path.exists():
        local_config = _read_json(local_path)
        config.update({key: value for key, value in local_config.items() if value is not None})
        sources.append(str(local_path.relative_to(root)))

    if not config:
        warnings.append("No path configuration could be loaded")

    return PathConfig(mcc_root=root, config=config, sources=sources, warnings=warnings)


def resolve_configured_path(config: dict[str, Any], key: str) -> Path | None:
    value = config.get(key)
    if value in (None, ""):
        return None
    return canonicalize(str(value))

