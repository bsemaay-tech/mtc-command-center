from __future__ import annotations

import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .paths import canonicalize, default_mcc_root, load_path_config, resolve_configured_path


_YOUTUBE_URL_RE = re.compile(
    r"https?://(?:www\.)?(?:youtube\.com/watch\?v=[^\s<>\")]+|youtu\.be/[^\s<>\")]+)",
    re.IGNORECASE,
)


def build_strategy_registry(mcc_root: str | Path | None = None) -> dict[str, Any]:
    root = canonicalize(mcc_root or default_mcc_root())
    path_config = load_path_config(root)
    mtc_v2_root = resolve_configured_path(path_config.config, "mtc_v2_root")
    if mtc_v2_root is None:
        return _empty_registry("mtc_v2_root_not_configured")

    quantlens_root = mtc_v2_root / "06_QUANTLENS_LAB"
    if not quantlens_root.exists():
        return _empty_registry(str(quantlens_root))

    candidates = _read_candidates(quantlens_root)
    strategies = _read_promoted_strategies(quantlens_root)
    timestamps = [item.get("updated_at") for item in candidates + strategies if item.get("updated_at")]
    return {
        "schema_version": "1.0",
        "generated_at": max(timestamps) if timestamps else None,
        "candidates": candidates,
        "strategies": strategies,
    }


def _read_candidates(quantlens_root: Path) -> list[dict[str, Any]]:
    csv_path = quantlens_root / "_registry" / "quantlens_candidate_registry.csv"
    jsonl_path = quantlens_root / "_registry" / "quantlens_candidate_registry.jsonl"
    if csv_path.exists():
        return _read_candidate_csv(csv_path, quantlens_root)
    if jsonl_path.exists():
        return _read_candidate_jsonl(jsonl_path, quantlens_root)
    return _discover_candidate_folders(quantlens_root)


def _read_candidate_csv(path: Path, quantlens_root: Path) -> list[dict[str, Any]]:
    candidates = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, [])
        for fields in reader:
            row = _candidate_csv_row(header, fields)
            candidates.append(_candidate_from_row(row, path, quantlens_root))
    return candidates


def _read_candidate_jsonl(path: Path, quantlens_root: Path) -> list[dict[str, Any]]:
    candidates = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict):
            candidates.append(_candidate_from_row(row, path, quantlens_root))
    return candidates


def _discover_candidate_folders(quantlens_root: Path) -> list[dict[str, Any]]:
    folders = []
    for stage, status in (("01_TRIAGED_CANDIDATES", "TRIAGED"), ("03_SALVAGE_IDEAS", "SALVAGE_ONLY")):
        root = quantlens_root / stage
        if not root.exists():
            continue
        for path in sorted(root.iterdir()):
            if path.is_dir():
                stat = path.stat()
                folders.append(
                    {
                        "id": path.name,
                        "candidate_id": path.name,
                        "name": path.name,
                        "status": status,
                        "evidence_level": "folder_only",
                        "candidate_folder": _relative_to_lab(path, quantlens_root),
                        "updated_at": _timestamp(stat.st_mtime),
                        "source_path": str(path),
                    }
                )
    return folders


def _candidate_from_row(row: dict[str, Any], source_path: Path, quantlens_root: Path) -> dict[str, Any]:
    candidate_id = str(row.get("candidate_id") or "").strip()
    status = str(row.get("status") or "UNKNOWN").strip()
    folder = str(row.get("candidate_folder") or "").strip()
    backtest_path = quantlens_root / "05_BACKTEST_RESULTS" / f"{candidate_id}_results.json"
    summary_path = quantlens_root / "05_BACKTEST_RESULTS" / f"{candidate_id}_summary.md"
    raw_source_url = _normalize_source_url(row.get("source_url"))
    source_url = raw_source_url
    if not source_url:
        source_url = _source_url_from_candidate_folder(folder, quantlens_root)
    return {
        "id": candidate_id,
        "candidate_id": candidate_id,
        "name": row.get("title") or candidate_id,
        "title": row.get("title") or candidate_id,
        "status": status,
        "evidence_level": _candidate_evidence(status, backtest_path, summary_path),
        "notes": row.get("next_action") or row.get("mtc_overlap") or "",
        "source_url": source_url or row.get("source_url"),
        "source_url_source": "candidate_folder" if source_url and not raw_source_url else ("source_record" if raw_source_url else ""),
        "market_type": row.get("market_type"),
        "timeframe": row.get("timeframe"),
        "candidate_kind": _split_kind(row.get("candidate_kind")),
        "commercial_value_score": _as_int(row.get("commercial_value_score")),
        "complexity_score": _as_int(row.get("complexity_score")),
        "repaint_risk": row.get("repaint_risk"),
        "lookahead_risk": row.get("lookahead_risk"),
        "closed_source_risk": row.get("closed_source_risk"),
        "candidate_folder": folder,
        "backtest_result_path": _relative_to_lab(backtest_path, quantlens_root) if backtest_path.exists() else None,
        "summary_path": _relative_to_lab(summary_path, quantlens_root) if summary_path.exists() else None,
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at") or _timestamp(source_path.stat().st_mtime),
        "source_path": str(source_path),
    }


