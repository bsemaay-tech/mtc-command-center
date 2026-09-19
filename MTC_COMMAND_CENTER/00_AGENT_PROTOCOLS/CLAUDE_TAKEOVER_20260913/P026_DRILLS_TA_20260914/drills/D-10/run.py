import json
import os
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

LANE = Path(r"C:/tmp/P026_DRILLS_TA_20260914")
_TMP = LANE / "tmp"
_TMP.mkdir(parents=True, exist_ok=True)
os.environ["TEMP"] = str(_TMP)
os.environ["TMP"] = str(_TMP)
os.environ["PYTHONUTF8"] = "1"

python = r"C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe"
watchdog_py = LANE / "wt" / "MTC_COMMAND_CENTER" / "tools" / "opsa" / "watchdog.py"
BASE = LANE / "fixtures"
state_dir = BASE / "watchdog_state" / "recovery"
state_file = BASE / "watchdog_state" / "recovery_state.json"
log_path = BASE / "watchdog_state" / "recovery_notifier.jsonl"
state_dir.mkdir(parents=True, exist_ok=True)
for child in sorted(state_dir.glob("*")):
    if child.is_file():
        child.unlink()
    elif child.is_dir():
        for c in sorted(child.rglob("*"), reverse=True):
            if c.is_file():
                c.unlink()
            elif c.is_dir():
                try:
                    c.rmdir()
                except OSError:
                    pass
        try:
            child.rmdir()
        except OSError:
            pass
if state_file.exists():
    state_file.unlink()
if log_path.exists():
    log_path.unlink()

id_name = "p030_market_data_collector"
base = datetime(2026, 9, 14, 6, 0, 0, tzinfo=timezone.utc)
hb_path = state_dir / f"{id_name}.hb.json"


def emit_at(ts: datetime):
    payload = {
        "schema": "mtc.opsa_heartbeat/v1",
        "id": id_name,
        "seq": 1,
        "emitted_at": ts.isoformat().replace("+00:00", "Z"),
        "pid": 777,
    }
    hb_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def run_watchdog(name, now_dt):
    cmd = [
        python,
        str(watchdog_py),
        "--state-dir",
        str(state_dir),
        "--silence-seconds",
        "300",
        "--expect",
        id_name,
        "--notifier",
        "local_log",
        "--notifier-log",
        str(log_path),
        "--state-file",
        str(state_file),
        "--now",
        now_dt.isoformat().replace("+00:00", "Z"),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    print(f"{name}: rc={proc.returncode}")
    print(proc.stdout.rstrip())
    if proc.stderr:
        print(proc.stderr.rstrip())


emit_at(base)
run_watchdog("step1-silent", base + timedelta(seconds=301))
emit_at(base + timedelta(seconds=302))
run_watchdog("step2-ok", base + timedelta(seconds=303))
run_watchdog("step3-silent", base + timedelta(seconds=1200))

print("notifier-entries")
if log_path.exists():
    for line in log_path.read_text(encoding="utf-8").splitlines():
        print(line)
