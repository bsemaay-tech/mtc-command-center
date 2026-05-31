import pytest
import json
import sys
import subprocess
from pathlib import Path
import tempfile
import os

# Ensure src can be imported
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.optimizer_v0.search import load_search_space

def test_print_space_dry_run():
    """Verify --print-space runs as a dry-run and exits without executing trials."""
    
    # Path to known config files
    case_path = PROJECT_ROOT / "mtc_backtest" / "configs" / "cases" / "full_jul2025_jan2026_parity.json"
    space_path = PROJECT_ROOT / "mtc_backtest" / "configs" / "space_example.json"
    
    if not case_path.exists() or not space_path.exists():
        pytest.skip("Config files not found, skipping dry-run test")

    cmd = [
        sys.executable, "-m", "src.optimizer_v0", "run",
        "--case", str(case_path),
        "--mode", "random",
        "--space-file", str(space_path),
        "--print-space"
    ]
    
    # Run from mtc_backtest directory to handle relative paths correctly if needed
    cwd = PROJECT_ROOT / "mtc_backtest"
    
    result = subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": str(cwd)}
    )

    assert result.returncode == 0, f"Dry run failed with stderr: {result.stderr}"
    assert "SEARCH SPACE (DRY RUN)" in result.stdout
    assert "Executing" not in result.stdout
    assert "trials" not in result.stdout

def test_load_search_space_validation():
    """Verify load_search_space raises ValueError on invalid schema."""
    
    invalid_schema = {
        "random": {
            "test_param": {
                "values": [1, 2, 3] 
                # Missing "dist"
            }
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as tmp:
        json.dump(invalid_schema, tmp)
        tmp_path = Path(tmp.name)
        
    try:
        with pytest.raises(ValueError, match="missing dist"):
            load_search_space(tmp_path)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()
