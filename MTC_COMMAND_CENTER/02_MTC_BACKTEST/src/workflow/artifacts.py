from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def utc_now_compact() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


def _run_git(args: list[str], cwd: Path) -> str:
    try:
        out = subprocess.check_output(["git", *args], cwd=str(cwd), text=True, stderr=subprocess.DEVNULL)
        return out.strip()
    except Exception:
        return ""


def git_identity(project_root: Path) -> dict[str, Any]:
    commit = _run_git(["rev-parse", "HEAD"], project_root)
    branch = _run_git(["rev-parse", "--abbrev-ref", "HEAD"], project_root)
    dirty = bool(_run_git(["status", "--porcelain"], project_root))
    return {"git_commit": commit, "git_branch": branch, "git_dirty": dirty}


def sha256_bytes(data: bytes) -> str:
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_paths(paths: Iterable[Path]) -> str:
    h = hashlib.sha256()
    for p in sorted(paths, key=lambda x: str(x).replace("\\", "/")):
        h.update(str(p).encode("utf-8", errors="ignore"))
        try:
            h.update(p.read_bytes())
        except Exception:
            continue
    return h.hexdigest()


def config_hash(config_obj: Any) -> str:
    if hasattr(config_obj, "model_dump_json"):
        payload = config_obj.model_dump_json().encode("utf-8")
    else:
        payload = json.dumps(config_obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return sha256_bytes(payload)


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def default_artifact_dir(project_root: Path, run_type: str, run_name: str) -> Path:
    ts = utc_now_compact()
    safe_name = "".join(c if c.isalnum() or c in {"_", "-"} else "_" for c in run_name).strip("_")
    if not safe_name:
        safe_name = "run"
    outdir = project_root / "results" / f"{run_type}_runs" / f"{safe_name}_{ts}"
    return ensure_dir(outdir)


def build_manifest(
    *,
    project_root: Path,
    run_type: str,
    run_id: str,
    case_file: Path | None = None,
    dataset_file: Path | None = None,
    symbol: str | None = None,
    timeframe: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    config_obj: Any = None,
    seed: int | None = None,
    workers: int | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    git = git_identity(project_root)
    engine_py = list((project_root / "src" / "engine").rglob("*.py"))
    engine_hash = sha256_paths(engine_py)

    dataset_hash = ""
    dataset_rows = None
    if dataset_file is not None and dataset_file.exists():
        dataset_hash = sha256_file(dataset_file)

    case_hash = ""
    if case_file is not None and case_file.exists():
        case_hash = sha256_file(case_file)

    manifest: dict[str, Any] = {
        "manifest_version": "1",
        "run_id": run_id,
        "run_type": run_type,
        "created_at": utc_now_iso(),
        "python_version": sys.version,
        "python_executable": sys.executable,
        "platform": os.name,
        "engine_module_hash": engine_hash,
        "case_file": str(case_file) if case_file else "",
        "case_file_hash": case_hash,
        "dataset_file": str(dataset_file) if dataset_file else "",
        "dataset_hash": dataset_hash,
        "dataset_rows": dataset_rows,
        "symbol": symbol or "",
        "timeframe": timeframe or "",
        "start_date": start_date or "",
        "end_date": end_date or "",
        "config_hash": config_hash(config_obj) if config_obj is not None else "",
        "seed": seed,
        "workers": workers,
    }
    manifest.update(git)
    if extra:
        manifest.update(extra)
    return manifest


def write_manifest(outdir: Path, manifest: dict[str, Any]) -> Path:
    ensure_dir(outdir)
    out = outdir / "manifest.json"
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return out


def write_results(outdir: Path, payload: dict[str, Any]) -> Path:
    ensure_dir(outdir)
    out = outdir / "results.json"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    return out


def write_report(outdir: Path, markdown: str) -> Path:
    ensure_dir(outdir)
    out = outdir / "report.md"
    out.write_text(markdown, encoding="utf-8")
    return out


def render_simple_report(
    *,
    title: str,
    run_id: str,
    status: str,
    key_values: dict[str, Any],
    artifact_paths: dict[str, str] | None = None,
) -> str:
    lines = [
        f"# {title}",
        "",
        f"- run_id: `{run_id}`",
        f"- status: `{status}`",
    ]
    for k, v in key_values.items():
        lines.append(f"- {k}: `{v}`")
    if artifact_paths:
        lines.append("")
        lines.append("## Artifacts")
        for k, v in artifact_paths.items():
            lines.append(f"- {k}: `{v}`")
    lines.append("")
    return "\n".join(lines)

