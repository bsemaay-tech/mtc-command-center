from pathlib import Path
from datetime import datetime, timezone
import json

MCC_ROOT = Path(__file__).resolve().parents[5]
OVERNIGHT_DIR = MCC_ROOT / "03_QUANTLENS" / "tools" / "overnight_runs"
ALIVE_THRESHOLD_MINUTES = 15


def build_overnight_heartbeat() -> dict:
    """
    Reads all _heartbeat*.json files from overnight_runs/.
    Returns the most recent heartbeat's data plus an is_alive flag.
    """
    if not OVERNIGHT_DIR.exists():
        return {"available": False, "reason": "overnight_runs dir not found"}

    heartbeat_files = sorted(OVERNIGHT_DIR.glob("_heartbeat*.json"))
    if not heartbeat_files:
        return {"available": False, "reason": "no heartbeat files found"}

    # Pick most recent by mtime
    latest = max(heartbeat_files, key=lambda p: p.stat().st_mtime)

    try:
        data = json.loads(latest.read_text(encoding="utf-8"))
    except Exception as e:
        return {"available": False, "reason": f"parse error: {e}"}

    # Determine is_alive from timestamp field (try common key names)
    ts_str = data.get("timestamp") or data.get("ts") or data.get("updated_at")
    is_alive = False
    age_minutes = None
    if ts_str:
        try:
            ts = datetime.fromisoformat(str(ts_str).replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            age_minutes = (now - ts).total_seconds() / 60
            is_alive = age_minutes < ALIVE_THRESHOLD_MINUTES
        except Exception:
            pass

    return {
        "available": True,
        "source_file": latest.name,
        "is_alive": is_alive,
        "age_minutes": round(age_minutes, 1) if age_minutes is not None else None,
        "stage": data.get("stage") or data.get("phase") or data.get("step"),
        "status": data.get("status"),
        "run_id": data.get("run_id"),
        "timestamp": ts_str,
        "raw": data,
    }
