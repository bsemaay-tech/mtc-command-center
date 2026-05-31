from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BLOCKED_SHARED_PATH_PARTS = {
    ("data", "mtc_signals.json"),
    ("data", "pine_trades.csv"),
    ("reports", "parity"),
}


def utc_run_id(prefix: str = "run") -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{prefix}_{stamp}_{uuid.uuid4().hex[:8]}"


def safe_id(prefix: str, index: int) -> str:
    return f"{prefix}_{index:05d}"


@dataclass(frozen=True)
class WorkerPaths:
    root: Path
    run_id: str
    worker_id: str

    @property
    def worker_root(self) -> Path:
        return self.root / "workers" / self.worker_id

    @property
    def log_path(self) -> Path:
        return self.worker_root / "logs" / "worker.log"

    def variant_root(self, variant_id: str) -> Path:
        return self.worker_root / "variants" / variant_id


def ensure_worker(worker_paths: WorkerPaths) -> None:
    (worker_paths.worker_root / "logs").mkdir(parents=True, exist_ok=True)
    (worker_paths.worker_root / "variants").mkdir(parents=True, exist_ok=True)


def ensure_variant(worker_paths: WorkerPaths, variant_id: str) -> Path:
    ensure_worker(worker_paths)
    path = worker_paths.variant_root(variant_id)
    path.mkdir(parents=True, exist_ok=True)
    return path


def assert_isolated_output(path: Path, worker_root: Path) -> None:
    resolved = path.resolve()
    root = worker_root.resolve()
    if root not in [resolved, *resolved.parents]:
        raise ValueError(f"worker output escaped worker root: {resolved}")
    parts = tuple(part.lower() for part in resolved.parts)
    for blocked in BLOCKED_SHARED_PATH_PARTS:
        blocked_lower = tuple(part.lower() for part in blocked)
        if all(part in parts for part in blocked_lower):
            raise ValueError(f"blocked shared output path: {resolved}")


def write_json_isolated(path: Path, worker_root: Path, payload: dict[str, Any] | list[Any]) -> None:
    assert_isolated_output(path, worker_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + f".{os.getpid()}.tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    tmp.replace(path)


def append_log(worker_paths: WorkerPaths, message: str) -> None:
    ensure_worker(worker_paths)
    assert_isolated_output(worker_paths.log_path, worker_paths.worker_root)
    with worker_paths.log_path.open("a", encoding="utf-8") as fh:
        fh.write(f"{datetime.now(timezone.utc).isoformat()} {message}\n")
