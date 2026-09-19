import os
import subprocess
from pathlib import Path

LANE = Path(r"C:/tmp/P026_DRILLS_TA_20260914")
_TMP = LANE / "tmp"
_TMP.mkdir(parents=True, exist_ok=True)
os.environ["TEMP"] = str(_TMP)
os.environ["TMP"] = str(_TMP)
os.environ["PYTHONUTF8"] = "1"

python = r"C:/tmp/P020_IMPL_20260912/01a0924d-2c4b-7da1-99e1-24e2a7c7685c/.venv/Scripts/python.exe"
backup_py = LANE / "wt" / "MTC_COMMAND_CENTER" / "tools" / "opsa" / "backup.py"
config = LANE / "fixtures" / "config" / "d2_store_config.json"

result = subprocess.run(
    [python, str(backup_py), "--config", str(config), "--dry-run", "--store", "p030_closed_partition"],
    cwd=str(LANE),
    check=False,
)

backup_root_d2 = LANE / "fixtures" / "backup_root_d2"
entries = sorted(p.relative_to(backup_root_d2).as_posix() for p in backup_root_d2.rglob("*") if p != backup_root_d2)
print(f"backup_root_d2_listing={entries}")
print(f"backup_root_d2_has_runs={(backup_root_d2 / 'runs').exists()}")
print(f"backup_root_d2_has_manifest={(backup_root_d2 / 'manifest.jsonl').exists()}")
raise SystemExit(result.returncode)