def _source_url_from_candidate_folder(folder: str, quantlens_root: Path) -> str:
    if not folder:
        return ""
    rel = Path(folder)
    candidate_roots = [quantlens_root / rel, quantlens_root.parent / rel]
    for base in candidate_roots:
        if base.exists():
            url = _first_youtube_url_in_dir(base)
            if url:
                return url
    return ""


def _first_youtube_url_in_dir(path: Path) -> str:
    for candidate in sorted(path.rglob("*.md")):
        url = _first_youtube_url_in_file(candidate)
        if url:
            return url
    return ""


def _first_youtube_url_in_file(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""
    match = _YOUTUBE_URL_RE.search(text)
    if not match:
        return ""
    return _normalize_source_url(match.group(0))


def _normalize_source_url(value: Any) -> str:
    url = str(value or "").strip()
    if not url or url.upper() == "UNKNOWN_URL":
        return ""
    match = _YOUTUBE_URL_RE.search(url)
    if match:
        return match.group(0).rstrip(").,")
    return url


def _candidate_csv_row(header: list[str], fields: list[str]) -> dict[str, Any]:
    if len(fields) <= len(header):
        return dict(zip(header, fields))

    # Some historical rows contain unquoted commas in mtc_overlap. Keep the
    # stable leading columns and the stable trailing workflow/date columns.
    repaired = fields[:12]
    repaired.append(",".join(field.strip() for field in fields[12:-4]))
    repaired.extend(fields[-4:])
    return dict(zip(header, repaired))


def _read_promoted_strategies(quantlens_root: Path) -> list[dict[str, Any]]:
    promoted_root = quantlens_root / "06_PROMOTED_TO_PARITY"
    if not promoted_root.exists():
        return []

    strategies = []
    for spec_path in sorted(promoted_root.glob("*/producer_spec.json")):
        try:
            raw = json.loads(spec_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(raw, dict):
            strategies.append(_strategy_from_spec(raw, spec_path, quantlens_root))
    return strategies


def _strategy_from_spec(raw: dict[str, Any], spec_path: Path, quantlens_root: Path) -> dict[str, Any]:
    metrics = raw.get("metrics_lockbox") if isinstance(raw.get("metrics_lockbox"), dict) else {}
    status_values = raw.get("promotion_status")
    if isinstance(status_values, list):
        status = "|".join(str(item) for item in status_values)
    else:
        status = str(status_values or "PROMOTED")
    return {
        "id": raw.get("candidate_id") or spec_path.parent.name,
        "strategy_id": raw.get("candidate_id") or spec_path.parent.name,
        "candidate_id": raw.get("engine_strategy_id"),
        "name": raw.get("strategy_family") or raw.get("candidate_id") or spec_path.parent.name,
        "status": status,
        "evidence_level": "promoted_to_parity",
        "notes": _strategy_notes(metrics),
        "symbol": raw.get("symbol"),
        "timeframe": raw.get("timeframe"),
        "direction": raw.get("direction"),
        "return_pct_compound": metrics.get("return_pct_compound"),
        "profit_factor": metrics.get("profit_factor"),
        "trades": metrics.get("trades"),
        "max_drawdown_pct": metrics.get("max_drawdown_pct"),
        "win_rate": metrics.get("win_rate"),
        "param_stable": metrics.get("param_stable"),
        "source_path": str(spec_path),
        "updated_at": _timestamp(spec_path.stat().st_mtime),
    }


def _candidate_evidence(status: str, backtest_path: Path, summary_path: Path) -> str:
    normalized = status.upper()
    if backtest_path.exists():
        return "backtested"
    if summary_path.exists():
        return "summary_only"
    if "PROTOTYPED" in normalized:
        return "prototype_recorded"
    if "SALVAGE" in normalized:
        return "salvage_only"
    return "triaged"


def _strategy_notes(metrics: dict[str, Any]) -> str:
    parts = []
    if metrics.get("return_pct_compound") is not None:
        parts.append(f"return {metrics.get('return_pct_compound')}%")
    if metrics.get("profit_factor") is not None:
        parts.append(f"PF {metrics.get('profit_factor')}")
    if metrics.get("trades") is not None:
        parts.append(f"{metrics.get('trades')} trades")
    return ", ".join(parts)


def _split_kind(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [item for item in str(value).replace("|", ",").split(",") if item]


def _relative_to_lab(path: Path, quantlens_root: Path) -> str:
    try:
        return str(path.relative_to(quantlens_root.parent))
    except ValueError:
        return str(path)


def _as_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _timestamp(epoch_seconds: float) -> str:
    return datetime.fromtimestamp(epoch_seconds, timezone.utc).isoformat()


def _empty_registry(source: str) -> dict[str, Any]:
    _ = source
    return {
        "schema_version": "1.0",
        "generated_at": None,
        "candidates": [],
        "strategies": [],
    }
