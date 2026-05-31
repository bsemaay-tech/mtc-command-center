"""
Run history and artifact helpers for Streamlit UI.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from src.optimizer_v0.store_sqlite import SQLiteStore


def resolve_db_path(candidates: List[str] | None = None) -> Path:
    if candidates is None:
        candidates = ["results/optimizer_v0.db", "results/results.db", "results.db"]
    for raw in candidates:
        p = Path(raw)
        if p.exists():
            return p
    return Path(candidates[0])


def load_run_history(db_path: Path, limit: int = 50) -> List[Dict[str, Any]]:
    if not db_path.exists():
        return []
    store = SQLiteStore(db_path)
    return store.list_runs(limit=limit)


def summarize_run(db_path: Path, run_id: str) -> Dict[str, Any]:
    store = SQLiteStore(db_path)
    run = store.get_run(run_id)
    trials = [dict(r) for r in store.fetch_trials(run_id)]
    ok = [t for t in trials if t.get("status") == "OK"]
    pruned = [t for t in trials if t.get("status") == "PRUNED"]
    errors = [t for t in trials if str(t.get("status", "")).startswith("ERROR")]
    ok_scores = [float(t["score"]) for t in ok if t.get("score") is not None]
    best_score = max(ok_scores) if ok_scores else None
    return {
        "run": run,
        "counts": {
            "total": len(trials),
            "ok": len(ok),
            "pruned": len(pruned),
            "errors": len(errors),
        },
        "best_score": best_score,
    }


def compare_runs(db_path: Path, run_a: str, run_b: str) -> Dict[str, Any]:
    store = SQLiteStore(db_path)
    trials_a = [dict(r) for r in store.fetch_trials(run_a)]
    trials_b = [dict(r) for r in store.fetch_trials(run_b)]
    keys_a = {t["params_key"] for t in trials_a if t.get("params_key")}
    keys_b = {t["params_key"] for t in trials_b if t.get("params_key")}
    overlap = keys_a.intersection(keys_b)
    ok_a = [t for t in trials_a if t.get("status") == "OK" and t.get("score") is not None]
    ok_b = [t for t in trials_b if t.get("status") == "OK" and t.get("score") is not None]
    best_a = max((float(t["score"]) for t in ok_a), default=None)
    best_b = max((float(t["score"]) for t in ok_b), default=None)
    return {
        "run_a": run_a,
        "run_b": run_b,
        "overlap_params_key": len(overlap),
        "best_score_a": best_a,
        "best_score_b": best_b,
        "trials_a": len(trials_a),
        "trials_b": len(trials_b),
    }


def list_result_artifacts(results_dir: Path, run_hint: str = "") -> List[Path]:
    if not results_dir.exists():
        return []
    files = [p for p in results_dir.rglob("*") if p.is_file()]
    files.sort(key=lambda p: p.as_posix())
    if run_hint:
        hinted = [p for p in files if run_hint in p.as_posix()]
        if hinted:
            return hinted
    return files


def read_artifact_preview(path: Path, max_chars: int = 4000) -> str:
    suffix = path.suffix.lower()
    if suffix in {".json"}:
        data = json.loads(path.read_text(encoding="utf-8"))
        return json.dumps(data, indent=2)[:max_chars]
    text = path.read_text(encoding="utf-8", errors="replace")
    return text[:max_chars]
