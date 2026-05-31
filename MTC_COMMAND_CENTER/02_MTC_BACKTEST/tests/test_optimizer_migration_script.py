import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def test_migration_script_smoke(tmp_path):
    db_path = tmp_path / "migrate.db"
    cmd = [
        sys.executable,
        "scripts/migrate_optimizer_db.py",
        "--db",
        str(db_path),
    ]
    mtc_root = str(PROJECT_ROOT / "mtc_backtest")
    env = {**subprocess.os.environ, "PYTHONPATH": mtc_root}
    result = subprocess.run(
        cmd,
        cwd=mtc_root,
        capture_output=True,
        text=True,
        env=env,
    )

    assert result.returncode == 0, result.stderr
    assert "Schema version target" in result.stdout
