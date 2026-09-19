import json
import os
import shutil
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
base = LANE / "fixtures"
base_state = base / "watchdog_state"
base_notifier = base / "watchdog_notifier"
base_state.mkdir(parents=True, exist_ok=True)
base_notifier.mkdir(parents=True, exist_ok=True)


def reset_dir(path: Path) -> Path:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_hb(path: Path, payload) -> None:
    if isinstance(payload, str):
        path.write_text(payload, encoding="utf-8")
    else:
        path.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True), encoding="utf-8")


def run_case(name, state_dir, now_ts, args_extra=None) -> None:
    log_path = base_notifier / f"{name}.jsonl"
    if log_path.exists():
        log_path.unlink()
    cmd = [
        python,
        str(watchdog_py),
        "--state-dir",
        str(state_dir),
        "--silence-seconds",
        "300",
        "--notifier",
        "local_log",
        "--notifier-log",
        str(log_path),
    ]
    if args_extra:
        cmd += args_extra
    if now_ts is not None:
        cmd += ["--now", now_ts]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    print(f"{name}: rc={proc.returncode}")
    print(f"{name}: stdout")
    if proc.stdout:
        print(proc.stdout.rstrip())
    print(f"{name}: stderr")
    if proc.stderr:
        print(proc.stderr.rstrip())
    print(f"{name}: notifier")
    if log_path.exists():
        for line in log_path.read_text(encoding="utf-8").splitlines():
            print(line)
    else:
        print(f"{name}: notifier-missing")


fresh_now = datetime(2026, 9, 14, 5, 0, 0, tzinfo=timezone.utc)
fresh_iso = (fresh_now + timedelta(seconds=10)).isoformat().replace("+00:00", "Z")
collector_id = "p030_market_data_collector"

# absent state dir
absent_dir = base_state / "absent"
if absent_dir.exists():
    shutil.rmtree(absent_dir)
run_case("absent-state-dir", absent_dir, (fresh_now + timedelta(seconds=1)).isoformat().replace("+00:00", "Z"))

# fresh ok — dedicated dir
ok_dir = reset_dir(base_state / "ok")
write_hb(
    ok_dir / f"{collector_id}.hb.json",
    {
        "schema": "mtc.opsa_heartbeat/v1",
        "id": collector_id,
        "seq": 1,
        "emitted_at": fresh_now.isoformat().replace("+00:00", "Z"),
        "pid": 111,
    },
)
run_case("fresh-ok", ok_dir, fresh_iso)

# silent — dedicated dir with only the aged beat
silent_dir = reset_dir(base_state / "silent")
write_hb(
    silent_dir / f"{collector_id}.hb.json",
    {
        "schema": "mtc.opsa_heartbeat/v1",
        "id": collector_id,
        "seq": 1,
        "emitted_at": fresh_now.isoformat().replace("+00:00", "Z"),
        "pid": 111,
    },
)
run_case("silent", silent_dir, (fresh_now + timedelta(seconds=10_000)).isoformat().replace("+00:00", "Z"))

# missing — empty dir with --expect
missing_dir = reset_dir(base_state / "missing_expect")
run_case(
    "missing",
    missing_dir,
    fresh_iso,
    ["--expect", "missing_id"],
)

# unreadable — only an unparseable file
unreadable_dir = reset_dir(base_state / "unreadable")
write_hb(unreadable_dir / "bad.hb.json", "{not-json")
run_case("unreadable", unreadable_dir, fresh_iso)

# bad timestamp — only a heartbeat missing emitted_at
bad_ts_dir = reset_dir(base_state / "bad_timestamp")
write_hb(
    bad_ts_dir / "good2.hb.json",
    {
        "schema": "mtc.opsa_heartbeat/v1",
        "id": "good2",
        "seq": 1,
        "pid": 222,
    },
)
run_case("bad-ts", bad_ts_dir, fresh_iso)

# clock skew — only a far-future stamp
skew_dir = reset_dir(base_state / "clock_skew")
future_now = datetime(2026, 9, 14, 5, 0, 0, tzinfo=timezone.utc)
write_hb(
    skew_dir / "skewed.hb.json",
    {
        "schema": "mtc.opsa_heartbeat/v1",
        "id": "skewed",
        "seq": 1,
        "emitted_at": (future_now + timedelta(seconds=900)).isoformat().replace("+00:00", "Z"),
        "pid": 333,
    },
)
run_case("clock-skew", skew_dir, future_now.isoformat().replace("+00:00", "Z"))

# empty state dir with no --expect
empty_dir = reset_dir(base_state / "empty")
run_case("empty-no-expect", empty_dir, (fresh_now + timedelta(seconds=5)).isoformat().replace("+00:00", "Z"))

# invalid --now
invalid_dir = reset_dir(base_state / "invalid_now")
run_case("invalid-now", invalid_dir, "not-a-timestamp")
