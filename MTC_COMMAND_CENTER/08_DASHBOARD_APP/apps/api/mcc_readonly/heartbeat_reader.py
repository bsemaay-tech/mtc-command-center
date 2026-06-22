from pathlib import Path
from datetime import datetime, timezone
import json

MCC_ROOT = Path(__file__).resolve().parents[5]
OVERNIGHT_DIR = MCC_ROOT / "03_QUANTLENS" / "tools" / "overnight_runs"
ALIVE_THRESHOLD_MINUTES = 15
STALL_THRESHOLD_MINUTES = 15


def _age_minutes(ts_str) -> float | None:
    if not ts_str:
        return None
    try:
        ts = datetime.fromisoformat(str(ts_str).replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - ts).total_seconds() / 60
    except Exception:
        return None


def build_overnight_heartbeat(overnight_dir=None) -> dict:
    """
    Read run liveness/progress for the dashboard (read-only).

    Prefers the canonical progress contract (``progress/_latest.json`` ->
    ``mtc.run_progress/v1``) and derives running / stalled / dead / done / failed.
    Falls back to the legacy ``_heartbeat*.json`` glob for older runs.
    """
    base = Path(overnight_dir) if overnight_dir is not None else OVERNIGHT_DIR
    if not base.exists():
        return {"available": False, "reason": "overnight_runs dir not found"}

    new = _read_progress_contract(base)
    if new is not None:
        return new
    return _read_legacy_heartbeat(base)


def _read_progress_contract(base: Path):
    latest_path = base / "progress" / "_latest.json"
    if not latest_path.exists():
        return None
    try:
        run_id = json.loads(latest_path.read_text(encoding="utf-8")).get("run_id")
    except Exception as e:
        return {"available": False, "reason": f"_latest.json parse error: {e}"}
    if not run_id:
        return None

    run_dir = base / "progress" / run_id
    hb_path = run_dir / "heartbeat.json"
    if not hb_path.exists():
        return None
    try:
        hb = json.loads(hb_path.read_text(encoding="utf-8"))
    except Exception as e:
        return {"available": False, "reason": f"heartbeat parse error: {e}"}

    # process-liveness = freshest of heartbeat.updated_at and supervisor.alive_at
    proc_ts = hb.get("updated_at")
    sup_path = run_dir / "supervisor.json"
    if sup_path.exists():
        try:
            sup_alive = json.loads(sup_path.read_text(encoding="utf-8")).get("alive_at")
            if (_age_minutes(sup_alive) or 1e9) < (_age_minutes(proc_ts) or 1e9):
                proc_ts = sup_alive
        except Exception:
            pass

    proc_age = _age_minutes(proc_ts)
    progress_age = _age_minutes(hb.get("last_progress_at"))

    status = None
    status_path = run_dir / "status.json"
    if status_path.exists():
        try:
            status = json.loads(status_path.read_text(encoding="utf-8"))
        except Exception:
            status = None

    if status is not None:
        state = "done" if status.get("result") == "ok" else "failed"
        is_alive = False
    elif proc_age is None or proc_age >= ALIVE_THRESHOLD_MINUTES:
        state, is_alive = "dead", False
    elif progress_age is not None and progress_age >= STALL_THRESHOLD_MINUTES:
        state, is_alive = "stalled", True
    else:
        state, is_alive = "running", True

    progress = hb.get("progress") or {}
    return {
        "available": True,
        "source": "progress/v1",
        "run_id": run_id,
        "runner": hb.get("runner"),
        "state": state,
        "status": state,  # legacy-compatible alias
        "is_alive": is_alive,
        "age_minutes": round(proc_age, 1) if proc_age is not None else None,
        "progress_age_minutes": round(progress_age, 1) if progress_age is not None else None,
        "phase": hb.get("phase"),
        "stage": hb.get("phase"),  # legacy-compatible alias
        "progress_pct": progress.get("pct"),
        "progress_current": progress.get("current"),
        "progress_total": progress.get("total"),
        "eta_seconds": progress.get("eta_seconds"),
        "counters": hb.get("counters") or {},
        "updated_at": hb.get("updated_at"),
        "last_progress_at": hb.get("last_progress_at"),
        "timestamp": hb.get("updated_at"),  # legacy-compatible alias
        "result": (status or {}).get("result"),
        "exit_code": (status or {}).get("exit_code"),
        "raw": hb,
    }


def _read_legacy_heartbeat(base: Path) -> dict:
    heartbeat_files = sorted(base.glob("_heartbeat*.json"))
    if not heartbeat_files:
        return {"available": False, "reason": "no heartbeat files found"}

    latest = max(heartbeat_files, key=lambda p: p.stat().st_mtime)
    try:
        data = json.loads(latest.read_text(encoding="utf-8"))
    except Exception as e:
        return {"available": False, "reason": f"parse error: {e}"}

    ts_str = data.get("timestamp") or data.get("ts") or data.get("updated_at")
    age_minutes = _age_minutes(ts_str)
    is_alive = age_minutes is not None and age_minutes < ALIVE_THRESHOLD_MINUTES

    return {
        "available": True,
        "source": "legacy",
        "source_file": latest.name,
        "is_alive": is_alive,
        "age_minutes": round(age_minutes, 1) if age_minutes is not None else None,
        "stage": data.get("stage") or data.get("phase") or data.get("step"),
        "status": data.get("status"),
        "state": data.get("status"),
        "run_id": data.get("run_id"),
        "timestamp": ts_str,
        "raw": data,
    }
